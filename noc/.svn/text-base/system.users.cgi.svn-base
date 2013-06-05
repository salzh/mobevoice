#!/usr/bin/perl
#require "include.cgi";
require "lookup.cgi";
#=======================================================
# TODO: we dont have users in version2 structure. Clients structure will be changed to allow non ANI clients (web clients). All this code need check.
#=======================================================
# lock this app to system.manager eyes only
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("radio.report") ne 1) {adm_error("no permission"); exit;}
#=======================================================



#use LWP::Simple;
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
#unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
#unless (&active_user_permission_check("radio.report")) {adm_error("no permission"); exit;}
#=======================================================


#$user247 = "test";
#$pass247 = "test";


#=======================================================
# main loop
#=======================================================
$my_url = "system.users.cgi";
$action = $form{action};
$range  = clean_int($form{range}) || 3600 * 20;
$month  = clean_int($form{month}) || 1;
$did	= clean_str($form{did}, '+', '') ;
$did    = $did ? $did : 'ALL';
$carrier= clean_str($form{carrier}, ',', '');
$carrier= $carrier ? $carrier : 'ALL';
$fromdate = $form{fromdate};
$fromdate = '' unless $fromdate =~ /\d\d\d\d\-\d\d\-\d\d/;
$enddate  = $form{enddate};
$enddate  = '' unless $enddate =~ /\d\d\d\d\-\d\d\-\d\d/;

$MAX247 = 100; #limit the count of lookup data2407

if 		($action eq "radio_report_now")		{ &do_radio_report_now();	}
elsif 	($action eq "radio_report_now_image"){ &do_radio_report_now_image();	}
elsif	($action eq "radio_report_top")		{ &do_radio_report_top();	}
elsif   ($action eq 'radio_edit_username')	{ &do_radio_edit_username();		}
else										{ 	&do_radio_report_now();}
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

	%did_users  = ();
	$datefilter = '';
	if ($fromdate) {
		$datefilter .= "unix_timestamp(datetime_start) > unix_timestamp('$fromdate 00:00:00') AND ";
	} else {
		$datefilter .= "1 AND ";
	}

	if ($enddate) {
		$datefilter .= "unix_timestamp(datetime_start) < unix_timestamp('$enddate 23:59:59')";
	} else {
		$datefilter .="1";
	}

	$sql        = "SELECT did,ani,answered_time FROM radio_log_session " .
				 "WHERE answered_time > 0 AND " . ($did eq 'ALL' ? '' : "did='$did' AND ") .
				 "UNIX_TIMESTAMP() - UNIX_TIMESTAMP(datetime_start) < " . $month*30*24*3600 .
				 " AND $datefilter";
	warn $sql;
	
	%did	    = database_select($sql,  "did,ani,answered_time");
	#%unique_did = database_select_as_hash("SELECT DISTINCT(did),1 FROM radio_log_session WHERE length(did) > 0");
	%unique_did = database_select_as_hash("SELECT DISTINCT(did),1 FROM radio_log_session WHERE length(did) > 0");
	%ani_carrier = database_select_as_hash("SELECT ani,carriername FROM ani_lookup", "carriername");
	%did_radio		= database_select_as_hash("select did,radio_data_station.title from radio_data_did,radio_data_station " .
											  "where radio_data_did.radio_data_station_id=radio_data_station.id", "title");

	for (0..$did{ROWS}-1) {
		#$unique_did{$did{DATA}{$_}{did}} = 1 unless $unique_did{$did{DATA}{$_}{did}};
		next if $my_user{1}{group_id} == '2' && !$my_dids{$did{DATA}{$_}{did}};
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
	$indbcount			= 0;
    foreach (sort{$did_users{$b} <=> $did_users{$a}} keys %did_users){
		next unless $did_users{$_} >= $range;
		$total++;
		($a, $d) = split '-', $_, 2;
		$t		 = int ($did_users{$_} / 60);
		if ($indbcount < $MAX247) {
			$h		 = lookup($a);
		} else {
			$h = {name => '-', carriername => '-'};
		}

		$indbcount++ if !$h->{isindb};
		$top_stations .= "<tr><td>$a</td><td class=ar><a href='#' " .
						 "onclick=\"window.open('system.users.cgi?action=radio_edit_username&ani=$a&name=$h->{name}', 'EDIT','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');return false;\">$h->{name}</td><td>$d</td><td>$did_radio{$d}{title}</td>" .
						 "<td>$h->{carriername}</td><td>$t</td></tr>\n";
		$top_csv	 .= "$a,\"$h->{name}\",$d,\"$did_radio{$d}{title}\",\"$h->{carriername}\",$t\n";
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
=cut
$didselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_did) {
	next if $my_user{1}{group_id} == '2' && !$my_dids{$_};
	$didselecthtml .= "<option value=\"$_\"" . ($did eq "$_" ? ' SELECTED' : '') . "> $_ - $did_radio{$_}{title}</option>";
}


%unique_carrier = database_select_as_hash("SELECT distinct(carriername),1 from ani_lookup");
$carrierselecthtml = '"<option value="ALL">-ALL-</option>"';
for (sort keys %unique_carrier) {
	$carrierselecthtml .= "<option value=\"$_\"" . ($carrier eq "$_" ? ' SELECTED' : '') . "> $_ </option>";
}

$choise = '<SCRIPT src="WebCalendar.js"/></SCRIPT>'.
		  '<form action="" method="get" name="userminute">' .
		  "From Date: <input type='text' onClick='SelectDate(this, \"yyyy-MM-dd\")' name='fromdate' value='" . $fromdate. "'/>".
		  "End  Date: <input type='text' onClick='SelectDate(this,\"yyyy-MM-dd\")' name='enddate' value='" . $enddate . "'/><br>".

		  #'From Date: <input type="text" name="fromdate" style="width: 100px;" value="'. $fromdate . '"/>&nbsp;&nbsp;'.
		  #'End  Date: <input type="text" name="enddate" style="width: 100px;" value="'. $enddate . '"/><br>'.
		  'Months: <select name="month"  style="width: 100px;" id="month">' .
		  '<option value="1"' . ($month eq '1' ? ' SELECTED' : '') . '> 1 </option>' .
 		  '<option value="2"' . ($month eq '2' ? ' SELECTED' : '') . '> 2 </option>' .
 		  '<option value="3"' . ($month eq '3' ? ' SELECTED' : '') . '> 3 </option>' .
 		  '<option value="4"' . ($month eq '4' ? ' SELECTED' : '') . '> 4 </option>' .
 		  '<option value="5"' . ($month eq '5' ? ' SELECTED' : '') . '> 5 </option>' .
 		  '<option value="6"' . ($month eq '6' ? ' SELECTED' : '') . '> 6 </option>' .
		  '<option value="999"' . ($month eq '999' ? ' SELECTED' : '') . '> No Limit </option>' .

		  '</select>' .
		  'Hours: <select name="range"  style="width: 100px;" id="range">' .
		  '<option value="3600"' . ($range eq '3600' ? ' SELECTED' : '') . '> 1 </option>' .
		  '<option value="18000"' . ($range eq '18000' ? ' SELECTED' : '') . '> 5 </option>' .
		  '<option value="36000"' . ($range eq '36000' ? ' SELECTED' : '') . '> 10 </option>' .
		  '<option value="72000"' . ($range eq '72000' ? ' SELECTED' : '') . '> 20 </option>' .
		  '<option value="1"' . ($range eq '1' ? ' SELECTED' : '') . '> No Limit </option>' .
		  '</select>' .
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
    $t{title}	= "User Report ($total)";
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[

$choise
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
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
<a 	href="$myurl?action=$action&limit=$limit&subaction=download&range=$range&month=$month&did=$did&carrier=$carrier&fromdate=$fromdate&enddate=$enddate">&#187 Download (csv format) </a>

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
	if ($form{subaction} eq 'download') {
		print "Content-type: text/csv\n";
		print "Content-Disposition: attachment;filename=users_minutes.csv\n";
		print "\n";

		print $top_csv;
	} else {
		&template_print("template.html",%t);
	}
}


sub do_radio_edit_username () {
	$ani  = $form{'ani'};
	$ani =~ s/[^\d+]//g;
	$name = clean_str($form{'name'}, ",", "");
	cgi_hearder_html();

	if (!$form{subaction}) {
print <<DISPLAY;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>$ani new name</title>
</head>

<body>
<center>
<form name="form" method="post" action="system.users.cgi">
Edit name for <font color="red">$ani</font>:<br>
<input type="hidden" name="ani" value="$ani"/>
<input type="hidden" name="action" value="radio_edit_username" />
<input name="newname" type="text"  value="$name"/>

<input type="submit" name="subaction" value="submit" />
</form>
</center>
</body>
</html>
DISPLAY

	} else {
		$newname = clean_str($form{'newname'}, ",", "");
		$ani     = "+$ani" unless $ani =~ /^\+/;

    %my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} " .
									   "where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");
	if ($my_user{1}{group_id} == 2) {
		$tmpani =~ s/\+//g;
		%row = database_select("select * from radio_data_station_owner where radio_data_station_id in " .
						   "(select distinct(radio_data_station_id) from radio_log_session where " .
						   "radio_data_station_id > 0 and (ani='$tmpani' or ani='+$tmpani'));");
		if ($row{ROWS} < 1) {
			print <<ERROR;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>EDIT</title>
</head>

<body>
	<center> Error: Permission Denied ...</center>
</body>
</html>
ERROR

exit 0;
		}
	}

	database_do("UPDATE ani_lookup SET " .
				"lasteditname='$newname',lastedittime=CURRENT_TIMESTAMP,lastedituserid='$app{session_cookie_u}' " .
				"WHERE ani='$ani'");

		print <<HTML;
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>EDIT</title>
<script>
window.onload = function() {window.close()}
</script>

</head>

<body>
	<center> Update Successfully ...</center>
</body>
</html>
HTML

	}
}

sub do_radio_report_top(){
    #
	#==========================================
    # prepare year/month select and values
	#==========================================
	%yearmonth_list = &database_select_as_hash("SELECT distinct DATE_FORMAT(datetime_start,'\%Y\%m'),1 FROM radio_log_session  ");
	%hash = database_select_as_hash("SELECT 1,1,max(DATE_FORMAT(datetime_start,'\%Y\%m')) FROM radio_log_session ","flag,value");
	$filter_yearmonth = clean_int($form{filter_yearmonth});
	$filter_yearmonth = (length($filter_yearmonth) ne 6) ? "" : $filter_yearmonth;
	$filter_yearmonth = ( ($filter_yearmonth eq "") && ($hash{1}{flag} eq 1) ) ? $hash{1}{value} : $filter_yearmonth;
	$filter_yearmonth = (exists($yearmonth_list{$filter_yearmonth})) ? $filter_yearmonth : "";
	$filter_yearmonth_year	= substr($filter_yearmonth,0,4);
	$filter_yearmonth_month	= substr($filter_yearmonth,4,2);
    $filter_yearmonth_month_day_01 = $filter_yearmonth_year."-".$filter_yearmonth_month."-01";
	$filter_yearmonth_select = "";
	foreach $id (sort{$b <=> $a} keys %yearmonth_list) {
		$tmp = ($id eq $filter_yearmonth) ? " selected " : "";
		$filter_yearmonth_select .= "<option $tmp value='$id'>".substr($id,0,4)."/".substr($id,4,2)."</option>";
	}
    #
	#==========================================
    # get top radios for this monyth
	#==========================================
	$sql = "
		SELECT radio_data_station_id
		FROM radio_log_session
		where datetime_start >= '$filter_yearmonth_month_day_01' and datetime_start < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)
		group by radio_data_station_id
		order by sum(answered_time) desc
		LIMIT 0,4
	";
	@top_radios = &database_select_as_array($sql);
	$top_radios_string = join(",",@top_radios);
	#
	#
	#==========================================
	# Query data
	#==========================================
	%data = ();
	foreach $station_id (@top_radios) {
		$sql = "
			select
				DATE_FORMAT(datetime_start,'\%d'),
				sum(answered_time)
			from
				radio_log_session
			where
				datetime_start >= '$filter_yearmonth_month_day_01' and datetime_start < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)
				and radio_data_station_id = '$station_id'
			group by
				DATE_FORMAT(datetime_start,'\%d')
		";
		%hash = &database_select_as_hash($sql);
		foreach $day (keys %hash) { $data{station}{$station_id}{data}{$day}{minutes} = int($hash{$day}/60); }
		%hash = &database_select_as_hash("select 1,1,title from radio_data_station where id='$station_id' ","flag,title");
		$data{station}{$station_id}{title} = ( ($hash{1}{flag} eq 1) && ($hash{1}{title} ne "") ) ? $hash{1}{title} : "Unknown $station_id";
	}
	$sql = "
		select
			DATE_FORMAT(datetime_start,'\%d'),
			sum(answered_time)
		from
			radio_log_session
		where
			datetime_start >= '$filter_yearmonth_month_day_01' and datetime_start < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)
			and radio_data_station_id not in ($top_radios_string)
		group by
			DATE_FORMAT(datetime_start,'\%d')
	";
	%hash = &database_select_as_hash($sql);
	foreach $day (keys %hash) { $data{others}{data}{$day}{minutes} = int($hash{$day}/60); }
	#
	#
	#==========================================
	# plot top radios minutes day by day
	#==========================================
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	%plot = ();
	$plot{uid} = "minutes_day_by_day";
	$plot{x} = 500;
	$plot{y} = 230;
	$station_index = 1;
	$plot{series}{$station_index}{name} 	= "Other radios";
	$plot{series}{$station_index}{color} = "808080";
	$slice_index = 0;
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{$station_index} = $data{others}{data}{$dd}{minutes};
		$plot{data}{$slice_index}{$station_index}++;
		$plot{data}{$slice_index}{$station_index}--;
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	$station_index++;
	foreach $station_id (reverse @top_radios) {
		$plot{series}{$station_index}{name} 	= "$data{station}{$station_id}{title}";
		$plot{series}{$station_index}{color} = "ff0000";
		$plot{series}{$station_index}{color} = ($station_index eq 3) ? "92c23e" : $plot{series}{$station_index}{color};
		$plot{series}{$station_index}{color} = ($station_index eq 4) ? "f8d322" : $plot{series}{$station_index}{color};
		$plot{series}{$station_index}{color} = ($station_index eq 5) ? "ff6600" : $plot{series}{$station_index}{color};
		$slice_index = 0;
		foreach $d (@days) {
			$dd = substr("00".$d,-2,2);
			$plot{data}{$slice_index}{$station_index} = $data{station}{$station_id}{data}{$dd}{minutes};
			$plot{data}{$slice_index}{$station_index}++;
			$plot{data}{$slice_index}{$station_index}--;
			$plot{slices}{$slice_index} = $dd;
			$slice_index++;
		}
		$station_index++
	}
	%plot = &plot_StackedColumn2D(%plot);
	$top_radios_minutes = $plot{html};
	#
	#
	#==========================================
	# plot radio by radio
	#==========================================
	%plots = ();
	$plots_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $station_id (reverse @top_radios) {
		%plot = ();
		$plot{uid} = "TOP_RADIO_".$plots_index;
		$plot{x} = 350;
		$plot{y} = 200;
		$plot{series}{1}{name} 	= "$data{station}{$station_id}{title}";
		$plot{series}{1}{color} = "ff0000";
		$plot{series}{1}{color} = ($plots_index eq 2) ? "92c23e" : $plot{series}{1}{color};
		$plot{series}{1}{color} = ($plots_index eq 3) ? "f8d322" : $plot{series}{1}{color};
		$plot{series}{1}{color} = ($plots_index eq 4) ? "ff6600" : $plot{series}{1}{color};
		$slice_index = 0;
		foreach $d (@days) {
			$dd = substr("00".$d,-2,2);
			$plot{data}{$slice_index}{1} = $data{station}{$station_id}{data}{$dd}{minutes};
			$plot{data}{$slice_index}{1}++;
			$plot{data}{$slice_index}{1}--;
			$plot{slices}{$slice_index} = $dd;
			$slice_index++;
		}
		%plot = &plot_MSColumn2D(%plot);
		$plots{$plots_index} = $plot{html};
		$plots_index++;
	}
	%plot = ();
	$plot{uid} = "TOP_RADIO_".$plots_index;
	$plot{x} = 350;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Other radios";
	$plot{series}{1}{color} = "808080";
	$slice_index = 0;
	$tmp = 0;
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = $data{others}{data}{$dd}{minutes};
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $dd;
		$tmp += $plot{data}{$slice_index}{1};
		$slice_index++;
	}
	if ($tmp > 0) {
		%plot = &plot_MSColumn2D(%plot);
		$plots{$plots_index} = $plot{html};
	}
	#
	#
	#==========================================
	# print page
	#==========================================
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Top phone radios";
	$t{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<form action=$my_url>
	Year/month: 	<select name=filter_yearmonth>	<option value=''>Select month</option>		<option value=''> </option>$filter_yearmonth_select</select> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	<input type=submit value='Update'>
	<input type=hidden name=action value=radio_report_top>
	</form>
	<br>

	<fieldset style="width:730px;"><legend>Total minutes group by top radios</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td valign=top>$top_radios_minutes</td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
		<td valign=top>$minutes_month_by_month</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Top radios</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td valign=top>$plots{1}</td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
		<td valign=top>$plots{2}</td>
	</table>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td valign=top>$plots{3}</td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
		<td valign=top>$plots{4}</td>
	</table>
	</fieldset>
	<br>


	];
	&template_print("template.html",%t);
}
#=======================================================



#=======================================================
# PLOT
#=======================================================
sub plot_lines(){
	local(%plot) = @_;
	local($slice,$serie);
	$plot{xml} = "";
	$plot{xml} .= "<graph ";
	$plot{xml} .= "formatNumberScale='1' ";
	$plot{xml} .= "decimalPrecision='0' ";
	$plot{xml} .= "numdivlines='4' ";
	$plot{xml} .= "numVdivlines='0' ";
	$plot{xml} .= "yaxisminvalue='0' ";
	$plot{xml} .= "showValues='0' ";
	$plot{xml} .= "formatNumberScale='0' anchorAlpha='0' ";
	$plot{xml} .= "bgColor='FFFFFF' ";
	$plot{xml} .= "shadowAlpha='30' ";
	$plot{xml} .= "chartLeftMargin='0' ";
	$plot{xml} .= "chartRightMargin='5' ";
	$plot{xml} .= "chartTopMargin='10' ";
	$plot{xml} .= "chartBottomMargin='0' ";
	$plot{xml} .= "rotateNames='1' animation='0'  >";
	$plot{xml} .= "<categories>";
	foreach (sort{$a <=> $b} keys %{$plot{data}}) { $plot{xml} .= "<category name='$plot{slices}{$_}'/>"; }
	$plot{xml} .= "</categories>";
	foreach $serie (sort{$a <=> $b} keys %{$plot{series}}) {
		$plot{xml} .= "<dataset seriesName='$plot{series}{$serie}{name}' color='$plot{series}{$serie}{color}' anchorBorderColor='$plot{series}{$serie}{color}' anchorBgColor='$plot{series}{$serie}{color}'>";
		foreach $slice (sort{$a <=> $b} keys %{$plot{data}}) {
			$plot{xml} .= "<set value='$plot{data}{$slice}{$serie}'/>";
		}
		$plot{xml} .= "</dataset>";
	}
	$plot{xml} .= "</graph>";
	$plot{html} = qq[
	<div id="$plot{uid}" class=clear style="padding-left:0px;">loading...</div>
	<script type="text/javascript">
	var myChartbar = new FusionCharts("design/FusionChartsFree/Charts/FCF_MSLine.swf", "myChartId", "$plot{x}", "$plot{y}");
	myChartbar.setDataXML("$plot{xml}");
	myChartbar.render("$plot{uid}");
	</script>
	];
	return %plot;
}
sub plot_area(){
	local(%plot) = @_;
	local($slice,$serie);
	$plot{xml} = "";
	$plot{xml} .= "<graph ";
	$plot{xml} .= "formatNumberScale='1' ";
	$plot{xml} .= "decimalPrecision='0' ";
	$plot{xml} .= "numdivlines='4' ";
	$plot{xml} .= "numVdivlines='0' ";
	$plot{xml} .= "yaxisminvalue='0' ";
	$plot{xml} .= "showValues='0' ";
	$plot{xml} .= "formatNumberScale='0' anchorAlpha='0' ";
	$plot{xml} .= "bgColor='FFFFFF' ";
	$plot{xml} .= "shadowAlpha='30' ";
	$plot{xml} .= "chartLeftMargin='0' ";
	$plot{xml} .= "chartRightMargin='5' ";
	$plot{xml} .= "chartTopMargin='10' ";
	$plot{xml} .= "chartBottomMargin='0' ";
	$plot{xml} .= "rotateNames='1' animation='0' showAreaBorder='0' >";
	$plot{xml} .= "<categories>";
#
#<graph  caption='Site hits per hour'
#                numdivlines='4'
#                showgridbg='1'
#                lineThickness='1'
#                showNames='1'
#                yaxisminvalue='0'
#                formatNumberScale='1'
#                showLimits='1'
#                showAlternateHGridColor='1'
#                showAreaBorder='1'
#
	foreach (sort{$a <=> $b} keys %{$plot{data}}) { $plot{xml} .= "<category name='$plot{slices}{$_}'/>"; }
	$plot{xml} .= "</categories>";
	foreach $serie (sort{$a <=> $b} keys %{$plot{series}}) {
		$plot{xml} .= "<dataset seriesName='$plot{series}{$serie}{name}' color='$plot{series}{$serie}{color}' anchorBorderColor='$plot{series}{$serie}{color}' anchorBgColor='$plot{series}{$serie}{color}'>";
		foreach $slice (sort{$a <=> $b} keys %{$plot{data}}) {
			$plot{xml} .= "<set value='$plot{data}{$slice}{$serie}'/>";
		}
		$plot{xml} .= "</dataset>";
	}
	$plot{xml} .= "</graph>";
	$plot{html} = qq[
	<div id="$plot{uid}" class=clear style="padding-left:0px;">loading...</div>
	<script type="text/javascript">
	var myChartbar = new FusionCharts("design/FusionChartsFree/Charts/FCF_StackedArea2D.swf", "myChartId", "$plot{x}", "$plot{y}");
	myChartbar.setDataXML("$plot{xml}");
	myChartbar.render("$plot{uid}");
	</script>
	];
	return %plot;
}
sub plot_StackedColumn3D(){
	local(%plot) = @_;
	local($slice,$serie);
	$plot{xml} = "";
	$plot{xml} .= "<graph ";
	$plot{xml} .= "formatNumberScale='1' ";
	$plot{xml} .= "decimalPrecision='0' ";
	$plot{xml} .= "numdivlines='4' ";
	$plot{xml} .= "numVdivlines='0' ";
	$plot{xml} .= "yaxisminvalue='0' ";
	$plot{xml} .= "showValues='0' ";
	$plot{xml} .= "formatNumberScale='0' anchorAlpha='0' ";
	$plot{xml} .= "bgColor='FFFFFF' ";
	$plot{xml} .= "shadowAlpha='30' ";
	$plot{xml} .= "chartLeftMargin='0' ";
	$plot{xml} .= "chartRightMargin='5' ";
	$plot{xml} .= "chartTopMargin='10' ";
	$plot{xml} .= "chartBottomMargin='0' ";
	$plot{xml} .= "rotateNames='1' animation='0'  >";
	$plot{xml} .= "<categories>";
	foreach (sort{$a <=> $b} keys %{$plot{data}}) { $plot{xml} .= "<category name='$plot{slices}{$_}'/>"; }
	$plot{xml} .= "</categories>";
	foreach $serie (sort{$a <=> $b} keys %{$plot{series}}) {
		$plot{xml} .= "<dataset seriesName='$plot{series}{$serie}{name}' color='$plot{series}{$serie}{color}' anchorBorderColor='$plot{series}{$serie}{color}' anchorBgColor='$plot{series}{$serie}{color}'>";
		foreach $slice (sort{$a <=> $b} keys %{$plot{data}}) {
			$plot{xml} .= "<set value='$plot{data}{$slice}{$serie}'/>";
		}
		$plot{xml} .= "</dataset>";
	}
	$plot{xml} .= "</graph>";
	$plot{html} = qq[
	<div id="$plot{uid}" class=clear style="padding-left:0px;">loading...</div>
	<script type="text/javascript">
	var myChartbar = new FusionCharts("design/FusionChartsFree/Charts/FCF_StackedColumn3D.swf", "myChartId", "$plot{x}", "$plot{y}");
	myChartbar.setDataXML("$plot{xml}");
	myChartbar.render("$plot{uid}");
	</script>
	];
	return %plot;
}
sub plot_StackedColumn2D(){
	local(%plot) = @_;
	local($slice,$serie);
	$plot{xml} = "";
	$plot{xml} .= "<graph ";
	$plot{xml} .= "formatNumberScale='1' ";
	$plot{xml} .= "decimalPrecision='0' ";
	$plot{xml} .= "numdivlines='4' ";
	$plot{xml} .= "numVdivlines='0' ";
	$plot{xml} .= "yaxisminvalue='0' ";
	$plot{xml} .= "showValues='0' ";
	$plot{xml} .= "formatNumberScale='0' anchorAlpha='0' ";
	$plot{xml} .= "bgColor='FFFFFF' ";
	$plot{xml} .= "shadowAlpha='30' ";
	$plot{xml} .= "chartLeftMargin='0' ";
	$plot{xml} .= "chartRightMargin='5' ";
	$plot{xml} .= "chartTopMargin='10' ";
	$plot{xml} .= "chartBottomMargin='0' ";
	$plot{xml} .= "rotateNames='1' animation='0'  >";
	$plot{xml} .= "<categories>";
	foreach (sort{$a <=> $b} keys %{$plot{data}}) { $plot{xml} .= "<category name='$plot{slices}{$_}'/>"; }
	$plot{xml} .= "</categories>";
	foreach $serie (sort{$a <=> $b} keys %{$plot{series}}) {
		$plot{xml} .= "<dataset seriesName='$plot{series}{$serie}{name}' color='$plot{series}{$serie}{color}' anchorBorderColor='$plot{series}{$serie}{color}' anchorBgColor='$plot{series}{$serie}{color}'>";
		foreach $slice (sort{$a <=> $b} keys %{$plot{data}}) {
			$plot{xml} .= "<set value='$plot{data}{$slice}{$serie}'/>";
		}
		$plot{xml} .= "</dataset>";
	}
	$plot{xml} .= "</graph>";
	$plot{html} = qq[
	<div id="$plot{uid}" class=clear style="padding-left:0px;">loading...</div>
	<script type="text/javascript">
	var myChartbar = new FusionCharts("design/FusionChartsFree/Charts/FCF_StackedColumn2D.swf", "myChartId", "$plot{x}", "$plot{y}");
	myChartbar.setDataXML("$plot{xml}");
	myChartbar.render("$plot{uid}");
	</script>
	];
	return %plot;
}
sub plot_MSColumn2D(){
	local(%plot) = @_;
	local($slice,$serie);
	$plot{xml} = "";
	$plot{xml} .= "<graph ";
	$plot{xml} .= "formatNumberScale='1' ";
	$plot{xml} .= "decimalPrecision='0' ";
	$plot{xml} .= "numdivlines='4' ";
	$plot{xml} .= "numVdivlines='0' ";
	$plot{xml} .= "yaxisminvalue='0' ";
	$plot{xml} .= "showValues='0' ";
	$plot{xml} .= "formatNumberScale='0' anchorAlpha='0' ";
	$plot{xml} .= "bgColor='FFFFFF' ";
	$plot{xml} .= "shadowAlpha='30' ";
	$plot{xml} .= "chartLeftMargin='0' ";
	$plot{xml} .= "chartRightMargin='5' ";
	$plot{xml} .= "chartTopMargin='10' ";
	$plot{xml} .= "chartBottomMargin='0' ";
	$plot{xml} .= "rotateNames='1' animation='0'  >";
	$plot{xml} .= "<categories>";
	foreach (sort{$a <=> $b} keys %{$plot{data}}) { $plot{xml} .= "<category name='$plot{slices}{$_}'/>"; }
	$plot{xml} .= "</categories>";
	foreach $serie (sort{$a <=> $b} keys %{$plot{series}}) {
		$plot{xml} .= "<dataset seriesName='$plot{series}{$serie}{name}' color='$plot{series}{$serie}{color}' anchorBorderColor='$plot{series}{$serie}{color}' anchorBgColor='$plot{series}{$serie}{color}'>";
		foreach $slice (sort{$a <=> $b} keys %{$plot{data}}) {
			$plot{xml} .= "<set value='$plot{data}{$slice}{$serie}'/>";
		}
		$plot{xml} .= "</dataset>";
	}
	$plot{xml} .= "</graph>";
	$plot{html} = qq[
	<div id="$plot{uid}" class=clear style="padding-left:0px;">loading...</div>
	<script type="text/javascript">
	var myChartbar = new FusionCharts("design/FusionChartsFree/Charts/FCF_MSColumn2D.swf", "myChartId", "$plot{x}", "$plot{y}");
	myChartbar.setDataXML("$plot{xml}");
	myChartbar.render("$plot{uid}");
	</script>
	];
	return %plot;
}
sub plot_MSArea2D(){
	local(%plot) = @_;
	local($slice,$serie);
	$plot{xml} = "";
	$plot{xml} .= "<graph ";
	$plot{xml} .= "formatNumberScale='1' ";
	$plot{xml} .= "decimalPrecision='0' ";
	$plot{xml} .= "numdivlines='4' ";
	$plot{xml} .= "numVdivlines='0' ";
	$plot{xml} .= "yaxisminvalue='0' ";
	$plot{xml} .= "showValues='0' ";
	$plot{xml} .= "formatNumberScale='0' anchorAlpha='0' ";
	$plot{xml} .= "bgColor='FFFFFF' ";
	$plot{xml} .= "shadowAlpha='30' ";
	$plot{xml} .= "chartLeftMargin='0' ";
	$plot{xml} .= "chartRightMargin='5' ";
	$plot{xml} .= "chartTopMargin='10' ";
	$plot{xml} .= "chartBottomMargin='0' ";
	$plot{xml} .= "rotateNames='1' animation='0' showAreaBorder='0' >";
	$plot{xml} .= "<categories>";
#
#<graph  caption='Site hits per hour'
#                numdivlines='4'
#                showgridbg='1'
#                lineThickness='1'
#                showNames='1'
#                yaxisminvalue='0'
#                formatNumberScale='1'
#                showLimits='1'
#                showAlternateHGridColor='1'
#                showAreaBorder='1'
#
	foreach (sort{$a <=> $b} keys %{$plot{data}}) { $plot{xml} .= "<category name='$plot{slices}{$_}'/>"; }
	$plot{xml} .= "</categories>";
	foreach $serie (sort{$a <=> $b} keys %{$plot{series}}) {
		$plot{xml} .= "<dataset seriesName='$plot{series}{$serie}{name}' color='$plot{series}{$serie}{color}' anchorBorderColor='$plot{series}{$serie}{color}' anchorBgColor='$plot{series}{$serie}{color}' areaBorderColor='$plot{series}{$serie}{color}'  areaBorderThickness='$plot{series}{$serie}{color}' areaAlpha='60' >";
		foreach $slice (sort{$a <=> $b} keys %{$plot{data}}) {
			$plot{xml} .= "<set value='$plot{data}{$slice}{$serie}'/>";
		}
		$plot{xml} .= "</dataset>";
	}
	$plot{xml} .= "</graph>";
	$plot{html} = qq[
	<div id="$plot{uid}" class=clear style="padding-left:0px;">loading...</div>
	<script type="text/javascript">
	var myChartbar = new FusionCharts("design/FusionChartsFree/Charts/FCF_MSArea2D.swf", "myChartId", "$plot{x}", "$plot{y}");
	myChartbar.setDataXML("$plot{xml}");
	myChartbar.render("$plot{uid}");
	</script>
	];
	return %plot;
}
sub do_test_ney(){
	#
	#---------------------------------------
	# start
	#---------------------------------------
	%t = &menu_permissions_get_as_template();
	$html = "";
	$tmp = qq[
		root@net-sul-643:/home# ./rain2.pl
		INTERNAL _____________________ :
		10.1.4.10 __________ : 1462 Kb
		10.1.1.134 _________ : 1028 Kb
		10.1.1.120 _________ : 702 Kb
		10.1.1.133 _________ : 559 Kb
		10.1.1.103 _________ : 404 Kb
		10.1.1.121 _________ : 391 Kb
		10.1.3.200 _________ : 96 Kb
		10.1.3.255 _________ : 58 Kb
		10.1.2.255 _________ : 47 Kb
		10.2.1.255 _________ : 47 Kb
		10.1.1.255 _________ : 47 Kb
		10.2.2.255 _________ : 47 Kb
		10.1.4.255 _________ : 47 Kb
		10.1.3.201 _________ : 9 Kb
		10.1.2.101 _________ : 4 Kb
		10.1.1.135 _________ : 0 Kb
		10.1.1.101 _________ : 0 Kb
		UNKNOWN ______________________ :
		DST=200.155.17.100 _ : 382 Kb
		SRC=201.49.213.186 _ : 382 Kb
		DST=200.155.17.103 _ : 70 Kb
		DST=200.155.31.143 _ : 23 Kb
		SRC=200.155.31.136 _ : 23 Kb
		SRC=200.155.17.100 _ : 23 Kb
		SRC=200.155.17.101 _ : 23 Kb
		SRC=200.155.17.102 _ : 23 Kb
		DST=200.155.31.133 _ : 1 Kb
		DST=200.155.31.135 _ : 1 Kb
		DST=200.155.31.134 _ : 1 Kb
		DST=200.155.31.136 _ : 1 Kb
		DST=200.155.17.101 _ : 1 Kb
		SRC=80.24.77.44 ____ : 0 Kb
		DST=200.155.17.102 _ : 0 Kb
		SRC=84.110.164.38 __ : 0 Kb
		DST=200.155.31.132 _ : 0 Kb
		SRC=201.41.240.222 _ : 0 Kb
		SRC=200.155.133.1 __ : 0 Kb
		SRC=200.155.37.65 __ : 0 Kb
		SRC=200.155.117.42 _ : 0 Kb
	];
	#
	#---------------------------------------
	# read file
	#---------------------------------------
	open(IN,"/home/neyfrota/Projetos/vtex/firewall.alog/log/messages");
	while(<IN>){
		chomp;
		$l = $_;
		@v = split(/ /,$l);
		## Jun 20 04:04:59 fwvtex kernel: RULE 25 -- ACCEPT IN=ppp0 OUT=eth1 SRC=10.1.4.10 DST=201.6.0.112 LEN=64 TOS=0x00 PREC=0x00 TTL=127 ID=61552 PROTO=UDP SPT=1044 DPT=5 LEN=44
		## [Jun] - [20] - [04:04:59] - [fwvtex] - [kernel:] - [RULE] - [25] - [--] - [ACCEPT] - [IN=eth0] - [OUT=eth1] - [SRC=10.1.1.133] - [DST=200.49.216.58] - [LEN=62] - [TOS=0x00] - [PREC=0x00] - [TTL=127] - [ID=30029] - [PROTO=UDP] - [SPT=53942] - [DPT=53] - [LEN=42] -
		if ((@v)[5] ne "RULE") {next}
		if ((@v)[8] ne "ACCEPT") {next}
		%vv  = ();
		foreach $val (@v) {
			if (index($val,"=") eq -1) {next}
			($v1,$v2) = split(/=/,$val);
			$vv{$v1} = $v2;
		}
		$bytes 		= $vv{LEN} || 0;
		$vv{IN}		= $vv{IN} || "UNKNOWN";
		$vv{OUT}	= $vv{OUT} || "UNKNOWN";
		$bytes++; $bytes--;
		$tmp = $vv{IN};
		$tmp = ($tmp eq "ppp0") ? "VPN" : $tmp;
		$tmp = ($tmp eq "eth0") ? "Intranet" : $tmp;
		$tmp = ($tmp eq "eth1") ? "Internet" : $tmp;
		$in = $tmp;
		$tmp = $vv{OUT};
		$tmp = ($tmp eq "ppp0") ? "VPN" : $tmp;
		$tmp = ($tmp eq "eth0") ? "Intra" : $tmp;
		$tmp = ($tmp eq "eth1") ? "Inter" : $tmp;
		$out = $tmp;

		#$direction = "$vv{IN}->$vv{OUT}";
		#$data{$vv{SRC}}{"$direction"} += $bytes;
		#$data{$vv{DST}}{"$direction"} += $bytes;


		#$data{"Total directions"}{$direction} += $bytes;
		#$data{"Source"}{$vv{SRC}} += $bytes;
		#$data{"Destination"}{$vv{DST}} += $bytes;

		$host = ($out eq "Inter") ? "SRC=".$vv{SRC} : "DST=".$vv{DST};
		$data{"$in to $out"}{$host} += $bytes;


	#	$c++;if ($c>10000) {last}
	}
	close(IN);


	#
	#
	#---------------------------------------
	# print
	#---------------------------------------
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Services/recharges overview";
	$t{dic}{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>


	<fieldset style="width:730px;"><legend>Total send</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_total_send_day</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_total_send_month</td>
	</table>
	</fieldset>
	<br>

	];
	&template_print("template.html",%t);
}
#=======================================================

=pod
sub lookup (){
	$ani = shift || {};
	return {} unless length($ani) > 6;    #ignore invalid ani

	warn "lookup ani=$ani"; return;
	$ani    = '+$ani' unless $ani =~ /^\+/;
	%h		= database_select_as_hash("SELECT ani,carrierid,carriername,iswireless,countrycode,name FROM ani_lookup " .
									  " WHERE ani='$ani'");

	return \%h if $h{$ani};
	$xml	= get "https://api.data24-7.com/carrier.php?username=$user247&password=$pass247&p1=$ani";

	$carrierid		= getvalue('carrierid', $xml);
	$carriername	= getvalue('carriername', $xml);
	$iswireless		= getvalue('iswireless', $xml);
	$countrycode	= getvalue('countrycode', $xml);
	$balance		= getvalue('balance', $xml);

	$xml	= '';
	#name service is only for phone number of USA
	if ($ani =~ /^(?:|\+)1/) {
		$xml = get "https://api.data24-7.com/id.php?username=$user247&password=$pass247&&p1=$ani";
	}

	$name			= getvalue('name', $xml);

	return {} unless $balance > 0;

	database_do_insert("INSERT into (ani,carrierid,carriername,iswireless,countrycode,name) VALUES ".
					   "('$ani', '$carrierid', '$carriername', '$iswireless', '$countrycode', '$name')");

	return {ani => $ani, 'carrierid' => $carrierid, 'carriername' => $carriername, 'iswireless' => $iswireless,
			countrycode => $countrycode, name => $name};

}

sub getvalue () {
	($key, $xml) = @_;
	return '' unless $key && $xml;

	my($value) =  $buffer =~ m{<$key>(.*?)</$key>}s;
	return defined $value ? $value : '';
}

=cut









