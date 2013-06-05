function createObject()
{
var request_type;
var browser = navigator.appName;
    if(browser == "Microsoft Internet Explorer"){
    request_type = new ActiveXObject("Microsoft.XMLHTTP");
    }else{
    request_type = new XMLHttpRequest();
    }
    return request_type;
}

var http = createObject();
var nocache = 0;

//Change the languages for all display message
function change_language(pos,lang_id)
{
   
   if (lang_id == 1)
   {
	  if (document.getElementById('French_'+pos).className  == 'activetab') 
	  {
	     document.getElementById('French_'+pos).className = document.getElementById('French_'+pos).className.replace( /(?:^|\s)activetab(?!\S)/g , '' );
	  }
          if (document.getElementById('Spanish_'+pos).className  == 'activetab') 
          {
             document.getElementById('Spanish_'+pos).className = document.getElementById('Spanish_'+pos).className.replace( /(?:^|\s)activetab(?!\S)/g , '' );
          }
	  if (document.getElementById('English_'+pos).className == "")
	  {
	    document.getElementById('English_'+pos).className += 'activetab';
	  }
   }
   else if (lang_id == 2)
   {

	  if (document.getElementById('English_'+pos).className  == 'activetab')
	  {
	    document.getElementById('English_'+pos).className = document.getElementById('English_'+pos).className.replace( /(?:^|\s)activetab(?!\S)/g , '' );
	  }
          if (document.getElementById('Spanish_'+pos).className  == 'activetab') 
          {
             document.getElementById('Spanish_'+pos).className = document.getElementById('Spanish_'+pos).className.replace( /(?:^|\s)activetab(?!\S)/g , '' );
          }
	  if (document.getElementById('French_'+pos).className == "")
	  {
	    document.getElementById('French_'+pos).className += 'activetab';
	  }
   }
   else if (lang_id == 3)
   {
	  if (document.getElementById('English_'+pos).className  == 'activetab')
	  {
	    document.getElementById('English_'+pos).className = document.getElementById('English_'+pos).className.replace( /(?:^|\s)activetab(?!\S)/g , '' );
	  }
          if (document.getElementById('French_'+pos).className  == 'activetab') 
          {
             document.getElementById('French_'+pos).className = document.getElementById('French_'+pos).className.replace( /(?:^|\s)activetab(?!\S)/g , '' );
          }
	  if (document.getElementById('Spanish_'+pos).className == "")
	  {
	    document.getElementById('Spanish_'+pos).className += 'activetab';
	  }
   }

var msg_type=document.getElementById('Msg_'+pos).value; 
document.getElementById('Error_'+pos).innerHTML = "<img src=design/ajaxLoadRedbg2.gif hspace=0 vspace=0 border=0 align=left id='loading'>";

 http.open('get','change_message.cgi?msg_type='+msg_type+'&lang_id='+lang_id);
 http.send(null);
 http.onreadystatechange = function()
 {
   if(http.readyState==4 && http.status==200)
   {   
     document.getElementById('Error_'+pos).innerHTML = " ";
     var data=http.responseText.split("&*&#");
     document.getElementById('txt_'+pos).value = data[0]; 
     document.getElementById('language_id_'+pos).value = data[1];            
   }   
 }
}

//Edit and cancel option for all message interface
function message_edit(pos)
{
var btnval = document.getElementById('edit_'+pos).value;

if (btnval == "cancel")
{
  document.getElementById('edit_'+pos).value="edit";
  document.getElementById('txt_'+pos).disabled=true;
  document.getElementById('save_'+pos).disabled=true;
}
else
{
document.getElementById('txt_'+pos).disabled=false;
document.getElementById('save_'+pos).disabled=false;
document.getElementById('edit_'+pos).value="cancel";
}
}

// Check the all normal message without using xxxx
function message_save(pos)
{
  var savebtn = document.getElementById('save_'+pos).value;
  var message = document.getElementById('txt_'+pos).value;
  var msg_type = document.getElementById('Msg_'+pos).value;
  var lang_id =  document.getElementById('language_id_'+pos).value;
  document.getElementById('Error_'+pos).innerHTML = "<img src=design/ajaxLoadRedbg2.gif hspace=0 vspace=0 border=0 align=left id='loading'>";
  
  if(message != "")
  {
     var len=message.length;						
	if(len >= 160)
	{
          document.getElementById('Error_'+pos).innerHTML = "Please enter maximum of 160 characters including spaces.";
	}
        else
        {
           http.open('get','sms_messages.cgi?message='+encodeURIComponent(message)+'&msg_type='+msg_type+'&lang_id='+lang_id);

           http.send(null);
           http.onreadystatechange = function()
           {
              if(http.readyState==4 && http.status==200)
              {   
                
                document.getElementById('Error_'+pos).innerHTML = "Sucessfully updated";
              }   
           }
         
        } 
  } 
  else
  { 
    alert("Please enter the message content to save");
    document.getElementById('Error_'+pos).innerHTML = "";
  } 			
}


//Check the messages of reroute last call function

function reroute_last_call(pos)
{
  var savebtn = document.getElementById('save_'+pos).value;
  var message = document.getElementById('txt_'+pos).value;
  var msg_type = document.getElementById('Msg_'+pos).value;
  var lang_id =  document.getElementById('language_id_'+pos).value;
  document.getElementById('Error_'+pos).innerHTML = "<img src=design/ajaxLoadRedbg2.gif hspace=0 vspace=0 border=0 align=left id='loading'>";

  if(message != "")
  {  
     var ErrorVal = "";
     var len=message.length;						
	
        if(len >= 160)
	{
	  document.getElementById('Error_'+pos).innerHTML = "Please enter maximum of 160 characters including spaces.";
	}
        else if(msg_type == "LAST_CALL_ROUTE_INFO")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number";  
		}				
	}
        else if(msg_type == "LAST_CALL_ROUTE")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number";  
		}				
	}
        else if(msg_type == "RRLC_RESP_INFO")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number and xxxxx for route value";  
		}				
	}
        else if(msg_type == "CALL_ROUTE_SELECTION")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number and xxxxx for route value";  
		}				
	}
        else if(msg_type == "RRLC_FUTURE_ROUTE")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for route value and xxxxx for number";  
		}				
	}
        else if(msg_type == "FUTURE_ROUTE_INFO")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number and xxxxx for route value";  
		}				
	}
        
        if(ErrorVal == "Ok")
	{
			
           http.open('get','sms_messages.cgi?message='+encodeURIComponent(message)+'&msg_type='+msg_type+'&lang_id='+lang_id);
           http.send(null);
           http.onreadystatechange = function()
           {
              if(http.readyState==4 && http.status==200)
              {   
                document.getElementById('Error_'+pos).innerHTML = "Sucessfully updated";
              }   
           }
        }
  }
  else
  { 
    alert("Please enter the message content to save");
    document.getElementById('Error_'+pos).innerHTML = "";
  } 			
}

//Check the messages of add ani functionality
function add_ani(pos)
{
  var savebtn = document.getElementById('save_'+pos).value;
  var message = document.getElementById('txt_'+pos).value;
  var msg_type = document.getElementById('Msg_'+pos).value;
  var lang_id =  document.getElementById('language_id_'+pos).value;
  document.getElementById('Error_'+pos).innerHTML = "<img src=design/ajaxLoadRedbg2.gif hspace=0 vspace=0 border=0 align=left id='loading'>";

  if(message != "")
  {  
     var ErrorVal = "";
     var len=message.length;						
	
        if(len >= 160)
	{
	  document.getElementById('Error_'+pos).innerHTML = "Please enter maximum of 160 characters including spaces.";
	}
        else if(msg_type == "ANI_RESP_INFO")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number and  xxxxx for ani number";  
		}				
	}
        else if(msg_type == "DUPLICATE_ANI_INFO")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number";  
		}				
	}
        else if(msg_type == "EXISTS_ZENO_USER")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number";  
		}				
	}
       
        
        if(ErrorVal == "Ok")
	{
			
           http.open('get','sms_messages.cgi?message='+encodeURIComponent(message)+'&msg_type='+msg_type+'&lang_id='+lang_id);
           http.send(null);
           http.onreadystatechange = function()
           {
              if(http.readyState==4 && http.status==200)
              {   
                document.getElementById('Error_'+pos).innerHTML = "Sucessfully updated";
              }   
           }
        }
  }
  else
  { 
    alert("Please enter the message content to save");
    document.getElementById('Error_'+pos).innerHTML = "";
  } 			
}

function refer_msgCheck(pos)
{
  var savebtn = document.getElementById('save_'+pos).value;
  var message = document.getElementById('txt_'+pos).value;
  var msg_type = document.getElementById('Msg_'+pos).value;
  var lang_id =  document.getElementById('language_id_'+pos).value;
  document.getElementById('Error_'+pos).innerHTML = "<img src=design/ajaxLoadRedbg2.gif hspace=0 vspace=0 border=0 align=left id='loading'>";

  if(message != "")
  {  
     var ErrorVal = "";
     var len=message.length;						
	
        if(len >= 160)
	{
	  document.getElementById('Error_'+pos).innerHTML = "Please enter maximum of 160 characters including spaces.";
	}
        else if(msg_type == "REFER_INVITATION_MSG")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for Refer name and  xxxxx for User name";  
		}				
	}
        else if(msg_type == "REFER_INVITATION_24H")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for Refer name and  xxxxx for User name";  
		}				
	}
        else if(msg_type == "REFER_INVITATION_48H")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for Refer name and  xxxxx for User name";  
		}				
	}
        else if(msg_type == "REFER_INVITATION_10D")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for Refer name and  xxxxx for User name";  
		}				
	}
        else if(msg_type == "REFER_NOT_JOINED_11D")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for Refer name and  xxxxx for User name";  
		}				
	}
        else if(msg_type == "REFER_PROMOTION_MSG")       
        {    
                if ((message.search(/\bxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for phone number";  
		}				
	}

        if(ErrorVal == "Ok")
	{
			
           http.open('get','sms_messages.cgi?message='+encodeURIComponent(message)+'&msg_type='+msg_type+'&lang_id='+lang_id);
           http.send(null);
           http.onreadystatechange = function()
           {
              if(http.readyState==4 && http.status==200)
              {   
                document.getElementById('Error_'+pos).innerHTML = "Sucessfully updated";
              }   
           }
        }
  }
  else
  { 
    alert("Please enter the message content to save");
    document.getElementById('Error_'+pos).innerHTML = "";
  } 			
}

//Check the general message of all message
function check_message(pos)
{
  var savebtn = document.getElementById('save_'+pos).value;
  var message = document.getElementById('txt_'+pos).value;
  var msg_type = document.getElementById('Msg_'+pos).value;
  var lang_id =  document.getElementById('language_id_'+pos).value;
  document.getElementById('Error_'+pos).innerHTML = "<img src=design/ajaxLoadRedbg2.gif hspace=0 vspace=0 border=0 align=left id='loading'>";


  if(message != "")
  {  
     var ErrorVal = "";
     var len=message.length;						
	
        if(len >= 160)
	{
	  document.getElementById('Error_'+pos).innerHTML = "Please enter maximum of 160 characters including spaces.";
	}
        else if (msg_type == "ROUTE_CHANGE_INFO")        
        {    
                if ((message.search(/\bxxxx\b/i) != -1) && (message.search(/\bxxxxx\b/i) != -1) && (message.search(/\bxxxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for route value and +xxxxx for number and xxxxxx to name";  
		}				
	}
        else if (msg_type == "DUPLICATE_CONTACT_INFO")        
        {    
                if ((message.search(/\bxxxx\b/i) != -1))
	        {							
		  ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for name and dial number";  
		}				
	}
        else if (msg_type == "REFER_RESP_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for referrer name";  
		}				
	}
        else if (msg_type == "REFUND_APPROVAL_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1) && (message.search(/\bxxxxx\b/) != -1) && (message.search(/\bxxxxxx\b/) != -1) && (message.search(/\bxxxxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for rate value and xxxxx for number and xxxxxx for datetime and xxxxxxx to current balance";  
		}				
	}
        else if (msg_type == "REFUND_DECLINE_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1)  && (message.search(/\bxxxxx\b/) != -1) && (message.search(/\bxxxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for rate value and xxxxx for number and xxxxxx for datetime";  
		}				
	}
        else if (msg_type == "SEARCH_CONTACT_NOT_FOUND")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for contact name/number";  
		}				
	}
        else if (msg_type == "SEARCH_RESP_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for contact name and dial number";  
		}				
	}
        else if (msg_type == "DELETE_CONTACT_NOT_FOUND")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for contact Name/Number";  
		}				
	}
        else if (msg_type == "DELETE_RESP_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for contact Name/Number";  
		}				
	}
        else if (msg_type == "USER_PIN_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for PIN number";  
		}				
	}
        else if (msg_type == "NEW_PIN_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for PIN number";  
		}				
	}      
        else if (msg_type == "ADD_CONTACT_RESP_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1) && (message.search(/\bxxxxx\b/) != -1) && (message.search(/\bxxxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for contact name and xxxxx for number and xxxxxx for dial number";  
		}				
	}     
        else if (msg_type == "FORWARD_RESP_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1) && (message.search(/\bxxxxx\b/) != -1) && (message.search(/\bxxxxxx\b/) != -1) && (message.search(/\bxxxxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for number and xxxxx for name and xxxxxx for number and xxxxxxx for name";  
		}				
	}
        else if (msg_type == "EXISTS_FORWARD_NUMBER")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for phone number";  
		}				
	}
        else if (msg_type == "CONTACT_NOT_FOUND_MSG")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for contact name/number";  
		}				
	}
        else if (msg_type == "LASTCALL_INFO")        
        { 
                if ((message.search(/\bxx\b/) != -1) && (message.search(/\bxxx\b/) != -1) && (message.search(/\bxxxx\b/) != -1) && (message.search(/\bxxxxx\b/) != -1) && (message.search(/\bxxxxxx\b/) != -1) && (message.search(/\bxxxxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xx for s.no and xxx for name and xxxx for number and xxxxx for datetime and xxxxxx for call charge and xxxxxxx for current balance.";  
		}				
	}
        else if (msg_type == "CALL_HISTORY_INFO")        
        { 
                if ((message.search(/\bxxxx\b/) != -1))        
                {							
                   ErrorVal = "Ok";
	        }
		else
		{
		  document.getElementById('Error_'+pos).innerHTML = "Please substitute xxxx for call history details.";  
		}				
	}

        if(ErrorVal == "Ok")
	{
			
           http.open('get','sms_messages.cgi?message='+encodeURIComponent(message)+'&msg_type='+msg_type+'&lang_id='+lang_id);
           http.send(null);
           http.onreadystatechange = function()
           {
              if(http.readyState==4 && http.status==200)
              {   
                document.getElementById('Error_'+pos).innerHTML = "Sucessfully updated";
              }   
           }
        }
  }
  else
  { 
    alert("Please enter the message content to save");
    document.getElementById('Error_'+pos).innerHTML = "";
  } 			
}



















