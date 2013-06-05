#!/usr/bin/perl
require "include.cgi";
use Data::Dumper;
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_manage_radio") ne 1) {adm_error("no permission"); exit;}
#=======================================================


#=======================================================
# create dataitem specifications
#=======================================================    
%dataitemconfig_station 			= ();
%dataitemconfig_commissionlisten	= ();
%dataitemconfig_commissionowner		= ();
%dataitemconfig_tag					= ();
&define_all_data_itens(); # i create a sub just to easy fold code... dont need be inside a sub
sub define_all_data_itens() {  
	%hash = ();
	$hash{title}				= "Radio station";
	$hash{sql_key}				= "SELECT 1 FROM radio_station where extension=#KEY# ";
	$hash{sql_del}				= "delete from radio_station where extension=#KEY# ";
	$hash{sql_add}				= "insert into radio_station (extension,date_add,date_last_change) values (#KEY#,now(),now()) ";
	$hash{sql_edit}				= "update radio_station set date_last_change=now() where extension=#KEY# ";
	$hash{key_mode}				= "MANUAL";
	$hash{key_item}				= 0;
	$hash{key_duplicate_sql}	= "SELECT 1 FROM radio_station where extension=#KEY# ";
	$hash{key_duplicate_message}= "Radio extension already in use";
	$hash{items}{0}{title}			= "Extension";
	$hash{items}{0}{type}			= "NUMBER";
	$hash{items}{0}{min}			= 0;
	$hash{items}{0}{max}			= 99999999;
	$hash{items}{0}{sql_get}		= "SELECT extension FROM radio_station where extension=#KEY# ";
	$hash{items}{0}{error_message}	= "Please select radio extension";
	$hash{items}{1}{title}			= "Title";
	$hash{items}{1}{type}			= "STRING";
	$hash{items}{1}{sql_get}		= "SELECT title FROM radio_station where extension=#KEY# ";
	$hash{items}{1}{sql_set}		= "update radio_station set title=#VALUE# where extension=#KEY# ";
	$hash{items}{1}{error_message}	= "Please select radio title";
	$hash{items}{2}{title}			= "Description";
	$hash{items}{2}{type}			= "STRING";
	$hash{items}{2}{sql_get}		= "SELECT description FROM radio_station where extension=#KEY# ";
	$hash{items}{2}{sql_set}		= "update radio_station set description=#VALUE# where extension=#KEY# ";
	$hash{items}{2}{error_message}	= "Please select radio description";
	$hash{items}{3}{title}			= "Status";
	$hash{items}{3}{type}			= "SELECT";
	$hash{items}{3}{options_sql}	= "SELECT id,title FROM radio_station_status order by id limit 0,1000";
	$hash{items}{3}{sql_get}		= "SELECT status FROM radio_station where extension=#KEY# ";
	$hash{items}{3}{sql_set}		= "update radio_station set status=#VALUE# where extension=#KEY# ";
	$hash{items}{3}{error_message}	= "PLease select radio status";
	$hash{items}{4}{title}			= "Stream type";
	$hash{items}{4}{type}			= "SELECT";
	$hash{items}{4}{options}{0}{value}	= "SHOUTCAST";
	$hash{items}{4}{options}{0}{title}	= "Shoutcast stream";
	$hash{items}{4}{options}{1}{value}	= "UNKNOWN";
	$hash{items}{4}{options}{1}{title}	= "Unknown stream type";
	$hash{items}{4}{sql_get}		= "SELECT stream_type FROM radio_station where extension=#KEY# ";
	$hash{items}{4}{sql_set}		= "update radio_station set stream_type=#VALUE# where extension=#KEY# ";
	$hash{items}{4}{error_message}	= "Please select radio stream URL";
	$hash{items}{5}{title}			= "Stream URL";
	$hash{items}{5}{type}			= "STRING";
	$hash{items}{5}{sql_get}		= "SELECT stream_url FROM radio_station where extension=#KEY# ";
	$hash{items}{5}{sql_set}		= "update radio_station set stream_url=#VALUE# where extension=#KEY# ";
	$hash{items}{5}{error_message}	= "Please select radio stream URL";
	$hash{items}{6}{title}			= "Tags";
	$hash{items}{6}{type}			= "MULTISELECT";
	$hash{items}{6}{options_sql}	= "SELECT id,title FROM radio_tag order by title limit 0,1000";
	$hash{items}{6}{sql_set_before}	= "delete from radio_tag_station where station_extension=#KEY# ";
	$hash{items}{6}{sql_get}		= "SELECT 1 FROM radio_tag_station where station_extension=#KEY# and tag_id=#OPTIONID# ";
	$hash{items}{6}{sql_set}		= "insert into radio_tag_station (station_extension,tag_id) values (#KEY#,#OPTIONID#)  ";
	$hash{items}{6}{sql_unset}		= "delete FROM radio_tag_station where station_extension=#KEY# and tag_id=#OPTIONID# ";
	$hash{items}{6}{error_message}	= "Please one or more radio stream URL";
	$hash{items}{7}{title}			= "Listen commission";
	$hash{items}{7}{type}			= "SELECT";
	$hash{items}{7}{flags}			= "ALLOW_BLANK";
	$hash{items}{7}{options_sql}	= "SELECT id,title FROM service_commission_type WHERE engine='RADIO_LISTEN' ORDER BY title ";
	$hash{items}{7}{sql_get}		= "SELECT listen_commission_id FROM radio_station where extension=#KEY# ";
	$hash{items}{7}{sql_set}		= "update radio_station set listen_commission_id=#VALUE# where extension=#KEY# ";
	$hash{items}{7}{error_message}	= "PLease select radio listen commission";
	$hash{items}{8}{title}			= "Owner commission";
	$hash{items}{8}{type}			= "SELECT";
	$hash{items}{8}{flags}			= "ALLOW_BLANK";
	$hash{items}{8}{options_sql}	= "SELECT id,title FROM service_commission_type WHERE engine='RADIO_OWNER' ORDER BY title ";
	$hash{items}{8}{sql_get}		= "SELECT owner_commission_id FROM radio_station where extension=#KEY# ";
	$hash{items}{8}{sql_set}		= "update radio_station set owner_commission_id=#VALUE# where extension=#KEY# ";
	$hash{items}{8}{error_message}	= "PLease select radio owner commission";
	$hash{items}{9}{title}			= "Owner Service_ID";
	$hash{items}{9}{type}			= "NUMBER";
	$hash{items}{9}{flags}			= "ALLOW_BLANK";
	$hash{items}{9}{sql_get}		= "SELECT owner_service_id FROM radio_station where extension=#KEY# ";
	$hash{items}{9}{sql_set}		= "update radio_station set owner_service_id=#VALUE# where extension=#KEY# ";
	$hash{items}{9}{error_message}	= "Enter zenofon service_id to collect owner commissions";
	%dataitemconfig_station = %hash;
	#=======================================================
	%hash = ();
	$hash{title}						= "Radio listen commission";
	$hash{sql_key}						= "SELECT 1 FROM service_commission_type where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{sql_del}						= "delete from service_commission_type where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{sql_add}						= "insert into service_commission_type (engine) values ('RADIO_LISTEN') ";
	$hash{items}{0}{title}				= "Title";
	$hash{items}{0}{type}				= "STRING";
	$hash{items}{0}{sql_get}			= "SELECT title FROM service_commission_type where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{0}{sql_set}			= "update service_commission_type set title=#VALUE# where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{0}{error_message}		= "Please select commission title";
	$hash{items}{1}{title}				= "Value type";
	$hash{items}{1}{type}				= "SELECT";
	$hash{items}{1}{options}{0}{value}	= "VALUE";
	$hash{items}{1}{options}{0}{title}	= "Fixed value per listen session";
	$hash{items}{1}{options}{1}{value}	= "BY_CALL_MINUTES";
	$hash{items}{1}{options}{1}{title}	= "Rate per minute";
	$hash{items}{1}{sql_get}			= "SELECT value_type FROM service_commission_type where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{1}{sql_set}			= "update service_commission_type set value_type=#VALUE# where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{1}{error_message}		= "Please select commission value type";
	$hash{items}{2}{title}				= "Commission value";
	$hash{items}{2}{type}				= "NUMBER";
	$hash{items}{2}{min}				= 0;
	$hash{items}{2}{max}				= 100;
	$hash{items}{2}{sql_get}			= "SELECT value FROM service_commission_type where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{2}{sql_set}			= "update service_commission_type set value=#VALUE# where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{2}{error_message}		= "Please select listen commission";
	$hash{items}{3}{title}				= "Days to use as credit";
	$hash{items}{3}{type}				= "NUMBER";
	$hash{items}{3}{min}				= 0;
	$hash{items}{3}{max}				= 9999;
	$hash{items}{3}{sql_get}			= "SELECT days_to_convert_to_credit FROM service_commission_type where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{3}{sql_set}			= "update service_commission_type set days_to_convert_to_credit=#VALUE# where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{3}{error_message}		= "Please select days";
	$hash{items}{4}{title}				= "Days to withdraw";
	$hash{items}{4}{type}				= "NUMBER";
	$hash{items}{4}{min}				= 0;
	$hash{items}{4}{max}				= 9999;
	$hash{items}{4}{sql_get}			= "SELECT days_to_convert_to_check FROM service_commission_type where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{4}{sql_set}			= "update service_commission_type set days_to_convert_to_check=#VALUE# where engine='RADIO_LISTEN' and id=#KEY# ";
	$hash{items}{4}{error_message}		= "Please select days";
	%dataitemconfig_commissionlisten = %hash;
	#=======================================================
	%hash = ();
	$hash{title}						= "Radio owner commission";
	$hash{sql_key}						= "SELECT 1 FROM service_commission_type where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{sql_del}						= "delete from service_commission_type where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{sql_add}						= "insert into service_commission_type (engine) values ('RADIO_OWNER') ";
	$hash{items}{0}{title}				= "Title";
	$hash{items}{0}{type}				= "STRING";
	$hash{items}{0}{sql_get}			= "SELECT title FROM service_commission_type where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{0}{sql_set}			= "update service_commission_type set title=#VALUE# where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{0}{error_message}		= "Please select commission title";
	$hash{items}{1}{title}				= "Value type";
	$hash{items}{1}{type}				= "SELECT";
	$hash{items}{1}{options}{0}{value}	= "VALUE";
	$hash{items}{1}{options}{0}{title}	= "Fixed value per listen session";
	$hash{items}{1}{options}{1}{value}	= "BY_CALL_MINUTES";
	$hash{items}{1}{options}{1}{title}	= "Rate per minute";
	$hash{items}{1}{sql_get}			= "SELECT value_type FROM service_commission_type where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{1}{sql_set}			= "update service_commission_type set value_type=#VALUE# where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{1}{error_message}		= "Please select commission value type";
	$hash{items}{2}{title}				= "Commission value";
	$hash{items}{2}{type}				= "NUMBER";
	$hash{items}{2}{min}				= 0;
	$hash{items}{2}{max}				= 100;
	$hash{items}{2}{sql_get}			= "SELECT value FROM service_commission_type where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{2}{sql_set}			= "update service_commission_type set value=#VALUE# where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{2}{error_message}		= "Please select owner commission";
	$hash{items}{3}{title}				= "Days to use as credit";
	$hash{items}{3}{type}				= "NUMBER";
	$hash{items}{3}{min}				= 0;
	$hash{items}{3}{max}				= 9999;
	$hash{items}{3}{sql_get}			= "SELECT days_to_convert_to_credit FROM service_commission_type where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{3}{sql_set}			= "update service_commission_type set days_to_convert_to_credit=#VALUE# where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{3}{error_message}		= "Please select days";
	$hash{items}{4}{title}				= "Days to withdraw";
	$hash{items}{4}{type}				= "NUMBER";
	$hash{items}{4}{min}				= 0;
	$hash{items}{4}{max}				= 9999;
	$hash{items}{4}{sql_get}			= "SELECT days_to_convert_to_check FROM service_commission_type where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{4}{sql_set}			= "update service_commission_type set days_to_convert_to_check=#VALUE# where engine='RADIO_OWNER' and id=#KEY# ";
	$hash{items}{4}{error_message}		= "Please select days";
	%dataitemconfig_commissionowner = %hash;
	#=======================================================
	%hash = ();
	$hash{title}						= "Radio listen commission";
	$hash{sql_key}						= "SELECT 1 FROM radio_tag where id=#KEY# ";
	$hash{sql_del}						= "delete from radio_tag where id=#KEY# ";
	$hash{sql_add}						= "insert into radio_tag (title) values ('') ";
	$hash{items}{0}{title}				= "Title";
	$hash{items}{0}{type}				= "STRING";
	$hash{items}{0}{sql_get}			= "SELECT title FROM radio_tag where id=#KEY# ";
	$hash{items}{0}{sql_set}			= "update radio_tag set title=#VALUE# where id=#KEY# ";
	$hash{items}{0}{error_message}		= "Please select tag title";
	%dataitemconfig_tag = %hash;
	#=======================================================
	%hash = ();
	$hash{title}						= "Radio gateway";
	$hash{sql_key}						= "SELECT 1 FROM radio_gateway where id=#KEY# ";
	$hash{sql_del}						= "delete from radio_gateway where id=#KEY# ";
	$hash{sql_del_2}					= "update radio_gateway_did set radio_gateway_id=null where radio_gateway_id=#KEY# ";
	$hash{sql_add}						= "insert into radio_gateway (title) values ('') ";
	$hash{items}{0}{title}				= "Title";
	$hash{items}{0}{type}				= "STRING";
	$hash{items}{0}{sql_get}			= "SELECT title FROM radio_gateway where id=#KEY# ";
	$hash{items}{0}{sql_set}			= "update radio_gateway set title=#VALUE# where id=#KEY# ";
	$hash{items}{0}{error_message}		= "Please select gateway title";
	$hash{items}{1}{title}				= "DIDs";
	$hash{items}{1}{type}				= "SELECT";
	$hash{items}{1}{flags}				= "ALLOW_BLANK";
	$hash{items}{1}{options_sql}		= "SELECT id,title FROM radio_gateway_did WHERE radio_gateway_id is null or radio_gateway_id=#KEY# ORDER BY title ";
	$hash{items}{1}{sql_get}			= "SELECT id FROM radio_gateway_did where radio_gateway_id=#KEY# limit 0,1";
	$hash{items}{1}{sql_before_all_sets}= "update radio_gateway_did set radio_gateway_id=null where radio_gateway_id=#KEY# ";
	$hash{items}{1}{sql_set}			= "update radio_gateway_did set radio_gateway_id=#KEY# where id=#VALUE# ";
	$hash{items}{1}{error_message}		= "PLease select radio gateway DID";
	foreach $i (1..9) {
		$hash{items}{$i+1}{title}			= "Favorite $i";
		$hash{items}{$i+1}{type}			= "NUMBER";
		$hash{items}{$i+1}{flags}			= "ALLOW_BLANK";
		$hash{items}{$i+1}{sql_get}			= "SELECT favorite_0$i FROM radio_gateway where id=#KEY# ";
		$hash{items}{$i+1}{sql_set}			= "update radio_gateway set favorite_0$i=#VALUE# where id=#KEY# ";
		$hash{items}{$i+1}{error_message}	= "Enter Radio extension For favorite $i";
	}

	%dataitemconfig_radiogateway = %hash;
}
#=======================================================



#=======================================================
# main loop
#=======================================================    
$my_url = "radio.cgi";
$action = $form{action};
if 		($action eq "radio_stations")					{ &do_radio_stations();					}
elsif 	($action eq "radio_station_edit")				{ &do_radio_station_edit();				}
elsif 	($action eq "radio_station_del")				{ &do_radio_station_del();				}
elsif 	($action eq "radio_station_add")				{ &do_radio_station_add();				}
elsif 	($action eq "radio_station_download")			{ &do_radio_station_download();			}
elsif 	($action eq "radio_station_upload")				{ &do_radio_station_upload();			}
elsif 	($action eq "radio_commissions_listen")			{ &do_radio_commissions_listen();		}
elsif 	($action eq "radio_commission_listen_edit")		{ &do_radio_commission_listen_edit();	}
elsif 	($action eq "radio_commission_listen_del")		{ &do_radio_commission_listen_del();	}
elsif 	($action eq "radio_commission_listen_add")		{ &do_radio_commission_listen_add();	}
elsif 	($action eq "radio_commissions_owner")			{ &do_radio_commissions_owner();		}
elsif 	($action eq "radio_commission_owner_edit")		{ &do_radio_commission_owner_edit();	}
elsif 	($action eq "radio_commission_owner_del")		{ &do_radio_commission_owner_del();		}
elsif 	($action eq "radio_commission_owner_add")		{ &do_radio_commission_owner_add();		}
elsif 	($action eq "radio_tags")						{ &do_radio_tags();						}
elsif 	($action eq "radio_tag_edit")					{ &do_radio_tag_edit();					}
elsif 	($action eq "radio_tag_del")					{ &do_radio_tag_del();					}
elsif 	($action eq "radio_tag_add")					{ &do_radio_tag_add();					}
elsif 	($action eq "radio_gateways")					{ &do_radio_gateways();					}
elsif 	($action eq "radio_gateway_edit")				{ &do_radio_gateway_edit();				}
elsif 	($action eq "radio_gateway_del")				{ &do_radio_gateway_del();				}
elsif 	($action eq "radio_gateway_add")				{ &do_radio_gateway_add();				}
elsif 	($action eq "radio_musiconhold_update_all")		{ &do_radio_musiconhold_update_all();	}
else													{ &cgi_redirect("config.cgi");			}
exit;
#=======================================================




#=======================================================
sub do_radio_musiconhold_update_all(){
	print "Content-type: text/plain\n\n";
	$sql = "SELECT 1,1,count(*) FROM radio_station ";
	%hash = database_select_as_hash($sql,"flag,value");
	$tmp = ($hash{1}{flag} eq 1) ? $hash{1}{value} : 0;
	print "This action sync all radio servers (send data from radio_control [here] \n";
	print "to radio_data). Just add &sync_now=1 at this url to start proccess \n";
	print "and DONT stop cgi proccess.\n";
	print "\n";
	print "Because first we delete all stations at radio_data and then re-create\n"; 
	print "one by one, you have to wait system sync ALL $tmp radio stations. \n";
	print "Dont stop or we will leave radio_data with incomplete data\n";
	print "\n";
	if ($form{sync_now} eq 1) {
		print "Sync started! DONT STOP now!!\n";
		&zenofon_radiodata_extension_del_all();
		$sql = "SELECT extension,stream_type,stream_url FROM radio_station r LIMIT 0,1000";
		%hash = database_select_as_hash($sql,"type,url");
		$c=0;
		foreach $e (keys %hash) {
			$c++;
			$t = $hash{$e}{type};
			$u = $hash{$e}{url};
			#$tmp = 1;
			$tmp = &zenofon_radiodata_extension_set($e,$t,$u);
			if ($tmp eq 1) {
				print "$c\t$e\t[OK] $t $u \n";
			} else {
				print "$c\t$e\t[ERROR] \n";
			}
		}
	}
}
#=======================================================
sub do_radio_station_download(){
	#
	# start page
    print "Pragma: public\n";
    print "Expires: 0\n";
    print "Cache-Control: must-revalidate, post-check=0, pre-check=0\n";
    print "Content-type: application/octet-stream\n";
    print "Content-Disposition: attachment; filename=\"radio_stations.csv\"\n";
    print "Content-Description: File Transfert\n";
    print "\n";
    print "extension,";
    print "status,";
    print "title,";
    print "stream_url,";
    print "description\n";
	#
	# check search 
	$search = &trim(&clean_str(substr($form{search},0,1024),"()-_+"));
	$search_is_enabled = ($search eq "") ? 0 : 1;
	#
	# support tables
	%status_list = database_select_as_hash("select id,title from radio_station_status ");
	#
	# prepare data query
	$sql = "";
	if ($search_is_enabled eq 1) {
		#
		# data query with search
	} else {
		#
		# data query with no search
		$sql = "SELECT extension,status,title,stream_url,description FROM radio_station  ";
	}
	#
	# query data
    %hash = database_select_as_hash($sql,"status_id,title,stream_url,description");
    $tmp0="";
    $tmps=" ";
    $tmp1="\"";
    $tmp2="\r";
    $tmp3="\n";
    $tmp4="\,";
	foreach $id (sort{$a <=> $b} keys %hash){
		$status_id = $hash{$id}{status_id};
		$status = (exists($status_list{$status_id})) ? $status_list{$status_id} : "disabled";
		$status = "\L$status";
		$line = "";
		$tmp=$id;						$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .= "\"$tmp\",";
		$tmp=$status;					$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .= "\"$tmp\",";
		$tmp=$hash{$id}{title};			$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .=  "\"$tmp\",";
		$tmp=$hash{$id}{stream_url};	$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .=  "\"$tmp\",";
		$tmp=$hash{$id}{description};	$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .=  "\"$tmp\"\n";
		print $line
    }
}
sub do_radio_station_upload(){
	#
    #----------------------------------
	# read upload if we have save_id
    #----------------------------------
    $error_message = "";
    $ok_message = "";
    if ($form{save_id} eq 1) {
    	#
    	# prepare string with valid extensions into database
		$valid_extensions = "|";
		%hash = database_select_as_hash("select extension from radio_station ");
		foreach (keys %hash) { $valid_extensions .= "$_|"; }
		%station_status = database_select_as_hash("select id,title from radio_station_status ");
		%status_title_2_id = ();
		foreach $tmp (keys %station_status) {
			$tmp1 = $station_status{$tmp};
			$status_title_2_id{"\U$tmp1"} = $tmp;
		}
	    #
	    # write upload data into temp file. and create statistic data
	    $temp_file = "/tmp/.upload.rate.".time.".tmp";
	    $filehandle = $cgi->param("FileUpload");
	    open(LOCAL, ">$temp_file");
	    while($bytesread=read($filehandle,$buffer,1024)) { print LOCAL $buffer; }
	    close(LOCAL);
	    #
	    # check CSV file header
	    open(LOCAL,$temp_file);
	    $line = <LOCAL>;
	    $line = &csvtools_line_join_values(&csvtools_line_split_values($line));
	    if ("\L$line" ne "extension,status,title,stream_url,description") { $error_message = "Incorrect CSV file. Try to download file, edit and upload"; }
		#
		# if file sounds ok, try to process line by line
		if ($error_message  eq "") {
			%stats = ();
			@sql_to_run = ();
			$error_count = 0;
			@error_messages = ();
			$line_count=0;
			while(<LOCAL>){
				#
				# move line
				$line_count++;
				if ($error_count>20) {last}
				# 
				# read line
				$line = $_;
				@values = &csvtools_line_split_values($line);
				$extension = @data[0];
				%station_csv = ();
				$station_csv{status}		= &clean_str(@data[1]," /&|?-_–(\@)-,=+;.<>[]:?<>","MINIMAL");
				$station_csv{title}			= &clean_str(@data[2]," /&|?-_–(\@)-,=+;.<>[]:?<>","MINIMAL");
				$station_csv{stream_url}	= &clean_str(@data[3]," /&?-_–(\@)-,=+;.<>[]:?<>","MINIMAL");
				$station_csv{description}	= &clean_str(@data[4]," /&|?-_–(\@)-,=+;.<>[]:?<>","MINIMAL");
				$station_csv{status_id}		= (exists($status_title_2_id{"\U$station_csv{status}"})) ? $status_title_2_id{"\U$station_csv{status}"} : 0;
				$station_csv{status}		= $station_status{$station_csv{status_id}};
				# 
				# check extension
				if ($extension eq "") { $stats{line_skip_no_extension}++; next; }
				if (clean_int($extension) ne $extension) { $stats{line_skip_bad_extension_format}++; next; }
				if (index($valid_extensions,"|$extension|") eq -1) { $stats{line_skip_no_add}++; next; }
				#
				# get database station data
				%hash = database_select_as_hash("select 1,1,status,title,stream_url,description from radio_station where extension='$extension' ", "flag,status_id,title,stream_url,description");
				if ($hash{1}{flag} ne 1) { $stats{line_skip_cannot_read_station}++; next; }
				%station_db = %{$hash{1}};
				$station_db{status}		= $station_status{$station_db{status_id}};
				#
				# check if need edit
				$tmp1 = $station_db{status}.$station_db{title}.$station_db{stream_url}.$station_db{description};
				$tmp2 = $station_csv{status}.$station_csv{title}.$station_csv{stream_url}.$station_csv{description};
				if ($tmp1 eq $tmp2) { $stats{line_skip_no_change}++; next; }
				#
				# check line values before edit
				$line_error = "";
				if ($station_csv{title} eq "")	 		{ $line_error .= "Bad Title. ";		}
				if ($station_csv{description} eq "")	{ $line_error .= "Bad Description. ";	}
				if ($station_csv{stream_url} eq "")	 	{ $line_error .= "Bad url. "; 		}
				if ($line_error ne "") {
					$error_count++; 
					@error_messages=(@error_messages,"$line_error at line $line_count <br><br>[$line]<br>[".@values."]<br>[".join("|",@values)."]<br><br><br>");
					$stats{line_error_bad_CSV_data}++;
					next;
				}
				#
				# if no error, prepare sql
				$sql = "Update radio_station set title='%s', description='%s', stream_url='%s', status='%s', date_last_change=now() where extension='%s' ";
				$sql = &database_scape_sql($sql,$station_csv{title},$station_csv{description},$station_csv{stream_url},$station_csv{status_id},$extension);
				@sql_to_run = (@sql_to_run ,$sql);
				$stats{line_edit}++;
			}
			#
			# if data and no errors, lets apply
			if ( ($line_count>0) && ($error_count eq 0) ) {
				foreach $sql (@sql_to_run) { &database_do($sql); }
				&zenofon_radio_sync_radio_stations();
			}
			#
			# prepare user message
			if ( ($line_count>0) && ($error_count eq 0) ) {
			    $ok_message = "Upload OK<br> ";
			    $ok_message .= "<br><b>Statistics:</b><br>";
			    $ok_message .= "Total lines read = ". ($line_count+ 0) . "<br>";
			    $ok_message .= "lines change data = ". ($stats{line_edit}+ 0) . "<br>";
			    $ok_message .= "Lines do not change data = ". ($stats{line_skip_no_change}+ 0) . "<br>";
			    $ok_message .= "Lines error = ". ($stats{line_skip_no_add} + $stats{line_skip_no_extension} + $stats{line_skip_bad_extension_format} + $stats{line_skip_cannot_read_station} + 0) . "<br>";
			} else {
			    $error_message = "We have errors in this file.<br>";
			    foreach (@error_messages) { $error_message .= "$_.<br>"; } 
			}
		}
    }
	#
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $error_message	= ($error_message eq "") 	? "" : "<div class=alert_box><div class=alert_box_inside>$error_message </div></div>";
    $ok_message 	= ($ok_message eq "") 		? "" : "<div class=alert_box><div class=alert_box_inside style='background-image:url(/design/icons/tick-circle.png);'>$ok_message </div></div>";
    $t{my_url}	= $my_url;
    $t{title}	= "Upload/download radio stations settings";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio stations";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_stations";
    $t{breadcrumb}{2}{title}	= "Upload/download radio stations settings";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[
	<div class=clear style=width:300px;>

		<h1>Downlod</h1>
		Download a CSV file wih all radio stations settings.
		Right now we can only edit title, status, URL and description.
		<br><br>
    	<a href='$my_url?action=radio_station_download'>&#187; Download all radio stations settings</a><br>
		<br><br>

		<h1>Upload</h1>
		Upload CSV file with radio station settings.
		No radio will be deleted or created.
		System only edit radio stations that match extension in your CSV file.
		<br><br>
		<form action=$my_url method=post enctype="multipart/form-data" onsubmit="modal_loadingblock();">
			CSV file to upload:<br>
			<input name=FileUpload type=file><br>
			<input type=hidden name=action value=radio_station_upload>
			<input type=hidden name=save_id value=1>
			<button type=submit class="button button_positive " >Upload and edit radio stations</button>
		</form>
		<br>
		$error_message 
		$ok_message 

	</div>    
	];
	&template_print("template.html",%t);
}
#=======================================================
sub do_radio_stations(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "extension,title,status,url"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT ra.extension,ra.extension,ra.title,rs.title,ra.stream_url
		FROM radio_station as ra, radio_station_status as rs
		where ra.status=rs.id and ra.extension in (#SELECTED_IDS#) 
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM radio_station ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by last changed stations";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT extension FROM radio_station order by date_last_change desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Order by new stations";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT extension FROM radio_station order by date_add desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{2}{title} 	= "Order by extension";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{2}{sql} 	= "SELECT extension FROM radio_station order by CAST(extension AS SIGNED) limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{3}{title} 	= "Order by station title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{3}{sql} 	= "SELECT extension FROM radio_station order by title limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{4}{title} 	= "Order by station status";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{4}{sql} 	= "SELECT extension FROM radio_station order by CAST(status AS SIGNED), CAST(extension AS SIGNED)limit #LIMIT_1#,#LIMIT_2# ";
	# filter ids by page and search
	$datatable{sql}{filter_ids_by_search}{search_points}{0} = "SELECT extension,10 FROM radio_station where title like '%#WORD#%' ";
	$datatable{sql}{filter_ids_by_search}{search_points}{1} = "SELECT extension,1 FROM radio_station where description like '%#WORD#%' ";
	$datatable{sql}{filter_ids_by_search}{search_points}{2} = "SELECT extension,1 FROM radio_station where extension like '%#WORD#%' ";
	$datatable{sql}{filter_ids_by_search}{search_points}{3} = "SELECT extension,100 FROM radio_station where extension = '#WORD#' ";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_stations";
    $datatable{html}{line_click_link}		= "$my_url?action=radio_station_edit&key=#EXTENSION#";
	$datatable{html}{title}					= "Radio stations";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "extension,title,status,url";
    $datatable{html}{col_titles}			= "Extension,Station title,Status,Url";
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
    #-------------------------------
	# print page
    #-------------------------------
    %t = ();
    $t{my_url}					= $my_url;
    $t{title}					= "Radio stations";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Radio stations";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_stations";
    $tmp = format_number($datatable{data}{count},0);
	$t{content}	= qq[
    	$datatable_html 
    	<br>
    	<a href='$my_url?action=radio_station_add'>&#187; Add new radio station</a><br>
    	<a href='$my_url?action=radio_station_upload'>&#187; Upload/download radio stations settings</a><br>
	];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%datatable)."</pre>";
	&template_print("template.html",%t);
}
sub do_radio_station_add(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_station = ();
	%{$my_station{config}} = %dataitemconfig_station;
	&dataitem_initialize(\%my_station);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "";
    #$form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "SA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_stations&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_stations";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_add";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_addform_process(\%my_station,\%form_settings,\%form);
	# if form was processed ok, lets update radiodata
	if ($form_settings{status_ok} eq 1) {
	    $tmp_extension	= $my_station{data}{key};
	    $tmp_type		= $my_station{data}{items}{4}{value};
	    $tmp_url		= $my_station{data}{items}{5}{value};
		$tmp_uid 		= &key_md5("$tmp_type|$tmp_url");
		$sql = "Update radio_station set stream_uid='$tmp_uid' where extension='$tmp_extension' ";
		&database_do($sql);
		&zenofon_radio_sync_radio_stations();
		&cgi_redirect($form_settings{url_form_ok});
	}
	$html_form = &dataitem_web_addform_gethtml(\%my_station,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Add new radio station";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio stations";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_stations&page=$form{page}";
    $t{breadcrumb}{2}{title}	= "Add new radio station";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%my_station)."</pre>";
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%form_settings)."</pre>";
	&template_print("template.html",%t);
}
sub do_radio_station_del(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_station = ();
	%{$my_station{config}} = %dataitemconfig_station;
	&dataitem_initialize(\%my_station);
	$my_station{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_station)) {adm_error("ERROR: $my_station{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    #$form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{options}				= "";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "SD";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_edit&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_stations&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete radio station '$my_station{data}{items}{0}{value}'?</b> This will also delete all data bellong to this radio station. This as no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_del";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_deleteform_process(\%my_station,\%form_settings,\%form);
	# if form was processed ok, lets update radiodata
	if ($form_settings{status_ok} eq 1) {
	    #$tmp_e = $my_station{data}{key};
		#$tmp_a = &zenofon_radiodata_extension_del($tmp_e);
		# because we cannot re-delete a deleted station, there is no way to ask user to retry if sync fail.
		# better leave trash data at radio servers and time-to-time resync all data
		#&cgi_redirect($form_settings{url_form_ok});
		&zenofon_radio_sync_radio_stations();
		&cgi_redirect($form_settings{url_form_ok});
	}
	$html_form = &dataitem_web_deleteform_gethtml(\%my_station,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Delete radio station";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio stations";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_stations&page=$form{page}";
    $t{breadcrumb}{2}{title}	= "Edit radio station";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_station_edit&key=$form{key}&page=$form{page}";
    $t{breadcrumb}{3}{title}	= "Delete";
    $t{breadcrumb}{3}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%my_station)."</pre>";
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%form_settings)."</pre>";
	&template_print("template.html",%t);
}
sub do_radio_station_edit(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_station = ();
	%{$my_station{config}} = %dataitemconfig_station;
	&dataitem_initialize(\%my_station);
	$my_station{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_station)) {adm_error("ERROR: $my_station{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    #$form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{options}				= "";
    $form_settings{mode}				= "EDIT";
    $form_settings{click_id_prefix}		= "SE";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_stations&page=$form{page}";
    $form_settings{url_button_delete}	= "$my_url?action=radio_station_del&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_stations&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_edit";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_editform_process(\%my_station,\%form_settings,\%form);
	# if form was processed ok, lets update radiodata
	if ($form_settings{status_ok} eq 1) {
	    $tmp_extension	= $my_station{data}{key};
	    $tmp_type		= $my_station{data}{items}{4}{value};
	    $tmp_url		= $my_station{data}{items}{5}{value};
		$tmp_uid 		= &key_md5("$tmp_type|$tmp_url");
		$sql = "Update radio_station set stream_uid='$tmp_uid' where extension='$tmp_extension' ";
		&database_do($sql);
		&zenofon_radio_sync_radio_stations();
		&cgi_redirect($form_settings{url_form_ok});
	}
	$html_form = &dataitem_web_editform_gethtml(\%my_station,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit radio station";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio stations";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_stations&page=$form{page}";
    $t{breadcrumb}{2}{title}	= "Edit radio station";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%my_station)."</pre>";
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%form_settings)."</pre>";
	&template_print("template.html",%t);
}    
#=======================================================
sub do_radio_commissions_listen(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "id,title,qtd"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT ct.id,ct.id,ct.title,(select count(*) from radio_station as rs where rs.listen_commission_id=ct.id) 
		FROM service_commission_type as ct 
		WHERE ct.engine='RADIO_LISTEN' and ct.id in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM service_commission_type WHERE engine='RADIO_LISTEN' ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM service_commission_type WHERE engine='RADIO_LISTEN' order by title limit #LIMIT_1#,#LIMIT_2# ";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_commissions_listen";
    $datatable{html}{line_click_link}		= "$my_url?action=radio_commission_listen_edit&key=#ID#";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "title,qtd";
    $datatable{html}{col_titles}			= "Listen commission,Stations assigned";
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
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Radio listen commission";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Radio listen commissions";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_commissions_listen";
    $t{content}	= qq[ 
    	$datatable_html 
    	<br>
    	<a href=$my_url?action=radio_commission_listen_add>&#187; Add new radio listen commission</a>
    ];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%datatable)."</pre>";
    &template_print("template.html",%t);
}
sub do_radio_commission_listen_add(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_commission = ();
	%{$my_commission{config}} = %dataitemconfig_commissionlisten;
	&dataitem_initialize(\%my_commission);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "SA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_commissions_listen&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_commissions_listen";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_commission_listen_add";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_addform_process(\%my_commission,\%form_settings,\%form);
	$html_form = &dataitem_web_addform_gethtml(\%my_commission,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Add new radio listen commission";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio listen commissions";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_commissions_listen";
    $t{breadcrumb}{2}{title}	= "Add new radio listen commission";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
sub do_radio_commission_listen_edit(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_commission = ();
	%{$my_commission{config}} = %dataitemconfig_commissionlisten;
	&dataitem_initialize(\%my_commission);
	$my_commission{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_commission)) {adm_error("ERROR: $my_commission{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{click_id_prefix}		= "SE";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_commissions_listen&page=$form{page}";
    $form_settings{url_button_delete}	= "$my_url?action=radio_commission_listen_del&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_commissions_listen&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_commission_listen_edit";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_editform_process(\%my_commission,\%form_settings,\%form);
	$html_form = &dataitem_web_editform_gethtml(\%my_commission,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit radio listen commission";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio listen commissions";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_commissions_listen";
    $t{breadcrumb}{2}{title}	= "Edit radio listen commission";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}    
sub do_radio_commission_listen_del(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_commission = ();
	%{$my_commission{config}} = %dataitemconfig_commissionlisten;
	&dataitem_initialize(\%my_commission);
	$my_commission{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_commission)) {adm_error("ERROR: $my_commission{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "SD";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_commission_listen_edit&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_commissions_listen&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete radio listen commission '$my_commission{data}{items}{0}{value}'?</b> This will also delete all connections to radio station. This does not delete past commissions. This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_commission_listen_del";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_deleteform_process(\%my_commission,\%form_settings,\%form);
	$html_form = &dataitem_web_deleteform_gethtml(\%my_commission,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Delete listen commission";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio listen commissions";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_commissions_listen";
    $t{breadcrumb}{2}{title}	= "Edit radio listen commission";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_commission_listen_edit&key=$form{key}&page=$form{page}";
    $t{breadcrumb}{3}{title}	= "Delete";
    $t{breadcrumb}{3}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
#=======================================================
sub do_radio_commissions_owner(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "id,title,qtd"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT ct.id,ct.id,ct.title,(select count(*) from radio_station as rs where rs.owner_commission_id=ct.id) 
		FROM service_commission_type as ct 
		WHERE ct.engine='RADIO_OWNER' and ct.id in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM service_commission_type WHERE engine='RADIO_OWNER' ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM service_commission_type WHERE engine='RADIO_OWNER' order by title limit #LIMIT_1#,#LIMIT_2# ";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_commissions_owner";
    $datatable{html}{line_click_link}		= "$my_url?action=radio_commission_owner_edit&key=#ID#";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "title,qtd";
    $datatable{html}{col_titles}			= "Listen commission,Stations assigned";
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
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Radio owner commission";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Radio owner commissions";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_commissions_owner";
    $t{content}	= qq[ 
    	$datatable_html 
    	<br>
    	<a href=$my_url?action=radio_commission_owner_add>&#187; Add new radio owner commission</a>
    ];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%datatable)."</pre>";
    &template_print("template.html",%t);
}
sub do_radio_commission_owner_add(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_commission = ();
	%{$my_commission{config}} = %dataitemconfig_commissionowner;
	&dataitem_initialize(\%my_commission);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "SA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_commissions_owner&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_commissions_owner";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_commission_owner_add";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_addform_process(\%my_commission,\%form_settings,\%form);
	$html_form = &dataitem_web_addform_gethtml(\%my_commission,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Add new radio owner commission";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio owner commissions";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_commissions_owner";
    $t{breadcrumb}{2}{title}	= "Add new radio owner commission";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
sub do_radio_commission_owner_edit(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_commission = ();
	%{$my_commission{config}} = %dataitemconfig_commissionowner;
	&dataitem_initialize(\%my_commission);
	$my_commission{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_commission)) {adm_error("ERROR: $my_commission{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{click_id_prefix}		= "SE";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_commissions_owner&page=$form{page}";
    $form_settings{url_button_delete}	= "$my_url?action=radio_commission_owner_del&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_commissions_owner&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_commission_owner_edit";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_editform_process(\%my_commission,\%form_settings,\%form);
	$html_form = &dataitem_web_editform_gethtml(\%my_commission,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit radio owner commission";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio owner commissions";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_commissions_owner";
    $t{breadcrumb}{2}{title}	= "Edit radio owner commission";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}    
sub do_radio_commission_owner_del(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_commission = ();
	%{$my_commission{config}} = %dataitemconfig_commissionowner;
	&dataitem_initialize(\%my_commission);
	$my_commission{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_commission)) {adm_error("ERROR: $my_commission{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "SD";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_commission_owner_edit&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_commissions_owner&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete radio owner commission '$my_commission{data}{items}{0}{value}'?</b> This will also delete all connections to radio station. This does not delete past commissions. This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_commission_owner_del";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_deleteform_process(\%my_commission,\%form_settings,\%form);
	$html_form = &dataitem_web_deleteform_gethtml(\%my_commission,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Delete owner commission";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio owner commissions";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_commissions_owner";
    $t{breadcrumb}{2}{title}	= "Edit radio owner commission";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_commission_owner_edit&key=$form{key}&page=$form{page}";
    $t{breadcrumb}{3}{title}	= "Delete";
    $t{breadcrumb}{3}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
#=======================================================
sub do_radio_tags(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "id,title,qtd"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT rt.id,rt.id,rt.title,(select count(*) from radio_tag_station as rts where rt.id=rts.tag_id) 
		FROM radio_tag as rt 
		WHERE rt.id in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM radio_tag  ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_tag order by title limit #LIMIT_1#,#LIMIT_2# ";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_tags";
    $datatable{html}{line_click_link}		= "$my_url?action=radio_tag_edit&key=#ID#";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "title,qtd";
    $datatable{html}{col_titles}			= "Tag,Stations assigned";
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
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Radio tags";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Radio tags";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_tags";
    $t{content}	= qq[ 
    	$datatable_html 
    	<br>
    	<a href=$my_url?action=radio_tag_add>&#187; Add new radio tag</a>
    ];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%datatable)."</pre>";
    &template_print("template.html",%t);
}
sub do_radio_tag_add(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_tag;
	&dataitem_initialize(\%my_dataitem);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "TA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_tags&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_tags";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_tag_add";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_addform_process(\%my_dataitem,\%form_settings,\%form);
	$html_form = &dataitem_web_addform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Add new radio tag";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio tags";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_tags";
    $t{breadcrumb}{2}{title}	= "Add new radio tag";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
sub do_radio_tag_edit(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_tag;
	&dataitem_initialize(\%my_dataitem);
	$my_dataitem{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{click_id_prefix}		= "SE";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_tags&page=$form{page}";
    $form_settings{url_button_delete}	= "$my_url?action=radio_tag_del&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_tags&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_tag_edit";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_editform_process(\%my_dataitem,\%form_settings,\%form);
	$html_form = &dataitem_web_editform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit radio tag";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio tags";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_tags";
    $t{breadcrumb}{2}{title}	= "Edit radio tag";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}    
sub do_radio_tag_del(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_tag;
	&dataitem_initialize(\%my_dataitem);
	$my_dataitem{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "SD";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_tag_edit&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_tags&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete radio tag '$my_dataitem{data}{items}{0}{value}'?</b> This will also delete all connections to radio station. This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_tag_del";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_deleteform_process(\%my_dataitem,\%form_settings,\%form);
	$html_form = &dataitem_web_deleteform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Delete tag";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio tags";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_tags";
    $t{breadcrumb}{2}{title}	= "Edit radio tag";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_tag_edit&key=$form{key}&page=$form{page}";
    $t{breadcrumb}{3}{title}	= "Delete";
    $t{breadcrumb}{3}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%my_dataitem)."</pre>";
	&template_print("template.html",%t);
}
#=======================================================
sub do_radio_gateways(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
    $datatable{sql}{col_names}			= "id,title,did"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT 
		rg.id,
		rg.id,
		rg.title, 
		(select rgd.title from radio_gateway_did as rgd where rgd.radio_gateway_id=rg.id limit 0,1) as did 
		FROM radio_gateway as rg  
		where rg.id in (#SELECTED_IDS#)  
	";
	# filter ids by page and order
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM radio_gateway ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_gateway order by title limit #LIMIT_1#,#LIMIT_2# ";
	# html values	
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_gateways";
    $datatable{html}{line_click_link}		= "$my_url?action=radio_gateway_edit&key=#ID#";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "title,did";
    $datatable{html}{col_titles}			= "Radio gateway,DIDs assigned";
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
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Radio gateways";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio gateways";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_gateways";
    $t{content}	= qq[ 
    	$datatable_html 
    	<br>
    	<a href=$my_url?action=radio_gateway_add>&#187; Add new radio gateway</a>
    ];
    &template_print("template.html",%t);
	
}
sub do_radio_gateway_add(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_radiogateway;
	&dataitem_initialize(\%my_dataitem);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "TA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_gateways&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_gateways";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_gateway_add";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_addform_process(\%my_dataitem,\%form_settings,\%form);
	$html_form = &dataitem_web_addform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Add new radio gateway";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio gateways";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_gateways";
    $t{breadcrumb}{2}{title}	= "Add new radio gateway";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
	
}
sub do_radio_gateway_edit(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_radiogateway;
	$my_dataitem{data}{key}  = &clean_int(substr($form{key},0,100));;
	&dataitem_initialize(\%my_dataitem);
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{click_id_prefix}		= "RGE";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_gateways&page=$form{page}";
    $form_settings{url_button_delete}	= "$my_url?action=radio_gateway_del&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_gateways&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_gateway_edit";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_editform_process(\%my_dataitem,\%form_settings,\%form);
	$html_form = &dataitem_web_editform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit radio gateway";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio gateways";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_gateways";
    $t{breadcrumb}{2}{title}	= "Edit radio gateway";
    $t{breadcrumb}{2}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%my_dataitem)."</pre>";
	&template_print("template.html",%t);
}
sub do_radio_gateway_del(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_radiogateway;
	&dataitem_initialize(\%my_dataitem);
	$my_dataitem{data}{key}  = &clean_int(substr($form{key},0,100));;
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{options}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "SD";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_gateway_edit&key=$form{key}&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_gateways&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete radio gateway '$my_dataitem{data}{items}{0}{value}'?</b> This will also delete all connections to radio station. This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_gateway_del";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_deleteform_process(\%my_dataitem,\%form_settings,\%form);
	$html_form = &dataitem_web_deleteform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Delete gateway";
    $t{breadcrumb}{0}{title}	= "System settings";
    $t{breadcrumb}{0}{url}		= "config.cgi";
    $t{breadcrumb}{1}{title}	= "Radio gateways";
    $t{breadcrumb}{1}{url}		= "$my_url?action=radio_gateways";
    $t{breadcrumb}{2}{title}	= "Edit radio gateway";
    $t{breadcrumb}{2}{url}		= "$my_url?action=radio_gateway_edit&key=$form{key}&page=$form{page}";
    $t{breadcrumb}{3}{title}	= "Delete";
    $t{breadcrumb}{3}{url}		= "";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	#$t{content}		.= "<br><br><h1>DEBUG ONLY FOR NOW</h1>";
	#$t{content}		.= "<div style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>"; foreach (sort keys %form) {$t{content}	.= "DUMP FORM ($_) = ($form{$_})<br>"; } $t{content} .= "</div>"; 
	#$t{content}		.= "<pre style='border:1px solid #c0c0c0; margin:10px; padding:10px; font-size:10px; line-height:110%;'>".Dumper(%my_dataitem)."</pre>";
	&template_print("template.html",%t);

}
#=======================================================






#=======================================================
# radio API to access yang rs.php
#=======================================================
# http://67.55.209.154/rs.php?optype=edit&exten=123&radiourl=http://1.2.3.44&radiotype=shoutcast  (for add or edit new radio)
# http://67.55.209.154/rs.php?optype=del&exten=123 to delete radio :exten =123
# http://67.55.209.154/rs.php?optype=delall to clear 
#=======================================================
sub zenofon_radiodata_extension_set() {	
	local($extension_raw,$radio_type_raw,$radio_url_raw) = @_;
	local($sql,%hash,$i,$tmp,$tmp1,$tmp2);
	local($url,$radiodata_ip,$answer);
	#
	# check basic things
	$extension	= &clean_int($extension_raw);
	$radio_type	= &clean_str($radio_type_raw);
	$radio_url	= &clean_str($radio_url_raw,"URL");
#warning("RADIO_EXTENSION:$extension");
#warning("RADIO_TYPE:$radio_type");
#warning("RADIO_URL:$radio_url");
	if ( ($extension eq "") || ($extension ne $extension_raw) ) {return 0 }
	if ( ($radio_type eq "") || ($radio_type ne $radio_type_raw) ) {return 0 }
	if ( ($radio_url eq "") || ($radio_url ne $radio_url_raw) ) {return 0 }
	$radio_type	= "\U$radio_type";
	#
	# prepare url
	$radiodata_ip = "67.55.209.154"; # later, use  &data_get("adm_data","radiodata","ip") and add this set at general settings;
	$url  = "https://".$radiodata_ip."/rs.php?optype=edit";
	$url .= "&exten=".&cgi_url_encode($extension);
	$url .= "&radiourl=".&cgi_url_encode($radio_url);
	$url .= "&radiotype=".&cgi_url_encode($radio_type);
	#$url  = "https://".$radiodata_ip."/index.html";
#warning("URL:$url");
	#
	# connect and get status
	$objRequest		= HTTP::Request->new("GET",$url);
	$objUserAgent	= LWP::UserAgent->new;
	$objResponse	= $objUserAgent->request($objRequest);
	if (!$objResponse->is_error) {
		$answer = $objResponse->content;
#warning("ANSWER:$answer");
		if ($answer eq "00") {
#warning("STATUS:OK");
			return 1;
		} else {
#warning("STATUS:DATA_ERROR");
			return 0;
		}
	} else {
#warning("STATUS:NETWORK_ERROR");
		return 0; 
	}
}
sub zenofon_radiodata_extension_get() {	return 0; }
sub zenofon_radiodata_extension_del() {	
	local($extension_raw,) = @_;
	local($sql,%hash,$i,$tmp,$tmp1,$tmp2);
	local($url,$radiodata_ip,$answer);
	#
	# check basic things
	$extension	= &clean_int($extension_raw);
#warning("RADIO_EXTENSION:$extension");
	if ( ($extension eq "") || ($extension ne $extension_raw) ) {return 0 }
	#
	# prepare url
	$radiodata_ip = "67.55.209.154"; # later, use  &data_get("adm_data","radiodata","ip") and add this set at general settings;
	$url  = "https://".$radiodata_ip."/rs.php?optype=del";
	$url .= "&exten=".&cgi_url_encode($extension);
	#$url  = "https://".$radiodata_ip."/index.html";
#warning("URL:$url");
	#
	# connect and get status
	$objRequest		= HTTP::Request->new("GET",$url);
	$objUserAgent	= LWP::UserAgent->new;
	$objResponse	= $objUserAgent->request($objRequest);
	if (!$objResponse->is_error) {
		$answer = $objResponse->content;
#warning("ANSWER:$answer");
		if ($answer eq "00") {
#warning("STATUS:OK");
			return 1;
		} else {
#warning("STATUS:DATA_ERROR");
			return 0;
		}
	} else {
#warning("STATUS:NETWORK_ERROR");
		return 0; 
	}
}
sub zenofon_radiodata_extension_del_all() {	
	local($sql,%hash,$i,$tmp,$tmp1,$tmp2);
	local($url,$radiodata_ip,$answer);
	#
	# prepare url
	$radiodata_ip = "67.55.209.154"; # later, use  &data_get("adm_data","radiodata","ip") and add this set at general settings;
	$url  = "https://".$radiodata_ip."/rs.php?optype=delall";
#warning("URL:$url");
	#
	# connect and get status
	$objRequest		= HTTP::Request->new("GET",$url);
	$objUserAgent	= LWP::UserAgent->new;
	$objResponse	= $objUserAgent->request($objRequest);
	if (!$objResponse->is_error) {
		$answer = $objResponse->content;
#warning("ANSWER:$answer");
		if ($answer eq "00") {
#warning("STATUS:OK");
			return 1;
		} else {
#warning("STATUS:DATA_ERROR");
			return 0;
		}
	} else {
#warning("STATUS:NETWORK_ERROR");
		return 0; 
	}

}
#=======================================================
# NEW radio API to access musiconhold
#=======================================================
# we move radio control to radio_data server, no more 
# need update musiconhold table by remote api. Now we 
#just need sync radio_stations -> musiconhold tables
#=======================================================
sub zenofon_radio_sync_radio_stations(){
	$sql = "SELECT extension,stream_type,stream_url,stream_uid FROM radio_station where stream_uid is null or stream_uid = '' ";
	%hash = database_select_as_hash($sql,"type,url,uid");
	foreach $e (keys %hash){
		$type	= $hash{$e}{type};
		$url	= $hash{$e}{url};
		$uid	= $hash{$e}{uid};
		if ($uid eq "") {
			$uid = &key_md5("$type|$url");
			$sql = "Update radio_station set stream_uid='$uid' where extension='$e' ";
			&database_do($sql);
			
		}
	}
}
#=======================================================




#=======================================================
# trash
#=======================================================
	#$sql = "delete FROM radio_station ";
	#database_do($sql);
	#$sql = "SELECT exten,radiourl,description FROM musiconhold ";
	#%hash = database_select_as_hash($sql,"url,desc");
	#foreach $e (keys %hash) {
	#	$t = $hash{$e}{desc};
	#	$u = $hash{$e}{url};
	#	$sql = "insert into radio_station (extension,title,description,date_add,date_last_change,stream_type,stream_url) values ('%s', '%s', '%s', now(), now(), '%s', '%s')";
	#	$sql = &database_scape_sql($sql,$e,substr($t,0,20),$t,"showtcast",$u);
	#	database_do($sql)
	#}
#=======================================================
	
	
	
	