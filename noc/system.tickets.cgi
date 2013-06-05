#!/usr/bin/perl
require "include.cgi";
#=======================================================
# TODO: Why we are coding a ticket only for zenoradio? can we install a app for all zeno and save development time to make zeno better?
#=======================================================
# lock this app to system.manager eyes only
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("radio.report") ne 1) {adm_error("no permission"); exit;}
#=======================================================



#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
#unless (&active_user_permission_check("radio.report") > 0) {adm_error("no permission"); exit;}
#=======================================================




#=======================================================
# get active stations
#=======================================================
# 0  no access to radio settings
# 1  view and edit they own radios
# 2  View and edit all radios plus radio DIDs
$stations_allow = "";
$tmp1	= &active_user_permission_get("radio.report");

$my_url = "system.tickets.cgi";
$action = $form{action};
$chatframe = qq[<div style="position:absolute; top:61px; right:300px;">
<iframe src="http://www.google.com/talk/service/badge/Show?tk=z01q6amlqjcr0icb5pu49pbsup3bq4juhdbh867iuj9mjsg94ngunf621iokk15lclup2kmg46qi52jgq0q15e2hu3tiotbktkfh78ou7gb4duhtvooqu6gtk1qudrop1rispb6utu3g5bnm03e6km6nui1s60k9pmft9u07v&amp;w=200&amp;h=60" frameborder="0" allowtransparency="true" width="200" height="60"></iframe></div>
];

%my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} " .
									   "where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

if 		($action eq "tickets_list")	{ &do_tickets_list();		}
elsif 	($action eq "tickets_add")	{ &do_tickets_add();		}
elsif	($action eq "tickets_reply"){ &do_tickets_reply();		}
elsif	($action eq "tickets_del")	{ &do_tickets_del();		}
elsif   ($action eq 'tickets_view') { &do_tickets_view();		}
else								{ &do_tickets_list();		}
exit;


sub do_tickets_list () {
	$createby = $my_user{1}{group_id} == 2 ? "1=1" : "createby='$my_user{1}{name}'";
	$sql	  = "select id,title,content,level,create_datetime,update_datetime,status,createby,last_replyby " .
				"from tickets where $createby order by create_datetime desc";
	warn $sql;
	%hash     = database_select_as_hash($sql, "title,content,level,create_datetime,update_datetime,status,createby,last_replyby");
	$top_stations = '';
	for (sort {$b <=> $a} keys %hash) {
		$c = length($hash{$_}{content}) > 40 ?
			substr($hash{$_}{content}, 0, 40) . "<a href='$my_url?action=tickets_view&&id=$_'>...</a>" :
			substr($hash{$_}{content}, 0, 40);

		$top_stations .= "<tr><td>$hash{$_}{title}</td><td>$c</td>" .
						 "<td>$hash{$_}{level}</td><td>$hash{$_}{createby}</td><td>$hash{$_}{last_replyby}<td>$hash{$_}{create_datetime}</td>" .
						 "<td>$hash{$_}{update_datetime}</td><td>$hash{$_}{status}</td></td>".
						 "<td><a href='$my_url?action=tickets_view&&id=$_'>Detail&Reply</a></td>" .
						 "<td><a href='$my_url?action=tickets_del&&id=$_' onclick='return confirm(\"Are you sure to delete it\");' />Del</tr>";
	}

	$choise = '<form action="" method="get" name="ticketlist">' .
			  '<input type="submit" onclick="add_new_tickets();return false;" value="New" />' .
			  '</form>';


    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Noc Tickets";
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[
$chatframe

$choise
<script>
	function add_new_tickets () {
		window.location.href="$my_url?action=tickets_add";
	}

	function del_tickets() {
		var s = confirm("Are you sure to delete your selection?");
		if (s) {
			alert("processing...");
		}
	}

</script>

<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Title</td>
		<td>Content</td>
		<td>Priority</td>
		<td>Createby</td>
		<td>LastReplyby</td>
		<td>Create Datetime</td>
		<td>Update Datetime</td>
		<td>Status</td>
		<td>Action</td>
		<td>Del</td>
		</tr>
	</thead>
	<tbody>
		$top_stations
	</tbody>
</table>
<br>
];

	&template_print("template.html",%t);

}


sub do_tickets_add () {

	if ($form{subaction} && $form{subaction} eq 'add') {
		$title   = database_clean_string($form{title});
		$content = database_clean_string($form{content});
		$level	 = database_clean_string($form{level});

		$newid	 = database_do_insert("insert into tickets(title,content,level,createby) values " .
						   "('$title','$content','$level','$my_user{1}{name}')");

		save_file('attach', $newid);

		sendemail("New ticket: $title", "Title: $title\nPriority: $level\nCreate By: $my_user{1}{name}\n\n$content\n" .
				  "Attachment: " . getfilebyid($newid, 1) . "\n");
		cgi_hearder_html();

		print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>ADD</title>
<script>
window.location = "$my_url";

</script>
</head>

<body>
	<center> New Tickets Added id=$newid ... <a href="$my_url"> Return </a></center>
</body>
</html>
HTML
		exit 0;

	} else {
		$choise = '<form action="" method="post" name="ticketlist" enctype ="multipart/form-data">' .
				  '<input type="hidden" name="subaction" value="add">'.
				  '<input type="hidden" name="action" value="tickets_add">'.

				  'Title: <br><input type="text" name="title" value="" size="40"/><p>'.
				  'Content: <br><textarea name="content" rows="10" cols="80"></textarea><p>' .
				  'Level: <br><select name="level"><option value="test">Test</option><option value="normal">Normal</option>' .
				  '<option value="911">911</option></select><p>' .
				  'Upload File:<br> <input type="file" name="attach" /><p>' .
				  '<input type="submit" value="submit" />' .
				  '</form>';


		%t = &menu_permissions_get_as_template();
		$t{my_url}	= $my_url;
		$t{title}	= "Noc Tickets";
		$t{content} = "";
		#
		# add extra info for admin
		$t{content} .= qq[
$chatframe
$choise
<br>
];

		&template_print("template.html",%t);
	}

}


sub do_tickets_view () {
	$id	  = $form{id};
	%hash = database_select_as_hash("select 1,id,title,content,level,create_datetime,update_datetime,status,createby " .
								    "from tickets where id='$id'",
								    "id,title,content,level,create_datetime,update_datetime,status,createby");

	$choise = '<form action="" method="post"  enctype ="multipart/form-data"/>' .
			  '<input type="hidden" name="action" value="tickets_reply" />' .
			  '<input type="hidden" name="id" value="' . $id . '" />' .

			  'Reply: <br><textarea name="content" rows="10" cols="80"></textarea><p>' .
 			  'Upload File:<br> <input type="file" name="attach" /><p>' .

			  'Change Status: <br><select name="status"><option value="initial"'.
			  ($hash{1}{status} eq 'initial' ? 'SELECTED' : '') . '>Initial</option>'.
			  '<option value="processing"' . ($hash{1}{status} eq 'processing' ? 'SELECTED' : '') . '>Processing</option>'.
			  '<option value="closed"'. ($hash{1}{status} eq 'closed' ? 'SELECTED' : '') . '>Closed</option></select><br>' .
			  '<input type="submit" value="submit" />' .
			  '</form>';

	%reply = database_select_as_hash ("select rid,content,createby,update_datetime from tickets_reply where tid='$id'",
									   "content,createby,update_datetime");

	$reply_html = '';
	for (sort  keys %reply) {
		$reply_html .= '<div name="reply">' .
					   '<font color="red">Replied by ' . $reply{$_}{createby} . ' on datetime ' .
						$reply{$_}{update_datetime} . '</font><p><pre>' .
					    f($reply{$_}{content}) . "</pre></div>";
		$reply_attachment = getfilebyid($_,0,1);
		$reply_html .= ($reply_attachment ? "<br> $reply_attachment" : '');
	}

    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Noc Tickets";
    $t{content} = "";
	#
	# add extra info for admin
	$ticket_content   = f($hash{1}{content});
	$ticket_attachment = getfilebyid($id);
	$ticket_content  .= ($ticket_attachment ? "<br>$ticket_attachment" : '');

	$t{content} .= qq[
$chatframe
<div name="publish">
<font color="blue">Created by $hash{1}{createby} on datetime $hash{1}{create_datetime}</font><p>
$ticket_content
</div>
$reply_html
<hr>
$choise
<br>
];

	&template_print("template.html",%t);

}


sub do_tickets_del () {
	$id = clean_int($form{id});

	if ($my_user{1}{group_id} == 2) {
		database_do ("delete from tickets where id='$id'");
	} else {
		database_do ("delete from tickets where id='$id' and createby='$my_user{1}{name}'");
	}

	cgi_hearder_html();

	print <<DELETE;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>Delete</title>
<script>
window.location = "$my_url";
</script>
</head>

<body>
	<center> Ticket Deleted id=$id ... <a href=$my_url>Return</a></center>
</body>
</html>
DELETE
		exit 0;

}

sub do_tickets_reply () {
	$id		 = clean_int($form{id});
	$content = database_clean_string($form{content});
	$status  = database_clean_string($form{status}) || 'processing';
	$status  = 'processing' if $status eq 'initial';

	$rid	 = database_do_insert("insert into tickets_reply (tid,content,createby) values ('$id', '$content', '$my_user{1}{name}')");

	database_do("update tickets set status='$status',update_datetime=CURRENT_TIMESTAMP,last_replyby='$my_user{1}{name}' where id='$id'");

	save_file('attach', $rid, 1);
	$id		 = clean_int($form{id});

	%ticket = database_select_as_hash("select 1, title from tickets where id='$id'", "title");
	sendemail("Re: $ticket{1}{title}", "$content\n--\n$my_user{1}{name}\nZenoradio Noc Support Team\n"  .
			  "Attachment: " . getfilebyid($rid, 1) . "\n", $my_user{1}{email});
	$id		 = clean_int($form{id});

	warn "id4: $id";

	cgi_hearder_html();

	print <<REPLY;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>Reply</title>
<script>
window.location = "$my_url?action=tickets_view&id=$id";
</script>
</head>

<body>
	<center> Reply submited Reply id=$rid...<a href="$my_url?action=tickets_view&id=$id" />Return</a></center>
</body>
</html>
REPLY
		exit 0;

}

sub f() {
	my $str = shift || '';
	$str    =~ s{(http(?:|s)://\S+)}{<a href="$1" target="_blank">$1</a>}g;
	$str	=~ s{\n}{<br>\n}g;
	return $str;
}

sub do_tickets_list_default () {
    %t = &menu_permissions_get_as_template();

    $t{my_url}	= $my_url;
    $t{title}	= "Tickets List";
    $t{content} = qq[

	coming soon...

	];
	&template_print("template.html",%t);
}

sub sendemail {

    my $title = shift || 'notitle';
    my $body  = shift || 'nocontent';

    my $to  = shift || '';
	$to    .= 'support@zenoradio.com,cesia@zenoradio.com,bh@zenoradio.com';
    my $cc  = shift || 'zhongxiang721@gmail.com';
    my $bcc = shift || '';
    my $attachment = shift || '';
	my $from = '/usr/local/conference_radio/website/www/noc/muttrc ';

    my $cmd = "mutt -s \"$title\"  -F $from" .
              ($cc ? "-c \"$cc\" " : '') .
              ($bcc ? "-b \"$bcc\" " : '') .
              ($attachment ? "-a $attachment " : '').
              "-s \"$title\" " . $to;
    $cmd = "echo \"$body\" | $cmd";
    warn $cmd;
    system($cmd);

=pod
    warn "Can't fork for send email" unless defined (my $child = fork);
    if ($child == 0) {
        exit 0;
    } else {
        return {status => 1, message => "OK"};
    }
=cut

}

sub save_file() {
	($field, $id, $t) = @_;
	$name = $form{$field};
	return if !$name;

	($n, $postfix) = $name =~ m{([^\\\/]+?)\.([^\\\/]+)$};
	$postfix ||= '';

	$fh  = $cgi->upload($field);

	$id	 = "R$id" if $t;
  # undef may be returned if it's not a valid file handle
	if (defined $fh) {
   		my $io = $fh->handle;
		open (OUTFILE, '>', "files/$id.$postfix");
		while ($bytesread = $io->read($buffer,1024)) {
			print OUTFILE $buffer;
		}

		return 1;
	}

	return;
}

sub getfilebyid () {
	my ($id, $w, $t) = @_;

	$id	 = "R$id" if $t;
	warn "id: $id";
	$dir  = "./files";
	while (<$dir/$id.*>) {
		warn $_;
		($file = $_) =~ s{\./files/}{};
		$file  = "https://www.zenoradio.com/noc/files/$file";

		if ($w) {
			return $file;
		}

		if ($file =~ m/\.(?:png|jpg|jpeg|gif|bmp)$/i) {
			return "<img src='$file'></img>";
		} else {
			return "<a href='$file'>$file</a>";
		}
	}

	return ;
}

