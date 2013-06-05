//javascript Sms services

$(document).ready(function(){
	//Get form Id 
	var frmname=$("form").attr("id");
	
	if(frmname == "Form_SMS")
	{		
		$("textarea").keyup(function(){
			
			var clsname=$(this).attr("id");
			var Splitval=clsname.split("_");				
			$('#Error_'+Splitval[1]).text("");		
			$('#Error_'+Splitval[1]).removeClass("success");
		    $('#Error_'+Splitval[1]).removeClass("error");
		});
		
		//edit and save button on click method
		$("textarea").attr("disabled","disabled");
		$("[value='Save']").attr("disabled","disabled");
		$("input:[type='button']").click(function(){
			var getBtnId=$(this).attr("id");
			var Splitval=getBtnId.split("_");				
			var getBtnValue=$(this).attr("value");
			var getTxtraVal="";		
			if(getBtnValue == "Edit")
			{				
				$("#txt_"+Splitval[1]).removeAttr("disabled","disabled");
				$("#save_"+Splitval[1]).removeAttr("disabled","disabled");
				$("#txt_"+Splitval[1]).focus();
				$(this).attr("value","Cancel");
			}
			else if(getBtnValue == "Cancel")
			{
				$("#txt_"+Splitval[1]).attr("disabled","disabled");
				$("#save_"+Splitval[1]).attr("disabled","disabled");
				$(this).attr("value","Edit");
			}
			else
			{
				var textareaval=$.trim($("#txt_"+Splitval[1]).val());
				var ConfirmationTextarea = "txt_"+Splitval[1];
				var ErrorVal = "";
				$('#Error_'+Splitval[1]).fadeIn("slow");
				if(textareaval != '')
				{
					var len=textareaval.length;						
					if(len >= 150)
					{
						$('#Error_'+Splitval[1]).text("Please enter maximum of 150 characters including spaces");
						$('#Error_'+Splitval[1]).addClass("error");
						ErrorVal = "No";
					}
					else if(ConfirmationTextarea == "txt_3")
					{
						if ((textareaval.search(/\bxxxx\b/i) != -1) && (textareaval.search(/\bxxxxxxxxxx\b/i) != -1) && (textareaval.search(/\bxxxxxxxx\b/i) != -1))
						{							
							ErrorVal = "Ok";
						}
						else
						{
							$('#Error_'+Splitval[1]).text("Please substitute xxxx for name and +xxxxxxxxxx for to talk number and xxxxxxxx to dial number");
							$('#Error_'+Splitval[1]).addClass("error");
							ErrorVal = "No";
						}						
					}
					else if (ConfirmationTextarea == "txt_4")
				        {
					    if ((textareaval.search(/\bxxxxxxx\b/i) != -1))
						{							
						   ErrorVal = "Ok";
						}
						else
						{
						   $('#Error_'+Splitval[1]).text("Please substitute xxxxxxx for user commands");
						   $('#Error_'+Splitval[1]).addClass("error");
						   ErrorVal = "No";
						}	
					} 
                                        else if (ConfirmationTextarea == "txt_5")
				        {
					    if ((textareaval.search(/\bxxxx\b/i) != -1))
						{							
						   ErrorVal = "Ok";
						}
						else
						{
						   $('#Error_'+Splitval[1]).text("Please substitute xxxx to phone number of friend");
						   $('#Error_'+Splitval[1]).addClass("error");
						   ErrorVal = "No";
						}	
					}
					else
					{
						ErrorVal = "Ok";
					}
					
					if(ErrorVal == "Ok")
					{
						CallAjax(Splitval[1]);
					}					
				}
				else
				{
					var lablenam=$.trim($("#lbl_"+Splitval[1]).text());					
					$('#Error_'+Splitval[1]).text("Enter the "+ lablenam);
					$('#Error_'+Splitval[1]).addClass("error");					
				}			
			}
		});
	}
});

function CallAjax(Arg)
{
	$('#Error_'+Arg).html('<img src=design/ajaxLoadRedbg2.gif hspace=0 vspace=0 border=0 align=left id="loadimg">');
	$("#save_"+Arg).attr("value","Save...");
	$.ajax({
        type: "GET",
        url: "./sms_syntaxchange.cgi", // URL of the Perl script
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        // send Type and Message  as parameters to the Perl script
        data: "message=" + encodeURIComponent($("#txt_"+Arg).val()) + "&type=" + $("#txt_"+Arg).attr("name") + "&hdnflag=FlagSave",
        // script call was *not* successful
        error: function(XMLHttpRequest, textStatus, errorThrown) { 
          $('div#loginResult').text("responseText: " + XMLHttpRequest.responseText 
            + ", textStatus: " + textStatus 
            + ", errorThrown: " + errorThrown);
          $('div#loginResult').addClass("error");
        }, // error 
        // script call was successful 
        // data contains the JSON values returned by the Perl script 
        success: function(data){		
          if (data.error) { // script returned error			
            $('#Error_'+Arg).text("data.error: " + data.error);			
            $('#Error_'+Arg).addClass("error");
          } // if
          else { // login was successful		           
            $('#Error_'+Arg).text(data.success + " " + data.Text);
			$("#save_"+Arg).attr("value","Save");
            $('#Error_'+Arg).addClass("success");
          } //else
        } // success
      }); // ajax
}
