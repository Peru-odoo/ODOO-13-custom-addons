# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import Warning,UserError


class account_move_line(models.Model):
    _inherit = "account.move.line"
    
    
    def _get_computed_taxes_invoice_lines(self,move_id):
        self.ensure_one()
        if move_id.is_sale_document(include_receipts=True):
            # Out invoice.
            if self.product_id.taxes_id:
                tax_ids = self.product_id.taxes_id.filtered(lambda tax: tax.company_id == move_id.company_id)
            elif self.account_id.tax_ids:
                tax_ids = self.account_id.tax_ids
            else:
                tax_ids = self.env['account.tax']
            if not tax_ids and not self.exclude_from_invoice_tab:
                tax_ids = move_id.company_id.account_sale_tax_id
        elif move_id.is_invoice_document(include_receipts=True):
            # In invoice.
            if self.product_id.supplier_taxes_id:
                tax_ids = self.product_id.supplier_taxes_id.filtered(lambda tax: tax.company_id == move_id.company_id)
            elif self.account_id.tax_ids:
                tax_ids = self.account_id.tax_ids
            else:
                tax_ids = self.env['account.tax']
            if not tax_ids and not self.exclude_from_invoice_tab:
                tax_ids = move_id.company_id.account_invoice_tax_id
        else:
            # Miscellaneous operation.
            tax_ids = self.account_id.tax_ids

        if self.company_id and tax_ids:
            tax_ids = tax_ids.filtered(lambda tax: tax.company_id == self.company_id)

        fiscal_position = move_id.fiscal_position_id
        if tax_ids and fiscal_position:
            return fiscal_position.map_tax(tax_ids, partner=self.partner_id)
        else:
            return tax_ids


class account_move(models.Model):
    _inherit = "account.move"
    

    def default_sh_invoice_bm_is_cont_scan(self):
        if self.env.user and self.env.user.company_id:
            return self.env.user.company_id.sh_invoice_bm_is_cont_scan
    
    sh_invoice_barcode_mobile = fields.Char(string = "Mobile Barcode")
    
    sh_invoice_bm_is_cont_scan = fields.Char(string='Continuously Scan?',default = default_sh_invoice_bm_is_cont_scan, readonly=True)
        
 
    

    
    def write(self,vals):
        if self.env.context.get('check_move_validity') != False:
            res = super(account_move,self).with_context(check_move_validity = False).write(vals)
        else:
            res = super(account_move,self).write(vals)
        return res
     
    @api.model_create_multi
    def create(self,vals):
        if self.env.context.get('check_move_validity') != False:
            res = super(account_move,self).with_context(check_move_validity = False).create(vals)
        else:
            res = super(account_move,self).create(vals)
        return res
    
    
    
        
    
    @api.onchange('sh_invoice_barcode_mobile')
    def _onchange_sh_invoice_barcode_mobile(self):
        
        if self.sh_invoice_barcode_mobile in ['',"",False,None]:
            return
        
        
        CODE_SOUND_SUCCESS = ""
        CODE_SOUND_FAIL = ""
        if self.env.user.company_id.sudo().sh_invoice_bm_is_sound_on_success:
            CODE_SOUND_SUCCESS = "SH_BARCODE_MOBILE_SUCCESS_"
        
        if self.env.user.company_id.sudo().sh_invoice_bm_is_sound_on_fail:
            CODE_SOUND_FAIL = "SH_BARCODE_MOBILE_FAIL_"
                        
                                
                
        #step 1 make sure order in proper state.
        if not self.partner_id:
            if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'You must first select a partner!')
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                
            return        
        
        
                          
        
        if self and self.state != "draft":
            selections = self.fields_get()["state"]["selection"]
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
        
            if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:
                message = _(CODE_SOUND_FAIL + 'You can not scan item in %s state.')% (value)
                self.env['bus.bus'].sendone(
                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                
            return
                
               
        #step 2 increaset product qty by 1 if product not in order line than create new order line.
        elif self:
            search_lines = False
            domain = []
            if self.env.user.company_id.sudo().sh_invoice_barcode_mobile_type == "barcode":            
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.barcode == self.sh_invoice_barcode_mobile)
                domain = [("barcode","=",self.sh_invoice_barcode_mobile)]
            
            elif self.env.user.company_id.sudo().sh_invoice_barcode_mobile_type == "int_ref":            
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.default_code == self.sh_invoice_barcode_mobile)   
                domain = [("default_code","=",self.sh_invoice_barcode_mobile)]

            elif self.env.user.company_id.sudo().sh_invoice_barcode_mobile_type == "sh_qr_code":            
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.sh_qr_code == self.sh_invoice_barcode_mobile)   
                domain = [("sh_qr_code","=",self.sh_invoice_barcode_mobile)]
                                
            elif self.env.user.company_id.sudo().sh_invoice_barcode_mobile_type == "all":            
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.barcode == self.sh_invoice_barcode_mobile 
                                                              or ol.product_id.default_code == self.sh_invoice_barcode_mobile
                                                              or ol.product_id.sh_qr_code == self.sh_invoice_barcode_mobile)   
                domain = ["|","|",
                    ("default_code","=",self.sh_invoice_barcode_mobile),
                    ("barcode","=",self.sh_invoice_barcode_mobile),
                    ("sh_qr_code","=",self.sh_invoice_barcode_mobile)
                                        
                ]                                            


            if search_lines:
                for line in search_lines:
                    line.quantity += 1
                    line._onchange_product_id()
                    
                    if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_success:
                        message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (line.product_id.name,line.quantity)                        
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})                    

                    break
            else:
                search_product = self.env["product.product"].search(domain, limit = 1)
                if search_product:
                      
                    ir_property_obj = self.env['ir.property']
                    account_id = False  
                     
                    if self.type in ['out_invoice','out_refund']:
                        account_id = search_product.property_account_income_id.id or search_product.categ_id.property_account_income_categ_id.id
                        if not account_id:
                            inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
                            account_id = self.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
                        if not account_id:
                            
                            if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:
                                message = _('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %(search_product.name)                                
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                                
                            return                            
                            
                              
                             
                    if self.type in ['in_invoice','in_refund']:
                        account_id = search_product.property_account_expense_id.id or search_product.categ_id.property_account_expense_categ_id.id
                        if not account_id:
                            inc_acc = ir_property_obj.get('property_account_expense_categ_id', 'product.category')
                            account_id = self.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
                        if not account_id:
                                                       
                            if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:
                                message = _('There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %(search_product.name)                                
                                self.env['bus.bus'].sendone(
                                    (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                    {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})
                                
                            return 
                                                                                                         
                     
                    
                    invoice_line_val = {
                       "name": search_product.name,
                       "product_id": search_product.id,
                       "quantity": 1,
                       "price_unit": search_product.standard_price,
                       'account_id':account_id,
                       
                    }
                    if self._origin.id:
                        invoice_line_val.update({'move_id':self._origin.id})
                        
                    if self.type in ['out_invoice','out_refund']:
                        if search_product.taxes_id:
                            invoice_line_val.update({'tax_ids':[(6,0,search_product.taxes_id.filtered(lambda tax: tax.company_id == self.company_id).ids)]})
                    elif self.type in ['in_invoice','in_refund']:
                        if search_product.supplier_taxes_id:
                            invoice_line_val.update({'tax_ids':[(6,0,search_product.supplier_taxes_id.filtered(lambda tax: tax.company_id == self.company_id).ids)]})
#                      
                    if search_product.uom_id:
                        invoice_line_val.update({
                            "product_uom_id": search_product.uom_id.id,                            
                        })    
                    #create
                    if self._origin.id:
                        self.update({'invoice_line_ids':[(0,0,invoice_line_val)]})
                        
                        if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (search_product.name, 1)                        
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})  
                                                
                        
                    else:
                        new_order_line = self.invoice_line_ids.with_context(check_move_validity = False).new(invoice_line_val)
                        self.invoice_line_ids += new_order_line
                        new_order_line.tax_ids = new_order_line._get_computed_taxes_invoice_lines(self)
                        
                        if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_success:
                            message = _(CODE_SOUND_SUCCESS + 'Product: %s Qty: %s') % (new_order_line.product_id.name,new_order_line.quantity)                        
                            self.env['bus.bus'].sendone(
                                (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                                {'type': 'simple_notification', 'title': _('Succeed'), 'message': message, 'sticky': False, 'warning': False})                         
                        
                        
                    
                else:                           
                    if self.env.user.company_id.sudo().sh_invoice_bm_is_notify_on_fail:    
                        message = _(CODE_SOUND_FAIL + 'Scanned Internal Reference/Barcode not exist in any product!')                  
                        self.env['bus.bus'].sendone(
                            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
                            {'type': 'simple_notification', 'title': _('Failed'), 'message': message, 'sticky': False, 'warning': True})    

                