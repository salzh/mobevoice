#!/usr/bin/perl
require "include.cgi";

 
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (adm_security_check("can_system_config") ne 1) {adm_error("no permission"); exit;}
#=======================================================
 

#=======================================================
# main loop
#=======================================================
$folder_rrd_data	= "/usr/local/multilevel/data/rrd/";
$my_url 			= "login.cgi";
$action 			= $form{action};
if 	($action eq "login_list")			{ if (&active_user_permission_check("noc:can_manage_users") ne 1) {adm_error("no permission"); exit;}     &do_login_list();			}
elsif 	($action eq "login_edit")		{ if (&active_user_permission_check("noc:can_manage_users") ne 1) {adm_error("no permission"); exit;}     &do_login_edit();			}
elsif 	($action eq "login_add")		{ if (&active_user_permission_check("noc:can_manage_users") ne 1) {adm_error("no permission"); exit;}     &do_login_add();			}
elsif 	($action eq "login_del")		{ if (&active_user_permission_check("noc:can_manage_users") ne 1) {adm_error("no permission"); exit;}     &do_login_del();			}
elsif 	($action eq "perm_matrix")	{ if (&active_user_permission_check("noc:can_manage_users") ne 1) {adm_error("no permission"); exit;}	&do_login_perm_matrix(); 	} 

#========================================================================
else									{ if (&active_user_permission_check("noc:can_manage_users") ne 1) {adm_error("no permission"); exit;}     &do_login_list();			}
exit;
#=======================================================
 
#========================================================================
sub do_login_list(){
	#
	# pega a lista
	%hash = database_select_as_hash("select id,web_user,web_password,permission_id   from adm_users  ","web_user,web_password,permission_id");
    %perm_list 		= &database_select_as_hash("select id,name from adm_users_permissions ","name");
 
	$html_list = "<table class=fields_group_table border=0 colspan=0 cellpadding=0 cellspacing=0>";
	$html_list .= "<tr><td>User</td><td>Password</td><td>Permission</td><td>Action</td></tr>";
    foreach $id (sort{ $hash{$a}{ui_order} <=> $hash{$b}{ui_order}} keys %hash) {
		$html_list .= "<tr>";
		$html_list .= "<td width=120 >".$hash{$id}{web_user}."</td>"; 
		$html_list .="<td width=120 >". $hash{$id}{web_password}."</td>" ; 
		$html_list .="<td width=240 >". $perm_list{$hash{$id}{permission_id}}{name}."</td>" ;  
	 	$html_list .= "<td width=120 >";
	 	$html_list .= "<a href=$my_url?action=login_edit&id=$id onClick=\"modal_open(\'Edit Login\',\'$my_url?action=login_edit&id=$id\',300,360); return false;\">Edit</a>";
		$html_list .= "| <a href=$my_url?action=login_del&id=$id onClick=\"modal_open(\'Delete Login\',\'$my_url?action=login_del&id=$id\',300,360); return false;\">Del</a>";
	
		$html_list .= "</td>";	   
		$html_list .= "</tr>";
	}
	$html_list .="</table>" ;  
	$html_list .= "<a href=$my_url?action=login_add onClick=\"modal_open(\'Add Login\',\'$my_url?action=login_add\',300,360); return false;\">Add New</a>"; 
	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    #
    # print page
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Login</a>";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Login";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}	= qq[
	<div class=clear style=width:700px>
		<fieldset class=config_select_list><legend>Login</legend>
		<ul>
		$html_list
		</ul>
		</fieldset>
	</div>
    ];
	#foreach(170..400) {$t{dic}{content}	.= qq[$_ = &#$_;<br>];}
    &template_print("template.html",%t);
	
}
sub do_login_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $status_id = clean_int(substr($form{id},0,100));
    %hash = database_select_as_hash("select 1,1,web_user,web_password,permission_id  from adm_users where id='$status_id' ","flag,web_user,web_password,permission_id");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{dic}{content} = "Invalid parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
	
	#---------------------------------------------------
	# get age status title
	#---------------------------------------------------
    $web_user  = $hash{1}{web_user} ;
    $web_password = $hash{1}{web_password} ;
	$permission_id = $hash{1}{permission_id} ;
        
  	$html_select = "";
    %perm_list 		= &database_select_as_hash("select id,name from adm_users_permissions ","name");
	foreach $id (sort{$a  <=>  $b } keys %perm_list) {		 
			$tmp =   ($permission_id eq $id)   ? "selected" : ""; 
			$html_select .= "<option value='".$id."' $tmp > ".$perm_list{$id}{name}."</option>";
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
		 if ($form{web_user} eq "") {
			$form_ok = 0;
			$form_message = "Please input username <br><br>";
			$form{web_user} = "";
		}
		elsif   ($form{web_password} eq "")      { 
			$form_ok = 0;
			$form_message = "Please input password <br><br>";
			$form{web_password} = "";
		 	
		}else {
			$form_ok = 1;
		} 
		
	}
	#
 
	$form{web_user}	= &database_escape($form{web_user});
	$form{web_password}	= &database_escape($form{web_password});
	$form{permission_id} = &database_escape($form{permission_id});
	 
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&database_do("update adm_users set web_user ='$form{web_user}',web_password ='$form{web_password}',permission_id='$form{permission_id}'   where id='$status_id' ");
		&action_history("noc:config:login:edit",('id'=>$status_id,'adm_user_id'=>$app{session_cookie_u}));
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
		$form{web_user} = $web_user;
		$form{web_password} = $web_password ;
		$form{permission_id} = $permission_id ;
	 
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
 
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[
	Change Login 
	<br>
	<br>
	<form action=$my_url>
	 Username
	 <br>
	 <input name="web_user" value="$form{web_user}" /><br>
	 Password <br>
	 <input name="web_password" value="$form{web_password}" /><br>
	 Permission <br>
	 <select name="permission_id" >
		 $html_select
	 </select>
	 <br>
	 
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=id value=$status_id>
	<input type=hidden name=action value=login_edit>
    ];
    &template_print("template.modal.html",%t);
}
sub do_login_add(){
   
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
		if ($form{web_user} eq "") {
			$form_ok = 0;
			$form_message = "Please input username <br><br>";
			$form{web_user} = "";
		}
		elsif   ($form{web_password} eq "")      { 
			$form_ok = 0;
			$form_message = "Please input password <br><br>";
			$form{web_password} = "";
		 	
		}else {
			$form_ok = 1;
		} 
		
	}
	$form{web_user}	= &database_escape($form{web_user});
	$form{web_password}	= &database_escape($form{web_password});
	$form{permission_id} = &database_escape($form{permission_id});
	
	if ($form{permission_id} eq "") {
		$form{permission_id} = 2;
		
	}
	 
	 
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		&database_do("insert into adm_users(web_user,web_password,permission_id) values ('$form{web_user}','$form{web_password}','$form{permission_id}')");
		&action_history("noc:config:login:add",('title'=>$form{web_user},'adm_user_id'=>$app{session_cookie_u}));
		%t = ();
	    $t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	    &template_print("template.modal.html",%t);
		exit;
	}
	
	$html_select = "";
    %perm_list 		= &database_select_as_hash("select id,name from adm_users_permissions ","name");
	foreach $id (sort{$a  <=>  $b } keys %perm_list) {		 
			$tmp =   ($form{permission_id} eq $id)   ? "selected" : ""; 
			$html_select .= "<option value='".$id."' $tmp > ".$perm_list{$id}{name}."</option>";
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
	Add Login
	<br>
	<br>
	<form action=$my_url>
	 Username
	 <br>
	 <input name="web_user" value="$form{web_user}" /><br>
	Password <br>
	 <input name="web_password" value="$form{web_password}" /><br>
	 Permission <br>
	 <select name="permission_id" >
		 $html_select
	 </select>
	 <br>
	 
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Save</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=action value=login_add>
    ];
    &template_print("template.modal.html",%t);
}
sub do_login_del(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $status_id = clean_int(substr($form{id},0,100));
    %hash = database_select_as_hash("select 1,1,web_user from adm_users  where id='$status_id' ","flag,web_user");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{dic}{content} = "Invalid parameter";
		&template_print("template.modal.html",%t);
		exit;
	}
	
	#---------------------------------------------------
	# get age status title
	#---------------------------------------------------
    $title  = $hash{1}{web_user} ;
    
     
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
		&database_do("delete from  adm_users where id='$status_id' ");
		&action_history("noc:config:login:del",('id'=>$status_id,'adm_user_id'=>$app{session_cookie_u}));
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
		$form{web_user} = $web_user;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
 
    $t{dic}{my_url}	= $my_url;
    $t{dic}{content}	= qq[
	Delete Login
	<br>
	<br>
	<form action=$my_url>
	 Are you sure to delete this login information ? 
	<br>
	<br>
	 
	<font color=red><b>$form_message</b></font>
	<button type=button onclick=parent.modal_close()><img src=/design/icons/delete.png align=left>Cancel</button>
	<button type=submit><img src=/design/icons/tick.png align=left>Delete</button>
	<input type=hidden name=save value=1>
	<input type=hidden name=id value=$status_id>
	<input type=hidden name=action value=login_del>
    ];
    &template_print("template.modal.html",%t);
}
 
sub do_login_perm_matrix(){
	#
	#===========================================================================
	# pega data
	#===========================================================================
	$product_id = "";
	 
	#
	@status_dic_list = qw(can_view_pin  can_view_email can_login_as_service
	can_manage_users profile_edit can_manage_rate can_manage_services can_manage_checks
	 can_manage_status can_manage_commissions can_manage_coupons  can_send_email can_view_reports
	 can_email_edit can_edit_pages  can_edit_pages_help can_read_help can_write_help can_read_tickets
	 can_read_work );
	$status_dic_string = join(",",@status_dic_list);
	$sql = "
	SELECT id,name ,ui_order,$status_dic_string
	FROM adm_users_permissions 
	";
	
	%status_list = database_select_as_hash($sql,'name,ui_order,'.$status_dic_string);
 
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
				$form_sql{$status_id} ="update adm_users_permissions set " ;
				#-----------------------------------
				# check integer (non blank)
				#----------------------------------- \
				$tmp_sql  = "" ;
				foreach $dic_name (@status_dic_list)  { 
					$form_item_name 	= "dic:$dic_name:$status_id";
					unless(exists($form{$form_item_name})) {next}
					$form_item_value	= &trim(substr($form{$form_item_name},0,255));
					if (&form_check_integer($form_item_value) eq 1) {
						$tmp_sql .=" ".$dic_name."=".&clean_int($form_item_value).",";
						#$form_sql{$form_item_name} = "update adm_users_permissions set $dic_name='".&clean_int($form_item_value)."' where id='$status_id' ";
					} else {
						$save_is_ok = 0;
						$form_error{$form_item_name} = 1;
					}
				}
			 
				
				$tmp_sql =~s/,$//;
				$form_sql{$status_id} .= $tmp_sql ;
				
				if ($save_is_ok eq 1) {
						$form_sql{$status_id} .=" where id=".$status_id;
 				}
			}
		
		
			#
			#-----------------------------------
			# apply changes if ok
			#-----------------------------------
			if ($save_is_ok eq 1) {
				foreach (keys %form_sql) { &database_do($form_sql{$_}) }
				cgi_redirect("$my_url?action=perm_matrix");
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
	 
		#
		#---------------------------------------------------------
		# insert access settings group
		#---------------------------------------------------------
		$tmp0 = "accesss_settings";
		$form_html{$tmp0} .= $html_group."<tr>";
	    $form_html{$tmp0} .= qq[<td style='$ui_group_style'>$status_list{$status_id}{name}</td>];
	
		foreach $dic_name (@status_dic_list){
		 
				 
			 $tmp1="dic:".$dic_name.":$status_id"; 		$tmp2=$form{$tmp1}; $tmp3=($form_error{$tmp1} eq 1)?$error_style:""; $tmp4=($tmp2 eq 1)?"selected":""; 
			 $form_html{$tmp0} .= qq[<td style='$ui_group_style'><select name="$tmp1" style='$tmp3'><option $tmp4 value=0>No</option><option $tmp4 value=1>Yes</option></select></td>];
		}		
		 
		$form_html{$tmp0} .= "</tr>";
	  
	}
		$thead = "<tr><td ><h1>Access and permissions</h1></td>";
		foreach $dic_name (@status_dic_list){
			$dic_name =~ s/_/ /g ;
			$thead .= '<td width=70>'.$dic_name.'</td>';
		}		
		
		$thead.="</tr>";
	 
		
	#
	#===========================================================================
    # print page
	#===========================================================================
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Login  permissions";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "login.cgi";
    $t{breadcrumb}{1}{title}	= "Login   permissions";
    $t{breadcrumb}{1}{url}		= "";
    $click_chain = &multilevel_clickchain_set("psea");
    $t{dic}{content}	= qq[
    	<form action=$my_url method=post>


		$form_error_message 
 



	    <fieldset style="padding-top:0px;"><legend style="font:normal normal 30px Trebuchet, Trebuchet MS, Arial, sans-serif; letter-spacing:-1px; margin:0; padding:1; border:0;">Status settings</legend>
		    <div style=width:300px;margin-bottom:20px;>
		    	Login permission matrix  
			</div>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=FieldsTable xxonclick="sortColumn(event)">
		    <thead>
				 $thead
		    </thead>
		    <tbody >$form_html{accesss_settings}</tbody>
		    </table>
		    <br>
 

		</fieldset>

 
	    <br>
	    <br>

 






		<input type=hidden name=action value=perm_matrix>
		<input type=hidden name=product_id value=$product_id>
		<input type=hidden name=save value=1>
		<input type=hidden name=click_chain value=$click_chain>
		<button type=button class="cancel"	onclick="window.location='$my_url?action=perm_matrix'">Cancel</button>
		<button type=submit class="save"  	>Modify Permission Table </button>
		</tr></table>
	
		</form>
		<br>&nbsp;
    ];
    &template_print("template.html",%t);
	
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
