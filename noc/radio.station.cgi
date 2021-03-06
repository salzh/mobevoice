#!/usr/bin/perl

require "include.cgi";
#=======================================================
# Manage stations.
#=======================================================
# this are a radio-owner actions. We always need check
# if THIS use has access to THAT station
#=======================================================



#=======================================================
# tip If you want debug
#=======================================================
#
# drop debug messages at cgi output its a pain.
# you can simple use
#warning("This is a debug");
#warning("session_status=".$app{session_status});
# This command use Logger::Syslog and print message
# at local syslog. Just open a terminal and run this.
# tail -f /var/log/messages
# or
# tail -f /var/log/syslog
# to see outputs in realtime
#
# REMEMBER to remove all your warnings after debug.
# This is a extra overhead for system with production
# load
#
#=======================================================


#=======================================================
# logout if no session
#=======================================================
# if no login session is not enabled, redirect to index
# index do the magic to ask login
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}


#=======================================================
# check main permission
#=======================================================
# this allow only people with permission to manage radio stations
# later on, each section check if THIS user has permission to THAT station
#=======================================================
unless (&active_user_permission_get("radio.manager") >0) {adm_error("no permission"); exit;}
#=======================================================



#=======================================================
# create dataitem specifications
#=======================================================
# this are our dataitens in use for this cgi
# this code live inside a sub to easy fold in komodoedit
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

	#extra fields: show on public page,short description,keywords,big description,logo
	##show on public page
	$tmp++;
	$hash{items}{$tmp}{title}				= "Show on public page";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "NO";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
	$hash{items}{$tmp}{options}{1}{title}	= "YES";
	$hash{items}{$tmp}{sql_get}				= "SELECT on_public FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station set on_public=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Select on_public from radio_data_station.";

	##short description
	$tmp++;
	$hash{items}{$tmp}{title}				= "Short Description";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT short_descr FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set short_descr=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select radio station short description";

	##key words
	$tmp++;
	$hash{items}{$tmp}{title}				= "Key Words";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT keywords FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set keywords=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select radio station keywords";

	##big description
	$tmp++;
	$hash{items}{$tmp}{title}				= "Big Descrtiption";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT big_description FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set big_description=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select radio station big descrition";
	
	##logo
	$tmp++;
	$hash{items}{$tmp}{title}				= "Logo Url";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT logo FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set logo=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select radio station logo";

	
	%dataitemconfig_radio_station_simple= %hash;
	#--------------------------------
	%hash = ();
	$hash{title}						= "Radio station DID";
	$hash{sql_key}						= "SELECT 1 FROM radio_data_station where id=#KEY# ";
	$hash{sql_del}						= "delete from radio_data_station 				where id=#KEY# ";
	$hash{sql_del_1}					= "delete from radio_data_station_ani 			where radio_station_id=#KEY# ";
	$hash{sql_del_2}					= "delete from radio_data_station_ani_extradata	where radio_station_id=#KEY# ";
	$hash{sql_del_3}					= "delete from radio_data_station_channel 		where radio_data_station_id=#KEY# ";
	$hash{sql_del_4}					= "delete from radio_data_station_owner 		where radio_data_station_id=#KEY# ";
	$hash{sql_del_5}					= "delete from radio_data_station_prompt 		where radio_data_station_id=#KEY# ";
	$hash{sql_add}						= "insert into radio_data_station (title) values ('') ";
	$tmp=0;
	$hash{items}{$tmp}{title}			= "Title";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT title FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set title=#VALUE# where id=#KEY# ";
#	$tmp++;
#	$hash{items}{$tmp}{title}			= "DIDs";
#	$hash{items}{$tmp}{type}			= "SELECT";
#	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
#	$hash{items}{$tmp}{options_first} 	= "(No DID assigned)";
#	$hash{items}{$tmp}{options_sql}		= "SELECT id,title FROM radio_data_did WHERE radio_data_station_id is null or radio_data_station_id=#KEY# ORDER BY title ";
#	$hash{items}{$tmp}{sql_get}			= "SELECT id FROM radio_data_did where radio_data_station_id=#KEY# limit 0,1";
#	$hash{items}{$tmp}{sql_set}			= "update radio_data_did set radio_data_station_id=null where radio_data_station_id=#KEY# ";
#	$hash{items}{$tmp}{sql_set_1}		= "update radio_data_did set radio_data_station_id=#KEY# where id=#VALUE# ";
#	$hash{items}{$tmp}{error_message}	= "PLease select radio gateway DID";
	$tmp++;
	$hash{items}{$tmp}{title}			= "Owners";
	$hash{items}{$tmp}{type}			= "MULTISELECT";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{options_sql}		= "SELECT id,name FROM system_user order by name ";
	$hash{items}{$tmp}{sql_before_set}	= "delete from radio_data_station_owner where radio_data_station_id=#KEY# ";
	$hash{items}{$tmp}{sql_get}			= "SELECT 1 FROM radio_data_station_owner where radio_data_station_id=#KEY# and system_user_id=#OPTIONID# ";
	$hash{items}{$tmp}{sql_set}			= "insert into radio_data_station_owner (radio_data_station_id,system_user_id) values (#KEY#,#OPTIONID#)  ";
	$hash{items}{$tmp}{sql_unset}		= "delete FROM radio_data_station_owner where radio_data_station_id=#KEY# and system_user_id=#OPTIONID# ";

		$tmp++;
	$hash{items}{$tmp}{title}				= "Show on public page";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "NO";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
	$hash{items}{$tmp}{options}{1}{title}	= "YES";
	$hash{items}{$tmp}{sql_get}				= "SELECT on_public FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station set on_public=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Select on_public from radio_data_station.";

	##short description
	$tmp++;
	$hash{items}{$tmp}{title}			= "Short Description";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT short_descr FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set short_descr=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select radio station short description";

	##key words
	$tmp++;
	$hash{items}{$tmp}{title}			= "Key Words";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{sql_get}			= "SELECT keywords FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set keywords=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select radio station keywords";
	
	##big description
	$tmp++;
	$hash{items}{$tmp}{title}			= "Big Descrtiption";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{sql_get}			= "SELECT big_description FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set big_description=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please fill big descrition";
	
	##logo
	$tmp++;
	$hash{items}{$tmp}{title}			= "Logo Url";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT logo FROM radio_data_station where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_station set logo=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select radio station logo";

	%dataitemconfig_radio_station		= %hash;
	#--------------------------------
	%hash = ();
	$hash{title}							= "Radio channel";
	$hash{sql_key}							= "SELECT 1 FROM radio_data_station_channel where id=#KEY# ";
	$hash{sql_del}							= "delete from radio_data_station_channel where id=#KEY# ";
	$hash{sql_add}							= "insert into radio_data_station_channel (title) values ('') ";
	$tmp = 0;
	$hash{items}{$tmp}{title}				= "radio_data_station_id";
	$hash{items}{$tmp}{type}				= "NUMBER";
	$hash{items}{$tmp}{flags}				= "UI_HIDDEN,UI_READONLY";
	$hash{items}{$tmp}{sql_get}				= "SELECT radio_data_station_id  FROM radio_data_station_channel where id=#KEY# ";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Extension";
	$hash{items}{$tmp}{type}				= "NUMBER";
	$hash{items}{$tmp}{min}					= 0;
	$hash{items}{$tmp}{max}					= 99999999;
	$hash{items}{$tmp}{flags}				= "ALLOW_EMPTY";
	$hash{items}{$tmp}{sql_get}				= "SELECT extension FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set extension=#VALUE# where id=#KEY# ";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Title";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}				= "SELECT title FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set title=#VALUE# where id=#KEY# ";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Channel status";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "Disable this channel";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
	$hash{items}{$tmp}{options}{1}{title}	= "Enable this channel";
	$hash{items}{$tmp}{sql_get}				= "SELECT enabled FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set enabled=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Select stream type for background music.";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Background music";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{options}{0}{value}	= "MANUAL";
	$hash{items}{$tmp}{options}{0}{title}	= "Manual play/stop background music";
	$hash{items}{$tmp}{options}{1}{value}	= "ALWAYSON";
	$hash{items}{$tmp}{options}{1}{title}	= "Always play background music";
	$hash{items}{$tmp}{sql_get}				= "SELECT stream_mode FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set stream_mode=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Select policie for background music.";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Background music type";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{options}{0}{value}	= "SHOUTCAST";
	$hash{items}{$tmp}{options}{0}{title}	= "Shoutcast stream";
	$hash{items}{$tmp}{options}{1}{value}	= "MMS";
	$hash{items}{$tmp}{options}{1}{title}	= "MMS stream";
	$hash{items}{$tmp}{options}{2}{value}	= "MP3";
	$hash{items}{$tmp}{options}{2}{title}	= "Mp3 file over internet";
	$hash{items}{$tmp}{sql_get}				= "SELECT stream_type FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set stream_type=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Select stream type for background music.";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Background music URL";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}				= "SELECT stream_url FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set stream_url=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Select stream url for background music";
	%dataitemconfig_radio_station_channel = %hash;
	#--------------------------------
	%hash = ();
	$hash{title}							= "Add radio channel";
	$hash{sql_key}							= "SELECT 1 FROM radio_data_station_channel where id=#KEY# ";
	$hash{sql_add}							= "insert into radio_data_station_channel (title) values ('') ";
	$tmp = 0;
	$hash{items}{$tmp}{title}				= "radio_data_station_id";
	$hash{items}{$tmp}{type}				= "NUMBER";
	$hash{items}{$tmp}{flags}				= "UI_HIDDEN,UI_READONLY";
	$hash{items}{$tmp}{sql_get}				= "SELECT radio_data_station_id  FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set radio_data_station_id=#VALUE# where id=#KEY# ";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Extension";
	$hash{items}{$tmp}{type}				= "NUMBER";
	$hash{items}{$tmp}{min}					= 0;
	$hash{items}{$tmp}{max}					= 99999999;
	$hash{items}{$tmp}{flags}				= "ALLOW_EMPTY";
	$hash{items}{$tmp}{sql_get}				= "SELECT extension FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set extension=#VALUE# where id=#KEY# ";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Title";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}				= "SELECT title FROM radio_data_station_channel where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update radio_data_station_channel set title=#VALUE# where id=#KEY# ";
	%dataitemconfig_radio_station_channel_addonly = %hash;
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
#	$hash{items}{4}{sql_get}			= "SELECT stream_type FROM radio_data_station_stream where id=#KEY# ";
#	$hash{items}{4}{sql_set}			= "update radio_data_station_stream set stream_type=#VALUE# where id=#KEY# ";
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
# check_access_to_this_station
#=======================================================
# we gona call this sub all the time to make sure THIS user
# has permission on THAT station. We return 1 if ok
# and 0 if no permission
#=======================================================
sub check_access_to_this_station(){
	local($station_id) = @_;
	$station_id = &clean_int($station_id);
	if ($station_id eq "") {return 0;}
	#
	# check if station id exists
	%hash = &database_select_as_hash("SELECT 1,1 FROM radio_data_station where id='$station_id' ","flag");
	if ($hash{1}{flag} ne 1) {return 0;}
	#
	# check if user has access
	if (&active_user_permission_get("radio.manager") eq 1) {return 1;}
	$user_id = $app{session_cookie_u};
	$user_id = &clean_int($user_id);
	if ($user_id eq "") {return 0;}
	%hash = &database_select_as_hash("SELECT 1,1 FROM radio_data_station_owner where system_user_id='$user_id' and radio_data_station_id='$station_id'  ","flag");
	if ($hash{1}{flag} eq 1) {return 1;}
	return 0;
}
#=======================================================



#=======================================================
# main loop
#=======================================================
$my_url = "radio.station.cgi";
$action = $form{action};
if 		($action eq "radio_station_list")					{ &do_radio_station_list();					}
elsif 	($action eq "radio_station_add")					{ &do_radio_station_add();					}
elsif 	($action eq "radio_station_edit")					{ &do_radio_station_edit();					}
elsif 	($action eq "radio_station_del")					{ &do_radio_station_del();					}

elsif 	($action eq "radio_station_settings")				{ &do_radio_station_settings();				}
elsif 	($action eq "radio_station_clients")				{ &do_radio_station_clients();				}
elsif 	($action eq "radio_station_history")				{ &do_radio_station_history();				}

elsif 	($action eq "radio_station_channel_list")			{ &do_radio_station_channel_list();			}
elsif 	($action eq "radio_station_channel_edit")			{ &do_radio_station_channel_edit();			}
elsif 	($action eq "radio_station_channel_add")			{ &do_radio_station_channel_add();			}
elsif 	($action eq "radio_station_channel_del")			{ &do_radio_station_channel_del();			}

elsif 	($action eq "radio_station_now")					{ &do_radio_station_now();					}
elsif 	($action eq "radio_station_now_status")				{ &do_radio_station_now_status();			}
elsif 	($action eq "radio_station_now_order_set")			{ &do_radio_station_now_order_set();		}
elsif 	($action eq "radio_station_now_member_mode")		{ &do_radio_station_now_member_mode();		}
elsif 	($action eq "radio_station_now_member_name")		{ &do_radio_station_now_member_name();		}
elsif 	($action eq "radio_station_now_member_flag")		{ &do_radio_station_now_member_flag();		}
elsif 	($action eq "radio_station_now_poll_set")			{ &do_radio_station_now_poll_set();			}
elsif 	($action eq "radio_station_now_poll_reset")			{ &do_radio_station_now_poll_reset();		}
elsif 	($action eq "radio_station_now_poll_ovpl_set")		{ &do_radio_station_now_poll_ovpl_set();	}
elsif 	($action eq "radio_station_now_talk_pin")			{ &do_radio_station_now_talk_pin();			}
elsif 	($action eq "radio_station_now_listen_pin")			{ &do_radio_station_now_listen_pin();		}

elsif 	($action eq "radio_station_now_stream_stop")		{ &do_radio_station_now_stream_stop();		}
elsif 	($action eq "radio_station_now_stream_start")		{ &do_radio_station_now_stream_start();		}
elsif 	($action eq "radio_station_now_stream_volumeup")	{ &do_radio_station_now_stream_volumeup();	}
elsif 	($action eq "radio_station_now_stream_volumedown")	{ &do_radio_station_now_stream_volumedown();}
elsif 	($action eq "radio_station_now_stream_set")			{ &do_radio_station_now_stream_set();		}

elsif 	($action eq "radio_station_prompt_list")			{ &do_radio_station_prompt_list();			}
elsif 	($action eq "radio_station_prompt_wait_record")		{ &do_radio_station_prompt_wait_record();	}
elsif 	($action eq "radio_station_prompt_add")				{ &do_radio_station_prompt_add();			}
elsif 	($action eq "radio_station_prompt_del")				{ &do_radio_station_prompt_del();			}
elsif 	($action eq "radio_station_prompt_edit")			{ &do_radio_station_prompt_edit();			}
elsif 	($action eq "radio_station_prompt_play")			{ &do_radio_station_prompt_play();			}
elsif 	($action eq "radio_station_prompt_upload")			{ &do_radio_station_prompt_upload();		}
elsif 	($action eq "do_channel_updown")				{ &do_channel_updown();		}
elsif 	($action eq "do_radio_listen")				{ &do_radio_listen();		}
elsif 	($action eq "get_stream_search_html")				{ &get_stream_search_html();		}
elsif 	($action eq "do_upload_logo")				{ &do_upload_logo();		}


else									{ &do_radio_station_list();			}
exit;
#=======================================================


#=======================================================
# actions
#=======================================================
sub do_radio_station_list(){
    #
    #-------------------------------
    # prepare sql
    #-------------------------------
    $stations_allow = "";
	$stations_allow_sql = " 1=0 ";
	if (&active_user_permission_get("radio.data.access") eq 2) {
		$stations_allow_sql = " 1=1 ";
	} else {
		$user_id = &clean_int($app{session_cookie_u});
		$stations_allow = join(",",&database_select_as_array("SELECT distinct radio_data_station_id FROM radio_data_station_owner where system_user_id='$user_id' "));
		if ($stations_allow ne "") {
			$stations_allow_sql = " radio_data_station.id in ($stations_allow) ";
		}
	}

	warn "stations_allow_sql: $stations_allow_sql";
    #
    #-------------------------------
    # if only one radio, go direct
    #-------------------------------
	if (&active_user_permission_get("radio.manager") ne 1) {
		if ($stations_allow ne "") {
			if (index($stations_allow,",") eq -1)  {
				cgi_redirect("$my_url?action=radio_station_now&station_id=$stations_allow")
			}
		}
	}
    #
    #-------------------------------
    # prepare datatable
    #-------------------------------
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} 			= "SELECT count(*) FROM radio_data_station where $stations_allow_sql ";
#	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by DID";
#	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT radio_data_station.id FROM radio_data_station left join radio_data_did on radio_data_station.id=radio_data_did.radio_data_station_id where $stations_allow_sql order by radio_data_did.title asc  limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_data_station where $stations_allow_sql order by title limit #LIMIT_1#,#LIMIT_2# ";
    $datatable{sql}{col_names}			= "id,title,did,owners,on_public,keywords,short_descr,big_description,logo"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
#	$datatable{sql}{get_data} 			= "
#		SELECT
#		rs.id,
#		rs.id,
#		rs.title,
#		(select rd.title from radio_data_did as rd where rd.radio_data_station_id=rs.id limit 0,1) as did,
#		(select count(*) from radio_data_station_stream as rs where rs.radio_data_station_id=rs.id and deleted=0) as extensions
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
		rs.on_public,
		rs.short_descr,
		rs.keywords,
		rs.big_description,
		rs.logo
		FROM radio_data_station as rs
		where rs.id in (#SELECTED_IDS#)
	";
	# filter ids by page and order
	# html values
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_gateways";
    $datatable{html}{line_click_link}		= "$my_url?action=radio_station_now&station_id=#ID#";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "title,did,owners,on_public,short_descr,keywords,big_description,logo";
    $datatable{html}{col_titles}			= "Phone radio,DIDs assigned,Owners,Show On Public,Short Description,Keywords,Big Description,Logo";
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
		@array = &database_select_as_array("select title from radio_data_did where radio_data_station_id='$id' ");
		$datatable{data}{values}{$id}{did} 	 = join(", ", @array);
		@array = &database_select_as_array("SELECT u.name FROM radio_data_station_owner as l, system_user as u where l.system_user_id=u.id and l.radio_data_station_id='$id' ");
		$datatable{data}{values}{$id}{owners}	 = join(", ", @array);

		$datatable{data}{values}{$id}{on_public} = $datatable{data}{values}{$id}{on_public} ? 'YES' : 'NO';
		$datatable{data}{values}{$id}{logo}	 = "<img src='$datatable{data}{values}{$id}{logo}' width=130 height=55 />";
	}
	$datatable_html = &datatable_get_html(\%datatable);
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = ();
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Radio stations";
	$tmp = (&active_user_permission_get("radio.manager") eq 1) ? "<a href=$my_url?action=radio_station_add>&#187; Add new phone radio</a>" : "";
    $t{content}	= qq[
    	$datatable_html
    	<br>
		$tmp
    ];
    &template_print("template.html",%t);

}
sub do_radio_station_add(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_check("radio.manager") ne 1) {adm_error("no permission"); exit;}
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
    $t{title}	= "Add new radio station";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);

}
sub do_radio_station_del(){
	#
    #----------------------------------
    # check permission
    #----------------------------------
	if (&active_user_permission_check("radio.manager") ne 1) {adm_error("no permission"); exit;}
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
    $form_settings{message}				= "Do you really want <b>delete '$my_dataitem{data}{items}{0}{value}' radio station?</b><br><br>This action delete all data (history, prompts, settings) on this radio station.<br><br>This is a no undo action.";
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
    $t{title}	= "Delete radio station";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);

}
sub do_radio_station_edit(){
    #
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%my_dataitem = ();
	if (&active_user_permission_get("radio.manager") eq 1) {
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
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{click_id_prefix}		= "RGE";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_settings&station_id=$my_dataitem{data}{key}";
	if (&active_user_permission_get("radio.manager") eq 1) {
	    $form_settings{url_button_delete}= "$my_url?action=radio_station_del&station_id=$my_dataitem{data}{key}";
	}
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_settings&station_id=$my_dataitem{data}{key}";
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
    $t{title}	= "Edit radio station";
    $t{title}	= "\"$station_title\" radio station";
    $t{content}		.= qq[

	<div id="navigation_tab">
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected>Settings</a>
	</div>


	<fieldset style="width:400px;">$html_form</fieldset>
	<a title="click here to upload your custom logo" href="javascript: show_upload_logo();return false;">&#187 upload logo</a><p>
	<script>
	function upload_logo() {
		
	}
	</script>
	<form action="" method="post" name="logoform" enctype ="multipart/form-data">
	<input type="hidden" name="station_id" value="$station_id" />
	<input type="hidden" name="action" value="do_upload_logo" />
	<input type="file" name="logo" /><input type="submit" value="submit" />
	</form>
    ];
	&template_print("template.html",%t);
}
sub do_radio_station_history(){
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
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
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
			and radio_data_station_id='$station_id'
		group by
			DATE_FORMAT(datetime_start,'\%d')
	";
	%data = &database_select_as_hash($sql,"seconds");
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
			and radio_data_station_id='$station_id'
		group by
			DATE_FORMAT(datetime_start,'\%Y\%m')
	";
	%data = &database_select_as_hash($sql,"seconds");
	%plot = ();
	$plot{uid} = "minutes_month_by_month";
	$plot{x} = 300;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Minutes";
	$plot{series}{1}{color} = "d0d0d0";
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
			and radio_data_station_id='$station_id'
	];
	%known_anis = &database_select_as_hash($sql);
	$sql = "
		select
			DATE_FORMAT(datetime_start,'\%d'),ani,answered_time
		from
			radio_log_session
		where
		    ani<>''
			and datetime_start >= '$filter_yearmonth_month_day_01' and datetime_start < DATE_ADD('$filter_yearmonth_month_day_01', INTERVAL 1 MONTH)
			and radio_data_station_id='$station_id'
		order by id
	";
	%data = ();
	$connection = $database->prepare($sql);
	$connection->execute;
	while ( @rows = $connection->fetchrow_array(  ) ) {
		$tmp1 = (@rows)[0];
		$tmp2 = (@rows)[1];
		$tmp3 = (@rows)[2];
		$tmp3++;$tmp3--;
		unless (exists($known_anis{$tmp2})) {
			$data{$tmp1}{new} += $tmp3;
			$known_anis{$tmp2}=1;
		} else {
			$data{$tmp1}{old} += $tmp3;
		}
	}
	%plot = ();
	$plot{uid} = "new_clients_day_by_day";
	$plot{x} = 350;
	$plot{y} = 200;
	$plot{series}{1}{name} 	= "Minutes from new clients (per day)";
	$plot{series}{1}{color} = "5d788c";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = int($data{$dd}{new}/60);
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
	$plot{series}{1}{name} 	= "Minutes from return clients (per day)";
	$plot{series}{1}{color} = "D0D0D0";
	$slice_index = 1;
	@days = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31);
	foreach $d (@days) {
		$dd = substr("00".$d,-2,2);
		$plot{data}{$slice_index}{1} = int($data{$dd}{old}/60);
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
			and radio_data_station_id='$station_id'
		group by ani
	";
	$connection = $database->prepare($sql);
	$connection->execute;
	while ( @rows = $connection->fetchrow_array(  ) ) {
		$tmp1 = (@rows)[0];
		$tmp2 = (@rows)[1];
		if ( ($tmp1 ne "") && ($tmp2 > 120) ) { $total{active_clients_at_start_of_month}++ }
	}
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
			and radio_data_station_id='$station_id'
		group by ani
	";
	$connection = $database->prepare($sql);
	$connection->execute;
	while ( @rows = $connection->fetchrow_array(  ) ) {
		$tmp1 = (@rows)[0];
		$tmp2 = (@rows)[1];
		if ( ($tmp1 ne "") && ($tmp2 > 120) ) { $total{active_clients_at_end_of_month}++ }
	}
	# inactive ANIs
	$sql = qq[
		select 1,1,sum(distinct ani)
		from radio_log_session
		where
			ani<>''
			and datetime_start<date_sub('$filter_yearmonth_month_day_01', interval 6 month)
			and radio_data_station_id='$station_id'
	];
	%hash = &database_select_as_hash($sql,"flag,value");
	$total{inactive_clients} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} ne "") ) ? $hash{1}{value} : 0;
	#
	#
	#==========================================
	# print page
	#==========================================
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
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" radio station";
    $t{content}	= qq[

	<div id="navigation_tab">
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" class=selected>History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" >Settings</a>
	</div>

	<script language="JavaScript" src="design/FusionChartsFree/JSClass/FusionCharts.js"></script>

	<form action=$my_url>
	Year/month: 	<select name=filter_yearmonth>	<option value=''>Select month</option>		<option value=''> </option>$filter_yearmonth_select</select>
	<input type=submit value='Update'>
	<input type=hidden name=station_id value='$station_id'>
	<input type=hidden name=action value=radio_station_history>
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
		<tr>
		<td class=ar><h2>$ic</h2></td>
		<td >Inactive clients </td>
		</tr>
	</table>
	</fieldset>
	<br>


	<fieldset style="width:730px;"><legend>Minutes by new/return clients</legend>
	Here we count radio minutes we serve group by 'New client' and 'Return client'.
	'New client' is a radio client (ANI number) with no access to this radio in last 6 months.
	'Return client' is a radio client (ANI number) with at least one radio session in last 6 months.
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

	<fieldset style="width:730px;"><legend>Minutes global</legend>
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
sub do_radio_station_clients(){
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
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" radio station";
    $t{content}	= qq[

	<div id="navigation_tab" >
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" class=selected>Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id"  >Settings</a>
	</div>

	<div style=padding:30px;>
	Work in progress:<br>
	Tool to manage clients that dial and listen this radio station.<br>
	Reports, drilldown tool, manage clients data, export numbers to use in external marketing tools.
	</div>

    ];
    &template_print("template.html",%t);

}
sub do_radio_station_settings(){
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
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
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
		$message_dids = "".join(", ",@array)."";
	}
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" radio station";
    $t{content}	= qq[

	<div id="navigation_tab" style="margin-bottom:5px;">
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
	</div>
	<div id="navigation_tab" style="margin-bottom:20px;">
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >General</a>
		<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" >Channels</a>
		<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Prompts</a>
	</div>


				<fieldset style="width:500px"><legend>Info</legend>
					<form class=dataitemform  >
					<table class=clear border=0 colspan=0 cellpadding=2 cellspacing=0 >
					    <tr>
					    	<td valign=top>Title</td>
					    	<td valign=top><input readonly disabled value='$station_title' > </td>
				    	</tr>
					    <tr>
					    	<td valign=top>DIDs</td>
					    	<td valign=top><input readonly disabled value='$message_dids' > </td>
				    	</tr>
					</table>
					</form>
					<a href="$my_url?action=radio_station_edit&station_id=$station_id">&#187; Edit</a>
				</fieldset>


    ];
    &template_print("template.html",%t);

}
sub do_radio_station_channel_list(){
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
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    #-------------------------------
    # prepare datatable
    #-------------------------------
	# data definition
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} 			= "SELECT count(*) FROM radio_data_station_channel where radio_data_station_id='$station_id' ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by extension ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_data_station_channel where radio_data_station_id='$station_id' order by ABS(extension) limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM radio_data_station_channel where radio_data_station_id='$station_id' order by title  limit #LIMIT_1#,#LIMIT_2# ";
    $datatable{sql}{col_names}			= "id,enabled,extension,title,stream_type,stream_url,stream_approved,info"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT id,id,enabled,extension,title,stream_type,stream_url,stream_approved,''
		FROM radio_data_station_channel
		where id in (#SELECTED_IDS#)
	";
	# html info
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "radio_station_channel_list";
    $datatable{html}{form}{data}{1}{name}	= "station_id";
    $datatable{html}{form}{data}{1}{value}	= "$station_id";
    $datatable{html}{line_click_link}		= "$my_url?action=radio_station_channel_edit&channel_id=#ID#";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{col_names}				= "extension,title,info";
    $datatable{html}{col_titles}			= "Extension #,Channel title,Info";
	$form{page} 			= ($form{next} 		eq 1) ? $form{page}+1 : $form{page};
	$form{page} 			= ($form{previous} 	eq 1) ? $form{page}-1 : $form{page};
	$datatable{page} 		= $form{page};
	$datatable{page_size} 	= $form{page_size};
	$datatable{search}		= $form{search};
	$datatable{order}		= $form{order};
	&datatable_query_data(\%datatable);
	# dynamic data
	$enabled_channels_count = 0;
	$enabled_channels_info = "";
	foreach $id (keys %{$datatable{data}{values}}){

		$datatable{data}{values}{$id}{info} = "(Unknown)";
		if ($datatable{data}{values}{$id}{enabled} eq 1) {
			$enabled_channels_count++;
			$enabled_channels_info = "'$datatable{data}{values}{$id}{title}'";
			$enabled_channels_info .= ($datatable{data}{values}{$id}{extension} ne "")  ?  " (ext:$datatable{data}{values}{$id}{extension})" : "";
			if ($datatable{data}{values}{$id}{stream_approved} eq 1) {
				$datatable{data}{values}{$id}{info} = "Approved $datatable{data}{values}{$id}{stream_type} background music";
			} else {
				$datatable{data}{values}{$id}{info} = "NOT approved $datatable{data}{values}{$id}{stream_type} background music";
			}
		} else {
			$datatable{data}{values}{$id}{info} = "Disabled";
		}

		$tmp1 = ($datatable{data}{values}{$id}{title} eq "") ? "(No title $id)" : $datatable{data}{values}{$id}{title};
		$tmp2  = qq[<a href=# onclick="play_radio('$id')"><img src='design/icons/control_play.png' hspace=0 vspace=0 border=0 align=left></a>];
		$tmp2 .= qq[<a href="$my_url?action=radio_station_channel_edit&channel_id=$id">$tmp1</a>];
		$datatable{data}{values}{$id}{title} = $tmp2;

		$tmp1  = $datatable{data}{values}{$id}{extension};
		$tmp2  = qq[<a href="$my_url?action=do_channel_updown&mode=2&channel_id=$id"><img src='design/icons/bullet_arrow_up.png' hspace=0 vspace=0 border=0 align=left></a>];
		$tmp2 .= qq[<a href="$my_url?action=do_channel_updown&mode=1&channel_id=$id"><img src='design/icons/bullet_arrow_down.png' hspace=0 vspace=0 border=0 align=left></a>];
		$tmp2 .= qq[<a href="$my_url?action=radio_station_channel_edit&channel_id=$id">$tmp1</a>];
		$datatable{data}{values}{$id}{extension} = $tmp2;

	}
	$datatable_html = &datatable_get_html(\%datatable);
	#
    #----------------------------------
    # get prompt_question/noinput
    #----------------------------------
    %channels = database_select_as_hash("SELECT id,extension FROM radio_data_station_channel where radio_data_station_id='$station_id' and enabled=1 ","extension");
    %hash = database_select_as_hash("SELECT 1,1,prompt_question_logic,prompt_noinput_logic from radio_data_station where id='$station_id' ","flag,question,noinput");
    $prompt_question		= ($hash{1}{flag} eq 1) ? $hash{1}{question} : "";
    $prompt_noinput 		= ($hash{1}{flag} eq 1) ? $hash{1}{noinput} : "";
    $html_prompt_question	= "";
    $html_prompt_noinput	= "";
    if ($enabled_channels_count eq 0) {
	    $html_prompt_question = "When a client connect to this station, we cannot play anything because we dont have any channel enabled.";
    } elsif ($enabled_channels_count eq 1) {
	    $html_prompt_question = "When a client connect to this station, we send direct to channel $enabled_channels_info because is the only enabled.";
    } elsif ($prompt_question eq "prompt") {
	    $html_prompt_question = "When a client connect to this station, we ask extension channel he want to listen.";
    } elsif ($prompt_question eq "promptorquicklast") {
	    $html_prompt_question = "When a client connect to this station, we ask extension channel he want to listen but if he return too fast, auto dial last channel to help client.";
    } elsif ( ($prompt_question ne "") && (exists($channels{$prompt_question})) ) {
	    $html_prompt_question = "When a client connect to this station, we send direct to channel $channels{$prompt_question}{extension} without ask.";
    } else{
	    $html_prompt_question = "When a client connect to this station, we ask extension channel he want to listen.";
    }
    if ($enabled_channels_count eq 0) {
	    $html_prompt_noinput = "";
    } elsif ($enabled_channels_count eq 1) {
	    $html_prompt_noinput = "";
    } elsif ($prompt_noinput eq "prompt") {
	    $html_prompt_noinput = "Keep ask channel until client select one.";
    } elsif ($prompt_noinput eq "last") {
	    $html_prompt_noinput = "If no client input, remember they last channel.";
    } elsif ($prompt_noinput eq "next") {
	    $html_prompt_noinput = "If no client input, remember they last channel selected and send to next";
    } elsif ( ($prompt_noinput ne "") && (exists($channels{$prompt_noinput})) ) {
	    $html_prompt_noinput = "If no client input, send to channel $channels{$prompt_noinput}{extension}.";
    } else{
	    $html_prompt_noinput = "Keep ask channel until client select one.";
    }
    #
    #-------------------------------
    # print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" radio station";
    $t{content}	= qq[
		<script>
		function play_radio(id) {
			window.open('$my_url?action=do_radio_listen&id=' + id,				'Listen','width=300,height=100,top=150,left=100,toolbar=no,resizable=yes,status=no,location=no');

		};
		</script>
		<div id="navigation_tab" style="margin-bottom:5px;">
			<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
			<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
			<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
			<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
			<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
		</div>
		<div id="navigation_tab" style="margin-bottom:5px;">
			<a href="$my_url?action=radio_station_settings&station_id=$station_id" >General</a>
			<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" class=selected >Channels</a>
			<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Prompts</a>
		</div>

    	<p>$html_prompt_question $html_prompt_noinput</p>

		$datatable_html

		<a href="$my_url?action=radio_station_channel_add&station_id=$station_id" >&#187 Add new channel.</a>

    ];
    &template_print("template.html",%t);

}
sub do_radio_station_channel_edit(){
   #
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_radio_station_channel;
	$channel_id = &clean_int(substr($form{channel_id},0,100));
	$my_dataitem{data}{key} = $channel_id;
	&dataitem_initialize(\%my_dataitem);
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
	$station_id = $my_dataitem{data}{items}{0}{value};
    #
    #----------------------------------
    # get and check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = $station_id;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR: $station_object{status_message}");}
	$station_title = $station_object{data}{items}{0}{value};
	$channel_host = $hardcoded_call_server;
	#
    #----------------------------------
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    #$form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{click_id_prefix}		= "RGE";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_channel_list&station_id=$station_id";
    $form_settings{url_button_delete}	= "$my_url?action=radio_station_channel_del&channel_id=$channel_id";
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_channel_list&station_id=$station_id";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_channel_edit";
    $form_settings{hidden_elements}{2}{name}	= "channel_id";
    $form_settings{hidden_elements}{2}{value}	= $channel_id;
    #
    #----------------------------------
    # process form
    #----------------------------------
	if (&dataitem_web_editform_process(\%my_dataitem,\%form_settings,\%form) eq 1) {
		if ( ($form_settings{status_ok} eq 1) && ($form_settings{status_error} eq 0) ) {
			#---------------------------------
			# For was saved with success.. lets post-process (check stream)
			#---------------------------------
			%hash = database_select_as_hash("SELECT 1,1,enabled,stream_url,stream_type FROM radio_data_station_channel where id='$channel_id'","flag,enabled,url,type");
			$channel_now_type	= $hash{1}{type};
			$channel_now_url	= $hash{1}{url};
		    if ($hash{1}{enabled} eq 1) {
				#---------------------------------
				# stream is enabled and change.
				#---------------------------------
				# flag as not approved
				&database_do ("update radio_data_station_channel set stream_approved=0 where id='$channel_id' ");
				# cancel all streams
				&app_konference_channel_stream_disconnect($channel_host,$channel_id);
				sleep(1);
				# try start stream
				&app_konference_channel_stream_connect($channel_host,$channel_id);
				# wait
				sleep(16);
				# test if stream still up
				$channel_now_count = 0;
				%conferences = &app_konference_list($channel_host,$channel_id);
				foreach $id (keys %conferences) { if ($conferences{$id}{type} eq "STREAM") { $channel_now_count++; } }
				if ($channel_now_count eq 1) {
					# approve and redirect if stream still up
					&database_do ("update radio_data_station_channel set stream_approved=1 where id='$channel_id' ");
				} else {
					# Not approved, lets inject error and stay here
					$form_settings{status_ok}			= 0;
					$form_settings{status_error}		= 1;
					$form_settings{status_message}	= "This background music type our URL was not approved.";
				}
		    } else {
				#---------------------------------
		    	# stream is disabled, we need stop
				#---------------------------------
				&app_konference_channel_stream_disconnect($channel_host,$channel_id);
				sleep(1);
		    }
		}
		if ($form_settings{status_ok} eq 1) {
			&cgi_redirect($form_settings{url_form_ok});
			exit;
		}
	}
	$html_form = &dataitem_web_editform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------

    $taglist		= get_tag_list();
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit radio station";
    $t{title}	= "\"$station_title\" radio station";
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
	var url = document.getElementsByName("data6")[0].value;
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
	//\$('#stream_title').val(title);
	\$('input[name=data2]').val(title);
	//\$('#stream_url').val(url);
	\$('input[name=data6]').val(url);
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
<div id="content">
		<div id="navigation_tab" style="margin-bottom:5px;">
			<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
			<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
			<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
			<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
			<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
		</div>
		<div id="navigation_tab" style="margin-bottom:15px;">
			<a href="$my_url?action=radio_station_settings&station_id=$station_id" >General</a>
			<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" class=selected >Channels</a>
			<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Prompts</a>
		</div>

<input type="submit" name="listen" value="listen" onclick="listen();return false;"/> <font color="red">(** stream testing only works on Windows)</font>
<div id='player'></div>
	<fieldset style="width:400px;">$html_form</fieldset>
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
</div>
    ];
	&template_print("template.html",%t);
}
sub do_radio_station_channel_del(){
	#
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_radio_station_channel;
	$channel_id = &clean_int(substr($form{channel_id},0,100));
	$my_dataitem{data}{key} = $channel_id;
	&dataitem_initialize(\%my_dataitem);
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
	$station_id = $my_dataitem{data}{items}{0}{value};
	$channel_host = $hardcoded_call_server;
    #
    #----------------------------------
    # get and check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = $station_id;
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR: $station_object{status_message}");}
	$station_title = $station_object{data}{items}{0}{value};
	#
    #----------------------------------
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    #$form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{click_id_prefix}		= "uwh";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_channel_edit&channel_id=$channel_id";
    $form_settings{url_form_ok}			= "$my_url?action=radio_station_channel_list&station_id=$station_id";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete '$my_dataitem{data}{items}{2}{value}' channel</b> from '$station_title' station ? This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_channel_del";
    $form_settings{hidden_elements}{2}{name}	= "channel_id";
    $form_settings{hidden_elements}{2}{value}	= $channel_id;
    #
    #----------------------------------
    # process form
    #----------------------------------
	if (&dataitem_web_deleteform_process(\%my_dataitem,\%form_settings,\%form) eq 1) {
		if ( ($form_settings{status_ok} eq 1) && ($form_settings{status_error} eq 0) ) {
			&app_konference_channel_stream_disconnect($channel_host,$channel_id);
			&cgi_redirect($form_settings{url_form_ok});
			exit;
		}
	}
	$html_form = &dataitem_web_deleteform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" radio station";
    $t{content}		.= qq[

		<div id="navigation_tab" style="margin-bottom:5px;">
			<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
			<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
			<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
			<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
			<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
		</div>
		<div id="navigation_tab" style="margin-bottom:15px;">
			<a href="$my_url?action=radio_station_settings&station_id=$station_id" >General</a>
			<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" class=selected >Channels</a>
			<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Prompts</a>
		</div>

	<fieldset style="width:400px;">$html_form</fieldset>
    ];
	&template_print("template.html",%t);
}
sub do_radio_station_channel_add(){
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
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    #----------------------------------
    # prepare dataitem and check
    #----------------------------------
	%edit_object = ();
	%{$edit_object{config}} = %dataitemconfig_radio_station_channel_addonly;
	&dataitem_initialize(\%edit_object);
	# inject station_id into this object
	$edit_object{data}{items}{0}{value} = $station_id;
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "RXXEDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{click_id_prefix}		= "TA";
    $form_settings{url_button_cancel}	= "$my_url?action=radio_station_channel_list&station_id=$station_id";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "page";
    $form_settings{hidden_elements}{0}{value}	= "$form{page}";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "radio_station_channel_add";
    $form_settings{hidden_elements}{2}{name}	= "station_id";
    $form_settings{hidden_elements}{2}{value}	= "$station_id";
    #
    #----------------------------------
    # process form
    #----------------------------------
	# inject station_id again into this object, just to uverlap form values
	$edit_object{data}{items}{0}{value} = $station_id;
	&dataitem_web_addform_process(\%edit_object,\%form_settings,\%form);
	if ($form_settings{status_ok} eq 1) {
		&cgi_redirect("$my_url?action=radio_station_channel_edit&channel_id=$edit_object{data}{key}");
		exit;
	}
	$html_form = &dataitem_web_addform_gethtml(\%edit_object,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit radio station";
    $t{title}	= "\"$station_title\" radio station";
    $t{content}		.= qq[

		<div id="navigation_tab" style="margin-bottom:5px;">
			<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
			<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
			<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
			<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
			<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
		</div>
		<div id="navigation_tab" style="margin-bottom:15px;">
			<a href="$my_url?action=radio_station_settings&station_id=$station_id" >General</a>
			<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" class=selected >Channels</a>
			<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id" >Prompts</a>
		</div>


	<fieldset style="width:400px;">$html_form</fieldset>
    ];
	&template_print("template.html",%t);
}
sub do_radio_station_now(){
    #
    #----------------------------------
    # use radio_station dataitem to check station
    #----------------------------------
	%station_object = ();
	%{$station_object{config}} = %dataitemconfig_radio_station;
	$station_object{data}{key}  = &clean_int(substr($form{station_id},0,100));
	&dataitem_initialize(\%station_object);
	unless (&dataitem_get(\%station_object)) {adm_error("ERROR : $station_object{status_message}");}
	$station_id = $station_object{data}{key};
	$station_title = $station_object{data}{items}{0}{value};
	#
    #----------------------------------
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
	#
    #----------------------------------
    # check channel
    #----------------------------------
    %channels = database_select_as_hash("SELECT id,extension,title FROM radio_data_station_channel where enabled=1 and radio_data_station_id='$station_id'","extension,title");
	$channel_id 			= &clean_str(substr($form{channel_id},0,100));
	$channel_count 			= 0;
	$channel_id_selected	= "";
	foreach $id (sort{$channels{$a}{extension} <=> $channels{$b}{extension}} keys %channels){
		$channel_count++;
		$channel_id_selected = ($channel_id_selected eq "") ? $id : $channel_id_selected;
		$channel_id_selected = ($id eq $channel_id) ? $id : $channel_id_selected;
	}
	$channel_id = ($channel_id eq "OVERVIEW") ? "" : $channel_id_selected;
	#
	# print select
	$html_channels 			= "";
	$html_channels_empty 	= "<option value=''>No channels to select</option>";
	foreach $id (sort{$channels{$a}{extension} <=> $channels{$b}{extension}} keys %channels){
		$html_channels_empty = "";
		$tmp = ($id eq $channel_id) ? " selected " : "";
		$html_channels .= "<option $tmp value='$id'>Channel '$channels{$id}{title}' (Ext:$channels{$id}{extension})</a>";
	}
	$html_channels .= $html_channels_empty;
	#
    #-------------------------------
    # print page
    #-------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "\"$station_title\" radio station";
    $t{content}	= qq[

	<div id="navigation_tab" style="margin-bottom:5px;">
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" class=selected>Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" >Settings</a>
	</div>

	<div id=navigation_tab style='margin-bottom:20px;'>
		<form class=clear action=$my_url>
		<input type=hidden name=action value=radio_station_now>
		<input type=hidden name=station_id value='$station_id'>
		&nbsp;&nbsp;Select channel to realtime view: <select name=channel_id Onchange="this.form.submit();" >
			<option value='OVERVIEW'>Channels overview</option>
			<option value=''>&nbsp;</option>
			$html_channels
		</select>
		</form>
	</div>
	];
	#
	#
	if ($channel_id eq "") {
		if ($channel_count eq 0){
			#
			# ================================================
			# print no channel page
			# ================================================
			$t{content}	.= qq[
			When a client dial to radio, we cannot play anything because we dont have any channel enabled.<br>
			Go <a href=$my_url?action=radio_station_channel_list&station_id=$station_id>channels settings</a> to setup at least one channel.
			];
		} else {
			#
			# ================================================
			# print channel overview page
			# ================================================
			$t{content}	.= qq[
			TODO: Print realtime station channels information.<br>
			];
		}
	}
	# ================================================
	#
	#
	# ================================================
	# print channel now page
	# ================================================
	if ($channel_id ne "") {
			$t{content}	.= qq[
			<style>
			.CallerCard {
				margin:0px;
				border:0px solid green;
				padding:0px;
				float:left;
		    	margin-right:5px;
		    	margin-bottom:5px;
			}
			.CallerCard1 {
				padding:0px;
				margin:0px;
				border:1px solid #f8d322;
				border-radius:4px;
				background-color:#fff18e;
				width:110px;
				height:50px;
				overflow:hidden;
				font-size:11px;
				font-face:arial;
				line-height:140%;
			}
			.CallerCard2 {
				padding-left:5px;
				padding-right:0px;
				padding-top:2px;
				padding-bottom:0px;
			}

			.RealimeLeftBox {
				width:200;
				border-radius:3px;
				background-color:#e0e0e0;
				border:1px solid #d0d0d0;
				font-size:12px;
				line-height:120%;
			}
			.RealimeLeftBoxinside{
				padding:5px;
			}

			.RealtimePoolTable{
				padding:0px;
				margin:0px;
				border:0px;
				width:100%;
				margin-top:8px;
				margin-bottom:5px;
			}
			.RealtimePoolTable thead td {
				margin:0;
				padding:1px;
				border:0;
				font-size: 11px;
				text-align:center;
				white-space:nowrap;
				border-top:1px solid #c0c0c0;
				border-bottom:1px solid #c0c0c0;
			}
			.RealtimePoolTable tbody tr:hover { padding:0px;margin:0px;border:0px; background-color: #f0f0ff;}
			.RealtimePoolTable tbody tr:hover { padding:0px;margin:0px;border:0px; background-color: #f0f0ff;}
			.RealtimePoolTable tbody td {
				margin:0;
				padding:1px;
				border:0;
				border-bottom:1px solid #c0c0c0;
				font-size: 11px;
			}

			.PercentBar {
				padding:0px;
				margin:0px;
				border:0px;
				float:right;
			}
			.PercentBar_background {
				padding:0px;
				margin:0px;
				border:0px;
				width:100px;
				height:12px;
				background:none repeat scroll 0 0 #AAAAAA;
				border-color:#777777 #CCCCCC #CCCCCC #777777;
				border-style:solid;
				border-width:0.09em;
				float:right;
				margin-top:0.09em;
				position:relative;
			}
			.PercentBar_bar {
				width:0%;
				background-color:#496FC7;
				height:12px;
			}
			.PercentBar_value {
				color:#FFFFFF;
				height:12px;
				line-height:15px;
				position:absolute;
				text-align:center;
				top:0;
				width:100%;
				font-family:Tahoma,Arial,sans-serif;
				font-size:11px;
			}
			.VoteBubble_vote{
				padding:0px;
				margin:0px;
				border:0px;
				border-radius:6px;
				background-color:#ffffff;
				padding-left:5px;
				padding-right:5px;
				margin-right:3px;
				xxwidth:13px;
				font-size:10px;
				text-align:center;
				height:13px;
				font-weight:bold;
				color:#ffffff;
				float:right;
			}
			.VoteBubble_count{
				float:right;
			}
			</style>


			<table class=clear border=0 colspan=0 cellpadding=2 cellspacing=0 ><tr>
			<td valign=top width=200>

				<div class=clear style="margin-top:2px; width:200; border-radius:3px; background-color:#e0e0e0; border:1px solid #d0d0d0;">
				<div class=clear style="padding:5px; ">
					<h1><img src=/noc/design/icons/cassette.png align=left>Background audio</h1>
					<table class=clear width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 style="margin-bottom:5px;margin-top:5px;">
					<tr>
						<td width=30 style="background-color:#a0a0a0; padding:1px; padding-left:4px; border:1px solid #a0a0a0; border-radius:4px 0px 0px 4px; ">
							<a
							target=io_action
							href=$my_url?action=radio_station_now_stream_start&channel_id=$channel_id
							onclick="alertmessage('<img src=design/busy.gif align=left> Lets try to start background audio...',40)"
							title='Start background audio'
							style="background-image:url(/noc/design/icons/control_play_blue.png);background-repeat:no-repeat; padding:1px; padding-left:16px;"
							></a>
							<a
							target=io_action
							href=$my_url?action=radio_station_now_stream_stop&channel_id=$channel_id
							onclick="alertmessage('<img src=design/busy.gif align=left> Lets try to stop background audio...',20)"
							title='Stop background audio'
							style="background-image:url(/noc/design/icons/control_stop_blue.png);background-repeat:no-repeat; padding:1px; padding-left:16px;"
							></a>
						</td>
						<td style="background-color:#d0d0d0; padding:1px; padding-left:4px; border:1px solid #a0a0a0; color:#808080; border-radius:0px 4px 4px 0px; ">
							<div id=stream_info class=clear style="width:100%; font-size:12px; overflow: hidden;"></div>
						<td>
					</tr>
					</table>
					<table class=clear width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 >
					<tr>
						<td width=30 style="background-color:#a0a0a0; padding:1px; padding-left:4px; border:1px solid #a0a0a0; border-radius:4px 0px 0px 4px;">
							<a
							target=io_action
							href=$my_url?action=radio_station_now_stream_volumedown&channel_id=$channel_id
							title='Lower background audio volume'
							style="background-image:url(/noc/design/icons/03-30.png);background-repeat:no-repeat; padding:1px; padding-left:16px;"
							></a>
							<a
							target=io_action
							href=$my_url?action=radio_station_now_stream_volumeup&channel_id=$channel_id
							title='Rise background audio volume'
							style="background-image:url(/noc/design/icons/03-29.png);background-repeat:no-repeat; padding:1px; padding-left:16px;"
							></a>
						</td>
						<td style="background-color:#d0d0d0; padding:1px; padding-left:4px; border:1px solid #a0a0a0; color:#808080; border-radius:0px 4px 4px 0px; ">
							<div id=stream_volume class=clear style="width:100%; font-size:12px;  overflow: hidden;"></div>
						<td>
					</tr>
					</table>
					<div id=stream_warning class=clear style="width:100%; margin:0px; margin-top:5px; margin-bottom:5px; font-size:12px; line-height:120%; color:#808080;"></div>
					<a
					href="$my_url?action=radio_station_channel_edit&station_id=$station_id&channel_extension=$channels{$channel_id}{extension}"
					style="background-image:url(/noc/design/icons/control_equalizer_blue.png);background-repeat:no-repeat; padding:1px; padding-left:16px;"
					>Settings</a>
				</div>
				</div>
				<br>


				<div class=RealimeLeftBox><div class=RealimeLeftBoxinside>
					<h1><img src=/noc/design/icons/02-32.png align=left>Poll</h1>
					Ask question to your listeners and see results here.<br>
					<table class=RealtimePoolTable border=0 colspan=0 cellpadding=0 cellspacing=0 >
						<thead>
							<tr>
							<td id=poll_title colspan=2 style="text-align:right;">&nbsp;</td>
							<td >\%</td>
							</tr>
						</thead>
						<tbody>
							<tr><td class=ac style="width:15px; background-color:#808080;	font-weight:bold; color:#ffffff;">0</td><td class=ar style="width:50px;" 	id=poll_0_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_0_bar class=PercentBar_bar ></div><div id=poll_0_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#800000;	font-weight:bold; color:#ffffff;">1</td><td class=ar 						id=poll_1_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_1_bar class=PercentBar_bar ></div><div id=poll_1_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#FF0000;	font-weight:bold; color:#ffffff;">2</td><td class=ar 						id=poll_2_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_2_bar class=PercentBar_bar ></div><div id=poll_2_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#800080;	font-weight:bold; color:#ffffff;">3</td><td class=ar 						id=poll_3_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_3_bar class=PercentBar_bar ></div><div id=poll_3_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#FF00FF;	font-weight:bold; color:#ffffff;">4</td><td class=ar 						id=poll_4_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_4_bar class=PercentBar_bar ></div><div id=poll_4_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#008000;	font-weight:bold; color:#ffffff;">5</td><td class=ar 						id=poll_5_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_5_bar class=PercentBar_bar ></div><div id=poll_5_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#808000;	font-weight:bold; color:#ffffff;">6</td><td class=ar 						id=poll_6_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_6_bar class=PercentBar_bar ></div><div id=poll_6_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#FF6600;	font-weight:bold; color:#ffffff;">7</td><td class=ar 						id=poll_7_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_7_bar class=PercentBar_bar ></div><div id=poll_7_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#000080;	font-weight:bold; color:#ffffff;">8</td><td class=ar 						id=poll_8_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_8_bar class=PercentBar_bar ></div><div id=poll_8_percent class=PercentBar_value></div></div></div></td></tr>
							<tr><td class=ac style="			background-color:#00FFFF;	font-weight:bold; color:#ffffff;">9</td><td class=ar 						id=poll_9_votes>&nbsp;</td><td class=al><div class=PercentBar><div class=PercentBar_background ><div id=poll_9_bar class=PercentBar_bar ></div><div id=poll_9_percent class=PercentBar_value></div></div></div></td></tr>
						</tbody>
					</table>
					<div id=poll_enabled_on style="display:none">
						&#187; Poll is started. (
						<a href="$my_url?action=radio_station_now_poll_set&value=0&channel_id=$channel_id" target=io_action >stop</a>
						)
					</div>
					<div id=poll_enabled_off style="display:none">
						&#187; Poll is stoped. (
						<a href="$my_url?action=radio_station_now_poll_set&value=1&channel_id=$channel_id" target=io_action >start</a>,
						<a href="$my_url?action=radio_station_now_poll_reset&channel_id=$channel_id" target=io_action >reset</a>
						)
					</div>


					<div id=poll_ovpl_on style="display:none">
						&#187; One vote per client (<a href="$my_url?action=radio_station_now_poll_ovpl_set&value=0&channel_id=$channel_id" target=io_action >change</a>)
					</div>
					<div id=poll_ovpl_off style="display:none">
						&#187; Multiple votes per client (<a href="$my_url?action=radio_station_now_poll_ovpl_set&value=1&channel_id=$channel_id" target=io_action >change</a>)
					</div>
				</div></div>
				<br>

				<div class=clear style="width:200; border-radius:3px; background-color:#e0e0e0; border:1px solid #d0d0d0;">
				<div class=clear style="padding:5px; font-size:12px;line-height:120%;">
					<h1><img src=/noc/design/icons/lock.png align=left>Listen pin</h1>
					Make this channel protected by password.
					<br><br>
					Listen pin is <span id=listenpin_info>unknown</span> <a href=# onclick="editlistenpin()">(Edit)</a>
				</div>
				</div>
				<br>

				<div class=clear style="width:200; border-radius:3px; background-color:#e0e0e0; border:1px solid #d0d0d0;">
				<div class=clear style="padding:5px; font-size:12px;line-height:120%;">
					<h1><img src=/noc/design/icons/microphone--exclamation.png align=left>Talk pin</h1>
					Talk pin alow clients enable and disable talk-over radio without your assistence.
					<br><br>
					Talk pin is <span id=talkpin_info>unknown</span> <a href=# onclick="edittalkpin()">(Edit)</a>
				</div>
				</div>
				<br>

			</td>
			<td>&nbsp;&nbsp;&nbsp;</td>
			<td valign=top>

				<div class=alert_box style="margin-bottom:10px; width:770px; display:none;" id=alertmessage_box><div class=alert_box_inside id=alertmessage_text></div></div>

				<h3 id=clients_title >Active clients</h3>
				This are all active clients right now in this channel.You can group clients by
				<a href="$my_url?action=radio_station_now_order_set&value=TYPE&channel_id=$channel_id" target=io_action >type</a>
				or
				<a href="$my_url?action=radio_station_now_order_set&value=VOTE&channel_id=$channel_id" target=io_action >vote</a>
				<span id=clients_ui_order></span><br>
				<br>

				<div id=clients_cards class=clear style="width:800px; " ></div>
				<br clear=both>

			</td>
			</tr>
			</table>

		 	<a href=# onclick="MyDisplay('io_action');MyDisplay('io_status');">.</a>
			<iframe id=io_action name=io_action style="display:none; border:1px solid red; width:900px; height:150px;"></iframe>
			<iframe id=io_status name=io_status style="display:none; border:1px solid green; width:900px; height:150px;"></iframe>
			<script type="text/javascript">
			listenclients_qtd 		= 0;
			talkclients_qtd 		= 0;
			realtime_status_timmer	= null;
			realtime_status_enabled	= 1;
			function realtime_status_action(){
				if (realtime_status_enabled == 1)  {
					realtime_status_enabled = 0;
					document.getElementById("io_status").src = "$my_url?action=radio_station_now_status&channel_id=$channel_id";
				}
				realtime_status_timmer=setTimeout("realtime_status_action()",3000);
			}
			function realtime_status_done(){
				realtime_status_enabled	= 1;
			}
			function realtime_status_set_info_talkpin(message){
				MyHTML("talkpin_info",message);
			}
			function realtime_status_set_info_listenpin(message){
				MyHTML("listenpin_info",message);
			}
			function realtime_status_set_info_stream(status,volume,warning){
				MyHTML("stream_info",status);
				MyHTML("stream_volume",volume);
				MyHTML("stream_warning",warning);
			}
			function realtime_status_set_private_clients_cards(qtd,cards){
				title = "";
				if (qtd <= 0) {
					MyDisplay("Privatechat_box",0);
					title = "No clients in private chat";
				} else {
					MyDisplay("Privatechat_box",1);
					title = qtd+ " client(s) in private chat";
				}
				MyHTML("Privatechat_cards","<h1>"+title+"</h1>"+cards);
			}
			function realtime_status_set_clients_cards(qtd,ui_order,cards){
				MyHTML("clients_cards",cards);
				//MyHTML("clients_ui_order","(Right now "+ui_order+")");
				qtd++;
				qtd--;
				listenclients_qtd = qtd;
				if (qtd <= 0) {
					MyHTML("clients_title","No active clients");
				} else if (qtd == 1) {
					MyHTML("clients_title","One client");
				} else {
					MyHTML("clients_title",qtd+" clients");
				}
			}
			function realtime_status_set_poll(enabled,ovpl,t,v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,p0,p1,p2,p3,p4,p5,p6,p7,p8,p9){
				if (enabled == 1) {
					MyDisplay("poll_enabled_on",1);
					MyDisplay("poll_enabled_off",0);
				} else {
					MyDisplay("poll_enabled_on",0);
					MyDisplay("poll_enabled_off",1);
				}
				if (ovpl == 1) {
					MyDisplay("poll_ovpl_on",1);
					MyDisplay("poll_ovpl_off",0);
				} else {
					MyDisplay("poll_ovpl_on",0);
					MyDisplay("poll_ovpl_off",1);
				}
				MyHTML("poll_title",t+" votes");
				MyHTML("poll_0_votes",v0);
				MyHTML("poll_1_votes",v1);
				MyHTML("poll_2_votes",v2);
				MyHTML("poll_3_votes",v3);
				MyHTML("poll_4_votes",v4);
				MyHTML("poll_5_votes",v5);
				MyHTML("poll_6_votes",v6);
				MyHTML("poll_7_votes",v7);
				MyHTML("poll_8_votes",v8);
				MyHTML("poll_9_votes",v9);
				MyHTML("poll_0_percent",p0+"%");
				MyHTML("poll_1_percent",p1+"%");
				MyHTML("poll_2_percent",p2+"%");
				MyHTML("poll_3_percent",p3+"%");
				MyHTML("poll_4_percent",p4+"%");
				MyHTML("poll_5_percent",p5+"%");
				MyHTML("poll_6_percent",p6+"%");
				MyHTML("poll_7_percent",p7+"%");
				MyHTML("poll_8_percent",p8+"%");
				MyHTML("poll_9_percent",p9+"%");
				document.getElementById("poll_0_bar").style.width = p0;
				document.getElementById("poll_1_bar").style.width = p1;
				document.getElementById("poll_2_bar").style.width = p2;
				document.getElementById("poll_3_bar").style.width = p3;
				document.getElementById("poll_4_bar").style.width = p4;
				document.getElementById("poll_5_bar").style.width = p5;
				document.getElementById("poll_6_bar").style.width = p6;
				document.getElementById("poll_7_bar").style.width = p7;
				document.getElementById("poll_8_bar").style.width = p8;
				document.getElementById("poll_9_bar").style.width = p9;
			}
			realtime_status_action();
			</script>

			<script type="text/javascript">
			function editname(client_id,name) {
				newname = prompt("Enter client name",name);
				if (newname) {
					if (newname != name) {
						alert("$my_url?action=radio_station_now_member_name&client_id="+client_id+"&station_id=$station_id&value="+encodeURI(newname));
						document.getElementById("io_action").src = "$my_url?action=radio_station_now_member_name&client_id="+client_id+"&station_id=$station_id&value="+encodeURI(newname);
					}
				}
			}
			function edittalkpin() {
				newvalue = prompt("Enter talk-pin to allow clients talk over radio. Multiple numbers split by coma. Empty to disable","");
				if (newvalue) {
					document.getElementById("io_action").src = "$my_url?action=radio_station_now_talk_pin&channel_id=$channel_id&value="+encodeURI(newvalue);
				} else if (newvalue == "") {
					document.getElementById("io_action").src = "$my_url?action=radio_station_now_talk_pin&channel_id=$channel_id&value=";
				}
			}
			function editlistenpin() {
				newvalue = prompt("Enter listen-pin to protect this channel by password. Multiple numbers split by coma. Empty to disable","");
				if (newvalue) {
					document.getElementById("io_action").src = "$my_url?action=radio_station_now_listen_pin&channel_id=$channel_id&value="+encodeURI(newvalue);
				} else if (newvalue == "") {
					document.getElementById("io_action").src = "$my_url?action=radio_station_now_listen_pin&channel_id=$channel_id&value=";
				}
			}
			function alertmessage(msg,seconds) {
				if (msg == "") {
					MyDisplay("alertmessage_box",0);
				} else {
					MyDisplay("alertmessage_box",1);
					MyHTML("alertmessage_text",msg);
					miliseconds = 1000*seconds;
					setTimeout("alertmessage('',0)",miliseconds);
				}
			}
			</script>
	    ];
	}
    &template_print("template.html",%t);

}
sub do_radio_station_now_status(){
	#
	#-------------------------------------
	# check channel id
	#-------------------------------------
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash(
		"SELECT 1,1,radio_data_station_id,extension,listen_pin,talk_pin,ui_order,stream_type,stream_url,stream_mode,stream_approved,unix_timestamp(poll_timestamp),poll_enabled,poll_one_vote_per_listener,poll_option_0_count,poll_option_1_count,poll_option_2_count,poll_option_3_count,poll_option_4_count,poll_option_5_count,poll_option_6_count,poll_option_7_count,poll_option_8_count,poll_option_9_count FROM radio_data_station_channel where enabled=1 and id='$channel_id'",
		"flag,station_id,extension,listen_pin,talk_pin,ui_order,stream_type,stream_url,stream_mode,stream_approved,poll_ts,poll_enabled,poll_ovpl,poll_0,poll_1,poll_2,poll_3,poll_4,poll_5,poll_6,poll_7,poll_8,poll_9"
	);
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id			= $hash{1}{station_id};
	$extension 			= $hash{1}{extension};
	$talk_pin 			= $hash{1}{talk_pin};
	$listen_pin			= $hash{1}{listen_pin};
	$stream_type		= $hash{1}{stream_type};
	$stream_url			= $hash{1}{stream_url};
	$stream_mode		= $hash{1}{stream_mode};
	$ui_order			= $hash{1}{ui_order};
	$stream_approved	= ($hash{1}{stream_approved} eq 1) ? 1 : 0;
	$stream_volume		= "0";
	$host				= "";
	#
	#-------------------------------------
	# summary poll
	#-------------------------------------
	%poll = ();
	$poll{enabled}	= ($hash{1}{poll_enabled} eq 1) ? 1 : 0;
	$poll{ovpl}		= ($hash{1}{poll_ovpl} eq 1) ? 1 : 0;
	$poll{total}	= 0;
	foreach (0..9) {
		$poll{value}{$_} 	= $hash{1}{"poll_".$_};
		$poll{percent}{$_}	= 0;
		$poll{total} += $poll{value}{$_};
	}
	if ($poll{total} > 0) {
		foreach (0..9) {
			$poll{percent}{$_}	= int(100*($poll{value}{$_}/$poll{total}));
		}
	}
	#
	#-------------------------------------
	# check permission to this station
	#-------------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
	#
	#-------------------------------------
	# start page
	#-------------------------------------
	print "content-type: text/html\n\n";
	#
	#-------------------------------------
	# get public conference
	#-------------------------------------
	#%conference = &app_konference_list($host,$channel_id);
	%conference = &radio_get_active_sessions_of_channel($channel_id);
	print "CHANNEL_ID=$channel_id<br><pre style=font-size:10px;>". Dumper(%conference)."</pre><hr>";
	#
	#-------------------------------------
	# print poll
	#-------------------------------------
	$html_poll_value = "";
	$html_poll_percent = "";
	foreach (0..9) {
		$html_poll_value 	.= "'".&format_number($poll{value}{$_},0)."',";
		$html_poll_percent	.= "'".$poll{percent}{$_}."',";
	}
	$html_poll_value = substr($html_poll_value,0,-1);
	$html_poll_percent = substr($html_poll_percent,0,-1);
	$html_poll_total = &format_number($poll{total},0);
	print qq[
	Poll<br>
	value   = $html_poll_value<br>
	percent = $html_poll_percent<br>
	total   = $html_poll_total <br>
	<script>parent.realtime_status_set_poll("$poll{enabled}","$poll{ovpl}","$html_poll_total",$html_poll_value,$html_poll_percent);</script>
	<hr>
	];
	#
	#-------------------------------------
	# build client-cards and get stream data
	#-------------------------------------
	$qtd = 0;
	$stream_count = 0;
	$html_clients	= "";
	foreach $id (keys %conference) {
		# prepare card
		$html = "";
		$html .= "<div class=CallerCard><div class=CallerCard1><div class=CallerCard2>";
		#
		# pin
		#$html .= "<div style='float:right'><a style='font-size:6px; color:#808080;' target=io_action  href=$my_url?action=radio_station_now_member_kick&log_id=$conference{$id}{radio_log_session_id} title='Kick this client out of this channel'>x</a></div>";
		#if ($conference{$id}{flag_1} eq "1") {
		#	$html .= "<div style='float:right'><a target=io_action href=$my_url?action=radio_station_now_member_flag&ani=$conference{$id}{ani}&station_id=$station_id&flag=1&value=0 title='un-pin'		><img src=/noc/design/img/pin_small.png				width=16 height=16 hspace=0 vspace=0 border=0></a></div>";
		#} else {
		#	$html .= "<div style='float:right'><a target=io_action href=$my_url?action=radio_station_now_member_flag&ani=$conference{$id}{ani}&station_id=$station_id&flag=1&value=1 title='pin'		><img src=/noc/design/img/pin_small-disabled.png 	width=16 height=16 hspace=0 vspace=0 border=0></a></div>";
		#}
		#
		# name / ani
		$html .= "<div style='overflow:hidden; white-space: nowrap;  height:15px;'>";
		if ($conference{$id}{client_id} eq "") {
			$html .= "<span style=color:c0c0c0;>unknown</span>";
		} else {
			$html .= "$conference{$id}{ani_format}";
			#
			# a simple name change does not make sense. At end we gonna have 2 names, one from client and other that host assign. Too complex
			# we need move to card edit and then add flags instead name.
			# lets disable name change until we add card edit
			# TODO: we need a card edit. That show client data and all client-station data.
			#if ($conference{$id}{name} eq "") {
			#	$html .= "<a href=# onclick=\"editname('$conference{$id}{client_id}','$conference{$id}{name}')\" title='Edit client name' >";
			#	$html .= "$conference{$id}{ani_format}</a>";
			#} else {
			#	$html .= "<a href=# onclick=\"editname('$conference{$id}{client_id}','$conference{$id}{name}')\" title='Edit client name'>";
			#	$html .= "$conference{$id}{name}</a>";
			#}
		}
		$html .= "</a></div>";
		#
		# add votes
		$tmp1 = "";
		$tmp1 = ($conference{$id}{last_vote} eq 0) ? "#808080" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 1) ? "#800000" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 2) ? "#FF0000" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 3) ? "#800080" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 4) ? "#FF00FF" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 5) ? "#008000" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 6) ? "#808000" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 7) ? "#FF6600" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 8) ? "#000080" : $tmp1;
		$tmp1 = ($conference{$id}{last_vote} eq 9) ? "#00FFFF" : $tmp1;
		if ($tmp1 ne "") {
			$tmp2 = $conference{$id}{votes_count};
			$tmp2++;$tmp2--;
			$html .= "<div class=VoteBubble_vote style='background-color:$tmp1'>$conference{$id}{last_vote}/$tmp2</div>";
		}
		#
		# duration
		$html .= "$conference{$id}{duration}<br>";
		#
		# bottom icons
		if ($conference{$id}{type} eq "LISTENER") {
			$tmp=$conference{$id}{radio_log_session_id};
			$html .= qq[
				<div id=mode_status_$tmp onmouseover="MyDisplay('mode_status_$tmp',0);MyDisplay('mode_ask_$tmp',1);" class=clear>
				<a href=# style="background-position:0 0; padding-top:2px;background-image:url(/noc/design/icons/cassette.png);background-repeat:no-repeat;padding-left:18px;">Listen client</a>
				</div>
				<div id=mode_ask_$tmp onmouseout="MyDisplay('mode_status_$tmp',1);MyDisplay('mode_ask_$tmp',0);" style="display:none;" class=clear>
				Set:
				<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=1&log_id=$conference{$id}{radio_log_session_id} >Talk</a> or
				<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=2&log_id=$conference{$id}{radio_log_session_id} >Private</a>
				</div>
			];
		} elsif ($conference{$id}{type} eq "TALKER") {
			$html .= qq[
				<div id=mode_status_$tmp onmouseover="MyDisplay('mode_status_$tmp',0);MyDisplay('mode_ask_$tmp',1);" class=clear>
				<a href=# style="background-position:0 0; padding-top:2px;background-image:url(/noc/design/icons/microphone.png);background-repeat:no-repeat;padding-left:18px;">Talk over radio</a>
				</div>
				<div id=mode_ask_$tmp onmouseout="MyDisplay('mode_status_$tmp',1);MyDisplay('mode_ask_$tmp',0);" style="display:none;" class=clear>
				Set:
				<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=0&log_id=$conference{$id}{radio_log_session_id} >Listen</a> or
				<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=2&log_id=$conference{$id}{radio_log_session_id} >Private</a>
				</div>
			];
		} elsif ($conference{$id}{type} eq "PRIVATE") {
			$html .= qq[
				<div id=mode_status_$tmp onmouseover="MyDisplay('mode_status_$tmp',0);MyDisplay('mode_ask_$tmp',1);" class=clear>
				<a href=# style="background-position:0 0; padding-top:2px;background-image:url(/noc/design/icons/group_add.png);background-repeat:no-repeat;padding-left:18px;">Private talk</a>
				</div>
				<div id=mode_ask_$tmp onmouseout="MyDisplay('mode_status_$tmp',1);MyDisplay('mode_ask_$tmp',0);" style="display:none;" class=clear>
				Set:
				<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=0&log_id=$conference{$id}{radio_log_session_id} >Listen</a> or
				<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=1&log_id=$conference{$id}{radio_log_session_id} >Talk</a>
				</div>
			];
		}
		#$html .= "<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=0&log_id=$conference{$id}{radio_log_session_id} >Listen</a>/";
		#$html .= "<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=1&log_id=$conference{$id}{radio_log_session_id} >Talk</a>/";
		#$html .= "<a target=io_action href=$my_url?action=radio_station_now_member_mode&mode=2&log_id=$conference{$id}{radio_log_session_id} >Private</a>";
		#
		# finish card
		$html .= "</div></div></div>";
		#
		# add card
		if (index("|TALKER|LISTENER|PRIVATE|","|$conference{$id}{type}|") ne -1) {
			$conference{$id}{card_html} = $html;
			$qtd++;
		} elsif ($conference{$id}{type} eq "STREAM") {
			$stream_duration	= $conference{$id}{duration};
			$stream_muted		= $conference{$id}{muted};
			$stream_volume		= $conference{$id}{volume_talk};
			$stream_count++;
		}
	}
	#
	#-------------------------------------
	# print client-cards
	#-------------------------------------
	$html = "";
	if ($ui_order eq "VOTE") {
		# ====== order by vote ======
		%hash = ();
		foreach $id (sort{$conference{$b}{votes_count} <=> $conference{$a}{votes_count}} keys %conference) {
			if (index("|TALKER|LISTENER|PRIVATE|","|$conference{$id}{type}|") eq -1) {next}
			$t = ($conference{$id}{last_vote} eq "") ? "NO" : "$conference{$id}{last_vote}";
			$hash{$t}{q}++;
			$hash{$t}{ids} .= $id.",";
		}
		foreach $v (0..9) {
			if ($hash{$v}{q} <1){next}
			$html .= "<h1>$hash{$v}{q} Clients voted for option $v</h1>";
			foreach $id (split(/\,/,$hash{$v}{ids}) ) {
				if (exists($conference{$id}{card_html})) {
					$html .= $conference{$id}{card_html};
				}
			}
			$html .= "<br clear=both>";
		}
		$v = "NO";
		if ($hash{$v}{q} >=1 ){
			$html .= "<h1>$hash{$v}{q} no vote clients</h1>";
			foreach $id (split(/\,/,$hash{$v}{ids}) ) {
				if (exists($conference{$id}{card_html})) {
					$html .= $conference{$id}{card_html};
				}
			}
			$html .= "<br clear=both>";
		}
	} else {
		# ====== order by type ======
		%hash = ();
		foreach $id (sort{$conference{$b}{duration_seconds} <=> $conference{$a}{duration_seconds}} keys %conference) {
			if (index("|TALKER|LISTENER|PRIVATE|","|$conference{$id}{type}|") eq -1) {next}
			$t = $conference{$id}{type};
			$hash{$t}{q}++;
			$hash{$t}{ids} .= $id.",";
		}
		$t = "PRIVATE";
		if ($hash{$t}{q} >=1 ){
			$html .= "<h1>$hash{$t}{q} private chat client(s)</h1>";
			foreach $id (split(/\,/,$hash{$t}{ids}) ) {
				if (exists($conference{$id}{card_html})) {
					$html .= $conference{$id}{card_html};
				}
			}
			$html .= "<br clear=both>";
		}
		$t = "TALKER";
		if ($hash{$t}{q} >=1 ){
			$html .= "<h1>$hash{$t}{q} talk-over-radio client(s)</h1>";
			foreach $id (split(/\,/,$hash{$t}{ids}) ) {
				if (exists($conference{$id}{card_html})) {
					$html .= $conference{$id}{card_html};
				}
			}
			$html .= "<br clear=both>";
		}
		$t = "LISTENER";
		if ($hash{$t}{q} >=1 ){
			$html .= ($html eq "") ? "" : "<h1>$hash{$t}{q} listen client(s)</h1>";
			foreach $id (split(/\,/,$hash{$t}{ids}) ) {
				if (exists($conference{$id}{card_html})) {
					$html .= $conference{$id}{card_html};
				}
			}
			$html .= "<br clear=both>";
		}
	}
	print qq[
	<div id=clients_cards>$html</div>
	<script>parent.realtime_status_set_clients_cards("$qtd","$ui_order",document.getElementById("clients_cards").innerHTML);</script>
	];
	#
	#-------------------------------------
	# play/stop/mute
	#-------------------------------------
	$stream_msg_status	= "";
	$stream_msg_volume	= "";
	$stream_msg_warning	= "";
	if ($stream_count eq 1) {
		if ($stream_muted eq 1) {
			$stream_msg_status	= "MUTED $stream_duration ";
		} else {
			$stream_msg_status	= "PLAY $stream_duration";
		}
	} elsif ($stream_count > 1)  {
		$stream_msg_status	= "CORRUPTED";
	} else {
		$stream_msg_status	= "STOP";
	}
	# channel status
	if ($stream_url eq "") {
		$stream_msg_warning	= "No stream set. Change settings to fix.";
	} elsif ($qtds > 1) {
		$stream_msg_warning	= "Music is corrupted. Try stop/play to reset or go settings to change. ";
	} elsif ($stream_approved ne 1) {
		$stream_msg_warning	= "Stream not approved. Try stop/play to reset or go settings to change.";
	}
	print qq[<script>parent.realtime_status_set_info_stream("$stream_msg_status","Volume: $stream_volume","$stream_msg_warning")</script>];
	#
	#-------------------------------------
	# pin
	#-------------------------------------
	$talk_pin = ($talk_pin eq "") ? "disabled" : $talk_pin;
	print qq[<script>parent.realtime_status_set_info_talkpin("$talk_pin")</script>];
	$listen_pin = ($listen_pin eq "") ? "disabled" : $listen_pin;
	print qq[<script>parent.realtime_status_set_info_listenpin("$listen_pin")</script>];
	#
	#-------------------------------------
	# finish page
	#-------------------------------------
	print qq[<script>parent.realtime_status_done();</script>];
	exit;
}
sub do_radio_station_now_poll_set() {
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,unix_timestamp(poll_timestamp),poll_one_vote_per_listener FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,poll_ts,poll_ovpl");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id	= $hash{1}{station_id};
	$poll_ts	= $hash{1}{poll_ts};
	$poll_ovpl	= $hash{1}{poll_ovpl};
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
	#
	# reset
	$value = ($form{value} eq 1) ? 1 : 0;
	$sql = "
	Update
		radio_data_station_channel
	set
		poll_enabled = '$value'
	where
		enabled=1 and id='$channel_id'
	";
	&database_do($sql);
	#
	# start page
	print "content-type: text/html\n\n$sql";

}
sub do_radio_station_now_order_set() {
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,unix_timestamp(poll_timestamp),poll_one_vote_per_listener FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,poll_ts,poll_ovpl");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id	= $hash{1}{station_id};
	$poll_ts	= $hash{1}{poll_ts};
	$poll_ovpl	= $hash{1}{poll_ovpl};
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
	#
	# reset
	$value = trim(substr(&clean_str($form{value},"URL"),0,32));
	$sql = "
	Update
		radio_data_station_channel
	set
		ui_order = '$value'
	where
		enabled=1 and id='$channel_id'
	";
	&database_do($sql);
	#
	# start page
	print "content-type: text/html\n\n$sql";

}
sub do_radio_station_now_poll_reset() {
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,unix_timestamp(poll_timestamp),poll_one_vote_per_listener FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,poll_ts,poll_ovpl");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id	= $hash{1}{station_id};
	$poll_ts	= $hash{1}{poll_ts};
	$poll_ovpl	= $hash{1}{poll_ovpl};
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
	#
	# reset
	$sql = "
	Update
		radio_data_station_channel
	set
		poll_timestamp = now(),
		poll_option_0_count=0,
		poll_option_1_count=0,
		poll_option_2_count=0,
		poll_option_3_count=0,
		poll_option_4_count=0,
		poll_option_5_count=0,
		poll_option_6_count=0,
		poll_option_7_count=0,
		poll_option_8_count=0,
		poll_option_9_count=0
	where
		enabled=1 and id='$channel_id'
	";
	&database_do($sql);
	$sql = "
	Update
		radio_log_session
	set
		poll_last_vote_value = null, poll_votes_count=0
	where
		datetime_stop is null and
		radio_data_station_channel_id = '$channel_id'
	";
	&database_do($sql);
	#
	# start page
	print "content-type: text/html\n\n$sql";

}
sub do_radio_station_now_poll_ovpl_set() {
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,unix_timestamp(poll_timestamp),poll_one_vote_per_listener FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,poll_ts,poll_ovpl");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id	= $hash{1}{station_id};
	$poll_ts	= $hash{1}{poll_ts};
	$poll_ovpl	= $hash{1}{poll_ovpl};
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
	#
	# reset
	$sql = "";
	$sql = ($form{value} eq 1) ? "Update radio_data_station_channel set poll_one_vote_per_listener=1 where enabled=1 and id='$channel_id'" : $sql;
	$sql = ($form{value} eq 0) ? "Update radio_data_station_channel set poll_one_vote_per_listener=0 where enabled=1 and id='$channel_id'" : $sql;
	if ($sql ne "") { &database_do($sql); }
	#
	# start page
	print "content-type: text/html\n\n$sql";

}
sub do_radio_station_now_member_mode(){
	#
	# start
	print "content-type: text/html\n\n";
	#
	# check log_id
	$log_id = &clean_int(substr($form{log_id},0,100));
    %hash = &database_select_as_hash("SELECT 1,1,radio_data_station_id,radio_data_station_channel_id,app_konference_sip_channel,system_host FROM radio_log_session where datetime_stop is null and id='$log_id'","flag,station_id,channel_id,sip,host");
    if ($hash{1}{flag} ne 1) { print "ERROR:Unknown log_id"; return; }
	$station_id	= $hash{1}{station_id};
	$channel_id = $hash{1}{channel_id};
	$sip  		= $hash{1}{sip};
	#$host		= $hash{1}{host};
	$host 		= $hardcoded_call_server;
	$mode 		= (index("|0|1|2|","|$form{mode}|") eq -1) ? 0 : $form{mode};
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { print "ERROR:no permission"; return; }
	#
	# do the magic
	&app_konference_set_channel_mode($host,$sip,$mode);
	#
	# print page
	print "OK\n";
	print "<script>parent.getnextpage();</script>";

}
sub do_radio_station_now_member_flag() {
    if (index("|1|2|3|4|","|$form{flag}|") eq -1) { adm_error("ERROR : Unknown flag_id"); }
    $flag = "flag_".$form{flag};
	$ani = &clean_int(substr($form{ani},0,100));
	$station_id = &clean_int(substr($form{station_id},0,100));
    %hash = &database_select_as_hash("SELECT 1,1 FROM radio_data_station_ani where ani='$ani' and radio_station_id='$station_id' ","flag");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown member_id"); }
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    # change value
	#$value	= &radio_data_station_ani_get($station_id,$ani,$flag);
	#$value = ( ($value eq "1") && ($form{value} eq "toggle") ) ? "0" : $value;
	#$value = ( ($value eq "0") && ($form{value} eq "toggle") ) ? "0" : $value;
	#$value = ($form{value} eq "1") ? "1" : $value;
	#$value = ($form{value} eq "0") ? "0" : $value;
	#&radio_data_station_ani_set($station_id,$ani,$flag,$value);
	#
	# print page
	print "content-type: text/html\n\n";
	print "<script>parent.getpage();</script>";
}
sub do_radio_station_now_member_name() {
    $value 		= &trim(substr(&clean_str($form{value},"SQLSAFE"),0,250));
	$client_id	= &clean_int(substr($form{client_id},0,100));
	$station_id	= &clean_int(substr($form{station_id},0,100));
    %hash = &database_select_as_hash("SELECT 1,1 FROM radio_data_client where id='$client_id' ","flag");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown client_id"); }
	#
	# check permission to this station
	# TODO: CHeck if this client_id belong to this station.
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    # change value
	#&radio_data_station_ani_set($station_id,$ani,"name",$value);
	&radio_data_client_station_set($client_id,$station_id,"name",$value);
	#
	# print page
	print "content-type: text/html\n\n";
	print "<script>parent.getpage();</script>";

}
sub do_radio_station_now_talk_pin(){
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,extension,talk_pin FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,extension,talk_pin");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id	= $hash{1}{station_id};
	$extension 	= $hash{1}{extension};
	$talk_pin 	= $hash{1}{talk_pin};
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    # clean value
    $value = &trim(substr(&clean_str($form{value},"SQLSAFE"),0,250));
    @array=();
    $c=0;
    foreach $tmp (split(/\,/,$value)) {
    	$tmp = substr(&clean_int($tmp),0,20);
    	if ($tmp ne "") {@array = (@array,$tmp)}
    	$c++;if($c>=10) {last}
    }
    $value = join(",",@array);
    #
    # save value
	&database_do("update radio_data_station_channel set talk_pin='$value' where id='$channel_id' ");
	#
	# print page
	print "content-type: text/html\n\n";
	print "<script>parent.getpage();</script>";
}
sub do_radio_station_now_listen_pin(){
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,extension FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,extension");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id	= $hash{1}{station_id};
	$extension 	= $hash{1}{extension};
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    # clean value
    $value = &trim(substr(&clean_str($form{value},"SQLSAFE"),0,250));
    @array=();
    $c=0;
    foreach $tmp (split(/\,/,$value)) {
    	$tmp = substr(&clean_int($tmp),0,20);
    	if ($tmp ne "") {@array = (@array,$tmp)}
    	$c++;if($c>=10) {last}
    }
    $value = join(",",@array);
    #
    # save value
	&database_do("update radio_data_station_channel set listen_pin='$value' where id='$channel_id' ");
	#
	# print page
	print "content-type: text/html\n\n";
	print "<script>parent.getpage();</script>";
}
sub do_radio_station_now_stream_stop(){
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,stream_type,stream_url FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,type,url");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id		= $hash{1}{station_id};
	$stream_type	= $hash{1}{type};
	$stream_url		= $hash{1}{url};
	$host			= $hardcoded_call_server;
	$message = "";
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    # remove approve flag
    #&database_do("update radio_data_station_channel  set stream_approved=0 where id='$channel_id'");
	#
	# stop all system streams
    if ($message eq "") {
		&app_konference_channel_stream_disconnect($host,$channel_id);
    }
	#
	# print page
	print "content-type: text/html\n\n";
	$message = ($message eq "") ? "<img src=design/icons/tick-circle-frame.png align=left> Background audio is disabled." : $message ;
	print qq[
		<script>parent.alertmessage("$message",10);</script>
	];
	print "<script>parent.getpage();</script>";
}
sub do_radio_station_now_stream_volumeup(){
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,stream_type,stream_url FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,type,url");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id		= $hash{1}{station_id};
	$stream_type	= $hash{1}{type};
	$stream_url		= $hash{1}{url};
	$host			= "";
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    # remove approve flag
    #&database_do("update radio_data_station_channel  set stream_approved=0 where id='$channel_id'");
	#
	# volume all system streams
    if ($message eq "") {
		%conference = &app_konference_list($host,$channel_id);
		foreach $id (keys %conference) {
			if ($conference{$id}{type} eq "STREAM") {
				&app_konference_talkvolume_up($host,$conference{$id}{sip_channel});
			}
		}
    }
	#
	# print page
	print "content-type: text/html\n\n";
	print "<script>parent.alertmessage('');</script>";
	print "<script>parent.getpage();</script>";
}
sub do_radio_station_now_stream_volumedown(){
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,stream_type,stream_url FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,type,url");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id		= $hash{1}{station_id};
	$stream_type	= $hash{1}{type};
	$stream_url		= $hash{1}{url};
	$host			= "";
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    # remove approve flag
    #&database_do("update radio_data_station_channel  set stream_approved=0 where id='$channel_id'");
	#
	# volume all system streams
    if ($message eq "") {
		%conference = &app_konference_list($host,$channel_id);
		foreach $id (keys %conference) {
			if ($conference{$id}{type} eq "STREAM") {
				&app_konference_talkvolume_down($host,$conference{$id}{sip_channel});
			}
		}
    }
	#
	# print page
	print "content-type: text/html\n\n";
	print "<script>parent.alertmessage('');</script>";
	print "<script>parent.getpage();</script>";
}
sub do_radio_station_now_stream_start(){
	#
	# check channel id
	$channel_id = &clean_int(substr($form{channel_id},0,100));
    %hash = database_select_as_hash("SELECT 1,1,radio_data_station_id,stream_type,stream_url FROM radio_data_station_channel where enabled=1 and id='$channel_id'","flag,station_id,type,url");
    if ($hash{1}{flag} ne 1) { adm_error("ERROR : Unknown channel_id"); }
	$station_id			= $hash{1}{station_id};
	$stream_type		= $hash{1}{type};
	$stream_url			= $hash{1}{url};
	$stream_url_final	= "ZENOFON:$stream_type:$stream_url";
	$message 			= "";
	$host				= $hardcoded_call_server;
	#
	# check permission to this station
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
    #
    # remove approve flag
    &database_do("update radio_data_station_channel  set stream_approved=0 where id='$channel_id'");
	#
	# check basic
    if ($message eq "") {
    	if (index("|SHOUTCAST|MMS|","|$stream_type|") eq -1) { $message = "<img src=design/icons/exclamation.png align=left> Unknown as stream type. " }
    	if ($stream_url eq "") { $message = "<img src=design/icons/exclamation.png align=left> You need first setup stream url to use as background audio. " }
    }
	#
	# disconnect and reconnect
    if ($message eq "") {
		&app_konference_channel_stream_disconnect($host,$channel_id);
		&app_konference_channel_stream_connect($host,$channel_id);
    }
    #
    # check if already connected
    #if ($message eq "") {
	#	$qtds = 0;
	#	%conference = &app_konference_list($host,$channel_id);
	#	foreach $id (keys %conference) {
	#		if ($conference{$id}{type} eq "STREAM") {
	#			$qtds++;
	#		}
	#	}
    #	if ($qtds eq 1) { $message = "<img src=design/icons/tick-circle-frame.png align=left> Background audio is already running" }
    #	elsif ($qtds > 1) { $message = "<img src=design/icons/exclamation.png align=left> System error. Cannot start background audio." }
    #}
    #
    # connect
    if ($message eq "") {
		$ans = &app_konference_channel_stream_connect($host,$channel_id);
    }
	#
	# wait and check
    if ($message eq "") {
		sleep(15);
		$qtds = 0;
		%conference = &app_konference_list($host,$channel_id);
		foreach $id (keys %conference) {
			if ($conference{$id}{type} eq "STREAM") {
				$qtds++;
			}
		}
    	if ($qtds eq 0) {
    		$message = "<img src=design/icons/exclamation.png align=left> I cannot start $stream_url_final stream as background audio. Please check this URL ";
    	}
    	elsif ($qtds > 1) {
    		$message = "<img src=design/icons/exclamation.png align=left> System error. Cannot start background audio."
    	}
    }
	#
	# print page
	print "content-type: text/html\n\n";
	if ($message eq "") {
	    &database_do("update radio_data_station_channel set stream_approved=1 where id='$channel_id'");
		$message =  "<img src=design/icons/tick-circle-frame.png align=left> Background audio is running";
	}
	print qq[
		<script>parent.alertmessage("$message",10);</script>
	];
	print "<script>parent.getpage();</script>";
}
sub do_radio_station_prompt_list(){
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
    #----------------------------------
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
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

	<div id="navigation_tab" style="margin-bottom:5px;">
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
	</div>
	<div id="navigation_tab" style="margin-bottom:20px;">
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" >General</a>
		<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" >Channels</a>
		<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id"  class=selected >Prompts</a>
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
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
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
    $t{content}		.= qq[

	<div id="navigation_tab" style="margin-bottom:5px;">
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
	</div>
	<div id="navigation_tab" style="margin-bottom:20px;">
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" >General</a>
		<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" >Channels</a>
		<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id"  class=selected >Prompts</a>
	</div>

    <fieldset style="width:350px;">$html_form</fieldset><br>

    ];
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
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
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
						$cmd = "/usr/bin/sox -t mp3 $temp_file -r 8000 -c1 -t gsm $temp_file_gsm resample -ql 2>\&1 ";
						$ans = `$cmd`;
						$ans = &cgi_mime_get_from_file($temp_file_gsm);
					} elsif ($temp_file_mime eq "audio/x-wav") {
						$cmd = "/usr/bin/sox -t wav $temp_file -r 8000 -c1 -t gsm $temp_file_gsm resample -ql 2>\&1 ";
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
						    $error_message = "I cannot convert or understand this file.";
			    		}
					}
				}
				#
				# clean
				unlink($temp_file);
				unlink($temp_file_gsm);
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
		$error_message = "<div class=alert_box ><div class=alert_box_inside style='background-image:url(/noc/design/icons/exclamation.png);padding-left:22px;'>$error_message</div></div><br>";
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

	<div id="navigation_tab" style="margin-bottom:5px;">
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
	</div>

	<div id="navigation_tab" style="margin-bottom:20px;">
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" >General</a>
		<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" >Channels</a>
		<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id"  class=selected >Prompts</a>
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
		function update_upload_data(){
			value = document.forms[0].elements[3].selectedIndex;
			if (value == "2") {MyDisplay('upload_data',1)} else {MyDisplay('upload_data',0)}
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
		<!--    			<option $record_mode_is_phone  value='phone'>Record prompt by phone</option>  -->
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
	    	<button class=cancel type=button onclick="window.location='$my_url?action=radio_station_prompt_list&station_id=$station_id'">Cancel</button>
	    	<button class=cancel type=button onclick="window.location='$my_url?action=radio_station_prompt_del&prompt_id=$prompt_id'">Delete</button>
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
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
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
    $t{content}		.= qq[

	<div id="navigation_tab" style="margin-bottom:5px;">
		<a href="$my_url?action=radio_station_list" style="float:right;">Close X</a>
		<a href="$my_url?action=radio_station_now&station_id=$station_id" >Radio now</a>
		<a href="$my_url?action=radio_station_history&station_id=$station_id" >History</a>
		<a href="$my_url?action=radio_station_clients&station_id=$station_id" >Clients</a>
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" class=selected >Settings</a>
	</div>
	<div id="navigation_tab" style="margin-bottom:20px;">
		<a href="$my_url?action=radio_station_settings&station_id=$station_id" >General</a>
		<a href="$my_url?action=radio_station_channel_list&station_id=$station_id" >Channels</a>
		<a href="$my_url?action=radio_station_prompt_list&station_id=$station_id"  class=selected >Prompts</a>
	</div>

    	<fieldset style="width:350px;">$html_form</fieldset><br>

    ];
	&template_print("template.html",%t);
}
sub do_radio_station_prompt_play(){
	$id  = &clean_int(substr($form{id},0,100));
	#
	# TODO: add permission. Get station_id and match in permission for this user.
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
sub do_radio_station_prompt_wait_record(){
	print "content-type: text/html\n\n";
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
    # check permission
    #----------------------------------
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
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



#####migrate from v1######
sub do_channel_updown {
	$mode	  = $form{mode} || 0; #down: 1, up: other
	$streamid   = clean_int($form{channel_id});
	$extension = clean_int($form{extension});
	$stationid = clean_int($form{stationid});
	#
	# TODO: WARNING Security flaw!
	# we need check if the active user has right to edit this chanel date
	# right now, anyone at zenofon can change any channel.. can change they channels and OTHER people channels
	# user permission is per station, so, with channel_id you need find station_id and then check user permission at this station_id
	# you can check 3 first blocks at do_radio_station_channel_del action
	# first block: try to read channel dataitem* with this channel_id
	# second block: try to read station dataitem with station_id comes from above channel dataitem
	# 3rd block: Check if active user has right to access this station
	#
	# dataitem its a internal zenofon API that we define one "object" and use this object manage data (add/edit/delete) and control webforms
	# We did it, because we always write the same code and logic over and over ... dataitem helpus to avoid this over work
	# webforms for data itens are veeery secure. they protect form many things like people create urls and try force users execute actions. Webforms always check before save (second interaction), if user realy saw the form (first interaction)
	# and also make easy to change all aplication by just change dataitem apis
	# example: If we change dataitem api that handle edit web form, we change form ALL application.
	# check do_radio_station_prompt_add for add example,
	# check do_radio_station_prompt_del for delete example
	# check do_radio_station_edit for edit example
	# check define_all_data_itens at begin to see all dataitens config that we have in this cgi. (I just add in sub to help fold/unfold at komodo edit)
	#
	%hash = database_select_as_hash("select 1, radio_data_station_id,extension from radio_data_station_channel where id='$streamid'","stationid,extension");
	#
	# TODO: protect from bad data
	# if some one send a invalid channel, system will accept and maybe bad things can hapen.
	# will take long time to understand that data corruption comes from this lack of check plus a client send random urls
	# We need check if this channel_id is REALY available.
	# Best way to do is create a dummy data and if we get this data, means the query run fine and channel id is valid
	# proto code its like this:
	# %hash = database_select_as_hash("select 1,1,value1,value2 from table where id='$id'","flag,value1,value2");
	# if ($hash{1}{flag} ne 1) {refresh_url("back to where come from"); exit;}
	# if query runs, $hash{1}{flag} will always 1, so we can use it as flag if this is valid or not
	#
	$extension = $hash{1}{extension};
	$stationid = $hash{1}{stationid};
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
	refresh_url("$my_url?action=radio_station_channel_list&station_id=$stationid");
}

sub do_radio_listen () {
	$id  = clean_int($form{'id'});
	%radio = database_select_as_hash("select id,stream_url,title from radio_data_station_channel where id='$id'", 'url,title');
	# TODO: protect from bad data (same as channelupdown)
	# TODO: future problems. Dows this "object id=wmp" understand podcasts? we gonna have podcasts url in future
	# TODO: only works on windows? no osx/linux/android/iphone/etc etc?
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

sub get_stream_search_html {
	#
	# TODO: What is tag? we dont have anything about tag at version2 data model.
	# Is this something at version1 that we dont map at version2 draft? we ned know to understand
	# as i see, we create tags connected to user. If we delete a user, all tags goes away. If we create one tag with one user, other users that also own this radio will not see. Is this what we want?
	#
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

sub do_upload_logo {
	$station_id = &clean_int($form{station_id});
    if (&check_access_to_this_station($station_id) ne 1) { adm_error("ERROR : No permission to access this radio station"); }
	$fname = time;
	
	$fname = save_file('logo', $fname);
	if ($fname) {
		database_do("update radio_data_station set logo='$fname' where id='$station_id'");		
	}

	refresh_url("$my_url?action=radio_station_edit&station_id=$station_id");
}

sub save_file() {
	($field, $id, $t) = @_;
	$name = $form{$field};
	return if !$name;

	($n, $postfix) = $name =~ m{([^\\\/]+?)\.([^\\\/]+)$};
	$postfix ||= '';

	$fh  = $cgi->upload($field);

	$id	 = "R$id" if $t;
  # undef may be returned if it's not a valid file handle
	if (defined $fh) {
   		my $io = $fh->handle;
		open (OUTFILE, '>', "files/$id.$postfix");
		while ($bytesread = $io->read($buffer,1024)) {
			print OUTFILE $buffer;
		}

		return "files/$id.$postfix";
	}

	return;
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


#=======================================================



