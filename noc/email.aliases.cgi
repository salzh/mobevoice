#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_email_edit") ne 1) {adm_error("no permission"); exit;}
#=======================================================


#=======================================================
# main loop
#=======================================================
$my_url = "email.aliases.cgi";
$action = $form{action};
if 		($action eq "edit")	{ &do_edit(); }
elsif 	($action eq "save")	{ &do_save(); }
else						{ &do_view(); }
exit;
#=======================================================


#========================================================================
# actions
#========================================================================
sub do_view(){
	#
	# read data
	$buf = "";
	open(IN,"/etc/aliases.web");
	while(<IN>){ chomp(); $buf .= "$_<br>";}
	close(IN);
	$status = "";
	open(IN,"/etc/aliases.status");
	while(<IN>){ chomp(); $status .= "$_<br>";}
	close(IN);
	if ($status eq "") {
		$message = qq[
		<b><font color=red>WARNING:</font></b> This email map still <b>NOT</b> active! <br>
		Please wait few minutes and <a href=$my_url>check again</a>
		];
	} else {
		$message = qq[
		This email map is active! <a href=# onclick="MyDisplay('status_detail')">Show detail</a><br>
		<div id=status_detail style=display:none;>$status</div>
		];
	}
    #
    # print page
    %t = ();
    $t{title}	= "Zenofon email map</a>";
    $t{content}	= qq[

    	<div style="height:400px; width:550px; xxoverflow-x:hidden; xxoverflow-y:auto; overflow:auto;border:1px solid #a0a0a0; background-color:#e0e0e0; font-size:11px; line-height:130%; padding:5px;">
    		$buf
    	</div>
    	<a href=$my_url?action=edit>Edit this email map.</a><br>
    	<br>
    	$message 
    ];
    &template_print("template.html",%t);	
}
#========================================================================
# actions
#========================================================================
sub do_edit(){
    #
    # start some things
    $id = clean_int(substr($form{id},0,1));
    #
    # check and load template
    $file = (-e "/etc/aliases.backup.".$id) ? "/etc/aliases.backup.".$id : "/etc/aliases.web";
    $file_name = (-e "/etc/aliases.backup.".$id) ? "Backup $id" : "Active mail map";
    $buf = "";
    open(IN,$file);
    while(<IN>){$buf .= $_;}
    close(IN);
    $tmp1 = "<textarea";
    $tmp2 = "&lt;textarea";
    $buf =~ s/$tmp1/$tmp2/eg;
    $tmp1 = "</textarea";
    $tmp2 = "&lt;/textarea";
    $buf =~ s/$tmp1/$tmp2/eg;
    #
    # create form
    $html = qq[
    <form action=$my_url method=post>
    <input type=hidden name=start value=1>
    <textarea wrap=off name=text style="height:400px; width:550px; border:1px solid #a0a0a0; background-color:#ffffff; font-size:11px; line-height:130%; padding:5px;">$buf</textarea><br>
    <input type=hidden name=id value=$id>
    <input type=hidden name=action value=save>
    <button class=cancel type=button onclick="window.location='$my_url'">Cancel</button>
    <button class=save type=submit >Save this as active mail map</button>
    <input type=hidden name=stop value=1>
    </form>
    <br>
    Edit file: <b>$file_name</b><br>
    You can edit <a href=$my_url?action=edit>Active mail map</a>, or last 
    <a href=$my_url?action=edit&id=1>1</a>, 
    <a href=$my_url?action=edit&id=2>2</a>, 
    <a href=$my_url?action=edit&id=3>3</a>, 
    <a href=$my_url?action=edit&id=4>4</a>, 
    <a href=$my_url?action=edit&id=5>5</a>, 
    backups
    ];
    #
    # print page
    %t = ();
    $t{title}		= "Edit Zenofon mail map";
    $t{content}	= $html;
    &template_print("template.html",%t);
    
}
sub do_save(){
    #
    # check and load template
    if ($form{start}.$form{stop} ne "11") {adm_error("Internal error. Try again.");return}
    #
    # check text
    # Uppercase and lowercase English letters (a–z, A–Z)
	# Digits 0 to 9
	# Characters ! # $ % & ' * + - / = ? ^ _ ` { | } ~
	# Sapace, enter, : and @ 
$buf = &clean_str($form{text},"\n\r\t:\@ .-_=,;/#!","MINIMAL");
if ($buf ne $form{text}) {adm_error("We found invalid chars in this mail map. Please use a-z,A-Z,0-9 and '\@#.,;-_=!'. Hit back, fix and try again ");return}
$tmp1="\r"; $tmp2=" "; $buf =~ s/$tmp1/$tmp2/eg;
$buf =~ s/\cM\n/\n/g;
$tmp1="\t"; $tmp2="      "; $buf =~ s/$tmp1/$tmp2/eg;

    #
    # backup
    copy("/etc/aliases.backup.4","/etc/aliases.backup.5");
    copy("/etc/aliases.backup.3","/etc/aliases.backup.4");
    copy("/etc/aliases.backup.2","/etc/aliases.backup.3");
    copy("/etc/aliases.backup.1","/etc/aliases.backup.2");
    copy("/etc/aliases.web","/etc/aliases.backup.1");
    #
    # save 
    open(OUT,">/etc/aliases.web");
    print OUT $buf;
    close(OUT);
    #
    # clean status
    open(OUT,">/etc/aliases.status"); 
    print OUT "";
    close(OUT);
    #
    # send to start
    cgi_redirect($my_url);
}
#========================================================================





