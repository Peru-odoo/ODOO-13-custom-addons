# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import Warning,UserError

class account_move_line(models.Model):
    _inherit = "account.move.line"
    
    sh_invoice_barcode_scanner_is_last_scanned = fields.Boolean(string = "Last Scanned?")
    
    def _get_computed_taxes_invoice_lines(self,move_id):
        self.ensure_one()
        
        tax_ids = None
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
        elif move_id.is_purchase_document(include_receipts=True):
            # In invoice.
            if self.product_id.supplier_taxes_id:
                tax_ids = self.product_id.supplier_taxes_id.filtered(lambda tax: tax.company_id == move_id.company_id)
            elif self.account_id.tax_ids:
                tax_ids = self.account_id.tax_ids
            else:
                tax_ids = self.env['account.tax']
            if not tax_ids and not self.exclude_from_invoice_tab:
                tax_ids = move_id.company_id.account_purchase_tax_id
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
    _name = "account.move"
    _inherit = ["barcodes.barcode_events_mixin", "account.move"]   
    
      
    def write(self,vals):
        res = False
        for rec in self:
            if self.env.context.get('check_move_validity') != False:
                res = super(account_move,self).with_context(check_move_validity = False).write(vals)
            else:
                res = super(account_move,self).write(vals)
        
        if not res:
            res = super(account_move,self).write(vals) 
            return res           
        
        return res
     
    @api.model_create_multi
    def create(self,vals):
        res = False        
        if self.env.context.get('check_move_validity') != False:
            res = super(account_move,self).with_context(check_move_validity = False).create(vals)
        else:
            res = super(account_move,self).create(vals)
            
        if not res:
            res = super(account_move,self).create(vals)
            return res  
                    
        return res
    
    def _add_product(self, barcode):
        #step 1 make sure order in proper state.
#         if not self.partner_id:
#             raise UserError(_("You must first select a partner!"))     
#         
        is_last_scanned = False
        sequence = 0
        warm_sound_code = ""
        
        if self.env.user.company_id.sudo().sh_invoice_barcode_scanner_last_scanned_color:  
            is_last_scanned = True          
        
        if self.env.user.company_id.sudo().sh_invoice_barcode_scanner_move_to_top:
            sequence = -1
            
        if self.env.user.company_id.sudo().sh_invoice_barcode_scanner_warn_sound:
            warm_sound_code = "SH_BARCODE_SCANNER_"    
            
        if self.env.user.company_id.sudo().sh_invoice_barcode_scanner_auto_close_popup:
            warm_sound_code += "AUTO_CLOSE_AFTER_" + str(self.env.user.company_id.sudo().sh_invoice_barcode_scanner_auto_close_popup) + "_MS&"   
                    
                      
        
        if self and self.state != "draft":
            selections = self.fields_get()["state"]["selection"]
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
            raise UserError(_(warm_sound_code + "You can not scan item in %s state.") %(value))
               
        #step 2 increaset product qty by 1 if product not in order line than create new order line.
        elif self:
            self.invoice_line_ids.with_context(check_move_validity = False).update({
                'sh_invoice_barcode_scanner_is_last_scanned': False,
                'sequence': 0,
                })               
            
            search_lines = False
            domain = []
            if self.env.user.company_id.sudo().sh_invoice_barcode_scanner_type == "barcode":            
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.barcode == barcode)
                domain = [("barcode","=",barcode)]
            
            elif self.env.user.company_id.sudo().sh_invoice_barcode_scanner_type == "int_ref":            
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.default_code == barcode)   
                domain = [("default_code","=",barcode)]
            
            elif self.env.user.company_id.sudo().sh_invoice_barcode_scanner_type == "sh_qr_code":            
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.sh_qr_code == barcode)   
                domain = [("sh_qr_code","=",barcode)]
                
            elif self.env.user.company_id.sudo().sh_invoice_barcode_scanner_type == "all":            
                search_lines = self.invoice_line_ids.filtered(lambda ol: ol.product_id.barcode == barcode or 
                                                              ol.product_id.default_code == barcode or
                                                              ol.product_id.sh_qr_code == barcode
                                                              )   

                domain = ["|","|",
                          
                    ("default_code","=",barcode),
                    ("barcode","=",barcode),
                    ("sh_qr_code","=",barcode)
                    
                ]  
                                          
            #Write
            if search_lines:
                for line in search_lines:
                    
                    line.quantity += 1
                    line.sh_invoice_barcode_scanner_is_last_scanned = is_last_scanned
                    line.sequence = sequence
                    line._onchange_product_id()
                    line._onchange_price_subtotal()
                self._compute_invoice_taxes_by_group()
                self._onchange_invoice_line_ids()
                self._compute_amount()
                self._recompute_dynamic_lines(recompute_all_taxes=True)
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
                            raise UserError(
                                _(warm_sound_code + 'There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %
                                (search_product.name,))   
                             
                    if self.type in ['in_invoice','in_refund']:
                        account_id = search_product.property_account_expense_id.id or search_product.categ_id.property_account_expense_categ_id.id
                        if not account_id:
                            inc_acc = ir_property_obj.get('property_account_expense_categ_id', 'product.category')
                            account_id = self.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
                        if not account_id:
                            raise UserError(
                                _(warm_sound_code + 'There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %
                                (search_product.name,))                              
                                                                                   
                     
                    
                    invoice_line_val = {
                       "name": search_product.name,
                       "product_id": search_product.id,
                       "quantity": 1,
#                        "price_unit": search_product.standard_price,
                       'account_id':account_id,
                       'sh_invoice_barcode_scanner_is_last_scanned':is_last_scanned,
                       'sequence':sequence,
                       
                    }
                    
                    
                    if self.type in ['out_invoice','out_refund']:
                        invoice_line_val.update({
                            "price_unit" : search_product.lst_price
                            })
                    
                    elif self.type in ['in_invoice','in_refund']:
                        invoice_line_val.update({
                            "price_unit" : search_product.standard_price
                            })                    
                    
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
                    self.update(
                            {'invoice_line_ids': [(0, 0, invoice_line_val)]})
                    
                    for rec in self.invoice_line_ids:
                        rec._onchange_product_id()
                        rec._onchange_price_subtotal()
                        
                    self._compute_invoice_taxes_by_group()
                    self._onchange_invoice_line_ids()
                    self._compute_amount()
                    self._recompute_dynamic_lines(recompute_all_taxes=True)
                    
                else:
                    raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))           
    
    def on_barcode_scanned(self, barcode):
        self._add_product(barcode)
          
                
                