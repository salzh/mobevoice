#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_manage_checks") ne 1) {adm_error("no permission"); exit;}
#=======================================================



#=======================================================
# main loop
#=======================================================
$my_url = "commission.checks.cgi";
$action = $form{action};
if 		($action eq "accept")		{ &do_accept(); } 
elsif 	($action eq "cancel")		{ &do_cancel(); }
elsif 	($action eq "revert")		{ &do_revert(); }
elsif 	($action eq "view")			{ &do_view(); 	}
else								{ &do_list(); 	}
exit;
#=======================================================



#========================================================================
# actions
#========================================================================
sub do_accept(){
	#
	# confere request_id
	$request_id = clean_int(substr($form{request_id},0,100));
	%hash = database_select_as_hash("SELECT 1,1,status,service_id FROM service_commission_invoice where send_to='CHECK' and id ='$request_id' ","flag,status,service_id");
    if ($hash{1}{flag} ne 1) {adm_error("Unknown request_id");return}
    if ($hash{1}{status} ne 0) {adm_error("I cannot change due wrong status");return}
	#
	# acao
	database_do("update service_commission_invoice set status=1 where id ='$request_id' ");
	%counting = &database_select_as_hash("SELECT 1,1,count(*) FROM service_commission_invoice where send_to='CHECK' and service_id='$hash{1}{service_id}' and status=0","flag,value");
	if ( ($counting{1}{flag} eq 1) && ($counting{1}{value} eq 0) ) {
		&data_set("service_data",$hash{1}{service_id},"ss_flags",",DATA,");
	} else {
		&data_set("service_data",$hash{1}{service_id},"ss_flags",",");
	}
	&action_history("com:chk:aprove",('service_id'=>$hash{1}{service_id},'commission_invoice_id'=>$request_id,'adm_user_id'=>$app{session_cookie_u}));
	#
	# return
	&cgi_redirect("$my_url?action=list");
	#&cgi_redirect("$my_url?action=view&request_id=$request_id");
}
sub do_cancel(){
	#
	# confere request_id
	$request_id = clean_int(substr($form{request_id},0,100));
	%hash = database_select_as_hash("SELECT 1,1,status,service_id FROM service_commission_invoice where send_to='CHECK' and id ='$request_id' ","flag,status,service_id");
    if ($hash{1}{flag} ne 1) {adm_error("Unknown request_id");return}
    if ($hash{1}{status} ne 0) {adm_error("I cannot change due wrong status");return}
	#
	# acao
	database_do("update service_commission set invoice_id=null where invoice_id ='$request_id' ");
	database_do("update service_commission_invoice set status=-1 where id ='$request_id' ");
	%counting = &database_select_as_hash("SELECT 1,1,count(*) FROM service_commission_invoice where send_to='CHECK' and service_id='$hash{1}{service_id}' and status=0","flag,value");
	if ( ($counting{1}{flag} eq 1) && ($counting{1}{value} eq 0) ) {
		&data_set("service_data",$hash{1}{service_id},"ss_flags",",DATA,");
	} else {
		&data_set("service_data",$hash{1}{service_id},"ss_flags",",");
	}
	&action_history("com:chk:reject",('service_id'=>$hash{1}{service_id},'commission_invoice_id'=>$request_id,'adm_user_id'=>$app{session_cookie_u}));
	#
	# return
	&cgi_redirect("$my_url?action=list");
	#&cgi_redirect("$my_url?action=view&request_id=$request_id");
}
sub do_revert(){
	#
	# confere request_id
	$request_id = clean_int(substr($form{request_id},0,100));
	%hash = database_select_as_hash("SELECT 1,1,status,service_id FROM service_commission_invoice where send_to='CHECK' and id ='$request_id' ","flag,status,service_id");
    if ($hash{1}{flag} ne 1) {adm_error("Unknown request_id");return}
    if ($hash{1}{status} ne 1) {adm_error("I cannot change due wrong status");return}
	#
	# acao
	database_do("update service_commission_invoice set status=0 where id ='$request_id' ");
	%counting = &database_select_as_hash("SELECT 1,1,count(*) FROM service_commission_invoice where send_to='CHECK' and service_id='$hash{1}{service_id}' and status=0","flag,value");
	if ( ($counting{1}{flag} eq 1) && ($counting{1}{value} eq 0) ) {
		&data_set("service_data",$hash{1}{service_id},"ss_flags",",DATA,");
	} else {
		&data_set("service_data",$hash{1}{service_id},"ss_flags",",");		
	}
	&action_history("com:chk:unaprove",('service_id'=>$hash{1}{service_id},'commission_invoice_id'=>$request_id,'adm_user_id'=>$app{session_cookie_u}));
	#
	# return
	#&cgi_redirect("$my_url?action=list");
	&cgi_redirect("$my_url?action=view&request_id=$request_id");
}
sub do_list(){
	#
	# pega dados das ids
	$sql = "
	SELECT 
		service_commission_invoice.id,
		service.name,
		service_status.name,
		unix_timestamp(service_commission_invoice.creation_date),
		service_commission_invoice.status,
		service_commission_invoice.value
	FROM 
		service_commission_invoice,
		service,
		service_status
	where 
		service_commission_invoice.send_to='CHECK' 
		and service_commission_invoice.service_id = service.id 
		and service.status = service_status.id
	order by 
		service_commission_invoice.creation_date desc
	limit 0,200
	";
	$html = ""; 
	%hash = database_select_as_hash($sql,"service_name,service_status,date,status,value");
	foreach $id (sort{$hash{$b}{date} <=> $hash{$a}{date}} keys %hash) {
		$link =  "<a href=$my_url?action=view&request_id=$id>";
		$html .= "<tr>"; 
		$html .= "<td>$link".&format_time_time($hash{$id}{date})."</a></td>"; 
		$html .= "<td>$link$hash{$id}{service_name}</a></td>"; 
		$html .= "<td>$link$hash{$id}{service_status}</a></td>";
		$tmp = "<td >(unknown)</td>";
		$tmp = ($hash{$id}{status} eq  0) ? "<td style=background-color:red;color:#ffffff><b>Wait action</b></td>" : $tmp ;
		$tmp = ($hash{$id}{status} eq  1) ? "<td ><img src=/design/icons/tick.png align=left>Aproved</td>" : $tmp ;
		$tmp = ($hash{$id}{status} eq -1) ? "<td ><img src=/design/icons/cancel.png align=left>Rejected</td>" : $tmp ;
		$html .= $tmp;
		$html .= "<td class=ar>$link\$".&format_number($hash{$id}{value},2)."</a></td>"; 
		$html .= "</tr>"; 
	}
    #
    # print page
    %t = ();
    $t{dic}{title}		= "Settings &#187; <a href=$my_url>Commissions checks</a>";
    $t{dic}{content}	= qq[
		<br>
		
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable xxwidth=100% onclick="sortColumn(event)">
			<thead>
				<tr>
				<td rowspan=2>Date</td>
				<td colspan=2>Service</td>
				<td colspan=2>Check request</td>
				</tr>
				<tr>
				<td>Name</td>
				<td>Status</td>
				<td>Status</td>
				<td>Value</td>
				</tr>
			</thead>
			<tbody>
				$html
			</tbody>
		</table>
		<br>
		Show only last 200 recent "check requests"
	];
    &template_print("template.html",%t);
    
}
sub do_view(){
    #
    # start some things
    $request_id = clean_int(substr($form{request_id},0,100));
    #
    # pega dados
	$sql = "
	SELECT
		1,1,
		service_commission_invoice.id,
		service.id,
		service.name,
		service_status.name,
		unix_timestamp(service_commission_invoice.creation_date),
		service_commission_invoice.status,
		service_commission_invoice.value
	FROM 
		service_commission_invoice,
		service,
		service_status
	where 
		service_commission_invoice.send_to='CHECK' 
		and service_commission_invoice.service_id = service.id 
		and service.status = service_status.id
		and service_commission_invoice.id = '$request_id'
	";
	%hash = database_select_as_hash($sql,"flag,id,service_id,service_name,service_status,date,status,value");
	%data = %{$hash{1}};
	#
	# se nao tem, para
    if ($data{flag} ne 1) {adm_error("Unknown request_id");return}
	#
	# pega address
	foreach (qw(paypal country name bname addr1 addr2 city state zip)) {
		$data{$_} = &data_get("service_data",$data{service_id},"ss_$_");
	}
	#
	# pega history
	$sql = "
	SELECT action_log.id,unix_timestamp(action_log.date),action_log.adm_user_id,action_log_type.title
	FROM action_log,action_log_type
	where action_log.commission_invoice_id=$request_id and action_log.type=action_log_type.id 
	";
	%hash = database_select_as_hash($sql,"date,adm_user_id,title");
	%adm_user_names = database_select_as_hash("select id,web_user from adm_users  ");
	$data{history} = "";
	foreach $id (sort{$hash{$a}{date} <=> $hash{$b}{date}} keys %hash) {
		$noc_user = (exists($adm_user_names{$hash{$id}{adm_user_id}})) ? " (by $adm_user_names{$hash{$id}{adm_user_id}})" : "";
		$data{history} .= &format_time_time($hash{$id}{date})." - $hash{$id}{title} $noc_user<br>";
	}
	#
	# get SSN
	#$ssn = multilevel_securedata_ss_get($data{service_id});
    #
    # print start page
    %t = ();
	$data{status_string} = "(unknown)";
	$data{status_string} = ($data{status} eq  0) ? "Wait action" : $data{status_string};
	$data{status_string} = ($data{status} eq  1) ? "Aproved" : $data{status_string};
	$data{status_string} = ($data{status} eq -1) ? "Rejected" : $data{status_string};
	$data{value_string} = &format_number($data{value},2);
    $t{dic}{title}	= "Settings &#187; <a href=$my_url>Commissions checks</a> &#187; View";
    $t{dic}{content}= qq[
		<br>
		Service name: <a href=services.cgi?service_id=$data{service_id}&action=view_commissions>$data{service_name} (View)</a><br>
		Service status: $data{service_status} <br>
		Check value: \$$data{value_string}<br>
		Check status: $data{status_string}<br>
		<br>
		<!-- Social security: $ssn ($data{ss})<br> -->
		Paypal: $data{paypal}<br>
		Name: $data{name}<br>
		Address 1: $data{addr1}<br>
		Address 2: $data{addr2}<br>
		City: $data{city}<br>
		State: $data{state}<br>
		Country: $data{country}<br>
		Zip: $data{zip}<br>
		<br>
		$data{history}
		<br>
		<table><tr>
		<td>
			<form action$my_url>
			<button align=left type=submit><img src=/design/icons/arrow_left.png align=left>Back</button>
			<input type=hidden name=action value=list>
			</form>
		</td>
	];
	#
	# print actions
	if ($data{status} eq  0) {
	    $t{dic}{content} .= qq[
		<td>
			<form action$my_url>
			<button align=left type=submit><img src=/design/icons/tick.png align=left>Aprove</button>
			<input type=hidden name=request_id value=$request_id>
			<input type=hidden name=action value=accept>
			</form>
		</td>
		<td>
			<form action$my_url onsubmit="return confirm('Do you really want reject? No way to undo after reject.');">
			<button align=left type=submit ><img src=/design/icons/cancel.png align=left>Reject</button>
			<input type=hidden name=request_id value=$request_id>
			<input type=hidden name=action value=cancel>
			</form>
		</td>
		];
	} elsif ($data{status} eq 1) {
	    $t{dic}{content} .= qq[
		<td>
			<form action$my_url>
			<button align=left type=submit><img src=/design/icons/tick.png align=left>Un-aprove</button>
			<input type=hidden name=request_id value=$request_id>
			<input type=hidden name=action value=revert>
			</form>
		</td>
		];
	}
	#
	# print
	$t{dic}{content} .= qq[
		</tr></table><br>
	];
    &template_print("template.html",%t);
    
}
#========================================================================




