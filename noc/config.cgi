#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
#if (adm_security_check("can_system_config") ne 1) {adm_error("no permission"); exit;}
#=======================================================





#=======================================================
# main loop
#=======================================================
$folder_rrd_data	= "/usr/local/multilevel/data/rrd/";
$my_url 			= "config.cgi";
$action 			= $form{action};
if 		($action eq "service_status_edit")		{ if (&active_user_permission_check("noc:can_manage_status") ne 1) {adm_error("no permission"); exit;}	&do_service_status_edit(); 		} 
elsif 	($action eq "service_status_list")		{ if (&active_user_permission_check("noc:can_manage_status") ne 1) {adm_error("no permission"); exit;}	&do_service_status_list(); 		} 
elsif 	($action eq "service_status_matrix")	{ if (&active_user_permission_check("noc:can_manage_status") ne 1) {adm_error("no permission"); exit;}	&do_service_status_matrix(); 	} 
#========================================================================
elsif 	($action eq "tmp_dst_block")			{ if (&active_user_permission_check("noc:can_manage_status") ne 1) {adm_error("no permission"); exit;}	&do_tmp_dst_block(); 			} 
elsif 	($action eq "suspicious_ips")			{ if (&active_user_permission_check("noc:can_manage_security") ne 1) {adm_error("no permission"); exit;}	&do_suspicious_ips(); 	} 
#========================================================================
elsif 	($action eq "commissions_OLD")							{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&OLD_do_commissions(); 							} 
elsif 	($action eq "commissions")								{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commissions(); 								} 
elsif 	($action eq "commission_type_add")						{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_add(); 						} 
elsif 	($action eq "commission_type_edit")						{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_edit();	 					} 
elsif 	($action eq "commission_type_del")						{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_del(); 						} 
elsif 	($action eq "commission_type_age")						{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_age(); 						} 
elsif 	($action eq "commission_type_age_edit")					{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_age_edit(); 				} 
elsif 	($action eq "commission_type_by_call_number")			{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_by_call_number(); 			} 
elsif 	($action eq "commission_type_by_call_number_add")		{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_by_call_number_add(); 		} 
elsif 	($action eq "commission_type_by_call_number_edit")		{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_by_call_number_edit(); 		} 
elsif 	($action eq "commission_type_by_call_number_del")		{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_by_call_number_del(); 		} 
elsif 	($action eq "commission_type_by_call_number_download")	{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_by_call_number_download(); 	} 
elsif 	($action eq "commission_type_by_call_number_upload")	{ if (&active_user_permission_check("noc:can_manage_commissions") ne 1) {adm_error("no permission"); exit;}	&do_commission_type_by_call_number_upload(); 	} 
#========================================================================
elsif 	($action eq "coupons_list")				{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}		&do_coupons_list();			}
elsif 	($action eq "coupons_edit")				{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}		&do_coupons_edit();			}
elsif 	($action eq "coupons_stock_generate")	{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}		&do_coupons_stock_generate();	}
elsif 	($action eq "coupons_stock_enable")		{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}		&do_coupons_stock_enable();	}
elsif 	($action eq "coupons_stock_disable")	{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}		&do_coupons_stock_disable();	}
elsif 	($action eq "coupons_stock_delete")		{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}		&do_coupons_stock_delete();	}
#========================================================================
elsif 	($action eq "agestatus_list")			{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}     &do_agestatus_list();			}
elsif 	($action eq "agestatus_edit")			{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}     &do_agestatus_edit();			}
elsif 	($action eq "agestatus_add")			{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}     &do_agestatus_add();			}
elsif 	($action eq "agestatus_del")			{ if (&active_user_permission_check("noc:can_manage_coupons") ne 1) {adm_error("no permission"); exit;}     &do_agestatus_del();			}
#========================================================================
else											{ &do_select(); 				}
exit;
#=======================================================


#========================================================================
# actions
#========================================================================
sub do_select(){
	#
	&cgi_redirect("index.cgi#settings");
	exit;
	#
    #
    # print page
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "System settings";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{content}	= qq[
	
	<style>
	.local_div{
		padding:0px;
		margin:0px;
		border:0px;
		float:left; 
		margin-right:10px; 
		margin-bottom:15px;
	}
	.local_fieldset {
		margin:0px;
		padding:10px;
		width:200px;
		height:150px;
	}
	</style>
	
	<div class=local_div><fieldset class=local_fieldset><legend>Phone services</legend>
		<a target=_top href="config.cgi?action=service_status_matrix"	>&#187; Status and permissions</a>
		<!-- 
		<a target=_top href="config.cgi?action=service_status_list"		>(old)</a> 
		-->
		<br>
		<a target=_top href="config.cgi?action=agestatus_list"			>&#187; Services age status</a><br>
		<a target=_top href="rate.cgi"									>&#187; Calls rates and routes</a><br>
		<a target=_top href="config.cgi?action=commissions"				>&#187; Commissions type</a> <a target=_top href="config.cgi?action=commissions_OLD">(old)</a><br>
		<a target=_top href="commission.checks.cgi"						>&#187; Commissions checks</a><br>
		<a target=_top href="config.cgi?action=coupons_list"			>&#187; Promotions</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Noc access</legend>
		<a target=_top href="system.access.cgi">NOC permissions</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Radio</legend>
		<a target=_top href="radio.ney.cgi?action=radio_stations"			>&#187; Radio stations</a><br>
		<a target=_top href="radio.ney.cgi?action=radio_commissions_listen"	>&#187; Radio listen commissions</a><br>
		<a target=_top href="radio.ney.cgi?action=radio_commissions_owner"	>&#187; Radio owner commissions</a><br>
		<a target=_top href="radio.ney.cgi?action=radio_tags"				>&#187; Radio tags</a><br>
		<a target=_top href="radio.cgi"										>&#187; (OLD) Radio Stations</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Security</legend>
		<a target=_top href="config.cgi?action=tmp_dst_block"			>&#187; Temporary DST block</a><br>
		<a target=_top href="config.cgi?action=suspicious_ips"			>&#187; Suspicious ips</a><br>
		<a target=_top onclick="alert('Under construction')" href=# 	>&#187; Banned credit cards</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Email</legend>
		<a target=_top href="email.edit.cgi"							>&#187; Automatic email messages</a><br>
		<a target=_top href="email.send.cgi"							>&#187; Send mass email</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Website</legend>
		<a target=_top href="website.help.cgi"							>&#187; Website help</a><br>
		<a target=_top href="website.pages.cgi"							>&#187; Website pages</a><br>
		<a target=_top href="index.cgi?action=set_frame&title=Zenofon+news&url=/news/wp-admin/">&#187; Website news (blog)</a><br>
	</fieldset></div>




<br clear=both>&nbsp;

	];
    &template_print("template.html",%t);
	
}
#========================================================================
sub do_coupons_stock_delete(){
	#
	#----------------------------------------------
	# verifica coupon_id
	#----------------------------------------------
	$coupon_id = clean_int(substr($form{coupon_id},0,100));
	%hash = database_select_as_hash("select 1,1,title,auto_pause_engine from service_coupon_type where id='$coupon_id' ","flag,title,engine");
	if ($hash{1}{flag} ne 1) {%t=(); $t{dic}{content}="Incorrect coupon type $coupon_id"; &template_print("template.modal.html",%t); exit;}
	$coupon_title = $hash{1}{title};
	$coupon_engine = $hash{1}{engine};
	#
	#----------------------------------------------
	# get count
	#----------------------------------------------
	$sql = "select 1,1,count(*) from service_coupon_stock where status=0 and coupon_type_id='$coupon_id'";
	%hash = database_select_as_hash($sql,"flag,qtd");
	$coupon_qtd = ($hash{1}{flag} eq 1) ? $hash{1}{qtd} : 0;
	#
	#----------------------------------------------
	# check and save
	#----------------------------------------------
	$msg = "";
	if ( &multilevel_clickchain_check("ccsg",$form{save}) eq 1 ) {
		$qtd = clean_int($form{qtd});
		if ( ($qtd ne "") && ($qtd eq $form{qtd}) && ($qtd>0) && ($qtd<5001) ) {
			&database_do("delete from service_coupon_stock where service_coupon_stock.status=0 and coupon_type_id='$coupon_id' limit $qtd ");
		}
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$clickchain_id = &multilevel_clickchain_set("ccsg");
	%t = ();
	$tmp = &format_number($coupon_qtd);
    $t{dic}{content}	= qq[
	You have $tmp '$coupon_title' coupons ready to delete.
	Select how many coupons do you want delete.<br>
	<br>
	<form action=$my_url >
	<select name=qtd>
	<option value=10>Delete 10 'New - Disabled' coupons</option>
	<option value=100>Delete 100 'New - Disabled' coupons</option>
	<option value=500>Delete 500 'New - Disabled' coupons</option>
	<option value=1000>Delete 1000 'New - Disabled' coupons</option>
	<option value=5000>Delete 5000 'New - Disabled' coupons</option>
	</select><br>
	<br>
	<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
	<button type=submit class="button button_positive button_save"   >Delete coupons</button>
	<input type=hidden name=start value=0>
	<input type=hidden name=coupon_id value=$coupon_id>
	<input type=hidden name=action value=coupons_stock_delete>
	<input type=hidden name=save value=$clickchain_id>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_coupons_stock_disable(){
	#
	#----------------------------------------------
	# verifica coupon_id
	#----------------------------------------------
	$coupon_id = clean_int(substr($form{coupon_id},0,100));
	%hash = database_select_as_hash("select 1,1,title,auto_pause_engine from service_coupon_type where id='$coupon_id' ","flag,title,engine");
	if ($hash{1}{flag} ne 1) {%t=(); $t{dic}{content}="Incorrect coupon type $coupon_id"; &template_print("template.modal.html",%t); exit;}
	$coupon_title = $hash{1}{title};
	$coupon_engine = $hash{1}{engine};
	#
	#----------------------------------------------
	# get count
	#----------------------------------------------
	$sql = "select 1,1,count(*) from service_coupon_stock where status=1 and coupon_type_id='$coupon_id'";
	%hash = database_select_as_hash($sql,"flag,qtd");
	$coupon_qtd = ($hash{1}{flag} eq 1) ? $hash{1}{qtd} : 0;
	#
	#----------------------------------------------
	# check and save
	#----------------------------------------------
	$msg = "";
	if ( &multilevel_clickchain_check("ccsg",$form{save}) eq 1 ) {
		$qtd = clean_int($form{qtd});
		if ( ($qtd ne "") && ($qtd eq $form{qtd}) && ($qtd>0) && ($qtd<5001) ) {
			&database_do("update service_coupon_stock set service_coupon_stock.status=0 where service_coupon_stock.status=1 and coupon_type_id='$coupon_id' limit $qtd ");
		}
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$clickchain_id = &multilevel_clickchain_set("ccsg");
	%t = ();
	$tmp = &format_number($coupon_qtd);
    $t{dic}{content}	= qq[
	You have $tmp '$coupon_title' coupons ready to disable.
	Select how many coupons do you want disable.<br>
	<br>
	<form action=$my_url >
	<select name=qtd>
	<option value=10>Disable 10 'New - Free to use' coupons</option>
	<option value=100>Disable 100 'New - Free to use' coupons</option>
	<option value=500>Disable 500 'New - Free to use' coupons</option>
	<option value=1000>Disable 1000 'New - Free to use' coupons</option>
	<option value=5000>Disable 5000 'New - Free to use' coupons</option>
	</select><br>
	<br>
	<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
	<button type=submit class="button button_positive button_save"   >Disable coupons</button>
	<input type=hidden name=start value=0>
	<input type=hidden name=coupon_id value=$coupon_id>
	<input type=hidden name=action value=coupons_stock_disable>
	<input type=hidden name=save value=$clickchain_id>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_coupons_stock_enable(){
	#
	#----------------------------------------------
	# verifica coupon_id
	#----------------------------------------------
	$coupon_id = clean_int(substr($form{coupon_id},0,100));
	%hash = database_select_as_hash("select 1,1,title,auto_pause_engine from service_coupon_type where id='$coupon_id' ","flag,title,engine");
	if ($hash{1}{flag} ne 1) {%t=(); $t{dic}{content}="Incorrect coupon type $coupon_id"; &template_print("template.modal.html",%t); exit;}
	$coupon_title = $hash{1}{title};
	$coupon_engine = $hash{1}{engine};
	#
	#----------------------------------------------
	# get count
	#----------------------------------------------
	$sql = "select 1,1,count(*) from service_coupon_stock where status=0 and coupon_type_id='$coupon_id'";
	%hash = database_select_as_hash($sql,"flag,qtd");
	$coupon_qtd = ($hash{1}{flag} eq 1) ? $hash{1}{qtd} : 0;
	#
	#----------------------------------------------
	# check and save
	#----------------------------------------------
	$msg = "";
	if ( &multilevel_clickchain_check("ccsg",$form{save}) eq 1 ) {
		$qtd = clean_int($form{qtd});
		if ( ($qtd ne "") && ($qtd eq $form{qtd}) && ($qtd>0) && ($qtd<5001) ) {
			&database_do("update service_coupon_stock set service_coupon_stock.status=1 where service_coupon_stock.status=0 and coupon_type_id='$coupon_id' limit $qtd ");
		}
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$clickchain_id = &multilevel_clickchain_set("ccsg");
	%t = ();
	$tmp = &format_number($coupon_qtd);
    $t{dic}{content}	= qq[
	You have $tmp '$coupon_title' coupons ready to enable.
	Select how many coupons do you want enable.<br>
	<br>
	<form action=$my_url >
	<select name=qtd>
	<option value=10>Enable 10 'New - Disabled' coupons</option>
	<option value=100>Enable 100 'New - Disabled' coupons</option>
	<option value=500>Enable 500 'New - Disabled' coupons</option>
	<option value=1000>Enable 1000 'New - Disabled' coupons</option>
	<option value=5000>Enable 5000 'New - Disabled' coupons</option>
	</select><br>
	<br>
	<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
	<button type=submit class="button button_positive button_save"   >Enable coupons</button>
	<input type=hidden name=start value=0>
	<input type=hidden name=coupon_id value=$coupon_id>
	<input type=hidden name=action value=coupons_stock_enable>
	<input type=hidden name=save value=$clickchain_id>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_coupons_stock_generate(){
	#
	#----------------------------------------------
	# verifica coupon_id
	#----------------------------------------------
	$coupon_id = clean_int(substr($form{coupon_id},0,100));
	%hash = database_select_as_hash("select 1,1,title,auto_pause_engine from service_coupon_type where id='$coupon_id' ","flag,title,engine");
	if ($hash{1}{flag} ne 1) {%t=(); $t{dic}{content}="Incorrect coupon type $coupon_id"; &template_print("template.modal.html",%t); exit;}
	$coupon_title = $hash{1}{title};
	$coupon_engine = $hash{1}{engine};
	#
	#----------------------------------------------
	# check and save
	#----------------------------------------------
	$msg = "";
	if ( &multilevel_clickchain_check("ccsg",$form{save}) eq 1 ) {
		%t = ();
		$stop = clean_int($form{stop});
		$now = clean_int($form{start});
		$t{dic}{content} = "now=$now stop=$stop <br>";
		if ( ($stop ne $form{stop}) || ($now ne $form{start}) || ($stop eq "") || ($now eq "") ) {
			$t{dic}{content} .= "error <script>parent.error();</script>";
		} else {
			foreach (1..1000) {
				&database_do("insert into service_coupon_stock (coupon_type_id,status) values ('$coupon_id','0')");
				$now++;
				if ($now>=$stop) {last}
			}
			if ($now>=$stop) {
				$t{dic}{content} .= "finish <script>parent.finish();</script>";
			} else {
				$id = &multilevel_clickchain_set("ccsg");
				$t{dic}{content} .= "update <script>parent.update($now,$stop,'$id');</script>";
			}
		}
		&template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$clickchain_id = &multilevel_clickchain_set("ccsg");
	%t = ();
    $t{dic}{content}	= qq[
	
		<div id=g_form>
			<form action=$my_url target=io onSubmit="return generate_coupons('');">
			<select name=stop>
			<option value=10>Create 10 'New - Disabled' coupons</option>
			<option value=100>Create 100 'New - Disabled' coupons</option>
			<option value=500>Create 500 'New - Disabled' coupons</option>
			<option value=1000>Create 1000 'New - Disabled' coupons</option>
			<option value=5000>Create 5000 'New - Disabled' coupons</option>
			</select><br>
			<br>
			<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
			<button type=submit class="button button_positive button_save"   >Generate coupons</button>
			<input type=hidden name=start value=0>
			<input type=hidden name=coupon_id value=$coupon_id>
			<input type=hidden name=action value=coupons_stock_generate>
			<input type=hidden name=save value=$clickchain_id>
			</form>
		</div>

		<div id=g_working style=display:none>
			<div class=alert_box ><div><b>Warning:</b> System is workin. Do not close this window. </div></div><br>
			<br>
			<div id=g_working_msg style="padding:20px;">
			<img src=design/loading.gif align=left> Please wait...
			</div>
			<br clear=both>
		</div>

		
		<form action=$my_url target=io style=display:none>
		<input type=hidden name=start value=>
		<input type=hidden name=stop value=>
		<input type=hidden name=save value=>
		<input type=hidden name=coupon_id value=$coupon_id>
		<input type=hidden name=action value=coupons_stock_generate>
		</form>
		<iframe src=design/blank.html name=io id=io class=clear style=display:none></iframe>
		<script>
		function generate_coupons(){
			if (!confirm('Generate coupons take some time. You cannot close this window. Do you want generate coupons?')) {return false}
			MyDisplay("g_form",0);
			MyDisplay("g_working",1);
			return true;
		}
		function update(start,stop,id){
			MyHTML("g_working_msg","<img src=design/loading.gif align=left> Please wait ("+start+" of "+stop+")...");
			document.forms[1].elements[0].value=start;
			document.forms[1].elements[1].value=stop;
			document.forms[1].elements[2].value=id;
			document.forms[1].submit();
		}
		function finish(){
			MyDisplay("g_working",0);
			alert('Coupons created!');
			parent.modal_parent_reload();
		}
		function error(){
			MyDisplay("g_working",0);
			alert('Syetem error!');
			parent.modal_parent_reload();
		}
		</script>
		
    ];
    &template_print("template.modal.html",%t);
}
sub do_coupons_edit(){
	#
	#----------------------------------------------
	# verifica coupon_id
	#----------------------------------------------
	$coupon_id = clean_int(substr($form{coupon_id},0,100));
	%hash = database_select_as_hash("select 1,1,title,auto_pause_engine,ui_msg_in_stock,ui_msg_out_stock,ui_msg_assigned from service_coupon_type where id='$coupon_id' ","flag,title,engine,ui_msg_in_stock,ui_msg_out_stock,ui_msg_assigned");
	if ($hash{1}{flag} ne 1) {cgi_redirect("$my_url?action=coupons_list"); exit;}
	$coupon_title = $hash{1}{title};
	$coupon_engine = $hash{1}{engine};
	$coupon_msg_in_stock 	= $hash{1}{ui_msg_in_stock};
	$coupon_msg_out_stock 	= $hash{1}{ui_msg_out_stock};
	$coupon_msg_assigned	= $hash{1}{ui_msg_assigned};
	%form_error = ();
	$form_error_flag = 0;
	$error_style = "style='background-color:red;color:#ffffff;'";
	#
	#----------------------------------------------
	# check and save
	#----------------------------------------------
	if ( &multilevel_clickchain_check("cce",$form{save}) eq 1 ) {
		#
		# textareas
		foreach $name (qw(msg_in_stock msg_out_stock msg_assigned)) {
			$form{$name} = trim(clean_str(substr($form{$name},0,65536),"\@.,! /\$?*<>;[]()=_-:\n"));
			$tmp1="\r"; $tmp2="\n"; 	$form{$name} =~ s/$tmp1/$tmp2/eg; 
			$tmp1="\n"; $tmp2="<br>";	$form{$name} =~ s/$tmp1/$tmp2/eg;
		}
		#
		# strings not empty
		foreach $name (qw(title)) {
			$value = clean_str(substr($form{$name},0,1000),"(\$)");
			if(  ($value eq "") ||  ($value ne $form{$name})) {
				$form_error_flag = 1;
				$form_error{$name} = $error_style;
			} 
		}
		#
		# verifica os steps
		foreach $s (1..10) {
			$n1 = "slice_".$s."_value"; 
			$n2 = "slice_".$s."_delay"; 
			$n3 = "slice_".$s."_title";
			$v1 = &clean_float(substr($form{$n1},0,100));
			$v2 = &clean_int(substr($form{$n2},0,100));
			$v3 = &clean_str(substr($form{$n3},0,100));
			if ($v1.$v2 eq "") {
				$form{$n3} = "";
			} else {
				if (
				($v1 eq "") || ($v2 eq "") || ($v3 eq "") || 
				($v1 ne $form{$n1}) || ($v2 ne $form{$n2}) || ($v3 ne $form{$n3})
				) {
					$form_error_flag = 1;
					$form_error{$n1} = $error_style;
					$form_error{$n2} = $error_style;
					$form_error{$n3} = $error_style;
				} 
			}
		}
		#
		# verifica engine
		$form{engine} = (index("|autorecharge|","|$form{engine}|") eq -1) ? "" : $form{engine};
		#
		# tenta save
		if ($form_error_flag ne 1) {
			&database_do("update service_coupon_type set title='$form{title}', auto_pause_engine='$form{engine}' where id='$coupon_id'");
			&database_do("update service_coupon_type set ui_msg_in_stock='$form{msg_in_stock}' where id='$coupon_id'");
			&database_do("update service_coupon_type set ui_msg_out_stock='$form{msg_out_stock}' where id='$coupon_id'");
			&database_do("update service_coupon_type set ui_msg_assigned='$form{msg_assigned}' where id='$coupon_id'");
			@sqls = ();
			@sqls = (@sqls,"delete from service_coupon_type_slice where coupon_type_id='$coupon_id' ");
			$sequence = 1;
			foreach $s (1..10) {
				$v = $form{"slice_".$s."_value"};
				$d = $form{"slice_".$s."_delay"};
				$t = $form{"slice_".$s."_title"};
				if ($v.$d eq "") {next}
				$sql = "
				insert into service_coupon_type_slice
				( coupon_type_id, sequence,    title, type,   delay_in_hours, value ) values
				( '$coupon_id',   '$sequence', '$t',  'FREE', '$d',           '$v'  )
				";
				@sqls = (@sqls,$sql);
				$sequence++;				
			}
			foreach (@sqls) {database_do($_)}
			cgi_redirect("$my_url?action=coupons_list");
			exit;
		}
		#
	}
	#
	#----------------------------------------------
	# load
	#----------------------------------------------
	if ( $form{save} eq "") {
		$sql = "
		SELECT 
		service_coupon_type_slice.sequence,
		service_coupon_type_slice.value,
		service_coupon_type_slice.delay_in_hours,
		service_coupon_type_slice.title
		FROM service_coupon_type,service_coupon_type_slice
		where service_coupon_type_slice.coupon_type_id = service_coupon_type.id 
		and service_coupon_type.id='$coupon_id'
		";
		%hash = database_select_as_hash($sql,"value,delay,title");
		foreach $id (keys %hash){
			$form{"slice_".$id."_value"} = $hash{$id}{value};
			$form{"slice_".$id."_delay"} = $hash{$id}{delay};
			$form{"slice_".$id."_title"} = $hash{$id}{title};
		}
		$form{title} 	= $coupon_title;
		$form{engine}	= $coupon_engine;
		$form{msg_in_stock}	= $coupon_msg_in_stock;
		$form{msg_out_stock}= $coupon_msg_out_stock;
		$form{msg_assigned}	= $coupon_msg_assigned;
		$tmp1="<br>"; $tmp2="\n"; $form{msg_in_stock} =~ s/$tmp1/$tmp2/eg; 
		$tmp1="<br>"; $tmp2="\n"; $form{msg_out_stock} =~ s/$tmp1/$tmp2/eg; 
		$tmp1="<br>"; $tmp2="\n"; $form{msg_assigned} =~ s/$tmp1/$tmp2/eg; 
	}
	#
	#----------------------------------------------
	# pega inventario
	#----------------------------------------------
	$sql = "
	select service_coupon_stock_status.title,count(*)
	from service_coupon_stock,service_coupon_stock_status
	where service_coupon_stock.status= service_coupon_stock_status.id and service_coupon_stock.coupon_type_id='$coupon_id'
	group by service_coupon_stock_status.title
	";
	$html_status = "";
	%hash = database_select_as_hash($sql,"qtd");
	$tot = 0;
	foreach (sort{$a cmp $b} keys %hash) {
		$html_status .= &format_number($hash{$_}{qtd},0)." coupons '$_'<br>";
		$tot += $hash{$_}{qtd};
	}
	$html_total = &format_number($tot,0)." coupons at total";
	$sql = "
	select 1,1,count(*)
	from service_coupon_stock,service_coupon_stock_status
	where service_coupon_stock.status=service_coupon_stock_status.id
	and service_coupon_stock_status.is_ready_to_assign=1
	and service_coupon_stock.coupon_type_id='$coupon_id'
	";
	%hash = database_select_as_hash($sql,"flag,qtd");
	$html_available = 0;
	$html_warning = "<div class=alert_box ><div><b>Warning:</b> I cannot determine if we have available coupons in stock</div></div><br>";
	if ($hash{1}{flag} eq 1) {
		$html_available = &format_number($hash{1}{qtd},0);
		if ($hash{1}{qtd} <= 0) {
			$html_warning = "<div class=alert_box ><div style=\"background-image:url(/design/icons/delete.png);\"><b>Error:</b> No coupons available in stock to assign.</div></div><br>";
		} elsif ($hash{1}{qtd} < 200) {
			$html_warning = "<div class=alert_box ><div><b>Warning:</b> Low stock ($html_available itens) of coupons available to assign.</div></div><br>";
		} else {
			$html_warning = "<div class=alert_box ><div style=\"background-image:url(/design/icons/tick.png);\">$html_available coupons available</div></div><br>";
		}
	}


	#
	#----------------------------------------------
	# arruma formulario
	#----------------------------------------------
	%form_engine = ();
	$form_engine{$form{engine}} = "selected";
	$form_error_message = ($form_error_flag eq 1) ? "<font color=red><b>Error!</b> I cannot save! Please check red fields</font><br><br>" : ""; 
	#
	#----------------------------------------------
	# monta pagina
	#----------------------------------------------
	$clickchain_id = &multilevel_clickchain_set("cce");
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url>Settings</a> &#187; <a href=$my_url?action=coupons_list>Promotion</a> &#187; '$coupon_title'";
    $t{dic}{content}	= qq[

		<style>
		.xxfields_group_table {
			border:1px solid #c0c0c0;
			background-color:#f0f0f0;
			padding-right:4px;
		}
		.xxfields_group_table td {
			font-size:10px;
			padding:1px;
			}
		.xxfields_group_table td input{
			font-size:10px;
			border: 1px solid #e0e0e0;
			height:16px;
			padding:1px;
			margin:0px;
			width:100%;
		}
		.fields_group_table td input{
			width:100%;
		}
		</style>



		<div class=clear style="float:left; border-right:1px solid #e0e0e0; margin-right:20px; padding-right:20px;">
		<div class=clear style="width:520px;">
			<form action=$my_url class=clear>
			<fieldset class=config_group><legend>Promotion settings</legend>
				<div><h1>Title</h1					>Public title for <br>this coupon type<br 		><br><input $form_error{title}  type=text name=title value="$form{title}" style=width:100%></div>
				<div><h1>Engine</h1>Engine to control promotion and coupons policies<br 			><br><select name=engine style=width:100%><option value=""> (Manual)</option><option $form_engine{autorecharge} value="autorecharge">by auto-recharge status.</option></select></div>
			</fieldset>
			<fieldset class=config_group><legend>Messages</legend>
				<div style="height:auto;"><h1>Message 1</h1	>In stock coupon details. Used in sign-in for new service and auto recharge coupon<textarea style="font-size:9px;width:100%;height:100px;" name=msg_in_stock>$form{msg_in_stock}</textarea></div>
				<div style="height:auto;"><h1>Message 2</h1	>Out of stock coupon details in sign-in form or top banner for auto-recharge coupon<textarea style="font-size:9px;width:100%;height:100px;" name=msg_out_stock>$form{msg_out_stock}</textarea></div>
				<div style="height:auto;"><h1>Message ok</h1>Sucessfully assigned coupon message<textarea style="font-size:9px;width:100%;height:100px;" name=msg_assigned>$form{msg_assigned}</textarea></div>
			</fieldset>
			<fieldset class=config_group><legend>Values</legend>
				Value, delay in hours to activate (relative from the above step) and public description for each free credit step<br><br>
				<div style="width:100%; height:auto;">
					<table class=fields_group_table border=0 colspan=0 cellpadding=0 cellspacing=0 >
					<tr><td>Step:&nbsp;&nbsp;</td><td width=20%>Value:</td><td width=20%>Delay:</td><td width=60%>Description:</td></tr>
					<tr><td><input type=text readonly disabled value=1></td><td><input  $form_error{slice_1_value}  name=slice_1_value  value="$form{slice_1_value}"  ></td><td><input $form_error{slice_1_delay}  name=slice_1_delay  value="$form{slice_1_delay}"  ></td><td><input $form_error{slice_1_title} name=slice_1_title  value="$form{slice_1_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=2></td><td><input  $form_error{slice_2_value}  name=slice_2_value  value="$form{slice_2_value}"  ></td><td><input $form_error{slice_2_delay}  name=slice_2_delay  value="$form{slice_2_delay}"  ></td><td><input $form_error{slice_2_title} name=slice_2_title  value="$form{slice_2_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=3></td><td><input  $form_error{slice_3_value}  name=slice_3_value  value="$form{slice_3_value}"  ></td><td><input $form_error{slice_3_delay}  name=slice_3_delay  value="$form{slice_3_delay}"  ></td><td><input $form_error{slice_3_title} name=slice_3_title  value="$form{slice_3_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=4></td><td><input  $form_error{slice_4_value}  name=slice_4_value  value="$form{slice_4_value}"  ></td><td><input $form_error{slice_4_delay}  name=slice_4_delay  value="$form{slice_4_delay}"  ></td><td><input $form_error{slice_4_title} name=slice_4_title  value="$form{slice_4_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=5></td><td><input  $form_error{slice_5_value}  name=slice_5_value  value="$form{slice_5_value}"  ></td><td><input $form_error{slice_5_delay}  name=slice_5_delay  value="$form{slice_5_delay}"  ></td><td><input $form_error{slice_5_title} name=slice_5_title  value="$form{slice_5_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=6></td><td><input  $form_error{slice_6_value}  name=slice_6_value  value="$form{slice_6_value}"  ></td><td><input $form_error{slice_6_delay}  name=slice_6_delay  value="$form{slice_6_delay}"  ></td><td><input $form_error{slice_6_title} name=slice_6_title  value="$form{slice_6_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=7></td><td><input  $form_error{slice_7_value}  name=slice_7_value  value="$form{slice_7_value}"  ></td><td><input $form_error{slice_7_delay}  name=slice_7_delay  value="$form{slice_7_delay}"  ></td><td><input $form_error{slice_7_title} name=slice_7_title  value="$form{slice_7_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=8></td><td><input  $form_error{slice_8_value}  name=slice_8_value  value="$form{slice_8_value}"  ></td><td><input $form_error{slice_8_delay}  name=slice_8_delay  value="$form{slice_8_delay}"  ></td><td><input $form_error{slice_8_title} name=slice_8_title  value="$form{slice_8_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=9></td><td><input  $form_error{slice_9_value}  name=slice_9_value  value="$form{slice_9_value}"  ></td><td><input $form_error{slice_9_delay}  name=slice_9_delay  value="$form{slice_9_delay}"  ></td><td><input $form_error{slice_9_title} name=slice_9_title  value="$form{slice_9_title}"  ></td></tr>
					<tr><td><input type=text readonly disabled value=10></td><td><input $form_error{slice_10_value} name=slice_10_value value="$form{slice_10_value}" ></td><td><input $form_error{slice_10_delay} name=slice_10_delay value="$form{slice_10_delay}" ></td><td><input $form_error{slice_0_title} name=slice_10_title value="$form{slice_10_title}" ></td></tr>
					</table>
				</div>
			</fieldset>
			$form_error_message
			<button type=button class="cancel"	onclick="window.location='$my_url?action=coupons_list'">Cancel</button>
			<button type=submit class="save"  	>Save</button>
			<input type=hidden name=coupon_id value=$coupon_id>
			<input type=hidden name=action value=coupons_edit >
			<input type=hidden name=save value=$clickchain_id >
			</form>
		</div>
		</div>


		<div class=clear style="float:left;">
		<div class=clear style="width:250px;">
			<fieldset ><legend>Inventory</legend>
			<div class=clear style="font-size:10px;">
			$html_status
			<hr align=left size=1 noshade color=#c0c0c0 >
			$html_total
			</div>
			<br>
			$html_warning 
			<button type=button class="button" onclick="modal_open('Generate coupons','$my_url?action=coupons_stock_generate&coupon_id=$coupon_id',300,280);" style=width:100%;>Generate new coupons</button><br>
			<button type=button class="button" onclick="modal_open('Disable coupons','$my_url?action=coupons_stock_disable&coupon_id=$coupon_id',300,280);" style=width:100%;>Disable coupons</button><br>
			<button type=button class="button" onclick="modal_open('Enable coupons','$my_url?action=coupons_stock_enable&coupon_id=$coupon_id',300,280);" style=width:100%;>Enable coupons</button><br>
			<button type=button class="button" onclick="modal_open('Delete coupons','$my_url?action=coupons_stock_delete&coupon_id=$coupon_id',300,280);" style=width:100%;>Delete coupons</button><br>
			</fieldset>
		</div>
		</div>


	<br clear=both>
    ];
    &template_print("template.html",%t);
	
}
sub do_coupons_list(){
	#
	# pega a lista
	%coupons = database_select_as_hash("select id,title from service_coupon_type ","title");
	$sql = "
	select service_coupon_stock.coupon_type_id,count(*) 
	from service_coupon_stock,service_coupon_stock_status
	where service_coupon_stock.status= service_coupon_stock_status.id
	and is_ready_to_assign=1
	group by service_coupon_stock.coupon_type_id
	";
	%hash = database_select_as_hash($sql,"qtd");
	foreach (keys %hash) {
		unless (exists($coupons{$_})) {next}
		$coupons{$_}{ready} += $hash{$_}{qtd};  
	}
	$sql = "
	select service_coupon_stock.coupon_type_id,count(*) 
	from service_coupon_stock,service_coupon_stock_status
	where service_coupon_stock.status= service_coupon_stock_status.id
	group by service_coupon_stock.coupon_type_id
	";
	%hash = database_select_as_hash($sql,"qtd");
	foreach (keys %hash) {
		unless (exists($coupons{$_})) {next}
		$coupons{$_}{all} += $hash{$_}{qtd};  
	}
	$html_list = "";
    foreach $id (sort{$coupons{$a}{title} cmp $coupons{$b}{title}} keys %coupons) {
		$html_list .= "<li>";
		$html_list .= "<a href=$my_url?action=coupons_edit&coupon_id=$id>$coupons{$id}{title}</a> ";
		#$html_list .= " (inventory: ";
		#$html_list .= " Free=".&format_number($coupons{$id}{ready},0);
		#$html_list .= " Total=".&format_number($coupons{$id}{all},0);
		#$html_list .= ")";
		if ($coupons{$id}{ready} < 100){
			$html_list .= " <span style='font-size:5px;color:red;'>(".&format_number($coupons{$id}{ready},0)." coupons left)</span>";
		} else {
			$html_list .= " <span style='font-size:5px;color:#c0c0c0;'>(".&format_number($coupons{$id}{ready},0)." coupons left)</span>";
		}
		$html_list .= "</li>";
	}
    #
    # print page
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url>Settings</a> &#187; <a href=$my_url?action=coupons_list>Promotions</a>";
    $t{dic}{content}	= qq[
	<div class=clear style=width:450px>
		<fieldset class=config_select_list><legend>Select promotion</legend>
		<ul>
		$html_list
		</ul>
		</fieldset>
	</div>
    ];
	#foreach(170..400) {$t{dic}{content}	.= qq[$_ = &#$_;<br>];}
    &template_print("template.html",%t);
	
}
#========================================================================
sub do_service_status_list(){
	#
	# pega a lista
	%hash = database_select_as_hash("SELECT id,ui_order,ui_group,name FROM service_status where deleted=0","ui_order,ui_group,name");
	$html_changestatus_select = "";
	$id_group = "";
    foreach $id (sort{$hash{$a}{ui_order} <=> $hash{$b}{ui_order}} keys %hash) {
		if ($id_group ne $hash{$id}{ui_group}) {$html_changestatus_select .= "<br>";}
		$id_group = $hash{$id}{ui_group};
		$html_changestatus_select 	.= "<li><a href=$my_url?action=service_status_edit&status_id=$id>$hash{$id}{name}</a></li>";
	}
    #
    # print page
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url>Settings</a> &#187; <a href=$my_url?action=service_status_list>Phone services status</a>";
    $t{dic}{content}	= qq[
	<form action=$my_url>
	<div class=clear style=width:400px>
		<fieldset><legend>Select service status</legend>
		<ul>
		$html_changestatus_select
		</ul>
		</fieldset>
	</div>
	</form>
    ];
	#foreach(170..400) {$t{dic}{content}	.= qq[$_ = &#$_;<br>];}
    &template_print("template.html",%t);
	
}
sub do_service_status_edit(){
	#
	#===========================================================================
	# pega status data
	#===========================================================================
	$status_id = clean_int(substr($form{status_id},0,100));
	$sql = "
		SELECT
			1,1,
			id,
			name,
			text,
			can_add_refer,
			refer_status,
			signin_coupon_premium_id,
			signin_coupon_default_id,
			can_collect_commission,
			can_web_access,
			can_receive_calls,
			can_make_calls,
			can_add_credit,
			can_auto_recharge,
			can_request_commission_check,
			pin_locked,
			need_ani_check,
			switch_on_first_call,
			switch_on_first_credit,
			switch_on_suspicious,
			limit_max_balance,
			limit_max_recharges_in_7days,
			limit_ani_channels,
			call_flood_minutes_in_24hrs,
			call_flood_calls_in_1hr,
			call_flood_cross_service_dst_in_7days,
			coupon_id_auto_recharge_signin,
			coupon_id_ani_confirmation,
			coupon_pause_all,
			rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_callback,rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,
			switch_on_autorecharge_ok_charge,switch_on_autorecharge_in,switch_on_autorecharge_out
		FROM
			service_status
		where
			deleted=0 and
			id = '$status_id'
	";
	%hash = database_select_as_hash($sql,"flag,id,name,text,can_add_refer,refer_status,signin_coupon_premium_id,signin_coupon_default_id,can_collect_commission,can_web_access,can_receive_calls,can_make_calls,can_add_credit,can_auto_recharge,can_request_commission_check,pin_locked,need_ani_check,switch_on_first_call,switch_on_first_credit,switch_on_suspicious,limit_max_balance,limit_max_recharges_in_7days,limit_ani_channels,call_flood_minutes_in_24hrs,call_flood_calls_in_1hr,call_flood_cross_service_dst_in_7days,coupon_id_auto_recharge_signin,coupon_id_ani_confirmation,coupon_pause_all,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_callback,rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,switch_on_autorecharge_ok_charge,switch_on_autorecharge_in,switch_on_autorecharge_out");
	if ($hash{1}{flag} ne 1) {cgi_redirect("$my_url?action=service_status_list"); exit;}
	%status_data = %{$hash{1}};
	%status_list = database_select_as_hash("SELECT id,ui_order,ui_group,name FROM service_status where deleted=0","ui_order,ui_group,name");
	%coupons_list = database_select_as_hash("SELECT service_coupon_type.id,service_coupon_type.title FROM service_coupon_type,service_coupon_type_status where service_coupon_type.status=service_coupon_type_status.id and service_coupon_type_status.deleted=0","name");
	%rates_list = database_select_as_hash("SELECT id,name FROM product_rate_table ","name");
	#
	#===========================================================================
	# save from
	#===========================================================================
	$debug_clickcheck = &active_session_get("click_check_config");
	if ( ($form{click_check} eq &active_session_get("click_check_config")) && ($form{save} eq 1) ) {
		#
		# start
		%ok_data = ();
		#
		# basic
		$ok_data{name} = substr(clean_str($form{name},"(),:-_"),0,200); 
		#$ok_data{text} = substr(clean_str($form{text},"(),:-_<>="),0,65536); 
		$ok_data{text} = trim(clean_str(substr($form{text},0,65536),"\@. []()=_-:\n"));
		$tmp1="\r"; $tmp2="\n"; 	$ok_data{text} =~ s/$tmp1/$tmp2/eg; 
		$tmp1="\n"; $tmp2="<br>";	$ok_data{text} =~ s/$tmp1/$tmp2/eg;
		#
		# checbox
		foreach $id (qw(can_add_refer can_collect_commission can_web_access can_receive_calls can_make_calls can_add_credit can_auto_recharge can_request_commission_check pin_locked need_ani_check)){
			$ok_data{$id} = ($form{$id} eq 1) ? 1 : 0; 
		}
		# 
		# string
		#foreach $id (qw(rate_slot_1_name rate_slot_2_name rate_slot_3_name rate_slot_4_name)){
		#	$ok_data{$id} = substr(clean_str($form{$id}," (),:-_"),0,200); 
		#}
		#
		# integer 
		foreach $id (qw(limit_max_balance limit_max_recharges_in_7days limit_ani_channels call_flood_minutes_in_24hrs call_flood_calls_in_1hr call_flood_cross_service_dst_in_7days)){
			$value = $form{$id};
			$value = (clean_int($value) eq $value) ? $value : 0;
			$value = ("" eq $value) ? 0 : $value;
			$value = ($value<0) ? 0 : $value;
			$value = ($value>65536) ? 65536 : $value;
			$ok_data{$id} = $value;
		}
		#
		# status list
		foreach $id (qw(switch_on_first_call switch_on_first_credit refer_status switch_on_suspicious switch_on_autorecharge_ok_charge switch_on_autorecharge_in switch_on_autorecharge_out)){
			$ok_data{$id} = (exists($status_list{$form{$id}})) ? "'$form{$id}'" : "null"; 
		}
		#
		# rates list
		#foreach $id (qw(rate_slot_1 rate_slot_2 rate_slot_3 rate_slot_4 rate_slot_callback)){
		#	$ok_data{$id} = (exists($rates_list{$form{$id}})) ? "'$form{$id}'" : "null"; 
		#}
		#
		# coupons
		$ok_data{coupon_pause_all} 					= ($form{coupon_pause_all} eq 1) ? 1 : 0;
		#$ok_data{coupon_id_new_service} 			= (exists($coupons_list{$form{coupon_id_new_service}})) 			? "'".$form{coupon_id_new_service}."'" 			: "null";
		$ok_data{coupon_id_auto_recharge_signin} 	= (exists($coupons_list{$form{coupon_id_auto_recharge_signin}})) 	? "'".$form{coupon_id_auto_recharge_signin}."'"	: "null";
		$ok_data{coupon_id_ani_confirmation} 		= (exists($coupons_list{$form{coupon_id_ani_confirmation}})) 		? "'".$form{coupon_id_ani_confirmation}."'" 	: "null";
		$ok_data{signin_coupon_default_id} 			= (exists($coupons_list{$form{signin_coupon_default_id}})) 		? "'".$form{signin_coupon_default_id}."'" 	: "null";
		$ok_data{signin_coupon_premium_id} 			= (exists($coupons_list{$form{signin_coupon_premium_id}})) 		? "'".$form{signin_coupon_premium_id}."'" 	: "null";
		#
		# save
		$sql = "
		update service_status set 
			name = '$ok_data{name}', 
			text = '$ok_data{text}',
			can_add_refer = '$ok_data{can_add_refer}',
			refer_status = $ok_data{refer_status}, 
			signin_coupon_premium_id = $ok_data{signin_coupon_premium_id}, 
			signin_coupon_default_id = $ok_data{signin_coupon_default_id}, 
			can_collect_commission = '$ok_data{can_collect_commission}',
			can_web_access = '$ok_data{can_web_access}',
			can_receive_calls = '$ok_data{can_receive_calls}',
			can_make_calls = '$ok_data{can_make_calls}',
			can_add_credit = '$ok_data{can_add_credit}',
			can_auto_recharge = '$ok_data{can_auto_recharge}',
			can_request_commission_check = '$ok_data{can_request_commission_check}',
			pin_locked = '$ok_data{pin_locked}',
			need_ani_check = '$ok_data{need_ani_check}',
			switch_on_first_call = $ok_data{switch_on_first_call},
			switch_on_first_credit = $ok_data{switch_on_first_credit},
			switch_on_suspicious = $ok_data{switch_on_suspicious},
			switch_on_autorecharge_ok_charge = $ok_data{switch_on_autorecharge_ok_charge},
			switch_on_autorecharge_in = $ok_data{switch_on_autorecharge_in},
			switch_on_autorecharge_out = $ok_data{switch_on_autorecharge_out},
			limit_max_balance = '$ok_data{limit_max_balance}',
			limit_max_recharges_in_7days = '$ok_data{limit_max_recharges_in_7days}',
			limit_ani_channels = '$ok_data{limit_ani_channels}',
			call_flood_minutes_in_24hrs = '$ok_data{call_flood_minutes_in_24hrs}',
			call_flood_calls_in_1hr = '$ok_data{call_flood_calls_in_1hr}', 	
			call_flood_cross_service_dst_in_7days = '$ok_data{call_flood_cross_service_dst_in_7days}',
			coupon_pause_all = '$ok_data{coupon_pause_all}' ,
			coupon_id_auto_recharge_signin = $ok_data{coupon_id_auto_recharge_signin},
			coupon_id_ani_confirmation = $ok_data{coupon_id_ani_confirmation}
		where
			deleted=0 and
			id = '$status_id'
		";
		#	rate_slot_1 = $ok_data{rate_slot_1}, 
		#	rate_slot_2 = $ok_data{rate_slot_2}, 
		#	rate_slot_3 = $ok_data{rate_slot_3}, 
		#	rate_slot_4 = $ok_data{rate_slot_4}, 
		#	rate_slot_callback = $ok_data{rate_slot_callback}, 
		#	rate_slot_1_name = '$ok_data{rate_slot_1_name}', 
		#	rate_slot_2_name = '$ok_data{rate_slot_2_name}', 
		#	rate_slot_3_name = '$ok_data{rate_slot_3_name}', 
		#	rate_slot_4_name = '$ok_data{rate_slot_4_name}'
		#print "content-type: text/plain\n\n";print "$sql\n-----------------------------------------\n";foreach (sort keys %form) {	print "NAME=$_ \t FORM=$form{$_} \t OK=$ok_data{$_} \n";}exit;
		&database_do($sql);
		cgi_redirect("$my_url?action=service_status_list");
		exit;
	}
	#
	#===========================================================================
	# load from
	#===========================================================================
	if ($form{save} ne 1) {
		foreach (keys %status_data) {$form{$_} = $status_data{$_} }
		$tmp1="<br>"; $tmp2="\n"; $form{text} =~ s/$tmp1/$tmp2/eg; 
	}
	#
	#===========================================================================
	# prepare from
	#===========================================================================
	foreach $name (qw(can_add_refer can_collect_commission can_web_access can_receive_calls can_make_calls can_add_credit can_auto_recharge can_request_commission_check pin_locked need_ani_check)){
		$form{$name."_checked"} = ($form{$name} eq 1) ? "checked" : "";
	}
	$tmp1 = "";
    foreach $id (sort{$status_list{$a}{ui_order} <=> $status_list{$b}{ui_order}} keys %status_list) {
		$tmp3 = ($status_list{$id}{ui_group} eq $tmp1) ? "" : "<option value=''></option>";
		$tmp1 = $status_list{$id}{ui_group};
		foreach $name (qw(switch_on_first_call refer_status switch_on_first_credit switch_on_suspicious switch_on_autorecharge_ok_charge switch_on_autorecharge_in switch_on_autorecharge_out)){
			$tmp4 = ($id eq $form{$name}) ? "selected" : "";
			$form{$name."_select"} .= "$tmp3<option $tmp4 value=$id>$status_list{$id}{name}</option>";
		}
		$tmp4 = ($id eq $status_id) ? "selected" : "";
		$form{"status_id_select"} .= "$tmp3<option $tmp4 value=$id>$status_list{$id}{name}</option>";
	}
    foreach $id (sort{$coupons_list{$a}{name} cmp $coupons_list{$b}{name}} keys %coupons_list) {
		foreach $name (qw(coupon_id_new_service signin_coupon_premium_id signin_coupon_default_id coupon_id_ani_confirmation)){
			$tmp = ($id eq $form{$name}) ? "selected" : "";
			$form{$name."_select"} .= "<option $tmp value=$id>$coupons_list{$id}{name}</option>";
		}

	}
    foreach $id (sort{$rates_list{$a}{name} cmp $rates_list{$b}{name}} keys %rates_list) {
		foreach $name (qw(rate_slot_1 rate_slot_2 rate_slot_3 rate_slot_4 rate_slot_callback)){
			$tmp4 = ($id eq $form{$name}) ? "selected" : "";
			$form{$name."_select"} .= "<option $tmp4 value=$id>$rates_list{$id}{name}</option>";
		}
	}
	$tmp = (1 ne $form{coupon_pause_all}) ? "selected" : "";
	$form{"coupon_pause_all_select"} .= "<option $tmp value=0>Enabled</option>";
	$tmp = (1 eq $form{coupon_pause_all}) ? "selected" : "";
	$form{"coupon_pause_all_select"} .= "<option $tmp value=1>Disable all</option>";
	$click_check = time;
	&active_session_set("click_check_config",$click_check);
	#
	#===========================================================================
    # print page
	#===========================================================================
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url>Settings</a> &#187; <a href=$my_url?action=service_status_list>Phone services status</a> &#187; '$status_data{name}'";
    $t{dic}{content}	= qq[


	<form action=$my_url>

		    <fieldset class=config_group><legend>'$status_data{name}' status settings</legend>
				<div style="height:130px;" ><h1>Tite</h1>Edit this status title.<br><br><input type=text name=name value="$form{name}"></div>
				<div style="height:130px;" ><h1>Description:<h1><textarea style=height:100px; name=text>$form{text}</textarea></div>
			</fieldset>


		    <fieldset class=config_group><legend>Services access permissions</legend>
				<div ><h1>Web access</h1			>Allow this services log-in into /myaccount web interface<br	><br><input type=checkbox name=can_web_access 	$form{can_web_access_checked} value=1>Enable</div>
				<div ><h1>Calls permission</h1		>Allow this services place calls<br 							><br><input type=checkbox name=can_make_calls 	$form{can_make_calls_checked} value=1>Enable</div>
				<div ><h1>Limited acces</h1			>Only allow dial from know ANI and dial only to know DST. <br 	><br><input type=checkbox name=pin_locked 		$form{pin_locked_checked} value=1>Enable</div>
				<div ><h1>Need ANI check</h1		>Enable ANI check for this services<br 							><br><input type=checkbox name=need_ani_check 	$form{need_ani_check_checked} value=1>Enable</div>
			</fieldset>

		    <fieldset class=config_group><legend>Services billing permissions</legend>
				<div><h1>Max balance</h1				>Max balance allowed for this services<br 						><br><input type=text 		name=limit_max_balance 				value="$form{limit_max_balance}" style=width:50px;>dollars</div>
				<div><h1>7days recharges</h1			>Limit max recharges in 7 days for this services<br 			><br><input type=text 		name=limit_max_recharges_in_7days 	value="$form{limit_max_recharges_in_7days}" style=width:50px;>dollars</div>
				<div><h1>Collect commissions</h1		>Allow service collect commissions<br 							><br><input type=checkbox 	name=can_collect_commission 		$form{can_collect_commission_checked} value=1>Enable</div>
				<div><h1>Add credit</h1					>Allow service add credit by CC profile or by commissions. <br 	><br><input type=checkbox 	name=can_add_credit 				$form{can_add_credit_checked} value=1>Enable</div>
				<div><h1>Auto recharge</h1				>Allow servce run auto-recharge<br 								><br><input type=checkbox 	name=can_auto_recharge 				$form{can_auto_recharge_checked} value=1>Enable</div>
				<div><h1>Request commission check</h1	>Allow service request commissions check<br 					><br><input type=checkbox 	name=can_request_commission_check 	$form{can_request_commission_check_checked} value=1>Enable</div>
			</fieldset>

<!-- 
		    <fieldset class=config_group><legend>Services calls rates/route</legend>
				<div><h1>Call-back</h1>Select and rate/route table for callback calls<br 		><select style=width:100% name=rate_slot_callback><option>(disabled)</option><option></option>$form{rate_slot_callback_select}</select></div>
				<div><h1>Route #1 <font size=1>(default)</font></h1>Select name (for web) and rate/route table<br 		><input type=text name=rate_slot_1_name value="$form{rate_slot_1_name}" style=width:100%;><br><select style=width:100% name=rate_slot_1><option>(disabled)</option><option></option>$form{rate_slot_1_select}</select></div>
				<div><h1>Route #2</h1>Select name (for web) and rate/route table<br 		><input type=text name=rate_slot_2_name value="$form{rate_slot_2_name}" style=width:100%;><br><select style=width:100% name=rate_slot_2><option>(disabled)</option><option></option>$form{rate_slot_2_select}</select></div>
				<div><h1>Route #3</h1>Select name (for web) and rate/route table<br 		><input type=text name=rate_slot_3_name value="$form{rate_slot_3_name}" style=width:100%;><br><select style=width:100% name=rate_slot_3><option>(disabled)</option><option></option>$form{rate_slot_3_select}</select></div>
				<div><h1>Route #4</h1>Select name (for web) and rate/route table<br 		><input type=text name=rate_slot_4_name value="$form{rate_slot_4_name}" style=width:100%;><br><select style=width:100% name=rate_slot_4><option>(disabled)</option><option></option>$form{rate_slot_4_select}</select></div>
			</fieldset>
-->

		    <fieldset class=config_group><legend>Services promotions</legend>
				<div><h1>Promotions status</h1			>control all in use and future promotions<br	><br><select style=width:100% name=coupon_pause_all>$form{coupon_pause_all_select}</select></div>
				<div><h1>ANI confirm promotion</h1		>Coupon for text ANI confirm promotion:<br	><br><select style=width:100% name=coupon_id_ani_confirmation><option>(no coupon)</option><option></option>$form{xxxxcoupon_id_ani_confirmation_select}</select></div>
				<div><h1>Auto recharge promotion</h1	>Coupon for auto recharge promotion<br 		><br><select style=width:100% name=coupon_id_auto_recharge_signin><option>(no coupon)</option><option></option>$form{coupon_id_auto_recharge_signin_select}</select></div>
			</fieldset>

		    <fieldset class=config_group><legend>Services referral settings</legend>
				<div><h1>Referral</h1				>Enable or disable public invite for this services<br 			><br><input type=checkbox name=can_add_refer 	$form{can_add_refer_checked} value=1>Enable</div>
				<div><h1>Referral sign-in</h1		>New referral from this services start with this status:<br 	><br><select style=width:100% name=refer_status><option>(automatic)</option><option></option>$form{refer_status_select}</select></div>
				<div><h1>Sign-in default promotion</h1	>Default coupon for new sign-in referral:<br 						><br><select style=width:100% name=signin_coupon_default_id><option>(no coupon)</option><option></option>$form{signin_coupon_default_id_select}</select></div>
				<div><h1>Sign-in premium promotion</h1	>Coupon for premium (selected by carrier) sign-in referral:<br 	><br><select style=width:100% name=signin_coupon_premium_id><option>(no coupon)</option><option></option>$form{signin_coupon_premium_id_select}</select></div>
			</fieldset>

		    <fieldset class=config_group><legend>Services call flood limits</legend>
				<div><h1>Call per ANI</h1			>Max number of calls per ani.<br 																											><br><input type=text disabled readonly name=nothing value="1" style=width:50px;>calls</div>
				<div><h1>Call minutes in 24hrs</h1	>Max call minutes for this services in 24hrs period.<br 																					><br><input type=text name=call_flood_minutes_in_24hrs				value="$form{call_flood_minutes_in_24hrs}" style=width:50px;>minutes</div>
				<div><h1>Calls in 1hr</h1			>Max call count for this services in 1hr period.<br 																						><br><input type=text name=call_flood_calls_in_1hr					value="$form{call_flood_calls_in_1hr}" style=width:50px;>calls</div>
				<div><h1>DST flood</h1				>Check if DST number is in use by another services in 24rs period. <br 	><br><input type=text name=call_flood_cross_service_dst_in_7days	value="$form{call_flood_cross_service_dst_in_7days}" style=width:50px;>calls</div>
			</fieldset>

		    <fieldset class=config_group><legend>Services auto-switch-status settings</legend>
				<div><h1>on suspicious</h1				>If system detect suspicious action, change status to:<br 				><br><select name=switch_on_suspicious><option>(Disabled)</option><option></option>$form{switch_on_suspicious_select}</select></div>
				<div><h1>on first call</h1				>If system detect first call by this service, change status to:<br 		><br><select name=switch_on_first_call><option>(Disabled)</option><option></option>$form{switch_on_first_call_select}</select></div>
				<div><h1>on first charge</h1			>If system detect first money-in charge, change status to:<br 			><br><select name=switch_on_first_credit><option>(Disabled)</option><option></option>$form{switch_on_first_credit_select}</select></div>
				<div><h1>on autorecharge Sign-In</h1	>If system detect user auto recharge sign-in, change to:<br 			><br><select name=switch_on_autorecharge_in><option>(Disabled)</option><option></option>$form{switch_on_autorecharge_in_select}</select></div>
				<div><h1>on autorecharge Sign-Out</h1	>If system detect user auto recharge sign-out, change to:<br 			><br><select name=switch_on_autorecharge_out><option>(Disabled)</option><option></option>$form{switch_on_autorecharge_out_select}</select></div>
				<div><h1>on autorecharge charge</h1		>If system detect charge from autorecharge, change to:<br 				><br><select name=switch_on_autorecharge_ok_charge><option>(Disabled)</option><option></option>$form{switch_on_autorecharge_ok_charge_select}</select></div>
			</fieldset>

	<br clear=both>
	<input type=hidden name=action value=service_status_edit>
	<input type=hidden name=status_id value=$status_id>
	<input type=hidden name=save value=1>
	<input type=hidden name=click_check value=$click_check>
	<button type=button class="cancel"	onclick="window.location='$my_url?action=service_status_list'">Cancel</button>
	<button type=submit class="save"  	onclick="modal_loadingblock()">Save</button>
	</tr></table>

	</form>
	<br>&nbsp;
    ];
	
	#$t{dic}{content}	.= "CLICKCHECK = ($debug_clickcheck) ($form{click_check})<hr>$sql<hr>";
	#foreach (sort keys %ok_data) {$t{dic}{content}	.= qq[DUMP OK_DATA ($_)=($ok_data{$_})<br>];}
	#foreach (sort keys %form) {$t{dic}{content}	.= qq[DUMP FORM ($_)=($form{$_})<br>];}

    &template_print("template.html",%t);
}
#========================================================================
sub OLD_do_phone_routes(){
    #
	#----------------
    # start
	#----------------
    $ok_message = "";
    $error_message = "";
	$error = "";
    #
	#----------------
    # try save
	#----------------
	if ($form{save} ne "") {
		if ( &multilevel_clickchain_check("sph",$form{save}) eq 1 ) {
			foreach $i (0..9){
				&data_set("adm_data","router","filter_".$i, trim($form{"router_0_filter_".$i}) );
				&data_set("adm_data","router","string_".$i, trim($form{"router_0_string_".$i}) );
				&data_set("adm_data","router_1","filter_".$i, trim($form{"router_1_filter_".$i}) );
				&data_set("adm_data","router_1","string_".$i, trim($form{"router_1_string_".$i}) );
			}
			#&cgi_redirect($my_url);
			#return;
			$ok_message = "Setings saved.";
		}
	}
    #
	#----------------
    # load
	#----------------
	if ($form{save} eq "") {
		foreach $i (0..9){
		    $form{"router_0_filter_".$i} 	= &data_get("adm_data","router","filter_".$i);
		    $form{"router_0_string_".$i} 	= &data_get("adm_data","router","string_".$i);
		    $form{"router_1_filter_".$i} 	= &data_get("adm_data","router_1","filter_".$i);
		    $form{"router_1_string_".$i} 	= &data_get("adm_data","router_1","string_".$i);
		}
	}
    #
	#----------------
    # html messages
	#----------------
    $ok_message = ($ok_message eq "") ? "" : "<div class=alert_box style=width:720px ><div class=alert_box_inside>$ok_message</div></div><br>";
    #
	#----------------
    # print page
	#----------------
	$clickchain_id = &multilevel_clickchain_set("sph");
    %t = ();
    $t{dic}{title}	= "<a href=$my_url>Settings</a> &#187; Phone routes";
    $t{dic}{content} = qq[

	$ok_message		

	<form action=$my_url method=post>

		<div class=clear style="width:350px; float:left; margin-right:20px;">
		<fieldset><legend>Cheap Route</legend>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 width=100%>
			<tr>
			<td><b>Filter</b></td>
			<td><b>Dial String</b></td>
			</tr>
			<tr><td width=40%><input style='width:100%; $error_field_router_0_filter_0'	name=router_0_filter_0 value='$form{router_0_filter_0}'></td><td><input style='width:100%; $error_field_router_0_string_0'	name=router_0_string_0 value='$form{router_0_string_0}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_1'	name=router_0_filter_1 value='$form{router_0_filter_1}'></td><td><input style='width:100%; $error_field_router_0_string_1'	name=router_0_string_1 value='$form{router_0_string_1}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_2'	name=router_0_filter_2 value='$form{router_0_filter_2}'></td><td><input style='width:100%; $error_field_router_0_string_2'	name=router_0_string_2 value='$form{router_0_string_2}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_3'	name=router_0_filter_3 value='$form{router_0_filter_3}'></td><td><input style='width:100%; $error_field_router_0_string_3'	name=router_0_string_3 value='$form{router_0_string_3}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_4'	name=router_0_filter_4 value='$form{router_0_filter_4}'></td><td><input style='width:100%; $error_field_router_0_string_4'	name=router_0_string_4 value='$form{router_0_string_4}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_5'	name=router_0_filter_5 value='$form{router_0_filter_5}'></td><td><input style='width:100%; $error_field_router_0_string_5'	name=router_0_string_5 value='$form{router_0_string_5}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_6'	name=router_0_filter_6 value='$form{router_0_filter_6}'></td><td><input style='width:100%; $error_field_router_0_string_6'	name=router_0_string_6 value='$form{router_0_string_6}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_7'	name=router_0_filter_7 value='$form{router_0_filter_7}'></td><td><input style='width:100%; $error_field_router_0_string_7'	name=router_0_string_7 value='$form{router_0_string_7}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_8'	name=router_0_filter_8 value='$form{router_0_filter_8}'></td><td><input style='width:100%; $error_field_router_0_string_8'	name=router_0_string_8 value='$form{router_0_string_8}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_0_filter_9'	name=router_0_filter_9 value='$form{router_0_filter_9}'></td><td><input style='width:100%; $error_field_router_0_string_9'	name=router_0_string_9 value='$form{router_0_string_9}'></td></tr>
		</table>
		</fieldset>
		</div>

		<div class=clear style="width:350px; float:left; margin-right:20px;">
		<fieldset><legend>Quality Route</legend>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 width=100%>
			<tr>
			<td><b>Filter</b></td>
			<td><b>Dial String</b></td>
			</tr>
			<tr><td width=40%><input style='width:100%; $error_field_router_1_filter_0'	name=router_1_filter_0 value='$form{router_1_filter_0}'></td><td><input style='width:100%; $error_field_router_1_string_0'	name=router_1_string_0 value='$form{router_1_string_0}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_1'	name=router_1_filter_1 value='$form{router_1_filter_1}'></td><td><input style='width:100%; $error_field_router_1_string_1'	name=router_1_string_1 value='$form{router_1_string_1}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_2'	name=router_1_filter_2 value='$form{router_1_filter_2}'></td><td><input style='width:100%; $error_field_router_1_string_2'	name=router_1_string_2 value='$form{router_1_string_2}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_3'	name=router_1_filter_3 value='$form{router_1_filter_3}'></td><td><input style='width:100%; $error_field_router_1_string_3'	name=router_1_string_3 value='$form{router_1_string_3}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_4'	name=router_1_filter_4 value='$form{router_1_filter_4}'></td><td><input style='width:100%; $error_field_router_1_string_4'	name=router_1_string_4 value='$form{router_1_string_4}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_5'	name=router_1_filter_5 value='$form{router_1_filter_5}'></td><td><input style='width:100%; $error_field_router_1_string_5'	name=router_1_string_5 value='$form{router_1_string_5}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_6'	name=router_1_filter_6 value='$form{router_1_filter_6}'></td><td><input style='width:100%; $error_field_router_1_string_6'	name=router_1_string_6 value='$form{router_1_string_6}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_7'	name=router_1_filter_7 value='$form{router_1_filter_7}'></td><td><input style='width:100%; $error_field_router_1_string_7'	name=router_1_string_7 value='$form{router_1_string_7}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_8'	name=router_1_filter_8 value='$form{router_1_filter_8}'></td><td><input style='width:100%; $error_field_router_1_string_8'	name=router_1_string_8 value='$form{router_1_string_8}'></td></tr>
			<tr><td><input style='width:100%; $error_field_router_1_filter_9'	name=router_1_filter_9 value='$form{router_1_filter_9}'></td><td><input style='width:100%; $error_field_router_1_string_9'	name=router_1_string_9 value='$form{router_1_string_9}'></td></tr>
		</table>
		</fieldset>
		</div>

		<br clear=both>
		<div style='width:560px;'>
		<div style='font-size:10px; padding:10px; line-height:130%;'>
		<div class=clear style="margin-bottom:20px; margin-right:5px; float:left; "><b>Filter:</b></div> Match begin of E164 numbers (55 to brasil, 1212 to USA miami), full number if end with period (12121234567. for specific number) or any number if empty <br clear=both>
		<div class=clear style="margin-bottom:10px; margin-right:5px; float:left; "><b>Dial string:</b></div> Valid asterisk SIP dial string (number\@gw_ip). You can use FULL for full e164 number, COUNTRY for country code and NUMBER for areacode+number.<br>
		</div>
		</div>

		$error_message
		<input type=hidden name=action value=phone_routes>
		<input type=hidden name=save value=$clickchain_id>
		<button type=button class=cancel onclick="window.location='$my_url'">Cancel</button>
		<button type=submit class=save>Save</button>


	</form>
	
    ];
    &template_print("template.html",%t);
}
sub OLD_do_commissions(){
    #
	#----------------
    # start
	#----------------
    $ok_message = "";
    $error_message = "";
	$error = "";
    #
	#----------------
    # try save
	#----------------
	if ($form{save} ne "") {
	if ( &multilevel_clickchain_check("sac",$form{save}) eq 1 ) {
		#
		#----------------------------
		# check credit commission
		#----------------------------
		$n = "commission_credit_value";
		$v1 = $form{$n};
		$v2 = clean_float(substr($v1,0,30));
		$v2++;
		$v2--;
		if ( ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_credit_value = "background-color:red;";
		}
		$n = "commission_credit_mode";
		$v1 = $form{$n};
		if (index("|SINGLE|ZENO|","|$v1|") eq -1) {
			$error_message = "Check red fields";
			$error_field_commission_credit_mode = "background-color:red;";
		}
		$n = "commission_credit_days_1";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_credit_days_1 = "background-color:red;";
		}
		$n = "commission_credit_days_2";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_credit_days_2 = "background-color:red;";
		}
		#
		#----------------------------
		# check new friend commission
		#----------------------------
		$n = "commission_newf_value";
		$v1 = $form{$n};
		$v2 = clean_float(substr($v1,0,30));
		$v2++;
		$v2--;
		if ( ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newf_value = "background-color:red;";
		}
		$n = "commission_newf_mode";
		$v1 = $form{$n};
		if (index("|SINGLE|ZENO|","|$v1|") eq -1) {
			$error_message = "Check red fields";
			$error_field_commission_newf_mode = "background-color:red;";
		}
		$n = "commission_newf_days_1";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newf_days_1 = "background-color:red;";
		}
		$n = "commission_newf_days_2";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newf_days_2 = "background-color:red;";
		}
		#
		#----------------------------
		# check new friend call commission
		#----------------------------
		$n = "commission_newfcall_value";
		$v1 = $form{$n};
		$v2 = clean_float(substr($v1,0,30));
		$v2++;
		$v2--;
		if ( ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newfcall_value = "background-color:red;";
		}
		$n = "commission_newfcall_mode";
		$v1 = $form{$n};
		if (index("|SINGLE|ZENO|","|$v1|") eq -1) {
			$error_message = "Check red fields";
			$error_field_commission_newfcall_mode = "background-color:red;";
		}
		$n = "commission_newfcall_days_1";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newfcall_days_1 = "background-color:red;";
		}
		$n = "commission_newfcall_days_2";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newfcall_days_2 = "background-color:red;";
		}
		#
		#----------------------------
		# try to save
		#----------------------------
		if ($error_message eq "") {
			#
			&data_set("adm_data","commission","credit_percentage",$form{commission_credit_value});
			&data_set("adm_data","commission","credit_mode",$form{commission_credit_mode});
			&data_set("adm_data","commission","credit_activation_date_1",$form{commission_credit_days_1});
			&data_set("adm_data","commission","credit_activation_date_2",$form{commission_credit_days_2});
			#
			&data_set("adm_data","commission","newf_value",$form{commission_newf_value});
			&data_set("adm_data","commission","newf_mode",$form{commission_newf_mode});
			&data_set("adm_data","commission","newf_activation_date_1",$form{commission_newf_days_1});
			&data_set("adm_data","commission","newf_activation_date_2",$form{commission_newf_days_2});
			#
			&data_set("adm_data","commission","newfcall_value",$form{commission_newfcall_value});
			&data_set("adm_data","commission","newfcall_mode",$form{commission_newfcall_mode});
			&data_set("adm_data","commission","newfcall_activation_date_1",$form{commission_newfcall_days_1});
			&data_set("adm_data","commission","newfcall_activation_date_2",$form{commission_newfcall_days_2});
			#
			$ok_message = "Setings saved.";
		}
	}
	}
    #
	#----------------
    # load
	#----------------
	if ($form{save} eq "") {
		#
		$form{commission_credit_value}	= &data_get("adm_data","commission","credit_percentage");
		$form{commission_credit_mode}	= &data_get("adm_data","commission","credit_mode");
		$form{commission_credit_days_1}	= &data_get("adm_data","commission","credit_activation_date_1");
		$form{commission_credit_days_2}	= &data_get("adm_data","commission","credit_activation_date_2");
		#
		$form{commission_newf_value}	= &data_get("adm_data","commission","newf_value");
		$form{commission_newf_mode}		= &data_get("adm_data","commission","newf_mode");
		$form{commission_newf_days_1}	= &data_get("adm_data","commission","newf_activation_date_1");
		$form{commission_newf_days_2}	= &data_get("adm_data","commission","newf_activation_date_2");
		#
		$form{commission_newfcall_value}	= &data_get("adm_data","commission","newfcall_value");
		$form{commission_newfcall_mode}		= &data_get("adm_data","commission","newfcall_mode");
		$form{commission_newfcall_days_1}	= &data_get("adm_data","commission","newfcall_activation_date_1");
		$form{commission_newfcall_days_2}	= &data_get("adm_data","commission","newfcall_activation_date_2");
		#
	}
    #
	#----------------
    # html messages
	#----------------
    #
	#----------------
    # html messages
	#----------------
    $message = ($ok_message eq "") ? "" : "<div class=alert_box ><div class=alert_box_inside>$ok_message</div></div><br>";
    $message = ($error_message eq "") ? $message : "<div class=alert_box ><div class=alert_box_inside>$error_message</div></div><br>";
    #
	#----------------
    # print page
	#----------------
    %t = ();
	$select_commission_credit_mode{$form{commission_credit_mode}} = "selected";
	$select_commission_newf_mode{$form{commission_newf_mode}} = "selected";
	$select_commission_newfcall_mode{$form{commission_newfcall_mode}} = "selected";
	$clickchain_id = &multilevel_clickchain_set("sac");
    $t{dic}{title}	= "<a href=$my_url>Settings</a> &#187; Automatic commissions";
    $t{dic}{content} = qq[

	<form action=$my_url name="mainform" method=post>

		<div class=clear style="width:500px; ">
			$message
			<fieldset><legend>Automatic commissions</legend>
				
				<b>Friend credit commission</b><br>
				<table border=0 colspan=0 cellpadding=0 cellspacing=0 style='border-top:1px solid #c0c0c0'>
				<td width=70	style='padding-left:0px;'>Percentage<br><input style='width:100%; $error_field_commission_credit_value' name=commission_credit_value value='$form{commission_credit_value}'></td>
				<td width=70	style='padding-left:5px;'>Mode<br><select style='width:100%; $error_field_commission_credit_mode' name=commission_credit_mode ><option $select_commission_credit_mode{SINGLE} value=SINGLE>Single</option><option $select_commission_credit_mode{ZENO} value=ZENO>Zeno</option></select></td>
				<td 			style='padding-left:5px;'>Convert days<br><input style='width:100%; $error_field_commission_credit_days_1' name=commission_credit_days_1 value='$form{commission_credit_days_1}' ></td>
				<td 			style='padding-left:5px;'>Withdraw days<br><input style='width:100%; $error_field_commission_credit_days_2' name=commission_credit_days_2 value='$form{commission_credit_days_2}' ></td>
				</table>
				<br>
	
				
				<b>New friend commission</b><br>
				<table border=0 colspan=0 cellpadding=0 cellspacing=0 style='border-top:1px solid #c0c0c0'>
				<td width=70	style='padding-left:0px;'>Value<br><input style='width:100%; $error_field_commission_newf_value' name=commission_newf_value value='$form{commission_newf_value}'></td>
				<td width=70	style='padding-left:5px;'>Mode<br><select style='width:100%; $error_field_commission_newf_mode' name=commission_newf_mode ><option $select_commission_newf_mode{SINGLE} value=SINGLE>Single</option><option $select_commission_newf_mode{ZENO} value=ZENO>Zeno</option></select></td>
				<td 			style='padding-left:5px;'>Convert days<br><input style='width:100%;  $error_field_commission_newf_days_1' name=commission_newf_days_1 value='$form{commission_newf_days_1}' ></td>
				<td 			style='padding-left:5px;'>Withdraw days<br><input style='width:100%; $error_field_commission_newf_days_2' name=commission_newf_days_2 value='$form{commission_newf_days_2}' ></td>
				</table>
				<br>
	
				<b>Friends first call commission</b><br>
				<table border=0 colspan=0 cellpadding=0 cellspacing=0 style='border-top:1px solid #c0c0c0'>
				<td width=70	style='padding-left:0px;'>Value<br><input style='width:100%; $error_field_commission_newfcall_value' name=commission_newfcall_value value='$form{commission_newfcall_value}'></td>
				<td width=70	style='padding-left:5px;'>Mode<br><select style='width:100%; $error_field_commission_newfcall_mode' name=commission_newfcall_mode ><option $select_commission_newfcall_mode{SINGLE} value=SINGLE>Single</option><option $select_commission_newfcall_mode{ZENO} value=ZENO>Zeno</option></select></td>
				<td 			style='padding-left:5px;'>Convert days<br><input style='width:100%; $error_field_commission_newfcall_days_1' name=commission_newfcall_days_1 value='$form{commission_newfcall_days_1}' ></td>
				<td 			style='padding-left:5px;'>Withdraw days<br><input style='width:100%; $error_field_commission_newfcall_days_2' name=commission_newfcall_days_2 value='$form{commission_newfcall_days_2}' ></td>
				</table>
	
			</fieldset>
















			<div style='font-size:10px; padding:10px; line-height:130%;'>
				<div class=clear style="margin-bottom:4px; margin-right:5px; float:left; "><b>enable/disable:</b></div> To disable, just enter zero as value.<br clear=both>
				<div class=clear style="margin-bottom:15px; margin-right:5px; float:left; "><b>Single mode:</b></div> Only target service will get the 100% OF VALUE as commission and we do not send commissions for they parents.<br clear=both>
				<div class=clear style="margin-bottom:15px; margin-right:5px; float:left; "><b>Zeno mode:</b></div> Send 50% OF THE VALUE as commission for target service, 25% to they parent, 12.5% to parent of parent and soo on<br clear=both>
				<div class=clear style="margin-bottom:15px; margin-right:5px; float:left; "><b>Convert days:</b></div> Days to wait before enable convert this commission into phone credits. Leave zero for now.<br clear=both>
				<div class=clear style="margin-bottom:15px; margin-right:5px; float:left; "><b>Withdraw days:</b></div> Days to wait before enable check request for this commission. Leave zero for now.<br clear=both>
			</div>
		</div>

		$error_message
		<input type=hidden name=action value=commissions>
		<input type=hidden name=save value=$clickchain_id>
		<button type=button class=cancel onclick="window.location='$my_url'">Cancel</button>
		<button type=submit class=save onclick="modal_loadingblock()">Save</button>


	</form>

	
    ];
    &template_print("template.html",%t);
}
sub OLD_do_blocked_email_domains(){
    #
	#----------------
    # start
	#----------------
    $ok_message = "";
    $error_message = "";
	$error = "";
    #
	#----------------
    # try save
	#----------------
	if ($form{save} ne "") {
		if ( &multilevel_clickchain_check("bed",$form{save}) eq 1 ) {
			open(OUT,">$app_root/data/blocked.email.domains.txt");
			foreach (split(' ',$form{blocked_email_domains})){
				$_ = &trim($_);
				if ($_ eq "") {next}
				print OUT "$_\n";
			}
			close(OUT);
			$ok_message = "Setings saved.";
		}
	}
    #
	#----------------
    # load
	#----------------
	if ($form{save} eq "") {
		open(IN,"$app_root/data/blocked.email.domains.txt");
		$form{blocked_email_domains} = "";
		while (<IN>){
			chomp($_);
			$_ = &trim($_);
			if ($_ eq "") {next}
			$form{blocked_email_domains} .= "$_\n";
		}
		close(IN);
	}
    #
	#----------------
    # html messages
	#----------------
    #
	#----------------
    # html messages
	#----------------
    $message = ($ok_message eq "") ? "" : "<div class=alert_box ><div class=alert_box_inside>$ok_message</div></div><br>";
    $message = ($error_message eq "") ? $message : "<div class=alert_box ><div class=alert_box_inside>$error_message</div></div><br>";
    #
	#----------------
    # print page
	#----------------
    %t = ();
	$clickchain_id = &multilevel_clickchain_set("bed");
    $t{dic}{title}	= "<a href=$my_url>Settings</a> &#187; Blocked email domains";
    $t{dic}{content} = qq[

	<form action=$my_url name="mainform" method=post>

		<div class=clear style="width:500px; ">
			$message

			<fieldset><legend>Blocked email domanins</legend>
			Domains that we DO NOT accept in email when user request confirmation code to create one new account.
			Enter domain only (baddomain.com for user\@baddomain.com email), one per line.
			<textarea name=blocked_email_domains style="width:100%;height:150px;">$form{blocked_email_domains}</textarea>
			</fieldset>

		</div>
		<br>
		<input type=hidden name=action value=blocked_email_domains>
		<input type=hidden name=save value=$clickchain_id>
		<button type=button class=cancel onclick="window.location='$my_url'">Cancel</button>
		<button type=submit class=save onclick="modal_loadingblock()">Save</button>


	</form>

	
    ];
    &template_print("template.html",%t);
}
sub OLD_do_system_config(){
    #
	#----------------
    # start
	#----------------
    $ok_message = "";
    $error_message = "";
	$error = "";
    #
	#----------------
    # try save
	#----------------
	if ($form{save} eq 1) {
		#
		# check cs_email
		#$n = "cs_email";
		#$v1 = $form{$n};
		#$v2 = clean_str(substr($v1,0,512),".\@_-","MINIMAL");
		#if ( ($v1 eq "") || ($v1 ne $v2) ) {
		#	$error_message = "Check red fields";
		#	$error_field_cs_email = "background-color:red;";
		#}
		#
		# check cs_dialstring
		#$n = "cs_dialstring";
		#$v1 = $form{$n};
		#$v2 = clean_str(substr($v1,0,512),".\@_-()[]|&/","MINIMAL");
		#if ( ($v1 eq "") || ($v1 ne $v2) ) {
		#	$error_message = "Check red fields";
		#	$error_field_cs_dialstring = "background-color:red;";
		#}
		#
		#----------------------------
		# check credit commission
		#----------------------------
		$n = "commission_credit_value";
		$v1 = $form{$n};
		$v2 = clean_float(substr($v1,0,30));
		$v2++;
		$v2--;
		if ( ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_credit_value = "background-color:red;";
		}
		$n = "commission_credit_mode";
		$v1 = $form{$n};
		if (index("|SINGLE|ZENO|","|$v1|") eq -1) {
			$error_message = "Check red fields";
			$error_field_commission_credit_mode = "background-color:red;";
		}
		$n = "commission_credit_days_1";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_credit_days_1 = "background-color:red;";
		}
		$n = "commission_credit_days_2";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_credit_days_2 = "background-color:red;";
		}
		#
		#----------------------------
		# check free credit for public invite
		#----------------------------
		$n = "freecredit_public";
		$v1 = $form{$n};
		$v2 = clean_float(substr($v1,0,30));
		$v2++;
		$v2--;
		if ( ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_freecredit_public = "background-color:red;";
		}
		#
		#----------------------------
		# check free credit for private invite
		#----------------------------
		$n = "freecredit_private";
		$v1 = $form{$n};
		$v2 = clean_float(substr($v1,0,30));
		$v2++;
		$v2--;
		if ( ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_freecredit_private = "background-color:red;";
		}
		#
		#----------------------------
		# check new friend commission
		#----------------------------
		$n = "commission_newf_value";
		$v1 = $form{$n};
		$v2 = clean_float(substr($v1,0,30));
		$v2++;
		$v2--;
		if ( ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newf_value = "background-color:red;";
		}
		$n = "commission_newf_mode";
		$v1 = $form{$n};
		if (index("|SINGLE|ZENO|","|$v1|") eq -1) {
			$error_message = "Check red fields";
			$error_field_commission_newf_mode = "background-color:red;";
		}
		$n = "commission_newf_days_1";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newf_days_1 = "background-color:red;";
		}
		$n = "commission_newf_days_2";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newf_days_2 = "background-color:red;";
		}
		#
		#----------------------------
		# check new friend call commission
		#----------------------------
		$n = "commission_newfcall_value";
		$v1 = $form{$n};
		$v2 = clean_float(substr($v1,0,30));
		$v2++;
		$v2--;
		if ( ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newfcall_value = "background-color:red;";
		}
		$n = "commission_newfcall_mode";
		$v1 = $form{$n};
		if (index("|SINGLE|ZENO|","|$v1|") eq -1) {
			$error_message = "Check red fields";
			$error_field_commission_newfcall_mode = "background-color:red;";
		}
		$n = "commission_newfcall_days_1";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newfcall_days_1 = "background-color:red;";
		}
		$n = "commission_newfcall_days_2";
		$v1 = $form{$n};
		$v2 = clean_int(substr($v1,0,30));
		if ( ($v2>3650) || ($v2<0) || ($v1 eq "") || ($v1 ne $v2) ) {
			$error_message = "Check red fields";
			$error_field_commission_newfcall_days_2 = "background-color:red;";
		}
		#
		#----------------------------
		# try to save
		#----------------------------
		if ($error_message eq "") {
			#&data_set("adm_data","cs","email",$form{cs_email});
			#&data_set("adm_data","cs","dialstring",$form{cs_dialstring});
			#&data_set("adm_data","billing","commission_base_value",$form{commission_vale});
			#
			&data_set("adm_data","commission","credit_percentage",$form{commission_credit_value});
			&data_set("adm_data","commission","credit_mode",$form{commission_credit_mode});
			&data_set("adm_data","commission","credit_activation_date_1",$form{commission_credit_days_1});
			&data_set("adm_data","commission","credit_activation_date_2",$form{commission_credit_days_2});
			#
			&data_set("adm_data","commission","newf_value",$form{commission_newf_value});
			&data_set("adm_data","commission","newf_mode",$form{commission_newf_mode});
			&data_set("adm_data","commission","newf_activation_date_1",$form{commission_newf_days_1});
			&data_set("adm_data","commission","newf_activation_date_2",$form{commission_newf_days_2});
			#
			&data_set("adm_data","commission","newfcall_value",$form{commission_newfcall_value});
			&data_set("adm_data","commission","newfcall_mode",$form{commission_newfcall_mode});
			&data_set("adm_data","commission","newfcall_activation_date_1",$form{commission_newfcall_days_1});
			&data_set("adm_data","commission","newfcall_activation_date_2",$form{commission_newfcall_days_2});
			#
			&data_set("adm_data","invite","private_freecredit",$form{freecredit_private});
			&data_set("adm_data","invite","public_freecredit",$form{freecredit_public});
			#
			foreach $i (0..9){
				&data_set("adm_data","router","filter_".$i, trim($form{"router_filter_".$i}) );
				&data_set("adm_data","router","string_".$i, trim($form{"router_string_".$i}) );
			}
			#
			open(OUT,">$app_root/data/blocked.email.domains.txt");
			foreach (split(' ',$form{blocked_email_domains})){
				$_ = &trim($_);
				if ($_ eq "") {next}
				print OUT "$_\n";
			}
			close(OUT);
			#
			$ok_message = "Setings saved.";
		}
	}
    #
	#----------------
    # load
	#----------------
	if ($form{save} ne 1) {
	    #$form{cs_email} 		= &data_get("adm_data","cs","email");
	    #$form{cs_dialstring} 	= &data_get("adm_data","cs","dialstring");
		#
		$form{commission_credit_value}	= &data_get("adm_data","commission","credit_percentage");
		$form{commission_credit_mode}	= &data_get("adm_data","commission","credit_mode");
		$form{commission_credit_days_1}	= &data_get("adm_data","commission","credit_activation_date_1");
		$form{commission_credit_days_2}	= &data_get("adm_data","commission","credit_activation_date_2");
		#
		$form{commission_newf_value}	= &data_get("adm_data","commission","newf_value");
		$form{commission_newf_mode}		= &data_get("adm_data","commission","newf_mode");
		$form{commission_newf_days_1}	= &data_get("adm_data","commission","newf_activation_date_1");
		$form{commission_newf_days_2}	= &data_get("adm_data","commission","newf_activation_date_2");
		#
		$form{commission_newfcall_value}	= &data_get("adm_data","commission","newfcall_value");
		$form{commission_newfcall_mode}		= &data_get("adm_data","commission","newfcall_mode");
		$form{commission_newfcall_days_1}	= &data_get("adm_data","commission","newfcall_activation_date_1");
		$form{commission_newfcall_days_2}	= &data_get("adm_data","commission","newfcall_activation_date_2");
		#
		$form{freecredit_private}	= &data_get("adm_data","invite","private_freecredit");
		$form{freecredit_public}	= &data_get("adm_data","invite","public_freecredit");
		#
		foreach $i (0..9){
		    $form{"router_filter_".$i} 	= &data_get("adm_data","router","filter_".$i);
		    $form{"router_string_".$i} 	= &data_get("adm_data","router","string_".$i);
		}
		#
		open(IN,"$app_root/data/blocked.email.domains.txt");
		$form{blocked_email_domains} = "";
		while (<IN>){
			chomp($_);
			$_ = &trim($_);
			if ($_ eq "") {next}
			$form{blocked_email_domains} .= "$_\n";
		}
		close(IN);
	}
    #
	#----------------
    # html messages
	#----------------
    if ($ok_message ne "") {
		$ok_message = qq[
		<div class=alert_box ><div>$ok_message
		</div>
		</div><br>
		];
	}
	if ($error_message ne "") {
		$error_message = qq[
			<font color=red>
			<img src=/noc/design/icons/error.png width=16 height=16 hspace=0 vspace=0 border=0 align=left>&nbsp;$error_message
			</font>
			<br>
		];
	}
    #
	#----------------
    # print page
	#----------------
    %t = ();
	$select_commission_credit_mode{$form{commission_credit_mode}} = "selected";
	$select_commission_newf_mode{$form{commission_newf_mode}} = "selected";
	$select_commission_newfcall_mode{$form{commission_newfcall_mode}} = "selected";
    #$t{dic}{title} = "System config$nn";
    $t{dic}{title}	= "<a href=$my_url>Config</a> &#187; System settings";
    $t{dic}{content} = qq[
	<div class=clear style="width:900px;">
		$ok_message		
		<form action=$my_url name="mainform" method=post>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 >

		<td valign=top width=410 >

			<fieldset><legend>Automatic commissions</legend>
				
				<b>Friend credit commission</b><br>
				<table border=0 colspan=0 cellpadding=0 cellspacing=0 style='border-top:1px solid #c0c0c0'>
				<td width=70	style='padding-left:0px;'>Percentage<br><input style='width:100%; $error_field_commission_credit_value' name=commission_credit_value value='$form{commission_credit_value}'></td>
				<td width=70	style='padding-left:5px;'>Mode<br><select style='width:100%; $error_field_commission_credit_mode' name=commission_credit_mode ><option $select_commission_credit_mode{SINGLE} value=SINGLE>Single</option><option $select_commission_credit_mode{ZENO} value=ZENO>Zeno</option></select></td>
				<td 			style='padding-left:5px;'>Convert days<br><input style='width:100%; $error_field_commission_credit_days_1' name=commission_credit_days_1 value='$form{commission_credit_days_1}' ></td>
				<td 			style='padding-left:5px;'>Withdraw days<br><input style='width:100%; $error_field_commission_credit_days_2' name=commission_credit_days_2 value='$form{commission_credit_days_2}' ></td>
				</table>
				<br>

				
				<b>New friend commission</b><br>
				<table border=0 colspan=0 cellpadding=0 cellspacing=0 style='border-top:1px solid #c0c0c0'>
				<td width=70	style='padding-left:0px;'>Value<br><input style='width:100%; $error_field_commission_newf_value' name=commission_newf_value value='$form{commission_newf_value}'></td>
				<td width=70	style='padding-left:5px;'>Mode<br><select style='width:100%; $error_field_commission_newf_mode' name=commission_newf_mode ><option $select_commission_newf_mode{SINGLE} value=SINGLE>Single</option><option $select_commission_newf_mode{ZENO} value=ZENO>Zeno</option></select></td>
				<td 			style='padding-left:5px;'>Convert days<br><input style='width:100%;  $error_field_commission_newf_days_1' name=commission_newf_days_1 value='$form{commission_newf_days_1}' ></td>
				<td 			style='padding-left:5px;'>Withdraw days<br><input style='width:100%; $error_field_commission_newf_days_2' name=commission_newf_days_2 value='$form{commission_newf_days_2}' ></td>
				</table>
				<br>


				<b>Friends first call commission</b><br>
				<table border=0 colspan=0 cellpadding=0 cellspacing=0 style='border-top:1px solid #c0c0c0'>
				<td width=70	style='padding-left:0px;'>Value<br><input style='width:100%; $error_field_commission_newfcall_value' name=commission_newfcall_value value='$form{commission_newfcall_value}'></td>
				<td width=70	style='padding-left:5px;'>Mode<br><select style='width:100%; $error_field_commission_newfcall_mode' name=commission_newfcall_mode ><option $select_commission_newfcall_mode{SINGLE} value=SINGLE>Single</option><option $select_commission_newfcall_mode{ZENO} value=ZENO>Zeno</option></select></td>
				<td 			style='padding-left:5px;'>Convert days<br><input style='width:100%; $error_field_commission_newfcall_days_1' name=commission_newfcall_days_1 value='$form{commission_newfcall_days_1}' ></td>
				<td 			style='padding-left:5px;'>Withdraw days<br><input style='width:100%; $error_field_commission_newfcall_days_2' name=commission_newfcall_days_2 value='$form{commission_newfcall_days_2}' ></td>
				</table>
				<a name=commission_help></a>
				<div class=clear id=commission_help_off >
					<a href="#commission_help" onclick="MyDisplay('commission_help_off',0);MyDisplay('commission_help_on',1);">Help</a><br>
				</div>
				<div class=clear id=commission_help_on style=display:none>
					<a href="#commission_help" onclick="MyDisplay('commission_help_off',1);MyDisplay('commission_help_on',0);">Close help</a><br>
					<font style='font-size:11px; color:#c0c0c0'>
					<b>enable/disable:</b> To disable, just enter zero as value.<br>
					<b>Single mode:</b> Only target service will get the 100% OF VALUE as commission and we do not send commissions for they parents.<br>
					<b>Zeno mode:</b> Send 50% OF THE VALUE as commission for target service, 25% to they parent, 12.5% to parent of parent and soo on<br>
					<b>Convert days:</b> Days to wait before enable convert this commission into phone credits. Leave zero for now.
					<b>Withdraw days:</b> Days to wait before enable check request for this commission. Leave zero for now.
					</font>
				</div>
			</fieldset><br>

			<fieldset><legend>Invite free credit</legend>
				<table border=0 colspan=0 cellpadding=0 cellspacing=0 >
				<td style='padding-left:0px;'>Free credit for public invites:<br	><input style='width:100%; $error_field_freecredit_public'	name=freecredit_public	value='$form{freecredit_public}' ></td>
				<td style='padding-left:5px;'>Free credit for private invites:<br	><input style='width:100%; $error_field_freecredit_private'	name=freecredit_private	value='$form{freecredit_private}'></td>
				</table>
				<a name=freecredit_help></a>
				<div class=clear id=freecredit_help_off >
					<a href="#freecredit_help" onclick="MyDisplay('freecredit_help_off',0);MyDisplay('freecredit_help_on',1);">Help</a><br>
				</div>
				<div class=clear id=freecredit_help_on style=display:none>
					<br>
					<a href="#freecredit_help" onclick="MyDisplay('freecredit_help_off',1);MyDisplay('freecredit_help_on',0);">Close help</a><br>
					<font style='font-size:11px; color:#c0c0c0'>
					Set zero to disable or value to set free credit for each type of invitation at the moment the client create new service.
					</font>
				</div>
			</fieldset><br>

			<br>
			$error_message
			<input type=hidden name=action value=system_config>
			<input type=hidden name=save value=1>
			<input type=submit value="save">
		</td>

		<td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>

		<td valign=top>

			<fieldset><legend>Blocked email domanins</legend>
			Domains that we DO NOT accept in email when user request confirmation code to create one new account.
			Enter domain only (baddomain.com for user\@baddomain.com email), one per line.
			<textarea name=blocked_email_domains style="width:100%;height:100px;">$form{blocked_email_domains}</textarea>
			</fieldset>



			<fieldset><legend>Destination route</legend>
			System use the first match from top to bottom, soo leave the last one as generic route.

			<table border=0 colspan=0 cellpadding=3 cellspacing=0 width=100%>
				<tr>
				<td><b>Filter</b></td>
				<td><b>Dial String</b></td>
				</tr>
				<tr><td><input style='width:100%; $error_field_router_filter_0'	name=router_filter_0 value='$form{router_filter_0}'></td><td><input style='width:100%; $error_field_router_string_0'	name=router_string_0 value='$form{router_string_0}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_1'	name=router_filter_1 value='$form{router_filter_1}'></td><td><input style='width:100%; $error_field_router_string_1'	name=router_string_1 value='$form{router_string_1}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_2'	name=router_filter_2 value='$form{router_filter_2}'></td><td><input style='width:100%; $error_field_router_string_2'	name=router_string_2 value='$form{router_string_2}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_3'	name=router_filter_3 value='$form{router_filter_3}'></td><td><input style='width:100%; $error_field_router_string_3'	name=router_string_3 value='$form{router_string_3}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_4'	name=router_filter_4 value='$form{router_filter_4}'></td><td><input style='width:100%; $error_field_router_string_4'	name=router_string_4 value='$form{router_string_4}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_5'	name=router_filter_5 value='$form{router_filter_5}'></td><td><input style='width:100%; $error_field_router_string_5'	name=router_string_5 value='$form{router_string_5}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_6'	name=router_filter_6 value='$form{router_filter_6}'></td><td><input style='width:100%; $error_field_router_string_6'	name=router_string_6 value='$form{router_string_6}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_7'	name=router_filter_7 value='$form{router_filter_7}'></td><td><input style='width:100%; $error_field_router_string_7'	name=router_string_7 value='$form{router_string_7}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_8'	name=router_filter_8 value='$form{router_filter_8}'></td><td><input style='width:100%; $error_field_router_string_8'	name=router_string_8 value='$form{router_string_8}'></td></tr>
				<tr><td><input style='width:100%; $error_field_router_filter_9'	name=router_filter_9 value='$form{router_filter_9}'></td><td><input style='width:100%; $error_field_router_string_9'	name=router_string_9 value='$form{router_string_9}'></td></tr>
				<tr>
					<td valign=top><font style='font-size:11px; color:#c0c0c0'>
					Filter match begin of E164 numbers (55 to brasil), full number if end with period (12121234567. for specific number) or any number if empty 
					</font></td>
					<td valign=top><font style='font-size:11px; color:#c0c0c0'>
					Dial string is a valid asterisk SIP dial string. You can use FULL for full e164 number, COUNTRY for country code and NUMBER for areacode+number.
					</td>
				</tr>
			</table>
			</fieldset>
		</td>

		</table>
		</form>
	</div>
	
    ];
    &template_print("template.html",%t);
}
sub do_service_status_matrix(){
	#
	#===========================================================================
	# pega data
	#===========================================================================
	$product_id = "";
	##################@status_dic_list = qw(name text ui_order ui_group can_add_refer refer_status can_collect_commission can_add_credit can_auto_recharge can_request_commission_check  switch_on_first_call switch_on_first_credit switch_on_suspicious limit_max_balance limit_max_recharges_in_7days limit_ani_channels call_flood_minutes_in_24hrs call_flood_calls_in_1hr call_flood_cross_service_dst_in_7days coupon_id_new_service coupon_id_auto_recharge_signin coupon_pause_all rate_id_dial_out rate_id_dial_in rate_id_callback);
	#@status_dic_list = qw(can_add_refer refer_status switch_on_first_call switch_on_first_credit switch_on_suspicious limit_ani_channels call_flood_minutes_in_24hrs call_flood_calls_in_1hr call_flood_cross_service_dst_in_7days coupon_id_new_service coupon_id_auto_recharge_signin coupon_pause_all rate_id_dial_out rate_id_dial_in rate_id_callback);
	# can_collect_commission can_add_credit can_auto_recharge can_request_commission_check limit_max_balance limit_max_recharges_in_7days 
	#
	# can_collect_radio_commission 
	# ALTER TABLE `multilevel`.`service_status` ADD COLUMN `can_collect_radio_commission` TINYINT(4)  DEFAULT 0 AFTER `can_collect_commission`;
	#
	@status_dic_list = qw(can_enter_CC_active_in_another_service can_enter_blacklisted_CC switch_on_dial_blacklisted_DST switch_on_enter_blacklisted_CC switch_on_enter_CC_active_in_another_service call_flood_minutes_in_24hrs call_flood_cross_service_dst_in_7days call_flood_calls_in_1hr switch_on_first_call switch_on_first_credit switch_on_suspicious switch_on_autorecharge_ok_charge switch_on_autorecharge_in switch_on_autorecharge_out signin_coupon_default_id signin_coupon_premium_id can_add_refer refer_status refer_status_premium name ui_order ui_group can_web_access can_receive_calls can_make_calls pin_locked need_ani_check can_collect_commission can_collect_radio_commission can_add_credit can_request_commission_check limit_max_balance limit_max_recharges_in_7days coupon_pause_all );
	$status_dic_string = join(",",@status_dic_list);
	$sql = "
	SELECT id,$status_dic_string
	FROM service_status
	where deleted=0 and product_id='$product_id' 
	";
	%status_list = database_select_as_hash($sql,$status_dic_string);
	%select_status_list = database_select_as_hash("SELECT id,name,ui_order,ui_group FROM service_status where product_id='$product_id' and deleted=0","name,ui_order,ui_group");
	%coupons_list = database_select_as_hash("SELECT id,title  FROM service_coupon_type where status=1 ","name");
	%rates_list = database_select_as_hash("SELECT id,name FROM rate","name");
	#
	#===========================================================================
	# try to save
	#===========================================================================
	$form_error_message = "";
	%form_error = ();
	%form_sql = ();
	if ($form{save} eq 1) {
		if (&multilevel_clickchain_check("psea",$form{click_chain}) eq 1) {
			$save_is_ok = 1;
			foreach $status_id (sort{$status_list{$a}{ui_order} <=> $status_list{$b}{ui_order}} keys %status_list){
				#
				#-----------------------------------
				# check integer (non blank)
				#-----------------------------------
				foreach $dic_name (qw(ui_order call_flood_minutes_in_24hrs call_flood_cross_service_dst_in_7days call_flood_calls_in_1hr)){
					$form_item_name 	= "dic:$dic_name:$status_id";
					unless(exists($form{$form_item_name})) {next}
					$form_item_value	= &trim(substr($form{$form_item_name},0,255));
					if (&form_check_integer($form_item_value) eq 1) {
						$form_sql{$form_item_name} = "update service_status set $dic_name='".&clean_int($form_item_value)."' where id='$status_id' ";
					} else {
						$save_is_ok = 0;
						$form_error{$form_item_name} = 1;
					}
				}
				#
				#-----------------------------------
				# check float (non blank)
				#-----------------------------------
				foreach $dic_name (qw(limit_max_balance limit_max_recharges_in_7days)){
					$form_item_name 	= "dic:$dic_name:$status_id";
					unless(exists($form{$form_item_name})) {next}
					$form_item_value	= &trim(substr($form{$form_item_name},0,255));
					if (&form_check_float($form_item_value) eq 1) {
						$form_sql{$form_item_name} = "update service_status set $dic_name='".&clean_float($form_item_value)."' where id='$status_id' ";
					} else {
						$save_is_ok = 0;
						$form_error{$form_item_name} = 1;
					}
				}
				#
				#-----------------------------------
				# check string (non blank)
				#-----------------------------------
				foreach $dic_name (qw(name ui_group)){					
					$form_item_name 	= "dic:$dic_name:$status_id";
					unless(exists($form{$form_item_name})) {next}
					$form_item_value	= &trim(substr($form{$form_item_name},0,255));
					if (&form_check_string($form_item_value) eq 1) {
						$form_sql{$form_item_name} = "update service_status set $dic_name='".substr(&database_escape(&trim(&clean_str($form_item_value,"()-_ .<>$,%"))),0,250)."' where id='$status_id' ";
					} else {
						$save_is_ok = 0;
						$form_error{$form_item_name} = 1;
					}
				}				
				#
				#-----------------------------------
				# check on/off (1/0 switchs)
				#-----------------------------------
				foreach $dic_name (qw(can_enter_CC_active_in_another_service can_enter_blacklisted_CC can_add_refer can_web_access can_receive_calls can_make_calls pin_locked need_ani_check can_collect_commission can_collect_radio_commission can_request_commission_check coupon_pause_all )){					
					$form_item_name 	= "dic:$dic_name:$status_id";
					unless(exists($form{$form_item_name})) {next}
					$form_item_value	= ($form{$form_item_name} eq 1) ? 1 : 0;
					$form_sql{$form_item_name} = "update service_status set $dic_name='$form_item_value' where id='$status_id' ";
				}				
				#
				#-----------------------------------
				# check on/off switchs that we need mix
				#-----------------------------------
				$form_item_name 	= "dic:can_add_credit:$status_id";
				$form_item_value	= ($form{$form_item_name} eq 1) ? 1 : 0;
				$form_sql{"dic:can_add_credit:$status_id"} = "update service_status set can_add_credit='$form_item_value' where id='$status_id' ";
				$form_sql{"dic:can_auto_recharge:$status_id"} = "update service_status set can_auto_recharge='$form_item_value' where id='$status_id' ";
				#
				#-----------------------------------
				# check select_status_list (empty as null)
				#-----------------------------------
				foreach $dic_name (qw(refer_status refer_status_premium switch_on_autorecharge_ok_charge switch_on_autorecharge_in switch_on_autorecharge_out switch_on_first_call switch_on_first_credit switch_on_suspicious switch_on_dial_blacklisted_DST switch_on_enter_blacklisted_CC switch_on_enter_CC_active_in_another_service)){					
					$form_item_name 	= "dic:$dic_name:$status_id";
					unless(exists($form{$form_item_name})) {next}
					$form_item_value	= &clean_int(substr($form{$form_item_name},0,255));
					if ($form_item_value eq "") {
						$form_sql{$form_item_name} = "update service_status set $dic_name=null where id='$status_id' ";
					} elsif (exists($select_status_list{$form_item_value})) {
						$form_sql{$form_item_name} = "update service_status set $dic_name='$form_item_value' where id='$status_id' ";
					} else {
						$save_is_ok = 0;
						$form_error{$form_item_name} = 1;
					}
				}				
				#
				#-----------------------------------
				# check coupons_list (empty as null)
				#-----------------------------------
				foreach $dic_name (qw(signin_coupon_default_id signin_coupon_premium_id)){					
					$form_item_name 	= "dic:$dic_name:$status_id";
					unless(exists($form{$form_item_name})) {next}
					$form_item_value	= &clean_int(substr($form{$form_item_name},0,255));
					if ($form_item_value eq "") {
						$form_sql{$form_item_name} = "update service_status set $dic_name=null where id='$status_id' ";
					} elsif (exists($coupons_list{$form_item_value})) {
						$form_sql{$form_item_name} = "update service_status set $dic_name='$form_item_value' where id='$status_id' ";
					} else {
						$save_is_ok = 0;
						$form_error{$form_item_name} = 1;
					}
				}				
			}
			#
			#-----------------------------------
			# apply changes if ok
			#-----------------------------------
			if ($save_is_ok eq 1) {
				foreach (keys %form_sql) { &database_do($form_sql{$_}) }
				cgi_redirect("$my_url?action=product_edit&product_id=$product_id");
			} else {
				$form_error_message = "<div class=alert_box xstyle=width:300px;><div><b>Not saved</b><br>Please check fields, fix and try again</div></div><br>";
			}
		}
	}
	#
	#===========================================================================
	# load form
	#===========================================================================
	if ($form{save} ne 1) {
		foreach $dic_name (@status_dic_list){
			foreach $status_id (keys %status_list){
				$form{"dic:$dic_name:$status_id"} = $status_list{$status_id}{$dic_name};
			}
		}		
	}
	#
	#===========================================================================
    # form data -> form html
	#===========================================================================
	%form_html = ();
	$ui_group_last = "";
	$error_style="background-color:#ff5c00;color:#ffffff;"; 
	foreach $status_id (sort{$status_list{$a}{ui_order} <=> $status_list{$b}{ui_order}} keys %status_list){
		#
		#---------------------------------------------------------
		# insert blank line to split status in all form groups
		#---------------------------------------------------------
		$ui_group_style = ""; # $ui_group_style = "border-top:20px solid #ebeadb;";
		$html_group 	= "";
		if ($status_list{$status_id}{ui_group} ne $ui_group_last) {
			$html_group 	= "<tr><td colspan=10 style='background-color:#ebeadb;'><b><i>$status_list{$status_id}{ui_group}</i></b></td></tr>";
		}
		$ui_group_last = $status_list{$status_id}{ui_group};
		#
		#---------------------------------------------------------
		# insert display settings group
		#---------------------------------------------------------
		$tmp0 = "display_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $tmp1="dic:ui_order:$status_id";	$tmp2=$form{$tmp1};	$tmp3=($form_error{$tmp1} eq 1)?$error_style:"";	$form_html{$tmp0} .= qq[<td style='$ui_group_style $tmp3'><input name="$tmp1" value="$tmp2"></td>];
	    $tmp1="dic:ui_group:$status_id";	$tmp2=$form{$tmp1};	$tmp3=($form_error{$tmp1} eq 1)?$error_style:"";	$form_html{$tmp0} .= qq[<td style='$ui_group_style $tmp3'><input name="$tmp1" value="$tmp2"></td>];
	    $tmp1="dic:name:$status_id";		$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:"";	$form_html{$tmp0} .= qq[<td style='$ui_group_style $tmp3'><input name="$tmp1" value="$tmp2"></td>];
		$form_html{$tmp0} .= "</tr>";
		#
		#---------------------------------------------------------
		# insert access settings group
		#---------------------------------------------------------
		$tmp0 = "accesss_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'>$status_list{$status_id}{name}</td>];
		$tmp1="dic:can_web_access:$status_id"; 		$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:can_receive_calls:$status_id";	$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:can_make_calls:$status_id"; 		$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:pin_locked:$status_id"; 			$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:need_ani_check:$status_id";		$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$form_html{$tmp0} .= "</tr>";
		#
		#---------------------------------------------------------
		# insert billing settings group
		#---------------------------------------------------------
		$tmp0 = "billing_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'>$status_list{$status_id}{name}</td>];
		$tmp1="dic:can_collect_commission:$status_id"; 			$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:can_collect_radio_commission:$status_id"; 	$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:can_add_credit:$status_id"; 					$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:can_request_commission_check:$status_id"; 	$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:can_enter_CC_active_in_another_service:$status_id"; 	$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:can_enter_blacklisted_CC:$status_id"; 				$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
	    $tmp1="dic:limit_max_balance:$status_id";				$tmp2=$form{$tmp1};	$tmp3=($form_error{$tmp1} eq 1)?$error_style:"";	$form_html{$tmp0} .= qq[<td style='$ui_group_style $tmp3'><input name="$tmp1" class=ar value="$tmp2"></td>];
	    $tmp1="dic:limit_max_recharges_in_7days:$status_id";	$tmp2=$form{$tmp1};	$tmp3=($form_error{$tmp1} eq 1)?$error_style:"";	$form_html{$tmp0} .= qq[<td style='$ui_group_style $tmp3'><input name="$tmp1" class=ar value="$tmp2"></td>];
		$tmp1="dic:coupon_pause_all:$status_id"; 				$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$form_html{$tmp0} .= "</tr>";
		#
		#---------------------------------------------------------
		# insert referral settings group
		#---------------------------------------------------------
		$tmp0 = "referral_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'>$status_list{$status_id}{name}</td>];
		$tmp1="dic:can_add_refer:$status_id"; 					$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		$tmp1="dic:refer_status:$status_id"; 			
			$tmp2=$form{$tmp1}; 
			$tmp3=($form_error{$tmp1} eq 1)?$error_style:""; 
			$form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'>];
			$form_html{$tmp0} .= qq[<option value=''>(select)</option>];
			$form_html{$tmp0} .= qq[<option value=''>&nbsp;</option>];
			foreach $tmp4 (sort{$select_status_list{$a}{ui_order} <=> $select_status_list{$b}{ui_order}} keys %select_status_list){
				$tmp5 = ($tmp2 eq $tmp4) ? "selected" : ""; 
				$form_html{$tmp0} .= qq[<option $tmp5 value='$tmp4'>$select_status_list{$tmp4}{name}</option>];
			}
			$form_html{$tmp0} .= qq[</select></td>];
		$tmp1="dic:refer_status_premium:$status_id"; 			
			$tmp2=$form{$tmp1}; 
			$tmp3=($form_error{$tmp1} eq 1)?$error_style:""; 
			$form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'>];
			$form_html{$tmp0} .= qq[<option value=''>(select)</option>];
			$form_html{$tmp0} .= qq[<option value=''>&nbsp;</option>];
			foreach $tmp4 (sort{$select_status_list{$a}{ui_order} <=> $select_status_list{$b}{ui_order}} keys %select_status_list){
				$tmp5 = ($tmp2 eq $tmp4) ? "selected" : ""; 
				$form_html{$tmp0} .= qq[<option $tmp5 value='$tmp4'>$select_status_list{$tmp4}{name}</option>];
			}
			$form_html{$tmp0} .= qq[</select></td>];
		$tmp1="dic:signin_coupon_default_id:$status_id"; 			
			$tmp2=$form{$tmp1}; 
			$tmp3=($form_error{$tmp1} eq 1)?$error_style:""; 
			$form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'>];
			$form_html{$tmp0} .= qq[<option value=''>(select)</option>];
			$form_html{$tmp0} .= qq[<option value=''>&nbsp;</option>];
			foreach $tmp4 (sort{$coupons_list{$a}{name} <=> $coupons_list{$b}{name}} keys %coupons_list){
				$tmp5 = ($tmp2 eq $tmp4) ? "selected" : ""; 
				$form_html{$tmp0} .= qq[<option $tmp5 value='$tmp4'>$coupons_list{$tmp4}{name}</option>];
			}
			$form_html{$tmp0} .= qq[</select></td>];
		$tmp1="dic:signin_coupon_premium_id:$status_id"; 			
			$tmp2=$form{$tmp1}; 
			$tmp3=($form_error{$tmp1} eq 1)?$error_style:""; 
			$form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'>];
			$form_html{$tmp0} .= qq[<option value=''>(select)</option>];
			$form_html{$tmp0} .= qq[<option value=''>&nbsp;</option>];
			foreach $tmp4 (sort{$coupons_list{$a}{name} <=> $coupons_list{$b}{name}} keys %coupons_list){
				$tmp5 = ($tmp2 eq $tmp4) ? "selected" : ""; 
				$form_html{$tmp0} .= qq[<option $tmp5 value='$tmp4'>$coupons_list{$tmp4}{name}</option>];
			}
			$form_html{$tmp0} .= qq[</select></td>];
		$form_html{$tmp0} .= "</tr>";
		#
		#---------------------------------------------------------
		# insert basic_switch settings group
		#---------------------------------------------------------
		$tmp0 = "basic_switch_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'>$status_list{$status_id}{name}</td>];
		foreach $tmp_item (qw(switch_on_first_call switch_on_first_credit)){
			$tmp1="dic:$tmp_item:$status_id"; 			
			$tmp2=$form{$tmp1}; 
			$tmp3=($form_error{$tmp1} eq 1)?$error_style:""; 
			$form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'>];
			$form_html{$tmp0} .= qq[<option value=''>&nbsp;</option>];
			foreach $tmp4 (sort{$select_status_list{$a}{ui_order} <=> $select_status_list{$b}{ui_order}} keys %select_status_list){
				$tmp5 = ($tmp2 eq $tmp4) ? "selected" : ""; 
				$form_html{$tmp0} .= qq[<option $tmp5 value='$tmp4'>$select_status_list{$tmp4}{name}</option>];
			}
			$form_html{$tmp0} .= qq[</select></td>];
		}
		$form_html{$tmp0} .= "</tr>";
		#
		#---------------------------------------------------------
		# insert autorecharge_switch settings group
		#---------------------------------------------------------
		$tmp0 = "autorecharge_switch_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'>$status_list{$status_id}{name}</td>];
		foreach $tmp_item (qw(switch_on_autorecharge_ok_charge switch_on_autorecharge_in switch_on_autorecharge_out)){
			$tmp1="dic:$tmp_item:$status_id"; 			
			$tmp2=$form{$tmp1}; 
			$tmp3=($form_error{$tmp1} eq 1)?$error_style:""; 
			$form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'>];
			$form_html{$tmp0} .= qq[<option value=''>&nbsp;</option>];
			foreach $tmp4 (sort{$select_status_list{$a}{ui_order} <=> $select_status_list{$b}{ui_order}} keys %select_status_list){
				$tmp5 = ($tmp2 eq $tmp4) ? "selected" : ""; 
				$form_html{$tmp0} .= qq[<option $tmp5 value='$tmp4'>$select_status_list{$tmp4}{name}</option>];
			}
			$form_html{$tmp0} .= qq[</select></td>];
		}
		$form_html{$tmp0} .= "</tr>";
		#
		#---------------------------------------------------------
		# insert flood settings group
		#---------------------------------------------------------
		$tmp0 = "flood_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'>$status_list{$status_id}{name}</td>];
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'><input disabled readonly class=ar value="1"></td>];
	    $tmp1="dic:call_flood_minutes_in_24hrs:$status_id";				$tmp2=$form{$tmp1};	$tmp3=($form_error{$tmp1} eq 1)?$error_style:"";	$form_html{$tmp0} .= qq[<td style='$ui_group_style $tmp3'><input name="$tmp1" class=ar value="$tmp2"></td>];
	    $tmp1="dic:call_flood_calls_in_1hr:$status_id";					$tmp2=$form{$tmp1};	$tmp3=($form_error{$tmp1} eq 1)?$error_style:"";	$form_html{$tmp0} .= qq[<td style='$ui_group_style $tmp3'><input name="$tmp1" class=ar value="$tmp2"></td>];
	    $tmp1="dic:call_flood_cross_service_dst_in_7days:$status_id";	$tmp2=$form{$tmp1};	$tmp3=($form_error{$tmp1} eq 1)?$error_style:"";	$form_html{$tmp0} .= qq[<td style='$ui_group_style $tmp3'><input name="$tmp1" class=ar value="$tmp2"></td>];
		$form_html{$tmp0} .= "</tr>";
		#
		#---------------------------------------------------------
		# insert basic_switch settings group
		#---------------------------------------------------------
		$tmp0 = "suspicious_switch_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'>$status_list{$status_id}{name}</td>];
		foreach $tmp_item (qw(switch_on_suspicious switch_on_dial_blacklisted_DST switch_on_enter_blacklisted_CC switch_on_enter_CC_active_in_another_service)){
			$tmp1="dic:$tmp_item:$status_id"; 			
			$tmp2=$form{$tmp1}; 
			$tmp3=($form_error{$tmp1} eq 1)?$error_style:""; 
			$form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'>];
			$form_html{$tmp0} .= qq[<option value=''>&nbsp;</option>];
			foreach $tmp4 (sort{$select_status_list{$a}{ui_order} <=> $select_status_list{$b}{ui_order}} keys %select_status_list){
				$tmp5 = ($tmp2 eq $tmp4) ? "selected" : ""; 
				$form_html{$tmp0} .= qq[<option $tmp5 value='$tmp4'>$select_status_list{$tmp4}{name}</option>];
			}
			$form_html{$tmp0} .= qq[</select></td>];
		}
		$form_html{$tmp0} .= "</tr>";
	}
	#
	#===========================================================================
    # print page
	#===========================================================================
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Services status and permissions";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Services status and permissions";
    $t{breadcrumb}{1}{url}		= "";
    $click_chain = &multilevel_clickchain_set("psea");
    $t{dic}{content}	= qq[
    	<form action=$my_url method=post>


		$form_error_message 

	    <fieldset style="padding-top:0px;"><legend style="font:normal normal 30px Trebuchet, Trebuchet MS, Arial, sans-serif; letter-spacing:-1px; margin:0; padding:1; border:0;">Status names</legend>
		    <div style=width:600px;margin-bottom:20px;>
  				This are your "service status" names, groups and order. 
  				We recomend if you edit this part, to keep things organized, save this changes first, then come back to edit other settings.
			</div>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
				<tr>
				<td width=50>Order</td>
				<td width=150>Group</td>
				<td >Name</td>
				</tr>
		    </thead>
		    <tbody >$form_html{display_settings}</tbody>
		    </table>
	    </fieldset>
	    <br>
	    <br>



	    <fieldset style="padding-top:0px;"><legend style="font:normal normal 30px Trebuchet, Trebuchet MS, Arial, sans-serif; letter-spacing:-1px; margin:0; padding:1; border:0;">Status settings</legend>
		    <div style=width:300px;margin-bottom:20px;>
		    	Control access, permissions, billing, referral and limit settings for services bellong to this status 
			</div>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
				<tr>
				<td ><h1>Access and permissions</h1></td>
				<td width=70>Can access web interface</td>
				<td width=70>Can receive calls</td>
				<td width=70>Can place calls</td>
				<td width=70>Access only by ANI/DST allowed</td>
				<td width=70>Check ANI by phone call <font size=1>(if possible)</font></td>
				</tr>
		    </thead>
		    <tbody >$form_html{accesss_settings}</tbody>
		    </table>
		    <br>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
				<tr>
				<td ><h1>Billing</h1></td>
				<td width=60>Can collect Zenofon commission</td>
				<td width=60>Can collect Radio commission</td>
				<td width=60>Can add credit</td>
				<td width=60>Can request commission check</td>
				<td width=60>Can enter CC in use by another service</td>
				<td width=60>Can enter CC in deny-list</td>
				<td width=60>Max phone balance allowed</td>
				<td width=60>Max phone recharges in 7 days</td>
				<td width=60>Pause all coupons</td>
				</tr>
		    </thead>
		    <tbody >$form_html{billing_settings}</tbody>
		    </table>
		    <br>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
		    	<tr>
				<td ><h1>Referral</h1></td>
				<td width=60>Can invite referral</td>
				<td width=120>New referral status if ANI is regular</td>
				<td width=120>New referral status if ANI is premium</td>
				<td width=150>Referral sign-in coupon if ANI is regular</td>
				<td width=150>Referral sign-in coupon if ANI is premium</td>
				</tr>
		    </thead>
		    <tbody >$form_html{referral_settings}</tbody>
		    </table>
		    <br>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
				<tr>
				<td ><h1>Calls flood limit</h1></td>
				<td width=80>Max calls count at same time</td>
				<td width=80>Max calls minutes in 24hrs</td>
				<td width=80>Max calls count in 1hr </td>
				<td width=80>Max calls count for one DST dialed from multiple services.</td>
				</tr>
		    </thead>
		    <tbody >$form_html{flood_settings}</tbody>
		    </table>

		</fieldset>



		</fieldset>
	    <br>
	    <br>





	    <fieldset style="padding-top:0px;"><legend style="font:normal normal 30px Trebuchet, Trebuchet MS, Arial, sans-serif; letter-spacing:-1px; margin:0; padding:1; border:0;">Auto switch status</legend>
		    <div style=width:400px;margin-bottom:20px;>
		    To control permission by user actions, we can ask system to switch status by some client actions.
			</div>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
				<tr>
				<td ><h1>Basic</h1></td>
				<td width=150>if first call,<br>change to</td>
				<td width=150>if first recharge,<br>change to</td>
				</tr>
		    </thead>
		    <tbody >$form_html{basic_switch_settings}</tbody>
		    </table>
		    <br>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
				<tr>
				<td ><h1>Auto-recharge</h1></td>
				<td width=150>if sign-in auto-recharge,<br>change to</td>
				<td width=150>if sign-out auto-recharge,<br>change to</td>
				<td width=150>if auto-recharge charge ok,<br>change to</td>
				</tr>
		    </thead>
		    <tbody >$form_html{autorecharge_switch_settings}</tbody>
		    </table>
		    <br>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
				<tr>
				<td ><h1>Suspicious</h1></td>
				<td width=150>if basic suspicious action change to</td>
				<td width=150>if client dial to blocked numbers, change to</td>
				<td width=150>if client enter blacklisted credit card, change to</td>
				<td width=150>if client enter credit card used by other service, change to</td>
				</tr>
		    </thead>
		    <tbody >$form_html{suspicious_switch_settings}</tbody>
		    </table>

		</fieldset>
	    <br>
	    <br>






		<input type=hidden name=action value=service_status_matrix>
		<input type=hidden name=product_id value=$product_id>
		<input type=hidden name=save value=1>
		<input type=hidden name=click_chain value=$click_chain>
		<button type=button class="cancel"	onclick="window.location='$my_url?action=product_edit&product_id=$product_id'">Cancel</button>
		<button type=submit class="save"  	>Save all settings</button>
		</tr></table>
	
		</form>
		<br>&nbsp;
    ];
    &template_print("template.html",%t);
	
}
#========================================================================
sub do_suspicious_ips() {
    #
	#----------------
    # start
	#----------------
    $ok_message = "";
    $error_message = "";
	$error = "";
    #
	#----------------
    # try save
	#----------------
	if ($form{save} ne "") {
		if ( &multilevel_clickchain_check("esi",$form{save}) eq 1 ) {
			$raw = ",";
			foreach (split(' ',$form{list})){
				$_ = &trim($_);
				if ($_ eq "") {next}
				$raw .= "$_,";
			}
			&data_set("adm_data","security","suspicious_ips",$raw);
			$ok_message = "Setings saved.";
		}
	}
    #
	#----------------
    # load
	#----------------
	if ($form{save} eq "") {
		$raw = &data_get("adm_data","security","suspicious_ips");
		$form{list} = "";
		foreach (split(/\,/,$raw)) {
			chomp($_);
			$_ = &trim($_);
			if ($_ eq "") {next}
			$form{list} .= "$_\n";
		}
	}
    #
	#----------------
    # html messages
	#----------------
    #
	#----------------
    # html messages
	#----------------
    $message = ($ok_message eq "") ? "" : "<div class=alert_box ><div class=alert_box_inside>$ok_message</div></div><br>";
    $message = ($error_message eq "") ? $message : "<div class=alert_box ><div class=alert_box_inside>$error_message</div></div><br>";
    #
	#----------------
    # print page
	#----------------
    %t = ();
	$clickchain_id = &multilevel_clickchain_set("esi");
    $t{title}	= "Suspicious IPs";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Suspicious IPs";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{content} = qq[
	<form action=$my_url name="mainform" method=post>
		<div class=clear style="width:300px; ">
			$message
			Always enable security code (captcha) and other securith limits for web access come from this IPs<br>
			<br>
			<textarea name=list style="width:100%;height:150px;">$form{list}</textarea><br>
			<font color=#c0c0c0>&nbsp;(Enter IP one per line)</font>
		</div>
		<br>
		<input type=hidden name=action value=suspicious_ips>
		<input type=hidden name=save value=$clickchain_id>
		<button type=button class=cancel onclick="window.location='$my_url'">Cancel</button>
		<button type=submit class=save onclick="modal_loadingblock()">Save</button>
	</form>
    ];
    &template_print("template.html",%t);
}
sub do_tmp_dst_block(){
    #
	#----------------
    # start
	#----------------
    $ok_message = "";
    $error_message = "";
	$error = "";
    #
	#----------------
    # try save
	#----------------
	if ($form{save} ne "") {
		if ( &multilevel_clickchain_check("esi",$form{save}) eq 1 ) {
			$raw = ",";
			foreach (split(' ',$form{list})){
				$_ = &trim($_);
				if ($_ eq "") {next}
				$raw .= "$_,";
			}
			$nothing = "                                                                                                    ";			
			$nothing = $nothing.$nothing.$nothing.$nothing.$nothing.$nothing.$nothing.$nothing.$nothing.$nothing;
			$nothing = $nothing.$nothing;
			$raw_and_nothing = $raw.$nothing;
			$raw1 = substr($raw_and_nothing,0,200);
			$raw2 = substr($raw_and_nothing,200,200);
			$raw3 = substr($raw_and_nothing,400,200);
			$raw4 = substr($raw_and_nothing,600,200);
			$raw5 = substr($raw_and_nothing,800,200);
			$raw6 = substr($raw_and_nothing,1000,200);
			$raw7 = substr($raw_and_nothing,1200,200);
			$raw8 = substr($raw_and_nothing,1400,200);
			$raw9 = substr($raw_and_nothing,1600,200);
			$raw10 = substr($raw_and_nothing,1800,200);
			&data_set("adm_data","security","tmp_dst_block",$raw1);
			&data_set("adm_data","security","tmp_dst_block_1",$raw2);
			&data_set("adm_data","security","tmp_dst_block_2",$raw3);
			&data_set("adm_data","security","tmp_dst_block_3",$raw4);
			&data_set("adm_data","security","tmp_dst_block_4",$raw5);
			&data_set("adm_data","security","tmp_dst_block_5",$raw6);
			&data_set("adm_data","security","tmp_dst_block_6",$raw7);
			&data_set("adm_data","security","tmp_dst_block_7",$raw8);
			&data_set("adm_data","security","tmp_dst_block_8",$raw9);
			&data_set("adm_data","security","tmp_dst_block_9",$raw10);
			$ok_message = "Setings saved.";
		}
	}
    #
	#----------------
    # load
	#----------------
	if ($form{save} eq "") {
		$raw = &data_get("adm_data","security","tmp_dst_block");
		$raw .= &data_get("adm_data","security","tmp_dst_block_1");
		$raw .= &data_get("adm_data","security","tmp_dst_block_2");
		$raw .= &data_get("adm_data","security","tmp_dst_block_3");
		$raw .= &data_get("adm_data","security","tmp_dst_block_4");
		$raw .= &data_get("adm_data","security","tmp_dst_block_5");
		$raw .= &data_get("adm_data","security","tmp_dst_block_6");
		$raw .= &data_get("adm_data","security","tmp_dst_block_7");
		$raw .= &data_get("adm_data","security","tmp_dst_block_8");
		$raw .= &data_get("adm_data","security","tmp_dst_block_9");
		$raw = trim($raw);
		$form{list} = "";
		foreach (split(/\,/,$raw)) {
			chomp($_);
			$_ = &trim($_);
			if ($_ eq "") {next}
			$form{list} .= "$_\n";
		}
	}
    #
	#----------------
    # html messages
	#----------------
    #
	#----------------
    # html messages
	#----------------
    $message = ($ok_message eq "") ? "" : "<div class=alert_box ><div class=alert_box_inside>$ok_message</div></div><br>";
    $message = ($error_message eq "") ? $message : "<div class=alert_box ><div class=alert_box_inside>$error_message</div></div><br>";
    #
	#----------------
    # print page
	#----------------
    %t = ();
	$clickchain_id = &multilevel_clickchain_set("esi");
    $t{title}	= "Temporary DST block";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Temporary DST block";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{content} = qq[
	<form action=$my_url name="mainform" method=post>
		<div class=clear style="width:300px; ">
			$message
			Block and log calls that DST number match any of this E164 prefix.<br>
			<br>
			<textarea name=list style="width:100%;height:150px;">$form{list}</textarea><br>
			<font color=#c0c0c0>&nbsp;(Enter E164 prefix one per line)</font>
		</div>
		<br>
		<input type=hidden name=action value=tmp_dst_block>
		<input type=hidden name=save value=$clickchain_id>
		<button type=button class=cancel onclick="window.location='$my_url'">Cancel</button>
		<button type=submit class=save onclick="modal_loadingblock()">Save</button>
	</form>
    ];
    &template_print("template.html",%t);
}
#========================================================================
sub do_agestatus_list(){
	#
	# pega a lista
	%hash = database_select_as_hash("select id,title, min_days,ui_order from service_age  ","title,min_days,ui_order");
 
	$html_list = "<table class=fields_group_table border=0 colspan=0 cellpadding=0 cellspacing=0>";
	$html_list .= "<tr><td>Title</td><td>Min Days</td><td>UI Order</td><td>Action</td></tr>";
    foreach $id (sort{ $hash{$a}{ui_order} <=> $hash{$b}{ui_order}} keys %hash) {
		$html_list .= "<tr>";
		$html_list .= "<td width=240 >".$hash{$id}{title}."</td>"; 
		$html_list .="<td width=120 >". $hash{$id}{min_days}."</td>" ; 
		$html_list .= "<td width=120 >".$hash{$id}{ui_order}."</td>" ;
		
	 	$html_list .= "<td width=120 >";
	 	$html_list .= "<a href=$my_url?action=agestatus_edit&id=$id onClick=\"modal_open(\'Edit service age status\',\'$my_url?action=agestatus_edit&id=$id\',300,360); return false;\">Edit</a>";
		$html_list .= "| <a href=$my_url?action=agestatus_del&id=$id onClick=\"modal_open(\'Delete service age status\',\'$my_url?action=agestatus_del&id=$id\',300,360); return false;\">Del</a>";
	
		$html_list .= "</td>";	   
		$html_list .= "</tr>";
	}
	$html_list .="</table>" ;  
	$html_list .= "<a href=$my_url?action=agestatus_add onClick=\"modal_open(\'Add service age status\',\'$my_url?action=agestatus_add\',300,360); return false;\">Add New</a>"; 
	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    #
    # print page
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Service age status</a>";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Service age status";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}	= qq[
	<div class=clear style=width:700px>
		<fieldset class=config_select_list><legend>Select Age Status</legend>
		<ul>
		$html_list
		</ul>
		</fieldset>
	</div>
    ];
	#foreach(170..400) {$t{dic}{content}	.= qq[$_ = &#$_;<br>];}
    &template_print("template.html",%t);
	
}
sub do_agestatus_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $status_id = clean_int(substr($form{id},0,100));
    %hash = database_select_as_hash("select 1,1,title,min_days, ui_order from service_age where id='$status_id' ","flag,title,min_days,ui_order");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{dic}{content} = "Invalid parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
	
	#---------------------------------------------------
	# get age status title
	#---------------------------------------------------
    $title  = $hash{1}{title} ;
    $min_days = $hash{1}{min_days} ;   
    $ui_order = $hash{1}{ui_order} ;     
    warning('title:'.$title.',min_days:'.$min_days.',ui order:'.$ui_order);
    
	#
	#-------------------------------------------
	# start
	#-------------------------------------------
	%t = ();
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_ok = 0;
	$form_message = "";
 	if ($form{save} eq 1) {
		 if ($form{title} eq "") {
			$form_ok = 0;
			$form_message = "Please input title <br><br>";
			$form{title} = "";
		} elsif ( ($form{min_days} eq "") || ($form{min_days} <= 0 )) {
			$form_ok = 0;
			$form_message = "Please input an integer value for  min days<br><br>";
			$form{min_days} = "";			
		} elsif ( ($form{ui_order} eq "")  )   { 
			$form_ok = 0;
			$form_message = "Please input ui order <br><br>";
			$form{ui_order} = "";
		 	
		}else {
			$form_ok = 1;
		} 
		
	}
	#
	$form{min_days} = clean_int(substr($form{min_days},0,30 ));	
	$form{ui_order} = clean_int(substr($form{ui_order},0,30 ));
	$form{title}	= &database_escape($form{title});
	 
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&database_do("update service_age set title ='$form{title}',min_days ='$form{min_days}',ui_order='$form{ui_order}'  where id='$status_id' ");
		&action_history("noc:config:agestatus:edit",('id'=>$status_id,'adm_user_id'=>$app{session_cookie_u}));
		%t = ();
	    $t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	    &template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} ne 1) {
		$form{title} = $title;
		$form{min_days} = $min_days ;
		$form{ui_order} = $ui_order ;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
 
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[
	Change Age Status
	<br>
	<br>
	<form action=$my_url>
	 Title
	 <br>
	 <input name="title" value="$form{title}" /><br>
	 Min Days <br>
	 <input name="min_days" value="$form{min_days}" /><br>
	 UI Order<br>
	 <input name="ui_order" value="$form{ui_order}" /><br>
	 
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=id value=$status_id>
	<input type=hidden name=action value=agestatus_edit>
    ];
    &template_print("template.modal.html",%t);
}
sub do_agestatus_add(){
   
	#
	#-------------------------------------------
	# start
	#-------------------------------------------
	%t = ();
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_ok = 0;
	$form_message = "";
	
	if ($form{save} eq 1) {
		 if ($form{title} eq "") {
			$form_ok = 0;
			$form_message = "Please input title <br><br>";
			$form{title} = "";
		} elsif ( ($form{min_days} eq "") || ($form{min_days} <= 0 )) {
			$form_ok = 0;
			$form_message = "Please input an integer value for  min days<br><br>";
			$form{min_days} = "";			
		} elsif ( ($form{ui_order} eq "")  )   { 
			$form_ok = 0;
			$form_message = "Please input ui order <br><br>";
			$form{ui_order} = "";
		 	
		}else {
			$form_ok = 1;
		} 
		
	}
	#
	$form{min_days} = clean_int(substr($form{min_days},0,30 ));	
	$form{ui_order} = clean_float(substr($form{ui_order},0,30 ));
	$form{title}	= &database_escape($form{title});
	 
	 
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&database_do("insert into service_age(title,min_days,ui_order) values ('$form{title}','$form{min_days}','$form{ui_order}')");
		&action_history("noc:config:agestatus:add",('title'=>$form{title},'adm_user_id'=>$app{session_cookie_u}));
		%t = ();
	    $t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	    &template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} ne 1) {
#		$form{title} = $title;
#		$form{threshold_days} = $threshold_days ;
#		$form{commission_factor} = $commission_factor ;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
 
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[
	Change Age Status
	<br>
	<br>
	<form action=$my_url>
	 Title
	 <br>
	 <input name="title" value="$form{title}" /><br>
	 Min Days <br>
	 <input name="min_days" value="$form{min_days}" /><br>
	 UI Order <br>
	 <input name="ui_order" value="$form{ui_order}" /><br>
	 
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=action value=agestatus_add>
    ];
    &template_print("template.modal.html",%t);
}
sub do_agestatus_del(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $status_id = clean_int(substr($form{id},0,100));
    %hash = database_select_as_hash("select 1,1,title,min_days, ui_order  from service_age  where id='$status_id' ","flag,title,threshold_days,commission_factor");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{dic}{content} = "Invalid parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
	
	#---------------------------------------------------
	# get age status title
	#---------------------------------------------------
    $title  = $hash{1}{title} ;
    $min_days = $hash{1}{min_days} ;   
    $ui_order = $hash{1}{ui_order} ;     
     
	#
	#-------------------------------------------
	# start
	#-------------------------------------------
	%t = ();
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_ok = 1;
	$form_message = "";
	 
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&database_do("delete from  service_age where id='$status_id' ");
		&action_history("noc:config:agestatus:del",('id'=>$status_id,'adm_user_id'=>$app{session_cookie_u}));
		%t = ();
	    $t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	    &template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} ne 1) {
		$form{title} = $title;
		$form{min_days} = $min_days ;
		$form{ui_order} = $ui_order ;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
 
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[
	Delete Service Age Status
	<br>
	<br>
	<form action=$my_url>
	 Are you sure to delete this age status information ? 
	<br>
	<br>
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Delete</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=id value=$status_id>
	<input type=hidden name=action value=agestatus_del>
    ];
    &template_print("template.modal.html",%t);
}
#========================================================================
sub do_commissions(){
  	#
	# get engines types 
	%html_list =();
	%commission_engines = database_select_as_hash("SELECT id,ui_order,title,text FROM service_commission_type_engine","ui_order,title,text");
	#
	# prepare default for each engine
	foreach $engine (keys %commission_engines) {
	 	$html_list{$engine} =qq[
	 	<br>
	 	<center>
	 	No Configurations for this<br>type of commission<br><br> 
	 	<button onClick=\"modal_open(\'Create commission setting\',\'$my_url?action=commission_type_add&engine=$engine\',400,330); return false;\">Create Now</button>
	 	</center>
	 	]; 
	}
	#
	# check each engine data
	%hash = database_select_as_hash("select id, engine,title, value,value_type, apply_mode, days_to_convert_to_credit, days_to_convert_to_check  from service_commission_type","engine,title,value,value_type,apply_mode,days_to_convert_to_credit,days_to_convert_to_check");
	foreach $id (sort{ $hash{$a}{engine} cmp $hash{$b}{engine}} keys %hash) {
     	$engine = $hash{$id}{engine} ;
		$is_phone_enabled = ( index("|REFERRAL_FIRST_CALL|REFERRAL_DIALOUT_DST|REFERRAL_DIALOUT_DID|SERVICE_FIRST_CALL|SERVICE_DIALOUT_DST|SERVICE_DIALOUT_DID|SERVICE_RADIO_DID|","|$engine|") eq -1 ) ? 0 : 1;
     	$phone_table_edit = "";
    	if ($is_phone_enabled eq 1) {
	     	$phone_table_edit = qq[
			<button onClick="window.location='$my_url?action=commission_type_by_call_number&type_id=$id'">Edit phone values</button>
	     	];
		}
		$tmp = "by $hash{$id}{value_type}";
		$tmp = ($hash{$id}{value_type} eq "VALUE"			) ? "fixed value" : $tmp;
		$tmp = ($hash{$id}{value_type} eq "PERCENTAGE"		) ? "percent of value" : $tmp;
		$tmp = ($hash{$id}{value_type} eq "BY_CALL_MINUTES"	) ? "per call minutes" : $tmp;
     	$html_list{$engine}  = qq[
	     	<table class=fields_group_table border=0 colspan=0 cellpadding=0 cellspacing=0>
		     	<tr><td width=240 >Description</td><td> $hash{$id}{title}</td></tr>
		     	<tr><td>Commission </td><td>$hash{$id}{value}, $tmp</td></tr>
		     	<tr><td>Mode</td><td>$hash{$id}{apply_mode}</td></tr> 
		     	<tr><td>Convert days</td><td>$hash{$id}{days_to_convert_to_credit}</td></tr>
		     	<tr><td>Withdraw days</td><td>$hash{$id}{days_to_convert_to_check}</td></tr>
	     	</table>	
	     	<hr>
     		<button onClick="modal_open('Edit Commission Type','$my_url?action=commission_type_edit&type_id=$id',400,330); return false;">Edit</button>
			<button onClick="modal_open('Delete Commission Type','$my_url?action=commission_type_del&type_id=$id',300,150); return false;">Delete</button>
			<button onClick="window.location='$my_url?action=commission_type_age&type_id=$id'">Edit Age Discount</button>
			$phone_table_edit
    	];
	}
	#
    # print page
    %t = ();
    $t{my_url}		= $my_url;
    $t{title}	= "Commissions type";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Commissions type";
    $t{breadcrumb}{2}{url}		= "$my_url?action=commissions";
	foreach $engine (sort{$commission_engines{$a}{ui_order} <=> $commission_engines{$b}{ui_order}} keys %commission_engines) {
	    $t{content} .= qq[
		<div class=clear style="float:left; width:480px; ">
		<fieldset style="margin-bottom:20px;margin-right:20px; padding:10px; height:210px;">
			<legend>$commission_engines{$engine}{title}</legend>
	     	$commission_engines{$engine}{text}<br>
	     	<hr>
			$html_list{$engine}
 		</fieldset>
 		</div>
	 	]; 
	}
	#foreach(170..400) {$t{content}	.= qq[$_ = &#$_;<br>];}
    &template_print("template.html",%t);
}
sub do_commission_type_add(){   
	#
	#-------------------------------------------
	# start
	#-------------------------------------------
	%t = ();
	$engine = $form{engine};
	$is_phone_enabled = ( index("|REFERRAL_FIRST_CALL|REFERRAL_DIALOUT_DST|REFERRAL_DIALOUT_DID|SERVICE_FIRST_CALL|SERVICE_DIALOUT_DST|SERVICE_DIALOUT_DID|SERVICE_RADIO_DID|","|$engine|") eq -1 ) ? 0 : 1;
	%commission_engines = database_select_as_hash("SELECT id,ui_order,title,text FROM service_commission_type_engine","ui_order,title,text");
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_ok = 0;
	$form_message = "";
	if ($form{save} eq 1) {
		 if ($form{engine} eq "") {
			$form_ok = 0;
			$form_message = "Please check input engine <br><br>";
			$form{engine} = "";
		}elsif ($form{title} eq "") {
			$form_ok = 0;
			$form_message = "Please check input description <br><br>";
			$form{title} = "";
		} elsif ( ($form{value} eq "") || ($form{value} < 0 )) {
			$form_ok = 0;
			$form_message = "Please check input commission value<br><br>";
			$form{value} = "";			
		} elsif (index("|VALUE|PERCENTAGE|BY_CALL_MINUTES|","|$form{value_type}|") eq -1) {
			$form_ok = 0;
			$form_message = "Please check value_type<br><br>";
			$form{value} = "";			
		} elsif (index("|SINGLE|ZENO|","|$form{apply_mode}|") eq -1) {
			$form_ok = 0;
			$form_message = "Please check apply_mode<br><br>";
			$form{value} = "";			
		}elsif ( ($form{days_to_convert_to_credit} eq "") || ($form{days_to_convert_to_credit} < 0 )) {
			$form_ok = 0;
			$form_message = "Please check input days_to_convert_to_credit<br><br>";
			$form{days_to_convert_to_credit} = "";			
		}elsif ( ($form{days_to_convert_to_check} eq "") || ($form{days_to_convert_to_check} < 0 )) {
			$form_ok = 0;
			$form_message = "Please check input days_to_convert_to_check<br><br>";
			$form{days_to_convert_to_check} = "";			
		}else {
			$form_ok = 1;
		} 
	}
	$form{days_to_convert_to_credit}	= clean_int(substr($form{days_to_convert_to_credit},0,30));	
	$form{days_to_convert_to_check}		= clean_int(substr($form{days_to_convert_to_check},0,30));
 	$form{value} 						= clean_float(substr($form{value},0,30));
	$form{title}						= &database_escape($form{title});
	$form{engine}						= &database_escape($form{engine});
	$form{value_type}					= &database_escape($form{value_type});
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&database_do("
			insert into service_commission_type
			(engine,title,value,value_type,apply_mode,days_to_convert_to_credit,days_to_convert_to_check) values 
			('$form{engine}','$form{title}','$form{value}','$form{value_type}','$form{apply_mode}','$form{days_to_convert_to_credit}','$form{days_to_convert_to_check}')
			");
		&action_history("noc:config:commtype:add",('title'=>$form{title},'adm_user_id'=>$app{session_cookie_u}));
		%t = ();
	    $t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	    &template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} ne 1) {
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $t{dic}{my_url}	= $my_url;
    $tmp = ($is_phone_enabled eq 1) ? "<option $select_apply_mode{BY_CALL_MINUTES} value=BY_CALL_MINUTES>per call minutes</option>" : "";
    $t{dic}{content}	= qq[
	<h1>'$commission_engines{$engine}{title}'</h1><hr><br>
	<form action=$my_url>
		<table>
			<tr>
			<td width=100>Description</td>
			<td width=250><input name="title" value="$form{title}" /></td>
			</tr>
	 		<tr>
	 		<td>Commission </td>
	 		<td><input type="text" name="value" value="$form{value}"  style="width:20%" /> 
	 			<select style='width:60%; $error_value_type;  ' name=value_type>
	   			<option $select_apply_mode{VALUE} value=VALUE>fixed value</option>
	   			<option $select_apply_mode{PERCENTAGE} value=PERCENTAGE>percent of value</option>
	   			$tmp 
	   			</select>
	   		</td>
	   		</tr>
	 		<tr>
	 		<td>Mode</td>
	 		<td> <select style='width:40%; $error_apply_mode; ' name=apply_mode >
	   			<option $select_apply_mode{SINGLE} value=SINGLE>Single</option>
	   			<option $select_apply_mode{ZENO} value=ZENO>Zeno</option>
	   			</select>
			</td>
			</tr>
	 		<tr>
	 		<td>Convert days</td>
	 		<td> <input   name="days_to_convert_to_credit" value="$form{days_to_convert_to_credit}"  style="width:40%" /></td>
	 		</tr>
	  		<tr>
	  		<td>Withdraw days</td>
	  		<td>  <input name="days_to_convert_to_check" value="$form{days_to_convert_to_check}" style="width:40%" /></td>
	  		</tr>
		</table>
	 <br>
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=engine value=$form{engine}>
	<input type=hidden name=action value=commission_type_add>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_commission_type_edit(){
	#
	#-------------------------------------------
	# start
	#-------------------------------------------
	%t = ();
	#
	#-------------------------------------------
    # get data by id
	#-------------------------------------------
    $type_id = clean_int(substr($form{type_id},0,100)); 
    %hash = database_select_as_hash(
    	"select 1,1,engine,title,value,value_type,apply_mode,days_to_convert_to_credit,days_to_convert_to_check from service_commission_type where id='$type_id' ",
    	"flag,engine,title,value,value_type,apply_mode,days_to_convert_to_credit,days_to_convert_to_check"
    );
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
	$engine 					= $hash{1}{engine} ;
	$title 						= $hash{1}{title};
	$engine 					= $hash{1}{engine};
	$value 						= $hash{1}{value};
	$value_type 				= $hash{1}{value_type};
	$apply_mode 				= $hash{1}{apply_mode};
	$days_to_convert_to_credit	= $hash{1}{days_to_convert_to_credit};
	$days_to_convert_to_check 	= $hash{1}{days_to_convert_to_check};
	$is_phone_enabled 			= ( ($engine eq 'SERVICE_DIALOUT_DST') || ($engine eq 'SERVICE_DIALOUT_DID')  || ($engine eq 'SERVICE_RADIO_DID') ) ? 1 : 0;
	%commission_engines 		= database_select_as_hash("SELECT id,ui_order,title,text FROM service_commission_type_engine","ui_order,title,text");
	#	
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_ok = 0;
	$form_message = "";
	if ($form{save} eq 1) {
		if ($form{title} eq "") {
			$form_ok = 0;
			$form_message = "Please check input description <br><br>";
			$form{title} = "";
		} elsif ( ($form{value} eq "") || ($form{value} < 0 )) {
			$form_ok = 0;
			$form_message = "Please check input commission value<br><br>";
			$form{value} = "";			
		} elsif (index("|VALUE|PERCENTAGE|BY_CALL_MINUTES|","|$form{value_type}|") eq -1) {
			$form_ok = 0;
			$form_message = "Please check value_type<br><br>";
			$form{value} = "";			
		} elsif (index("|SINGLE|ZENO|","|$form{apply_mode}|") eq -1) {
			$form_ok = 0;
			$form_message = "Please check apply_mode<br><br>";
			$form{value} = "";			
		}elsif ( ($form{days_to_convert_to_credit} eq "") || ($form{days_to_convert_to_credit} < 0 )) {
			$form_ok = 0;
			$form_message = "Please check input days_to_convert_to_credit<br><br>";
			$form{days_to_convert_to_credit} = "";			
		}elsif ( ($form{days_to_convert_to_check} eq "") || ($form{days_to_convert_to_check} < 0 )) {
			$form_ok = 0;
			$form_message = "Please check input days_to_convert_to_check<br><br>";
			$form{days_to_convert_to_check} = "";			
		}else {
			$form_ok = 1;
		} 
	}
	#
	$form{days_to_convert_to_credit} 	= clean_int(substr($form{days_to_convert_to_credit},0,30 ));	
	$form{days_to_convert_to_check} 	= clean_int(substr($form{days_to_convert_to_check},0,30 ));
 	$form{value} 						= clean_float(substr($form{value},0,30 ));
	$form{title}						= &database_escape($form{title});
	$form{engine}						= &database_escape($form{engine});
	$form{value_type}					= &database_escape($form{value_type});
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&database_do("
			update service_commission_type set  
			title='$form{title}',
			value='$form{value}',
			value_type='$form{value_type}',
			apply_mode='$form{apply_mode}',
			days_to_convert_to_credit='$form{days_to_convert_to_credit}',
			days_to_convert_to_check='$form{days_to_convert_to_check}' 
			where id='$type_id'  
			");
		&action_history("noc:config:commtype:edit",('id'=>$type_id,'adm_user_id'=>$app{session_cookie_u}));
		%t = ();
	    $t{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	    &template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} ne 1) {
		$form{title} 						= $title;
		$form{value} 						= $value ;
		$select_engine{$engine} 			='selected' ;
		$select_apply_mode{$apply_mode} 	='selected' ;
		$select_value_type{$value_type} 	='selected' ;
 		$form{days_to_convert_to_credit}	= $days_to_convert_to_credit ;
		$form{days_to_convert_to_check} 	= $days_to_convert_to_check ;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $t{my_url}	= $my_url;
    $tmp = ($is_phone_enabled eq 1) ? "<option $select_value_type{BY_CALL_MINUTES} value=BY_CALL_MINUTES>per call minutes</option>" : "";
    $t{content}	= qq[
	<h1>'$commission_engines{$engine}{title}'</h1><hr><br>
	<form action=$my_url>
		<table>
			<tr>
			<td width=100>Description</td>
			<td width=250><input name="title" value="$form{title}" /></td>
			</tr>
	 		<tr>
	 		<td>Commission </td>
	 		<td><input type="text" name="value" value="$form{value}"  style="width:20%" /> 
	 			<select style='width:60%; $error_value_type;  ' name=value_type>
	   			<option $select_value_type{VALUE} value=VALUE>fixed value</option>
	   			<option $select_value_type{PERCENTAGE} value=PERCENTAGE>percent of value</option>
	   			$tmp 
	   			</select>
	   		</td>
	   		</tr>
	 		<tr>
	 		<td>Mode</td>
	 		<td> <select style='width:40%; $error_apply_mode; ' name=apply_mode >
	   			<option $select_apply_mode{SINGLE} value=SINGLE>Single</option>
	   			<option $select_apply_mode{ZENO} value=ZENO>Zeno</option>
	   			</select>
			</td>
			</tr>
	 		<tr>
	 		<td>Convert days</td>
	 		<td> <input   name="days_to_convert_to_credit" value="$form{days_to_convert_to_credit}"  style="width:40%" /></td>
	 		</tr>
	  		<tr>
	  		<td>Withdraw days</td>
	  		<td>  <input name="days_to_convert_to_check" value="$form{days_to_convert_to_check}" style="width:40%" /></td>
	  		</tr>
		</table>
	 <br>
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=type_id value=$form{type_id}>
	<input type=hidden name=action value=commission_type_edit>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_commission_type_del(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $type_id = clean_int(substr($form{type_id},0,100));
    %hash = database_select_as_hash("select 1,1,title,engine  from service_commission_type  where id='$type_id' ","flag,title,engine");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
	#---------------------------------------------------
	# get age status title
	#---------------------------------------------------
    $commission_title 	= $hash{1}{title};
    $commission_engine	= $hash{1}{engine};
	%commission_engines	= database_select_as_hash("SELECT id,ui_order,title,text FROM service_commission_type_engine","ui_order,title,text");
	$engine_title 		= $commission_engines{$commission_engine}{title};
	#
	#-------------------------------------------
	# start
	#-------------------------------------------
	%t = ();
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_ok = 1;
	$form_message = "";
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&database_do("delete from service_commission_type  where id='$type_id' ");
		&database_do("delete from service_commission_type_age_discount  where service_commission_type_id='$type_id' ");
		&database_do("delete from service_commission_type_by_call_number  where service_commission_type_id='$type_id' ");
		&action_history("noc:config:commtype:del",('id'=>$type_id,'adm_user_id'=>$app{session_cookie_u}));
		%t = ();
	    $t{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	    &template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} ne 1) {
		$form{title} = $title;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $t{my_url}	= $my_url;
    $t{content}	= qq[
	<form action=$my_url>
	Are you sure to delete '$engine_title' commission information ? 
	<br>
	<br>
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Delete</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=type_id value=$type_id>
	<input type=hidden name=action value=commission_type_del>
    ];
    &template_print("template.modal.html",%t);
}
sub do_commission_type_age(){
	#
	#-------------------------------------------
    # get data by id
	#-------------------------------------------
    $commission_id = clean_int(substr($form{type_id},0,100)); 
    %hash = database_select_as_hash("select 1,1,engine,title from service_commission_type where id='$commission_id' ","flag,engine,title");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.html",%t);
		exit;
	}
	$commission_engine 				= $hash{1}{engine} ;
	$commission_title 				= $hash{1}{title};
	$commission_is_phone_enabled 	= ( ($commission_engine eq 'SERVICE_DIALOUT_DST') || ($commission_engine eq 'SERVICE_DIALOUT_DID') ) ? 1 : 0;
	%commission_engines 			= database_select_as_hash("SELECT id,ui_order,title FROM service_commission_type_engine","ui_order,title");
	$commission_engine_title		= $commission_engines{$commission_engine}{title};
	#
	#-------------------------------------------
    # age list and values and build table
	#-------------------------------------------
  	%html_table 		= "";
  	$html_table_empty	= "<tr><td colspan=10><center><br>Empty...<br>&nbsp;</center></td></tr>";
  	%age_list 			= database_select_as_hash("select id,title,ui_order from service_age","title,ui_order");
	%age_values 		= database_select_as_hash("select service_age_id,discount_percentage from service_commission_type_age_discount where service_commission_type_id='$commission_id' ","value");
	foreach $age_id  (sort{$age_list{$a}{ui_order} <=>$age_list{$b}{ui_order} } keys %age_list) {
		$age_discount_value = $age_values{$age_id}{value};
		$age_discount_value++;
		$age_discount_value--;
		$html_link = "<a href=\"$my_url?action=commission_type_age_edit&type_id=$commission_id&age_id=$age_id\" onClick=\"modal_open(\'Commission Age discount\',\'$my_url?action=commission_type_age_edit&type_id=$commission_id&age_id=$age_id\',400,230); return false;\">";
		$html_table .= qq[
		 	<tr>
	 		<td>$html_link$age_list{$age_id}{title}</a></td>
	 	  	<td class=ar>$html_link$age_discount_value\%</a></td>
	 	  	</tr>
	 	]; 
	 	$html_table_empty = "";
	 }
	#
	#-------------------------------------------
    # age list and values and build table
	#-------------------------------------------
    $t{my_url}	= $my_url;
    $t{title}	= "<a href=$my_url>Settings</a> &#187; <a href=$my_url?action=commission_age?id_commission=$id_commission>Commission Type:$commission_list{$id_commission}{title} </a>";
    $t{title}	= "Edit age discount";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Commissions type";
    $t{breadcrumb}{2}{url}		= "$my_url?action=commissions";
    $t{breadcrumb}{3}{title}	= "'$commission_engine_title' commission";
    $t{breadcrumb}{3}{url}		= "$my_url?action=commissions";
    $t{breadcrumb}{4}{title}	= "Edit age discount";
    $t{breadcrumb}{4}{url}		= "#";
    $t{content}	= qq[
	<div class=clear style=width:400px>
		Edit service age discount to apply in '$commission_engine_title' commissions.<br>
		<br>

		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable>
			<thead>
				<tr>
				<td>Service age range</td>
				<td class=ar width=100>Discount</td>
				</tr>
			</thead>
			<tbody>
				$html_table
				$html_table_empty
			</tbody>
		</table>
		<br>
		<button type=button onclick="window.location='$my_url?action=commissions'">&#171; Back</button>
	</div>
    ];
	#foreach(170..400) {$t{content}	.= qq[$_ = &#$_;<br>];}
    &template_print("template.html",%t);
}
sub do_commission_type_age_edit(){
	#
	#-------------------------------------------
    # get data by id
	#-------------------------------------------
    $commission_id = clean_int(substr($form{type_id},0,100)); 
    %hash = database_select_as_hash("select 1,1,engine,title from service_commission_type where id='$commission_id' ","flag,engine,title");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
	$commission_engine 				= $hash{1}{engine} ;
	$commission_title 				= $hash{1}{title};
	$commission_is_phone_enabled 	= ( ($commission_engine eq 'SERVICE_DIALOUT_DST') || ($commission_engine eq 'SERVICE_DIALOUT_DID') ) ? 1 : 0;
	%commission_engines 			= database_select_as_hash("SELECT id,ui_order,title FROM service_commission_type_engine","ui_order,title");
	$commission_engine_title		= $commission_engines{$commission_engine}{title};
	#
	#-------------------------------------------
    # get data by id
	#-------------------------------------------
    $age_id 	= clean_int(substr($form{age_id},0,100)); 
  	%age_list 	= database_select_as_hash("select id,title,ui_order from service_age","title,ui_order");
	unless (exists($age_list{$age_id})){
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
	$age_title			= $age_list{$age_id}{title};
	%age_values 		= database_select_as_hash("select service_age_id,discount_percentage from service_commission_type_age_discount where service_commission_type_id='$commission_id' ","value");
	$age_discount_value = $age_values{$age_id}{value};
	$age_discount_value++;
	$age_discount_value--;
	#
	#-------------------------------------------
	# form action
	#-------------------------------------------
	$form_message = "";
	$form{discount_value} = &clean_float(substr($form{discount_value},0,30));
	$form{discount_value}++;
	$form{discount_value}--;
	if ($form{save} eq 1) {
		#
		#----------------------------
		# second time in form, lets try to save
		#----------------------------
		if ( ($form{discount_value}<0) || ($form{discount_value}>100) ) {
			#
			#----------------------------
			# invalid form value
			#----------------------------
			$form_message = "Please selecta  value from 0 to 100<br><br>";
		} else {
			# 
			#----------------------------
			# we have all ok to save
			#----------------------------
			#
			# garbage colector (clean in case we change age table)
			$allow_age_id = join(",",(keys %age_list));
			$sql = "delete FROM service_commission_type_age_discount where service_age_id not in ($allow_age_id)";
			&database_do($sql);
			#
			# delete old value
			$sql = &database_scape_sql("delete from service_commission_type_age_discount where service_commission_type_id='%d' and service_age_id='%d' ",$commission_id,$age_id);
			&database_do($sql);
			#
			# add new value
			$sql = &database_scape_sql("insert into service_commission_type_age_discount (service_commission_type_id,service_age_id,discount_percentage) values ('%d','%d','%s') ",$commission_id,$age_id,$form{discount_value});
			&database_do($sql);
			#
			# log
			&action_history("noc:config:commage:edit");
			#
			# reload page
			%t = ();
		    $t{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		    &template_print("template.modal.html",%t);
			exit;
		} 
	} else { 
		#
		#----------------------------
		# first time in form, lets populate form
		#----------------------------
    	$form{discount_value} = $age_discount_value;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
  
    $t{my_url}	= $my_url;
    $t{content}	= qq[
	<h1>Commission age discount</h1><hr>
	Enter discount value to apply in '$commission_engine_title' for services with '$age_title' age range 
	<br>
	<br>
	<form action=$my_url>
		Discount: <input name="discount_value" value="$form{discount_value}" style="width:75px" /> percent<br>
		<br>
		<font color=red><b>$form_message</b></font>
		<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
		<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
		<input type=hidden name=save value=1>
		<input type=hidden name=type_id value=$commission_id>
		<input type=hidden name=age_id value=$age_id>
		<input type=hidden name=action value=commission_type_age_edit>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_commission_type_by_call_number(){
	#
	#-------------------------------------------
    # get commission data
	#-------------------------------------------
    $commission_id = clean_int(substr($form{type_id},0,100)); 
    %hash = database_select_as_hash("select 1,1,engine,title,value_type,value from service_commission_type where id='$commission_id' ","flag,engine,title,value_type,value");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.html",%t);
		exit;
	}
	$commission_engine 				= $hash{1}{engine} ;
	$commission_title 				= $hash{1}{title};
	$commission_is_phone_enabled 	= ( index("|REFERRAL_FIRST_CALL|REFERRAL_DIALOUT_DST|REFERRAL_DIALOUT_DID|SERVICE_FIRST_CALL|SERVICE_DIALOUT_DST|SERVICE_DIALOUT_DID|SERVICE_RADIO_DID|","|$commission_engine|") eq -1 ) ? 0 : 1;
	%commission_engines 			= database_select_as_hash("SELECT id,ui_order,title FROM service_commission_type_engine","ui_order,title");
	$commission_engine_title		= $commission_engines{$commission_engine}{title};
	$commission_value_type			= $hash{1}{value_type};
	$commission_value_type_string	= "by $commission_value_type";
	$commission_value_type_string	= ($commission_value_type eq "VALUE"			) ? "fixed value" 		: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "PERCENTAGE"		) ? "percent of value"	: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "BY_CALL_MINUTES"	) ? "per call minutes"	: $commission_value_type_string	;
	$commission_value				= $hash{1}{value};
	$commission_value++;
	$commission_value--;
    if ($commission_is_phone_enabled ne 1) {
		%t = ();
		$t{content} = "Invalid commission type ($commission_is_phone_enabled,$commission_engine)";
		&template_print("template.html",%t);
		exit;
	}
    #
    #-----------------------------------------------
    # get page
    #-----------------------------------------------
    %hash = database_select_as_hash("select 1,1,count(*) FROM service_commission_type_by_call_number where service_commission_type_id='$commission_id' ","flag,count");
	$lines_count	= $hash{1}{count};
	$page_size		= clean_int($form{page_size});
	$page_size		= ($page_size eq "") ? 10 : $page_size;
	$page_min		= 1;
	$page_max		= int(($lines_count-1)/$page_size)+1;
	$page_max		= ($page_max<$page_min) ? $page_min : $page_max;
	$page	 		= clean_int($form{page});
	$page	 		= ($form{next} eq 1) ? $page+1 : $page;
	$page 			= ($form{previous} eq 1) ? $page-1 : $page;
	$page 			= ($page<$page_min) ? $page_min : $page;
	$page 			= ($page>$page_max) ? $page_max : $page;
	$sql_start		= ($page-1)*$page_size;
	$sql_stop		= $page_size;
	#
	#-------------------------------------------
    # get list and build table
	#-------------------------------------------
  	%html_table 		= "";
  	$html_table_empty	= "<tr><td colspan=10><center><br>Empty...<br>&nbsp;</center></td></tr>";
  	%numbers_list		= database_select_as_hash_with_auto_key(" 
	SELECT id,prefix,title,value 
	FROM service_commission_type_by_call_number 
	where service_commission_type_id='$commission_id' 
	order by prefix
	limit $sql_start,$sql_stop 
	","id,prefix,title,value");
	foreach $id  (sort{$a <=> $b} keys %numbers_list) {
		$number_id		= $numbers_list{$id}{id};
		$number_prefix 	= $numbers_list{$id}{prefix};
		$number_title	= $numbers_list{$id}{title};
		$number_value 	= $numbers_list{$id}{value};
		$number_value++;
		$number_value--;
		$html_link = "<a href=\"$my_url?action=commission_type_by_call_number_edit&number_id=$number_id\" onClick=\"modal_open(\'Edit value by phone number\',\'$my_url?action=commission_type_by_call_number_edit&number_id=$number_id\',400,400); return false;\">";
		$html_table .= qq[
		 	<tr>
	 		<td>$html_link$number_prefix</a></td>
	 		<td>$html_link$number_title</a></td>
	 	  	<td class=ar>$html_link$number_value $commission_value_type_string</a></td>
	 		<td class=ac><a href=\"$my_url?action=commission_type_by_call_number_del&number_id=$number_id\" onClick=\"modal_open(\'Delete phone number entry\',\'$my_url?action=commission_type_by_call_number_del&number_id=$number_id\',300,130); return false;\">[x]</a></td>
	 	  	</tr>
	 	]; 
	 	$html_table_empty = "";
	}
	#
	#-------------------------------------------
    # page select
	#-------------------------------------------
	$page_select = "";
	foreach($page_min..$page_max) {
		if  ( ($_ eq $page_min) || ($_ eq $page_max) || (int($_/100) eq ($_/100) ) ||  ( ($page>($_-100)) && ($page<($_+100)) ) ) {
			$tmp = ($_ eq $page) ? "selected" : ""; 
			$page_select .= "<option $tmp value=$_>Page: $_ of $page_max</option>";
		}
	}
	#
	#-------------------------------------------
    # age list and values and build table
	#-------------------------------------------
    $t{my_url}	= $my_url;
    $t{title}	= "<a href=$my_url>Settings</a> &#187; <a href=$my_url?action=commission_age?id_commission=$id_commission>Commission Type:$commission_list{$id_commission}{title} </a>";
    $t{title}	= "Value by phone number";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Commissions type";
    $t{breadcrumb}{2}{url}		= "$my_url?action=commissions";
    $t{breadcrumb}{3}{title}	= "'$commission_engine_title' commission";
    $t{breadcrumb}{3}{url}		= "$my_url?action=commissions";
    $t{breadcrumb}{4}{title}	= "Value by phone number";
    $t{breadcrumb}{4}{url}		= "#";
    $t{content}	= qq[
	<div class=clear style=width:600px>
		Default value for commission '$commission_engine_title' is '$commission_value $commission_value_type_string', 
		but if phone number match in this list, the value from list wins. <br>
		Remember all numbers in system are E164 format. We match the start of number. Example: Enter 5521 to mach country 55, areacode 21. Enter 1212 to match usa 212. Do not enter 1, because will match all country thar start with 1 (not only usa)<br>
		<br>

		<form action=$my_url>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable>
				<thead>
					<tr>
					<td>Contry, area, number</td>
					<td>Name</td>
					<td class=ar>Specific value</td>
					<td class=ar>Delete</td>
					</tr>
				</thead>
				<tbody>
					$html_table
					$html_table_empty
				</tbody>
				<tfoot>
					<tr><td colspan=4>
					<button type=submit name=previous value=1>&#171;</button>
					<select name=page onchange="document.forms[0].submit()">$page_select</select>
					<button type=submit name=next value=1>&#187;</button>
					</td></tr>
				</tfoot>
			</table>
			<a href="$my_url?action=commission_type_by_call_number_add&type_id=$commission_id" onClick="modal_open('Add new value by phone number','$my_url?action=commission_type_by_call_number_add&type_id=$commission_id',400,400); return false;" >&#187; Add new entry</a><br>
			<a href="$my_url?action=commission_type_by_call_number_upload&type_id=$commission_id" onClick="modal_open('Upload table','$my_url?action=commission_type_by_call_number_upload&type_id=$commission_id',350,220); return false;" >&#187; Upload table</a><br>
			<a href="$my_url?action=commission_type_by_call_number_download&type_id=$commission_id" >&#187; Download table</a><br>
			<input type=hidden name=action value=commission_type_by_call_number>
			<input type=hidden name=type_id value=$commission_id>
		</form>
		<br>
		<button type=button onclick="window.location='$my_url?action=commissions'">&#171; Back</button>
	</div>
    ];
    &template_print("template.html",%t);
}
sub do_commission_type_by_call_number_upload(){
	#
	#-------------------------------------------
    # get commission data
	#-------------------------------------------
    $commission_id = clean_int(substr($form{type_id},0,100)); 
    %hash = database_select_as_hash("select 1,1,engine,title,value_type,value from service_commission_type where id='$commission_id' ","flag,engine,title,value_type,value");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.html",%t);
		exit;
	}
	$commission_engine 				= $hash{1}{engine} ;
	$commission_title 				= $hash{1}{title};
	$commission_is_phone_enabled 	= ( index("|REFERRAL_FIRST_CALL|REFERRAL_DIALOUT_DST|REFERRAL_DIALOUT_DID|SERVICE_FIRST_CALL|SERVICE_DIALOUT_DST|SERVICE_DIALOUT_DID|SERVICE_RADIO_DID|","|$commission_engine|") eq -1 ) ? 0 : 1;
	%commission_engines 			= database_select_as_hash("SELECT id,ui_order,title FROM service_commission_type_engine","ui_order,title");
	$commission_engine_title		= $commission_engines{$commission_engine}{title};
	$commission_value_type			= $hash{1}{value_type};
	$commission_value_type_string	= "$commission_value_type";
	$commission_value_type_string	= ($commission_value_type eq "VALUE"			) ? "value" 		: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "PERCENTAGE"		) ? "percent"		: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "BY_CALL_MINUTES"	) ? "per_minute"	: $commission_value_type_string	;
	$commission_value				= $hash{1}{value};
	$commission_value++;
	$commission_value--;
    if ($commission_is_phone_enabled ne 1) {
		%t = ();
		$t{content} = "Invalid commission type";
		&template_print("template.html",%t);
		exit;
	}
	#
	#-------------------------------------------
    # process form 
	#-------------------------------------------
	$form_error_msg = "";
	if ($form{save} ne ""){
		if (&multilevel_clickchain_check("cpt",$form{save}) eq 1) {
		    #
			#-------------------------------------------
		    # save csv upload at tmp_file
			#-------------------------------------------
		    $temp_file = "/tmp/.upload.rate.".time.".tmp";
		    $filehandle = $cgi->param("FileUpload");
		    open(LOCAL, ">$temp_file");
		    while($bytesread=read($filehandle,$buffer,1024)) { print LOCAL $buffer; }
		    close(LOCAL);
		    #
			#-------------------------------------------
		    # get correct csv head 
			#-------------------------------------------
		    # to avoid upload percentage over rate per minute or value and make big mistakes, 
		    # we generate specific head at download and match this head at upload. 
		    # its a extra work for client but lower bad upload data by user
			$csv_header_correct = "prefix,name,$commission_value_type_string";
		    #
			#-------------------------------------------
		    # check csv header
			#-------------------------------------------
		    if ($form_error_msg eq "") {
			    open(LOCAL,$temp_file);
			    $line = <LOCAL>;
			    $csv_head = &csv_line_clean($line); 
			    if ("\L$csv_head" ne $csv_header_correct) {
					$form_error_msg = "incorrect CSV header. Correct header is '$csv_header_correct'. Check values and type changes (value,percentage or rate per minute) adn values with new type. ";
			    }
				close(LOCAL);
		    }
		    #
			#-------------------------------------------
		    # check csv data
			#-------------------------------------------
		    if ($form_error_msg eq "") {
		    	$error_count = 0;
				$line_count = 1;
			    open(LOCAL,$temp_file);
			    $line = <LOCAL>;
			    $prefix_buffer = "|";
				while (<LOCAL>){
					$line = $_;
					$line_count++;
					if ($error_count >3) { last;}
					if (&trim($line) eq "") {next}
				    @values = &csv_line_to_array($line); 
				    $values_qtd = @values; 
					if  ( $values_qtd ne 3 )  {$error_count++; $form_error_msg .="Incorrect collumns count at line $line_count. "; next;} 
				    $prefix = &clean_int($values[0]);
				    $name	= &clean_str($values[1]);
				    $value	= $values[2]; $value++; $value--;
					if  ( ($prefix eq "") || (clean_int($values[0]) ne $prefix) )  {$error_count++; $form_error_msg .="Incorrect prefix at line $line_count. "; next;} 
					if ($commission_value_type eq "VALUE") {
						if  ( ($value < 0) || ($value > 100) )  {$error_count++; $form_error_msg .="Incorrect value (0 to 100) at line $line_count. "; next;} 
					} elsif ($commission_value_type eq "PERCENTAGE") {
						if  ( ($value < 0) || ($value > 200) )  {$error_count++; $form_error_msg .="Incorrect value (0 to 100) at line $line_count. "; next;} 
					} elsif ($commission_value_type eq "BY_CALL_MINUTES") {
						if  ( ($value < 0) || ($value > 100) )  {$error_count++; $form_error_msg .="Incorrect value (0 to 100) at line $line_count. "; next;} 
					} else {
						$error_count++; $form_error_msg .="Incorrect value (0 to 100) at line $line_count. "; next;
					}
				    if (index($prefix_buffer,"|$prefix|") ne -1) {$error_count++; $form_error_msg .="Duplicate prefix '$prefix' at line $line_count. "; next;} 
				    $prefix_buffer .= "$prefix|";
				}
				close(LOCAL);
				if ($error_count > 0) {$form_error_msg .="CSV rejected with $error_count errors. ";}
		    }
		    #
			#-------------------------------------------
		    # apply csv data if possible
			#-------------------------------------------
		    if ($form_error_msg eq "") {
				database_do("delete from service_commission_type_by_call_number where service_commission_type_id='$commission_id' ");
			    open(LOCAL,$temp_file);
			    $line = <LOCAL>;
				while (<LOCAL>){
					$line = $_;
					if (&trim($line) eq "") {next}
				    @values = &csv_line_to_array($line); 
				    $prefix = &clean_int($values[0]);
				    $name	= &clean_str($values[1]);
				    $value	= $values[2]; $value++; $value--;
					$sql = &database_scape_sql(
						"insert into service_commission_type_by_call_number (service_commission_type_id,prefix,title,value) values ('%s','%s','%s','%s')",
						$commission_id,$prefix,$name,$value
					);
					database_do($sql);
				}
				close(LOCAL);
		    }
		    #
			#-------------------------------------------
		    # remove tmp_file
			#-------------------------------------------
		    unlink($temp_file);
		    #
			#-------------------------------------------
		    # return page
			#-------------------------------------------
		    if ($form_error_msg eq "") {
				%t = ();
			    $t{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			    &template_print("template.modal.html",%t);
				exit;
		    }
		} else {
			$form_error_msg = "Internal error. Try again";
		}
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$form_error_msg = ($form_error_msg eq "") ? "" : "<div class=alert_box><div class=alert_box_inside>$form_error_msg</div></div><br>";
	$save_id = &multilevel_clickchain_set("cpt");
    $t{my_url}	= $my_url;
    $t{content}	= qq[
	All data will be replaced by new uploaded data.<br>
	<br>
	<form action=$my_url method=post enctype="multipart/form-data" >
		CSV file:<br>
		<input name=FileUpload type=file><br>
		<br>
		$form_error_msg 
		<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
		<button type=submit><img src=/design/icons/tick.png align=left>Upload</button>
		<input type=hidden name=save value=$save_id>
		<input type=hidden name=type_id value=$commission_id>
		<input type=hidden name=action value=commission_type_by_call_number_upload>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub csv_line_to_array(){
	local($line) = @_;
	local($tmp,$tmp1,$tmp2,@array,@array1,@array2);
    @array = ();
	chomp($line);
	if (index($line,",") eq -1) {$tmp1 = "\t"; $tmp2=","; $line =~ s/$tmp1/$tmp2/eg; }
    foreach $tmp (split(/\,/,$line)){
	    $tmp1 = "\""; $tmp2=" "; $tmp =~ s/$tmp1/$tmp2/eg; 
	    $tmp1 = "\'"; $tmp2=" "; $tmp =~ s/$tmp1/$tmp2/eg; 
	    $tmp = trim($tmp);
	    @array = (@array,$tmp);
    }
    return @array
}
sub csv_line_clean(){
	local($line) = @_;
	return join(",",&csv_line_to_array($line));
}
sub do_commission_type_by_call_number_download(){
	#
	#-------------------------------------------
    # get commission data
	#-------------------------------------------
    $commission_id = clean_int(substr($form{type_id},0,100)); 
    %hash = database_select_as_hash("select 1,1,engine,title,value_type,value from service_commission_type where id='$commission_id' ","flag,engine,title,value_type,value");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.html",%t);
		exit;
	}
	$commission_engine 				= $hash{1}{engine} ;
	$commission_title 				= $hash{1}{title};
	$commission_is_phone_enabled 	= ( index("|REFERRAL_FIRST_CALL|REFERRAL_DIALOUT_DST|REFERRAL_DIALOUT_DID|SERVICE_FIRST_CALL|SERVICE_DIALOUT_DST|SERVICE_DIALOUT_DID|SERVICE_RADIO_DID|","|$commission_engine|") eq -1 ) ? 0 : 1;
	%commission_engines 			= database_select_as_hash("SELECT id,ui_order,title FROM service_commission_type_engine","ui_order,title");
	$commission_engine_title		= $commission_engines{$commission_engine}{title};
	$commission_value_type			= $hash{1}{value_type};
	$commission_value_type_string	= "$commission_value_type";
	$commission_value_type_string	= ($commission_value_type eq "VALUE"			) ? "value" 		: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "PERCENTAGE"		) ? "percent"		: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "BY_CALL_MINUTES"	) ? "per_minute"	: $commission_value_type_string	;
	$commission_value				= $hash{1}{value};
	$commission_value++;
	$commission_value--;
    if ($commission_is_phone_enabled ne 1) {
		%t = ();
		$t{content} = "Invalid commission type";
		&template_print("template.html",%t);
		exit;
	}
	#
	#-------------------------------------------
    # print header
	#-------------------------------------------
	$csv_title = &clean_str("$commission_engine_title - per country - $commission_value_type_string");
    #print "Content-type: text/plain\n";
    print "Pragma: public\n";
    print "Expires: 0\n";
    print "Cache-Control: must-revalidate, post-check=0, pre-check=0\n";
    print "Content-type: application/octet-stream\n";
    print "Content-Disposition: attachment; filename=\"$csv_title.csv\"\n";
    print "Content-Description: File Transfert\n";
    print "\n";
    print "prefix,name,$commission_value_type_string\n";
	#
	#-------------------------------------------
    # get data
	#-------------------------------------------
  	%numbers_list = database_select_as_hash(" 
	SELECT id,prefix,title,value 
	FROM service_commission_type_by_call_number 
	where service_commission_type_id='$commission_id' 
	order by prefix
	","prefix,title,value");
	foreach $number_id  (keys %numbers_list) {
		$number_prefix 	= $numbers_list{$number_id}{prefix};
		$number_title	= $numbers_list{$number_id}{title};
		$number_value 	= $numbers_list{$number_id}{value};
		$number_value++;
		$number_value--;
	    print "$number_prefix,\"$number_title\",$number_value\n";
	}
}
sub do_commission_type_by_call_number_edit(){
	#
	#-------------------------------------------
    # get number_id
	#-------------------------------------------
    $number_id	= clean_int(substr($form{number_id},0,100)); 
  	%hash 	= database_select_as_hash("select 1,1,prefix,title,value,service_commission_type_id from service_commission_type_by_call_number where  id='$number_id' ","flag,prefix,title,value,service_commission_type_id");
	if ($hash{1}{flag} ne 1){
		%t = ();
		$t{content} = "Invalid number_id parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
    $number_prefix	= $hash{1}{prefix}; 
	$number_title	= $hash{1}{title};
	$number_value	= $hash{1}{value};
	$commission_id	= $hash{1}{service_commission_type_id};
	$number_value++;
	$number_value--;
	#
	#-------------------------------------------
    # get commission by id
	#-------------------------------------------
    $commission_id = clean_int($commission_id); 
    %hash = database_select_as_hash("select 1,1,engine,title,value_type,value from service_commission_type where id='$commission_id' ","flag,engine,title,value_type,value");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.html",%t);
		exit;
	}
	$commission_engine 				= $hash{1}{engine} ;
	$commission_title 				= $hash{1}{title};
	$commission_is_phone_enabled 	= ( index("|REFERRAL_FIRST_CALL|REFERRAL_DIALOUT_DST|REFERRAL_DIALOUT_DID|SERVICE_FIRST_CALL|SERVICE_DIALOUT_DST|SERVICE_DIALOUT_DID|SERVICE_RADIO_DID|","|$commission_engine|") eq -1 ) ? 0 : 1;
	%commission_engines 			= database_select_as_hash("SELECT id,ui_order,title FROM service_commission_type_engine","ui_order,title");
	$commission_engine_title		= $commission_engines{$commission_engine}{title};
	$commission_value_type			= $hash{1}{value_type};
	$commission_value_type_string	= "by $commission_value_type";
	$commission_value_type_string	= ($commission_value_type eq "VALUE"			) ? "fixed value" 		: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "PERCENTAGE"		) ? "percent of value"	: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "BY_CALL_MINUTES"	) ? "per call minutes"	: $commission_value_type_string	;
	$commission_value				= $hash{1}{value};
	$commission_value++;
	$commission_value--;
	#
	#-------------------------------------------
	# form action
	#-------------------------------------------
	$form_message = "";
	$form{prefix}	= &clean_int(substr($form{prefix},0,255));
	$form{title}	= &trim(substr($form{title},0,255));
	$form{value}	= &clean_float(substr($form{value},0,30));
	$form{value}++;
	$form{value}--;
	if ($form{save} eq 1) {
		#
		#----------------------------
		# second time in form, lets try to save
		#----------------------------
		if ($form{prefix} eq "") {
			$form_message = "Please select prefix with length from 1 to 100<br><br>";
		} elsif ($form{title} eq "") {
			$form_message = "Please select title with length from 1 to 255<br><br>";
		} elsif ( ($form{value}<0) || ($form{value}>1000) ) {
			$form_message = "Please select value from 0 to 1000<br><br>";
		} else {
			# 
			#----------------------------
			# we have all ok to save
			#----------------------------
			#
			# garbage colector (clean in case we change age table)
			#$allow_age_id = join(",",(keys %age_list));
			#$sql = "delete FROM service_commission_type_age_discount where service_age_id not in ($allow_age_id)";
			#&database_do($sql);
			#
			# change value
			$sql = &database_scape_sql("
				update service_commission_type_by_call_number  set 
					prefix='%s',
					title='%s',
					value='%s' 
				where id='%d' ",
				$form{prefix},$form{title},$form{value},$number_id);
			&database_do($sql);
			#
			# log
			#&action_history("noc:config:commage:edit");
			#
			# reload page
			%t = ();
		    $t{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		    &template_print("template.modal.html",%t);
			exit;
		} 
	} else { 
		#
		#----------------------------
		# first time in form, lets populate form
		#----------------------------
		$form{title}	= $number_title;
		$form{prefix}	= $number_prefix;
		$form{value}	= $number_value;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $t{my_url}	= $my_url;
    $t{content}	= qq[
	<h1>Commission value by phone number</h1><hr>
	Default value for commission '$commission_engine_title' is '$commission_value $commission_value_type_string', 
	but if phone number match this prefix, this new value wins. <br>
	Remember all numbers in system are E164 format. We match the start of number. Example: Enter 5521 to mach country 55, areacode 21. Enter 1212 to match usa 212. Do not enter 1, because will match all country thar start with 1 (not only usa)<br>
	<br>
	<form action=$my_url>
		<table>
		<tr><td>Number prefix:	</td><td><input name="prefix" value="$form{prefix}" /></td></tr>
		<tr><td>Prefix title:	</td><td><input name="title" value="$form{title}" /></td></tr>
		<tr><td>New value:		</td><td><input name="value" value="$form{value}" style="width:75px" /> $commission_value_type_string</td></tr>
		</table>
		<br>
		<font color=red><b>$form_message</b></font>
		<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
		<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
		<input type=hidden name=save value=1>
		<input type=hidden name=number_id value=$number_id>
		<input type=hidden name=action value=commission_type_by_call_number_edit>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_commission_type_by_call_number_add(){
	#
	#-------------------------------------------
    # get commission data
	#-------------------------------------------
    $commission_id = clean_int(substr($form{type_id},0,100)); 
    %hash = database_select_as_hash("select 1,1,engine,title,value_type,value from service_commission_type where id='$commission_id' ","flag,engine,title,value_type,value");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.html",%t);
		exit;
	}
	$commission_engine 				= $hash{1}{engine} ;
	$commission_title 				= $hash{1}{title};
	$commission_is_phone_enabled 	= ( index("|REFERRAL_FIRST_CALL|REFERRAL_DIALOUT_DST|REFERRAL_DIALOUT_DID|SERVICE_FIRST_CALL|SERVICE_DIALOUT_DST|SERVICE_DIALOUT_DID|SERVICE_RADIO_DID|","|$commission_engine|") eq -1 ) ? 0 : 1;
	%commission_engines 			= database_select_as_hash("SELECT id,ui_order,title FROM service_commission_type_engine","ui_order,title");
	$commission_engine_title		= $commission_engines{$commission_engine}{title};
	$commission_value_type			= $hash{1}{value_type};
	$commission_value_type_string	= "by $commission_value_type";
	$commission_value_type_string	= ($commission_value_type eq "VALUE"			) ? "fixed value" 		: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "PERCENTAGE"		) ? "percent of value"	: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "BY_CALL_MINUTES"	) ? "per call minutes"	: $commission_value_type_string	;
	$commission_value				= $hash{1}{value};
	$commission_value++;
	$commission_value--;
	#
	#-------------------------------------------
	# form action
	#-------------------------------------------
	$form_message = "";
	$form{prefix}	= &clean_int(substr($form{prefix},0,255));
	$form{title}	= &trim(substr($form{title},0,255));
	$form{value}	= &clean_float(substr($form{value},0,30));
	$form{value}++;
	$form{value}--;
	if ($form{save} eq 1) {
		#
		#----------------------------
		# second time in form, lets try to save
		#----------------------------
		%active_prefixes = database_select_as_hash("SELECT prefix,1 FROM service_commission_type_by_call_number where service_commission_type_id='$commission_id' ");
		if ($form{prefix} eq "") {
			$form_message = "Please select prefix with length from 1 to 100<br><br>";
		} elsif (exists($active_prefixes{$form{prefix}})) {
			$form_message = "This prefix alread exist<br><br>";
		} elsif ($form{title} eq "") {
			$form_message = "Please select title with length from 1 to 255<br><br>";
		} elsif ( ($form{value}<0) || ($form{value}>1000) ) {
			$form_message = "Please select value from 0 to 1000<br><br>";
		} else {
			# 
			#----------------------------
			# we have all ok to save
			#----------------------------
			#
			# garbage colector (clean in case we change age table)
			#$allow_age_id = join(",",(keys %age_list));
			#$sql = "delete FROM service_commission_type_age_discount where service_age_id not in ($allow_age_id)";
			#&database_do($sql);
			#
			# change value
			$sql = &database_scape_sql("
				insert into service_commission_type_by_call_number 
				(service_commission_type_id, prefix, title, value) values 
				('%d',                       '%s',   '%s',  '%s' ) 
				",
				$commission_id,$form{prefix},$form{title},$form{value});
			&database_do($sql);
			#
			# log
			#&action_history("noc:config:commage:edit");
			#
			# reload page
			%t = ();
		    $t{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		    &template_print("template.modal.html",%t);
			exit;
		} 
	} else { 
		#
		#----------------------------
		# first time in form, lets populate form
		#----------------------------
		$form{title}	= "";
		$form{prefix}	= "";
		$form{value}	= "0";
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $t{my_url}	= $my_url;
    $t{content}	= qq[
	<h1>Commission value by phone number</h1><hr>
	Default value for commission '$commission_engine_title' is '$commission_value $commission_value_type_string', 
	but if phone number match this prefix, this new value wins. <br>
	Remember all numbers in system are E164 format. We match the start of number. Example: Enter 5521 to mach country 55, areacode 21. Enter 1212 to match usa 212. Do not enter 1, because will match all country thar start with 1 (not only usa)<br>
	<br>
	<form action=$my_url>
		<table>
		<tr><td>Number prefix:	</td><td><input name="prefix" value="$form{prefix}" /></td></tr>
		<tr><td>Prefix title:	</td><td><input name="title" value="$form{title}" /></td></tr>
		<tr><td>New value:		</td><td><input name="value" value="$form{value}" style="width:75px" /> $commission_value_type_string</td></tr>
		</table>
		<br>
		<font color=red><b>$form_message</b></font>
		<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
		<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
		<input type=hidden name=save value=1>
		<input type=hidden name=type_id value=$commission_id>
		<input type=hidden name=action value=commission_type_by_call_number_add>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_commission_type_by_call_number_del(){
	#
	#-------------------------------------------
    # get number_id
	#-------------------------------------------
    $number_id	= clean_int(substr($form{number_id},0,100)); 
  	%hash 	= database_select_as_hash("select 1,1,prefix,title,value,service_commission_type_id from service_commission_type_by_call_number where  id='$number_id' ","flag,prefix,title,value,service_commission_type_id");
	if ($hash{1}{flag} ne 1){
		%t = ();
		$t{content} = "Invalid number_id parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
    $number_prefix	= $hash{1}{prefix}; 
	$number_title	= $hash{1}{title};
	$number_value	= $hash{1}{value};
	$commission_id	= $hash{1}{service_commission_type_id};
	$number_value++;
	$number_value--;
	#
	#-------------------------------------------
    # get commission by id
	#-------------------------------------------
    $commission_id = clean_int($commission_id); 
    %hash = database_select_as_hash("select 1,1,engine,title,value_type,value from service_commission_type where id='$commission_id' ","flag,engine,title,value_type,value");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{content} = "Invalid parameter";
		&template_print("template.html",%t);
		exit;
	}
	$commission_engine 				= $hash{1}{engine} ;
	$commission_title 				= $hash{1}{title};
	$commission_is_phone_enabled 	= ( index("|REFERRAL_FIRST_CALL|REFERRAL_DIALOUT_DST|REFERRAL_DIALOUT_DID|SERVICE_FIRST_CALL|SERVICE_DIALOUT_DST|SERVICE_DIALOUT_DID|SERVICE_RADIO_DID|","|$commission_engine|") eq -1 ) ? 0 : 1;
	%commission_engines 			= database_select_as_hash("SELECT id,ui_order,title FROM service_commission_type_engine","ui_order,title");
	$commission_engine_title		= $commission_engines{$commission_engine}{title};
	$commission_value_type			= $hash{1}{value_type};
	$commission_value_type_string	= "by $commission_value_type";
	$commission_value_type_string	= ($commission_value_type eq "VALUE"			) ? "fixed value" 		: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "PERCENTAGE"		) ? "percent of value"	: $commission_value_type_string	;
	$commission_value_type_string	= ($commission_value_type eq "BY_CALL_MINUTES"	) ? "per call minutes"	: $commission_value_type_string	;
	$commission_value				= $hash{1}{value};
	$commission_value++;
	$commission_value--;
	#
	#-------------------------------------------
	# form action
	#-------------------------------------------
	$form_message = "";
	if ($form{save} eq 1) {
			# 
			#----------------------------
			# we have all ok to save
			#----------------------------
			#
			# garbage colector (clean in case we change age table)
			#$allow_age_id = join(",",(keys %age_list));
			#$sql = "delete FROM service_commission_type_age_discount where service_age_id not in ($allow_age_id)";
			#&database_do($sql);
			#
			# change value
			$sql = &database_scape_sql("delete from service_commission_type_by_call_number where id='%d' ",$number_id);
			&database_do($sql);
			#
			# log
			#&action_history("noc:config:commage:edit");
			#
			# reload page
			%t = ();
		    $t{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		    &template_print("template.modal.html",%t);
			exit;
	} else { 
		#
		#----------------------------
		# first time in form, lets populate form
		#----------------------------
		$form{title}	= $number_title;
		$form{prefix}	= $number_prefix;
		$form{value}	= $number_value;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
  
    $t{my_url}	= $my_url;
    $t{content}	= qq[
    Are you sure to delete prefix '$number_prefix'?
	<br>
	<br>
	<form action=$my_url>
		<font color=red><b>$form_message</b></font>
		<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
		<button type=submit><img src=/design/icons/tick.png align=left>Delete</button>
		<input type=hidden name=save value=1>
		<input type=hidden name=number_id value=$number_id>
		<input type=hidden name=action value=commission_type_by_call_number_del>
	</form>
    ];
    &template_print("template.modal.html",%t);
}
#========================================================================


