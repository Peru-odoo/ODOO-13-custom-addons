odoo.define('aspl_manage_so_pos_orders.db', function (require) {
    "use strict";

    var DB = require('point_of_sale.DB');

    DB.include({
        notification: function(type, message){
            var types = ['success','warning','info', 'danger'];
            if($.inArray(type.toLowerCase(),types) != -1){
                $('div.span4').remove();
                var newMessage = '';
                message = message;
                switch(type){
                case 'success' :
                    newMessage = '<i class="fa fa-check" aria-hidden="true"></i> '+message;
                    break;
                case 'warning' :
                    newMessage = '<i class="fa fa-exclamation-triangle" aria-hidden="true"></i> '+message;
                    break;
                case 'info' :
                    newMessage = '<i class="fa fa-info" aria-hidden="true"></i> '+message;
                    break;
                case 'danger' :
                    newMessage = '<i class="fa fa-ban" aria-hidden="true"></i> '+message;
                    break;
                }
                $('body').append('<div class="span4 pull-right">' +
                        '<div class="alert alert-'+type+' fade">' +
                        newMessage+
                       '</div>'+
                     '</div>');
                $(".alert").removeClass("in").show();
                $(".alert").delay(200).addClass("in").fadeOut(3000);
            }
        },
        init: function(options){
            this._super.apply(this, arguments);
            this.sale_order_write_date = null;
            this.sale_order_by_id = {};
            this.sale_order_sorted = [];
            this.sale_order_search_string = "";
            this.order_write_date = null;
            this.order_by_id = {};
            this.order_sorted = [];
            this.order_search_string = "";
            this.sale_invoice_write_date = null;
            this.sale_invoice_by_id = {};
            this.sale_invoice_sorted = [];
            this.sale_invoice_search_string = "";
        },
        add_orders: function(orders){
            var updated_count = 0;
            var new_write_date = '';
            for(var i = 0, len = orders.length; i < len; i++){
                var order = orders[i];
                if (    this.order_write_date &&
                        this.order_by_id[order.id] &&
                        new Date(this.order_write_date).getTime() + 1000 >=
                        new Date(order.write_date).getTime() ) {
                    continue;
                } else if ( new_write_date < order.write_date ) {
                    new_write_date  = order.write_date;
                }
                if (!this.order_by_id[order.id]) {
                    this.order_sorted.push(order.id);
                }
                this.order_by_id[order.id] = order;
                updated_count += 1;
            }
            this.order_write_date = new_write_date || this.order_write_date;
            if (updated_count) {
                // If there were updates, we need to completely
                this.order_search_string = "";
                for (var id in this.order_by_id) {
                    var order = this.order_by_id[id];
                    this.order_search_string += this._order_search_string(order);
                }
            }
            return updated_count;
        },
        add_sale_orders: function(orders){
            var updated_count = 0;
            var new_write_date = '';
            for(var i = 0, len = orders.length; i < len; i++){
                var order = orders[i];
                if (    this.sale_order_write_date &&
                        this.sale_order_by_id[order.id] &&
                        new Date(this.sale_order_write_date).getTime() + 1000 >=
                        new Date(order.write_date).getTime() ) {
                    continue;
                } else if ( new_write_date < order.write_date ) {
                    new_write_date  = order.write_date;
                }
                if (!this.sale_order_by_id[order.id]) {
                    this.sale_order_sorted.push(order.id);
                }
                this.sale_order_by_id[order.id] = order;
                updated_count += 1;
            }
            this.sale_order_write_date = new_write_date || this.sale_order_write_date;
            if (updated_count) {
                // If there were updates, we need to completely
                this.sale_order_search_string = "";
                for (var id in this.sale_order_by_id) {
                    var order = this.sale_order_by_id[id];
                    this.sale_order_search_string += this._sale_order_search_string(order);
                }
            }
            return updated_count;
        },
        add_sale_invoices: function(invoices){
            var updated_count = 0;
            var new_write_date = '';
            for(var i = 0, len = invoices.length; i < len; i++){
                var invoice = invoices[i];
                if (    this.sale_invoice_write_date &&
                        this.sale_invoice_by_id[invoice.id] &&
                        new Date(this.sale_invoice_write_date).getTime() + 1000 >=
                        new Date(invoice.write_date).getTime() ) {
                    continue;
                } else if ( new_write_date < invoice.write_date ) {
                    new_write_date  = invoice.write_date;
                }
                if (!this.sale_invoice_by_id[invoice.id]) {
                    this.sale_invoice_sorted.push(invoice.id);
                }
                this.sale_invoice_by_id[invoice.id] = invoice;
                updated_count += 1;
            }
            this.sale_invoice_write_date = new_write_date || this.sale_invoice_write_date;
            if (updated_count) {
                // If there were updates, we need to completely
                this.sale_invoice_search_string = "";
                for (var id in this.sale_invoice_by_id) {
                    var invoice = this.sale_invoice_by_id[id];
                    this.sale_invoice_search_string += this._sale_invoice_search_string(invoice);
                }
            }
            return updated_count;
        },
        _order_search_string: function(order){
            var str =  order.name;
            if(order.pos_reference){
                str += '|' + order.pos_reference;
            }
            if(order.partner_id.length > 0){
                str += '|' + order.partner_id[1];
            }
            str = '' + order.id + ':' + str.replace(':','') + '\n';
            return str;
        },
        _sale_order_search_string: function(order){
            var str =  order.name;
            if(order.partner_id){
                str += '|' + order.partner_id[1];
            }
            str = '' + order.id + ':' + str.replace(':','') + '\n';
            return str;
        },
        _sale_invoice_search_string: function(invoice){
            var str =  invoice.display_name;
            if(invoice.partner_id){
                str += '|' + invoice.partner_id[1];
            }
            str = '' + invoice.id + ':' + str.replace(':','') + '\n';
            return str;
        },
        get_order_write_date: function(){
            return this.order_write_date;
        },
        get_order_by_id: function(id){
            return this.order_by_id[id];
        },
        get_sale_order_write_date: function(){
            return this.sale_order_write_date;
        },
        get_sale_order_by_id: function(id){
            return this.sale_order_by_id[id];
        },
        get_sale_invoice_write_date: function(){
            return this.sale_invoice_write_date;
        },
        get_sale_invoice_by_id: function(id){
            return this.sale_invoice_by_id[id];
        },
        search_order: function(query){
            try {
                query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
                query = query.replace(' ','.+');
                var re = RegExp("([0-9]+):.*?"+query,"gi");
            }catch(e){
                return [];
            }
            var results = [];
            var r;
            for(var i = 0; i < this.limit; i++){
                r = re.exec(this.order_search_string);
                if(r){
                    var id = Number(r[1]);
                    results.push(this.get_order_by_id(id));
                }else{
                    break;
                }
            }
            return results;
        },
        search_sale_order: function(query){
            try {
                query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
                query = query.replace(' ','.+');
                var re = RegExp("([0-9]+):.*?"+query,"gi");
            }catch(e){
                return [];
            }
            var results = [];
            var r;
            for(var i = 0; i < this.limit; i++){
                r = re.exec(this.sale_order_search_string);
                if(r){
                    var id = Number(r[1]);
                    results.push(this.get_sale_order_by_id(id));
                }else{
                    break;
                }
            }
            return results;
        },
        search_invoice: function(query){
            try {
                query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,'.');
                query = query.replace(' ','.+');
                var re = RegExp("([0-9]+):.*?"+query,"gi");
            }catch(e){
                return [];
            }
            var results = [];
            var r;
            for(var i = 0; i < this.limit; i++){
                r = re.exec(this.sale_invoice_search_string);
                if(r){
                    var id = Number(r[1]);
                    results.push(this.get_sale_invoice_by_id(id));
                }else{
                    break;
                }
            }
            return results;
        },
    });

});