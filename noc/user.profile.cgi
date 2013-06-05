#!/usr/bin/perl
#=======================================================
# user account profile
#=======================================================
# allow user manage they own profile
# We need move this action to index.cgi (that also do login)
# and remove this CGI
#=======================================================
require "include.cgi";





#=======================================================
# logout if no session
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
unless (&active_user_permission_check("user.profile") eq 1) {adm_error("no permission"); exit;}
$my_url = "user.profile.cgi";
&do_profile();
exit;
#=======================================================
sub do_profile(){
	#
	# start 
    %t = &menu_permissions_get_as_template();
    %hash = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password");
	%user_data = %{$hash{1}};	
	#
	# save
	$error = 0;
	if ($form{save} eq 1) {
		#
		# check name
		$data = $form{name};
		$data = &clean_str(substr($data,0,255)," ()[]_-");
		if ( ($form{name} ne $data) || ($data eq "") ) {$t{msg_error_name} = 1; $error=1}
		$form{name} = $data;
		#
		# check email
		$data = $form{email};
		$data = &clean_str(substr($data,0,255),"_-");
		if ( ($form{email} ne $data) || ($data eq "") ) {$t{msg_error_email} = 1; $error=1}
		$form{email} = $data;

		#
		# check password
		if ($form{password_action} eq 1) {
			$data0 = &clean_str(substr($form{password_active},0,255),"_-");
			$data1 = &clean_str(substr($form{password_new},0,255),"_-");
			$data2 = &clean_str(substr($form{password_retype},0,255),"_-");
			if ( (length($data1)<5) || (length($data1)>50) || ($form{password_new} ne $data1) || ($data1 eq "") || ($data1 ne $data2) ) {$t{msg_error_new_password} = 1; $error=1}
			if (substr($user_data{web_password},0,1) eq "_") {
				# new md5 password
				$data0_md5 = "_".key_md5($data0.$user_data{web_user});
				if ( ($data0 eq "") || ($data0_md5 ne $user_data{web_password}) ) {$t{msg_error_password} = 1; $error=1}
			} else {
				# old password to dont breake people login until they change password
				if ( ($data0 eq "") || ($data0 ne $user_data{web_password}) ) {$t{msg_error_password} = 1; $error=1}
			} 
			$form{password} = $data1;
		}
		#
		# try to save
		if ($error eq 0) {
			if ($form{password_action} eq 1) {
				$password_md5 = "_".key_md5($form{password}.$user_data{web_user});
				&database_do(&database_scape_sql("update $app{users_table} set web_password='%s' where id='%s' ",$password_md5,$user_data{id}) );
			}
			if ($user_data{name} ne $form{name}) {
				&database_do(&database_scape_sql("update $app{users_table} set name='%s' where id='%s' ",$form{name},$user_data{id}) );
			}
			if ($user_data{email} ne $form{email}) {
				&database_do(&database_scape_sql("update $app{users_table} set email='%s' where id='%s' ",$form{email},$user_data{id}) );
			}
			$t{msg_ok} = 1;
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
	$msg_error 	= ($t{msg_error_name} eq 1) ? "Incorrect name<br>" : "";
	$msg_error 	= ($t{msg_error_email} eq 1) ? "Incorrect email<br>" : "";
	$msg_error 	= ($t{msg_error_new_password} eq 1) ? "incorrect new password<br>" : "";
	$msg_error 	= ($t{msg_error_password} eq 1) ? "Incorrect actual password<br>" : "";
	$msg_error 	= ($msg_error eq "") ? "" : "<font color=red><b>$msg_error</b></font>";
	$msg_ok 	= ($t{msg_ok} eq 1) ? "<font color=green><b>Saved.</b></font>" : "";
    $t{title}		= "Your account";
    $t{content}	.= qq[
	
			<form action=$my_url method=post style="padding-left:20px;">
			Your log-in:<br>
			<input name=web_user disabled read-only readonly value="$form{web_user}"><br>

			<br>
			Your contact name:<br>
			<input name=name value="$form{name}"><br>
			<br>

			Your contact email:<br>
			<input name=email value="$form{email}"><br>
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
#=======================================================
