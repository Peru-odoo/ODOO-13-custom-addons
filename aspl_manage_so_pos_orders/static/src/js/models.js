odoo.define('aspl_manage_so_pos_orders.models', function (require) {
"use strict";

    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');
    var core = require('web.core');

    var _t = core._t;

    models.load_fields("res.partner", ['property_product_pricelist']);
    models.load_fields("product.product", ['type', 'invoice_policy']);
    models.load_fields("res.users", ['display_own_sales_order']);

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function(attr,options){
            var self = this;
            var res = _super_Order.initialize.call(this, attr, options);
            this.set({
                'sale_order_name': false,
                'invoice_name': false,
                'order_id': false,
                'shipping_address': false,
                'invoice_address': false,
                'sale_note': false,
                'signature': false,
                'inv_id': false,
                'sale_order_date': false,
                'edit_quotation': false,
                'paying_sale_order': false,
                'sale_order_pay': false,
                'invoice_pay': false,
                'sale_order_requested_date': false,
                'invoice_id':false,
                'sale_order_reprint':false,
            });
            $('.js_edit_quotation').hide();
        },
        generateUniqueId_barcode: function() {
            return new Date().getTime();
        },
//        generate_unique_id: function() {
//            var timestamp = new Date().getTime();
//            return Number(timestamp.toString().slice(-10));
//        },
        set_pos_reference: function(pos_reference) {
            this.set('pos_reference', pos_reference)
        },
        get_pos_reference: function() {
            return this.get('pos_reference')
        },
        set_user_name: function(user_id) {
            this.set('user_id', user_id);
        },
        get_user_name: function() {
            return this.get('user_id');
        },
        set_journal: function(statement_ids) {
            this.set('statement_ids', statement_ids)
        },
        get_journal: function() {
            return this.get('statement_ids');
        },
        set_sale_order_name: function(name){
            this.set('sale_order_name', name);
        },
        get_sale_order_name: function(){
            return this.get('sale_order_name');
        },
        set_sale_order_reprint: function(flag){
            this.set('sale_order_reprint', flag);
        },
        get_sale_order_reprint: function(){
            return this.get('sale_order_reprint');
        },
        set_sale_amount_due: function(amount_due){
            this.set('amount_due', amount_due);
        },
        get_sale_amount_due: function(){
            return this.get('amount_due');
        },
        set_invoice_name: function(name){
            this.set('invoice_name', name);
        },
        get_invoice_name: function(){
            return this.get('invoice_name');
        },
        export_as_JSON: function() {
            var submitted_order = _super_Order.export_as_JSON.call(this);
            var new_val = {
                signature: this.get_signature(),
                old_order_id: this.get_order_id(),
                sequence: this.get_sequence(),
                pos_reference: this.get_pos_reference()
            }
            $.extend(submitted_order, new_val);
            return submitted_order;
        },
        export_for_printing: function(){
            var orders = _super_Order.export_for_printing.call(this);
            var new_val = {
                sale_order_name: this.get_sale_order_name() || false,
                sale_amount_due: this.get_sale_amount_due() || false,
                sale_order_reprint: this.get_sale_order_reprint() || false,
                invoice_name: this.get_invoice_name() || false,
                sale_note: this.get_sale_note() || '',
                signature: this.get_signature() || '',
                reprint_payment: this.get_journal() || false,
                ref: this.get_pos_reference() || false,
                date_order: this.get_date_order() || false,
                partner : this.get_client_name() || false,
            };
            $.extend(orders, new_val);
            return orders;
        },
        set_sequence:function(sequence){
            this.set('sequence',sequence);
        },
        get_sequence:function(){
            return this.get('sequence');
        },
        set_order_id: function(order_id){
            this.set('order_id', order_id);
        },
        get_order_id: function(){
            return this.get('order_id');
        },
        set_amount_paid: function(amount_paid) {
            this.set('amount_paid', amount_paid);
        },
        get_amount_paid: function() {
            return this.get('amount_paid');
        },
        set_amount_return: function(amount_return) {
            this.set('amount_return', amount_return);
        },
        get_amount_return: function() {
            return this.get('amount_return');
        },
        set_amount_tax: function(amount_tax) {
            this.set('amount_tax', amount_tax);
        },
        get_amount_tax: function() {
            return this.get('amount_tax');
        },
        set_amount_total: function(amount_total) {
            this.set('amount_total', amount_total);
        },
        get_amount_total: function() {
            return this.get('amount_total');
        },
        set_company_id: function(company_id) {
            this.set('company_id', company_id);
        },
        get_company_id: function() {
            return this.get('company_id');
        },
        set_date_order: function(date_order) {
            this.set('date_order', date_order);
        },
        get_date_order: function() {
            return this.get('date_order');
        },
        set_pos_reference: function(pos_reference) {
            this.set('pos_reference', pos_reference)
        },
        set_shipping_address: function(val){
            this.set('shipping_address', val);
        },
        get_shipping_address: function() {
            return this.get('shipping_address');
        },
        set_print_invoice_receipt: function(invoice_receipt) {
            this.set('invoice_receipt', invoice_receipt);
        },
        get_print_invoice_receipt: function() {
            return this.get('invoice_receipt');
        },
        set_invoice_address: function(val){
            this.set('invoice_address', val);
        },
        get_invoice_address: function() {
            return this.get('invoice_address');
        },
        set_sale_note: function(val){
            this.set('sale_note', val);
        },
        get_sale_note: function() {
            return this.get('sale_note');
        },
        set_signature: function(signature) {
            this.set('signature', signature);
        },
        get_signature: function() {
            return this.get('signature');
        },
        set_inv_id: function(inv_id) {
            this.set('inv_id', inv_id)
        },
        get_inv_id: function() {
            return this.get('inv_id');
        },
        set_sale_order_date: function(sale_order_date) {
            this.set('sale_order_date', sale_order_date)
        },
        get_sale_order_date: function() {
            return this.get('sale_order_date');
        },
        set_sale_order_requested_date: function(sale_order_requested_date) {
            this.set('sale_order_requested_date', sale_order_requested_date)
        },
        get_sale_order_requested_date: function() {
            return this.get('sale_order_requested_date');
        },
        set_edit_quotation: function(edit_quotation) {
            this.set('edit_quotation', edit_quotation)
        },
        get_edit_quotation: function() {
            return this.get('edit_quotation');
        },
        set_paying_sale_order: function(paying_sale_order) {
            this.set('paying_sale_order', paying_sale_order)
        },
        get_paying_sale_order: function() {
            return this.get('paying_sale_order');
        },
        set_sale_order_pay: function(sale_order_pay) {
            this.set('sale_order_pay', sale_order_pay)
        },
        get_sale_order_pay: function() {
            return this.get('sale_order_pay');
        },
        set_invoice_id: function(invoice_id) {
            this.set('invoice_id', invoice_id)
        },
        get_invoice_id: function() {
            return this.get('invoice_id');
        },
        set_invoice_pay: function(invoice_pay) {
            this.set('invoice_pay', invoice_pay)
        },
        get_invoice_pay: function() {
            return this.get('invoice_pay');
        },
    });

    var _super_posmodel = models.PosModel;
    models.PosModel = models.PosModel.extend({
        load_server_data: function(){
            var self = this;
            var product_index = _.findIndex(this.models, function (model) {
                return model.model === "product.product";
            });
            var product_model = this.models[product_index];
            product_model.domain = [['sale_ok','=',true]];
            var partner_index = _.findIndex(this.models, function (model) {
                return model.model === "res.partner";
            });
            var partner_model = this.models[partner_index];
            partner_model.domain = [];
            var loaded = _super_posmodel.prototype.load_server_data.call(this);
            return loaded.then(function(){
                self.countries = _.each(self.countries, (res)=>{
                    return res['value'] = res.name
                })
                self.states = _.each(self.states, (res)=>{
                    return res['value'] = res.name
                })
                var date = new Date();
                var domain;
                var start_date;
                self.domain_sale_order = [];
                if(date){
                    if(self.config.sale_order_last_days){
                        date.setDate(date.getDate() - self.config.sale_order_last_days);
                    }
                    start_date = date.toJSON().slice(0,10);
                    self.domain_sale_order.push(['create_date' ,'>=', start_date]);
                } else {
                    domain = [];
                }
                self.domain_sale_order.push(['state','not in',['cancel']]);
                var params = {
                    model: 'sale.order',
                    method: 'search_read',
                    domain: self.domain_sale_order,
                    fields: self.fieldNames,
                }
                rpc.query(params, {async: false}).then(function(orders){
                    self.db.add_sale_orders(orders);
                    if(self.user.display_own_sales_order){
                        var user_orders = [];
                        orders.map(function(sale_order){
                            if(sale_order.user_id[0] == self.user.id){
                                user_orders.push(sale_order);
                            }
                        });
                        orders = user_orders;
                    }
                    orders.map(function(sale_order){
                        if(sale_order.date_order){
                             let localTime =  moment.utc(sale_order['date_order']).toDate();
                             sale_order['date_order'] = moment(localTime).format('YYYY-MM-DD HH:mm:ss')
                        }
                    });
                    self.set({'pos_sale_order_list' : orders});
                    // for pos order
                    if(self.config.enable_reorder){
                        var from_date = moment().format('YYYY-MM-DD')
                        if(self.config.order_last_days){
                            from_date = moment().subtract(self.config.order_last_days, 'days').format('YYYY-MM-DD');
                        }
                        self.domain_as_args = [['state','not in',['cancel']], ['create_date', '>=', from_date]];
                        var params = {
                            model: 'pos.order',
                            method: 'ac_pos_search_read',
                            args: [{'domain': self.domain_as_args}],
                            fields: self.fieldNames,
                        }
                        rpc.query(params, {async: false}).then(function(orders){
                            if(orders.length > 0){
                                self.db.add_orders(orders);
                                self.set({'pos_order_list' : orders});
                            }
                        });
                    }
                });
            });
        },
        _save_to_server: function (orders, options) {
            var self = this;
            return _super_posmodel.prototype._save_to_server.apply(this, arguments)
            .then(function(server_ids){
                if(server_ids && server_ids.length > 0 && self.config.enable_reorder){
                    var params = {
                        model: 'pos.order',
                        method: 'ac_pos_search_read',
                        args: [{'domain': [['id','=',server_ids[0]['id']]]}],
                        fields: self.fieldNames,
                    }
                    rpc.query(params, {async: false}).then(function(orders){
                        if(orders.length > 0){
                            orders = orders[0];
                            var exist_order = _.findWhere(self.get('pos_order_list'), {'pos_reference': orders.pos_reference})
                            if(exist_order){
                                _.extend(exist_order, orders);
                            } else {
                                var order_list = self.get('pos_order_list') ? self.get('pos_order_list') : [];
                                order_list.push(orders);
                                self.set('pos_order_list',order_list)
                            }
                            var new_orders = _.sortBy(self.get('pos_order_list'), 'id').reverse();
                            self.db.add_orders(new_orders);
                            self.set({ 'pos_order_list' : new_orders });
                        }
                    });
                }
                return server_ids;
            });
        },
        addZero: function(value){
            if (value < 10) {
                value = "0" + value;
            }
            return value;
        },
        create_sale_order: function(delivery_done){
            var self = this;
            var order = this.get_order();
            var currentOrderLines = order.get_orderlines();
            var customer_id = order.get_client().id;
            var location_id = self.config.picking_type_id ? self.config.picking_type_id[0] : false;
            var paymentlines = false;
            var paid = false;
            var confirm = false;
            var orderLines = [];
            for(var i = 0; i < currentOrderLines.length; i++){
                orderLines.push(currentOrderLines[i].export_as_JSON());
            }
            if(self.config.sale_order_operations === "paid" || order.get_order_id() || order.get_edit_quotation()) {
                paymentlines = [];
                _.each(order.get_paymentlines(), function(paymentline){
                    paymentlines.push({
                        'journal_id': paymentline.payment_method['id'],
                        'amount': paymentline.get_amount(),
                    })
                });
                paid = true
            }
            if(self.config.sale_order_operations === "confirm" && !order.get_edit_quotation()){
                confirm = true;
            }
            var vals = {
                orderlines: orderLines,
                customer_id: customer_id,
                location_id: location_id,
                journals: paymentlines,
                pricelist_id: order.pricelist.id || false,
                partner_shipping_id: order.get_shipping_address() || customer_id,
                partner_invoice_id: order.get_invoice_address() || customer_id,
                note: order.get_sale_note() || "",
                signature: order.get_signature() || "",
                inv_id: order.get_inv_id() || false,
                order_date: order.get_sale_order_date() || moment().format('YYYY-MM-DD HH:mm:ss'),
                requested_date: order.get_sale_order_requested_date() || false,
                sale_order_id: order.get_order_id() || false,
                edit_quotation: order.get_edit_quotation() || false,
                warehouse_id: self.config.warehouse_id ? self.config.warehouse_id[0] : false,
                confirm: confirm,
                paid: paid,
                delivery_done:delivery_done,
            }
            var params = {
                model: 'sale.order',
                method: 'create_sales_order',
                args: [vals],
            }
            rpc.query(params, {async: false}).then(function(sale_order){
                if(sale_order && sale_order[0]){
                    sale_order = sale_order[0];
                    if(paid && order.get_paying_sale_order()){
                        $('#btn_so').show();
                        if(sale_order){
                            order.set_sale_order_name(sale_order.name);
                        }
                        self.gui.show_screen('receipt');
                    } else{
                        var edit = order.get_edit_quotation();
                        order.finalize();
                        var url = window.location.origin + '/web#id=' + sale_order.id + '&view_type=form&model=sale.order';
                        self.gui.show_popup('saleOrder', {'url':url, 'name':sale_order.name, 'edit': edit});

                    }
                    var record_exist = false;
                    _.each(self.get('pos_sale_order_list'), function(existing_order){
                        if(existing_order.id === sale_order.id){
                            _.extend(existing_order, sale_order);
                            record_exist = true;
                        }
                    });
                    if (!record_exist){
                        var exist = _.findWhere(self.get('pos_sale_order_list'), {id: sale_order.id});
                        if(!exist){
                            var defined_orders = self.get('pos_sale_order_list');
                            var new_orders = [sale_order].concat(defined_orders);
                            self.db.add_sale_orders(new_orders);
                            new_orders.map(function(new_order){
                                let localTime =  moment.utc(new_order['date_order']).toDate();
                                new_order['date_order'] = moment(localTime).format('YYYY-MM-DD HH:mm:ss')
                            });
                            self.set({'pos_sale_order_list': new_orders})
                        }
                    }
                }
            });
        },
    });

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        export_for_printing: function() {
            var lines = _super_orderline.export_for_printing.call(this);
            lines.product_id = this.get_product().id
            return lines;
        }
    });

});