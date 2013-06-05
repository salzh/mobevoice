function refreshRefundList(){
   var type = $("#refundtype").val();
   top.location = "call_refund.cgi?type=" + type;
}

function CheckDecimal(inputtxt)  
{  
 var numbers =/^[0-9]+(\.[0-9]+)+$/;
 if(inputtxt.match(numbers)){
   return true;
 }else{
   return false;
 }  
}

function doRefund(refund_id){
   var service_id = $("#service" + refund_id).text();
   var call_id = $("#callid" + refund_id).text();
   var amount = $("#rate" + refund_id).text();
   var refund_amount = $("#refund" + refund_id).val();
   if(!CheckDecimal(refund_amount)){
      alert("Please enter a valid refund amount");
      return;
   }
   var type = $("#sel" + refund_id).val();
   if(type=="partial" && (refund_amount > amount || refund_amount<0)){
      alert("Refund Amount cannot be less than 0 or more then Call amount");
      return;
   }
   
   var typeText;
   if(type == "decline"){
      typeText = "Deline";
   }else if(type == "partial"){
      typeText = "Partial Refund $" + refund_amount;
   }else if(type == "full"){
      typeText = "Full Refund $" + amount;
   }else{
      alert("Please check a Refund Type");
      return;
   }
   var r = confirm("Are you sure you want to " + typeText + " this Refund request");
   
   if(!r){
      return;
   }
   
   $("#submit" + refund_id).val("Working...");
   $("#submit" + refund_id).attr("disabled", "disabled");
   
   $.get("call_refund.cgi", {
      'action': 'refund',
      'service_id': service_id,
      'amount': amount,
      'refundamount': refund_amount,
      'refund_id': refund_id,
      'type': type
   }, function(d){
      if(d == "success"){
         alert("Refund Processed");
         $("#submit" + refund_id).val("Complete");
      }else{
         alert(d);
         $("#submit" + refund_id).removeAttr("disabled");
      }
   })
}


function displayRefund(refund_id){
   var type = $("#sel" + refund_id).val();
   if(type == "partial"){
      $("#refund" + refund_id).removeAttr("disabled");
   }else{
      $("#refund" + refund_id).attr("disabled", "disabled");
   }
}

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

function update(pos)
{
   var position = "submit" + pos;
    document.getElementById(position).value ="Loading...";
   var call_id= encodeURI(document.getElementById('callid'+pos).innerHTML);
   var rate_value= encodeURI(document.getElementById('rate'+pos).innerHTML);
   var refund_action = encodeURI(document.getElementById('sel'+pos).value);
   var refund_status = document.getElementById('sel'+pos).value;
   var refund_amount = encodeURI(document.getElementById('refund'+pos).value);
  // var refund = "refund"+pos;
  
   if (refund_status == "Full Refund")
   {
                
                  var r=confirm("Are you sure you would like to fully refund this request by the full refund amount of $"+rate_value);
       
	           if (r==true)
                    {
                       http.open('get','refund.cgi?call_id='+call_id+'&rate_value='+rate_value+'&refund_action='+refund_action+'&refund_amount='+rate_value);
	                   http.send(null);
	                   http.onreadystatechange = function()
	                   {
		                 if(http.readyState==4 && http.status==200)
		                 {   
                                      if (http.responseText == "success")
                                       {
			               alert("Full refund amount successfully updated");
			               document.getElementById(position).value ="Processed";
			               document.getElementById(position).disabled = true;
			               document.getElementById('refund'+pos).disabled = true;
	                               document.getElementById('refund_status'+pos).innerHTML =refund_status;
                                       }
				       else
				       {
                                          alert(http.responseText);
                                          document.getElementById(position).value ="submit";
				       }
		                 }
	                   }
	            }
		    else
		    {
		        document.getElementById(position).value ="submit";
		    }
           
   }
   else if (refund_status == "Partial Refund")
   {
	    if (refund_amount > 0)
	    {
                if (refund_amount < rate_value)
	        {
	               
		      var r=confirm("Are you sure you would like to Partially refund this request by the partial refund amount of $"+refund_amount);
       
	                if (r==true)
                         {  
					   
			   http.open('get','refund.cgi?call_id='+call_id+'&rate_value='+rate_value+'&refund_action='+refund_action+'&refund_amount='+refund_amount);
	                   http.send(null);
	                   http.onreadystatechange = function()
	                   {
		                 if(http.readyState==4 && http.status==200)
		                 {
                                       if (http.responseText == "success")
                                       { 
			               alert("Partial refund amount successfully updated");
			               document.getElementById(position).value ="Processed";
				       document.getElementById(position).disabled = true;
			               document.getElementById('refund'+pos).disabled = true;
				       document.getElementById('refund_status'+pos).innerHTML =refund_status;
                                       }
                                       else
                                       {
                                         alert(http.responseText);
                                          document.getElementById(position).value ="submit";
                                       }
		                 }
	                   }
			}
			else
			{
			   document.getElementById(position).value ="submit";
			}
	        }
	        else
	        {
		        alert("Refund amount should not be more than Call charge");
	            document.getElementById(position).value ="submit";
	        }
             } 
	     else
	     {
		alert("Please enter the refund amount value only.");
		document.getElementById(position).value ="submit";
	     }
   }
   else if (refund_status == "Decline")
   {
	   
                   var r=confirm("Are you sure you would like to Declined this request by the full refund amount of $"+rate_value);
       
	          
	            if (r==true)
                    {
                       var refund_amount = 0;
	                   http.open('get','refund.cgi?call_id='+call_id+'&rate_value='+rate_value+'&refund_action='+refund_action+'&refund_amount='+refund_amount);
	                   http.send(null);
	                   http.onreadystatechange = function()
	                   {
		                 if(http.readyState==4 && http.status==200)
		                 {
			               if (http.responseText == "success")
                                       { 
                                       alert("Declined successfully updated");
			               document.getElementById(position).value ="Processed"; 
				       document.getElementById(position).disabled = true; 
			               document.getElementById('refund'+pos).disabled = true;
	                               document.getElementById('refund_status'+pos).innerHTML =refund_status;
                                       }
                                       else
                                       {
                                          alert(http.responseText);
                                          document.getElementById(position).value ="submit";
                                       }
		                 }
	                  }
	            
	            }
	            else
		    {
	               document.getElementById(position).value ="submit";
		    }
             

   }
}

function display(pos) 
{
   var refund_action = document.getElementById('sel'+pos).value;
   if (refund_action == "Partial Refund")
   {
     document.getElementById('refund'+pos).disabled = false;
	 document.getElementById('refund'+pos).value = "";
   }else{
   
	 document.getElementById('refund'+pos).disabled = true;
	 document.getElementById('refund'+pos).value = "";
   }
}



