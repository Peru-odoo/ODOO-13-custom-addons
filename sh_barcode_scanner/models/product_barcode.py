# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.
from odoo import models,fields,api,_
from odoo.osv import expression

class ShProductTemplate(models.Model):
    _inherit='product.template'
    
    barcode_line_ids = fields.One2many('product.template.barcode','template_id','Barcode Lines')

class ShProduct(models.Model):
    _inherit='product.product'
    
    barcode_line_ids = fields.One2many('product.template.barcode','product_id','Barcode Lines')
    
#     display_name= fields.Char("Display Name",store=True)
#     
#     @api.model
#     def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
#         res = super(ShProduct, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
#         mutli_barcode_search = self._search([('barcode_line_ids.name', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
#         multi_barcode_res=[]
#         if mutli_barcode_search:
#             multi_barcode_res = self.browse(mutli_barcode_search).name_get()
#         return res + multi_barcode_res
#     
#     
class ShProductBarcode(models.Model):
    _name='product.template.barcode'
    _description="Product Barcode"
    
    template_id = fields.Many2one('product.template','Product Template')
    product_id = fields.Many2one('product.product','Product')
    name = fields.Char("Barcode",required=True)