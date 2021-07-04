odoo.define('sh_all_in_one_mbs.sh_scan_inventory_adjt_tree', function (require) {
"use strict";

		var core = require('web.core');
		var Sidebar = require('web.Sidebar');
		var ListController = require('web.ListController');
		var session = require('web.session');


		var QWeb = core.qweb;

		var _t = core._t;

		ListController.include({

			 renderButtons: function($node) {
			
		     var self = this;				 
			 this._super.apply(this, arguments);
			 
			 	
			 
	            if (this.modelName != "stock.inventory.line") {
	            	this.$buttons.find('button.js_cls_btn_sh_scan_inventory_adjt_tree').hide();
	            	
	                //var data = this.model.get(this.handle);	                
	                //if (data.context.journal_type !== 'cash') {
	                 //   this.$buttons.find('button.o_button_import').hide();
	                //}
	                
	                
	            }			 
			 	 
				 
			 
					 if (this.$buttons) {
							 let filter_button = this.$buttons.find('.js_cls_btn_sh_scan_inventory_adjt_tree');
							 //  on click on the button with class js_cls_btn_sh_scan_inventory_adjt_tree call the function sh_import_product_var_gs_action
							 filter_button && filter_button.click(this.proxy('sh_inventory_adjustment_barcode_mobile_action')) ;
					 }
					 
					 
			 },
			 
			 sh_inventory_adjustment_barcode_mobile_action: function () {
				 	//$.blockUI();
			        var self = this;
			        
			        //REMOVE OLD SCANNING DIV.
			        this.$('.js_cls_sh_scan_inventory_adjt_tree_scanning_portion').remove();
	        
			        
			        // RENDER NEW SCANNING DIV
			        this.$('.o_list_view').before( QWeb.render('sh_inventory_adjustment_barcode_mobile.scan.wizard.tree') );			        

			        
			    	
			        function decodeOnce(codeReader, selectedDeviceId) {
			            codeReader.decodeFromInputVideoDevice(selectedDeviceId, 'video').then((result) => {
			            	console.log(result)
			            	
			            	//$('input[name="sh_inventory_adjt_barcode_mobile"]').val(result.text);    				
			    	  		//$('input[name="sh_inventory_adjt_barcode_mobile"]').change();
			            	
			        		
			            	//TREE VIEW SCANNING STUFF

			                
			            	self._rpc({
			                    model: 'stock.inventory',
			                    method: 'action_sh_scan_inventory_adjt_tree',
			                    args: [self.inventory_id,result.text]
			                }).then(function (res) {
			                	
			                	 $(".o_list_table").find('th[data-name="write_date"]').click();
			                	 $(".o_list_table").find('th[data-name="write_date"]').click();
			                	 
			                	self.trigger_up('reload');
			                    
			                });		            	
			            	
			                //TREE VIEW SCANNING STUFF
			            	
			            	
			            	//RESET READER
			                codeReader.reset();
			                $("#js_id_sh_inventory_adjt_barcode_mobile_reset_btn").click();  
			                
			        		//HIDE VIDEO
			        		$('#js_id_sh_inventory_adjt_barcode_mobile_vid_div').hide();  
			           		
			        		//HIDE STOP BUTTON
			        		$("#js_id_sh_inventory_adjt_barcode_mobile_reset_btn").hide();  
			        		
			        		//RESULT
			                document.getElementById('js_id_sh_inventory_adjt_barcode_mobile_result').textContent = result.text;
			                
			                
			                
			        		
			                
			            }).catch((err) => {
			              console.error(err)

			            })
			          }

			          function decodeContinuously(codeReader, selectedDeviceId) {
			            codeReader.decodeFromInputVideoDeviceContinuously(selectedDeviceId, 'video', (result, err) => {
			              if (result) {
			                // properly decoded qr code
			                console.log('Found QR code!', result)
			            	//$('input[name="sh_inventory_adjt_barcode_mobile"]').val(result.text);    				
			        		//$('input[name="sh_inventory_adjt_barcode_mobile"]').change();            
			        		
			            	//TREE VIEW SCANNING STUFF
			                self._rpc({
			                    model: 'stock.inventory',
			                    method: 'action_sh_scan_inventory_adjt_tree',
			                    args: [self.inventory_id,result.text]
			                }).then(function (res) {
			                	
			                	 $(".o_list_table").find('th[data-name="write_date"]').click();
			                	 $(".o_list_table").find('th[data-name="write_date"]').click();
			                	 

			                	 
			                	
			                    

			                	 //codeReader.reset();					                	 
		                	 
			                	 
					             //$("#js_id_sh_inventory_adjt_barcode_mobile_start_btn").click();  	
					             
					             self.trigger_up('reload');
					             
			                	 
			                });			            	
			            	//TREE VIEW SCANNING STUFF
			                


			                
			                
			        		//RESULT
			                document.getElementById('js_id_sh_inventory_adjt_barcode_mobile_result').textContent = result.text;
			        		
			              }

			              if (err) {
			                // As long as this error belongs into one of the following categories
			                // the code reader is going to continue as excepted. Any other error
			                // will stop the decoding loop.
			                //
			                // Excepted Exceptions:
			                //
			                //  - NotFoundException
			                //  - ChecksumException
			                //  - FormatException

			                if (err instanceof ZXing.NotFoundException) {
			                	console.log('No QR code found.')
			    	          	//EMPTY INPUT
			    	      		//$('input[name="sh_inventory_adjt_barcode_mobile"]').val('');    				
			    	      		//$('input[name="sh_inventory_adjt_barcode_mobile"]').change();              
			                }

			                if (err instanceof ZXing.ChecksumException) {
			                  console.log('A code was found, but it\'s read value was not valid.')
			                }

			                if (err instanceof ZXing.FormatException) {
			                  console.log('A code was found, but it was in a invalid format.')
			                }
			              }
			            })
			          }	
			    	
			    	
			    		
			    	
			    	
			    	//HIDE STOP BUTTON (SAFETY IN XML WE ALSO DO AND HERE ALSO.)
			    	$("#js_id_sh_inventory_adjt_barcode_mobile_reset_btn").hide();

			        let selectedDeviceId;

			        
			        
			        const codeReader = new ZXing.BrowserMultiFormatReader()
			        //const codeReader = new ZXing.BrowserBarcodeReader()    
			        
			        console.log('ZXing code reader initialized');
			        codeReader.getVideoInputDevices()
			        .then(function(result) {
			        	//THEN METHOD START HERE
			        	//const sourceSelect = $("#js_id_sh_inventory_adjt_barcode_mobile_cam_select");
			        	const sourceSelect = document.getElementById('js_id_sh_inventory_adjt_barcode_mobile_cam_select');
			    		
			        	//$('input[name="sh_inventory_adjt_barcode_mobile"]').val('');    				
			    		//$('input[name="sh_inventory_adjt_barcode_mobile"]').change();
			    		
			            _.each(result, function(item) {
			                //self._add_filter(item.partner_id[0], item.partner_id[1], !active_partner, true);
			                const sourceOption = document.createElement('option')
			                sourceOption.text = item.label
			                sourceOption.value = item.deviceId
			                sourceSelect.appendChild(sourceOption)
			                
			            });
			                    
			            //CUSTOM EVENT HANDLER START HERE
			            
			     
			            /*
			             * =============================
			             * ONCHANGE SELECT CAMERA
			             * =============================
			             */        
			        	$(document).on('change', '#js_id_sh_inventory_adjt_barcode_mobile_cam_select', function() {
			        		  // Does some stuff and logs the event to the console
			        		selectedDeviceId = sourceSelect.value;    
			                
			        	});

			        	
			        	
			        	
			            /*
			             * ================================================
			             * WHEN CLICK Continuously Scan BUTTON.
			             * ================================================
			             */			        	
			        	
			        	$(document).on('click', 'input[name="js_sh_chkbox_inventory_adjt_bm_is_cont_scan"]', function() {
			        		//reset code reader here
			        		//RESET READER
			                codeReader.reset();
			                
			        		//HIDE VIDEO
			        		$('#js_id_sh_inventory_adjt_barcode_mobile_vid_div').hide();  
			           		
			        		//HIDE STOP BUTTON
			        		$("#js_id_sh_inventory_adjt_barcode_mobile_reset_btn").hide();    
			                
			        	});			        	
			            
            
			        			            
			            /*
			             * ========================
			             * WHEN CLICK START BUTTON.
			             * ========================
			             */
			            $(document).on("click","#js_id_sh_inventory_adjt_barcode_mobile_start_btn",function(event) {

			            	//EMPTY INPUT
			        		//$('input[name="sh_inventory_adjt_barcode_mobile"]').val('');    				
			        		//$('input[name="sh_inventory_adjt_barcode_mobile"]').change();
			        					            	
			            	
			        		//SHOW VIDEO
			        		$('#js_id_sh_inventory_adjt_barcode_mobile_vid_div').show();    
			        		
			        		//SHOW STOP BUTTON
			        		$("#js_id_sh_inventory_adjt_barcode_mobile_reset_btn").show();
			        		
			        		 //decodeContinuously(codeReader, selectedDeviceId);	
			          		
			        		 //CALL METHOD
			    			//CONTINUOUS SCAN OR NOT.
			    			
			        		if( $('input[name="js_sh_chkbox_inventory_adjt_bm_is_cont_scan"]').is(":checked") ){
			    	              decodeContinuously(codeReader, selectedDeviceId);		
			    			}else{
			    	              decodeOnce(codeReader, selectedDeviceId);
			    			} 
			    			     		

			                
			                
			            });
			            
			               
			            
			            /*
			             * =============================
			             * WHEN CLICK STOP/RESET BUTTON.
			             * =============================
			             */
			            $(document).on("click","#js_id_sh_inventory_adjt_barcode_mobile_reset_btn",function() {
			                console.log('STOP CAMERA');
			                document.getElementById('js_id_sh_inventory_adjt_barcode_mobile_result').textContent = '';
			        		
			                //EMPTY VALUE
			                //$('input[name="sh_inventory_adjt_barcode_mobile"]').val('');    				
			        		//$('input[name="sh_inventory_adjt_barcode_mobile"]').change();
			        		
			        		//RESET READER
			                codeReader.reset();
			                
			        		//HIDE VIDEO
			        		$('#js_id_sh_inventory_adjt_barcode_mobile_vid_div').hide();  
			           		
			        		//HIDE STOP BUTTON
			        		$("#js_id_sh_inventory_adjt_barcode_mobile_reset_btn").hide();    		
			                
			                
			            });        
			                    
			            
			        // CUSTOM ENENT HANDLER ENDS HERE
			            
			        // THEN METHOD ENDS HERE
			        }).catch(function (reason) { 
			        	
			      	  console.log("Error ==>" + reason);
			      });
			        
			        			        
			        
			        
			        
			        //this.$('.o_list_view').before( "<h1>Test</h1>" );

			        /*
			        return self._rpc({
			            model: 'sh.import.product.var.gs.log',
			            method: 'action_import_product_variants',
			            args: [null],
			            context: self.context,
			        })
			        .then(function(res){
			        	console.log("done");
			        	self.trigger_up('reload');	
			        	$.unblockUI();
			        });
			        */
			        

			 }

	 });

});





