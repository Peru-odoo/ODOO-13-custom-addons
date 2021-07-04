# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class res_company(models.Model):
    _inherit = "res.company"

    sh_product_barcode_mobile_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR code'),        
        ('all','All')
        ],default = 'barcode', string='Product Scan Options In Mobile', translate=True)

    sh_product_bm_is_cont_scan = fields.Boolean(string='Product Continuously Scan?', translate=True)
    
    sh_product_bm_is_notify_on_success = fields.Boolean(string='Product Notification On Product Succeed?', translate=True)
    
    sh_product_bm_is_notify_on_fail = fields.Boolean(string='Product Notification On Product Failed?', translate=True)
        
    sh_product_bm_is_sound_on_success = fields.Boolean(string='Product Play Sound On Product Succeed?', translate=True)
    
    sh_product_bm_is_sound_on_fail = fields.Boolean(string='Product Play Sound On Product Failed?', translate=True)
            
    
    
    sh_product_bm_is_default_code = fields.Boolean(string='Show Internal Reference?', translate=True)
                
    sh_product_bm_is_lst_price = fields.Boolean(string='Show Sale Price?', translate=True)
    
    sh_product_bm_is_qty_available = fields.Boolean(string='Show Quantity On Hand?', translate=True)
    
    sh_product_bm_is_virtual_available = fields.Boolean(string='Show Forecast Quantity?', translate=True)
    
                            