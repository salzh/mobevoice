#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_view_reports") ne 1) {adm_error("no permission"); exit;}
use Data::Dumper;
#=======================================================


#=======================================================
# main loop
#=======================================================
$my_url = "reports.cgi";
$action = $form{action};
if    ($action eq "money_overview")		{ &do_money_overview();		}
elsif ($action eq "calls_overview")		{ &do_calls_overview();		}
elsif ($action eq "calls_error")		{ &do_calls_error();		}
elsif ($action eq "calls_cdr")			{ &do_calls_cdr();			}
elsif ($action eq "calls_now")			{ &do_calls_now();			}
elsif ($action eq "calls_duration")		{ &do_calls_duration();		}
elsif ($action eq "calls_country")		{ &do_calls_country();		}
elsif ($action eq "calls_route")		{ &do_calls_route();}
elsif ($action eq "services_overview")	{ &do_services_overview();	}
elsif ($action eq "commission_contest")	{ &do_commission_contest2();	}
elsif ($action eq "history_log")		{ &do_history_log();		}
elsif ($action eq "radio_overview")		{ &do_radio_overview();		}
elsif ($action eq "radio_now")			{ &do_radio_now();			}
elsif ($action eq "radio_top_radio")	{ &do_radio_top_radio();	}
elsif ($action eq "radio_top_listen")	{ &do_radio_top_listen();	}
elsif ($action eq "radio_minutes")		{ &do_radio_minutes();		}
elsif ($action eq "sql_query")			{ &do_sql_query();			}
elsif ($action eq "commission_contest2")	{ &do_commission_contest2();	}
else									{ &do_select();				}

exit;
#=======================================================


#=======================================================
# generic SQL query
# in future, we gonna use only this reports
#=======================================================
sub do_sql_query(){
    #
    # start template
    %t = %template_base;
    $t{title} = "Reports";
    $t{breadcrumb}{1}{title}	= "Projects list";
    $t{breadcrumb}{1}{url}		= "work.cgi";
    #
    # print page
	$t{dic}{content} .= qq[
	];
	&template_print("template.html",%t);
	
}
#=======================================================



#=======================================================
# report select
#=======================================================
sub do_select(){
	#
	&cgi_redirect("index.cgi#reports");
	exit;
	#
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Reports";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "";
    $t{content}	= qq[

	
	<style>
	.local_div{
		padding:0px;
		margin:0px;
		border:0px;
		float:left; 
		margin-right:10px; 
		margin-bottom:15px;
	}
	.local_fieldset {
		margin:0px;
		padding:10px;
		width:200px;
		height:150px;
	}
	</style>
	
	<div class=local_div><fieldset class=local_fieldset><legend>Calls</legend>
		<a target=_top href="reports.cgi?action=calls_now"				>&#187; Calls sessions now</a><br>
		<a target=_top href="reports.cgi?action=calls_overview"			>&#187; Calls overview</a><br>
		<a target=_top href="reports.cgi?action=calls_error"			>&#187; Calls error</a><br>
		<a target=_top href="reports.cgi?action=calls_country"			>&#187; Calls per country</a><br>
		<a target=_top href="reports.cgi?action=calls_cdr"				>&#187; Calls CDR</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Radio</legend>
		<a target=_top href="reports.cgi?action=radio_now"		>&#187; Radio sessions now</a><br>
		<a target=_top href="reports.cgi?action=radio_overview"	>&#187; Radio overview</a><br>
		<a target=_top href="reports.cgi?action=radio_top"		>&#187; Top radios</a><br>
		<a target=_top href="reports.cgi?action=radio_cdr"		>&#187; Radio CDR</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Actions</legend>
		<a target=_top href="reports.cgi?action=history_log&display=list"	>&#187; Actions now</a><br>
		<a target=_top href="reports.cgi?action=history_log"				>&#187; Actions overview</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>System</legend>
		<a target=_top href="reports.cgi?action=services_overview"				>&#187; Services/reachrges overview</a><br>
		<a target=_top href="reports.cgi?action=commission_contest"				>&#187; Commission contest</a><br>
		<a target=_top href="index.cgi?action=set_frame&title=Servers status&url=/noc/status/">&#187; Servers status</a><br>
		<a target=_top href="reports.cgi?action=test_ney"						>&#187; Test ney</a><br>
	</fieldset></div>

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
	%t = ();
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


#=======================================================
# reports
#=======================================================
sub do_clients_export(){
	
}
sub do_services_overview_pie(){
	local (%pie) = @_;
	$pie{xml} = "<graph bgColor='ffffff' decimalPrecision='0' showPercentageValues='1' showNames='0' numberPrefix='' showValues='0' showPercentageInLabel='0' animation='0' >";
	$pie{html} = "";
	$pie{total} = 0;
	foreach $id (sort{$a <=> $b} keys %{$pie{data}}) {
		$pie{data}{$id}{value_string} 	= &format_number($pie{data}{$id}{value},0);
		$pie{xml} .= "<set name='$pie{data}{$id}{title}' color='$pie{data}{$id}{color}'	value='$pie{data}{$id}{value}' />";
		$pie{html} .= "<tr>";
		$pie{html} .= "<td bgcolor=$pie{data}{$id}{color}><img src=/design/img/spc.gif width=10 height=10 hspace=0 vspace=0 border=0></td>";
		$pie{html} .= "<td>$pie{data}{$id}{title}</td>";
		$pie{html} .= "<td class=ar>$pie{data}{$id}{value_string}</td>";
		$pie{html} .= "</tr>";
		$pie{total} += $pie{data}{$id}{value};
	}
	if ($pie{total}>0) {
		$pie{html} .= "<tr>";
		$pie{html} .= "<td>&nbsp;</td>";
		$pie{html} .= "<td>&nbsp;</td>";
		$pie{html} .= "<td class=ar style='border-top:1px solid #c0c0c0;'>".&format_number($pie{total},0)."</td>";
		$pie{html} .= "</tr>";
	}
	$pie{xml} .= "</graph>";
	return qq[
	<div class=clear style="float:left; margin-right:20px;">
	<fieldset style="background:#ffffff;width:330px;"><legend>$pie{title}</legend>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
		<td><div id="$pie{div_id}" class=clear style="padding-left:0px;">loading...</div></td>
		<td>
			<table border=0 colspan=0 cellpadding=0 cellspacing=5 class=clear>
			$pie{html}
			</table>
		</td>
		</table>
		<script type="text/javascript">
		var myChartbar = new FusionCharts("design/FusionChartsFree/Charts/FCF_Pie2D.swf ", "myChartId", "150", "150"); 
		myChartbar.setDataXML("$pie{xml}");
		myChartbar.render("$pie{div_id}");
		</script>
	</fieldset>
	</div>
	];
}
sub do_services_overview(){
	#
	#---------------------------------------
	# start
	#---------------------------------------
	%t = ();
	$html = "";
	#
	#-----------------------------------------------------------------------
	# pie 1 and 2
	#-----------------------------------------------------------------------
	$sql = "
		SELECT service_status.ui_group,count(*)
		FROM service_status,service
		where service_status.id=service.status
		group by service_status.ui_group
		order by service_status.ui_group
	";
	%hash = &database_select_as_hash($sql);
	%pie = ();
	$pie{title} = "All services";
	$pie{div_id} = "pie1";
	$pie{data}{1}{value} = $hash{"Trial"} || 0;			$pie{data}{1}{title} = "Trial";			$pie{data}{1}{color} = "#ff0000";
	$pie{data}{2}{value} = $hash{"Pay as you go"} || 0;	$pie{data}{2}{title} = "Pay as you go";	$pie{data}{2}{color} = "#ff6600";
	$pie{data}{3}{value} = $hash{"Auto recharge"} || 0;	$pie{data}{3}{title} = "Auto recharge";	$pie{data}{3}{color} = "#006f00";
	$pie{data}{4}{value} = $hash{"Disabled"} || 0;
	$pie{data}{4}{value} += $hash{"Development"} || 0;
	$pie{data}{4}{title} = "Others";		$pie{data}{4}{color} = "#c0c0c0";
	$t{dic}{content} .= &do_services_overview_pie(%pie);
	%pie = ();
	$pie{title} = "Active services";
	$pie{div_id} = "pie2";
	$pie{data}{3}{value} = $hash{"Auto recharge"} || 0;	$pie{data}{3}{title} = "Auto recharge";	$pie{data}{3}{color} = "#006f00";
	$pie{data}{2}{value} = $hash{"Pay as you go"} || 0;	$pie{data}{2}{title} = "Pay as you go";	$pie{data}{2}{color} = "#ff6600";
	$pie{data}{4}{value} = $hash{"Development"} || 0;	$pie{data}{4}{title} = "Development";	$pie{data}{4}{color} = "#c0c0c0";
	$pie{data}{1}{value} = $hash{"Disabled"} || 0;		$pie{data}{1}{title} = "Disabled";		$pie{data}{1}{color} = "#ff0000";
	$t{dic}{content} .= &do_services_overview_pie(%pie);
	#
	#-----------------------------------------------------------------------
	# pie 3
	#-----------------------------------------------------------------------
	$sql = "
		select 
		1,1,
		count(*) ,
		sum(IF(FIND_IN_SET('suspicious',service_status.tags)>0,1,0)) as a5,
		sum(IF(FIND_IN_SET('not_suspicious',service_status.tags)>0,1,0)) as a6
		from 
		service,service_status
		where 
		service.status=service_status.id
	";
	%hash = &database_select_as_hash($sql,"flag,t,s,ns");
	if ($hash{1}{flag} eq 1) {
		%hash = %{$hash{1}};
		%pie = ();
		$pie{title} = "Suspicious count";
		$pie{div_id} = "pie3";
		$pie{data}{1}{value} = $hash{"s"} || 0;						$pie{data}{1}{title} = "Suspicious";	$pie{data}{1}{color} = "#ff0000";
		$pie{data}{2}{value} = $hash{"ns"} || 0;					$pie{data}{2}{title} = "Good client";	$pie{data}{2}{color} = "#006f00";
		$pie{data}{3}{value} = $hash{"t"}-($hash{"s"}+$hash{"ns"});	$pie{data}{3}{title} = "Not tested";	$pie{data}{3}{color} = "#ff6600";
		$t{dic}{content} .= &do_services_overview_pie(%pie);
	}
	#
	#-----------------------------------------------------------------------
	# pie 4 and 5
	#-----------------------------------------------------------------------
	$sql = "
		select 
		1,1,
		count(*) ,
		sum(IF(FIND_IN_SET('with_no_calls',service_status.tags)>0,1,0)) as a5
		from 
		service,service_status
		where 
		service.status=service_status.id and FIND_IN_SET('invited',service_status.tags)>0 and creation_date < date_sub(now(),interval 90 day)
	";
	%hash = &database_select_as_hash($sql,"flag,t,c");
	%pie = ();
	$pie{title} = "Old trial services";
	$pie{div_id} = "pie4";
	$pie{data}{1}{value} = $hash{1}{"t"}-$hash{1}{"c"};	$pie{data}{1}{title} = "No call";	$pie{data}{1}{color} = "#ff0000";
	$pie{data}{2}{value} = $hash{1}{"c"} || 0;			$pie{data}{2}{title} = "with call";	$pie{data}{2}{color} = "#006f00";
	$t{dic}{content} .= &do_services_overview_pie(%pie);
	$sql = "
		select 
		1,1,
		count(*) ,
		sum(IF(FIND_IN_SET('with_no_calls',service_status.tags)>0,1,0)) as a5
		from 
		service,service_status
		where 
		service.status=service_status.id and FIND_IN_SET('invited',service_status.tags)>0 and creation_date >= date_sub(now(),interval 90 day)
	";
	%hash = &database_select_as_hash($sql,"flag,t,c");
	%pie = ();
	$pie{title} = "Recent trial services";
	$pie{div_id} = "pie5";
	$pie{data}{1}{value} = $hash{1}{"t"}-$hash{1}{"c"};	$pie{data}{1}{title} = "No call";	$pie{data}{1}{color} = "#ff0000";
	$pie{data}{2}{value} = $hash{1}{"c"} || 0;			$pie{data}{2}{title} = "with call";	$pie{data}{2}{color} = "#006f00";
	$t{dic}{content} .= &do_services_overview_pie(%pie);
	#	
	#==========================================
	# plota signin
	#==========================================
	%data = ();
	%plot = ();
	%hash = ();
	$sql = "
		SELECT 
		type,DATE_FORMAT(date,'\%Y-\%m-\%d'),count(*)
		from action_log
		where date >date_sub(now(),interval 60 day) and (type = 'status:new' or type = 'status:first_call' or type = 'status:first_recharge') 
		group by type,DATE_FORMAT(date,'\%Y-\%m-\%d')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"t,d,v");
	foreach $k (keys %hash) { $data{$hash{$k}{d}}{$hash{$k}{t}} += $hash{$k}{v}; }
	$plot{uid} = "signindays";
	$plot{x} = 450;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "Sign-in";
	$plot{series}{1}{color} = "ff6600";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{"status:new"};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>30) {last}
	}
	%plot = &plot_lines(%plot);
	$plot_signin_days = $plot{html};
	%data = ();
	%plot = ();
	%hash = ();
	$sql = "
		SELECT 
		type,DATE_FORMAT(date,'\%Y-\%m'),count(*)
		from action_log
		where date >date_sub(now(),interval 900 day) and (type = 'status:new' or type = 'status:first_call' or type = 'status:first_recharge') 
		group by type,DATE_FORMAT(date,'\%Y-\%m')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"t,d,v");
	foreach $k (keys %hash) { $data{$hash{$k}{d}}{$hash{$k}{t}} += $hash{$k}{v}; }
	$plot{uid} = "signinmonths";
	$plot{x} = 250;
	$plot{y} = 255;
	$plot{series}{1}{name} 	= "Sign-in";
	$plot{series}{1}{color} = "ff6600";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{"status:new"};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_lines(%plot);
	$plot_signin_months = $plot{html};
	#	
	#==========================================
	# plota new clients
	#==========================================
	%data = ();
	%plot = ();
	%hash = ();
	$sql = "
		SELECT 
		type,DATE_FORMAT(date,'\%Y-\%m-\%d'),count(*)
		from action_log
		where date >date_sub(now(),interval 60 day) and (type = 'status:new' or type = 'status:first_call' or type = 'status:first_recharge') 
		group by type,DATE_FORMAT(date,'\%Y-\%m-\%d')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"t,d,v");
	foreach $k (keys %hash) { $data{$hash{$k}{d}}{$hash{$k}{t}} += $hash{$k}{v}; }
	$plot{uid} = "actionsdays";
	$plot{x} = 450;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "First call";
	$plot{series}{1}{color} = "f8d322";
	$plot{series}{2}{name} 	= "First recharge";
	$plot{series}{2}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{"status:first_call"};
		$plot{data}{$slice_index}{2} += $data{$slice}{"status:first_recharge"};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>30) {last}
	}
	%plot = &plot_lines(%plot);
	$plot_firstactions_days = $plot{html};
	%data = ();
	%plot = ();
	%hash = ();
	$sql = "
		SELECT 
		type,DATE_FORMAT(date,'\%Y-\%m'),count(*)
		from action_log
		where date >date_sub(now(),interval 900 day) and (type = 'status:new' or type = 'status:first_call' or type = 'status:first_recharge') 
		group by type,DATE_FORMAT(date,'\%Y-\%m')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"t,d,v");
	foreach $k (keys %hash) { $data{$hash{$k}{d}}{$hash{$k}{t}} += $hash{$k}{v}; }
	$plot{uid} = "actionsmonths";
	$plot{x} = 250;
	$plot{y} = 255;
	$plot{series}{1}{name} 	= "First call";
	$plot{series}{1}{color} = "f8d322";
	$plot{series}{2}{name} 	= "First recharge";
	$plot{series}{2}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{"status:first_call"};
		$plot{data}{$slice_index}{2} += $data{$slice}{"status:first_recharge"};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_lines(%plot);
	$plot_firstactions_months = $plot{html};
	#	
	#==========================================
	# plota recharges 
	#==========================================
	%data = ();
	%plot = ();
	%hash = ();
	$sql = "
		SELECT 
		credit_type,DATE_FORMAT(date,'\%Y-\%m-\%d'),sum(credit)
		from credit 
		where date >date_sub(now(),interval 70 day) and status=1
		group by credit_type,DATE_FORMAT(date,'\%Y-\%m-\%d')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"t,d,v");
	foreach $k (keys %hash) { $data{$hash{$k}{d}}{$hash{$k}{t}} += $hash{$k}{v}; }
	$plot{uid} = "rechargesdays";
	$plot{x} = 450;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "Auto recharge";
	$plot{series}{1}{color} = "ff6600";
	$plot{series}{2}{name} 	= "Pay as you go";
	$plot{series}{2}{color} = "f8d322";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{"AUTHORIZE_ACIM"};
		$plot{data}{$slice_index}{2} += $data{$slice}{"AUTHORIZE_CIM"}+$data{$slice}{"AUTHORIZE_CC"};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>30) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_recharges_days = $plot{html};
	%data = ();
	%plot = ();
	%hash = ();
	$sql = "
		SELECT 
		credit_type,DATE_FORMAT(date,'\%Y-\%m'),sum(credit)
		from credit 
		where date >date_sub(now(),interval 900 day) and status=1 
		group by credit_type,DATE_FORMAT(date,'\%Y-\%m')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"t,d,v");
	foreach $k (keys %hash) { $data{$hash{$k}{d}}{$hash{$k}{t}} += $hash{$k}{v}; }
	$plot{uid} = "rechargesmonths";
	$plot{x} = 250;
	$plot{y} = 255;
	$plot{series}{1}{name} 	= "Auto recharge";
	$plot{series}{1}{color} = "ff6600";
	$plot{series}{2}{name} 	= "Pay as you go";
	$plot{series}{2}{color} = "f8d322";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{"AUTHORIZE_ACIM"};
		$plot{data}{$slice_index}{2} += $data{$slice}{"AUTHORIZE_CIM"}+$data{$slice}{"AUTHORIZE_CC"};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_recharges_months = $plot{html};
	#	
	#==========================================
	# plota free
	#==========================================
	%data = ();
	%plot = ();
	%hash = ();
	$sql = "
		SELECT 
		credit_type,DATE_FORMAT(date,'\%Y-\%m-\%d'),sum(credit)
		from credit 
		where date >date_sub(now(),interval 70 day) and status=1 
		group by credit_type,DATE_FORMAT(date,'\%Y-\%m-\%d')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"t,d,v");
	foreach $k (keys %hash) { $data{$hash{$k}{d}}{$hash{$k}{t}} += $hash{$k}{v}; }
	$plot{uid} = "freedays";
	$plot{x} = 450;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "Cash";
	$plot{series}{1}{color} = "ff6600";
	$plot{series}{2}{name} 	= "free";
	$plot{series}{2}{color} = "f8d322";
	$plot{series}{3}{name} 	= "Commission";
	$plot{series}{3}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{"CASH"};
		$plot{data}{$slice_index}{2} += $data{$slice}{"FREE"};
		$plot{data}{$slice_index}{3} += $data{$slice}{"COMMISSION_CRED"};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>30) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_free_days = $plot{html};
	%data = ();
	%plot = ();
	%hash = ();
	$sql = "
		SELECT 
		credit_type,DATE_FORMAT(date,'\%Y-\%m'),sum(credit)
		from credit 
		where date >date_sub(now(),interval 900 day) and status=1 
		group by credit_type,DATE_FORMAT(date,'\%Y-\%m')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"t,d,v");
	foreach $k (keys %hash) { $data{$hash{$k}{d}}{$hash{$k}{t}} += $hash{$k}{v}; }
	$plot{uid} = "freemonths";
	$plot{x} = 250;
	$plot{y} = 255;
	$plot{series}{1}{name} 	= "Cash";
	$plot{series}{1}{color} = "ff6600";
	$plot{series}{2}{name} 	= "free";
	$plot{series}{2}{color} = "f8d322";
	$plot{series}{3}{name} 	= "Commission";
	$plot{series}{3}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{"CASH"};
		$plot{data}{$slice_index}{2} += $data{$slice}{"FREE"};
		$plot{data}{$slice_index}{3} += $data{$slice}{"COMMISSION_CRED"};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_free_months = $plot{html};
	#
	#---------------------------------------
	# print
	#---------------------------------------
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Services/recharges overview";
	$t{dic}{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>


	<fieldset style="width:730px;"><legend>clients first actions</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_firstactions_days</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_firstactions_months</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Clients Sign-in</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_signin_days</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_signin_months</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Credit-card recharges</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_recharges_days</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_recharges_months</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Other recharges</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_free_days</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_free_months</td>
	</table>
	</fieldset>
	<br>

	<div style="width:800px;">$t{dic}{content}</div>

	];
	&template_print("template.html",%t);



}
sub OLD_do_services_overview(){
	#
	#---------------------------------------
	# totais
	#---------------------------------------
	%data = ();
	$sql = "
		select 
			1,1,
			count(*) ,
			sum(IF(FIND_IN_SET('active',service_status.tags)>0,1,0)) as a1,
			sum(IF(FIND_IN_SET('invited',service_status.tags)>0,1,0)) as a2,
			sum(IF(FIND_IN_SET('disabled',service_status.tags)>0,1,0)) as a3,
			sum(IF(FIND_IN_SET('deleted',service_status.tags)>0,1,0)) as a4,
			sum(IF(FIND_IN_SET('suspicious',service_status.tags)>0,1,0)) as a5,
			sum(IF(FIND_IN_SET('not_suspicious',service_status.tags)>0,1,0)) as a6
		from 
			service,service_status
		where 
			service.status=service_status.id
	";
	%hash = &database_select_as_hash($sql,"flag,total,active,invited,disabled,deleted,suspicious,not_suspicious");
	if ($hash{1}{flag} eq 1){
		%data = %{$hash{1}};
		#
		#-----------------------------------------------------------------------
		# subtract auto recharges
		#-----------------------------------------------------------------------
		$sql = "
		select 
			1,1,
			count(*) ,
			sum(IF(FIND_IN_SET('active',service_status.tags)>0,1,0)) as a1,
			sum(IF(FIND_IN_SET('invited',service_status.tags)>0,1,0)) as a2,
			sum(IF(FIND_IN_SET('disabled',service_status.tags)>0,1,0)) as a3
		from 
			service,service_status,service_profile_cc
		where 
			service.status=service_status.id
			and service_profile_cc.service_id = service.id
			and service_profile_cc.active=1
			and service_profile_cc.is_auto_recharge=1
		";
		%hash = &database_select_as_hash($sql,"flag,qtd,active,invited,disabled");
		$data{auto} = 0;
		if ($hash{1}{flag} eq 1){
			if ($hash{1}{qtd} eq $hash{1}{active}+$hash{1}{invited}+$hash{1}{disabled}){
				$data{auto} = $hash{1}{qtd};
				$data{active} -= $hash{1}{active};
				$data{invited} -= $hash{1}{invited};
				$data{disabled} -= $hash{1}{disabled};
			}
		}
		#
		#-----------------------------------------------------------------------
		# pie 1
		#-----------------------------------------------------------------------
		%pie = ();
		$pie{title} = "Services by type";
		$pie{div_id} = "pie1";
		$pie{data}{1}{value} = $data{invited};	$pie{data}{1}{title} = "Trial";			$pie{data}{1}{color} = "#ff0000";
		$pie{data}{2}{value} = $data{active};	$pie{data}{2}{title} = "Pay as you go";	$pie{data}{2}{color} = "#ff6600";
		$pie{data}{3}{value} = $data{auto};		$pie{data}{3}{title} = "Auto recharge";	$pie{data}{3}{color} = "#006f00";
		$pie{data}{4}{value} = $data{disabled};	$pie{data}{4}{title} = "Disabled";		$pie{data}{4}{color} = "#c0c0c0";
		$t{dic}{content} .= &do_services_overview_pie(%pie);
		#
		#-----------------------------------------------------------------------
		# pie 2
		#-----------------------------------------------------------------------
		%pie = ();
		$pie{title} = "Services by suspicious";
		$pie{div_id} = "pie2";
		$pie{data}{1}{value} = $data{suspicious};
		$pie{data}{2}{value} = $data{not_suspicious};
		$pie{data}{3}{value} = ($data{active}+$data{invited})-($data{not_suspicious}+$data{suspicious});
		$pie{data}{3}{value} = ($pie{data}{3}{value}<0) ? 0 : $pie{data}{3}{value};
		$pie{data}{1}{color}	= "#ff0000";
		$pie{data}{2}{color}	= "#006f00";
		$pie{data}{3}{color}	= "#c0c0c0";
		$pie{data}{1}{title}	= "Suspicious";
		$pie{data}{2}{title}	= "Good client";
		$pie{data}{3}{title}	= "Unknown";
		$t{dic}{content} .= &do_services_overview_pie(%pie);
	}
	#
	#==========================================
	# trial services history
	#==========================================
	# LAST 12 MONTHS
	%plot = ();
	$plot{uid} = "t12m";
	$plot{x} = 200;
	$plot{y} = 170;
	$plot{series}{1}{name} 	= "Trial";
	$plot{series}{1}{color} = "f8d322";
	@month_names = qw (Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
	%data = ();
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m'),count(*)
		from action_log
		where date>date_sub(now(),interval 400 day) 
		and type='status:new' 
		group by DATE_FORMAT(date,'\%Y\%m')
		order by DATE_FORMAT(date,'\%Y\%m') desc
		limit 0,12
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{1} += $hash{$id}{value}; }
	$slice_index = 1;
	foreach $slice (sort{$a <=> $b} keys %data) {
		$month_number = substr($slice,4,2); $month_number++; $month_number--; $month_number--;
		$month_string = (@month_names)[$month_number];
		$month_string = ($month_string eq "") ? $month_number : $month_string;
		$plot{data}{$slice_index}{1} += $data{$slice}{1};
		$plot{slices}{$slice_index} = $month_string;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_lines(%plot);
	$html_trial_12months = $plot{html};
	# LAST 60 DAYS
	%plot = ();
	$plot{uid} = "t60d";
	$plot{x} = 470;
	$plot{y} = 170;
	$plot{series}{1}{name} 	= "Trial";
	$plot{series}{1}{color} = "f8d322";
	%data = ();
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m\%d'),count(*)
		from action_log
		where date>date_sub(now(),interval 70 day) 
		and type='status:new' 
		group by DATE_FORMAT(date,'\%Y\%m\%d')
		order by DATE_FORMAT(date,'\%Y\%m\&d') desc
		limit 0,60
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{1} += $hash{$id}{value}; }
	# TODO: apaga o que nao é 12 mais recentes
	$slice_index = 1;
	foreach $slice (sort{$a <=> $b} keys %data) {
		$day_string = substr($slice,6,2);
		$day_string++;
		$day_string--;
		$plot{data}{$slice_index}{1} += $data{$slice}{1};
		$plot{slices}{$slice_index} = $day_string;
		$slice_index++;
		if ($slice_index>61) {last}
	}
	%plot = &plot_lines(%plot);
	$html_trial_60days = $plot{html};
	#
	#==========================================
	# active history
	#==========================================
	# LAST 12 MONTHS
	%plot = ();
	$plot{uid} = "a12m";
	$plot{x} = 200;
	$plot{y} = 170;
	$plot{series}{1}{name} 	= "Auto recharge";
	$plot{series}{1}{color} = "006f00";
	$plot{series}{2}{name} 	= "Pay as you go";
	$plot{series}{2}{color} = "ff6600";
	@month_names = qw (Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
	%data = ();
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m'),count(*)
		from action_log
		where date>date_sub(now(),interval 400 day) 
		and type='status:first_recharge' 
		group by DATE_FORMAT(date,'\%Y\%m')
		order by DATE_FORMAT(date,'\%Y\%m') desc
		limit 0,12
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{2} += $hash{$id}{value}; }
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m'),count(*)
		from action_log
		where date>date_sub(now(),interval 400 day) 
		and type='ar:status:on' 
		group by DATE_FORMAT(date,'\%Y\%m')
		order by DATE_FORMAT(date,'\%Y\%m') desc
		limit 0,12
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{1} += $hash{$id}{value}; }
	# TODO: apaga o que nao é 12 mais recentes
	$slice_index = 1;
	foreach $slice (sort{$a <=> $b} keys %data) {
		$month_number = substr($slice,4,2); $month_number++; $month_number--; $month_number--;
		$month_string = (@month_names)[$month_number];
		$month_string = ($month_string eq "") ? $month_number : $month_string;
		$plot{data}{$slice_index}{1} += $data{$slice}{1};
		$plot{data}{$slice_index}{2} += $data{$slice}{2};
		$plot{slices}{$slice_index} = $month_string;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_lines(%plot);
	$html_active_12months = $plot{html};
	# LAST 60 DAYS
	%plot = ();
	$plot{uid} = "a60d";
	$plot{x} = 470;
	$plot{y} = 170;
	$plot{series}{1}{name} 	= "Auto recharge";
	$plot{series}{1}{color} = "006f00";
	$plot{series}{2}{name} 	= "Pay as you go";
	$plot{series}{2}{color} = "ff6600";
	%data = ();
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m\%d'),count(*)
		from action_log
		where date>date_sub(now(),interval 70 day) 
		and type='status:first_recharge' 
		group by DATE_FORMAT(date,'\%Y\%m\%d')
		order by DATE_FORMAT(date,'\%Y\%m\&d') desc
		limit 0,60
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{2} += $hash{$id}{value}; }
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m\%d'),count(*)
		from action_log
		where date>date_sub(now(),interval 70 day) 
		and type='ar:status:on' 
		group by DATE_FORMAT(date,'\%Y\%m\%d')
		order by DATE_FORMAT(date,'\%Y\%m\&d') desc
		limit 0,60
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{1} += $hash{$id}{value}; }
	# TODO: apaga o que nao é 12 mais recentes
	$slice_index = 1;
	foreach $slice (sort{$a <=> $b} keys %data) {
		$day_string = substr($slice,6,2);
		$day_string++;
		$day_string--;
		$plot{data}{$slice_index}{1} += $data{$slice}{1};
		$plot{data}{$slice_index}{2} += $data{$slice}{2};
		$plot{slices}{$slice_index} = $day_string;
		$slice_index++;
		if ($slice_index>61) {last}
	}
	%plot = &plot_lines(%plot);
	$html_active_60days = $plot{html};
	#
	#==========================================
	# disabled history
	#==========================================
	# LAST 12 MONTHS
	%plot = ();
	$plot{uid} = "d12m";
	$plot{x} = 200;
	$plot{y} = 170;
	$plot{series}{1}{name} 	= "Disabled";
	$plot{series}{1}{color} = "c0c0c0";
	@month_names = qw (Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
	%data = ();
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m'),count(*)
		from action_log
		where date>date_sub(now(),interval 400 day) 
		and type='noc:service:status:change' and value_new like '%disabled%'  
		group by DATE_FORMAT(date,'\%Y\%m')
		order by DATE_FORMAT(date,'\%Y\%m') desc
		limit 0,12
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{1} += $hash{$id}{value}; }
	# TODO: apaga o que nao é 12 mais recentes
	$slice_index = 1;
	foreach $slice (sort{$a <=> $b} keys %data) {
		$month_number = substr($slice,4,2); $month_number++; $month_number--; $month_number--;
		$month_string = (@month_names)[$month_number];
		$month_string = ($month_string eq "") ? $month_number : $month_string;
		$plot{data}{$slice_index}{1} += $data{$slice}{1};
		$plot{slices}{$slice_index} = $month_string;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_lines(%plot);
	$html_disable_12months = $plot{html};
	# LAST 60 DAYS
	%plot = ();
	$plot{uid} = "d60d";
	$plot{x} = 470;
	$plot{y} = 170;
	$plot{series}{1}{name} 	= "Disabled";
	$plot{series}{1}{color} = "c0c0c0";
	%data = ();
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m\%d'),count(*)
		from action_log
		where date>date_sub(now(),interval 70 day) 
		and type='noc:service:status:change' and value_new like '%disabled%'  
		group by DATE_FORMAT(date,'\%Y\%m\%d')
		order by DATE_FORMAT(date,'\%Y\%m\&d') desc
		limit 0,60
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{1} += $hash{$id}{value}; }
	# TODO: apaga o que nao é 12 mais recentes
	$slice_index = 1;
	foreach $slice (sort{$a <=> $b} keys %data) {
		$day_string = substr($slice,6,2);
		$day_string++;
		$day_string--;
		$plot{data}{$slice_index}{1} += $data{$slice}{1};
		$plot{slices}{$slice_index} = $day_string;
		$slice_index++;
		if ($slice_index>61) {last}
	}
	%plot = &plot_lines(%plot);
	$html_disable_60days = $plot{html};
	#
	#---------------------------------------
	# print
	#---------------------------------------
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Services overview";
	$t{dic}{content} = qq[
		<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>


		$t{dic}{content}
	<br clear=both>
	<br>

	<fieldset style="width:700px;"><legend>Active services</legend>
	Active services from last 12 months and last 60 days<br>
	<br>
	<div class=clear style='float:left; margin-right:20px;'>$html_active_12months</div>
	<div class=clear style='float:left; '>$html_active_60days</div>
	<br clear=both>	
	</fieldset>
	<br>

	<fieldset style="width:700px;"><legend>Trial services</legend>
	Trial services from last 12 months and last 60 days<br>
	<br>
	<div class=clear style='float:left; margin-right:20px;'>$html_trial_12months</div>
	<div class=clear style='float:left; '>$html_trial_60days</div>
	<br clear=both>	
	</fieldset>
	<br>

	<fieldset style="width:700px;"><legend>Disabled services</legend>
	Disabled services from last 12 months and last 60 days<br>
	<br>
	<div class=clear style='float:left; margin-right:20px;'>$html_disable_12months</div>
	<div class=clear style='float:left; '>$html_disable_60days</div>
	<br clear=both>	
	</fieldset>
	<br>


	];
	&template_print("template.html",%t);
}
sub do_money_overview(){
	#
	#---------------------------------------
	# start
	#---------------------------------------
	%t = ();
	#
	#---------------------------------------
	# html_money_by_status
	#---------------------------------------
	%data = ();
	$html = "";
	$sql = "
		select 
			service_status.name,
			count(*),
			sum(credit.credit),
			sum(credit.value)
		from 
			credit,
			service,
			service_status
		where  
			credit.service_id = service.id
			and service.status = service_status.id
		group by service_status.name
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"index,count,credit,value");
	foreach $id (keys %hash) {
		$index = $hash{$id}{index};
		$data{$index}{cred_count}		+= $hash{$id}{count};
		$data{$index}{cred_recharge}	+= $hash{$id}{credit};
		$data{$index}{cred_value}		+= $hash{$id}{value};
	}
	$sql = "
		select 
			service_status.name,
			count(*),
			sum(service.balance-service.limit)
		from 
			service,
			service_status
		where  
			service.status = service_status.id
		group by service_status.name
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"index,count,balance");
	foreach $id (keys %hash) {
		$index = $hash{$id}{index};
		$data{$index}{services_count}	+= $hash{$id}{count};
		$data{$index}{services_balance}	+= $hash{$id}{balance};
	}
	$sql = "
		select 
			service_status.name,
			count(*),
			sum(calls.seconds),
			sum(calls.value)
		from 
			calls,
			service,
			service_status
		where  
			calls.service_id = service.id
			and service.status = service_status.id
		group by service_status.name
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"index,count,seconds,value");
	foreach $id (keys %hash) {
		$index = $hash{$id}{index};
		$data{$index}{calls_count}	+= $hash{$id}{count};
		$data{$index}{calls_seconds}	+= $hash{$id}{seconds};
		$data{$index}{calls_value}	+= $hash{$id}{value};
	}
	%tot = ();
	foreach $index (sort{$a cmp $b} keys %data) {
		$html .= "<tr>";
		$html .= "<td class=al>$index</a>";
		$html .= "<td class=ar>".&format_number($data{$index}{services_count},0)."</a>";
		$html .= "<td class=ar>\$".&format_number($data{$index}{cred_value},2)."</a>";
		$html .= "<td class=ar>\$".&format_number(($data{$index}{cred_recharge}-$data{$index}{cred_value}),2)."</a>";
		#$html .= "<td class=ar>\$".&format_number($data{$index}{cred_recharge},2)."</a>";
		#$html .= "<td class=ar>".&format_number($data{$index}{calls_count},0)."</a>";
		#$html .= "<td class=ar>".&format_number(($data{$index}{calls_seconds}/60),0)."</a>";
		$html .= "<td class=ar>\$".&format_number($data{$index}{calls_value},2)."</a>";
		$tmp_1 = $data{$index}{cred_value}-$data{$index}{calls_value};
		$tmp_2 = ($tmp_1<0) ? "style=color:red" : "";
		$html .= "<td class=ar $tmp_2>\$".&format_number($tmp_1,2)."</a>";
		$tmp_1 = $data{$index}{cred_recharge}-$data{$index}{calls_value};
		$tmp_2 = ($tmp_1<0) ? "style=color:red" : "";
		$html .= "<td class=ar $tmp_2>\$".&format_number($tmp_1,2)."</a>";
		$tmp_1 = $data{$index}{cred_recharge}-$data{$index}{calls_value};
		$tmp_1 = $tmp_1 - $data{$index}{services_balance};
		$tmp_2 = ($tmp_1<0) ? "style=color:red" : "";
		$html .= "<td class=ar $tmp_2>\$".&format_number($data{$index}{services_balance},2)."</a>";
		$html .= "<tr>";
		$tot{1} += $data{$index}{services_count};
		$tot{2} += $data{$index}{cred_value};
		$tot{3} += ($data{$index}{cred_recharge}-$data{$index}{cred_value});
		$tot{4} += $data{$index}{cred_recharge};
		$tot{5} += $data{$index}{calls_count};
		$tot{6} += $data{$index}{calls_seconds};
		$tot{7} += $data{$index}{calls_value};
		$tot{8} += ($data{$index}{cred_value}-$data{$index}{calls_value});
		$tot{9} += ($data{$index}{cred_recharge}-$data{$index}{calls_value});
		$tot{10} += $data{$index}{services_balance};
	}
	$html_money_by_status = $html;
	$html = "";
	if ($html_money_by_status ne "") {
		$html .= "<tr>";
		$html .= "<td class=al>TOTAL</a>";
		$html .= "<td class=ar>".&format_number($tot{1},0)."</a>";
		$html .= "<td class=ar>\$".&format_number($tot{2},2)."</a>";
		$html .= "<td class=ar>\$".&format_number($tot{3},2)."</a>";
		#$html .= "<td class=ar>\$".&format_number($tot{4},2)."</a>";
		#$html .= "<td class=ar>".&format_number($tot{5},0)."</a>";
		#$html .= "<td class=ar>".&format_number(($tot{6}/60),0)."</a>";
		$html .= "<td class=ar>\$".&format_number($tot{7},2)."</a>";
		$tmp_1 = $tot{8};
		$tmp_2 = ($tmp_1<0) ? "style=color:red" : "";
		$html .= "<td class=ar $tmp_2>\$".&format_number($tmp_1,2)."</a>";
		$tmp_1 = $tot{9};
		$tmp_2 = ($tmp_1<0) ? "style=color:red" : "";
		$html .= "<td class=ar $tmp_2>\$".&format_number($tmp_1,2)."</a>";
		$tmp_1 = ($tot{4}-$tot{7})-$tot{10};
		$tmp_2 = ($tmp_1<0) ? "style=color:red" : "";
		$html .= "<td class=ar $tmp_2>\$".&format_number($tot{10},2)."</a>";
		$html .= "<tr>";
	}
	$html_money_by_status_total = $html;
	#
	#---------------------------------------
	# html_money_in_out_month
	#---------------------------------------
	%data = ();
	$html = "";
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m'),count(*),sum(credit),sum(value) 
		from credit
		where  date>date_sub(now(),interval 400 day) and status=1
		group by DATE_FORMAT(date,'\%Y\%m')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"date,count,credit,value");
	foreach $id (keys %hash) {
		$date = $hash{$id}{date};
		$data{$date}{cred_count}	+= $hash{$id}{count};
		$data{$date}{cred_recharge}	+= $hash{$id}{credit};
		$data{$date}{cred_value}	+= $hash{$id}{value};
	}
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m'),count(*),sum(seconds),sum(value) 
		from calls
		where  date>date_sub(now(),interval 400 day) 
		group by DATE_FORMAT(date,'\%Y\%m')
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"date,count,seconds,value");
	foreach $id (keys %hash) {
		$date = $hash{$id}{date};
		$data{$date}{calls_count}	+= $hash{$id}{count};
		$data{$date}{calls_seconds}	+= $hash{$id}{seconds};
		$data{$date}{calls_value}	+= $hash{$id}{value};
	}
	foreach $date (sort{$a <=> $b} keys %data) {
		$html .= "<tr>";
		$html .= "<td class=al>".substr($date,0,4)." - ".substr($date,4,2)."</a>";
		$html .= "<td class=ar>".&format_number($data{$date}{cred_count},0)."</a>";
		$html .= "<td class=ar>\$".&format_number($data{$date}{cred_value},2)."</a>";
		$html .= "<td class=ar>\$".&format_number(($data{$date}{cred_recharge}-$data{$date}{cred_value}),2)."</a>";
		$html .= "<td class=ar>\$".&format_number($data{$date}{cred_recharge},2)."</a>";
		$html .= "<td class=ar>".&format_number($data{$date}{calls_count},0)."</a>";
		$html .= "<td class=ar>".&format_number(($data{$date}{calls_seconds}/60),0)."</a>";
		$html .= "<td class=ar>\$".&format_number($data{$date}{calls_value},2)."</a>";
		$tmp_1 = $data{$date}{cred_value}-$data{$date}{calls_value};
		$tmp_2 = ($tmp_1<0) ? "style=color:red" : "";
		$html .= "<td class=ar $tmp_2>\$".&format_number($tmp_1,2)."</a>";
		$tmp_1 = $data{$date}{cred_recharge}-$data{$date}{calls_value};
		$tmp_2 = ($tmp_1<0) ? "style=color:red" : "";
		$html .= "<td class=ar $tmp_2>\$".&format_number($tmp_1,2)."</a>";
		$html .= "<tr>";
	}
	$html_money_in_out_month = $html;
	#
	#---------------------------------------
	# print
	#---------------------------------------
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Money overview";
	$t{dic}{content} .= qq[

		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% onclick="sortColumn(event)">
			<thead>
				<tr>
					<td colspan=11><h1>Money overview by services status</h1></td>
				</tr>
				<tr>
					<td rowspan=2>Service status</td>
					<td rowspan=2>Services</td>
					<td colspan=2>Credits</td>
					<td rowspan=2>Calls<br>value <font size=1 color=#808080>(C)</font></td>
					<td rowspan=2>ZenoFon<br>balance<br><font size=1 color=#808080>(A-C)</font></td>
					<td rowspan=2>Credits<br>not used<br><font size=1 color=#808080>((A+B)-C)</font></td>
					<td rowspan=2>Services<br>balance</td>
				</tr>
				<tr>
					<td>Money in <font size=1 color=#808080>(A)</font></td>
					<td>Free <font size=1 color=#808080>(B)</td>
				</tr>
			</thead>
			<tbody>
			$html_money_by_status
			</tbody>
			<tfoot>
			$html_money_by_status_total 
			</tfoot>
		</table>
		<br><br>


		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% onclick="sortColumn(event)">
			<thead>
				<tr>
					<td colspan=10><h1>Money in and out by month</h1></td>
				</tr>
				<tr>
					<td rowspan=2>Year / month</td>
					<td colspan=4>Credits</td>
					<td colspan=3>Calls</td>
					<td rowspan=2>ZenoFon<br>balance<br><font size=1 color=#808080>(A-C)</font></td>
					<td rowspan=2>Credits<br>not used<br><font size=1 color=#808080>(B-C)</font></td>
				</tr>
				<tr>
					<td>Quantity</td>
					<td>Money in <font size=1 color=#808080>(A)</font></td>
					<td>Free</td>
					<td>Total <font size=1 color=#808080>(B)</font></td>
					<td>Quantity</td>
					<td>Minutes</td>
					<td>Value <font size=1 color=#808080>(C)</font></td>
				</tr>
			</thead>
			<tbody>
			$html_money_in_out_month
			</tbody>
		</table>

	];
	&template_print("template.html",%t);
}
sub do_calls_overview_old(){
	#
	#==========================================
	# start
	#==========================================
	%t = ();
	#
	#==========================================
	# Bad calls
	#==========================================
	%data = ();
	$data_days = 7;
	$data_dst_lenth = 5;
	$html = "";
	#--------------------------
	# pega no connection
	#--------------------------
	$sql = "
		select left(dst,$data_dst_lenth),count(*)
		from calls_log
		where 
		billing_id is null and 
		service_id is not null and 
		dst <> '' and 
		error_id is null and
		datetime_start>date_sub(now(),interval $data_days day) 
		group by left(dst,$data_dst_lenth)
		order by count(*) desc
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"code,count");
	foreach $id (keys %hash) {
		$data{codes}{$hash{$id}{code}}{count_error}	+= $hash{$id}{count};
		$data{codes}{$hash{$id}{code}}{country}	= "";
	}
	#--------------------------
	# pega low seconds
	#--------------------------
	$sql = "
		select left(dst,$data_dst_lenth),count(*)
		from calls
		where 
		date>date_sub(now(),interval $data_days  day) and seconds<5
		group by left(dst,$data_dst_lenth)
		order by count(*) desc
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"code,count");
	foreach $id (keys %hash) {
		$data{codes}{$hash{$id}{code}}{count_error}	+= $hash{$id}{count};
		$data{codes}{$hash{$id}{code}}{country}	= "";
	}
	#--------------------------
	# pega count_ok
	#--------------------------
	$sql = "
		select left(dst,$data_dst_lenth),count(*)
		from calls
		where 
		date>date_sub(now(),interval $data_days  day) and seconds>=5
		group by left(dst,$data_dst_lenth)
		order by count(*) desc
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"code,count");
	foreach $id (keys %hash) {
		#unless(exists($data{code}{$hash{$id}{code}})) {next}
		$data{codes}{$hash{$id}{code}}{count_ok}	+= $hash{$id}{count};
	}
	#--------------------------
	# calc country
	#--------------------------
	%country_names = &database_select_as_hash("SELECT code,name FROM country");
	$country_codes_buf = "|".join("|",(keys %country_names))."|";
	foreach $code (keys %{$data{codes}}) {
		$country = "(UNKNOWN)";
		foreach $size (1..4){
			$sub_code = substr($code,0,$size);
			if (index($country_codes_buf,"|$sub_code|") eq -1) {next}
			unless (exists($country_names{$sub_code})) {next}
			$country = $country_names{$sub_code};
		}
		$data{codes}{$code}{country} = $country;
		$data{country}{$country}{count_error} += $data{codes}{$code}{count_error};
		$data{country}{$country}{count_ok} += $data{codes}{$code}{count_ok};
	}
	#--------------------------
	# delete zero errors and calc percentage
	#--------------------------
	foreach $country (keys %{$data{country}}) {		
		if ( ($data{country}{$country}{count_error}>0) && ($data{country}{$country}{count_ok}>0) && (($data{country}{$country}{count_error}+$data{country}{$country}{count_ok})>10) ){
			$p = $data{country}{$country}{count_error}/($data{country}{$country}{count_error}+$data{country}{$country}{count_ok});
			$data{country}{$country}{percent_error} = int($p*100);
		} else {
			delete $data{country}{$country};
		}
	}
	foreach $code (keys %{$data{codes}}) {		
		if ( ($data{codes}{$code}{count_error}>0) && ($data{codes}{$code}{count_ok}>0) && (($data{codes}{$code}{count_error}+$data{codes}{$code}{count_ok})>10) ){
			$p = $data{codes}{$code}{count_error}/($data{codes}{$code}{count_error}+$data{codes}{$code}{count_ok});
			$data{codes}{$code}{percent_error} = int($p*100);
		} else {
			delete $data{codes}{$code};
		}
	}
	#--------------------------
	# html country
	#--------------------------
	$html = "";
	foreach $country (sort{$data{country}{$b}{percent_error} <=> $data{country}{$a}{percent_error}} keys %{$data{country}}) {
		$html .= "<tr>";
		$html .= "<td class=al>$country</a>";
		$html .= "<td class=ar>".&format_number($data{country}{$country}{count_ok},0)."</td>";
		$html .= "<td class=ar>".&format_number($data{country}{$country}{count_error},0)."</td>";
		$html .= "<td class=ar>$data{country}{$country}{percent_error}\%</td>";
		$html .= "<tr>";
	}
	$html_bad_calls_country = $html;
	#--------------------------
	# html areacodes
	#--------------------------
	$html = "";
	foreach $code (sort{$data{codes}{$b}{percent_error} <=> $data{codes}{$a}{percent_error}} keys %{$data{codes}}) {
		$html .= "<tr>";
		$html .= "<td class=al>$code</a>";
		$html .= "<td class=al>$data{codes}{$code}{country}</td>";
		$html .= "<td class=ar>".&format_number($data{codes}{$code}{count_ok},0)."</td>";
		$html .= "<td class=ar>".&format_number($data{codes}{$code}{count_error},0)."</td>";
		$html .= "<td class=ar>$data{codes}{$code}{percent_error}\%</td>";
		$html .= "<tr>";
	}
	$html_bad_calls_codes = $html;
	#
	#==========================================
	# Minutes history
	#==========================================
	#
	# LAST 12 MONTHS
	%plot = ();
	$plot{uid} = "m12m";
	$plot{x} = 200;
	$plot{y} = 150;
	$plot{series}{1}{name} 	= "Minutes";
	$plot{series}{1}{color} = "92c23e";
	$slice_index = 1;
	@month_names = qw (Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m'),sum(seconds)
		from calls
		where date>date_sub(now(),interval 400 day) 
		group by DATE_FORMAT(date,'\%Y\%m')
		order by DATE_FORMAT(date,'\%Y\%m')
		limit 0,12
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (sort{$a <=> $b} keys %hash) {
		$month_number = substr($hash{$id}{slice},4,2); $month_number++; $month_number--; $month_number--;
		$month_string = (@month_names)[$month_number];
		$month_string = ($month_string eq "") ? $month_number : $month_string;
		$plot{data}{$slice_index}{1} += int($hash{$id}{value}/60);
		$plot{slices}{$slice_index} = $month_string;
		$slice_index++;
	}
	%plot = &plot_lines(%plot);
	$html_minutes_12months = $plot{html};
	#
	# LAST 60 DAYS
	%plot = ();
	$plot{uid} = "m60d";
	$plot{x} = 470;
	$plot{y} = 150;
	$plot{series}{1}{name} 	= "Minutes";
	$plot{series}{1}{color} = "92c23e";
	$slice_index = 1;
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m\%d'),sum(seconds)
		from calls
		where date>date_sub(now(),interval 70 day) 
		group by DATE_FORMAT(date,'\%Y\%m\%d')
		order by DATE_FORMAT(date,'\%Y\%m\%d')
		limit 0,60
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (sort{$a <=> $b} keys %hash) {
		$day_string = substr($hash{$id}{slice},6,2);
		$day_string++;
		$day_string--;
		$plot{data}{$slice_index}{1} += int($hash{$id}{value}/60);
		$plot{slices}{$slice_index} = $day_string;
		$slice_index++;
	}
	%plot = &plot_lines(%plot);
	$html_minutes_60days = $plot{html};


	#
	#==========================================
	# calls history
	#==========================================
	#
	# LAST 12 MONTHS
	%plot = ();
	$plot{uid} = "c12m";
	$plot{x} = 200;
	$plot{y} = 150;
	$plot{series}{1}{name} 	= "Rejected";
	$plot{series}{1}{color} = "ff6600";
	$plot{series}{2}{name} 	= "Billed";
	$plot{series}{2}{color} = "92c23e";
	$plot{series}{3}{name} 	= "Not connected";
	$plot{series}{3}{color} = "f8d322";
	@month_names = qw (Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec);
	%data = ();
	$sql = "
		select DATE_FORMAT(datetime_start,'\%Y\%m'),count(*)
		from calls_log
		where datetime_start>date_sub(now(),interval 400 day) 
		and error_id is not null
		group by DATE_FORMAT(datetime_start,'\%Y\%m')
		order by DATE_FORMAT(datetime_start,'\%Y\%m') desc
		limit 0,12
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{1} += $hash{$id}{value}; }
	$sql = "
		select DATE_FORMAT(datetime_start,'\%Y\%m'),count(*)
		from calls_log
		where datetime_start>date_sub(now(),interval 400 day) 
		and error_id is null and billing_id is null
		group by DATE_FORMAT(datetime_start,'\%Y\%m')
		order by DATE_FORMAT(datetime_start,'\%Y\%m') desc
		limit 0,12
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{3} += $hash{$id}{value}; }
	$sql = "
		select DATE_FORMAT(datetime_start,'\%Y\%m'),count(*)
		from calls_log
		where datetime_start>date_sub(now(),interval 400 day) 
		and error_id is null and billing_id is not null
		group by DATE_FORMAT(datetime_start,'\%Y\%m')
		order by DATE_FORMAT(datetime_start,'\%Y\%m') desc
		limit 0,12
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{2} += $hash{$id}{value}; }
	# TODO: apaga o que nao é 12 mais recentes
	$slice_index = 1;
	foreach $slice (sort{$a <=> $b} keys %data) {
		$month_number = substr($slice,4,2); $month_number++; $month_number--; $month_number--;
		$month_string = (@month_names)[$month_number];
		$month_string = ($month_string eq "") ? $month_number : $month_string;
		$plot{data}{$slice_index}{1} += $data{$slice}{1};
		$plot{data}{$slice_index}{2} += $data{$slice}{2};
		$plot{data}{$slice_index}{3} += $data{$slice}{3};
		$plot{slices}{$slice_index} = $month_string;
		$slice_index++;
		if ($slice_index>12) {last}
	}

	%plot = &plot_lines(%plot);
	$html_calls_12months = $plot{html};
	#
	# LAST 60 DAYS
	%plot = ();
	$plot{uid} = "c60d";
	$plot{x} = 470;
	$plot{y} = 150;
	$plot{series}{1}{name} 	= "Rejected";
	$plot{series}{1}{color} = "ff6600";
	$plot{series}{2}{name} 	= "Billed";
	$plot{series}{2}{color} = "92c23e";
	$plot{series}{3}{name} 	= "Not connected";
	$plot{series}{3}{color} = "f8d322";
	%data = ();
	$sql = "
		select DATE_FORMAT(date,'\%Y\%m\%d'),sum(seconds)
		from calls
		where date>date_sub(now(),interval 70 day) 
		group by DATE_FORMAT(date,'\%Y\%m\%d')
		order by DATE_FORMAT(date,'\%Y\%m\%d') desc
		limit 0,60
	";
	$sql = "
		select DATE_FORMAT(datetime_start,'\%Y\%m\%d'),count(*)
		from calls_log
		where datetime_start>date_sub(now(),interval 70 day) 
		and error_id is not null
		group by DATE_FORMAT(datetime_start,'\%Y\%m\%d')
		order by DATE_FORMAT(datetime_start,'\%Y\%m\%d') desc
		limit 0,60
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{1} += $hash{$id}{value}; }
	$sql = "
		select DATE_FORMAT(datetime_start,'\%Y\%m\%d'),count(*)
		from calls_log
		where datetime_start>date_sub(now(),interval 70 day) 
		and error_id is null and billing_id is null
		group by DATE_FORMAT(datetime_start,'\%Y\%m\%d')
		order by DATE_FORMAT(datetime_start,'\%Y\%m\%d') desc
		limit 0,60
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{3} += $hash{$id}{value}; }
	$sql = "
		select DATE_FORMAT(datetime_start,'\%Y\%m\%d'),count(*)
		from calls_log
		where datetime_start>date_sub(now(),interval 70 day) 
		and error_id is null and billing_id is not null
		group by DATE_FORMAT(datetime_start,'\%Y\%m\%d')
		order by DATE_FORMAT(datetime_start,'\%Y\%m\%d')
		limit 0,60
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"slice,value");
	foreach $id (keys %hash) {	$data{$hash{$id}{slice}}{2} += $hash{$id}{value}; }
	# TODO: apaga o que nao é 12 mais recentes
	$slice_index = 1;
	foreach $slice (sort{$a <=> $b} keys %data) {
		$day_string = substr($slice,6,2);
		$day_string++;
		$day_string--;
		$plot{data}{$slice_index}{1} += $data{$slice}{1};
		$plot{data}{$slice_index}{2} += $data{$slice}{2};
		$plot{data}{$slice_index}{3} += $data{$slice}{3};
		$plot{slices}{$slice_index} = $day_string;
		$slice_index++;
		if ($slice_index>61) {last}
	}


	%plot = &plot_lines(%plot);
	$html_calls_60days = $plot{html};
	#
	#==========================================
	# print page
	#==========================================
	%t = ();
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Calls overview";
	$t{dic}{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<fieldset style="width:700px;"><legend>Minutes history</legend>
	Minutes history from last 12 months and last 60 days<br>
	We only count connected and billed calls<br>
	<br>
	<div class=clear style='float:left; margin-right:20px;'>$html_minutes_12months</div>
	<div class=clear style='float:left; '>$html_minutes_60days</div>
	<br clear=both>	
	</fieldset>
	<br>

	<fieldset style="width:700px;"><legend>Calls history</legend>
	Calls history from last 12 months and last 60 days<br>
	Rejected are calls come from clients and rejected by zenofon.<br>
	Accepted are calls accepted but not billed.<br>
	Billed are calls accepted and connected.<br>
	<br>
	<div class=clear style='float:left; margin-right:20px;'>$html_calls_12months</div>
	<div class=clear style='float:left; '>$html_calls_60days</div>
	<br clear=both>	
	</fieldset>
	<br>

	<fieldset style="width:700px;"><legend>Connection problems</legend>
	We check error calls (no connection or less than 5 seconds calls) in last $data_days days.<br>
	We group by country and by first $data_dst_lenth digits of destination number.<br>
	Use this report to pin point connections problems in DST providers<br>
	<br>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 >
		<td valign=top>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
				<thead>
				<tr>
				<td >Country</td>
				<td >Calls<br>OK</td>
				<td >Calls<br>Error</td>
				<td >Error<br>rate</td>
				<td >&nbsp;&nbsp;</td>
				</tr>
				</thead>
				<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
				$html_bad_calls_country
				</tbody>
			</table>
		</td><td>&nbsp;&nbsp;&nbsp;</td><td valign=top>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
				<thead>
				<tr>
				<td >First $data_dst_lenth<br>digits</td>
				<td >Country</td>
				<td >Calls<br>OK</td>
				<td >Calls<br>Error</td>
				<td >Error<br>rate</td>
				<td >&nbsp;&nbsp;</td>	
				</tr>
				</thead>
				<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
				$html_bad_calls_codes
				</tbody>
			</table>
		</td>
		</table>
	</fieldset>
	<br>
	

	];
	&template_print("template.html",%t);
}

sub do_calls_route(){
#
	#==========================================
	# start
	#==========================================
	%t = ();
	%route_codes_to_names = &database_select_as_hash("SELECT id,name FROM product_rate_table");
	%route_names_to_codes = ();
	%route_names_to_names = ();
	foreach $id (keys %route_codes_to_names) {
		$tmp = &clean_str($route_codes_to_names{$id},"MINIMAL");
		$route_names_to_codes{$tmp} .= ($route_names_to_codes{$tmp} eq "") ? "$id" : ",$id";
		$route_names_to_names{$tmp} = $route_codes_to_names{$id};
	}
	$form{route} = &clean_str(substr($form{route},0,100),"MINIMAL");
	$form{days} = &clean_int(substr($form{days},0,100));
	$form{days} = (index("|7|15|30|60|90|365|","|$form{days}|") eq -1) ? 7 : $form{days};
	#	
	#--------------------------
	# pega count_overview
	#--------------------------
	$html_route_overview	= "<tr><td colspan=10><br><font color=#c0c0c0>Empty</font><br>&nbsp;</td></tr>";
	$sql = "
		select cl.rate_slot, sum(seconds)
		from calls c
		join calls_log cl on cl.id=c.id
		where 
		date>date_sub(now(),interval $form{days} day) 
		group by cl.rate_slot
		order by sum(seconds) desc
	";
	$html = "";
	%hash = &database_select_as_hash($sql,"value");
	$default_country = "";
	foreach $id (sort{$hash{$b}{value} <=> $hash{$a}{value}} keys %hash) {
		$name = $route_codes_to_names{$id};
		$tmp = &clean_str($name,"MINIMAL");
		$default_route = ($default_route eq "") ? $tmp : $default_route;
		$html .= "<tr>";
		$html .= "<td><a href=$my_url?action=calls_route&route=$tmp&days=$form{days}>(#$id) - $name</a></td>";
		$html .= "<td class=ar>".&format_number(($hash{$id}{value}/60),0)."</td>";
		$html .= "</tr>";
	}
	$html_route_overview = $html;
		

	#
	#--------------------------
	# calc country detail
	#--------------------------
	$html_route_detail 	= "<tr><td colspan=10><br><font color=#c0c0c0>Empty</font><br>&nbsp;</td></tr>";
	$html_route_services 	= "<tr><td colspan=10><br><font color=#c0c0c0>Empty</font><br>&nbsp;</td></tr>";
	$bak_route = $form{route} ;
	$form{route} = ($form{route} eq "") ? $default_route : $form{route};
	$route_sql = $route_names_to_codes{$form{route}};
	$route_name= $route_names_to_names{$form{route}};
	if ($route_sql eq "") {
		$route_name= "(Select route) ($form{route}) ($route_sql)";
	} else {
		$sql = "
		select name,sum(seconds)
		from calls c
		join calls_log cl on cl.id=c.id
		where 
		date>date_sub(now(),interval $form{days} day) and cl.rate_slot in ($route_sql)
		group by c.name
		";
		%hash = &database_select_as_hash($sql,"value");
		$html = "";
		foreach $name (sort{$hash{$b}{value} <=> $hash{$a}{value}} keys %hash) {
			$html .= "<tr>";
			$html .= "<td>$name</a></td>";
			$html .= "<td class=ar>".&format_number(($hash{$name}{value}/60),0)."</td>";
			$html .= "</tr>";
		}
		$html_route_detail = $html;
		
		#latest 7 days if country specified
	if ($bak_route ne "") {
		$sql = "
		select left(cast(c.date as char),10),sum(seconds)
		from calls c
		join calls_log cl on cl.id=c.id
		where 
		c.date>date_sub(now(),interval $form{days} day) 
		and cl.rate_slot in ($route_sql) 
		group by left(c.date,10)
		";
	
	} else {
		$sql = "
		select left(cast(c.date as char),10),sum(seconds)
		from calls c
		where 
		c.date>date_sub(now(),interval $form{days} day) 
		group by left(cast(c.date as char),10)
		";
		
	} 
		$html = "";
	 
		
		%hash = &database_select_as_hash($sql,"value");
		foreach $name (sort{$b cmp $a} keys %hash) {
			$html .= "<tr>";
			$html .= "<td>$name</a></td>";
			$html .= "<td class=ar>".&format_number(($hash{$name}{value}/60),0)."</td>";
			$html .= "</tr>";
		}
		$html_route_daily = $html;
		$sql = "
		select s.id,sum(seconds)
		from calls c
		join service s on s.id=c.service_id
		join calls_log cl on cl.id=c.id
		where 
		c.date>date_sub(now(),interval $form{days} day) 
		and cl.rate_slot in ($route_sql)
		group by s.id
		";
		%hash = &database_select_as_hash($sql,"value");
		@selected_services = ();
		foreach (  (sort{$hash{$b}{value} <=> $hash{$a}{value}} keys %hash)[0..50] ) {
			if ($_ eq "") {next}
			@selected_services = (@selected_services,$_);
		}
		$services_sql = join(",",@selected_services);
		$sql = "
		select s.id,s.name,s.email,ss.name
		from service s
		join service_status ss on s.status=ss.id
		where 
		s.id in ($services_sql)
		";
		%hash2 = &database_select_as_hash($sql,"name,email,status");
		$html = "";
		foreach $id (sort{$hash{$b}{value} <=> $hash{$a}{value}} @selected_services) {
			if ($id eq "") {next}
			$html .= "<tr>";
			$html .= "<td><a href=services.cgi?action=view&service_id=$id>$hash2{$id}{name} ($hash2{$id}{email})</a></td>";
			$html .= "<td>$hash2{$id}{status}</td>";
			$html .= "<td class=ar>".&format_number(($hash{$id}{value}/60),0)."</td>";
			$html .= "</tr>";
		}
		$html_route_services = $html;
	
	}
	
	#
	#==========================================
	# print page
	#==========================================
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Calls per route";
#foreach(sort keys %form) {$t{dic}{content} .= qq[FORM $_=$form{$_}<br>]; }
#foreach(sort keys %country_names_to_codes) {$t{dic}{content} .= qq[country_names_to_codes $_=$country_names_to_codes{$_}<br>]; }
#foreach(sort keys %country_names_to_names) {$t{dic}{content} .= qq[country_names_to_names $_=$country_names_to_names{$_}<br>]; }

	$t{dic}{content} .= qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>
	<div class=clear style="width:800px;">

	<fieldset style="float:left; width:250px; margin-right:15px;"><legend>Route</legend>
		Country and minute for last $form{days}. You can select this report by
		<a href=$my_url?action=calls_route&route=$form{route}&days=7>7</a>, 
		<a href=$my_url?action=calls_route&route=$form{route}&days=15>15</a>, 
		<a href=$my_url?action=calls_route&route=$form{route}&days=30>30</a>, 
		<a href=$my_url?action=calls_route&route=$form{route}&days=60>60</a>, 
		<a href=$my_url?action=calls_route&route=$form{route}&days=90>90</a> and  
		<a href=$my_url?action=calls_route&route=$form{route}&days=365>365</a> days.<br>
		<br>
		<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
			<thead>
			<tr>
			<td >Route</td>
			<td >Minutes</td>
			<!--<td >&nbsp;&nbsp;</td>-->
			</tr>
			</thead>
			<tbody style="height:270px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
			$html_route_overview
			</tbody>
		</table>
	</fieldset>


	<fieldset style="float:left; width:400px;"><legend>$route_name</legend>
		Here you see details about selected Route.
		Area names (multiple area codes) and top 50 talk services<br>
		<br>
		<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
			<thead>
			<tr>
			<td >Area name</td>
			<td >Minutes</td>
			<!--<td >&nbsp;&nbsp;</td>-->
			</tr>
			</thead>
			<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
			$html_route_detail
			
			</tbody>
		</table>
		<br>
		Here you see latest 7 days statistics for route :$bak_route
		 
		<br>
		<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
			<thead>
			<tr>
			<td >Date</td>
		 
			<td >Minutes</td>
			<!--<td >&nbsp;&nbsp;</td>-->
			</tr>
			</thead>
			<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
			$html_route_daily
			</tbody>
		</table>
			<br>
		<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
			<thead>
			<tr>
			<td >Service</td>
			<td >Status</td>
			<td >Minutes</td>
			<!--<td >&nbsp;&nbsp;</td>-->
			</tr>
			</thead>
			<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
			$html_route_services
			</tbody>
		</table>
		
	</fieldset>
	<br clear=both>
	
	</div>

	];
	&template_print("template.html",%t);	
}

sub do_calls_country(){
	#
	#==========================================
	# start
	#==========================================
	%t = ();
	%country_codes_to_names = &database_select_as_hash("SELECT code,name FROM country");
	%country_names_to_codes = ();
	%country_names_to_names = ();
	foreach $id (keys %country_codes_to_names) {
		$tmp = &clean_str($country_codes_to_names{$id},"MINIMAL");
		$country_names_to_codes{$tmp} .= ($country_names_to_codes{$tmp} eq "") ? "$id" : ",$id";
		$country_names_to_names{$tmp} = $country_codes_to_names{$id};
	}
	$form{country} = &clean_str(substr($form{country},0,100),"MINIMAL");
	$form{days} = &clean_int(substr($form{days},0,100));
	$form{days} = (index("|7|15|30|60|90|365|","|$form{days}|") eq -1) ? 7 : $form{days};
	#	
	#--------------------------
	# pega count_overview
	#--------------------------
	$html_country_overview	= "<tr><td colspan=10><br><font color=#c0c0c0>Empty</font><br>&nbsp;</td></tr>";
	$sql = "
		select country,sum(seconds)
		from calls
		where 
		date>date_sub(now(),interval $form{days} day) 
		group by country
		order by sum(seconds) desc
	";
	$html = "";
	%hash = &database_select_as_hash($sql,"value");
	$default_country = "";
	foreach $id (sort{$hash{$b}{value} <=> $hash{$a}{value}} keys %hash) {
		$name = $country_codes_to_names{$id};
		$tmp = &clean_str($name,"MINIMAL");
		$default_country = ($default_country eq "") ? $tmp : $default_country;
		$html .= "<tr>";
		$html .= "<td><a href=$my_url?action=calls_country&country=$tmp&days=$form{days}>$name</a></td>";
		$html .= "<td class=ar>".&format_number(($hash{$id}{value}/60),0)."</td>";
		$html .= "</tr>";
	}
	$html_country_overview = $html;
		

	#
	#--------------------------
	# calc country detail
	#--------------------------
	$html_country_detail 	= "<tr><td colspan=10><br><font color=#c0c0c0>Empty</font><br>&nbsp;</td></tr>";
	$html_country_services 	= "<tr><td colspan=10><br><font color=#c0c0c0>Empty</font><br>&nbsp;</td></tr>";
	$bak_country = $form{country} ;
	$form{country} = ($form{country} eq "") ? $default_country : $form{country};
	$country_sql = $country_names_to_codes{$form{country}};
	$country_name= $country_names_to_names{$form{country}};
	if ($country_sql eq "") {
		$country_name= "(Select country) ($form{country}) ($country_sql)";
	} else {
		$sql = "
		select name,sum(seconds)
		from calls
		where 
		date>date_sub(now(),interval $form{days} day) and country in ($country_sql)
		group by name
		";
		%hash = &database_select_as_hash($sql,"value");
		$html = "";
		foreach $name (sort{$hash{$b}{value} <=> $hash{$a}{value}} keys %hash) {
			$html .= "<tr>";
			$html .= "<td>$name</a></td>";
			$html .= "<td class=ar>".&format_number(($hash{$name}{value}/60),0)."</td>";
			$html .= "</tr>";
		}
		$html_country_detail = $html;
		#latest 7 days if country specified
	if ($bak_country ne "") {
		$sql = "
		select left(calls.date,10),sum(seconds)
		from calls
		where 
		calls.date>date_sub(now(),interval $form{days} day) 
		and calls.country in ($country_sql) 
		group by left(calls.date,10)
		";
	
	} else {
		$sql = "
		select left(calls.date,10),sum(seconds)
		from calls
		where 
		calls.date>date_sub(now(),interval $form{days} day) 
		group by left(calls.date,10)
		";
		
	} 
		$html = "";
	 
		
		%hash = &database_select_as_hash($sql,"value");
		foreach $name (sort{$b cmp $a} keys %hash) {
			$html .= "<tr>";
			$html .= "<td>$name</a></td>";
			$html .= "<td class=ar>".&format_number(($hash{$name}{value}/60),0)."</td>";
			$html .= "</tr>";
		}
		$html_country_daily = $html;
		
		$sql = "
		select service.id,sum(seconds)
		from calls,service
		where 
		calls.date>date_sub(now(),interval $form{days} day) 
		and calls.country in ($country_sql)
		and calls.service_id=service.id
		group by service.id
		";
		%hash = &database_select_as_hash($sql,"value");
		@selected_services = ();
		foreach (  (sort{$hash{$b}{value} <=> $hash{$a}{value}} keys %hash)[0..50] ) {
			if ($_ eq "") {next}
			@selected_services = (@selected_services,$_);
		}
		$services_sql = join(",",@selected_services);
		$sql = "
		select service.id,service.name,service.email,service_status.name
		from service,service_status
		where 
		service.status=service_status.id and 
		service.id in ($services_sql)
		";
		%hash2 = &database_select_as_hash($sql,"name,email,status");
		$html = "";
		foreach $id (sort{$hash{$b}{value} <=> $hash{$a}{value}} @selected_services) {
			if ($id eq "") {next}
			$html .= "<tr>";
			$html .= "<td><a href=services.cgi?action=view&service_id=$id>$hash2{$id}{name} ($hash2{$id}{email})</a></td>";
			$html .= "<td>$hash2{$id}{status}</td>";
			$html .= "<td class=ar>".&format_number(($hash{$id}{value}/60),0)."</td>";
			$html .= "</tr>";
		}
		$html_country_services = $html;
	
	}
	
	#
	#==========================================
	# print page
	#==========================================
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Calls per country";
#foreach(sort keys %form) {$t{dic}{content} .= qq[FORM $_=$form{$_}<br>]; }
#foreach(sort keys %country_names_to_codes) {$t{dic}{content} .= qq[country_names_to_codes $_=$country_names_to_codes{$_}<br>]; }
#foreach(sort keys %country_names_to_names) {$t{dic}{content} .= qq[country_names_to_names $_=$country_names_to_names{$_}<br>]; }
	$t{dic}{content} .= qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>
	<div class=clear style="width:800px;">

	<fieldset style="float:left; width:250px; margin-right:15px;"><legend>Country</legend>
		Country and minute for last $form{days}. You can select this report by
		<a href=$my_url?action=calls_country&country=$form{country}&days=7>7</a>, 
		<a href=$my_url?action=calls_country&country=$form{country}&days=15>15</a>, 
		<a href=$my_url?action=calls_country&country=$form{country}&days=30>30</a>, 
		<a href=$my_url?action=calls_country&country=$form{country}&days=60>60</a>, 
		<a href=$my_url?action=calls_country&country=$form{country}&days=90>90</a> and  
		<a href=$my_url?action=calls_country&country=$form{country}&days=365>365</a> days.<br>
		<br>
		<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
			<thead>
			<tr>
			<td >Country</td>
			<td >Minutes</td>
			<td >&nbsp;&nbsp;</td>
			</tr>
			</thead>
			<tbody style="height:270px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
			$html_country_overview
			</tbody>
		</table>
	</fieldset>


	<fieldset style="float:left; width:400px;"><legend>$country_name</legend>
		Here you see details about selected country.
		Area names (multiple area codes) and top 50 talk services<br>
		<br>
		<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
			<thead>
			<tr>
			<td >Area name</td>
			<td >Minutes</td>
			<td >&nbsp;&nbsp;</td>
			</tr>
			</thead>
			<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
			$html_country_detail
			
			</tbody>
		</table>
		<br>
		Here you see latest 7 days statistics for country :$bak_country
		 
		<br>
		<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
			<thead>
			<tr>
			<td >Date</td>
		 
			<td >Minutes</td>
			<td >&nbsp;&nbsp;</td>
			</tr>
			</thead>
			<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
			$html_country_daily
			</tbody>
		</table>
			<br>
		<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
			<thead>
			<tr>
			<td >Service</td>
			<td >Status</td>
			<td >Minutes</td>
			<td >&nbsp;&nbsp;</td>
			</tr>
			</thead>
			<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
			$html_country_services
			</tbody>
		</table>
		
	</fieldset>
	<br clear=both>
	
	</div>

	];
	&template_print("template.html",%t);
}
sub do_calls_overview(){
	#
	#==========================================
	# start
	#==========================================
	$prefix = &clean_int($form{prefix});
	%t = ();
	#	
	#==========================================
	# plota duration days
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and left(calls_log.dst,".length($prefix).") = '$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d'),
		sum( IF(calls.seconds<15,1,0) ),
		sum( IF(calls.seconds<300,1,0) ),
		sum( IF(calls.seconds<1800,1,0) ),
		sum( IF(calls.seconds>=1800,1,0) )
	FROM calls_log, calls 
	where 
		calls_log.datetime_start >date_sub(now(),interval 60 day) 
		and calls_log.datetime_stop is not null
		and calls_log.billing_id is not null
		and calls_log.billing_id = calls.id
		$sql_prefix 
	group by DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d')
	";
	%data = &database_select_as_hash($sql,"s,m1,m2,l");
	%plot = ();
	$plot{uid} = "60days";
	$plot{x} = 450;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "15 sec calls";
	$plot{series}{1}{color} = "ff0000";
	$plot{series}{2}{name} 	= "5 min calls";
	$plot{series}{2}{color} = "ff6600";
	$plot{series}{3}{name} 	= "30 min calls";
	$plot{series}{3}{color} = "f8d322";
	$plot{series}{4}{name} 	= "Long calls";
	$plot{series}{4}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{s};
		$plot{data}{$slice_index}{2} += $data{$slice}{m1}-$data{$slice}{s};
		$plot{data}{$slice_index}{3} += $data{$slice}{m2}-$data{$slice}{m1};
		$plot{data}{$slice_index}{4} += $data{$slice}{l};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>30) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_duration_days = $plot{html};
	#	
	#==========================================
	# plota duration months
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and left(calls_log.dst,".length($prefix).") = '$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m') as dt,
		sum( IF(calls.seconds<15,1,0) ) s15,
		sum( IF(calls.seconds<300,1,0) ),
		sum( IF(calls.seconds<1800,1,0) ) m30,
		sum( IF(calls.seconds>=1800,1,0) ) m60beyond
	FROM calls_log, calls 
	where 
		calls_log.datetime_start >date_sub(now(),interval 600 day) 
		and calls_log.datetime_stop is not null
		and calls_log.billing_id is not null
		and calls_log.billing_id = calls.id
		$sql_prefix 
	group by DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m')
	";
	%data = &database_select_as_hash($sql,"s,m1,m2,l");
	%plot = ();
	$plot{uid} = "2years";
	$plot{x} = 250;
	$plot{y} = 255;
	$plot{series}{1}{name} 	= "15 sec calls";
	$plot{series}{1}{color} = "ff0000";
	$plot{series}{2}{name} 	= "5 min calls";
	$plot{series}{2}{color} = "ff6600";
	$plot{series}{3}{name} 	= "30 min calls";
	$plot{series}{3}{color} = "f8d322";
	$plot{series}{4}{name} 	= "Long calls";
	$plot{series}{4}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{s};
		$plot{data}{$slice_index}{2} += $data{$slice}{m1}-$data{$slice}{s};
		$plot{data}{$slice_index}{3} += $data{$slice}{m2}-$data{$slice}{m1};
		$plot{data}{$slice_index}{4} += $data{$slice}{l};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_duration_monts = $plot{html};
	#	
	#==========================================
	# plota asr/acd days
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and left(calls_log.dst,".length($prefix).") = '$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d'),
		count(*),
		sum( IF(calls.seconds<30,1,0) )
	FROM calls_log, calls 
	where 
		calls_log.datetime_start >date_sub(now(),interval 60 day) 
		and calls_log.datetime_stop is not null
		and calls_log.billing_id is not null
		and calls_log.billing_id = calls.id
		$sql_prefix 
	group by DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d')
	";
	%data = &database_select_as_hash($sql,"ok,oks15");
	$sql = "
	SELECT 
		DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d'),
		count(*)
	FROM calls_log 
	where 
		calls_log.datetime_start >date_sub(now(),interval 60 day) 
		and calls_log.datetime_stop is not null
		and calls_log.billing_id is null
		$sql_prefix 
	group by DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d')
	";
	%hash = &database_select_as_hash($sql);
	foreach (keys %hash) {$data{$_}{error} = $hash{$_};}
	%plot = ();
	$plot{uid} = "asrdays";
	$plot{x} = 400;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "ASR";
	$plot{series}{1}{color} = "ff0000";
	#$plot{series}{2}{name} 	= "ASR (plus <30 sec calls)";
	#$plot{series}{2}{color} = "ff6600";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$tmp_ok 	= $data{$slice}{ok};
		$tmp_error	= $data{$slice}{error};
		$tmp_tot	= $tmp_error+$tmp_ok;
		$plot{data}{$slice_index}{1} = ($tmp_tot>0) ? int(100*($tmp_ok/$tmp_tot)) : 0;
		$tmp_ok 	= $data{$slice}{ok}-$data{$slice}{oks15};
		$tmp_error	= $data{$slice}{error}+$data{$slice}{oks15};
		$tmp_tot	= $tmp_error+$tmp_ok;
		#$plot{data}{$slice_index}{2} = ($tmp_tot>0) ? int(100*($tmp_ok/$tmp_tot)) : 0;
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>30) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_asr_days = $plot{html};
	#	
	#==========================================
	# plota asr/acd hours
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and left(calls_log.dst,".length($prefix).") = '$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d: \%h'),
		count(*),
		sum( IF(calls.seconds<30,1,0) )
	FROM calls_log, calls 
	where 
		calls_log.datetime_start >date_sub(now(),interval 96 hour) 
		and calls_log.datetime_stop is not null
		and calls_log.billing_id is not null
		and calls_log.billing_id = calls.id
		$sql_prefix 
	group by DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d: \%h')
	";
	%data = &database_select_as_hash($sql,"ok,oks15");
	$sql = "
	SELECT 
		DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d: \%h'),
		count(*)
	FROM calls_log 
	where 
		calls_log.datetime_start >date_sub(now(),interval 96 hour) 
		and calls_log.datetime_stop is not null
		and calls_log.billing_id is null
		$sql_prefix 
	group by DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d: \%h')
	";
	%hash = &database_select_as_hash($sql);
	foreach (keys %hash) {$data{$_}{error} = $hash{$_};}
	%plot = ();
	$plot{uid} = "asrhours";
	$plot{x} = 300;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "ASR";
	$plot{series}{1}{color} = "ff0000";
	#$plot{series}{2}{name} 	= "ASR (plus <30 sec calls)";
	#$plot{series}{2}{color} = "ff6600";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$tmp_ok 	= $data{$slice}{ok};
		$tmp_error	= $data{$slice}{error};
		$tmp_tot	= $tmp_error+$tmp_ok;
		$plot{data}{$slice_index}{1} = ($tmp_tot>0) ? int(100*($tmp_ok/$tmp_tot)) : 0;
		$tmp_ok 	= $data{$slice}{ok}-$data{$slice}{oks15};
		$tmp_error	= $data{$slice}{error}+$data{$slice}{oks15};
		$tmp_tot	= $tmp_error+$tmp_ok;
		#$plot{data}{$slice_index}{2} = ($tmp_tot>0) ? int(100*($tmp_ok/$tmp_tot)) : 0;
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>24) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_asr_hour = $plot{html};
	#	
	#==========================================
	# plota minutes days
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and left(calls_log.dst,".length($prefix).") = '$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d'),
		sum(calls.seconds)
	FROM calls_log, calls 
	where 
		calls_log.datetime_start >date_sub(now(),interval 90 day) 
		and calls_log.datetime_stop is not null
		and calls_log.billing_id is not null
		and calls_log.billing_id = calls.id
		$sql_prefix 
	group by DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d')
	";
	%data = &database_select_as_hash($sql,"sec");
	$d1 = "";
	$d2 = "";
	foreach $slice (sort{$b cmp $a} keys %data) {
		$d1 = ($d1 eq "") ? substr($slice,0,7) : $d1;
		if ($d1 ne substr($slice,0,7)) {
			$d2 = substr($slice,0,7);
			last;
		}
	}
	%plot = ();
	$plot{uid} = "mindays";
	$plot{x} = 400;
	$plot{y} = 200;
	$plot{series}{2}{name} 	= "$d1 Minutes";
	$plot{series}{2}{color} = "92c23e";
	$plot{series}{1}{name} 	= "$d2 Minutes";
	$plot{series}{1}{color} = "f8d322";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{2} = int($data{$d1."-".$dd}{sec}/60);
		$plot{data}{$slice_index}{1} = int($data{$d2."-".$dd}{sec}/60);
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSArea2D(%plot);
	$plot_min_days = $plot{html};
	#	
	#==========================================
	# plota minutes hours
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and left(calls_log.dst,".length($prefix).") = '$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d: \%H'),
		sum(calls.seconds)
	FROM calls_log, calls 
	where 
		calls_log.datetime_start >date_sub(now(),interval 7 day) 
		and calls_log.datetime_stop is not null
		and calls_log.billing_id is not null
		and calls_log.billing_id = calls.id
		$sql_prefix 
	group by DATE_FORMAT(calls_log.datetime_start,'\%Y-\%m-\%d: \%H')
	";
	%data = &database_select_as_hash($sql,"sec");
	$d1 = "";
	$d2 = "";
	foreach $slice (sort{$b cmp $a} keys %data) {
		$d1 = ($d1 eq "") ? substr($slice,0,10) : $d1;
		if ($d1 ne substr($slice,0,10)) {
			$d2 = substr($slice,0,10);
			last;
		}
	}
	%plot = ();
	$plot{uid} = "minhours";
	$plot{x} = 300;
	$plot{y} = 200;
	$plot{series}{2}{name} 	= "$d1 Minutes";
	$plot{series}{2}{color} = "92c23e";
	$plot{series}{1}{name} 	= "$d2 Minutes";
	$plot{series}{1}{color} = "f8d322";
	$slice_index = 1;
	@hours = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23);
	foreach $h (@hours) {
		$hh = substr("00".$h,-2,2);
		$plot{data}{$slice_index}{2} = int($data{"$d1: $hh"}{sec}/60);
		$plot{data}{$slice_index}{1} = int($data{"$d2: $hh"}{sec}/60);
		$plot{slices}{$slice_index} = $hh;
		$slice_index++;
	}
	%plot = &plot_MSArea2D(%plot);
	$plot_min_hour = $plot{html};
	#
	#==========================================
	# print page
	#==========================================
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Calls overview";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "reports.cgi";
    $t{breadcrumb}{1}{title}	= "Calls overview";
    $t{breadcrumb}{1}{url}		= "";
	$t{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<fieldset style="width:730px;"><legend>Filter charts by</legend>
	<form action=$my_url>
	Destination number starts with:<input name=prefix value="$prefix"><button type=submit>Refresh</button>
	<input type=hidden name=action value=calls_overview>
	</form>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Calls minutes</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_min_hour</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_min_days</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Calls ASR</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_asr_hour</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_asr_days</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Call count grouped by call duration</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_duration_days</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_duration_monts</td>
	</table>
	</fieldset>
	<br>
	];
	&template_print("template.html",%t);
}
sub do_calls_error(){
	#
	#==========================================
	# start
	#==========================================
	$prefix = &clean_int($form{prefix});
	%t = ();
	#
	#==========================================
	# Bad calls
	#==========================================
	%data = ();
	$data_days = 7;
	$data_dst_lenth = 5;
	$html = "";
	#--------------------------
	# pega no connection
	#--------------------------
	$sql = "
		select left(dst,$data_dst_lenth),count(*)
		from calls_log
		where 
		billing_id is null and 
		service_id is not null and 
		dst <> '' and 
		error_id is null and
		datetime_start>date_sub(now(),interval $data_days day) 
		group by left(dst,$data_dst_lenth)
		order by count(*) desc
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"code,count");
	foreach $id (keys %hash) {
		$data{codes}{$hash{$id}{code}}{count_error}	+= $hash{$id}{count};
		$data{codes}{$hash{$id}{code}}{country}	= "";
	}
	#--------------------------
	# pega low seconds
	#--------------------------
	$sql = "
		select left(dst,$data_dst_lenth),count(*)
		from calls
		where 
		date>date_sub(now(),interval $data_days  day) and seconds<5
		group by left(dst,$data_dst_lenth)
		order by count(*) desc
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"code,count");
	foreach $id (keys %hash) {
		$data{codes}{$hash{$id}{code}}{count_error}	+= $hash{$id}{count};
		$data{codes}{$hash{$id}{code}}{country}	= "";
	}
	#--------------------------
	# pega count_ok
	#--------------------------
	$sql = "
		select left(dst,$data_dst_lenth),count(*)
		from calls
		where 
		date>date_sub(now(),interval $data_days  day) and seconds>=5
		group by left(dst,$data_dst_lenth)
		order by count(*) desc
	";
	%hash = &database_select_as_hash_with_auto_key($sql,"code,count");
	foreach $id (keys %hash) {
		#unless(exists($data{code}{$hash{$id}{code}})) {next}
		$data{codes}{$hash{$id}{code}}{count_ok}	+= $hash{$id}{count};
	}
	#--------------------------
	# calc country
	#--------------------------
	%country_names = &database_select_as_hash("SELECT code,name FROM country");
	$country_codes_buf = "|".join("|",(keys %country_names))."|";
	foreach $code (keys %{$data{codes}}) {
		$country = "(UNKNOWN)";
		foreach $size (1..4){
			$sub_code = substr($code,0,$size);
			if (index($country_codes_buf,"|$sub_code|") eq -1) {next}
			unless (exists($country_names{$sub_code})) {next}
			$country = $country_names{$sub_code};
		}
		$data{codes}{$code}{country} = $country;
		$data{country}{$country}{count_error} += $data{codes}{$code}{count_error};
		$data{country}{$country}{count_ok} += $data{codes}{$code}{count_ok};
	}
	#--------------------------
	# delete zero errors and calc percentage
	#--------------------------
	foreach $country (keys %{$data{country}}) {		
		if ( ($data{country}{$country}{count_error}>0) && ($data{country}{$country}{count_ok}>0) && (($data{country}{$country}{count_error}+$data{country}{$country}{count_ok})>10) ){
			$p = $data{country}{$country}{count_error}/($data{country}{$country}{count_error}+$data{country}{$country}{count_ok});
			$data{country}{$country}{percent_error} = int($p*100);
		} else {
			delete $data{country}{$country};
		}
	}
	foreach $code (keys %{$data{codes}}) {		
		if ( ($data{codes}{$code}{count_error}>0) && ($data{codes}{$code}{count_ok}>0) && (($data{codes}{$code}{count_error}+$data{codes}{$code}{count_ok})>10) ){
			$p = $data{codes}{$code}{count_error}/($data{codes}{$code}{count_error}+$data{codes}{$code}{count_ok});
			$data{codes}{$code}{percent_error} = int($p*100);
		} else {
			delete $data{codes}{$code};
		}
	}
	#--------------------------
	# html country
	#--------------------------
	$html = "";
	foreach $country (sort{$data{country}{$b}{percent_error} <=> $data{country}{$a}{percent_error}} keys %{$data{country}}) {
		$html .= "<tr>";
		$html .= "<td class=al>$country</a>";
		$html .= "<td class=ar>".&format_number($data{country}{$country}{count_ok},0)."</td>";
		$html .= "<td class=ar>".&format_number($data{country}{$country}{count_error},0)."</td>";
		$html .= "<td class=ar>$data{country}{$country}{percent_error}\%</td>";
		$html .= "<tr>";
	}
	$html_bad_calls_country = $html;
	#--------------------------
	# html areacodes
	#--------------------------
	$html = "";
	foreach $code (sort{$data{codes}{$b}{percent_error} <=> $data{codes}{$a}{percent_error}} keys %{$data{codes}}) {
		$html .= "<tr>";
		$html .= "<td class=al>$code</a>";
		$html .= "<td class=al>$data{codes}{$code}{country}</td>";
		$html .= "<td class=ar>".&format_number($data{codes}{$code}{count_ok},0)."</td>";
		$html .= "<td class=ar>".&format_number($data{codes}{$code}{count_error},0)."</td>";
		$html .= "<td class=ar>$data{codes}{$code}{percent_error}\%</td>";
		$html .= "<tr>";
	}
	$html_bad_calls_codes = $html;
	#
	#==========================================
	# print page
	#==========================================
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Calls error";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "reports.cgi";
    $t{breadcrumb}{1}{title}	= "Calls error";
    $t{breadcrumb}{1}{url}		= "";
	$t{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<fieldset style="width:730px;"><legend>Connection problems</legend>
	We check error calls (no connection or less than 5 seconds calls) in last $data_days days.<br>
	We group by country and by first $data_dst_lenth digits of destination number.<br>
	Use this report to pin point connections problems in DST providers<br>
	<br>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 >
		<td valign=top>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
				<thead>
				<tr>
				<td >Country</td>
				<td >Calls<br>OK</td>
				<td >Calls<br>Error</td>
				<td >Error<br>rate</td>
				<td >&nbsp;&nbsp;</td>
				</tr>
				</thead>
				<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
				$html_bad_calls_country
				</tbody>
			</table>
		</td><td>&nbsp;&nbsp;&nbsp;</td><td valign=top>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable onclick="sortColumn(event)">
				<thead>
				<tr>
				<td >First $data_dst_lenth<br>digits</td>
				<td >Country</td>
				<td >Calls<br>OK</td>
				<td >Calls<br>Error</td>
				<td >Error<br>rate</td>
				<td >&nbsp;&nbsp;</td>
				</tr>
				</thead>
				<tbody style="height:120px; overflow:auto; overflow-x:hidden; overflow-y:auto;">
				$html_bad_calls_codes
				</tbody>
			</table>
		</td>
		</table>
	</fieldset>
	<br>
	];
	&template_print("template.html",%t);
}
sub do_calls_cdr(){
	
	%t = ();
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Call CDR";
	#
	#-------------------------------------
	# prepare date
	#-------------------------------------
	$date_1 = "";
	$date_2 = "";
	if ( ($form{date1} ne "") && ($form{date2} ne "") ) {
		$tmp1 = &clean_int($form{date1});
		$tmp11 = substr($tmp1,0,4); $tmp11++; $tmp11--;
		$tmp12 = substr($tmp1,4,2); $tmp12++; $tmp12--;
		$tmp13 = substr($tmp1,6,2); $tmp13++; $tmp13--;
		if ( ($tmp11>2000) && ($tmp11<3000) && ($tmp12>=1) && ($tmp12<=12) && ($tmp13>=1) && ($tmp13<=31) ) {
			$date_1 = substr("0000".$tmp11,-4,4)."-".substr("0000".$tmp12,-2,2)."-".substr("0000".$tmp13,-2,2);
			$form{date1} = $date_1;
		}
		$tmp1 = &clean_int($form{date2});
		$tmp11 = substr($tmp1,0,4); $tmp11++; $tmp11--;
		$tmp12 = substr($tmp1,4,2); $tmp12++; $tmp12--;
		$tmp13 = substr($tmp1,6,2); $tmp13++; $tmp13--;
		if ( ($tmp11>2000) && ($tmp11<3000) && ($tmp12>=1) && ($tmp12<=12) && ($tmp13>=1) && ($tmp13<=31) ) {
			$date_2 = substr("0000".$tmp11,-4,4)."-".substr("0000".$tmp12,-2,2)."-".substr("0000".$tmp13,-2,2);
			$form{date2} = $date_2;
		}
		$date_min = "$date_1 00:00:00";
		$date_max = "$date_2 23:59:59";
	} else {
		my ($dd,$mm,$yy) = (localtime)[3,4,5];
		$today = sprintf("%04d-%02d-%02d",$yy+1900,$mm+1,$dd) ;
		
		 ($dd,$mm,$yy) = (localtime(time() -3600*24*7) )[3,4,5];
		 $oneweekago  = sprintf("%04d-%02d-%02d",$yy+1900,$mm+1,$dd) ;
		 
		$form{date1} = ($form{date1} eq "") ?  $oneweekago : $form{date1};
		$form{date2} = ($form{date2} eq "") ?  $today : $form{date2};
	}
	$date_ok = ( ($date_2 ne "") && ($date_1 ne "") ) ? 1 : 0;
	#-------------------------------------
	# so faz se tem data
	#-------------------------------------
	if ($date_ok eq 1) {
		#
		#-------------------------------------
		# start
		#-------------------------------------
		%services_commissions = ();
		%services_data = ();
		%services_calls = ();
		%services_tree = ();
		$blocked_services_ids = "|1|2|0|";
		
	
		
		#
		#-------------------------------------
		# commissions
		#-------------------------------------
		$sql = "
			select id,date,ani,did,dst,service_id,seconds,rate_value from calls  
			where date >='$date_min' and date<='$date_max' 
			
		";
		warning($sql);
		%calls  = &database_select_as_hash($sql,"date,ani,did,dst,service_id,seconds,rate_value");
  		#
		#-------------------------------------
		# get tree
		#-------------------------------------
	 
		
		    print "Pragma: public\n";
	    print "Expires: 0\n";
	    print "Cache-Control: must-revalidate, post-check=0, pre-check=0\n";
	    print "Content-type: application/octet-stream\n";
	    print "Content-Disposition: attachment; filename=\"zenofon.cdr.csv\"\n";
	    print "Content-Description: File Transfert\n";
	    #print "Content-type: text/plain\n";
	    print "\n";
	    print "Date,ANI,DID,DST,Service_ID,Seconds,Cost\n";
	     
		 
		 
		foreach $id (sort{$b <=> $a} keys %calls){		 
	 
				 
				    print "\"$calls{$id}{date}\",";
				    print "\"$calls{$id}{ani}\",";
					print "\"$calls{$id}{did}\",";
					print "\"$calls{$id}{dst}\",";
					print "\"$calls{$id}{service_id}\",";
					print "\"$calls{$id}{seconds}\",";
					print "\"$calls{$id}{rate_value}\",";
					#
				    print "\n";
				 
			}
		
	    exit;
    
	 
		}
	#
	#-------------------------------------
	# print page
	#-------------------------------------
	$t{dic}{content}	.= qq[
		<form action=$my_url>
		Start date (YYYY-MM-DD): <input type=text name=date1 value="$form{date1}"><br>
		End date (YYYY-MM-DD): <input type=text name=date2 value="$form{date2}"><br>
		<input type=submit value=Download><br>
		<input type=hidden name=action value=calls_cdr>
		</form>
		<br>
 	];
	&template_print("template.html",%t);

}
sub do_radio_minutes(){
    #
    #-------------------------------
    # prepare year/month select and values
    #-------------------------------
	%yearmonth_select = &database_select_as_hash("SELECT distinct DATE_FORMAT(datetime_start,'\%Y\%m'),1 FROM radio_listen_session ");
	%hash = database_select_as_hash("SELECT 1,1,max(DATE_FORMAT(datetime_start,'\%Y\%m')) FROM radio_listen_session ","flag,value");
	$form{yearmonth} = clean_int($form{yearmonth});
	$form{yearmonth} = (length($form{yearmonth}) ne 6) ? "" : $form{yearmonth};
	$form{yearmonth} = ( ($form{yearmonth} eq "") && ($hash{1}{flag} eq 1) ) ? $hash{1}{value} : $form{yearmonth};
	$form{yearmonth} = (exists($yearmonth_select{$form{yearmonth}})) ? $form{yearmonth} : "";
	$year	= substr($form{yearmonth},0,4);
	$month	= substr($form{yearmonth},4,2);
    #
    #-------------------------------
    # get top radios
    #-------------------------------
    $sql = "
    	SELECT radio_extension,count(*),concat('Unknown ',radio_extension)
		FROM radio_listen_session  
		where datetime_start>date_sub(now(),interval 60 day)
		group by radio_extension
		order by count(*) desc 
		LIMIT 0,10
	";
	%top_radios = database_select_as_hash($sql,"count,title");
	$ids = join("," , (keys %top_radios));
	$sql = "SELECT extension,title FROM radio_station where extension in ($ids)";
	%hash = database_select_as_hash($sql);
	foreach $e (keys %hash){ if (exists($top_radios{$e})) { $top_radios{$e}{title} = $hash{$e}; }  }
    #
    #-------------------------------
    # get gateway 
    #-------------------------------
	$sql = "SELECT id,title,title FROM radio_gateway";
	%radio_gw = database_select_as_hash($sql,"title,did");
    #
    #-------------------------------
    # radios select 
    #-------------------------------
    $form{radio_ext} = &clean_int(substr($form{radio_ext},0,100));
	$form{radio_filter} = ($form{radio_ext} ne "") ? "EXTENSION" : $form{radio_filter};
    $select_radio = "";
	# extension filter
	$tmp = ($form{radio_filter} eq "EXTENSION") ? "selected" : "";
    $select_radio .= "<option $tmp value='EXTENSION'>By radio extension &#187;</option>";
    $select_radio .= "<option value=''>&nbsp;</option>";
    # by radio stations
    $select_radio .= "<option value=''>By radio station</option>";
    foreach $e (sort{$top_radios{$b}{count} <=> $top_radios{$a}{count}} keys %top_radios) {
		$tmp = ($form{radio_filter} eq "T$e") ? "selected" : "";
	    $select_radio .= "<option $tmp value='T$e'>&nbsp;&#187; ($e) $top_radios{$e}{title}</option>";
    }
    $select_radio .= "<option value=''>&nbsp;</option>";
    # by radio gw
    $select_radio .= "<option value=''>By radio DID</option>";
	$tmp = ($form{radio_filter} eq "G") ? "selected" : "";
    $select_radio .= "<option $tmp value='G'>&nbsp;&#187; Main access (or unknown DID)</option>";
    foreach $i (sort{$top_radios{$a}{title} <=> $top_radios{$b}{title}} keys %radio_gw) {
		$tmp = ($form{radio_filter} eq "G".$i) ? "selected" : "";
	    $select_radio .= "<option $tmp value='G$i'>&nbsp;&#187; $radio_gw{$i}{title}</option>";
    }
    $select_radio .= "<option value=''>&nbsp;</option>";
    #
    #-------------------------------
    # get statistics
    #-------------------------------
    # uids
    $sql = "
    	SELECT 1,1,count(*),count(distinct ANI) 
    	FROM radio_listen_call 
		where 
			datetime_stop is not null and 
			month(datetime_start) = '$month' and 
			year(datetime_start) = '$year'
    	";
	%hash = &database_select_as_hash($sql,"flag,value1,value2");
	$data{total_calls}	= ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value1},0) : 0;
	$data{total_uids}	= ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value2},0) : 0;
	$data{total_uids_x_calls} = ($data{total_uids}>0) ? &format_number(($data{total_calls}/$data{total_uids}),2) : 0;
    $sql = "
    	SELECT 1,1,count(*),sum(answered_time)
    	FROM radio_listen_session 
		where 
			month(datetime_start) = '$month' and 
			year(datetime_start) = '$year'
    	";
	%hash = &database_select_as_hash($sql,"flag,value1,value2");
	$data{total_sessions}			= ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value1},0) : 0;
	$data{total_sessions_minutes}	= ($hash{1}{flag} eq 1) ? &format_number( int($hash{1}{value2}/60) ,0) : 0;
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "day,uids,calls,sessions,minutes"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		select 
			DATE_FORMAT(datetime_start,'\%Y-\%m-\%d'),
			DATE_FORMAT(datetime_start,'\%Y-\%m-\%d'),
			0,
			0,
			count(*),
			round(sum(answered_time)/60)
		from radio_listen_session 
		where MONTH(datetime_start)='$month' and YEAR(datetime_start)='$year' 
		group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d')
	";
	#
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "select count(distinct DATE_FORMAT(datetime_start,'%d')) from radio_listen_session where MONTH(datetime_start)='$month' and YEAR(datetime_start)='$year'  ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by day";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "select DATE_FORMAT(datetime_start,'\%Y-\%m-\%d') from radio_listen_session  where MONTH(datetime_start)='$month' and YEAR(datetime_start)='$year'  group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d') order by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d') ";
	#
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_minutes";
    $datatable{html}{form}{data}{1}{yearmonth}	= "action";
    $datatable{html}{form}{data}{1}{value}	= $form{yearmonth};
    $datatable{html}{line_click_link}		= "";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "day,uids,calls,sessions,minutes";
    $datatable{html}{col_titles}			= "Date,Unique clients this day,Calls count,Listen count,Listen minutes";
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
	# add extra data
	foreach $id (keys %{$datatable{data}{values}}){
		$tmp_y = substr($id,0,4);
		$tmp_m = substr($id,5,2);
		$tmp_d = substr($id,8,2);
		# add owner commission
		#$sql = "
		#	select 1,1,sum(c.value)
		#	from 
		#		service_commission as c, 
		#		radio_listen_session as rl 
		#	where 
		#		c.id=rl.owner_commission_id and 
		#		rl.owner_commission_id is not null and 
		#		rl.datetime_stop is not null and 
		#		day(rl.datetime_start) = '$tmp_d' and 
		#		month(rl.datetime_start) = '$tmp_m' and 
		#		year(rl.datetime_start) = '$tmp_y'
		#";
		#%hash = database_select_as_hash($sql,"flag,value");
		#$datatable{data}{values}{$id}{commissions_owner} = ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value},2) : 0; 
		# add listen commission
		#$sql = "
		#	select 1,1,sum(c.value)
		#	from 
		#		service_commission as c, 
		#		radio_listen_session as rl 
		#	where 
		#		c.id=rl.listen_commission_id and 
		#		rl.listen_commission_id is not null and 
		#		rl.datetime_stop is not null and 
		#		day(rl.datetime_start) = '$tmp_d' and 
		#		month(rl.datetime_start) = '$tmp_m' and 
		#		year(rl.datetime_start) = '$tmp_y'
		#";
		#%hash = database_select_as_hash($sql,"flag,value");
		#$datatable{data}{values}{$id}{commissions_listen} = ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value},2) : 0; 
		# total calls
		$sql = "
			select 1,1,count(*)
			from 
				radio_listen_call 
			where 
				datetime_stop is not null and 
				day(datetime_start) = '$tmp_d' and 
				month(datetime_start) = '$tmp_m' and 
				year(datetime_start) = '$tmp_y'
		";
		%hash = database_select_as_hash($sql,"flag,value");
		$datatable{data}{values}{$id}{calls} = ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value},0) : 0; 
		# get uids
		$sql = "
			select 1,1,count(distinct ANI)
			from 
				radio_listen_call 
			where 
				datetime_stop is not null and 
				day(datetime_start) = '$tmp_d' and 
				month(datetime_start) = '$tmp_m' and 
				year(datetime_start) = '$tmp_y'
		";
		%hash = database_select_as_hash($sql,"flag,value");
		$datatable{data}{values}{$id}{uids} = ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value},0) : 0; 
	}
	$datatable_html = &datatable_get_html(\%datatable);
	#
	#==========================================
	# print page
	#==========================================
	$html_yearmonth_select = "";
	foreach $id (sort{$b <=> $a} keys %yearmonth_select) {
		$tmp = ($id eq $form{yearmonth}) ? " selected " : "";
		$html_yearmonth_select .= "<option $tmp value='$id'>".substr($id,0,4)."-".substr($id,4,2)."</option>";		
	}
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Radio minutes";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "reports.cgi";
    $t{breadcrumb}{1}{title}	= "Radio minutes";
    $t{breadcrumb}{1}{url}		= "";
	$t{content} = qq[
	
	<h3><b>$data{total_sessions_minutes}</b> minutes in $year-$month</h3>
	<div class=clear style=width:540px;>
	In this month, we have <b>$data{total_uids}</b> unique clients 
	that dial <b>$data{total_calls}</b> times (around $data{total_uids_x_calls} calls per client) 
	and listen <b>$data{total_sessions}</b> radio sessions 
	in <b>$data{total_sessions_minutes}</b> minutes at total.
	</div>
	<br>

	<form action=reports.cgi>
	Month: <select name=yearmonth><option value=''>Select month</option><option value=''> </option>$html_yearmonth_select</select> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
<!--
	Radio: <select name=radio_filter><option value=''>All radios</option><option value=''> </option>$select_radio</select><input name=radio_ext value='$form{radio_ext}' style='width:70px'> &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
-->
	<input type=submit value='Update'>
	<input type=hidden name=action value=radio_minutes>
	</form>

	<br>
	$datatable_html
	<br>
	&#187; Download CDRs (not finished)
	];
	&template_print("template.html",%t);
}
sub do_history_log(){
	#
	#---------------------------------
	# start 
	#---------------------------------
	($filter_type,$filter_1,$filter_2) = split(/\|/,&clean_str(substr($form{filter},0,100),"|:"));
	$user = clean_int(substr($form{user},0,100));
	$form{display} = ($form{display} eq "list") ? "list" : "overview";
	$select_user = "";
	$select_filter= "";
	$select_display= "";
	#
	#---------------------------------
	# get display
	#---------------------------------
	$select_display .= "<option value='overview' >Overview</a>";
	$tmp = ($form{display} eq "list") ? "selected" : "";
	$select_display .= "<option value='list' $tmp>List</a>";
	#
	#---------------------------------
	# get users
	#---------------------------------
	%hash = database_select_as_hash("select id,name,web_user,deleted from adm_users","name,web_user,deleted");
	foreach $id (sort{$hash{$a}{name} cmp $hash{$b}{name} } keys %hash) {
		$tmp1 = ($form{user} eq $id) ? "selected" : "";
		$tmp2 = ($hash{$id}{deleted} eq 0) ? $hash{$id}{web_user} : "DELETED";
		$select_user .= "<option value='$id' $tmp1>$hash{$id}{name} ($tmp2)</a>";
	}
	#
	#---------------------------------
	# get actions
	#---------------------------------
	%hash_1 = database_select_as_hash("SELECT distinct action_log_type.group,1 FROM action_log_type");
	%hash_2 = database_select_as_hash("SELECT id,action_log_type.group,title FROM action_log_type","group,title");
	foreach $group (sort{$a cmp $b} keys %hash_1){
		$filter_id 		= "group|$group";
		$tmp 			= ($form{filter} eq $filter_id) ? "selected" : "";
		$select_filter .= "<option $tmp value='$filter_id'>$group</a>";
		foreach $id (sort{$hash_2{$a}{title} cmp $hash_2{$b}{title}} keys %hash_2){
			if ($group ne $hash_2{$id}{group}) {next}
			$filter_id 		= "action|$id";
			$tmp 			= ($form{filter} eq $filter_id) ? "selected" : "";
			$select_filter .= "<option $tmp value='$filter_id'>&nbsp;&nbsp;&nbsp;$hash_2{$id}{title}</a>";
		}
		$select_filter .= "<option value=''>&nbsp;</a>";
	}
	#
	#---------------------------------
	# get calls type
	#---------------------------------
	#
	#---------------------------------
	# print start form
	#---------------------------------
	%t = ();
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; History log";
	$t{dic}{content}.= qq[
	
		<form action=$my_url>
		<input type=hidden name=action value=history_log>
	
		<fieldset ><legend>Filter</legend>
		<table border=0 colspan=0 cellpadding=2 cellspacing=0 class=clear>
			<td valign=top>
				Display:<br>
				<select name=display>
				$select_display
				</select>
			</td>
			<td valign=top>
				Action type:<br>
				<select name=filter>
				<option value=''>All actions</a>
				<option value=''>&nbsp;</a>
				$select_filter
				</select>
			</td>
			<td valign=top>
				NOC User:<br>
				<select name=user>
				<option value=''>Show all users</a>
				<option value=''>&nbsp;</a>
				$select_user
				<option value=''>&nbsp;</a>
				</select>
			</td>
			<td valign=top >
				&nbsp;<br>
				<button type=submit class="button button_positive button_search" name=submit_button>Search</button><br>
			</td>
			<td>
		</table>
		</fieldset>
		<br>
		
	];
	#
	#---------------------------------
	# overview
	#---------------------------------
	if ($form{display} eq "overview") {
			%adm_user_names = database_select_as_hash("select id,web_user from adm_users  ");
			$html_actions_summary = "";
			%data = ();


#			$sql_user = ($user ne "") ? " where adm_user_id='$user' " : "";
#			$sql = "SELECT 1,1,count(*) FROM action_log $sql_user ";
#			if ( ($filter_type eq "action_group") && ($filter_1 ne "") ){
#				$sql_user = ($user ne "") ? " action_log.adm_user_id='$user' and " : "";
#				$sql = "SELECT 1,1,count(*) FROM action_log,action_log_type where $sql_user action_log_type.group='$filter_1' and action_log_type.id=action_log.type ";
#			}
#			if ( ($filter_type eq "action") && ($filter_1 ne "") ){
#				$sql_user = ($user ne "") ? " adm_user_id='$user' and " : "";
#				$sql = "SELECT 1,1,count(*) FROM action_log where $sql_user type='$filter_1'";
#			}
#			%hash = database_select_as_hash($sql,"flag,value");
			#
			# get calls summary
#			if ($user eq "") {
#				%calls_statistics_strings = database_select_as_hash("select id,value from calls_log_info ");
#				$sql = "
#				SELECT 
#					DATE_FORMAT(calls_log.datetime_start,'%Y%m%d'),
#					IF(error_id>=0,1,0),
#					IF(billing_id>=0,1,0),
#					info_id,
#					count(*)
#				FROM calls_log
#				where 
#					calls_log.datetime_start>date_sub(now(),interval 7 day) 
#				group by 
#					DATE_FORMAT(calls_log.datetime_start,'%Y%m%d'),
#					IF(error_id>=0,1,0),
#					IF(billing_id>=0,1,0),
#					info_id
#				";
#				%hash = &database_select_as_hash_with_auto_key($sql,"date,is_error,was_billed,string_id,qtd");
#				foreach $id (keys %hash){
#					$tmp = (exists($calls_statistics_strings{$hash{$id}{string_id}})) ? " - $calls_statistics_strings{$hash{$id}{string_id}}" : "";
#					$t = "Approved but not billed";
#					$t = ($hash{$id}{is_error} eq 1) ? "Rejected$tmp" : $t;
#					$t = ($hash{$id}{was_billed} eq 1) ? "Approved and billed" : $t;
#					#$t = ($hash{$id}{} eq 1) ? "" : $t;
#					$g = "Calls";
#					$d = $hash{$id}{date};
#					$data{values}{$g}{$t}{$d}	+= $hash{$id}{qtd};
#					$data{dates}{$d} 			+= $hash{$id}{qtd};
#				}
#			}
			#
			# get history summary
			$user_sql 	= ($user eq "") ? "" : " action_log.adm_user_id='$user' and ";
			$group_sql 	= ( ($filter_type eq "group") && ($filter_1 ne "") )   ? " action_log_type.group='$filter_1' and " : "";
			$action_sql	= ( ($filter_type eq "action") && ($filter_1 ne "") )  ? " action_log.type='$filter_1' and " : "";
			$sql = "
				SELECT
					DATE_FORMAT(action_log.date,'%Y%m%d'),
					action_log_type.id,
					action_log_type.group,
					action_log_type.title,
					count(*)
				FROM 
					action_log,
					action_log_type
				where
					$user_sql
					$group_sql
					$action_sql
					action_log.type = action_log_type.id and 
					action_log.date>date_sub(now(),interval 7 day) 
				group by 
					DATE_FORMAT(action_log.date,'%Y%m%d'),action_log_type.id,action_log_type.group,action_log_type.title
			";
			%hash = &database_select_as_hash_with_auto_key($sql,"date,id,group,title,qtd");
			foreach $id (keys %hash){
				$a = $hash{$id}{title};
				$t = $hash{$id}{title};
				$g = $hash{$id}{group};
				$d = $hash{$id}{date};
				$data{ids}{$g}{$t}				 = $hash{$id}{id};
				$data{values}{$g}{$t}{$d}		+= $hash{$id}{qtd};
				$data{dates}{$d} 				+= $hash{$id}{qtd};
				$data{titles}{$hash{$id}{id}} 	 = "$g - $t";
			}
			#
			# monta html
			$html_actions_summary = "";
			$g_id = 0;
			foreach $g (sort{$a cmp $b} keys %{$data{values}}){
				#$g_rowspan = keys %{$data{values}{$g}};
				$g_id++;
				$html_actions_summary .= "<tbody><tr><td class=group_title colspan=20><b><a href=\"javascript:MyDisplayTbody('group$g_id')\">+</a>&nbsp;<a href='$my_url?action=history_log&display=list&user=$form{user}&filter=group|$g'>$g</a></b></td></tr></tbody>";
				$html_actions_summary .= "<tbody id=group$g_id>";
				foreach $t (sort{$a cmp $b} keys %{$data{values}{$g}}){
					$html_actions_summary .= "<tr>";
					$a_id = $data{ids}{$g}{$t};
					$html_actions_summary .= "<td style=padding-left:20px;><a href='$my_url?action=history_log&display=list&user=$form{user}&filter=action|$a_id'>$t</a></td>";
					foreach $d (sort{$b <=> $a} keys %{$data{dates}}){
						$v = format_number($data{values}{$g}{$t}{$d},0);
						$v = ($data{values}{$g}{$t}{$d} eq "") ? "&nbsp;" : $v;
						$html_actions_summary .= "<td class=ar >$v</td>";
					}
					$html_actions_summary .= "</tr>";
				}
				$html_actions_summary .= "</tbody>";
			}
		
		
			$t{dic}{content}.= qq[
			<style>
			.group_title{
			height:25;  
			background-color: #ebeadb;
			margin:0; 
			padding:0; 
			border:0;
			font-size: 12px;
			white-space: nowrap; 
			padding-left:5px;
			padding-right:5px;
			padding-top:2px;
			padding-bottom:2px;
			color:#000000;
			border-top:1px solid #f0f0f0; 
			border-left:1px solid #f0f0f0; 
			border-right:1px solid #c0c0c0; 
			border-bottom:1px solid #c0c0c0;
			}
			</style>
			<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% onclick="sortColumn(event)">
				<thead>
					<tr>
					<td ><h1>History log summary</h1></td>
					<td >Today</td>
					<td >-1 day</td>
					<td >-2 days</td>
					<td >-3 days</td>
					<td >-4 days</td>
					<td >-5 days</td>
					<td >-6 days</td>
					<td >-7 days</td>
					</tr>
				</thead>
				$html_actions_summary
			</table>
			&nbsp;
			];	
	} 
	#
	#---------------------------------
	# list actions ($filter_type,$filter_1,$filter_2)
	#---------------------------------
	if 	($form{display} eq "list")	{
			#
			#---------------------------------------------------
			# total
			#---------------------------------------------------
			$sql_user = ($user ne "") ? " where adm_user_id='$user' " : "";
			$sql = "SELECT 1,1,count(*) FROM action_log $sql_user ";
			if ( ($filter_type eq "group") && ($filter_1 ne "") ){
				$sql_user = ($user ne "") ? " action_log.adm_user_id='$user' and " : "";
				$sql = "SELECT 1,1,count(*) FROM action_log,action_log_type where $sql_user action_log_type.group='$filter_1' and action_log_type.id=action_log.type ";
			}
			if ( ($filter_type eq "action") && ($filter_1 ne "") ){
				$sql_user = ($user ne "") ? " adm_user_id='$user' and " : "";
				$sql = "SELECT 1,1,count(*) FROM action_log where $sql_user type='$filter_1'";
			}
			%hash = database_select_as_hash($sql,"flag,value");
			#
			#---------------------------------------------------
			# calcula paginas
			#---------------------------------------------------
			$quantity 		= ($hash{1}{flag} eq 1) ? $hash{1}{value} : 1;
			$page_size		= clean_int($form{page_size});
			$page_size		= ($page_size eq "") ? 10 : $page_size;
			$page_min		= 1;
			$page_max		= int(($quantity-1)/$page_size)+1;
			$page_max		= ($page_max<$page_min) ? $page_min : $page_max;
			$page 			= clean_int($form{history_page});
			$page 			= ($form{next} eq 1) ? $page+1 : $page;
			$page 			= ($form{previous} eq 1) ? $page-1 : $page;
			$page 			= ($page<$page_min) ? $page_min : $page;
			$page 			= ($page>$page_max) ? $page_max : $page;
			$page_sql_start	= ($page-1)*$page_size;
			$page_sql_stop	= $page_size;
			#
			#---------------------------------------------------
			# pega dados 
			#---------------------------------------------------
			$ids_action_log = "";
			$ids_service_id	= "";
			%data_action_log= ();
			%data_service_id= ();
			$sql_user = ($user ne "") ? " where adm_user_id='$user' and " : "";
			$sql = "
			SELECT id,unix_timestamp(date),service_id
			FROM action_log
			$sql_user 
			order by id desc
			limit $page_sql_start,$page_sql_stop
			";
			if ( ($filter_type eq "group") && ($filter_1 ne "") ){
				$sql_user = ($user ne "") ? " action_log.adm_user_id='$user' and " : "";
				$sql = "
				SELECT action_log.id,unix_timestamp(action_log.date),action_log.service_id
				FROM action_log,action_log_type
				where $sql_user action_log_type.group='$filter_1' and action_log_type.id=action_log.type 
				order by action_log.id desc
				limit $page_sql_start,$page_sql_stop
				";
			}
			if ( ($filter_type eq "action") && ($filter_1 ne "") ){
				$sql_user = ($user ne "") ? " action_log.adm_user_id='$user' and " : "";
				$sql = "
				SELECT action_log.id,unix_timestamp(action_log.date),action_log.service_id
				FROM action_log
				where $sql_user action_log.type='$filter_1'
				order by action_log.id desc
				limit $page_sql_start,$page_sql_stop
				";
			}
			%data = database_select_as_hash($sql,"date,service_id");
			foreach $id (keys %data){
				$ids_action_log .= ($id ne "") ? "$id," : "";
				$ids_service_id	.= ($data{$id}{service_id} ne "") ? "$data{$id}{service_id}," : "";
			}
			if ($ids_service_id ne "") {
				$ids_service_id = substr($ids_service_id,0,-1);
				$sql = "
				SELECT
					service.id,
					service.name,
					service.email,
					service_status.name
				FROM
					service, service_status
				where
					service.id in ($ids_service_id)
					and service.status=service_status.id
				";
				%data_service_id = &database_select_as_hash($sql,"name,email,status");
			}
			%data_action_log	= &action_history_get_info(substr($ids_action_log,0,-1),"no_date,no_user"); 
			#
			#---------------------------------------------------
			# monta o html
			#---------------------------------------------------
			$html_history = "";
			foreach $action_log_id (sort{$data{$b}{date} <=> $data{$a}{date} } keys %data) {
				$html_history .= "<tr>";
				$html_history .= "<td valign=top style=white-space:nowrap;>".&format_time_gap($data{$action_log_id}{date})."</td>";
				if ($data_action_log{$action_log_id}{user} ne "") {
					$html_history .= "<td valign=top >$data_action_log{$action_log_id}{user}</td>";
				} else {
					$html_history .= "<td valign=top ><font color=#c0c0c0>(nobody)</font></td>";
				}
				$service_id = $data{$action_log_id}{service_id};
				if (exists($data_service_id{$service_id})) {
					$html_history .= "
					<td valign=top >
					<a href=services.cgi?action=view&service_id=$service_id>$service_id - 
					$data_service_id{$service_id}{name} ($data_service_id{$service_id}{email})
					</a>
					</td>
					";
				} else {
					$html_history .= "<td valign=top ><font color=#c0c0c0>(no&nbsp;service)</font></td>";
				}
				$html_history .= "<td valign=top >$data_action_log{$action_log_id}{text_simple}</td>";
			}
			#
			#---------------------------------------------------
			# imprime pagina
			#---------------------------------------------------
			$html_pg_list = "";
			foreach($page_min..$page_max) {
				if  ( ($_ eq $page_min) || ($_ eq $page_max) || (int($_/100) eq ($_/100) ) ||  ( ($page>($_-100)) && ($page<($_+100)) ) ) {
					$tmp = ($_ eq $page) ? "selected" : ""; 
					$html_pg_list .= "<option $tmp value=$_>Page: $_ of $page_max</option>";
				}
			}
			$html_pgsize_list = "";
			$tmp = (15 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=10>10 itens per page</option>";
			$tmp = (30 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=30>30 itens per page</option>";
			$tmp = (100 eq $form{page_size}) ? "selected" : ""; $html_pgsize_list .= "<option $tmp value=100>100 itens per page</option>";
			$t{dic}{content}	.= qq[
					<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% style=margin-top:13px; onclick="sortColumn(event)">
						<thead>
							<tr>
							<td colspan=4><h1>History log</h1></td>
							</tr>
							<tr>
							<td >Date</td>
							<td >NOC</td>
							<td >Service</td>
							<td >Action</td>
							</tr>
						</thead>
						<tbody >
							$html_history 
						</tbody>
						<tfoot>
							<tr><td colspan=8 >
							<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
								<td ><button type=submit name=previous value=1><img src=/design/icons/bullet_arrow_left.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
								<td ><select name=history_page onchange="this.form.submit()">$html_pg_list</select></td>
								<td ><select name=page_size onchange="document.forms[0].submit()">$html_pgsize_list</select></td>
								<td ><button type=submit name=next value=1><img src=/design/icons/bullet_arrow_right.png hspace=0 vspace=0 border=0 width=16 height=16></button></td>
							</table>
							</td></tr>
						</tfoor>
					</table>
			];


	}
	#
	#---------------------------------
	# end page
	#---------------------------------
	$t{dic}{content}.= qq[
		</form>
	];
	&template_print("template.html",%t);
}
sub do_radio_overview(){
	#
	#==========================================
	# start
	#==========================================
	$prefix = &clean_int($form{prefix});
	%t = ();
	#	
	#==========================================
	# plota duration days
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and radio_extension='$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(datetime_start,'\%Y-\%m-\%d'),
		sum( IF(answered_time<15,1,0) ),
		sum( IF(answered_time<300,1,0) ),
		sum( IF(answered_time<1800,1,0) ),
		sum( IF(answered_time>=1800,1,0) )
	FROM radio_listen_session
	where 
		datetime_start >date_sub(now(),interval 60 day) 
		and datetime_stop is not null
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d')
	";
	%data = &database_select_as_hash($sql,"s,m1,m2,l");
	%plot = ();
	$plot{uid} = "60days";
	$plot{x} = 450;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "15 sec calls";
	$plot{series}{1}{color} = "ff0000";
	$plot{series}{2}{name} 	= "5 min calls";
	$plot{series}{2}{color} = "ff6600";
	$plot{series}{3}{name} 	= "30 min calls";
	$plot{series}{3}{color} = "f8d322";
	$plot{series}{4}{name} 	= "Long calls";
	$plot{series}{4}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{s};
		$plot{data}{$slice_index}{2} += $data{$slice}{m1}-$data{$slice}{s};
		$plot{data}{$slice_index}{3} += $data{$slice}{m2}-$data{$slice}{m1};
		$plot{data}{$slice_index}{4} += $data{$slice}{l};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>30) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_duration_days = $plot{html};
	#	
	#==========================================
	# plota duration months
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and radio_extension='$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(datetime_start,'\%Y-\%m') as dt,
		sum( IF(answered_time<15,1,0) ) s15,
		sum( IF(answered_time<300,1,0) ),
		sum( IF(answered_time<1800,1,0) ) m30,
		sum( IF(answered_time>=1800,1,0) ) m60beyond
	FROM radio_listen_session
	where 
		datetime_start >date_sub(now(),interval 600 day) 
		and datetime_stop is not null
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m')
	";
	%data = &database_select_as_hash($sql,"s,m1,m2,l");
	%plot = ();
	$plot{uid} = "2years";
	$plot{x} = 250;
	$plot{y} = 255;
	$plot{series}{1}{name} 	= "15 sec calls";
	$plot{series}{1}{color} = "ff0000";
	$plot{series}{2}{name} 	= "5 min calls";
	$plot{series}{2}{color} = "ff6600";
	$plot{series}{3}{name} 	= "30 min calls";
	$plot{series}{3}{color} = "f8d322";
	$plot{series}{4}{name} 	= "Long calls";
	$plot{series}{4}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{s};
		$plot{data}{$slice_index}{2} += $data{$slice}{m1}-$data{$slice}{s};
		$plot{data}{$slice_index}{3} += $data{$slice}{m2}-$data{$slice}{m1};
		$plot{data}{$slice_index}{4} += $data{$slice}{l};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_duration_monts = $plot{html};
	#	
	#==========================================
	# plota minutes days
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and radio_extension='$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(datetime_start,'\%Y-\%m-\%d'),
		sum(answered_time)
	FROM radio_listen_session
	where 
		datetime_start >date_sub(now(),interval 90 day) 
		and datetime_stop is not null
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d')
	";
	%data = &database_select_as_hash($sql,"sec");
	$d1 = "";
	$d2 = "";
	foreach $slice (sort{$b cmp $a} keys %data) {
		$d1 = ($d1 eq "") ? substr($slice,0,7) : $d1;
		if ($d1 ne substr($slice,0,7)) {
			$d2 = substr($slice,0,7);
			last;
		}
	}
	%plot = ();
	$plot{uid} = "mindays";
	$plot{x} = 400;
	$plot{y} = 200;
	$plot{series}{2}{name} 	= "$d1 Minutes";
	$plot{series}{2}{color} = "92c23e";
	$plot{series}{1}{name} 	= "$d2 Minutes";
	$plot{series}{1}{color} = "f8d322";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{2} = int($data{$d1."-".$dd}{sec}/60);
		$plot{data}{$slice_index}{1} = int($data{$d2."-".$dd}{sec}/60);
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSArea2D(%plot);
	$plot_min_days = $plot{html};
	#	
	#==========================================
	# plota minutes hours
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : "and radio_extension='$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(datetime_start,'\%Y-\%m-\%d: \%H'),
		sum(answered_time)
	FROM radio_listen_session 
	where 
		datetime_start >date_sub(now(),interval 7 day) 
		and datetime_stop is not null
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d: \%H')
	";
	%data = &database_select_as_hash($sql,"sec");
	$d1 = "";
	$d2 = "";
	foreach $slice (sort{$b cmp $a} keys %data) {
		$d1 = ($d1 eq "") ? substr($slice,0,10) : $d1;
		if ($d1 ne substr($slice,0,10)) {
			$d2 = substr($slice,0,10);
			last;
		}
	}
	%plot = ();
	$plot{uid} = "minhours";
	$plot{x} = 300;
	$plot{y} = 200;
	$plot{series}{2}{name} 	= "$d1 Minutes";
	$plot{series}{2}{color} = "92c23e";
	$plot{series}{1}{name} 	= "$d2 Minutes";
	$plot{series}{1}{color} = "f8d322";
	$slice_index = 1;
	@hours = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23);
	foreach $h (@hours) {
		$hh = substr("00".$h,-2,2);
		$plot{data}{$slice_index}{2} = int($data{"$d1: $hh"}{sec}/60);
		$plot{data}{$slice_index}{1} = int($data{"$d2: $hh"}{sec}/60);
		$plot{slices}{$slice_index} = $hh;
		$slice_index++;
	}
	%plot = &plot_MSArea2D(%plot);
	$plot_min_hour = $plot{html};
	#
	#===========================================================================
    # print page
	#===========================================================================
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Radio overview";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "reports.cgi";
    $t{breadcrumb}{1}{title}	= "Radio overview";
    $t{breadcrumb}{1}{url}		= "";
	$t{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<fieldset style="width:730px;"><legend>Filter charts by</legend>
	<form action=$my_url>
	Enter radio extension:<input name=prefix value="$prefix"><button type=submit>Refresh</button>
	<input type=hidden name=action value=radio_overview>
	</form>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Calls minutes</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_min_hour</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_min_days</td>
	</table>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Call count grouped by call duration</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_duration_days</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_duration_monts</td>
	</table>
	</fieldset>
	<br>

	];
    &template_print("template.html",%t);
	
}
sub OLD_do_radio_overview(){
  #
	#==========================================
	# start
	#==========================================
	#
	################################################################
	################################################################
	#$prefix = $form{prefix};
	# never trust form data to add into sql.. Sql inject enabled!!!
	# we need clean...we have &database_scape_sql to do this.. but... because
	# %Y-%m-%d format got parsed and fucked by database_scape_sql, we need do by hand
	$prefix = substr(clean_int($form{prefix}),0,100);
	# now we have a number only and limit size to 100 digits
	# no way to people inject sql onthis data
	#
	################################################################
	################################################################
	#
	%t = ();
	#	
	#==========================================
	# plota duration days
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : " and radio_extension = '$prefix' ";
	$sql = "
	SELECT  
		DATE_FORMAT(datetime_start,'\%Y-\%m-\%d'),
		sum( IF(answered_time<15,1,0) ),
		sum( IF(answered_time<300,1,0) ),
		sum( IF(answered_time<1800,1,0) ),
		sum( IF(answered_time>=1800,1,0) )
	FROM radio_listen_session  
	where 
		datetime_start >date_sub(now(),interval 60 day) 
		and datetime_stop is not null	
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d')
	";
warning(clean_str($sql,"'\"()\%<>=,_"));
	%data = &database_select_as_hash($sql,"s,m1,m2,l");
	%plot = ();
	$plot{uid} = "60days";
	$plot{x} = 450;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "15 sec calls";
	$plot{series}{1}{color} = "ff0000";
	$plot{series}{2}{name} 	= "5 min calls";
	$plot{series}{2}{color} = "ff6600";
	$plot{series}{3}{name} 	= "30 min calls";
	$plot{series}{3}{color} = "f8d322";
	$plot{series}{4}{name} 	= "Long calls";
	$plot{series}{4}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{s};
		$plot{data}{$slice_index}{2} += $data{$slice}{m1}-$data{$slice}{s};
		$plot{data}{$slice_index}{3} += $data{$slice}{m2}-$data{$slice}{m1};
		$plot{data}{$slice_index}{4} += $data{$slice}{l};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>30) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_duration_days = $plot{html};
	#	
	#==========================================
	# plota duration months
	#==========================================
	$data = ();
 	$sql_prefix = ($prefix eq "") ? "" : " and radio_extension  = '$prefix' ";
	$sql = "
 	SELECT 
		DATE_FORMAT(datetime_start,'\%Y-\%m') as dt,
 		sum( IF(answered_time<15,1,0) ) s15,
		sum( IF(answered_time<300,1,0) ),
 		sum( IF(answered_time<1800,1,0) ) m30,
		sum( IF(answered_time>=1800,1,0) ) m60beyond
	FROM radio_listen_session  
	where 
		datetime_start >date_sub(now(),interval 600 day) 
		and datetime_stop is not null	 
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m')
	";
	%data = &database_select_as_hash($sql,"s,m1,m2,l");
	%plot = ();
	$plot{uid} = "2years";
	$plot{x} = 250;
	$plot{y} = 255;
	$plot{series}{1}{name} 	= "15 sec calls";
	$plot{series}{1}{color} = "ff0000";
	$plot{series}{2}{name} 	= "5 min calls";
	$plot{series}{2}{color} = "ff6600";
	$plot{series}{3}{name} 	= "30 min calls";
	$plot{series}{3}{color} = "f8d322";
	$plot{series}{4}{name} 	= "Long calls";
	$plot{series}{4}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$b cmp $a} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{s};
		$plot{data}{$slice_index}{2} += $data{$slice}{m1}-$data{$slice}{s};
		$plot{data}{$slice_index}{3} += $data{$slice}{m2}-$data{$slice}{m1};
		$plot{data}{$slice_index}{4} += $data{$slice}{l};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>12) {last}
	}
	%plot = &plot_StackedColumn2D(%plot);
	$plot_duration_monts = $plot{html};
	#==========================================
	# plota minutes days
	#==========================================
	$data = ();
	$sql = "
	SELECT 
		DATE_FORMAT(datetime_start,'\%Y-\%m-\%d'),
		sum(answered_time)
	FROM radio_listen_session   
	where 
		datetime_start >date_sub(now(),interval 90 day) 
		and datetime_stop is not null
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d')
	";
	%data = &database_select_as_hash($sql,"sec");
	$d1 = "";
	$d2 = "";
	foreach $slice (sort{$b cmp $a} keys %data) {
		$d1 = ($d1 eq "") ? substr($slice,0,7) : $d1;
		if ($d1 ne substr($slice,0,7)) {
			$d2 = substr($slice,0,7);
			last;
		}
	}
	%plot = ();
	$plot{uid} = "mindays";
	$plot{x} = 400;
	$plot{y} = 200;
	$plot{series}{2}{name} 	= "$d1 Minutes";
	$plot{series}{2}{color} = "92c23e";
	$plot{series}{1}{name} 	= "$d2 Minutes";
	$plot{series}{1}{color} = "f8d322";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{2} = int($data{$d1."-".$dd}{sec}/60);
		$plot{data}{$slice_index}{1} = int($data{$d2."-".$dd}{sec}/60);
		$plot{slices}{$slice_index} = $dd;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$plot_min_days = $plot{html};
	#	
	#==========================================
	# plota minutes hours
	#==========================================
	$data = ();
 	$sql_prefix = ($prefix eq "") ? "" : " and radio_extension = '$prefix' ";
	$sql = "
	SELECT 
		DATE_FORMAT(datetime_start,'\%Y-\%m-\%d: \%H'),
		sum(answered_time)
	FROM radio_listen_session   
	where 
		datetime_start >date_sub(now(),interval 7 day) 
		and datetime_stop is not null  
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d: \%H')
	";
	%data = &database_select_as_hash($sql,"sec");
	$d1 = "";
	$d2 = "";
	foreach $slice (sort{$b cmp $a} keys %data) {
		$d1 = ($d1 eq "") ? substr($slice,0,10) : $d1;
		if ($d1 ne substr($slice,0,10)) {
			$d2 = substr($slice,0,10);
			last;
		}
	}
	%plot = ();
	$plot{uid} = "minhours";
	$plot{x} = 300;
	$plot{y} = 200;
	$plot{series}{2}{name} 	= "$d1 Minutes";
	$plot{series}{2}{color} = "92c23e";
	$plot{series}{1}{name} 	= "$d2 Minutes";
	$plot{series}{1}{color} = "f8d322";
	$slice_index = 1;
	@hours = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23);
	foreach $h (@hours) {
		$hh = substr("00".$h,-2,2);
		$plot{data}{$slice_index}{2} = int($data{"$d1: $hh"}{sec}/60);
		$plot{data}{$slice_index}{1} = int($data{"$d2: $hh"}{sec}/60);
		$plot{slices}{$slice_index} = $hh;
		$slice_index++;
	}
	%plot = &plot_MSColumn2D(%plot);
	$plot_min_hour = $plot{html};
	#	plot_StackedColumn2D
	#
 	#==========================================
	# top 100 extensions played counts
	#==========================================
	$data = ();
	$sql_prefix = ($prefix eq "") ? "" : " and radio_extension = '$prefix' ";
	$sql = "
	SELECT 
		radio_extension,
		count(*) as counts,
		sum(answered_time) as seconds 
	FROM radio_listen_session    
	where 
		radio_extension <>'' 
		and datetime_start >date_sub(now(),interval 90 day) 
		and datetime_stop is not null  

		group by radio_extension 
	order by sum(answered_time) desc 
	limit 0,50
	";
	%data = &database_select_as_hash($sql,"counts,seconds");
	%plot = ();
	$plot{uid} = "top100_extens";
	$plot{x} = 720;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= "$d1 Counts";
	$plot{series}{1}{color} = "ff0000";
	$plot{series}{2}{name} 	= "$d2 Minutes";
	$plot{series}{2}{color} = "ff6600";
#	$plot{series}{3}{name} 	= "30 min calls";
#	$plot{series}{3}{color} = "f8d322";
#	$plot{series}{4}{name} 	= "Long calls";
#	$plot{series}{4}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$data{$b}{seconds} <=> $data{$a}{seconds}} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{counts};
		$plot{data}{$slice_index}{2} += $data{$slice}{seconds}/60 ;
	#	$plot{data}{$slice_index}{3} += $data{$slice}{m2}-$data{$slice}{m1};
	#	$plot{data}{$slice_index}{4} += $data{$slice}{l};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>100) {last}
	}
	# plot_MSColumn2D
	%plot = &plot_StackedColumn2D(%plot);
	$plot_top100_extens = $plot{html};
	 
	#	
 	#==========================================
	# filter by radio station extension
	#==========================================
	$data = ();
	$exten = $form{exten};
	$exten = &database_escape($exten) ;
	$sql_prefix = ($exten eq "") ? "" : " and radio_extension = '$exten' ";
	$sql = "
	SELECT 
		DATE_FORMAT(datetime_start,'\%Y-\%m-\%d'),
		count(id) as counts,
		sum(answered_time) as seconds 
	FROM radio_listen_session 
	where 
		datetime_start >date_sub(now(),interval 90 day) 
		and datetime_stop is not null		 
		$sql_prefix 
	group by DATE_FORMAT(datetime_start,'\%Y-\%m-\%d')
	"; 
	
	%data = &database_select_as_hash($sql,"counts,seconds");
	%plot = ();
	$plot{uid} = "single_radio";
	$plot{x} = 720;
	$plot{y} = 250;
	$plot{series}{1}{name} 	= $exten." $d1 Counts";
	$plot{series}{1}{color} = "ff0000";
	$plot{series}{2}{name} 	= $exten." $d2 Minutes";
	$plot{series}{2}{color} = "ff6600";
#	$plot{series}{3}{name} 	= "30 min calls";
#	$plot{series}{3}{color} = "f8d322";
#	$plot{series}{4}{name} 	= "Long calls";
#	$plot{series}{4}{color} = "92c23e";
	$slice_index = 1;
	foreach $slice (sort{$data{$b}{seconds} <=> $data{$a}{seconds}} keys %data) {
		$plot{data}{$slice_index}{1} += $data{$slice}{counts};
		$plot{data}{$slice_index}{2} += $data{$slice}{seconds}/60.00 ;
	#	$plot{data}{$slice_index}{3} += $data{$slice}{m2}-$data{$slice}{m1};
	#	$plot{data}{$slice_index}{4} += $data{$slice}{l};
		$plot{slices}{$slice_index} = $slice;
		$slice_index++;
		if ($slice_index>100) {last}
	}
	# plot_MSColumn2D
	%plot = &plot_StackedColumn2D(%plot);
	$plot_singleradio = $plot{html};
	 
	#
	#
	#==========================================
	# print page
	#==========================================
	%t = ();
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Radios overview";
	$t{dic}{content} = qq[
	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<fieldset style="width:730px;"><legend>Latest 90 days Radio Activity</legend>
	
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_singleradio</td>
	</table>
	<br>
	<form action=$my_url>
	Input Radio Station Extension:<input name=exten value="$exten"><button type=submit>Refresh</button>
	<input type=hidden name=action value=radio_overview>
	</form>
	</fieldset>
	<br>

	<fieldset style="width:730px;"><legend>Calls minutes</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_min_hour</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_min_days</td>
	</table>
	</fieldset>
	<br> 
	<!--fieldset style="width:730px;"><legend>Call count grouped by call duration</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_duration_days</td><td>&nbsp;&nbsp;&nbsp;&nbsp;</td><td valign=top>$plot_duration_monts</td>
	</table>
	</fieldset-->
	<br>
 	<fieldset style="width:730px;"><legend>Top radios(and play counts,minutes)</legend><br>
	<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear>
	<td valign=top>$plot_top100_extens</td>
	</table>
	</fieldset>
	<br>
	<br>
	];
	&template_print("template.html",%t);
 
}
sub do_radio_top_radio(){
    #
    #-------------------------------
    # prepare year/month select and values
    #-------------------------------
	%yearmonth_select = &database_select_as_hash("SELECT distinct DATE_FORMAT(datetime_start,'\%Y\%m'),1 FROM radio_listen_session ");
	%hash = database_select_as_hash("SELECT 1,1,max(DATE_FORMAT(datetime_start,'\%Y\%m')) FROM radio_listen_session ","flag,value");
	$form{yearmonth} = clean_int($form{yearmonth});
	$form{yearmonth} = (length($form{yearmonth}) ne 6) ? "" : $form{yearmonth};
	$form{yearmonth} = ( ($form{yearmonth} eq "") && ($hash{1}{flag} eq 1) ) ? $hash{1}{value} : $form{yearmonth};
	$form{yearmonth} = (exists($yearmonth_select{$form{yearmonth}})) ? $form{yearmonth} : "";
	$year	= substr($form{yearmonth},0,4);
	$month	= substr($form{yearmonth},4,2);
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "extension,title,minutes"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT 
			r.extension,
			r.extension,
			r.title,
			0
		FROM 
			radio_station as r 
		where 
			r.extension in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "
		SELECT count(distinct radio_extension) 
		FROM radio_listen_session 
		where  datetime_stop is not null and MONTH(datetime_stop)='$month' and YEAR(datetime_stop)='$year'  
	";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Top radios on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "
		SELECT r.extension 
		FROM radio_listen_session as rs, radio_station as r
		where rs.datetime_stop is not null and MONTH(rs.datetime_stop)='$month' and YEAR(rs.datetime_stop)='$year' and r.extension= rs.radio_extension
		group by r.extension 
		order by sum(rs.answered_time) desc 
		limit #LIMIT_1#,#LIMIT_2# 
	";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_top_radio";
    $datatable{html}{line_click_link}		= "";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "extension,title,minutes";
    $datatable{html}{col_titles}			= "Extension,Radio title,Minutes";
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
	# add extra data
	foreach $id (keys %{$datatable{data}{values}}){
		$tmp_extension	= $datatable{data}{values}{$id}{extension};
		$tmp_service_id	= $datatable{data}{values}{$id}{service_id};
		#
		# add minutes
		$sql = "
		SELECT 1,1,sum(answered_time) 
		FROM radio_listen_session 
		WHERE datetime_stop is not null and MONTH(datetime_stop)='$month' and YEAR(datetime_stop)='$year' and radio_extension='$tmp_extension'
		";
		%hash = database_select_as_hash($sql,"flag,value");
		$datatable{data}{values}{$id}{minutes} = ($hash{1}{flag} eq 1) ? &format_number(int($hash{1}{value}/60),0) : 0; 
	}
	$datatable_html = &datatable_get_html(\%datatable);
	#
	#===========================================================================
    # print page
	#===========================================================================
	$html_yearmonth_select = "";
	foreach $id (sort{$b <=> $a} keys %yearmonth_select) {
		$tmp = ($id eq $form{yearmonth}) ? " selected " : "";
		$html_yearmonth_select .= "<option $tmp value='$id'>".substr($id,0,4)."/".substr($id,4,2)."</option>";		
	}
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Top radios in $year/$month";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "reports.cgi";
    $t{breadcrumb}{1}{title}	= "Top radios in $year/$month";
    $t{breadcrumb}{1}{url}		= "";
    $t{content}	= qq[


	<form action=reports.cgi>
	Month: <select name=yearmonth><option value=''>Select month</option><option value=''> </option>$html_yearmonth_select</select> &nbsp;&nbsp;&nbsp;
	<input type=submit value='Update'>
	<input type=hidden name=action value=radio_top_radio>
	</form>
	<br>

    $datatable_html
    ];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%datatable)."</pre>";
    &template_print("template.html",%t);
	
}
sub do_radio_top_listen(){
    #
    #-------------------------------
    # prepare year/month select and values
    #-------------------------------
	%yearmonth_select = &database_select_as_hash("SELECT distinct DATE_FORMAT(datetime_start,'\%Y\%m'),1 FROM radio_listen_session ");
	%hash = database_select_as_hash("SELECT 1,1,max(DATE_FORMAT(datetime_start,'\%Y\%m')) FROM radio_listen_session ","flag,value");
	$form{yearmonth} = clean_int($form{yearmonth});
	$form{yearmonth} = (length($form{yearmonth}) ne 6) ? "" : $form{yearmonth};
	$form{yearmonth} = ( ($form{yearmonth} eq "") && ($hash{1}{flag} eq 1) ) ? $hash{1}{value} : $form{yearmonth};
	$form{yearmonth} = (exists($yearmonth_select{$form{yearmonth}})) ? $form{yearmonth} : "";
	$year	= substr($form{yearmonth},0,4);
	$month	= substr($form{yearmonth},4,2);
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "ani,calls,minutes"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT 
			ani,
			ani,
			count(*),
			sum(answered_time) 
		FROM 
			radio_listen_call  
		where 
			ani in (#SELECTED_IDS#) 
		group by ani 
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "
		SELECT count(distinct ani) 
		FROM radio_listen_call 
		where  datetime_stop is not null and MONTH(datetime_stop)='$month' and YEAR(datetime_stop)='$year'  
	";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Top listen minutes ANI on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "
		SELECT ani 
		FROM radio_listen_call 
		where datetime_stop is not null and MONTH(datetime_stop)='$month' and YEAR(datetime_stop)='$year' 
		group by ani 
		order by sum(answered_time) desc 
		limit #LIMIT_1#,#LIMIT_2# 
	";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Top listen call count ANI on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "
		SELECT ani 
		FROM radio_listen_call 
		where datetime_stop is not null and MONTH(datetime_stop)='$month' and YEAR(datetime_stop)='$year' 
		group by ani 
		order by count(*) desc 
		limit #LIMIT_1#,#LIMIT_2# 
	";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_top_listen";
    $datatable{html}{line_click_link}		= "";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "ani,calls,minutes";
    $datatable{html}{col_titles}			= "Listener ANI,Calls count,Minutes";
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
	$datatable_html = &datatable_get_html(\%datatable);
	#
	#===========================================================================
    # print page
	#===========================================================================
	$html_yearmonth_select = "";
	foreach $id (sort{$b <=> $a} keys %yearmonth_select) {
		$tmp = ($id eq $form{yearmonth}) ? " selected " : "";
		$html_yearmonth_select .= "<option $tmp value='$id'>".substr($id,0,4)."/".substr($id,4,2)."</option>";		
	}
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Top listen ANI in $year/$month";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "reports.cgi";
    $t{breadcrumb}{1}{title}	= "Top listen ANI in $year/$month";
    $t{breadcrumb}{1}{url}		= "";
    $t{content}	= qq[

	<form action=reports.cgi>
	Month: <select name=yearmonth><option value=''>Select month</option><option value=''> </option>$html_yearmonth_select</select> &nbsp;&nbsp;&nbsp;
	<input type=submit value='Update'>
	<input type=hidden name=action value=radio_top_listen>
	</form>
	<br>

    $datatable_html
    ];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%datatable)."</pre>";
    &template_print("template.html",%t);
	
}
sub do_radio_now(){
    #
    #-------------------------------
    # get active radio sessions
    #-------------------------------
    $sql = "show processlist";
	%hash = &database_select_as_hash($sql,"user,host,db,command,time,state,info");
	$data = ();
	$debug = "";
	foreach $id (keys %hash) {
		if ($hash{$id}{user} eq "radio-iowa-01") {$data{session_count_01}++}
		if ($hash{$id}{user} eq "radio-iowa-02") {$data{session_count_02}++}
		$debug .= "<tr><td>id=$id</td>";
		foreach $n (qw(user host db command time state info)){
			$debug .= "<td>$n=$hash{$id}{$n}</td>";
		}
		$debug .= "</tr>";
	}
	$data{session_count_01}++; $data{session_count_01}--;
	$data{session_count_02}++; $data{session_count_02}--;
	$data{session_count_total} = $data{session_count_01}+$data{session_count_02};
    #
    #-------------------------------
    # get statistics
    #-------------------------------
    # 30 days
    $sql = "SELECT 1,1,count(distinct ANI) FROM radio_listen_call where datetime_start>date_sub(now(),interval 30 day)";
	%hash = &database_select_as_hash($sql,"flag,value");
	$data{unique_ani_30days} = ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value},0) : 0;
    $sql = "SELECT 1,1,count(*),sum(answered_time) FROM radio_listen_session where datetime_start>date_sub(now(),interval 30 day)";
	%hash = &database_select_as_hash($sql,"flag,value1,value2");
	$data{radio_sessions_30days} 	= ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value1},0) : 0;
	$data{minutes_30days} 			= ($hash{1}{flag} eq 1) ? &format_number(($hash{1}{value2}/60),0) : 0;
	# 7 days
    $sql = "SELECT 1,1,count(distinct ANI) FROM radio_listen_call where datetime_start>date_sub(now(),interval 7 day)";
	%hash = &database_select_as_hash($sql,"flag,value");
	$data{unique_ani_7days} = ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value},0) : 0;
    $sql = "SELECT 1,1,count(*),sum(answered_time) FROM radio_listen_session where datetime_start>date_sub(now(),interval 7 day)";
	%hash = &database_select_as_hash($sql,"flag,value1,value2");
	$data{radio_sessions_7days} 	= ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value1},0) : 0;
	$data{minutes_7days} 			= ($hash{1}{flag} eq 1) ? &format_number(($hash{1}{value2}/60),0) : 0;
	# 24hrs
    $sql = "SELECT 1,1,count(distinct ANI) FROM radio_listen_call where datetime_start>date_sub(now(),interval 24 hour)";
	%hash = &database_select_as_hash($sql,"flag,value");
	$data{unique_ani_24hours} = ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value},0) : 0;
    $sql = "SELECT 1,1,count(*),sum(answered_time) FROM radio_listen_session where datetime_start>date_sub(now(),interval 24 hour)";
	%hash = &database_select_as_hash($sql,"flag,value1,value2");
	$data{radio_sessions_24hours} 	= ($hash{1}{flag} eq 1) ? &format_number($hash{1}{value1},0) : 0;
	$data{minutes_24hours} 			= ($hash{1}{flag} eq 1) ? &format_number(($hash{1}{value2}/60),0) : 0;
    #
    #-------------------------------
    # prepare listen sessions datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "date,minutes,ani,did,radio_extension,service_id,listen_call_id"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT id,datetime_start,round((unix_timestamp(now())-unix_timestamp(datetime_start))/60),'','',radio_extension,'',listen_call_id  
		FROM radio_listen_session 
		WHERE id in (#SELECTED_IDS#) 
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM radio_listen_session where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour)  ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "New calls on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_listen_session where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour) order by datetime_start desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Old calls on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM radio_listen_session where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour) order by datetime_start asc limit #LIMIT_1#,#LIMIT_2# ";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_now";
    $datatable{html}{line_click_link}		= "";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "date,minutes,ani,did,radio_extension,service_id";
    $datatable{html}{col_titles}			= "Date,Minutes,ANI,DID,Radio extension,Zenofon service_id";
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
		# get ani,did, service_id
		$tmp = clean_int($datatable{data}{values}{$id}{listen_call_id});
		if ($tmp ne "") {
			%hash = database_select_as_hash("SELECT 1,1,ani,did,listen_service_id FROM radio_listen_call where id='$tmp' ","flag,ani,did,service_id");
			$datatable{data}{values}{$id}{service_id}	= ($hash{1}{flag} eq 1) ? $hash{1}{service_id} : ""; 
			$datatable{data}{values}{$id}{ani} 			= ($hash{1}{flag} eq 1) ? $hash{1}{ani} : ""; 
			$datatable{data}{values}{$id}{did} 			= ($hash{1}{flag} eq 1) ? $hash{1}{did} : ""; 
		}
		# add name
		$tmp = clean_int($datatable{data}{values}{$id}{service_id});
		if ($tmp ne "") {
			%hash = database_select_as_hash("SELECT 1,1,name FROM service where id='$tmp' ","flag,value");
			$datatable{data}{values}{$id}{service_id} = ($hash{1}{flag} eq 1) ? "$tmp - $hash{1}{value}" : $datatable{data}{values}{$id}{service_id}; 
		}
	}
    #$datatable{html}{title}	= "We have $datatable{data}{count} active radio sessions right now";
    #$datatable{html}{title}	= "Last and active radio sessions.";
	$datatable_html = &datatable_get_html(\%datatable);
	#
	# code clip
	# add data 247
	#$sql_base = "
	#SELECT 1,1,carrier.name,carrier.flag_is_mobile,carrier.flag_premium_signin
	#FROM carrier,carrier_cache_data247
	#where carrier.id=carrier_cache_data247.carrier_id and carrier_cache_data247.number=%s	
	#"; 

	#
	#===========================================================================
    # print page
	#===========================================================================
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Radios sessions now";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "reports.cgi";
    $t{breadcrumb}{1}{title}	= "Radio sessions now";
    $t{breadcrumb}{1}{url}		= "";
    $t{content}	= qq[

		<h3><b>$data{session_count_total}</b> active radio sessions now</h3>
		We have <b>$data{session_count_01}</b> radio sessions at radio-iowa-01 server<br>
		and <b>$data{session_count_02}</b> radio sessions at radio-iowa-02 server<br>
		<br>

		<h3>Summary</h3>
		&#187 In last 30 days: <b>$data{unique_ani_30days}</b> unique ANIs listen <b>$data{radio_sessions_30days}</b> radio sessions with <b>$data{minutes_30days}</b> Minutes<br>
		&#187 In last 7 days: <b>$data{unique_ani_7days}</b> unique ANIs listen <b>$data{radio_sessions_7days}</b> radio sessions with <b>$data{minutes_7days}</b> Minutes<br>
		&#187 In last 24 hours: <b>$data{unique_ani_24hours}</b> unique ANIs listen <b>$data{radio_sessions_24hours}</b> radio sessions with <b>$data{minutes_24hours}</b> Minutes<br>
		<font color=red size=1>(checking numbers... need baruch check)</font><br>
		<br>

		<h3>Radio session</h3>
		Active and last radio sessions right now<br>
	    $datatable_html

    ];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%datatable)."</pre>";
    &template_print("template.html",%t);
}
sub do_calls_now(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "date,minutes,ani,did,dst,service_id,rate_slot"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT id,datetime_start,round((unix_timestamp(now())-unix_timestamp(datetime_start))/60),ani,did,dst,service_id,rate_slot  
		FROM calls_log 
		WHERE id in (#SELECTED_IDS#) 
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM calls_log where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour)  ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "New calls on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM calls_log where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour) order by datetime_start desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Old calls on top ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM calls_log where datetime_stop is null and datetime_start>date_sub(now(),interval 24 hour) order by datetime_start asc limit #LIMIT_1#,#LIMIT_2# ";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "calls_now";
    $datatable{html}{line_click_link}		= "";
    $datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "date,minutes,ani,did,dst,service_id,service_name,status_name,rate_slot";
    $datatable{html}{col_titles}			= "Date,Minutes,ANI,DID,DST,Zenofon service_id,Name,Status,Slot";
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
	# add data 247
	$sql_base = "
	SELECT 1,1,carrier.name,carrier.flag_is_mobile,carrier.flag_premium_signin
	FROM carrier,carrier_cache_data247
	where carrier.id=carrier_cache_data247.carrier_id and carrier_cache_data247.number=%s	
	"; 
	foreach $id (keys %{$datatable{data}{values}}){
		$tmp = "ani";
		$sql = &database_scape_sql($sql_base,$datatable{data}{values}{$id}{$tmp});
		%hash = database_select_as_hash($sql,"flag,name,is_mobile,is_premium");
		if ($hash{1}{flag} eq 1) { $datatable{data}{values}{$id}{$tmp} .= " ($hash{1}{name})"}
		$tmp = "dst";
		$sql = &database_scape_sql($sql_base,$datatable{data}{values}{$id}{$tmp});
		%hash = database_select_as_hash($sql,"flag,name,is_mobile,is_premium");
		if ($hash{1}{flag} eq 1) { $datatable{data}{values}{$id}{$tmp} .= " ($hash{1}{name})"}
		
		$tmp_serviceid = $datatable{data}{values}{$id}{service_id};
		%hash = database_select_as_hash("select 1,1, service.name,service_status.name from service,service_status where service.id='$tmp_serviceid' and  service_status.id = service.status","flag,name,status");
	
		$datatable{data}{values}{$id}{service_name}= ($hash{1}{flag} eq 1)   ? $hash{1}{name} : '';
		$datatable{data}{values}{$id}{status_name}= ($hash{1}{flag} eq 1)   ? $hash{1}{status} : '';
		
	}
	# add title
    $datatable{html}{title}	= "We have $datatable{data}{count} active calls right now";
	# build html
	

	$datatable_html = &datatable_get_html(\%datatable);
	#
	#===========================================================================
    # print page
	#===========================================================================
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Calls sessions now";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "reports.cgi";
    $t{breadcrumb}{1}{title}	= "Calls sessions now";
    $t{breadcrumb}{1}{url}		= "";
    $t{content}	= qq[
	    $datatable_html
    ];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%datatable)."</pre>";
    &template_print("template.html",%t);
}
#-------------------------------------
#-  by yang: do-commission_contest is obsolete ,use _contest2()
#-----------------------------------------
sub do_commission_contest(){
	
	%t = ();
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Commission contest";
	#
	#-------------------------------------
	# prepare date
	#-------------------------------------
	$date_1 = "";
	$date_2 = "";
	$option = 0;
	if ($form{option} ne "") {
		$option =$form{option};
	}
	if ( ($form{date1} ne "") && ($form{date2} ne "") ) {
		$tmp1 = &clean_int($form{date1});
		$tmp11 = substr($tmp1,0,4); $tmp11++; $tmp11--;
		$tmp12 = substr($tmp1,4,2); $tmp12++; $tmp12--;
		$tmp13 = substr($tmp1,6,2); $tmp13++; $tmp13--;
		if ( ($tmp11>2000) && ($tmp11<3000) && ($tmp12>=1) && ($tmp12<=12) && ($tmp13>=1) && ($tmp13<=31) ) {
			$date_1 = substr("0000".$tmp11,-4,4)."-".substr("0000".$tmp12,-2,2)."-".substr("0000".$tmp13,-2,2);
			$form{date1} = $date_1;
		}
		$tmp1 = &clean_int($form{date2});
		$tmp11 = substr($tmp1,0,4); $tmp11++; $tmp11--;
		$tmp12 = substr($tmp1,4,2); $tmp12++; $tmp12--;
		$tmp13 = substr($tmp1,6,2); $tmp13++; $tmp13--;
		if ( ($tmp11>2000) && ($tmp11<3000) && ($tmp12>=1) && ($tmp12<=12) && ($tmp13>=1) && ($tmp13<=31) ) {
			$date_2 = substr("0000".$tmp11,-4,4)."-".substr("0000".$tmp12,-2,2)."-".substr("0000".$tmp13,-2,2);
			$form{date2} = $date_2;
		}
		$date_min = "$date_1 00:00:00";
		$date_max = "$date_2 23:59:59";
	} else {
		$form{date1} = ($form{date1} eq "") ? "2010-03-15" : $form{date1};
		$form{date2} = ($form{date2} eq "") ? "2010-04-15" : $form{date2};
	}
	$date_ok = ( ($date_2 ne "") && ($date_1 ne "") ) ? 1 : 0;
	#
	#-------------------------------------
	# so faz se tem data
	#-------------------------------------
	if ($date_ok eq 1) {
		#
		#-------------------------------------
		# start
		#-------------------------------------
		%services_commissions = ();
		%services_data = ();
		%services_calls = ();
		%services_tree = ();
		$blocked_services_ids = "|1|2|0|";
		$deep_size = 15;
		#
		#-------------------------------------
		# commissions
		#-------------------------------------
		$sql = "
			select service_id,count(*),sum(value)
			from service_commission
			where creation_date>='$date_min' and creation_date<='$date_max' 
			group by service_id
			order by sum(value) desc
			limit 0,500
		";
		%services_commissions = &database_select_as_hash($sql,"qtd,value");
		$services_ids = join("," , (keys %services_commissions));
		#
		#-------------------------------------
		# get service names
		#-------------------------------------
		if ($services_ids ne "") {
			$sql = "
			select service.id,service.name,service.email,service_status.name
			from service,service_status
			where service.status=service_status.id and service.id in ($services_ids)
			";
			$sql = "
			select service.id,service.name,service.email,service_status.name,service_invite.id
			from service,service_status,service_invite
			where service.status=service_status.id and service.id=service_invite.service_id and service.id in ($services_ids)
			";
			%services_data = &database_select_as_hash($sql,"name,email,status,invite");
		}
		#
		#-------------------------------------
		# get calls
		#-------------------------------------
		if ($services_ids ne "") {
			$sql = "
			select service_id,count(*),sum(seconds)
			from calls
			where  service_id in ($services_ids)
			";
			#%services_calls = &database_select_as_hash($sql,"qtd,seconds");
		}
		#
		#-------------------------------------
		# get tree
		#-------------------------------------
		foreach $service_id ( keys %services_commissions) {
			$search_ids = $service_id;
			foreach $deep (1..$deep_size) {
				%hash = &database_select_as_hash("select service_id,1 from service_tree where parent_service_id in ($search_ids)");
				$search_ids = "";
				foreach $search_id (keys %hash) {
					$search_ids .= "$search_id,";
					$services_tree{$service_id}{$deep}++;
				}
				if ($search_ids eq "") {
					last;
				} else {
					$search_ids = substr($search_ids,0,-1);
				}
			}
		}
		#
		#-------------------------------------
		# create html
		#-------------------------------------
		$html = "";
		foreach $service_id (sort{$services_commissions{$b}{value} <=> $services_commissions{$a}{value}} keys %services_commissions) {
			if (index($blocked_services_ids,"|$service_id|") ne -1) {next} 
			$html .= "<tr>";
			$html .= "<td><a href=services.cgi?action=view&service_id=$service_id>$service_id</a></td>";
			$html .= "<td>$services_data{$service_id}{name}</td>";
			$html .= "<td>$services_data{$service_id}{email}</td>";
			$html .= "<td>$services_data{$service_id}{status}</td>";
			$html .= "<td><a href=http://www.zenofon.com/$services_data{$service_id}{invite}>http://www.zenofon.com/$services_data{$service_id}{invite}</a></td>";
			if ($option ne "2") {
				$html .= "<td class=ar>".&format_number($services_commissions{$service_id}{qtd},0)."</td>";
			} else {
				$html .="&nbsp;";
			}
			if ($option ne "1") {
				$html .= "<td class=ar>\$".&format_number($services_commissions{$service_id}{value},2)."</td>";
			} else
			{
				$html .="&nbsp;";
			}
			foreach $deep_show (1..$deep_size) {
				$html .= "<td class=ar>".&format_number($services_tree{$service_id}{$deep_show},0)."</td>";
			}
			$html .= "";
			$html .= "</tr>";
		}
	}
	
	for ($i=0;$i<3; $i++) {
		$arr_option{$i} ='';
	}
		$arr_option{$option} = 'checked' ;
	#
	#-------------------------------------
	# print page
	#-------------------------------------
	$t{dic}{content}	.= qq[
		<form action=$my_url>
		Start date (YYYY-MM-DD): <input type=text name=date1 value="$form{date1}"><br>
		End date (YYYY-MM-DD): <input type=text name=date2 value="$form{date2}"><br>
	
		<input type="radio" name="option" value=1  $arr_option{1} />Only Referred Counts
		<input type="radio" name="option" value=2  $arr_option{2} />Only Commissions
		<input type="radio" name="option" value=0  $arr_option{0} />Display Both
		<input type=submit value=go><br>
		<input type=hidden name=action value=commission_contest>
		</form>
		<br>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100% onclick="sortColumn(event)">
			<thead>
				<tr>
				<td colspan=5>Service</td>
				<td colspan=2>Commissions</td>
				<td colspan=20 rowspan=2>Services in tree (deep 1, 2, 3, ...n)</td>
				</tr>
				<tr>
				<td>ID</td>
				<td>Name</td>
				<td>Email</td>
				<td>Status</td>
				<td>Invite Link</td>
				<td>Qtd</td>
				<td>Sum</td>
				</tr>
			</thead>
			<tbody>
			$html
			</tbody>
		</table>
	];
	&template_print("template.html",%t);
}
#=======================================================
sub do_commission_contest2(){
	%t = ();
	$t{dic}{my_url}	= $my_url;
	$t{dic}{title}	= "<a href=$my_url>Reports</a> &#187; Commission contest";
	#
	#-------------------------------------
	# prepare date
	#-------------------------------------
	$date_1 = "";
	$date_2 = "";
	$option = 0;
	if ($form{option} ne "") {
		$option =$form{option};
	}
	if ( ($form{date1} ne "") && ($form{date2} ne "") ) {
		$tmp1 = &clean_int($form{date1});
		$tmp11 = substr($tmp1,0,4); $tmp11++; $tmp11--;
		$tmp12 = substr($tmp1,4,2); $tmp12++; $tmp12--;
		$tmp13 = substr($tmp1,6,2); $tmp13++; $tmp13--;
		if ( ($tmp11>2000) && ($tmp11<3000) && ($tmp12>=1) && ($tmp12<=12) && ($tmp13>=1) && ($tmp13<=31) ) {
			$date_1 = substr("0000".$tmp11,-4,4)."-".substr("0000".$tmp12,-2,2)."-".substr("0000".$tmp13,-2,2);
			$form{date1} = $date_1;
		}
		$tmp1 = &clean_int($form{date2});
		$tmp11 = substr($tmp1,0,4); $tmp11++; $tmp11--;
		$tmp12 = substr($tmp1,4,2); $tmp12++; $tmp12--;
		$tmp13 = substr($tmp1,6,2); $tmp13++; $tmp13--;
		if ( ($tmp11>2000) && ($tmp11<3000) && ($tmp12>=1) && ($tmp12<=12) && ($tmp13>=1) && ($tmp13<=31) ) {
			$date_2 = substr("0000".$tmp11,-4,4)."-".substr("0000".$tmp12,-2,2)."-".substr("0000".$tmp13,-2,2);
			$form{date2} = $date_2;
		}
		$date_min = "$date_1 00:00:00";
		$date_max = "$date_2 23:59:59";
	} else {
		$form{date1} = ($form{date1} eq "") ? "2010-03-15" : $form{date1};
		$form{date2} = ($form{date2} eq "") ? "2010-04-15" : $form{date2};
	}
	$date_ok = ( ($date_2 ne "") && ($date_1 ne "") ) ? 1 : 0;
	#
	#-------------------------------------
	# so faz se tem data
	#-------------------------------------
	if ($date_ok eq 1) {
		#
		#-------------------------------------
		# start
		#-------------------------------------
		%services_new = ();
		%services_data = ();
		%services_calls = ();
		%services_tree = ();
		$blocked_services_ids = "|1|2|0|";
		$deep_size = 10;
		#
		#-------------------------------------
		# commissions
		#-------------------------------------
		$sql = "
			select id,service_id,deep,value
			from service_commission
			where engine='REFERRAL_SIGNIN' and service_id >2 and creation_date>='$date_min' and creation_date<='$date_max' 
		";
		%services_commissions = &database_select_as_hash($sql,"service_id,deep,value");
		%parent_services = ();
		%parent_services_values = ();
		foreach $id ( keys %services_commissions) {
			$service_id = $services_commissions{$id}{service_id} ;
			$deep  = $services_commissions{$id}{deep};
			$value = $services_commissions{$id}{value};
			
			$parent_services{$service_id}{0} ++;
			$parent_services{$service_id}{$deep} ++;
		 
			
		}
		$sql = "
			select service_id,sum(value)
			from service_commission 
			where  service_id >2 and creation_date>='$date_min' and creation_date<='$date_max'
			 group by service_id 
		";
	 
		%parent_services_values = &database_select_as_hash($sql,"value");
	
	 
		 $services_ids = join("," , (keys %parent_services));
		# warning("service_ids:".$services_ids) ;
		$sql = "
			select service.id,service.name,service.email,service_status.name 
			from service,service_status 
			where service.status=service_status.id   and service.id  in (".$services_ids.")";
			
		%services_data = &database_select_as_hash($sql,"name,email,status");
		
		$sql = "
			select service_id,id
			from service_invite
			where  service_id  in (".$services_ids.")";
			
		%services_invitedata = &database_select_as_hash($sql,"invite");
		
		#
		#-------------------------------------
		# create html
		#-------------------------------------
		$html = "";
	
		foreach $service_id (sort{$parent_services{$b}{0} <=> $parent_services{$a}{0}}  keys %parent_services) {
			if (index($blocked_services_ids,"|$service_id|") ne -1) {next}
			
			
			
			
			$html .= "<tr>";
			$html .= "<td><a href=services.cgi?action=view&service_id=$service_id>$service_id</a></td>";
			$html .= "<td>$services_data{$service_id}{name}</td>";
			$html .= "<td>$services_data{$service_id}{email}</td>";
			$html .= "<td>$services_data{$service_id}{status}</td>";
			$html .= "<td><a href=http://www.zenofon.com/$services_invitedata{$service_id}{invite}>http://www.zenofon.com/$services_invitedata{$service_id}{invite}</a></td>";
			 
			$html .= "<td class=ar>".&format_number($parent_services{$service_id}{0},0)."</td>";
			 
			$html .= "<td class=ar>".&format_number($parent_services_values{$service_id}{value},2)."</td>";
		 
			 
			 
			foreach $deep_show (1..$deep_size) {
				$html .= "<td class=ar>".&format_number($parent_services{$service_id}{$deep_show},0)."</td>";
			}
			$html .= "";
			$html .= "</tr>";
		}
	}
	
	for ($i=0;$i<3; $i++) {
		$arr_option{$i} ='';
	}
		$arr_option{$option} = 'checked' ;
	#
	#-------------------------------------
	# print page
	#-------------------------------------
	$t{dic}{content}	.= qq[
		<form action=$my_url>
		Start date (YYYY-MM-DD): <input type=text name=date1 value="$form{date1}"><br>
		End date (YYYY-MM-DD): <input type=text name=date2 value="$form{date2}"><br>
		(we only display 10 deep refers)
	 
		<input type=submit value=go><br>
		<input type=hidden name=action value=commission_contest2>
		</form>
		<br>
		click column name to sort<br>
		<table id="table-1" border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=100%  ">
			<thead>
				<tr>
				<td>ID</td>
				<td>Name</td>
				<td>Email</td>
				<td>Status</td>
				<td>Invite Link</td>
				<td>Refers</td>
				<td>Earned</td>
				<td>D1</td>
				<td>D2</td>
				<td>D3</td>
				<td>D4</td>
				<td>D5</td>
				<td>D6</td>
				<td>D7</td>
				<td>D8</td>
				<td>D9</td>
				<td>D10</td>
				
				</tr>
			</thead>
			<tbody>
			$html
			</tbody>
		</table>
		<script src="/noc/design/sortabletable.js"	 type="text/javascript"	></script>
		<script type="text/javascript">

var st1 = new SortableTable(document.getElementById("table-1"),
	["Number", "CaseInsensitiveString","String","String","String",
	"Number", "Number", "Number","Number", "Number","Number", "Number","Number", "Number","Number","Number","Number"]);

</script>
	];
	&template_print("template.html",%t);
}
#=======================================================


















