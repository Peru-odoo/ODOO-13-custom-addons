# -*- coding: utf-8 -*-
#############################################################################
#
#   AadPlus IT Solutions.
#
#    Author: <https://www.aadplusgroup.com>)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': "POS Product Multi variant",
    'version': '13.0.1.0.1',
    'summary': """Product with multi-variants""",
    'description': """Configure products having variants in POS""",
    'author': 'AadPlus IT Solutions',
    'company': 'AadPlus IT Solutions',
    'maintainer': 'AadPlus IT Solutions',
    'website': "https://www.aadplusgroup.com",
    'category': 'Point of Sale',
    'depends': ['base',
                'point_of_sale',
                "sale_management"
                ],
    'data': ['views/pos_variants.xml',
             'security/ir.model.access.csv',
             'views/pos_wizard.xml',
             "views/sale_product_view.xml", "views/report_saleorder.xml"],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',"LGPL-3"
    'installable': True,
    'qweb': ['static/src/xml/label.xml',
             'static/src/xml/popup.xml'],
    'auto_install': False,
}
