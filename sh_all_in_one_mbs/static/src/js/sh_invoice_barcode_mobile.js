$(document).ready(function(){
    
	
	
	
    function decodeOnce(codeReader, selectedDeviceId) {
        codeReader.decodeFromInputVideoDevice(selectedDeviceId, 'video').then((result) => {
        	console.log(result)
        	$('input[name="sh_invoice_barcode_mobile"]').val(result.text);    				
	  		$('input[name="sh_invoice_barcode_mobile"]').change();

    		//RESET READER
            codeReader.reset();
            
    		//HIDE VIDEO
    		$('#js_id_sh_invoice_barcode_mobile_vid_div').hide();  
       		
    		//HIDE STOP BUTTON
    		$("#js_id_sh_invoice_barcode_mobile_reset_btn").hide();  
    		
    		//RESULT
            document.getElementById('js_id_sh_invoice_barcode_mobile_result').textContent = result.text;
    		
            
        }).catch((err) => {
          console.error(err)

        })
      }

      function decodeContinuously(codeReader, selectedDeviceId) {
        codeReader.decodeFromInputVideoDeviceContinuously(selectedDeviceId, 'video', (result, err) => {
          if (result) {
            // properly decoded qr code
            console.log('Found QR code!', result)
        	$('input[name="sh_invoice_barcode_mobile"]').val(result.text);    				
    		$('input[name="sh_invoice_barcode_mobile"]').change();            
    		
    		//RESULT
            document.getElementById('js_id_sh_invoice_barcode_mobile_result').textContent = result.text;
    		
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
	      		$('input[name="sh_invoice_barcode_mobile"]').val('');    				
	      		$('input[name="sh_invoice_barcode_mobile"]').change();              
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
	$("#js_id_sh_invoice_barcode_mobile_reset_btn").hide();

    let selectedDeviceId;

    
    
    const codeReader = new ZXing.BrowserMultiFormatReader()
    //const codeReader = new ZXing.BrowserBarcodeReader()    
    
    console.log('ZXing code reader initialized');
    codeReader.getVideoInputDevices()
    .then(function(result) {
    	//THEN METHOD START HERE
    	//const sourceSelect = $("#js_id_sh_invoice_barcode_mobile_cam_select");
    	const sourceSelect = document.getElementById('js_id_sh_invoice_barcode_mobile_cam_select');
		
    	$('input[name="sh_invoice_barcode_mobile"]').val('');    				
		$('input[name="sh_invoice_barcode_mobile"]').change();
		
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
    	$(document).on('change', '#js_id_sh_invoice_barcode_mobile_cam_select', function() {
    		  // Does some stuff and logs the event to the console
    		selectedDeviceId = sourceSelect.value;    
            
    	});
        	
        
        
        
        /*
         * ========================
         * WHEN CLICK START BUTTON.
         * ========================
         */
        $(document).on("click","#js_id_sh_invoice_barcode_mobile_start_btn",function(event) {

        	//EMPTY INPUT
    		$('input[name="sh_invoice_barcode_mobile"]').val('');    				
    		$('input[name="sh_invoice_barcode_mobile"]').change();
    		
    		//SHOW VIDEO
    		$('#js_id_sh_invoice_barcode_mobile_vid_div').show();    
    		
    		//SHOW STOP BUTTON
    		$("#js_id_sh_invoice_barcode_mobile_reset_btn").show();
    		
    		
      		//CALL METHOD
			//CONTINUOUS SCAN OR NOT.
			if( $('span[name="sh_invoice_bm_is_cont_scan"]').text() == 'True' ){
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
        $(document).on("click","#js_id_sh_invoice_barcode_mobile_reset_btn",function() {
            console.log('STOP CAMERA');
            document.getElementById('js_id_sh_invoice_barcode_mobile_result').textContent = '';
    		
            //EMPTY VALUE
            $('input[name="sh_invoice_barcode_mobile"]').val('');    				
    		$('input[name="sh_invoice_barcode_mobile"]').change();
    		
    		//RESET READER
            codeReader.reset();
            
    		//HIDE VIDEO
    		$('#js_id_sh_invoice_barcode_mobile_vid_div').hide();  
       		
    		//HIDE STOP BUTTON
    		$("#js_id_sh_invoice_barcode_mobile_reset_btn").hide();    		
            
            
        });        
                
        
    // CUSTOM ENENT HANDLER ENDS HERE
        
    // THEN METHOD ENDS HERE
    }).catch(function (reason) { 
    	
  	  console.log("Error ==>" + reason);
  });
    
       
    
});


	




