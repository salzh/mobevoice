#!/usr/bin/perl
require "include.cgi";


#%t = ();
#foreach(sort keys %form) {$t{dic}{content} .= qq[FORM -- $_=$form{$_}<br>];}
#foreach(sort keys %ENV) {$t{dic}{content} .= qq[ENV -- $_=$ENV{$_}<br>];}
#&template_print("template.menu.html",%t);
#exit;

#=======================================================
# main loop
#=======================================================
$my_url = "index.cgi";
$action = $form{action};
if 		($action eq "logout")			{ &do_logout(); 					} 
elsif 	($action eq "login")			{ &do_login(); 						}
elsif 	($action eq "imagecheck")		{ &imagecheck_get_image($form{id}); }
elsif 	($action eq "set_frame") 		{ if ($app{session_status} eq 1) { &do_set_frame(); 		} else {&do_login(); } }	
#elsif 	($action eq "set_frame_title") 	{ if ($app{session_status} eq 1) { &do_set_frame_title();	} else {&do_login(); } }	
elsif 	($action eq "profile") 			{ if ($app{session_status} eq 1) { &do_profile(); 			} else {&do_login(); } }	
elsif 	($action eq "dashboard") 		{ if ($app{session_status} eq 1) { &do_dashboard();			} else {&do_login(); } }	
else 									{ if ($app{session_status} eq 1) { &do_dashboard();			} else {&do_login(); } }
exit;
#=======================================================




#========================================================================
# outras acoes
#========================================================================
sub DELETE_do_index(){
	&cgi_hearder_html();
	print qq[
	<html>
		<head>
		<script>
		function update_page(){
			menu.location="$my_url?action=menu"; 
			user.location="$my_url?action=user"; 
			kb.location="knowledgebase.cgi"; 
		}
		kb_display_status = 0;
		function kb_show(){
			document.body.cols="190,300,*";
		}
		function kb_hide(){
			document.body.cols="190,0,*";
		}
		function kb_toggle(){
			if (document.body.cols!="190,0,*") {
				document.body.cols="190,0,*";
			} else {
				document.body.cols="190,300,*";
			}
		}
		</script>
		
		<title>ZenoFon - Network Operation Center</title>
		</head>
		<frameset cols="190,0,*" frameborder="0" noresize marginwidth="0" marginheight="0" name="level1">
			<frameset rows="70,*,70" frameborder="0" noresize marginwidth="0" marginheight="0" name="level2">
			<frame src="design/template.menu.logo.html" name="logo" 	scrolling="auto" 	frameborder="0" noresize marginwidth="0" marginheight="0"></FRAME>
			<frame src="$my_url?action=menu" 			name="menu" 	scrolling="auto" 	frameborder="0" noresize marginwidth="0" marginheight="0"></FRAME>
			<frame src="$my_url?action=user" 			name="user" 	scrolling="auto" 	frameborder="0" noresize marginwidth="0" marginheight="0"></FRAME>
			</frameset>
		<frame src="knowledgebase.cgi"	 		name="kb"		scrolling="auto"	frameborder="0" 		 marginwidth="0" marginheight="0"></FRAME>
		<frame src="$my_url?action=dashboard" 	name="content"	scrolling="auto"	frameborder="0" noresize marginwidth="0" marginheight="0"></FRAME>
		</frameset>
		<body>
		You need frames for better user experience. You can access <a href=$my_url?action=menu>menu</a> and/or <a href=$my_url?action=dashboard>content</a> one by one
		</body>
	</html>
	];
}
sub DELETE_do_menu(){
    %t = ();

	if ($app{session_status} eq 1)	{
		%hash = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password FROM adm_users where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password");
		$t{dic}{user_name} = ($hash{1}{name} eq "") ? "" : "<b>\"$hash{1}{name}\"</b>";

		$t{dic}{content} = qq[

		<div class=menu_group >
		<h1><a href="javascript:MyDisplay('user')" ><img src=design/icons/01-07.png hspace=0 vspace=0 border=0 width=16 height=16 style="margin-right:2px;" >$t{dic}{user_name}</a></h1>
		<div class=clear id=user>
		<a target=content href=/noc/index.cgi?action=profile>Your account</a><br>
		<a target=content href=index.cgi?action=logout onclick="return confirm('Do you really want log-out?');" >Log-out</a><br>
		</div>
		</div>

		<div class=menu_group >
		<h1><a href="javascript:MyDisplay('workgroup')" ><img src=design/icons/user_comment.png hspace=0 vspace=0 border=0 width=16 height=16 style="margin-right:2px;" >Workgroup</a></h1>
		<div class=clear id=workgroup>
		<a target=content href="/noc/forum/viewforum.php?f=4">Workgroup forum</a><br>
		<a target=content href=http://www.zenofon.com/contact/staff>Customer service</a> <a target=content href=http://www.zenofon.com/contact/admin>(adm)</a><br>
		<!-- <a xtarget=content href=# onclick="parent.kb_toggle()">Knowledgebase</a><br> -->
		</div>
		</div>

		<div class=menu_group >
		<h1><a href="javascript:MyDisplay('appservices')" ><img src=design/icons/phone_sound.png hspace=0 vspace=0 border=0 width=16 height=16 style="margin-right:2px;" >Phone services</a></h1>
		<div class=clear id=appservices>
		<a target=content href=zenofon.services.cgi?remember=1>Search services</a><br>
		<a target=content href=zenofon.services.report.cgi>Reports</a><br>
		<a target=content href=zenofon.config.cgi?action=service_status_list>Edit services status</a><br>
		<a target=content href=zenofon.checks.cgi>Commissions checks</a><br>
		Rate (<a target=content href=zenofon.product.rate.cgi>Dial-out</a>/<a target=content href=zenofon.product.rate.callback.cgi>callback</a>)<br>
		</div>
		</div>


		<div class=menu_group >
		<h1><a href="javascript:MyDisplay('website')" ><img src=design/icons/page_edit.png hspace=0 vspace=0 border=0 width=16 height=16 style="margin-right:2px;" >Website</a></h1>
		<div class=clear id=website>
		<a target=content href=/news/wp-admin/>Edit zenofon news</a><br>
		<a target=content href=zenofon.web.help.edit.cgi>Edit help topics</a><br>
		<a target=content href=zenofon.web.edit.cgi>Edit web pages</a><br>
		<a target=content href=zenofon.email.edit.cgi>Edit email message</a><br>
		</div>
		</div>

		<div class=menu_group >
		<h1><a href="javascript:MyDisplay('system')"><img src=design/icons/computer_error.png hspace=0 vspace=0 border=0 width=16 height=16 style="margin-right:2px;" >System tools</a></h1>
		<div class=clear id=system>
		<a target=content href=/noc/status/bin/index.cgi?plugin=cpu&plugin=load&plugin=processes&plugin=interface&plugin=memory&timespan=3600&action=show_selection&ok_button=OK>System status</a><br>
		<a target=content href=zenofon.config.cgi?action=system_config>System config</a><br>
		<a target=content href=zenofon.email.send.cgi>Send mass email</a><br>
		</div>
		</div>

		];
	} else {
	}
    &template_print("template.menu.html",%t);
    
}
sub do_set_frame(){
    %t = ();
    $t{title}	= $form{title};
    $t{url}		= $form{url};
    $t{breadcrumb}{1}{title}	= $form{title};
    $t{breadcrumb}{1}{url}		= "";
	&template_print("template.iframe.html",%t);
}
sub do_profile(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    %hash = database_select_as_hash("SELECT 1,1,id,name,email,gravatar_email,gravatar_url,web_user,web_password FROM adm_users where id='$app{session_cookie_u}'","flag,id,name,email,g_email,g_url,web_user,web_password");
	%user_data = %{$hash{1}};	
	#
	# save
	$error = 0;
	if ($form{save} eq 1) {
		#
		# check name
		$data = $form{name};
		$data = &clean_str(substr($data,0,255)," ()[]_-");
		if ( ($form{name} ne $data) || ($data eq "") ) {$t{dic}{msg_error_name} = 1; $error=1}
		$form{name} = $data;
		#
		# check email
		$data = $form{email};
		$data = &clean_str(substr($data,0,255),"_-");
		if ( ($form{email} ne $data) || ($data eq "") ) {$t{dic}{msg_error_email} = 1; $error=1}
		$form{email} = $data;
		#
		# check email
		$data = $form{g_email};
		$data = &clean_str(substr($data,0,255),"_-");
		if ($data ne "") {
			if ($form{g_email} ne $data) {$t{dic}{msg_error_g_email} = 1; $error=1}
		}
		$form{g_email} = $data;
		#
		# check password
		if ($form{password_action} eq 1) {
			$data0 = &clean_str(substr($form{password_active},0,255),"_-");
			$data1 = &clean_str(substr($form{password_new},0,255),"_-");
			$data2 = &clean_str(substr($form{password_retype},0,255),"_-");
			if ( (length($data1)<5) || (length($data1)>50) || ($form{password_new} ne $data1) || ($data1 eq "") || ($data1 ne $data2) ) {$t{dic}{msg_error_new_password} = 1; $error=1}
			if ( ($data0 eq "") || ($data0 ne $user_data{web_password}) ) {$t{dic}{msg_error_password} = 1; $error=1}
			$form{password} = $data1;
		}
		#
		# try to save
		if ($error eq 0) {
			$tmp = ($form{g_email} ne "") ? $form{g_email} : $form{email};
			$tmp = ($tmp eq "") ? time : $tmp;
			$gravatar_url = "http://www.gravatar.com/avatar/". md5_hex(lc $tmp) ."?d=monsterid";
			database_do("update adm_users set name='$form{name}' , gravatar_email='$form{g_email}', gravatar_url='$gravatar_url', email='$form{email}' where id='$user_data{id}' ");
			if ($form{password_action} eq 1) {
				database_do("update adm_users set web_password='$form{password}' where id='$user_data{id}' ");
			}
			$t{dic}{msg_ok} = 1;
			$form{password_action} =0;
		}
	}
	#
	# load
	if ($form{save} ne 1) {
		$form{name}		= $user_data{name};
		$form{email}	= $user_data{email};
		$form{g_email}	= $user_data{g_email};
	}
	$form{web_user}	= $user_data{web_user};
	#
	# print page
	$password_action_select	= ($form{$password_action_select} eq 1) ? "selected" : "";
	$password_action_display= ($form{$password_action_select} eq 1) ? "" : "style=display:none;";
	$msg_error 	= "";
	$msg_error 	= ($t{dic}{msg_error_name} eq 1) ? "Incorrect name<br>" : "";
	$msg_error 	= ($t{dic}{msg_error_email} eq 1) ? "Incorrect email<br>" : "";
	$msg_error 	= ($t{dic}{msg_error_new_password} eq 1) ? "incorrect new password<br>" : "";
	$msg_error 	= ($t{dic}{msg_error_password} eq 1) ? "Incorrect email<br>" : "";
	$msg_error 	= ($msg_error eq "") ? "" : "<font color=red><b>$msg_error</b></font>";
	$msg_ok 	= ($t{dic}{msg_ok} eq 1) ? "<font color=green><b>Saved.</b></font>" : "";
    $t{dic}{title}		= "My account";
    $t{dic}{content}	.= qq[
	
			<form action=index.cgi method=post style="padding-left:20px;">
			Your log-in:<br>
			<input name=web_user disabled read-only readonly value="$form{web_user}"><br>

			<br>
			Your contact name:<br>
			<input name=name value="$form{name}"><br>
			<br>
		
			Your contact email:<br>
			<input name=email value="$form{email}"><br>
			<br>
		
			Your <a href=http://en.gravatar.com/ target=_blank>gravatar</a> email:<br>
			<input name=g_email value="$form{g_email}"><br>
			<br>
		
			Your password:<br>
			<select name=password_action onchange="if (this.selectedIndex == 0) {MyDisplay('password_fields',0)} else {MyDisplay('password_fields',1)} ">
			<option value=0 >Do not change</option>
			<option value=1 $password_action_select>Change password</option>
			</select><br>
			<br>

			<div class=clear id=password_fields $password_action_display >
				Your active password:<br>
				<input type=password name=password_active value=""><br>
				<br>
				Your new password:<br>
				<input type=password name=password_new value=""><br>
				<br>
				Re-type your new password:<br>
				<input type=password name=password_retype value=""><br>
				<br>
			</div>
		
			<input type=submit value="Save"><br>
			<input type=hidden name=save value=1>
			<input type=hidden name=action value=profile>
			<br>

			$msg_error
			$msg_ok

		</form>
	];
    &template_print("template.html",%t);
}
sub do_dashboard(){
    #
 	print "location: /noc/services.cgi?remember=1\n\n";
 	exit;
	# 
	$tmp  = "index.cgi?";
	$tmp .= "action=set_frame";
	$tmp .= "&title=".&cgi_url_encode("Things to-do");
	$tmp .= "&url=".&cgi_url_encode("https://teambox.com/login");
 	print "location: $tmp\n\n";
	exit;
	#
	$li  = "index.cgi?action=set_frame&title=".&cgi_url_encode("Infrastructure task list")."&url=".&cgi_url_encode("https://teambox.com/projects/zenofon-infrastructure/task_lists");
	$lr  = "index.cgi?action=set_frame&title=".&cgi_url_encode("Zenofon radio task list")."&url=".&cgi_url_encode("https://teambox.com/projects/zenofon-radio/task_lists");
	$lc  = "index.cgi?action=set_frame&title=".&cgi_url_encode("Zenofon calls task list")."&url=".&cgi_url_encode("https://teambox.com/projects/zenofon-calls/task_lists");
	$ly  = "index.cgi?action=set_frame&title=".&cgi_url_encode("All task list")."&url=".&cgi_url_encode("https://teambox.com/task_lists");
    #
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Zenofon NOC";
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
		height:130px;
		padding-top:0px;
	}
	.local_box_info{
		float:left;
		width:230px;
		border:0px solid green;
	}
	.local_box_action{
		float:right;
		border:0px solid red;
		width:700px;
	}
	.local_box_action_inside{
	}
	</style>

	<a name=tools></a>
	<div class=local_box_info>
		<h3>Tools</h3>
		Day by day most used tools
	</div>
	<div class=local_box_action>
		<div class=local_div><fieldset class=local_fieldset><legend>Services</legend>
			<form action=/noc/services.cgi>
			<input name=query><br>
			<input type=submit value=search><br>
			</form>
			<br>
			<a target=_top href="/noc/services.cgi?remember=1"				>&#187; Remember last search</a><br>
		</fieldset></div>
		<div class=local_div><fieldset class=local_fieldset><legend>Development</legend>
	        <a target="_top" href="index.cgi?action=set_frame&title=Documentation&url=https://dev.zenofon.com/trac/zenofon/wiki">&#187; Documentation</a><br />
	        <a target="_top" href="$li">&#187; Task list: Infrastructure</a><br/>
	        <a target="_top" href="$lr">&#187; Task list: Zenofon radio</a><br/>
	        <a target="_top" href="$lc">&#187; Task list: Zenofon calls</a><br/>
	        <a target="_top" href="$ly">&#187; All Task list</a><br/>
<!--	        <a target="_top" href="index.cgi?action=set_frame&title=Test+website&url=https://test.zenofon.com/">&#187; test website</a><br /> -->
		</fieldset></div>
		<div class=local_div><fieldset class=local_fieldset><legend>Customer service</legend>
	        <a target="_top" href="index.cgi?action=set_frame&title=Customer+service&url=https://dev.zenofon.com/trac/zenofon/wiki/CustomerService">&#187; Documentation</a><br />
	        <a target="_top" href="index.cgi?action=set_frame&title=Manage+clients+tickets&url=https://tickets.zenofon.com/admin/">&#187; Manage Clients tickets</a><br />
	        <a target="_top" href="index.cgi?action=set_frame&title=Clents+ticket+form&url=https://tickets.zenofon.com/">&#187; Clients ticket form</a><br />
		</fieldset></div>
	</div>
	<br clear=both>

<hr size=1 noshade color=#c0c0c0 style="margin-top:10px; margin-bottom:20px;">

	<a name=reports></a>
	<div class=local_box_info>
		<h3>Reports</h3>
		See what is going on with system reports
	</div>
	<div class=local_box_action>
		<div class=local_div><fieldset class=local_fieldset><legend>Calls</legend>
			<a target=_top href="reports.cgi?action=calls_now"				>&#187; Calls sessions now</a><br>
			<a target=_top href="reports.cgi?action=calls_overview"			>&#187; Calls overview</a><br>
			<a target=_top href="reports.cgi?action=calls_error"			>&#187; Calls error</a><br>
			<a target=_top href="reports.cgi?action=calls_country"			>&#187; Calls per country</a><br>
			<a target=_top href="reports.cgi?action=calls_cdr"				>&#187; Calls CDR</a><br>
		</fieldset></div>
		<div class=local_div><fieldset class=local_fieldset><legend>Radio</legend>
			<a target=_top href="reports.cgi?action=radio_now"		>&#187; Radio now</a><br>
			<a target=_top href="reports.cgi?action=radio_overview"	>&#187; Radio overview</a><br>
			<a target=_top href="reports.cgi?action=radio_minutes"	>&#187; Radio minutes</a><br>
			<a target=_top href="reports.cgi?action=radio_top_radio">&#187; Top radio</a><br>
			<a target=_top href="reports.cgi?action=radio_top_listen">&#187; Top listen</a><br>
		</fieldset></div>
		<div class=local_div><fieldset class=local_fieldset><legend>System</legend>
			<a target=_top href="reports.cgi?action=history_log&display=list"	>&#187; Actions now</a><br>
			<a target=_top href="reports.cgi?action=history_log"				>&#187; Actions overview</a><br>
			<a target=_top href="reports.cgi?action=services_overview"				>&#187; Services/reachrges overview</a><br>
			<a target=_top href="reports.cgi?action=commission_contest"				>&#187; Commission contest</a><br>
			<a target=_top href="index.cgi?action=set_frame&title=Servers status&url=/noc/status/">&#187; Servers status</a><br>
		</fieldset></div>
	</div>
	<br clear=both>
	

<hr size=1 noshade color=#c0c0c0 style="margin-top:10px; margin-bottom:20px;">


	<a name=settings></a>
	<div class=local_box_info>
		<h3>Settings</h3>
		Configure all system settings 
	</div>
	<div class=local_box_action>
		<div class=local_div><fieldset class=local_fieldset><legend>Phone services</legend>
			<a target=_top href="config.cgi?action=service_status_matrix"	>&#187; Status and permissions</a><br>
			<a target=_top href="config.cgi?action=agestatus_list"			>&#187; Services age status</a><br>
			<a target=_top href="rate.cgi"									>&#187; Calls rates and routes</a><br>
			<a target=_top href="config.cgi?action=commissions"				>&#187; Commissions type</a> <a target=_top href="config.cgi?action=commissions_OLD">(old)</a><br>
			<a target=_top href="commission.checks.cgi"						>&#187; Commissions checks</a><br>
			<a target=_top href="config.cgi?action=coupons_list"			>&#187; Promotions</a><br>
		</fieldset></div>
		<div class=local_div><fieldset class=local_fieldset><legend>Radio</legend>
			<a target=_top href="radio.cgi?action=radio_gateways"			>&#187; Radio DIDs</a><br>
			<a target=_top href="radio.cgi?action=radio_stations"			>&#187; Radio stations</a><br>
			<a target=_top href="radio.cgi?action=radio_commissions_listen"	>&#187; Radio listen commissions</a><br>
			<a target=_top href="radio.cgi?action=radio_commissions_owner"	>&#187; Radio owner commissions</a><br>
			<a target=_top href="radio.cgi?action=radio_tags"				>&#187; Radio tags</a><br>
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
	</div>
	<br clear=both>&nbsp;

<script>document.forms[0].elements[0].focus();</script>


	];
    &template_print("template.html",%t);
	exit;


	#
	&cgi_redirect("services.cgi");
	exit;
	#
    %t = ();
    $t{title}	= "Today";
    $t{breadcrumb}{1}{title}	= "Workgroup";
    $t{breadcrumb}{1}{url}		= "";
    $t{breadcrumb}{2}{title}	= "Today";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}= "Today page is not finished. <br>Use top menu to navigate";
	&template_print("template.html",%t);
	exit;
	#
	# start 
    %t = ();
    $t{dic}{title}		= "Workgroup";
    $t{dic}{content}	.= qq[
    Nothing here...
	];
	&template_print("template.html",%t);
	exit;
	#
	# old old old
	$arg_array = join(" ",@_);
	#
	# get history list
	$sql = "
		SELECT
			action_log.id,
			unix_timestamp(action_log.date),
			action_log_type.title,
			action_log.service_id,
			action_log.call_debug_id,
			action_log.value_old,
			action_log.value_new
		FROM 
			action_log,
			action_log_type
		where
			action_log.type = action_log_type.id
			and action_log.adm_user_id = '$app{session_cookie_u}'
		order by
			action_log.id desc
		limit 0,100
	";
	%hash = database_select_as_hash($sql,"date,title,service_id,call_debug_id,value_old,value_new");
	$html_actions = "";
	foreach $id (sort{$b <=> $a} keys %hash){
		$title  = "";
		$title .= ($hash{$id}{call_debug_id} ne "") ? "<a href='services.cgi?service_id=$hash{$id}{service_id}&action=debug_call&service_id=2&debug_id=$hash{$id}{call_debug_id}'>" : "";
		$title .= $hash{$id}{title}." ";
		$title .= ($hash{$id}{call_debug_id} ne "") ? "</a>" : "";
		$tmp = "";
		$tmp .= ($hash{$id}{value_old} ne "") ? "old='$hash{$id}{value_old}' " : "";
		$tmp .= ($hash{$id}{value_new} ne "") ? " new='$hash{$id}{value_new}'" : "";
		$title .= ($tmp ne "") ? "($tmp) " : "";
		$date = &format_time_time($hash{$id}{date});		
		$html_actions .= "
		<tr>
		<td>$date</td>
		<td><a href='services.cgi?action=view&service_id=$hash{$id}{service_id}'>$hash{$id}{service_id}</a></td>
		<td>$title</td>
		</tr>
		";
	}
    #
    # print page
    %t = ();
    $t{dic}{title}		= "Dashboard";
    $t{dic}{content}	.= qq[

	<style>
	.float_box{
		border:0px;
		padding:0px;
		margin:0px;
		float:left;
		margin-right:15px;
		margin-bottom:20px;
		width:350px;
	}
	</style>

	<div class=float_box style=width:220px;><div>
	<FIELDSET style=height:150px; ><LEGEND>Search service</LEGEND>
		<form action=services.cgi>
		<input style="width:100px;" name=query  value="$form{query}" >
		<input style="width:50px;" type=submit name=submit_button value=Search><br>
		
		<font color=#c0c0c0 style=line-height:100%;font-size:9px;>
		<br>Type name, email, ANI/DST number or service id. You can type fragment or complete information. For ANI/DST number use E164 (country, area, number) format. DST numbers search calls only 30 days in the past<br><br>
		</font>
		<a href=services.cgi?remember=1>&#187; Last search</a>
		<input type=hidden name=action value=search>
		<input type=hidden name=mode value=search>
		</form>
	</fieldset>
	</div></div>

	
	<div class=float_box style=width:485px;><div>
	<FIELDSET style=height:150px; ><LEGEND>Workgroup <font size=3 face=verdana,arial><a href=http://groups.google.com/group/zenofon/topics target=_blank color=#c0c0c0;>(Visit workgroup forum)</a></font></LEGEND>
		<iframe xxsrc="http://groups.google.com/group/zenofon/feed/rss_v2_0_msgs.xml" class=clear
			style="width:100%; height:125px; overflow:scroll; overflow-x:hidden; overflow-y:scroll;"
		>
		</iframe>
	</fieldset>
	</div></div>
	<br clear=both>


	<div class=clear style=width:720px;>
	<FIELDSET ><LEGEND>Your last actions</LEGEND>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100%  onclick="sortColumn(event)">
			<thead>
				<tr>
				<td>Date</td>
				<td>Service</td>
				<td>Action</td>
				</tr>
			</thead>
			<tbody style=height:200px;overflow:scroll;overflow-x:hidden;overflow-y:scroll;>
			$html_actions 
			</tbody>
		</table>
	</fieldset>
	</div>


	<script>document.forms[0].elements[0].focus();</script>

	];
	if (index($arg_array,"reload_menu") ne -1) { $t{dic}{content} .= "<script>parent.update_page();</script>";	}
	#foreach (sort keys %app){ $t{dic}{content} .= "APP - ($_) - ($app{$_}) <br>"; }
    &template_print("template.html",%t);
}
sub do_login() {
	#
	&multilevel_check_ip_flood("NOC_Login");
    #
    # inicializa algumas coisas
    $error 	= 0;
    $account	= substr(trim(clean_str("\L$form{account}" ,"_-")),0,100);
    $password	= substr(trim(clean_str("\L$form{password}","_-")),0,100);
    $imagecheck = substr(trim(clean_str($form{imagecheck_id},"_-")),0,100);
    $key		= substr(trim(clean_str($form{imagecheck_user_input},"_-")),0,100);
	$account_id = "";
    # 
    # confere nome senha estao ok
    if (  ($account ne "") && ($password ne "")  ) {
		#
		# primeiro nivel
		if ($error eq 0) {
			#if ( ($imagecheck eq "") || ($key eq "") )	{$error = 1}
			if ($account ne $form{account}) 			{$error = 1}
			if ($password ne $form{password})			{$error = 1}
		}
		#
		# segundo nivel
		if ($error eq 0) {
			%hash = database_select_as_hash("select 1,1,id,web_password from adm_users where web_user='$account' ","flag,id,password");
			if ( ($hash{1}{flag} eq 1) && ($hash{1}{id} ne "") && ($hash{1}{password} ne "") &&  ($hash{1}{password} eq $password)  )	{
				$account_id = $hash{1}{id};
			} else {
				$error = 1
			}
			#if (imagecheck_check($imagecheck,$key) ne 1)	{$error = 1}
		}
		#
		# se ok, adicionar o cookie e desviar pra pagina inicial
		if ($error eq 0) {
			&session_attach($account_id);
			&do_dashboard("reload_menu");
			exit;
		} 
    }
    #
    # imprime a pagina
    #$imagecheck		= imagecheck_new();
    $error_message	= ($error eq 1) ? "<br><div style=\"background-color:yellow; border:1px solid #808080; padding:10px;\"><b>Error</b><br>Incorrect account, password or security code</div>" : "";
    %t = ();
    $t{dic}{title}	= "";
    $t{dic}{content} = qq[
	<div class=clear style="padding-left:100px;padding-top:100px;">
	<fieldset style="width:250px; background-color:#eff7fa;"	    >
		<h3>Zenofon log-in</h3><br>
		<form class=clear action=/noc/$my_url method=post target=_top>
		    Log-in: <br><input type=text 		name=account  value="" style="width:100%;"><br>
		    Password:<br><input type=password 	name=password value="" style="width:100%;"><br>

			$error_message
		    <br>
		    <input type=submit name=submit   value="Log-in" style="width:80px;"><br>
		    <input type=hidden name=action value=login >
		</form>
	</fieldset>
	</div>
	<script>
	document.forms[0].elements[0].focus();
	</script>
	];
    &template_print("template.login.html",%t);
#
#		    Security code:<br>
#		    <div class=clear style="width:100%; border:1px solid #c0c0c0; background-color:#ffffff;">
#				<img src=/noc/$my_url?action=imagecheck&id=$imagecheck hspace=30 align=right vspace=5 border=0>
#				<input type=text value="" name=imagecheck_user_input style="width:100px; border:0px; height:42px;"><br clear=both>
#		    </div>
#		    <input type=hidden name=imagecheck_id value="$imagecheck" >
#
}
sub do_logout(){
    session_detach();
	cgi_redirect("/noc/$my_url?action=dashboard");
    exit;
}
#=======================================================



