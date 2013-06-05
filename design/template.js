function MyDisplay(id,flag)	{ 
	obj = document.getElementById(id);
	if (!obj) {return false}
	if ( (flag==1) || (flag==0) ) {
		if (flag == 1) {obj.style.display = "block"}
		if (flag == 0) {obj.style.display = "none"}
	} else {
		if (obj.style.display == "block") {obj.style.display = "none"} else {obj.style.display = "block"}
	}
}
function MyClass(id,newclass)	{
	obj = document.getElementById(id);
	if (!obj) {return false}
	obj.className = newclass;
}
function MyHTML(id,value) {
	obj = document.getElementById(id);
	if (!obj) {return false}
	obj.innerHTML  = value;
}
function balance_bar_set(v,p){
	b = (150*(p/100));
	if (b>150) {b=150}
	if (b<1) {b=1}
	html = "<div vlass=clear style='padding:20px;padding-right:50px;'><a href=login.cgi?action=logout><img src=/design/icons/cross.png hspace=0 vspace=0 border=0 align=right>Log-out</a></div>";
	html = "<div class=balance_message >Your balance is $"+v+"</div>";
	html += "<div class=balance_bar_external ><div class=balance_bar_internal style='width:"+b+"' ></div></div>";
	html += "<br clear=both><a href=./?action=credit>Add more credit</a>";
	MyHTML("balance_box",html);
}

function requestRefund(id, button){
	$(button).text("Sending refund request");
	$(button).attr("disabled","disabled");
	
	$.get("requestRefund.cgi?action=requestRefund&id="+id, function(d){
			if(d == "success"){
				alert("Refund Request. Please allow 3-4 Days to process your refund");
				$(button).text("Refund Requested");
			}else{
				alert("Refund Request failed, Please try again later");
				$(button).removeAttr("disabled");
				$(button).text("Request refund");
			}
	});
}