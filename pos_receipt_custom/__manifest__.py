# -*- coding: utf-8 -*-
{
    'name': "POS RECEIPT CUSTOM",
    'summary': """
       Inherit default pos receipt. This module can work with PosBox or POS NETWORK PRINTER module
       """,
    'description': """
        Inherit default pos receipt. This module can work with PosBox or POS NETWORK PRINTER module
    """,
    'author': "Aimé Jules Andrinirina",
    'website': "https://www.aimejules.com",
    'license': 'AGPL-3',
    'category': 'Point Of Sale',
    'version': '2.0',
    'images': ['static/description/banner.jpg'],
    'depends': [
        'base',
        'point_of_sale',
    ],
    'data': ['views/assets.xml'],
    'qweb': ['static/src/xml/pos.xml'],
    'price': 0,
    'currency': 'EUR',
}
