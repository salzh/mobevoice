#!/usr/bin/perl
#=======================================================
# system wide settings
#=======================================================
# multiple system wide settings will live here in this cgi
# at moment we only have DID->radio_station actions
#=======================================================
require "include.cgi";



#=======================================================
# logout if no session
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("system.manager") ne 1) {adm_error("no permission"); exit;}
#=======================================================


#=======================================================
# create dataitem specifications
#=======================================================    
%dataitemconfig_didsettings = ();
&define_all_data_itens(); # i create a sub just to easy fold code... dont need be inside a sub
sub define_all_data_itens() {  
	#--------------------------------
	%hash = ();
	$hash{title}						= "DID settings";
	$hash{sql_key}						= "SELECT 1 FROM radio_data_did where id=#KEY# ";
	$hash{sql_del}						= "delete from radio_data_did where id=#KEY# ";
	$hash{sql_add}						= "insert into radio_data_did (title) values ('New DID') ";
	$tmp = 0;
	$hash{items}{$tmp}{title}			= "DID title";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT title FROM radio_data_did where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_did set title=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}	= "Enter friendly name for this DID";
	$tmp++;
	$hash{items}{$tmp}{title}			= "DID number (E164 only digits)";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{flags}			= "ONLY_SET_IF_NOT_EMPTY,ALLOW_EMPTY";
	$hash{items}{$tmp}{sql_get}			= "SELECT did FROM radio_data_did where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_did set did=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}	= "Enter E164 DID number with only digits";
	$tmp++;
	$hash{items}{$tmp}{title}			= "Radio station";
	$hash{items}{$tmp}{type}			= "SELECT";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{options_first} 	= "(Radio station not assigned)";
	$hash{items}{$tmp}{options_sql}		= "SELECT id,title FROM radio_data_station ORDER BY title ";
	$hash{items}{$tmp}{sql_get}			= "SELECT radio_data_station_id FROM radio_data_did where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update radio_data_did set radio_data_station_id=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}	= "Select radio station assigned to this DID";
	%dataitemconfig_didsettings = %hash;
}
#=======================================================





#=======================================================
# main loop
#=======================================================    
$my_url = "system.settings.cgi";
$action = $form{action};
if 		($action eq "did_list")			{ &do_did_list();				}
elsif 	($action eq "did_add")			{ &do_did_add();				}
elsif 	($action eq "did_del")			{ &do_did_del();				}
elsif 	($action eq "did_edit")			{ &do_did_edit();				}
else									{ &do_did_list();				}
exit;
#=======================================================



#=======================================================
# actions
#=======================================================
sub do_did_list(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM radio_data_did ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM radio_data_did order by title asc limit #LIMIT_1#,#LIMIT_2# ";
    $datatable{sql}{col_names}			= "id,title,did,station"; # first collumn is the unique key and cannot be addressed in data table. If we need this collumn
    $datatable{sql}{get_data} 			= "
		SELECT 
			did.id,
			did.id,
			did.title,
			did.did,
			(select station.title from radio_data_station as station where station.id=did.radio_data_station_id limit 0,1) 
		FROM 
			radio_data_did as did
		where 
			id in (#SELECTED_IDS#)  
	";
    $datatable{html}{col_names}				= "title,did,station";
    $datatable{html}{col_titles}			= "DID title,E164 number,Assigned radio station";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "did_list";
    $datatable{html}{line_click_link}		= "$my_url?action=did_edit&did_id=#ID#";
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
    %t = &menu_permissions_get_as_template();
    $t{my_url}	= $my_url;
    $t{title}	= "List DIDs";
    $t{content}	= qq[ 
    	$datatable_html 
    	<br>
    	<a href=$my_url?action=did_add>&#187; Add new DID</a>
    ];
    &template_print("template.html",%t);
	
}
sub do_did_edit(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_didsettings;
	$my_dataitem{data}{key}  = &clean_int(substr($form{did_id},0,100));
	&dataitem_initialize(\%my_dataitem);
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{url_button_cancel}	= "$my_url?action=did_list&did_id=$my_dataitem{data}{key}";
    $form_settings{url_button_delete}	= "$my_url?action=did_del&did_id=$my_dataitem{data}{key}";
    $form_settings{url_form_ok}			= "$my_url?action=did_list&did_id=$my_dataitem{data}{key}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "did_edit";
    $form_settings{hidden_elements}{2}{name}	= "did_id";
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
    $t{my_url}		= $my_url;
    $t{title}		= "Edit DID";
    $t{content}		.= qq[<fieldset style="width:450px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
sub do_did_add(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_didsettings;
	&dataitem_initialize(\%my_dataitem);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{url_button_cancel}	= "$my_url?action=did_list";
    $form_settings{url_form_ok}			= "$my_url?action=did_list";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "action";
    $form_settings{hidden_elements}{0}{value}	= "did_add";
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
    $t{title}	= "Add new DID";
    $t{content}		.= qq[<fieldset style="width:450px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
	
}
sub do_did_del(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_didsettings;
	&dataitem_initialize(\%my_dataitem);
	$my_dataitem{data}{key}  = &clean_int(substr($form{did_id},0,100));;
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{url_button_cancel}	= "$my_url?action=did_edit&did_id=$my_dataitem{data}{key}";
    $form_settings{url_form_ok}			= "$my_url?action=did_list&did_id=$my_dataitem{data}{key}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete '$my_dataitem{data}{items}{0}{value} ($my_dataitem{data}{items}{1}{value})' DID?</b> This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "action";
    $form_settings{hidden_elements}{0}{value}	= "did_del";
    $form_settings{hidden_elements}{1}{name}	= "did_id";
    $form_settings{hidden_elements}{1}{value}	= $my_dataitem{data}{key};
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
    $t{title}	= "Delete DID";
    $t{content}		.= qq[<fieldset style="width:450px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);

}
#=======================================================



