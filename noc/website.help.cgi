#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_edit_pages_help") ne 1) {adm_error("no permission"); exit;}

#=======================================================




#=======================================================
# main loop
#=======================================================
$my_url = "website.help.cgi";
$action = $form{action};
if 		($action eq "topic_edit")			{ &do_topic_edit();			} 
elsif 	($action eq "topic_add")			{ &do_topic_add();			}
elsif 	($action eq "topic_del")			{ &do_topic_del();			}
elsif 	($action eq "topic_up")				{ &do_topic_up();			}
elsif 	($action eq "topic_down")			{ &do_topic_down();			}
elsif 	($action eq "topic_flag")			{ &do_topic_flag();			}
elsif 	($action eq "group_edit")			{ &do_group_edit();			} 
elsif 	($action eq "group_add")			{ &do_group_add();			}
elsif 	($action eq "group_del")			{ &do_group_del();			}
elsif 	($action eq "group_up")				{ &do_group_up();			}
elsif 	($action eq "group_down")			{ &do_group_down();			}
else										{ &do_start(); 				}
exit;
#=======================================================


#========================================================================
# actions
#========================================================================
sub do_group_add()	{
	#
	# cria e manda pra lista
    %hash = database_select_as_hash("select 1,1,max(sequence) from web_help_group","flag,seq");
	if ($hash{1}{flag} ne 1) {adm_error("No sequence");return}
	$seq = $hash{1}{seq};
	$seq++;
	database_do("insert into web_help_group (web_help_group.sequence) values ('$seq') ");
	%hash	= database_select_as_hash("SELECT 1,LAST_INSERT_ID();");
	$gid	= $hash{1};
	cgi_redirect("$my_url?action=group_edit&gid=$gid");
}
sub do_group_edit()	{
	#
	# verifica gid
    $gid = clean_int(substr($form{gid},0,100));
    if ($gid eq "") {adm_error("Invalid group id");return}
    %hash = database_select_as_hash("select 1,1 from web_help_group where id='$gid'","flag");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown group id");return}
	#
	# defaults
	%t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "Edit help group";
	$t{dic}{title}	= "<a href=config.cgi>Settings</a> &#187; <a href=$my_url>Website help</a> &#187; Edit group";
	$error = "";
	#
	# check before save
	if ($form{save} eq 1) {
		#
		# check title
		$data = $form{title};
		$data = &clean_html(substr($data,0,100));
		if ( ($form{title} ne $data) || ($data eq "") ) {$error .= "Incorrect title. "}
		$form{title} = $data;
		#
		# check text
		$data = $form{text};
		$data = substr($data,0,1024*8);
		if ( ($form{text} ne $data) || ($data eq "") ) {$error .= "Incorrect text. "}
		$form{text} = $data;
	}
	#
	# save if ok
	if ( ($error eq "") && ($form{save} eq 1) )  {
		$form{active} 	= ($form{active} eq 1) ? 1 : 0;
		$form{title}	= &database_escape($form{title});
		$form{text}		= &database_escape($form{text});
	    database_do("update web_help_group set title='$form{title}', text='$form{text}' where id='$gid'");
		cgi_redirect($my_url);
		return;
	}
	#
	# load if not save
	if ($form{save} ne 1) {
	    %hash = database_select_as_hash("select 1,1,title,text from web_help_group where id='$gid'","flag,title,text");
		$form{title}	= $hash{1}{title};
		$form{text}		= $hash{1}{text};
	}
	#
	# print page
    $t{dic}{content} = qq[
		<br>
		<form action=$my_url style="width:500px;">

		Title:<br>
		<input type=text name=title value="$form{title}" style="width:100%"><br>

		Text:<Br>
		<textarea name=text style="width:100%; height:200px;">$form{text}</textarea><br>

		<br>
		<button style="padding:3px;" type=button onclick="window.location='$my_url';"><img style="margin-right:5px;" src=../design/icons/delete.png hspace=0 vspace=0 border=0 width=16 height=16 align=left>Cancel</button>
		<button type=submit  style="padding:3px;"><img style="margin-right:5px;" src=../design/icons/accept.png hspace=0 vspace=0 border=0 width=16 height=16 align=left>Save</button>

		<input type=hidden name=gid value=$gid>
		<input type=hidden name=action value=group_edit>
		<input type=hidden name=save value=1>
		</form>
		<font color=red>$error</font>
	];
	#foreach (sort keys %form) { $t{dic}{content} .= "DUMP-FORM ($_)=($form{$_})<br>"}
	&template_print("template.html",%t);
}
sub do_group_up()	{
	#
	# verifica gid
    $gid = clean_int(substr($form{gid},0,100));
    if ($gid eq "") {adm_error("Invalid group id");return}
    %hash = database_select_as_hash("select 1,1 from web_help_group where id='$gid'","flag");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown group id");return}
	#
	# calcula from e to 
	$from_id	= "";
	$from_seq	= "";
	$to_id		= "";
	$to_seq		= "";
    %hash = database_select_as_hash("select id,sequence from web_help_group ","seq");
	foreach $id (sort{$hash{$a}{seq} <=> $hash{$b}{seq}} keys %hash) {
		if ($id eq $gid) {
			$from_id	= $id;
			$from_seq	= $hash{$id}{seq};
			last;
		}
		$to_id	= $id;
		$to_seq	= $hash{$id}{seq};
	}
	#
	# move se tudo ok
	if (  ($from_id	ne "") && ($to_id ne "") && ($to_id ne $from_id) ) {
	    database_do("update web_help_group set sequence='$from_seq' where id='$to_id'");
	    database_do("update web_help_group set sequence='$to_seq' where id='$from_id'");
	}
	#
	# redireciona
	cgi_redirect("$my_url");	
}
sub do_group_down()	{
	#
	# verifica gid
    $gid = clean_int(substr($form{gid},0,100));
    if ($gid eq "") {adm_error("Invalid group id");return}
    %hash = database_select_as_hash("select 1,1 from web_help_group where id='$gid'","flag");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown group id");return}
	#
	# calcula from e to 
	$from_id	= "";
	$from_seq	= "";
	$to_id		= "";
	$to_seq		= "";
	$get_next	= 0;
    %hash = database_select_as_hash("select id,sequence from web_help_group ","seq");
	foreach $id (sort{$hash{$a}{seq} <=> $hash{$b}{seq}} keys %hash) {
		if ($get_next eq 1) {
			$to_id	= $id;
			$to_seq	= $hash{$id}{seq};
			last;
		}
		if ($id eq $gid) {
			$from_id	= $id;
			$from_seq	= $hash{$id}{seq};
			$get_next=1;
		}
	}
	#
	# move se tudo ok
	if (  ($from_id	ne "") && ($to_id ne "") && ($to_id ne $from_id) ) {
	    database_do("update web_help_group set sequence='$from_seq' where id='$to_id'");
	    database_do("update web_help_group set sequence='$to_seq' where id='$from_id'");
	}
	#
	# redireciona
	cgi_redirect("$my_url?debug=$gid,$from_id,$from_seq,$to_id,$to_seq");
}
sub do_group_del()	{
	#
	# verifica gid
    $gid = clean_int(substr($form{gid},0,100));
    if ($gid eq "") {adm_error("Invalid group id");return}
    %hash = database_select_as_hash("select 1,1 from web_help_group where id='$gid'","flag");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown group id");return}
	#
	# delete
    %hash = database_select_as_hash("SELECT 1,1,count(*) FROM web_help_topic where web_help_topic.group='$gid'","flag,qtd");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown group id");return}
	if ( ($hash{1}{flag} ne 1) || ($hash{1}{qtd} > 0) ) {
		adm_error("I cannot delete group with topics. You have to delete all topics before delete this group.");
		return;
	} else {
		database_do("delete from web_help_group where id='$gid'");
	}
	#
	# redirect
	cgi_redirect("$my_url");
}
sub do_topic_add()	{
	#
	# verifica gid
    $gid = clean_int(substr($form{gid},0,100));
    if ($gid eq "") {adm_error("Invalid group id");return}
    %hash = database_select_as_hash("select 1,1 from web_help_group where id='$gid'","flag");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown group id");return}
	#
	# cria e manda pra lista
    %hash = database_select_as_hash("select 1,1,max(sequence) from web_help_topic","flag,seq");
	if ($hash{1}{flag} ne 1) {adm_error("No sequence");return}
	$seq = $hash{1}{seq};
	$seq++;
	database_do("insert into web_help_topic (web_help_topic.group,web_help_topic.sequence) values ('$gid','$seq') ");
	%hash	= database_select_as_hash("SELECT 1,LAST_INSERT_ID();");
	$tid	= $hash{1};
	cgi_redirect("$my_url?action=topic_edit&tid=$tid");
}
sub do_topic_edit()	{
	#
	# verifica tid
    $tid = clean_int(substr($form{tid},0,100));
    if ($tid eq "") {adm_error("Invalid topic id");return}
    %hash = database_select_as_hash("select 1,1,web_help_topic.group from web_help_topic where id='$tid'","flag,group");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown topic id");return}
	$gid = $hash{1}{group};
	#
	# defaults
	%t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "Edit help topic";
	$t{dic}{title}	= "<a href=config.cgi>Settings</a> &#187; <a href=$my_url>Website help</a> &#187; Edit topic";
	$error = "";
	#
	# check before save
	if ($form{save} eq 1) {
		#
		# check title
		$data = $form{title};
		$data = &clean_html(substr($data,0,100));
		if ( ($form{title} ne $data) || ($data eq "") ) {$error .= "Incorrect title. "}
		$form{title} = $data;
		#
		# check keywords
		$data = $form{keywords};
		$data = &clean_html(substr($data,0,255));
		if ( ($form{keywords} ne $data) ) {$error .= "Incorrect keywords. "}
		$form{keywords} = $data;
		#
		# check text
		$data = $form{text};
		$data = substr($data,0,1024*8);
		if ( ($form{text} ne $data) || ($data eq "") ) {$error .= "Incorrect text. "}
		$form{text} = $data;
	}
	#
	# save if ok
	if ( ($error eq "") && ($form{save} eq 1) )  {
		$form{active} 	= ($form{active} eq 1) ? 1 : 0;
		$form{title}	= &database_escape($form{title});
		$form{text}		= &database_escape($form{text});
		$form{keywords}	= &database_escape($form{keywords});
	    database_do("update web_help_topic set title='$form{title}', keywords='$form{keywords}', text='$form{text}', active='$form{active}' where id='$tid'");
		cgi_redirect($my_url);
		return;
	}
	#
	# load if not save
	if ($form{save} ne 1) {
	    %hash = database_select_as_hash("select 1,1,title,text,active,keywords from web_help_topic where id='$tid'","flag,title,text,active,keywords");
		$form{title}	= $hash{1}{title};
		$form{text}		= $hash{1}{text};
		$form{keywords}	= $hash{1}{keywords};
		$form{active}	= $hash{1}{active};
	}
	#
	# print page
	$form_active_select{$form{active}} = " selected "; 
    $t{dic}{content} = qq[
		<br>
		<form action=$my_url style="width:500px;">

		Title:<br>
		<input type=text name=title value="$form{title}" style="width:100%"><br>

		Keywords: (to help in search)<br>
		<input type=text name=keywords value="$form{keywords}" style="width:100%"><br>

		Text:<Br>
		<textarea name=text style="width:100%; height:200px;">$form{text}</textarea><br>

		Status:<br>
		<select name=active style="width:100%">
		<option $form_active_select{1} value=1>Active on website</option>
		<option $form_active_select{0} value=0>Inactive! Does not show on website.</option>
		</select><br>
		
		<br>
		<button class=cancel style="padding:3px;" type=button onclick="window.location='$my_url';">Cancel</button>
		<button class=save type=submit  style="padding:3px;">Save</button>

		<input type=hidden name=tid value=$tid>
		<input type=hidden name=action value=topic_edit>
		<input type=hidden name=save value=1>
		</form>
		<font color=red>$error</font>
	];
	&template_print("template.html",%t);
}
sub do_topic_up()	{
	#
	# verifica tid
    $tid = clean_int(substr($form{tid},0,100));
    if ($tid eq "") {adm_error("Invalid topic id");return}
    %hash = database_select_as_hash("select 1,1,web_help_topic.group from web_help_topic where id='$tid'","flag,group");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown topic id");return}
	$gid = $hash{1}{group};
	#
	# calcula from e to 
	$from_id	= "";
	$from_seq	= "";
	$to_id		= "";
	$to_seq		= "";
    %hash = database_select_as_hash("select id,sequence from web_help_topic where web_help_topic.group=$gid","seq");
	foreach $id (sort{$hash{$a}{seq} <=> $hash{$b}{seq}} keys %hash) {
		if ($id eq $tid) {
			$from_id	= $id;
			$from_seq	= $hash{$id}{seq};
			last;
		}
		$to_id	= $id;
		$to_seq	= $hash{$id}{seq};
	}
	#
	# move se tudo ok
	if (  ($from_id	ne "") && ($to_id ne "") && ($to_id ne $from_id) ) {
	    database_do("update web_help_topic set sequence='$from_seq' where id='$to_id'");
	    database_do("update web_help_topic set sequence='$to_seq' where id='$from_id'");
	}
	#
	# redireciona
	cgi_redirect("$my_url");	
}
sub do_topic_down()	{
	#
	# verifica tid
    $tid = clean_int(substr($form{tid},0,100));
    if ($tid eq "") {adm_error("Invalid topic id");return}
    %hash = database_select_as_hash("select 1,1,web_help_topic.group from web_help_topic where id='$tid'","flag,group");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown topic id");return}
	$gid = $hash{1}{group};
	#
	# calcula from e to 
	$from_id	= "";
	$from_seq	= "";
	$to_id		= "";
	$to_seq		= "";
	$get_next	= 0;
    %hash = database_select_as_hash("select id,sequence from web_help_topic where web_help_topic.group=$gid","seq");
	foreach $id (sort{$hash{$a}{seq} <=> $hash{$b}{seq}} keys %hash) {
		if ($get_next eq 1) {
			$to_id	= $id;
			$to_seq	= $hash{$id}{seq};
			last;
		}
		if ($id eq $tid) {
			$from_id	= $id;
			$from_seq	= $hash{$id}{seq};
			$get_next=1;
		}
	}
	#
	# move se tudo ok
	if (  ($from_id	ne "") && ($to_id ne "") && ($to_id ne $from_id) ) {
	    database_do("update web_help_topic set sequence='$from_seq' where id='$to_id'");
	    database_do("update web_help_topic set sequence='$to_seq' where id='$from_id'");
	}
	#
	# redireciona
	cgi_redirect("$my_url");
}
sub do_topic_del()	{
	#
	# verifica tid
    $tid = clean_int(substr($form{tid},0,100));
    if ($tid eq "") {adm_error("Invalid topic id");return}
    %hash = database_select_as_hash("select 1,1,web_help_topic.group,active from web_help_topic where id='$tid'","flag,group,active");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown topic id");return}
	$gid = $hash{1}{group};
	$active = $hash{1}{active};
	#
	# delete
	if ($active eq 1) {
		adm_error("I cannot delete active topic. You have to disable this topic before delete.");
		return;
	} else {
		database_do("delete from web_help_topic where id='$tid'");
	}
	#
	# redirect
	cgi_redirect("$my_url");
}
sub do_topic_flag()	{
	#
	# verifica tid
    $tid = clean_int(substr($form{tid},0,100));
    if ($tid eq "") {adm_error("Invalid topic id");return}
    %hash = database_select_as_hash("select 1,1,web_help_topic.group,active,flag from web_help_topic where id='$tid'","flag,group,active,topic_flag");
	unless ($hash{1}{flag} eq 1) {adm_error("Unknown topic id");return}
	$gid = $hash{1}{group};
	$active = $hash{1}{active};
	$flag = ($hash{1}{topic_flag} eq 1) ? 1 : 0;
	#
	# delete
	if ($flag eq 1) {
	    database_do("update web_help_topic set flag='0' where id='$tid'");
	} else {
	    database_do("update web_help_topic set flag='1' where id='$tid'");
	}
	#
	# redirect
	cgi_redirect("$my_url");
}
sub do_start(){
	#
	# inicializa
	%data = ();
    #
    # pega os grupos
    %hash = database_select_as_hash("select id,sequence,title from web_help_group","sequence,title");
    foreach $id_loop (keys %hash) {
		$data{$id_loop}{seq} 	= $hash{$id_loop}{sequence};
		$data{$id_loop}{title}	= $hash{$id_loop}{title};
	}
	#$data{unknown}{seq} 		= -1;
	#$data{unknown}{dont_edit} 	= 1;
	#$data{unknown}{title} 		= "Topics with no group";
    #
    # pega os topicos
    %hash = database_select_as_hash("select id,sequence,web_help_topic.group,title,active,flag from web_help_topic","sequence,group,title,active,flag");
    foreach $id_loop (keys %hash) {
		$gid = $hash{$id_loop}{group};
		$data{$gid}{topics}{$id_loop}{seq} 	= $hash{$id_loop}{sequence};
		$data{$gid}{topics}{$id_loop}{title}= $hash{$id_loop}{title};
		$data{$gid}{topics}{$id_loop}{active}= $hash{$id_loop}{active};
		$data{$gid}{topics}{$id_loop}{flag}	= $hash{$id_loop}{flag};
	}
	#
	# monta o html
	$html = "<br>";
	foreach $gid (sort{$data{$a}{seq} <=> $data{$b}{seq} } keys %data) {
		$html_loop = "";
		foreach $tid (sort{$data{$gid}{topics}{$a}{seq} <=> $data{$gid}{topics}{$b}{seq} } keys %{$data{$gid}{topics}}) {
			$title = ($data{$gid}{topics}{$tid}{title} eq "") ? "<font style='color:#c0c0c0;'>No title topic</font>" : $data{$gid}{topics}{$tid}{title};
			$icon = "page_white.png";
			$icon = ($data{$gid}{topics}{$tid}{flag} eq 1) ? "page_white_star.png" : $icon;
			$icon = ($data{$gid}{topics}{$tid}{active} ne 1) ? "page_white_error.png" : $icon;
			$html_loop .= qq[
			<div class=clear style="width:100%;height:21px;" onmouseOver="MyDisplay('t$tid',1)" onmouseOut="MyDisplay('t$tid',0)" >
				<div class=clear style="float:left">
					<a href=$myurl?action=topic_edit&tid=$tid>
					<img src=../design/icons/$icon hspace=0 vspace=0 border=0 style='margin-right:5px;' align=left>$title
					</a>
				</div>
				<div class=clear style="float:left; display:none;" id=t$tid>
					<div class=clear style="background-color:#FFFACD; height:16px; border:1px solid #000080; margin-left:5px; padding-left:5px; padding-right:5px;" >
					<a title="Show on first page"	href=$myurl?action=topic_flag&tid=$tid><img src=../design/icons/bullet_star.png hspace=0 vspace=0 border=0 xalign=left></a>
					<a title="Move up"				href=$myurl?action=topic_up&tid=$tid><img src=../design/icons/bullet_arrow_up.png hspace=0 vspace=0 border=0 xalign=left></a>
					<a title="Move down"			href=$myurl?action=topic_down&tid=$tid><img src=../design/icons/bullet_arrow_down.png hspace=0 vspace=0 border=0 xalign=left></a>
					<a title="Delete"				href=$myurl?action=topic_del&tid=$tid><img src=../design/icons/bullet_delete.png hspace=0 vspace=0 border=0 xalign=left></a>
					</div>
				</div>
				<div class=clear style='clear:both; margin-left:30px;'></div>
			</div>
			];
		}
		#if ($html_loop  eq "") {
		#	$html_loop = "<font style='color:#c0c0c0;'>No topics</font><br>";
		#}
		if ($data{$gid}{dont_edit} ne 1) {
			$title = ($data{$gid}{title} eq "") ? "<font style='color:#c0c0c0;'>No title group</font>" : $data{$gid}{title};
			$html .= qq[
			<div class=clear style="width:100%;" onmouseOver="MyDisplay('g$gid',1)" onmouseOut="MyDisplay('g$gid',0)" >
				<div class=clear style="float:left">
					<h1>
					<a href=$myurl?action=group_edit&gid=$gid><img src=../design/icons/folder_page_white.png hspace=0 vspace=0 border=0 style='margin-right:5px;' align=left></a>
					<a href=$myurl?action=group_edit&gid=$gid>$title</a>
					</h1>
				</div>
				<div class=clear style="float:left; display:none;" id=g$gid>
					<div class=clear style="background-color:#FFFACD; height:16px; border:1px solid #000080; margin-left:5px; padding-left:5px; padding-right:5px;" >
					<a title="Move up"		href=$myurl?action=group_up&gid=$gid><img src=../design/icons/bullet_arrow_up.png hspace=0 vspace=0 border=0 xalign=left></a>
					<a title="Move down"	href=$myurl?action=group_down&gid=$gid><img src=../design/icons/bullet_arrow_down.png hspace=0 vspace=0 border=0 xalign=left></a>
					<a title="Delete"		href=$myurl?action=group_del&gid=$gid><img src=../design/icons/bullet_delete.png hspace=0 vspace=0 border=0 xalign=left></a>
					</div>
				</div>
				<div class=clear style='clear:both; margin-left:30px;'></div>
			</div>
			<div id=dgdata$gid class=clear style='display:block; clear:both; margin-left:30px;'>
				$html_loop
				<a href=$myurl?action=topic_add&gid=$gid><img src=../design/icons/page_white_add.png hspace=0 vspace=0 border=0 style='margin-right:5px;' align=left><b>Create a new topic</b></a><br>
			</div>
			<br>
			];
		} else {
			$html .= qq[
			<h1><img src=../design/icons/folder_error.png hspace=0 vspace=0 border=0 style='margin-right:5px;' align=left>$data{$gid}{title}</h1>
			<div class=clear style='clear:both; margin-left:30px;'>
				$html_loop
			</div>
			<br>
			];
		}
	}
	$html .= "<h1><img src=../design/icons/folder_add.png hspace=0 vspace=0 border=0 style='margin-right:5px;' align=left><a href=$myurl?action=group_add>Add a new group</a></h1>";
    #
    # imprime pagina
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "Help topics";
	$t{dic}{title}	= "<a href=config.cgi>Settings</a> &#187; <a href=$my_url>Website help</a>";
    $t{dic}{content}= $html;
    &template_print("template.html",%t);
}
#========================================================================


