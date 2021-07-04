# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError




class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"
    
    sequence = fields.Integer(string='Sequence', default=0)
    sh_inven_adjt_barcode_scanner_is_last_scanned = fields.Boolean(string = "Last Scanned?")  
    
class StockInventory(models.Model):
    _name = "stock.inventory"
    _inherit = ['barcodes.barcode_events_mixin', 'stock.inventory']
    
  
   
   
    def sh_barcode_scanner_get_inventory_lines_values(self,product_id):
        # TDE CLEANME: is sql really necessary ? I don't think so
        locations = self.env['stock.location']
        if self.location_ids:
            locations = self.env['stock.location'].search([('id', 'child_of', self.location_ids.ids)])
        else:
            locations = self.env['stock.location'].search([('company_id', '=', self.company_id.id), ('usage', 'in', ['internal', 'transit'])])
        domain = ' sq.location_id in %s AND sq.quantity != 0 AND pp.active'
        args = (tuple(locations.ids),)

        vals = []
        Product = self.env['product.product']
        # Empty recordset of products available in stock_quants
        quant_products = self.env['product.product']

        # If inventory by company
        if self.company_id:
            domain += ' AND sq.company_id = %s'
            args += (self.company_id.id,)
        
        # ==============================
        # softhealer custom code        
        
        if product_id:
            domain += ' AND sq.product_id in %s'
            args += (tuple(  [product_id] ),)

        # ==============================
        # softhealer custom code
            
            

        self.env['stock.quant'].flush(['company_id', 'product_id', 'quantity', 'location_id', 'lot_id', 'package_id', 'owner_id'])
        self.env['product.product'].flush(['active'])
        self.env.cr.execute("""SELECT sq.product_id, sum(sq.quantity) as product_qty, sq.location_id, sq.lot_id as prod_lot_id, sq.package_id, sq.owner_id as partner_id
            FROM stock_quant sq
            LEFT JOIN product_product pp
            ON pp.id = sq.product_id
            WHERE %s
            GROUP BY sq.product_id, sq.location_id, sq.lot_id, sq.package_id, sq.owner_id """ % domain, args)

        for product_data in self.env.cr.dictfetchall():
            product_data['company_id'] = self.company_id.id
            product_data['inventory_id'] = self.id
            
            
            # ==============================
            # softhealer custom code
            product_data['sh_inven_adjt_barcode_scanner_is_last_scanned'] = True
            product_data['sequence'] = -1
            # ==============================
            # softhealer custom code
            
                                                
            # replace the None the dictionary by False, because falsy values are tested later on
            for void_field in [item[0] for item in product_data.items() if item[1] is None]:
                product_data[void_field] = False
            product_data['theoretical_qty'] = product_data['product_qty']
            if self.prefill_counted_quantity == 'zero':
                product_data['product_qty'] = 0
            if product_data['product_id']:
                product_data['product_uom_id'] = Product.browse(product_data['product_id']).uom_id.id
                quant_products |= Product.browse(product_data['product_id'])
            vals.append(product_data)
        return vals   
   
   
   
   
   
      
   
   
   
   
   
   
   
   
   
   
   
    def action_start_sh_inventory_adjust_barcode_scanning(self):
        self.ensure_one()
        action_tree = self.action_start()  
        action = {
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('stock.view_inventory_form').id, 'form')],
            'view_mode': 'form',
            'res_id':self.id,
            'name': _(self.name or 'Inventory'),
            'res_model': 'stock.inventory',
            'target':'current',
        }
        action['context'] = action_tree.get('context',{})
        action['domain'] = action_tree.get('domain',[])
        return action          
    
          
    def _add_product(self, barcode):
        
        domain = []
                
        is_last_scanned = False
        sequence = 0
        warm_sound_code = ""
        
        if self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_last_scanned_color:  
            is_last_scanned = True          
        
        if self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_move_to_top:
            sequence = -1
            
        if self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_warn_sound:
            warm_sound_code = "SH_BARCODE_SCANNER_"     
                    
        if self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_auto_close_popup:
            warm_sound_code += "AUTO_CLOSE_AFTER_" + str(self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_auto_close_popup) + "_MS&"   

        
        
        #step 1: state validation.
        if self and self.state != 'confirm':
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
            raise UserError(_("You can not scan item in %s state.") %(value))
        
        elif self:
                
            self.line_ids.update({
                'sh_inven_adjt_barcode_scanner_is_last_scanned': False,
                'sequence': 0,
                })             
            
            
            search_lines = False
                        
            if self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_type == 'barcode':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.barcode == barcode)
                domain = [("barcode","=", barcode)]            
            
            
            elif self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_type == 'int_ref':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.default_code == barcode)
                domain = [("default_code","=",barcode)]
                                

            elif self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_type == 'sh_qr_code':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.sh_qr_code == barcode)
                domain = [("sh_qr_code","=",barcode)]                   
                
            
            elif self.env.user.company_id.sudo().sh_inven_adjt_barcode_scanner_type == 'all':
                search_lines = self.line_ids.filtered(lambda l: l.product_id.barcode == barcode or 
                                                      l.product_id.default_code == barcode or
                                                      l.product_id.sh_qr_code == barcode,                                                      
                                                      )
                
                domain = ["|","|",
                    ("default_code","=", barcode),
                    ("barcode","=", barcode),
                    ("sh_qr_code","=", barcode),                    
                ]  
                                
                   
            if search_lines:
                for line in search_lines:
                    line.product_qty += 1
                    line.sh_inven_adjt_barcode_scanner_is_last_scanned = is_last_scanned,
                    line.sequence = sequence
                    break
            else:
                # =========================================
                # Create Inventory Line Here
                domain += [
                    ('type','=','product')
                ]
                
                product = self.env['product.product'].search(domain,limit = 1)
                       
                if product:
                    lines_vals = self.sh_barcode_scanner_get_inventory_lines_values(product.id)
                    
                    # add sequence and last scanned here
                    if len(lines_vals) == 1:
                        lines_vals[0].update({
                            "product_qty": 1
                            })
                    
                    if not lines_vals:                        
                        if self.location_ids:
                            lines_vals = [{
                            
                                'product_id': product.id, 
                                'product_qty': 1, 
                                'location_id': self.location_ids[0].ids[0], 
                                'prod_lot_id': False, 
                                'package_id': False, 
                                'partner_id': False, 
                                'inventory_id':self.id,
                                'sh_inven_adjt_barcode_scanner_is_last_scanned': True, 
                                'sequence': -1, 
                                'product_uom_id': product.uom_id.id if product.uom_id else False,
                            
                            }]
                        else:
                            raise UserError(_(warm_sound_code + "Please specify at least one location in inventory"))                               

                    self.env['stock.inventory.line'].create( lines_vals )    
                    
                    
                else:                  
                    raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))      
            
    def on_barcode_scanned(self, barcode):  
        self._add_product(barcode)  











class stock_scrap(models.Model):
    _name = "stock.scrap"
    _inherit = ['barcodes.barcode_events_mixin', 'stock.scrap']
    
    
    def on_barcode_scanned(self, barcode):            
        
        warm_sound_code = ""
#         if self.env.user.company_id.sudo().sh_scrap_barcode_scanner_warn_sound:
#             warm_sound_code = "SH_BARCODE_SCANNER_"           
#                
#         if self.env.user.company_id.sudo().sh_scrap_barcode_scanner_auto_close_popup:
#             warm_sound_code += "AUTO_CLOSE_AFTER_" + str(self.env.user.company_id.sudo().sh_scrap_barcode_scanner_auto_close_popup) + "_MS&"   
#         
#         
        #step 1: state validation.
        if self and self.state != 'draft':
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
            warning_mess = {
                'title': _('Error!'),
                'message' : (warm_sound_code + 'You can not scan item in %s state.') %(value)
            }
            return {'warning': warning_mess}
        
        elif self.product_id:
            
            if self.env.user.company_id.sudo().sh_scrap_barcode_scanner_type == 'barcode':
                if self.product_id.barcode == barcode:
                    self.scrap_qty += 1
                else:
                    warning_mess = {
                        "title": _("Error!"),
                        "message" : (warm_sound_code + "You can not change product after scan started. If you want to scan new product than pls create new scrap.")
                    }
                    return {"warning": warning_mess}                    
            
            elif self.env.user.company_id.sudo().sh_scrap_barcode_scanner_type == 'int_ref':
                if self.product_id.default_code == barcode:
                    self.scrap_qty += 1
                else:
                    warning_mess = {
                        "title": _("Error!"),
                        "message" : (warm_sound_code + "You can not change product after scan started. If you want to scan new product than pls create new scrap.")
                    }
                    return {"warning": warning_mess}                      
            
            elif self.env.user.company_id.sudo().sh_scrap_barcode_scanner_type == 'sh_qr_code':
                if self.product_id.sh_qr_code == barcode:
                    self.scrap_qty += 1
                else:
                    warning_mess = {
                        "title": _("Error!"),
                        "message" : (warm_sound_code + "You can not change product after scan started. If you want to scan new product than pls create new scrap.")
                    }
                    return {"warning": warning_mess}   
            
            
            elif self.env.user.company_id.sudo().sh_scrap_barcode_scanner_type == 'all':
                if self.product_id.barcode == barcode or self.product_id.default_code == barcode or self.product_id.sh_qr_code == barcode:
                    self.scrap_qty += 1
                else:
                    warning_mess = {
                        "title": _("Error!"),
                        "message" : (warm_sound_code + "You can not change product after scan started. If you want to scan new product than pls create new scrap.")
                    }
                    return {"warning": warning_mess}  
        else:
            domain = []
            
            if self.env.user.company_id.sudo().sh_scrap_barcode_scanner_type == 'barcode':
                domain = [("barcode","=",barcode)]
            
            elif self.env.user.company_id.sudo().sh_scrap_barcode_scanner_type == 'int_ref':
                domain = [("default_code","=",barcode)]
            
            elif self.env.user.company_id.sudo().sh_scrap_barcode_scanner_type == 'sh_qr_code':
                domain = [("sh_qr_code","=",barcode)]
            
            elif self.env.user.company_id.sudo().sh_scrap_barcode_scanner_type == 'all':
                domain = ["|","|",
                          
                    ("default_code","=",barcode),
                    ("barcode","=",barcode),
                    ("sh_qr_code","=",barcode)
                    
                ]  
                
            
            search_product = self.env["product.product"].search(domain, limit = 1)
            
            if search_product:                    
                self.product_id = search_product.id
                

            else:
                warning_mess = {
                    "title": _("Error!"),
                    "message" : (warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!")
                }
                return {"warning": warning_mess} 














class stock_move(models.Model):
    _name = "stock.move"
    _inherit = ['barcodes.barcode_events_mixin', 'stock.move']

    sequence = fields.Integer(string='Sequence', default=0)
    sh_inventory_barcode_scanner_is_last_scanned = fields.Boolean(string = "Last Scanned?")
        
            
    def on_barcode_scanned(self, barcode):
        
                        
        is_last_scanned = False
        sequence = 0
        warm_sound_code = ""
        
        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_last_scanned_color:  
            is_last_scanned = True          
        
        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_move_to_top:
            sequence = -1
            
        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_warn_sound:
            warm_sound_code = "SH_BARCODE_SCANNER_"       
            
        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_auto_close_popup:
            warm_sound_code += "AUTO_CLOSE_AFTER_" + str(self.env.user.company_id.sudo().sh_inventory_barcode_scanner_auto_close_popup) + "_MS&"   

        

        # =============================           
        # UPDATED CODE
        move_lines = False
        
        # INCOMING
        # ===================================
        if self.picking_code in ['incoming']:
            move_lines = self.move_line_nosuggest_ids

        # OUTGOING AND TRANSFER
        # ===================================         
        elif self.picking_code in ['outgoing','internal']:
            move_lines = self.move_line_ids    
                        
        
        # UPDATED CODE
        # =============================    
                
        
        if self.picking_id.state not in ['confirmed','assigned']:
            selections = self.picking_id.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] == self.picking_id.state), self.picking_id.state)
            raise UserError(_(warm_sound_code + "You can not scan item in %s state.") %(value))
        
 
        elif move_lines:

            
            
            for line in move_lines:
                if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'barcode':
                    if self.product_id.barcode == barcode:
                        similar_lines = move_lines.filtered(lambda ml: ml.product_id.barcode == barcode)
                        len_similar_lines = len(similar_lines)

                        if len_similar_lines:
                            last_line = similar_lines[len_similar_lines - 1]
                            last_line.qty_done += 1


                        
                        self.sequence = sequence
                        self.sh_inventory_barcode_scanner_is_last_scanned = is_last_scanned
                        
                        if self.quantity_done == self.product_uom_qty + 1:                      
                            warning_mess = {
                                    'title': _('Alert!'),
                                    'message' : warm_sound_code + 'Becareful! Quantity exceed than initial demand!'
                                }
                            return {'warning': warning_mess}                                  
                        break
                    else:
                        raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))                            
                    
                elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'int_ref':
                    if self.product_id.default_code == barcode:
                        similar_lines = move_lines.filtered(
                            lambda ml: ml.product_id.default_code == barcode)
                        len_similar_lines = len(similar_lines)

                        if len_similar_lines:
                            last_line = similar_lines[len_similar_lines - 1]
                            last_line.qty_done += 1
                                                    
                        self.sequence = sequence
                        self.sh_inventory_barcode_scanner_is_last_scanned = is_last_scanned
                                                
                        
                        if self.quantity_done == self.product_uom_qty + 1:                      
                            warning_mess = {
                                    'title': _('Alert!'),
                                    'message' : warm_sound_code + 'Becareful! Quantity exceed than initial demand!'
                                }
                            return {'warning': warning_mess}                                   
                        break
                    else:
                        raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))                             
                                        
                    
                    
                    
                    
                elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'sh_qr_code':
                    if self.product_id.sh_qr_code == barcode:
                        similar_lines = move_lines.filtered(
                            lambda ml: ml.product_id.sh_qr_code == barcode)
                        len_similar_lines = len(similar_lines)

                        if len_similar_lines:
                            last_line = similar_lines[len_similar_lines - 1]
                            last_line.qty_done += 1
                                                    
                        
                        self.sequence = sequence
                        self.sh_inventory_barcode_scanner_is_last_scanned = is_last_scanned
                                                
                        
                        if self.quantity_done == self.product_uom_qty + 1:                      
                            warning_mess = {
                                    'title': _('Alert!'),
                                    'message' : warm_sound_code + 'Becareful! Quantity exceed than initial demand!'
                                }
                            return {'warning': warning_mess}                                   
                        break
                    else:
                        raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))                        
                    
                    
                    
                elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'all':
                    if self.product_id.barcode == barcode or self.product_id.default_code == barcode or self.product_id.sh_qr_code == barcode:                       
                        similar_lines = move_lines.filtered(
                            lambda ml: ml.product_id.barcode == barcode or ml.product_id.default_code == barcode or ml.product_id.sh_qr_code == barcode)
                        len_similar_lines = len(similar_lines)

                        if len_similar_lines:
                            last_line = similar_lines[len_similar_lines - 1]
                            last_line.qty_done += 1
                                                    
                        
                        self.sequence = sequence
                        self.sh_inventory_barcode_scanner_is_last_scanned = is_last_scanned
                                                
                        if self.quantity_done == self.product_uom_qty + 1:                    
                            warning_mess = {
                                    'title': _('Alert!'),
                                    'message' :warm_sound_code + 'Becareful! Quantity exceed than initial demand!'
                                }
                            return {'warning': warning_mess}                                  
                        break
                    else:
                        raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))                              
                
        else:
            raise UserError(_(warm_sound_code + "Pls add all product items in line than rescan."))
        
        
    
    
            
class stock_picking(models.Model):
    _name = "stock.picking"
    _inherit = ['barcodes.barcode_events_mixin', 'stock.picking']   
    
      
            
    def on_barcode_scanned(self, barcode):
        
        is_last_scanned = False
        sequence = 0
        warm_sound_code = ""
        
        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_last_scanned_color:  
            is_last_scanned = True          
        
        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_move_to_top:
            sequence = -1
            
        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_warn_sound:
            warm_sound_code = "SH_BARCODE_SCANNER_"
            
        if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_auto_close_popup:
            warm_sound_code += "AUTO_CLOSE_AFTER_" + str(self.env.user.company_id.sudo().sh_inventory_barcode_scanner_auto_close_popup) + "_MS&"   

            
                    
        
        if self and self.state not in ['assigned','draft','confirmed']:
            selections = self.fields_get()['state']['selection']
            value = next((v[1] for v in selections if v[0] == self.state), self.state)
            raise UserError(_(warm_sound_code + "You can not scan item in %s state.") %(value))                
            
        
        elif self:
            
            
            self.move_ids_without_package.update({
                'sh_inventory_barcode_scanner_is_last_scanned': False,
                'sequence': 0,
                }) 
                        
            
            search_mls = False
            domain = []
            
            if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'barcode':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.barcode == barcode)
                domain = [("barcode","=",barcode)]
            
            elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'int_ref':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.default_code == barcode)
                domain = [("default_code","=",barcode)]                
                
            elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'sh_qr_code':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.sh_qr_code == barcode)
                domain = [("sh_qr_code","=",barcode)]    
            
            elif self.env.user.company_id.sudo().sh_inventory_barcode_scanner_type == 'all':
                search_mls = self.move_ids_without_package.filtered(lambda ml: ml.product_id.barcode == barcode or 
                                                                    ml.product_id.default_code == barcode or
                                                                    ml.product_id.sh_qr_code == barcode                                                                    
                                                                    )
                domain = ["|","|",
                          
                    ("default_code","=",barcode),
                    ("barcode","=",barcode),
                    ("sh_qr_code","=",barcode)
                    
                ]  
                                                
                                            
            if search_mls:
                for move_line in search_mls:
                    
                    if move_line.show_details_visible:
                        raise UserError(_(warm_sound_code + "You can not scan product item for Detailed Operations directly here, Pls click detail button (at end each line) and than rescan your product item."))                                       
                                      
                    if self.state == 'draft':
                        move_line.product_uom_qty += 1
                        move_line.sh_inventory_barcode_scanner_is_last_scanned = is_last_scanned
                        move_line.sequence = sequence                              
                        
                    else:
                        move_line.quantity_done = move_line.quantity_done + 1
                        move_line.sh_inventory_barcode_scanner_is_last_scanned = is_last_scanned
                        move_line.sequence = sequence                        
    #                     move_line.update({'quantity_done':move_line.quantity_done + 1})
                                                                    
                        if move_line.quantity_done == move_line.product_uom_qty + 1:                    
                            warning_mess = {
                                    'title': _('Alert!'),
                                    'message' :warm_sound_code + 'Becareful! Quantity exceed than initial demand!'
                                }
                            return {'warning': warning_mess} 
                    
                    break
                                    
            elif self.state == 'draft':
                if self.env.user.company_id.sudo().sh_inventory_barcode_scanner_is_add_product:
                    if not self.picking_type_id:
                        raise UserError(_(warm_sound_code + "You must first select a Operation Type."))                        
                        
                    search_product = self.env["product.product"].search(domain, limit = 1)
                    if search_product:                                         
                         
                        order_line_val = {
                           "name": search_product.name,
                           "product_id": search_product.id,
                            "product_uom_qty": 1,
                           "price_unit": search_product.lst_price,
#                            "quantity_done" : 1,
                           "location_id" : self.location_id.id,
                           "location_dest_id": self.location_dest_id.id,
                           'date_expected' : str(fields.date.today()),
                           'sh_inventory_barcode_scanner_is_last_scanned':is_last_scanned,
                           'sequence':sequence,
                           
                        }      
                        if search_product.uom_id:
                            order_line_val.update({
                                "product_uom": search_product.uom_id.id,                            
                            })    
                            
                        old_lines = self.move_ids_without_package
                        new_order_line = self.move_ids_without_package.create(order_line_val)
                        self.move_ids_without_package = old_lines + new_order_line
                        new_order_line.onchange_product_id()                          
                                            
                    else: 
                        raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))                                          
                                           
                else:
                    raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))     
            else:
                raise UserError(_(warm_sound_code + "Scanned Internal Reference/Barcode not exist in any product!"))                     
                