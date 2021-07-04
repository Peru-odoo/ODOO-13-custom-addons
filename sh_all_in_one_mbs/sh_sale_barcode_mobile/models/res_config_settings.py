# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import api, fields, models


class res_config_settings(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_sale_barcode_mobile_type = fields.Selection([
        ('int_ref','Internal Reference'),
        ('barcode','Barcode'),
        ('sh_qr_code','QR code'),        
        ('all','All')
        ],related='company_id.sh_sale_barcode_mobile_type', string='Product Scan Options In Mobile (Sale)', translate=True,readonly = False)


    sh_sale_bm_is_cont_scan = fields.Boolean(related='company_id.sh_sale_bm_is_cont_scan', string='Continuously Scan?', translate=True,readonly = False)
    
    sh_sale_bm_is_notify_on_success = fields.Boolean(related='company_id.sh_sale_bm_is_notify_on_success',string='Notification On Product Succeed?', translate=True,readonly = False)
    
    sh_sale_bm_is_notify_on_fail = fields.Boolean(related='company_id.sh_sale_bm_is_notify_on_fail',string='Notification On Product Failed?', translate=True,readonly = False)
    
    sh_sale_bm_is_sound_on_success = fields.Boolean(related='company_id.sh_sale_bm_is_sound_on_success', string='Play Sound On Product Succeed?', translate=True, readonly = False)
    
    sh_sale_bm_is_sound_on_fail = fields.Boolean(related='company_id.sh_sale_bm_is_sound_on_fail', string='Play Sound On Product Failed?', translate=True, readonly = False)
        
