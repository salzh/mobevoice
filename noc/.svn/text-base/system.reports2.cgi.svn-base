#!/usr/bin/perl
require "include.cgi";
#=======================================================
# TODO: Date format on version2 is complete different and still change (next week we will change clients structure to accept non ANI clients). All this code need review.
#=======================================================
# lock this app to system.manager eyes only
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("system.manager") ne 1) {adm_error("no permission"); exit;}
#=======================================================



#print "Content-type: text/html; charset=gbk\n\n";
use CGI::Carp qw(fatalsToBrowser);
use Carp; $SIG{ __DIE__ } = sub { Carp::confess( @_ ) };
use Data::Dumper;
#=======================================================
# logout if no session
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}

#if (&active_user_permission_check("system.manager") ne 1) {adm_error("no permission"); exit;}
#=======================================================



#=======================================================
# main loop
#=======================================================    
$my_url = "system.reports.cgi";
$action = $form{action};
if 		($action eq "system_reports_minutes_radio")	{ &do_system_reports_minutes_radio();		}
elsif 	($action eq "system_reports_minutes")		{ &do_system_reports_minutes();				}
elsif 	($action eq "system_reports_status")		{ &do_system_reports_status();				}	
elsif	($action eq "Top_phone_radios")		{ &do_Top_phone_radios();	}
elsif	($action eq "radio_report_now")		{ &do_radio_report_now();	}
elsif	($action eq "radio_report_now_image"){ &do_radio_report_now_image();	}
else 		{&cgi_redirect("./"); }
exit;
#=======================================================    



#=======================================================
# actions
#=======================================================
sub do_radio_report_now(){
    $total_calls = 0;
    $sql_active_dead_call_limit = " 6 hour ";  # calls bigger than this are flag as dead and then dont show in report
    $sql_past_call_statistics_interval = " 1 hour "; # how deep to get statistics
    #
    #-------------------------------
    # get stations names and open calls
    #-------------------------------
  
	%stations = database_select_as_hash("SELECT id,title FROM radio_data_station","title");
	%hash = database_select_as_hash("SELECT radio_data_station_id,count(*) FROM radio_log_session where datetime_stop is null and datetime_start>date_sub(now(),interval $sql_active_dead_call_limit) group by radio_data_station_id ");
	  
	
	foreach $id (keys %hash) {
		if (exists($stations{$id})) {
			$stations{$id}{calls} += $hash{$id};
		}
	}
    $content = "";
    $content_empty = "<tr><td colspan=2><center>... empty ...</center></td></tr>";
    foreach (sort{$stations{$b}{calls} <=> $stations{$a}{calls}} keys %stations){
    	if ($stations{$_}{calls} > 0) {
		    $content .= "<tr class='filter_$stations{$_}{title}'><td><a href=\"radio.station.cgi?action=radio_station_history&station_id=$_\">$stations{$_}{title}</a></td><td class=ar>$stations{$_}{calls}</td></tr>";
		    $tmp = $stations{$_}{calls}; $tmp++; $tmp--;
		    $content_empty = "";
    	}
    }
    $content .= $content_empty;
    $top_stations = $content;
    #
    #-------------------------------
    # get system_host and open calls
    #-------------------------------
	%hash = database_select_as_hash("SELECT system_host,system_host,count(*) FROM radio_log_session where datetime_stop is null and datetime_start>date_sub(now(),interval $sql_active_dead_call_limit) group by system_host ","title,calls");
    $content = "";
    $content_empty = "<tr><td colspan=2><center>... empty ...</center></td></tr>";
    foreach (sort{$hash{$b}{calls} <=> $hash{$a}{calls}} keys %hash){
		$hash{$_}{calls}++;
		$hash{$_}{calls}--;
    	if ($hash{$_}{calls} > 0) {
		    $content .= "<tr><td >$hash{$_}{title}</td><td class=ar>$hash{$_}{calls}</td></tr>";
		    $total_calls += $hash{$_}{calls};
		    $content_empty = "";
    	}
    }
    $content .= $content_empty;
    $top_hosts = $content;
    #
    #-------------------------------
    # count average minutes last hour
    #-------------------------------
    $sql = "
	SELECT
		radio_data_station_channel_id ,
		count(*),
		SUM(IF(answered_time<=15, 1,0)) as calls_1,
		SUM(IF( (answered_time>15 and answered_time<=60) , 1,0)) as calls_2,
		SUM(IF( (answered_time>60 and answered_time<=600) , 1,0)) as calls_3,
		SUM(IF( (answered_time>600) , 1,0)) as calls_4,
		sum(answered_time)

	FROM
		radio_log_session
	where
		datetime_stop is not null and
		datetime_stop>date_sub(now(),interval $sql_past_call_statistics_interval) and
		answered_time is not null and
		radio_data_station_channel_id  is not null
	group by
		radio_data_station_channel_id 
    ";
	%hash = database_select_as_hash($sql,"calls,calls_1,calls_2,calls_3,calls_4,seconds");
	$bar_length_total = 100;
	$bar_height = 13;
    foreach $stream_id (keys %hash){
		$hash{$stream_id}{percentage_1} = ($hash{$stream_id}{calls}<1) ? 0 : (100*($hash{$stream_id}{calls_1}/$hash{$stream_id}{calls}));
		$hash{$stream_id}{percentage_2} = ($hash{$stream_id}{calls}<1) ? 0 : (100*($hash{$stream_id}{calls_2}/$hash{$stream_id}{calls}));
		$hash{$stream_id}{percentage_3} = ($hash{$stream_id}{calls}<1) ? 0 : (100*($hash{$stream_id}{calls_3}/$hash{$stream_id}{calls}));
		$hash{$stream_id}{percentage_4} = ($hash{$stream_id}{calls}<1) ? 0 : (100*($hash{$stream_id}{calls_4}/$hash{$stream_id}{calls}));
		$hash{$stream_id}{bar_length_1} = ($hash{$stream_id}{percentage_1}>0) ? int( ($bar_length_total - 4) * ($hash{$stream_id}{percentage_1}/100) )+1 : 1;
		$hash{$stream_id}{bar_length_2} = ($hash{$stream_id}{percentage_2}>0) ? int( ($bar_length_total - 4) * ($hash{$stream_id}{percentage_2}/100) )+1 : 1;
		$hash{$stream_id}{bar_length_4} = ($hash{$stream_id}{percentage_4}>0) ? int( ($bar_length_total - 4) * ($hash{$stream_id}{percentage_4}/100) )+1 : 1;
		$hash{$stream_id}{bar_length_3} = $bar_length_total - ($hash{$stream_id}{bar_length_1}+$hash{$stream_id}{bar_length_2}+$hash{$stream_id}{bar_length_4})
    }
    $selected_ids = join(",",(keys %hash));
    $sql = "
		SELECT s.id,r.title,r.id,s.extension,s.stream_type
		FROM radio_data_station_channel as s, radio_data_station as r
		where s.radio_data_station_id=r.id and s.id in ($selected_ids)
    ";
	%hash2 = database_select_as_hash($sql,"station,station_id,extension,type");
	foreach $id (keys %hash2) {
		if (exists($hash{$id})) {
			$hash{$id}{station} 	= $hash2{$id}{station};
			$hash{$id}{station_id} 	= $hash2{$id}{station_id};
			$hash{$id}{extension}	= $hash2{$id}{extension};
			$hash{$id}{type} 		= $hash2{$id}{type};
			%hash3 = database_select_as_hash("SELECT 1,1,title FROM radio_data_did where radio_data_station_id='$hash{$id}{station_id}' LIMIT 0,1","flag,value");
			$hash{$id}{did}			= ($hash3{1}{flag} eq 1) ? $hash3{1}{value} : "UNKNOWN";
		}
	}
    $content = "";
    $content_empty = "<tr><td colspan=3><center>... empty ...</center></td></tr>";
    foreach $stream_id (sort{$hash{$b}{percentage_1} <=> $hash{$a}{percentage_1}} keys %hash){
    	if ($hash{$stream_id}{calls} > 10) {
    		$tmp1 = ($hash{$stream_id}{station_id} eq "") ? "Unknown $stream_id" : "<a href=radio.station.cgi?action=radio_station_edit&station_id=$hash{$stream_id}{station_id}>$hash{$stream_id}{station}</a>";
    		$tmp2 = ($hash{$stream_id}{station_id} eq "") ? "&nbsp;" : "<a href=radio.station.cgi?action=radio_station_stream_edit&stream_id=$stream_id>$hash{$stream_id}{did}</a>";
    		$tmp3 = ($hash{$stream_id}{station_id} eq "") ? "&nbsp;" : "<a href=radio.station.cgi?action=radio_station_stream_edit&stream_id=$stream_id>Ext:$hash{$stream_id}{extension}</a>";
			$content .= "<tr class='filter_$hash{$stream_id}{station}'>";
			$content .= "<td >$tmp1</td>";
			$content .= "<td class=ar>$tmp2</td>";
			$content .= "<td class=al>$tmp3</td>";
			$content .= "<td width=40 class=ar>".&format_number($hash{$stream_id}{calls},0)."</td>";
			$content .= "<td width=$bar_length_total>";
			$content .= "<div class=clear style='Background-color:#f46b66; float:left; width:".$hash{$stream_id}{bar_length_1}."px' ><img title='".&format_number($hash{$stream_id}{percentage_1},2)."\%'  src=/noc/design/spc.gif width='$hash{$stream_id}{bar_length_1}'  height='$bar_height' hspace=0 vspace=0 border=0></div>";
			$content .= "<div class=clear style='Background-color:#ffbb6d; float:left; width:".$hash{$stream_id}{bar_length_2}."px' ><img title='".&format_number($hash{$stream_id}{percentage_2},2)."\%'  src=/noc/design/spc.gif width='$hash{$stream_id}{bar_length_1}'  height='$bar_height' hspace=0 vspace=0 border=0></div>";
			$content .= "<div class=clear style='Background-color:#dfb8fb; float:left; width:".$hash{$stream_id}{bar_length_3}."px' ><img title='".&format_number($hash{$stream_id}{percentage_3},2)."\%'  src=/noc/design/spc.gif width='$hash{$stream_id}{bar_length_1}'  height='$bar_height' hspace=0 vspace=0 border=0></div>";
			$content .= "<div class=clear style='Background-color:#c1e2c0; float:left; width:".$hash{$stream_id}{bar_length_4}."px' ><img title='".&format_number($hash{$stream_id}{percentage_4},2)."\%'  src=/noc/design/spc.gif width='$hash{$stream_id}{bar_length_1}'  height='$bar_height' hspace=0 vspace=0 border=0></div>";
			$content .= "</td>";
			$content .= "</tr>";
		    $content_empty = "";
    	}
    }
    $content .= $content_empty;
    $average_call_duration = $content;
    #
    #-------------------------------
    # count average minutes last hour
    #-------------------------------
    $sql = "
	SELECT
		system_host,
		count(*),
		SUM(IF(answered_time<=15, 1,0)) as calls_1,
		SUM(IF( (answered_time>15 and answered_time<=60) , 1,0)) as calls_2,
		SUM(IF( (answered_time>60 and answered_time<=600) , 1,0)) as calls_3,
		SUM(IF( (answered_time>600) , 1,0)) as calls_4,
		sum(answered_time)

	FROM
		radio_log_session
	where
		datetime_stop is not null and
		datetime_stop>date_sub(now(),interval $sql_past_call_statistics_interval) and
		answered_time is not null and
		radio_data_station_channel_id  is not null
	group by
		system_host
    ";
	%hash = database_select_as_hash($sql,"calls,calls_1,calls_2,calls_3,calls_4,seconds");
	$bar_length_total = 100;
	$bar_height = 13;
    foreach $stream_id (keys %hash){
		$hash{$stream_id}{percentage_1} = ($hash{$stream_id}{calls}<1) ? 0 : (100*($hash{$stream_id}{calls_1}/$hash{$stream_id}{calls}));
		$hash{$stream_id}{percentage_2} = ($hash{$stream_id}{calls}<1) ? 0 : (100*($hash{$stream_id}{calls_2}/$hash{$stream_id}{calls}));
		$hash{$stream_id}{percentage_3} = ($hash{$stream_id}{calls}<1) ? 0 : (100*($hash{$stream_id}{calls_3}/$hash{$stream_id}{calls}));
		$hash{$stream_id}{percentage_4} = ($hash{$stream_id}{calls}<1) ? 0 : (100*($hash{$stream_id}{calls_4}/$hash{$stream_id}{calls}));
		$hash{$stream_id}{bar_length_1} = ($hash{$stream_id}{percentage_1}>0) ? int( ($bar_length_total - 4) * ($hash{$stream_id}{percentage_1}/100) )+1 : 1;
		$hash{$stream_id}{bar_length_2} = ($hash{$stream_id}{percentage_2}>0) ? int( ($bar_length_total - 4) * ($hash{$stream_id}{percentage_2}/100) )+1 : 1;
		$hash{$stream_id}{bar_length_4} = ($hash{$stream_id}{percentage_4}>0) ? int( ($bar_length_total - 4) * ($hash{$stream_id}{percentage_4}/100) )+1 : 1;
		$hash{$stream_id}{bar_length_3} = $bar_length_total - ($hash{$stream_id}{bar_length_1}+$hash{$stream_id}{bar_length_2}+$hash{$stream_id}{bar_length_4})
    }
    $content = "";
    $content_empty = "<tr><td colspan=3><center>... empty ...</center></td></tr>";
    foreach $stream_id (sort{$hash{$b}{percentage_1} <=> $hash{$a}{percentage_1}} keys %hash){
    	if ($hash{$stream_id}{calls} > 10) {
			$content .= "<tr>";
			$content .= "<td >$stream_id</td>";
			$content .= "<td width=40 class=ar>".&format_number($hash{$stream_id}{calls},0)."</td>";
			$content .= "<td width=$bar_length_total>";
			$content .= "<div class=clear style='Background-color:#f46b66; float:left; width:".$hash{$stream_id}{bar_length_1}."px' ><img title='".&format_number($hash{$stream_id}{percentage_1},2)."\%'  src=/noc/design/spc.gif width='$hash{$stream_id}{bar_length_1}'  height='$bar_height' hspace=0 vspace=0 border=0></div>";
			$content .= "<div class=clear style='Background-color:#ffbb6d; float:left; width:".$hash{$stream_id}{bar_length_2}."px' ><img title='".&format_number($hash{$stream_id}{percentage_2},2)."\%'  src=/noc/design/spc.gif width='$hash{$stream_id}{bar_length_1}'  height='$bar_height' hspace=0 vspace=0 border=0></div>";
			$content .= "<div class=clear style='Background-color:#dfb8fb; float:left; width:".$hash{$stream_id}{bar_length_3}."px' ><img title='".&format_number($hash{$stream_id}{percentage_3},2)."\%'  src=/noc/design/spc.gif width='$hash{$stream_id}{bar_length_1}'  height='$bar_height' hspace=0 vspace=0 border=0></div>";
			$content .= "<div class=clear style='Background-color:#c1e2c0; float:left; width:".$hash{$stream_id}{bar_length_4}."px' ><img title='".&format_number($hash{$stream_id}{percentage_4},2)."\%'  src=/noc/design/spc.gif width='$hash{$stream_id}{bar_length_1}'  height='$bar_height' hspace=0 vspace=0 border=0></div>";
			$content .= "</td>";
			$content .= "</tr>";
		    $content_empty = "";
    	}
    }
    $content .= $content_empty;
    $average_call_duration_by_host = $content;

	%hash		 = database_select_as_hash("select did, title from radio_data_did", "title");
	%did_carrier = ();
	%carrier = ();

	for (keys %hash) {
		$hash{$_}{title} =~ /^(.*)\(/;
		$c = $1 || 'iowa';
		$c =~ s/\s//g;
		$did_carrier{$_} = $c;
		$carrier{$c} = 0;
	}

	$sql     = "SELECT did,did,count(*) FROM radio_log_session where datetime_stop is null and " .
				"datetime_start>date_sub(now(),interval $sql_active_dead_call_limit) group by did ";
	warn $sql;

	%hash    = database_select_as_hash($sql, "did,calls");

	for (keys %hash) {
		next unless $did_carrier{$_};
		$carrier{$did_carrier{$_}} += $hash{$_}{calls};
	}

	$top_carrier = '';
	for (sort{$carrier{$b} <=> $carrier{$a}} keys %carrier) {
		$top_carrier .= "<tr><td>$_</td><td>$carrier{$_}</td></tr>\n"
	}

	$taglist = get_tag_list();

	#
    #-------------------------------
	# print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "System now ($total_calls sessions)";
    $t{content} = "";
	#
	# add extra info for admin
	$t{content} .= qq[

	<script>
	status_time  = "-3600";
	status_type  = "listen";
	status_seq   = 0;
	function MySrc(id,newsrc)		{ obj = document.getElementById(id); if (obj) {obj.src = newsrc;} }
	function status_time_set(value) { status_time = value; status_update(); }
	function status_update(){
		status_seq++;
		url_time = status_time;
		MySrc("img_RI154"       ,"$my_url?action=radio_report_now_image&hostname=RI154;plugin=radio;type=conference_listeners;begin=" + url_time + ";force_refresh="+status_seq);
		MySrc("img_RI153"       ,"$my_url?action=radio_report_now_image&hostname=RI153;plugin=radio;type=conference_listeners;begin=" + url_time + ";force_refresh="+status_seq);
		MySrc("img_RT14"        ,"$my_url?action=radio_report_now_image&hostname=RT14;plugin=radio;type=conference_listeners;&begin=" + url_time + ";force_refresh="+status_seq);
		MySrc("img_rt15"        ,"$my_url?action=radio_report_now_image&hostname=radio-texas-15;plugin=radio;type=radio_calls;begin=" + url_time + ";force_refresh="+status_seq);
		MySrc("img_E199"        ,"$my_url?action=radio_report_now_image&hostname=radio-dfc-e199;plugin=radio;type=radio_calls;begin=" + url_time + ";force_refresh="+status_seq);
	  MySrc("img_E23"        ,"$my_url?action=radio_report_now_image&hostname=e23;plugin=radio;type=conference_listeners;begin=" + url_time + ";force_refresh="+status_seq);
	  MySrc("img_RI201"        ,"$my_url?action=radio_report_now_image&hostname=RI201;plugin=radio;type=conference_listeners;begin=" + url_time + ";force_refresh="+status_seq);
	  MySrc("img_E167"        ,"$my_url?action=radio_report_now_image&hostname=e167;plugin=radio;type=conference_listeners;begin=" + url_time + ";force_refresh="+status_seq);
	  MySrc("img_DEV"        ,"$my_url?action=radio_report_now_image&hostname=e90;plugin=radio;type=conference_listeners;begin=" + url_time + ";force_refresh="+status_seq);


	}

	function filter_station () {
		\$('#taglist').toggle();
	}
	var isMInput = 0;

	function do_filter () {
		var keyword = '';
		if (isMInput) {
			keyword = \$('#inputtag').val();
		} else {
			keyword = \$("input[name='tag']:checked").val();
		}

		//alert("filter by " + keyword);
		var pattern = new RegExp("^filter_");
		\$("tr").each(function(){
			var c = \$(this).attr('class');
			if (pattern.test(c)) {
				var p = new RegExp(keyword, "i");
				if (!p.test(c)) {
					\$(this).hide();
				}
			}
		});
	}


	function do_reset () {
		var pattern = new RegExp("^filter_");

		\$("tr").each(function(){
			var c = \$(this).attr('class');
			if (pattern.test(c)) {
				\$(this).show();
			}
		});
	}
	function toggle_tag(mode) {
		isMInput = mode;
		if (mode) {
			\$('#minput').show();
			\$('#showtag').hide();
		} else {
			\$('#minput').hide();
			\$('#showtag').show();
		}
	}

	</script>
	<a href="#" onclick="filter_station();return false">filter station</a><br>
	<div id='taglist' style="display: none">
	<a href="#" onclick="toggle_tag(0);return false;">Select Tags</a> &nbsp;|&nbsp;
	<a href="#" onclick="toggle_tag(1);return false;">Input Tags</a>
	<div id="showtag" >
	$taglist
	</div>
	<div id="minput" style="display: none">
	<input type="text" name="inputtag" id="inputtag" value=''/>
	</div>
	<input type="submit" onclick="do_filter(); return false" value="filter"/> &nbsp;&nbsp;
	<input type="submit" onclick="do_reset(); return false" value="reset"/>

	</div>

	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear><tr><td valign=top><img src=/noc/design/spc.gif width=600 height=1 hspace=0 vspace=0 border=0>

			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear width=100%><tr><td valign=top>
				<h1>Active sessions by station</h1>
				<div style="max-height:150px;overflow-x:hidden;overflow-y:auto; border-bottom:1px solid #a0a0a0; border-top:1px solid #a0a0a0;">
				<table width=100% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
					<thead>
						<tr>
						<td>Radio station</td>
						<td>Calls</td>
						</tr>
					</thead>
					<tbody>
						$top_stations
					</tbody>
				</table>
				</div>
			</td><td>&nbsp;</td>
				<td valign=top>
				<h1>Active sessions by Hosts</h1>
				<div style="max-height:150px;overflow-x:hidden;overflow-y:auto; border-bottom:1px solid #a0a0a0; border-top:1px solid #a0a0a0;">
				<table width=100% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
					<thead>
						<tr>
						<td>Host</td>
						<td>Calls</td>
						</tr>
					</thead>
					<tbody>
						$top_hosts
					</tbody>
				</table>
				</div>
			</td><td>&nbsp;</td>
				<td valign=top>
				<h1>Active sessions by Carriers</h1>
				<div style="max-height:150px;overflow-x:hidden;overflow-y:auto; border-bottom:1px solid #a0a0a0; border-top:1px solid #a0a0a0;">
				<table width=100% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
					<thead>
						<tr>
						<td>Carrier</td>
						<td>Calls</td>
						</tr>
					</thead>
					<tbody>
						$top_carrier
					</tbody>
				</table>
				</div>
			</td></tr></table>

			<br>
			<h1>Last hour statistics by radio channel</h1>
			<div style="max-height:200px;overflow-x:hidden;overflow-y:auto; border-bottom:1px solid #a0a0a0; border-top:1px solid #a0a0a0;">
			<table width=100% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
				<thead>
					<tr>
					<td colspan=3>Radio station / DID / extension</td>
					<td >Calls</td>
					<td >Session duration</td>
					</tr>
				</thead>
				<tbody>
					$average_call_duration
				</tbody>
			</table>
			</div>

			<br>
			<h1>Last hour statistics by radio host</h1>
			<div style="max-height:200px;overflow-x:hidden;overflow-y:auto; border-bottom:1px solid #a0a0a0; border-top:1px solid #a0a0a0;">
			<table width=100% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
				<thead>
					<tr>
					<td >Host</td>
					<td >Calls</td>
					<td >Session duration</td>
					</tr>
				</thead>
				<tbody>
					$average_call_duration_by_host
				</tbody>
			</table>
			</div>

			<br>
			<b>Session duration:</b>
			<div style="background-image:url(/noc/design/icons/bullet_red.png);background-repeat:no-repeat;padding-left:16px;"><b>Fail sessions:</b> Sessions with less than 15 seconds. </div>
			<div style="background-image:url(/noc/design/icons/bullet_orange.png);background-repeat:no-repeat;padding-left:16px;"><b>Curious client:</b> Calls from 15 seconds to 2 minutes. </div>
			<div style="background-image:url(/noc/design/icons/bullet_purple.png);background-repeat:no-repeat;padding-left:16px;"><b>Casual client:</b> Calls from 2 minutes to 10 minutes. </div>
			<div style="background-image:url(/noc/design/icons/bullet_green.png);background-repeat:no-repeat;padding-left:16px;"><b>Hard-usage client:</b> Calls with more than 10 minutes. </div>

	</td><td>&nbsp;&nbsp;&nbsp;</td><td valign=top><img src=/noc/design/spc.gif width=400 height=1 hspace=0 vspace=0 border=0>

			<div class=clear style=float:right>
			<a href="javascript:status_time_set('-3600')">1hr</a>,
			<a href="javascript:status_time_set('-7200')">2hrs</a>,
			<a href="javascript:status_time_set('-21600')">6hrs</a>,
			<a href="javascript:status_time_set('-86400')">24hrs</a>,
			<a href="javascript:status_time_set('-172800')">48hrs</a>,
			<a href="javascript:status_time_set('-2678400')">30 days</a>
			</div>
			<h1>Servers metrics</h1>
		  
		 <img id=img_DEV        width=400 height=176 src=/noc/design/spc.gif  hspace=2 vspace=2 border=0 float=left>


	</td></tr></table>

	<script>status_update();</script>
	];
	$t{content} .= qq[



	];
	&template_print("template.html",%t);




}
sub do_Top_phone_radios(){
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
	<input type=hidden name=action value=Top_phone_radios>
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
sub do_system_reports_minutes(){
    #
    #-------------------------------
    # prepare year/month select and values
    #-------------------------------
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
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    %t = &menu_permissions_get_as_template();
	$t{my_url}	= $my_url;
    $t{title}	= "system minutes at this month";
    $t{content}	= qq[ 
(work in progress) 
<!-- 
		<form action=$my_url>
		Year/month: 	<select name=filter_yearmonth>	<option value=''>Select month</option>		<option value=''> </option>$filter_yearmonth_select</select> 
		<input type=submit value='Update'>
		<input type=hidden name=action value=system_reports_minutes>
		</form>
		<br>

		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=600>
			<thead>
				<tr>
				<td >Radio station</td>
				<td width=50 class=ar >&nbsp;</td>
				<td width=70 class=ar >Minutes</td>
				</tr>
			</thead>
			<tbody >
				$html
			</tbody>
			<tfoot>
				$html_total
			</tfoot>
		</table>
-->
    ];
    &template_print("template.html",%t);
}
sub do_system_reports_minutes_radio(){
    #
    #-------------------------------
    # prepare year/month select and values
    #-------------------------------
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
    #-------------------------------
    # load data
    #-------------------------------
	$sql = "
		select 
			radio_data_station_id,DATE_FORMAT(datetime_start,'\%d'),count(*),sum(answered_time)
		from 
			radio_log_session 
		where 
		 datetime_start >= '$filter_yearmonth_month_day_01' and datetime_start < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)  
			and answered_time>0 
		group by radio_data_station_id,DATE_FORMAT(datetime_start,'\%d')
	";
	%log_data = &database_select_as_hash_with_auto_key($sql,"station_id,day,count,seconds");
	%radio_stations = &database_select_as_hash("SELECT id,title FROM radio_data_station ","title");
	#
    #-------------------------------
    # organize data
    #-------------------------------
    %data = ();
    foreach $i (keys %log_data){
    	$station_id = $log_data{$i}{station_id};
    	$day		= $log_data{$i}{day};
    	$seconds	= $log_data{$i}{seconds};
    	$data{s}{$station_id}{d}{$day} += $seconds; 
    	$data{t}{d}{$day} += $seconds; 
    }
    foreach $station_id (keys %{$data{s}}){
    	$data{s}{$station_id}{t} = (exists($radio_stations{$station_id})) ? $radio_stations{$station_id}{title} : "(Unknown station $station_id)";
    	$data{s}{$station_id}{ms} = 0;
    	$data{s}{$station_id}{ts} = 0;
	    foreach $d (keys %{$data{s}{$station_id}{d}}){
	    	$s = $data{s}{$station_id}{d}{$d};
	    	$data{s}{$station_id}{ms} = ($s > $data{s}{$station_id}{ms}) ? $s : $data{s}{$station_id}{ms};
	    	$data{s}{$station_id}{ts} += $s;
	    }
    }
   	$data{t}{ms} = 0;
   	$data{t}{ts} = 0;
    foreach $d (keys %{$data{t}{d}}){
    	$s = $data{t}{d}{$d};
    	$data{t}{ms} = ($s > $data{t}{ms}) ? $s : $data{t}{ms};
    	$data{t}{ts} += $s;
    }
	#
    #-------------------------------
    # render html
    #-------------------------------
    $html = "";
    $html_empty = "<tr><td colspan=10 style=padding:20px;><center>no data...</center></td></tr>";
	$bar_x=3;
	$bar_y=27;
    foreach $station_id (sort{$data{s}{$b}{ts} <=> $data{s}{$a}{ts}} keys %{$data{s}}){
      	$html_empty = "";
      	$html_month = "";
		foreach $day_int (1..31){
			$d = substr("00$day_int",-2,2);
			$v = $data{s}{$station_id}{d}{$d} || 0;
			$m = $data{s}{$station_id}{ms} || 0;
			$r = ($m>0) ? ($v/$m) : 0;	
			$t = "day $day_int with ". &format_number(($v/60),0) ." minutes";
			$b1 = int(($bar_y-2)*$r);
			$b1++;
			$b2 = $bar_y-$b1;
			$html_month .= "<td  title='$t' valign=top	style='width:".$bar_x."px; height:".$bar_y."px; background-color:#496FC7; margin:0px; padding:0px; border:0px;'>";
			$html_month .= "<div title='$t' 			style='width:".$bar_x."px; height:".$b2."px;    background-color:#aaaaaa; margin:0px; padding:0px; border:0px;'></div>";
			$html_month .= "</td>";
		}
    	$html .= "<tr>"; 
    	$html .= "<td><a href='radio.station.cgi?filter_yearmonth=$filter_yearmonth&station_id=$station_id&action=radio_station_history'>$data{s}{$station_id}{t}</a></td>"; 
    	$html .= "<td class=ac><table class=clear border=1 colspan=0 cellpadding=0 cellspacing=0><tr>$html_month</tr></table></td>"; 
    	$html .= "<td class=ar>". &format_number( ($data{s}{$station_id}{ts}/60) ,0). "</td>"; 
    	$html .= "</tr>"; 
    }
    $html .= $html_empty;
    $html_total = "";
   	$html_month = "";
	foreach $day_int (1..31){
		$d = substr("00$day_int",-2,2);
		$v = $data{t}{d}{$d} || 0;
		$m = $data{t}{ms} || 0;
		$r = ($m>0) ? ($v/$m) : 0;	
		$t = "day $day_int with ". &format_number(($v/60),0) ." minutes";
		$b1 = int(($bar_y-2)*$r);
		$b1++;
		$b2 = $bar_y-$b1;
		$html_month .= "<td  title='$t' valign=top	style='width:".$bar_x."px; height:".$bar_y."px; background-color:#496FC7; margin:0px; padding:0px; border:0px;'>";
		$html_month .= "<div title='$t' 			style='width:".$bar_x."px; height:".$b2."px;    background-color:#aaaaaa; margin:0px; padding:0px; border:0px;'></div>";
		$html_month .= "</td>";
	}
   	$html_total .= "<tr>"; 
   	$html_total .= "<td>Total</td>"; 
   	$html_total .= "<td class=ac><table class=clear border=1 colspan=0 cellpadding=0 cellspacing=0><tr>$html_month</tr></table></td>"; 
   	$html_total .= "<td class=ar>". &format_number( ($data{t}{ts}/60) ,0). "</td>"; 
   	$html_total .= "</tr>"; 
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    %t = &menu_permissions_get_as_template();
	$t{my_url}	= $my_url;
    $t{title}	= "Minutes by radio";
    $t{content}	= qq[ 

		<form action=$my_url>
		Year/month: 	<select name=filter_yearmonth>	<option value=''>Select month</option>		<option value=''> </option>$filter_yearmonth_select</select> 
		<input type=submit value='Update'>
		<input type=hidden name=action value=system_reports_minutes_radio>
		</form>
		<br>

		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=600>
			<thead>
				<tr>
				<td >Radio station</td>
				<td width=50 class=ar >&nbsp;</td>
				<td width=70 class=ar >Minutes</td>
				</tr>
			</thead>
			<tbody >
				$html
			</tbody>
			<tfoot>
				$html_total
			</tfoot>
		</table>

    ];
    &template_print("template.html",%t);
}
sub do_system_reports_status(){
    #
    #-------------------------------
    # print page
    #-------------------------------
	%hash = &database_select_as_hash("SELECT c.id,c.extension,c.title,s.id,s.title FROM radio_data_station_channel as c, radio_data_station as s where s.id=c.radio_data_station_id","ext,ctitle,id,title");
	%data = &app_konference_list_summary();
	foreach $cid (keys %{$data{by_conference}}) {
		$q = $data{by_conference}{$cid}{qtd_total} || 0;
		$t = $hash{$cid}{title} || "(Unknown radio)";
		$e = $hash{$cid}{ext} || "(Unknown channel)";
		$sid = $hash{$cid}{id} || "";
		$data{by_station}{$t}{qtd_total} += $q;
		$data{by_station_and_extension}{$t}{$e}{title} = $hash{$cid}{ctitle};
		$data{by_station_and_extension}{$t}{$e}{qtd_total} += $q;
		$data{by_station_and_extension}{$t}{$e}{extension_2_channel_id} = $cid;
		$data{station_title_2_id}{$t} = $sid;
	}
	$html = "";
	$html .= "<ul>";
	foreach $t (sort{$a cmp $b} keys %{$data{by_station}}) {
		if ($data{by_station}{$t}{qtd_total} >= 1) {
			$html .= "<li>";
			$html .= "$data{by_station}{$t}{qtd_total} client(s) at radio station <a href=radio.station.cgi?action=radio_station_history&station_id=$data{station_title_2_id}{$t}>$t</a>";
			$html .= "<ul>";
			foreach $e (sort{$a <=> $b} keys %{$data{by_station_and_extension}{$t}}) {
				if ($data{by_station_and_extension}{$t}{$e}{qtd_total} >= 1) {
					$ctitle = ($data{by_station_and_extension}{$t}{$e}{title} eq "") ? "channel $e" : $data{by_station_and_extension}{$t}{$e}{title};
					$html .= "<li>$data{by_station_and_extension}{$t}{$e}{qtd_total} client(s) at <a href=radio.station.cgi?action=radio_station_now&station_id=$data{station_title_2_id}{$t}&channel_id=$data{by_station_and_extension}{$t}{$e}{extension_2_channel_id}>$ctitle</a></li>";
				}
			}
			$html .= "</ul>";
			$html .= "</li>";
		}
	}
	$html .= "</ul>";
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "System status";
    $t{content}	= qq[
		<br>
		<div class=alert_box style=width:300px;><div class=alert_box>
    	<b>Not finished yet</b>. This is basic raw data, just to give enough information to develop other tools. Real report will give more information.
		</div></div>
		<br>
		<h1>$data{qtd_total} active client(s) in this server</h1>
		$html 
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
#=======================================================
sub get_tag_list {
	%hash = database_select_as_hash("select id,title from stream_tag", 'title');
	$list = '';

	$i = 1;
	$list = "";
	for (keys %hash) {
		next if !$hash{$_}{title};
		$list .= "<td><input type=\"radio\" name=\"tag\" value=\"$hash{$_}{title}\">$hash{$_}{title}</input></td>";
		$list .= "</tr><tr>\n" if $i++ % 10 == 0;
	}
	$list = "<table><tr>$list</tr></table>" if $list;
	return $list;
}
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

