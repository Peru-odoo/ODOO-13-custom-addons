# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import Warning,UserError
from io import BytesIO
import base64

try:
    import qrcode
except ImportError:
    qrcode = None

class product_template(models.Model):
    _inherit="product.template"
    
    
    sh_qr_code = fields.Char(string="QR Code",related='product_variant_ids.sh_qr_code', readonly=False) 
    sh_qr_code_img = fields.Binary(string = "QR Code Image",related='product_variant_ids.sh_qr_code_img', readonly=False)
 
    @api.model
    def create(self, vals):
        res = super(product_template, self).create(vals)
        is_create_qr_code = self.env['ir.config_parameter'].sudo().get_param('sh_product_qrcode_generator.is_sh_product_qrcode_generator_when_create')     
        if is_create_qr_code:          
            qr_sequence = self.env['ir.sequence'].next_by_code('seq.sh_product_qrcode_generator')
            if qr_sequence:    
                qr_code = qr_sequence
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_code)
                qr.make(fit=True)
         
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_code_image = base64.b64encode(temp.getvalue())
                 
                res.sh_qr_code = qr_code
                res.sh_qr_code_img = qr_code_image
        
        return res    
    
    
    
    
class product_product(models.Model):
    _inherit="product.product"
    
    
    sh_qr_code = fields.Char(string="QR Code",copy=False)
    sh_qr_code_img = fields.Binary(string = "QR Code Image",copy=False)
 
    @api.model
    def create(self, vals):
        res = super(product_product, self).create(vals)
        is_create_qr_code = self.env['ir.config_parameter'].sudo().get_param('sh_product_qrcode_generator.is_sh_product_qrcode_generator_when_create')     
        if is_create_qr_code:          
            qr_sequence = self.env['ir.sequence'].next_by_code('seq.sh_product_qrcode_generator')
            if qr_sequence:    
                qr_code = qr_sequence
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(qr_code)
                qr.make(fit=True)
         
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_code_image = base64.b64encode(temp.getvalue())
                 
                res.sh_qr_code = qr_code
                res.sh_qr_code_img = qr_code_image
        
        return res        
    
    