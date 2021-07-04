# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    "name": "Manage POS and Sales Orders",
    'summary': "Manage POS and Sales orders from Point of Sale.",
    "version": "1.0.8",
    "description": """
        Manage POS and Sales order from Point of Sale with Extended Features.
    """,
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'Point of Sale',
    'website': 'http://www.acespritech.com',
    'price': 99.00,
    'currency': 'EUR',
    'images': ['static/description/main_screenshot.png'],
    "depends": ['sale_management', 'point_of_sale'],
    "data": [
        'views/aspl_pos_create_so_extension.xml',
        'views/point_of_sale.xml',
    ],
    'qweb': ['static/src/xml/pos.xml', ],
    "auto_install": False,
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
