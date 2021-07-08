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
from odoo import api, models, fields


class PosVarients(models.Model):

    _inherit = ['product.template']

    pos_variants = fields.Boolean('pos variants', default=False)
    variant_line_ids = fields.One2many('variants.tree', 'variants_id', string="Configure Variants")


class VariantsSelection(models.Model):

    _name = 'variants.tree'

    variants_id = fields.Many2one('product.template')
    attribute = fields.Many2one('product.attribute', string='Attribute', ondelete='restrict', required=True, index=True)
    value = fields.Many2many('product.attribute.value', string='Values')
    extra_price = fields.Char(string="Price Extra")
    pos_active = fields.Boolean(string="Active")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_image = fields.Boolean(
        "Print Image",
        help="""If ticked, you can see the product image in
        report of sale order/quotation""",
    )
    image_sizes = fields.Selection(
        [
            ("image", "Big sized Image"),
            ("image_medium", "Medium Sized Image"),
            ("image_small", "Small Sized Image"),
        ],
        "Image Sizes",
        default="image_small",
        help="Image size to be displayed in report",
    )


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    image_small = fields.Binary("Product Image", related="product_id.image_1920")

