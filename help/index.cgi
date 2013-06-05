#!/usr/bin/perl
require "../include.cgi";


#=======================================================
# main loop
#=======================================================
$my_url = "index.cgi";
$action = $form{action};
if ( ($action eq "") && ($form{topic} ne "") ) {$action="topic"}
if ( ($action eq "") && ($form{group} ne "") ) {$action="group"}
if ( ($action eq "") && ($form{search} ne "") ) {$action="search"}
if    ($action eq "search")		{ &do_search();}
elsif ($action eq "group")		{ &do_group();}
elsif ($action eq "topic")		{ &do_topic();}
else							{ &do_start();}
exit;
#=======================================================





#=======================================================
# actions
#=======================================================
sub do_topic() {
    #
    #--------------------------------------------------
    # inicializa o que for possivel
    #--------------------------------------------------
    %t = ();
	#
    #--------------------------------------------------
	# verifica topic_id
    #--------------------------------------------------
    $tid = clean_int(substr($form{topic},0,100));
    if ($tid eq "") {&do_start;return}
    %hash = database_select_as_hash("select 1,1,web_help_topic.group,title,text from web_help_topic where id='$tid'","flag,group,title,text");
	unless ($hash{1}{flag} eq 1) {&do_start;return}
	$t{dic}{"topic_title"} = $hash{1}{title};
	$t{dic}{"topic_text"} = $hash{1}{text};
	$t{dic}{"topic_id"} = $tid;
	$gid = $hash{1}{group};
	$form{group} = $gid;
    #
    #--------------------------------------------------
    # confere group_id
    #--------------------------------------------------
    $gid = clean_int(substr($form{group},0,100));
    if ($gid eq "") {&do_start;return}
    %hash = database_select_as_hash("select 1,1,title,text from web_help_group where id='$gid'","flag,title,text");
	unless ($hash{1}{flag} eq 1) {&do_start;return}
	$t{dic}{"group_title"} = $hash{1}{title};
	$t{dic}{"group_text"} = $hash{1}{text};
	$t{dic}{"group_id"} = $gid;
    #
    #--------------------------------------------------
    # trata search
    #--------------------------------------------------
	$t{dic}{"search"} = $form{search};
	$t{dic}{"search_encoded"} = &cgi_url_encode($form{search});
    #
    #--------------------------------------------------
    # get topics
    #--------------------------------------------------
    #%hash = database_select_as_hash("select id,title,sequence from web_help_topic where web_help_topic.group='$gid' and active=1","title,sequence");
	#$c = 1;
    #foreach $id_loop (sort{$hash{$a}{sequence} <=> $hash{$b}{sequence} } keys %hash) {
	#	$t{dic}{"topic_".$c."_id"} = $id_loop;
	#	$t{dic}{"topic_".$c."_title"} = $hash{$id_loop}{title};
	#	$c++;
	#}
    #
    #--------------------------------------------------
    # get groups
    #--------------------------------------------------
    %hash = database_select_as_hash("select id,title,sequence from web_help_group ","title,sequence");
	$c = 1;
    foreach $id_loop (sort{$hash{$a}{sequence} <=> $hash{$b}{sequence} } keys %hash) {
		$t{dic}{"group_".$c."_id"} = $id_loop;
		$t{dic}{"group_".$c."_title"} = $hash{$id_loop}{title};
		$c++;
	}
    #
    #--------------------------------------------------
    # imprime pagina
    #--------------------------------------------------
    $t{dic}{my_url}				= $my_url;
    &template_print("template.help.topic.html",%t);
}


sub do_search() {
    #
    #--------------------------------------------------
    # inicializa o que for possivel
    #--------------------------------------------------
    %t = ();
    #
    #--------------------------------------------------
    # trata search
    #--------------------------------------------------
	$t{dic}{"search"} = $form{search};
	$t{dic}{"search_encoded"} = &cgi_url_encode($form{search});
	$t{dic}{"search_found"} = 0;
    #
    #--------------------------------------------------
    # search topics
    #--------------------------------------------------
	%selected_topics = ();
	$search = &trim(&clean_str(substr($form{search},0,256),"\@.-_ ()<>"));
	if ($search ne "") {
		foreach $word ( split(/ +/,$search) ) {
			$word = trim($word);
			if ($word eq "") {next}
			$sql = "
			SELECT id,1 
			FROM web_help_topic 
			where title like \"\%$word\%\" and active=1 
			order by web_help_topic.timestamp desc
			limit 0,1000 
			";
			%hash = database_select_as_hash($sql,"flag");
			foreach $id (keys %hash) { $selected_topics{$id}{points} += 80; }
		}
		foreach $word ( split(/ +/,$search) ) {
			$word = trim($word);
			if ($word eq "") {next}
			$sql = "
			SELECT id,1 
			FROM web_help_topic 
			where keywords like \"\%$word\%\" and active=1 
			order by web_help_topic.timestamp desc
			limit 0,1000 
			";
			%hash = database_select_as_hash($sql,"flag");
			foreach $id (keys %hash) { $selected_topics{$id}{points} += 5; }
		}
		$selected_topics_ids = "";
		foreach (keys %selected_topics) { $selected_topics_ids .= "$_,"; }
		if ($selected_topics_ids ne "") {
			$selected_topics_ids = substr($selected_topics_ids,0,-1);
			%hash = database_select_as_hash("select id,title,sequence from web_help_topic where active=1 and id in ($selected_topics_ids) ","title,sequence");
			foreach $id (keys %hash) {
				unless (exists($selected_topics{$id})) {next}
				$selected_topics{$id}{title} = $hash{$id}{title};
			}
			$c = 1;
			foreach $id (sort{$selected_topics{$b}{points} <=> $selected_topics{$a}{points} } keys %selected_topics) {
				$t{dic}{"search_found"} = 1;
				$t{dic}{"topic_".$c."_id"} = $id;
				$t{dic}{"topic_".$c."_title"} = "(".$selected_topics{$id}{points}.") ". $selected_topics{$id}{title};
				$t{dic}{"topic_".$c."_title"} = $selected_topics{$id}{title};
				$c++;
			}
		}
	}
    #
    #--------------------------------------------------
    # get groups
    #--------------------------------------------------
    %hash = database_select_as_hash("select id,title,sequence from web_help_group ","title,sequence");
	$c = 1;
    foreach $id_loop (sort{$hash{$a}{sequence} <=> $hash{$b}{sequence} } keys %hash) {
		$t{dic}{"group_".$c."_id"} = $id_loop;
		$t{dic}{"group_".$c."_title"} = $hash{$id_loop}{title};
		$c++;
	}
    #
    #--------------------------------------------------
    # imprime pagina
    #--------------------------------------------------
    $t{dic}{my_url}				= $my_url;
    &template_print("template.help.search.html",%t);
}

sub do_group() {
    #
    #--------------------------------------------------
    # inicializa o que for possivel
    #--------------------------------------------------
    %t = ();
    #
    #--------------------------------------------------
    # confere group_id
    #--------------------------------------------------
    $gid = clean_int(substr($form{group},0,100));
    if ($gid eq "") {&do_start;return}
    %hash = database_select_as_hash("select 1,1,title,text from web_help_group where id='$gid'","flag,title,text");
	unless ($hash{1}{flag} eq 1) {&do_start;return}
	$t{dic}{"group_title"} = $hash{1}{title};
	$t{dic}{"group_text"} = $hash{1}{text};
	$t{dic}{"group_id"} = $gid;
    #
    #--------------------------------------------------
    # get topics
    #--------------------------------------------------
    %hash = database_select_as_hash("select id,title,sequence from web_help_topic where web_help_topic.group='$gid' and active=1","title,sequence");
	$c = 1;
    foreach $id_loop (sort{$hash{$a}{sequence} <=> $hash{$b}{sequence} } keys %hash) {
		$t{dic}{"topic_".$c."_id"} = $id_loop;
		$t{dic}{"topic_".$c."_title"} = $hash{$id_loop}{title};
		$c++;
	}
    #
    #--------------------------------------------------
    # get groups
    #--------------------------------------------------
    %hash = database_select_as_hash("select id,title,sequence from web_help_group ","title,sequence");
	$c = 1;
    foreach $id_loop (sort{$hash{$a}{sequence} <=> $hash{$b}{sequence} } keys %hash) {
		$t{dic}{"group_".$c."_id"} = $id_loop;
		$t{dic}{"group_".$c."_title"} = $hash{$id_loop}{title};
		$c++;
	}
    #
    #--------------------------------------------------
    # imprime pagina
    #--------------------------------------------------
    $t{dic}{my_url}				= $my_url;
    &template_print("template.help.group.html",%t);
}

sub do_start() {
    #
    #--------------------------------------------------
    # inicializa o que for possivel
    #--------------------------------------------------
    %t = ();
    #
    #--------------------------------------------------
    # get flag topics
    #--------------------------------------------------
    %hash = database_select_as_hash("select id,title,unix_timestamp(web_help_topic.timestamp) from web_help_topic where flag=1 and active=1","title,timestamp");
	$c = 1;
    foreach $id_loop (sort{$hash{$b}{timestamp} <=> $hash{$a}{timestamp} } keys %hash) {
		$t{dic}{"topic_".$c."_id"} = $id_loop;
		$t{dic}{"topic_".$c."_title"} = $hash{$id_loop}{title};
		$c++;
	}
    #
    #--------------------------------------------------
    # get groups
    #--------------------------------------------------
    %hash = database_select_as_hash("select id,title,sequence from web_help_group ","title,sequence");
	$c = 1;
    foreach $id_loop (sort{$hash{$a}{sequence} <=> $hash{$b}{sequence} } keys %hash) {
		$t{dic}{"group_".$c."_id"} = $id_loop;
		$t{dic}{"group_".$c."_title"} = $hash{$id_loop}{title};
		$c++;
	}
    #
    #--------------------------------------------------
    # imprime pagina
    #--------------------------------------------------
    $t{dic}{my_url}				= $my_url;
    &template_print("template.help.start.html",%t);
}
#=======================================================
