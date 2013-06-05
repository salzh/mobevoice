#!/usr/bin/perl
require "include.cgi";

#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_send_email") ne 1) {adm_error("no permission"); exit;}
#=======================================================


$my_url = "email.test.cgi";
$action = $form{action};

if 		($action eq "send_email")		{&do_send_email();}
else								{&do_email_layout();}
exit;

sub do_send_email(){
	$to = $form{toemail};
	$from = $form{fromemail};
	$subject = $form{subject};
	$email = $form{email};
	if($to eq ""){
		&do_email_layout();
		exit;
	}
	if($from eq ""){
		&do_email_layout();
		exit;
	}
	if($subject eq ""){
		&do_email_layout();
		exit;
	}
	if($email eq ""){
		&do_email_layout();
		exit;
	}
	send_email($from,$to,$subject,$email,1);
	%t = ();
	$t{dic}{content} = "Mail Sent";
	&template_print("template.html",%t);
	
}

sub do_email_layout(){
	$to = $form{toemail};
	$from = $form{fromemail};
	$subject = $form{subject};
	$email = $form{email};
	
	%t = ();
	$t{dic}{content} = qq[
<div>
	<form method=post>
		To Email: <input type=text name=toemail size=40 value='$to'><br>
		From Email: 
		<select name=fromemail>
		<option>work\@zenofon.com</option>
		<option>support\@zenofon.com</option>
		<option>test\@zenofon.com</option>
		<option>cs\@zenofon.com</option>
		</select>
		<br>
		Subject: <input type=text name=subject size=40 value='$subject'><br>
		<textarea cols=80 rows=15 name=email>$email</textarea>
		<br>
		<input type=hidden name=action value=send_email>
		<button type=submit>Send email</button>
	</form>
</div>
	];
	&template_print("template.html",%t);
}