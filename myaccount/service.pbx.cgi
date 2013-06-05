#!/usr/bin/perl
#=======================================================
# start some check
#=======================================================
require "../include.cgi";
%carriers_list = ();
$carriers_list{"USAATT"}		= "At&t";
$carriers_list{"USAALLTEL"}		= "Alltel";
$carriers_list{"USABOOST"}		= "Boost mobile";
$carriers_list{"USAONE"}		= "Cellular One";
$carriers_list{"USACRICKET"}	= "Cricket";
$carriers_list{"USACINGULAR"}	= "Go/Cingular (prepaid)";
$carriers_list{"USAMETROPCS"}	= "Metro PCS";
$carriers_list{"USASPRINT"}		= "Sprint/Nextel";
$carriers_list{"USATMOBILE"}	= "T-mobile";
$carriers_list{"USATMOBILETOGO"}= "T-mobile ToGo";
$carriers_list{"USATRACKFONE"}	= "Tracfone";
$carriers_list{"USAUS"}			= "U.S. Cellular";
$carriers_list{"USAVERIZON"}	= "Verizon Wireless";
$carriers_list{"USAVERIZONPAYG"}= "Verizon Wireless Pay as you go";
$carriers_list{"USAVIRGIN"}		= "Virgin Mobile";
$carriers_list{"UNKNOWN"}		= "Unknown";
$carriers_list{"LANDLINE"}		= "Landline";
$carriers_list{"NOTLISTED"}		= "Not listed";
#=======================================================


#=======================================================
# main loop
#=======================================================
$my_url = "service.pbx.cgi";
$action = $form{action};
#warning("action=$action");
#warning("session status:".$app{session_status});
if  ($app{session_status} eq 1) {
	if    ($action eq "dst")		{ &do_dst();				}
	elsif    ($action eq "dst_skype")	{ &do_dst_skype();			}
	elsif    ($action eq "dst_radio")	{ &do_dst_radio();			}
	elsif    ($action eq "radio_add")	{ &do_radio_add();			}
	elsif    ($action eq "radio_edit")	{ &do_radio_edit();			}
	elsif    ($action eq "radio_del")	{ &do_radio_del();			}
	elsif ($action eq "ani")		{ &do_ani();				}
	elsif ($action eq "cid")		{ &do_cid();				}
	elsif ($action eq "add")		{ &ip_flood_surge_protection("Signin"); &do_add();				}
	elsif ($action eq "save_global"){ &do_save_global(); }
	else							{ &do_overview();			}
} else {
	if    ($action eq "add")		{ &ip_flood_surge_protection("Signin"); &do_add();				}
	else							{ cgi_redirect("index.cgi");}
}
exit;
#=======================================================



#=======================================================
# actions listed here
#=======================================================
sub do_cid() {
	$save 	= 0;
	$number = clean_int(substr($form{"cid_number"},0,1024));
	$mode 	= clean_str(substr($form{"cid_mode"},0,1024));
	$manual	= 0;
	if ($mode eq "auto") {
		$save = 1;
		$manual	= 0;
		$number = "";
	} elsif ($mode eq "manual") {
		$manual	= 1;
		if ($number eq "") {
			$t{dic}{"cid_error_no_number"} = 1;
			$save = 0;
		} else {
			$save = 1;
		}
		#
		#($flag,$number_e164,$country) = &multilevel_check_E164_number($number);
		#if ($number eq "") {
		#	$t{dic}{"cid_error_no_number"} = 1;
		#	$save = 0;
		#} elsif ($flag eq "USANOAREACODE") {
		#	$t{dic}{"cid_error_usa_no_areacode"} = 1;
		#	$save = 0;
		#} elsif ($flag eq "UNKNOWNCOUNTRY") {
		#	$t{dic}{"cid_error_unknown_country"} = 1;
		#	$save = 0;
		#} elsif ($flag eq "OK") {
		#	$number = $number_e164;
		#	$save = 1;
		#} else {
		#	$t{dic}{"cid_error_wrong_number"} = 1;
		#	$save = 0;
		#}
		#
	}
	if ($save eq 1) {
		$t{dic}{"cid_ok"} = 1;
		&data_set("service_data",$app{service_id},"cid_manual",$manual);
		&data_set("service_data",$app{service_id},"cid_number",$number);
	}
	do_overview(%t);
}
sub do_overview() {
    #
    #--------------------------------------------------
    # inicia umas coisas
    #--------------------------------------------------
	local(%hash) = @_;
    %t = %template_default;
 	$t{cid_ok} = $hash{sid_ok};
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
    $t{dic}{my_url}					= $my_url;
    $t{dic}{skype_index_range_low}	= 1001;
    $t{dic}{skype_index_range_hi}	= 1025;    
    $t{dic}{phone_index_range_low}	= 1;
	# change by yassine  to allow more than 53 DID  , change form 53-> 148 
    $t{dic}{phone_index_range_hi}	= 148;   
    $t{dic}{radio_index_range_low}	= 2001;
    $t{dic}{radio_index_range_hi}	= 2009; 
       
	%hash = database_select_as_hash("select 1,1,service_status.need_ani_check from service,service_status where service.id='$app{service_id}' and service.status=service_status.id ","flag,value");
	$t{dic}{"ani_need_confirmation"} 	= ( ($hash{1}{flag} eq 1) && ($hash{1}{value} eq 1) ) ? 1 : 0; 
    #
    #--------------------------------------------------
    # ANI list
    #--------------------------------------------------
	
	$sqlName = "select name,value from service_data where target='$app{service_id}' and name like 'ani_%_name'";
	%aninameHash = &database_select_as_hash($sqlName,"value");
	
	$sqlNumber = "select name,value from service_data where target='$app{service_id}' and name like 'ani_%_number'";
	%aninumberHash = &database_select_as_hash($sqlNumber, "value");
	
    $found_ani = 0;
    foreach $index (1..20) {
		$name 	= $aninameHash{"ani_".$index."_name"}{value} ; #&data_get("service_data",$app{service_id},"ani_".$index."_name");
		$number = $aninumberHash{"ani_".$index."_number"}{value} ; #&data_get("service_data",$app{service_id},"ani_".$index."_number");
		if ($number ne "") {
			$t{dic}{"ani_".$index."_number"} = &format_E164_number($number,"USA");
			$t{dic}{"ani_".$index."_name"} = $name;
			if ($t{dic}{"ani_need_confirmation"} eq 1) {
				$tmp = $t{dic}{"ani_".$index."_number"};
				($tmp1,$tmp2,$tmp3) = &multilevel_check_E164_number($tmp);
				$tmp = ($tmp1 eq "OK") ? $tmp2 : $tmp;
				$t{dic}{"ani_".$index."_error"} = (&multilevel_anicheck_check($app{service_id},$tmp) eq 1) ? 0 : 1;
			} else {
				$t{dic}{"ani_".$index."_error"} = 0;
			}
			$found_ani= 1;
		}
    }
	$t{dic}{ani_empty} = ($found_ani eq 1) ? 0 : 1;
    #
    #--------------------------------------------------
    # DST list
    #--------------------------------------------------
	
	$sqlName = "select name,value from service_data where target='$app{service_id}' and name like 'dst_%_name'";
	%dstnameHash = &database_select_as_hash($sqlName,"value");
	
	$sqlNumber = "select name,value from service_data where target='$app{service_id}' and name like 'dst_%_number'";
	%dstnumberHash = &database_select_as_hash($sqlNumber, "value");
	
    foreach $index ($t{dic}{phone_index_range_low}..$t{dic}{phone_index_range_hi}) {
		$name = $dstnameHash{"dst_".$index."_name"}{value}; #&data_get("service_data",$app{service_id},"dst_".$index."_name");
		$number = $dstnumberHash{"dst_".$index."_number"}{value}; #&data_get("service_data",$app{service_id},"dst_".$index."_number");
		if ($number ne "") {
			$number = &format_E164_number($number,"USA");
			$t{dic}{"dst_".$index."_number"} = $number;
			$t{dic}{"dst_".$index."_name"} = $name;
			$t{dic}{"dst_".$index."_number"} =~ s/^011 //;
		}
    }
    #
    #--------------------------------------------------
    # SKYPE list
    #--------------------------------------------------
    foreach $index ($t{dic}{skype_index_range_low}..$t{dic}{skype_index_range_hi}) {
    	$name = $dstnameHash{"dst_".$index."_name"}{value}; #&data_get("service_data",$app{service_id},"dst_".$index."_name");
		$number = $dstnumberHash{"dst_".$index."_number"}{value}; #&data_get("service_data",$app{service_id},"dst_".$index."_number");
		if ($number ne "") {
			$number = &format_E164_number($number,"USA");
			$t{dic}{"dst_".$index."_number"} = $number;
			$t{dic}{"dst_".$index."_name"} = $name;
		}
    }
   	#--------------------------------------------------
    # DID-RADIO list
    #--------------------------------------------------
    foreach $index ($t{dic}{radio_index_range_low}..$t{dic}{radio_index_range_hi}) {
    	$name = $dstnameHash{"dst_".$index."_name"}{value}; #&data_get("service_data",$app{service_id},"dst_".$index."_name");
		$number = $dstnumberHash{"dst_".$index."_number"}{value}; #&data_get("service_data",$app{service_id},"dst_".$index."_number");
		if ($number ne "") {
			$number = &format_E164_number($number,"USA");
			$t{dic}{"dst_".$index."_number"} = $number;
			$t{dic}{"dst_".$index."_name"} = $name;
		}
    }
   	#--------------------------------------------------
    # My Uploaded Radio
    #--------------------------------------------------
    %hash_radio = ();
    $html_myradiolist ="";
   	%hash_radio = database_select_as_hash("select name,description,radiourl,radiotype from musiconhold where service_id='$app{service_id}' ","description,radiourl,radiotype");
     foreach $id ( keys %hash_radio) { 
     	$exten = $id;
		$html_myradiolist 	.= "<li><a href=$my_url?action=radio_edit&id=$id>Exten:$exten <br>Radio Name: $hash_radio{$id}{description}</a></li>";
	}
	$t{dic}{html_myradiolist} = $html_myradiolist ;
	$t{dic}{html_radioadd} = "<br><a href=$my_url?action=radio_add onClick=\"modal_open(\'Add \',\'$my_url?action=radio_add\',300,360); return false;\">Add Radio Station</a>"; 
	
    #--------------------------------------------------
    # CID
    #--------------------------------------------------
	$t{dic}{cid_manual}		= &data_get("service_data",$app{service_id},"cid_manual");
	$t{dic}{cid_manual}		= ($t{dic}{cid_manual} eq 1) ? 1 : 0;
	$t{dic}{cid_automatic}	= ($t{dic}{cid_manual} eq 1) ? 0 : 1;
	$t{dic}{cid_mode}		= ($t{dic}{cid_manual} eq 1) ? "manual" : "auto";
	$t{dic}{cid_number}		= &data_get("service_data",$app{service_id},"cid_number");
	#$t{dic}{cid_number}		= &format_E164_number($t{dic}{cid_number},"USA");
	#$t{dic}{cid_debug} .= "VIEW - manual=$t{dic}{cid_manual} / automatic=$t{dic}{cid_automatic} / mode=$t{dic}{cid_mode} / number=$t{dic}{cid_number} ";
	#
	#---------------------------------------------------------------------------
	# status
	#---------------------------------------------------------------------------
	$sql = "
	select 1,1, service_status.id, service_status.name, service_status.pin_locked 
	from service,service_status 
	where service.id='$app{service_id}' and service.status=service_status.id  
	";
	%hash = database_select_as_hash($sql,"flag,status_id,status_name,locked");
	$t{dic}{service_status_id}		= $hash{1}{status_id};
	$t{dic}{service_status_name}	= $hash{1}{status_name};
	$t{dic}{service_is_pin_locked} 	= $hash{1}{locked};
	$t{dic}{"service_status_id_flag_".$hash{1}{status_id}} = 1;
 
 
		$callback  = &data_get("service_data",$app{service_id},"dst_1_callback");
		$routeann  = &data_get("service_data",$app{service_id},"dst_1_routeann");
		$balanceann  = &data_get("service_data",$app{service_id},"dst_1_balanceann");
	   $t{dic}{"callback_option_0_is_selected"} = ($callback eq "0") ? 1 : 0;
	 $t{dic}{"callback_option_1_is_selected"} = ($callback eq "1") ? 1 : 0;
	  $t{dic}{"callback_option_2_is_selected"} = ($callback eq "2") ? 1 : 0;
   
	  $t{dic}{"routeann_option_0_is_selected"} = ($routeann eq "0") ? 1 : 0;
          $t{dic}{"routeann_option_1_is_selected"} = ($routeann ne "0") ? 1 : 0;

	    $t{dic}{"balanceann_option_0_is_selected"} = ($balanceann eq "0") ? 1 : 0;
		$t{dic}{"balanceann_option_1_is_selected"} = ($balanceann ne "1") ? 0 : 1;
	
    #
    #--------------------------------------------------
    # user data
    #--------------------------------------------------
    &template_print("template.pbx.overview.html",%t);
}
sub do_ani(){
    #
    #--------------------------------------------------
    # start default values
    #--------------------------------------------------
	$ok = 1;
	$index = "";
    %t = %template_default;
    $t{dic}{my_url} 					= $my_url;
    $t{dic}{"error_wrong_number"} 		= 0;
    $t{dic}{"error_usa_no_areacode"} 	= 0;
    $t{dic}{"error_not_e164"} 			= 0;
    $t{dic}{"error_unknown_country"} 	= 0;
	$t{dic}{"error_ani_in_use"}			= 0;
	$t{dic}{"error_no_more_index"} 		= 0;
    $t{dic}{"error_bad_index"} 			= 0;
    $t{dic}{"error_bad_confirmation"} 	= 0;
    $t{dic}{"number"} 					= "";
    $t{dic}{"name"} 					= "";
    $t{dic}{"callid"} 					= "";
    $t{dic}{"carrier"} 					= "";
    $t{dic}{"index"} 					= "";
	%hash = database_select_as_hash("select 1,1,service_status.need_ani_check from service,service_status where service.id='$app{service_id}' and service.status=service_status.id ","flag,value");
	$t{dic}{"ani_need_confirmation"} 	= ( ($hash{1}{flag} eq 1) && ($hash{1}{value} eq 1) ) ? 1 : 0;
	#
    #--------------------------------------------------
    # get index by form or find a free one if new=1
    #--------------------------------------------------
	if ($form{new} eq 1) {
		$sql = "select name, value from service_data where target=$app{service_id} and name like 'ani_%_number'";
		%aniHash = database_select_as_hash($sql, "value");
		foreach $loop (1..20) {
			#if (&data_get("service_data",$app{service_id},"ani_".$loop."_number") eq "")
			if ( $aniHash{"ani_".$loop."_number"}{value} eq "")
			{
				$index = $loop;
				last;
			}
		}
		if ($index eq "") {$t{dic}{"error_no_more_index"} = 1;$ok = 0;}
	} else {
		$index = &clean_int(substr($form{index},0,10));
		if ( ($index<1) || ($index>50) || ($index eq "") ) {
			$t{dic}{"error_bad_index"} = 1;
			$ok = 0;
		}
	}
	$t{dic}{"index"} = $index;
    #
    #--------------------------------------------------
    # try to delete
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{delete} eq 1) ) {
		# delete data
		$tmp = &data_get("service_data",$app{service_id},"ani_".$index."_number");
		&multilevel_anicheck_unset($app{service_id},$tmp);
		
		$numberToDelete = data_get("service_data", $app{service_id}, "ani_".$index."_number");
		
		&data_delete("service_data",$app{service_id},"ani_".$index."_name");
		&data_delete("service_data",$app{service_id},"ani_".$index."_number");
		&data_delete("service_data",$app{service_id},"ani_".$index."_callid");
		&data_delete("service_data",$app{service_id},"ani_".$index."_carrier");
		&action_history("status:ani:delete",('service_id'=>$app{service_id},'value_old'=>$number));
		# update ani list
		@sql_list = ();
		#@sql_list = (@sql_list,"delete from service_ani where service_id='$app{service_id}'");
		$sql = "delete from service_ani where service_id='$app{service_id}' and ani='$numberToDelete' ";
		
		#foreach $loop (1..20) {
		#	$number = clean_int(&data_get("service_data",$app{service_id},"ani_".$loop."_number"));
		#	if ($number eq "") {next}
		#	@sql_list = (@sql_list,"insert into service_ani (ani,service_id) values ('$number', '$app{service_id}') ");
		#}
		#foreach (@sql_list) {database_do($_)};
		database_do($sql);
		$sql = "select 1,1 from service_data where target='$app{service_id}' and name like 'ani_%_number' and value='$numberToDelete'";
		%hash = database_select_as_hash($sql, "flag");
		if($hash{1}{flag} eq "1"){
			$sql = "insert into service_ani (ani, service_id) values ('$numberToDelete', '$app{service_id}')";
			database_do($sql);
		}
		# return to status
		cgi_redirect("$my_url");
		exit;
	}
    #
    #--------------------------------------------------
    # check before save
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} eq 1) ) {
		# clean from data
		$number = clean_int(substr($form{"number"},0,1024));
		$name	= clean_str(substr($form{"name"},0,1024),"-_()<>\@");
		$callid	= clean_int(substr($form{"callid"},0,1024));
		$carrier= clean_str(substr($form{"carrier"},0,1024));
		$carrier= (exists($carriers_list{$carrier})) ? $carrier : "";
		# check and format number
		($flag,$number_e164,$country) = &multilevel_check_E164_number($number);
		if ($flag eq "USANOAREACODE") {
			$t{dic}{"error_usa_no_areacode"} = 1;
			$ok = 0;
		} elsif ($flag eq "UNKNOWNCOUNTRY") {
			$t{dic}{"error_unknown_country"} = 1;
			$ok = 0;
		} elsif ($flag eq "OK") {
			$number = $number_e164;
		} else {
			$t{dic}{"error_wrong_number"} = 1;
			$ok = 0;
		}
		# check rate
		if ($ok eq 1) {
			#
			# pega rate_table, baseado no status do servico 
			$sql = "select 1,1,service_status.rate_slot_callback from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
			%hash = database_select_as_hash($sql,"flag,id");
			if ( ($hash{1}{flag} eq "1") && ($hash{1}{id} ne "") ) {
				%hash = &multilevel_rate_table_get($number,$hash{1}{id});
				if ($hash{ok_to_use} eq 1) {
				} else {
					$t{dic}{"error_wrong_number"} = 1;
					$ok = 0;
				}
			} else {
				$t{dic}{"error_wrong_number"} = 1;
				$ok = 0;
			}
		}
		# second level check ANI list
		if ($ok eq 1) {
			%hash = database_select_as_hash("select 1,1,count(*) from service_ani where ani='$number' and service_id<>'$app{service_id}'","flag,qtd");
			unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ) {
				$t{dic}{"error_ani_in_use"} = 1;
				$ok = 0;
			}
		}
		# 3rd level check - block this ANI if this service is pin_locked and ANI has calls in other services for the last 6 months
		if ($ok eq 1) {
			$sql = "
			select 1,1,service_status.pin_locked
			from service,service_status 
			where service.id='$app{service_id}' and service.status=service_status.id  
			";
			%hash = database_select_as_hash($sql,"flag,pin_locked");
			if ( ($hash{1}{flag} eq 1) && ($hash{1}{pin_locked} eq 1) ) {
				%hash = database_select_as_hash("SELECT 1,1,count(*) FROM calls where ani='$number' and  service_id!='$app{service_id}' and date>adddate(current_date(),-180)","flag,qtd");
				if ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} ne 0) ) {
					$t{dic}{"error_ani_blocked_for_pin_locked_service"} = 1;
					$ok = 0;
				}
			}
		}
		# disable ani confirm in case already confirmated
		if ( ($t{dic}{"ani_need_confirmation"} eq 1) && ($ok eq 1) ) {
			$t{dic}{"ani_need_confirmation"} = (&multilevel_anicheck_check($app{service_id},$number) eq 1) ? 0 : 1;

			#$number_validated = &data_get("service_data",$app{service_id},"ani_".$index."_number_validated");
			#if ( ($number eq $number_validated) && ($number_validated ne "") ){
			#	$t{dic}{"ani_need_confirmation"} = 0;
			#}
		}
	}
	#
    #--------------------------------------------------
	# dial ani confirmation
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} eq 1) && ($t{dic}{"ani_need_confirmation"} eq 1) && ($form{dial_ani_confirmation} eq 1) ) {
		#
		# todo: detect race and flood
		#
		# deaults
		$t{dic}{"ani_lock_for_confirmation"} = 1;
		$t{dic}{"ani_confirmation_dialing"} = 1;
		$ok=0;
		#
		# if no code, create code
		$confirmation_code = &active_session_get("anicheck_code");
		$confirmation_ani  = &active_session_get("anicheck_number");
		if ( ($confirmation_ani ne $number) || ($confirmation_ani eq "") || ($confirmation_code eq "") ) {
			@chars=('0'..'9');
			$confirmation_code  = "";
			foreach (1..4) {$confirmation_code  .= $chars[rand @chars];}
			&active_session_set("anicheck_code",$confirmation_code);
			&active_session_set("anicheck_number",$number);
		}
		#
		#$callback_queue_folder =  "/var/spool/asterisk/outgoing/";
		#$channel_string		= &multilevel_dialstring_get($number);
		#$callback_file		= time.$number.".sendcode.call"; 
		#$callback_file_buf 	=  "Channel: $channel_string\n";
		#$callback_file_buf 	.= "MaxRetries: 2\n";
		#$callback_file_buf 	.= "RetryTime: 5\n";
		#$callback_file_buf 	.= "WaitTime: 40\n";
		#$callback_file_buf 	.= "Application: DeadAGI\n";
		#$callback_file_buf 	.= "Data: play_code.pl,code=$confirmation_code\n";
		#$callback_file_buf 	.= "AlwaysDelete:Yes\n";
		#$callback_file_buf 	.= "Archive:No\n";
		#%my_timestamp = &get_today(time+5);
		#$timestamp_future = substr("0000".$my_timestamp{YEAR},-4,4) . substr("00".$my_timestamp{MONTH},-2,2) . substr("00".$my_timestamp{DAY},-2,2) . substr("00".$my_timestamp{HOUR},-2,2) . substr("00".$my_timestamp{MINUTE},-2,2) .".".substr("00".$my_timestamp{SECOND},-2,2);
		#open (OUT,">/tmp/$callback_file");
		#print OUT $callback_file_buf;
		#close (OUT);
		#$cmd = "chmod 666 /tmp/$callback_file; ";
		#$cmd .= "touch -t $timestamp_future /tmp/$callback_file; ";
		#$cmd .= "mv /tmp/$callback_file $callback_queue_folder; ";
		#$tmp = `$cmd`;
		# dial ani and play code using new format
		&dial_and_play_code($number,$confirmation_code);
		&action_history("security:ani_check_request",('service_id'=>$app{service_id},'value_old'=>$confirmation_code,'value_new'=>$number));
	}
	#
    #--------------------------------------------------
	# grab save with ani confirmation
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} eq 1) && ($t{dic}{"ani_need_confirmation"} eq 1) ) {
		$t{dic}{"ani_lock_for_confirmation"} = 1;
		$ok = 0;
		if ($form{save_ani_confirmation} eq 1) {
			$tmp1 = &active_session_get("anicheck_code");
			$tmp2 = &active_session_get("anicheck_number");
			if ( ($tmp1 ne "") && ($tmp2 ne "") && ($form{ani_confirmation} ne "") && ($form{ani_confirmation} eq $tmp1) && ($number eq $tmp2) ) {
				$ok = 1;
			} else {
				$t{dic}{"error_bad_ani_confirmation"} = 1;
			}
			#
			#$tmp = &data_get("service_data",$app{service_id},"ani_".$index."_confirmation");
			#if ( ($tmp ne "") && ($form{ani_confirmation} ne "") && ($form{ani_confirmation} eq $tmp1) && ($number eq $tmp2) ) {
			#	$ok = 1;
			#} else {
			#	$t{dic}{"error_bad_ani_confirmation"} = 1;
			#}
		}
	}
    #
    #--------------------------------------------------
    # if all ok, save
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} eq 1) ) {
		# save data
		&data_set("service_data",$app{service_id},"ani_".$index."_name"		,$name);
		&data_set("service_data",$app{service_id},"ani_".$index."_callid"	,$callid);
		&data_set("service_data",$app{service_id},"ani_".$index."_number"	,$number);
		&data_set("service_data",$app{service_id},"ani_".$index."_carrier"	,$carrier);
		&action_history("status:ani:add",('service_id'=>$app{service_id},'value_new'=>$number));
		#
		# TODO sera precisamos salvar o ani pra confirmacao sempre ou so quando necessario?
		if ($t{dic}{"ani_need_confirmation"} eq 1)  {
			&multilevel_anicheck_set($app{service_id},$number);
			&action_history("security:ani_checked",('service_id'=>$app{service_id},'value_new'=>$number));
			&active_session_delete("anicheck_code");
			&active_session_delete("anicheck_number");
		} else {
			&multilevel_anicheck_touch($app{service_id},$number);
		}
		&data_delete("service_data",$app{service_id},"ani_".$index."_confirmation");
		&data_delete("service_data",$app{service_id},"ani_".$index."_confirmation_ani");
		# update ani list
		@sql_list = ();
		#@sql_list = (@sql_list,"delete from service_ani where service_id='$app{service_id}' ");
		#foreach $loop (1..20) {
		#	$number = clean_int(&data_get("service_data",$app{service_id},"ani_".$loop."_number"));
		#	if ($number eq "") {next}
		#	@sql_list = (@sql_list,"insert into service_ani (ani,service_id) values ('$number', '$app{service_id}') ");
		#}
		#foreach (@sql_list) {database_do($_)};
		$sql = "insert into service_ani (ani, service_id) values ('$number', '$app{service_id}')";
		database_do($sql);
		cgi_redirect("$my_url");
		exit;
	}
    #
    #--------------------------------------------------
    # if not save, then load
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} ne 1) ) {
		#$form{"callid"}	= &format_dial_number(&data_get("service_data",$app{service_id},"ani_".$index."_callid"));
		$form{"callid"}	= &data_get("service_data",$app{service_id},"ani_".$index."_callid");
		$form{"number"} = &format_E164_number(&data_get("service_data",$app{service_id},"ani_".$index."_number"),"USA");
		$form{"name"} 	= &data_get("service_data",$app{service_id},"ani_".$index."_name");
		$form{"carrier"}= &data_get("service_data",$app{service_id},"ani_".$index."_carrier");
		$form{"carrier"}= (exists($carriers_list{$form{"carrier"}})) ? $form{"carrier"} : "";
		$t{dic}{"number"}	= $form{"number"};
		$t{dic}{"name"}		= $form{"name"};
		$t{dic}{"callid"}	= $form{"callid"};
		$t{dic}{"carrier"}	= $form{"carrier"};
	}
    #
    #--------------------------------------------------
    # carrier list
    #--------------------------------------------------
	foreach $loop (keys %carriers_list) {
		$t{dic}{"carriers_list_".$loop."_is_selected"} = ($form{"carrier"} eq $loop) ? 1 : 0;
	}
    #
    #--------------------------------------------------
    # fill form
    #--------------------------------------------------
	$t{dic}{"number"}	= $form{"number"};
	$t{dic}{"name"}		= $form{"name"};
	$t{dic}{"callid"}	= $form{"callid"};
	$t{dic}{"carrier"}	= $form{"carrier"};
	$t{dic}{"billing_rate_found"}			= 0;
	$t{dic}{"billing_rate_per_minute"}		= "";
	$t{dic}{"billing_duration_per_1_dollar"}= "";
	$t{dic}{"billing_value_per_hour"}		= "";
	$t{dic}{"billing_country_name"}			= "";
	$t{dic}{"billing_country_code"}			= "";
	$t{dic}{"billing_rate_name"}			= "";
	$t{dic}{"billing_number"}				= &data_get("service_data",$app{service_id},"ani_".$index."_number");
	$t{dic}{"billing_number_ok"}			= 0;
	($billing_number_flag , $billing_number_e164, $billing_number_country) = &multilevel_check_E164_number($t{dic}{"billing_number"});
	if ($billing_number_flag eq "OK") { 
		%country_codes 	= database_select_as_hash("select code,name from country");
		$t{dic}{"billing_number_ok"}			= 1;
		$t{dic}{"billing_number"}				= &format_E164_number($billing_number_e164,"USA");
		$t{dic}{"billing_country_name"}			= (exists($country_codes{$billing_number_country})) ? $country_codes{$billing_number_country} : "";
		$t{dic}{"billing_country_code"}			= $billing_number_country;
		%call_price = &multilevel_call_get_rate($billing_number_e164,1,"product_rate_callback");
		if ($call_price{rate_found} eq 1) {
			$t{dic}{"billing_rate_found"}			= 1;
			$t{dic}{"billing_rate_per_minute"}		= ($call_price{rate_per_minute}<0.01) ? &format_number($call_price{rate_per_minute},4) : &format_number($call_price{rate_per_minute},2);
			$t{dic}{"billing_duration_per_1_dollar"}= &format_time(60*(1/$call_price{rate_per_minute}));
			$t{dic}{"billing_value_per_hour"}		= &format_number(($call_price{rate_per_minute}*60),2);
			$t{dic}{"billing_rate_name"}			= $call_price{rate_name};
		}
	}
    #
    #--------------------------------------------------
    # print page
    #--------------------------------------------------
	$t{dic}{"error"} = ($t{dic}{"error_wrong_number"} 						eq 1) ? 1 : $t{dic}{"error"};
	$t{dic}{"error"} = ($t{dic}{"error_usa_no_areacode"} 					eq 1) ? 1 : $t{dic}{"error"};
	$t{dic}{"error"} = ($t{dic}{"error_not_e164"} 							eq 1) ? 1 : $t{dic}{"error"};
	$t{dic}{"error"} = ($t{dic}{"error_unknown_country"} 					eq 1) ? 1 : $t{dic}{"error"};
	$t{dic}{"error"} = ($t{dic}{"error_ani_in_use"}							eq 1) ? 1 : $t{dic}{"error"};
	$t{dic}{"error"} = ($t{dic}{"error_ani_blocked_for_pin_locked_service"} eq 1) ? 1 : $t{dic}{"error"};
	$t{dic}{"error"} = ($t{dic}{"error_bad_ani_confirmation"} 				eq 1) ? 1 : $t{dic}{"error"};
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
	foreach(sort keys %{$t{dic}}) {if ($_ eq "debug") {next} $t{dic}{"debug"} .= "TEMPLATE DUMP -- $_=$t{dic}{$_}<br>";}
	&template_print("template.pbx.ani.html",%t);
}


sub do_save_global(){

	$callback = clean_int(substr($form{"callback"},0,1024));
	$routeann = clean_int(substr($form{"routeann"},0,1024));
	$balanceann = clean_int(substr($form{"balanceann"},0,1024));
	#print "Content-type: text/html\n\n";
	
	
	#change by yassine $index <= 53  to $index <= 148
	for ($index = 1; $index <= 148; $index++) {  
		&data_set("service_data",$app{service_id},"dst_".$index."_callback"        ,$callback);
		&data_set("service_data",$app{service_id},"dst_".$index."_routeann"        ,$routeann);
		&data_set("service_data",$app{service_id},"dst_".$index."_balanceann"        ,$balanceann);
	}

	#$sql = "update service_data set value='$callback' where name like 'dst_%_callback' and target='$app{service_id}'";
	#&database_do($sql);
	#$sql = "update service_data set value='$routeann' where name like 'dst_%_routeann' and target='$app{service_id}'";
	#&database_do($sql);	
	#$sql = "update service_data set value='$balanceann' where name like 'dst_%_balanceann' and target='$app{service_id}'";
	#&database_do($sql);
	
	
	cgi_redirect($my_url);
	exit;
	
}
sub do_dst(){
    #
    #--------------------------------------------------
    # start default values
    #--------------------------------------------------
	$ok = 1;
	$index = "";
    %t = %template_default;
    $t{dic}{my_url} 						= $my_url;
    $t{dic}{"error"} 						= 0;
    $t{dic}{"error_number_format"} 			= 0;
    $t{dic}{"error_number_e164_format"} 	= 0;
    $t{dic}{"error_number_skype_format"}	= 0;
    $t{dic}{"error_number_no_rate"} 		= 0;
    $t{dic}{"error_number_unknown_country"} = 0;
	$t{dic}{"error_no_more_index"} 			= 0;
    $t{dic}{"error_bad_index"} 				= 0;
    $t{dic}{"number"} 						= "";
    $t{dic}{"name"} 						= "";
    $t{dic}{"callid"} 						= "";
    $t{dic}{"carrier"} 						= "";
	$t{dic}{"callback"}                     = "";
	$t{dic}{"routeann"}                     = "";
    $t{dic}{"balanceann"}                   = "";
    $t{dic}{"index"} 						= "";
    $t{dic}{"index_new"} 					= "";
    $index_range_low	= 1;
	# changed by yassine to allow more than 53 DID , 53->148
    $index_range_hi		= 148;  
	foreach(sort keys %form) {$t{dic}{"debug"} .= "FORM DUMP -- $_=$form{$_}<br>";}
    #
    #--------------------------------------------------
    # get index by form or find a free one if new=1
    #--------------------------------------------------
	$t{dic}{"index_is_new"} = 0;
	if ($form{new} eq 1) {
		$sql = "select name, value from service_data where target='$app{service_id}' and name like 'dst_%_number'";
		%dstNumber = database_select_as_hash($sql, "value");
		foreach $loop ($index_range_low..$index_range_hi) {
			#if (&data_get("service_data",$app{service_id},"dst_".$loop."_number") eq "")
			if ( $dstNumber{"dst_".$loop."_number"}{value} eq "")
			{
				$index = $loop;
				last;
			}
		}
		if ($index eq "") {$t{dic}{"error"} = 1; $t{dic}{"error_no_more_index"} = 1;$ok = 0;}
		$t{dic}{"index_is_new"} = 1;
	} else {
		$index = &clean_int(substr($form{index},0,10));
		if ( ($index<$index_range_low) || ($index>$index_range_hi) || ($index eq "") ) {
			$t{dic}{"error"} = 1;
			$t{dic}{"error_bad_index"} = 1;
			$ok = 0;
		}
	}
	$t{dic}{"index"} = $index;
    #
    #--------------------------------------------------
    # check new index
    #--------------------------------------------------
	$index_new = &clean_int(substr($form{index_new},0,10));
	if ( ($index_new<$index_range_low) || ($index_new>$index_range_hi) || ($index_new eq "") ) {
		$index_new = "";
	}
	$t{dic}{"index_new"} = $index_new;
    #
    #--------------------------------------------------
    # try to delete
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{delete} eq 1) ) {
		# delete data
		&data_delete("service_data",$app{service_id},"dst_".$index."_name");
		&data_delete("service_data",$app{service_id},"dst_".$index."_number");
		&data_delete("service_data",$app{service_id},"dst_".$index."_callid");
		&data_delete("service_data",$app{service_id},"dst_".$index."_carrier");
		&data_delete("service_data",$app{service_id},"dst_".$index."_rslot");
		&data_delete("service_data",$app{service_id},"dst_".$index."_callback");
		&data_delete("service_data",$app{service_id},"dst_".$index."_routeann");
		&data_delete("service_data",$app{service_id},"dst_".$index."_balanceann");

		# return to status
		cgi_redirect("$my_url#dst");
		exit;
	}
    #
    #--------------------------------------------------
    # try to save
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} eq 1) ) {
		# clean from data
		$number	= clean_str(substr($form{"number"},0,1024),":-_()+.");
		$name	= clean_str(substr($form{"name"},0,1024),"-_():<>\@.");
		$callid	= clean_int(substr($form{"callid"},0,1024));
		$carrier= clean_str(substr($form{"carrier"},0,1024));
		$carrier= (exists($carriers_list{$carrier})) ? $carrier : "";
		$rslot	= clean_int(substr($form{"rslot"},0,1024));
		$rslot	= (index("|1|2|3|4|5|6|7|8|9|","|$rslot|") eq -1) ? 1 : $rslot;
		
		#$callback = clean_int(substr($form{"callback"},0,1024));
		
		$callback = &data_get("service_data",$app{service_id},"dst_1_callback");
		$routeann = &data_get("service_data",$app{service_id},"dst_1_routeann");
		$balanceann = &data_get("service_data",$app{service_id},"dst_1_balanceann");
		
		$callback = $callback?$callback:0;
		$routeann = $rslot?$rslot:0;
		$balanceann = $balanceann?$balanceann:0;
		#$routeann = clean_int(substr($form{"routeann"},0,1024));
		#$balanceann = clean_int(substr($form{"balanceann"},0,1024));
		
		#$rslot	= &data_get("service_data",$app{service_id},"dst_".$index."_rslot");
		#		
		# check and format number
		($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($number);
		$t{dic}{number_status} 				= $number_status;
		$t{dic}{number_raw} 				= $number;
		$t{dic}{number_clean} 				= $number_clean;
		$t{dic}{number_format} 				= $number_format;
		$t{dic}{number_format_skype}		= ($number_format eq "SKYPE") ? 1 : 0;
		$t{dic}{number_format_sip}			= ($number_format eq "SIP") ? 1 : 0;
		if ($number_status ne "OK") {
			$ok = 0;
			$t{dic}{"error"} = 1;
			if ($number_format eq "SKYPE") {
			    $t{dic}{"error_number_skype_format"} = 1;
			} elsif ($number_format eq "SIP") {
				if ($number_status eq "UNKNOWNCOUNTRY") {
				    $t{dic}{"error_number_unknown_country"} = 1;
				} else {
				    $t{dic}{"error_number_e164_format"} = 1;
				}
			} else {
			    $t{dic}{"error_number_format"} = 1;
			}
		} else {
			$number = $number_clean;
		}
		#		
		# check rate
		if ($ok eq 1) {
			#
			# pega rate_table, baseado no status do servico e slot da extensao
			$rate_table_id = "";
			$sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9 from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
			%hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9");
			%rateSlots = %hash;
			if ($hash{1}{flag} eq "1") {
				$user_slot = &data_get("service_data",$app{service_id},"dst_".$index."_rslot") || 1;
				$rate_table_id = $hash{1}{rate_slot_1};
				$rate_table_id = ( ($user_slot eq 1) && ($hash{1}{rate_slot_1} ne "") ) ? $hash{1}{rate_slot_1} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 2) && ($hash{1}{rate_slot_2} ne "") ) ? $hash{1}{rate_slot_2} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 3) && ($hash{1}{rate_slot_3} ne "") ) ? $hash{1}{rate_slot_3} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 4) && ($hash{1}{rate_slot_4} ne "") ) ? $hash{1}{rate_slot_4} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 5) && ($hash{1}{rate_slot_5} ne "") ) ? $hash{1}{rate_slot_5} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 6) && ($hash{1}{rate_slot_6} ne "") ) ? $hash{1}{rate_slot_6} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 7) && ($hash{1}{rate_slot_7} ne "") ) ? $hash{1}{rate_slot_7} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 8) && ($hash{1}{rate_slot_8} ne "") ) ? $hash{1}{rate_slot_8} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 9) && ($hash{1}{rate_slot_9} ne "") ) ? $hash{1}{rate_slot_9} : $rate_table_id;
			}
			#
			# agora tenta pegar rate
			if ($rate_table_id ne "") {
				%hash = &multilevel_rate_table_get($number,$rate_table_id);
				
				for($routeId=1;$routeId<=9 && ($hash{ok_to_use} ne 1);$routeId++){
					$rate_table_id = $rateSlots{1}{"rate_slot_$routeId"};
					%hash = &multilevel_rate_table_get($number,$rate_table_id);
				}
				
				if ($hash{ok_to_use} ne 1) {
					$t{dic}{"error"} = 1;
				    $t{dic}{"error_number_no_rate"} = 1;
					$ok = 0;
					
				}
			} else {
				$t{dic}{"error"} = 1;
			    $t{dic}{"error_number_no_rate"} = 1;
				$ok = 0;
			}
		}
		#
		# if all ok, lets save data
		if ($ok eq 1) {
			if ( ($index_new ne "") && ($index_new ne $index) ) {
				$v1 = &data_get("service_data",$app{service_id},"dst_".$index_new."_callid");
				$v2 = &data_get("service_data",$app{service_id},"dst_".$index_new."_number");
				$v3 = &data_get("service_data",$app{service_id},"dst_".$index_new."_name");
				$v4 = &data_get("service_data",$app{service_id},"dst_".$index_new."_carrier");
				$v5 = &data_get("service_data",$app{service_id},"dst_".$index_new."_rslot");
				&data_set("service_data",$app{service_id},"dst_".$index_new."_name"		,$name);
				&data_set("service_data",$app{service_id},"dst_".$index_new."_callid"	,$callid);
				&data_set("service_data",$app{service_id},"dst_".$index_new."_number"	,$number);
				&data_set("service_data",$app{service_id},"dst_".$index_new."_carrier"	,$carrier);
				&data_set("service_data",$app{service_id},"dst_".$index_new."_rslot"	,$rslot);
				&data_set("service_data",$app{service_id},"dst_".$index."_name"		,$v3);
				&data_set("service_data",$app{service_id},"dst_".$index."_callid"	,$v1);
				&data_set("service_data",$app{service_id},"dst_".$index."_number"	,$v2);
				&data_set("service_data",$app{service_id},"dst_".$index."_carrier"	,$v4);
				&data_set("service_data",$app{service_id},"dst_".$index."_rslot"	,$v5);
				&data_set("service_data",$app{service_id},"dst_".$index."_callback"        ,$callback);
				&data_set("service_data",$app{service_id},"dst_".$index."_routeann"        ,$routeann);
			    &data_set("service_data",$app{service_id},"dst_".$index."_balanceann"        ,$balanceann);	

			} else {
				&data_set("service_data",$app{service_id},"dst_".$index."_name"		,$name);
				&data_set("service_data",$app{service_id},"dst_".$index."_callid"	,$callid);
				&data_set("service_data",$app{service_id},"dst_".$index."_number"	,$number);
				&data_set("service_data",$app{service_id},"dst_".$index."_carrier"	,$carrier);
				&data_set("service_data",$app{service_id},"dst_".$index."_rslot"	,$rslot);
				&data_set("service_data",$app{service_id},"dst_".$index."_callback"        ,$callback);
				&data_set("service_data",$app{service_id},"dst_".$index."_routeann"        ,$routeann);
				&data_set("service_data",$app{service_id},"dst_".$index."_balanceann"      ,$balanceann);
			}
			# save data
			# return to status
			cgi_redirect("$my_url#dst");
			exit;
		}
	}
    #
    #--------------------------------------------------
    # if not save, then load
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} ne 1) ) {
		#$form{"callid"}	= &format_dial_number(&data_get("service_data",$app{service_id},"dst_".$index."_callid"));
		$form{"callid"}	= &data_get("service_data",$app{service_id},"dst_".$index."_callid");
		$form{"number"} = &multiformat_phone_number_format_for_user(&data_get("service_data",$app{service_id},"dst_".$index."_number"),"USA");
		$form{"name"} 	= &data_get("service_data",$app{service_id},"dst_".$index."_name");
		$form{"carrier"}= &data_get("service_data",$app{service_id},"dst_".$index."_carrier");
		$form{"carrier"}= (exists($carriers_list{$form{"carrier"}})) ? $form{"carrier"} : "";
		$form{"rslot"}	= &data_get("service_data",$app{service_id},"dst_".$index."_rslot");
		$form{"callback"}  = &data_get("service_data",$app{service_id},"dst_".$index."_callback");
		$form{"routeann"}  = &data_get("service_data",$app{service_id},"dst_".$index."_routeann");
		$form{"balanceann"}  = &data_get("service_data",$app{service_id},"dst_".$index."_balanceann");

		$t{dic}{"freeminutes_this_dest"}  = &data_get("service_data",$app{service_id},"dst_".$index."_freeminutes");
		
		
		$sql = "select 1,1,value from service_coupon_type_slice  where coupon_type_id=2  order by sequence asc  limit 1";
		
		%hash = database_select_as_hash($sql,"flag,value");
		
		if ($hash{1}{flag} eq 1) {
			$t{dic}{"freeminutes_per_dest"} = $hash{1}{value};
		}else {
			$t{dic}{"freeminutes_per_dest"} = 20;
			
		}
				
		if ($t{dic}{"freeminutes_this_dest"} eq "") {
			 
			 	$t{dic}{"freeminutes_this_dest"} = $t{dic}{"freeminutes_per_dest"} ;
		}

	}
	
	#
    #--------------------------------------------------
    # Check auto recharge is enabled or not
    #--------------------------------------------------
	$out = 0;
	$sql = "select 1,1,is_auto_recharge from service_profile_cc  where service_id='$app{service_id}' order by id desc limit 1";

	%hash = database_select_as_hash($sql,"flag,is_auto_recharge");
	if ($hash{1}{flag} eq 1) {
		$out = $hash{1}{is_auto_recharge};
	}
	$t{dic}{"is_auto_recharge"} = $out ;
	
    #
    #--------------------------------------------------
    # get list of free slots
    #--------------------------------------------------
	
	$sql = "select name, value from service_data where target='$app{service_id}' and name like 'dst_%_number'";
	%dstNumber = database_select_as_hash($sql, "value");
	
	$sql = "select name, value from service_data where target='$app{service_id}' and name like 'dst_%_name'";
	%dstName = database_select_as_hash($sql, "value");
	
	
	foreach $loop ($index_range_low..$index_range_hi) {
		$v1 = $dstNumber{"dst_".$loop."_number"}{value}; #&data_get("service_data",$app{service_id},"dst_".$loop."_number");
		$v2 = $dstName{"dst_".$loop."_name"}{value}; #&data_get("service_data",$app{service_id},"dst_".$loop."_name");
		
	
		$t{dic}{"index_".$loop."_is_free"} 	= ($v1 eq "") ? 1 : 0;
		$t{dic}{"index_".$loop."_number"} 	= $v1; 
		$t{dic}{"index_".$loop."_name"} 	= $v2;
		$t{dic}{"index_".$loop."_is_active"}= ($loop eq $index) ? 1 : 0; 
		
		
	}
    #
    #--------------------------------------------------
    # carrier list
    #--------------------------------------------------
	foreach $loop (keys %carriers_list) {
		$t{dic}{"carriers_list_".$loop."_is_selected"} = ($form{"carrier"} eq $loop) ? 1 : 0;
	}

    #  default callback option is disable callback
	if ($form{"callback"} eq "") {
		$form{"callback"} = 2;
	}

	$t{dic}{"callback_option_0_is_selected"} = ($form{"callback"} eq "0") ? 1 : 0;
	$t{dic}{"callback_option_1_is_selected"} = ($form{"callback"} eq "1") ? 1 : 0;
	$t{dic}{"callback_option_2_is_selected"} = ($form{"callback"} eq "2") ? 1 : 0;
   
	$t{dic}{"routeann_option_0_is_selected"} = ($form{"routeann"} eq "0") ? 1 : 0;
    $t{dic}{"routeann_option_1_is_selected"} = ($form{"routeann"} ne "0") ? 1 : 0;

	$t{dic}{"balanceann_option_0_is_selected"} = ($form{"balanceann"} eq "0") ? 1 : 0;
    $t{dic}{"balanceann_option_1_is_selected"} = ($form{"balanceann"} ne "1") ? 0 : 1;

    #
    #--------------------------------------------------
    # get rate for this number
    #--------------------------------------------------
	$t{dic}{"number"}	= $form{"number"};
	$t{dic}{"name"}		= $form{"name"};
	$t{dic}{"callid"}	= $form{"callid"};
	$t{dic}{"carrier"}	= $form{"carrier"};
	$t{dic}{"rslot"}	= $form{"rslot"};
	$t{dic}{"billing_rate_found"}			= 0;
	$t{dic}{"billing_rate_per_minute"}		= "";
	$t{dic}{"billing_duration_per_1_dollar"}= "";
	$t{dic}{"billing_value_per_hour"}		= "";
	$t{dic}{"billing_country_name"}			= "";
	$t{dic}{"billing_country_code"}			= "";
	$t{dic}{"billing_rate_name"}			= "";
	$t{dic}{"billing_number"}				= &data_get("service_data",$app{service_id},"dst_".$index."_number");
	$t{dic}{"billing_route"}				= &data_get("service_data",$app{service_id},"dst_".$index."_rslot") || 1;
	$t{dic}{"billing_number_ok"}			= 0;
	$t{dic}{"billing_rate_table_id"}		= "";
	$sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9, service_status.rate_slot_1_name,service_status.rate_slot_2_name,service_status.rate_slot_3_name,service_status.rate_slot_4_name,service_status.rate_slot_5_name,service_status.rate_slot_6_name,service_status.rate_slot_7_name,service_status.rate_slot_8_name,service_status.rate_slot_9 from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
	%hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9,rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,rate_slot_5_name,rate_slot_6_name,rate_slot_7_name,rate_slot_8_name,rate_slot_9");
	if ($hash{1}{flag} eq "1") {
		$t{dic}{"billing_route_1_name"} 	= $hash{1}{"rate_slot_1_name"};
		$t{dic}{"billing_route_2_name"} 	= $hash{1}{"rate_slot_2_name"};
		$t{dic}{"billing_route_3_name"} 	= $hash{1}{"rate_slot_3_name"};
		$t{dic}{"billing_route_4_name"} 	= $hash{1}{"rate_slot_4_name"};
		$t{dic}{"billing_route_5_name"} 	= $hash{1}{"rate_slot_5_name"};
		$t{dic}{"billing_route_6_name"} 	= $hash{1}{"rate_slot_6_name"};
		$t{dic}{"billing_route_7_name"} 	= $hash{1}{"rate_slot_7_name"};
		$t{dic}{"billing_route_8_name"} 	= $hash{1}{"rate_slot_8_name"};
		$t{dic}{"billing_route_9_name"} 	= $hash{1}{"rate_slot_9_name"};
		$t{dic}{"billing_route_1_rate_id"} 	= $hash{1}{rate_slot_1};
		$t{dic}{"billing_route_2_rate_id"} 	= $hash{1}{rate_slot_2};
		$t{dic}{"billing_route_3_rate_id"} 	= $hash{1}{rate_slot_3};
		$t{dic}{"billing_route_4_rate_id"} 	= $hash{1}{rate_slot_4};
		$t{dic}{"billing_route_5_rate_id"} 	= $hash{1}{rate_slot_5};
		$t{dic}{"billing_route_6_rate_id"} 	= $hash{1}{rate_slot_6};
		$t{dic}{"billing_route_7_rate_id"} 	= $hash{1}{rate_slot_7};
		$t{dic}{"billing_route_8_rate_id"} 	= $hash{1}{rate_slot_8};
		$t{dic}{"billing_route_9_rate_id"} 	= $hash{1}{rate_slot_9};
		$t{dic}{"billing_route_name"} 		= $hash{1}{"rate_slot_".$t{dic}{"billing_route"}."_name"};
	}
	if ($t{dic}{"billing_number"} ne "") {
		foreach $i (1..9) {
			# pega rate_id conforme slot_id
			$t{dic}{"billing_rate_table_id"} = ( ($t{dic}{"billing_route"} eq $i) && ($t{dic}{"billing_route_".$i."_rate_id"} ne "") ) ? $t{dic}{"billing_route_".$i."_rate_id"} : $t{dic}{"billing_rate_table_id"};
			# pega o rate-per-minute em cada slot
			if ($t{dic}{"billing_route_".$i."_rate_id"} eq "") {next} 
			%hash = &multilevel_rate_table_get($t{dic}{"billing_number"},$t{dic}{"billing_route_".$i."_rate_id"});
			$t{dic}{"billing_route_".$i."_rate_per_minute"} = "";
			if ($hash{ok_to_use} eq 1) {
				$t{dic}{"billing_route_".$i."_rate_per_minute"}	= ($hash{rate_per_minute}<0.01) ? &format_number($hash{rate_per_minute},4) : &format_number($hash{rate_per_minute},2);
			}
		}
		# pega rate desse numero no slot rate_id especificado pelo slot
		if ($t{dic}{"billing_rate_table_id"} ne "") {
			warning("+++billing rate table id:".$t{dic}{"billing_rate_table_id"});
			%call_price = &multilevel_rate_table_get($t{dic}{"billing_number"},$t{dic}{"billing_rate_table_id"});

			if ($call_price{ok_to_use} eq 1) {
				%country_codes 	= database_select_as_hash("select code,name from country");
				$t{dic}{"billing_number_ok"}			= 1;
				$t{dic}{"billing_number"}				= &multiformat_phone_number_format_for_user($t{dic}{"billing_number"},"USA");
				$t{dic}{"billing_country_name"}			= (exists($country_codes{$call_price{rate_country}})) ? $country_codes{$call_price{rate_country}} : "";
				$t{dic}{"billing_country_code"}			= $call_price{rate_country};
				$t{dic}{"billing_rate_found"}			= 1;
				$t{dic}{"billing_rate_per_minute"}		= ($call_price{rate_per_minute}<0.01) ? &format_number($call_price{rate_per_minute},4) : &format_number($call_price{rate_per_minute},2);
				
				if ($call_price{rate_per_minute} > 0) {
					$t{dic}{"billing_duration_per_1_dollar"}= &format_time(60*(1/$call_price{rate_per_minute}));
				}
				$t{dic}{"billing_value_per_hour"}		= &format_number(($call_price{rate_per_minute}*60),2);
				$t{dic}{"billing_rate_name"}			= $call_price{rate_name};
			}
		}
	}
    #
    #--------------------------------------------------
    # print page
    #--------------------------------------------------
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
	#foreach(sort keys %{$t{dic}}) {if ($_ eq "debug") {next} $t{dic}{"debug"} .= "TEMPLATE DUMP -- $_=$t{dic}{$_}<br>";}
    &template_print("template.pbx.dst.html",%t);
	exit;
}
sub do_dst_skype(){
    #
    #--------------------------------------------------
    # start default values
    #--------------------------------------------------
	$ok = 1;
	$index = "";
    %t = %template_default;
    $t{dic}{my_url} 						= $my_url;
    $t{dic}{"error"} 						= 0;
    $t{dic}{"error_number_format"} 			= 0;
    $t{dic}{"error_number_e164_format"} 	= 0;
    $t{dic}{"error_number_skype_format"}	= 0;
    $t{dic}{"error_number_no_rate"} 		= 0;
    $t{dic}{"error_number_unknown_country"} = 0;
	$t{dic}{"error_no_more_index"} 			= 0;
    $t{dic}{"error_bad_index"} 				= 0;
    $t{dic}{"number"} 						= "";
    $t{dic}{"name"} 						= "";
    $t{dic}{"callid"} 						= "";
    $t{dic}{"carrier"} 						= "";
    $t{dic}{"callback"}						="";
    $t{dic}{"index"} 						= "";
    $t{dic}{"index_new"} 					= "";
    $index_range_low	= 1001;
    $index_range_hi		= 1025;    
	foreach(sort keys %form) {$t{dic}{"debug"} .= "FORM DUMP -- $_=$form{$_}<br>";}
    #
    #--------------------------------------------------
    # get index by form or find a free one if new=1
    #--------------------------------------------------
	$t{dic}{"index_is_new"} = 0;
	if ($form{new} eq 1) {
		$sql = "select name, value from service_data where target='$app{service_id}' and name like 'dst_%_number'";
		%dstHash = database_select_as_hash($sql, "value");
		foreach $loop ($index_range_low..$index_range_hi) {
			#if (&data_get("service_data",$app{service_id},"dst_".$loop."_number") eq "")
			if ( $dstHash{"dst_".$loop."_number"}{value} eq "")
			{
				$index = $loop;
				last;
			}
		}
		if ($index eq "") {$t{dic}{"error"} = 1; $t{dic}{"error_no_more_index"} = 1;$ok = 0;}
		$t{dic}{"index_is_new"} = 1;
	} else {
		$index = &clean_int(substr($form{index},0,10));
		if ( ($index<$index_range_low) || ($index>$index_range_hi) || ($index eq "") ) {
			$t{dic}{"error"} = 1;
			$t{dic}{"error_bad_index"} = 1;
			$ok = 0;
		}
	}
	$t{dic}{"index"} = $index;
    #
    #--------------------------------------------------
    # check new index
    #--------------------------------------------------
	$index_new = &clean_int(substr($form{index_new},0,10));
	if ( ($index_new<$index_range_low) || ($index_new>$index_range_hi) || ($index_new eq "") ) {
		$index_new = "";
	}
	$t{dic}{"index_new"} = $index_new;
    #
    #--------------------------------------------------
    # try to delete
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{delete} eq 1) ) {
		# delete data
		&data_delete("service_data",$app{service_id},"dst_".$index."_name");
		&data_delete("service_data",$app{service_id},"dst_".$index."_number");
		&data_delete("service_data",$app{service_id},"dst_".$index."_callid");
		&data_delete("service_data",$app{service_id},"dst_".$index."_carrier");
		&data_delete("service_data",$app{service_id},"dst_".$index."_rslot");
		&data_delete("service_data",$app{service_id},"dst_".$index."_callback");	
		# return to status
		cgi_redirect("$my_url#dst");
		exit;
	}
    #
    #--------------------------------------------------
    # try to save
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} eq 1) ) {
		# clean from data
		$number	= clean_str(substr($form{"number"},0,1024),":-_()+.");
		$name	= clean_str(substr($form{"name"},0,1024),"-_():<>\@.");
		$rslot	= 1;
		#		
		# check and format number
		($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($number);
		$t{dic}{number_status} 				= $number_status;
		$t{dic}{number_raw} 				= $number;
		$t{dic}{number_clean} 				= $number_clean;
		$t{dic}{number_format} 				= $number_format;
		$t{dic}{number_format_skype}		= ($number_format eq "SKYPE") ? 1 : 0;
		$t{dic}{number_format_sip}			= ($number_format eq "SIP") ? 1 : 0;
		if ($number_status ne "OK") {
			$ok = 0;
			$t{dic}{"error"} = 1;
			if ($number_format eq "SKYPE") {
			    $t{dic}{"error_number_skype_format"} = 1;
			} elsif ($number_format eq "SIP") {
				if ($number_status eq "UNKNOWNCOUNTRY") {
				    $t{dic}{"error_number_unknown_country"} = 1;
				} else {
				    $t{dic}{"error_number_e164_format"} = 1;
				}
			} else {
			    $t{dic}{"error_number_format"} = 1;
			}
		} else {
			$number = $number_clean;
		}
		#		
		# check rate
		if ($ok eq 1) {
			#
			# pega rate_table, baseado no status do servico e slot da extensao
			$rate_table_id = "";
			$sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9 from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
			%hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9");
			if ($hash{1}{flag} eq "1") {
				$user_slot = &data_get("service_data",$app{service_id},"dst_".$index."_rslot") || 1;
				$rate_table_id = $hash{1}{rate_slot_1};
			}
			#
			# agora tenta pegar rate
			if ($rate_table_id ne "") {
				%hash = &multilevel_rate_table_get($number,$rate_table_id);
				if ($hash{ok_to_use} ne 1) {
					$t{dic}{"error"} = 1;
				    $t{dic}{"error_number_no_rate"} = 1;
					$ok = 0;
				}
			} else {
				$t{dic}{"error"} = 1;
			    $t{dic}{"error_number_no_rate"} = 1;
				$ok = 0;
			}
		}
		#
		# if all ok, lets save data
		if ($ok eq 1) {
			if ( ($index_new ne "") && ($index_new ne $index) ) {
				$v2 = &data_get("service_data",$app{service_id},"dst_".$index_new."_number");
				$v3 = &data_get("service_data",$app{service_id},"dst_".$index_new."_name");
				$v5 = &data_get("service_data",$app{service_id},"dst_".$index_new."_rslot");
				&data_set("service_data",$app{service_id},"dst_".$index_new."_name"		,$name);
				&data_set("service_data",$app{service_id},"dst_".$index_new."_number"	,$number);
				&data_set("service_data",$app{service_id},"dst_".$index_new."_rslot"	,$rslot);
				&data_set("service_data",$app{service_id},"dst_".$index."_name"		,$v3);
				&data_set("service_data",$app{service_id},"dst_".$index."_number"	,$v2);
				&data_set("service_data",$app{service_id},"dst_".$index."_rslot"	,$v5);

				 &data_set("service_data",$app{service_id},"dst_".$index."_callback" ,$callback_option);
			
			} else {
				&data_set("service_data",$app{service_id},"dst_".$index."_name"		,$name);
				&data_set("service_data",$app{service_id},"dst_".$index."_number"	,$number);
				&data_set("service_data",$app{service_id},"dst_".$index."_rslot"	,$rslot);
				&data_set("service_data",$app{service_id},"dst_".$index."_callback" ,$callback_option);
			}
			# save data
			# return to status
			cgi_redirect("$my_url#skypedst");
			exit;
		}
	}
    #
    #--------------------------------------------------
    # if not save, then load
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} ne 1) ) {
		#$form{"callid"}	= &format_dial_number(&data_get("service_data",$app{service_id},"dst_".$index."_callid"));
		$form{"number"} = &multiformat_phone_number_format_for_user(&data_get("service_data",$app{service_id},"dst_".$index."_number"),"USA");
		$form{"name"} 	= &data_get("service_data",$app{service_id},"dst_".$index."_name");
		$form{"rslot"}	= 1;
	}
    #
    #--------------------------------------------------
    # get list of free slots
    #--------------------------------------------------
	$sql = "select name, value from service_data where tagrget='$app{service_id}' and name like 'dst_%_number'";
	%dstNumber = database_select_ash_hash($sql, "value");
	
	$sql = "select name, value from service_data where tagrget='$app{service_id}' and name like 'dst_%_name'";
	%dstName = database_select_ash_hash($sql, "value");
	
	foreach $loop ($index_range_low..$index_range_hi) {
		$v1 = $dstNumber{"dst_".$loop."_number"}{value}; #&data_get("service_data",$app{service_id},"dst_".$loop."_number");
		$v2 = $dstName{"dst_".$loop."_name"}{value}; #&data_get("service_data",$app{service_id},"dst_".$loop."_name");
		$t{dic}{"index_".$loop."_is_free"} 	= ($v1 eq "") ? 1 : 0;
		$t{dic}{"index_".$loop."_number"} 	= $v1; 
		$t{dic}{"index_".$loop."_name"} 	= $v2;
		$t{dic}{"index_".$loop."_is_active"}= ($loop eq $index) ? 1 : 0; 
	}
    #
    #--------------------------------------------------
    # carrier list
    #--------------------------------------------------
	foreach $loop (keys %carriers_list) {
		$t{dic}{"carriers_list_".$loop."_is_selected"} = ($form{"carrier"} eq $loop) ? 1 : 0;
	}
    #
    #--------------------------------------------------
    # get rate for this number
    #--------------------------------------------------
	$t{dic}{"number"}	= $form{"number"};
	$t{dic}{"name"}		= $form{"name"};
	$t{dic}{"callid"}	= $form{"callid"};
	$t{dic}{"carrier"}	= $form{"carrier"};
	$t{dic}{"rslot"}	= $form{"rslot"};
	$t{dic}{"billing_rate_found"}			= 0;
	$t{dic}{"billing_rate_per_minute"}		= "";
	$t{dic}{"billing_duration_per_1_dollar"}= "";
	$t{dic}{"billing_value_per_hour"}		= "";
	$t{dic}{"billing_country_name"}			= "";
	$t{dic}{"billing_country_code"}			= "";
	$t{dic}{"billing_rate_name"}			= "";
	$t{dic}{"billing_number"}				= &data_get("service_data",$app{service_id},"dst_".$index."_number");
	$t{dic}{"billing_route"}				= 1;
	$t{dic}{"billing_number_ok"}			= 0;
	$t{dic}{"billing_rate_table_id"}		= "";
	$sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9, service_status.rate_slot_1_name,service_status.rate_slot_2_name,service_status.rate_slot_3_name,service_status.rate_slot_4_name,service_status.rate_slot_5_name,service_status.rate_slot_6_name,service_status.rate_slot_7_name,service_status.rate_slot_8_name,service_status.rate_slot_9 from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
	%hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9,rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,rate_slot_5_name,rate_slot_6_name,rate_slot_7_name,rate_slot_8_name,rate_slot_9");
	if ($hash{1}{flag} eq "1") {
		$t{dic}{"billing_route_1_name"} 	= $hash{1}{"rate_slot_1_name"};
		$t{dic}{"billing_route_2_name"} 	= $hash{1}{"rate_slot_2_name"};
		$t{dic}{"billing_route_3_name"} 	= $hash{1}{"rate_slot_3_name"};
		$t{dic}{"billing_route_4_name"} 	= $hash{1}{"rate_slot_4_name"};
		$t{dic}{"billing_route_5_name"} 	= $hash{1}{"rate_slot_5_name"};
		$t{dic}{"billing_route_6_name"} 	= $hash{1}{"rate_slot_6_name"};
		$t{dic}{"billing_route_7_name"} 	= $hash{1}{"rate_slot_7_name"};
		$t{dic}{"billing_route_8_name"} 	= $hash{1}{"rate_slot_8_name"};
		$t{dic}{"billing_route_9_name"} 	= $hash{1}{"rate_slot_9_name"};
		$t{dic}{"billing_route_1_rate_id"} 	= $hash{1}{rate_slot_1};
		$t{dic}{"billing_route_2_rate_id"} 	= $hash{1}{rate_slot_2};
		$t{dic}{"billing_route_3_rate_id"} 	= $hash{1}{rate_slot_3};
		$t{dic}{"billing_route_4_rate_id"} 	= $hash{1}{rate_slot_4};
		$t{dic}{"billing_route_5_rate_id"} 	= $hash{1}{rate_slot_5};
		$t{dic}{"billing_route_6_rate_id"} 	= $hash{1}{rate_slot_6};
		$t{dic}{"billing_route_7_rate_id"} 	= $hash{1}{rate_slot_7};
		$t{dic}{"billing_route_8_rate_id"} 	= $hash{1}{rate_slot_8};
		$t{dic}{"billing_route_9_rate_id"} 	= $hash{1}{rate_slot_9};
		$t{dic}{"billing_route_name"} 		= $hash{1}{"rate_slot_".$t{dic}{"billing_route"}."_name"};
	}
	if ($t{dic}{"billing_number"} ne "") {
		foreach $i (1..9) {
			# pega rate_id conforme slot_id
			$t{dic}{"billing_rate_table_id"} = ( ($t{dic}{"billing_route"} eq $i) && ($t{dic}{"billing_route_".$i."_rate_id"} ne "") ) ? $t{dic}{"billing_route_".$i."_rate_id"} : $t{dic}{"billing_rate_table_id"};
			# pega o rate-per-minute em cada slot
			if ($t{dic}{"billing_route_".$i."_rate_id"} eq "") {next} 
			%hash = &multilevel_rate_table_get($t{dic}{"billing_number"},$t{dic}{"billing_route_".$i."_rate_id"});
			$t{dic}{"billing_route_".$i."_rate_per_minute"} = "";
			if ($hash{ok_to_use} eq 1) {
				$t{dic}{"billing_route_".$i."_rate_per_minute"}	= ($hash{rate_per_minute}<0.01) ? &format_number($hash{rate_per_minute},4) : &format_number($hash{rate_per_minute},2);
			}
		}
		# pega rate desse numero no slot rate_id especificado pelo slot
		if ($t{dic}{"billing_rate_table_id"} ne "") {
			%call_price = &multilevel_rate_table_get($t{dic}{"billing_number"},$t{dic}{"billing_rate_table_id"});
			if ($call_price{ok_to_use} eq 1) {
				%country_codes 	= database_select_as_hash("select code,name from country");
				$t{dic}{"billing_number_ok"}			= 1;
				$t{dic}{"billing_number"}				= &multiformat_phone_number_format_for_user($t{dic}{"billing_number"},"USA");
				$t{dic}{"billing_country_name"}			= (exists($country_codes{$call_price{rate_country}})) ? $country_codes{$call_price{rate_country}} : "";
				$t{dic}{"billing_country_code"}			= $call_price{rate_country};
				$t{dic}{"billing_rate_found"}			= 1;
				$t{dic}{"billing_rate_per_minute"}		= ($call_price{rate_per_minute}<0.01) ? &format_number($call_price{rate_per_minute},4) : &format_number($call_price{rate_per_minute},2);
				$t{dic}{"billing_duration_per_1_dollar"}= &format_time(60*(1/$call_price{rate_per_minute}));
				$t{dic}{"billing_value_per_hour"}		= &format_number(($call_price{rate_per_minute}*60),2);
				$t{dic}{"billing_rate_name"}			= $call_price{rate_name};
			}
		}
	}
    #
    #--------------------------------------------------
    # print page
    #--------------------------------------------------
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
	#foreach(sort keys %{$t{dic}}) {if ($_ eq "debug") {next} $t{dic}{"debug"} .= "TEMPLATE DUMP -- $_=$t{dic}{$_}<br>";}
    &template_print("template.pbx.dst.skype.html",%t);
	exit;
}

sub do_dst_radio(){
    #
    #--------------------------------------------------
    # start default values
    #--------------------------------------------------
	$ok = 1;
	$index = "";
    %t = %template_default;
    $t{dic}{my_url} 						= $my_url;
    $t{dic}{"error"} 						= 0;
    $t{dic}{"error_number_format"} 			= 0;
    $t{dic}{"error_number_e164_format"} 	= 0;
    $t{dic}{"error_number_skype_format"}	= 0;
    $t{dic}{"error_number_no_rate"} 		= 0;
    $t{dic}{"error_number_unknown_country"} = 0;
	$t{dic}{"error_no_more_index"} 			= 0;
    $t{dic}{"error_bad_index"} 				= 0;
    $t{dic}{"number"} 						= "";
    $t{dic}{"name"} 						= "";
    $t{dic}{"callid"} 						= "";
    $t{dic}{"carrier"} 						= "";
    $t{dic}{"index"} 						= "";
    $t{dic}{"index_new"} 					= "";
    $index_range_low	= 2001;
    $index_range_hi		= 2009;    
	foreach(sort keys %form) {$t{dic}{"debug"} .= "FORM DUMP -- $_=$form{$_}<br>";}
    #
    #--------------------------------------------------
    # get index by form or find a free one if new=1
    #--------------------------------------------------
	$t{dic}{"index_is_new"} = 0;
	if ($form{new} eq 1) {
		foreach $loop ($index_range_low..$index_range_hi) {
			if (&data_get("service_data",$app{service_id},"dst_".$loop."_number") eq "") {$index = $loop;last;}
		}
		if ($index eq "") {$t{dic}{"error"} = 1; $t{dic}{"error_no_more_index"} = 1;$ok = 0;}
		$t{dic}{"index_is_new"} = 1;
	} else {
		$index = &clean_int(substr($form{index},0,10));
		if ( ($index<$index_range_low) || ($index>$index_range_hi) || ($index eq "") ) {
			$t{dic}{"error"} = 1;
			$t{dic}{"error_bad_index"} = 1;
			$ok = 0;
		}
	}
	$t{dic}{"index"} = $index;
    #
    #--------------------------------------------------
    # check new index
    #--------------------------------------------------
	$index_new = &clean_int(substr($form{index_new},0,10));
	if ( ($index_new<$index_range_low) || ($index_new>$index_range_hi) || ($index_new eq "") ) {
		$index_new = "";
	}
	$t{dic}{"index_new"} = $index_new;
    #
    #--------------------------------------------------
    # try to delete
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{delete} eq 1) ) {
		# delete data
		&data_delete("service_data",$app{service_id},"dst_".$index."_name");
		&data_delete("service_data",$app{service_id},"dst_".$index."_number");
		&data_delete("service_data",$app{service_id},"dst_".$index."_callid");
		&data_delete("service_data",$app{service_id},"dst_".$index."_carrier");
		&data_delete("service_data",$app{service_id},"dst_".$index."_rslot");
		# return to status
		cgi_redirect("$my_url#dst");
		exit;
	}
    #
    #--------------------------------------------------
    # try to save
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} eq 1) ) {
		# clean from data
 
		$number	= clean_str(substr($form{"number"},0,1024),"-_()\:<>\/\@.");
		$name	= clean_str(substr($form{"name"},0,1024),"-_():<>\@.");
	 
		
		$rslot	= 1;
		#		
		# check and format number
		if  ($number eq "")   {
			$number_status = 'NOK' ; 	
		}else {
			$sql ="select 1,1,exten from musiconhold where exten='$number' limit 1";
			 %hash = database_select_as_hash($sql,"flag,exten");
			if ($hash{1}{flag} eq "1") {
				$number_status ='OK' ;
			}else {
			$number_status ='NOK' ;	
			}
			
		}
			
				
	 
	#	($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($number);
	
	 	$number_clean = $number;
	 	$number_format = "RADIO" ;
 
		$t{dic}{number_status} 				= 'OK';
		$t{dic}{number_raw} 				= $number;
		$t{dic}{number_clean} 				= $number;
		$t{dic}{number_format} 				= 'RADIO';
		$t{dic}{number_format_skype}		= ($number_format eq "SKYPE") ? 1 : 0;
		$t{dic}{number_format_sip}			= ($number_format eq "SIP") ? 1 : 0;
		$t{dic}{number_format_radio}		= ($number_format eq "RADIO") ? 1 : 0;
		if ($number_status ne "OK") {
			$ok = 0;
			$t{dic}{"error"} = 1;
			if ($number_format eq "RADIO") {
			    $t{dic}{"error_number_radio_format"} = 1;
			}else {
			    $t{dic}{"error_number_format"} = 1;
			}
		} else {
			$number = $number_clean;
		}
		#		
		# added by yang, why we need check rate for internet radio or skype ,let me ignore following 
		if ($ok eq 1) {
			#
			# pega rate_table, baseado no status do servico e slot da extensao
			$rate_table_id = "";
			$sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9 from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
			%hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9");
			if ($hash{1}{flag} eq "1") {
				$user_slot = &data_get("service_data",$app{service_id},"dst_".$index."_rslot") || 1;
				$rate_table_id = $hash{1}{rate_slot_1};
			}
			################################
			# I remove many lines ,by Yang,Compare with do_dst_skype() #
			###############################
 
		}
	 
		#
		# if all ok, lets save data
		if ($ok eq 1) {
			if ( ($index_new ne "") && ($index_new ne $index) ) {
				$v2 = &data_get("service_data",$app{service_id},"dst_".$index_new."_number");
				$v3 = &data_get("service_data",$app{service_id},"dst_".$index_new."_name");
				$v5 = &data_get("service_data",$app{service_id},"dst_".$index_new."_rslot");
				&data_set("service_data",$app{service_id},"dst_".$index_new."_name"		,$name);
				# because in radio url ,we have :, which will be removed in data_set()  ,so cannot use data_set function
				#	&data_set("service_data",$app{service_id},"dst_".$index_new."_number"	,$number);
			
				$name_numberfield = "dst_".$index_new."_number" ;
				database_do("delete from service_data where target='$app{service_id}' and name='$name_numberfield'");
				database_do("insert into service_data (target,name,value) values ('$app{service_id}','$name_numberfield','$number') ");
			
			
			
				&data_set("service_data",$app{service_id},"dst_".$index_new."_rslot"	,$rslot);
				&data_set("service_data",$app{service_id},"dst_".$index."_name"		,$v3);
				
				# because in radio url ,we have :, in data_set() we will remove : ,so cannot use data_set function
				#&data_set("service_data",$app{service_id},"dst_".$index."_number"	,$v2);
			
				$name_numberfield = "dst_".$index."_number" ;
				database_do("delete from service_data where target='$app{service_id}' and name='$name_numberfield'");
				database_do("insert into service_data (target,name,value) values ('$app{service_id}','$name_numberfield','$v2') ");
			 
				&data_set("service_data",$app{service_id},"dst_".$index."_rslot"	,$v5);
				
				
				
				
			} else {
				&data_set("service_data",$app{service_id},"dst_".$index."_name"		,$name);
			
				# because in radio url ,we have :, in data_set() we will remove : ,so cannot use data_set function
			 
				$name_numberfield = "dst_".$index."_number" ;
				database_do("delete from service_data where target='$app{service_id}' and name='$name_numberfield'");
				database_do("insert into service_data (target,name,value) values ('$app{service_id}','$name_numberfield','$number') ");
				#&data_set("service_data",$app{service_id},"dst_".$index."_number"	,$number);
				&data_set("service_data",$app{service_id},"dst_".$index."_rslot"	,$rslot);
			}
			# save data
		
			# return to status
			cgi_redirect("$my_url#radiodst");
			exit;
		}
	}
    #
    #--------------------------------------------------
    # if not save, then load
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} ne 1) ) {
		#$form{"callid"}	= &format_dial_number(&data_get("service_data",$app{service_id},"dst_".$index."_callid"));
		$form{"number"} = &data_get("service_data",$app{service_id},"dst_".$index."_number") ;
		$form{"name"} 	= &data_get("service_data",$app{service_id},"dst_".$index."_name");
		$form{"select_radio"} = $form{"number"} ;
		$form{"rslot"}	= 1;
	}
    #
    #--------------------------------------------------
    # get list of free slots
    #--------------------------------------------------
	foreach $loop ($index_range_low..$index_range_hi) {
		$v1 = &data_get("service_data",$app{service_id},"dst_".$loop."_number");
		$v2 = &data_get("service_data",$app{service_id},"dst_".$loop."_name");
		$t{dic}{"index_".$loop."_is_free"} 	= ($v1 eq "") ? 1 : 0;
		$t{dic}{"index_".$loop."_number"} 	= $v1; 
		$t{dic}{"index_".$loop."_name"} 	= $v2;
		$t{dic}{"index_".$loop."_is_active"}= ($loop eq $index) ? 1 : 0; 
	}
    #
    #--------------------------------------------------
    # carrier list
    #--------------------------------------------------
	foreach $loop (keys %carriers_list) {
		$t{dic}{"carriers_list_".$loop."_is_selected"} = ($form{"carrier"} eq $loop) ? 1 : 0;
	}
	 
	 
	
    #
    #--------------------------------------------------
    # get rate for this number
    #--------------------------------------------------
	$t{dic}{"number"}	= $form{"number"};
	$t{dic}{"name"}		= $form{"name"};
	$t{dic}{"callid"}	= $form{"callid"};
	$t{dic}{"carrier"}	= $form{"carrier"};
	$t{dic}{"rslot"}	= $form{"rslot"};
	$t{dic}{"billing_rate_found"}			= 0;
	$t{dic}{"billing_rate_per_minute"}		= "";
	$t{dic}{"billing_duration_per_1_dollar"}= "";
	$t{dic}{"billing_value_per_hour"}		= "";
	$t{dic}{"billing_country_name"}			= "";
	$t{dic}{"billing_country_code"}			= "";
	$t{dic}{"billing_rate_name"}			= "";
	$t{dic}{"billing_number"}				= &data_get("service_data",$app{service_id},"dst_".$index."_number");
	$t{dic}{"billing_route"}				= 1;
	$t{dic}{"billing_number_ok"}			= 0;
	$t{dic}{"billing_rate_table_id"}		= "";
	$sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9, service_status.rate_slot_1_name,service_status.rate_slot_2_name,service_status.rate_slot_3_name,service_status.rate_slot_4_name,service_status.rate_slot_5_name,service_status.rate_slot_6_name,service_status.rate_slot_7_name,service_status.rate_slot_8_name,service_status.rate_slot_9 from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
	%hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9,rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,rate_slot_5_name,rate_slot_6_name,rate_slot_7_name,rate_slot_8_name,rate_slot_9");
	if ($hash{1}{flag} eq "1") {
		$t{dic}{"billing_route_1_name"} 	= $hash{1}{"rate_slot_1_name"};
		$t{dic}{"billing_route_2_name"} 	= $hash{1}{"rate_slot_2_name"};
		$t{dic}{"billing_route_3_name"} 	= $hash{1}{"rate_slot_3_name"};
		$t{dic}{"billing_route_4_name"} 	= $hash{1}{"rate_slot_4_name"};
		$t{dic}{"billing_route_5_name"} 	= $hash{1}{"rate_slot_5_name"};
		$t{dic}{"billing_route_6_name"} 	= $hash{1}{"rate_slot_6_name"};
		$t{dic}{"billing_route_7_name"} 	= $hash{1}{"rate_slot_7_name"};
		$t{dic}{"billing_route_8_name"} 	= $hash{1}{"rate_slot_8_name"};
		$t{dic}{"billing_route_9_name"} 	= $hash{1}{"rate_slot_9_name"};
		$t{dic}{"billing_route_1_rate_id"} 	= $hash{1}{rate_slot_1};
		$t{dic}{"billing_route_2_rate_id"} 	= $hash{1}{rate_slot_2};
		$t{dic}{"billing_route_3_rate_id"} 	= $hash{1}{rate_slot_3};
		$t{dic}{"billing_route_4_rate_id"} 	= $hash{1}{rate_slot_4};
		$t{dic}{"billing_route_5_rate_id"} 	= $hash{1}{rate_slot_5};
		$t{dic}{"billing_route_6_rate_id"} 	= $hash{1}{rate_slot_6};
		$t{dic}{"billing_route_7_rate_id"} 	= $hash{1}{rate_slot_7};
		$t{dic}{"billing_route_8_rate_id"} 	= $hash{1}{rate_slot_8};
		$t{dic}{"billing_route_9_rate_id"} 	= $hash{1}{rate_slot_9};
		$t{dic}{"billing_route_name"} 		= $hash{1}{"rate_slot_".$t{dic}{"billing_route"}."_name"};
	}
	if ($t{dic}{"billing_number"} ne "") {
		foreach $i (1..9) {
			# pega rate_id conforme slot_id
			$t{dic}{"billing_rate_table_id"} = ( ($t{dic}{"billing_route"} eq $i) && ($t{dic}{"billing_route_".$i."_rate_id"} ne "") ) ? $t{dic}{"billing_route_".$i."_rate_id"} : $t{dic}{"billing_rate_table_id"};
			# pega o rate-per-minute em cada slot
			if ($t{dic}{"billing_route_".$i."_rate_id"} eq "") {next} 
			%hash = &multilevel_rate_table_get($t{dic}{"billing_number"},$t{dic}{"billing_route_".$i."_rate_id"});
			$t{dic}{"billing_route_".$i."_rate_per_minute"} = "";
			if ($hash{ok_to_use} eq 1) {
				$t{dic}{"billing_route_".$i."_rate_per_minute"}	= ($hash{rate_per_minute}<0.01) ? &format_number($hash{rate_per_minute},4) : &format_number($hash{rate_per_minute},2);
			}
		}
		# pega rate desse numero no slot rate_id especificado pelo slot
		if ($t{dic}{"billing_rate_table_id"} ne "") {
			%call_price = &multilevel_rate_table_get($t{dic}{"billing_number"},$t{dic}{"billing_rate_table_id"});
			if ($call_price{ok_to_use} eq 1) {
				%country_codes 	= database_select_as_hash("select code,name from country");
				$t{dic}{"billing_number_ok"}			= 1;
				$t{dic}{"billing_number"}				= &multiformat_phone_number_format_for_user($t{dic}{"billing_number"},"USA");
				$t{dic}{"billing_country_name"}			= (exists($country_codes{$call_price{rate_country}})) ? $country_codes{$call_price{rate_country}} : "";
				$t{dic}{"billing_country_code"}			= $call_price{rate_country};
				$t{dic}{"billing_rate_found"}			= 1;
				$t{dic}{"billing_rate_per_minute"}		= ($call_price{rate_per_minute}<0.01) ? &format_number($call_price{rate_per_minute},4) : &format_number($call_price{rate_per_minute},2);
				$t{dic}{"billing_duration_per_1_dollar"}= &format_time(60*(1/$call_price{rate_per_minute}));
				$t{dic}{"billing_value_per_hour"}		= &format_number(($call_price{rate_per_minute}*60),2);
				$t{dic}{"billing_rate_name"}			= $call_price{rate_name};
			}
		}
	}
    #
    #--------------------------------------------------
    # print page
    #--------------------------------------------------
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
	#foreach(sort keys %{$t{dic}}) {if ($_ eq "debug") {next} $t{dic}{"debug"} .= "TEMPLATE DUMP -- $_=$t{dic}{$_}<br>";}
    &template_print("template.pbx.dst.radio.html",%t);
	exit;
}


sub do_add_radio(){
    #
    #--------------------------------------------------
    # start default values
    #--------------------------------------------------
	$ok = 1;
	$index = "";
    %t = %template_default;
    $t{dic}{my_url} 						= $my_url;
    $t{dic}{"error"} 						= 0;
    $t{dic}{"error_number_format"} 			= 0;
    $t{dic}{"error_number_e164_format"} 	= 0;
    $t{dic}{"error_number_skype_format"}	= 0;
    $t{dic}{"error_number_no_rate"} 		= 0;
    $t{dic}{"error_number_unknown_country"} = 0;
	$t{dic}{"error_no_more_index"} 			= 0;
    $t{dic}{"error_bad_index"} 				= 0;
    $t{dic}{"number"} 						= "";
    $t{dic}{"name"} 						= "";
    $t{dic}{"callid"} 						= "";
    $t{dic}{"carrier"} 						= "";
    $t{dic}{"index"} 						= "";
    $t{dic}{"index_new"} 					= "";
    $index_range_low	= 2001;
    $index_range_hi		= 2009;    
	foreach(sort keys %form) {$t{dic}{"debug"} .= "FORM DUMP -- $_=$form{$_}<br>";}
    #
    #--------------------------------------------------
    # get index by form or find a free one if new=1
    #--------------------------------------------------
	$t{dic}{"index_is_new"} = 0;
	if ($form{new} eq 1) {
		foreach $loop ($index_range_low..$index_range_hi) {
			if (&data_get("service_data",$app{service_id},"dst_".$loop."_number") eq "") {$index = $loop;last;}
		}
		if ($index eq "") {$t{dic}{"error"} = 1; $t{dic}{"error_no_more_index"} = 1;$ok = 0;}
		$t{dic}{"index_is_new"} = 1;
	} else {
		$index = &clean_int(substr($form{index},0,10));
		if ( ($index<$index_range_low) || ($index>$index_range_hi) || ($index eq "") ) {
			$t{dic}{"error"} = 1;
			$t{dic}{"error_bad_index"} = 1;
			$ok = 0;
		}
	}
	$t{dic}{"index"} = $index;
    #
    #--------------------------------------------------
    # check new index
    #--------------------------------------------------
	$index_new = &clean_int(substr($form{index_new},0,10));
	if ( ($index_new<$index_range_low) || ($index_new>$index_range_hi) || ($index_new eq "") ) {
		$index_new = "";
	}
	$t{dic}{"index_new"} = $index_new;
    #
    #--------------------------------------------------
    # try to delete
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{delete} eq 1) ) {
		# delete data
		&data_delete("service_data",$app{service_id},"dst_".$index."_name");
		&data_delete("service_data",$app{service_id},"dst_".$index."_number");
		&data_delete("service_data",$app{service_id},"dst_".$index."_callid");
		&data_delete("service_data",$app{service_id},"dst_".$index."_carrier");
		&data_delete("service_data",$app{service_id},"dst_".$index."_rslot");
		# return to status
		cgi_redirect("$my_url#dst");
		exit;
	}
    #
    #--------------------------------------------------
    # try to save
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} eq 1) ) {
		# clean from data
 
		$number	= clean_str(substr($form{"number"},0,1024),"-_()\:<>\/\@.");
		$name	= clean_str(substr($form{"name"},0,1024),"-_():<>\@.");
		$select_radio =  $form{"select_radio"} ;
		if ($select_radio ne "-1") {
			$number = $select_radio ;
			$form{"number"} = '';
			
		}
		
		
		
		
		
		$rslot	= 1;
		#		
		# check and format number
		if  ($number eq "")   {
			$number_status = 'NOK' ; 	
		}elsif (substr($form{number},0,4) eq 'mms:') {
				$protocol_radio ='mms'; 
				$number_status = 'OK' ;
		}elsif ( substr($number,0,5) eq 'http:') {
			$protocol_radio ='shoutcast';
			$number_status = 'OK' ;
		}else {
			$number_status ='NOK' ;
		}
			
				
	 
	#	($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($number);
	
	 	$number_clean = $number;
 
		$t{dic}{number_status} 				= 'OK';
		$t{dic}{number_raw} 				= $number;
		$t{dic}{number_clean} 				= $number;
		$t{dic}{number_format} 				= 'RADIO';
		$t{dic}{number_format_skype}		= ($number_format eq "SKYPE") ? 1 : 0;
		$t{dic}{number_format_sip}			= ($number_format eq "SIP") ? 1 : 0;
		$t{dic}{number_format_radio}		= ($number_format eq "RADIO") ? 1 : 0;
		if ($number_status ne "OK") {
			$ok = 0;
			$t{dic}{"error"} = 1;
			if ($number_format eq "RADIO") {
			    $t{dic}{"error_number_radio_format"} = 0;
			} elsif ($number_format eq "SIP") {
				if ($number_status eq "UNKNOWNCOUNTRY") {
				    $t{dic}{"error_number_unknown_country"} = 1;
				} else {
				    $t{dic}{"error_number_e164_format"} = 1;
				}
			} else {
			    $t{dic}{"error_number_format"} = 1;
			}
		} else {
			$number = $number_clean;
		}
		#		
		# added by yang, why we need check rate for internet radio or skype ,let me ignore following 
		if ($ok eq 1) {
			#
			# pega rate_table, baseado no status do servico e slot da extensao
			$rate_table_id = "";
			$sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9 from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
			%hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9");
			if ($hash{1}{flag} eq "1") {
				$user_slot = &data_get("service_data",$app{service_id},"dst_".$index."_rslot") || 1;
				$rate_table_id = $hash{1}{rate_slot_1};
			}
			################################
			# I remove many lines ,by Yang,Compare with do_dst_skype() #
			###############################
 
		}
	 
		#
		# if all ok, lets save data
		if ($ok eq 1) {
			if ( ($index_new ne "") && ($index_new ne $index) ) {
				$v2 = &data_get("service_data",$app{service_id},"dst_".$index_new."_number");
				$v3 = &data_get("service_data",$app{service_id},"dst_".$index_new."_name");
				$v5 = &data_get("service_data",$app{service_id},"dst_".$index_new."_rslot");
				&data_set("service_data",$app{service_id},"dst_".$index_new."_name"		,$name);
				# because in radio url ,we have :, which will be removed in data_set()  ,so cannot use data_set function
				#	&data_set("service_data",$app{service_id},"dst_".$index_new."_number"	,$number);
			
				$name_numberfield = "dst_".$index_new."_number" ;
				database_do("delete from service_data where target='$app{service_id}' and name='$name_numberfield'");
				database_do("insert into service_data (target,name,value) values ('$app{service_id}','$name_numberfield','$number') ");
			
			
			
				&data_set("service_data",$app{service_id},"dst_".$index_new."_rslot"	,$rslot);
				&data_set("service_data",$app{service_id},"dst_".$index."_name"		,$v3);
				
				# because in radio url ,we have :, in data_set() we will remove : ,so cannot use data_set function
				#&data_set("service_data",$app{service_id},"dst_".$index."_number"	,$v2);
			
				$name_numberfield = "dst_".$index."_number" ;
				database_do("delete from service_data where target='$app{service_id}' and name='$name_numberfield'");
				database_do("insert into service_data (target,name,value) values ('$app{service_id}','$name_numberfield','$v2') ");
			 
				&data_set("service_data",$app{service_id},"dst_".$index."_rslot"	,$v5);
				
				
				
				
			} else {
				&data_set("service_data",$app{service_id},"dst_".$index."_name"		,$name);
			
				# because in radio url ,we have :, in data_set() we will remove : ,so cannot use data_set function
			 
				$name_numberfield = "dst_".$index."_number" ;
				database_do("delete from service_data where target='$app{service_id}' and name='$name_numberfield'");
				database_do("insert into service_data (target,name,value) values ('$app{service_id}','$name_numberfield','$number') ");
				#&data_set("service_data",$app{service_id},"dst_".$index."_number"	,$number);
				&data_set("service_data",$app{service_id},"dst_".$index."_rslot"	,$rslot);
			}
			# save data
			
			#if input a new url ,let's save to musiconhold table
			if ($select_radio eq '-1') {
					$radiourl =   &database_escape($number); 
					$name	=  $radiourl ;
					$directory ="/var/lib/asterisk/mohmp3";
					if ($protocol_radio eq 'mms') {  $application = '/etc/asterisk/mmsplay.sh '.$radiourl; }
					else {
						$application = '/etc/asterisk/shoutplay.sh '.$radiourl;
					} 
					&database_do("insert into musiconhold(name,radiourl,directory,application) values ('$name','$radiourl','$directory','$application')" );
						 
			}
			# return to status
			cgi_redirect("$my_url#radiodst");
			exit;
		}
	}
    #
    #--------------------------------------------------
    # if not save, then load
    #--------------------------------------------------
	if ( ($ok eq 1) && ($form{save} ne 1) ) {
		#$form{"callid"}	= &format_dial_number(&data_get("service_data",$app{service_id},"dst_".$index."_callid"));
		$form{"number"} = &data_get("service_data",$app{service_id},"dst_".$index."_number") ;
		$form{"name"} 	= &data_get("service_data",$app{service_id},"dst_".$index."_name");
		$form{"select_radio"} = $form{"number"} ;
		$form{"rslot"}	= 1;
	}
    #
    #--------------------------------------------------
    # get list of free slots
    #--------------------------------------------------
	foreach $loop ($index_range_low..$index_range_hi) {
		$v1 = &data_get("service_data",$app{service_id},"dst_".$loop."_number");
		$v2 = &data_get("service_data",$app{service_id},"dst_".$loop."_name");
		$t{dic}{"index_".$loop."_is_free"} 	= ($v1 eq "") ? 1 : 0;
		$t{dic}{"index_".$loop."_number"} 	= $v1; 
		$t{dic}{"index_".$loop."_name"} 	= $v2;
		$t{dic}{"index_".$loop."_is_active"}= ($loop eq $index) ? 1 : 0; 
	}
    #
    #--------------------------------------------------
    # carrier list
    #--------------------------------------------------
	foreach $loop (keys %carriers_list) {
		$t{dic}{"carriers_list_".$loop."_is_selected"} = ($form{"carrier"} eq $loop) ? 1 : 0;
	}
	#--------------------------------------------------
    # list all radios
    #--------------------------------------------------
    $list_radios ='';
    $is_radioinlist = false;  
    %radios_list =();
    %radios_list = database_select_as_hash("select id,name,radiourl from musiconhold","name,radiourl");
	foreach $loop (keys %radios_list) {
		$selected = '';
		if ($radios_list{$loop}{radiourl} eq $form{"select_radio"}) {
			$selected = 'selected' ;
			$is_radioinlist = true ;
		}
		
		$list_radios .=qq[<option value='$radios_list{$loop}{radiourl}' $selected   >$radios_list{$loop}{name}</option>];
 
	 }
	 $t{dic}{"list_radios"} = $list_radios ;
	 
	 
	 
	
    #
    #--------------------------------------------------
    # get rate for this number
    #--------------------------------------------------
	$t{dic}{"number"}	= $form{"number"};
	$t{dic}{"name"}		= $form{"name"};
	$t{dic}{"callid"}	= $form{"callid"};
	$t{dic}{"carrier"}	= $form{"carrier"};
	$t{dic}{"rslot"}	= $form{"rslot"};
	$t{dic}{"billing_rate_found"}			= 0;
	$t{dic}{"billing_rate_per_minute"}		= "";
	$t{dic}{"billing_duration_per_1_dollar"}= "";
	$t{dic}{"billing_value_per_hour"}		= "";
	$t{dic}{"billing_country_name"}			= "";
	$t{dic}{"billing_country_code"}			= "";
	$t{dic}{"billing_rate_name"}			= "";
	$t{dic}{"billing_number"}				= &data_get("service_data",$app{service_id},"dst_".$index."_number");
	$t{dic}{"billing_route"}				= 1;
	$t{dic}{"billing_number_ok"}			= 0;
	$t{dic}{"billing_rate_table_id"}		= "";
	$sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9, service_status.rate_slot_1_name,service_status.rate_slot_2_name,service_status.rate_slot_3_name,service_status.rate_slot_4_name,service_status.rate_slot_5_name,service_status.rate_slot_6_name,service_status.rate_slot_7_name,service_status.rate_slot_8_name,service_status.rate_slot_9 from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ";
	%hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9,rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,rate_slot_5_name,rate_slot_6_name,rate_slot_7_name,rate_slot_8_name,rate_slot_9");
	if ($hash{1}{flag} eq "1") {
		$t{dic}{"billing_route_1_name"} 	= $hash{1}{"rate_slot_1_name"};
		$t{dic}{"billing_route_2_name"} 	= $hash{1}{"rate_slot_2_name"};
		$t{dic}{"billing_route_3_name"} 	= $hash{1}{"rate_slot_3_name"};
		$t{dic}{"billing_route_4_name"} 	= $hash{1}{"rate_slot_4_name"};
		$t{dic}{"billing_route_5_name"} 	= $hash{1}{"rate_slot_5_name"};
		$t{dic}{"billing_route_6_name"} 	= $hash{1}{"rate_slot_6_name"};
		$t{dic}{"billing_route_7_name"} 	= $hash{1}{"rate_slot_7_name"};
		$t{dic}{"billing_route_8_name"} 	= $hash{1}{"rate_slot_8_name"};
		$t{dic}{"billing_route_9_name"} 	= $hash{1}{"rate_slot_9_name"};
		$t{dic}{"billing_route_1_rate_id"} 	= $hash{1}{rate_slot_1};
		$t{dic}{"billing_route_2_rate_id"} 	= $hash{1}{rate_slot_2};
		$t{dic}{"billing_route_3_rate_id"} 	= $hash{1}{rate_slot_3};
		$t{dic}{"billing_route_4_rate_id"} 	= $hash{1}{rate_slot_4};
		$t{dic}{"billing_route_5_rate_id"} 	= $hash{1}{rate_slot_5};
		$t{dic}{"billing_route_6_rate_id"} 	= $hash{1}{rate_slot_6};
		$t{dic}{"billing_route_7_rate_id"} 	= $hash{1}{rate_slot_7};
		$t{dic}{"billing_route_8_rate_id"} 	= $hash{1}{rate_slot_8};
		$t{dic}{"billing_route_9_rate_id"} 	= $hash{1}{rate_slot_9};
		$t{dic}{"billing_route_name"} 		= $hash{1}{"rate_slot_".$t{dic}{"billing_route"}."_name"};
	}
	if ($t{dic}{"billing_number"} ne "") {
		foreach $i (1..9) {
			# pega rate_id conforme slot_id
			$t{dic}{"billing_rate_table_id"} = ( ($t{dic}{"billing_route"} eq $i) && ($t{dic}{"billing_route_".$i."_rate_id"} ne "") ) ? $t{dic}{"billing_route_".$i."_rate_id"} : $t{dic}{"billing_rate_table_id"};
			# pega o rate-per-minute em cada slot
			if ($t{dic}{"billing_route_".$i."_rate_id"} eq "") {next} 
			%hash = &multilevel_rate_table_get($t{dic}{"billing_number"},$t{dic}{"billing_route_".$i."_rate_id"});
			$t{dic}{"billing_route_".$i."_rate_per_minute"} = "";
			if ($hash{ok_to_use} eq 1) {
				$t{dic}{"billing_route_".$i."_rate_per_minute"}	= ($hash{rate_per_minute}<0.01) ? &format_number($hash{rate_per_minute},4) : &format_number($hash{rate_per_minute},2);
			}
		}
		# pega rate desse numero no slot rate_id especificado pelo slot
		if ($t{dic}{"billing_rate_table_id"} ne "") {
			%call_price = &multilevel_rate_table_get($t{dic}{"billing_number"},$t{dic}{"billing_rate_table_id"});
			if ($call_price{ok_to_use} eq 1) {
				%country_codes 	= database_select_as_hash("select code,name from country");
				$t{dic}{"billing_number_ok"}			= 1;
				$t{dic}{"billing_number"}				= &multiformat_phone_number_format_for_user($t{dic}{"billing_number"},"USA");
				$t{dic}{"billing_country_name"}			= (exists($country_codes{$call_price{rate_country}})) ? $country_codes{$call_price{rate_country}} : "";
				$t{dic}{"billing_country_code"}			= $call_price{rate_country};
				$t{dic}{"billing_rate_found"}			= 1;
				$t{dic}{"billing_rate_per_minute"}		= ($call_price{rate_per_minute}<0.01) ? &format_number($call_price{rate_per_minute},4) : &format_number($call_price{rate_per_minute},2);
				$t{dic}{"billing_duration_per_1_dollar"}= &format_time(60*(1/$call_price{rate_per_minute}));
				$t{dic}{"billing_value_per_hour"}		= &format_number(($call_price{rate_per_minute}*60),2);
				$t{dic}{"billing_rate_name"}			= $call_price{rate_name};
			}
		}
	}
    #
    #--------------------------------------------------
    # print page
    #--------------------------------------------------
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
	#foreach(sort keys %{$t{dic}}) {if ($_ eq "debug") {next} $t{dic}{"debug"} .= "TEMPLATE DUMP -- $_=$t{dic}{$_}<br>";}
    &template_print("template.pbx.dst.radio.html",%t);
	exit;
}

sub do_add(){
    #
	#============================================
    # start default values
	#============================================
    %t = %template_default;
    $t{mode} = "";
        $refcode    =$form{referal};
        #check if code valid if yes continue else return ;

      if ($refcode ne "") 
      {
            
                $sql = "
                        select 
                                1,1,
                                service.id,
                                service.name,
                                service_status.refer_status,
                                service_status.refer_status_premium,
                                service_status.signin_coupon_premium_id,
                                service_status.signin_coupon_default_id
                        from
                                service_invite,
                                service,
                                service_status
                        where
                                service_invite.free = 0 and 
                                service_invite.service_id = service.id and 
                                service.status = service_status.id and 
                                service_status.deleted = 0 and 
                                service_status.can_add_refer = 1 and 
                                service_invite.id = '$refcode'
                        ";
                %hash = database_select_as_hash($sql,"flag,id,name,signin_status,signin_status_premium,signin_coupon_premium_id,signin_coupon_default_id");
                 
                if ($hash{1}{flag} ne 1) 
                {
                    cgi_redirect("/index.cgi?referal=$refcode");
           
                };
                
        }else
      {

      } 
	#
	#============================================
	# pega invite
	#============================================
	$t{invite_ok} = 0;
	$buf = ($buf eq "") && ($form{referal} ne "")   ? $form{referal}   : $buf;
    $buf = ($buf eq "")                             ? $cookie{"i"}     : $buf;
    $buf = ($buf eq "") && ($form{invite} ne "")    ? $form{invite}    : $buf;
        
	$buf = clean_str(substr($buf,0,100),"-_","MINIMAL");
	$buf = (length($buf) < 3) ? "" : $buf;
	$buf = (length($buf) > 20) ? "" : $buf;
	if ($buf ne "") {
		$sql = "
			select 
				1,1,
				service.id,
				service.name,
				service_status.refer_status,
				service_status.refer_status_premium,
				service_status.signin_coupon_premium_id,
				service_status.signin_coupon_default_id
			from
				service_invite,
				service,
				service_status
			where
				service_invite.free = 0 and 
				service_invite.service_id = service.id and 
				service.status = service_status.id and 
				service_status.deleted = 0 and 
				service_status.can_add_refer = 1 and 
				service_invite.id = '$buf'
			";
		%hash = database_select_as_hash($sql,"flag,id,name,signin_status,signin_status_premium,signin_coupon_premium_id,signin_coupon_default_id");
		if ($hash{1}{flag} eq 1) {
			$t{invite_ok}						= 1;
			$t{invite_id}						= $buf;
			$t{invite_service_id}				= $hash{1}{id};
			$t{invite_service_name}				= $hash{1}{name};
			$t{invite_signin_status}			= $hash{1}{signin_status};
			$t{invite_signin_status_default}	= $hash{1}{signin_status};
			$t{invite_signin_status_premium}	= $hash{1}{signin_status_premium};
			$t{invite_signin_coupon_premium_id}	= $hash{1}{signin_coupon_premium_id};
			$t{invite_signin_coupon_default_id}	= $hash{1}{signin_coupon_default_id};
		}
		
		$t{no_invite} = 0;
        if( $buf eq  "soup" ) {$t{no_invite}=1;};
	}
	#
	#============================================
	# get default coupon
	#============================================
	%coupon = ();
	$t{coupon_default_exists}		= 0;
	$t{coupon_default_in_stock}		= 0;
	$t{coupon_default_stock_qtd}	= 0;
	$t{coupon_default_ani_locked}	= 0;
	$t{coupon_default_error}		= 0;
	if ( ($t{invite_ok} eq 1) && ($t{invite_signin_coupon_default_id} ne "") && ($t{invite_signin_coupon_default_id} > 0) ) {
		$sql = "
		select 
			1,1,
			service_coupon_type.id,
			service_coupon_type.title
		from 
			service_coupon_type,service_coupon_type_status
		where 
			service_coupon_type.id = '$t{invite_signin_coupon_default_id}' and 
			service_coupon_type.status = service_coupon_type_status.id and 
			service_coupon_type_status.is_active = 1
		";
		%hash = database_select_as_hash($sql,"flag,id,title");
		if ($hash{1}{flag} eq 1) {
			$t{coupon_default_exists}		= 1;
			$t{coupon_default_type_id}		= $hash{1}{id};
			$t{coupon_default_title}		= $hash{1}{title};
			$sql = "
			select 1,1,count(*)
			from 
				service_coupon_stock,
				service_coupon_stock_status
			where 
				service_coupon_stock.coupon_type_id='$t{coupon_default_type_id}' and 
				service_coupon_stock.status = service_coupon_stock_status.id and 
				service_coupon_stock_status.is_ready_to_assign
			";
			%hash = database_select_as_hash($sql,"flag,value");
			if ($hash{1}{flag} eq 1) {
				$t{coupon_default_in_stock}		= ($hash{1}{value}>0) ? 1 : 0;
				$t{coupon_default_stock_qtd}	= $hash{1}{value};
			}
		}
	}
	#
	#============================================
	# get premium coupon
	#============================================
	%coupon = ();
	$t{coupon_premium_exists}		= 0;
	$t{coupon_premium_in_stock}		= 0;
	$t{coupon_premium_stock_qtd}	= 0;
	$t{coupon_premium_ani_locked}	= 0;
	$t{coupon_premium_error}		= 0;
	if ( ($t{invite_ok} eq 1) && ($t{invite_signin_coupon_premium_id} ne "") && ($t{invite_signin_coupon_premium_id} > 0) ) {
		$sql = "
		select 
			1,1,
			service_coupon_type.id,
			service_coupon_type.title
		from 
			service_coupon_type,service_coupon_type_status
		where 
			service_coupon_type.id = '$t{invite_signin_coupon_premium_id}' and 
			service_coupon_type.status = service_coupon_type_status.id and 
			service_coupon_type_status.is_active = 1
		";
		%hash = database_select_as_hash($sql,"flag,id,title");
		if ($hash{1}{flag} eq 1) {
			$t{coupon_premium_exists}		= 1;
			$t{coupon_premium_type_id}		= $hash{1}{id};
			$t{coupon_premium_title}		= $hash{1}{title};
			$sql = "
			select 1,1,count(*)
			from 
				service_coupon_stock,
				service_coupon_stock_status
			where 
				service_coupon_stock.coupon_type_id='$t{coupon_premium_type_id}' and 
				service_coupon_stock.status = service_coupon_stock_status.id and 
				service_coupon_stock_status.is_ready_to_assign
			";
			%hash = database_select_as_hash($sql,"flag,value");
			if ($hash{1}{flag} eq 1) {
				$t{coupon_premium_in_stock}		= ($hash{1}{value}>0) ? 1 : 0;
				$t{coupon_premium_stock_qtd}	= $hash{1}{value};
			}
		}
	}
	#
	#============================================
	# pega rate table a ser usada como route 1 do status que supostamente devera ser atribuido com esse convite
	#============================================
	$t{rate_table_for_ani} = 9;
	$t{rate_table_for_dst} = 10;
	if ( ($t{invite_ok} eq 1) && ($t{invite_signin_status} ne "") && ($t{invite_signin_status} > 0) ) {
		$sql = "select  1,1,rate_slot_1,rate_slot_callback from service_status where id = '$t{invite_signin_status}' ";
		%hash = database_select_as_hash($sql,"flag,value1,value2");
		if ($hash{1}{flag} eq 1) {
			$t{rate_table_for_ani} = $hash{1}{value2};
			$t{rate_table_for_dst} = $hash{1}{value1};
		}
	}
    #
	#============================================
    # Check ANI
	#============================================
    $t{ani} 				= substr($form{ani},0,100);
	#$t{aniName}				= clean_str(substr($form{aniName}, 0, 100));
	#$t{aniEmail}			= substr($form{aniEmail}, 0, 100);
    $t{ani_ok} 				= 0;
    $t{ani_error} 			= 0;
    $t{ani_error_format} 	= 0;
    $t{ani_error_no_rate} 	= 0;
    $t{ani_error_in_use} 	= 0;
    $t{ani_error_locked} 	= 0;
	

    if ($t{ani} ne "") {
		# check format 
		($tmp0,$tmp1,$tmp2) = &multilevel_check_E164_number(&clean_int($t{ani}));
		if ($tmp0 eq "OK") {
			$t{ani} = $tmp1;
		} else {
		    $t{ani_error} 			= 1;
		    $t{ani_error_format} 	= 1;
		}
		# check rate
		if ($t{ani_error} eq 0) {
			%hash = &multilevel_rate_table_get($t{ani},$t{rate_table_for_ani});
			if ($hash{ok_to_use} ne 1) {
			    $t{ani_error} 			= 1;
			    $t{ani_error_no_rate} 	= 1;
			}
		}
		# second level check ANI list
		if ($t{ani_error} eq 0) {
			%hash = database_select_as_hash("select 1,1,count(*) from service_ani where ani='$number' and service_id<>'$app{service_id}'","flag,qtd");
			unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ) {
			    $t{ani_error} 			= 1;
			    $t{ani_error_in_use} 	= 1;
			}
		}
	    # Se ANI ta ok flag ele
		if ($t{ani_error} eq 0) {
		    $t{ani_ok} = 1;
		    $t{ani_E164} = $t{ani};
		    $t{ani} = &format_E164_number($t{ani},"USA");
		}
    }
	#
	#============================================
	# Get provider by ani
	#============================================
    $t{ani_provider_found} = 0;
    if ( ($t{ani_ok} eq 1) && ($t{ani_E164} ne "") ) {
	    %hash = &get_carrier_by_number($t{ani_E164});
		if ($hash{found} eq 1) {
		    $t{ani_provider_found}					= 1;
			$t{ani_provider_id}						= $hash{carrier_id};
			$t{ani_provider_name} 					= $hash{carrier_name};
			$t{ani_provider_is_mobile} 				= ($hash{carrier_is_mobile} eq 1) ? 1 : 0;
			$t{ani_provider_is_premium} 			= ($hash{flag_premium_signin} eq 1) ? 1 : 0;
			$t{"ani_provider_type_".$hash{type}} 	= 1;
		}
    }
	#
	#============================================
	# choose premium/default signin_status
	#============================================
	$t{invite_signin_status} = $t{invite_signin_status_default};
	if ( ($t{ani_provider_is_premium} eq 1) && ($t{invite_signin_status_premium} ne "") ) {
		$t{invite_signin_status} = $t{invite_signin_status_premium};
	}
	#
	#============================================
	# choose premium/default cooupon
	#============================================
	$t{coupon_error}		= 0;
	$t{coupon_exists}		= $t{coupon_default_exists};
	$t{coupon_type_id}		= $t{coupon_default_type_id};
	$t{coupon_title}		= $t{coupon_default_title};
	$t{coupon_in_stock}		= $t{coupon_default_in_stock};
	$t{coupon_stock_qtd}	= $t{coupon_default_stock_qtd};
	$t{coupon_is_premium}	= 0;
	if ( ($t{coupon_premium_in_stock} eq 1) && ($t{ani_provider_is_premium} eq 1) ) {
		$t{coupon_exists}		= $t{coupon_premium_exists};
		$t{coupon_type_id}		= $t{coupon_premium_type_id};
		$t{coupon_title}		= $t{coupon_premium_title};
		$t{coupon_in_stock}		= $t{coupon_premium_in_stock};
		$t{coupon_stock_qtd}	= $t{coupon_premium_stock_qtd};
		$t{coupon_is_premium}	= 1;
	}
	#
	#============================================
	# re-check coupon: one coupon per ANI
	#============================================
	# new logic limitation
	if ( ($t{ani_ok} eq 1) && ($t{coupon_in_stock} eq 1)  ) {
		%hash = database_select_as_hash("select 1,1,count(*) from service_signin where ani='$t{ani_E164}' and service_id is not null ","flag,qtd");
		unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ) {
			$t{coupon_error}			= 1;
			$t{coupon_error_ani_locked}	= 1;
		}
	}
    #
	#============================================
    # Check DST
	#============================================
    $t{dst} 				= substr($form{dst},0,100);
    $t{dst_ok} 				= 0;
    $t{dst_error} 			= 0;
    $t{dst_error_format} 	= 0;
    $t{dst_error_no_rate} 	= 0;
	
#	if( $t{ani_ok} eq 1 ){
#		
#		if($t{aniName} eq ""){
#			$t{ani_ok} = 0;
#			$t{form_error} = 1;
#			$t{ani_name_invalid} = 1;
#		}
#				
#		if (!($t{aniEmail} =~ /^\w+\@([\da-zA-Z\-]{1,}\.){1,}[\da-zA-Z-]{2,6}$/)){
#			$t{ani_ok} = 0;
#			$t{form_error} = 1;
#			$t{ani_email_invalid} = 1;
#		}
#				
#		if ( $t{dstEmail} ne "" && !($t{dstEmail} =~ /^\w+\@([\da-zA-Z\-]{1,}\.){1,}[\da-zA-Z-]{2,6}$/)){
#			$t{ani_ok} = 0;
#			$t{form_error} = 1;
#			$t{dst_email_invalid} = 1;
#		}
#	}
		
    if ($t{dst} ne "") {
		# check format 
		($tmp0,$tmp1,$tmp2) = &multilevel_check_E164_number(&clean_int($t{dst}));
		if ($tmp0 eq "OK") {
			$t{dst} = $tmp1;
		} else {
		    $t{dst_error} 			= 1;
		    $t{dst_error_format} 	= 1;
		}
		# check rate
		if ($t{dst_error} eq 0) {
			%hash = &multilevel_rate_table_get($t{dst},$t{rate_table_for_dst});
			if ($hash{ok_to_use} ne 1) {
			    $t{dst_error} 			= 1;
			    $t{dst_error_no_rate} 	= 1;
			}
		}
	    # Se dst ta ok flag ele
		if ($t{dst_error} eq 0) {
		    $t{dst_ok} = 1;
		    $t{dst_E164} = $t{dst};
		    $t{dst} = &format_E164_number($t{dst},"USA");
		}
    }
	#
	#============================================
	# re-check coupon: no coupon if multiple DST
	#============================================
	if ( ($t{dst_ok} eq 1) && ($t{coupon_in_stock} eq 1)  ) {
		$sql = "
		SELECT 1,1,count(*) FROM calls 
		where dst='$t{dst_E164}' and date>date_sub(now(), interval 90 day) and value>0 
		";
		%hash = database_select_as_hash($sql,"flag,qtd");
		unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} < 30) ) {
			$t{coupon_error}			= 1;
			$t{coupon_error_dst_locked}	= 1;
		}
	}
    #
	#============================================
    # pega o signin caso tenha ani
	#============================================
	$t{signin_found} 			= 0;
	$t{signin_pin_found} 		= 0;
	$t{signin_ok} 				= 0;
    if ( ($t{ani_ok} eq 1) && ($t{ani_E164} ne "") ) {
		$sql = "
		SELECT 1,1,id,dst,pin
		FROM service_signin
		where ani='$t{ani_E164}' and service_id is null
		order by date_start desc limit 0,1
		";
		%hash = database_select_as_hash($sql,"flag,id,dst,pin");
		if ($hash{1}{flag} eq 1) {
			$t{signin_found}= 1;
			$t{signin_id} 	= $hash{1}{id};
			$t{signin_ani} 	= $t{ani_E164};
			$t{signin_dst} 	= $hash{1}{dst};
			$t{signin_pin} 	= $hash{1}{pin};
			$t{signin_ok} 	= 1;
		}
	}
    #
	#============================================
    # pega o servico caso tenha ani e signin 
	#============================================
	$t{service_found} 				= 0;
    if ( ($t{ani_ok} eq 1) && ($t{ani_E164} ne "") ) {
		$sql = "
		select 1,1,service.id,service.name,service.email
		from service,service_ani
		where service.id = service_ani.service_id and service_ani.ani='$t{ani_E164}'
		";
		%hash = database_select_as_hash($sql,"flag,id,name,email");
		if ($hash{1}{flag} eq 1) {
			$t{service_found} 	= 1;
			$t{service_id} 		= $hash{1}{id};
			$t{service_name} 	= $hash{1}{name};
			$t{service_email} 	= $hash{1}{email};
		}
    }
	
				
    #
	#============================================
    # check pin
	#============================================
	$t{pin} 		= substr($form{pin},0,100);
	$t{aniName}		= clean_str(substr($form{aniName}, 0, 100));
	$t{aniEmail} 	= clean_str(substr($form{aniEmail},0,100),"+.()-=[]?><#\@");
	
    #
	#============================================
    # check term
	#============================================
	$t{terms} = ($form{terms} eq 1) ? 1 : 0;
    #
	#============================================
    # check accept coupon error
	#============================================
	$t{coupon_error_accepted} = ($form{coupon_error_accepted} eq 1) ? 1 : 0;
    #
	#============================================
    # action
	#============================================
	$t{invite_ok} = 1; #we dont need invite any more
	
    $t{mode} = "unknown";
    if ($app{session_status} eq 1) {    
    	#
	    # Se ta logado, melhor avisar pra ir pra myaccount
	    # ou mostrar uma pagina sobre como add mais contatos e anis
    	$t{mode} = "loged_in";
    	#
    } elsif ($t{invite_ok} ne 1) {    
    	#
	    # verifica se tem invite. Se nao tem para
    	$t{mode} = "no_invite";
    	#
    } elsif ($t{service_found} eq 1) {    
    	#
    	# se tem servico com esse ani, avisar ele tem que login
    	$t{mode} = "ani_in_use";
    	#
    } else {
		if ($t{signin_ok} eq 0){
			# 
			# nao tem sign in, ja sei eh step 1
			$t{mode} = "signin_step_1";
			#
			# extra errors
			
			if ($t{ani}.$t{dst} ne "") {
				if ( ($t{ani_error} eq 0) && ($t{ani} eq "") )  { $t{ani_error}=1; $t{ani_error_empty}=1; }
				if ( ($t{dst_error} eq 0) && ($t{dst} eq "") )  { $t{dst_error}=1; $t{dst_error_empty}=1; }
				####################################################
				#  since we are sign in ,the ani should be mobile
				####################################################
				if ( $t{ani_provider_is_mobile} ne 1 ) {
					$t{ani_error}	= 1;
					$t{form_error_ani_needmobile}	= 1;
 					warning('not a mobile'.$t{ani});
				}   
				if ($t{ani_error} eq 1) {
				    $t{form_error} 				= 1;
				    $t{form_error_ani_empty} 	= $t{ani_error_empty};
				    $t{form_error_ani_format} 	= $t{ani_error_format};
				    $t{form_error_ani_no_rate}	= $t{ani_error_no_rate};
		    		$t{form_error_ani_in_use}	= $t{ani_error_in_use};
		    		$t{form_error_ani_locked}	= $t{ani_error_locked};
				}
				if ($t{dst_error} eq 1) {
				    $t{form_error} 				= 1;
				    $t{form_error_dst_empty} 	= $t{dst_error_empty};
				    $t{form_error_dst_format} 	= $t{dst_error_format};
				    $t{form_error_dst_no_rate}	= $t{dst_error_no_rate};
	    			$t{form_error_dst_locked}	= $t{dst_error_locked};
				}
				if ( $t{terms} ne 1)  {
					$t{form_error} = 1;
					$t{form_error_terms}	= 1;
				}
				
			}
			
			if ( ($t{coupon_error} eq 1) && ($t{coupon_in_stock} eq 1) ) {
				if ($t{coupon_error_accepted} eq 0) {
					$t{form_error} = 1;
					$t{form_error_coupon_error_accepted} = 1;
				}
			}
			#
			# seguindo o que tem que se fazer
		    if ( ($t{form_error} ne 1) &&  ($t{ani_ok} eq 1) && ($t{dst_ok} eq 1) ) {
		    	#
		    	###################################################
		    	# criar sign-in - START
		    	###################################################
		    	#
		    	# criando sign-in
				$t{signin_pin} = &multilevel_pin_generate();
				if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
				if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
				if ($t{signin_pin} eq "")  {
					# erro criando pin
					$t{form_error}	= 1;
					$t{form_error_system}	= 1;
				} else {
					$sql = " 
					insert into service_signin  
					(date_start,  date_last_change,  ani,             dst,           pin               ) values 
					(now(),       now(),             '$t{ani_E164}', '$t{dst_E164}', '$t{signin_pin}'  ) 
					";
					$t{signin_id} = database_do_insert($sql);
					
				
					if ($t{signin_id} eq "") {
						# erro criando signin
						$t{form_error}	= 1;
						$t{form_error_system}	= 1;
					} else {
						&action_history("status:signin:new",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=>$t{signin_pin}));
						&database_do("update service_pin set signin_id='$t{signin_id}' where pin='$t{signin_pin}' ");
						$t{mode} = "signin_step_2";
						$t{debug} .= "ENVIANDO PIN<br>";	
								    	
						# send pin, we only send last 4 digits of the pin (trac ticket #40)
						$confirmcode = substr($t{signin_pin},-4,4) ;
						&dial_and_play_code($t{ani_E164}, $confirmcode );
						$t{pin_send}		= 1;
						&action_history("status:signin:pin:did",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=>$confirmcode));
					}
				}
				#
		    	###################################################
		    	# criar sign-in - STOP
		    	###################################################
		    	#
		    }
		} else {
			# 
			# ja tem sign in, entao eh step 2
			$t{mode} = "signin_step_2";
			#
			# confere se PIN_DID ainda existe e recria se necessario
			$sql = "select 1,1 from service_pin where pin='$t{signin_pin}' and service_id is null and signin_id='$t{signin_id}' and free=1 ";
			%hash = database_select_as_hash($sql,"flag,pin");
			if ($hash{1}{flag} ne 1) {
				$t{signin_pin} = &multilevel_pin_generate();
				if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
				if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
				&database_do("update service_pin set signin_id='$t{signin_id}' where pin='$t{signin_pin}' ");
			}
			#
			# update dst se necessario
			if ($t{dst_E164} eq "") {
				$t{dst_E164} = $t{signin_dst};
				$t{dst} = &format_E164_number($t{signin_dst},"E164");
			} else {
				if ($t{dst_ok} eq 1){
					&database_do(" update service_signin set dst='$t{dst_E164}' where id='$t{signin_id}' ");
				}				
			}
			#
			# extra errors
			if ( ($t{ani_error} eq 0) && ($t{ani} eq "") )  { $t{ani_error}=1; $t{ani_error_empty}=1; }
			if ( ($t{dst_error} eq 0) && ($t{dst} eq "") )  { $t{dst_error}=1; $t{dst_error_empty}=1; }
			if ($t{ani_error} eq 1) {
			    $t{form_error} 				= 1;
			    $t{form_error_ani_empty} 	= $t{ani_error_empty};
			    $t{form_error_ani_format} 	= $t{ani_error_format};
			    $t{form_error_ani_no_rate}	= $t{ani_error_no_rate};
	    		$t{form_error_ani_in_use}	= $t{ani_error_in_use};
	    		$t{form_error_ani_locked}	= $t{ani_error_locked};
			}
			if ($t{dst_error} eq 1) {
			    $t{form_error} 				= 1;
			    $t{form_error_dst_empty} 	= $t{dst_error_empty};
			    $t{form_error_dst_format} 	= $t{dst_error_format};
			    $t{form_error_dst_no_rate}	= $t{dst_error_no_rate};
    			$t{form_error_dst_locked}	= $t{dst_error_locked};
			}
			#if ( ($t{coupon_error} eq 1) && ($t{coupon_in_stock} eq 1) ) {
			#	if ($t{coupon_error_accepted} eq 0) {
			#		$t{form_error} = 1;
			#		$t{form_error_coupon_error_accepted} = 1;
			#	}
			#}
			#
			# so executa as acoues e nao tem erro
			if ($t{form_error} ne 1) {
				# 
				# re-enviar PIN 
				if ($form{re_send_pin} eq 1) {
					# send pin, we only send last 4 digits of the pin (ticket #40)
					$confirmcode = substr($t{signin_pin},-4,4) ;						
					&dial_and_play_code($t{ani_E164}, $confirmcode );
					$t{pin_send} = 1;
					&action_history("status:signin:pin:did",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=>$confirmcode));
				}
				#
				# verificar user input pin
				if ($t{pin} ne "") {
					if (&clean_int(substr($t{pin},0,100)) ne substr($t{signin_pin},-4,4)) {
						#
						# se pin ta errado, informar o erro
						$t{form_error}		= 1;
						$t{form_error_pin}	= 1;
					}elsif( $t{aniName} eq ""){
						$t{form_error} = 1;
						$t{form_error_aniName_empty} = 1;
					}elsif(($t{aniEmail} eq "")){
						$t{form_error} = 1;
						$t{form_error_aniEmail_empty} = 1;
					}elsif (!( (index($t{aniEmail},"\@") ne -1) && (index($t{aniEmail},"\@") eq rindex($t{aniEmail},"\@"))  && (index($t{aniEmail},".") ne -1) )){
						$t{form_error} = 1;
						$t{form_error_aniEmail_format} = 1;
					}else {
						$t{pin_ok} = 1;
						$confirmcode = substr($t{signin_pin},-4,4) ;
						&action_history("status:signin:pin:did:ok",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=> $confirmcode));
						#
				    	###################################################
				    	# criar SERVICE - START
				    	###################################################
				    	#
						#
						# criar servico (default status=new)
						$sql  = "
							insert into service 
							(product_id,  status, 					name, 				email, 		 creation_date,  last_change  ) values 
							('1',         '$t{invite_signin_status}',  '$t{aniName}', '$t{aniEmail}', now(),          now()        ) 
						";
						$t{service_id} 		= &database_do_insert($sql);
						
						#&active_session_set("service_name",$t{aniName});
						#&active_session_set("service_email",$t{aniEmail});
						
						#&active_session_set("service_name",$t{aniName});
						#&active_session_set("service_email",$t{aniEmail});
						#&session_set($app{session_cookie_k},"service_email",$t{aniEmail});
						#&session_set($app{session_cookie_k},"service_name",$t{aniName});
						#&session_set($app{session_cookie_k},"service_alert"	,"");
						
						%email = ();
						$email{to}				= $service_email;
						$email{template}		= "service.add";
						$email{dic}{pin}		= $t{signin_pin};
						$email{dic}{email}		= $service_email;
						&multilevel_send_email(%email);
						&action_history("status:signin:pin:email:ok",('service_id'=>$service_id,,'value_old'=>$email{dic}{email},'value_new'=>$email{dic}{pin}));
				
						
						#
						# se ok, terminar o trabalho e login
						if ($t{service_id} ne "") {
							#
							# add on tree
							$sql  = " 
							insert into service_tree 
							(service_id,        parent_service_id        )  values 
							('$t{service_id}',  '$t{invite_service_id}'  ) 
							";
							database_do($sql);
							&data_set("service_data",$t{invite_service_id},"last_friend_time",time);
							#
							# update pin
							&database_do("update service_pin set service_id='$t{service_id}' where pin='$t{signin_pin}' ");
							#
							# update signin
							&database_do("update service_signin set service_id='$t{service_id}' where id='$t{signin_id}' ");
							#
							# update action_log 
							&database_do("update action_log set service_id='$t{service_id}' where signin_id='$t{signin_id}' and service_id is null ");
							#
							# criar invite
							$tmp= &multilevel_invite_create($t{service_id});
							#
							# adicionar primeiro ANI
							&data_set("service_data",$t{service_id},"ani_1_number"		,$t{ani_E164});
							&data_set("service_data",$t{service_id},"ani_1_provider"	,$t{form_provider});
							&multilevel_anicheck_touch($t{service_id},$t{dst_E164});
							&database_do("insert into service_ani (ani,service_id) values ('$t{ani_E164}', '$t{service_id}') ");
							#
							# adicionar primeiro DST
							&data_set("service_data",$t{service_id},"dst_1_number"	,$t{dst_E164});
							&data_set("service_data",$t{service_id},"dst_1_name"	,$t{dstName});
							&data_set("service_data",$t{service_id},"dst_1_rslot"	,1);
							#
							# adicionar defaults
							&data_set("service_data",$t{service_id},"trigger_nf",1);
							&data_set("service_data",$t{service_id},"trigger_nfof",1);
							&data_set("service_data",$t{service_id},"trigger_nc",1);
							&data_set("service_data",$t{service_id},"trigger_ec",1);
							&data_set("service_data",$t{service_id},"trigger_lb",1);
							&data_set("service_data",$t{service_id},"email_news",1);
							#
							# adicionar coupon se possivel
							if ( ($t{coupon_type_id} ne "") && ($t{coupon_in_stock} eq 1) && ($t{coupon_exists} eq 1) && ($t{coupon_error} ne 1) ) {
								# tenta add coupon
								%coupon = ();
								$coupon{service_id}		= $t{service_id};
								$coupon{coupon_type_id}	= $t{coupon_type_id};
								%coupon = &multilevel_coupon_assign(%coupon);
								if ($coupon{ok} eq 1) {
									if (&multilevel_coupon_next_slice($coupon{coupon_stock_id})>0){
										$t{coupon_assigned}	= 1;
									}
								}
							}
							#
							# delete request code
							&database_do("update service_signin set date_last_change=now(), date_stop=now() where id='$t{signin_id}' ");
							#
							# apply commission
							%commission_data = ();
							$commission_data{service_id}				= $t{invite_service_id};
							$commission_data{from_service_id}			= $t{service_id};
							$commission_data{commission_type_engine} 	= "REFERRAL_SIGNIN";
							%commission_data = &multilevel_commission_new(%commission_data);
							#
							# email parent tree sobre new friend
							$notification_service_id = $t{invite_service_id};
							foreach $notification_proximity_level (0..20) {
								%tmp_hash = database_select_as_hash("select 1,1,name,email from service where service.id='$notification_service_id' ","flag,name,email");
								if ($tmp_hash{1}{flag} eq 1) {
									$notification_service_email	= $tmp_hash{1}{email};
									$notification_flag_type 	= ($notification_proximity_level eq 0) ? "trigger_nf" : "trigger_nfof";
									$notification_flag 			= &data_get("service_data",$notification_service_id,$notification_flag_type);
									if ( ($notification_flag eq 1) && ($notification_service_email ne "") ){
										%email = ();
										$email{template}					= ($notification_proximity_level eq 0) ? "alert.new.friend" : "alert.new.friend.of.friend";
										$email{to}							= $notification_service_email;
										$email{dic}{invite_branch_distance}	= "you";
										$email{dic}{invite_branch_distance}	= ($notification_proximity_level eq 1) ? "your friend" : $email{dic}{invite_branch_distance};
										$email{dic}{invite_branch_distance}	= ($notification_proximity_level eq 2) ? "one person away" : $email{dic}{invite_branch_distance};
										$email{dic}{invite_branch_distance}	= ($notification_proximity_level > 2) ? ($notification_proximity_level-1)." people away" : $email{dic}{invite_branch_distance};
										&multilevel_send_email(%email);
									}
								}
								%tmp_hash = database_select_as_hash("select 1,1,parent_service_id from service_tree where service_id='$notification_service_id'","flag,value");
								if ( ($tmp_hash{1}{flag} eq 1) && ($tmp_hash{1}{value} ne "") ) {
									$notification_service_id = $tmp_hash{1}{value};
								} else {
									last;
								}
							}
							
							#send New friend joined message to referrer
							
							my $referral_number=&data_get("service_data",$t{invite_service_id},"ani_1_number");							
							
							
							my %hash = database_select_as_hash("SELECT 1,1,msg_type,msg_text FROM sms_customtext","1,msg_type,msg_text");
							my $joinmessage = $hash{1}{msg_text};
										
							$joinmessage =~ s/xxxx/$t{ani}/i;
							
							&sendSMS_Twilio($referral_number,$joinmessage);
							#
							# log-in
							session_attach($t{service_id});
							#&session_set($app{session_cookie_k},"service_alert"	,"emailquestion");
							&session_set($app{session_cookie_k},"flag_first_login"	,1);
							&active_session_set("service_name",$t{aniName});
							&active_session_set("service_email",$t{aniEmail});
							&session_set($app{session_cookie_k},"service_email",$t{aniEmail});
							&session_set($app{session_cookie_k},"service_name",$t{aniName});
							&session_set($app{session_cookie_k},"service_alert"	,"");
							#
							# log action
							&action_history("status:new",('signin_id'=>$t{signin_id},'service_id'=>$t{service_id},'value_old'=>$t{ani_E164}));
							#
							# mostrar dados
							$t{mode} = "add_ok";
							#
						} else {
							$t{form_error}			= 1;
							$t{form_error_system}	= 1;
						}
						#
				    	###################################################
				    	# criar SERVICE - STOP
				    	###################################################
				    	#
					}
				}
			}
		}
    }
    #
	#============================================
    # preare page
	#============================================
    $t{"mode_".$t{mode}} = 1;
    $t{"my_url"} = $my_url;
    $t{signin_pin_formated} = &format_pin($t{signin_pin});
    $t{form_error} = ( ($t{ani_error} eq 1) || ($t{dst_error} eq 1) || ($t{form_pin_error} eq 1) ) ? 1 : $t{form_error};
	#$tmp=""; foreach(sort keys %t) {if ($_ eq "debug") {next} $tmp .= "$_=$t{$_}<br>";}$t{debug} .= $tmp;			    	
    &template_print("template.pbx.add.html",%t);
}

sub service_add_pin_assign_signin_id(){
	local($pin,$signin_id) = @_;
	local(%hash,$tmp,$tmp1,$tmp2,$sql);
	if ($signin_id eq "") 	{ return ""; }
	if ($pin eq "") 		{ $pin=&multilevel_pin_generate(); }
	if ($pin eq "") 		{ $pin=&multilevel_pin_generate(); }
	if ($pin eq "") 		{ return ""; }
	&database_do("update service_pin set last_change=now(),signin_id='$signin_id' where pin='$pin' ");
	return $pin;
}
sub service_add_pin_assign_service_id(){
	local($pin,$service_id) = @_;
	local(%hash,$tmp,$tmp1,$tmp2,$sql);
	if ($service_id eq "") 	{ return ""; }
	if ($pin eq "") 		{ return ""; }
	&database_do("update service_pin set last_change=now(),service_id='$service_id' where pin='$pin' ");
	return $pin;
}
#=======================================================

sub do_radio_add(){
	 	#
	#-------------------------------------------
	# start
	#-------------------------------------------
	%t = ();
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_ok = 0;
	$form_message = "";
	
	if ($form{save} eq 1) {
		 if ($form{description} eq "") {
			$form_ok = 0;
			$form_message = "Please input radio Name <br><br>";
			$form{description} = "";
		} elsif  ($form{radiourl} eq "")   {
			$form_ok = 0;
		 
			$form_message = "Please input radio url ,begin with http:// or mms://<br><br>";
			$form{radiourl} = "";
			 		
			
		}elsif (substr($form{radiourl},0,4) eq 'mms:') {
				$protocol_radio ='mms'; 
				$form_ok = 1;
		}elsif ( substr($form{radiourl},0,5) eq 'http:') {
			$protocol_radio ='shoutcast';
			$form_ok = 1;
				
		}else {	$form_ok = 1;
		} 
		
	}
	#
	
 	 
	 
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		$form{radiourl} =   &database_escape($form{radiourl}); 
		$form{description}	= &database_escape($form{description});
		$form{radiotype}	= &database_escape($form{radiotype});
		$directory ="/var/lib/asterisk/mohmp3";
		if ($form{radiotype} eq 'MMS') {  $application = '/etc/asterisk/mmsplay.sh '.$form{radiourl}; }
		else {
			$application = '/etc/asterisk/shoutplay.sh '.$form{radiourl};
		}
	
		&database_do("insert into musiconhold(description,radiourl,directory,application,radiotype,service_id) values ('$form{description}','$form{radiourl}','$directory','$application','$form{radiotype}','$app{service_id}')" );
	#	&action_history("noc:config:agestatus:add",('title'=>$form{title},'adm_user_id'=>$app{session_cookie_u}));
		
		%hash = database_select_as_hash("SELECT 1,LAST_INSERT_ID();");
		$radio_id = $hash{1};
		
		#if not specify exten,we populate exten = id(name)
		if ($data1 eq "") {  
			$sql ="update musiconhold set exten='$radio_id' where name='$radio_id'";
			database_do($sql);
		} 
	
		%t = ();
	    $t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
	  	cgi_redirect("$my_url#dst");
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} ne 1) {
#		$form{title} = $title;
#		$form{threshold_days} = $threshold_days ;
#		$form{commission_factor} = $commission_factor ;
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
 	
    $t{dic}{my_url}	= $my_url;
   
    $t{dic}{content}	= qq[
	 
	 
	<form action=$my_url method=post class=clear >
	 Radio Name <br>
	 
	 <input name="description" value="$form{description}" size="50" /><br> 
	 
	 Radio Url(begin with http:// or mms://) <br>
 
	 <input name="radiourl" value="$form{radiourl}" size="50"  /><br> 
	 Radio Type <br>
 	 <select name="radiotype">
 	 <option value='SHOUTCAST' $selected_radiotype{SHOUTCAST}> SHOUTCAST </option>
 	 <option value='MMS' $selected_radiotype{MMS} > MMS   </option>
 	 </select>
	  (we current support mms radiotype and shoutcast radiotype,you must specify correct radiotype ,so we know how to play )
	 <br/>
	<font color=red><b>$form_message</b></font>
	<button style="padding:3px;" type=button onclick="window.location='%my_url%';"><img style="margin-right:5px;" src=/design/icons/delete.png hspace=0 vspace=0 border=0 width=16 height=16 align=left>Cancel</button>
 	<button type=submit  style="padding:3px;"><img style="margin-right:5px;" src=/design/icons/accept.png hspace=0 vspace=0 border=0 width=16 height=16 align=left>Save</button>
		
	<input type=hidden name=save value=1>
	<input type=hidden name=action value=radio_add>
    ];
    
    
				
    &template_print("template.pbx.radio.html",%t);
}
sub do_radio_edit(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $radio_id = clean_int(substr($form{id},0,100));
    %hash = database_select_as_hash("select 1,1,description,radiourl,radiotype  from musiconhold  where name='$radio_id' and service_id='$app{service_id}' ","flag,description,radiourl,radiotype");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{dic}{content} = "Invalid parameter";
		cgi_redirect("$my_url#dst");
		exit;
	}
	
	#---------------------------------------------------
	# get age status title
	#---------------------------------------------------
    $description  = $hash{1}{description} ;
    $radiourl = $hash{1}{radiourl} ; 
    $radiotype = $hash{1}{radiotype} ;  
   
    
	#
	#-------------------------------------------
	# start
	#-------------------------------------------
	%t = ();
	#
	#-------------------------------------------
	# check form
	#-------------------------------------------
	$form_ok = 0;
	$form_message = "";
 	if ($form{save} eq 1) {
		 if ($form{description} eq "") {
			$form_ok = 0;
			$form_message = "Please input radio name <br><br>";
			$form{description} = "";
		}  elsif ( ($form{radiourl} eq "")  )   { 
			$form_ok = 0;
			$form_message = "Please input radio url <br><br>";
			$form{radiourl} = "";		
		}else {
			$form_ok = 1;
		} 
		
	}
	#
 
	$form{description}	= &database_escape($form{description});
	$form{radiourl}	= &database_escape($form{radiourl});
	$form{radiotype} =  &database_escape($form{radiotype});
	#
	#-------------------------------------------
	# save
	#-------------------------------------------
	if ( ($form_ok eq 1) && ($form{save} eq 1) ) {
		
	 
		if ($form{radiotype} eq 'MMS') {  $application = '/etc/asterisk/mmsplay.sh '.$form{radiourl}; }
		else {
			$application = '/etc/asterisk/shoutplay.sh '.$form{radiourl};
		}
	 	&database_do("update musiconhold set description ='$form{description}',radiourl ='$form{radiourl}',application='$application' ,radiotype='$form{radiotype}' where name='$radio_id' ");
	#	&action_history("noc:config:agestatus:edit",('id'=>$status_id,'adm_user_id'=>$app{session_cookie_u}));
		%t = ();
	    $t{dic}{content} = "Saved!<br> please wait... <script>parent.modal_parent_reload();</script>";
		cgi_redirect("$my_url#dst");
		exit;
	}
	#
	#-------------------------------------------
	# load
	#-------------------------------------------
	if ($form{save} ne 1) {
		$form{description} = $description;
		$form{radiourl} = $radiourl ;
		$form{radiotype} = $radiotype;
		$selected_radiotype{$radiotype} = 'selected';
	 
	}
	#
	#-------------------------------------------
	# print page
	#-------------------------------------------
 
    $t{dic}{my_url}	= $my_url;
   
	 $t{dic}{content}	= qq[
	 
	 
	<form action=$my_url method=post class=clear >
	 Radio Name <br>
	 
	 <input name="description" value="$form{description}" size="50" /><br> 
	 
	 Radio Url(begin with http:// or mms://) <br>
 
	 <input name="radiourl" value="$form{radiourl}" size="50"  /><br> 
	 Radio Type <br>
 	 <select name="radiotype">
 	 <option value='SHOUTCAST' $selected_radiotype{SHOUTCAST}> SHOUTCAST </option>
 	 <option value='MMS' $selected_radiotype{MMS} > MMS   </option>
 	 </select>
	  (we current support mms radiotype and shoutcast radiotype,you must specify correct radiotype ,so we know how to play )
	 <br/>
	<font color=red><b>$form_message</b></font>
	<button style="padding:3px;" type=button onclick="window.location='$my_url';"><img style="margin-right:5px;" src=/design/icons/delete.png hspace=0 vspace=0 border=0 width=16 height=16 align=left>Cancel</button>
 	<button style="padding:3px;" type=button onclick="if (confirm('Delete?')) {window.location='$my_url?action=radio_del&id=$radio_id'};"><img style="margin-right:5px;" src=/design/icons/bin.png hspace=0 vspace=0 border=0 width=16 height=16 align=left>Delete this radio</button>
			
 	<button type=submit  style="padding:3px;"><img style="margin-right:5px;" src=/design/icons/accept.png hspace=0 vspace=0 border=0 width=16 height=16 align=left>Save</button>
		
	<input type=hidden name=save value=1>
	<input type=hidden name=id value=$radio_id>
	<input type=hidden name=action value=radio_edit>
    ];
    &template_print("template.pbx.radio.html",%t);
}

sub do_radio_del(){
    #
	#-------------------------------------------
    # confere service_id e client_id
	#-------------------------------------------
    $radio_id = clean_int(substr($form{id},0,100));
    %hash = database_select_as_hash("select 1,1,description  from musiconhold   where name='$radio_id' and service_id='$app{service_id}' ","flag,description");
    unless ($hash{1}{flag} eq 1) {
		%t = ();
		$t{dic}{content} = "Be Sure only can delete your own radio station";
		cgi_redirect("$my_url#dst");
	}
	
	&database_do("delete from  musiconhold where name='$radio_id' "); 
	cgi_redirect("$my_url#dst");
 
 
}

#=======================================================


