odoo.define('sh_barcode_scanner.sound_sh_barcode_scanner', function (require) {
"use strict";



var ajax = require('web.ajax');
var core = require('web.core');
var Dialog = require('web.Dialog');
var CrashManager = require('web.CrashManager').CrashManager;
var AbstractWebClient = require('web.AbstractWebClient');


var WarningDialog  = require('web.CrashManager').WarningDialog;
var QWeb = core.qweb;
var _t = core._t;
var _lt = core._lt;
var qweb = core.qweb;




var CrashManager = CrashManager.include({
	

    show_warning: function (error, options) {
    	

		/****************************************************************
		 * softhealer custom code start here
		 * SH_BARCODE_SCANNER_ is a code to identi
		 * fy that message is coming from barcode scanner.
		 * here we remove code for display valid message and play sound.       
		 * ***************************************************************
        */
		if (error.data.message.length){
			
    		//for auto close popup start here
    		var auto_close_ms = error.data.message.match("AUTO_CLOSE_AFTER_(.*)_MS&");
    		if(auto_close_ms && auto_close_ms.length == 2){
    			auto_close_ms = auto_close_ms[1];    			
    			var original_msg = "AUTO_CLOSE_AFTER_"+ auto_close_ms +"_MS&";
    			error.data.message = error.data.message.replace(original_msg, "");  
    			setTimeout(function(){     				
    				$('.o_technical_modal').find('button[type="button"] > span:contains("Ok")').closest('button').trigger( "click" );
    			}, auto_close_ms);	    			
    			
    		} 	  
    		//for auto close popup ends here
    		
    		
    		//for play sound start here
    		//if message has SH_BARCODE_SCANNER_
    		var str_msg = error.data.message.match("SH_BARCODE_SCANNER_");    		
    		if (str_msg){
    			//remove SH_BARCODE_SCANNER_ from message and make valid message
    			error.data.message = error.data.message.replace("SH_BARCODE_SCANNER_", "");
    			    			
    			//play sound
    			var src = "/sh_barcode_scanner/static/src/sounds/error.wav";
    	        $('body').append('<audio src="'+src+'" autoplay="true"></audio>');	   
    		}
    		//for play sound ends here

		}
		
	
					
		//softhealer custom code ends here    	
    	
    	
        return this._super.apply(this, arguments);

        
    },	
	

});

return {
    CrashManager: CrashManager,
};

});


