#!/usr/bin/perl
require "include.cgi";
use Data::Dumper;
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_view_reports") ne 1) {adm_error("no permission"); exit;}
#=======================================================

#=======================================================
# main loop
#=======================================================
$my_url = "call_refund.cgi";
$action = $form{action};
if 		($action eq "refund")		{ &do_refund(); } 
else							{ &do_list(); }
exit;
#=======================================================

sub do_credit_add(){
	my($service_id, $value, $text) = @_;

		# confere valor
		$value++;
		$value--;
		#
		# adiciona o credito
				%order = ();
				$order{service_id}	= $service_id;
				$order{value_credit}= $value;
				$order{value_money}	= 0;
				$order{type}		= "FREE";
				$order{text}		= "$text";
				$order{ok}			= 0;
				%order = multilevel_credit_add(%order);
				
				if ($order{ok} eq 1)  {
					&action_history("noc:service:credit:free",('service_id'=>$service_id,'credit_id'=>$order{new_credit_id},'adm_user_id'=>$app{session_cookie_u}));
				}
				
	#SMS notification
	my %aniHash = database_select_as_hash("SELECT 1,ani from service_signin where service_id='$service_id'", "ani");
	$ani = $aniHash{1}{ani};
	my $joinmessage = "Zenofon just refunded you \$$value";
	&sendSMS_Twilio($ani,$joinmessage);
	return %order;
}

sub do_refund(){
	#$call_id = $form{call_id};
	$service_id = $form{service_id};
	$amount = $form{amount};
	$refundamount = $form{refundamount};
	$refund_id = $form{refund_id};
	$type = $form{type};
	print "Content-type: text/plain\n\n";
	
	$sql = "select 1,status from call_refund where id='$refund_id'";
	%hash = database_select_as_hash($sql, "status");
	if($hash{1}{status} ne "pending"){
		print "Invalid Refund - $sql";
		exit;
	}
	
	$sql = "update call_refund set status='$type' where id='$refund_id'";
	database_do($sql);
		
	if($type eq "decline"){
		
		$sql = qq[
			select 1, 1, cl.date, cl.dst
			from call_refund cr join calls cl on cl.id=cr.call_id
			where cr.id='$refund_id'
		];
		
		%hash = database_select_as_hash($sql, "flag,date,dst");

		$date = $hash{1}{date};
		$dst = $hash{1}{dst};
		
		my %aniHash = database_select_as_hash("SELECT 1,ani from service_signin where service_id='$service_id'", "ani");
		$ani = $aniHash{1}{ani};
		
		my $message = "Sorry, your refund request of \$$amount for the call to $dst on $date has been declined. For questions, please contact us at (917) 284-9450.";
		&sendSMS_Twilio($ani,$message);
	
		print "success";
		exit;
	}
	
	if($type eq "full"){
		#$sql = "update service set balance = balance+$amount where id='$service_id'";
		#database_do($sql);
		&do_credit_add($service_id, $amount, "refund Full");
		print "success";
		exit;
	}
	
	if($type eq "partial"){
		if($refundamount>$amount){
			print "Refund amount cannot be more than Call amount";
			exit;
		}
		#$sql = "update service set balance = balance+$refundamount where id='$service_id'";
		#database_do($sql);
		&do_credit_add($service_id, $refundamount, "refund partial");
		
		$sql = "update call_refund set amount=$refundamount where id='$refund_id'";
		database_do($sql);
		print "success";
		exit;
	}
	
	print "Refund type not recognised";
}

sub do_list(){
	%t = ();
	$t{dic}{title} = "[WEB] Call Refund";
	$type = $form{type};
	if($type eq ""){
		$type = "pending";
	}
	if($type eq "all"){
		$type = "%";
	}
	
	$sql = "select 1,count(*) from call_refund where status like '$type'";
	%hash = database_select_as_hash($sql, "time");
	$quantity = $hash{1}{time};
	$page_size		= clean_int($form{'page_size'});
	$page_size      = ($page_size eq "") ? 100 : $page_size;
	$page_min		= 1;
	$page_max		= int(($quantity-1)/$page_size)+1;
	$page_max		= ($page_max<$page_min) ? $page_min : $page_max;
	$page 			= clean_int($form{history_page});
	$page 			= ($form{next} eq 1) ? $page+1 : $page;
	$page 			= ($form{previous} eq 1) ? $page-1 : $page;
	$page 			= ($page<$page_min) ? $page_min : $page;
	$page 			= ($page>$page_max) ? $page_max : $page;
	$selected_start	= ($page-1)*$page_size;
	$selected_stop	= $selected_start+($page_size-1);


	$html_pg_list = "";
	foreach($page_min..$page_max) {
		if  ( ($_ eq $page_min) || ($_ eq $page_max) || (int($_/100) eq ($_/100) ) ||  ( ($page>($_-100)) && ($page<($_+100)) ) ) {
			$tmp = ($_ eq $page) ? "selected" : ""; 
			$html_pg_list .= "<option $tmp value=$_>Page: $_ of $page_max</option>";
		}
	}
    $html_pgsize_list = "";
    $tmp = (10 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=10>10 items per page</option>";
    $tmp = (30 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=30>30 items per page</option>";
    $tmp = (100 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=100>100 items per page</option>";
	
	
	$sql = qq[
		select 
		cr.id,cr.service_id, cr.call_id, cr.request_date, cr.status, cr.amount,
		s.name,
		c.date, ROUND(c.seconds/60, 2), Round(c.value, 4) as callcharge,
		ss.name
		from call_refund cr 
		join calls c on cr.call_id=c.id
		join service s on s.id=cr.service_id
		join service_status ss on ss.id=s.status
		where cr.status like '$type'
		limit $selected_start, $page_size
	];

	%hash = database_select_as_hash($sql, "service_id,call_id,date,status,amount,name,calldate,calltime,callcharge,serviceStatus");
	
	$pendingselected = $type eq "pending"?"selected":"";
	$fullselected = $type eq "full"?"selected":"";
	$partialselected = $type eq "partial"?"selected":"";
	$declineselected = $type eq "decline"?"selected":"";
	$allselected = $type eq "%"?"selected":"";
	    $t{dic}{content}	.= qq[
<select id="refundtype" onchange="refreshRefundList()">
<option $pendingselected value="pending">Pending</option>
<option $fullselected value="full">Full Refunded</option>
<option $partialselected value="partial">Partially Refunded</option>
<option $declineselected value="decline">Declined</option>
<option $allselected value="all">All</option>
</select>

<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; onclick="sortColumn(event)">  
<thead>
	<tr>
	<td colspan=11><h1>Call refund</h1></td>
	</tr>
	<tr>
	<td width=50>Id</td>
	<td >User Name</td>
	<td width=50>Call Id</td>
	<td  width=50>Call Time</td>
	<td >Call Duration</td>
	<td >Call Charge</td>
	<td >Refund Request Time</td>
	<td >Refund Status</td>
	<td >Refund Action</td>
	<td >Refund Amount</td>
	<td >Action</td>
	</tr>
	</thead>
];
	for $refundId(sort {$hash{$b}{date} <=> $hash{$a}{date}} keys %hash){
		$getName = $hash{$refundId}{name};
		$service_id = $hash{$refundId}{service_id};
		$i = $hash{$refundId}{call_id};
		$date = $hash{$refundId}{calldate};
		$seconds = $hash{$refundId}{calltime};
		$callcharge = $hash{$refundId}{callcharge};
		$value = $hash{$refundId}{amount};
		$refundDate = $hash{$refundId}{date};
		$status = $hash{$refundId}{status};
		$serviceStatus = $hash{$refundId}{serviceStatus};
		$seldisabled = "";
		$selected = "";
		if($status ne "pending"){
			$seldisabled = "disabled";
			$selected = "<option selected>$status</option>";
		}
		$t{dic}{content}	.= qq[
<tr>
<td><a id='service$refundId' target=_blank href = 'https://www.zenofon.com/noc/services.cgi?action=view&service_id=$service_id'>$service_id</a></td>
<td>$getName - $serviceStatus</td>
<td><span name='callid$refundId' id='callid$refundId'>$i</span></td>
<td>$date</td>
<td>$seconds</td>
<td><span name='rate$refundId' id='rate$refundId'>$callcharge</span></td>
<td>$refundDate</td>
<td><span id='refund_status$refundId'>$status</span></td>
<td>
<select name='selelectaction' id='sel$refundId' onchange="displayRefund($refundId)" $seldisabled>
$selected
<option value='pending'>Pending</option>
<option value='full'>Full Refund</option>
<option value='decline'>Decline</option>
<option value='partial'>Partial Refund</option>
</select></td>
<td><input type=text name='refund$refundId' id='refund$refundId' value='$value' disabled="true" size="10" ></td> ];

if ($status eq "pending")
{
$t{dic}{content}	.= qq[<td><input type='button' value='submit' name='submit$refundId' id='submit$refundId' onclick="doRefund($refundId)"></td>];
}
else
{
$t{dic}{content}	.= qq[<td><input type='button' value='Processed' name='submit$refundId' id='submit$refundId' disabled="true"></td>];
}
$t{dic}{content}	.= qq[</tr> ];

	}


        $t{dic}{content}.= qq[
        <tfoot>
		<tr><td colspan=11><form action='call_refund.cgi' method='get'>
		<input type=hidden name=action value=sms_refund>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td ><button type=submit name=previous value=1><img src=/design/icons/bullet_arrow_left.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
		<td ><select name=history_page onchange="this.form.submit()">$html_pg_list</select></td>
		<td ><select name='page_size' id='page_size' onchange="document.forms[0].submit()">$html_pgsize_list</select></td>
		<td ><button type=submit name=next value=1><img src=/design/icons/bullet_arrow_right.png hpace=0 vspace=0 border=0 width=16 height=16></button></td>
		</table></form>
		</td></tr>
        </tfoot>
</table>
</form>
</body>
</html>
];

	template_print("template.html", %t);
}
