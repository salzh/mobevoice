#!/usr/bin/perl
require "include.cgi";
#=======================================================
# TODO: What is stations-new? a test code? can we delete? we dont need test code in production with flaws to expose bussines data
#=======================================================
# lock this app to system.manager eyes only
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("radio.manager") ne 1) {adm_error("no permission"); exit;}
#=======================================================




#=======================================================
# logout if no session
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
#unless (&active_user_permission_get("radio.data.access") >0) {adm_error("no permission"); exit;}
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
	#--------------------------------
	%hash = ();
	$hash{title}						= "Radio station";
	$hash{sql_key}						= "SELECT 1 FROM radio_data_station where id=#KEY# ";
	$tmp=0;
	$hash{items}{$tmp}{title}				= "Title";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT title FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set title=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select radio station title";
	$tmp++;
	$hash{items}{$tmp}{title}			= "DIDs";
	$hash{items}{$tmp}{type}			= "SELECT";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY,UI_READONLY";
	$hash{items}{$tmp}{options_first} 	= "(No DID assigned)";
	$hash{items}{$tmp}{options_sql}		= "SELECT id,title FROM radio_data_did WHERE radio_data_station_id is null or radio_data_station_id=#KEY# ORDER BY title ";
	$hash{items}{$tmp}{sql_get}			= "SELECT id FROM radio_data_did where radio_data_station_id=#KEY# limit 0,1";
	$hash{items}{$tmp}{error_message}	= "PLease select radio gateway DID";
	%dataitemconfig_radio_station_simple= %hash;
	#--------------------------------
	%hash = ();
	$hash{title}						= "Radio station DID";
	$hash{sql_key}						= "SELECT 1 FROM radio_data_station where id=#KEY# ";
	$hash{sql_del}						= "delete from radio_data_station where id=#KEY# ";
	$hash{sql_del_1}					= "update radio_data_station_channel set enabled=0 where radio_data_station_id=#KEY# ";
	$hash{sql_del_2}					= "update radio_data_did set radio_data_station_id=null where radio_data_station_id=#KEY# ";
	$hash{sql_add}						= "insert into radio_data_station (title) values ('') ";
	$tmp=0;
	$hash{items}{$tmp}{title}			= "Title";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT title FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set title=#VALUE# where id=#KEY# ";
	$tmp++;
	$hash{items}{$tmp}{title}			= "DIDs";
	$hash{items}{$tmp}{type}			= "SELECT";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{options_first} 	= "(No DID assigned)";
	$hash{items}{$tmp}{options_sql}		= "SELECT id,title FROM radio_data_did WHERE radio_data_station_id is null or radio_data_station_id=#KEY# ORDER BY title ";
	$hash{items}{$tmp}{sql_get}			= "SELECT id FROM radio_data_did where radio_data_station_id=#KEY# limit 0,1";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_did set radio_data_station_id=null where radio_data_station_id=#KEY# ";
	$hash{items}{$tmp}{sql_set_1}		= "update radio_data_did set radio_data_station_id=#KEY# where id=#VALUE# ";
	$hash{items}{$tmp}{error_message}	= "PLease select radio gateway DID";
	$tmp++;
	$hash{items}{$tmp}{title}			= "Owners";
	$hash{items}{$tmp}{type}			= "MULTISELECT";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{options_sql}		= "SELECT id,name FROM system_user order by name ";
	$hash{items}{$tmp}{sql_before_set}	= "delete from radio_data_station_owner where radio_data_station_id=#KEY# ";
	$hash{items}{$tmp}{sql_get}			= "SELECT 1 FROM radio_data_station_owner where radio_data_station_id=#KEY# and system_user_id=#OPTIONID# ";
	$hash{items}{$tmp}{sql_set}			= "insert into radio_data_station_owner (radio_data_station_id,system_user_id) values (#KEY#,#OPTIONID#)  ";
	$hash{items}{$tmp}{sql_unset}		= "delete FROM radio_data_station_owner where radio_data_station_id=#KEY# and system_user_id=#OPTIONID# ";
	%dataitemconfig_radio_station		= %hash;
	#--------------------------------
	%hash = ();
	$hash{title}						= "Radio station stream";
	$hash{sql_key}						= "SELECT 1 FROM radio_data_station_channel where id=#KEY# and enabled=1 ";
	$hash{sql_del}						= "update radio_data_station_channel set enabled=0 where id=#KEY# ";
	$hash{sql_add}						= "insert into radio_data_station_channel (date_add) values (now() ) ";
	$hash{items}{0}{title}				= "radio_data_station_id";
	$hash{items}{0}{type}				= "NUMBER";
	$hash{items}{0}{flags}				= "UI_HIDDEN,UI_READONLY";
	$hash{items}{0}{sql_get}			= "SELECT radio_data_station_id FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{0}{sql_set}			= "update radio_data_station_channel set radio_data_station_id=#VALUE# where id=#KEY# ";
	$hash{items}{1}{title}				= "Radio";
	$hash{items}{1}{type}				= "STRING";
	$hash{items}{1}{flags}				= "UI_READONLY";
	$hash{items}{2}{title}				= "Extension";
	$hash{items}{2}{type}				= "NUMBER";
	$hash{items}{2}{min}				= 0;
	$hash{items}{2}{max}				= 99999999;
	$hash{items}{2}{flags}				= "ALLOW_EMPTY";
	$hash{items}{2}{sql_get}			= "SELECT extension FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{2}{sql_set}			= "update radio_data_station_channel set extension=#VALUE# where id=#KEY# ";
	$hash{items}{2}{error_message}		= "Please select radio extension";

	$hash{items}{3}{title}				= "Title";
	$hash{items}{3}{type}				= "STRING";
	$hash{items}{3}{sql_get}			= "SELECT title FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{3}{sql_set}			= "update radio_data_station_channel set title=#VALUE# where id=#KEY# ";
	$hash{items}{3}{error_message}		= "Please select radio extension title";

	$hash{items}{4}{title}				= "Content source type";
	$hash{items}{4}{type}				= "SELECT";
	$hash{items}{4}{options}{0}{value}	= "SHOUTCAST";
	$hash{items}{4}{options}{0}{title}	= "Shoutcast stream";
	$hash{items}{4}{options}{1}{value}	= "MMS";
	$hash{items}{4}{options}{1}{title}	= "MMS stream ";
	$hash{items}{4}{options}{2}{value}	= "MP3";
	$hash{items}{4}{options}{2}{title}	= "Mp3 file ";
	$hash{items}{4}{options}{3}{value}	= "TEST1";
	$hash{items}{4}{options}{3}{title}	= "(DO NOT USE) Development 1";
	$hash{items}{4}{options}{4}{value}	= "TEST2";
	$hash{items}{4}{options}{4}{title}	= "(DO NOT USE) Development 2";

	$hash{items}{4}{sql_get}			= "SELECT stream_type FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{4}{sql_set}			= "update radio_data_station_channel set stream_type=#VALUE# where id=#KEY# ";
	$hash{items}{4}{error_message}		= "Please select content type";

	$hash{items}{5}{title}				= "Content source URL";
	$hash{items}{5}{type}				= "STRING";
	$hash{items}{5}{sql_get}			= "SELECT stream_url FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{5}{sql_set}			= "update radio_data_station_channel set stream_url=#VALUE# where id=#KEY# ";
	$hash{items}{5}{error_message}		= "Please select content URL";

	$hash{items}{6}{title}				= "Content source permission";
	$hash{items}{6}{type}				= "STRING";
	$hash{items}{6}{sql_get}			= "SELECT stream_permission FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{6}{sql_set}			= "update radio_data_station_channel set stream_permission=#VALUE# where id=#KEY# ";
	$hash{items}{6}{error_message}		= "Please select content permission";

	%dataitemconfig_radio_station_stream = %hash;
	#--------------------------------
	%hash = ();
	$hash{title}						= "Radio station prompt";
	$hash{sql_key}						= "SELECT 1 FROM radio_data_station_prompt where id=#KEY#  ";
	$hash{sql_del}						= "delete from radio_data_station_prompt where id=#KEY# ";
	$hash{sql_add}						= "insert into radio_data_station_prompt (date_add) values (now() ) ";
	$hash{items}{0}{title}				= "radio_data_station_id";
	$hash{items}{0}{type}				= "NUMBER";
	$hash{items}{0}{flags}				= "UI_HIDDEN,UI_READONLY";
	$hash{items}{0}{sql_get}			= "SELECT radio_data_station_id FROM radio_data_station_prompt where id=#KEY# ";
	$hash{items}{0}{sql_set}			= "update radio_data_station_prompt set radio_data_station_id=#VALUE# where id=#KEY# ";
	$hash{items}{1}{title}				= "Radio";
	$hash{items}{1}{type}				= "STRING";
	$hash{items}{1}{flags}				= "UI_READONLY";
	$hash{items}{2}{title}				= "Title";
	$hash{items}{2}{type}				= "STRING";
	$hash{items}{2}{sql_get}			= "SELECT title FROM radio_data_station_prompt where id=#KEY# ";
	$hash{items}{2}{sql_set}			= "update radio_data_station_prompt set title=#VALUE# where id=#KEY# ";
	$hash{items}{2}{error_message}		= "Please select radio prompt title";

#	$hash{items}{3}{title}				= "Prompt";
#	$hash{items}{3}{type}				= "SELECT";
#	$hash{items}{3}{flags}				= "ALLOW_EMPTY";
#	$hash{items}{3}{options_first} 		= "(Do not change)";
#	$hash{items}{3}{options}{0}{value}	= "1";
#	$hash{items}{3}{options}{0}{title}	= "Record prompt by phone";
#	$hash{items}{3}{sql_get}			= "SELECT 1 FROM radio_data_station_prompt where id=#KEY# and phone_record_pin is not null ";
#	$hash{items}{3}{sql_set}			= "update radio_data_station_prompt set phone_record_pin=if (#VALUE# = '1', concat(id,round(9*rand()),round(9*rand())) , null)  where id=#KEY#";
#	$hash{items}{3}{error_message}		= "Please select extension stream URL";

#	$hash{items}{4}{title}				= "Radio action";
#	$hash{items}{4}{type}				= "SELECT";
#	$hash{items}{4}{flags}				= "ALLOW_EMPTY";
#	$hash{items}{4}{options}{0}{value}	= "0";
#	$hash{items}{4}{options}{0}{title}	= "Welcome prompt";
#	$hash{items}{4}{options}{1}{value}	= "1";
#	$hash{items}{4}{options}{1}{title}	= "Help prompt";
#	$hash{items}{4}{sql_get}			= "SELECT stream_type FROM radio_data_station_channel where id=#KEY# ";
#	$hash{items}{4}{sql_set}			= "update radio_data_station_channel set stream_type=#VALUE# where id=#KEY# ";
#	$hash{items}{4}{error_message}		= "Please select extension stream URL";

#	$hash{items}{3}{title}				= "Prompt file";
#	$hash{items}{3}{type}				= "FILE";
#	$hash{items}{3}{sql_mimetype_get}	= "SELECT prompt_mimetype FROM radio_data_station_prompt where id=#KEY# ";
#	$hash{items}{3}{sql_mimetype_set}	= "update radio_data_station_prompt set prompt_mimetype=#VALUE# where id=#KEY# ";
#	$hash{items}{3}{sql_bytes_get}		= "SELECT prompt_bytes FROM radio_data_station_prompt where id=#KEY# ";
#	$hash{items}{3}{sql_bytes_set}		= "update radio_data_station_prompt set prompt_bytes=#VALUE# where id=#KEY# ";
#	$hash{items}{3}{accept_mimetype}	= "audio/mpeg,audio/x-wav";
#	$hash{items}{3}{accept_bytes_max}	= 1024*1024;
#	$hash{items}{3}{accept_bytes_min}	= 1;
#	$hash{items}{3}{transcode}{cmd}							= "command to translate file after upload";
#	$hash{items}{3}{transcode}{new_mimetype}				= "audio/x-gsm";
#	$hash{items}{3}{transcode}{"audio/x-wav"}{cmd}			= "command to translate file after upload";
#	$hash{items}{3}{transcode}{"audio/x-wav"}{new_mimetype}	= "audio/x-gsm";

	%dataitemconfig_radio_station_prompt = %hash;
	#--------------------------------

}
#=======================================================



#=======================================================
# get active stations
#=======================================================
# 0  no access to radio settings
# 1  view and edit they own radios
# 2  View and edit all radios plus radio DIDs
$stations_allow = "";
$stations_not_allow = "";
$issysadmin	= 0;
$tmp1	= &active_user_permission_get("radio.data.access");
if ($tmp1 eq "1"){
	$stations_allow = join(",",&database_select_as_array("SELECT distinct radio_data_station_id FROM radio_data_station_owner where system_user_id='$app{session_cookie_u}' "));
	$stations_not_allow = join(",",&database_select_as_array("SELECT distinct radio_data_station_id FROM radio_data_station_owner where system_user_id!='$app{session_cookie_u}' "));
} elsif ($tmp1 eq "2"){
	$stations_allow = "ALL";
	$issysadmin	= 1;
}
#=======================================================



#=======================================================
# main loop
#=======================================================
$my_url = "radio.stations.cgi";
$action = $form{action};

%my_user = database_select_as_hash("SELECT 1,1,id,name,email,web_user,web_password,group_id FROM $app{users_table} " .
								"where id='$app{session_cookie_u}'","flag,id,name,email,web_user,web_password,group_id");

if 		($action eq "radio_station_list")			{ &do_radio_station_list();				}
elsif 	($action eq "radio_station_view")			{ &do_radio_station_view();				}
elsif 	($action eq "radio_station_add")			{ &do_radio_station_add();				}
elsif 	($action eq "radio_station_del")			{ &do_radio_station_del();				}
elsif 	($action eq "radio_station_edit")			{ &do_radio_station_edit();				}
#elsif 	($action eq "radio_station_edit_simple")	{ &do_radio_station_edit_simple();		}
elsif 	($action eq "radio_station_stream_list")	{ &do_radio_station_stream_list();		}
elsif 	($action eq "radio_station_stream_add")		{ &do_radio_station_stream_add();		}
elsif 	($action eq "radio_station_stream_del")		{ &do_radio_station_stream_del();		}
elsif 	($action eq "radio_station_stream_edit")	{ &do_radio_station_stream_edit();		}
elsif 	($action eq "radio_station_stream_edit_new")	{ &do_radio_station_stream_edit_new();		}
elsif 	($action eq "radio_station_stream_add_new")	{ &do_radio_station_stream_add_new();		}

elsif 	($action eq "radio_station_stream_download"){ &do_radio_station_stream_download();	}
elsif 	($action eq "radio_station_stream_upload")	{ &do_radio_station_stream_upload();	}
elsif 	($action eq "radio_station_prompt_list")		{ &do_radio_station_prompt_list();			}
elsif 	($action eq "radio_station_prompt_wait_record")	{ &do_radio_station_prompt_wait_record();	}
elsif 	($action eq "radio_station_prompt_add")			{ &do_radio_station_prompt_add();			}
elsif 	($action eq "radio_station_prompt_del")			{ &do_radio_station_prompt_del();			}
elsif 	($action eq "radio_station_prompt_edit")		{ &do_radio_station_prompt_edit();			}
elsif 	($action eq "radio_station_prompt_play")		{ &do_radio_station_prompt_play();			}
elsif 	($action eq "radio_station_prompt_upload")		{ &do_radio_station_prompt_upload();		}
elsif 	($action eq "do_radio_listen")					{ &do_radio_listen();		}
elsif 	($action eq "radio_station_stream_list_new")	{ &do_radio_station_stream_list_new();		}
elsif 	($action eq "do_stream_updown")					{ &do_stream_updown();		}
elsif 	($action eq "do_stream_delete")					{ &do_stream_delete();		}
elsif 	($action eq "get_stream_search_html")			{ &get_stream_search_html();		}
elsif 	($action eq "do_tag_admin")						{ &do_tag_admin();		}


else												{ &do_radio_station_list();				}
exit;
#=======================================================


#=======================================================
# station actions
#=======================================================
sub do_radio_station_list(){
    #
    #-------------------------------
    # prepare datatable
    #-------------------------------
	$who = clean_str($form{owner});
	$stations_allow_sql = " 1=0 ";
	$stations_notallow_sql = "";
	if ($stations_allow eq "ALL") {
		$stations_allow_sql = " 1=1 ";
	} elsif ($stations_allow ne "") {
		$stations_allow_sql = " radio_data_station.id in ($stations_allow) ";
		$stations_notallow_sql = " radio_data_station.id not in ($stations_allow) ";
	}
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} 			= "SELECT count(*) FROM radio_data_station where $stations_allow_sql ";
	#$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Last change on top";
	#$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_data_station where $stations_allow_sql order by date_last_change desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by DID";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT radio_data_station.id FROM radio_data_station left join radio_data_did on radio_data_station.id=radio_data_did.radio_data_station_id where $stations_allow_sql order by radio_data_did.title asc  limit #LIMIT_1#,#LIMIT_2# ";
	if ($who eq 'others') {
		$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT radio_data_station.id FROM radio_data_station left join radio_data_did on radio_data_station.id=radio_data_did.radio_data_station_id where $stations_notallow_sql order by radio_data_did.title asc  limit #LIMIT_1#,#LIMIT_2# ";
	}

warning($datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql});
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM radio_data_station where $stations_allow_sql order by title limit #LIMIT_1#,#LIMIT_2# ";
	if ($who eq 'others') {
		$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM radio_data_station where $stations_notallow_sql order by title limit #LIMIT_1#,#LIMIT_2# ";

	}

    $datatable{sql}{col_names}			= "id,title,did,extensions,owners"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
#	$datatable{sql}{get_data} 			= "
#		SELECT
#		rs.id,
#		rs.id,
#		rs.title,
#		(select rd.title from radio_data_did as rd where rd.radio_data_station_id=rs.id limit 0,1) as did,
#		(select count(*) from radio_data_station_channel as rs where rs.radio_data_station_id=rs.id and enabled=1) as extensions
#		FROM radio_data_station as rs
#		where rs.id in (#SELECTED_IDS#)
#	";
	$datatable{sql}{get_data} 			= "
		SELECT
		rs.id,
		rs.id,
		rs.title,
		'',
		'',
		''
		FROM radio_data_station as rs
		where rs.id in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	# html values
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_gateways";
	$datatable{html}{form}{data}{1}{name}	= "owner";
    $datatable{html}{form}{data}{1}{value}	= "others" if $who eq 'others';
    $datatable{html}{line_click_link}		= $who eq 'others' ? '' : "$my_url?action=radio_station_view&station_id=#ID#";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "title,did,extensions,owners,action";
    $datatable{html}{col_titles}			= "Phone radio,DID assigned,Extensions count,Owners,Action";
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
	# add extra values at hash before render html
	foreach $id (keys %{$datatable{data}{values}}){
		%hash = &database_select_as_hash("select 1,1,title from radio_data_did where radio_data_station_id='$id' limit 0,1","flag,value");
		$datatable{data}{values}{$id}{did} = ($hash{1}{flag} eq 1) ? "$hash{1}{value}" : "&nbsp;";
		%hash = &database_select_as_hash("select 1,1,count(*) from radio_data_station_channel where radio_data_station_id='$id' and enabled=1 ","flag,value");
		$datatable{data}{values}{$id}{extensions} = ($hash{1}{flag} eq 1) ? "$hash{1}{value}" : "&nbsp;";
		@array = &database_select_as_array("SELECT u.name FROM radio_data_station_owner as l, system_user as u where l.system_user_id=u.id and l.radio_data_station_id='$id' ");
		$datatable{data}{values}{$id}{owners} = join(", ",@array);
		$action = ($who eq 'others' ? "pull" : "push");
		$datatable{data}{values}{$id}{action} = "<a href=\"$my_url?myaction=$action&id=$id\" onclick=\"return confirm('Are you sure to $action this radio');\"> $action </a>";
	}
	$datatable_html = &datatable_get_html(\%datatable);
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Phone radios";

	$tab = $issysadmin ? '' : ($who eq 'others' ? "<a href=\"$my_url\"><font color=\"gray\">My Stations</font></a></a>&nbsp;&nbsp; <a href=\"$my_url?owner=others\">Other Stations</a><br>" : "<a href=\"$my_url\">My Stations</a></a>&nbsp;&nbsp; <a href=\"$my_url?owner=others\"><font color=\"gray\">Other Stations</font></a><br>");
	#$tmp = ($stations_allow eq "ALL") ? "<a href=$my_url?action=radio_station_add>&#187; Add new phone radio</a>" : "";
	$tmp = "<a href=$my_url?action=radio_station_add>&#187; Add new phone radio</a>";

    $t{content}	= qq[
		$tab
    	$datatable_html
    	<br>
		$tmp
    ];
    &template_print("template.html",%t);

}
sub do_radio_station_view(){
	#&cgi_redirect("$my_url?action=radio_station_stream_list&station_id=$form{station_id}");
	#return;
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR : $station_object{status_message}");}
	$station_id = $station_object{data}{key};
	$station_title = $station_object{data}{items}{0}{value};
	#
    #----------------------------------
	# get dids
    #----------------------------------
	$message_dids = "";
	@array = database_select_as_array("select title from radio_data_did where radio_data_station_id='$station_id' order by title  ");
	$tmp = @array;
	if ($tmp <= 0) {
		$message_dids = "";
	} else {
		$message_dids = "( ".join(", ",@array)." )";
	}
	#
    #----------------------------------
	# get owners
    #----------------------------------
	$message_owners = "";
	@array = &database_select_as_array("SELECT u.name FROM radio_data_station_owner as l, system_user as u where l.system_user_id=u.id and l.radio_data_station_id='$station_id' ");
	$tmp = @array;
	if ($tmp <= 0) {
		$message_owners = "";
	} else {
		$message_owners = "($tmp owners) ";
	}
	#
    #----------------------------------
	# get extensions info
    #----------------------------------
	%hash = &database_select_as_hash("select 1,1,count(*) from radio_data_station_channel where radio_data_station_id='$station_id' and enabled=1 ","flag,value");
	$extensions_count_total = ($hash{1}{flag} eq 1) ? $hash{1}{value} : 0;
	%hash = &database_select_as_hash("select 1,1,count(*) from radio_data_station_channel where radio_data_station_id='$station_id' and enabled=1 and extension in (1,2,3,4,5,6,7,8,9) ","flag,value");
	$extensions_count_favorites = ($hash{1}{flag} eq 1) ? $hash{1}{value} : 0;
	#
    #----------------------------------
	# get custom prompts
    #----------------------------------
	%hash = &database_select_as_hash("select 1,1,count(*),sum(prompt_size_bytes) from radio_data_station_prompt where radio_data_station_id='$station_id' ","flag,value1,value2");
	$prompt_count		= ($hash{1}{flag} eq 1) ? $hash{1}{value1} : 0;
	$prompt_kbytes		= ($hash{1}{flag} eq 1) ? ($hash{1}{value2}/1024) : 0;
	$prompt_percentage	= (100*( $prompt_kbytes/(1024) ));
	$prompt_percentage	= ($prompt_percentage < 1) ? &format_number($prompt_percentage,2) : &format_number($prompt_percentage,0);
	$prompt_kbytes		= ($prompt_kbytes < 5) ? &format_number($prompt_kbytes,2) : &format_number($prompt_kbytes,0);
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" phone radio";
	$edit_button = "";
	if (&active_user_permission_get("radio.data.access") eq 1) {
		$edit_button = "<button type=button onclick=\"window.location='$my_url?action=radio_station_edit_simple&station_id=$station_id'\">Edit</button>";
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		$edit_button = "<button type=button onclick=\"window.location='$my_url?action=radio_station_edit&station_id=$station_id'\">Edit</button>";
	}
	$hide_custom_prompts = (&active_user_permission_get("radio.data.prompt.access") eq 1) ? "" : "style=display:none;";

    $t{content}	= qq[

<div id="navigation_tab">
<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
<a href="$my_url?action=radio_station_view&station_id=$station_id" class=selected>Overview</a>
<a href="$my_url?action=radio_station_edit&station_id=$station_id" >Settings</a>
<a href="$my_url?action=radio_station_stream_list_new&station_id=$station_id" >Content sources</a>
<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Custom prompts</a>
</div>


Show phone radio overview here in this page. <br>
Things like balance, notes and other things.<br>
Users with no write permission can seee this tab but not others<br>

    ];
    &template_print("template.html",%t);

}
sub do_radio_station_add(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	unless (&active_user_permission_get("radio.data.access") eq 1) {adm_error("no permission"); exit;}
	#
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_radio_station;
	&dataitem_initialize(\%my_dataitem);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "TA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_list";
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_list";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_add";
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
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Add new phone radio";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);

}
sub do_radio_station_del(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	unless (&active_user_permission_get("radio.data.access") eq 2) {adm_error("no permission"); exit;}
    #
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_radio_station;
	&dataitem_initialize(\%my_dataitem);
	$my_dataitem{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "SD";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_edit&station_id=$my_dataitem{data}{key}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_list";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete '$my_dataitem{data}{items}{0}{value}' radio station?</b> This will also delete all connections to radio station. This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_del";
    $form_settings{hidden_elements}{2}{name}	= "station_id";
    $form_settings{hidden_elements}{2}{value}	= $my_dataitem{data}{key};
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
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Delete phone radio";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);

}
sub do_radio_station_edit(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
    $edit_full = 0;
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	    $edit_full = 1;
	} else {
		adm_error("no permission");
		return;
	}
    #
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%my_dataitem = ();
	if ($edit_full eq 1) {
		%{$my_dataitem{config}} = %dataitemconfig_radio_station;
	} else {
		%{$my_dataitem{config}} = %dataitemconfig_radio_station_simple;
	}
	$my_dataitem{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%my_dataitem);
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
	$station_id = $form{station_id};
	$station_title = "Need solve this";
	$station_title = $my_dataitem{data}{items}{0}{value};
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{click_id_prefix}		= "RGE";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_view&station_id=$my_dataitem{data}{key}";
	if ($edit_full eq 1) {
	    $form_settings{url_button_delete}= "$my_url?action=radio_station_del&station_id=$my_dataitem{data}{key}";
	}
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_view&station_id=$my_dataitem{data}{key}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_edit";
    $form_settings{hidden_elements}{2}{name}	= "station_id";
    $form_settings{hidden_elements}{2}{value}	= $my_dataitem{data}{key};
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
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit phone radio";
    $t{title}	= "\"$station_title\" phone radio";
    $t{content}		.= qq[

<div id="navigation_tab">
<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
<a href="$my_url?action=radio_station_view&station_id=$station_id">Overview</a>
<a href="$my_url?action=radio_station_edit&station_id=$station_id" class=selected>Settings</a>
<a href="$my_url?action=radio_station_stream_lis_newt&station_id=$station_id" >Content sources</a>
<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Custom prompts</a>
</div>


	<fieldset style="width:400px;">$html_form</fieldset>
    ];
	&template_print("template.html",%t);
}
sub do_radio_station_stream_list(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR : $station_object{status_message}");}
	$station_id 	= $station_object{data}{key};
	$station_title	= $station_object{data}{items}{0}{value};
    #
    #-------------------------------
    # prepare datatable
    #-------------------------------
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM radio_data_station_channel where radio_data_station_id=$station_id and enabled=1 ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by extension";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_data_station_channel where radio_data_station_id=$station_id and enabled=1 order by ABS(extension) limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Last change on top";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM radio_data_station_channel where radio_data_station_id=$station_id and enabled=1 order by date_last_change desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{2}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{2}{sql} 	= "SELECT id FROM radio_data_station_channel where radio_data_station_id=$station_id and enabled=1 order by title limit #LIMIT_1#,#LIMIT_2# ";
    $datatable{sql}{col_names}			= "id,extension,title,stream_type,stream_url"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT
		id,
		id,
		extension,
		title,
		stream_type,
		stream_url
		FROM radio_data_station_channel
		where id in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	# html values
    #$datatable{html}{title}				= "'".$station_object{data}{items}{0}{value}."' extensions";
    $datatable{html}{col_names}				= "extension,title,stream_type,stream_url";
    $datatable{html}{col_titles}			= "Extension,Title,Type,URL";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_station_stream_list";
    $datatable{html}{form}{data}{1}{name}	= "station_id";
    $datatable{html}{form}{data}{1}{value}	= "$station_id";
    $datatable{html}{line_click_link}		= "$my_url?action=radio_station_stream_edit&stream_id=#ID#";

	$datatable{html}{cols}{0}{data_col_name}			= "extension";
    $datatable{html}{cols}{0}{title}					= "Extension";
	$datatable{html}{cols}{1}{data_col_name}			= "title";
    $datatable{html}{cols}{1}{title}					= "Title";
	$datatable{html}{cols}{2}{data_col_name}			= "stream_type";
    $datatable{html}{cols}{2}{title}					= "Type";
	$datatable{html}{cols}{3}{data_col_name}			= "stream_url";
    $datatable{html}{cols}{3}{title}					= "URL (* click to listen, not work on mac)";
    $datatable{html}{cols}{3}{url}			= "javascript: play_radio('#ID#');";

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
    $station_extensions_count = $datatable{data}{count};
    $station_extensions_count++;
    $station_extensions_count--;
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" phone radio";
    $t{content}	= qq[
<script>
function play_radio(id) {
	window.open('$my_url?action=do_radio_listen&id=' + id,				'Listen','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');

};
</script>

<div id="navigation_tab">
<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
<a href="$my_url?action=radio_station_view&station_id=$station_id" >Overview</a>
<a href="$my_url?action=radio_station_edit&station_id=$station_id" >Settings</a>
<a href="$my_url?action=radio_station_stream_list_new&station_id=$station_id" class=selected>Content sources</a>
<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Custom prompts</a>
</div>


    	$datatable_html
    	<br>
    	<a href=$my_url?action=radio_station_stream_add&station_id=$station_id>&#187; Add new content source</a><br>
    	<a href=$my_url?action=radio_station_stream_upload&station_id=$station_id>&#187; Import/export content sources</a><br>

    ];
    &template_print("template.html",%t);

}

sub do_radio_listen () {
	$id  = clean_int($form{'id'});
	%radio = database_select_as_hash("select id,stream_url,title from radio_data_station_channel where id='$id'", 'url,title');
	$url = $radio{$id}{url};

	cgi_hearder_html();

print qq[
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<title>$radio{$id}{title} -- $url</title>
<script>
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

</script>
</head>

<body onload="showPlayer('player', '$url')">
<center>

<div id='player'></div>


</center>
</body>
</html>
];

	}


sub do_radio_station_stream_list_new(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}

	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR : $station_object{status_message}");}
	$station_id 	= $station_object{data}{key};
	$station_title	= $station_object{data}{items}{0}{value};
    #
	$sql 			= "SELECT id,extension,title,stream_type,stream_url FROM radio_data_station_channel where radio_data_station_id='$station_id' and enabled = '1' order by --extension asc";
	warn $sql;
	%stream			= database_select($sql, "id,extension,title,type,url");
	$datatable_html = '';

	for (0..$stream{ROWS}-1) {
		$url = "$my_url?action=radio_station_stream_edit_new&stream_id=$stream{DATA}{$_}{id}";
		$datatable_html .= "<tr><td><a href='$my_url?action=do_stream_updown&mode=0&streamid=$stream{DATA}{$_}{id}&extension=$stream{DATA}{$_}{extension}&stationid=$station_id' title='Up it'>" .
						   "<img src='up.jpg'/></a> &nbsp; <a href='$my_url?action=do_stream_updown&mode=1&streamid=$stream{DATA}{$_}{id}&extension=$stream{DATA}{$_}{extension}&stationid=$station_id' title='Down it'><img src='down.jpg'/></a></td><td><a href='$url'>$stream{DATA}{$_}{extension}</a></td><td><a href='$url'>$stream{DATA}{$_}{title}</td>" .
						   "</a><td>PUBLIC</td><td><a href='javascript: play_radio(\"$stream{DATA}{$_}{id}\");' title='click to listen it'>$stream{DATA}{$_}{url}</a></td>" .
						   "<td><a href='#' title='Click to upload' >Not Configured</a></td><td><a href='$my_url?action=do_stream_delete&streamid=$stream{DATA}{$_}{id}&extension=$stream{DATA}{$_}{extension}&stationid=$station_id' onclick='return confirm(\"Are u sure to Delete it\");'>delete</a></td></tr>\n";
	}

    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" phone radio";
    $t{content}	= qq[
<script>
function play_radio(id) {
	window.open('$my_url?action=do_radio_listen&id=' + id,				'Listen','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');

};
</script>

<div id="navigation_tab">
<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
<a href="$my_url?action=radio_station_view&station_id=$station_id" >Overview</a>
<a href="$my_url?action=radio_station_edit&station_id=$station_id" >Settings</a>
<a href="$my_url?action=radio_station_stream_list_new&station_id=$station_id" class=selected>Content sources</a>
<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Custom prompts</a>
</div>
<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Justify<br> Extension</td>
		<td>Extension</td>
		<td>Title</td>
		<td>Type</td>
		<td>Url</td>
		<td>Prompt</td>
		<td>Delete</td>
		</tr>
	</thead>
	<tbody>
		$datatable_html
	</tbody>
</table>
    	<br>
    	<a href=$my_url?action=radio_station_stream_add_new&station_id=$station_id>&#187; Add new content source</a><br>

    ];
#    	<a href=$my_url?action=radio_station_stream_upload&station_id=$station_id>&#187; Import/export content sources</a><br>

    &template_print("template.html",%t);

}

sub do_radio_station_stream_add(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR: $station_object{status_message}");}
	$station_id = $station_object{data}{key};
    #
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%stream_object = ();
	%{$stream_object{config}} = %dataitemconfig_radio_station_stream;
	&dataitem_initialize(\%stream_object);
	# inject station_id into this object
	$stream_object{data}{items}{0}{value} = $station_id;
	# inject radio name
	$stream_object{data}{items}{1}{value} = $station_object{data}{items}{0}{value};
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    #$form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "TA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_stream_list&station_id=$station_id&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_stream_list&station_id=$station_id";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_stream_add";
    $form_settings{hidden_elements}{2}{name}	= "station_id";
    $form_settings{hidden_elements}{2}{value}	= "$station_id";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_addform_process(\%stream_object,\%form_settings,\%form);
	$html_form = &dataitem_web_addform_gethtml(\%stream_object,\%form_settings,\%form);
	if ($form_settings{status_ok} eq 1) {
		&radio_data_station_stream_update_radio_data_provider_id()
		&cgi_redirect($form_settings{url_form_ok});
		exit;
	}
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Add new phone radio content";
    $t{content}		.= qq[
<script>
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
	var url = document.getElementsByName("stream_url")[0].value;
	if (!url) {
		alert("Warning: Content Source Url is null");
		return false;
	}
	showPlayer('player', url);
}
</script>

<input type="submit" name="listen" value="listen" onclick="listen();return false;"/>
<div id='player'></div>


	<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
sub do_radio_station_stream_edit(){
    #
    #----------------------------------
    # get and check stream
    #----------------------------------
	%stream_object = ();
	%{$stream_object{config}} = %dataitemconfig_radio_station_stream;
	$stream_object{data}{key}  = &clean_int(substr($form{stream_id},0,100));;
	&dataitem_initialize(\%stream_object);
	unless (&dataitem_get(\%stream_object)) {adm_error("ERROR: $stream_object{status_message}");}
	$station_id 		= $stream_object{data}{items}{0}{value};
	$stream_id 			= $stream_object{data}{key};
	$old_stream_type	= $stream_object{data}{items}{4}{value};
	$old_stream_url		= $stream_object{data}{items}{5}{value};
    #
    #----------------------------------
    # get and check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = $station_id;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR: $station_object{status_message}");}
	# inject radio name
	$stream_object{data}{items}{1}{value} = $station_object{data}{items}{0}{value};
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$station_id,") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_object = ();
    $form_object{flags}				= "";
    $form_object{mode}					= "EDIT";
    $form_object{click_id_prefix}		= "RGE";
    $form_object{url_button_cancel}		= "$my_url?action=radio_station_stream_list&station_id=$station_id&page=$form{page}";
    $form_object{url_button_delete}		= "$my_url?action=radio_station_stream_del&stream_id=$stream_id&page=$form{page}";
    $form_object{url_form_ok}			= "$my_url?action=radio_station_stream_list&station_id=$station_id&page=$form{page}";
    $form_object{url_form_action}		= "$my_url";
    $form_object{hidden_elements}{0}{name}	= "page";
    $form_object{hidden_elements}{0}{value}	= "$form{page}";
    $form_object{hidden_elements}{1}{name}	= "action";
    $form_object{hidden_elements}{1}{value}	= "radio_station_stream_edit";
    $form_object{hidden_elements}{2}{name}	= "stream_id";
    $form_object{hidden_elements}{2}{value}	= $stream_object{data}{key};
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_editform_process(\%stream_object,\%form_object,\%form);
	$html_form = &dataitem_web_editform_gethtml(\%stream_object,\%form_object,\%form);
    #
    #----------------------------------
    # do the zenofon UID hack
    #----------------------------------
    # what we have to do is check if we had some change at stream data (type or url)
    # if yes, we need delete old dataitem and add new one.
    # This ensure that different streams always get a new unique ID
    # remember remove redirct_if_ok option in form settings above so code bellow can run
    #----------------------------------
	if ($form_object{status_ok} eq 1) {
		$new_stream_type	= $stream_object{data}{items}{4}{value};
		$new_stream_url		= $stream_object{data}{items}{5}{value};
		if ( ($new_stream_type ne $old_stream_type) || ($new_stream_url ne $old_stream_url) ) {
			# create new dataitem
			%new_stream_object = ();
			%{$new_stream_object{config}} = %dataitemconfig_radio_station_stream;
			&dataitem_initialize(\%new_stream_object);
			# inject data
			foreach $i (keys %{$stream_object{config}{items}}) {
				$new_stream_object{data}{items}{$i}{value} = $stream_object{data}{items}{$i}{value};
			}
			# add new dataitem
			$tmps1 = &dataitem_add(\%new_stream_object);
			# delete actual dataitem
			$tmps2 = &dataitem_del(\%stream_object);
		}
		&radio_data_station_stream_update_radio_data_provider_id()
		&cgi_redirect($form_object{url_form_ok});
		exit;
	}
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit phone radio content";
    $t{content}		.= qq[
<script>
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
	var url = document.getElementsByName("stream_url")[0].value;
	if (!url) {
		alert("Warning: Content Source Url is null");
		return false;
	}
	showPlayer('player', url);
}
</script>

<input type="submit" name="listen" value="listen" onclick="listen();return false;"/> <font color="red">(** stream testing only works on Windows)</font>
<div id='player'></div>

<fieldset style="width:350px;">$html_form</fieldset><br>];
#$tmp .= "<pre>";
#$tmp .= "ADD=$tmps1\n";
#$tmp .= "DEL=$tmps2\n";
#$tmp .= "[$old_stream_type] = [$new_stream_type]\n";
#$tmp .= "[$old_stream_url] = [$new_stream_url]\n";
#$tmp .= "\n";
#$tmp .= "STATION OBJECT\n".Dumper(%station_object)."\n\n";
#$tmp .= "STREAM OBJECT\n".Dumper(%stream_object)."\n\n";
#$tmp .= "NEW STREAM OBJECT\n".Dumper(%new_stream_object)."\n\n";
#$tmp .= "FORM OBJECT\n".Dumper(%form_object)."\n\n";
#$tmp .= "FORM USER DATA\n".Dumper(%form)."\n\n";
#$tmp .= "<pre>";
#$t{content} .= $tmp;
	&template_print("template.html",%t);
}

sub do_radio_station_stream_add_new() {
	do_radio_station_stream_edit_new(1);
};

sub do_radio_station_stream_edit_new(){
	($mode) = @_;
    #
    #----------------------------------
    # get and check stream
    #----------------------------------
	if ($form{subaction}) {
		do_stream_admin();
		exit 0;
	}

	%stream_object = ();
	%{$stream_object{config}} = %dataitemconfig_radio_station_stream;
	$stream_object{data}{key}  = &clean_int(substr($form{stream_id},0,100));;
	if (!$mode) {
		&dataitem_initialize(\%stream_object);
		unless (&dataitem_get(\%stream_object)) {adm_error("ERROR: $stream_object{status_message}");}
		#warn Dumper(\%stream_object);
	}
	$taglist		= get_tag_list();

	$station_id 	= $stream_object{data}{items}{0}{value} || clean_int($form{station_id});
	$stream_id 		= $stream_object{data}{key};

	$stream_type	= $stream_object{data}{items}{4}{value};
	$stream_permission	= $stream_object{data}{items}{6}{value};

	$stream_url		= $stream_object{data}{items}{5}{value};
    $stream_title	= $stream_object{data}{items}{3}{value};
    $stream_extension	= $stream_object{data}{items}{2}{value};

    $stream_type_option  = "<option value=''>&nbsp;</option>" .
						  "<option  value='SHOUTCAST' " .
						  ($stream_type eq 'SHOUTCAST' ? 'SELECTED' : '') .
						  ">Shoutcast stream</option><option  value='MMS' " .
						  ($stream_type eq 'MMS' ? 'SELECTED' : '') .
						  ">MMS stream </option><option  value='MP3' " .
						  ($stream_type eq 'MP3' ? 'SELECTED' : '') .
						  ">Mp3 file </option>";
    $stream_permission_option  = "<option  value='public' " .
						  ($stream_permission eq 'public' ? 'SELECTED' : '') .
						  ">public</option><option  value='private' " .
						  ($stream_permission eq 'private' ? 'SELECTED' : '') .
						  ">private</option>";


	$extensionlist		= "<select name='newextension'>";
	%hash = database_select_as_hash("select 1,max(--extension) from radio_data_station_channel where radio_data_station_id='$station_id' and enabled='1'", 'max');
	$max  = $hash{1}{max};
	$extensionlist .= "<option value='9999' selected>last (**default)</option>" .
						  "<option value='1'" .  ($stream_extension eq '1' ? 'selected' : '') . ">first</first>";

	for (2..$max) {
		$extensionlist .= "<option value='$_' " . ($stream_extension eq $_ ? 'selected' : '') . ">$_</option>";
	}

	$extensionlist .= "</select>";

    #----------------------------------
	$station_id  ||= $form{station_id};
	warn "select id, title from radio_data_station where id='$station_id'";
	%hash = database_select_as_hash("select id, title from radio_data_station where id='$station_id'", 'title');
	$radio_name = $hash{$station_id}{title};

	%t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= ($mode ? "Add phone radio content" : "Edit phone radio content");
	$initialtag = 'input additional tag here ...';

    $t{content}		.= qq[
<div id="content">
<script>
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
	var url = document.getElementsByName("stream_url")[0].value;
	if (!url) {
		alert("Warning: Content Source Url is null");
		return false;
	}
	showPlayer('player', url);
}

function do_search() {
	\$('#content').toggle();
	\$('#streamlist').toggle();
	\$('#searchtip').toggle();
	\$('#searchtip2').toggle();

}

function do_add(streamid,extension,radioname,title,url) {
	\$('#content').show();
	\$('#streamlist').hide();
	\$('#searchtip').html("Search Radio Stream");
	//\$('#radio_name').val(radioname);
	\$('#stream_title').val(title);
	\$('#stream_url').val(url);
	\$('#searchtip').toggle();
	\$('#searchtip2').toggle();

}


function do_stream_search() {
	var keyword   = '';
	var initialtag = '$initialtag';
	var othertag  = \$('#othertag').val();
	var addtag    = 0;
	if (othertag && othertag != initialtag ) {
		addtag = confirm('Do you wanna store the tag "' + othertag + '"');
	}

	\$('#searchstreambody').ajaxStart(function(){
		\$('#searchstreambody').html('<tr><td colspan=4 align="center"><img src="demo_wait.gif"/></td><tr>');
	});


	\$("[name='tag']").each(function(){
		if(\$(this).attr("checked"))
		{
		  keyword += \$(this).val() + ',';

		}
	});


	\$.get('$my_url', {action: "get_stream_search_html", keyword: keyword, addtag: addtag, othertag: othertag}, function(data) {
			\$('#searchstreambody').html(data);
	});

}

function play_radio(id) {
	window.open('$my_url?action=do_radio_listen&id=' + id, 'Listen','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');

};

</script>

<input type="submit" name="listen" value="listen" onclick="listen();return false;"/> <font color="red">(** stream testing only works on Windows)</font>
<div id='player'></div>

<fieldset style="width:350px;">
<form class=dataitemform  action='radio.stations.cgi' method=post>
   		<table class=clear border=0 colspan=0 cellpadding=2 cellspacing=0 >
		<input type=hidden name='action' value='$action'>
		<input type=hidden name='subaction' value='submit'>

			    	<tr>

			    	<td valign=top>Radio</td>
			    	<td valign=top><input  read-only disabled  name="radio_name" id="radio_name" value='$radio_name' > </td>
			    	</tr>



			    	<tr>
			    	<td valign=top>Title</td>
			    	<td valign=top><input  name="stream_title" id="stream_title" value='$stream_title' > </td>
			    	</tr>

		    	<tr>
		    		<td valign=top>Content source type</td>
		    		<td valign=top>

		    			<select  name="stream_type" id="stream_type" style='' >
		    			$stream_type_option
		    			</select>

					</td>
		    	</tr>

				<tr>
		    		<td valign=top>Content permission type</td>
		    		<td valign=top>

		    			<select  name="stream_permission" id="stream_permission" style='' >
		    			$stream_permission_option
		    			</select>

					</td>
		    	</tr>


			    	<tr>
			    	<td valign=top>Content source URL</td>
			    	<td valign=top><input  name="stream_url" id="stream_url" value='$stream_url' > </td>
			    	</tr>
					<tr>
					<td valign=top>Extension</td>
			    	<td valign=top>$extensionlist</td>
			    	</tr>

		</table>
    	<br>
		<input type=hidden name='stream_id' value='$stream_id'>
		<input type=hidden name='station_id' value='$station_id'>
		<input type=hidden name='oldextension' value='$stream_extension'>
      	<button class=cancel type=button onclick="window.location='radio.stations.cgi?action=radio_station_stream_list_new&station_id=$station_id&page='">Cancel</button>

    	<button class=delete type=button onclick="window.location='radio.stations.cgi?action=do_stream_delete&streamid=$stream_id&stationid=$station_id'">Delete</button>
    	<button class=save type=submit>Save</button>
    	<input type=hidden name='page' value=''>
    </form>
</fieldset><br>
</div>
<a href="#" onclick="do_search(); return false;"><span id="searchtip">Search Radio Stream</span><span id="searchtip2" style="display: none">Return</span></a>

		<div id="streamlist" style="display: none">
		<a href="$my_url?action=do_tag_admin" title="click to manage your tags" target=_blank>TAGS</a>:
		<table>
		$taglist
		  <tr><td colspan=6>
			  <input type="text" name="othertag" id="othertag" size=30 value="$initialtag" />
			  <input type="submit" name="subaction" value="go" onclick="do_stream_search(); return false"/>
			  </td>
		   </tr>
		</table>


<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
	<tr><td>Add To <br>Your List</td><td  >Station</td><td  >Stream Title</td><td  >Stream URL <br>(* click to listen, not work on mac)</td></tr></thead>
	<tbody id="searchstreambody">
	</tbody>
</table>
</div>];

#$tmp .= "<pre>";
#$tmp .= "ADD=$tmps1\n";
#$tmp .= "DEL=$tmps2\n";
#$tmp .= "[$old_stream_type] = [$new_stream_type]\n";
#$tmp .= "[$old_stream_url] = [$new_stream_url]\n";
#$tmp .= "\n";
#$tmp .= "STATION OBJECT\n".Dumper(%station_object)."\n\n";
#$tmp .= "STREAM OBJECT\n".Dumper(%stream_object)."\n\n";
#$tmp .= "NEW STREAM OBJECT\n".Dumper(%new_stream_object)."\n\n";
#$tmp .= "FORM OBJECT\n".Dumper(%form_object)."\n\n";
#$tmp .= "FORM USER DATA\n".Dumper(%form)."\n\n";
#$tmp .= "<pre>";
#$t{content} .= $tmp;
	&template_print("template.html",%t);
}

sub do_radio_station_stream_del(){
    #
    #----------------------------------
    # get and check stream
    #----------------------------------
	%stream_object = ();
	%{$stream_object{config}} = %dataitemconfig_radio_station_stream;
	$stream_object{data}{key}  = &clean_int(substr($form{stream_id},0,100));;
	&dataitem_initialize(\%stream_object);
	unless (&dataitem_get(\%stream_object)) {adm_error("ERROR: $stream_object{status_message}");}
	$station_id = $stream_object{data}{items}{0}{value};
	$stream_id = $stream_object{data}{key};
    #
    #----------------------------------
    # get and check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = $station_id;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR: $station_object{status_message}");}
	# inject radio name
	$stream_object{data}{items}{1}{value} = $station_object{data}{items}{0}{value};
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$station_id,") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    #$form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "SD";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_stream_edit&stream_id=$stream_id&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_stream_list&station_id=$station_id&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete '$stream_object{data}{items}{3}{value}' content</b> from '$stream_object{data}{items}{1}{value}' radio ? This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_stream_del";
    $form_settings{hidden_elements}{2}{name}	= "stream_id";
    $form_settings{hidden_elements}{2}{value}	= $stream_id;
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_deleteform_process(\%stream_object,\%form_settings,\%form);
	$html_form = &dataitem_web_deleteform_gethtml(\%stream_object,\%form_settings,\%form);
	if ($form_settings{status_ok} eq 1) {
		&radio_data_station_stream_update_radio_data_provider_id()
		&cgi_redirect($form_settings{url_form_ok});
		exit;
	}
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Delete phone radio content";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
#$tmp = "<pre>";
#$tmp .= "STATION OBJECT\n".Dumper(%station_object)."\n\n";
#$tmp .= "STREAM OBJECT\n".Dumper(%stream_object)."\n\n";
#$tmp .= "FORM SETTINGS\n".Dumper(%form_settings)."\n\n";
#$tmp .= "FORM\n".Dumper(%form)."\n\n";
#$tmp .= "<pre>";
#$t{content} .= $tmp;
	&template_print("template.html",%t);
}
sub do_radio_station_stream_download(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR : $station_object{status_message}");}
	$station_id 		= $station_object{data}{key};
	$station_title 		= $station_object{data}{items}{0}{value};
	$station_title_clean= &clean_str($station_title,"MINIMAL"," ");
	#
    #----------------------------------
	# start page
    #----------------------------------
    print "Pragma: public\n";
    print "Expires: 0\n";
    print "Cache-Control: must-revalidate, post-check=0, pre-check=0\n";
    print "Content-type: application/octet-stream\n";
    print "Content-Disposition: attachment; filename=\"Extensions for radio $station_title_clean.csv\"\n";
    print "Content-Description: File Transfert\n";
    print "\n";
    print "extension,";
    print "stream_type,";
    print "stream_url,";
    print "title\n";
	#
    #----------------------------------
	# query and print
    #----------------------------------
	$sql = "SELECT id,extension,stream_type,stream_url,title FROM radio_data_station_channel where radio_data_station_id='$station_id' ";
    %hash = database_select_as_hash($sql,"extension,stream_type,stream_url,title");
    $tmp0="";
    $tmps=" ";
    $tmp1="\"";
    $tmp2="\r";
    $tmp3="\n";
    $tmp4="\,";
	foreach $id (sort{$hash{$a}{extension} <=> $hash{$b}{extension}} keys %hash){
		$line = "";
		$tmp=$hash{$id}{extension};		$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .= "\"$tmp\",";
		$tmp=$hash{$id}{stream_type};	$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .= "\"$tmp\",";
		$tmp=$hash{$id}{stream_url};	$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .= "\"$tmp\",";
		$tmp=$hash{$id}{title};			$tmp =~ s/$tmp1/$tmp0/eg; $tmp =~ s/$tmp2/$tmp0/eg; $tmp =~ s/$tmp3/$tmps/eg; $tmp =~ s/$tmp4/$tmp0/eg;	$line .= "\"$tmp\"\n";
		print $line;
    }
}
sub do_radio_station_stream_upload(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR : $station_object{status_message}");}
	$station_id 		= $station_object{data}{key};
	$station_title 		= $station_object{data}{items}{0}{value};
	$station_title_clean= &clean_str($station_title,"MINIMAL"," ");
	#
    #----------------------------------
	# read upload if we have save_id
    #----------------------------------
    $error_message = "";
    $ok_message = "";
    if ($form{save_id} eq 1) {
    	#
    	# save radio_data_station_stream_ids in a cache,
    	# so maybe we can re-use after delete all and
    	# reinsert all from csv file
		$id_cache = ();
		$sql = "SELECT id,extension,stream_type,stream_url,title FROM radio_data_station_channel where radio_data_station_id='$station_id' ";
    	%hash = database_select_as_hash($sql,"extension,stream_type,stream_url,title");
		foreach $id (keys %hash){
			if ($hash{$id}{extension} eq "") {next}
			$id_cache_key = $station_id."|".$hash{$id}{extension}."|".$hash{$id}{stream_type}."|".$hash{$id}{stream_url};
			$id_cache{$id_cache_key} = $id;
		}
	    #
	    # write upload data into temp file. and create statistic data
	    $temp_file = "/tmp/.upload.extensions.".time.".tmp";
	    $filehandle = $cgi->param("FileUpload");
	    open(LOCAL, ">$temp_file");
	    while($bytesread=read($filehandle,$buffer,1024)) { print LOCAL $buffer; }
	    close(LOCAL);
	    #
	    # check CSV file header
	    open(LOCAL,$temp_file);
	    $line = <LOCAL>;
	    $line = &csvtools_line_join_values(&csvtools_line_split_values($line));
	    if ("\L$line" ne "extension,stream_type,stream_url,title") { $error_message = "Incorrect CSV file. Bad header. Try to download file, edit and upload"; }
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
				%csv_line = ();
				$csv_line{extension}	= &clean_int(@data[0]);
				$csv_line{stream_type}	= &clean_str(@data[1]," /&|?-_–(\@)-,=+;.<>[]:?<>","MINIMAL");
				$csv_line{stream_url}	= &clean_str(@data[2]," /&|?-_–(\@)-,=+;.<>[]:?<>","MINIMAL");
				$csv_line{title}		= &clean_str(@data[3]," /&|?-_–(\@)-,=+;.<>[]:?<>","MINIMAL");
				$csv_line{stream_type}	= "\U$csv_line{stream_type}";
				#
				# check line values before edit
				$line_error = "";
				if (index("|SHOUTCAST|MMS|MP3|","|$csv_line{stream_type}|") eq -1)	{ $line_error .= "Bad stream_type ($csv_line{stream_type}). ";		}
				if ($csv_line{stream_url} eq "")	 								{ $line_error .= "Bad stream_url. "; 		}
				if ($line_error ne "") {
					$error_count++;
					#@error_messages=(@error_messages,"$line_error at line $line_count <br><br>[$line]<br>[".@values."]<br>[".join("|",@values)."]<br><br><br>");
					@error_messages=(@error_messages,"$line_error at line $line_count.<br>");
					$stats{line_error_bad_CSV_data}++;
					next;
				}
				#
				# if no error, prepare sql
				$id_cache_key = $station_id."|".$csv_line{extension}."|".$csv_line{stream_type}."|".$csv_line{stream_url};
				if (exists($id_cache{$id_cache_key})) {
					# we have id and no change in stream, lets reuse the id
					$sql = "
						insert into radio_data_station_channel
						(id,   radio_data_station_id, extension, stream_type, stream_url, title) values
						('%s', '%s',                  '%s',      '%s',        '%s',       '%s' )
					";
					$sql = &database_scape_sql($sql,$id_cache{$id_cache_key},$station_id,$csv_line{extension},$csv_line{stream_type},$csv_line{stream_url},$csv_line{title});
				} else {
					# we dont remember one old id for this stream, lets allow database create a new one
					$sql = "
						insert into radio_data_station_channel
						(radio_data_station_id, extension, stream_type, stream_url, title) values
						('%s',                  '%s',      '%s',        '%s',       '%s' )
					";
					$sql = &database_scape_sql($sql,$station_id,$csv_line{extension},$csv_line{stream_type},$csv_line{stream_url},$csv_line{title});
				}
				@sql_to_run = (@sql_to_run ,$sql);
				$stats{line_edit}++;
			}
			#
			# if data and no errors, lets apply
			if ( ($line_count>0) && ($error_count eq 0) ) {
				&database_do("delete FROM radio_data_station_channel where radio_data_station_id='$station_id'");
				foreach $sql (@sql_to_run) { &database_do($sql); }
#foreach $sql (@sql_to_run) { $ney .= "[$sql]<br>"; }
				#&radio_asterisk_musiconhold_update();
			}
			#
			# prepare user message
			if ( ($line_count>0) && ($error_count eq 0) ) {
			    $ok_message = "<h1><b>Upload OK</b></h1> ";
			    $ok_message .= "We import ". ($line_count+ 0) . " content sources for radio station '$station_title' ($station_id).<br><br> ";
		    	$ok_message .= "<a href=$my_url?action=radio_station_stream_list&station_id=$station_id>&#187; Back to contents list</a><br>";
			    #$ok_message .= "<br><b>Statistics:</b><br>";
			    #$ok_message .= "Total lines read = ". ($line_count+ 0) . "<br>";
			    #$ok_message .= "lines change data = ". ($stats{line_edit}+ 0) . "<br>";
			    #$ok_message .= "Lines do not change data = ". ($stats{line_skip_no_change}+ 0) . "<br>";
			    #$ok_message .= "Lines error = ". ($stats{line_skip_no_add} + $stats{line_skip_no_extension} + $stats{line_skip_bad_extension_format} + $stats{line_skip_cannot_read_station} + 0) . "<br>";
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
    %t = &menu_permissions_get_as_template();
    $error_message	= ($error_message eq "") 	? "" : "<div class=alert_box><div class=alert_box_inside>$error_message </div></div>";
    $ok_message 	= ($ok_message eq "") 		? "" : "<div class=alert_box><div class=alert_box_inside style='background-image:url(/design/icons/tick-circle.png);'>$ok_message </div></div>";
    $t{my_url}	= $my_url;
    $t{title}	= "Import/export phone radio content";
    $t{content}		.= qq[
	<div class=clear style=width:300px;>

		<h1>Downlod</h1>
		Download a CSV file wih all radio content sources and edit the way you want.
		<br>
    	<a href=$my_url?action=radio_station_stream_download&station_id=$station_id>&#187; Download data as CSV file</a><br>
    	<a href=$my_url?action=radio_station_stream_list&station_id=$station_id>&#187; Back to content list</a><br>
		<br>

		<h1>Upload</h1>
		Upload CSV file with radio content sources that you edited above
		<br>
		<form action=$my_url method=post enctype="multipart/form-data" onsubmit="modal_loadingblock();">
			<input disabled read-only value="$station_title">
			<input name=FileUpload type=file><br>
			<input type=hidden name=action value=radio_station_stream_upload>
			<input type=hidden name=station_id value=$station_id>
			<input type=hidden name=save_id value=1>
			<button type=submit class="button button_positive " >Upload CSV file</button>
		</form>
		<br>
		$error_message
		$ok_message

	</div>

	];
	&template_print("template.html",%t);
}
sub do_radio_station_prompt_wait_record(){
	print "content-type: text/html\n\n";
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		return;
	}
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {return;}
	$station_id 	= $station_object{data}{key};
	$station_title	= $station_object{data}{items}{0}{value};
    #
    #----------------------------------
    # Get prompts wait for record
    #----------------------------------
    $html_need_record = "";
    $html_refresh = "";
    $sql= "
		SELECT id,title,phone_record_pin
		FROM radio_data_station_prompt
		where phone_record_pin is not null and radio_data_station_id='$station_id'
    ";
	%hash = database_select_as_hash($sql,"title,pin");
    foreach $tmp (sort{$hash{$a}{title} cmp $hash{$b}{title}} keys %hash) {
	    $html_need_record .= "&#187; To record <b>\"$hash{$tmp}{title}\"</b> use pin <b>$hash{$tmp}{pin}</b><br>  ";
	    $html_refresh = "<meta http-equiv='refresh' content='10'> ";
    }
    print qq[
    	$html_refresh
    	<div id=data>$html_need_record</div>
    	<script>
			obj = document.getElementById('data');
    		html = obj.innerHTML;
    		parent.wait_record(html)
    	</script>
    ]
}
sub do_radio_station_prompt_list(){
	#
    #----------------------------------
    # check permission
    #---------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
	if (&active_user_permission_get("radio.data.prompt.access") ne 1) {adm_error("no permission"); return;}
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR : $station_object{status_message}");}
	$station_id 	= $station_object{data}{key};
	$station_title	= $station_object{data}{items}{0}{value};
    #
    #-------------------------------
    # prepare datatable
    #-------------------------------
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM radio_data_station_prompt where radio_data_station_id=$station_id  ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_data_station_prompt where radio_data_station_id=$station_id order by title limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Last change on top";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM radio_data_station_prompt where radio_data_station_id=$station_id order by date_last_change desc limit #LIMIT_1#,#LIMIT_2# ";
    $datatable{sql}{col_names}			= "id,title,prompt_size_kbytes,prompt_size_seconds,play,download,in_use"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT
		id,
		id,
		title,
		prompt_size_bytes/1024,
		prompt_size_seconds,'','',''
		FROM radio_data_station_prompt
		where id in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	# html values
    $datatable{html}{line_click_link}		= "$my_url?action=radio_station_prompt_edit&prompt_id=#ID#";
    $datatable{html}{cols}{0}{data_col_name}			= "play";
    $datatable{html}{cols}{0}{title}					= "Play";
    $datatable{html}{cols}{0}{url}						= "javascript:play_prompt('#ID#');";
    $datatable{html}{cols}{0}{width}					= 30;
    $datatable{html}{cols}{0}{flags}					= "ALIGN_CENTER";
    $datatable{html}{cols}{2}{data_col_name}			= "title";
    $datatable{html}{cols}{2}{title}					= "Custom prompt title";
    $datatable{html}{cols}{3}{data_col_name}			= "in_use";
    $datatable{html}{cols}{3}{title}					= "In use at:";
    $datatable{html}{cols}{3}{width}					= 150;
    $datatable{html}{cols}{4}{data_col_name}			= "prompt_size_kbytes";
    $datatable{html}{cols}{4}{title}					= "Kbytes";
    $datatable{html}{cols}{4}{flags}					= "FORMAT_FLOAT_2_DIGITS,ALIGN_RIGHT";
    $datatable{html}{cols}{4}{width}					= 100;
    $datatable{html}{cols}{5}{data_col_name}			= "prompt_size_seconds";
    $datatable{html}{cols}{5}{title}					= "Seconds";
    $datatable{html}{cols}{5}{flags}					= "FORMAT_DECIMAL,ALIGN_RIGHT";
    $datatable{html}{cols}{5}{width}					= 100;
#    $datatable{html}{cols}{6}{data_col_name}			= "download";
#    $datatable{html}{cols}{6}{title}					= "Upload/<br>record";
#    $datatable{html}{cols}{6}{url}						= "$my_url?action=radio_station_prompt_upload&prompt_id=#ID#";
#    $datatable{html}{cols}{6}{width}					= 30;
#    $datatable{html}{cols}{6}{flags}					= "ALIGN_CENTER";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_station_prompt_list";
    $datatable{html}{form}{data}{1}{name}	= "station_id";
    $datatable{html}{form}{data}{1}{value}	= "$station_id";
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
	# add extra values at hash before render html
	%hash = &database_select_as_hash("select 1,1,prompt_welcome,prompt_help,prompt_extension_question,prompt_extension_error from radio_data_station where id='$station_id' limit 0,1","flag,prompt_welcome,prompt_help,prompt_extension_question,prompt_extension_error");
	foreach $id (keys %{$datatable{data}{values}}){
		@array = ();
		if ($hash{1}{prompt_welcome} 			eq $id) { @array = (@array,"Welcome Prompt"); 	}
		if ($hash{1}{prompt_help} 				eq $id) { @array = (@array,"Help prompt"); 		}
		if ($hash{1}{prompt_extension_question} eq $id) { @array = (@array,"ask radio"); 		}
		if ($hash{1}{prompt_extension_error} 	eq $id) { @array = (@array,"invalid radio"); 	}
		$datatable{data}{values}{$id}{in_use} 	= join(",",@array);
		$datatable{data}{values}{$id}{play} 	= "<img src=/noc/design/icons/control_play.png hspace=0 vspace=0 border=0 width=16 height=16>";
		$datatable{data}{values}{$id}{download} = "<img src=/noc/design/icons/control_eject.png hspace=0 vspace=0 border=0 width=16 height=16>";

	}
	$datatable_html = &datatable_get_html(\%datatable);
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Phone radio custom prompts";
    $t{title}	= "\"$station_title\" phone radio";
    $t{content}	= qq[

<div id="navigation_tab">
<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
<a href="$my_url?action=radio_station_view&station_id=$station_id" >Overview</a>
<a href="$my_url?action=radio_station_edit&station_id=$station_id" >Settings</a>
<a href="$my_url?action=radio_station_stream_list_new&station_id=$station_id" >Content sources</a>
<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" class=selected>Custom prompts</a>
</div>

		<script>
		can_play=0;
		is_playing=0;
		function play_prompt(id){
			if (can_play == 1) {
				url = "$my_url?action=radio_station_prompt_play&id="+id;
				soundManager.destroySound("helloWorld");
				soundManager.createSound("helloWorld",url);
				soundManager.play("helloWorld");
			}
		}
		</script>
		<script src="/noc/design/soundmanager/script/soundmanager2-nodebug-jsmin.js"></script>
		<script>
			soundManager.url = '/noc/design/soundmanager/swf/';
			soundManager.flashVersion = 9;
			soundManager.useFlashBlock = false;
			soundManager.onready(function() {
				can_play=1;
			});
		</script>


		<script>
		function wait_record(html){
			if (html == "") {
				MyDisplay('wait_record',0);
			} else {
				MyDisplay('wait_record',1);
				MyHTML('wait_record_list',html)
			}
		}
		</script>
   		<div id=wait_record style="display:none;">
	   		<div class=alert_box style="width:500px"><div class=alert_box_inside style="background-image:url(/noc/design/busy.gif)">
	   		We have phone record wait in line. To record a prompt, dial (xxx)xxx-xxxx or dial to skype id zenofon, enter PIN number belong to prompt you want record and follow instructions.<br>
	   		<br>
	   		<div id=wait_record_list style="border:0px; padding:0px; margin:0px;"></div>
	   		</div></div><br>
   		</div>
   		<iframe id=wait_record name=wait_record style="display:none;" src="$my_url?action=radio_station_prompt_wait_record&station_id=$station_id"></iframe>

    	$datatable_html
    	<br>
    	<a href=$my_url?action=radio_station_prompt_add&station_id=$station_id>&#187; Add new custom prompt</a><br>

    ];
    &template_print("template.html",%t);
#<br><br><div class=alert_box style="width:400px;xfloat:right"><div class=alert_box_inside style="padding-left:10px;">
#<B><font color=red>WARNING</font></b><br> Custom prompts is not finished! We enable web interface to administrator just for test. Dont delete existent data. Create new and play with new. <br>Check <a href=https://work.zenofon.com/projects/radio/task_lists target=_blank>develop status</a> for more info
#</div></div>

}
sub do_radio_station_prompt_add(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$form{station_id},") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
	if (&active_user_permission_get("radio.data.prompt.access") ne 1) {adm_error("no permission"); return;}
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR: $station_object{status_message}");}
	$station_id = $station_object{data}{key};
    #
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%prompt_object = ();
	%{$prompt_object{config}} = %dataitemconfig_radio_station_prompt;
	&dataitem_initialize(\%prompt_object);
	# inject station_id into this object
	$prompt_object{data}{items}{0}{value} = $station_id;
	# inject radio name
	$prompt_object{data}{items}{1}{value} = $station_object{data}{items}{0}{value};
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "TA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_prompt_list&station_id=$station_id&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_prompt_list&station_id=$station_id";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_prompt_add";
    $form_settings{hidden_elements}{2}{name}	= "station_id";
    $form_settings{hidden_elements}{2}{value}	= "$station_id";
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_addform_process(\%prompt_object,\%form_settings,\%form);
	$html_form = &dataitem_web_addform_gethtml(\%prompt_object,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Add new phone radio custom prompt";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
sub do_radio_station_prompt_play(){
	$id  = &clean_int(substr($form{id},0,100));
	if (&active_user_permission_get("radio.data.prompt.access") ne 1) {adm_error("no permission"); return;}
	#
	# get prompt data
	%hash = database_select_as_hash("SELECT 1,1 FROM radio_data_station_prompt where id='$id' and prompt_data is not null","flag");
	if ($hash{1}{flag} ne 1) {return}
	my $output = $database->prepare("SELECT prompt_data FROM radio_data_station_prompt where id='$id'  ");
	$output->execute;
	my ($prompt) = $output->fetchrow_array;
	#
	# TODO: optimize gsm->mp3 code
	# the code bellow its not state of art.
	# the right things is get a perl lib to convert $prompt from gsm to mp3 in fly and then output
	# but no time to play... time to make it work. This is a low usage tool, so no problem the below code
	# we need 2 steps because in production server, sox cannot mp3 and ffmpeg cannot gsm
	#
	# define temp files
    $temp_file_out = "/tmp/.play.prompt.".time.".".$id.".mp3";
    $temp_file_mid = "/tmp/.play.prompt.".time.".".$id.".wav";
    $temp_file_in = "/tmp/.play.prompt.".time.".".$id.".gsm";
    #
    # dump in data as temp file
	open(OUT,">$temp_file_in");
	binmode OUT;
	print OUT $prompt;
	close(OUT);
	#
	# transcode to mp3 (flash at web page only understand mp3)
	$cmd = "/usr/bin/sox -t gsm $temp_file_in -r 8000 -c1 -t wav $temp_file_mid resample -ql 2>/dev/null" ;
	$ans = `$cmd`;
	$cmd = "/usr/bin/ffmpeg -i $temp_file_mid $temp_file_out >/dev/null 2>/dev/null";
	$ans = `$cmd`;
	#$cmd = "/usr/bin/sox -t gsm $temp_file_in -r 8000 -c1 -t mp3 $temp_file_out resample -ql 2>/dev/null" ;
	#$ans = `$cmd`;
    #
    # open out file and page
	open(IN,$temp_file_out);
	print "content-type: audio/mpeg\n\n";
	#
	# print page with header and bin temp file (transcode above)
	binmode STDOUT;
	binmode IN;
	my $buffer = "";
	while (read(IN, $buffer, 10240)) {
    	print $buffer;
	}
	close(IN);
	#
	# clean temp files
	unlink($temp_file_in);
	unlink($temp_file_mid);
	unlink($temp_file_out);
}
sub do_radio_station_prompt_del(){
    #
    #----------------------------------
    # get and check prompt
    #----------------------------------
	%prompt_object = ();
	%{$prompt_object{config}} = %dataitemconfig_radio_station_prompt;
	$prompt_object{data}{key}  = &clean_int(substr($form{prompt_id},0,100));;
	&dataitem_initialize(\%prompt_object);
	unless (&dataitem_get(\%prompt_object)) {adm_error("ERROR: $prompt_object{status_message}");}
	$station_id = $prompt_object{data}{items}{0}{value};
	$prompt_id = $prompt_object{data}{key};
    #
    #----------------------------------
    # get and check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = $station_id;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR: $station_object{status_message}");}
	# inject radio name
	$prompt_object{data}{items}{1}{value} = $station_object{data}{items}{0}{value};
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$station_id,") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
	if (&active_user_permission_get("radio.data.prompt.access") ne 1) {adm_error("no permission"); return;}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "SD";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_prompt_edit&prompt_id=$prompt_id&page=$form{page}";
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_prompt_list&station_id=$station_id&page=$form{page}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete '$prompt_object{data}{items}{3}{value}' custom prompt</b> from '$prompt_object{data}{items}{1}{value}' radio ? This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_prompt_del";
    $form_settings{hidden_elements}{2}{name}	= "prompt_id";
    $form_settings{hidden_elements}{2}{value}	= $prompt_id;
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_deleteform_process(\%prompt_object,\%form_settings,\%form);
	$html_form = &dataitem_web_deleteform_gethtml(\%prompt_object,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Delete phone radio custom prompt";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
#$tmp = "<pre>";
#$tmp .= "STATION OBJECT\n".Dumper(%station_object)."\n\n";
#$tmp .= "prompt OBJECT\n".Dumper(%prompt_object)."\n\n";
#$tmp .= "FORM SETTINGS\n".Dumper(%form_settings)."\n\n";
#$tmp .= "FORM\n".Dumper(%form)."\n\n";
#$tmp .= "<pre>";
#$t{content} .= $tmp;
	&template_print("template.html",%t);
}
sub do_radio_station_prompt_edit(){
    #
    #----------------------------------
    # get and check prompt
    #----------------------------------
	%prompt_object = ();
	%{$prompt_object{config}} = %dataitemconfig_radio_station_prompt;
	$prompt_object{data}{key}  = &clean_int(substr($form{prompt_id},0,100));;
	&dataitem_initialize(\%prompt_object);
	unless (&dataitem_get(\%prompt_object)) {adm_error("ERROR: $prompt_object{status_message}");}
	$station_id 		= $prompt_object{data}{items}{0}{value};
	$prompt_id 			= $prompt_object{data}{key};
	$prompt_title 		= $prompt_object{data}{items}{2}{value};
    #
    #----------------------------------
    # get and check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = $station_id;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR: $station_object{status_message}");}
	# inject radio name
	$station_title = $station_object{data}{items}{0}{value};
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_get("radio.data.access") eq 1) {
		# check id
		if (index(",$stations_allow,",",$station_id,") eq -1) {
			adm_error("no permission");
			return;
		}
	} elsif (&active_user_permission_get("radio.data.access") eq 2) {
		# approved
	} else {
		adm_error("no permission");
		return;
	}
	if (&active_user_permission_get("radio.data.prompt.access") ne 1) {adm_error("no permission"); return;}
    #
    #----------------------------------
    # check save_id
    #----------------------------------
    $save_id_is_ok =  ($form{save_id} eq 1) ? 1 : 0;
    #
    #----------------------------------
    # flag/unflag phone record
    #----------------------------------
	if ($save_id_is_ok eq 1) {
    }
    #
    #----------------------------------
    # save if possible
    #----------------------------------
	if ($save_id_is_ok eq 1) {
		#
		# check name
		if (&form_check_string($form{title}) ne 1) {
		    $error_message = "Wrong prompt title";
		}
		#
		# check rec_mode = upload
		if ($error_message eq "") {
		    if ($form{record_mode} eq "upload") {
		    	#
		    	# download and check file
			    $temp_file 		= "/tmp/.upload.prompt.".time.".tmp";
			    $temp_file_gsm	= "/tmp/.upload.prompt.".time.".tmp.gsm";
		    	$temp_file_size = 0;
				$temp_file_mime	= "";
		    	$filehandle = $cgi->param("FileUpload");
			    open(LOCAL, ">$temp_file");
			    while($bytesread=read($filehandle,$buffer,1024)) { print LOCAL $buffer; $temp_file_size++;}
	    		close(LOCAL);
	    		if ($temp_file_size eq 0) {
				    $error_message = "We only accept MP3 and WAV files. This file is empty.";
	    		} else {
		    		$temp_file_mime = &cgi_mime_get_from_file("$temp_file");
		    		unless ( ($temp_file_mime eq "audio/mpeg") || ($temp_file_mime eq "audio/x-wav")  ) {
					    $error_message = "We only accept MP3 and WAV files. This file type is '$temp_file_mime'.";
		    		}
	    		}
		    	#
		    	# convert to gsm and upload to database blob
				if ($error_message eq "") {
					$ans = "";
					$gsm_seconds= 0;
					$gsm_bytes	= 0;
		    		if (  ($temp_file_mime eq "audio/mpeg") || ($temp_file_mime eq "application/octet-stream")  ) {
						$cmd = "/usr/bin/sox -t mp3 $temp_file -r 8000 -c1 -t gsm $temp_file_gsm resample -ql 2>/dev/null ";
						$ans = `$cmd`;
						$ans = &cgi_mime_get_from_file($temp_file_gsm);
					} elsif ($temp_file_mime eq "audio/x-wav") {
						$cmd = "/usr/bin/sox -t wav $temp_file -r 8000 -c1 -t gsm $temp_file_gsm resample -ql 2>/dev/null ";
						$ans = `$cmd`;
						$ans = &cgi_mime_get_from_file($temp_file_gsm);
					} else {
					    $error_message = "We only accept MP3 and WAV files. This file type is '$temp_file_mime' and i cannot convert.";
					}
					if ($error_message eq "") {
			    		if ($ans eq "audio/x-gsm")  {
							#
							#------------------------
							# get size bytes and seconds
							#------------------------
							$gsm_bytes = -s $temp_file_gsm;
							$gsm_seconds = int($gsm_bytes/1600);
							#
							#------------------------
							# upload to blob by sql
							#------------------------
							open IN, $temp_file_gsm;
							my $temp_file_gsm_data;
							while (<IN>) {$temp_file_gsm_data .= $_;}
							close IN;
							#my $sql = "INSERT INTO Table (ImageColumn) VALUES (?)";
							$sql = qq[
								update radio_data_station_prompt set
								prompt_last_change=now(),
								prompt_size_bytes=?,
								prompt_size_seconds=?,
								prompt_data=?
								where id=?
							];
							$connection = $database->prepare($sql);
							$tmp = $connection->execute($gsm_bytes, $gsm_seconds, $temp_file_gsm_data, $prompt_id );
							#warning("SQL=".$sql);
							#warning("TMP=".$tmp);
							#warning("DATABASE_ERR=".$database->errstr());
							#warning("CONNECTION_ERR=".$connection->errstr());
			    		} else {
						    $error_message = "I cannot convert or understand this file. ";
			    		}
					}
				}
				#
				# clean
				#unlink($temp_file);
				#unlink($temp_file_gsm);
		    }
		}
		#
		# save if possible
		if ($error_message eq "") {
			# save basic
			$sql = "update radio_data_station_prompt set title='%s'  where id='%s' ";
			$sql = &database_scape_sql($sql,$form{title},$prompt_id);
			&database_do($sql);
			# save phone_record_pin
		    if ($form{record_mode} eq "phone") {
				&database_do("update radio_data_station_prompt set phone_record_pin=concat(id,round(9*rand()),round(9*rand()))  where id='$prompt_id' ");
		    } else {
				&database_do("update radio_data_station_prompt set phone_record_pin=null  where id='$prompt_id' ");
		    }
		    # save prompt_action
		    foreach $tmp (qw(welcome help extension_question extension_error)) {
		    	$sql = "update radio_data_station set prompt_$tmp = null where id='$station_id' and prompt_$tmp = '$prompt_id' ";
		    	database_do($sql);
		    	if ($form{prompt_action} eq $tmp) {
			    	$sql = "update radio_data_station set prompt_$tmp = '$prompt_id' where id='$station_id' ";
			    	database_do($sql);
		    	}
    		}
    		# redirect
			&cgi_redirect("$my_url?action=radio_station_prompt_list&station_id=$station_id'");
			return;
		}
	}
	if ($error_message ne "") {
		$error_message = "<div class=alert_box ><div class=alert_box_inside style='background-image:url(/noc/design/icons/exclamation.png)'>$error_message</div></div><br>";
	}
    #
    #----------------------------------
    # load data
    #----------------------------------
    if ($form{save_id} eq "") {
    	$form{title} = $prompt_title;
    	%hash = database_select_as_hash("select 1,1,phone_record_pin from radio_data_station_prompt where id='$prompt_id'","flag,value");
    	$form{record_mode} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} ne "") ) ? "phone" : "";
    	#
    	# get prompt actions
    	foreach $tmp (qw(welcome help extension_question extension_error)) {
    		%hash = database_select_as_hash("select 1,1,prompt_$tmp  from radio_data_station where id='$station_id'","flag,value");
	    	$form{prompt_action} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} eq  $prompt_id) ) ? "$tmp" : $form{prompt_action};
    	}
    }
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit phone radio custom prompt";
    $record_mode_is_phone	= ($form{record_mode} eq "phone")	? "selected" : "";
    $record_mode_is_upload	= ($form{record_mode} eq "upload")	? "selected" : "";
    %prompt_action_is = ();
    $prompt_action_is{$form{prompt_action}} = "selected";
    $t{content}		.= qq[
		<script>
		can_play=0;
		is_playing=0;
		function play_prompt(id){
			if (can_play == 1) {
				url = "$my_url?action=radio_station_prompt_play&id="+id;
				soundManager.destroySound("helloWorld");
				soundManager.createSound("helloWorld",url);
				soundManager.play("helloWorld");
			}
		}
		</script>
		<script src="/noc/design/soundmanager/script/soundmanager2-nodebug-jsmin.js"></script>
		<script>
			soundManager.url = '/noc/design/soundmanager/swf/';
			soundManager.flashVersion = 9;
			soundManager.useFlashBlock = false;
			soundManager.onready(function() {
				can_play=1;
			});
		</script>
		<script>
		function update_upload_data(){
			value = document.forms[0].elements[3].selectedIndex;
			if (value == "3") {MyDisplay('upload_data',1)} else {MyDisplay('upload_data',0)}
		}
		function lock_upload_form(){
			MyDisplay('form_buttons_work',0);
			MyDisplay('form_buttons_wait',1);
			return true;
		}
		</script>


	<fieldset style="width:350px;">
    	<form class=dataitemform  action='$my_url' method=post method=post enctype="multipart/form-data" onsubmit="lock_upload_form();">
	   		<table class=clear border=0 colspan=0 cellpadding=2 cellspacing=0 >
		    	<tr>
			    	<td valign=top>Radio</td>
			    	<td colspan=2 valign=top><input  read-only disabled  value='$station_title' > </td>
		    	</tr>

		    	<tr>
			    	<td valign=top>Prompt title</td>
			    	<td valign=top><input name=title value='$form{title}' ></td>
			    	<td><a href="javascript:play_prompt($prompt_id)"><img src=/noc/design/icons/control_play.png hspace=0 vspace=0 border=0 width=16 height=16 align=left></a></td>
		    	</tr>

		    	<tr>
		    		<td valign=top>Prompt usage</td>
		    		<td colspan=2 valign=top>
		    			<select  name=prompt_action>
		    			<option value="">(do not use this prompt at radio)</option>
		    			<option value="">&nbsp;</option>
		    			<option $prompt_action_is{welcome}				value="welcome"				>Play as welcome prompt</option>
		    			<option $prompt_action_is{help}					value="help"				>Play as help prompt</option>
		    			<option $prompt_action_is{extension_question}	value="extension_question"	>Play as ask radio prompt</option>
		    			<option $prompt_action_is{extension_error}		value="extension_error"		>Play as invalid radio prompt</option>
		    			</select>
		    		</td>
		    	</tr>

		    	<tr>
		    		<td valign=top>Prompt audio</td>
		    		<td colspan=2 valign=top>
		    			<select  name=record_mode style='' onchange="update_upload_data()">
		    			<option value=''>(do not change audio)</option>
						<option value=''>&nbsp;</option>
		    			<option $record_mode_is_phone  value='phone'>Record prompt by phone</option>
		    			<option $record_mode_is_upload value='upload'>Upload file</option>
		    			</select><br>

		    			<div id=upload_data style="display:none; margin-top:5px;">
		    			You can upload wav and mp3 files.<br>
		    			File size limit is 1mb.<br>
						<input name=FileUpload type=file><br>
		    			</div>

					</td>
		    	</tr>


		</table>
    	<br>

		$error_message

		<div id=form_buttons_work >
	    	<button class=cancel type=button onclick="window.location='radio.stations.cgi?action=radio_station_prompt_list&station_id=$station_id'">Cancel</button>
	    	<button class=cancel type=button onclick="window.location='radio.stations.cgi?action=radio_station_prompt_del&prompt_id=$prompt_id'">Delete</button>
    		<button class=save type=submit>Save</button>
    	</div>
		<div id=form_buttons_wait style="display:none">
	    	<button class=cancel	type=button disabled read-only>Cancel</button>
	    	<button class=cancel	type=button disabled read-only>Delete</button>
    		<button class=save		type=button disabled read-only><img src=/noc/design/busy.gif align=left> Saving... </button>
    	</div>

    	<input type=hidden name='action' value='radio_station_prompt_edit'>
    	<input type=hidden name='prompt_id' value='$prompt_id'>
		<input type=hidden name=save_id value=1>
    </form>
    </fieldset><br>

	<script>update_upload_data()</script>

    ];
	&template_print("template.html",%t);
}
#=======================================================


sub do_stream_updown {
	$mode	  = $form{mode} || 0; #down: 1, up: other
	$streamid   = clean_int($form{streamid});
	$extension = clean_int($form{extension});
	$stationid = clean_int($form{stationid});


	%hash = database_select_as_hash("select 1, max(--extension) from radio_data_station_channel where radio_data_station_id='$stationid' and enabled='1'","max");
	if ($mode == 1) {
		$nextextension = $extension + 1;
		if ($extension < $hash{1}{max}) {
			$sql = "update radio_data_station_channel set extension=extension-1 where extension='$nextextension' " .
						"and radio_data_station_id='$stationid'";
			warn $sql;
			database_do($sql);
			$sql = "update radio_data_station_channel set extension=extension+1 where id='$streamid'";
			warn $sql;
			database_do($sql);
		}

	} else {
		$nextextension = $extension - 1;
		if ($extension > 1) {
			database_do("update radio_data_station_channel set extension=extension+1 where extension='$nextextension' " .
						"and radio_data_station_id='$stationid'");
			database_do("update radio_data_station_channel set extension=extension-1 where id='$streamid'");
		}
	}

	refresh_url("$my_url?action=radio_station_stream_list_new&station_id=$stationid");
}

sub do_stream_delete {
	$streamid   = clean_int($form{streamid});
	%hash		= database_select_as_hash("select id,radio_data_station_id,extension from radio_data_station_channel ".
										  "where id='$streamid'", 'stationid,extension');

	$extension = $hash{$streamid}{extension};
	$stationid = clean_int($form{stationid}) || $hash{$streamid}{stationid};

	database_do("update radio_data_station_channel set enabled='0' where id='$streamid'");
	database_do("update radio_data_station_channel set extension=extension-1 where extension > $extension and radio_data_station_id='$stationid' and extension > 1");

	refresh_url("$my_url?action=radio_station_stream_list_new&station_id=$stationid");
}

sub get_stream_search_html {
	$keyword  = database_clean_string($form{keyword});
	$othertag = database_clean_string($form{othertag});
	$addtag   = $form{addtag};
	$addtag   = 1 if lc($addtag) eq 'true' || $addtag == 1;

	$filter  = '';
	@fields  = ('radio_data_station.title', 'radio_data_station_channel.title');

	if ($keyword) {
		for my $f (@fields) {
			$filter .= " OR " if $filter;
			$filter .= " (" . join( " OR ", map(" (lower($f) like '%$_%') ", split(',', $keyword))) . ") ";
		}
	}

	if ($addtag && $othertag) {
		for my $f (@fields) {
			$filter .= " OR " if $filter;
			$filter .= " (lower($f) like '%$othertag%') ";
		}
		database_do("insert into stream_tag (title, createby) values ('$othertag', '$my_user{1}{name}')");
	}

	$sql = "select radio_data_station_channel.id,radio_data_station.title,extension,radio_data_station_channel.title,stream_type,stream_url " .
		"FROM radio_data_station_channel, radio_data_station " .
		"where radio_data_station_channel.radio_data_station_id=radio_data_station.id and stream_permission!='private' " .
		"and ($filter)";
	warn $sql;

	$html = '';

	%hash = database_select_as_hash($sql, "stationtitle,extension,title,type,url");
	%tmp  = ();

	for (sort keys %hash) {
		$hash{$_}{stationtitle} =~ s{[<>]}{}g;
		$hash{$_}{title}		=~ s{[<>]}{}g;
		$hash{$_}{url}			=~ s{[<>]}{}g;
		$key					= $hash{$_}{title} . $hash{$_}{url};
		next if $tmp{$key};
		$tmp{$key}				= 1;

		$html .= qq[
					<tr>
						<td><a href="#" onclick="do_add('$_', '$hash{$_}{extension}','$hash{$_}{stationtitle}','$hash{$_}{title}','$hash{$_}{url}');">ADD</a></td>
						<td>$hash{$_}{stationtitle}</td><td>$hash{$_}{title}</td>
						<td><a href="javascript: play_radio('$_');" title="Click to listen">$hash{$_}{url}</a></td>
					</tr>
				];
	}

	cgi_hearder_html();
	print $html;

}

sub do_tag_admin {
	$subaction = $form{subaction};
	if ($subaction eq 'add') {
		$title = database_clean_string($form{title});
		if ($title) {
			database_do("insert into stream_tag (title, createby) values ('$title', '$my_user{1}{name}')");
		}
		refresh_url("$my_url?action=$action");
	} elsif ($subaction eq 'edit') {
		$title = database_clean_string($form{title});
		$id	   = clean_int($form{id});
		database_do("update stream_tag set title='$title', createby='$my_user{1}{name}' where id='$id'");
		cgi_hearder_html();
		print "<font color='green'>updated</font>";

	} elsif ($subaction eq 'delete') {
	} else {
		%hash = database_select_as_hash("select id,title,createby,createtime from stream_tag order by createtime desc", "title,createby,createtime");
		$tag_html = '';
		$i = 1;
		for (sort {$hash{$b}{createtime} <=> $hash{$a}{createtime}} keys %hash) {
			$tag_html .= "<tr><td>$i</td><td><input type='text' name='title' id='title$_' value='$hash{$_}{title}' />" .
						 "<a href='#' onclick='edittag(\"$_\"); return false;' title='click to edit'/>edit</a></td>" .
						 "<td>$hash{$_}{createby}</td><td>$hash{$_}{createtime}</td></tr>\n";
			$i++;

		}
		%t = &menu_permissions_get_as_template();
		$t{my_url}	= $my_url;
		$t{title}	= "Stream Tag Admin";
		$record_mode_is_phone	= ($form{record_mode} eq "phone")	? "selected" : "";
		$record_mode_is_upload	= ($form{record_mode} eq "upload")	? "selected" : "";
		%prompt_action_is = ();
		$prompt_action_is{$form{prompt_action}} = "selected";
		$t{content}		.= qq[
		<script>
		function addtag() {
			window.location.href="$my_url?action=$action&subaction=add&title=" + \$('#title').val();
		}

		function edittag(id) {
			window.open('$my_url?action=$action&subaction=edit&id=' + id + '&title=' + \$('#title' + id).val(), 'EDIT','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');
		}
		</script>
		New Tag: <input type="text" name="title" id="title" value="" /><input type="submit" name="subaction" value="add" onclick="addtag();return false;"/>
		<table width=70% border=0 border=1 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable>
	<thead>
		<tr>
		<td>Seq</td>
		<td>Title</td>
		<td>Created By</td>
		<td>Created Time</td>
		</tr>
	</thead>
	<tbody>
		$tag_html
	</tbody>
	</table>
		];
	&template_print("template.html",%t);

	}
}


sub get_tag_list {
	%hash = database_select_as_hash("select id,title from stream_tag", 'title');
	$list = '';

	$i = 1;
	$list = "<tr>";
	for (keys %hash) {
		next if !$hash{$_}{title};
		$list .= "<td><input type=\"checkbox\" name=\"tag\" value=\"$hash{$_}{title}\">$hash{$_}{title}</input></td>";
		$list .= "</tr><tr>\n" if $i++ % 6 == 0;
	}

	return $list;
}

sub do_stream_admin {
	$title = database_clean_string($form{stream_title}) || _error("stream title is null");
	$url   = $form{stream_url} || _error("stream url is null");
	$type  = $form{stream_type} || _error("stream type is null");
	$permission  = $form{stream_permission} || _error("stream permission is null");

	$station_id    = $form{station_id} || _error("station id is null");
	$newextension  =  $form{newextension};
	$oldextension  =  $form{oldextension};
	%tmp   = database_select_as_hash("select 1, max(--extension) from radio_data_station_channel " .
										 "where radio_data_station_id='$station_id' and enabled='1'", 'maxext');

	if ($action eq 'radio_station_stream_edit_new') {
			$id   = $form{stream_id} || _error("stream id is null");
			warn "update radio_data_station_channel set title='$title',stream_url='$url',stream_type='$type',stream_permission='$permission' where id='$id'";
			database_do ("update radio_data_station_channel set title='$title',stream_url='$url',stream_type='$type',stream_permission='$permission' where id='$id'");
			if ($newextension && $newextension ne $oldextension) {
				if ($newextension eq '9999') {
					$newextension = $tmp{1}{maxext};
				}

				database_do("update radio_data_station_channel set extension='$oldextension' where radio_data_station_id='$station_id'" .
							" and extension='$newextension'");
				database_do("update radio_data_station_channel set extension='$newextension' where id='$id'");
			}

			refresh_url ("$my_url?action=radio_station_stream_list_new&station_id=$station_id");

	} elsif ($action eq 'radio_station_stream_add_new') {

		$ext   = $tmp{1}{maxext} + 1;
		warn "insert into radio_data_station_channel (radio_data_station_id,extension,title,stream_url,stream_type,stream_permission)" .
									 "values ('$station_id', '$ext', '$title', '$url', '$type', '$permission')";
		$newid = database_do_insert ("insert into radio_data_station_channel (radio_data_station_id,extension,title,stream_url,stream_type,stream_permission)" .
									 "values ('$station_id', '$ext', '$title', '$url', '$type', '$permission')");
		if ($newextension ne '9999') {
			%hash  = database_select_as_hash("select 1,extension from radio_data_station_channel where radio_data_station_id='$station_id'" .
						" and extension='$newextension' and enabled='1'", 'extension');

			if ($hash{1}{extension}) {
				database_do("update radio_data_station_channel set extension=extension+1 where extension >= $newextension and radio_data_station_id='$station_id'");

			}

			database_do("update  radio_data_station_channel set extension='$newextension' where id='$newid'");

		}

		refresh_url ("$my_url?action=radio_station_stream_list_new&station_id=$station_id");

	}
}

sub _error {
	($tip) = @_;
	cgi_hearder_html();
	print "<font color='red'>ERROR: $tip</font>";
	exit 0;
}

sub _ok {
	($tip) = @_;
	cgi_hearder_html();
	print "<font color='green'>OK: $tip</font>";
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
