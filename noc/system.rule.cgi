#!/usr/bin/perl
require "include.cgi";
#=======================================================
# TODO: What is system rule? a test code? can we delete? we dont need test code in production with flaws to expose bussines data
#=======================================================
# lock this app to system.manager eyes only
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("system.manager") ne 1) {adm_error("no permission"); exit;}
#=======================================================




#=======================================================
# logout if no session
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
#unless (&active_user_permission_check("system.user_profile") eq 1) {adm_error("no permission"); exit;}
$my_url = "system.rule.cgi";
$action = $form{action};
if 		($action eq "do_rule_edit")	{ &do_rule_edit();		}
elsif	($action eq "do_rule_add")	{ &do_rule_add();		}
elsif	($action eq "do_rule_delete")	{ &do_rule_delete();		}
#-------------------------------------------------------------
elsif	($action eq "do_rule_stop")	{ &do_rule_stop();		}
elsif	($action eq "do_rule_start")	{ &do_rule_start();		}
#-------------------------------------------------------------kevin 2011.12.7
elsif	($action eq "do_stream_search")	{ &do_stream_search();		}
elsif	($action eq "view_rule_log")	{ &view_rule_log();		}
elsif	($action eq "view_stat")	{ &view_stat();		}

else	{&do_rule_list()};

exit;

sub do_rule_list {
	%t = &menu_permissions_get_as_template();

	$t{title}		= "Incoming Rule List";
	%hash = database_select_as_hash("select id,ani_rule,did_rule,dst_type,dst_body,term_call,rulename from system_dialplan",
									"ani_rule,did_rule,dst_type,dst_body,term_call,rulename");
	%did  = database_select_as_hash("select radio_data_station_id,radio_data_did.title,radio_data_station.title " .
									"from radio_data_did,radio_data_station " .
									"where radio_data_did.radio_data_station_id=radio_data_station.id and " .
									"radio_data_station_id is not null", 'did_title,station_title');
	%stream = database_select_as_hash("select id,title,extension from radio_data_station_channel " .
									  "where radio_data_station_id='$stationid'	and enabled != '0'", 'title,extension');

	$body  = '';
	for my $ruleid (sort {$a <=> $b} keys %hash) {
		if ($hash{$ruleid}{dst_type} == 2 ) {
			%s = database_select_as_hash("select 1,title,extension from radio_data_station_channel where id='$hash{$ruleid}{dst_body}'", "title");
			$hash{$ruleid}{dst_body} = $s{1}{title};
		}

		@ani_rule = split(",", $hash{$ruleid}{ani_rule});
		if ($#ani_rule > 2) {
			$ani_rule[3] = '...';
			$#ani_rule   = 3;
		}
		@did_rule = split(",", $hash{$ruleid}{did_rule});
		if ($#did_rule > 2) {
			$did_rule[3] = '...';
			$#did_rule   = 3;
		}

		if ($hash{$ruleid}{dst_type} == 1 ){
			$stop_button = "<a href='$my_url?action=do_rule_stop&id=$ruleid&dst_type=3'>STOP</a>";
			}
			elsif ($hash{$ruleid}{dst_type} == 2 ){
			$stop_button = "<a href='$my_url?action=do_rule_stop&id=$ruleid&dst_type=4'>STOP</a>";
			}
			elsif ($hash{$ruleid}{dst_type} == 3 ){
			$stop_button = "<a href='$my_url?action=do_rule_start&id=$ruleid&dst_type=1'><font color=green>START</font></a>";
			}
			elsif ($hash{$ruleid}{dst_type} == 4 ){
			$stop_button = "<a href='$my_url?action=do_rule_start&id=$ruleid&dst_type=2'><font color=green>START</font></a>";
			}

		$body .= "<tr><td>$hash{$ruleid}{rulename}</td><td>" . join ("<br>", @ani_rule). "</td><td>" .
				join("<br>", map {"$did{$_}{did_title} - $did{$_}{station_title}"} @did_rule).
				"</td><td>" . ($hash{$ruleid}{dst_type} == 1 ? 'Play Mp3' : 'Goto Stream') . "</td><td>$hash{$ruleid}{dst_body}" .
				"</td><td>" . ($hash{$ruleid}{term_call} ? 'Y' : 'N') .
				"</td><td width=330>$stop_button | <a href='$my_url?action=do_rule_edit&id=$ruleid'> EDIT</a> | <a href='$my_url?action=do_rule_delete&id=$ruleid' onclick='return del_tickets();'> DELETE</a></td></tr>";
	}

	$t{content} .= qq[
<script>

	function del_tickets() {
		var s = confirm("Are you sure to delete your selection?");
		if (s) {
			alert("processing...");
		} else {
			return false;
		}
	}

</script>
<a href='$my_url?action=do_rule_add'>Add New Rule</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href='$my_url?action=view_rule_log'>View Rule Log</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href='$my_url?action=view_stat'>View Stat</a><br>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>rulename</td>
		<td>Ani Rule</td>
		<td>Did Rule</td>
		<td>Dst type</td>
		<td>Dst Arg</td>
		<td>Terminate Call</td>
		<td>Action</td>
		</tr>
	</thead>
	<tbody>
		$body
	</tbody>
</table>
<br>
];

    &template_print("template.html",%t);
}

sub view_rule_log {
	%t = &menu_permissions_get_as_template();

	$t{title}		= "View Rule Log";
	@ar	   = localtime;
	$today = sprintf("%04d-%02d-%02d", $ar[5]+1900, $ar[4]+1, $ar[3]);
	$fromdate = $form{fromdate} || $today;
	$enddate  = $form{enddate}  || $today;
	$msg	  = $form{msg};
	$did	  = $form{did};
	$cond  = " where calltime > '$fromdate 00:00:00' and calltime < '$enddate 23:59:59' ";
	$cond .= " and msg='$msg' " if $msg;
	$cond .= " and did='$did' " if $did;

	%hash = database_select_as_hash("select id,host,did,ani ,msg,calltime from rule_log $cond", "host,ani,did,msg,calltime");
	%mp3  = database_select_as_hash("select distinct(msg),1 from rule_log", "flag");
	%did  = database_select_as_hash("select distinct(ani),1 from rule_log", "flag");
	$mp3_option = '';
	$did_option = '';
	$body  = '';
	$top_csv = "calltime,host,ani,did,msg\n";
	for  (sort {$b <=> $a} keys %hash) {
		$total++;
		$body .= "<tr><td>$hash{$_}{calltime}</td><td>$hash{$_}{host}</td><td>$hash{$_}{ani}</td><td>$hash{$_}{did}</td><td>$hash{$_}{msg}</td></tr>\n";
		$top_csv .= "$hash{$_}{calltime},$hash{$_}{host},$hash{$_}{ani},$hash{$_}{did},\"$hash{$_}{msg}\"\n";
	}

	for (keys %mp3) {
		next unless /.mp3$/;
		($v = $_) =~ s/rule matched://g;
		$mp3_option .= "<option value='$_'" . ($_ eq $msg ? ' SELECTED ' : '') . ">$v</option>\n";
	}

	$mp3_option = "<select name='msg'><option value=''></option>$mp3_option</select>";

	for (sort {$a <=> $b} keys %did) {
		$did_option .= "<option value='$_'" . ($_ eq $did ? ' SELECTED ' : '') . ">$_</option>\n";
	}

	$did_option = "<select name='did'><option value=''></option>$did_option</select>";

	$t{content} .= qq[
	<SCRIPT src="WebCalendar.js"/></SCRIPT>
	<form action="" method="get" name="userminute">
	From Date: <input type='text' onClick='SelectDate(this, \"yyyy-MM-dd\")' name='fromdate' value='$fromdate'/>
	End Date: <input type='text' onClick='SelectDate(this,\"yyyy-MM-dd\")' name='enddate' value='$enddate'/><br>
	Select Mp3: $mp3_option<br>
	Select Did: $did_option
	<input type="hidden" name='action' value='view_rule_log'/>
	<input type="submit" name="submit" value="search"/>
	</form>
<p>
Total: <font color="red">$total</font>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>calltime</td>
		<td>host</td>
		<td>ani</td>
		<td>did</td>
		<td>msg</td>
		</tr>
	</thead>
	<tbody>
		$body
	</tbody>
</table>
		<a 	href="$my_url?action=$action&fromdate=$fromdate&enddate=$endate&subaction=download&msg=$msg&did=$did">&#187 Download (csv format) </a>

<br>
];

    if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=rule_log.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}



}

sub view_stat {
	%t = &menu_permissions_get_as_template();

	$t{title}		= "New Rule Stat";
	%hash = database_select_as_hash("select host,count(*),count(distinct ani),count(distinct did) from rule_log group by host",
									"total,ani,did");

	$body  = '';
	for  (sort keys %hash) {
		$body .= "<tr><td>$_</td><td>$hash{$_}{total}</td><td>$hash{$_}{ani}</td><td>$hash{$_}{did}</td></tr>\n";
	}

	$t{content} .= qq[
<script>

	</script>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>HOST</td>
		<td>HITs</td>
		<td>DIDs</td>
		<td>ANIs</td>
		</tr>
	</thead>
	<tbody>
		$body
	</tbody>
</table>
<br>
];

    &template_print("template.html",%t);
}

sub do_rule_delete {
	do_rule_admin();
}

sub do_rule_add {
    %t = &menu_permissions_get_as_template();
	if ($form{submit}) {
		do_rule_admin();
	}


	$t{title}		= "Incoming Rule Add";

	%hash = database_select_as_hash("select radio_data_did.id,radio_data_did.title,radio_data_station.title,radio_data_station_id " .
									"from radio_data_did,radio_data_station " .
									"where radio_data_did.radio_data_station_id=radio_data_station.id and " .
									"radio_data_station_id is not null", 'did_title,station_title,radio_data_station_id');

	$mp3_options = "<select name='mp3' id='mp3'><option value=''> **** null ****</option>";
	while (<mp3/*.mp3>) {
		($n, $postfix) = $_ =~ m{([^\\\/]+?)\.([^\\\/]+)$};
		$mp3_options .= "<option value='$n'>$n</option>";
	}
	$mp3_options .= "</select>";

	$did_rule_options = '';
	for (sort {$a <=> $b} keys %hash) {
		$did_rule_options .= "<option value='$hash{$_}{radio_data_station_id}'>$hash{$_}{did_title} - $hash{$_}{station_title}</option>\n";
	}

	$station_options = '';
	%hash = database_select_as_hash("select id,title from radio_data_station", 'title');
	for (sort {$a <=> $b} keys %hash) {
		$station_options .= "<option value='$_'>$hash{$_}{title}</option>\n";
	}

    $t{content}	.= qq[
			<script>

			function station_change() {
				var stationid = \$('#station').val();
				if (!stationid) {
					alert("please select a station");
					return
				}
				\$('#stream').html('<option>please waiting...</option>');
				\$('#stream').attr('disabled', true);

				\$.get("$my_url", {action: "do_stream_search", stationid: stationid}, function(data) {
				\$('#stream').html(data);
				\$('#stream').attr('disabled', false);
				});
			}
			  function showPlayer(id,url){
				var vhtml = '<object id="wmp"';
				var userAg = navigator.userAgent;
				if(-1 != userAg.indexOf("MSIE")){
					vhtml+=' classid="clsid:6BF52A52-394A-11d3-B153-00C04F79FAA6"';
				}
				else if(-1 != userAg.indexOf("Firefox") || -1 != userAg.indexOf("Chrome") || -1 != userAg.indexOf("Opera") || -1 != userAg.indexOf("Safari")){
					vhtml+=' type="application/x-ms-wmp"';
				}
				vhtml+=' width="230" height="64">';
				vhtml+='<param name="URL" value="'+url+'"/>';
				vhtml+='<param name="autoStart" value="true" />';
				vhtml+='<param name="invokeURLs" value="false">';
				vhtml+='<param name="playCount" value="100">';
				vhtml+='<param name="Volume" value="100">';
				vhtml+='<param name="defaultFrame" value="datawindow">';
				vhtml+='</object>';

				document.getElementById(id).innerHTML = vhtml;
			}

			function listen () {
				\$('#player').show();
				\$('#addfile').hide();

				var url = "mp3/" + \$('#mp3').val() + '.mp3';
				alert(url);
				if (!url) {
					alert("Warning: Content Source Url is null");
					return false;
				}
				showPlayer('player', url);
			}

			function uploadfile() {
				\$('#player').hide();
				\$('#addfile').show();
			}

			function change_input() {
				\$('#ani_manually').show();
				\$('#ani_batch').hide();
			}
 			function change_batch() {
				\$('#ani_manually').hide();
				\$('#ani_batch').show();
			}

			</script>
			<form action=$my_url method=post style="padding-left:20px;" enctype ="multipart/form-data">
			<input type="hidden" name="action" value="do_rule_add"/>
			Rule Name:<br>
			<input type="text" size=60 name="rulename"></input><br>
			ANI rule: <a href='#' onclick='change_input();return false;'>input<a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href='#' onclick='change_batch();return false;'>Upload File</a><br>
			<div id='ani_manually'>
			(Multile anis separted by comma)<br>
				<input type="text" size=60 name="ani_rule"></input><br>
			</div>

			<div id='ani_batch' style="display: none">
				(only .txt file allowed,  one ani per line, less than 2M)<br>
				<input type="file" size=60 name="ani_file"></input>			<br>

			</div>
			DID rule:<br>
			<select name="did_rule" multiple="multiple" size=6>
			<option value=''> ** null ** </option>
				$did_rule_options
			</select>
			<br><br><br>

			<h3>Destination:</h3>
			<hr>
			<table>
			<tr>
				<td>
				<input type="radio" name="dst_type" value="1" /> Play Mp3: </td><td>$mp3_options &nbsp;&nbsp;
				<img src='listen.jpg' title='click to listen the mp3' onclick='listen();return false;' />&nbsp;&nbsp;
				<img src='add.jpg' title='click to add new mp3'  onclick='uploadfile();return false;'/>
				</td>
			</tr>
			<tr ><td></td><td id='player'></td></tr>
			<tr  id='addfile' style="display: none"><td><font color='red'>only mp3 allowed,less than 2M </font></td><td>
			<input type="file" name="newfile"/></td></tr>

			<tr>
				<td>
				<input type="radio" name="dst_type" value="2" /> Goto Stream: </td><td><select name="station" id="station" onchange="station_change();"/>
				 <option value='' selected > --select station-- </option>$station_options</select>&nbsp;
				<select name="stream" id="stream" disabled>
				<option value=''> --select stream-- </option><option value='12'>China Station stream</option></select>
				</td>
			</tr>
			<tr>
				<td>
				<input type="checkbox" name="terminatecall" value="1" /></td><td><font color='red'> Terminate Call</font>
				</td>
			</tr>
			</table>
			<input type="submit" name="submit" value="submit"/>
		</form>
	];
    &template_print("template.html",%t);


}

sub do_rule_edit {
    %t = &menu_permissions_get_as_template();
	if ($form{submit}) {
		do_rule_admin();
		return;
	}

	$id = clean_int($form{id});

	$t{title}		= "Incoming Rule Edit";
	%rule = database_select_as_hash("select id,ani_rule,did_rule,dst_type,dst_body,term_call,rulename from system_dialplan where id='$id'",
									"ani_rule,did_rule,dst_type,dst_body,term_call,rulename");

	%hash = database_select_as_hash("select radio_data_did.id,radio_data_did.title,radio_data_station.title,radio_data_station_id " .
									"from radio_data_did,radio_data_station " .
									"where radio_data_did.radio_data_station_id=radio_data_station.id and " .
									"radio_data_station_id is not null", 'did_title,station_title,radio_data_station_id');

	$mp3_options = "<select name='mp3' id='mp3'><option value=''> **** null ****</option>";
	while (<mp3/*.mp3>) {
		($n, $postfix) = $_ =~ m{([^\\\/]+?)\.([^\\\/]+)$};
		$mp3_options .= "<option value='$n'" . ($rule{$id}{dst_body} eq $n ? ' SELECTED ' : '') .  ">$n</option>";
	}
	$mp3_options .= "</select>";

	$did_rule_options = '';
	for (sort {$a <=> $b} keys %hash) {
		$did_rule_options .= "<option value='$hash{$_}{radio_data_station_id}'" .
			(",$rule{$id}{did_rule}," =~ /,$hash{$_}{radio_data_station_id},/ ? ' SELECTED ' : '') . ">$hash{$_}{did_title} - $hash{$_}{station_title}</option>\n";
	}
	$mp3_selected = '';
	$mp3_body = '';
	$stream_selected = '';
	$station_options = '';
	$stream_options  = "<option value=''> --select stream-- </option><option value='12'>China Station stream</option></select>";
	%station = database_select_as_hash("select id,title from radio_data_station", 'title');
	$term_calls_checked = ($rule{$id}{term_call} ? ' CHECKED ' : '');
	if ($rule{$id}{dst_type} == 1) {
		$mp3_selected = 'CHECKED';
		$mp3_body = $rule{$id}{dst_body};

		for (sort {$station{$a}{title} <=> $station{$b}{title}} keys %station) {
			$station_options .= "<option value='$_'>$station{$_}{title}</option>\n";
		}

	} else {
		$stream_selected = 'CHECKED';
		$streamid		 = $rule{$id}{dst_body};
		%stream = database_select_as_hash("select id,title,extension,radio_data_station_id from radio_data_station_channel " .
										  "where id='$streamid' and enabled != '0'", 'title,extension,stationid');

		$stationid = $stream{$streamid}{stationid};
		for (sort {$station{$a}{title} <=>  $station{$b}{title}} keys %station) {
			$station_options .= "<option value='$_'" . ($stationid == $_ ? ' SELECTED ' : '') .
								">$station{$_}{title}</option>\n";
		}

		$stream_options = '';
		%stream = database_select_as_hash("select id,title,extension from radio_data_station_channel " .
										"where radio_data_station_id='$stationid' and enabled != '0'", 'title,extension');
		for (sort {$stream{$a}{extension} <=> $stream{$b}{extension}} keys %stream) {
			$stream_options .= "<option value='$_'" . ($streamid == $_ ? ' SELECTED ' : '') . "> $stream{$_}{title} </option>\n";
		}
	}

    $t{content}	.= qq[
			<script>

			function station_change() {
				var stationid = \$('#station').val();
				if (!stationid) {
					alert("please select a station");
					return
				}
				\$('#stream').html('<option>please waiting...</option>');
				\$('#stream').attr('disabled', true);

				\$.get("$my_url", {action: "do_stream_search", stationid: stationid}, function(data) {
				\$('#stream').html(data);
				\$('#stream').attr('disabled', false);
				});
			}
			  function showPlayer(id,url){
				var vhtml = '<object id="wmp"';
				var userAg = navigator.userAgent;
				if(-1 != userAg.indexOf("MSIE")){
					vhtml+=' classid="clsid:6BF52A52-394A-11d3-B153-00C04F79FAA6"';
				}
				else if(-1 != userAg.indexOf("Firefox") || -1 != userAg.indexOf("Chrome") || -1 != userAg.indexOf("Opera") || -1 != userAg.indexOf("Safari")){
					vhtml+=' type="application/x-ms-wmp"';
				}
				vhtml+=' width="230" height="64">';
				vhtml+='<param name="URL" value="'+url+'"/>';
				vhtml+='<param name="autoStart" value="true" />';
				vhtml+='<param name="invokeURLs" value="false">';
				vhtml+='<param name="playCount" value="100">';
				vhtml+='<param name="Volume" value="100">';
				vhtml+='<param name="defaultFrame" value="datawindow">';
				vhtml+='</object>';

				document.getElementById(id).innerHTML = vhtml;
			}

			function listen () {
				\$('#player').show();
				\$('#addfile').hide();

				var url = "mp3/" + \$('#mp3').val() + '.mp3';
				alert(url);
				if (!url) {
					alert("Warning: Content Source Url is null");
					return false;
				}
				showPlayer('player', url);
			}

			function uploadfile() {
				\$('#player').hide();
				\$('#addfile').show();
			}

			function change_input() {
				\$('#ani_manually').show();
				\$('#ani_batch').hide();
			}
 			function change_batch() {
				\$('#ani_manually').hide();
				\$('#ani_batch').show();
			}

			</script>
			<form action=$my_url method=post style="padding-left:20px;" enctype ="multipart/form-data">
			<input type="hidden" name="action" value="do_rule_edit"/>
			<input type="hidden" name="id" value="$id"/>
			Rule Name:<br>
			<input type="text" size=60 name="rulename" value="$rule{$id}{rulename}"></input><br>
			ANI rule: <a href='#' onclick='change_input();return false;'>input<a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href='#' onclick='change_batch();return false;'>Upload File</a><br>
			<div id='ani_manually'>
			(Multile anis separted by comma)<br>
				<input type="text" size=60 name="ani_rule" value='$rule{$id}{ani_rule}'></input><br>
			</div>

			<div id='ani_batch' style="display: none">
				(only .txt file allowed, one ani per line, less than 2M)<br>
				<input type="file" size=60 name="ani_file"></input>			<br>

			</div>
			DID rule:<br>
			<select name="did_rule" multiple="multiple" size=6>
			<option value=''> ** null ** </option>

				$did_rule_options
			</select>
			<br><br><br>

			<h3>Destination:</h3>
			<hr>
			<table>
			<tr>
				<td>
				<input type="radio" name="dst_type" value="1" $mp3_selected/> Play Mp3: </td><td>$mp3_options &nbsp;&nbsp;
				<img src='listen.jpg' title='click to listen the mp3' onclick='listen();return false;' />&nbsp;&nbsp;
				<img src='add.jpg' title='click to add new mp3'  onclick='uploadfile();return false;'/>
				</td>
			</tr>
			<tr ><td></td><td id='player'></td></tr>
			<tr  id='addfile' style="display: none"><td><font color='red'>only mp3 allowed,less than 2M </font></td><td>
			<input type="file" name="newfile"/></td></tr>
			<tr>
				<td>
				<input type="radio" name="dst_type" value="2" $stream_selected/> Goto Stream: </td><td><select name="station" id="station" onchange="station_change();"/>
				 <option value='' selected > --select station-- </option>$station_options</select>&nbsp;
				<select name="stream" id="stream" disabled>
				$stream_options

				</td>
			</tr>
			<tr>
				<td>
				<input type="checkbox" name="terminatecall" value="1" $term_calls_checked/></td><td><font color='red'> Terminate Call</font>
				</td>
			</tr>
			</table>
			<input type="submit" name="submit" value="submit"/>
		</form>
	];
    &template_print("template.html",%t);


}

sub do_stream_search {
	$stationid = clean_int($form{'stationid'});
	%hash = database_select_as_hash("select id,title,extension from radio_data_station_channel where radio_data_station_id='$stationid' and enabled != '0'", 'title,extension');
	cgi_hearder_html();
	for (sort {$hash{$b}{extension} < $hash{$a}{extension}} keys %hash) {
		print "<option value='$_'> $hash{$_}{title} </option>\n";
	}
}
#----------------------------------
sub do_rule_stop {

	database_do("update system_dialplan set dst_type = '$form{dst_type}' where id = '$form{id}'");
refresh_url("$my_url");
}
sub do_rule_start {

	database_do("update system_dialplan set dst_type = '$form{dst_type}' where id = '$form{id}'");
refresh_url("$my_url");
}
#-----------------------------------kevin 2011.11.7
sub do_rule_admin {
	if ($action eq 'do_rule_delete') {
		$id = clean_int($form{id});
		database_do("delete from system_dialplan where id='$id'");
	} elsif ($action eq 'do_rule_add') {
		$ani_rule = database_clean_string($form{ani_rule});
		$ani_rule .= read_file('ani_file');
		$did_rule = database_clean_string($form{did_rule});
		$dst_type = clean_int($form{dst_type}) || _error('destination type is null');
		$mp3      = database_clean_string($form{mp3});
		$stream   = clean_int($form{stream});
		$term_call= clean_int($form{terminatecall});
		$rulename = database_clean_string($form{rulename});
		$dst_body = ($dst_type == 1 ? $mp3 : $stream);
		if ($dst_type == 1) {
			$dst_body ||= save_file('newfile');
		}

		database_do_insert("insert into system_dialplan(ani_rule,did_rule,dst_type,dst_body,term_call,rulename) values " .
						   "('$ani_rule', '$did_rule', $dst_type,  '$dst_body', '$term_call', '$rulename')");

	} elsif ($action eq 'do_rule_edit') {
		$ani_rule = database_clean_string($form{ani_rule});
		$ani_rule .= read_file('ani_file');

		$did_rule = database_clean_string($form{did_rule});
		$dst_type = clean_int($form{dst_type}) || _error('destination type is null');
		$mp3      = database_clean_string($form{mp3});
		$stream   = clean_int($form{stream});
		$term_call= clean_int($form{terminatecall});
		$rulename = database_clean_string($form{rulename});

		$dst_body = ($dst_type == 1 ? $mp3 : $stream);
		if ($dst_type == 1) {
			$dst_body ||= save_file('newfile');
		}
		warn %form;
		$id		  = clean_int($form{id}) || _error('id is null');

		warn "id: $id - $form{id}";
		warn "update system_dialplan set ani_rule='$ani_rule', did_rule='$did_rule', dst_type='$dst_type', " .
						   "dst_body='$dst_body', term_call='$term_call',name='$name' where id='$id'";
		database_do("update system_dialplan set ani_rule='$ani_rule', did_rule='$did_rule', dst_type='$dst_type', " .
						   "dst_body='$dst_body', term_call='$term_call',rulename='$rulename' where id='$id'");

	}

	refresh_url("$my_url");
}

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
		# check email
		$data = $form{g_email};
		$data = &clean_str(substr($data,0,255),"_-");
		if ($data ne "") {
			if ($form{g_email} ne $data) {$t{msg_error_g_email} = 1; $error=1}
		}
		$form{g_email} = $data;
		#
		# check password
		if ($form{password_action} eq 1) {
			$data0 = &clean_str(substr($form{password_active},0,255),"_-");
			$data1 = &clean_str(substr($form{password_new},0,255),"_-");
			$data2 = &clean_str(substr($form{password_retype},0,255),"_-");
			if ( (length($data1)<5) || (length($data1)>50) || ($form{password_new} ne $data1) || ($data1 eq "") || ($data1 ne $data2) ) {$t{msg_error_new_password} = 1; $error=1}
			if ( ($data0 eq "") || ($data0 ne $user_data{web_password}) ) {$t{msg_error_password} = 1; $error=1}
			$form{password} = $data1;
		}
		#
		# try to save
		if ($error eq 0) {
			#$tmp = ($form{g_email} ne "") ? $form{g_email} : $form{email};
			#$tmp = ($tmp eq "") ? time : $tmp;
			#$gravatar_url = "http://www.gravatar.com/avatar/". md5_hex(lc $tmp) ."?d=monsterid";
			#database_do("update $app{users_table} set name='$form{name}' , gravatar_email='$form{g_email}', gravatar_url='$gravatar_url', email='$form{email}' where id='$user_data{id}' ");
			if ($form{password_action} eq 1) {
				&database_do(&database_scape_sql("update $app{users_table} set web_password='%s' where id='%s' ",$form{password},$user_data{id}) );
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
	$msg_error 	= ($t{msg_error_password} eq 1) ? "Incorrect email<br>" : "";
	$msg_error 	= ($msg_error eq "") ? "" : "<font color=red><b>$msg_error</b></font>";
	$msg_ok 	= ($t{msg_ok} eq 1) ? "<font color=green><b>Saved.</b></font>" : "";
    $t{title}		= "Your account profile";
    $t{content}	.= qq[

			<form action=$my_url method=get style="padding-left:20px;">
			Your log-in:<br>
			<input name=web_user disabled read-only readonly value="$form{web_user}"><br>

			<br>
			Your contact name:<br>
			<input name=name value="$form{name}"><br>
			<br>

			Your contact email:<br>
			<input name=email value="$form{email}"><br>
			<br>
<!--
			Your <a href=http://en.gravatar.com/ target=_blank>gravatar</a> email:<br>
			<input name=g_email value="$form{g_email}"><br>
			<br>
-->
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

sub save_file() {
	($field, $id, $t) = @_;
	$name = $form{$field};
	return '' if !$name;
	($n, $postfix) = $name =~ m{([^\\\/]+?)\.([^\\\/]+)$};
	_error("upload file error") unless $postfix eq 'mp3';

	$fh  = $cgi->upload($field);

  # undef may be returned if it's not a valid file handle
	if (defined $fh) {
   		my $io = $fh->handle;
		open (OUTFILE, '>', "mp3/$n.mp3");
		while ($bytesread = $io->read($buffer,1024)) {
			print OUTFILE $buffer;
		}

		return $n;
	}

	_error("upload file error");
}

sub read_file() {
	($field, $id, $t) = @_;
	$name = $form{$field};
	return '' if !$name;
	($n, $postfix) = $name =~ m{([^\\\/]+?)\.([^\\\/]+)$};
	_error("upload file error") unless $postfix eq 'txt';

	$fh  = $cgi->upload($field);
	$str = '';
  # undef may be returned if it's not a valid file handle
	if (defined $fh) {
   		my $io = $fh->handle;
		open (OUTFILE, '>', "mp3/$n.txt");
		while ($bytesread = $io->read($buffer,1024)) {
			print OUTFILE $buffer;
		}

		close OUTFILE;

		open FH, "mp3/$n.txt";
		while (<FH>) {
			chomp;
			s/\r//g;
			$str .= ',' if $str;
			$str .= $_;
		}

		return $str;
	}

	_error("upload file error");
}

sub _error {
	($tip) = @_;
	cgi_hearder_html();
	print "<font color='red'>ERROR: $tip</font>";
	exit 0;
}


sub refresh_url () {
	($url) = @_;
	cgi_hearder_html();
	print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>EDIT</title>
<script>
window.location.href = "$url";
</script>

</head>

<body>
	<center> Update Successfully ...</center>
</body>
</html>
HTML
}
