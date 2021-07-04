# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class res_company(models.Model):
    _inherit = "res.company"

    sh_sale_barcode_mobile_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR code'),        
        ('all','All')
        ],default = 'barcode', string='Product Scan Options In Mobile (Sale)', translate=True)

    sh_sale_bm_is_cont_scan = fields.Boolean(string='Continuously Scan?', translate=True)
    
    sh_sale_bm_is_notify_on_success = fields.Boolean(string='Notification On Product Succeed?', translate=True)
    
    sh_sale_bm_is_notify_on_fail = fields.Boolean(string='Notification On Product Failed?', translate=True)
        
    sh_sale_bm_is_sound_on_success = fields.Boolean(string='Play Sound On Product Succeed?', translate=True)
    
    sh_sale_bm_is_sound_on_fail = fields.Boolean(string='Play Sound On Product Failed?', translate=True)
            
            