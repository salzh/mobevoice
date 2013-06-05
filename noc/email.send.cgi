#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_send_email") ne 1) {adm_error("no permission"); exit;}
#=======================================================




#=======================================================
# main loop
#=======================================================
$my_url = "email.send.cgi";
$action = $form{action};
if 		($action eq "status")	{ &do_status();			} 
elsif 	($action eq "send")		{ &do_send();			}
elsif 	($action eq "delete")	{ &do_delete();			}
else							{ &do_status(); 		}
exit;
#=======================================================


#========================================================================
# actions
#========================================================================
sub do_status(){
	local($message) = @_;
    #
    # pega lista da outbox
    #opendir (DIR,"$app_root/data/send_email/out/$taskid.$seq.email";
    %data_out = ();
    opendir (DIR,"$app_root/data/send_email/out/");
    foreach $f (readdir(DIR)){
		if ($f eq "") {next}
		if (index($f,".email") eq -1) {next}
		($v1,$v2) = split(/\./,$f);
		$data_out{$v1}{q}++;
		if ($data_out{$v1}{n} eq "") {
			open(IN,"$app_root/data/send_email/out/$f");
			$tmp=<IN>;
			close(IN);
			chomp($tmp);
			($tmp1,$tmp2) = split(/\|/,$tmp);
			$data_out{$v1}{n} = $tmp2;
		}
    }
    $html_out = "";
    foreach (reverse sort keys %data_out){
		$html_out .= "<li>\"$data_out{$_}{n}\" <span style='font-size:9px; color:#c0c0c0;'>($data_out{$_}{q} message(s) to send)</span> <a href=$my_url?action=delete&id=$_>[Delete]</a></li>";
    }
    #
    # pega lista da sent
    %data_out = ();
    foreach $f (`cd /usr/local/multilevel/data/send_email/sent/; ls -1u | head -n 500`){
		chomp;
		if ($f eq "") {next}
		if (index($f,".email") eq -1) {next}
		($v1,$v2) = split(/\./,$f);
		$data_out{$v1}{q}++;
		if ($data_out{$v1}{n} eq "") {
			open(IN,"$app_root/data/send_email/sent/$f");
			$tmp=<IN>;
			close(IN);
			chomp($tmp);
			($tmp1,$tmp2) = split(/\|/,$tmp);
			$data_out{$v1}{n} = $tmp2;
		}
    }
    $html_sent = "";
    foreach (reverse sort keys %data_out){
		$html_sent .= "<li>\"$data_out{$_}{n}\" <span style='font-size:9px; color:#c0c0c0;'>($data_out{$_}{q} message(s) sended)</span></li>";
    }
    #
    # imprime pagina
    $html_out	= ($html_out  eq "") ? "<li><font color=#c0c0c0>...Empty...</font></li>" : $html_out;
    $html_sent	= ($html_sent eq "") ? "<li><font color=#c0c0c0>...Empty...</font></li>" : $html_sent;
	$message	= ($message   eq "") ? "" : "<script>alert('$message')</script>";
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "Settings &#187; <a href=$my_url>Send mass email</a>";
    $t{dic}{content}	= qq[


	<div class=clear style=width:600px>
		<fieldset class=config_select_list><legend>Email tasks</legend>
			<h1>in queue to send</h1>
			<ul style="padding-left:15px;margin-top:5px;">
			$html_out
		    <li><a href=$my_url>[Reload]</a></li>
			</ul>
			<br>
			<h1>finished</h1>
			<ul style="padding-left:15px;margin-top:5px;">
			$html_sent
			</ul>
		</fieldset>
		<a href="$my_url?action=send"><img src=design/icons/bullet_add.png border=0 align=left hspace=0 vspace=0>Create a new email task</a><br>
	</div>
	<br>
	
	$message
    ];
    #foreach (sort keys %data) {$t{dic}{content} .= "DATA $_=$data{$_}<br>";}
    &template_print("template.html",%t);
}
sub do_delete(){
	$id = substr(&clean_int($form{id}),0,100);
	$c=0;
    opendir (DIR,"$app_root/data/send_email/out/");
    foreach $f (readdir(DIR)){
		if ($f eq "") {next}
		if (index($f,".email") eq -1) {next}
		($v1,$v2) = split(/\./,$f);
		if ($v1 ne $id) {next}
		unlink("$app_root/data/send_email/out/$f");
		$c++;
    }
	$cs = &format_number($c,0);
	$msg = ($c eq 0) ? "No messages deleted in this task" : "$cs messades deleted in this task";
	&do_status($msg);
}
sub do_send(){
    (%data) = @_;
    #
    # se save task, verificar ela e gerar error msg ou adicionar e reload
    $message = "";
    if ($form{save} eq 1) {
		if ($form{subject} eq "") {
			$message .= "I need subject. ";
		}
		if ($form{message} eq "") {
			$message .= "I need message. ";
		}
		#
		# email to
		if ($form{email_to_mode} eq "manual") {
			if ($form{email_to} eq "") {
				$message .= "I need email to. ";
			}
		} elsif ($form{email_to_mode} eq "news") {
		} else {
			$message .= "Unknown email to mode. ";
		}
		#
		#
		if ($form{email_from} eq "") {
			$message .= "I need email from. ";
		}
		if ($message eq "") {
			my @chars =('0'..'9');
			$taskid = time;
			$taskid .= $chars[rand @chars];
			$taskid .= $chars[rand @chars];
			$taskid .= $chars[rand @chars];
			$taskid .= $chars[rand @chars];
			%email_list = ();
			#
			# pega email list
			if ($form{email_to_mode} eq "manual") {
				foreach $email_now (split(/\n/,$form{email_to})){
					chomp($email_now);
					$email_now = trim($email_now);
					if ($email_now eq "") {next}
					if (index($email_now,"\@") eq -1) {next}
					$email_list{$email_now}++;
				}
			} elsif ($form{email_to_mode} eq "news") {
				$sql = qq[
				SELECT 
					service.id,service.email 
				FROM 
					service_data, service
				where 
					service_data.name="email_news" and 
					service_data.value="1" and
					service_data.target=service.id and 
					service.email != ""
				];
			    %hash = database_select_as_hash($sql);
				foreach(keys %hash) {
					$email=$hash{$_};
					$email_list{$email}++;
				}
				
			}
			#
			#
			$seq=0;
			foreach $email_now (keys %email_list){
				$seq++;
				$file = "$app_root/data/send_email/out/$taskid.$seq.email";
				open (OUT,">$file");
				print OUT "subject|$form{subject}\n";
				print OUT "from|$form{email_from}\n";
				print OUT "to|$email_now\n";
				print OUT "src|email tool\n";
				print OUT "\n";
				print OUT "$form{message}";
				close(OUT);
			}
			cgi_redirect("$my_url");    
		}
    }
    $message = ($message eq "") ? "" : "<font color=red>$message</font><br><br>";	
    #
    # se save=0, pegar emails adicionados pela lista
    if ($form{save} ne 1) {
		#%emails = ();
		#foreach $id (sort{ $data{$b} <=> $data{$a} } keys %data) {
		#    $emails{$data{$id}{e}}++;
		#}
		#$form{email_to} = "";
		#foreach (sort keys %emails) {$form{email_to} .= "$_\n";}
		if ($form{service_ids} ne "") {
			@ids = ();
			foreach(split(/\,/,$form{service_ids})) {
				$tmp = clean_int($_);
				if ($tmp eq "") {next}
				@ids = (@ids,$tmp);
			}
			$ids_sql = join(",",@ids);
			if ($ids_sql ne "") {
				%hash = database_select_as_hash("select id,email from service where id in ($ids_sql)");
				foreach (keys %hash) {
					if ($hash{$_} eq "") {next}
					$form{email_to} .= "$hash{$_}\n";
				}
			}
		}
    }
	#
	# email news
	$sql = qq[
	SELECT
		1,count(*) 
	FROM 
		service_data, service
	where 
		service_data.name="email_news" and 
		service_data.value="1" and
		service_data.target=service.id and 
		service.email != ""
	];
	%hash = database_select_as_hash($sql);
	$email_news_qtd = &format_number($hash{1},0);
    #
    # monta a pagina com status e forms
	$form_select_email_to_mode{$form{email_to_mode}} = "selected";
    %t = ();
    $t{dic}{my_url}	= $my_url;
    #$t{dic}{title}	= "Create email task";
    $t{dic}{title}	= "Settings &#187; <a href=$my_url>Send mass email</a> &#187; Create email task";
    $t{dic}{content}	= qq[

	<script>
	function update_email_tu_ui(){
		MyDisplay('email_to_manual',0);
		MyDisplay('email_to_news',0);
		value = document.forms[0].elements[0].selectedIndex
		if (value == 0) {MyDisplay('email_to_manual',1);}
		if (value == 1) {MyDisplay('email_to_news',1);}
	}
	</script>


	<form action=$my_url  method=post>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear><tr>
	    
	    <td valign=top style="width:220px;">
			Email to:<br>
			<select name=email_to_mode onchange=update_email_tu_ui(); style="width:100%;">
			<option $form_select_email_to_mode{manual} value=manual>Manual mode</option>
			<option $form_select_email_to_mode{news} value=news>ZenoFon News</option>
			</select>
			<div class=clear id=email_to_manual>
			<br>Enter one email per line.<br>
			<textarea name=email_to style="width:100%; height:270px;">$form{email_to}</textarea>
			</div>
			<div class=clear id=email_to_news style="display:none;">
			<br>Send email for $email_news_qtd customers with "Zenofon news" flag enabled.<br>
			</div>
	    </td>

	    <td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
	    <td style="border-left:1px solid #e0e0e0;">&nbsp;&nbsp;&nbsp;&nbsp;</td>

	    <td valign=top>
	    From:<br>
	    <input name=email_from value="$form{email_from}" style="width:400px;"><br>
	    Subject:<br>
	    <input name=subject value="$form{subject}" style="width:400px;"><br>
	    Message:<br>
	    <textarea name=message style="width:400px; height:250px;">$form{message}</textarea><br>
	    </td>

	</tr></table>
	<br>
	$message<button type=submit class=save>Create email task</button><button type=button onclick="window.location='$my_url'" class=cancel>Cancel</button>
	<input type=hidden name=action value=send>
	<input type=hidden name=save value=1>
	</form>
	<script>update_email_tu_ui();</script>
    ];
    &template_print("template.html",%t);
}
#========================================================================


