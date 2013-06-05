#!/usr/bin/perl
#=======================================================
# manage web users for NOC system
#=======================================================
# manage users and set permission groups.
#=======================================================

require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
unless (&active_user_permission_check("user.manager") eq 1) {adm_error("no permission"); exit;}
#=======================================================


#=======================================================
# create dataitem specifications
#=======================================================    
&define_all_data_itens(); # i create a sub just to easy fold code... dont need be inside a sub
sub define_all_data_itens() {  
	#--------------------------------
	%hash = ();
	$hash{title}						= "NOC user";
	$hash{sql_key}						= "SELECT 1 FROM system_user where id=#KEY# ";
	$hash{sql_del}						= "delete from system_user where id=#KEY# ";
	$hash{sql_del_1}					= "delete from system_user_data where target=#KEY# ";
	$hash{sql_add}						= "insert into system_user (creation_date) values (now()) ";
	$tmp=0;
	$hash{items}{$tmp}{title}			= "Login";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT web_user FROM system_user where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update system_user set web_user=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}	= "Please select user login";
	$tmp++;
	$hash{items}{$tmp}{title}			= "Password";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{sql_get}			= "SELECT '' FROM system_user where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update system_user set web_password=IF(LENGTH(#VALUE#)>1, concat('_',MD5(concat(#VALUE#,web_user))) , web_password) where id=#KEY# ";
	$hash{items}{$tmp}{error_message}	= "Enter new password";
	$tmp++;
	$hash{items}{$tmp}{title}			= "Permission&nbsp;level";
	$hash{items}{$tmp}{type}			= "SELECT";
	$hash{items}{$tmp}{options_sql}		= "SELECT id,title FROM system_user_group ORDER BY ui_order ";
	$hash{items}{$tmp}{sql_get}			= "SELECT group_id FROM system_user where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update system_user set group_id=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}	= "PLease select user group";
	$tmp++;
	$hash{items}{$tmp}{title}			= "Owned radios";
	$hash{items}{$tmp}{type}			= "MULTISELECT";
	$hash{items}{$tmp}{flags}			= "ALLOW_EMPTY";
	$hash{items}{$tmp}{options_sql}		= "SELECT id,title FROM radio_data_station order by title ";
	$hash{items}{$tmp}{sql_before_set}	= "delete from radio_data_station_owner where system_user_id=#KEY# ";
	$hash{items}{$tmp}{sql_get}			= "SELECT 1 FROM radio_data_station_owner where system_user_id=#KEY# and radio_data_station_id=#OPTIONID# ";
	$hash{items}{$tmp}{sql_set}			= "insert into radio_data_station_owner (system_user_id,radio_data_station_id) values (#KEY#,#OPTIONID#)  ";
	$hash{items}{$tmp}{sql_unset}		= "delete FROM radio_data_station_owner where system_user_id=#KEY# and radio_data_station_id=#OPTIONID# ";
	$tmp++;
	$hash{items}{$tmp}{title}			= "Contact name";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT name FROM system_user where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update system_user set name=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}	= "Please select contact name";
	$tmp++;
	$hash{items}{$tmp}{title}			= "Contact email";
	$hash{items}{$tmp}{type}			= "STRING";
	$hash{items}{$tmp}{sql_get}			= "SELECT email FROM system_user where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}			= "update system_user set email=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}	= "Please select contact email";
	%dataitemconfig_user = %hash;
}
#=======================================================



#=======================================================
# main loop
#=======================================================    
$my_url = "user.manager.cgi";
$action = $form{action};
if 		($action eq "system_user_list")			{ &do_system_user_list();				}
elsif 	($action eq "system_user_add")			{ &do_system_user_add();				}
elsif 	($action eq "system_user_del")			{ &do_system_user_del();				}
elsif 	($action eq "system_user_edit")			{ &do_system_user_edit();				}
else											{ &do_system_user_list();				}
exit;
#=======================================================



#=======================================================
# actions
#=======================================================
sub do_system_user_list(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM system_user ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Last change on top";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM system_user order by timestamp desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Order by login";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM system_user order by web_user limit #LIMIT_1#,#LIMIT_2# ";
    $datatable{sql}{col_names}			= "id,web_user,name,email,group"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= qq[
		SELECT 
			u.id,
			u.id,
			u.web_user,
			u.name,
			u.email, 
			(select g.title from system_user_group as g where u.group_id=g.id limit 0,1)
		FROM 
			system_user as u
		where 
			u.id in (#SELECTED_IDS#)  
	];
	# filter ids by page and order
	# html values	
    #$datatable{html}{title}					= "'".$station_object{data}{items}{0}{value}."' extensions";
    $datatable{html}{col_names}				= "web_user,name,email,group";
    $datatable{html}{col_titles}			= "Login,Contact name,Contact email,Permission group";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "system_user_list";
    $datatable{html}{line_click_link}		= "$my_url?action=system_user_edit&user_id=#ID#";
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
    $t{title}	= "List users";
    $t{content}	= qq[ 
    	$datatable_html 
    	<br>
    	<a href=$my_url?action=system_user_add>&#187; Add new user</a>
    ];
    &template_print("template.html",%t);
	
}
sub do_system_user_password(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_user;
	$my_dataitem{data}{key}  = &clean_int(substr($form{user_id},0,100));
	&dataitem_initialize(\%my_dataitem);
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
	# TODO: block edit loged-in user (to avoid lock out problem)
	
}
sub do_system_user_edit(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_user;
	$my_dataitem{data}{key}  = &clean_int(substr($form{user_id},0,100));
	&dataitem_initialize(\%my_dataitem);
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
	# TODO: block edit loged-in user (to avoid lock out problem)
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{url_button_cancel}	= "$my_url?action=system_user_list&user_id=$my_dataitem{data}{key}";
    $form_settings{url_button_delete}	= "$my_url?action=system_user_del&user_id=$my_dataitem{data}{key}";
    $form_settings{url_form_ok}			= "$my_url?action=system_user_list&user_id=$my_dataitem{data}{key}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "system_user_edit";
    $form_settings{hidden_elements}{2}{name}	= "user_id";
    $form_settings{hidden_elements}{2}{value}	= $my_dataitem{data}{key};
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_editform_process(\%my_dataitem,\%form_settings,\%form);
	# TODO: check duplicate login
	# TODO: logout user if change group
	$html_form = &dataitem_web_editform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}		= $my_url;
    $t{title}		= "Edit user";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
sub do_system_user_add(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_user;
	&dataitem_initialize(\%my_dataitem);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{url_button_cancel}	= "$my_url?action=system_user_list";
    $form_settings{url_form_ok}			= "$my_url?action=system_user_list";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "action";
    $form_settings{hidden_elements}{0}{value}	= "system_user_add";
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
    $t{title}	= "Add new user";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
	
}
sub do_system_user_del(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_user;
	&dataitem_initialize(\%my_dataitem);
	$my_dataitem{data}{key}  = &clean_int(substr($form{user_id},0,100));;
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{url_button_cancel}	= "$my_url?action=system_user_edit&user_id=$my_dataitem{data}{key}";
    $form_settings{url_form_ok}			= "$my_url?action=system_user_stream_list&user_id=$my_dataitem{data}{key}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete '$my_dataitem{data}{items}{0}{value} ($my_dataitem{data}{items}{3}{value})' user?</b> This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "action";
    $form_settings{hidden_elements}{0}{value}	= "system_user_del";
    $form_settings{hidden_elements}{1}{name}	= "user_id";
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
    $t{title}	= "Delete user";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);

}
#=======================================================



