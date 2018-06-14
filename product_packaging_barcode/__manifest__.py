# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Product Packaging Barcode',
    'description': """
        Reimplement barcode field in Product Packagings (was deleted in v9)""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://acsone.eu',
    'depends': [
        'product',
        'barcodes',
    ],
    'data': [
        'views/product_packaging.xml',
    ],
}
