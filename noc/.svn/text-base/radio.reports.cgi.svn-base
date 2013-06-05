#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);

require "lookup.cgi";

#=======================================================
# reports for radio owners eye only
#=======================================================
# TODO: permissions and data at version2 are complete different then version1. we need review all code to approve
# we dont have mor radios. We have stations
#=======================================================
# lock this app to system.manager eyes only
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("radio.report") ne 1) {adm_error("no permission"); exit;}
#=======================================================




#=======================================================
# logout if no session
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
#unless (&active_user_permission_get("provider.data.access") >0) {adm_error("no permission"); exit;}
#=======================================================





#=======================================================
# get active stations
#=======================================================
# 0  no access to radio settings
# 1  view and edit they own radios
# 2  View and edit all radios plus radio DIDs
$stations_allow = "";
$tmp1	= &active_user_permission_get("radio.data.access");
$whoami = '';
if ($tmp1 eq "1"){
	$stations_allow = join(",",&database_select_as_array("SELECT distinct radio_data_station_id FROM radio_data_station_owner where system_user_id='$app{session_cookie_u}' "));
	$whoami = 'zj';
} elsif ($tmp1 eq "2"){
	$stations_allow = "ALL";
}
#=======================================================


#=======================================================
# main loop
#=======================================================
$my_url = "radio.reports.cgi";
$action = $form{action};
if 		($action eq "radio_report_minutes")		{ &do_radio_report_minutes();					}
elsif 	($action eq "radio_report_minutes_cdr")	{ &do_radio_report_minutes_cdr();				}
elsif	($action eq "radio_report_overview")	{ &do_radio_report_overview();					}
elsif	($action eq "radio_report_now")			{ &do_radio_report_now();						}
else											{ 	}
exit;
#=======================================================



#=======================================================
# actions
#=======================================================
sub do_radio_report_now(){
    #
    #-------------------------------
    # set permissions
    #-------------------------------
    $can_show_provider	= 1;
    $can_show_station	= 1;
    $can_show_ani		= 1;
    $can_show_ani_full	= 1;
    $can_show_did		= 0;
    #
    #-------------------------------
    # get basic data
    #-------------------------------
	%data_station	= database_select_as_hash("SELECT id,title FROM radio_data_station","title");
	#%data_provider	= database_select_as_hash("SELECT id,title FROM radio_data_provider","title");
	
	%data_stream	= database_select_as_hash("SELECT id,title FROM radio_data_station_channel","title");
	%hash = database_select_as_hash("SELECT radio_data_station_id,count(*) FROM radio_log_session where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour) group by radio_data_station_id ");
	foreach $id (keys %hash) {
		if (exists($data_station{$id})) {
			$data_station{$id}{calls} += $hash{$id};
		}
	}
    #
    #-------------------------------
    # get db connections by users, to guess total calls by each server
    #-------------------------------
    #$all_calls_now = 0;
	#%hash = &database_select_as_hash("show processlist","user,host,db,command,time,state,info");
	#foreach $id (keys %hash) {
	#	if (index("|radio-iowa-01|radio-iowa-02|ri1|ri2|rt14|rt15|rt16|","|$hash{$id}{user}|") ne -1) {$all_calls_now++}
	#}
    #
    #-------------------------------
    # stations select
    #-------------------------------
    $calls_now = 0;
    $filter_station_select = "";
    # check value from form
 	$filter_station = ($form{filter_station} eq "ALL") ? "ALL" : &clean_int($form{filter_station});
 	$filter_station = ( ($filter_station ne "") && ($stations_allow ne "ALL") && (index(",$stations_allow,",",$filter_station,") eq -1) ) ? "" : $filter_station;
	$filter_station = ($filter_station eq "") ? (split(/\,/,$stations_allow))[0] : $filter_station;
	# add all-stations option
	$tmp = ($filter_station eq "ALL") ? "selected" : "";
    $filter_station_select .= "<option $tmp value='ALL'>&#187; All radio stations</option>";
    $filter_station_select .= "<option>&nbsp;</option>";
	# add stations to select
	#%hash = database_select_as_hash("SELECT id,title FROM radio_data_station","title");
	foreach $id (sort{$data_station{$b}{calls} <=> $data_station{$a}{calls}} keys %data_station) {
		if ( ($stations_allow ne "ALL") && (index(",$stations_allow,",",$id,") eq -1) ) {next}
		$tmp = ($filter_station eq $id) ? "selected" : "";
    	$filter_station_select .= "<option $tmp value='$id'>&#187; (".&format_number($data_station{$id}{calls},0)." calls) $data_station{$id}{title}</option>";
	    $calls_now += $data_station{$id}{calls};
	}
	# prepare sql
    $filter_station_sql = " 1=0 ";
    if ($filter_station eq "ALL") {
		$filter_station_sql = " 1=1 ";
    } elsif ($filter_station ne "") {
		if ($whoami eq 'zj') {
			$filter_station_sql = " radio_data_station_id IN (" . join (",", map{"'$_'"} (split ',', $stations_allow)) . ") ";
		} else {
			$filter_station_sql = " radio_data_station_id='$filter_station' ";
		}
    }
    #
    #-------------------------------
    # prepare datatable
    #-------------------------------
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM radio_log_session where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour) and $filter_station_sql ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "New calls on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_log_session where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour) and $filter_station_sql order by datetime_start desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Old calls on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM radio_log_session where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour) and $filter_station_sql order by datetime_start limit #LIMIT_1#,#LIMIT_2# ";
    $datatable{sql}{col_names}			= "date,minutes,ani,did,radio_data_station_id,radio_data_station_title,extension,radio_data_station_channel_id ,radio_data_provider_id,radio_data_provider_title,content_source"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT
			id,
			DATE_FORMAT(datetime_start,'\%H:\%i:\%S'),
			round((unix_timestamp(now())-unix_timestamp(datetime_start))/60),
			ani,did,
			radio_data_station_id,'',extension,radio_data_station_channel_id ,radio_data_provider_id,'',''
		FROM radio_log_session
		WHERE id in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	# html values
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_report_now";
    $datatable{html}{form}{data}{1}{name}	= "filter_station";
    $datatable{html}{form}{data}{1}{value}	= $form{filter_station};
    $datatable{html}{line_click_link}		= "";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{cols}{0}{data_col_name}			= "date";
    $datatable{html}{cols}{0}{title}					= "Time";
    $datatable{html}{cols}{0}{flags}					= "";
    $datatable{html}{cols}{0}{width}					= 60;
    $datatable{html}{cols}{1}{data_col_name}			= "minutes";
    $datatable{html}{cols}{1}{title}					= "Minutes";
    $datatable{html}{cols}{1}{flags}					= "FORMAT_DECIMAL,ALIGN_RIGHT";
    $datatable{html}{cols}{1}{width}					= 50;
	if ($can_show_ani eq 1) {
	    $datatable{html}{cols}{2}{data_col_name}			= "ani";
	    $datatable{html}{cols}{2}{title}					= "Client phone<br>number";
	    $datatable{html}{cols}{2}{width}					= 110;
	}
	if ($can_show_did eq 1) {
	    $datatable{html}{cols}{3}{data_col_name}			= "did";
	    $datatable{html}{cols}{3}{title}					= "Phone radio<br>number";
	    $datatable{html}{cols}{3}{width}					= 110;
	}
	if ($can_show_station eq 1) {
    	$datatable{html}{cols}{4}{data_col_name}			= "radio_data_station_title";
	    $datatable{html}{cols}{4}{title}					= "Phone radio";
	}
	if ($can_show_provider eq 1) {
	    $datatable{html}{cols}{5}{data_col_name}			= "radio_data_provider_title";
    	$datatable{html}{cols}{5}{title}					= "Carrier";
	}
    $datatable{html}{cols}{6}{data_col_name}			= "content_source";
   	$datatable{html}{cols}{6}{title}					= "Content source";
	# dynamic data
	$form{page} = ($form{next} 		eq 1) ? $form{page}+1 : $form{page};
	$form{page} = ($form{previous} 	eq 1) ? $form{page}-1 : $form{page};
	$datatable{page} 		= $form{page};
	$datatable{page_size} 	= $form{page_size};
	$datatable{search}		= $form{search};
	$datatable{order}		= $form{order};
	#
    #-------------------------------
	# query datatable and get html
    #-------------------------------
	&datatable_query_data(\%datatable);
	foreach $id (keys %{$datatable{data}{values}}){
		# add name
		$tmp = clean_int($datatable{data}{values}{$id}{radio_data_station_id});
		$datatable{data}{values}{$id}{radio_data_station_title} = (exists($data_station{$tmp})) ? "$data_station{$tmp}{title}" : "<font color=#d0d0d0>No radio</font>";
		$tmp = clean_int($datatable{data}{values}{$id}{radio_data_provider_id});
		#$datatable{data}{values}{$id}{radio_data_provider_title} = (exists($data_provider{$tmp})) ? "$data_provider{$tmp}{title}" : "<font color=#d0d0d0>No provider</font>";
		$h = lookup($datatable{data}{values}{$id}{ani});
		warn "try to lookup " . $datatable{data}{values}{$id}{ani};

		$datatable{data}{values}{$id}{radio_data_provider_title} = $h->{carriername};
		$tmp = clean_int($datatable{data}{values}{$id}{radio_data_station_channel_id });
		if ($tmp eq "") {
			$datatable{data}{values}{$id}{content_source} = "Extension: $datatable{data}{values}{$id}{extension}";
		} else {
			$datatable{data}{values}{$id}{content_source} = (exists($data_stream{$tmp})) ? "$datatable{data}{values}{$id}{extension}: $data_stream{$tmp}{title}" : "Extension $datatable{data}{values}{$id}{extension}";
		}
		if ($datatable{data}{values}{$id}{did} eq "" ) {
			$datatable{data}{values}{$id}{did} = "&nbsp;";
		} else {
			$datatable{data}{values}{$id}{did} = &format_E164_number($datatable{data}{values}{$id}{did},"USA");
		}
		if ($datatable{data}{values}{$id}{ani} eq "" ) {
			$datatable{data}{values}{$id}{ani} = "&nbsp;";
		} else {
			if ($can_show_ani_full eq 1) {
				$datatable{data}{values}{$id}{ani} = &format_E164_number($datatable{data}{values}{$id}{ani},"USA");
			} else {
				$tmp = $datatable{data}{values}{$id}{ani};
				$datatable{data}{values}{$id}{ani} = "(".substr($tmp,1,3).") ".substr($tmp,4,3)."-XXXX";
			}
		}
	}
    #$datatable{html}{title}	= "Last and active radio sessions.";
	$datatable_html = &datatable_get_html(\%datatable);
	$calls_count = &format_number($datatable{data}{count},0);
	#
    #-------------------------------
	# print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "<b>".&format_number($calls_now,0)."</b> phone radio sessions now";
    $t{content} = qq[
	<script language="JavaScript">
	function show_filter() {
		\$('#radioname_search').toggle();
	}

	function do_filter() {
		var keyword = \$('#radioname').val();

		var pattern = new RegExp(keyword, "i");

		\$("#filter_station").each(function(){
		  \$(this).find("option").each(function(){
			if (!pattern.test(\$(this).html())) {
				\$(this).hide();
			}

			if (!keyword) {
				\$(this).show();
			}

		  });
		});
	}

	</script>
	<form action=$my_url>
	Radio station:	<select name='filter_station' id='filter_station'>	$filter_station_select</select> &nbsp;
	<a href='#' onclick='show_filter(); return false;' title='Click to filter radio station by name'> filter </a>
	<span id='radioname_search' style='display: none'><input type='text' name='radioname' id='radioname' value=''/>
	<input type=submit value='go' onclick='do_filter(); return false;'></span>|&nbsp;&nbsp;&nbsp;
	<input type=submit value='Update'>
	<input type=hidden name=action value=radio_report_now>
	</form>

	<br>
	$datatable_html
	<br>

	];
	&template_print("template.html",%t);
}
sub do_radio_report_minutes_cdr(){
	#
	# check station_id
 	$station_id = ($form{station_id} eq "ALL") ? "ALL" : &clean_int($form{station_id});
 	if ($stations_allow ne "ALL") {
	 	$station_id = ( (index(",$stations_allow,",",$station_id,") eq -1) ) ? "" : $station_id;
 	}
	if ($station_id eq "") {adm_error("No station"); }
	$station_title = "All stations";
	if ($station_id ne "ALL") {
		%hash = database_select_as_hash("SELECT 1,1,title FROM radio_data_station where id='$station_id' ","flag,value");
		if ($hash{1}{flag} ne "1") {adm_error("Unknown station"); }
		$station_title = $hash{1}{value};
	}
	$station_title = &clean_str($station_title," ","MINIMAL");
	#
	# check year/month
 	$month 	= &clean_int($form{month});
 	$year	= &clean_int($form{year});
	if ($month eq "") {adm_error("No month"); }
	if ($year  eq "") {adm_error("No year"); }
	if ( ($month<1) || ($month>12) ) {adm_error("Wrong month"); }
	if ( ($year<2000) || ($year>3000) ) {adm_error("Wrong year"); }
	#
	# prepare header
    print "Pragma: public\n";
    print "Expires: 0\n";
    print "Cache-Control: must-revalidate, post-check=0, pre-check=0\n";
    print "Content-type: application/octet-stream\n";
    print "Content-Disposition: attachment; filename=\"Radio CDR $year $month $station_title.csv\"\n";
    print "Content-Description: File Transfert\n";
#print "content-type: text/plain\n\n";
    print "\n";
    print "date,";
    print "ANI,";
    print "DID,";
    print "radio,";
    print "extension,";
    print "stream,";
    print "seconds\n";
	#
	# query and print
	%radio_stations 	= database_select_as_hash("SELECT id,title FROM radio_data_station ");
	%radio_streams		= database_select_as_hash("SELECT id,title FROM radio_data_station_channel ");
	foreach (keys %radio_stations) { $radio_stations{$_} = &clean_str($radio_stations{$_}," ","MINIMAL"); }
	foreach (keys %radio_streams ) { $radio_streams{$_}  = &clean_str($radio_streams{$_}," ","MINIMAL"); }
    $month_start		= $year."-".$month."-01";
	if ($station_id eq "ALL"){
		$sql = "
		SELECT id,
		DATE_FORMAT(datetime_start,'\%Y-\%m-\%d \%h:\%m:\%s'),
		ani,did,radio_data_station_id,extension,radio_data_station_channel_id ,answered_time
		FROM radio_log_session
  		where answered_time>0 and datetime_start >= '$month_start' and datetime_start < DATE_ADD('$month_start', INTERVAL 1 MONTH)
 	  	";
#order by id LIMIT 0,1000
	} else {
		$sql = "
		SELECT id,datetime_start,ani,did,radio_data_station_id,extension,radio_data_station_channel_id ,answered_time
		FROM radio_log_session
  		where answered_time>0 and radio_data_station_id='$station_id' and datetime_start >= '$month_start' and datetime_start < DATE_ADD('$month_start', INTERVAL 1 MONTH)
 	  	";
	}
#print "station_id=$station_id\n";
#print "month_start=$month_start\n";
#print "month=$month\n";
#print "year=$year\n";
#print "$sql\n\n";
    %hash = database_select_as_hash($sql,"date,ani,did,station_id,extension,stream_id,seconds");
	foreach $id (sort{$a <=> $b} keys %hash){
		$line = "";
		$tmp=$hash{$id}{date};			$tmp=&clean_str($tmp," -:","MINIMAL");	$line .= "\"$tmp\",";
		$tmp=$hash{$id}{ani};			$tmp=&format_dial_number(&clean_str($tmp," ","MINIMAL"));  $line .= "\"$tmp\",";
		$tmp=$hash{$id}{did};			$tmp=&format_dial_number(&clean_str($tmp," ","MINIMAL"));  $line .= "\"$tmp\",";
		$tmp=$hash{$id}{station_id};	$tmp=&clean_int($tmp); $tmp .= (exists($radio_stations{$tmp})) ? " $radio_stations{$tmp}" : "";	$line .= "\"$tmp\",";
		$tmp=$hash{$id}{extension};		$tmp=&clean_int($tmp); $line .= "\"$tmp\",";
		$tmp=$hash{$id}{stream_id};		$tmp=&clean_int($tmp); $tmp .= (exists($radio_streams{$tmp})) ? " $radio_streams{$tmp}" : "";	$line .= "\"$tmp\",";
		$tmp=$hash{$id}{seconds};		$tmp=&clean_int($tmp); $line .= "$tmp\n";
		print $line;
    }
}
sub do_radio_report_minutes(){
    #
    #-------------------------------
    # stations select
    #-------------------------------
    $filter_station_select = "";
    # check value from form
 	$filter_station = ($form{filter_station} eq "ALL") ? "ALL" : &clean_int($form{filter_station});
 	$filter_station = ( ($filter_station ne "") && ($stations_allow ne "ALL") && (index(",$stations_allow,",",$filter_station,") eq -1) ) ? "" : $filter_station;
	$filter_station = ($filter_station eq "") ? (split(/\,/,$stations_allow))[0] : $filter_station;
	# add all-stations option
	$tmp = ($filter_station eq "ALL") ? "selected" : "";
    $filter_station_select .= ($stations_allow eq "ALL") ? "<option $tmp value='ALL'>&#187; All radio stations</option>" : "";
    $filter_station_select .= ($stations_allow eq "ALL") ? "<option>&nbsp;</option>" : "";
	# add stations to select
	%hash = database_select_as_hash("SELECT id,title FROM radio_data_station","title");
	foreach $id (keys %hash) {
		if ( ($stations_allow ne "ALL") && (index(",$stations_allow,",",$id,") eq -1) ) {next}
		$tmp = ($filter_station eq $id) ? "selected" : "";
    	$filter_station_select .= "<option $tmp value='$id'>&#187; $hash{$id}{title}</option>";
	}
	# prepare sql
    $filter_station_sql = " 1=0 ";
	 $filter_daily_station_sql = " 1=0 ";
    if ($filter_station eq "ALL") {
		$filter_station_sql = " radio_data_station_id  is not null";
	  $filter_daily_station_sql = " radio_data_station_id=0";
    } elsif ($filter_station ne "") {
		$filter_station_sql = " radio_data_station_id='$filter_station' ";
	  $filter_daily_station_sql =" radio_data_station_id='$filter_station' ";
    }
    #
    #-------------------------------
    # prepare year/month select and values
    #-------------------------------
	%yearmonth_list = &database_select_as_hash("SELECT distinct DATE_FORMAT(date,'\%Y\%m'),1 FROM radio_log_listen_session_daily  ");
	%hash = database_select_as_hash("SELECT 1,1,max(DATE_FORMAT(date,'\%Y\%m')) FROM radio_log_listen_session_daily where $filter_station_sql ","flag,value");
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
    #-------------------------------
    # prepare datatable
    #-------------------------------
	%datatable = ();
	#$datatable{sql}{filter_ids_with_no_search}{get_total} = "select count(distinct DATE_FORMAT(datetime_start,'%d')) from radio_log_session where datetime_start >= '$filter_yearmonth_month_day_01' and datetime_start < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH) and $filter_station_sql   ";
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "select 31 ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by day";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "select DATE_FORMAT(date,'\%Y\%m\%d') from radio_log_listen_session_daily  where date >= '$filter_yearmonth_month_day_01' and date < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH) and $filter_daily_station_sql  group by DATE_FORMAT(date,'\%Y-\%m-\%d') order by DATE_FORMAT(date,'\%Y-\%m-\%d')  ";
    $datatable{sql}{col_names}			= "day,new_ani_count,old_ani_count,uids,sessions,minutes,less10_ani_count"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn



$datatable{sql}{get_data} 			= "
		select
			DATE_FORMAT(date,'\%Y\%m\%d'),
			DATE_FORMAT(date,'\%d \%M \%Y (\%W)'),
			new_clients as new_ani_count,
			return_clients as old_ani_count ,
			total_clients as uids,
			sessions,
			minutes,
			10mins_clients
		from
			radio_log_listen_session_daily
		where
			date>= '$filter_yearmonth_month_day_01' and date< DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)
			and $filter_daily_station_sql
		group by
			DATE_FORMAT(date,'\%Y-\%m-\%d')
	";

	warn $datatable{sql}{get_data};
	#
	# html values
    $datatable{html}{cols}{0}{data_col_name}			= "day";
    $datatable{html}{cols}{0}{title}					= "Date";
    $datatable{html}{cols}{0}{flags}					= "";
    $datatable{html}{cols}{1}{data_col_name}			= "new_ani_count";
    $datatable{html}{cols}{1}{title}					= "New clients<br>this day";
    $datatable{html}{cols}{1}{flags}					= "FORMAT_DECIMAL,ALIGN_RIGHT";
    $datatable{html}{cols}{1}{width}					= 100;
    $datatable{html}{cols}{2}{data_col_name}			= "old_ani_count";
    $datatable{html}{cols}{2}{title}					= "Return clients<br>this day";
    $datatable{html}{cols}{2}{flags}					= "FORMAT_DECIMAL,ALIGN_RIGHT";
    $datatable{html}{cols}{2}{width}					= 100;
    $datatable{html}{cols}{3}{data_col_name}			= "uids";
    $datatable{html}{cols}{3}{title}					= "Total clients<br>this day";
    $datatable{html}{cols}{3}{flags}					= "FORMAT_DECIMAL,ALIGN_RIGHT";
    $datatable{html}{cols}{3}{width}					= 100;
    $datatable{html}{cols}{4}{data_col_name}			= "sessions";
    $datatable{html}{cols}{4}{title}					= "Radio sessions<br>count";
    $datatable{html}{cols}{4}{flags}					= "FORMAT_DECIMAL,ALIGN_RIGHT";
    $datatable{html}{cols}{4}{width}					= 100;
    $datatable{html}{cols}{5}{data_col_name}			= "minutes";
    $datatable{html}{cols}{5}{title}					= "Radio sessions<br>minutes";
    $datatable{html}{cols}{5}{flags}					= "FORMAT_DECIMAL,ALIGN_RIGHT";
    $datatable{html}{cols}{5}{width}					= 100;

	$datatable{html}{cols}{6}{data_col_name}			= "less10_ani_count";
    $datatable{html}{cols}{6}{title}					= "Clients Less Than <br> 10 minutes";
    $datatable{html}{cols}{6}{flags}					= "FORMAT_DECIMAL,ALIGN_RIGHT";
    $datatable{html}{cols}{6}{width}					= 100;

    $datatable{html}{form}{action}						= "$my_url";
    $datatable{html}{form}{data}{0}{name}				= "action";
    $datatable{html}{form}{data}{0}{value}				= "radio_report_minutes";
    $datatable{html}{form}{data}{1}{filter_yearmonth}	= "filter_yearmonth";
    $datatable{html}{form}{data}{1}{value}				= $filter_yearmonth;
    $datatable{html}{form}{data}{2}{filter_station}		= "filter_station";
    $datatable{html}{form}{data}{2}{value}				= $filter_station;
	# dynamic data
	$form{page} = ($form{next} 		eq 1) ? $form{page}+1 : $form{page};
	$form{page} = ($form{previous} 	eq 1) ? $form{page}-1 : $form{page};
	$datatable{page} 		= 1;
	$datatable{page_size} 	= 50;
	$datatable{search}		= "";
	$datatable{order}		= 0;
	#
    #-------------------------------
	# query datatable and get html
    #-------------------------------
	&datatable_query_data(\%datatable);
	#
	# add extra data to this page
	$data{total_sessions_minutes}	= 0;
	$data{total_sessions}			= 0;

	foreach $id (sort{$a <=> $b} keys %{$datatable{data}{values}}){
		#
		#
		# statistics
		$data{total_sessions} 			+= $datatable{data}{values}{$id}{sessions};
		$data{total_sessions_minutes}	+= $datatable{data}{values}{$id}{minutes};


	}

	#
	# finish statistics
	$data{total_sessions} 			= &format_number($data{total_sessions},0);
	$data{total_sessions_minutes}	= &format_number($data{total_sessions_minutes},0);
	$sql = "
		select  1,1,count(distinct ani)
		from radio_log_session
		where ani<>'' and datetime_start>='$filter_yearmonth_month_day_01' and datetime_start<date_add('$filter_yearmonth_month_day_01', interval 1 month) and $filter_station_sql
	";
	%hash = &database_select_as_hash($sql,"flag,value");
	$data{total_clients} 			= &format_number($hash{1}{value},0);
	#
	# get html table for this data
	$datatable_html = &datatable_get_html(\%datatable);
	#
	#==========================================
	# print page
	#==========================================
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "<b>$data{total_sessions_minutes}</b> phone radio minutes";
	$t{content} = qq[
	<div class=clear style=width:450px;>
	In this month, we have <b>$data{total_clients}</b> unique clients
	that listen <b>$data{total_sessions}</b> radio sessions
	in <b>$data{total_sessions_minutes}</b> minutes at total.
	</div>
	<br>


	<form action=$my_url id=form_to_submit OnSubmit="return submitForm();">
		<table><tr>
		<td>
			Year/month:
			<button type=button OnClick="date_change(1)" id=date_previous>&#171 Past</button>
			<select id=date_select name=filter_yearmonth>	<option value=''>Select month</option>		<option value=''> </option>$filter_yearmonth_select</select>
			<button type=button OnClick="date_change(-1)" id=date_next>Present &#187</button>
		</td>
		<td>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</td>
		<td>
			Radio station:	<select name=filter_station>	$filter_station_select</select>
		</td>
		<td>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</td>
		<td>
			<button type=submit id=update_button_1 >Update</button>
			<button type=button read-only disabled id=update_button_2 style=display:none; ><img src=/noc/design/busy.gif align=left> Please wait...</button>
		</td>
		</tr></table>
	<input type=hidden name=action value=radio_report_minutes>
	</form>


<SCRIPT LANGUAGE="JavaScript">
function submitForm() {
	MyDisplay('update_button_1',0);
	MyDisplay('update_button_2',1);
	return true;
}
function date_change(gap){
	select = document.getElementById("date_select");
	val = select.selectedIndex;
	val_old = val;
	if (gap) {
		val = val+gap;
		if (val <= 2) {val=2}
		if (val >= (select.length-1) ) {val=(select.length-1)}
		if (val != val_old) {
			select.selectedIndex = val;
			document.getElementById("date_next").disabled=true;
			document.getElementById("date_next").readOnly=true;
			document.getElementById("date_previous").disabled=true;
			document.getElementById("date_previous").readOnly=true;
			MyDisplay('update_button_1',0);
			MyDisplay('update_button_2',1);
			document.getElementById("form_to_submit").submit();
		}
	}
	if (val == val_old) {
		document.getElementById("date_next").disabled		= (val <= 2) ? true : false;
		document.getElementById("date_next").readOnly		= (val <= 2) ? true : false;
		document.getElementById("date_previous").disabled	= (val >= (select.length-1)) ? true : false;
		document.getElementById("date_previous").readOnly	= (val >= (select.length-1)) ? true : false;
	}
}
date_change();
</script>



	<br>
	$datatable_html
	<br>
	<a
		onclick="if(confirm('This can take some minutes to calculate. Do you really need download this CDR?')) {return true} else {return false}"
		href="$my_url?action=radio_report_minutes_cdr&station_id=$filter_station&year=$filter_yearmonth_year&month=$filter_yearmonth_month"
		>&#187 Download CDR (csv format)
	</a>
	];
	&template_print("template.html",%t);
}
sub do_radio_report_overview(){
    #
	#==========================================
    # stations select
	#==========================================
    $filter_station_select = "";
    # check value from form
 	$filter_station = ($form{filter_station} eq "ALL") ? "ALL" : &clean_int($form{filter_station});
 	$filter_station = ( ($filter_station ne "") && ($stations_allow ne "ALL") && (index(",$stations_allow,",",$filter_station,") eq -1) ) ? "" : $filter_station;
	$filter_station = ($filter_station eq "") ? (split(/\,/,$stations_allow))[0] : $filter_station;
	# add all-stations option
	$tmp = ($filter_station eq "ALL") ? "selected" : "";
    $filter_station_select .= ($stations_allow eq "ALL") ? "<option $tmp value='ALL'>&#187; All radio stations</option>" : "";
    $filter_station_select .= ($stations_allow eq "ALL") ? "<option>&nbsp;</option>" : "";
	# add stations to select
	%hash = database_select_as_hash("SELECT id,title FROM radio_data_station","title");
	foreach $id (sort{$hash{$a}{title} cmp $hash{$b}{title} } keys %hash) {
		if ( ($stations_allow ne "ALL") && (index(",$stations_allow,",",$id,") eq -1) ) {next}
		$tmp = ($filter_station eq $id) ? "selected" : "";
    	$filter_station_select .= "<option $tmp value='$id'>&#187; $hash{$id}{title}</option>";
	}
	# prepare sql
    $filter_station_sql = " 1=0 ";
    if ($filter_station eq "ALL") {
		$filter_station_sql = " radio_data_station_id is not null ";
		$filter_daily_station_sql = " radio_data_station_id=0 ";
    } elsif ($filter_station ne "") {
		$filter_station_sql = " radio_data_station_id='$filter_station' ";
		$filter_daily_station_sql = " radio_data_station_id='$filter_station' ";
    }
    #
	#==========================================
    # prepare year/month select and values
	#==========================================
	%yearmonth_list = &database_select_as_hash("SELECT distinct DATE_FORMAT(date,'\%Y\%m'),1 FROM radio_log_listen_session_daily  ");
	%hash = database_select_as_hash("SELECT 1,1,max(DATE_FORMAT(date,'\%Y\%m')) FROM radio_log_listen_session_daily  ","flag,value");
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
	#
	#==========================================
	# plot minutes day by day
	#==========================================
	$sql = "
		select
			DATE_FORMAT(date,'\%d'),
			sum(minutes), sum(new_clients),sum(return_clients),sum(total_clients)
		from
			radio_log_listen_session_daily
		where
			date >= '$filter_yearmonth_month_day_01' and date < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)
			and $filter_daily_station_sql
		group by
			DATE_FORMAT(date,'\%d')
	";
	%data = &database_select_as_hash($sql,"minutes,new,old,uids");
	%plot = ();
	$plot{uid} = "minutes_day_by_day";
	$plot{x} = 400;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Minutes per day";
	$plot{series}{1}{color} = "5d788c";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = int($data{$dd}{minutes});
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$minutes_day_by_day = $plot{html};
	#
	#
	#==========================================
	# plot minutes month by month
	#==========================================
	$sql = "
		select
			DATE_FORMAT(date,'\%Y\%m'),
			sum(minutes)
		from
			radio_log_listen_session_daily
		where
			date > DATE_SUB(now(), INTERVAL 1 YEAR)
			and $filter_daily_station_sql
		group by
			DATE_FORMAT(date,'\%Y\%m')
	";
	%data2 = &database_select_as_hash($sql,"minutes");
	%plot = ();
	$plot{uid} = "minutes_month_by_month";
	$plot{x} = 300;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Minutes";
	$plot{series}{1}{color} = "d0d0d0";
	$slice_index = 1;
	foreach $d (sort{$b <=> $a} keys %data2) {
		$plot{data}{$slice_index}{1} = int($data2{$d}{minutes});
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $d;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$minutes_month_by_month = $plot{html};
	#
	#
	#==========================================
	# plot new clients day-by-day
	#==========================================

	%plot = ();
	$plot{uid} = "new_clients_day_by_day";
	$plot{x} = 350;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "First sessions per day";
	$plot{series}{1}{color} = "5d788c";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = $data{$dd}{new};
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$new_clients_day_by_day = $plot{html};
	%plot = ();
	$plot{uid} = "old_clients_day_by_day";
	$plot{x} = 350;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Return sessions per day";
	$plot{series}{1}{color} = "D0D0D0";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = $data{$dd}{old};
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$old_clients_day_by_day = $plot{html};
	#
	#
	#==========================================
	# get totals
	#==========================================
	%total = ();
	#
	# active_clients_at_start_of_month
	$sql = "
		select
			ani,sum(answered_time)
		from
			radio_log_session
		where
			ani<>''
			and datetime_start<'$filter_yearmonth_month_day_01'
			and datetime_start>date_sub('$filter_yearmonth_month_day_01', interval 6 month)
			and $filter_station_sql
		group by ani
	";
	$connection = $database->prepare($sql);
	$connection->execute;
	while ( @rows = $connection->fetchrow_array(  ) ) {
		$tmp1 = (@rows)[0];
		$tmp2 = (@rows)[1];
		if ( ($tmp1 ne "") && ($tmp2 > 120) ) { $total{active_clients_at_start_of_month}++ }
	}
	#
	# active_clients_at_end_of_month
	$sql = "
		select
			ani,sum(answered_time)
		from
			radio_log_session
		where
			ani<>''
			and datetime_start<=date_add('$filter_yearmonth_month_day_01', interval 1 month)
			and datetime_start>date_sub('$filter_yearmonth_month_day_01', interval 5 month)
			and $filter_station_sql
		group by ani
	";
	$connection = $database->prepare($sql);
	$connection->execute;
	while ( @rows = $connection->fetchrow_array(  ) ) {
		$tmp1 = (@rows)[0];
		$tmp2 = (@rows)[1];
		if ( ($tmp1 ne "") && ($tmp2 > 120) ) { $total{active_clients_at_end_of_month}++ }
	}
	#
	# inactive ANIs
	$sql = qq[
		select 1,1,sum(distinct ani)
		from radio_log_session
		where
			ani<>''
			and datetime_start<date_sub('$filter_yearmonth_month_day_01', interval 6 month)
			and $filter_station_sql
	];
	#%hash = &database_select_as_hash($sql,"flag,value");
	#$total{inactive_clients} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} ne "") ) ? $hash{1}{value} : 0;
	#
	#==========================================
	# print page
	#==========================================
    %t = &menu_permissions_get_as_template();

	$ic = &format_number($total{inactive_clients},0);
	$acsm = &format_number($total{active_clients_at_start_of_month},0);
	$acem = &format_number($total{active_clients_at_end_of_month},0);
	if ($total{active_clients_at_end_of_month} > $total{active_clients_at_start_of_month}){
		$acd = "(" .&format_number($total{active_clients_at_end_of_month}-$total{active_clients_at_start_of_month},0). " new clients)";
	} elsif ($total{active_clients_at_end_of_month} < $total{active_clients_at_start_of_month}){
		$acd = "(loose " .&format_number($total{active_clients_at_start_of_month}-$total{active_clients_at_end_of_month},0). " clients)";
	} else {
		$acd = "";
	}


    $t{my_url}	= $my_url;
    $t{title}	= "Phone radio overview";
	$t{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<form action=$my_url>
	Year/month: 	<select name=filter_yearmonth>	<option value=''>Select month</option>		<option value=''> </option>$filter_yearmonth_select</select> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	Radio station:	<select name=filter_station>	$filter_station_select</select> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	<input type=submit value='Update'>
	<input type=hidden name=action value=radio_report_overview>
	</form>
	<br>

	<fieldset style="width:730px;"><legend>Clients</legend>
	Clients count. One client is one ANI. We just count clients that listen at least 2 radio minutes. We dont count clients without ANI.
	'Inactive clients' are clients with no radio session in last 6 months.
	'Active clients' are clients with at least one radio session in last 6 months.
	<br>
	<br>
	<table border=0 colspan=0 cellpadding=2 cellspacing=0 class=clear>
		<tr>
		<td class=ar><h2>$acsm</h2></td>
		<td >Active clients at start of this month</td>
		</tr>
		<tr>
		<td class=ar><h3>$acem</h3></td>
		<td >Active clients at end of this month <font color=#c0c0c0>$acd</font></td>
		</tr>
	</table>




	</fieldset>
	<br>


	<fieldset style="width:730px;"><legend>Sessions</legend>
	Here we count radio sessions we serve group by 'First session' and 'Return sessions'.
	'First session' is a radio session we serve for a client with no access to this radio in last 6 months.
	'Return session' is a radio session we server for a know client (with at least one radio session in last 6 months).
	One client is one ANI. We do not count radio sessions without ANI.
	<br>
	<br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td valign=top>$new_clients_day_by_day</td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
		<td valign=top>$old_clients_day_by_day</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Minutes</legend>
	We just collect all radio sessions and sum all minutes.
	<br>
	<br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td valign=top>$minutes_day_by_day</td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
		<td valign=top>$minutes_month_by_month</td>
	</table>
	</fieldset>
	<br>


	];
	&template_print("template.html",%t);
}
sub do_radio_report_overview_OLD(){
    #
	#==========================================
    # stations select
	#==========================================
    $filter_station_select = "";
    # check value from form
 	$filter_station = ($form{filter_station} eq "ALL") ? "ALL" : &clean_int($form{filter_station});
 	$filter_station = ( ($filter_station ne "") && ($stations_allow ne "ALL") && (index(",$stations_allow,",",$filter_station,") eq -1) ) ? "" : $filter_station;
	$filter_station = ($filter_station eq "") ? (split(/\,/,$stations_allow))[0] : $filter_station;
	# add all-stations option
	$tmp = ($filter_station eq "ALL") ? "selected" : "";
    $filter_station_select .= ($stations_allow eq "ALL") ? "<option $tmp value='ALL'>&#187; All radio stations</option>" : "";
    $filter_station_select .= ($stations_allow eq "ALL") ? "<option>&nbsp;</option>" : "";
	# add stations to select
	%hash = database_select_as_hash("SELECT id,title FROM radio_data_station","title");
	foreach $id (keys %hash) {
		if ( ($stations_allow ne "ALL") && (index(",$stations_allow,",",$id,") eq -1) ) {next}
		$tmp = ($filter_station eq $id) ? "selected" : "";
    	$filter_station_select .= "<option $tmp value='$id'>&#187; $hash{$id}{title}</option>";
	}
	# prepare sql
    $filter_station_sql = " 1=0 ";
    if ($filter_station eq "ALL") {
		$filter_station_sql = " radio_data_station_id is not null ";
    } elsif ($filter_station ne "") {
		$filter_station_sql = " radio_data_station_id='$filter_station' ";
    }
    #
	#==========================================
    # prepare year/month select and values
	#==========================================
	%yearmonth_list = &database_select_as_hash("SELECT distinct DATE_FORMAT(datetime_start,'\%Y\%m'),1 FROM radio_log_session where $filter_station_sql  ");
	%hash = database_select_as_hash("SELECT 1,1,max(DATE_FORMAT(datetime_start,'\%Y\%m')) FROM radio_log_session where $filter_station_sql ","flag,value");
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
	#
	#==========================================
	# plot minutes day by day
	#==========================================
	$sql = "
		select
			DATE_FORMAT(datetime_start,'\%d'),
			sum(answered_time)
		from
			radio_log_session
		where
			datetime_start >= '$filter_yearmonth_month_day_01' and datetime_start < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)
			and $filter_station_sql
		group by
			DATE_FORMAT(datetime_start,'\%d')
	";
	%data = &database_select_as_hash($sql,"seconds");
	%plot = ();
	$plot{uid} = "minutes_day_by_day";
	$plot{x} = 400;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Minutes per day";
	$plot{series}{1}{color} = "92c23e";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = int($data{$dd}{seconds}/60);
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$minutes_day_by_day = $plot{html};
	#
	#
	#==========================================
	# plot minutes month by month
	#==========================================
	$sql = "
		select
			DATE_FORMAT(datetime_start,'\%Y\%m'),
			sum(answered_time)
		from
			radio_log_session
		where
			datetime_start > DATE_SUB(now(), INTERVAL 1 YEAR)
			and $filter_station_sql
		group by
			DATE_FORMAT(datetime_start,'\%Y\%m')
	";
	%data = &database_select_as_hash($sql,"seconds");
	%plot = ();
	$plot{uid} = "minutes_month_by_month";
	$plot{x} = 300;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Minutes";
	$plot{series}{1}{color} = "92c23e";
	$slice_index = 1;
	foreach $d (sort{$b <=> $a} keys %data) {
		$plot{data}{$slice_index}{1} = int($data{$d}{seconds}/60);
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $d;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$minutes_month_by_month = $plot{html};
	#
	#
	#==========================================
	# plot new clients day-by-day
	#==========================================
	# get known anis
	$sql = qq[
		select distinct ani,1
		from radio_log_session
		where
			ani<>''
			and datetime_start<'$filter_yearmonth_month_day_01'
			and datetime_start>date_sub('$filter_yearmonth_month_day_01', interval 6 month)
			and $filter_station_sql
	];
	%known_anis = &database_select_as_hash($sql);
	$sql = "
		select
			distinct DATE_FORMAT(datetime_start,'\%d'),ani
		from
			radio_log_session
		where
		    ani<>''
			and datetime_start >= '$filter_yearmonth_month_day_01' and datetime_start < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)
			and $filter_station_sql
		order by id
	";
	%data = ();
	$connection = $database->prepare($sql);
	$connection->execute;
	while ( @rows = $connection->fetchrow_array(  ) ) {
		$tmp1 = (@rows)[0];
		$tmp2 = (@rows)[1];
		unless (exists($known_anis{$tmp2})) {
			$data{$tmp1}{new}++;
			$known_anis{$tmp2}=1;
		} else {
			$data{$tmp1}{old}++;
		}
	}
	%plot = ();
	$plot{uid} = "new_clients_day_by_day";
	$plot{x} = 350;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "New clients per day";
	$plot{series}{1}{color} = "92c23e";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = $data{$dd}{new};
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$new_clients_day_by_day = $plot{html};
	%plot = ();
	$plot{uid} = "old_clients_day_by_day";
	$plot{x} = 350;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Return clients per day";
	$plot{series}{1}{color} = "92c23e";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = $data{$dd}{old};
		$plot{data}{$slice_index}{1}++;
		$plot{data}{$slice_index}{1}--;
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$old_clients_day_by_day = $plot{html};
	#
	#==========================================
	# print page
	#==========================================
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Phone radio overview";
	$t{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<form action=$my_url>
	Year/month: 	<select name=filter_yearmonth>	<option value=''>Select month</option>		<option value=''> </option>$filter_yearmonth_select</select> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	Radio station:	<select name=filter_station>	$filter_station_select</select> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
	<input type=submit value='Update'>
	<input type=hidden name=action value=radio_report_overview>
	</form>
	<br>

	<fieldset style="width:730px;"><legend>Minutes</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td valign=top>$minutes_day_by_day</td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
		<td valign=top>$minutes_month_by_month</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Clients</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td valign=top>$new_clients_day_by_day</td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>
		<td valign=top>$old_clients_day_by_day</td>
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

