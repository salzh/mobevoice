#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_email_edit") ne 1) {adm_error("no permission"); exit;}
#=======================================================


#=======================================================
# some global values
#=======================================================
$tmp = "
1|My Account|Login and restore password|design/template.myaccount.login.html|Login form for My Account tab. Also recovery password form
1|My Account|Setup|design/template.pbx.overview.html|See ANI list and DST list
1|My Account|Setup ANI|design/template.pbx.ani.html|Edit ANI (my numbers) list 
1|My Account|Setup DID|design/template.pbx.did.html|Edit DST (my friends) list
1|My Account|Profile|design/template.myaccount.profile.html|Edit name and email
1|My Account|Friends|design/template.myaccount.friends.html|Show friends and commissions summary (invite a friend in future)
1|My Account|Calls|design/template.myaccount.calls.html|Show calls
1|My Account|Notifications|design/template.myaccount.alerts.html|Edit email alerts
1|My Account|Credits|design/template.myaccount.credits.html|Manage credits.
2|Services|Service Information|design/template.services.html|Service information with link to accept invite and create account
2|Services|Service Add form|design/template.services.add.html|Form to create service (with terms of service). 
2|Services|Service Created|design/template.services.add.ok.html|Show-up when client sucessfuly create one new service
3|Help|Main help|help/index.html|Faq on help tab
4|About|about page|about/index.html|About zenofon. lets make client trust in us.
";
$tmp = "
0|New service|Service request|design/email.service.request.txt|when get invite, enter email and request zenofon account
0|New service|Service add|design/email.service.add.txt|The welcome email message when the user create new service
1|Active service|Lost PIN (single service)|design/email.lost.pin.txt|Remember PIN for user. In case he has only one service with this email
1|Active service|Lost PIN (multiple services)|design/email.lost.multiple.pin.txt|Remember PIN for user. In case he has MULTIPLE services with this email
1|Active service|Change email|design/email.change.email.txt|Message with the confirmation code to change email into myaccount-profile
2|Alerts|Call alert|design/email.alert.credit.each.call.txt|Call alert message
2|Alerts|New friend|design/email.alert.new.friend.txt|If a friend enter zenofon using your invite code
2|Alerts|New friend of friend|design/email.alert.new.friend.of.friend.txt|If a friend of friend enter zenofon
2|Alerts|Credit commission|design/email.alert.credit.commission.txt|Alert for commission when friend add credit
2|Alerts|Manual commission|design/email.manual.commission.txt|manual commission on NOC
2|Alerts|New friend commission|design/email.alert.newf.commission.txt|Alert for new friend commission
2|Alerts|friend first call commission|design/email.alert.newfcall.commission.txt|Alert for friend first call commission
3|Auto-recharge|Auto recharge ok|design/email.autorecharge.ok.txt|Auto recharge start and work fine
3|Auto-recharge|Limit per monh|design/email.autorecharge.overlimit.txt|Auto recharge detected but recharge not posible due month recharge limit
3|Auto-recharge|disabled|design/email.autorecharge.disabled.txt|We detect low balance (less than 2 dollars) but client do not have auto recharge. Good time to explain about auto recharge
4|Coupon|coupon added|design/email.coupon.add.txt|whenever adding coupon,we can send email
5|Mass Mail|rates update|design/email.rates.update.txt|when sending update about new rates from noc
";
$c=0;
%templates = ();
$dbg = "";
foreach $l(split(/\n/,$tmp)){
$dbg .= "LINE ($l)<br>";
    if ($l eq "") {next}
    $tmp1 = 
    ($gi,$g,$n,$f,$d) = split(/\|/,$l);
	$dbg .= "SPLIT $c - ($g,$n,$f,$d)<br>";
    $templates{i}{$c}{n} = $n;
    $templates{i}{$c}{f} = $f;
    $templates{i}{$c}{d} = $d;
    $templates{t}{$gi}{n} = $g;
    $templates{t}{$gi}{l}{$c} = 1;
    $c++;
}
#=======================================================




#=======================================================
# main loop
#=======================================================
$my_url = "email.edit.cgi";
$action = $form{action};
if 		($action eq "save")		{ &do_save(); } 
elsif 	($action eq "edit")		{ &do_edit(); }
else							{ &do_list(); }
exit;
#=======================================================



#========================================================================
# actions
#========================================================================
sub do_list(){
    $html = "<br>";
    foreach $gi (sort{$a <=>  $b} keys %{$templates{t}}) {
        #$html .= "<div class=clear style='width:360px; margin-right:50px; float:left;'> ";
		#$html .= "<h2>$templates{t}{$gi}{n}</h2><ol style='padding-top:0px; margin-top:0p;'>";
        #foreach $id (sort{$a <=> $b} keys %{$templates{t}{$gi}{l}}) {
		#	$html .= "<li style='margin-bottom:10px;'><a href=$my_url?action=edit&id=$id><b>$templates{i}{$id}{n}</b></a><br>$templates{i}{$id}{d}</li>";
		#}
		#$html .= "</ol><br></div>";

        #$html .= "<div class=clear style='width:250px; margin-right:10px; float:left;'> ";
		#$html .= "<fieldset><legend>$templates{t}{$gi}{n}</legend>";
        $html .= "<div class=clear style='width:300px; margin-right:20px; margin-bottom:20px; float:left;'> ";
		$html .= "<fieldset style='padding-right:0px;'><legend>$templates{t}{$gi}{n}</legend><div class=clear style='height:180px; overflow:scroll; padding-right:10px; overflow-x: hidden; overflow-y: scroll; '>";
        foreach $id (sort{$a <=> $b} keys %{$templates{t}{$gi}{l}}) {
			$html .= "<a href=$my_url?action=edit&id=$id><b>$templates{i}{$id}{n}</b></a><br>$templates{i}{$id}{d}<br><br>";
		}
		$html .= "</div></fieldset></div>";
		#$html .= "</fieldset></div>";
    }
    #
    # print page
    %t = ();
    $t{dic}{title}		= "<a href=config.cgi>Settings</a> &#187; <a href=$my_url>Email messages</a>";
    $t{dic}{content}	= $html;
    &template_print("template.html",%t);
    
}
sub do_edit(){
    #
    # start some things
    $id = clean_int(substr($form{id},0,100));
    #
    # check and load template
    unless (exists($templates{i}{$id})) {adm_error("Unknown ID");return}
    $file = "/usr/local/multilevel/www/$templates{i}{$id}{f}";
    unless (-e $file) {adm_error("Unknown FILE ($file)");return}
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
    <br>
    Name: $templates{i}{$id}{n}<br>
    Info: $templates{i}{$id}{d}<br>
    <form action=$my_url method=post>
    <input type=hidden name=start value=1>
    <textarea wrap=off name=text style="width:95%; height:400px;">$buf</textarea><br>
    <input type=hidden name=id value=$id>
    <input type=hidden name=action value=save>
    <button class=cancel type=button onclick="window.location='$my_url'">Cancel</button>
    <button class=save type=submit>Save</button>
    <input type=hidden name=stop value=1>
    </form>
    ];
    #
    # print page
    %t = ();
    $t{dic}{title}		= "<a href=config.cgi>Config</a> &#187; <a href=$my_url>Email messages</a> &#187; Edit";
    #$t{dic}{title}	= "Edit '$templates{i}{$id}{n}'";
    $t{dic}{content}	= $html;
    &template_print("template.html",%t);
    
}
sub do_save(){
    #
    # start some things
    $id = clean_int(substr($form{id},0,100));
    #
    # check and load template
    unless (exists($templates{i}{$id})) {adm_error("Unknown ID");return}
    $file = "/usr/local/multilevel/www/$templates{i}{$id}{f}";
    unless (-e $file) {adm_error("Unknown FILE ");return}
    if ($form{start}.$form{stop} ne "11") {adm_error("Internal error. Try again.");return}
    #
    # save and backup
    $tmp = clean_str($file,"MINIMAL");
    $file_bkp = $app_root."/data/templates-backup/$tmp.".time;
    copy($file,$file_bkp);
    open(OUT,">$file");
    print OUT $form{text};
    close(OUT);
    #
    # manda pra listar
    do_list();
}
#========================================================================




