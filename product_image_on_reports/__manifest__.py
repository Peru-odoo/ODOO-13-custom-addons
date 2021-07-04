# -*- coding: utf-8 -*-

{
    'name': 'Product Image on Reports',
    'version': '13.0.1.0.0',
    'category': 'Extra Tools',
    'license': 'AGPL-3',
    'summary': '''This module shows image of product on reports such as sales, invoice and purchase''',
    'author': 'Aktiv Software',
    'depends': [
        'sale_management', 'purchase'
    ],
    'website': 'www.aktivsoftware.com',
    'data': [
        'views/report_invoice.xml',
        'views/sale_report_template.xml',
        'views/purchase_order_templates.xml'

    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'installable': True,
    'auto_install': False,
}
