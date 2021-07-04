# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class res_company(models.Model):
    _inherit = "res.company"

    sh_purchase_barcode_mobile_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR code'),        
        ('all','All')
        ],default = 'barcode', string='Purchase Product Scan Options In Mobile', translate=True)

    sh_purchase_bm_is_cont_scan = fields.Boolean(string='Purchase Continuously Scan?', translate=True)
    
    sh_purchase_bm_is_notify_on_success = fields.Boolean(string='Purchase Notification On Product Succeed?', translate=True)
    
    sh_purchase_bm_is_notify_on_fail = fields.Boolean(string='Purchase Notification On Product Failed?', translate=True)
        
    sh_purchase_bm_is_sound_on_success = fields.Boolean(string='Purchase Play Sound On Product Succeed?', translate=True)
    
    sh_purchase_bm_is_sound_on_fail = fields.Boolean(string='Purchase Play Sound On Product Failed?', translate=True)
            
