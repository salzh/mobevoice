#!/usr/bin/perl
require "lookup.cgi";
#=======================================================
# TODO: permissions and data at version2 are complete different then version1. we need review all code to approve
#=======================================================
# lock this app to system.manager eyes only
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("radio.report") ne 1) {adm_error("no permission"); exit;}
#=======================================================




use LWP::Simple;
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
#unless (&active_user_permission_check("radio.report")) {adm_error("no permission"); exit;}
#=======================================================



#=======================================================
# main loop
#=======================================================
$my_url = "users.reports-new.cgi";
$action = $form{action};
$action = shift if !$action;
$limit	= clean_int($form{limit}) || 100;
$did	= clean_str($form{did},'+', ''); ;
$did    = ($did ? $did : 'ALL');
$carrier= clean_str($form{carrier}, ',', '');
$carrier= ($carrier ? $carrier : 'ALL');

$subaction = $form{subaction} || '';

if 		($action eq "radio_report_now")	{ &do_radio_report_now();		}
elsif	($action eq "top_daily_users")  { &do_topdaily_reports();		}
elsif 	($action eq "top_weekly_users")	{ &do_topweekly_reports();		}
elsif	($action eq "top_monthly_users"){ &do_topmonthly_reports();	}
elsif   ($action eq "users_gone_up")    { &do_users_goneup();			}
elsif	($action eq "users_gone_down")  { &do_users_goneup(1);			}
elsif   ($action eq "top_daily_station")		{ &do_top_daily_station_reports(24, "Top Daily Station");	}
elsif   ($action eq "top_weekly_station")		{ &do_top_daily_station_reports(24*7, "Top Weekly Station");	}
elsif   ($action eq "top_monthly_station")		{ &do_top_daily_station_reports(24*30, "Top Monthly Station");	}
elsif	($action eq "user_no_name")		{ &do_noname_users();			}
elsif	($action eq "do_lookup_ani")	{ &do_lookup_ani();			}
elsif	($action eq "carrier_reports")	{ &do_carrier_reports();			}
elsif	($action eq "carrier_daily_reports")	{ &do_carrier_daily_reports();			}

else									{ &do_radio_report_now();		}
exit;
#=======================================================



#=======================================================
# actions
#=======================================================
sub do_radio_report_now_image(){
	print "content-type: image/png\n\n";
	$url = "https://zeno:acai4times\@tools.zenofon.com/collectd/bin/graph.cgi?$ENV{QUERY_STRING}";
	$cmd = "wget --no-check-certificate -q -o /dev/null -O - \"$url\" ";
	open(IN, "$cmd |");
	binmode STDOUT;
	binmode IN;
	print <IN>;
	close(IN);
}
sub do_radio_report_now(){
    #
    #-------------------------------
    # get db connections by users, to guess total calls by each server
    #-------------------------------
=pod
	%calls_by_area = ();
	$calls_by_area{ri1} = 0;
	$calls_by_area{ri2} = 0;
	$calls_by_area{rt14}= 0;
	$calls_by_area{rt15}= 0;
	$calls_by_area{rt16}= 0;
	$calls_by_area{rt99}= 0;

    %my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

	warn "SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id";

	%my_dids = database_select_as_hash("SELECT did,1 from radio_data_did,radio_data_station_owner " .
									   "WHERE radio_data_did.radio_data_station_id=radio_data_station_owner.radio_data_station_id " .
									   "AND system_user_id='$app{session_cookie_u}'");
	warn "SELECT did,1 from radio_data_did,radio_data_station_owner " .
									   "WHERE radio_data_did.radio_data_station_id=radio_data_station_owner.radio_data_station_id " .
									   "system_user_id='$app{session_cookie_u}'";

	%did_users = ();
	%did	   = database_select("SELECT did,ani,answered_time,UNIX_TIMESTAMP(datetime_start) FROM radio_log_session " .
								 "WHERE answered_time > 0 AND " . ($did eq 'ALL' ? '' : "did='$did' AND ") .
								 "UNIX_TIMESTAMP() - UNIX_TIMESTAMP(datetime_start) < " . $month*30*24*3600,
								 "did,ani,answered_time,datetime_start");
	%unique_did = database_select_as_hash("SELECT DISTINCT(did),1 FROM radio_log_session WHERE length(did) > 0");
	for (0..$did{ROWS}-1) {
		#$unique_did{$did{DATA}{$_}{did}} = 1 unless $unique_did{$did{DATA}{$_}{did}};
		next if $my_user{1}{group_id} == '24' && !$my_dids{$did{DATA}{$_}{did}};
		$k = $did{DATA}{$_}{ani} . "-" . $did{DATA}{$_}{did};
		#warn $k . " == " . $did{DATA}{$_}{answered_time};
		$did_users{$k}{total} += $did{DATA}{$_}{answered_time};
		$did_users{$k}{t}     += $did{DATA}{$_}{answered_time} if time- $did{DATA}{$_}{datetime_start} < $days*24*3600;
	}


	undef %did;
    #
    #-------------------------------
    # count top stations
    #-------------------------------
    $top_stations = "";
    $top_stations_count = 0;
	$total				= 0;
    $top_stations_empty = "<tr><td colspan=2><center>... empty ...</center></td></tr>";
    foreach (sort{$did_users{$b}{total} <=> $did_users{$a}{total}} keys %did_users){
		next unless $did_users{$_}{total} >= $range;
		next if $did_users{$_}{t}	  > 0;   #user did make call in {days}
		$total++;
		($a, $d) = split '-', $_, 2;
		$t		 = int ($did_users{$_}{total} / 60);
		$h		 = lookup($a);
		$top_stations .= "<tr><td>$a</td><td class=ar>$h->{name}</td><td>$d</td>" .
						 "<td>$h->{carriername}</td><td>$t</td><td><a href='#'>click</a></td></tr>\n";

		#$tmp = $stations{$_}{calls}; $tmp++; $tmp--;
		#$top_stations_count += $tmp;

    }

=pod
	$choise = "<h3>Last <a href=\"system.users.cgi?range=$range&&month=1\"><font color=\""  . ($month == 1 ? 'red' : 'black') .
			  "\"> 1 </font></a> |" .
			  "<a href=\"system.users.cgi?range=$range&&month=2\"><font color=\""  . ($month == 2 ? 'red' : 'black') .
			  "\"> 2 </font></a> |" .
			  "<a href=\"system.users.cgi?range=$range&&month=3\"><font color=\""  . ($month == 3 ? 'red' : 'black') .
			  "\"> 3 </font></a> |" .
			  "<a href=\"system.users.cgi?range=$range&&month=4\"><font color=\""  . ($month == 4 ? 'red' : 'black') .
			  "\"> 4 </font></a> |" .
			  "<a href=\"system.users.cgi?range=$range&&month=5\"><font color=\""  . ($month == 5 ? 'red' : 'black') .
			  "\"> 5 </font></a> |" .
			  "<a href=\"system.users.cgi?range=$range&&month=6\"><font color=\""  . ($month == 6 ? 'red' : 'black') .
			  "\"> 6 </font></a> " . "Month </h3></br>\n" .
			  "<a href=\"system.users.cgi?range=3600&&month=$month\"><font color=\""  . ($range == 3600 ? 'red' : 'black') .
			  "\"> more than 1 hour </font></a> |" .
			  "<a href=\"system.users.cgi?range=18000&&month=$month\"><font color=\"" . ($range == 18000 ? 'red' : 'black') .
			  "\"> more than 5 hour </font></a> |" .
			  "<a href=\"system.users.cgi?range=36000&&month=$month\"><font color=\"" . ($range == 36000 ? 'red' : 'black') .
			  "\"> more than 10 hour </font></a> |" .
			  "<a href=\"system.users.cgi?range=72000&&month=$month\"><font color=\"" . ($range == 72000 ? 'red' : 'black') .
			  "\"> more than 20 hour </font></a>" ;

$didselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_did) {
	next if $my_user{1}{group_id} == '24' && !$my_dids{$_};
	$didselecthtml .= "<option value=\"$_\"" . ($did eq "$_" ? ' SELECTED' : '') . "> $_ </option>";
}

$choise = '<form action="" method="get" name="userminute">' .
		  "No Call Days  : <input type=\"text\" value=\"$days\" name=\"days\" style=\"width: 50px;\"/>" .
		  '&nbsp;&nbsp;&nbsp;' .
		  'Months: <select name="month"  style="width: 80px;" id="month">' .
		  '<option value="1"' . ($month eq '1' ? ' SELECTED' : '') . '> 1 </option>' .
 		  '<option value="2"' . ($month eq '24' ? ' SELECTED' : '') . '> 2 </option>' .
 		  '<option value="3"' . ($month eq '3' ? ' SELECTED' : '') . '> 3 </option>' .
 		  '<option value="4"' . ($month eq '4' ? ' SELECTED' : '') . '> 4 </option>' .
 		  '<option value="5"' . ($month eq '5' ? ' SELECTED' : '') . '> 5 </option>' .
 		  '<option value="6"' . ($month eq '6' ? ' SELECTED' : '') . '> 6 </option>' .
		  '</select>' .
		  'Hours: <select name="range"  style="width: 80px;" id="range">' .
		  '<option value="3600"' . ($range eq '3600' ? ' SELECTED' : '') . '> 1 </option>' .
		  '<option value="18000"' . ($range eq '18000' ? ' SELECTED' : '') . '> 5 </option>' .
		  '<option value="36000"' . ($range eq '36000' ? ' SELECTED' : '') . '> 10 </option>' .
		  '<option value="72000"' . ($range eq '72000' ? ' SELECTED' : '') . '> 20 </option>' .
		  '</select>' .
		  'Did  : <select name="did"  style="width: 100px;" id="range">' .
		  $didselecthtml . '</select>' .
		  '<input type="submit" value="view" />' .
	      '</form>';

=cut

	#
    #-------------------------------
    # count average minutes last hour
    #-------------------------------
    #-------------------------------
	# print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Users Report List";
    $t{content} = "";

	# add extra info for admin
	$t{content} .= qq[

<ul>
	<li><a href="$myurl?action=top_daily_users"> Top Daily Users </a></li>
	<li><a href="$my_url?action=top_weekly_users"> Top Weekly Users </a></li>
	<li><a href="$myurl?action=top_monthly_users"> Top Monthly Users</a></li>
	<li><a href="$myurl?action=top_daily_station"> Top Daily Stations </a></li>
	<li><a href="$myurl?action=top_weekly_station"> Top Weekly Stations </a></li>
	<li><a href="$myurl?action=top_monthly_station"> Top Monthly Stations </a></li>
	<li><a href="$myurl?action=users_gone_up"> Gone Up Users</a></li>
	<li><a href="$myurl?action=users_gone_down"> Gone Down Users</a></li>
	<li><a href="$myurl?action=user_no_name"> No Name attached Users </a></li>
	<li><a href="$myurl?action=carrier_reports"> Daily Carrier Reports </a></li>
	<li><a href="$myurl?action=carrier_daily_reports"> Carrier Daily Reports </a></li>

</ul>
	];
	#

#		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear><tr>
#			<td valign=top>
#				<img id=img_ra width=330 height=125 src=/noc/design/spc.gif  hspace=0 vspace=0 border=0 ><br>
#				<br>
#				<h1>Calls by area</h1>
#				<br>
#				<b>Radio Iowa total:</b> $calls_by_area{ti}<br>
#				<b>Radio Iowa 1:</b> $calls_by_area{ri1}<br>
#				<b>Radio Iowa 2:</b> $calls_by_area{ri2}<br>
#				<br>
#				<b>Radio Texas total:</b> $calls_by_area{tt}<br>
#				<b>Radio Texas 14:</b> $calls_by_area{rt14}<br>
#				<b>Radio Texas 15:</b> $calls_by_area{rt15}<br>
#			</td>
#			<td>
#			<td valign=top>
#				<img id=img_ria width=330 height=125 src=/noc/design/spc.gif  hspace=0 vspace=0 border=0 ><br>
#				<img id=img_ri1 width=330 height=125 src=/noc/design/spc.gif  hspace=0 vspace=0 border=0 ><br>
#				<img id=img_ri2 width=330 height=125 src=/noc/design/spc.gif  hspace=0 vspace=0 border=0 >
#			</td>
#			<td valign=top>
#				<img id=img_rta  width=330 height=125 src=/noc/design/spc.gif  hspace=0 vspace=0 border=0 ><br>
#				<img id=img_rt14 width=330 height=125 src=/noc/design/spc.gif  hspace=0 vspace=0 border=0 ><br>
#				<img id=img_rt15 width=330 height=125 src=/noc/design/spc.gif  hspace=0 vspace=0 border=0 >
#			</td>
#		</tr>
#		</table>

	#
	$t{content} .= qq[



	];
	&template_print("template.html",%t);
}

sub do_topdaily_reports_old{
	($interval, $title) = @_;
	$interval  ||= 24;
	$title	   ||= "Top Daily Users";

	%did_users = database_select_as_hash("SELECT ani,SUM(answered_time) total FROM radio_log_session " .
									"WHERE datetime_start>date_sub(now(),interval $interval hour)	 " .
									"GROUP BY ani ORDER BY total DESC LIMIT $limit", "total");

	    #-------------------------------
    # count top stations
    #-------------------------------
    $top_stations = "";
	$top_csv	  = "";
    $top_stations_count = 0;
	$total				= 0;
    $top_stations_empty = "<tr><td colspan=2><center>... empty ...</center></td></tr>";
	$i					= 1;
    foreach (sort{$did_users{$b}{total} <=> $did_users{$a}{total}} keys %did_users){
		next unless $did_users{$_}{total} >= $range;
		next if $did_users{$_}{t}	  > 0;   #user did make call in {days}
		$total++;
		$t		 = int ($did_users{$_}{total} / 60);
		$h		 = lookup($_);
		$top_stations .= "<tr><td>$i</td><td>$_</td><td class=ar><a href='#' " .
						 "onclick=\"window.open('system.users.cgi?action=radio_edit_username&ani=$_&name=$h->{name}', 'EDIT','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');return false;\">$h->{name}</td>" .
						 "<td>$h->{carriername}</td><td>$t</td><td><a href='#'>click</a></td></tr>\n";
		$top_csv	 .= "$i,$_,\"$h->{name}\",\"$h->{carriername}\",$t\n";

		$i++;
		#$tmp = $stations{$_}{calls}; $tmp++; $tmp--;
		#$top_stations_count += $tmp;

    }

$choise = '<form action="" method="get" name="userminute">' .
		  "<input type=\"hidden\" name=\"action\" value=\"$action\" />" .
		  "Count: <input type=\"text\" value=\"$limit\" name=\"limit\" style=\"width: 50px;\"/>" .
		  '<input type="submit" value="view" />' .
	      '</form>';
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= $title;
    $t{content} = "";
	#


	$t{content} .= qq[
$choise
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Seq</td>
		<td>CallerID</td>
		<td>Name</td>
		<td>Carrier</td>
		<td>Total Minute</td>
		<td>Action</td>
		</tr>
	</thead>
	<tbody>
		$top_stations
	</tbody>
</table>
<br>
<a 	href="users.reports.cgi?action=$action&limit=$limit&subaction=download">&#187 Download (csv format) </a>


	];
	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=$action.csv\n";
		print "\n";

		print "Seq,CallerID,Name,Carrier,Total Minute\n$top_csv";
	} else {
		&template_print("template.html",%t);
	}
}

sub do_topdaily_reports{
	($interval, $title) = @_;
	$interval  ||= 24;
	$title	   ||= "Top Daily Users";

    %my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

	warn "SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id";

	%my_dids = database_select_as_hash("SELECT did,1 from radio_data_did,radio_data_station_owner " .
									   "WHERE radio_data_did.radio_data_station_id=radio_data_station_owner.radio_data_station_id " .
									   "AND system_user_id='$app{session_cookie_u}'");
	warn "SELECT did,1 from radio_data_did,radio_data_station_owner " .
									   "WHERE radio_data_did.radio_data_station_id=radio_data_station_owner.radio_data_station_id " .
									   "system_user_id='$app{session_cookie_u}'";

	%did_users = ();
	%did	   = database_select("SELECT did,ani,answered_time FROM radio_log_session " .
								 "WHERE answered_time > 0 AND " . ($did eq 'ALL' ? '' : "did='$did' AND ") .
								 " datetime_start > date_sub(now(),interval $interval hour)",
								 "did,ani,answered_time");

	warn "finsih lookup radio_log_session";
	%unique_did = database_select_as_hash("SELECT DISTINCT(did),1 FROM radio_log_session WHERE length(did) > 0");

	%ani_carrier = database_select_as_hash("SELECT ani,carriername FROM ani_lookup", "carriername");

	%did_radio		= database_select_as_hash("select did,radio_data_station.title from radio_data_did,radio_data_station " .
											  "where radio_data_did.radio_data_station_id=radio_data_station.id", "title");

	for (0..$did{ROWS}-1) {
		#$unique_did{$did{DATA}{$_}{did}} = 1 unless $unique_did{$did{DATA}{$_}{did}};
		next if $my_user{1}{group_id} == '24' && !$my_dids{$did{DATA}{$_}{did}};
		if ($carrier && $carrier ne 'ALL') {
			#$h = lookup();
			$ani = $did{DATA}{$_}{ani};
			$ani = "+$ani" unless $k =~ /^\+/;
			next unless $carrier eq $ani_carrier{$ani}{carriername};
		}
		$k = $did{DATA}{$_}{ani} . "-" . $did{DATA}{$_}{did};
		#warn $k . " == " . $did{DATA}{$_}{answered_time};
		$did_users{$k} += $did{DATA}{$_}{answered_time};
	}

	%unique_carrier = database_select_as_hash("SELECT distinct(carriername),1 from ani_lookup");

	undef %did;
    #
    #-------------------------------
    # count top stations
    #-------------------------------
    $top_stations = "";
    $top_csv	  = "";

    $top_stations_count = 0;
	$total				= 0;
    $top_stations_empty = "<tr><td colspan=2><center>... empty ...</center></td></tr>";
	$i					= 1;
    foreach (sort{$did_users{$b} <=> $did_users{$a}} keys %did_users){
		last if $i > $limit;
		$total++;
		($a, $d) = split '-', $_, 2;
		$t		 = int ($did_users{$_} / 60);
		$h		 = lookup($a);

		$top_stations .= "<tr><td>$i</td><td>$a</td><td class=ar><a href='#' " .
						 "onclick=\"window.open('system.users.cgi?action=radio_edit_username&ani=$a&name=$h->{name}', 'EDIT','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');return false;\">$h->{name}</td><td>$d</td><td>$did_radio{$d}{title}</td>" .
						 "<td>$h->{carriername}</td><td>$t</td></tr>\n";
		$top_csv	 .= "$i,$a,\"$h->{name},$d,\"$did_radio{$d}{title}\",\"$h->{carriername}\",$t\n";
		$i++;


		#$tmp = $stations{$_}{calls}; $tmp++; $tmp--;
		#$top_stations_count += $tmp;

    }


$didselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_did) {
	next if $my_user{1}{group_id} == '24' && !$my_dids{$_};
	$didselecthtml .= "<option value=\"$_\"" . ($did eq "$_" ? ' SELECTED' : '') . "> $_-$did_radio{$_}{title} </option>";
}

$carrierselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_carrier) {
	$carrierselecthtml .= "<option value=\"$_\"" . ($carrier eq "$_" ? ' SELECTED' : '') . "> $_ </option>";
}

$choise = '<form action="" method="get" name="userminute">' .
		  "Limit: <input type=\"text\" name=\"limit\" value=\"$limit\" />".
		  "<input type=\"hidden\" name=\"action\" value=\"$action\" />".
		  'Did  : <select name="did"  style="width: 125px;" id="range">' .
		  $didselecthtml . '</select>' .
		  'Carrier: <select name="carrier"  style="width: 125px;" id="range">' .
		  $carrierselecthtml . '</select>' .


		  '<input type="submit" value="view" />' .
		  '</form>';



	#
    #-------------------------------
    # count average minutes last hour
    #-------------------------------
    #-------------------------------
	# print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= $title;
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[

$choise
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Seq</td>
		<td>CallerID</td>
		<td>Name</td>
		<td>DID</td>
		<td>Radio Name</td>
		<td>Carrier</td>
		<td>Total Minute</td>
		</tr>
	</thead>
	<tbody>
		$top_stations
	</tbody>
</table>
<br>
<a 	href="$my_url?action=$action&limit=$limit&subaction=download&did=$did&&carrier=$carrier">&#187 Download (csv format) </a>

	];
	$t{content} .= qq[



	];
	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=$title.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}
}

sub do_topweekly_reports{
	do_topdaily_reports(7*24, "Top Weekly Users");

}

sub do_topmonthly_reports{
	do_topdaily_reports(30*24, "Top Monthly Users");
}

sub do_users_goneup{
	$mode  = shift;
	$title = ($mode ? 'Users Gone Down' : 'Users Gone Up');

	$maxdays  = 7;

    %my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

	warn "SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id";

	%tmp     = database_select("SELECT system_user_id,radio_data_station_id,title from radio_data_station_owner,radio_data_station " .
							   "WHERE radio_data_station_owner.radio_data_station_id=radio_data_station.id",
								"system_user_id,radio_data_station_id,title");
	%station = ();
	for (0..$tmp{ROWS}-1) {
		$station{$tmp{DATA}{$_}{system_user_id}}{$tmp{DATA}{$_}{radio_data_station_id}} = 1;
		$station{title}{$tmp{DATA}{$_}{radio_data_station_id}} = $tmp{DATA}{$_}{title} unless $station{title}{$tmp{DATA}{$_}{radio_data_station_id}};
	}

	%did_users = ();
	%my_dids = database_select_as_hash("SELECT did,1 from radio_data_did,radio_data_station_owner " .
									   "WHERE radio_data_did.radio_data_station_id=radio_data_station_owner.radio_data_station_id " .
									   "AND system_user_id='$app{session_cookie_u}'");

	%unique_did = database_select_as_hash("SELECT DISTINCT(did),1 FROM radio_log_session WHERE length(did) > 0");

	%ani_carrier = database_select_as_hash("SELECT ani,carriername FROM ani_lookup", "carriername");


	%unique_carrier = database_select_as_hash("SELECT distinct(carriername),1 from ani_lookup");

	%did_radio		= database_select_as_hash("select did,radio_data_station.title from radio_data_did,radio_data_station " .
											  "where radio_data_did.radio_data_station_id=radio_data_station.id", "title");
	$did_str = '1';
	if ($did && $did ne 'ALL') {
		$did_str = "did='$did'";
	} else {
		if ($my_user{1}{group_id} == '24') {
			$did_str = " did IN (" . join(",",map("'$_'", keys %my_dids)) . ")";
		}
	}
	$now	 = time;
	@ar	     = localtime;
	$nowstr  = sprintf("%04d-%02d-%02d %02d:%02d:%02d", $ar[5]+1900, $ar[4]+1, $ar[3], 0,0,0);

	warn $nowstr;
	$interval = $maxdays;
	%hash = database_select("SELECT ani,did, answered_time,UNIX_TIMESTAMP(datetime_start) unixtime_start FROM radio_log_session " .
						   "WHERE ani != '' AND did != '' AND answered_time > 0 AND "  .
							" datetime_start < '$nowstr' AND datetime_start > DATE_SUB('$nowstr', INTERVAL $interval DAY) AND $did_str",
						    "ani,did,answered_time,unixtime_start");

	$time = $ar[2]*3600 + $ar[1]*60 + $ar[0];

	%ani_minutes = ();
	for (0..$hash{ROWS}-1) {
		#warn "$_ || $hash{$_}{unixtime_start} || $hash{$_}{answered_time}";
		next if $hash{DATA}{$_}{unixtime_start} >= $now-$time; #filter today's log

		$wd = int(($now-$time-$hash{DATA}{$_}{unixtime_start}) / (24*3600)) + 1;
		next if $wd > $maxdays;
		$k = $hash{DATA}{$_}{ani} . "-" . $hash{DATA}{$_}{did};
		$ani_minutes{$k}{$wd}	  += $hash{DATA}{$_}{answered_time};
		$ani_minutes{$k}{total}   += $hash{DATA}{$_}{answered_time};
	}

	$maxgonedays = 1;
	for my $ani (keys %ani_minutes) {
		$d = 1;
		for (2..$maxdays) {
			if ($mode) {
				last if $ani_minutes{$ani}{$_} <= $ani_minutes{$ani}{$_-1};
			} else {
				last if $ani_minutes{$ani}{$_} >= $ani_minutes{$ani}{$_-1};
			}

			$d++;
		}

		$maxgonedays = $d if $d > $maxgonedays;
		$ani_minutes{$ani}{keepdays} = $d;
	}

    $top_stations = "";
    $top_csv	  = "";

    $top_stations_count = 0;
	$total				= 0;
    $top_stations_empty = "<tr><td colspan=2><center>... empty ...</center></td></tr>";
	$i					= 1;
    foreach (sort{$ani_minutes{$b}{keepdays} <=> $ani_minutes{$a}{keepdays} or $ani_minutes{$b}{total} <=> $ani_minutes{$a}{total} } keys %ani_minutes){
		last if $i > $limit;
		$total++;
		($a, $d) = split '-', $_, 2;

		$h = lookup($a);
		next if $carrier ne 'ALL' && $carrier ne $h->{carriername};

		$ani_minutes{$_}{total} = int ($ani_minutes{$_}{total}/60);
		$m1 = int ($ani_minutes{$_}{1} / 60) || 0;
		$m2 = int ($ani_minutes{$_}{2} / 60) || 0;
		$m3 = int ($ani_minutes{$_}{3} / 60) || 0;
		$m4 = int ($ani_minutes{$_}{4} / 60) || 0;
		$m5 = int ($ani_minutes{$_}{5} / 60) || 0;
		$m6 = int ($ani_minutes{$_}{6} / 60) || 0;
		$m7 = int ($ani_minutes{$_}{7} / 60) || 0;
		$top_stations .= "<tr><td>$i</td><td>$a</td><td>$d</td><td>$did_radio{$d}{title}</td><td>$h->{name}</td><td class=ar>$h->{carriername}</td>" .
						 "<td>$ani_minutes{$_}{keepdays}</td><td>$ani_minutes{$_}{total}</td>" .
						 "<td>$m1</td><td>$m2</td><td>$m3</td><td>$m4</td><td>$m5</td><td>$m6</td><td>$m7</td></tr>\n";
		$top_csv	 .= "$i,$a,$d,\"$did_radio{$d}{title}\",\"$h->{name}\",\"$h->{carriername}\",$ani_minutes{$_}{keepdays},$ani_minutes{$_}{total}," .
						",$m1,$m2,$m3,$m4,$m5,$m6,$m7\n";
		$i++;


		#$tmp = $stations{$_}{calls}; $tmp++; $tmp--;
		#$top_stations_count += $tmp;

    }

$didselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_did) {
	next if $my_user{1}{group_id} == '24' && !$my_dids{$_};
	$didselecthtml .= "<option value=\"$_\"" . ($did eq "$_" ? ' SELECTED' : '') . "> $_  - $did_radio{$_}{title} </option>";
}

$carrierselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_carrier) {
	$carrierselecthtml .= "<option value=\"$_\"" . ($carrier eq "$_" ? ' SELECTED' : '') . "> $_ </option>";
}


$choise = '<form action="" method="get" name="userminute">' .
		  'Limit: <select name="limit" style="width: 80px;" />' .
		  '<option value="100" ' . ($limit eq '100' ? 'SELECTED' : '') . '> 100 </option>' .
		  '<option value="200" ' . ($limit eq '200' ? 'SELECTED' : '') . '> 200 </option>' .
		  '<option value="300" ' . ($limit eq '300' ? 'SELECTED' : '') . '> 300 </option>' .
		  '<option value="400" ' . ($limit eq '400' ? 'SELECTED' : '') . '> 400 </option>' .
		  '<option value="500" ' . ($limit eq '500' ? 'SELECTED' : '') . '> 500 </option>' .
		  '<option value="1000" ' . ($limit eq '1000' ? 'SELECTED' : '') . '> 1000 </option>' .
		  "</select>" .
		  "<input type=\"hidden\" name=\"action\" value=\"$action\" />".
		  'Did  : <select name="did"  style="width: 125px;" id="range">' .
		  $didselecthtml . '</select>' .
		  'Carrier: <select name="carrier"  style="width: 125px;" id="range">' .
		  $carrierselecthtml . '</select>' .


		  '<input type="submit" value="view" />' .
		  '</form>';



	#
    #-------------------------------
    # count average minutes last hour
    #-------------------------------
    #-------------------------------
	# print page
    #-------------------------------

	%t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= $title;
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[

$choise
<font color="blue">Max $title keep days: <font color="red">$maxgonedays</font></font>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Seq</td>
		<td>Ani</td>
		<td>Did</td>
		<td>Radio Title</td>
		<td>Name</td>
		<td>Carrier</td>
		<td>$title<br> Keep Days</td>
		<td>Total Minutes IN <br>Last $maxdays days</td>
		<td><font color="red">Yesterday</font></td>
		<td>2D</td>
		<td>3D</td>
		<td>4D</td>
		<td>5D</td>
		<td>6D</td>
		<td>7D</td>
		</tr>
	</thead>
	<tbody>
		$top_stations
	</tbody>
</table>
<br>
<a 	href="$my_url?action=$action&limit=$limit&subaction=download&did=$did&&carrier=$carrier">&#187 Download (csv format) </a>

	];

	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=$title.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}



}

sub do_users_gonedown {
	%t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= $title;
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[
		Page Will Come Soon ...

	];
	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=$title.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}


}


sub do_top_daily_station_reports{
		($interval, $title) = @_;
	$interval  ||= 24;
	$title	   ||= "Top Daily Users";

    %my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

	warn "SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id";

	%tmp     = database_select("SELECT system_user_id,radio_data_station_id,title from radio_data_station_owner,radio_data_station " .
							   "WHERE radio_data_station_owner.radio_data_station_id=radio_data_station.id",
								"system_user_id,radio_data_station_id,title");
	%station = ();
	for (0..$tmp{ROWS}-1) {
		$station{$tmp{DATA}{$_}{system_user_id}}{$tmp{DATA}{$_}{radio_data_station_id}} = 1;
		$station{title}{$tmp{DATA}{$_}{radio_data_station_id}} = $tmp{DATA}{$_}{title} unless $station{title}{$tmp{DATA}{$_}{radio_data_station_id}};
	}

	%did_users = ();
	%my_dids = database_select_as_hash("SELECT did,1 from radio_data_did,radio_data_station_owner " .
									   "WHERE radio_data_did.radio_data_station_id=radio_data_station_owner.radio_data_station_id " .
									   "AND system_user_id='$app{session_cookie_u}'");

	%did	   = database_select("SELECT radio_data_station_id,did,ani,answered_time FROM radio_log_session " .
								 "WHERE answered_time > 0 AND " . ($did eq 'ALL' ? '' : "did='$did' AND ") .
								 " datetime_start > date_sub(now(),interval $interval hour)",
								 "radio_data_station_id,did,ani,answered_time");

	warn "finsih lookup radio_log_session";
	%unique_did = database_select_as_hash("SELECT DISTINCT(did),1 FROM radio_log_session WHERE length(did) > 0");

	%ani_carrier = database_select_as_hash("SELECT ani,carriername FROM ani_lookup", "carriername");
	%did_radio		= database_select_as_hash("select did,radio_data_station.title from radio_data_did,radio_data_station " .
											  "where radio_data_did.radio_data_station_id=radio_data_station.id", "title");

	for (0..$did{ROWS}-1) {
		#$unique_did{$did{DATA}{$_}{did}} = 1 unless $unique_did{$did{DATA}{$_}{did}};
		next if $my_user{1}{group_id} == '24' && !($station{$app{session_cookie_u}} &&
												$station{$app{session_cookie_u}}{$did{DATA}{$_}{radio_data_station_id}});
		if ($carrier && $carrier ne 'ALL') {
			#$h = lookup();
			$ani = $did{DATA}{$_}{ani};
			$ani = "+$ani" unless $k =~ /^\+/;
			next unless $carrier eq $ani_carrier{$ani}{carriername};
		}
		$k = $did{DATA}{$_}{radio_data_station_id} . "-" . $did{DATA}{$_}{did};
		#warn $k . " == " . $did{DATA}{$_}{answered_time};
		$did_users{$k} += $did{DATA}{$_}{answered_time};
	}

	%unique_carrier = database_select_as_hash("SELECT distinct(carriername),1 from ani_lookup");

	undef %did;
    #
    #-------------------------------
    # count top stations
    #-------------------------------
    $top_stations = "";
    $top_csv	  = "";

    $top_stations_count = 0;
	$total				= 0;
    $top_stations_empty = "<tr><td colspan=2><center>... empty ...</center></td></tr>";
	$i					= 1;
    foreach (sort{$did_users{$b} <=> $did_users{$a}} keys %did_users){
		last if $i > $limit;
		$total++;
		($a, $d) = split '-', $_, 2;
		$t		 = int ($did_users{$_} / 60);

		$top_stations .= "<tr><td>$i</td><td>$station{title}{$a}</td><td class=ar>$d</td><td>$t</td></tr>\n";
		$top_csv	 .= "$i,\"$did_radio{$d}{title}\",$d,$t\n";
		$i++;


		#$tmp = $stations{$_}{calls}; $tmp++; $tmp--;
		#$top_stations_count += $tmp;

    }


$didselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_did) {
	next if $my_user{1}{group_id} == '24' && !$my_dids{$_};
	$didselecthtml .= "<option value=\"$_\"" . ($did eq "$_" ? ' SELECTED' : '') . "> $_-$did_radio{$_}{title} </option>";
}

$carrierselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_carrier) {
	$carrierselecthtml .= "<option value=\"$_\"" . ($carrier eq "$_" ? ' SELECTED' : '') . "> $_ </option>";
}

$choise = '<form action="" method="get" name="userminute">' .
		  "Limit: <input type=\"text\" name=\"limit\" value=\"$limit\" />".
		  "<input type=\"hidden\" name=\"action\" value=\"$action\" />".
		  'Did  : <select name="did"  style="width: 125px;" id="range">' .
		  $didselecthtml . '</select>' .
		  'Carrier: <select name="carrier"  style="width: 125px;" id="range">' .
		  $carrierselecthtml . '</select>' .


		  '<input type="submit" value="view" />' .
		  '</form>';



	#
    #-------------------------------
    # count average minutes last hour
    #-------------------------------
    #-------------------------------
	# print page
    #-------------------------------

	%t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= $title;
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[

$choise
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Seq</td>
		<td>Station</td>
		<td>DID</td>
		<td>Total Minute</td>
		</tr>
	</thead>
	<tbody>
		$top_stations
	</tbody>
</table>
<br>
<a 	href="$my_url?action=$action&limit=$limit&subaction=download&did=$did&&carrier=$carrier">&#187 Download (csv format) </a>

	];
	$t{content} .= qq[



	];
	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=$title.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}


}

sub do_carrier_reports {
	$station = clean_int($form{station}) || 888888;
	$date = $form{date};
	$date = '' unless $date =~ /\d\d\d\d\-\d\d\-\d\d/;

	if (!$date) {
		@ar	   = localtime;
		$date  = sprintf("%04d-%02d-%02d", $ar[5]+1900, $ar[4]+1, $ar[3]);

	}

    %my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

	%station = ();
	$stations_filter = '1=1';
	if ($my_user{1}{group_id} == 2) {
		%station =  database_select_as_hash("select radio_data_station_id, title from radio_data_station_owner,radio_data_station " .										"where radio_data_station.id=radio_data_station_owner.radio_data_station_id " .
											" and system_user_id='$app{session_cookie_u}'", "title");
		$stations_filter = " radio_data_station_id IN (" . join(",",map("'$_'", keys %station)) . ")";

	} else {

		%station = database_select_as_hash("select id,title from radio_data_station", "title");
	}

	%hash    = database_select_as_hash("select id,ani,radio_data_station_id,answered_time from radio_log_session " .
									   "where datetime_start > '$date 00:00:00' and " .
									   "datetime_start < '$date 23:59:59' and $stations_filter", "ani,radio_id,answered_time");

	%lookup = database_select_as_hash("select ani,carriername from ani_lookup", "carriername");
	%tmp    = ();

	$lookup{'000000'}{carriername} = 'unkown';
	for (keys %hash) {
		$ani = $hash{$_}{ani};
		$ani =~ s/^\+//;
		$ani =~ s/^1//;
		$ani = "+1$ani";
		$ani = "000000" unless exists $lookup{$ani};
		$tmp{"$ani-$hash{$_}{radio_id}"}{count} += 1;
		$tmp{"$ani-$hash{$_}{radio_id}"}{total} += $hash{$_}{answered_time};
	}

	%carrier = database_select_as_hash("select distinct(carriername),1 from ani_lookup", "flag");
	$carrier{unknown}{flag} = 1;

	for (keys %tmp) {
		next if $tmp{$_}{count} < 1;
		($ani, $radio_id) = split '-';
		$name = $lookup{$ani}{carriername};
		$name ||= "unknown";
		$carrier{"$name--$radio_id"}{count} += $tmp{$_}{count};
		$carrier{"$name--$radio_id"}{total} += $tmp{$_}{total};
	}

	$i = 1;
	$total_minutes = 0;
	$total_count   = 0;

	for (sort {$carrier{$b}{total} <=> $carrier{$a}{total}} keys %carrier) {
		($carrier, $radio_id) = split '--';

		next if $station != '888888' && $radio_id ne $station;

		$total = int $carrier{$_}{total}/60;
		$total_minutes += $total;
		$total_count   += $carrier{$_}{count} ;

		$top_stations .= "<tr><td>$i</td><td>$carrier</td><td>$station{$radio_id}{title}</td><td class=ar>$carrier{$_}{count}</td><td>$total</td></tr>\n";
		$top_csv	  .= "$i,$carrier,$station{$radio_id}{title},$carrier{$_}{count},$total\n";
		$i++;
	}


	$stationselecthtml = '<option value="888888"' . ($station eq "888888" ? ' SELECTED' : '') . "> -ALL Stations- </option>";
	for (sort keys %station) {
		$stationselecthtml .= "<option value=\"$_\"" . ($station eq "$_" ? ' SELECTED' : '') . "> $station{$_}{title} </option>";
	}

	$choise = '<SCRIPT src="WebCalendar.js"/></SCRIPT>'.
		  '<form action="" method="get" name="userminute">' .
		  '<input type="hidden" name="action" value="' . $action . '" />' .
		  "Date: <input type='text' onClick='SelectDate(this, \"yyyy-MM-dd\")' name='date' value='" . $date. "'/>" .
		  'Station: <select name="station">' . $stationselecthtml . '</select>' .
		  '<input type="submit" value="view" />' .
		  '</form>';

	%t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Carrier Daily Reports";
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[

$choise
Total Minutes: <font color="red">$total_minutes</font> &nbsp;&nbsp; Total Count: <font color="red"><font color="red">$total_count</font> <br>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Seq</td>
		<td>Carrier</td>
		<td>Radio Title</td>
		<td>Calls Total<br>Count</td>
		<td>Calls Total<br> Minutes</td>
		</tr>
	</thead>
	<tbody>
		$top_stations
	</tbody>
</table>
<br>
<a 	href="$my_url?action=$action&station=$station&subaction=download&date=$date">&#187 Download (csv format) </a>

	];
	$t{content} .= qq[



	];
	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=$title.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}

}

sub do_carrier_daily_reports {
	$station = clean_int($form{station}) || 888888;
	$carriername = $form{carriername} || 'unkown';

	$date = $form{date};
	$date = '' unless $date =~ /\d\d\d\d\-\d\d\-\d\d/;
	$end_date = $form{end_date};

	if (!$date) {
		@ar	   = localtime;
		$date  = sprintf("%04d-%02d-%02d", $ar[5]+1900, $ar[4]+1, $ar[3]);

	}

	if (!$end_date) {
		@ar	   = localtime;
		$end_date  = sprintf("%04d-%02d-%02d", $ar[5]+1900, $ar[4]+1, $ar[3]);

	}

    %my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

	%station = ();
	$stations_filter = '1=1';
	if ($my_user{1}{group_id} == 2) {
		%station =  database_select_as_hash("select radio_data_station_id, title from radio_data_station_owner,radio_data_station " .										"where radio_data_station.id=radio_data_station_owner.radio_data_station_id " .
											" and system_user_id='$app{session_cookie_u}'", "title");
		$stations_filter = " radio_data_station_id IN (" . join(",",map("'$_'", keys %station)) . ")";

	} else {

		%station = database_select_as_hash("select id,title from radio_data_station", "title");
	}

	%hash    = database_select_as_hash("select id,ani,DATE_FORMAT(datetime_start,'%Y-%m-%d') date,answered_time from radio_log_session " .
									   "where datetime_start > '$date 00:00:00' and " .
									   "datetime_start < '$end_date 23:59:59' and $stations_filter", "ani,date,answered_time");

	%lookup = database_select_as_hash("select ani,carriername from ani_lookup", "carriername");
	%tmp    = ();

	$lookup{'000000'}{carriername} = 'unkown';
	for (keys %hash) {
		$ani = $hash{$_}{ani};
		$ani =~ s/^\+//;
		$ani =~ s/^1//;
		$ani = "+1$ani";
		if ($carriername eq 'unknown') {
			next unless !$lookup{$ani} || !$lookup{$ani}{carriername};
		} else {
			next unless $lookup{$ani}{carriername} eq $carriername;
		}
		$tmp{$hash{$_}{date}}{count} += 1;
		$tmp{$hash{$_}{date}}{total} += $hash{$_}{answered_time};
	}



	$i = 1;
	$total_minutes = 0;
	$total_count   = 0;

	for (sort  keys %tmp) {
		$total = int $tmp{$_}{total}/60;
		$total_minutes += $tmp{$_}{total};
		$total_count   += $tmp{$_}{count} ;

		$top_stations .= "<tr><td>$i</td><td>$_</td><td>$tmp{$_}{count}</td><td>$total</td></tr>\n";
		$top_csv	  .= "$i,$_,$tmp{$_}{count},$total\n";
		$i++;
	}

	%carrier = database_select_as_hash("select distinct(carriername),1 from ani_lookup", "flag");

=pod
	$stationselecthtml = '<option value="unknown"' . ($station eq "unkown" ? ' SELECTED' : '') . "> -unknown- </option>";
	for (sort keys %station) {
		$stationselecthtml .= "<option value=\"$_\"" . ($station eq "$_" ? ' SELECTED' : '') . "> $station{$_}{title} </option>";
	}
=cut

	$stationselecthtml = '<option value="unknown"' . ($carriername eq "unkown" ? ' SELECTED' : '') . "> -unknown- </option>";
	for (sort keys %carrier) {
		$stationselecthtml .= "<option value=\"$_\"" . ($carriername eq "$_" ? ' SELECTED' : '') . "> $_ </option>";
	}

	$choise = '<SCRIPT src="WebCalendar.js"/></SCRIPT>'.
		  '<form action="" method="get" name="userminute">' .
		  '<input type="hidden" name="action" value="' . $action . '" />' .
		  'Carrier: <select name="carriername">' . $stationselecthtml . '</select>' .
		  "From Date: <input type='text' onClick='SelectDate(this, \"yyyy-MM-dd\")' name='date' value='" . $date. "'/>" .
		  "To   Date: <input type='text' onClick='SelectDate(this, \"yyyy-MM-dd\")' name='end_date' value='" . $end_date. "'/>" .
		  '<input type="submit" value="view" />' .
		  '</form>';

	%t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Carrier Daily Reports";
    $t{content} = "";
	$total_minutes = int $total_minutes / 60;
	#
	# add extra info for admin
	$t{content} .= qq[

$choise
Total Minutes: <font color="red">$total_minutes</font> &nbsp;&nbsp; Total Count: <font color="red"><font color="red">$total_count</font> <br>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Seq</td>
		<td>Date</td>
		<td>Calls Total<br>Count</td>
		<td>Calls Total<br> Minutes</td>
		</tr>
	</thead>
	<tbody>
		$top_stations
	</tbody>
</table>
<br>
<a 	href="$my_url?action=$action&date=$date&end_date=$end_date&carriername=$carriername">&#187 Download </a>

	];
	$t{content} .= qq[



	];
	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=$title.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}

}

sub do_noname_users{
=pod
	SELECT * FROM radio_log_session LEFT JOIN ani_lookup ON radio_log_session.ani=ani_lookup.ani OR CONCAT("+", radio_log_session.ani)=ani_lookup.ani where ani_lookup.ani='' limit 10;
	SELECT DISTINCT(radio_log_session.ani),did,answered_time FROM  radio_log_session left join ani_lookup on radio_log_session.ani=ani_lookup.ani OR CONCAT("+", radio_log_session.ani)=ani_lookup.ani where carriername is null limit 10;

	SELECT DISTINCT(radio_log_session.ani),did,answered_time FROM  radio_log_session left join ani_lookup on radio_log_session.ani=ani_lookup.ani OR CONCAT("+", radio_log_session.ani)=ani_lookup.ani where carriername is null and radio_log_session.ani!='';

select count(DISTINCT(radio_log_session.ani)) from radio_log_session;
SELECT count(DISTINCT(radio_log_session.ani),1,carriername) FROM  radio_log_session LEFT JOIN ani_lookup ON radio_log_session.ani=ani_lookup.ani OR CONCAT('+', radio_log_session.ani)=ani_lookup.ani WHERE carriername IS NULL AND radio_log_session.ani!='' LIMIT 10

=cut
	%my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

	warn "SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id";

	%my_dids = database_select_as_hash("SELECT did,1 from radio_data_did,radio_data_station_owner " .
									   "WHERE radio_data_did.radio_data_station_id=radio_data_station_owner.radio_data_station_id " .
									   "AND system_user_id='$app{session_cookie_u}'");
	warn "SELECT did,1 from radio_data_did,radio_data_station_owner " .
									   "WHERE radio_data_did.radio_data_station_id=radio_data_station_owner.radio_data_station_id " .
									   "system_user_id='$app{session_cookie_u}'";


	$did_str = '1';
	if ($did && $did ne 'ALL') {
		$did_str = "did='$did'";
	} else {
		if ($my_user{1}{group_id} == '24') {
			$did_str = " did IN (" . join(",",map("'$_'", keys %my_dids)) . ")";
		}
	}

	warn "didstr: $did_str";
	%noname_ani = database_select_as_hash("SELECT DISTINCT(radio_log_session.ani),1 FROM radio_log_session WHERE $did_str");
	%name		= database_select_as_hash("SELECT DISTINCT(ani),1 FROM ani_lookup");
 	%did_radio		= database_select_as_hash("select did,radio_data_station.title from radio_data_did,radio_data_station " .
											  "where radio_data_did.radio_data_station_id=radio_data_station.id", "title");


	for (keys %name) {
		s/\+//g;
		delete $noname_ani{$_}, $noname_ani{"+$_"};
	}

	$total     = keys %noname_ani;
	$totalpage = int($total / $limit) + ($total % $limit ? 1 : 0);
	#
	$top_stations = '';
	$top_csv	  = '';
	$offset		  = clean_int($form{offset}) || 1;
	$i			  = 0;

	@ani		  = ();
	for (sort keys %noname_ani) {
		$i++;
		next if $i < ($offset-1) * $limit;
		last if $i > ($offset-1) * $limit + $limit;
		push @ani, $_;

    }

	$interval   = 30*24*3600;
	$ani_str    = join ",", map("'$_'", @ani);
	$sql		= "SELECT ani,FLOOR(SUM(answered_time)/60) FROM radio_log_session " .
				  "WHERE ani IN ($ani_str) AND $did_str".
				  " Group BY ani";
	warn $sql;

	%ani_minute = database_select_as_hash($sql);

	$i		   -= $offset * $limit;
	$i			= 1 if $i < 1;
	for (sort {$ani_minute{$b} <=> $ani_minute{$a}} @ani) {
		$top_stations .= "<tr><td>$i</td><td>$_</td><td>$ani_minute{$_}<td> " .
						 "<a href=\"#\" onclick=\"window.open('$myurl?action=do_lookup_ani&ani=$_', 'EDIT','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');return false;\">lookup</td></tr>\n";
		$top_csv	 .= "$i,$a,$ani_minute{$_}\n";
		$i++;
	}

	%unique_did = database_select_as_hash("SELECT DISTINCT(did),1 FROM radio_log_session WHERE length(did) > 0");
	$didselecthtml = '"<option value="ALL">-ALL-</option>"';
	for (sort keys %unique_did) {
		next if $my_user{1}{group_id} == '24' && !$my_dids{$_};
		$didselecthtml .= "<option value=\"$_\"" . ($did eq "$_" ? ' SELECTED' : '') . "> $_ - $did_radio{$_}{title} </option>";
	}

	$choise = '<form action="" method="get" name="userminute">' .
		  'Limit: <select name="limit" style="width: 80px;" />' .
		  '<option value="100" ' . ($limit eq '100' ? 'SELECTED' : '') . '> 100 </option>' .
		  '<option value="200" ' . ($limit eq '200' ? 'SELECTED' : '') . '> 200 </option>' .
		  '<option value="300" ' . ($limit eq '300' ? 'SELECTED' : '') . '> 300 </option>' .
		  '<option value="400" ' . ($limit eq '400' ? 'SELECTED' : '') . '> 400 </option>' .
		  '<option value="500" ' . ($limit eq '500' ? 'SELECTED' : '') . '> 500 </option>' .
		  '<option value="1000" ' . ($limit eq '1000' ? 'SELECTED' : '') . '> 1000 </option>' .
		  "</select>" .
		  'Did  : <select name="did"  style="width: 125px;" id="range">' .
		  $didselecthtml . '</select>' .
		  "<input type=\"hidden\" name=\"action\" value=\"$action\" />".
		  'Page  : <input type="text" name="offset"  style="width: 40px;" id="range" value="' . $offset . '"/> / ' .  $totalpage .
		  '<input type="submit" value="view" />' .
		  '</form>';


    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "No Name Attached Users ($total)";
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[

$choise
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Seq</td>
		<td>Ani</td>
		<td>Total Minutes</td>
		<td>Manual Lookup</a></td>
		</tr>
	</thead>
	<tbody>
		$top_stations
	</tbody>
</table>
<br>
<a 	href="$my_url?action=$action&limit=$limit&subaction=download&did=$did&&carrier=$carrier">&#187 Download (csv format) </a>

	];
	$t{content} .= qq[



	];
	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=$title.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}
}

sub do_lookup_ani {
	$ani = $form{ani};
	$ani=~  s/[^\d+]//g;
	$h   = lookup($ani);
	cgi_hearder_html();
	$nl	 = "<br>\n";
	print "name: $h->{name}$nl" .
		  "carriername: $h->{carriername}$nl" .
		  "<a href=# onclick=\"window.close()\">Close Window</a>";

}

1;
