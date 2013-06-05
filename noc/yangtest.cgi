#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
#if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
#if (&active_user_permission_check("noc:can_manage_services") ne 1) {adm_error("no permission"); exit;}
#=======================================================



#=======================================================
# main loop
#=======================================================
$my_url = "yangtest.cgi";

$action = $form{action};
$action ="view_referral";
if 		($action eq "view")					{ &do_view_overview();			} 
elsif 	($action eq "view_overview")		{ &do_view_overview();			}
elsif 	($action eq "view_history")			{ &do_view_history();			}
elsif 	($action eq "view_calls")			{ &do_view_calls();				}
elsif 	($action eq "view_referral")		{ &do_view_referral();			}
elsif 	($action eq "view_commissions")		{ &do_view_commissions();		}
elsif 	($action eq "view_credits")			{ &do_view_credits();			}
elsif 	($action eq "view_coupons")			{ &do_view_coupons();			}
elsif 	($action eq "view_ccprofile")		{ &do_view_ccprofile();			}
elsif 	($action eq "view_login")			{ &do_view_login();				}
elsif 	($action eq "view_tree_js")			{ &do_view_tree_js();			}
elsif 	($action eq "detail_call")			{ &do_detail_call();			}
elsif 	($action eq "detail_ccprofile")		{ &do_detail_ccprofile();		}
elsif 	($action eq "detail_commission")	{ &do_detail_commission();		}
elsif 	($action eq "detail_coupon")		{ &do_detail_coupon();			}
elsif 	($action eq "detail_coupon_stop")	{ &do_detail_coupon_stop();		}
elsif 	($action eq "detail_coupon_unstop")	{ &do_detail_coupon_unstop();	}
elsif 	($action eq "email_edit")			{ &do_email_edit();				}
elsif 	($action eq "name_edit")			{ &do_name_edit();				}
elsif 	($action eq "invite_edit")			{ &do_invite_edit();			}
elsif 	($action eq "credit_add")			{ &do_credit_add();				}
elsif 	($action eq "credit_view")			{ &do_credit_view();			}
elsif 	($action eq "credit_del")			{ &do_credit_del();				}
elsif 	($action eq "credit_undel")			{ &do_credit_undel();			}
elsif 	($action eq "commission_add")		{ &do_commission_add();			}
elsif 	($action eq "status_edit")			{ &do_status_edit();			}
elsif 	($action eq "status_edit_multiple")	{ &do_status_edit_multiple();	}
elsif 	($action eq "profile_affiliate")	{ &do_profile_affiliate();		}
elsif 	($action eq "service_agestatus")	{ &do_service_agestatus();		}
elsif 	($action eq "note_edit")			{ &do_note_edit();				}
elsif 	($action eq "tags_select")			{ &do_tags_select();			}
elsif 	($action eq "tags_select_multiple")	{ &do_tags_select_multiple();	}
elsif 	($action eq "tag_edit")				{ &do_tag_edit();				}
elsif 	($action eq "tag_add")				{ &do_tag_add();				}
elsif 	($action eq "tag_del")				{ &do_tag_del();				}
elsif 	($action eq "clients_export")		{ &do_clients_export();			}
else										{ &do_search(); 				}
exit;
#=======================================================


#========================================================================
# actions
#========================================================================
sub do_invite_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,name from service where service.id='$service_id' ","flag,name");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
    %hash = database_select_as_hash("select 1,1,id from service_invite where service_id='$service_id' ","flag,name");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Unknown invite"; &template_print("template.modal.html",%t);exit; }
	$invite = $hash{1}{name};
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$save_id = &active_session_get("save_id_inv");
	$form_message = "";
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		$value = trim(clean_str(substr($form{invite},0,100),"-_"));
	    %hash = database_select_as_hash("select 1,1 from service_invite where and id='$value' ","flag");
		if ( ($value ne $form{invite}) ) {
			$form_message = "Bad format<br><br>";
		} elsif ( (length($value)<3) || (length($value)>20) ) {
			$form_message = "Invalid length<br><br>";
		} elsif ($value eq $invite) {
			$form_message = "No change need<br><br>";
		} elsif ( $hash{1}{flag} eq 1 ) {
			$form_message = "Already in use<br><br>";
		} elsif (-e "/usr/local/multilevel/www/$value") {
			$form_message = "Private word<br><br>";
		} else {
			%hash2 = database_select_as_hash("SELECT 1,1,id FROM service_invite where service_id='$service_id' ","flag,value");
			$value_old = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : "Unknown";
			&database_do("update service_invite set id='$value' where service_id='$service_id' ");
			%hash2 = database_select_as_hash("SELECT 1,1,id FROM service_invite where service_id='$service_id' ","flag,value");
			$value_new = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : "Unknown";
			&action_history("noc:service:invite:change",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>$value_old, 'value_new'=>$value_new ));
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
			&active_session_delete("save_id_nee");
			exit;
		}
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} eq "") {
		$form{invite} = $invite;
	}
    #
	#-------------------------------------------
    # Get last 3 changes
	#-------------------------------------------
    %history = database_select_as_hash("select id,1 from action_log where type='noc:service:invite:change' and service_id='$service_id' order by date desc limit 0,3","flag");
	$last_3_changes = "";
	foreach $his_id (sort{$b <=> $a} keys %history){
		%hash = action_history_get_info($his_id);
		$last_3_changes .= "<li>$hash{$his_id}{text_simple}$hash{$his_id}{text_extra}</li>";
	}
	$last_3_changes = ($last_3_changes ne "") ? "<div class=last_changes><h1>Last changes</h1><ul>$last_3_changes</ul></div>" : "";
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $save_id = time;
	&active_session_set("save_id_inv",$save_id);
	%t = ();
    $t{dic}{content}	= qq[
		<form action=$my_url>
		Invite:<br><input type=text name=invite value='$form{invite}'><br>	
		<br>
		<font color=red><b>$form_message</b></font>
		<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
		<button type=submit class="button button_positive button_save"  >Save</button>
		<input type=hidden name=save value=$save_id>
		<input type=hidden name=service_id value=$service_id>
		<input type=hidden name=action value=invite_edit>
		</form>
		<br>
		$last_3_changes 
    ];
    &template_print("template.modal.html",%t);
}
sub do_tag_add(){
    $service_id = clean_int(substr($form{service_id},0,100));
	$save_id = &active_session_get("save_id_ts");
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		$value = trim(clean_str(substr($form{tag_name},0,100),"\@. ()-_[]:"));
		&database_do("insert service_tag_string (tag) values ('$value') ");
		&action_history("noc:tag:edit",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>"add", 'value_new'=>$value ));
	}
	if ($service_id ne "") {
		cgi_redirect("$my_url?action=tags_select&service_id=$service_id");
	} else {
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
	}
	&active_session_delete("save_id_ts");
	exit;
}
sub do_tag_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    $tag_id = clean_int(substr($form{tag_id},0,100));
    %hash = database_select_as_hash("select 1,1,tag from service_tag_string where id='$tag_id' ","flag,name");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid tag_id"; &template_print("template.modal.html",%t);exit; }
	$tag_string = $hash{1}{name};
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$save_id = &active_session_get("save_id_te");
	$form_message = "";
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		$value = trim(clean_str(substr($form{value},0,100),"\@. ()-_[]:"));
		&database_do("update service_tag_string set tag='$value' where id='$tag_id' ");
		&action_history("noc:tag:edit",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>"edit", 'value_new'=>$value ));
		if ($service_id ne "") {
			cgi_redirect("$my_url?action=tags_select&service_id=$service_id");
		} else {
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
		}
		&active_session_delete("save_id_te");
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} eq "") {
		$form{value} = $tag_string;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $save_id = time;
	&active_session_set("save_id_te",$save_id);
	$cancel_action = ($service_id ne "") ? "window.location='$my_url?action=tags_select&service_id=$service_id'" : "parent.modal_close()";
	%t = ();
    $t{dic}{content}	= qq[
		<form action=$my_url>
		New Tag Name:<br><input type=text name=value value='$form{value}'><br>	
		<br>
		<button type=button class="button button_negative button_cancel" onclick="$cancel_action">Cancel</button>
		<button type=submit class="button button_positive button_save"  >Save</button>
		<input type=hidden name=save value=$save_id>
		<input type=hidden name=tag_id value=$tag_id>
		<input type=hidden name=service_id value=$service_id>
		<input type=hidden name=action value=tag_edit>
		</form>
		<br>
		<form action=$my_url>
		<button type=submit onclick="return confirm('Can i delete this tag?');" class="button button_negative button_delete"  >Delete</button>
		<input type=hidden name=save value=$save_id>
		<input type=hidden name=tag_id value=$tag_id>
		<input type=hidden name=service_id value=$service_id>
		<input type=hidden name=action value=tag_del>
		</form>
		$last_3_changes 
    ];
    &template_print("template.modal.html",%t);
}
sub do_tag_del(){
    $service_id = clean_int(substr($form{service_id},0,100));
    $tag_id = clean_int(substr($form{tag_id},0,100));
    %hash = database_select_as_hash("select 1,1,tag from service_tag_string where id='$tag_id' ","flag,name");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid tag_id"; &template_print("template.modal.html",%t);exit; }
	$tag_name = $hash{1}{name};
	$save_id = &active_session_get("save_id_te");
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		database_do ("delete from service_tag where tag_string_id='$tag_id' ");
		&database_do("delete from service_tag_string where id='$tag_id' ");
		&action_history("noc:tag:edit",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>"del", 'value_new'=>$tag_name ));
	}
	if ($service_id ne "") {
		cgi_redirect("$my_url?action=tags_select&service_id=$service_id");
	} else {
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
	}
	&active_session_delete("save_id_te");
	exit;
}
sub do_tags_select(){
    #
	#-------------------------------------------
    # confere service_id 
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,name from service where service.id='$service_id' ","flag,name");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
	#
	#-------------------------------------------
	# get data
	#-------------------------------------------
    %tags_list = database_select_as_hash("SELECT id,tag FROM service_tag_string");
    %tags_selected = database_select_as_hash("SELECT tag_string_id FROM service_tag WHERE service_id='$service_id' ");
    %tags_count = database_select_as_hash("SELECT tag_string_id,count(*) FROM service_tag group by tag_string_id");
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	$save_id = &active_session_get("save_id_ts");
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		database_do ("delete from service_tag where service_id='$service_id' ");
		foreach $name (keys %form) {
			if (index($name,"tag_id_") ne 0) {next}
			$value = &clean_int(substr($name,7,100));
			unless (exists($tags_list{$value})) {next}
			if ($form{$name} eq 1) {
				database_do ("insert into service_tag (service_id,tag_string_id) values ('$service_id','$value') ");
			}
		}
		&action_history("noc:service:tag:select",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u} ));
		#
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
		&active_session_delete("save_id_ts");
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} eq "") {
		foreach (keys %tags_selected) {
			$form{"tag_id_".$_} = 1;
		}
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$html_tags_list = "";
	foreach $tag_id (sort{$tags_list{$a} cmp $tags_list{$b}} keys %tags_list) {
		$tag_count = &format_number($tags_count{$tag_id},0);
		$tmp = ($form{"tag_id_".$tag_id} eq 1) ? "checked" : "";
		$html_tags_list .= qq[
			<tr>
			<td valign=top width=20><input type=checkbox $tmp name=tag_id_$tag_id value=1 style="margin-top:3px;margin-bottom:6px;"></td>
			<td valign=top >$tags_list{$tag_id}</td>
			<td valign=top >$tag_count</td>
			<td valign=top width=50 style=padding-top:3px; ><a class="buttonlink button_mini_edit" href=$my_url?action=tag_edit&service_id=$service_id&tag_id=$tag_id >edit</a></td>
			</tr>
		];
	}
    $save_id = time;
	&active_session_set("save_id_ts",$save_id);
	%t = ();
    $t{dic}{content}	= qq[

		<script>
		function new_tag(){
			value = prompt("Enter new tag name","");
			if (!value) {return}
			window.location="$my_url?action=tag_add&service_id=$service_id&save=$save_id&tag_name="+escape(value)
		}
		</script>
		<style>
		.local_service_data tbody tr { xxbackground-color:#ffffff; }
		.local_service_data tbody tr:hover { background-color:#f0f0ff; }
		.local_service_data tfoot tr { xxbackground-color:#ffffff; }
		.local_service_data tfoot tr:hover { background-color:#f0f0ff; }
		.local_service_data tbody tr td .buttonlink {display:none; }
		.local_service_data tbody tr:hover td .buttonlink {display:inline; }
		</style>
	
		<form action=$my_url>
		<table class=local_service_data border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear width=100% >
			<tbody>
			$html_tags_list
			</tbody>
			<tfoot >
			<tr ><td></td><td></td><td></td><td style=padding-top:3px;padding-bottom:2px;><a class="buttonlink button_mini_add" onclick="new_tag();">New</a><td></tr>
			<tfoot>
		</table>
		<br>
		<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
		<button type=submit class="button button_positive button_save"  >Save</button>
		<input type=hidden name=save value=$save_id>
		<input type=hidden name=service_id value=$service_id>
		<input type=hidden name=action value=tags_select>
		</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_tags_select_multiple(){
    #
	#-------------------------------------------
    # confere service_id 
	#-------------------------------------------
	%selected_ids = ();
	$selected_ids_qtd = 0;
    foreach $id (split(/\,/,$form{service_ids})) {
		%hash = database_select_as_hash("select 1,1 from service where service.id='$id' ","flag");
		if ($hash{1}{flag} eq 1) { $selected_ids{$id}++; $selected_ids_qtd++}
	}
	$selected_ids_sql = join(",",(keys %selected_ids));
    if ($selected_ids_sql eq "") { %t=(); $t{dic}{content}="Invalid service_ids"; &template_print("template.modal.html",%t);exit; }
	#
	#-------------------------------------------
	# get data
	#-------------------------------------------
    %tags_list	= database_select_as_hash("SELECT id,tag FROM service_tag_string");
    %tags_count	= database_select_as_hash("SELECT tag_string_id,count(*) FROM service_tag WHERE service_id in ($selected_ids_sql) group by tag_string_id ");
	#
	#-------------------------------------------
	# try to save
	#-------------------------------------------
	$form_message = "";
	if ( &multilevel_clickchain_check("tm",$form{save}) eq 1 ) {
		foreach $id (keys %form) {
			$tag_id = substr($id,7,100);
			if ($form{$id} eq 1) {
				&database_do ("delete from service_tag where tag_string_id='$tag_id' and service_id in ($selected_ids_sql) ");
				foreach $local_service_id (keys %selected_ids) {
					&database_do ("insert into service_tag (service_id,tag_string_id) values ('$local_service_id','$tag_id') ");
				}
			} elsif ($form{$id} eq -1) {
				&database_do ("delete from service_tag where tag_string_id='$tag_id' and service_id in ($selected_ids_sql) ");
			}
		}
		foreach $local_service_id (keys %selected_ids) {
			&action_history("noc:service:tag:select",('service_id'=>$local_service_id, 'adm_user_id'=>$app{session_cookie_u} ));
		}
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# load form
	#-------------------------------------------
	$html_tags_list = "";
	foreach $tag_id (sort{$tags_list{$a} cmp $tags_list{$b}} keys %tags_list) {
		$tag_count = ($tags_count{$tag_id} > 0) ? "(".&format_number($tags_count{$tag_id},0).")" : "";
		$tmp1 = ($form{"tag_id_".$tag_id} eq 1) ? "selected" : "";
		$tmp2 = ($form{"tag_id_".$tag_id} eq -1) ? "selected" : "";
		$html_tags_list .= qq[
			<tr style="padding-top:10px;">
			<td valign=top >$tags_list{$tag_id} $tag_count</td>
			<td valign=top >
				<select name=tag_id_$tag_id style="width:60px;">
				<option value=""></option>
				<option $tmp1 value="1">Add</option>
				<option $tmp2 value="-1">Delete</option>
				</select>
				</td>
			</tr>
		];
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$clickchain_id = &multilevel_clickchain_set("tm");
	%t = ();
    $t{dic}{content}	= qq[
		<form action=$my_url>

			<style>
			.local_service_data tbody tr { xxbackground-color:#ffffff; }
			.local_service_data tbody tr:hover { background-color:#f0f0ff; }
			.local_service_data tfoot tr { xxbackground-color:#ffffff; }
			.local_service_data tfoot tr:hover { background-color:#f0f0ff; }
			.local_service_data tbody tr td .buttonlink {display:none; }
			.local_service_data tbody tr:hover td .buttonlink {display:inline; }
			</style>
		
			<table class=local_service_data border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear width=100% >
				<tbody>
				$html_tags_list
				</tbody>
			</table>


			<br>
			<font color=red><b>$form_message</b></font>
			<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
			<button type=submit class="button button_positive button_save"  >Save Tags for this $selected_ids_qtd services</button>
			<input type=hidden name=save value=$clickchain_id>
			<input type=hidden name=action value=tags_select_multiple>
			<input type=hidden name=service_ids value="$form{service_ids}"><br>
		</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_note_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,name from service where service.id='$service_id' ","flag,name");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
    %hash = database_select_as_hash("select 1,1,text from service_note where service_id='$service_id' ","flag,text");
    $service_note = ($hash{1}{flag} eq 1) ? $hash{1}{text} : "";
	$tmp1="<br>"; $tmp2="\n"; $service_note =~ s/$tmp1/$tmp2/eg; 
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$save_id = &active_session_get("save_id");
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		$text = trim(clean_str(substr($form{text},0,65536),"\@. []()=_-:\n"));
		$tmp1="\r"; $tmp2="\n"; $text =~ s/$tmp1/$tmp2/eg; 
		$tmp1="\n"; $tmp2="<br>"; $text =~ s/$tmp1/$tmp2/eg;
		#
		%hash = database_select_as_hash("select 1,1 from service_note where service_id='$service_id' ","flag");
		if ($hash{1}{flag} eq 1) {
			database_do("update service_note set text='$text' where service_id='$service_id' ");
		} else {
			database_do("insert into service_note (service_id,text) values ('$service_id','$text')  ");
		}
		#
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
		&active_session_delete("save_id_nee");
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} eq "") {
		$form{text} = $service_note;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $save_id = time;
	&active_session_set("save_id",$save_id);
	%t = ();
    $t{dic}{content}	= qq[
		<form action=$my_url>
		<textarea name=text class=clear style="font-face:verdana,arial; font-size:10px; line-height:110%;  border:1px solid #c0c0c0; background-color:#f0f0f0;margin-top:6px;margin-bottom:5px; overflow-x:hidden;overflow-y:scroll; width:100%; height:200px; padding:3px;">$form{text}</textarea>
		<br>
		<br>
		<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
		<button type=submit class="button button_positive button_save"  >Save</button>
		<input type=hidden name=save value=$save_id>
		<input type=hidden name=service_id value=$service_id>
		<input type=hidden name=action value=note_edit>
		</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_name_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,name from service where service.id='$service_id' ","flag,name");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
	$name = $hash{1}{name};
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_message = "";
	if ( &multilevel_clickchain_check("nm",$form{save}) eq 1 ) {
		$value = trim(clean_str(substr($form{name},0,100),"\@."));
		if ( ($value ne $form{name}) ) {
			$form_message = "Unknown value<br><br>";
		} else {
			if ($value eq $name) {
				$form_message = "No change need<br><br>";
			} else {
				%hash2 = database_select_as_hash("SELECT 1,1,name FROM service where id='$service_id' ","flag,value");
				$value_old = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : "Unknown";
				&database_do("update service set service.name='$value' where service.id='$service_id' ");
				%hash2 = database_select_as_hash("SELECT 1,1,name FROM service where id='$service_id' ","flag,value");
				$value_new = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : "Unknown";
				&action_history("noc:service:name:change",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>$value_old, 'value_new'=>$value_new ));
				%t = ();
				$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
				&template_print("template.modal.html",%t);
				&active_session_delete("save_id_nee");
				exit;
			}
		}
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} eq "") {
		$form{name} = $name;
	}
    #
	#-------------------------------------------
    # Get last 3 changes
	#-------------------------------------------
    %adm_users = database_select_as_hash("select id,web_user,name from adm_users","web_user,name");
    %history = database_select_as_hash("select id,1 from action_log where type='noc:service:name:change' and service_id='$service_id' order by date desc limit 0,3","flag");
	$last_3_changes = "";
	foreach $his_id (sort{$b <=> $a} keys %history){
		%hash = action_history_get_info($his_id);
		$last_3_changes .= "<li>$hash{$his_id}{text_simple}$hash{$his_id}{text_extra}</li>";
	}
	$last_3_changes = ($last_3_changes ne "") ? "<div class=last_changes><h1>Last changes</h1><ul>$last_3_changes</ul></div>" : "";
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$save_id = &multilevel_clickchain_set("nm");
	%t = ();
    $t{dic}{content}	= qq[
		<form action=$my_url>
		New Name:<br><input type=text name=name value='$form{name}'><br>	
		<br>
		<font color=red><b>$form_message</b></font>
		<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
		<button type=submit class="button button_positive button_save"  >Save</button>
		<input type=hidden name=save value=$save_id>
		<input type=hidden name=service_id value=$service_id>
		<input type=hidden name=action value=name_edit>
		</form>
		<br>
		$last_3_changes 
    ];
    &template_print("template.modal.html",%t);
}
sub do_email_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,email from service where service.id='$service_id' ","flag,email");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
	$email = $hash{1}{email};
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$save_id = &active_session_get("save_id_nee");
	$form_message = "";
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		$value = trim(clean_str(substr($form{email},0,100),"\@."));
		if ( ($value ne $form{email}) ) {
			$form_message = "Unknown value<br><br>";
		} else {
			if ($value eq $email) {
				$form_message = "No change need<br><br>";
			} else {
				%hash2 = database_select_as_hash("SELECT 1,1,email FROM service where id='$service_id' ","flag,value");
				$value_old = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : "Unknown";
				&database_do("update service set service.email='$value' where service.id='$service_id' ");
				%hash2 = database_select_as_hash("SELECT 1,1,email FROM service where id='$service_id' ","flag,value");
				$value_new = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : "Unknown";
				&action_history("noc:service:email:change",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>$value_old, 'value_new'=>$value_new ));
				%t = ();
				$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
				&template_print("template.modal.html",%t);
				&active_session_delete("save_id_nee");
				exit;
			}
		}
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} eq "") {
		$form{email} = $email;
	}
    #
	#-------------------------------------------
    # Get last 3 changes
	#-------------------------------------------
    %adm_users = database_select_as_hash("select id,web_user,name from adm_users","web_user,name");
    %history = database_select_as_hash("select id,1 from action_log where type='noc:service:email:change' and service_id='$service_id' order by date desc limit 0,3","flag");
	$last_3_changes = "";
	foreach $his_id (sort{$b <=> $a} keys %history){
		%hash = action_history_get_info($his_id);
		$last_3_changes .= "<li>$hash{$his_id}{text_simple}$hash{$his_id}{text_extra}</li>";
	}
	$last_3_changes = ($last_3_changes ne "") ? "<div class=last_changes><h1>Last changes</h1><ul>$last_3_changes</ul></div>" : "";
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $save_id = time;
	&active_session_set("save_id_nee",$save_id);
	%t = ();
    $t{dic}{content}	= qq[
		<form action=$my_url>
		New email:<br><input type=text name=email value='$form{email}'><br>	
		<br>
		<font color=red><b>$form_message</b></font>
		<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
		<button type=submit class="button button_positive button_save"  >Save</button>
		<input type=hidden name=save value=$save_id>
		<input type=hidden name=service_id value=$service_id>
		<input type=hidden name=action value=email_edit>
		</form>
		<br>
		$last_3_changes 
    ];
    &template_print("template.modal.html",%t);
}
sub do_credit_undel(){
	%t = ();
	$error_message = "";
    #
	#-------------------------------------------
    # confere service_id 
	#-------------------------------------------
	if ($error_message eq "") {
		$service_id = clean_int(substr($form{service_id},0,100));
		%hash = database_select_as_hash("select 1,1,email from service where service.id='$service_id' ","flag,email");
		unless ($hash{1}{flag} eq 1) { $error_message = "Invalid service_id"; }
	}
    #
	#-------------------------------------------
    # confere credit_id
	#-------------------------------------------
	if ($error_message eq "") {
		$credit_id = clean_int(substr($form{credit_id},0,100));
		%hash = database_select_as_hash("select 1,1,status,service_id from credit where service_id='$service_id' and id='$credit_id' ","flag,status,service_id");
		unless ($hash{1}{flag} eq 1) { $error_message = "Invalid service_id"; }
		$service_id_from_cedit = $hash{1}{service_id};
		$credit_status = $hash{1}{status};
	}
    #
	#-------------------------------------------
    # check click id
	#-------------------------------------------
	if ($error_message eq "") {
		if ($form{save} ne &active_session_get("save_id_cd")) {
			$error_message = "System error. Try again";
		}
	}
    #
	#-------------------------------------------
    # service credit link
	#-------------------------------------------
	if ($error_message eq "") {
		if ($service_id_from_cedit ne $service_id) {
			$error_message = "Incorrect credit service";
		}
	}
    #
	#-------------------------------------------
    # check status
	#-------------------------------------------
	if ($error_message eq "") {
		if ($credit_status ne -1) {
			$error_message = "This is not a deleted credit";
		}
	}
    #
	#-------------------------------------------
    # check text
	#-------------------------------------------
	if ($error_message eq "") {
		$text = trim(clean_str(substr($form{text},0,255)));
		if ( ($text eq "") || ($text ne $form{text}) || (length($text)>200)  ) {
			$error_message = "Incorrect text";
		}
	}
    #
	#-------------------------------------------
    # try save
	#-------------------------------------------
	if ($error_message eq "") {
		%order=();
		$order{credit_id}	= $credit_id;
		$order{text} 		= $text;
		%order = &multilevel_credit_undel(%order);
		if ($order{ok} eq 1) {
			$tmp1 = substr($text,0,100);
			$tmp2 = (length($text)>100) ? substr($text,100,100) : "";
			&action_history("noc:service:credit:undel",('service_id'=>$service_id, 'credit_id'=>$credit_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>$tmp1, 'value_new'=>$tmp2 ));
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
			&active_session_delete("save_id_ca");
			exit;
		} else {
			$error_message = $order{message};
		}
	}
    #
	#-------------------------------------------
    # print page
	#-------------------------------------------
	$error_message = ($error_message eq "") ? "Ok but no action" : $error_message;
    $t{dic}{content}	= qq[
	<script>
	alert("$error_message");
	window.location="$my_url?action=credit_view&service_id=$service_id&credit_id=$credit_id";
	</script>
    ];
    &template_print("template.modal.html",%t);
}
sub do_credit_del(){
	%t = ();
	$error_message = "";
    #
	#-------------------------------------------
    # confere service_id 
	#-------------------------------------------
	if ($error_message eq "") {
		$service_id = clean_int(substr($form{service_id},0,100));
		%hash = database_select_as_hash("select 1,1,email from service where service.id='$service_id' ","flag,email");
		unless ($hash{1}{flag} eq 1) { $error_message = "Invalid service_id"; }
	}
    #
	#-------------------------------------------
    # confere credit_id
	#-------------------------------------------
	if ($error_message eq "") {
		$credit_id = clean_int(substr($form{credit_id},0,100));
		%hash = database_select_as_hash("select 1,1,status,service_id from credit where service_id='$service_id' and id='$credit_id' ","flag,status,service_id");
		unless ($hash{1}{flag} eq 1) { $error_message = "Invalid service_id"; }
		$service_id_from_cedit = $hash{1}{service_id};
		$credit_status = $hash{1}{status};
	}
    #
	#-------------------------------------------
    # check click id
	#-------------------------------------------
	if ($error_message eq "") {
		if ($form{save} ne &active_session_get("save_id_cd")) {
			$error_message = "System error. Try again";
		}
	}
    #
	#-------------------------------------------
    # service credit link
	#-------------------------------------------
	if ($error_message eq "") {
		if ($service_id_from_cedit ne $service_id) {
			$error_message = "Incorrect credit service";
		}
	}
    #
	#-------------------------------------------
    # check status
	#-------------------------------------------
	if ($error_message eq "") {
		if ($credit_status ne 1) {
			$error_message = "This is not a active credit";
		}
	}
    #
	#-------------------------------------------
    # check text
	#-------------------------------------------
	if ($error_message eq "") {
		$text = trim(clean_str(substr($form{text},0,255)));
		if ( ($text eq "") || ($text ne $form{text}) || (length($text)>200)  ) {
			$error_message = "Incorrect text";
		}
	}
    #
	#-------------------------------------------
    # try save
	#-------------------------------------------
	if ($error_message eq "") {
		%order=();
		$order{credit_id}	= $credit_id;
		$order{text} 		= $text;
		%order = &multilevel_credit_del(%order);
		if ($order{ok} eq 1) {
			$tmp1 = substr($text,0,100);
			$tmp2 = (length($text)>100) ? substr($text,100,100) : "";
			&action_history("noc:service:credit:del",('service_id'=>$service_id, 'credit_id'=>$credit_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>$tmp1, 'value_new'=>$tmp2 ));
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
			&active_session_delete("save_id_ca");
			exit;
		} else {
			$error_message = $order{message};
		}
	}
    #
	#-------------------------------------------
    # print page
	#-------------------------------------------
	$error_message = ($error_message eq "") ? "Ok but no action" : $error_message;
    $t{dic}{content}	= qq[
	<script>
	alert("$error_message");
	window.location="$my_url?action=credit_view&service_id=$service_id&credit_id=$credit_id";
	</script>
    ];
    &template_print("template.modal.html",%t);
}
sub do_credit_view(){
    #
	#-------------------------------------------
    # confere service_id 
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,email from service where service.id='$service_id' ","flag,email");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
    #
	#-------------------------------------------
    # confere credit_id
	#-------------------------------------------
    $credit_id = clean_int(substr($form{credit_id},0,100));
    %hash = database_select_as_hash("select 1,1 from credit where service_id='$service_id' and id='$credit_id' ","flag");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
    #
	#-------------------------------------------
    # pega dados
	#-------------------------------------------
	%hash = &database_select_as_hash("
		SELECT 1,1,unix_timestamp(date),status,credit_type,credit,value,text 
		FROM credit
		where id='$credit_id'
		","flag,date_timestamp,status,credit_type,credit,value,text"
		);
	%data = %{$hash{1}};
	$data{date} = &format_time_gap($data{date_timestamp});
	$data{credit_string} = &format_number($data{credit},2);
	$data{value_string} = &format_number($data{value},2);
	$data{type} =  $data{credit_type};
	$data{type} = ($data{credit_type} eq "FREE") 			? "Free recharge"	: $data{type};
	$data{type} = ($data{credit_type} eq "AUTHORIZE_CC")	? "Credit card" 	: $data{type};
	$data{type} = ($data{credit_type} eq "AUTHORIZE_CIM")	? "Pay as you go"	: $data{type};
	$data{type} = ($data{credit_type} eq "AUTHORIZE_ACIM")	? "Auto recharge" 	: $data{type};
	$data{type} = ($data{credit_type} eq "CASH") 			? "Cash recharge" 	: $data{type};
	$data{type} = ($data{credit_type} eq "COMMISSION_CRED")	? "by commissions"	: $data{type};
	$data{type} = ($data{status} eq 1) 						? "$data{type}" 			: "$data{type} <font color=red>ERROR</font>";
	%hash = &database_select_as_hash("select 1,1,adm_user_id from action_log where credit_id='$credit_id' ","flag,value");
	$data{adm_user_id} = "";
	$data{adm_user_name} = "<font color=#c0c0c0>(none)</font>";
	if ( ($hash{1}{flag} eq 1) && ($hash{1}{value} ne "") ) {
		$data{adm_user_id} = $hash{1}{value};
		%hash = database_select_as_hash("select 1,1,concat(name,' (',web_user,')') from adm_users where id='$data{adm_user_id}' ","flag,value");
		$data{adm_user_name} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} ne "") ) ? $hash{1}{value} : $data{adm_user_name};
	}
	$data{status_string} = "OK"; 
	$data{status_string} = ($data{status} eq 0) ? "Not ready" : $data{status_string}; 
	$data{status_string} = ($data{status} eq -1) ? "Deleted" : $data{status_string}; 
	#
	#-------------------------------------------
	# commissions
	#-------------------------------------------
	$data{commissions_all_not_invoiced} = 1;
	%hash = &database_select_as_hash("
		SELECT service_commission.id,service_commission.deep, service_commission.status, service_commission.invoice_id,service_commission.value, service.id,service.name
		FROM service_commission,service
		where service_commission.service_id=service.id and  service_commission.credit_id = '$credit_id'
		order by service_commission.deep 
		","deep,status,invoice_id,value,id,name,email"
		);
	foreach (sort{$hash{$a}{deep} <=> $hash{$b}{deep}} keys %hash) {
		#$data{commissions} .= "\$".&format_number($hash{$_}{value},4)." (".&format_number($hash{$_}{percentage},2)."%) to $hash{$_}{name}<br>";
		$tmp = "";
		$tmp = ($hash{$_}{status} eq -1) ? "<font color=red><b>(deleted)</b></font> " : $tmp;
		$tmp = ($hash{$_}{invoice_id} ne "") ? "<font color=red><b>(used)</b></font> " : $tmp;
		$data{commissions_all_not_invoiced} = ($hash{$_}{invoice_id} ne "") ? 0 : $data{commissions_all_not_invoiced};
		$data{commissions} .= "\$".&format_number($hash{$_}{value},4)." $tmp to $hash{$_}{name}<br>";
	}
    #
	#-------------------------------------------
    # Get last 3 changes
	#-------------------------------------------
    %adm_users = database_select_as_hash("select id,web_user,name from adm_users","web_user,name");
    %history = database_select_as_hash("select id,1 from action_log where (type='noc:service:credit:del' or type='noc:service:credit:undel') and service_id='$service_id' order by date desc limit 0,3","flag");
	$last_3_changes = "";
	foreach $his_id (sort{$b <=> $a} keys %history){
		%hash = action_history_get_info($his_id);
		$last_3_changes .= "<li>$hash{$his_id}{text_simple}$hash{$his_id}{text_extra}</li>";
	}
	$last_3_changes = ($last_3_changes ne "") ? "<br><div class=alert_box><div><h1>Last changes</h1><ul>$last_3_changes</ul></div></div>" : "";
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $save_id = time;
	$html_action 	= "";
	$html_icon 		= "";
	$html_button	= "";
	$html_action 	= ($data{status} eq 1 ) ? "credit_del" 		: $html_action;
	$html_icon 		= ($data{status} eq 1 ) ? "money_delete" 	: $html_icon;
	$html_button 	= ($data{status} eq 1 ) ? "Delete" 			: $html_button;
	$html_action 	= ($data{status} eq -1) ? "credit_undel"	: $html_action;
	$html_icon 		= ($data{status} eq -1) ? "money_add" 		: $html_icon;
	$html_button 	= ($data{status} eq -1) ? "Un-delete" 		: $html_button;
	$html_warning	= ( ($data{status} eq 1 ) && ($data{commissions_all_not_invoiced} ne 1) ) ? "<div class=alert_box><div xxclass=alert_box_inside><b>WARNING!</b> We have some used commissions. This commissions was already used by service (by phone credit or withdraw) and cannot be deleted. All other non used commissions can be deleted with no problem</div></div><br>" : "";
	&active_session_set("save_id_cd",$save_id);
	%t = ();
    $t{dic}{content}	= qq[
		<table class=fieldtable border=0 colspan=0 cellpadding=2 cellspacing=0 width=100% ><tr>
			<td valign=top width=80 >Date:<br>		<div class=dataset_text><div>$data{date}</div></div></td><td width=5 >&nbsp;&nbsp;</td>
			<td valign=top width=100 >Type:<br>		<div class=dataset_text><div>$data{type}</div></div></td><td width=5 >&nbsp;&nbsp;</td>
			<td valign=top xwidth=100% >Status:<br>	<div class=dataset_text><div>$data{status_string}</div></div></td>
		</tr></table>

		<table class=fieldtable border=0 colspan=0 cellpadding=2 cellspacing=0 width=100% ><tr>
			<td valign=top width=120 >Noc user:<br>		<div class=dataset_text><div>$data{adm_user_name}</div></div></td><td width=5 >&nbsp;&nbsp;</td>
			<td valign=top xwidth=100% >Info:<br>	<div class=dataset_text><div>$data{text}</div></div></td>
		</tr></table>

		<table class=fieldtable border=0 colspan=0 cellpadding=2 cellspacing=0 width=100% ><tr>
			<td valign=top width=35% >
				Zenofon credit:<br>	<div class=dataset_text><div>\$$data{credit_string}</div></div>
				Money in:<br>		<div class=dataset_text><div>\$$data{value_string}</div></div>
			</td>
			<td>&nbsp;&nbsp;</td>
			<td valign=top width=65% >
				Commissions:<br><div class=dataset_textarea style="height:65px; white-space:nowrap;"><div>$data{commissions}</div></div>
			</td>
		</tr></table>
	
		<div class=clear id=form_ask>
			<br>
			<button type=button class="button button_positive button_delete" onclick="MyDisplay('form_ask',0);MyDisplay('form_action',1);document.forms[0].elements[0].focus();" style="background-image:url(/design/icons/$html_icon);">$html_button this credit</button>
		</div>
		
		<script>
		function check_form(){
			if (!document.forms[0].elements[0].value){
				alert("Please enter description");
				return false;
			}
			return true;
		}
		</script>
		<div class=clear id=form_action style=display:none>
			<form action=$my_url onsubmit="return check_form();">
			Description: <font size=1 color=#c0c0c0>(client view this text)</font><br>
			<input type=text name=text value=""  size=3 MAXLENGTH=200><br>
			<br>
			
			$html_warning
			
			<button type=button class="button button_nagative button_cancel" onclick="MyDisplay('form_ask',1);MyDisplay('form_action',0);" >Cancel</button>
			<button type=submit class="button button_positive button_delete" style="background-image:url(/design/icons/money_delete);" >$html_button</button>
			<input type=hidden name=action value=$html_action>
			<input type=hidden name=service_id value=$service_id>
			<input type=hidden name=credit_id value=$credit_id>
			<input type=hidden name=save value=$save_id>
			</form>
		</div>
		
		$last_3_changes
    ];
    &template_print("template.modal.html",%t);
}
sub do_credit_add(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,email from service where service.id='$service_id' ","flag,email");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$save_id = &active_session_get("save_id_ca");
	$form_message = "";
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		#
		# confere type
		$type = trim(clean_str(substr($form{type},0,255)));
		$type = "\U$type";
		if (index("|FREE|CASH|","|$type|") eq -1)  {$form_message .= "wrong credit type. ";}
		#
		# confere valor
		$value = clean_float(substr($form{value},0,30));
		$value++;
		$value--;
		if ($type eq "CASH") {
			if ( ($value <= 0) || ($value>100) ) {$form_message .= "Wrong value. "; }
		} else {
			if ( ($value eq 0) || ($value <= -100) || ($value>100) ) {$form_message .= "Wrong value. ";}
		}
		#
		# confere texto
		$text = trim(clean_str(substr($form{text},0,255)));
		if ($text ne $form{text})  {$form_message .= "Wrong description. "; }
		#
		# adiciona o credito
		if ($form_message eq "") {
			if ($type eq "CASH") {
				%order = ();
				$order{service_id}	= $service_id;
				$order{value_credit}= $value;
				$order{value_money}	= $value;
				$order{type}		= "CASH";
				$order{text}		= "$text";
				$order{ok}			= 0;
				%order = multilevel_credit_add(%order);
				if ($order{ok} eq 1)  {
					&action_history("noc:service:credit:cash",('service_id'=>$service_id,'credit_id'=>$order{new_credit_id},'adm_user_id'=>$app{session_cookie_u}));
					%t = ();
					$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
					&template_print("template.modal.html",%t);
					&active_session_delete("save_id_ca");
					exit;
				} else {
					$form_message .= "System error. Try again in few minutes. ($order{message})"
				}
			} elsif ($type eq "FREE"){
				%order = ();
				$order{service_id}	= $service_id;
				$order{value_credit}= $value;
				$order{value_money}	= 0;
				$order{type}		= "FREE";
				$order{text}		= "$text";
				$order{ok}			= 0;
				%order = multilevel_credit_add(%order);
				$message = $order{message};
				if ($order{ok} eq 1)  {
					&action_history("noc:service:credit:free",('service_id'=>$service_id,'credit_id'=>$order{new_credit_id},'adm_user_id'=>$app{session_cookie_u}));
					%t = ();
					$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
					&template_print("template.modal.html",%t);
					&active_session_delete("save_id_ca");
					exit;
				} else {
					$form_message .= "System error. Try again in few minutes. ($order{message})"
				}
			} else {
				$form_message .= "Unknown credit type.";
			}
		}
	}
	$form_message .= ($form_message ne "") ? "<br><br>" : "";
    #
	#-------------------------------------------
    # Get last 3 changes
	#-------------------------------------------
    %adm_users = database_select_as_hash("select id,web_user,name from adm_users","web_user,name");
    %history = database_select_as_hash("select id,1 from action_log where (type='noc:service:credit:cash' or type='noc:service:credit:free') and service_id='$service_id' order by date desc limit 0,3","flag");
	$last_3_changes = "";
	foreach $his_id (sort{$b <=> $a} keys %history){
		%hash = action_history_get_info($his_id);
		$last_3_changes .= "<li>$hash{$his_id}{text_simple}$hash{$his_id}{text_extra}</li>";
	}
	$last_3_changes = ($last_3_changes ne "") ? "<div class=last_changes><h1>Last changes</h1><ul>$last_3_changes</ul></div>" : "";
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $save_id = time;
	&active_session_set("save_id_ca",$save_id);
	%t = ();
    $t{dic}{content}	= qq[
		<script>
		function check_form(){
			myform = document.forms[0];
			if (myform.elements[0].selectedIndex<1) {alert("You need select type"); return false}
			if (myform.elements[2].value == "") {alert("You need fill value"); return false}
			return true;
		}
		</script>
		<form action=$my_url onsubmit="return check_form();">
			Credit type<br>
			<select name=type>
			<option value="">...select...</option>
			<option value="Free">Free (do not generate commission)</option>
			<option value="cash">Cash (add commission to friends above)</option>
			</select><br>
			
			Description <font size=1 color=#c0c0c0>(User can read that in credts tab)</font><br>
			<input name=text value=""><br>
			
			Value:<br>
			<input name=value><br>

			<br>			
			<font color=red><b>$form_message</b></font>
			<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
			<button type=submit class="button button_positive button_save"  >Add credit</button>
			
			<input type=hidden name=save value=$save_id>
			<input type=hidden name=service_id value=$service_id>
			<input type=hidden name=action value=credit_add>
		</form>
		<br>
		$last_3_changes 
    ];
    &template_print("template.modal.html",%t);
}
sub do_commission_add(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,email from service where service.id='$service_id' ","flag,email");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$save_id = &active_session_get("save_id_ca");
	$form_message = "";
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		#
		# confere mode
		$mode = trim(clean_str(substr($form{mode},0,255)));
		$mode = "\U$mode";
		if (index("|ZENO|SINGLE|","|$mode|") eq -1)  {$form_message .= "wrong mode. ";}
		#
		# confere valor
		$value = clean_float(substr($form{value},0,30));
		$value++;
		$value--;
		if ( ($value <= 0) || ($value>100) ) {$form_message .= "Wrong value. "; }
		#
		# confere activation_date_1
		$activation_date_1 = clean_int(substr($form{activation_date_1},0,30));
		$activation_date_1++;
		$activation_date_1--;
		if ( ($activation_date_1 < 0) || ($activation_date_1>365) ) {$form_message .= "Wrong days to credit. "; }
		#
		# confere activation_date_2
		$activation_date_2 = clean_int(substr($form{activation_date_2},0,30));
		$activation_date_2++;
		$activation_date_2--;
		if ( ($activation_date_2 < 0) || ($activation_date_2>365) ) {$form_message .= "Wrong days to credit. "; }
		#
		# confere texto
		$text = trim(clean_str(substr($form{text},0,255)));
		if ($text ne $form{text})  {$form_message .= "Wrong description. "; }
		#
		# adiciona o credito 
		if ($form_message eq "") {
			#
			# modo antigo
			#%commission = ();
			#$commission{service_id} 		= $service_id;
			#$commission{value} 				= $value;
			#$commission{title}				= $text;
			#$commission{type} 				= "MANUAL";
			#$commission{email_template} 	= "manual.commission";
			#$commission{mode} 				= $mode;
			#$commission{activation_date_1} 	= $form{activation_date_1};
			#$commission{activation_date_2} 	= $form{activation_date_2};
			#%commission = &multilevel_commission_aXdXd(%commission);
			#if ($commission{status_ok} eq 1)  {
			#
			# modo novo
			%commission = ();
			$commission{service_id} 								= $service_id;
			$commission{commission_title}							= $text;
			$commission{commission_type_value} 						= $value;
			$commission{commission_type_engine} 					= "MANUAL";
			$commission{commission_type_apply_mode} 				= $mode;
			$commission{commission_type_days_to_convert_to_credit} 	= $form{activation_date_1};
			$commission{commission_type_days_to_convert_to_check}	= $form{activation_date_2};
			%commission = &multilevel_commission_new(%commission);
			if ($commission{ok} eq 1)  {
				#&action_history("noc:service:commission",
				#	(
				#	'service_id'=>$service_id,
				#	'commission_id'=>$order{commission_id},
				#	'value_old'=>"$mode:$value",
				#	'value_new'=>$text,
				#	'adm_user_id'=>$app{session_cookie_u}
				#	)
				#);
				%t = ();
				$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
				&template_print("template.modal.html",%t);
				&active_session_delete("save_id_ca");
				exit;
			} else {
				$form_message .= "System error. Try again in few minutes. ($commission{status_message})";
			}
		}
	}
	$form_message .= ($form_message ne "") ? "<br><br>" : "";
    #
	#-------------------------------------------
    # Get last 3 changes
	#-------------------------------------------
    %adm_users = database_select_as_hash("select id,web_user,name from adm_users","web_user,name");
    %history = database_select_as_hash("select id,1 from action_log where type='noc:service:commission' and service_id='$service_id' order by date desc limit 0,3","flag");
	$last_3_changes = "";
	foreach $his_id (sort{$b <=> $a} keys %history){
		%hash = action_history_get_info($his_id);
		$last_3_changes .= "<li>$hash{$his_id}{text_simple}$hash{$his_id}{text_extra}</li>";
	}
	$last_3_changes = ($last_3_changes ne "") ? "<div class=last_changes><h1>Last changes</h1><ul>$last_3_changes</ul></div>" : "";
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$form{activation_date_1} = ($form{activation_date_1} eq "") ? "7" : $form{activation_date_1}; 
	$form{activation_date_2} = ($form{activation_date_2} eq "") ? "90" : $form{activation_date_2};
	$form{"mode_radio_".$form{mode}} = "checked";
    $save_id = time;
	&active_session_set("save_id_ca",$save_id);
	%t = ();
    $t{dic}{content}	= qq[
		<script>
		function check_form(){
			myform = document.forms[0];
			if (myform.elements[0].selectedIndex<1) {alert("You need select type"); return false}
			if (myform.elements[2].value == "") {alert("You need fill value"); return false}
			return true;
		}
		</script>
		<form action=$my_url onsubmit="return check_form();">

			Description <font size=1 color=#c0c0c0>(User can read that in credts tab)</font><br>
			<input name=text value="$form{text}"><br>
			
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear width=100% ><tr>
				<td valign=top with=33%>Commission<br>value:<br><input name=value value="$form{value}"></td>
				<td>&nbsp;&nbsp;</td>
				<td valign=top with=33%>Days to credits:<br><input value="$form{activation_date_1}" name=activation_date_1></td>
				<td>&nbsp;&nbsp;</td>
				<td valign=top with=33%>Days to check:<br><input value="$form{activation_date_2}" name=activation_date_2></td>
			</tr></table>

			<br>
			<input type=radio $form{mode_radio_SINGLE}	name=mode value=SINGLE 	class=clear align=left	><b>Single mode</b ><br	><div class=clear style=padding-left:15px;color:#c0c0c0;font-size:10px;line-height:100%;margin-bottom:5px;>This service will get the <i>100% OF VALUE</i> as commission and we do not send commissions for they parents.</div>
			<input type=radio $form{mode_radio_ZENO} 	name=mode value=ZENO 	class=clear align=left	><b>Zeno mode</b><br	><div class=clear style=padding-left:15px;color:#c0c0c0;font-size:10px;line-height:100%;margin-bottom:5px;>Use Zeno logic. Send <i>50% OF THE VALUE</i> as commissions for this service, 25% to they parent, 12.5% to parent of parent and soo on</div>

			<br>			
			<font color=red><b>$form_message</b></font>
			<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
			<button type=submit class="button button_positive button_save"  >Add credit</button>
			
			<input type=hidden name=save value=$save_id>
			<input type=hidden name=service_id value=$service_id>
			<input type=hidden name=action value=commission_add>
		</form>
		<br>
		$last_3_changes 
    ];
    &template_print("template.modal.html",%t);
}
sub do_status_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash(
		"
		select 1,1,service.status
		from service, service_status
		where service.id='$service_id' and service.status=service_status.id and service_status.deleted=0 
		","flag,status");
    unless ($hash{1}{flag} eq 1) { %t=(); $t{dic}{content}="Invalid service_id"; &template_print("template.modal.html",%t);exit; }
	$service_status = $hash{1}{status};
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$save_id = &active_session_get("save_id_ca");
	$form_message = "";
	if ( ($form{save} ne "") && ($form{save} eq $save_id) ) {
		#
		# confere mode
		$status = clean_int(substr($form{status},0,255));
	    %hash = database_select_as_hash("select 1,1 from service_status where id='$status' and deleted=0 ","flag");
	    if ($hash{1}{flag} ne 1) {  $form_message .= "wrong status. "; }
		#
		# acao
		if ($form_message eq "") {
			%hash2 = database_select_as_hash("SELECT 1,1,service_status.name FROM service_status,service where service.status=service_status.id and service.id='$service_id' ","flag,value");
			$value_old = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : "Unknown";
			&database_do("update service set service.status=$status where service.id='$service_id' ");
			%hash2 = database_select_as_hash("SELECT 1,1,service_status.name FROM service_status,service where service.status=service_status.id and service.id='$service_id' ","flag,value");
			$value_new = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : "Unknown";
			&action_history("noc:service:status:change",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>$value_old, 'value_new'=>$value_new ));
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
			&active_session_delete("save_id_ca");
			exit;
		}
	}
	$form_message .= ($form_message ne "") ? "<br><br>" : "";
	#
	#-------------------------------------------
    # load
	#-------------------------------------------
	if ($form{save} eq "") {
		$form{status} = $service_status;	
	}
	#
	#-------------------------------------------
    # Get status
	#-------------------------------------------
	%hash = database_select_as_hash("SELECT id,name,text FROM service_status where deleted=0","name,text,deleted");
	$html_select 	= "";
	$html_info 		= "";
	$html_js 		= "";
	$split_id_last 	= "";
	$split_id_now 	= "";
    foreach $id (sort{$hash{$a}{name} cmp $hash{$b}{name}} keys %hash) {
		$split_id_now	= (index($hash{$id}{name},"(") eq -1) ? $hash{$id}{name} : substr($hash{$id}{name},0,index($hash{$id}{name},"("));
		$tmp1 = ($id eq $form{status}) ? " selected " : "";
		$tmp2 = ($id eq $service_status) ? "style='padding-left:18px;background-image:url(/design/icons/tick.png);background-repeat:no-repeat;'" : "";
		$html_select 	.= ($split_id_now ne $split_id_last) ? "<option>&nbsp;</option>" : "";
		$html_select 	.= "<option value=$id $tmp1 $tmp2>$hash{$id}{name}</option>";
		$html_info 		.= "<div id=info_$id $tmp1 style='display:none;'>$hash{$id}{text}</div>";
		$html_js 		.= "MyDisplay('info_$id',0);";
		$split_id_last	= $split_id_now;
	}
	$html_select .= "<option>&nbsp;</option>"; 
	#-------------------------------------------
    # Get last 3 changes
	#-------------------------------------------
    %adm_users = database_select_as_hash("select id,web_user,name from adm_users","web_user,name");
    %history = database_select_as_hash("
		select id,unix_timestamp(date),value_old,value_new,adm_user_id
		from action_log
		where type='noc:service:status:change' and service_id='$service_id'
		order by date desc
		limit 0,3
		","date,value_old,value_new,noc_user");
	$last_3_changes = "";
	foreach $his_id (sort{$b <=> $a} keys %history){
		$noc_name = (exists($adm_users{$history{$his_id}{noc_user}})) ? "$adm_users{$history{$his_id}{noc_user}}{web_user} ($adm_users{$history{$his_id}{noc_user}}{name})" : "UNKNOWN ($history{$his_id}{noc_user})";
		$last_3_changes .= "<li>".&format_time_gap($history{$his_id}{date}).", changed from '$history{$his_id}{value_old}' to '$history{$his_id}{value_new}' by $noc_name. </li>";
	}
	$last_3_changes = ($last_3_changes ne "") ? "<div class=last_changes><h1>Last changes</h1><ul>$last_3_changes</ul></div>" : "";
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
    $save_id = time;
	&active_session_set("save_id_ca",$save_id);
	%t = ();
    $t{dic}{content}	= qq[
		<script>
		function check_form(){
			myform = document.forms[0];
			if (myform.elements[0].selectedIndex<1) {alert("You need select status"); return false}
			return true;
		}
		function update_select(){
			myform	= document.forms[0];
			index	= myform.elements[0].selectedIndex;
			value	= myform.elements[0].options[index].value;
			$html_js
			MyDisplay("info_"+value,1);
		}
		</script>
		<form action=$my_url onsubmit="return check_form();">



			Status:<br>
			<select name=status onchange="update_select();" style=width:100%;>$html_select</select><br>
			<div style="padding:3px; font-size:10px;line-height:130%; ">$html_info</div><br>

			<font color=red><b>$form_message</b></font>
			<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
			<button type=submit class="button button_positive button_save"  >Change status</button>
			
			<input type=hidden name=save value=$save_id>
			<input type=hidden name=service_id value=$service_id>
			<input type=hidden name=action value=status_edit>
		</form>
		<br>
		$last_3_changes
		<script>update_select();</script>
    ];
    &template_print("template.modal.html",%t);
}
sub do_status_edit_multiple(){
    #
	#-------------------------------------------
    # confere service_id 
	#-------------------------------------------
	%selected_ids = ();
	$selected_ids_qtd = 0;
    foreach $id (split(/\,/,$form{service_ids})) {
		%hash = database_select_as_hash("select 1,1 from service,service_status where service.id='$id' and service.status=service_status.id and service_status.deleted=0 ","flag");
		if ($hash{1}{flag} eq 1) {
			$selected_ids{$id}++; $selected_ids_qtd++
		}
	}
	$selected_ids_sql = join(",",(keys %selected_ids));
    if ($selected_ids_sql eq "") { %t=(); $t{dic}{content}="Invalid service_ids"; &template_print("template.modal.html",%t);exit; }
	#
	#-------------------------------------------
	# get data
	#-------------------------------------------
	%data = ();
    %hash = database_select_as_hash("SELECT id,name FROM service_status where deleted=0 ");
	foreach (keys %hash) { $data{$_}{name}=$hash{$_} }
    %hash = database_select_as_hash_with_auto_key("SELECT status,id FROM service WHERE id in ($selected_ids_sql) ","status_id,service_id");
	foreach $id (keys %hash) {
		$st_id = $hash{$id}{status_id};
		$se_id = $hash{$id}{service_id};
		unless (exists($data{$st_id})) {next}
		$data{$st_id}{qtd}++;
		$data{$st_id}{ids} .= "$se_id,";
	}
	foreach $id (keys %data) {
		if ($data{$id}{ids} ne "") {$data{$id}{ids} = substr($data{$id}{ids},0,-1);}
	}
	#
	#-------------------------------------------
	# try to save
	#-------------------------------------------
	$form_message = "";
	if ( &multilevel_clickchain_check("ms",$form{save}) eq 1 ) {
		foreach $status_id (keys %data) {
			$status_id_new = $form{"status_".$status_id};
			if ($data{$status_id}{ids} eq "") {next}
			if ($status_id_new eq "") {next}
			if ($status_id_new eq $status_id) {next}
			unless (exists($data{$status_id_new})) {next}
			foreach $service_id (split(/\,/,$data{$status_id}{ids})){
				if ($service_id eq "") {next}
				%hash3 = database_select_as_hash("SELECT 1,1,service_status.name FROM service_status,service where service.status=service_status.id and service.id='$service_id' ","flag,value");
				$value_old = ($hash3{1}{flag} eq 1) ? $hash3{1}{value} : "Unknown";
				&database_do("update service set service.status=$status_id_new where service.id='$service_id' ");
				%hash3 = database_select_as_hash("SELECT 1,1,service_status.name FROM service_status,service where service.status=service_status.id and service.id='$service_id' ","flag,value");
				$value_new = ($hash3{1}{flag} eq 1) ? $hash3{1}{value} : "Unknown";
				&action_history("noc:service:status:change",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>$value_old, 'value_new'=>$value_new ));
			}
		}
		%t = ();
		$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		&template_print("template.modal.html",%t);
		exit;
	}
	#
	#-------------------------------------------
	# load form
	#-------------------------------------------
	$html_list = "";
	foreach $status_id (sort{$data{$a}{name} cmp $data{$b}{name}} keys %data) {
		if ($data{$status_id}{ids} eq "") {next}
		$html_select 	= "";
		$split_id_last 	= "";
		$split_id_now 	= "";
		foreach $id (sort{$data{$a}{name} cmp $data{$b}{name}} keys %data) {
			$split_id_now	= (index($data{$id}{name},"(") eq -1) ? $data{$id}{name} : substr($data{$id}{name},0,index($data{$id}{name},"("));
			$tmp1 = ($id eq $form{"status_".$status_id}) ? " selected " : "";
			$html_select 	.= ($split_id_now ne $split_id_last) ? "<option>&nbsp;</option>" : "";
			$html_select 	.= "<option value=$id $tmp1 $tmp2>Change to '$data{$id}{name}'</option>";
			$split_id_last	= $split_id_now;
		}
		$html_list .= qq[
		$data{$status_id}{qtd} service(s) with status '$data{$status_id}{name}'.<br>
		<select style=width:100% name=status_$status_id>
		<option style="color:#c0c0c0;">(Dont change status for this services)</option>
		$html_select 
		<option>&nbsp;</option>
		</select>
		<br>
		];
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$clickchain_id = &multilevel_clickchain_set("ms");
	%t = ();
    $t{dic}{content}	= qq[
		<form action=$my_url>

			$html_list

			<font color=red><b>$form_message</b></font>
			<button type=button class="button button_negative button_cancel" onclick=parent.modal_close()>Cancel</button>
			<button type=submit class="button button_positive button_save"  >Change status for this $selected_ids_qtd services</button>
			<input type=hidden name=save value=$clickchain_id>
			<input type=hidden name=action value=status_edit_multiple>
			<input type=hidden name=service_ids value="$form{service_ids}"><br>
		</form>
    ];
    &template_print("template.modal.html",%t);
}
sub do_profile_affiliate(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1 from service where service.id='$service_id' ","flag");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{dic}{content} = "Invalid service_id";
		&template_print("template.modal.html",%t);
		exit;
	}
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
		if (index("|,DEL,DATA,HEAD,|,DATA,|,|","|$form{flags}|") eq -1) {
			$form_ok = 0;
			$form_message = "Select one option<br><br>";
			$form{flags} = "";
		} else {
			$form_ok = 1;
		}
	}
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&data_set("service_data",$service_id,"ss_flags",$form{flags});
		&action_history("noc:service:affiliate:lock",('service_id'=>$service_id,'adm_user_id'=>$app{session_cookie_u}));
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
		$form{flags} = &data_get("service_data",$service_id,"ss_flags");
		$form{flags} = ($form{flags} eq "") ? ",DEL,DATA,HEAD," : $form{flags};
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$html_select = "";
	$tmp = ($form{flags} eq ",DEL,DATA,HEAD,"	) ? "selected" : "";$html_select .= "<option value=',DEL,DATA,HEAD,' 	$tmp>Complete unlocked</option>";
	$tmp = ($form{flags} eq ",DATA,"			) ? "selected" : "";$html_select .= "<option value=',DATA,' 			$tmp>Edit address only</option>";
	$tmp = ($form{flags} eq ","					) ? "selected" : "";$html_select .= "<option value=',' 					$tmp>Complete locked</option>";
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[
	affiliate profile locker control what client can do with affiliate profile.
	Most of time system handle this automatic.
	Only change if you know what are you doing.
	<br>
	<br>
	<form action=$my_url>
	<select name=flags><option value=''>(select lock mode)</option><option value=''></option>$html_select</select><br>	
	<br>
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=service_id value=$service_id>
	<input type=hidden name=action value=profile_affiliate>
    ];
    &template_print("template.modal.html",%t);
}
sub do_service_agestatus(){
    #
	#-------------------------------------------
    # check service_id and get some data
	#-------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1,age_id,age_is_manual from service where service.id='$service_id' ","flag,age_id,age_is_manual");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{dic}{content} = "Invalid service_id";
		&template_print("template.modal.html",%t);
		exit;
	}
    #
	#---------------------------------------------------
	# get age status title
	#---------------------------------------------------
    $age_id 		= $hash{1}{age_id} ;   
    $age_is_manual	= ($hash{1}{age_is_manual} eq 1) ? 1 : 0;   
    %age_list 		= &database_select_as_hash("select id,ui_order,title from service_age ","ui_order,title");
    $age_title 		= (exists($age_list{$age_id})) ? $age_list{$age_id}{title} : "(unknown)"; 
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
		if ( ($form{age_id} eq "AUTO") || (exists($age_list{$form{age_id}})) ) {
			$form_ok = 1;
		} else {
			$form_ok = 0;
			$form_message = "Select one option<br><br>";
			$form{age_id} = "";
		}
	}
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		if ($form{age_id} eq "AUTO") {
			&database_do("update service set age_is_manual=0 where id='$service_id' ");
			&action_history("noc:service:agestatus:edit",('service_id'=>$service_id,'adm_user_id'=>$app{session_cookie_u}));
			# TODO: calc agi_id.. maybe crate API call for that, to avoid duplicate code
		} else {
			&database_do("update service set age_id ='$form{age_id}', age_is_manual=1 where id='$service_id' ");
			&action_history("noc:service:agestatus:edit",('service_id'=>$service_id,'adm_user_id'=>$app{session_cookie_u}));
		}
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
		$form{age_id} = $age_id;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
	$html_select = "";
	foreach $id (sort{$age_list{$a}{ui_order} <=>  $age_list{$b}{ui_order}} keys %age_list) {		 
			$tmp = ( ($age_is_manual eq 1) && ($age_id eq $id) ) ? "selected" : ""; 
			$html_select .= "<option value='".$id."' $tmp >Set manualy to ".$age_list{$id}{title}."</option>";
	}
    $age_message = ($hash{1}{age_is_manual} eq 1) ? "<b><font color=red>Warning:</font></b> Service age is manualy set to '$age_title'. This status will not change as time goes by. Is this what you want?" : "Service age '$age_title' and will change automaticly as time goes by.";   
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[
	<br>
	$age_message
	<br>
	<br>
	<form action=$my_url>
	<select name=age_id>
		<option value='AUTO'>Set automatic</option>
		<option value=''></option>
		$html_select
		</select><br>	
	<br>
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=service_id value=$service_id>
	<input type=hidden name=action value=service_agestatus>
    ];
    &template_print("template.modal.html",%t);
}
#========================================================================
# view a service
#========================================================================
sub do_view_overview(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
    #
	#---------------------------------------------------
    # get notes
	#---------------------------------------------------
    %hash = database_select_as_hash("select 1,1,text from service_note where service_id='$service_id' ","flag,text");
    $notes = ($hash{1}{flag} eq 1) ? $hash{1}{text} : "";
    #
	#---------------------------------------------------
    # get tags
	#---------------------------------------------------
    %hash = database_select_as_hash(
		"
		SELECT service_tag_string.id,service_tag_string.tag
		FROM service_tag, service_tag_string
		WHERE service_tag.tag_string_id=service_tag_string.id and service_tag.service_id='$service_id' 
		","tag");
	$tags = "";
	foreach (sort{$hash{$a} cmp $hash{$b}} keys %hash) {$tags .= "'$hash{$_}{tag}', ";}
	if ($tags ne "") {
		$tags = substr($tags,0,-2);
	} else {
		$tags = "<font color=#c0c0c0>(no tags)</font>";
	}
	#
	#---------------------------------------------------
	# get afiliate profile
	#---------------------------------------------------
	$data{afiliate_profile_flags} = &data_get("service_data",$service_id,"ss_flags");
	$data{afiliate_profile_status} = "(unknown)";
	$data{afiliate_profile_status} = ($data{afiliate_profile_flags} eq ",DEL,DATA,HEAD,"	) ? "Complete unlocked"	: $data{afiliate_profile_status} ;
	$data{afiliate_profile_status} = ($data{afiliate_profile_flags} eq ",DATA,"				) ? "Edit address only"	: $data{afiliate_profile_status} ;
	$data{afiliate_profile_status} = ($data{afiliate_profile_flags} eq ","					) ? "Complete locked"	: $data{afiliate_profile_status} ;
    #
	#---------------------------------------------------
	# get age status title
	#---------------------------------------------------
    $age_id = $data{age_id} ;   
    $is_manualset_text = ($data{age_is_manual} eq "1")? 'manually set as ':'automatically set as ';
    %hash = database_select_as_hash("select 1,1,title from service_age where id='$age_id'  ","flag,title");
    $data{service_agestatus} = ($hash{1}{flag} eq 1) ? $hash{1}{title} : "";
    #
	#===========================================================================
    # imprime pagina
	#===========================================================================
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "Service Overview";
    $t{breadcrumb}{1}{title}	= "Clients & services";
    $t{breadcrumb}{1}{url}		= "";
    $t{breadcrumb}{2}{title}	= "Search services";
    $t{breadcrumb}{2}{url}		= "$my_url?remember=1";
    $t{breadcrumb}{3}{title}	= "Service number $service_id";
    $t{breadcrumb}{3}{url}		= "$my_url?action=view&service_id=$service_id";
    $t{breadcrumb}{4}{title}	= "Overview";
    $t{breadcrumb}{4}{url}		= "";
    $t{dic}{content}	= qq[
			<table border=0 colspan=0 cellpadding=2 cellspacing=0 width=600 class=clear>
			<tr>
				<td valign=top width=42% style=padding-right:25px;>
					Service name:<br>	<div class=dataset_text style="margin-bottom:5px;"><a href="$my_url?action=name_edit&service_id=$service_id"	onClick="modal_open('Edit service name','$my_url?action=name_edit&service_id=$service_id',300,285); return false;"></a><div>$data{name}</div></div>
					Service email:<br>	<div class=dataset_text style="margin-bottom:0px;"><a href="$my_url?action=email_edit&service_id=$service_id"	onClick="modal_open('Edit service email','$my_url?action=email_edit&service_id=$service_id',300,285); return false;"></a><div>$data{email}</div></div>
					Status:<br>			<div class=dataset_text 	style="margin-bottom:5px;"				><a href="$my_url?action=status_edit&service_id=$service_id"	onClick="modal_open('Edit service status','$my_url?action=status_edit&service_id=$service_id',300,400); return false;"></a><div>$data{status}</div></div>
					PIN:<br>	<div class=dataset_text style="margin-bottom:5px;"><div>$data{pin}</div></div>
					Invite:<br>	<div class=dataset_text style="margin-bottom:5px;">
						<a href="/$data{invite}" target=_blank style="background-image:url(/design/icons/arrow-045-medium.png);"></a>
						<a href="$my_url?action=invite_edit&service_id=$service_id"	onClick="modal_open('Edit invite code','$my_url?action=invite_edit&service_id=$service_id',300,280); return false;">&nbsp;</a>
						<div>$data{invite}</div></div>
					Affiliate profile:<br>	<div class=dataset_text><a href="$my_url?action=profile_affiliate&service_id=$service_id" onClick="modal_open('Edit affiliate profile','$my_url?action=profile_affiliate&service_id=$service_id',300,360); return false;"></a><div>$data{afiliate_profile_status}</div></div>
					Tags:<br>			<div class=dataset_text 	style="margin-bottom:5px; height:35px; "><a href="$my_url?action=tags_select&service_id=$service_id"	onClick="modal_open('Select tags','$my_url?action=tags_select&service_id=$service_id',400,450); return false;"></a><div>$tags</div></div>
				 	Age Status( $is_manualset_text):<br>	<div class=dataset_text><a href="$my_url?action=service_agestatus&service_id=$service_id" onClick="modal_open('Edit service age status','$my_url?action=service_agestatus&service_id=$service_id',300,360); return false;"></a><div>$data{service_agestatus}</div></div>
				</td>
				<td valign=top width=58%>
					Note:<br>			<div class=dataset_textarea style="margin-bottom:0px; height:313px;"><a href="$my_url?action=note_edit&service_id=$service_id" 		onClick="modal_open('Edit note','$my_url?action=note_edit&service_id=$service_id',350,300); return false;"></a><div>$notes</div></div>
				</td>
			</tr>		
			</table>


    ];
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub do_view_calls(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
	#
	#---------------------------------------------------
	# pega totais
	#---------------------------------------------------
	%hash = database_select_as_hash("SELECT 1,1,count(*) FROM calls_log where service_id='$service_id' and datetime_stop is not null ","flag,qtd");
	$quantity = ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd}>0)) ? $hash{1}{qtd} : 0; 
	#
	#---------------------------------------------------
	# calcula paginas
	#---------------------------------------------------
	$page_size		= clean_int(substr($form{page_size},0,100));
	$page_size		= ($page_size eq "") ? 15 : $page_size;
	$page_min		= 1;
	$page_max		= int(($quantity-1)/$page_size)+1;
	$page_max		= ($page_max<$page_min) ? $page_min : $page_max;
	$page 			= clean_int($form{history_page});
	$page 			= ($form{next} eq 1) ? $page+1 : $page;
	$page 			= ($form{previous} eq 1) ? $page-1 : $page;
	$page 			= ($page<$page_min) ? $page_min : $page;
	$page 			= ($page>$page_max) ? $page_max : $page;
	$sql_limit_1	= ($page-1)*$page_size;
	$sql_limit_2	= $page_size;
	#
	#---------------------------------------------------
	# pega calls
	#---------------------------------------------------
	%calls_info = database_select_as_hash("SELECT id,value FROM calls_log_info");
	$sql = "
	SELECT id,unix_timestamp(datetime_start),ani,did,dst,billing_id,error_id,info_id
	FROM calls_log where service_id='$service_id' and datetime_stop is not null
	order by datetime_start desc
	limit $sql_limit_1 , $sql_limit_2
	";
	%calls = database_select_as_hash($sql, "date,ani,did,dst,billing_id,error_id,info_id");
	foreach $id (keys %calls){
		if ($calls{$id}{billing_id} ne "") {
			%hash = database_select_as_hash("SELECT 1,1,seconds,balance_before,value FROM calls where id='$calls{$id}{billing_id}'","flag,seconds,balance,value");
			$calls{$id}{value}		= ( ($hash{1}{flag} eq 1) && ($hash{1}{value} 	ne "") ) ? $hash{1}{value} : "";
			$calls{$id}{balance}	= ( ($hash{1}{flag} eq 1) && ($hash{1}{balance} ne "") ) ? $hash{1}{balance} : "";
			$calls{$id}{seconds}	= ( ($hash{1}{flag} eq 1) && ($hash{1}{seconds} ne "") ) ? $hash{1}{seconds} : "";
		}
	}
	#
	#---------------------------------------------------
	# monta pagina
	#---------------------------------------------------
	$html_empty = "<tr><td colspan=10><center>empty...</center></td></tr>";
	$html = "";
	foreach $id (sort{$calls{$b}{date} <=> $calls{$a}{date}} keys %calls) {
		$html_empty = "";
		$calls{$id}{date} = &format_time_gap($calls{$id}{date});
		$calls{$id}{ani} = &format_E164_number($calls{$id}{ani},"USA");
		$calls{$id}{did} = &format_E164_number($calls{$id}{did},"USA"); 
		$calls{$id}{dst} = &format_E164_number($calls{$id}{dst},"USA");
		$calls{$id}{status} 	= $calls_info{$calls{$id}{info_id}};
		$calls{$id}{status} 	= ($calls{$id}{billing_id} ne "") ? "Billed!" : $calls{$id}{status};
		$calls{$id}{status} 	= ($calls{$id}{status} eq "") ? "not connected" : $calls{$id}{status};
		$calls{$id}{balance_1} 	= ($calls{$id}{balance} eq "") ? "&nbsp;" : "\$".&format_number($calls{$id}{balance},2);
		$calls{$id}{balance_2} 	= ($calls{$id}{balance} eq "") ? "&nbsp;" : "\$".&format_number(($calls{$id}{balance}-$calls{$id}{value}),2);
		$calls{$id}{value} 		= ($calls{$id}{value} eq "") ? "&nbsp;" : "\$".&format_number($calls{$id}{value},2);
		$calls{$id}{duration}	= ($calls{$id}{seconds} eq "") ? "&nbsp;" : &format_number($calls{$id}{seconds},0);
		$url = "<a href=\"$my_url?action=detail_call&call_log_id=$id\"	onClick=\"modal_open('Call debug','$my_url?action=detail_call&call_log_id=$id',600,400); return false;\" >";
		$html .= "
		<tr>
		<td>$url$calls{$id}{date}</a></td>
		<td>$url$calls{$id}{ani}</a>&nbsp;</td>
		<td>$url$calls{$id}{did}</a>&nbsp;</td>
		<td>$url$calls{$id}{dst}</a>&nbsp;</td>
		<td>$url$calls{$id}{status}</a>&nbsp;</td>
		<td class=ar>$calls{$id}{duration}</td>
		<td class=ar>$calls{$id}{value}</td>
		<td class=ar>$calls{$id}{balance_2}</td>
		</tr>
		";
	}
	$html .= $html_empty;
	$html_pg_list = "";
	foreach($page_min..$page_max) {
		$tmp = ($_ eq $page) ? "selected" : ""; 
		$html_pg_list .= "<option $tmp value=$_>Page: $_ of $page_max</option>";
	}
	$html_pgsize_list = "";
	$tmp = (15 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=15>15 itens per page</option>";
	$tmp = (50 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=50>50 itens per page</option>";
	$tmp = (500 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=500>500 itens per page</option>";
    $t{dic}{content}	= qq[
			<form action=$my_url>
			<input type=hidden name=action value=view_calls>
			<input type=hidden name=service_id value=$service_id>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; onclick="sortColumn(event)">
				<thead>
					<tr>
					<td >Date</td>
					<td >ANI</td>
					<td >DID</td>
					<td >DST</td>
					<td >Status</td>
					<td >Duration</td>
					<td >Value</td>
					<td >Balance<br>after</td>
					</tr>
				</thead>
				<tbody >
					$html
				</tbody>
				<tfoot>
					<tr><td colspan=9 >
					<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
						<td ><button type=submit name=previous value=1><img src=/design/icons/bullet_arrow_left.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
						<td ><select name=history_page onchange="this.form.submit()">$html_pg_list</select></td>
						<td ><select name=page_size onchange="document.forms[0].submit()">$html_pgsize_list</select></td>
						<td ><button type=submit name=next value=1><img src=/design/icons/bullet_arrow_right.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
					</table>
					</td></tr>
				</tfoor>
			</table>
			</form>
	];
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Service</a> &#187; Calls";
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub do_view_credits(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
	#
	#---------------------------------------------------
	# calcula paginas
	#---------------------------------------------------
	%hash = database_select_as_hash("SELECT 1,1,count(*) FROM credit where service_id='$service_id' ","flag,qtd");
	$quantity 		= ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} ne "") ) ? $hash{1}{qtd} : 0;
	$page_size		= clean_int($form{page_size});
	$page_size		= ($page_size eq "") ? 15 : $page_size;
	$page_min		= 1;
	$page_max		= int(($quantity-1)/$page_size)+1;
	$page_max		= ($page_max<$page_min) ? $page_min : $page_max;
	$page 			= clean_int($form{history_page});
	$page 			= ($form{next} eq 1) ? $page+1 : $page;
	$page 			= ($form{previous} eq 1) ? $page-1 : $page;
	$page 			= ($page<$page_min) ? $page_min : $page;
	$page 			= ($page>$page_max) ? $page_max : $page;
	$limit_start	= ($page-1)*$page_size;
	$limit_length	= $page_size;
	%credits = &database_select_as_hash("
		SELECT id,unix_timestamp(date),status,credit_type,credit,value,text 
		FROM credit
		where service_id='$service_id'
		order by date desc
		limit $limit_start,$limit_length
		","date,status,credit_type,credit,value,text"
		);
	$selected_ids = join(",",(keys %credits)); 
	if ($selected_ids ne ""){
		%adm_user_ids = &database_select_as_hash("select credit_id,adm_user_id from action_log where credit_id in ($selected_ids)");
		%adm_user_names = database_select_as_hash("select id,concat(name,' (',web_user,')') from adm_users  ");
	}
	#
	#---------------------------------------------------
	# pega totais
	#---------------------------------------------------
	%total = ();
	$total{qtd} = "0";
	$total{credit_all} 	= "0.00";
	$total{credit_money}= "0.00";
	$total{credit_free}	= "0.00";
	$total{credit_profit}	= "0.00";
	%hash = database_select_as_hash("SELECT 1,1,count(*),sum(credit),sum(value) FROM credit where service_id='$service_id' and status=1  ","flag,qtd,credit,value");
	if ($hash{1}{flag} eq 1) {
		$total{qtd} = $hash{1}{qtd};
		$total{credit_all} 	= &format_number($hash{1}{credit},2);
		$total{credit_money}= &format_number($hash{1}{value},2);
		$total{credit_free}	= &format_number(($hash{1}{credit}-$hash{1}{value}),2);
		$total{credit_profit}	= &format_number(($hash{1}{value}-($hash{1}{credit}-$hash{1}{value})),2);
	}
	#
	#---------------------------------------------------
	# monta o html
	#---------------------------------------------------
	foreach $id (sort{$credits{$b}{date} <=> $credits{$a}{date}} keys %credits) {
		$type =  $credits{$id}{credit_type};
		$type = ($credits{$id}{credit_type} eq "FREE") 				? "free" : $type;
		$type = ($credits{$id}{credit_type} eq "AUTHORIZE_CC")		? "credit card" : $type;
		$type = ($credits{$id}{credit_type} eq "AUTHORIZE_CIM")		? "pay as you go" : $type;
		$type = ($credits{$id}{credit_type} eq "AUTHORIZE_ACIM")	? "auto recharge" : $type;
		$type = ($credits{$id}{credit_type} eq "CASH") 				? "cash (on NOC)" : $type;
		$type = ($credits{$id}{credit_type} eq "COMMISSION_CRED")	? "by commission" : $type;
		$type = ($credits{$id}{status} eq 0) 	? "<font color=red>(in progress)</font> $type" : $type;
		$type = ($credits{$id}{status} eq -1) 	? "<font color=red>(deleted)</font> $type" : $type;
		$text = ($credits{$id}{text} eq "") ? "" : " '$credits{$id}{text}'";
		$adm_user_id 		= ($adm_user_ids{$id} ne "") ? $adm_user_ids{$id} : "";
		$adm_user_id_name 	= ($adm_user_names{$adm_user_id} ne "") ? " by $adm_user_names{$adm_user_id}" : "&nbsp;";
		$link 				= qq[<a href="$my_url?action=credit_view&service_id=$service_id&credit_id=$id"	onClick="modal_open('View credit','$my_url?action=credit_view&service_id=$service_id&credit_id=$id',450,500); return false;">];
		$html_history .= "<tr>";
		$html_history .= "<td valign=top style=white-space:nowrap;>$link".&format_time_gap($credits{$id}{date})."</a></td>";
		$html_history .= "<td valign=top >$link$type $text $adm_user_id_name</a></td>";
		$html_history .= "<td valign=top style=white-space:nowrap;>$link\$".&format_number($credits{$id}{credit},2)."</a></td>";
		$html_history .= "</tr>";
	}
    #
	#---------------------------------------------------
    # print page
	#---------------------------------------------------
	$html_pg_list = "";
	foreach($page_min..$page_max) {
		$tmp = ($_ eq $page) ? "selected" : ""; 
		$html_pg_list .= "<option $tmp value=$_>Page: $_ of $page_max</option>";
	}
	$html_pgsize_list = "";
	$tmp = (15 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=15>15 itens per page</option>";
	$tmp = (50 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=50>50 itens per page</option>";
	$tmp = (500 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=500>500 itens per page</option>";
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Service</a> &#187; Phone credits";
    $t{dic}{title}	= "Service phone credits";
    $t{breadcrumb}{1}{title}	= "Clients & services";
    $t{breadcrumb}{1}{url}		= "$my_url";
    $t{breadcrumb}{2}{title}	= "Search services";
    $t{breadcrumb}{2}{url}		= "$my_url?remember=1";
    $t{breadcrumb}{3}{title}	= "Service number $service_id";
    $t{breadcrumb}{3}{url}		= "$my_url?action=view&service_id=$service_id";
    $t{breadcrumb}{4}{title}	= "Phone credits";
    $t{breadcrumb}{4}{url}		= "";
    $t{dic}{content}	= qq[

		<table border=0 colspan=0 cellpadding=0 cellspacing=0 width=100%><tr>
			<td width=20% 	style="padding-right:10px;border-right:1px solid #c0c0c0;" >Balance:<br>	<div class=dataset_text 	><a style="background-image:url(/design/icons/add.png);" href="$my_url?action=credit_add&service_id=$service_id" onClick="modal_open('Add credit','$my_url?action=credit_add&service_id=$service_id',300,360); return false;"></a><div>\$$data{credit}</div></div></td>
			<td width=20% 	style=padding-right:10px;padding-left:10px; >Money credits:<br><div class=dataset_text 	><div>\$$total{credit_money}</div></div></td>
			<td 			style=padding-right:10px;>+</td>
			<td width=20% 	style=padding-right:10px; >Free credits:<br><div class=dataset_text 	><div>\$$total{credit_free}</div></div></td>
			<td 			style=padding-right:10px;>=</td>
			<td width=20% 	style="padding-right:10px;border-right:1px solid #c0c0c0;">Total credits:<br><div class=dataset_text 	><div>\$$total{credit_all}</div></div></td>
			<td width=20% 	style=padding-left:10px;>Profit: (money-free)<br><div class=dataset_text 	><div>\$$total{credit_profit}</div></div></td>
		</tr></table>

		<form action=$my_url>
		<input type=hidden name=action value=view_calls>
		<input type=hidden name=service_id value=$service_id>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; onclick="sortColumn(event)">
			<thead>
				<tr>
				<td colspan=4><h1>Credits</h1></td>
				</tr>
				<tr>
				<td width=100 >Date</td>
				<td >Type</td>
				<td >Value</td>
				</tr>
			</thead>
			<tbody >
				$html_history 
				$html_history_empty
			</tbody>
			<tfoot>
				<tr><td colspan=8 >
				<table border=0 colspan=0 cellpadding=0 cellspacing=0 >
					<td ><button type=submit name=previous value=1><img src=/design/icons/bullet_arrow_left.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
					<td ><select name=history_page onchange="this.form.submit()">$html_pg_list</select></td>
					<td ><select name=page_size onchange="document.forms[0].submit()">$html_pgsize_list</select></td>
					<td ><button type=submit name=next value=1><img src=/design/icons/bullet_arrow_right.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
				</table>
				</td></tr>
			</tfoor>
		</table>
		</form>
	];
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub do_view_referral(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
     $service_id = 25;
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
    #
	#---------------------------------------------------
    # get parents (tree above)
	#---------------------------------------------------
	$html_tree_above = "";
    %rtree_data = ();
    $rtree_found = "";
    $rtree_id_to_check = $service_id;
    foreach $rtree_deep (1..50){
		%hash = database_select_as_hash("SELECT 1,1,parent_service_id FROM service_tree where service_id='$rtree_id_to_check' ","flag,id");
		if ( ($hash{1}{flag} eq 1) && ($hash{1}{id} ne "")  ) {
			$rtree_data{$rtree_deep} = $hash{1}{id};
			$rtree_found .= "$hash{1}{id},";
			$rtree_id_to_check = $hash{1}{id};
		} else {
			last;
		}
    }
    if ($rtree_found ne "") {
		$rtree_found = substr($rtree_found,0,-1);
		%hash = database_select_as_hash("select service.id,service.name from service where service.id in ($rtree_found)");
		foreach $rtree_deep (sort{$b <=> $a} keys %rtree_data) {
			$id = $rtree_data{$rtree_deep};
			$hash{$id} = ($hash{$id} eq "") ? "(no name $id)" : $hash{$id};
			$html_tree_above .= "$hash{$id} <a style='color:#999999' href=$my_url?action=view_referral&service_id=$id>(edit)</a> &#187; ";
		}
    }
    #
	#---------------------------------------------------
	# get all tree down
	#---------------------------------------------------
	%tree = ();
    $tree_services_ids = $service_id;
    foreach $deep (1..50){
		$sql = "
			SELECT
				service_tree.service_id,
				FIND_IN_SET('active',service_status.tags),
				FIND_IN_SET('disabled',service_status.tags),
				FIND_IN_SET('not_suspicious',service_status.tags),
				FIND_IN_SET('suspicious',service_status.tags)
			FROM
				service_tree,service,service_status
			WHERE
				service_tree.parent_service_id in ($tree_services_ids)
				and service_tree.service_id = service.id
				and service.status = service_status.id
		";
		%hash = database_select_as_hash($sql,"active,disabled,not_suspicious,suspicious");
		$tree_services_ids = "";
		foreach $id (keys %hash){
			$tree_services_ids .= "$id,";
			$tree{$deep}{services_qtd}++;
			if ($hash{$id}{active} 			> 0) {$tree{$deep}{status_active}++;}
			if ($hash{$id}{suspicious} 		> 0) {$tree{$deep}{status_suspicious}++;}
			if ($hash{$id}{not_suspicious} 	> 0) {$tree{$deep}{status_not_suspicious}++;}
			if ($hash{$id}{disabled} 		> 0) {$tree{$deep}{status_disabled}++;}

			$recharge_query = "SELECT 1,1,sum(value) as total FROM credit where credit_type <>'FREE' and service_id=".$id;
			%hash2 =  database_select_as_hash($recharge_query,"flag,total");
			$recharge = 0;
			if ($hash2{1}{flag} eq 1)  {$recharge =0+ $hash2{1}{total};  }
			if ($hash{$id}{disabled}) {
				print 'deep:'.$deep.'  ,   service id:'.$id.',recharge:'.$recharge."\n";

			}
		}
		if ($tree_services_ids ne "") {
			$tree_services_ids = substr($tree_services_ids,0,-1);
			$tree{$deep}{services_ids} = $tree_services_ids;
		} else {
			last;
		}
    }
			exit;
	#
	#---------------------------------------------------
    # collect extra data
	#---------------------------------------------------
	foreach $deep (sort{$a <=> $b} keys %tree) {
		$ids = 	$tree{$deep}{services_ids};
		if ($ids eq "") {next}
		%hash = database_select_as_hash("SELECT 1,1,sum(value) FROM service_commission where status=1 and from_service_id in ($ids) and invoice_id is null and service_id='$service_id'","flag,value");
		$tree{$deep}{commissions_ready} += ($hash{1}{flag} ne 1) ? 0 : $hash{1}{value};
		%hash = database_select_as_hash("SELECT 1,1,sum(value) FROM service_commission where status=1 and from_service_id in ($ids) and invoice_id is not null and service_id='$service_id'","flag,value");
		$tree{$deep}{commissions_payed} += ($hash{1}{flag} ne 1) ? 0 : $hash{1}{value};
		%hash = database_select_as_hash("SELECT 1,1,sum(credit),sum(value) FROM credit where service_id in ($ids) and status=1","flag,value1,value2");
		$tree{$deep}{credits_all} += ($hash{1}{flag} ne 1) ? 0 : $hash{1}{value1};
		$tree{$deep}{credits_money} += ($hash{1}{flag} ne 1) ? 0 : $hash{1}{value2};
		$tree{$deep}{credits_free} = ($tree{$deep}{credits_all} - $tree{$deep}{credits_money});
		$tree{$deep}{credits_profit} = ($tree{$deep}{credits_money}-$tree{$deep}{credits_free});
	}
	#
	#---------------------------------------------------
    # print summary table
	#---------------------------------------------------
	$html = "";
	$html_empty = "<tr><td colspan=15><center>empty...</center></td></tr>";
	%tot = ();
	foreach $deep (sort{$a <=> $b} keys %tree) {
		$html_empty = "";
		$html .= "<tr>";
		$html .= "<td class=ar>$deep</td>";
		$html .= "<td class=ar>".&format_number($tree{$deep}{services_qtd},0)."</td>";
		if ($tree{$deep}{services_qtd}>0) {
			$html .= "<td class=ar>".&format_number($tree{$deep}{status_suspicious},0)." (".&format_number((($tree{$deep}{status_suspicious}/$tree{$deep}{services_qtd})*100),0)."\%)</td>";
			$html .= "<td class=ar>".&format_number($tree{$deep}{status_not_suspicious},0)." (".&format_number((($tree{$deep}{status_not_suspicious}/$tree{$deep}{services_qtd})*100),0)."\%)</td>";
			$html .= "<td class=ar>".&format_number($tree{$deep}{status_disabled},0)." (".&format_number((($tree{$deep}{status_disabled}/$tree{$deep}{services_qtd})*100),0)."\%)</td>";
		} else {
			$html .= "<td class=ar>&nbsp;</td>";
			$html .= "<td class=ar>&nbsp;</td>";
			$html .= "<td class=ar>&nbsp;</td>";
		}
		$html .= "<td class=ar>\$".&format_number($tree{$deep}{commissions_ready},2)."</td>";
		$html .= "<td class=ar>\$".&format_number($tree{$deep}{commissions_payed},2)."</td>";
		$html .= "<td class=ar>\$".&format_number($tree{$deep}{credits_free},2)."</td>";
		$html .= "<td class=ar>\$".&format_number($tree{$deep}{credits_money},2)."</td>";
		$html .= "<td class=ar>\$".&format_number($tree{$deep}{credits_profit},2)."</td>";
		#$html .= "<td class=ar>".&format_number($tmp,0)."</td>";
		$html .= "</tr>";
		foreach $name (keys %{$tree{$deep}}) {$tot{$name} += $tree{$deep}{$name};}
	}
	$table_tree_overview_body = $html.$html_empty;
	if ($tot{services_qtd}>0) {
		$html = "<tr>";
		$html .= "<td class=ar>Total</td>";
		$html .= "<td class=ar>".&format_number($tot{services_qtd},0)."</td>";
		$html .= "<td class=ar>".&format_number($tot{status_suspicious},0)." (".&format_number((($tot{status_suspicious}/$tot{services_qtd})*100),0)."\%)</td>";
		$html .= "<td class=ar>".&format_number($tot{status_not_suspicious},0)." (".&format_number((($tot{status_not_suspicious}/$tot{services_qtd})*100),0)."\%)</td>";
		$html .= "<td class=ar>".&format_number($tot{status_disabled},0)." (".&format_number((($tot{status_disabled}/$tot{services_qtd})*100),0)."\%)</td>";
		$html .= "<td class=ar>\$".&format_number($tot{commissions_ready},2)."</td>";
		$html .= "<td class=ar>\$".&format_number($tot{commissions_payed},2)."</td>";
		$html .= "<td class=ar>\$".&format_number($tot{credits_free},2)."</td>";
		$html .= "<td class=ar>\$".&format_number($tot{credits_money},2)."</td>";
		$html .= "<td class=ar>\$".&format_number($tot{credits_profit},2)."</td>";
		$table_tree_overview_foot = $html;
	}
	#
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Service</a> &#187; Referral";
    $t{dic}{title}	= "Service referral summary";
    $t{breadcrumb}{1}{title}	= "Clients & services";
    $t{breadcrumb}{1}{url}		= "$my_url";
    $t{breadcrumb}{2}{title}	= "Search services";
    $t{breadcrumb}{2}{url}		= "$my_url?remember=1";
    $t{breadcrumb}{3}{title}	= "Service number $service_id";
    $t{breadcrumb}{3}{url}		= "$my_url?action=view&service_id=$service_id";
    $t{breadcrumb}{4}{title}	= "Referral summary";
    $t{breadcrumb}{4}{url}		= "";
    $t{dic}{content}	= qq[
	
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; onclick="sortColumn(event)">
		<thead>
			<tr>
			<td colspan=12><h1>Referral summary</h1></td>
			</tr>
			<tr>
			<td colspan=1 rowspan=2>Deep</td>
			<td colspan=4 >Referral</td>
			<td colspan=2>Commissions earned</td>
			<td colspan=3 >Credits</td>
			</tr>
			<tr>
			<td>Qtd</td>
			<td>Suspicious</td>
			<td>Good</td>
			<td>Disabled</td>
			<td>Not payed</td>
			<td>Payed</td>
			<td>Free</td>
			<td>Money</td>
			<td>Profit</td>
			</tr>
		</thead>
		<tbody>$table_tree_overview_body</tbody>
		<tfoot>$table_tree_overview_foot</tfoot>
		</table>
	
		<br>
		<fieldset>
		<legend>Service tree</legend>
			<b>Parent services: </b>$html_tree_above<br>
			<br>
			<b>Referral services</b><br>
			<form id=tree >
			<div class=tree_line_end id=$service_id><a style="padding-bottom:1px; padding-right:3px; padding-left:3px;background:#5d788c; color:#ffffff;"  href=# onclick=ClickItem('$service_id')><img src=/design/icons/user_edit.png hspace=0 vspace=0 border=0 style='margin-right:5px;' align=left><b>$data{name}</b></a> <a style='color:#999999' href=$my_url?action=view_referral&service_id=$service_id>(this service)</a></div>
			<br>
			Bulk action for selected services: 
			<button type=button onclick=tree_tag('tags_select_multiple')>Edit tags</button>
			<button type=button onclick=tree_tag('status_edit_multiple')>Edit status</button>
			</form>
		</fieldset>

	<script>
	function tree_tag(action){
		myform 					= document.forms[0];
		elementsQuantity 		= myform.elements.length;
		elementsSelectedIds 	= "";
		title					= "Edit multiple services"
		if (action == "tags_select_multiple") { title = "Edit tags for multiple services"}
		if (action == "status_edit_multiple") { title = "Edit status for multiple services"}
		elementsSelectedQuantity= 0;
		for (i=0; i<elementsQuantity; i++){
			if (myform.elements[i].type=="checkbox"){
				if (myform.elements[i].checked){
					elementsSelectedIds = elementsSelectedIds+myform.elements[i].name+",";
					elementsSelectedQuantity++;
				}
			}
		}
		if (elementsSelectedQuantity > 0) {
			modal_open(
			title,
			"$my_url?action="+action+"&service_ids="+elementsSelectedIds,
			400,
			300
			);
		} else {
			alert("Plaese select one or more services");
		}
	}
	function ClickItem(div_clicked_id){
		div_clicked_id = ""+div_clicked_id;
		var div_clicked = document.getElementById(div_clicked_id);
		if (div_clicked.childNodes.length>3) {
			if ( (div_clicked.lastChild.style.display == "") || (div_clicked.lastChild.style.display == "block") ) {
				if (div_clicked.className == "tree_minus") {div_clicked.className="tree_plus"}
				if (div_clicked.className == "tree_minus_end") {div_clicked.className="tree_plus_end"}
				div_clicked.lastChild.style.display = "none"
			} else {
				if (div_clicked.className == "tree_plus") {div_clicked.className="tree_minus"}
				if (div_clicked.className == "tree_plus_end") {div_clicked.className="tree_minus_end"}
				div_clicked.lastChild.style.display = "block"
			}
		} else {
			if (div_clicked.className == "tree_plus") {div_clicked.className="tree_minus"}
			if (div_clicked.className == "tree_plus_end") {div_clicked.className="tree_minus_end"}
			var new_div_iframe = document.createElement('div');
			new_div_iframe.setAttribute('class',"tree_iframe");
			new_div_iframe.className = "tree_iframe";
			new_div_iframe.innerHTML = "<iframe style='display:none' src='$my_url?action=view_tree_js&id="+div_clicked_id+"'>";
			var new_div_box = document.createElement('div');
			new_div_box.setAttribute('id',div_clicked_id+"_box");
			new_div_box.setAttribute('class',"tree_box");
			new_div_box.className = "tree_box";
			new_div_box.innerHTML = "<div style='padding-top:5px; padding-bottom:10px;'><img src=/design/img/loading.gif align=left>Loading...</div>";
			div_clicked.appendChild(new_div_iframe);
			div_clicked.appendChild(new_div_box);
		}
	}
	function ContainerClean(container_div_id){
		container_div_id = ""+container_div_id;
		var div_obj = document.getElementById(container_div_id);
		div_obj.innerHTML = "";
	}
	function ContainerAppend(container_div_id,new_div_id,new_div_html,new_div_class){
		container_div_id = ""+container_div_id;
		new_div_id = ""+new_div_id;
		var container_div_obj = document.getElementById(container_div_id);
		new_div_item = document.createElement('div');
		new_div_item.setAttribute('id',new_div_id);
		new_div_item.setAttribute('class',new_div_class);
		new_div_item.className = new_div_class;
		new_div_item.innerHTML = new_div_html;
		container_div_obj.appendChild(new_div_item);
	}
	</script>
	<script>
	//ClickItem('$service_id');
	</script>


	];
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub do_view_commissions(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
	#
	#---------------------------------------------------
	# get commissoes values
	#---------------------------------------------------
    %hash = database_select_as_hash("SELECT 1,count(*),sum(value) FROM service_commission WHERE service_id = '$service_id' and status=1 and invoice_id is null ","qtd,value");
	$data{commission_total_value} = format_number($hash{1}{value},2);
    %hash = database_select_as_hash("SELECT 1,count(*),sum(value) FROM service_commission WHERE service_id = '$service_id' and status=1 and invoice_id is null and now()<activation_date_1 and now()<activation_date_2 ","qtd,value");
	$data{commission_slice_0_value} = format_number($hash{1}{value},2);
    %hash = database_select_as_hash("SELECT 1,count(*),sum(value) FROM service_commission WHERE service_id = '$service_id' and status=1 and invoice_id is null and now()>=activation_date_1  ","qtd,value");
	$data{commission_slice_1_value} = format_number($hash{1}{value},2);
    %hash = database_select_as_hash("SELECT 1,count(*),sum(value) FROM service_commission WHERE service_id = '$service_id' and status=1 and invoice_id is null and now()>=activation_date_2 ","qtd,value");
	$data{commission_slice_2_value} = format_number($hash{1}{value},2);
    %hash = database_select_as_hash("SELECT 1,count(*),sum(value) FROM service_commission WHERE service_id = '$service_id' and status=1 and invoice_id is not null ","qtd,value");
	$data{commission_used} = format_number($hash{1}{value},2);
	#
	#------------------------
	# filter to sql
	#------------------------
	$filter_sql = "";
	$filter_sql = ($form{filter} eq 0) ? " and invoice_id is null and now()<activation_date_1 and now()<activation_date_2 " : $filter_sql;
	$filter_sql = ($form{filter} eq 1) ? " and invoice_id is null and now()>=activation_date_1 " : $filter_sql;
	$filter_sql = ($form{filter} eq 2) ? " and invoice_id is null and now()>=activation_date_2 " : $filter_sql;
	$filter_sql = ($form{filter} eq 3) ? " and invoice_id is null and (now()>=activation_date_1 or now()>=activation_date_2) " : $filter_sql;
	#$filter_sql = ($form{filter} eq 4) ? " and invoice_id is not null and credit_id is not null " : $filter_sql;
	#$filter_sql = ($form{filter} eq 5) ? " and invoice_id is not null and credit_id is null " : $filter_sql;
	$filter_sql = ($form{filter} eq 6) ? " and invoice_id is not null " : $filter_sql;
	$filter_sql = ($form{filter} eq 7) ? " and invoice_id is null " : $filter_sql;
	if (substr($form{filter},0,1) eq "i") {
		$tmp = clean_int(substr($form{filter},1,100));
		if ( ($tmp ne "") && ($tmp eq substr($form{filter},1,100)) ) {
			$filter_sql = " and invoice_id = '$tmp' "  ;
		}
	}
	#
	#------------------------
	# monta o select inicio
	#------------------------
	$t{dic}{"filter_select"} = "<option>&#187; Show all commission history</option>";
	$t{dic}{"filter_select"} .= "<option>&nbsp;</option>";
	$t{dic}{"filter_select"} .= "<option>By commission status</option>";
	$tmp = ($form{filter} eq 0) ? "selected": "";$t{dic}{filter_select} .= "<option value=0 $tmp>&nbsp;&nbsp;&#187; New commissions not usable yet</option>";
	$tmp = ($form{filter} eq 1) ? "selected": "";$t{dic}{filter_select} .= "<option value=1 $tmp>&nbsp;&nbsp;&#187; Commissions transferable for phone credit only</option>";
	$tmp = ($form{filter} eq 2) ? "selected": "";$t{dic}{filter_select} .= "<option value=2 $tmp>&nbsp;&nbsp;&#187; Commissions that can be exchanged for cash</option>";
	$tmp = ($form{filter} eq 3) ? "selected": "";$t{dic}{filter_select} .= "<option value=3 $tmp>&nbsp;&nbsp;&#187; Commissions that can be exchanged for cash or phone credit</option>";
	$tmp = ($form{filter} eq 7) ? "selected": "";$t{dic}{filter_select} .= "<option value=7 $tmp>&nbsp;&nbsp;&#187; All unused commissions.</option>";
	$tmp = ($form{filter} eq 6) ? "selected": "";$t{dic}{filter_select} .= "<option value=6 $tmp>&nbsp;&nbsp;&#187; Credited commissions</option>";
	$t{dic}{"filter_select"} .= "<option>&nbsp;</option>";
	#
	#------------------------
	# monta o select invoices
	#------------------------
    $sql = "
		SELECT id,unix_timestamp(creation_date),credit_id,send_to,status,value 
		FROM service_commission_invoice 
		WHERE service_id='$service_id' 
		order by id desc
		limit 0,2000
	    ";
    %hash = database_select_as_hash($sql,"date,credit_id,type,status,value");
    $tmp = "";
    foreach $id (sort{$hash{$b}{date} <=> $hash{$a}{date}} keys %hash) {
		$value = &format_number($hash{$id}{value},2);
		if ($hash{$id}{type} eq "CREDIT") {
			$text = "Phone credit requested";
			$text = ($hash{$id}{status} eq 1) ? "Credit as phone credit" : $text;
			$text = (($hash{$id}{status} eq 1) && ($hash{$id}{credit_id} eq "")) ? "Phone credit failed" : $text;
			$text = ($hash{$id}{status} eq -1) ? "Phone credit rejected" : $text;
			$value= ($hash{$id}{status} >= 0) ? $value : ""; 
		} elsif ($hash{$id}{type} eq "CHECK") {
			$text = "exchanged for cash requested";
			$text = ($hash{$id}{status} eq 1) ? "exchanged for cash" : $text;
			$text = ($hash{$id}{status} eq -1) ? "exchanged for cash rejected" : $text;
			$value= ($hash{$id}{status} >= 0) ? $value : ""; 
		} else {
			next;
		}
		$date = &format_time_time($hash{$id}{date});
		$tmp1 = ($form{filter} eq "i$id") ? "selected": "";
	    $tmp .= "<option value=i$id $tmp1>&nbsp;&nbsp;&#187; $id - $date - $text - \$$value</option>";
    }
	if ($tmp ne "") {
		$t{dic}{"filter_select"} .= "<option>By credit type</option>";
		$t{dic}{"filter_select"} .= $tmp;
		$t{dic}{"filter_select"} .= "<option>&nbsp;</option>";
	}
	#
	#------------------------
	# pega total
	#------------------------
	%hash = database_select_as_hash("SELECT 1,1,count(*),sum(value) FROM service_commission where service_id='$service_id' $filter_sql ","flag,qtd,value");
	$quantity 	= ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd}>0) ) ? $hash{1}{qtd} : 0;
	$value		= ( ($hash{1}{flag} eq 1) && ($hash{1}{value}>0) ) ? $hash{1}{value} : 0;
	$t{dic}{total_qtd} 		= &format_number($quantity,0);
	$t{dic}{total_value} 	= &format_number($value,2);
	#
	#------------------------	
	# separa por paginacao
	#------------------------
	$page_size	= 12;
	$page_min	= 1;
	$page_max	= int(($quantity-1)/$page_size)+1;
	$page_max	= ($page_max<$page_min) ? $page_min : $page_max;
	$page 		= clean_int($form{page});
	$page 		= ($form{next} eq 1) ? $page+1 : $page;
	$page 		= ($form{previous} eq 1) ? $page-1 : $page;
	$page 		= ($page<$page_min) ? $page_min : $page;
	$page 		= ($page>$page_max) ? $page_max : $page;
	$sql_limit	= ($page-1)*$page_size;
	#
	#------------------------	
	# monta query
	#------------------------
	$sql = "
	SELECT
		unix_timestamp(creation_date),unix_timestamp(activation_date_1),unix_timestamp(activation_date_2),
		id,status,from_service_id,credit_id,deep,value,invoice_id,title,type,engine
	FROM service_commission 
	where service_id='$service_id' $filter_sql 
	order by  invoice_id,creation_date desc
	limit $sql_limit,$page_size
	";
	%hash = database_select_as_hash_with_auto_key($sql, "creation_date,date_1,date_2,id,status,from_service_id,credit_id,deep,value,invoice_id,title,type,engine");
	#
	#------------------------	
	# monta os selecionados
	#------------------------
	%from_services = ();
	$html_empty = "<tr><td colspan=8><center>Empty...</center></td></tr>";
	foreach $index (sort{$a <=> $b} keys %hash) {
		$html_empty = "";
		$date = &format_time_time($hash{$index}{creation_date});
		$value = &format_number($hash{$index}{value},2);
		$status = "Unknown";
		if ( ($hash{$index}{invoice_id} ne "") ) {
			$status = "Credited (invoice $hash{$index}{invoice_id})";
		} else {
			$flag_1 = (time>=$hash{$index}{date_1}) ? 1 : 0;
			$flag_2 = (time>=$hash{$index}{date_2}) ? 1 : 0;
			if 		($flag_1.$flag_2 eq "00") {$status = "New not usable yet"}
			elsif 	($flag_1.$flag_2 eq "01") {$status = "Transferable for phone credit only"}
			elsif 	($flag_1.$flag_2 eq "10") {$status = "Can be exchanged for cash"}
			elsif 	($flag_1.$flag_2 eq "11") {$status = "Can be exchanged for cash or phone credit"}
		}
		#
		$type = "$hash{$index}{engine}";
		$type = ($hash{$index}{type} eq "CREDIT"	) ? "Referral recharge" : $type;
		$type = ($hash{$index}{type} eq "MANUAL"	) ? "Manual by customer serice" : $type;
		$type = ($hash{$index}{type} eq "NEWF"		) ? "New referral sign-in" : $type;
		$type = ($hash{$index}{type} eq "NEWFCALL"	) ? "Referral first call" : $type;
		$type = ($hash{$index}{title} ne "") ? $hash{$index}{title} : $type;
		#
		$name = "&nbsp;";
		$distance = "&nbsp;";
		if ($hash{$index}{from_service_id} ne "") {
			$distance = ($hash{$index}{deep}-1)." people away";
			$distance = ($hash{$index}{deep} eq 1) ? "Friend" : $distance;
			$distance = ($hash{$index}{deep} eq 2) ? "Friend of friend" : $distance;
			if (exists($from_services{$hash{$index}{from_service_id}})) {
				$name = $from_services{$hash{$index}{from_service_id}};
			} else {
				%hash2 = database_select_as_hash("SELECT 1,1,name from service where id='$hash{$index}{from_service_id}' ","flag,value");
				$name = ($hash2{1}{flag} eq 1) ? $hash2{1}{value} : $name;
			}
		}
		$url = "<a href=\"$my_url?action=detail_commission&commission_id=$hash{$index}{id}\"	onClick=\"modal_open('View commission','$my_url?action=detail_commission&commission_id=$hash{$index}{id}',600,400); return false;\" >";
		#
		$t{dic}{table} .= "
		<tr>
		<td>$url$date</a></td>
		<td>$url$type</a></td>
		<td class=ar>$url\$$value</a></td>
		<td>$url$name</a></td>
		<td>$url$distance</a></td>
		<td>$url$status</a></td>
		</tr>
		";
	}
	$t{dic}{table} .= $html_empty;
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
	$t{dic}{select_pages} = "";
	$tmp1 = &format_number($page_max,0);
	foreach($page_min..$page_max) {
		$tmp = ($_ eq $page) ? "selected" : ""; 
		$t{dic}{select_pages} .= "<option $tmp value=$_>Page: ". &format_number($_,0). " of $tmp1</option>";
	}
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Service</a> &#187; Commissions";
    $t{dic}{title}	= "Service commissions";
    $t{breadcrumb}{1}{title}	= "Clients & services";
    $t{breadcrumb}{1}{url}		= "$my_url";
    $t{breadcrumb}{2}{title}	= "Search services";
    $t{breadcrumb}{2}{url}		= "$my_url?remember=1";
    $t{breadcrumb}{3}{title}	= "Service number $service_id";
    $t{breadcrumb}{3}{url}		= "$my_url?action=view&service_id=$service_id";
    $t{breadcrumb}{4}{title}	= "Commissions";
    $t{breadcrumb}{4}{url}		= "";
    $t{dic}{content}	= qq[
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 width=100%><tr>
			<td width=20% 	style=padding-right:10px;>Not ready:<br><div class=dataset_text 		><div>\$$data{commission_slice_0_value}</div></div></td>
			<td 			style=padding-right:10px;>+</td>
			<td width=20% 	style=padding-right:10px;>Ready to recharge:<br><div class=dataset_text ><div>\$$data{commission_slice_1_value}</div></div></td>
			<td 			style=padding-right:10px;>+</td>
			<td width=20% 	style=padding-right:10px;>Ready to pay:<br><div class=dataset_text 		><div>\$$data{commission_slice_2_value}</div></div></td>
			<td 			style=padding-right:10px;>=</td>
			<td width=20% 	style="padding-right:10px;border-right:1px solid #c0c0c0;">Total:<br><div class=dataset_text 	><div><a style="background-image:url(/design/icons/add.png);" href="$my_url?action=commission_add&service_id=$service_id" onClick="modal_open('Add commission','$my_url?action=commission_add&service_id=$service_id',300,420); return false;"></a>\$$data{commission_total_value}</div></div></td>
			<td width=20% 	style=padding-left:10px;>Used:<br><div class=dataset_text 	><div>\$$data{commission_used}</div></div></td>
		</tr></table>


		<form action=$my_url>
		<input type=hidden name=action value=view_commissions>
		<input type=hidden name=service_id value=$service_id>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; xxonclick="sortColumn(event)">
			<thead>
				<tr>
				<td class=al colspan=3><h1>Commissions</h2>Total \$$t{dic}{total_value} in $t{dic}{total_qtd} commissions </td>
				<td class=al colspan=2>From</td>
				<td class=al rowspan=2 style="width:160px;">Status</td>
				</tr>
				<tr>
				<td class=al >Date</td>
				<td class=al style="border-left:0px;">Type</td>
				<td class=al style="border-left:0px;">Value</td>
				<td class=al >Name</td>
				<td class=al style="border-left:0px;">Distance</td>
				</tr>
			</thead>
			<tbody > 
			$t{dic}{table}
			</tbody>
			<tfoot>
				<tr><td colspan=8 style=border:0px><h1>
				<button style="float:left;" type=submit name=previous value=1><img src=/design/icons/bullet_arrow_left.png hspace=0 vspace=0 border=0 width=16 height=16></button>
				<select style="float:left;" name=filter onchange="this.form.submit()">$t{dic}{"filter_select"}</select>
				<select style="float:left;" name=page onchange="this.form.submit()">$t{dic}{select_pages}</select>
				<button style="float:left;" type=submit name=next value=1><img src=/design/icons/bullet_arrow_right.png hspace=0 vspace=0 border=0 width=16 height=16></button>
				&nbsp;&nbsp;
				</h1></td></tr>
			</tfoor>
		</table>
		</form>

	];
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub do_view_history(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
    #
	#---------------------------------------------------
    # pega ids de calls
	#---------------------------------------------------
	%hash = database_select_as_hash("SELECT id,unix_timestamp(datetime_start) FROM calls_log where service_id='$service_id' and datetime_stop is not null ");
	foreach (keys %hash) {$collected_ids{substr("000000000000000000".$hash{$_},-15,15).substr("000000000000000000".$_,-15,15)."0"}++;}
    #
	#---------------------------------------------------
    # pega ids de acoes
	#---------------------------------------------------
	%hash = database_select_as_hash("SELECT id,unix_timestamp(date) FROM action_log where service_id='$service_id' ");
	foreach (keys %hash) {$collected_ids{substr("000000000000000000".$hash{$_},-15,15).substr("000000000000000000".$_,-15,15)."1"}++;}

#%t = ();
#$t{dic}{my_url}	= $my_url;
#$t{dic}{title}	= "<a href=$my_url?remember=1>Services</a> &#187; Service actions";
#foreach (sort{$b <=> $a} keys %collected_ids) {$t{dic}{content} .= qq[$_<br>];}
#$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
#&template_print("template.html",%t);


	#
	#---------------------------------------------------
	# calcula paginas
	#---------------------------------------------------
	$quantity 		= keys %collected_ids;
	$page_size		= clean_int($form{page_size});
	$page_size		= ($page_size eq "") ? 15 : $page_size;
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
	@selected_ids	= (sort{$b <=> $a} keys %collected_ids)[$selected_start..$selected_stop];
    #
	#---------------------------------------------------
    # pega dados de calls
	#---------------------------------------------------
	%calls_data = ();
	$calls_ids = "";
	foreach (@selected_ids) {
		if (substr($_,30,1) eq "0") {
			$tmp = substr($_,15,15);
			$tmp++;$tmp--;
			$calls_ids .= "$tmp,";
		}
	}
	if ($calls_ids ne "") {
		$calls_ids = substr($calls_ids,0,-1);
		$sql = "
		SELECT id,ani,did,dst,billing_id,error_id,info_id
		FROM calls_log where id in ($calls_ids) 
		limit 0,1000
		";
		%calls_data = database_select_as_hash($sql,"ani,did,dst,billing_id,error_id,info_id");
	}
    #
	#---------------------------------------------------
    # pega dados de actions
	#---------------------------------------------------
	%logs_data = ();
	$logs_ids = "";
	foreach (@selected_ids) {
		if (substr($_,30,1) eq "1") {
			$tmp = substr($_,15,15);
			$tmp++;$tmp--;
			$logs_ids .= "$tmp,";
		}
	}
	if ($logs_ids ne "") {
		$logs_ids = substr($logs_ids,0,-1);
		$sql = "
		select
		action_log.id,action_log.adm_user_id,action_log.value_old, action_log.value_new,
		action_log_type.group,action_log_type.title,action_log_type.description
		from action_log,action_log_type 
		where action_log.type=action_log_type.id and action_log.id in ($logs_ids)
		limit 0,1000
		";
		%logs_data = database_select_as_hash($sql,"noc_id,value_old,value_new,group,title,description");
	}
	#%data_logs = ();
	#$tmp = "";
	#foreach (@selected_ids) {if (substr($_,0,1) eq "L") {$tmp .= substr($_,1,100).",";} }
	#if ($tmp ne "") { %data_logs = &action_history_get_info(substr($tmp,0,-1),"no_date,no_user"); }
	#
	#---------------------------------------------------
	# monta o html
	#---------------------------------------------------
	%calls_log_info = database_select_as_hash("select id,value from calls_log_info ");
	%adm_users = database_select_as_hash("SELECT id,concat(name,' (',web_user,')') FROM adm_users LIMIT 0,1000");
	$line_timestamp = "";
	$line_style_1 = " ";
	$line_style_2 = " ";
	$line_style_top = "border-top:1px solid #c0c0c0; border-bottom:0px;";
	$line_style_not_top = "border-top:0px; border-bottom:0px; ";
	foreach $id_brute (@selected_ids) {
		if ($id_brute eq "") {next}
		$id_type 	= substr($id_brute,30,1);
		$id 		= substr($id_brute,15,15); $id++;$id--;
		$timestamp 	= substr($id_brute,0,15); $timestamp++;$timestamp--;
		#
		# LINE STYLE
		$line_timestamp = ($line_timestamp eq "") ? $timestamp : $line_timestamp;
		$line_gap = $timestamp-$line_timestamp;
		$tmp = $line_style_not_top;
		if (($line_gap>30) || ($line_gap<-30)) {
			$tmp = $line_style_1;
			$line_style_1 = $line_style_2;
			$line_style_2 = $tmp;
			$tmp = $line_style_top;
		}
		$line_style = $tmp.$line_style_1;
		$line_timestamp = $timestamp;
		#
		# global itens
		$html_history .= "<tr>";
		$html_history .= "<td valign=top style='$line_style white-space:nowrap;' >".&format_time_gap($timestamp)."</td>";
		#
		# calls detail
		if ($id_type eq "0") {
			if (exists($calls_data{$id})) {
#%calls_data = database_select_as_hash($sql,"ani,did,dst,billing_id,error_id,info_id");
				if ($calls_data{$id}{billing_id} eq "") {
					$html_history .= "<td style='$line_style' valign=top><img src=/design/icons/phone_delete.png hspace=0 vspace=0 align=left>&nbsp;Call not billed</td>";
				} else {
					$html_history .= "<td style='$line_style' valign=top><img src=/design/icons/phone.png hspace=0 vspace=0 align=left>&nbsp;Call OK</td>";
				}
				$html_history .= "<td style='$line_style' valign=top>";
				$html_history .= "<a href=\"$my_url?action=detail_call&call_log_id=$id\"	onClick=\"modal_open('Call debug','$my_url?action=detail_call&call_log_id=$id',600,400); return false;\" >";
				$html_history .= "Forward to ".&format_E164_number($calls_data{$id}{dst},"USA")."</td>";
				$html_history .= "<td style='$line_style' valign=top>&nbsp;</td>";
			} else {
				$html_history .= "<td style='$line_style' colspan=3><font color=#c0c0c0>(Unable to read call action id=$id)</font></td>";
			}
		}
		#
		# calls detail
		elsif ($id_type eq "1") {
#%logs_data = database_select_as_hash($sql,"noc_id,value_old,value_new,group,title,description");
			if (exists($logs_data{$id})) {
				$tmp = "application_go.png";
				$tmp = ($logs_data{$id}{group} eq "Coupons") 		? "coupon.png" : $tmp;
				$tmp = ($logs_data{$id}{group} eq "Suspicious") 	? "02-35.png" : $tmp;
				$tmp = ($logs_data{$id}{group} eq "NOC action") 	? "user_gray.png" : $tmp;
				$tmp = ($logs_data{$id}{group} eq "Security") 		? "01-50.png" : $tmp;
				$tmp = ($logs_data{$id}{group} eq "Service action")	? "user.png" : $tmp;
				$tmp = ($logs_data{$id}{group} eq "Billing") 		? "money.png" : $tmp;
				$html_history .= "<td style='$line_style white-space:nowrap;'><img src=/design/icons/$tmp hspace=0 vspace=0 align=left>&nbsp;$logs_data{$id}{group}</td>";
				if ($logs_data{$id}{description} eq "") {
					$tmp = "";
					$tmp .= ($logs_data{$id}{value_old} ne "") ? "old=$logs_data{$id}{value_old} " : "";
					$tmp .= ($logs_data{$id}{value_new} ne "") ? "new=$logs_data{$id}{value_new} " : "";
					$tmp = ($tmp eq "") ? "" : " ($tmp)";
					$html_history .= "<td style='$line_style'>$logs_data{$id}{title}$tmp</td>";
				} else {
					$tmp = $logs_data{$id}{description};
					$tmp1="#1"; $tmp2=$logs_data{$id}{value_old}; $tmp =~ s/$tmp1/$tmp2/eg; 
					$tmp1="#2"; $tmp2=$logs_data{$id}{value_new}; $tmp =~ s/$tmp1/$tmp2/eg; 
					$html_history .= "<td style='$line_style'>$tmp</td>";
				}
				$tmp = (exists($adm_users{$logs_data{$id}{noc_id}})) ? $adm_users{$logs_data{$id}{noc_id}} : "&nbsp;";
				$html_history .= "<td style='$line_style white-space:nowrap;'>$tmp</td>";
			} else {
				$html_history .= "<td style='$line_style' colspan=3><font color=#c0c0c0>(Unable to read log type=type=$id_type id=$id)</font></td>";
			}
		}
		#
		# error detail
		else {
			$html_history .= "<td style='$line_style' colspan=3><font color=#c0c0c0>(Unable to read log type=$id_type id=$id_brute)</font></td>";
		}
		$html_history .= "</tr>";
	}
    #
	#---------------------------------------------------
    # imprime pagina
	#---------------------------------------------------
	$html_pg_list = "";
	foreach($page_min..$page_max) {
		$tmp = ($_ eq $page) ? "selected" : ""; 
		$html_pg_list .= "<option $tmp value=$_>Page: $_ of $page_max</option>";
	}
	$html_pgsize_list = "";
	$tmp = (15 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=15>15 itens per page</option>";
	$tmp = (50 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=50>50 itens per page</option>";
	$tmp = (500 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=500>500 itens per page</option>";
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Service</a> &#187; Calls and actions";
    $t{dic}{title}	= "Service calls and actions";
    $t{breadcrumb}{1}{title}	= "Clients & services";
    $t{breadcrumb}{1}{url}		= "$my_url";
    $t{breadcrumb}{2}{title}	= "Search services";
    $t{breadcrumb}{2}{url}		= "$my_url?remember=1";
    $t{breadcrumb}{3}{title}	= "Service number $service_id";
    $t{breadcrumb}{3}{url}		= "$my_url?action=view&service_id=$service_id";
    $t{breadcrumb}{4}{title}	= "Calls and actions";
    $t{breadcrumb}{4}{url}		= "";
    $t{dic}{content}	= qq[
			<form action=$my_url>
			<input type=hidden name=action value=view_history>
			<input type=hidden name=service_id value=$service_id>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; xonclick="sortColumn(event)">
				<thead>
					<tr>
					<td colspan=4><h1>Calls and actions</h1></td>
					</tr>
					<tr>
					<td width=80>Date</td>
					<td width=100>Type</td>
					<td >Action</td>
					<td width=100>NOC user</td>
					</tr>
				</thead>
				<tbody >
					$html_history 
					$html_history_empty
				</tbody>
				<tfoot>
					<tr><td colspan=8 >
					<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
						<td ><button type=submit name=previous value=1><img src=/design/icons/bullet_arrow_left.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
						<td ><select name=history_page onchange="this.form.submit()">$html_pg_list</select></td>
						<td ><select name=page_size onchange="document.forms[0].submit()">$html_pgsize_list</select></td>
						<td ><button type=submit name=next value=1><img src=/design/icons/bullet_arrow_right.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
					</table>
					</td></tr>
				</tfoor>
			</table>
			</form>
    ];
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub do_view_coupons(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
    #
	#---------------------------------------------------
	# get all coupons
	#---------------------------------------------------
	$sql = "
	SELECT 
	service_coupon_stock.id,
	service_coupon_type.title,
	service_coupon_stock_status.title,
	unix_timestamp(service_coupon_stock.slice_timestamp)
	FROM 
	service_coupon_stock, service_coupon_stock_status, service_coupon_type
	where 
	service_coupon_stock.service_id='$service_id'
	and service_coupon_stock.status = service_coupon_stock_status.id
	and service_coupon_stock.coupon_type_id = service_coupon_type.id
	";
	%hash = &database_select_as_hash($sql,"title,status,date");
	$html = "";
	$html_empty = "<tr><td colspan=8><center>Empty...</center></td></tr>";
	foreach $id (sort{$b <=> $a} keys %hash) {
		$html_empty = "";
		$url = "<a href=\"$my_url?action=detail_coupon&coupon_id=$id\"	onClick=\"modal_open('View coupon','$my_url?action=detail_coupon&coupon_id=$id',400,300); return false;\" >";
		$html .= "<tr>";
		$html .= "<td>$url$hash{$id}{title}</a></td>";
		$html .= "<td style='white-space:nowrap;'>$url$hash{$id}{status}</a></td>";
		$html .= "<td style='white-space:nowrap;'>$url". &format_time_gap($hash{$id}{date}) ."</a></td>";
		$html .= "</tr>";
	}
	$html_coupons = $html.$html_empty;
    #
	#---------------------------------------------------
	# get selected cc profile
	#---------------------------------------------------
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Service</a> &#187; Promotion coupons";
    $t{dic}{title}	= "Service promotion and coupons";
    $t{breadcrumb}{1}{title}	= "Clients & services";
    $t{breadcrumb}{1}{url}		= "$my_url";
    $t{breadcrumb}{2}{title}	= "Search services";
    $t{breadcrumb}{2}{url}		= "$my_url?remember=1";
    $t{breadcrumb}{3}{title}	= "Service number $service_id";
    $t{breadcrumb}{3}{url}		= "$my_url?action=view&service_id=$service_id";
    $t{breadcrumb}{4}{title}	= "Promotion and coupons";
    $t{breadcrumb}{4}{url}		= "";
    
    $t{dic}{content}	= qq[
		
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; xonclick="sortColumn(event)">
				<thead>
					<tr>
					<td colspan=5><h1>Coupons</h1></td>
					</tr>
					<tr>
					<td >Name</td>
					<td width=100>Status</td>
					<td width=80>Last action</td>
					</tr>
				</thead>
				<tbody >
					$html_coupons
				</tbody>
			</table>
	];
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub do_view_ccprofile(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
    #
	#---------------------------------------------------
	# get all cc profiles
	#---------------------------------------------------
	$sql = "
	SELECT 
	id,unix_timestamp(creation_date),
	active,is_auto_recharge,cc_error,
	cc_type,cc_fingerprint,cc_number,first_name,last_name,ani
	FROM service_profile_cc 
	where service_id='$service_id' 
	";
	%profiles = &database_select_as_hash($sql,"date,active,is_auto_recharge,cc_error,cc_type,cc_fingerprint,cc_number,first_name,last_name,ani");
	$html = "";
	$html_empty = "<tr><td colspan=8><center>Empty...</center></td></tr>";
	foreach $id (sort{$b <=> $a} keys %profiles) {
		$html_empty = "";
		$status = "UNKNOWN";
		$status = ($profiles{$id}{active} eq 1) ? "Active, pay as you go" : $status;
		$status = ($profiles{$id}{is_auto_recharge} eq 1) ? "Active, auto recharge" : $status;
		$status = ($profiles{$id}{cc_error} eq 1) ? "Active but error" : $status;
		$status = ($profiles{$id}{active} ne 1) ? "Deleted" : $status;
		$url = "<a href=\"$my_url?action=detail_ccprofile&ccprofile_id=$id\"	onClick=\"modal_open('View credit card profile','$my_url?action=detail_ccprofile&ccprofile_id=$id',350,300); return false;\" >";

		$html .= "<tr>";
		$html .= "<td style='white-space:nowrap;'>$url". &format_time_gap($profiles{$id}{date}) ."</a></td>";
		$html .= "<td style='white-space:nowrap;'>$url$status</a></td>";
		$html .= "<td>$url$profiles{$id}{cc_type}</a></td>";
		$html .= "<td>$url$profiles{$id}{cc_number}</a></td>";
		$html .= "<td>$url$profiles{$id}{first_name} $profiles{$id}{last_name}</a></td>";
		$html .= "</tr>";
	}
	$html_cc_profiles = $html.$html_empty;
    #
	#---------------------------------------------------
	# get selected cc profile
	#---------------------------------------------------
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Service</a> &#187; Credit card profile";
    $t{dic}{title}	= "Service credit card profile";
    $t{breadcrumb}{1}{title}	= "Clients & services";
    $t{breadcrumb}{1}{url}		= "$my_url";
    $t{breadcrumb}{2}{title}	= "Search services";
    $t{breadcrumb}{2}{url}		= "$my_url?remember=1";
    $t{breadcrumb}{3}{title}	= "Service number $service_id";
    $t{breadcrumb}{3}{url}		= "$my_url?action=view&service_id=$service_id";
    $t{breadcrumb}{4}{title}	= "Credit card profile";
    $t{breadcrumb}{4}{url}		= "";
    $t{dic}{content}	= qq[
		
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; xonclick="sortColumn(event)">
				<thead>
					<tr>
					<td colspan=5><h1>Credit card profile hystory</h1></td>
					</tr>
					<tr>
					<td rowspan=2 width=80>Date</td>
					<td rowspan=2 width=100>Status</td>
					<td colspan=3 >Credit card</td>
					</tr>
					<tr>
					<td >Type</td>
					<td >Number</td>
					<td >Name</td>
					</tr>
				</thead>
				<tbody >
					$html_cc_profiles 
				</tbody>
			</table>

		
	];
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub do_view_empty(){
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($form{service_id},0,100));
	%data = &view_support_get_service_data($service_id);
    if ($data{found} ne 1) {&do_search();return}
	%t = ();
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Service</a> &#187; Not finished";
    $t{dic}{content}	= qq[<br>This action is not finished yet :(];
	$t{dic}{content} = &view_support_build_html_page($t{dic}{content},%data);
    &template_print("template.html",%t);
}
sub view_support_build_html_page(){
	local ($html,%service_data) = @_;
    $html = qq[
	<div class=clear style="width:210px; float:left;">
		<fieldset style="padding:10px;xpadding-top:0px;font-size:11px;line-height:120%;">
			<div class=clear style=float:right><a target=_blank href=services.cgi?action=view_login&service_id=$service_data{id}>[Log-in]</a></div>
			<h2>ID:$service_data{id}</h2>
			<b>Balance: </b>\$$service_data{credit}<br>
			<b>Status: </b>$service_data{status}<br>
			<b>Name: </b>$service_data{name}<br>
			<b>Email: </b>$service_data{email}<br>
			<br>
			<button onclick="window.location='$my_url?service_id=$service_data{id}&action=view_overview'" 		class=button style="width:100%">Overview</button><br>
			<button onclick="window.location='$my_url?service_id=$service_data{id}&action=view_history'" 		class=button style="width:100%">Calls and actions</button><br>
			<button onclick="window.location='$my_url?service_id=$service_data{id}&action=view_referral'" 		class=button style="width:100%">Referral</button><br>
			<button onclick="window.location='$my_url?service_id=$service_data{id}&action=view_commissions'" 	class=button style="width:100%">Commissions</button><br>
			<button onclick="window.location='$my_url?service_id=$service_data{id}&action=view_credits'" 		class=button style="width:100%">Phone credits</button><br>
			<button onclick="window.location='$my_url?service_id=$service_data{id}&action=view_coupons'" 		class=button style="width:100%">Promotion coupons</button><br>
			<button onclick="window.location='$my_url?service_id=$service_data{id}&action=view_ccprofile'" 		class=button style="width:100%">Credit card profile</button><br>
		</fieldset>
	</div>
	<div class=clear style="margin-left:230px;">
		$html
	</div>
	];
	return $html;
}
sub view_support_get_service_data(){
    #
	#---------------------------------------------------
    # start
	#---------------------------------------------------
	local ($service_id) = @_;
	local (%data,%hash);
	$data{found} = 0;
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
    $service_id = clean_int(substr($service_id,0,100));
	$data{id} = $service_id;
    $sql = "
	select
	    1,1,
	    service.name,
	    service.email,
	    unix_timestamp(service.creation_date),
	    service.balance,
	    service.limit,
	    service.age_id,
	    service.age_is_manual, 
	    service_status.id,service_status.name,
		service_pin.pin,
		service_invite.id		
	from
		service,
		service_status,
		service_pin,
		service_invite
	where
		service.id='$service_id' and
		service.id = service_pin.service_id and 
		service.id = service_invite.service_id and 
		service.status=service_status.id 
    ";
	if ($service_id ne "") {
		%hash = database_select_as_hash($sql,"flag,name,email,date,balance,limit,age_id,age_is_manual, status_id,status,pin,invite");
		if ($hash{1}{flag} eq 1) {
			foreach(keys %{$hash{1}}) {$data{$_} = $hash{1}{$_}; }
			$data{date} 	= format_time_time($data{date});
			$data{name} 	= ($data{name} eq "") ? "(no name $service_id)" : $data{name};
			$data{credit}	= format_number($data{balance}-$data{limit},2);
			$data{balance}	= format_number($data{balance},2);
			$data{limit}	= format_number($data{limit},2);
			$data{pin}		= format_pin($data{pin});
			
			$data{found} 	= 1;
		}
	}
    #
	#---------------------------------------------------
    # check service_id 
	#---------------------------------------------------
	return %data
}
sub do_view_tree_js() {
    &cgi_hearder_html();
    $service_id = clean_int(substr($form{id},0,100));
    #
    # busca lista de child ids desse parent
    $sql = "
	SELECT
	    service_tree.service_id,
	    unix_timestamp(service.creation_date),
	    service.name,
	    service_status.deleted 
	FROM
	    service_tree,
	    service,
	    service_status 
	where
	    service_tree.parent_service_id='$service_id' and
	    service_tree.service_id = service.id and
	    service.status=service_status.id 
	";
    %list = database_select_as_hash($sql,"date,name,deleted");
    #
    # busca somatorio dos dados
    $ids = "";
    foreach (keys %list) {$ids .= "$_,"}
    if ($ids ne "") {
		$ids = substr($ids,0,-1);
		$sql = "
			select parent_service_id,count(*) 
			from service_tree 
			where parent_service_id in ($ids)
			group by parent_service_id
		";
		%sum = database_select_as_hash($sql);
		foreach(keys %sum) {$list{$_}{friends} = $sum{$_};}
    }
    #
    # imprime em js pra popular a tabela
    print "<script>parent.ContainerClean('".$service_id."_box');</script>";
    $size = scalar keys %list;
    $c=0;
    foreach $id (sort{$list{$b}{date} <=> $list{$a}{date} } keys %list) {
		#
		# calcula extras
		$c++;
		#
		# calcula nome
		$name = $list{$id}{name};
		$friends = $list{$id}{friends};
		#
		# calcula url
		$url = ($friends ne "") ? "javascript:ClickItem($id)" : "javascript:void(0);";
		#
		# calcula class
		if ($c eq $size) {
			$class = ($friends ne "")  ? "tree_plus_end" : "tree_line_end";
		} else {
			$class = ($friends ne "")  ? "tree_plus" : "tree_line";
		}
		#
		# imprime node
		$name = ($name eq "") ? "(no name $id)" : $name;
		$html = "<a href='$url'><img src=/design/icons/user.png hspace=0 vspace=0 border=0 style='margin-right:5px;' align=left><input type=checkbox align=left style=float:left name=$id value=1>$name</a> <a style='color:#999999' href=$my_url?action=view_referral&service_id=$id>(edit)</a>";
        print "<script>parent.ContainerAppend('".$service_id."_box','$id',\"$html\",'$class');</script>";
    }
}
sub do_view_login(){
    #
    # confere service_id e client_id
    $service_id = clean_int(substr($form{service_id},0,100));
    %hash = database_select_as_hash("select 1,1 from service where service.id='$service_id' ","flag");
    unless ($hash{1}{flag} eq 1) {adm_error("Unknown client"); return;}
    #
    # faz login da conta
	# operaco suicida, daqui em diante nao posso mais
	# me manter nesse CGI. TOdas as variaveis vao mudar
    %hash = database_select_as_hash("select 1,1,name,email from service where service.id='$service_id' ","flag,name,email");
	$app{users_table}				= "service";
	$app{users_col_id}				= "id";
	$app{users_options_table}		= "service_data";
	$app{session_table}				= "service_session";
	$app{session_cookie_k_name}		= "sk";
	$app{session_cookie_u_name}		= "su";
	$app{session_logout_on_timeout} = 1;
	$app{session_timeout_seconds}	= 60*30*99;
	$app{session_active_service_id}	= "";
	$app{session_status}			= 0;
	$app{use_imagecheck}			= 1;
	if (session_attach($service_id) eq 1) {
		&session_set($app{session_cookie_k},"service_email"	    ,$hash{1}{email});
		&session_set($app{session_cookie_k},"service_name"	    ,$hash{1}{name});
		&session_set($app{session_cookie_k},"is_from_noc"	    ,1);
		if (&multilevel_coupon_engine_autorecharge_can_assign($service_id) eq 1) {
			$sql = "
				select 1,1,service_coupon_type.ui_msg_out_stock
				from service,service_status,service_coupon_type
				where
				service.id='$service_id'
				and service.status=service_status.id 
				and service_status.coupon_id_auto_recharge_signin = service_coupon_type.id
				and service_coupon_type.auto_pause_engine='autorecharge'
			";
			%hash = database_select_as_hash($sql,"flag,msg");
			$tmp = ($hash{1}{flag} eq 1) ? $hash{1}{msg} : "You have one promotion waiting for you! <a href=/myaccount/index.cgi?action=coupons>Check it now!</a>";
			&session_set($app{session_cookie_k},"service_message",$tmp);
		}
	}
	print "content-type: text/html\n\n";
	print "<body background=#ffffff><font face=verdana size=2><a href=/myaccount/>Please wait...</a>";
	print "<script>window.location=\"/myaccount/\"</script>";
    #cgi_redirect("/myaccount/");
    exit;
}
#========================================================================
# detail data
#========================================================================
sub do_detail_coupon_stop(){
	$coupon_id = &clean_int(substr($form{coupon_id},0,100));
	$sql = "
	select
		1,1,
		service_coupon_stock.id,
		service_coupon_stock.service_id,
		service_coupon_stock_status.is_ready_to_next_slice,
		service_coupon_stock_status.is_in_use,
		service_coupon_stock_status.is_paused
	from
		service_coupon_type,
		service_coupon_stock,
		service_coupon_stock_status
	where
		service_coupon_stock.id='$coupon_id'
		and service_coupon_stock.coupon_type_id = service_coupon_type.id
		and service_coupon_stock.status = service_coupon_stock_status.id
	";
	%hash = database_select_as_hash($sql,"flag,id,service_id,is_ready_to_next_slice,is_in_use,is_paused");
    unless ( ($hash{1}{flag} eq 1) && ($hash{1}{id} eq $coupon_id) )  { %t=(); $t{dic}{content}="Invalid coupon_id"; &template_print("template.modal.html",%t);exit; }
	if ($hash{1}{is_in_use} eq 1){
		if (&multilevel_coupon_stop($coupon_id) eq 1) {
			&action_history("coupon:status:stopbynoc",('coupon_stock_id'=>$id,'service_id'=>$hash{1}{service_id}));
		}
	}
	%t = ();
	$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	&template_print("template.modal.html",%t);
}	
sub do_detail_coupon_unstop(){
	$coupon_id = &clean_int(substr($form{coupon_id},0,100));
	$sql = "
	select
		1,1,
		service_coupon_stock.id,
		service_coupon_stock.service_id,
		service_coupon_stock_status.is_ready_to_next_slice,
		service_coupon_stock_status.is_in_use,
		service_coupon_stock_status.is_paused
	from
		service_coupon_type,
		service_coupon_stock,
		service_coupon_stock_status
	where
		service_coupon_stock.id='$coupon_id'
		and service_coupon_stock.coupon_type_id = service_coupon_type.id
		and service_coupon_stock.status = service_coupon_stock_status.id
	";
	%hash = database_select_as_hash($sql,"flag,id,service_id,is_ready_to_next_slice,is_in_use,is_paused");
    unless ( ($hash{1}{flag} eq 1) && ($hash{1}{id} eq $coupon_id) )  { %t=(); $t{dic}{content}="Invalid coupon_id"; &template_print("template.modal.html",%t);exit; }
	if ($hash{1}{is_in_use} eq 1){
		if (&multilevel_coupon_unstop($coupon_id) eq 1) {
			&action_history("coupon:status:unstopbynoc",('coupon_stock_id'=>$id,'service_id'=>$hash{1}{service_id}));
		}
	}
	%t = ();
	$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	&template_print("template.modal.html",%t);
}	
sub do_detail_coupon(){
	$coupon_id = &clean_int(substr($form{coupon_id},0,100));
	$sql = "
	select
		1,1,
		service_coupon_stock.id,
		unix_timestamp(service_coupon_stock.slice_timestamp),
		service_coupon_type.title,
		service_coupon_stock_status.title,
		service_coupon_stock_status.is_ready_to_next_slice,
		service_coupon_stock_status.is_in_use,
		service_coupon_stock_status.is_paused
	from
		service_coupon_type,
		service_coupon_stock,
		service_coupon_stock_status
	where
		service_coupon_stock.id='$coupon_id'
		and service_coupon_stock.coupon_type_id = service_coupon_type.id
		and service_coupon_stock.status = service_coupon_stock_status.id
	";
	%hash = database_select_as_hash($sql,"flag,id,timestamp,title,status,is_ready_to_next_slice,is_in_use,is_paused");
    unless ( ($hash{1}{flag} eq 1) && ($hash{1}{id} eq $coupon_id) )  { %t=(); $t{dic}{content}="Invalid coupon_id"; &template_print("template.modal.html",%t);exit; }
	%coupon_data = %{$hash{1}};
	$action = "";
	if ($coupon_data{is_in_use} eq 1){
		$action .= "<form action=$my_url>";
		if ($coupon_data{is_ready_to_next_slice}.$coupon_data{is_paused} eq "00"){
			$action .= "<button style='width:300px;' class=button type=submit>UN-STOP all future charges from this coupon</button>";
			$action .= "<input type=hidden name=action value=detail_coupon_unstop>";
		} else {
			$action .= "<button style='width:300px;' class=button type=submit>STOP all future charges from this coupon</button>";
			$action .= "<input type=hidden name=action value=detail_coupon_stop>";
		}
		$action .= "<input type=hidden name=coupon_id value=$coupon_id>";
		$action .= "</form>";
	}
	
	%t = ();
    $t{dic}{content}	= qq[
	<div class=alert_box><div class=alert_box_inside>
	<b>READ THIS:</b> This is not the perfect coupon detail page! This is only a workaround. Later we come back and do a real usefull detail page
	</div></div>
	<br>
	
		Title: $coupon_data{title}<br>
		Status: $coupon_data{status}<br>
		<br>
		$action

	];
    &template_print("template.modal.html",%t);

}
sub do_detail_call(){
    #
    # confere call log id
    $call_log_id = clean_int(substr($form{call_log_id},0,100));
	%t = ();
	#
	# print page
	$sql = "
	SELECT 1,1,unix_timestamp(datetime_start),id,ani,did,dst,billing_id,error_id,info_id,ast_unique_id,system_host 
	FROM calls_log where id='$call_log_id' 
	";
	%hash = database_select_as_hash($sql, "flag,date,id,ani,did,dst,billing_id,error_id,info_id,ast_unique_id,system_host");
	if ($hash{1}{flag} ne 1) {
		$t{dic}{content} .= "<b>Call not found</b><br>";
	} else {
		%call = %{$hash{1}}; 
		if ($call{info_id} ne "") {
			%hash = database_select_as_hash("select 1,1,value from calls_log_info where id='$call{info_id}'","flag,value");
			$call{info} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} ne "") ) ? $hash{1}{value} : "";
		}
		if ($call{billing_id} ne "") {
			%hash = database_select_as_hash("select 1,1,seconds,value,balance_before from calls where id='$call{billing_id}'","flag,seconds,value,balance_before");
			$call{seconds} 			= ( ($hash{1}{flag} eq 1) && ($hash{1}{seconds} 		ne "") ) ? $hash{1}{seconds} : "";
			$call{value} 			= ( ($hash{1}{flag} eq 1) && ($hash{1}{value} 			ne "") ) ? $hash{1}{value} : "";
			$call{balance_before}	= ( ($hash{1}{flag} eq 1) && ($hash{1}{balance_before} 	ne "") ) ? $hash{1}{balance_before} : "";
		}
		#
		# print page
		if ($call{error_id} eq "") {
			if ($call{billing_id} eq "") {
				$t{dic}{content} .= "<b>Call approved but not connected</b><br>";
			} else {
				$t{dic}{content} .= "<b>Call approved and connected</b><br>";
			}
		} else {
			$t{dic}{content} .= "<b>Call rejected</b><br>";
		}
		if ($call{info}			ne "") {$t{dic}{content} .= "Info: $call{info}<br>";}	
		$t{dic}{content} .= "Date: ". &format_time_gap($call{date}) ."<br>";
		$t{dic}{content} .= "Dial from: ". &format_E164_number($call{ani},"USA") ."<br>";
		$t{dic}{content} .= "Dial to: ". 	&format_E164_number($call{did},"USA") ."<br>";
		if ($call{dst}			ne "") {$t{dic}{content} .= "Connect to: ".&format_E164_number($call{dst},"USA")."<br>";}
		if ($call{billing_id} 	ne "") {$t{dic}{content} .= "Duration: ".	&format_time($call{seconds})."<br>"; }
		if ($call{billing_id} 	ne "") {$t{dic}{content} .= "Balance before: \$".&format_number($call{balance_before},4)."<br>"; }
		if ($call{billing_id} 	ne "") {$t{dic}{content} .= "Value: \$".&format_number($call{value},4)."<br>"; }
		if ($call{billing_id} 	ne "") {$t{dic}{content} .= ($call{balance_before} eq "") ? "" : "Balance after: \$".&format_number(($call{balance_before}-$call{value}),4); }
		#
		# debug
		if ( ($call{ast_unique_id} ne "") && ($call{system_host} ne "") ) {
			$cmd_last_time = 0;


			$cmd_host = &clean_str($call{system_host},"-.");
			$cmd_file = &clean_str($call{ast_unique_id},"-.");
			$cmd = "echo \"cat /var/log/asterisk/calls_log/$cmd_file\" | ssh -p 2223 -q  multilevel\@$cmd_host ";
			@lines = `$cmd`;

# 	$cmd_host = &clean_str($call{system_host},"-.");	
#	$cmd_file = &clean_str($call{ast_unique_id},"-.");
#	$cmd_url  = "http://$cmd_host/call_debug.cgi?id=$cmd_file";
#	@lines = ();
#	@lines = (@lines,"Cannot get call debug for call_id=$cmd_file_id host=$cmd_host");
#	my $ua = LWP::UserAgent->new;
 #	$ua->timeout(15);
#	$raw = $ua->get($cmd_url);
#	if ($raw->is_success) {
#		@lines = split(/\n/,$raw->decoded_content);
#	}

			$buf = "";
			$ln = 1;
			foreach (@lines){
				$buf .=$_."<br>\n";
			
				chomp;
				($tmp1,$tmp2) = split(/\|/,$_);
				if ( (index($tmp2,"!") ne -1) && (index($tmp2,"debug") ne -1) ) {
					($tmptmp1,@tmptmpall) = split(/\:/,$tmp2);
					$tmptmp2 = join(":",@tmptmpall);
					$c=1;
					foreach $tt0 (split(/\!/,$tmptmp2)) {
						$tt1="<"; $tt2="&lt;"; $tt0 =~ s/$tt1/$tt2/eg; 
						$tt1=">"; $tt2="&gt;"; $tt0 =~ s/$tt1/$tt2/eg; 
						$buf .= "$ln: $tmptmp1 $c: $tt0<br>\n";
						$c++;
						$ln++;
					}
				} else {
					$tmp = "";
					if ($cmd_last_time > 0) {
						$gap = ($tmp1-$cmd_last_time);
						if ($gap > 1) {
							$tmp = "<b>($gap seconds later)</b> ";
						}
					}
					$cmd_last_time = $tmp1;
					$tt1="<"; $tt2="&lt;"; $tmp2 =~ s/$tt1/$tt2/eg; 
					$tt1=">"; $tt2="&gt;"; $tmp2 =~ s/$tt1/$tt2/eg; 
					$buf .= "$ln: $tmp$tmp2<br>\n";
					$ln++;
				}
			}
			$t{dic}{content} .= qq[
			<br><b>Debug call "$cmd_file" at "$cmd_host" host</b><br>
			<pre style="font-size:10px;line-height:100%;white-space:nowrap;">$buf</pre>
			];
		}
	} 
    &template_print("template.modal.html",%t);
}
sub do_detail_ccprofile(){
    #
	#---------------------------------------------------
    # check ID
	#---------------------------------------------------
	$cc_profile_id = &clean_int(substr($form{ccprofile_id},0,100));
	$sql = "
	SELECT 1,1,id,service_id,cc_number,cc_error,cc_fingerprint,active,is_auto_recharge
	FROM  service_profile_cc
	where id='$cc_profile_id'
	";
	%hash = database_select_as_hash($sql,"flag,id,service_id,cc_number,cc_error,cc_fingerprint,active,is_auto_recharge");
    if ($hash{1}{flag} ne 1) { %t=(); $t{dic}{content}="Invalid credit card profile"; &template_print("template.modal.html",%t);exit; }
	%ccprofile_data = %{$hash{1}};
    #
	#---------------------------------------------------
    # error set/unset
	#---------------------------------------------------
	if ($form{error_set} ne "") {
		if ( &multilevel_clickchain_check("dccp",$form{error_set}) eq 1 ) {
			&multilevel_securedata_cc_error_set($cc_profile_id);
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
			exit;
		}
	}
	if ($form{error_unset} ne "") {
		if ( &multilevel_clickchain_check("dccp",$form{error_unset}) eq 1 ) {
			multilevel_securedata_cc_error_unset($cc_profile_id);
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
			exit;
		}
	}
    #
	#---------------------------------------------------
    # action block set/unset
	#---------------------------------------------------
	if ($form{block_set} ne "") {
		if ( &multilevel_clickchain_check("dccp",$form{block_set}) eq 1 ) {
			&multilevel_securedata_cc_block_set($cc_profile_id);
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
			exit;
		}
	}
	if ($form{block_unset} ne "") {
		if ( &multilevel_clickchain_check("dccp",$form{block_unset}) eq 1 ) {
			&multilevel_securedata_cc_block_unset($cc_profile_id);
			%t = ();
			$t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
			&template_print("template.modal.html",%t);
			exit;
		}
	}
    #
	#---------------------------------------------------
    # print page
	#---------------------------------------------------
	$clickchain_id = &multilevel_clickchain_set("dccp");
	$html_cc_profile_status = "";
	$html_cc_status = "";
	#
	# read cc_profile error flag 
	if ($ccprofile_data{active} eq 1) {
		if ($ccprofile_data{cc_error} eq 1) {
			$html_cc_profile_status .= qq[
			<font color=red><b>Warning:</b></font> This profile is flaged as error.<br>
			<form action=$my_url style="margin-top:5px;">
			<button class=button type=submit>Disable error</button>
			<input type=hidden name=error_unset value='$clickchain_id'>
			<input type=hidden name=action value=detail_ccprofile>
			<input type=hidden name=ccprofile_id value=$cc_profile_id>
			</form>
			];
		} else {
			$html_cc_profile_status .= qq[
			This credit card profile is ok.<br>
			<form action=$my_url style="margin-top:5px;">
			<button  class=button type=submit>Flag error</button>
			<input type=hidden name=error_set value='$clickchain_id'>
			<input type=hidden name=action value=detail_ccprofile>
			<input type=hidden name=ccprofile_id value=$cc_profile_id>
			</form>
			];
		}
	} else {
		$html_cc_profile_status .= qq[
		This credit card profile is deleted.<br>
		];
	}
	#
	# read cc status
	%hash = database_select_as_hash("SELECT 1,count(*) FROM service_profile_cc where cc_fingerprint='$ccprofile_data{cc_fingerprint}' and active=1 and service_id <> $ccprofile_data{service_id}");
	$multiple_use_count = $hash{1} || 0;
	$multiple_use_message  = "";
	if ($ccprofile_data{active} eq 1) {
		$multiple_use_message = ($multiple_use_count > 0) ? "<B>Warning!</b> This same credit card is active in other $multiple_use_count credit card profiles. Please check if this is a fake card" : 	$multiple_use_message ;
	} else {
		$multiple_use_message = ($multiple_use_count > 1) ? "<B>Warning!</b> This same credit card is active in other $multiple_use_count credit card profiles. Please check if this is a fake card" : 	$multiple_use_message ;
	}
	%hash = database_select_as_hash("SELECT 1,count(*) FROM security_cc_block where cc_fingerprint='$ccprofile_data{cc_fingerprint}'");
	$block_count = $hash{1} || 0;
	if ($block_count > 0) {
		$html_cc_status .= qq[
		<font color=red><b>Warning:</b></font> The credit card '$ccprofile_data{cc_number}' is banned in the system and cannot be added in any new 'Credit card profile'.<br>$multiple_use_message 
		<form action=$my_url style="margin-top:5px;" onSubmit="return confirm('Are you sure! This will allow clients enter this credit card in the system and also disable error in all active credit card profiles that use this card')">
		<button class=button type=submit>Allow this credit card in the system </button>
		<input type=hidden name=block_unset value='$clickchain_id'>
		<input type=hidden name=action value=detail_ccprofile>
		<input type=hidden name=ccprofile_id value=$cc_profile_id>
		</form>
		];
	} else {
		$html_cc_status .= qq[
		credit card '$ccprofile_data{cc_number}' is not banned in the system.<br>$multiple_use_message 
		<form action=$my_url style="margin-top:5px;" onSubmit="return confirm('Are you sure! We will never accept this card anymore and flag error all credit card profiles that use this card')">
		<button class=button type=submit>Ban this credit card in the system </button>
		<input type=hidden name=block_set value='$clickchain_id'>
		<input type=hidden name=action value=detail_ccprofile>
		<input type=hidden name=ccprofile_id value=$cc_profile_id>
		</form>
		];
	}
    #
	#---------------------------------------------------
    # print page
	#---------------------------------------------------
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[

	<fieldset><legend>Credit card profile status</legend>	
	$html_cc_profile_status
 	</fieldset><br>


	<fieldset><legend>Credit card status</legend>	
	$html_cc_status
 	</fieldset><br>

	];
	#foreach (sort keys %app){$t{dic}{content}	.= qq[$_=$app{$_}<br>];}
    &template_print("template.modal.html",%t);
}
sub do_detail_commission(){
    #
	#---------------------------------------------------
    # check ID
	#---------------------------------------------------
	$commission_id = &clean_int(substr($form{commission_id},0,100));
	$sql = "
	SELECT 1,1,
	unix_timestamp(creation_date),unix_timestamp(activation_date_1),unix_timestamp(activation_date_2), status,
	credit_id,invoice_id,from_service_id,deep,
	engine,value,age_discount_value_before,age_discount_percentage
	FROM service_commission 
	where id='$commission_id' 
	";
	%hash = database_select_as_hash($sql,"flag,creation_date,activation_date_1,activation_date_2,status,credit_id,invoice_id,from_service_id,deep,engine,value,age_discount_value_before,age_discount_percentage");
    if ($hash{1}{flag} ne 1) { %t=(); $t{dic}{content}="Invalid commission"; &template_print("template.modal.html",%t);exit; }
	%commission_data = %{$hash{1}};
	#
	# get debug data
	$debug = &log_debug_get("commission_id=".$commission_id);
	#
	# print page
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[
    commission id: $commission_id<br>
    Engine: $commission_data{engine}<br>
	<br><b>Debug commission</b><br>
	<pre style="font-size:10px;line-height:100%;xxwhite-space:nowrap;">$debug</pre>
	];
    &template_print("template.modal.html",%t);
}
#========================================================================
# search service
#========================================================================
sub do_search(){
    #
    #-----------------------------------------------
    # remember
    #-----------------------------------------------
	if ($form{remember} eq 1) {
		delete($form{remember});
		%form=();
		$buf = &active_session_get("search");
		foreach $block (split(/\&/,$buf)){
			($name,$value) = split(/\=/,$block);
			$form{&cgi_url_decode($name)} = &cgi_url_decode($value);
		}
	} else {
		unless ( ($form{email} eq "1") || ($form{export} eq "1") ) {
			delete($form{remember});
			$buf = "";
			foreach $name (keys %form) {
				$value = $form{$name};
				$buf .= &cgi_url_encode($name)."=".&cgi_url_encode($value)."&";
			}
			&active_session_set("search",$buf);
		}
	}
	delete($form{remember});
    #
    #-----------------------------------------------
    # start
    #-----------------------------------------------
    %selected_services				= ();
    %selected_services_extra_data	= ();
	$sort_mode = "BY_KEY_REVERSE";
	$query_quantity = 0;
	$query = clean_str(substr($form{query},0,256),"\@.-_()<>+=~ ");
	$form{query} = $query;
    #
    #-----------------------------------------------
    # query search
    #-----------------------------------------------
    if ($query ne "") {
		$sort_mode = "BY_POINTS_REVERSE";
		$query_quantity++;
		foreach $word ( split(/ +/,$query) ) {
			#
			#----------------------------------
			# start
			#----------------------------------
			$word = trim($word);
			if ($word eq "") {next}
			$word_int = &clean_int($word);
			#
			#----------------------------------
			# select conexts
			#----------------------------------
			$context_name 		= 0;
			$context_email		= 0;
			$context_service_id	= 0;
			$context_ani		= 0;
			$context_dst		= 0;
			$context_did		= 0;
			$context_callid		= 0;
			$context_cc_number	= 0;
			$context_cc_name	= 0;
			if (index("\U$word","ANI=") eq 0) {
				$context_ani = 1;
				$word=substr($word,4,100);
			} elsif (index("\U$word","DST=") eq 0) {
				$context_dst = 1;
				$word=substr($word,4,100);
			} elsif (index("\U$word","DID=") eq 0) {
				$context_did = 1;
				$word=substr($word,4,100);
			} elsif (index("\U$word","CALLID=") eq 0) {
				$context_dst = 1;
				$word=substr($word,7,100);
			} elsif (index("\U$word","NAME=") eq 0) {
				$context_name = 1;
				$word=substr($word,5,100);
			} elsif (index("\U$word","EMAIL=") eq 0) {
				$context_email = 1;
				$word=substr($word,6,100);
			} elsif (index("\U$word","SERVICEID=") eq 0) {
				$context_service_id = 1;
				$word=substr($word,10,100);
			} elsif (index("\U$word","CCNAME=") eq 0) {
				$context_cc_name = 1;
				$word=substr($word,7,100);
			} elsif (index("\U$word","CCNUMBER=") eq 0) {
				$context_cc_number = 1;
				$word=substr($word,9,100);
			} else {
				if ($word eq $word_int) {
					$context_service_id = 1;
					$context_cc_number = (length($word_int) eq 4) ? 1 : $context_cc_number;
					$context_dst = (length($word_int)>=4) ? 1 : $context_dst;
					$context_ani = (length($word_int)>=4) ? 1 : $context_ani;
					$context_did = (length($word_int)>=4) ? 1 : $context_did;
					$context_callid = (length($word_int)>=4) ? 1 : $context_callid;
				} else {
					$context_name = 1;
					$context_email = 1;
					$context_cc_name = 1;
				}
			}
			#----------------------------------
			# query each conext
			#----------------------------------
			#
			#--------------------------
			# name
			#--------------------------
			if ($context_name eq 1) {
				%list = database_select_as_hash("SELECT id,1 FROM service where name like \"\%$word\%\" order by creation_date desc limit 0,1000 ","flag");
				foreach $id (keys %list) { $selected_services{$id}{p}++;$selected_services{$id}{q}=1;}
			}
			#--------------------------
			# email 
			#--------------------------
			if ($context_email eq 1) {
				%list = database_select_as_hash("SELECT id,1,email FROM service where email like \"\%$word\%\" order by creation_date desc limit 0,1000 ","flag,email");
				foreach $id (keys %list) { 
					$selected_services{$id}{p}++;
					$selected_services{$id}{q}=1;
					$selected_services_extra_data{$id}{"email:$list{$id}{email}"}+=1;
				}
				%list = database_select_as_hash("SELECT id,1,email FROM service where email='$word' order by creation_date desc limit 0,100 ","flag,email");
				foreach $id (keys %list) { 
					$selected_services{$id}{p} +=100;
					$selected_services{$id}{q}=1;
					$selected_services_extra_data{$id}{"email:$list{$id}{email}"}+=100;
				}
			}
			#--------------------------
			# service_id
			#--------------------------
			if ($context_service_id eq 1) {
				%list = database_select_as_hash("SELECT id,1 FROM service where id='$word'","flag");
				foreach $id (keys %list) { $selected_services{$id}{p} +=1000;$selected_services{$id}{q}=1;}
			}
			#--------------------------
			# context_cc_number
			#--------------------------
			if ($context_cc_number eq 1) {
				%list = database_select_as_hash("SELECT service_id,id,1 from service_profile_cc where right(cc_number,4) = '$word' limit 0,1000 ","cc,flag");
				foreach $id (keys %list) { 
					$selected_services{$id}{p} +=1000;
					$selected_services{$id}{q}=1;
					$selected_services_extra_data{$id}{"cc:$list{$id}{cc}"}+=100;
				}
			}
			#--------------------------
			# context_cc_name
			#--------------------------
			if ($context_cc_number eq 1) {
				%list = database_select_as_hash("SELECT service_id,id,1 from service_profile_cc where first_name like '\%$word\%' or last_name like '\%$word\%' limit 0,1000 ","cc,flag");
				foreach $id (keys %list) { 
					$selected_services{$id}{p} +=1000;
					$selected_services{$id}{q}=1;
					$selected_services_extra_data{$id}{"cc:$list{$id}{cc}"}+=100;
				}
			}
			#--------------------------
			# query ani
			#--------------------------
			if ($context_ani eq 1) {
				if (index($word,"~") eq 0)  {
					$sql = "
					select distinct service_id,ani,1
					from calls_log
					where datetime_start>date_sub(now(),interval 365 day) and ani like \"\%$word_int\%\"
					limit 0,1000
					";
					$tmp=10;
				} else {
					$sql = "
					select distinct service_id,ani,1
					from calls_log
					where datetime_start>date_sub(now(),interval 365 day) and ani like \"$word_int\%\"
					limit 0,1000
					";
					$tmp=100;
				}
				%list = database_select_as_hash($sql,"ani,flag");
				foreach $id (keys %list) {
					$selected_services{$id}{p} +=$tmp;
					$selected_services{$id}{q} =1;
					$selected_services_extra_data{$id}{"ani:$list{$id}{ani}"}+=$tmp;
				}
				if (index($word,"~") eq 0)  {
					$sql = "
					select distinct service_id,ani,1
					from service_ani
					where ani like \"\%$word_int\%\"
					limit 0,1000
					";
					$tmp=10;
				} else {
					$sql = "
					select distinct service_id,ani,1
					from service_ani
					where ani like \"$word_int\%\"
					limit 0,1000
					";
					$tmp=100;
				}
				%list = database_select_as_hash($sql,"ani,flag");
				foreach $id (keys %list) {
					$selected_services{$id}{p} +=$tmp;
					$selected_services{$id}{q} = 10;
					$selected_services_extra_data{$id}{"ani:$list{$id}{ani}"}+=$tmp;
				}
			}
			#--------------------------
			# query did
			#--------------------------
			if ($context_did eq 1) {
				if (index($word,"~") eq 0)  {
					$sql = "
					select distinct service_id,did,1
					from calls_log
					where datetime_start>date_sub(now(),interval 365 day) and did like \"\%$word_int\%\"
					limit 0,1000
					";
					$tmp=10;
				} else {
					$sql = "
					select distinct service_id,did,1
					from calls_log
					where datetime_start>date_sub(now(),interval 365 day) and did like \"$word_int\%\"
					limit 0,1000
					";
					$tmp=100;
				}
				%list = database_select_as_hash($sql,"did,flag");
				foreach $id (keys %list) {
					$selected_services{$id}{p} +=$tmp;
					$selected_services{$id}{q} =1;
					$selected_services_extra_data{$id}{"did:$list{$id}{did}"}+=$tmp;
				}
			}
			#--------------------------
			# query dst
			#--------------------------
			if ($context_dst eq 1) {
				if (index($word,"~") eq 0)  {
					$sql = "
					select distinct service_id,dst,1
					from calls_log
					where datetime_start>date_sub(now(),interval 365 day) and dst like \"\%$word_int\%\"
					limit 0,1000
					";
					$tmp=10;
				} else {
					$sql = "
					select distinct service_id,dst,1 
					from calls_log
					where datetime_start>date_sub(now(),interval 365 day) and dst like \"$word_int\%\"
					limit 0,1000
					";
					$tmp=1000;
				}
				%list = database_select_as_hash($sql,"dst,flag");
				foreach $id (keys %list) {
					$selected_services{$id}{p} +=$tmp;
					$selected_services{$id}{q} =1;
					$selected_services_extra_data{$id}{"dst:$list{$id}{dst}"}+=$tmp;
				}
			}
			#--------------------------
		}
	}
    #
    #-----------------------------------------------
    # filters search
    #-----------------------------------------------
	foreach $index (1..4) {
		$filter = clean_str(substr($form{"filter_$index"},0,256),"\@.-_()<> ");
		$sql=""; 
		#if ($filter eq "master_flag_invited"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('invited',tags)>0 	and service.status=service_status.id"; }
		#if ($filter eq "master_flag_active"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('active',tags)>0 	and service.status=service_status.id"; }
		#if ($filter eq "master_flag_disabled"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('disabled',tags)>0 	and service.status=service_status.id"; }
		#if ($filter eq "master_flag_ianda"			) { $sql="SELECT service.id,1 FROM service_status,service where (FIND_IN_SET('invited',tags)>0 	or FIND_IN_SET('active',tags)>0) 	and service.status=service_status.id"; }

		#if ($filter eq "flag_calls_true"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_calls',tags)>0 		and service.status=service_status.id"; }
		#if ($filter eq "flag_calls_false"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_no_calls',tags)>0 	and service.status=service_status.id"; }
		#if ($filter eq "flag_calls_unknown"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_no_calls',tags)=0 	and FIND_IN_SET('with_calls',tags)=0 	and service.status=service_status.id"; }

		#if ($filter eq "flag_recharge_true"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_recharge',tags)>0 	and service.status=service_status.id"; }
		#if ($filter eq "flag_recharge_false"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_no_recharge',tags)>0 	and service.status=service_status.id"; }
		#if ($filter eq "flag_recharge_unknown"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_no_recharge',tags)=0 	and FIND_IN_SET('with_recharge',tags)>04and service.status=service_status.id"; }

		#if ($filter eq "flag_suspicious_yes"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('suspicious',tags)>0 		and service.status=service_status.id"; }
		#if ($filter eq "flag_suspicious_good"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('not_suspicious',tags)>0 	and service.status=service_status.id"; }
		#if ($filter eq "flag_suspicious_unknown"	) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('not_suspicious',tags)=0 	and FIND_IN_SET('suspicious',tags)=0  	and service.status=service_status.id"; }

		if ($filter eq "balance_less_than_05"		) { $sql="SELECT id,1 FROM service where (balance-service.limit) < -0.05 "; 	}
		if ($filter eq "balance_negative"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) < 0 "; 	}
		if ($filter eq "balance_zero"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) = 0 "; 	}
		if ($filter eq "balance_less_1"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 1 ";	}
		if ($filter eq "balance_less_5"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 5 "; 	}
		if ($filter eq "balance_less_10"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 10 "; 	}
		if ($filter eq "balance_less_20"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 20 "; 	}
		if ($filter eq "balance_less_50"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 50 "; 	}
		if ($filter eq "balance_more_0"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 0 "; 	}
		if ($filter eq "balance_more_1"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 1 "; 	}
		if ($filter eq "balance_more_5"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 5 "; 	}
		if ($filter eq "balance_more_10"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 10 ";	}
		if ($filter eq "balance_more_20"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 20 "; 	}
		if ($filter eq "balance_more_50"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 50 "; 	}
		
		if ($filter eq "creation_date_7days"		) { $sql="SELECT id,1 FROM service where creation_date>date_sub(now(),interval 7 day) "; }
		if ($filter eq "creation_date_15days"		) { $sql="SELECT id,1 FROM service where creation_date>date_sub(now(),interval 15 day) "; }
		if ($filter eq "creation_date_30days"		) { $sql="SELECT id,1 FROM service where creation_date>date_sub(now(),interval 30 day) "; }
		if ($filter eq "creation_date_60days"		) { $sql="SELECT id,1 FROM service where creation_date>date_sub(now(),interval 60 day) "; }

		if ($filter eq "last_100"					) { $sql="SELECT id,1 FROM service order by id desc limit 0,100 "; }
		if ($filter eq "last_200"					) { $sql="SELECT id,1 FROM service order by id desc limit 0,200 "; }
		if ($filter eq "last_500"					) { $sql="SELECT id,1 FROM service order by id desc limit 0,500 "; }
		if ($filter eq "last_1000"					) { $sql="SELECT id,1 FROM service order by id desc limit 0,1000 "; }

		if ($filter eq "last_call_7days"			) { $sql="SELECT target,1 FROM service_data where name='stat_last_call_ts' and value>unix_timestamp(date_sub(now(),interval 7 day)) "; }
		if ($filter eq "last_call_15days"			) { $sql="SELECT target,1 FROM service_data where name='stat_last_call_ts' and value>unix_timestamp(date_sub(now(),interval 15 day)) "; }
		if ($filter eq "last_call_30days"			) { $sql="SELECT target,1 FROM service_data where name='stat_last_call_ts' and value>unix_timestamp(date_sub(now(),interval 30 day)) "; }
		if ($filter eq "last_call_60days"			) { $sql="SELECT target,1 FROM service_data where name='stat_last_call_ts' and value>unix_timestamp(date_sub(now(),interval 60 day)) "; }

		if (index($filter,"status_") eq 0) {
			$tmp2 = "";
			foreach (split(/\_/,substr($filter,7,100))) {
				$tmp1 = clean_int($_);
				if ($tmp1 eq "") {next}
				$tmp2 .= $tmp1.",";
			}
			if ($tmp2 ne ""){
				$tmp2 = substr($tmp2,0,-1);
				$sql="SELECT id,1 FROM service where status in ($tmp2)";
			}
		}

		if (index($filter,"tag_") eq 0) {
			$tmp = clean_int($filter);
			$sql="SELECT service_id,1 FROM service_tag where tag_string_id=$tmp";
		}

		if ($sql ne "") { 
			$query_quantity++;
			%list = database_select_as_hash($sql);
			foreach $id (keys %list) {
				$selected_services{$id}{p} += 1;
				$selected_services{$id}{q} += 1;
			}
		}
	}
    #
    #-----------------------------------------------
    # clean non used services
    #-----------------------------------------------
	foreach $id (keys %selected_services) {
		if ($selected_services{$id}{q} < $query_quantity) {
			delete $selected_services{$id};
		}
	}
    #-----------------------------------------------
    #
    #
    #-----------------------------------------------
    # desvia pra exprt se necessario
    #-----------------------------------------------
    if ($form{export} eq "1"){
	    print "Pragma: public\n";
	    print "Expires: 0\n";
	    print "Cache-Control: must-revalidate, post-check=0, pre-check=0\n";
	    print "Content-type: application/octet-stream\n";
	    print "Content-Disposition: attachment; filename=\"zenofon.clients.csv\"\n";
	    print "Content-Description: File Transfert\n";
	    #print "Content-type: text/plain\n";
	    print "\n";
	    print "Email Address,First Name,Last Name,Work Phone,Home Phone,Country,Notes,Custom Field 1,Custom Field 2,Custom Field 3\n";
	    @selected_services_ids		= (keys %selected_services);
		$selected_services_ids_raw	= join(",",@selected_services_ids);
		if ($selected_services_ids_raw ne "") {
			# query os dados
			$sql = "
				select service.id,service.name,service.email,service_invite.id
				from service,service_invite
				where service.id in ($selected_services_ids_raw) and service.id=service_invite.service_id
				order by service.last_change 
			";
			%hash = database_select_as_hash($sql,"name,email,invite");
			foreach (keys %hash) {
				if ($hash{$_}{email} ne "") {
				    print "\"$hash{$_}{email}\",";
				    print "\"$hash{$_}{name}\",";
				    print "\"\",";
				    print "\"\",";
				    print "\"\",";
				    print "\"\",";
				    print "\"\",";
				    #
				    # old format
				    #print "\"<a href=http://www.zenofon.com/$hash{$_}{invite}>http://www.zenofon.com/$hash{$_}{invite}</a>\",";
				    #print "\"$hash{$_}{invite}\",";
				    #print "\"$_\"";
				    #
				    # new format
				    print "\"$_\",";
				    #print "\"<a href=http://www.zenofon.com/$hash{$_}{invite}>http://www.zenofon.com/$hash{$_}{invite}</a>\",";
				    print "\"http://www.zenofon.com/$hash{$_}{invite}\",";
				    print "\"$hash{$_}{invite}\"";
				    #
				    print "\n";
				}
			}
		}
	    exit;
    }
    #
    #
    #-----------------------------------------------
    # desvia pra email se necessario
    #-----------------------------------------------
    if ($form{email} eq "1"){
	    @selected_services_ids		= (keys %selected_services);
		$selected_services_ids_raw	= join(",",@selected_services_ids);
		%selected_emails = ();
		if ($selected_services_ids_raw ne "") {
			# query os dados
			$sql = "
			select id,email
			from service
			where 
			service.id in ($selected_services_ids_raw)
			";
			%hash = database_select_as_hash($sql);
			foreach (keys %hash) {
				if ($hash{$_} eq "") {next}
				$selected_emails{$hash{$_}}++;
			}
		}
		$form{email_to} = "";
		$qtd=0;
		foreach (sort keys %selected_emails) {$form{email_to} .= "$_\n";$qtd++;}
		%t = ();
		$t{dic}{my_url}		= $my_url;
		$t{dic}{title}		= "Send email";
		$t{dic}{content}	= qq[
		Please wait...
		<form action=OLD.email.send.cgi method=post>
			<div style="display:none;">
				<textarea name=email_to style="width:300px; height:300px;">$form{email_to}</textarea>
				<br>
				$qtd emails<br>
				<a href=javascript:history.back()>Go back</a>
				<br>
				<input type=submit value="... or click here">
				<input type=hidden name=action value=send>
			</div>
		</form>
		<script>document.forms[0].submit();</script>
		];
		&template_print("template.html",%t);
		return;
    }
    #-----------------------------------------------
    #
    #
    #-----------------------------------------------
    # monta paginacao
    #-----------------------------------------------
	$page_size	= clean_int($form{page_size});
	$page_size	= ($page_size eq "") ? 10 : $page_size;
	$quantity 	= keys %selected_services;
	$page_min	= 1;
	$page_max	= int(($quantity-1)/$page_size)+1;
	$page_max	= ($page_max<$page_min) ? $page_min : $page_max;
	$page 		= clean_int($form{page});
	$page 		= ($form{next} eq 1) ? $page+1 : $page;
	$page 		= ($form{previous} eq 1) ? $page-1 : $page;
	$page 		= ($page<$page_min) ? $page_min : $page;
	$page 		= ($page>$page_max) ? $page_max : $page;
	$selected_services_start	= ($page-1)*$page_size;
	$selected_services_stop		= $selected_services_start+($page_size-1);
	if ($sort_mode eq "BY_KEY_REVERSE") {
	    @selected_services_ids		= (sort{$b <=> $a} keys %selected_services)[$selected_services_start..$selected_services_stop];
	} elsif ($sort_mode eq "BY_POINTS_REVERSE") {
	    @selected_services_ids		= (sort{$selected_services{$b}{p} <=> $selected_services{$a}{p} } keys %selected_services)[$selected_services_start..$selected_services_stop];
	} else {
	    @selected_services_ids		= (sort{$a <=> $b} keys %selected_services)[$selected_services_start..$selected_services_stop];
	}
	$selected_services_ids_raw	= join(",",@selected_services_ids);
	@selected_services_ids 		= ();
	foreach (split(/\,/,$selected_services_ids_raw)) {
		if($_ eq "") {next}
		@selected_services_ids = (@selected_services_ids,$_);
	}
	$selected_services_ids_raw	= join(",",@selected_services_ids);
    #
    #
    #-----------------------------------------------
    # QUERY os dados dos selecionados
    #-----------------------------------------------
    %services_data = ();
	# pega dados dos servicos
	if ($selected_services_ids_raw ne "") {
		# query os dados
		$sql = "
		select service.id,service.name,service_status.name,service.balance
		from service,service_status 
		where 
		service.status = service_status.id and  
		service.id in ($selected_services_ids_raw) 
		";
		%services_data = database_select_as_hash($sql,"name,status_name,balance");
		%hash1 = database_select_as_hash("SELECT target,value FROM service_data where name='stat_last_call_ts' and target in ($selected_services_ids_raw) ");
		%hash2 = database_select_as_hash("SELECT target,value FROM service_data where name='stat_call_qtd' and target in ($selected_services_ids_raw) ");
		foreach $id (@selected_services_ids) {
			$services_data{$id}{status} = "$services_data{$id}{status_name}";
			$services_data{$id}{last_call_date} = $hash1{$id};
			$services_data{$id}{calls_count} = $hash2{$id};
			$index = 1;
			foreach $tmp0 (sort{$selected_services_extra_data{$id}{$b} <=> $selected_services_extra_data{$id}{$a}} keys %{$selected_services_extra_data{$id}}) {
				($tmp1,$tmp2) = split(/\:/,$tmp0);
				$tmp3  = $tmp0;
				if 		($tmp1 eq "did") {$tmp3 = "DID ".&format_E164_number($tmp2,"E164"); }
				elsif 	($tmp1 eq "dst") {$tmp3 = "DST ".&format_E164_number($tmp2,"E164"); }
				elsif 	($tmp1 eq "ani") {$tmp3 = "ANI ".&format_E164_number($tmp2,"E164"); }
				elsif 	($tmp1 eq "email") {$tmp3 = $tmp2}
				elsif 	($tmp1 eq "cc") {
					$tmp3 = "Credit card profile $tmp2";
					%list = database_select_as_hash("SELECT 1,1,cc_type,first_name,last_name,active,right(cc_number,4) from service_profile_cc where id='$tmp2'","flag,type,first,last,active,number");
					if ($list{1}{flag} eq 1) {
						$tmp3 = $list{1}{type}."-$list{1}{number} $list{1}{last} $list{1}{first}";
						$tmp3 .= ($list{1}{active} eq 1) ? "" : " (old)";
					}
				}
				$services_data{$id}{search}{$index} = $tmp3;
				if ($index>=3) {last}
				$index++;
			}
		}
    }
    #
    #-----------------------------------------------
    # create html dos dados dos selecionados
    #-----------------------------------------------
	$html_pg_list = "";
	foreach($page_min..$page_max) {
		if  ( ($_ eq $page_min) || ($_ eq $page_max) || (int($_/100) eq ($_/100) ) ||  ( ($page>($_-100)) && ($page<($_+100)) ) ) {
			$tmp = ($_ eq $page) ? "selected" : ""; 
			$html_pg_list .= "<option $tmp value=$_>Page: $_ of $page_max</option>";
		}
	}
	
	$html_pgsize_list = "";
	$tmp = (10 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=10>10 services per page</option>";
	$tmp = (30 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=30>30 services per page</option>";
	$tmp = (100 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=100>100 services per page</option>";
	$tmp = (500 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=500>500 services per page</option>";
	
    $html_list = "";
    $html_list_empty = "<tr><td colspan=11 style=padding:20px;><center><font color=#c0c0c0>...empty...</font></center></td></tr>";
	$quantity_string = &format_number($quantity,0);
    foreach $id (@selected_services_ids) {
		if ($id eq ""){
			$html_list .= "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><tr>";
			next;
		}
		$url = "<a href='$my_url?action=view&service_id=$id'>";
		$bal = &format_number($services_data{$id}{balance},2);
		$tmp1 = ($services_data{$id}{last_call_date} ne "") ? &format_time_gap($services_data{$id}{last_call_date}) : "&nbsp;";
		$tmp2 = "";
		$tmp2 .= ($services_data{$id}{search}{1} ne "") ? " $services_data{$id}{search}{1}," : "";
		$tmp2 .= ($services_data{$id}{search}{2} ne "") ? " $services_data{$id}{search}{2}," : "";
		$tmp2 .= ($services_data{$id}{search}{3} ne "") ? " $services_data{$id}{search}{3}," : "";
		$tmp2 = substr($tmp2,0,-1);
		$tmp3 = $services_data{$id}{calls_count} || 0;
		$tmp3 = &format_number($tmp3,0);
		$html_list .= qq[
	    <tr>
		<td valign=top><input style="width:13px;" type=checkbox name=$id value=1></td>
	    <td valign=top>$url$id</a></td>
	    <td valign=top>$url$services_data{$id}{name}</a>&nbsp;</td>
	    <td valign=top class=al style="white-space:nowrap;">$url$tmp2</a>&nbsp;</td>
	    <td valign=top class=al style="white-space:nowrap;">$url$services_data{$id}{status}</a>&nbsp;</td>
	    <td valign=top class=ar>$url$tmp3</a></td>
	    <td valign=top class=al>$url$tmp1</a></td>
	    <td valign=top class=ar>$url\$$bal</a></td>
	    </tr>
		];
	    #<td valign=top>$url$services_data{$id}{status} $services_data{$id}{last_suspicious}</a>&nbsp;</td>
		$html_list_empty = "";
    }
 	
  

	
 	
 	 
	#
	# monta os filtros
	$select_html = "";
	foreach $index (1..4) {
		%select_filter=();
		$select_filter{$form{"filter_".$index}} = "selected";
	 
		%htmlinfo 	= &get_statushtml('Auto-recharge','Auto Recharge',$index);
		$html_autorecharge = $htmlinfo{'html'} ;
		
		%htmlinfo 	= &get_statushtml('Pay-as-you-go','Pay as you go',$index);
		$html_payasyougo = $htmlinfo{'html'} ;
		
		%htmlinfo 	= &get_statushtml('Trial','Trial',$index);
		$html_trial = $htmlinfo{'html'} ;
		
		%htmlinfo 	= &get_statushtml('System','System',$index);
		$html_system = $htmlinfo{'html'} ;
		
		
		$select_html .= qq[
		<select name=filter_$index style="width:100%" >

		<option value=""></option>
		<option value="">Select by service status</option>

	 	$html_autorecharge
	 	$html_payasyougo
	 	$html_trial
	 	$html_system
		
	 
		<option value=""></option>
		<option value="">Select by active services status type</option>
		<option $select_filter{status_22_32} 		value="status_22_32"	>&nbsp;&nbsp;-&nbsp;All "suspicious" status type</option>
		<option $select_filter{status_21_31} 		value="status_21_31"	>&nbsp;&nbsp;-&nbsp;All "Good client" status type</option>
		<option $select_filter{status_20_30} 		value="status_20_30"	>&nbsp;&nbsp;-&nbsp;All "unknown" status type</option>

		];


		$select_html .= qq[
		<option value=""></option>
		<option value="">Select by Tag</option>
		];
	    %hash = database_select_as_hash("SELECT id,tag FROM service_tag_string");
		foreach $id (sort{$hash{$a} cmp $hash{$b}} keys %hash) {
			$tmp = ("tag_".$id eq $form{"filter_".$index}) ? "selected" : "";
			$select_html .= "<option $tmp value=tag_$id>&nbsp;&nbsp;-&nbsp;with tag $hash{$id}</a>";
		}

		$select_html .= qq[
		<option value=""></option>
		<option value="">New services</option>
		<option $select_filter{last_100} 	value=last_100  >&nbsp;&nbsp;-&nbsp;Last 100 recent services</option>
		<option $select_filter{last_200} 	value=last_200  >&nbsp;&nbsp;-&nbsp;Last 200 recent services</option>
		<option $select_filter{last_500} 	value=last_500  >&nbsp;&nbsp;-&nbsp;Last 500 recent services</option>
		<option $select_filter{last_1000} 	value=last_1000 >&nbsp;&nbsp;-&nbsp;Last 1000 recent services</option>
		<option value=""></option>
		<option value="">By creation date</option>
		<option $select_filter{creation_date_7days} 	value=creation_date_7days 	>&nbsp;&nbsp;-&nbsp;Services with 7 days old</option>
		<option $select_filter{creation_date_15days}	value=creation_date_15days 	>&nbsp;&nbsp;-&nbsp;Services with 15 days old</option>
		<option $select_filter{creation_date_30days}	value=creation_date_30days 	>&nbsp;&nbsp;-&nbsp;Services with 30 days old</option>
		<option $select_filter{creation_date_60days}	value=creation_date_60days 	>&nbsp;&nbsp;-&nbsp;Services with 60 days old</option>
		<option value=""></option>
		<option value="">By last call date</option>
		<option $select_filter{last_call_7days} 	value=last_call_7days	>&nbsp;&nbsp;-&nbsp;Last call was 7 days old</option>
		<option $select_filter{last_call_15days} 	value=last_call_15days	>&nbsp;&nbsp;-&nbsp;Last call was 15 days old</option>
		<option $select_filter{last_call_30days} 	value=last_call_30days	>&nbsp;&nbsp;-&nbsp;Last call was 30 days old</option>
		<option $select_filter{last_call_60days} 	value=last_call_60days	>&nbsp;&nbsp;-&nbsp;Last call was 60 days old</option>
		<option value=""></option>
		<option value="">By phone balance</option>
		<option $select_filter{balance_less_than_05} value=balance_less_than_05 >&nbsp;&nbsp;-&nbsp;Services with balance less than \$0.05</option>
		<option $select_filter{balance_negative}  	value=balance_negative	>&nbsp;&nbsp;-&nbsp;Services with balance negative</option>
		<option $select_filter{balance_zero} 		value=balance_zero		>&nbsp;&nbsp;-&nbsp;Services with balance zero</option>
		<option $select_filter{balance_less_1}  	value=balance_less_1	>&nbsp;&nbsp;-&nbsp;Services with balance \$1 or less</option>
		<option $select_filter{balance_less_5}  	value=balance_less_5	>&nbsp;&nbsp;-&nbsp;Services with balance \$5 or less</option>
		<option $select_filter{balance_less_10}  	value=balance_less_10	>&nbsp;&nbsp;-&nbsp;Services with balance \$10 or less</option>
		<option $select_filter{balance_less_20}  	value=balance_less_20	>&nbsp;&nbsp;-&nbsp;Services with balance \$20 or less</option>
		<option $select_filter{balance_less_50}  	value=balance_less_50	>&nbsp;&nbsp;-&nbsp;Services with balance \$50 or less</option>
		<option $select_filter{balance_more_0}  	value=balance_more_0	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$0 </option>
		<option $select_filter{balance_more_1}  	value=balance_more_1	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$1 </option>
		<option $select_filter{balance_more_5}  	value=balance_more_5	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$5 </option>
		<option $select_filter{balance_more_10}  	value=balance_more_10	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$10 </option>
		<option $select_filter{balance_more_20}  	value=balance_more_20	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$20 </option>
		<option $select_filter{balance_more_50}  	value=balance_more_50	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$50 </option>
		];


		$select_html .= qq[
		<option value=""></option>
		</select><br>
		];
	}
    #
    # print page
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "Search services";
    $t{breadcrumb}{1}{title}	= "Clients & services";
    $t{breadcrumb}{1}{url}		= "";
    $t{breadcrumb}{2}{title}	= "Search services";
    $t{breadcrumb}{2}{url}		= "$my_url?remember=1";
    $t{dic}{content}	= qq[
	
	<style>
	input {width:150px}
	</style>


	<form action=$my_url>
	<table border=0 colspan=0 cellpadding=2 cellspacing=0 class=clear>
		<td valign=top style="width:220px">
			Search for:<br>
			<input  name=query  style="width:100%;" value="$form{query}" ><br>
			<div style="color:#808080; line-height:130%; padding:5px; letter-spacing:0px; font-size:10px">
			Type service id, name, email, phone number (ANI/DID/DST), credit card last digits or name. 
			You can type fragment or complete information. 
			Phone numbers must be in E164 format (country, area, number). 
			We search calls only 30 days in the past</div>
		</td>
		<td valign=top style="width:400px">
			Filter by:<br>
			$select_html 
		</td>
		<td valign=top >
		&nbsp;<br>
		<button type=submit class="save" style="width:80px;margin-left:3px;" name=submit_button>Search</button><br>
		<button type=button class="cancel" style="width:80px;margin-left:3px;margin-top:3px;" onclick="window.location='$my_url'">Reset</button><br>
		</td>
		<td>
	</table>

	<input type=hidden name=action value=search>
	<br>

	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% onclick="sortColumn(event)">
	    <thead>
			<tr>
			<td width=20>&nbsp;</td>
			<td width=50>ID</td>
			<td >Name</td>
			<td >Search</td>
			<td width=180>Status</td>
			<td width=40>Calls</td>
			<td width=100>Last call</td>
			<td width=50>Balance</td>
			</tr>
	    </thead>
	    <tbody>
			$html_list
			$html_list_empty
	    </tbody>
		<tfoot>
			<tr><td colspan=10 >
				<button type=submit name=previous value=1>&#171;</button>
				<select name=page onchange="document.forms[0].submit()">$html_pg_list</select>
				<select name=page_size onchange="document.forms[0].submit()">$html_pgsize_list</select>
				<button type=submit name=next value=1>&#187;</button>
				($quantity_string services found)
			</td></tr>
		</tfoor>
	</table>
	
	
	
	
	
	<br>
		For selected services: 
		<button type=button class=button onclick=multiple_services_action('tags_select_multiple')>Edit tags</button>
		<button type=button class=button onclick=multiple_services_action('status_edit_multiple')>Edit status</button>
		<button type=button class=button onclick=multiple_services_action_email()>Send email</button>
		<br><br>
		For all $quantity_string services: <button name=email class=button type=submit value=1>Send email</button>  <button name=export class=button type=submit value=1>Export to constantcontact.com</button>
	</form>



	<script>
	function multiple_services_action_email(){
		myform 					= document.forms[0];
		elementsQuantity 		= myform.elements.length;
		elementsSelectedIds 	= "";
		elementsSelectedQuantity= 0;
		for (i=0; i<elementsQuantity; i++){
			if (myform.elements[i].type=="checkbox"){
				if (myform.elements[i].checked){
					elementsSelectedIds = elementsSelectedIds+myform.elements[i].name+",";
					elementsSelectedQuantity++;
				}
			}
		}
		if (elementsSelectedQuantity > 0) {
			url = "OLD.email.send.cgi?action=send&service_ids="+elementsSelectedIds;
			window.location=url
		} else {
			alert("Plaese select one or more services");
		}
	}
	function multiple_services_action(action){
		myform 					= document.forms[0];
		elementsQuantity 		= myform.elements.length;
		elementsSelectedIds 	= "";
		title					= "Edit multiple services"
		if (action == "tags_select_multiple") { title = "Edit tags for multiple services"}
		if (action == "status_edit_multiple") { title = "Edit status for multiple services"}
		elementsSelectedQuantity= 0;
		for (i=0; i<elementsQuantity; i++){
			if (myform.elements[i].type=="checkbox"){
				if (myform.elements[i].checked){
					elementsSelectedIds = elementsSelectedIds+myform.elements[i].name+",";
					elementsSelectedQuantity++;
				}
			}
		}
		if (elementsSelectedQuantity > 0) {
			modal_open(
			title,
			"$my_url?action="+action+"&service_ids="+elementsSelectedIds,
			400,
			300
			);
		} else {
			alert("Plaese select one or more services");
		}
	}
	</script>

	<script>
	document.forms[0].elements[0].focus();
	</script>


    ];
    &template_print("template.html",%t);
}
sub do_OLD_search(){
    #
    #-----------------------------------------------
    # remember
    #-----------------------------------------------
	if ($form{remember} eq 1) {
		delete($form{remember});
		%form=();
		$buf = &active_session_get("search");
		foreach $block (split(/\&/,$buf)){
			($name,$value) = split(/\=/,$block);
			$form{&cgi_url_decode($name)} = &cgi_url_decode($value);
		}
	} else {
		unless ($form{email} eq "1") {
			delete($form{remember});
			$buf = "";
			foreach $name (keys %form) {
				$value = $form{$name};
				$buf .= &cgi_url_encode($name)."=".&cgi_url_encode($value)."&";
			}
			&active_session_set("search",$buf);
		}
	}
	delete($form{remember});
    #
    #-----------------------------------------------
    # start
    #-----------------------------------------------
    %selected_services = ();
	%selected_services_ani = ();
	%selected_services_dst = ();
	$sort_mode = "BY_KEY_REVERSE";
	$query_quantity = 0;
	$query = clean_str(substr($form{query},0,256),"\@.-_()<>+=~ ");
	$form{query} = $query;
    #
    #-----------------------------------------------
    # query search
    #-----------------------------------------------
    if ($query ne "") {
		$sort_mode = "BY_POINTS_REVERSE";
		$query_quantity++;
		foreach $word ( split(/ +/,$query) ) {
			#
			#----------------------------------
			# start
			#----------------------------------
			$word = trim($word);
			if ($word eq "") {next}
			$word_int = &clean_int($word);
			#
			#----------------------------------
			# select conexts
			#----------------------------------
			$context_name 		= 0;
			$context_email		= 0;
			$context_service_id	= 0;
			$context_ani		= 0;
			$context_dst		= 0;
			if (index("\U$word","ANI=") eq 0) {
				$context_ani = 1;
				$word=substr($word,4,100);
			} elsif (index("\U$word","DST=") eq 0) {
				$context_dst = 1;
				$word=substr($word,4,100);
			} elsif (index("\U$word","NAME=") eq 0) {
				$context_name = 1;
				$word=substr($word,5,100);
			} elsif (index("\U$word","EMAIL=") eq 0) {
				$context_email = 1;
				$word=substr($word,6,100);
			} elsif (index("\U$word","SERVICEID=") eq 0) {
				$context_service_id = 1;
				$word=substr($word,4,100);
			} else {
				if ($word eq $word_int) {
					$context_service_id = 1;
					$context_dst = (length($word_int)>=4) ? 1 : $context_dst;
					$context_ani = (length($word_int)>=4) ? 1 : $context_ani;
				} else {
					$context_name = 1;
					$context_email = 1;
				}
			}
$dddd .= "($word) - ($word_int) - name=$context_name email=$context_email	service_id=$context_service_id ani=$context_ani dst=$context_dst <br>";
			#----------------------------------
			# query each conext
			#----------------------------------
			#
			# name
			if ($context_name eq 1) {
				%list = database_select_as_hash("SELECT id,1 FROM service where name like \"\%$word\%\" order by creation_date desc limit 0,1000 ","flag");
				foreach $id (keys %list) { $selected_services{$id}{p}++;$selected_services{$id}{q}=1;}
			}
			# email 
			if ($context_email eq 1) {
				%list = database_select_as_hash("SELECT id,1 FROM service where email like \"\%$word\%\" order by creation_date desc limit 0,1000 ","flag");
				foreach $id (keys %list) { $selected_services{$id}{p}++;$selected_services{$id}{q}=1;}
				%list = database_select_as_hash("SELECT id,1 FROM service where email='$word' order by creation_date desc limit 0,100 ","flag");
				foreach $id (keys %list) { $selected_services{$id}{p} +=100;$selected_services{$id}{q}=1;}
			}
			# service_id
			if ($context_service_id eq 1) {
				%list = database_select_as_hash("SELECT id,1 FROM service where id='$word'","flag");
				foreach $id (keys %list) { $selected_services{$id}{p} +=1000;$selected_services{$id}{q}=1;}
			}
			# query ani
			if ($context_ani eq 1) {
				if (index($word,"~") eq 0)  {
					$sql = "SELECT service_id,ani,1 FROM service_ani where ani like \"\%$word_int\%\" limit 0,1000 ";
					$tmp=10;
				} else {
					$sql = "SELECT service_id,ani,1 FROM service_ani where ani like \"$word_int\%\" limit 0,1000 ";
					$tmp=1000;
				}
$dddd .= "ANI query - $sql<br>";
				%list = database_select_as_hash($sql,"ani,flag");
				foreach $id (keys %list) {
$dddd .= "ANI query - $id - $list{$id}{ani} - $list{$id}{flag}<br>";
					$selected_services{$id}{p} +=$tmp;
					$selected_services{$id}{q} =1;
					$selected_services_ani{$id}=$list{$id}{ani};
				}
			}
			# query dst
			if ($context_dst eq 1) {
				if (index($word,"~") eq 0)  {
					$sql = "
					select service_id,dst,count(*) 
					from calls_log
					where datetime_start>date_sub(now(),interval 30 day) and dst like \"\%$word_int\%\"
					group by service_id,dst
					limit 0,1000
					";
					$tmp=10;
				} else {
					$sql = "
					select service_id,dst,count(*) 
					from calls_log
					where datetime_start>date_sub(now(),interval 30 day) and dst like \"$word_int\%\"
					group by service_id,dst
					limit 0,1000
					";
					$tmp=1000;
				}
$dddd .= "DST query - $sql<br>";
				%list = database_select_as_hash_with_auto_key($sql,"service_id,dst,flag");
				foreach $id (keys %list) {
$dddd .= "DST query - $id - $list{$id}{service_id} - $list{$id}{dst} - $list{$id}{flag}<br>";
					$selected_services{$list{$id}{service_id}}{p} +=$tmp;
					$selected_services{$list{$id}{service_id}}{q} =1;
					$selected_services_dst{$list{$id}{service_id}}{$list{$id}{dst}} += $list{$id}{flag}
				}
			}
		}
	}
    #
    #-----------------------------------------------
    # filters search
    #-----------------------------------------------
	foreach $index (1..4) {
		$filter = clean_str(substr($form{"filter_$index"},0,256),"\@.-_()<> ");
		$sql=""; 
		if ($filter eq "master_flag_invited"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('invited',tags)>0 	and service.status=service_status.id"; }
		if ($filter eq "master_flag_active"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('active',tags)>0 	and service.status=service_status.id"; }
		if ($filter eq "master_flag_disabled"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('disabled',tags)>0 	and service.status=service_status.id"; }
		if ($filter eq "master_flag_ianda"			) { $sql="SELECT service.id,1 FROM service_status,service where (FIND_IN_SET('invited',tags)>0 	or FIND_IN_SET('active',tags)>0) 	and service.status=service_status.id"; }

		if ($filter eq "flag_calls_true"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_calls',tags)>0 		and service.status=service_status.id"; }
		if ($filter eq "flag_calls_false"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_no_calls',tags)>0 	and service.status=service_status.id"; }
		if ($filter eq "flag_calls_unknown"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_no_calls',tags)=0 	and FIND_IN_SET('with_calls',tags)=0 	and service.status=service_status.id"; }

		if ($filter eq "flag_recharge_true"			) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_recharge',tags)>0 	and service.status=service_status.id"; }
		if ($filter eq "flag_recharge_false"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_no_recharge',tags)>0 	and service.status=service_status.id"; }
		if ($filter eq "flag_recharge_unknown"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('with_no_recharge',tags)=0 	and FIND_IN_SET('with_recharge',tags)>04and service.status=service_status.id"; }

		if ($filter eq "flag_suspicious_yes"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('suspicious',tags)>0 		and service.status=service_status.id"; }
		if ($filter eq "flag_suspicious_good"		) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('not_suspicious',tags)>0 	and service.status=service_status.id"; }
		if ($filter eq "flag_suspicious_unknown"	) { $sql="SELECT service.id,1 FROM service_status,service where FIND_IN_SET('not_suspicious',tags)=0 	and FIND_IN_SET('suspicious',tags)=0  	and service.status=service_status.id"; }

		if ($filter eq "balance_negative"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) < 0 "; 	}
		if ($filter eq "balance_zero"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) = 0 "; 	}
		if ($filter eq "balance_less_1"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 1 ";	}
		if ($filter eq "balance_less_5"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 5 "; 	}
		if ($filter eq "balance_less_10"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 10 "; 	}
		if ($filter eq "balance_less_20"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 20 "; 	}
		if ($filter eq "balance_less_50"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) <= 50 "; 	}
		if ($filter eq "balance_more_0"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 0 "; 	}
		if ($filter eq "balance_more_1"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 1 "; 	}
		if ($filter eq "balance_more_5"				) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 5 "; 	}
		if ($filter eq "balance_more_10"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 10 ";	}
		if ($filter eq "balance_more_20"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 20 "; 	}
		if ($filter eq "balance_more_50"			) { $sql="SELECT id,1 FROM service where (balance-service.limit) > 50 "; 	}

		if ($filter eq "creation_date_7days"		) { $sql="SELECT id,1 FROM service where creation_date>date_sub(now(),interval 7 day) "; }
		if ($filter eq "creation_date_15days"		) { $sql="SELECT id,1 FROM service where creation_date>date_sub(now(),interval 15 day) "; }
		if ($filter eq "creation_date_30days"		) { $sql="SELECT id,1 FROM service where creation_date>date_sub(now(),interval 30 day) "; }
		if ($filter eq "creation_date_60days"		) { $sql="SELECT id,1 FROM service where creation_date>date_sub(now(),interval 60 day) "; }

		if ($filter eq "last_100"					) { $sql="SELECT id,1 FROM service order by id desc limit 0,100 "; }
		if ($filter eq "last_200"					) { $sql="SELECT id,1 FROM service order by id desc limit 0,200 "; }
		if ($filter eq "last_500"					) { $sql="SELECT id,1 FROM service order by id desc limit 0,500 "; }
		if ($filter eq "last_1000"					) { $sql="SELECT id,1 FROM service order by id desc limit 0,1000 "; }

		if ($filter eq "last_call_7days"			) { $sql="SELECT target,1 FROM service_data where name='stat_last_call_ts' and value>unix_timestamp(date_sub(now(),interval 7 day)) "; }
		if ($filter eq "last_call_15days"			) { $sql="SELECT target,1 FROM service_data where name='stat_last_call_ts' and value>unix_timestamp(date_sub(now(),interval 15 day)) "; }
		if ($filter eq "last_call_30days"			) { $sql="SELECT target,1 FROM service_data where name='stat_last_call_ts' and value>unix_timestamp(date_sub(now(),interval 30 day)) "; }
		if ($filter eq "last_call_60days"			) { $sql="SELECT target,1 FROM service_data where name='stat_last_call_ts' and value>unix_timestamp(date_sub(now(),interval 60 day)) "; }

		if (index($filter,"status_") eq 0) {
			$tmp = clean_int($filter);
			$sql="SELECT id,1 FROM service where status=$tmp";
		}

		if (index($filter,"tag_") eq 0) {
			$tmp = clean_int($filter);
			$sql="SELECT service_id,1 FROM service_tag where tag_string_id=$tmp";
		}

		#if ($filter eq ""	) { $sql=""; }
		#$debuug .= "$index - $filter - $sql<br>";
		if ($sql ne "") { 
			$query_quantity++;
			%list = database_select_as_hash($sql);
			foreach $id (keys %list) {
				$selected_services{$id}{p} += 1;
				$selected_services{$id}{q} += 1;
			}
		}
	}
    #
    #-----------------------------------------------
    # clean non used services
    #-----------------------------------------------
	foreach $id (keys %selected_services) {
		if ($selected_services{$id}{q} < $query_quantity) {
			delete $selected_services{$id};
		}
	}
    #-----------------------------------------------
    #
    #
    #-----------------------------------------------
    # desvia pra email se necessario
    #-----------------------------------------------
    if ($form{email} eq "1"){
	    @selected_services_ids		= (keys %selected_services);
		$selected_services_ids_raw	= join(",",@selected_services_ids);
		%selected_emails = ();
		if ($selected_services_ids_raw ne "") {
			# query os dados
			$sql = "
			select id,email
			from service
			where 
			service.id in ($selected_services_ids_raw)
			";
			%hash = database_select_as_hash($sql);
			foreach (keys %hash) {
				if ($hash{$_} eq "") {next}
				$selected_emails{$hash{$_}}++;
			}
		}
		$form{email_to} = "";
		$qtd=0;
		foreach (sort keys %selected_emails) {$form{email_to} .= "$_\n";$qtd++;}
		%t = ();
		$t{dic}{my_url}		= $my_url;
		$t{dic}{title}		= "Send email";
		$t{dic}{content}	= qq[
		Please wait...
		<form action=OLD.email.send.cgi method=post>
			<div style="display:none;">
				<textarea name=email_to style="width:300px; height:300px;">$form{email_to}</textarea>
				<br>
				$qtd emails<br>
				<a href=javascript:history.back()>Go back</a>
				<br>
				<input type=submit value="... or click here">
				<input type=hidden name=action value=send>
			</div>
		</form>
		<script>document.forms[0].submit();</script>
		];
		&template_print("template.html",%t);
		return;
    }
    #-----------------------------------------------
    #
    #
    #-----------------------------------------------
    # monta paginacao
    #-----------------------------------------------
	$page_size	= clean_int($form{page_size});
	$page_size	= ($page_size eq "") ? 10 : $page_size;
	$quantity 	= keys %selected_services;
	$page_min	= 1;
	$page_max	= int(($quantity-1)/$page_size)+1;
	$page_max	= ($page_max<$page_min) ? $page_min : $page_max;
	$page 		= clean_int($form{page});
	$page 		= ($form{next} eq 1) ? $page+1 : $page;
	$page 		= ($form{previous} eq 1) ? $page-1 : $page;
	$page 		= ($page<$page_min) ? $page_min : $page;
	$page 		= ($page>$page_max) ? $page_max : $page;
	$selected_services_start	= ($page-1)*$page_size;
	$selected_services_stop		= $selected_services_start+($page_size-1);
	if ($sort_mode eq "BY_KEY_REVERSE") {
	    @selected_services_ids		= (sort{$b <=> $a} keys %selected_services)[$selected_services_start..$selected_services_stop];
	} elsif ($sort_mode eq "BY_POINTS_REVERSE") {
	    @selected_services_ids		= (sort{$selected_services{$b}{p} <=> $selected_services{$a}{p} } keys %selected_services)[$selected_services_start..$selected_services_stop];
	} else {
	    @selected_services_ids		= (sort{$a <=> $b} keys %selected_services)[$selected_services_start..$selected_services_stop];
	}
	$selected_services_ids_raw	= join(",",@selected_services_ids);
	@selected_services_ids 		= ();
	foreach (split(/\,/,$selected_services_ids_raw)) {
		if($_ eq "") {next}
		@selected_services_ids = (@selected_services_ids,$_);
	}
	$selected_services_ids_raw	= join(",",@selected_services_ids);
    #
    #
    #-----------------------------------------------
    # QUERY os dados dos selecionados
    #-----------------------------------------------
    %services_data = ();
	# pega dados dos servicos
	if ($selected_services_ids_raw ne "") {
		# query os dados
		$sql = "
		select service.id,service.name,service.email,service_status.name,service.balance,service.limit
		from service,service_status 
		where 
		service.status = service_status.id and  
		service.id in ($selected_services_ids_raw) 
		";
		%services_data = database_select_as_hash($sql,"name,email,status,balance,limit");
		foreach $id (@selected_services_ids) {
			$services_data{$id}{service} = "ZenoFon";
			$services_data{$id}{ani} = (exists($selected_services_ani{$id})) ? &format_E164_number($selected_services_ani{$id},"USA") : " ";
			if (exists($selected_services_dst{$id})) {
				foreach $number (keys %{$selected_services_dst{$id}}) {
					$services_data{$id}{dst} .= &format_E164_number($number,"E164");
					$services_data{$id}{dst} .= ($selected_services_dst{$id}{$number}>1) ? " (".$selected_services_dst{$id}{$number}."x)" : "";
					$services_data{$id}{dst} .= "<br>";
				}
			}
			if ($services_data{$id}{dst} ne "") { $services_data{$id}{dst} =substr($services_data{$id}{dst},0,-4);}
			$sql = "
			select
				1,1,action_log_type.title
			from
				action_log,action_log_type
			where 
				action_log.type = action_log_type.id and 
				action_log.type like \"suspicious:\%\" and 
				action_log.service_id=\"$id\"
			order by
				action_log.id desc
			limit 0,1
			";
			%tmp_hash = database_select_as_hash($sql,"flag,value");
			$services_data{$id}{last_suspicious} = ( ($tmp_hash{1}{flag} eq 1) && ($tmp_hash{1}{value} ne "") ) ? $tmp_hash{1}{value} : "";
			if ($services_data{$id}{last_suspicious} eq "") {
				$sql = "
				select
					1,1,action_log_type.title
				from
					action_log,action_log_type
				where 
					action_log.type = action_log_type.id and 
					action_log.service_id=\"$id\"
				order by
					action_log.id desc
				limit 0,1
				";
				%tmp_hash = database_select_as_hash($sql,"flag,value");
				$services_data{$id}{last_suspicious} = ( ($tmp_hash{1}{flag} eq 1) && ($tmp_hash{1}{value} ne "") ) ? $tmp_hash{1}{value} : "";
			}
		}
    }
    #
    #-----------------------------------------------
    # create html dos dados dos selecionados
    #-----------------------------------------------
	$html_pg_list = "";
	foreach($page_min..$page_max) {
		$tmp = ($_ eq $page) ? "selected" : ""; 
		$html_pg_list .= "<option $tmp value=$_>Page: $_ of $page_max</option>";
	}
	
	$html_pgsize_list = "";
	$tmp = (10 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=10>10 services per page</option>";
	$tmp = (30 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=30>30 services per page</option>";
	$tmp = (100 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=100>100 services per page</option>";
	$tmp = (500 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=500>500 services per page</option>";
	
    $html_list = "";
    $html_list_empty = "<tr><td colspan=8><center><br><font color=#c0c0c0>Nothing found...</font><br>&nbsp;</center></td></tr>";
	$quantity_string = &format_number($quantity,0);
    foreach $id (@selected_services_ids) {
		if ($id eq ""){
			$html_list .= "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><tr>";
			next;
		}
		$url = "<a href='$my_url?action=view&service_id=$id'>";
		$bal = &format_number($services_data{$id}{balance}-$services_data{$id}{limit},2);
		$html_list .= qq[
	    <tr>
		<td valign=top><input type=checkbox name=$id value=1></td>
	    <td valign=top>$url$id</a></td>
	    <td valign=top>$url$services_data{$id}{name}</a>&nbsp;</td>
	    <td valign=top>$url$services_data{$id}{email}</a>&nbsp;</td>
	    <td valign=top style=white-space:nowrap;>$url$services_data{$id}{ani}</a>&nbsp;</td>
	    <td valign=top style=white-space:nowrap;>$url$services_data{$id}{dst}</a>&nbsp;</td>
	    <td valign=top>$url$services_data{$id}{status}</a>&nbsp;</td>
	    <td valign=top class=ar>$url\$$bal</a></td>
	    </tr>
		];
	    #<td valign=top>$url$services_data{$id}{status} $services_data{$id}{last_suspicious}</a>&nbsp;</td>
		$html_list_empty = "";
    }
	#
	# monta os filtros
	$select_html = "";
	foreach $index (1..4) {
		%select_filter=();
		$select_filter{$form{"filter_".$index}} = "selected";

		$select_html .= qq[
		<select name=filter_$index style="width:100%" >
		<option value=""></option>
		<option value="">Select by status</option>
		];
		%hash = database_select_as_hash("SELECT id,name,text,deleted FROM service_status ","name,text,deleted");
		foreach $id (sort{$a <=> $b} keys %hash) {
			if ($hash{$id}{deleted} eq 1) {next}
			$tmp = ("status_".$id eq $form{"filter_".$index}) ? "selected" : "";
			$select_html .= "<option $tmp value=status_$id>&nbsp;&nbsp;-&nbsp;$hash{$id}{name}</a>";
		}

		$select_html .= qq[
		<option value=""></option>
		<option value="">Select by Tag</option>
		];
	    %hash = database_select_as_hash("SELECT id,tag FROM service_tag_string");
		foreach $id (sort{$hash{$a} cmp $hash{$b}} keys %hash) {
			$tmp = ("tag_".$id eq $form{"filter_".$index}) ? "selected" : "";
			$select_html .= "<option $tmp value=tag_$id>&nbsp;&nbsp;-&nbsp;with tag $hash{$id}</a>";
		}

		$select_html .= qq[
		<option value=""></option>
		<option value="">By status type</option>
		<option $select_filter{master_flag_invited} 	value=master_flag_invited 		>&nbsp;&nbsp;-&nbsp;Invited services</option>
		<option $select_filter{master_flag_active}  	value=master_flag_active		>&nbsp;&nbsp;-&nbsp;Active services</option>
		<option $select_filter{master_flag_disabled} 	value=master_flag_disabled		>&nbsp;&nbsp;-&nbsp;Disabled services</option>
		<option $select_filter{master_flag_ianda} 		value=master_flag_ianda			>&nbsp;&nbsp;-&nbsp;Invited or active services</option>
		<option value=""></option>
		<option value="">By suspicious flag</option>
		<option $select_filter{flag_suspicious_yes}  	value=flag_suspicious_yes		>&nbsp;&nbsp;-&nbsp;Flaged as suspicious</option>
		<option $select_filter{flag_suspicious_good} 	value=flag_suspicious_good		>&nbsp;&nbsp;-&nbsp;Flaged as not suspicious (good client)</option>
		<option $select_filter{flag_suspicious_unknown} value=flag_suspicious_unknown	>&nbsp;&nbsp;-&nbsp;Not flaged as suspicious or good client</option>
		<option value=""></option>
		<option value="">By recharge status (beta)</option>
		<option $select_filter{flag_recharge_true}  	value=flag_recharge_true		>&nbsp;&nbsp;-&nbsp;With Credit Card recharge </option>
		<option $select_filter{flag_recharge_false} 	value=flag_recharge_false		>&nbsp;&nbsp;-&nbsp;Without credit card recharge</option>
		<option $select_filter{flag_recharge_unknown} 	value=flag_recharge_unknown		>&nbsp;&nbsp;-&nbsp;I dont know if has credit card recharge</option>
		<option value=""></option>
		<option value="">By balance</option>
		<option $select_filter{balance_negative}  	value=balance_negative	>&nbsp;&nbsp;-&nbsp;Services with balance negative</option>
		<option $select_filter{balance_zero} 		value=balance_zero		>&nbsp;&nbsp;-&nbsp;Services with balance zero</option>
		<option $select_filter{balance_less_1}  	value=balance_less_1	>&nbsp;&nbsp;-&nbsp;Services with balance \$1 or less</option>
		<option $select_filter{balance_less_5}  	value=balance_less_5	>&nbsp;&nbsp;-&nbsp;Services with balance \$5 or less</option>
		<option $select_filter{balance_less_10}  	value=balance_less_10	>&nbsp;&nbsp;-&nbsp;Services with balance \$10 or less</option>
		<option $select_filter{balance_less_20}  	value=balance_less_20	>&nbsp;&nbsp;-&nbsp;Services with balance \$20 or less</option>
		<option $select_filter{balance_less_50}  	value=balance_less_50	>&nbsp;&nbsp;-&nbsp;Services with balance \$50 or less</option>
		<option $select_filter{balance_more_0}  	value=balance_more_0	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$0 </option>
		<option $select_filter{balance_more_1}  	value=balance_more_1	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$1 </option>
		<option $select_filter{balance_more_5}  	value=balance_more_5	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$5 </option>
		<option $select_filter{balance_more_10}  	value=balance_more_10	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$10 </option>
		<option $select_filter{balance_more_20}  	value=balance_more_20	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$20 </option>
		<option $select_filter{balance_more_50}  	value=balance_more_50	>&nbsp;&nbsp;-&nbsp;Services with balance more than \$50 </option>
		<option value=""></option>
		<option value="">By creation date</option>
		<option $select_filter{creation_date_7days} 	value=creation_date_7days 	>&nbsp;&nbsp;-&nbsp;Services with 7 days old</option>
		<option $select_filter{creation_date_15days}	value=creation_date_15days 	>&nbsp;&nbsp;-&nbsp;Services with 15 days old</option>
		<option $select_filter{creation_date_30days}	value=creation_date_30days 	>&nbsp;&nbsp;-&nbsp;Services with 30 days old</option>
		<option $select_filter{creation_date_60days}	value=creation_date_60days 	>&nbsp;&nbsp;-&nbsp;Services with 60 days old</option>
		<option value=""></option>
		<option value="">New services</option>
		<option $select_filter{last_100} 	value=last_100  >&nbsp;&nbsp;-&nbsp;Last 100 recent services</option>
		<option $select_filter{last_200} 	value=last_200  >&nbsp;&nbsp;-&nbsp;Last 200 recent services</option>
		<option $select_filter{last_500} 	value=last_500  >&nbsp;&nbsp;-&nbsp;Last 500 recent services</option>
		<option $select_filter{last_1000} 	value=last_1000 >&nbsp;&nbsp;-&nbsp;Last 1000 recent services</option>
		<option value=""></option>
		<option value="">By last call date</option>
		<option $select_filter{last_call_7days} 	value=last_call_7days	>&nbsp;&nbsp;-&nbsp;Last call was 7 days old</option>
		<option $select_filter{last_call_15days} 	value=last_call_15days	>&nbsp;&nbsp;-&nbsp;Last call was 15 days old</option>
		<option $select_filter{last_call_30days} 	value=last_call_30days	>&nbsp;&nbsp;-&nbsp;Last call was 30 days old</option>
		<option $select_filter{last_call_60days} 	value=last_call_60days	>&nbsp;&nbsp;-&nbsp;Last call was 60 days old</option>
		<option value=""></option>
		<option value="">By call status (beta)</option>
		<option $select_filter{flag_calls_true} 		value=flag_calls_true			>&nbsp;&nbsp;-&nbsp;With calls</option>
		<option $select_filter{flag_calls_false}  		value=flag_calls_false			>&nbsp;&nbsp;-&nbsp;With no calls</option>
		<option $select_filter{flag_calls_unknown} 		value=flag_calls_unknown		>&nbsp;&nbsp;-&nbsp;I dont known if has calls or not</option>
		];


		$select_html .= qq[
		<option value=""></option>
		</select><br>
		];
	}
    #
    # print page
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Services</a> &#187; Search";
    $t{dic}{content}	= qq[
	
	<style>
	input {width:150px}
	</style>


	<form action=$my_url>
	<table border=0 colspan=0 cellpadding=2 cellspacing=0 class=clear>
		<td valign=top style="width:220px">
			Search for:<br>
			<input  name=query  style="width:100%;" value="$form{query}" ><br>
			<font color=#c0c0c0 style="line-height:120%; letter-spacing:-1px; font-size:11px">Type name, email, ANI/DST number or service id. You can type fragment or complete information. For ANI/DST number use E164 (country, area, number) format. DST numbers search calls only 30 days in the past</font>
		</td>
		<td valign=top style="width:300px">
			Filter by:<br>
			$select_html 
		</td>
		<td valign=top >
		&nbsp;<br>
		<button type=submit class="button button_positive button_search" style="width:80px;margin-left:3px;" name=submit_button>Search</button><br>
		<button type=button class="button button_negative button_search_reset" style="width:80px;margin-left:3px;margin-top:3px;" onclick="window.location='$my_url'">Reset</button><br>
		</td>
		<td>
	</table>

	<input type=hidden name=action value=search>
	<br>

	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% onclick="sortColumn(event)">
	    <thead>
			<tr>
			<td >&nbsp;</td>
			<td >ID</td>
			<td>Name</td>
			<td>Email</td>
			<td>ANI</td>
			<td>DST</td>
			<td>Status / last action</td>
			<td>Balance</td>
			</tr>
	    </thead>
	    <tbody>
			$html_list
			$html_list_empty
	    </tbody>
		<tfoot>
			<tr><td colspan=8 >
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
				<td ><button type=submit name=previous value=1><img src=/design/icons/bullet_arrow_left.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
				<td ><select name=page onchange="document.forms[0].submit()">$html_pg_list</select></td>
				<td ><select name=page_size onchange="document.forms[0].submit()">$html_pgsize_list</select></td>
				<td ><button type=submit name=next value=1><img src=/design/icons/bullet_arrow_right.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
				<td >($quantity_string services found)</td>
			</table>
			</td></tr>
		</tfoor>
	</table>
	
	
	
	
	
	<br>
		For selected services: 
		<button type=button onclick=multiple_services_action('tags_select_multiple')>Edit tags</button>
		<button type=button onclick=multiple_services_action('status_edit_multiple')>Edit status</button>
		<button type=button onclick=multiple_services_action_email()>Send email</button>
		<br><br>
		For all $quantity_string services: <button name=email type=submit value=1>Send email</button>
	</form>



	<script>
	function multiple_services_action_email(){
		myform 					= document.forms[0];
		elementsQuantity 		= myform.elements.length;
		elementsSelectedIds 	= "";
		elementsSelectedQuantity= 0;
		for (i=0; i<elementsQuantity; i++){
			if (myform.elements[i].type=="checkbox"){
				if (myform.elements[i].checked){
					elementsSelectedIds = elementsSelectedIds+myform.elements[i].name+",";
					elementsSelectedQuantity++;
				}
			}
		}
		if (elementsSelectedQuantity > 0) {
			url = "OLD.email.send.cgi?action=send&service_ids="+elementsSelectedIds;
			window.location=url
		} else {
			alert("Plaese select one or more services");
		}
	}
	function multiple_services_action(action){
		myform 					= document.forms[0];
		elementsQuantity 		= myform.elements.length;
		elementsSelectedIds 	= "";
		title					= "Edit multiple services"
		if (action == "tags_select_multiple") { title = "Edit tags for multiple services"}
		if (action == "status_edit_multiple") { title = "Edit status for multiple services"}
		elementsSelectedQuantity= 0;
		for (i=0; i<elementsQuantity; i++){
			if (myform.elements[i].type=="checkbox"){
				if (myform.elements[i].checked){
					elementsSelectedIds = elementsSelectedIds+myform.elements[i].name+",";
					elementsSelectedQuantity++;
				}
			}
		}
		if (elementsSelectedQuantity > 0) {
			modal_open(
			title,
			"$my_url?action="+action+"&service_ids="+elementsSelectedIds,
			400,
			300
			);
		} else {
			alert("Plaese select one or more services");
		}
	}
	</script>

	<script>
	document.forms[0].elements[0].focus();
	</script>


    ];
    &template_print("template.html",%t);
}
sub do_clients_export(){
	#
	#---------------------------------------
	# print
	#---------------------------------------
	$t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url?remember=1>Services</a> &#187; Export";
	$t{dic}{content} = qq[

	lets start

	];
	&template_print("template.html",%t);
}
#========================================================================
 
 sub get_statushtml(){
	local($uigroup,$namegrp,$filter_index) = @_;
	local(%data);
	
	%data = ();
	 local ($select_html,$select_html1,$value_list,$tmp) ;
	 
	 $filter_value = $form{'filter_'.$filter_index};
	 	
     $select_html = "";
 	 $select_html1 = "";
 	 $value_list = ""; 
 	 
 	  %hash = database_select_as_hash(
 	 "SELECT id,name,ui_order,ui_group FROM service_status where product_id='0' and deleted=0 and ui_group='$uigroup' order by ui_group,ui_order",
 	 "name,ui_order,ui_group");

	foreach $id (sort{$hash{$a} cmp $hash{$b}} keys %hash) {
		
		$tmp ='';
		if ($filter_value eq 'status_'.$id) {
			$tmp ='selected';
		}
		 
		 $select_html .= "<option $tmp value=status_$id>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;status $hash{$id}{name}</option>";
		
			if ($value_list eq "") {
				$value_list .= $id;
			}else {
				$value_list.='_'.$id ;
			} 
	}
	
	# I feel strange ,i.e for all recharge status option value
	#the status looks like status_30_32_34_31_33,
	#but in url the filter is filter_1=status_31_33_30_32_34
	#that's different,so let's use one function to make it equal
   	$tmp ='';
   	if ($filter_value ne "") {
   		if (check_filtervalue($filter_value,'status_'.$value_list))  {
			$tmp ='selected';
		}
   	}
		
		
		
	$select_html1 .= "<option $tmp value=status_$value_list>&nbsp;&nbsp;-&nbsp;All \"".$namegrp."\" status</option>";
	$select_html1 .= $select_html ;
 
	$data{'html'} = $select_html1;

	return %data;
}

sub check_filtervalue() {
	local ($val1,$val2) = @_;
	local (%hash1,%hash2);
	%hash1 = ();
	%hash2 = ();

	if (index($val1,"status_") eq 0) {
		 	$val1 = substr($val1,7,100);
		 	@hash1 = split('_',$val1); 
			 
		}	
	if (index($val2,"status_") eq 0) {
		 
		 	$val2 = substr($val2,7,100);
		 	@hash2 = split('_',$val2); 
			 
		}	
		@hash1 = sort(@hash1);
		@hash2 = sort(@hash2);
		
		$firststring = join("_",@hash1);
		$secondstring = join("_",@hash2);
	#	debug('first:'.$firststring.'second:'.$secondstring) ;
		
		return ($firststring eq $secondstring) ;
		
			
}
 
	
 
