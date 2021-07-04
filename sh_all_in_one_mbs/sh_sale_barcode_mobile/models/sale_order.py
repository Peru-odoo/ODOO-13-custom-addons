# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import Warning,UserError
import datetime

class sale_order(models.Model):
    _inherit = "sale.order" 
   
   
    def default_sh_sale_bm_is_cont_scan(self):
        if self.env.user and self.env.user.company_id:
            return self.env.user.company_id.sh_sale_bm_is_cont_scan
    
    sh_sale_barcode_mobile = fields.Char(string = "Mobile Barcode")
    
    sh_sale_bm_is_cont_scan = fields.Char(string='Continuously Scan?',default = default_sh_sale_bm_is_cont_scan, readonly=True)
        
 
        
    
    @api.onchange('sh_sale_barcode_mobile')
    def _onchange_sh_sale_barcode_mobile(self):
        
        if self.sh_sale_barcode_mobile in ['',"",False,None]:
            return
        
        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_sale_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"
        
        if self.env.user.company_id.sudo().sh_sale_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"
                        
        # TODO: SOUND ALERT NEED.        
        #step 1 make sure order in proper state.
        if self and self.state in ["cancel","done"]:
            selections = self.fields_get()["state"]["selection"]
            value = next((v[1] for v in selections if v[0] == self.state), self.state)

            
            if self.env.user.company_id.sudo().sh_sale_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'You can not scan item in %s state.')% (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                
            return
                         
#             raise UserError(_("You can not scan item in %s state.") %(value))
                
        #step 2 increaset product qty by 1 if product not in order line than create new order line.
        elif self:
            search_lines = False
            domain = []
            if self.env.user.company_id.sudo().sh_sale_barcode_mobile_type == "barcode":            
                search_lines = self.order_line.filtered(lambda ol: ol.product_id.barcode == self.sh_sale_barcode_mobile)
                domain = [("barcode","=",self.sh_sale_barcode_mobile)]
             
            elif self.env.user.company_id.sudo().sh_sale_barcode_mobile_type == "int_ref":            
                search_lines = self.order_line.filtered(lambda ol: ol.product_id.default_code == self.sh_sale_barcode_mobile)   
                domain = [("default_code","=",self.sh_sale_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_sale_barcode_mobile_type == "sh_qr_code":            
                search_lines = self.order_line.filtered(lambda ol: ol.product_id.sh_qr_code == self.sh_sale_barcode_mobile)   
                domain = [("sh_qr_code","=",self.sh_sale_barcode_mobile)]
                                 
            elif self.env.user.company_id.sudo().sh_sale_barcode_mobile_type == "all":            
                search_lines = self.order_line.filtered(lambda ol: ol.product_id.barcode == self.sh_sale_barcode_mobile or ol.product_id.default_code == self.sh_sale_barcode_mobile or ol.product_id.sh_qr_code == self.sh_sale_barcode_mobile)   
                domain = ["|","|",
                    ("default_code","=",self.sh_sale_barcode_mobile),
                    ("barcode","=",self.sh_sale_barcode_mobile),
                    ("sh_qr_code","=",self.sh_sale_barcode_mobile),                    
                ]                                            
            if search_lines:
                for line in search_lines:
                    line.product_uom_qty += 1
                    line.product_id_change()
                    line._onchange_discount()    

                
                
                    if self.env.user.company_id.sudo().sh_sale_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (line.product_id.name,line.product_uom_qty)
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                    break
            else:
                search_product = self.env["product.product"].search(domain, limit = 1)
                if search_product:
                    vals = {
                        'product_id': search_product.id,
                        'name': search_product.name,
                        'product_uom': search_product.uom_id.id,
                        'product_uom_qty': 1,
                        'price_unit': search_product.lst_price,
                    }
                    if search_product.uom_id:
                        vals.update({
                            "product_uom": search_product.uom_id.id,                            
                        })                      
                    new_order_line = self.order_line.new(vals)
                    self.order_line += new_order_line
                    new_order_line.product_id_change()
                    new_order_line._onchange_discount() 
                    
                    
                    
                        
                    # ==========================================================================
                    # To Apply Discount
                    # ==========================================================================
                    if (new_order_line and new_order_line.product_id and new_order_line.product_uom and
                            self.partner_id and self.pricelist_id and
                            self.pricelist_id.discount_policy == 'without_discount' and
                            self.env.user.has_group('product.group_discount_per_so_line')):
                                       
                        new_order_line.discount = 0.0
                        product = new_order_line.product_id.with_context(
                            lang=self.partner_id.lang,
                            partner=self.partner_id,
                            quantity=new_order_line.product_uom_qty,
                            date=self.date_order,
                            pricelist=self.pricelist_id.id,
                            uom=new_order_line.product_uom.id,
                            fiscal_position=self.env.context.get('fiscal_position')
                        )
                
                        product_context = dict(self.env.context, partner_id=self.partner_id.id, date=self.date_order, uom=new_order_line.product_uom.id)
                
                        price, rule_id = self.pricelist_id.with_context(product_context).get_product_price_rule(new_order_line.product_id, new_order_line.product_uom_qty or 1.0, self.partner_id)
                        new_list_price, currency = new_order_line.with_context(product_context)._get_real_price_currency(product, rule_id, new_order_line.product_uom_qty, new_order_line.product_uom, self.pricelist_id.id)
                
                        if new_list_price != 0:
                            if self.pricelist_id.currency_id != currency:
                                # we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
                                new_list_price = currency._convert(
                                    new_list_price, self.pricelist_id.currency_id,
                                    self.company_id or self.env.company, self.date_order or fields.Date.today())
                            discount = (new_list_price - price) / new_list_price * 100
                            if (discount > 0 and new_list_price > 0) or (discount < 0 and new_list_price < 0):
                                new_order_line.discount = discount
                            
                    # ==========================================================================
                    # To Apply Discount
                    # ==========================================================================                        
                        
                                              
                    
                    
                    
                    
                    
                    
                    
                    

                    if self.env.user.company_id.sudo().sh_sale_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (new_order_line.product_id.name,new_order_line.product_uom_qty)                        
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})
                                        
                 
                else:
                    if self.env.user.company_id.sudo().sh_sale_bm_is_notify_on_fail:    
                        message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')                  
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                    
                    
                                                           
#                     raise UserError(_("Scanned Internal Reference/Barcode not exist in any product!"))    



