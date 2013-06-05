#!/usr/bin/perl
require "include.cgi";
#=======================================================
# TODO: What is system tools? test code? can we delete?
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

@group_id = database_select_as_array("SELECT group_id FROM system_user where id = '$app{session_cookie_u}'");


#------------------------------------------
if ($group_id[0]  == 2)
{
	 &view_log();	# jump to system admin
}
else	{&view_log_market()};# jump to market admin
#------------------------------------------Kevin 2011.12.11
exit;

sub view_log_market {


#$app{session_cookie_u} = 99;
my @radio_data_station_id = database_select_as_array("SELECT radio_data_station_id FROM radio_data_station_owner where system_user_id = '$app{session_cookie_u}'");

my $radio_data_station_id_in = join(',',@radio_data_station_id);


#------------------------------------------------------------------------	2011.12.11 KEVIN

	%t = &menu_permissions_get_as_template();
	$did = clean_int($form{did});
	$ani = clean_int($form{ani});

	$t{title}		= "View Call Log";
	$cond  = "";
	$cond .= "ani='$ani' " if $ani;
	$cond .= " and did='$did' " if $did;
#------------------------------------------------------------------------
	$cond .= " and radio_data_station_id in ($radio_data_station_id_in)";
#------------------------------------------------------------------------	2011.12.11 KEVIN
	$cond  = "where " . ($cond ? $cond : ' 1=0 ');

	%hash = database_select_as_hash("select id,datetime_start,datetime_stop,radio_data_station_id,ani,did,system_host,answered_time " .
									" from radio_log_session $cond ", "start,stop,stationid,ani,did,host,duration");


	$body  = '';
	$top_csv = "calltime,host,ani,did,msg\n";
	for  (sort {$b <=> $a} keys %hash) {
		$total++;


		$body .= "<tr><td>$hash{$_}{start}</td><td>$hash{$_}{stop}</td><td>$hash{$_}{stationid}</td><td>$hash{$_}{ani}</td><td>$hash{$_}{did}</td><td>$hash{$_}{host}</td><td>$hash{$_}{duration}</td></tr>\n";
		$top_csv .= "$hash{$_}{start},$hash{$_}{stop},$hash{$_}{stationid},$hash{$_}{ani},$hash{$_}{did},$hash{$_}{host},$hash{$_}{duration}\n";
	}



	$t{content} .= qq[
	<SCRIPT src="WebCalendar.js"/></SCRIPT>
	<form action="" method="get" name="userminute">
	ANI: <input type="text" name="ani" value=""/>&nbsp;DID: <input type="text" name="did" value="" />
	<input type="hidden" name='action' value='view_log'/>
	<input type="submit" name="submit" value="search"/>
	</form>
<p>
Total: <font color="red">$total</font>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>datetime_start</td>
		<td>datetime_stop</td>
		<td>radio_data_station_id</td>
		<td>ani</td>
		<td>did</td>
		<td>system_host</td>
		<td>answered_time</td>
		</tr>
	</thead>
	<tbody>
		$body
	</tbody>
</table>
		<a 	href="$my_url?action=$action&ani=$ani&did=$did">&#187 Download (csv format) </a>

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
#------------------------------------------Kevin 2011.12.11


sub view_log {


	%t = &menu_permissions_get_as_template();
	$did = clean_int($form{did});
	$ani = clean_int($form{ani});

	$t{title}		= "View Call Log";
	$cond  = "";
	$cond .= "ani='$ani' " if $ani;
	$cond .= " and did='$did' " if $did;
	$cond  = "where " . ($cond ? $cond : ' 1=0 ');

	%hash = database_select_as_hash("select id,datetime_start,datetime_stop,radio_data_station_id,ani,did,system_host,answered_time " .
									" from radio_log_session $cond ", "start,stop,stationid,ani,did,host,duration");


	$body  = '';
	$top_csv = "calltime,host,ani,did,msg\n";
	for  (sort {$b <=> $a} keys %hash) {
		$total++;


		$body .= "<tr><td>$hash{$_}{start}</td><td>$hash{$_}{stop}</td><td>$hash{$_}{stationid}</td><td>$hash{$_}{ani}</td><td>$hash{$_}{did}</td><td>$hash{$_}{host}</td><td>$hash{$_}{duration}</td></tr>\n";
		$top_csv .= "$hash{$_}{start},$hash{$_}{stop},$hash{$_}{stationid},$hash{$_}{ani},$hash{$_}{did},$hash{$_}{host},$hash{$_}{duration}\n";
	}



	$t{content} .= qq[
	<SCRIPT src="WebCalendar.js"/></SCRIPT>
	<form action="" method="get" name="userminute">
	ANI: <input type="text" name="ani" value=""/>&nbsp;DID: <input type="text" name="did" value="" />
	<input type="hidden" name='action' value='view_log'/>
	<input type="submit" name="submit" value="search"/>
	</form>
<p>
Total: <font color="red">$total</font>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>datetime_start</td>
		<td>datetime_stop</td>
		<td>radio_data_station_id</td>
		<td>ani</td>
		<td>did</td>
		<td>system_host</td>
		<td>answered_time</td>
		</tr>
	</thead>
	<tbody>
		$body
	</tbody>
</table>
		<a 	href="$my_url?action=$action&ani=$ani&did=$did">&#187 Download (csv format) </a>

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

