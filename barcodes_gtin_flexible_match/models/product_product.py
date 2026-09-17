# Copyright 2026 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models

from ..tools.barcodes_gtin import get_gtin_variants


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _expand_barcode_domain_term(self, domain_term):
        """Helper to transform barcode equality domains to 'in' queries with GTIN variants."""
        if not (isinstance(domain_term, (list, tuple)) and len(domain_term) == 3):
            return domain_term

        field, operator, value = domain_term
        if field != "barcode":
            return domain_term

        if operator == "=" and isinstance(value, str):
            variants = get_gtin_variants(value)
            if variants:
                return ("barcode", "in", variants)

        elif operator in ("in", "=in") and isinstance(value, (list, tuple, set)):
            expanded_values = set()
            for val in value:
                if isinstance(val, str):
                    variants = get_gtin_variants(val)
                    expanded_values.update(variants or [val])
                else:
                    expanded_values.add(val)
            return ("barcode", "in", list(expanded_values))

        return domain_term

    @api.model
    def _search(
        self,
        args,
        offset=0,
        limit=None,
        order=None,
        count=False,
        access_rights_uid=None,
    ):
        """Intercept domain queries on 'barcode' to convert '=' into 'in' with GTIN variants."""
        if self.env.company.barcode_flexible_gtin_match:
            args = [self._expand_barcode_domain_term(arg) for arg in args]

        return super()._search(
            args,
            offset=offset,
            limit=limit,
            order=order,
            count=count,
            access_rights_uid=access_rights_uid,
        )
