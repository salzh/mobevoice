#!/usr/bin/perl
#=======================================================
# manage permission groups 
#=======================================================
# all system use permission groups to allow/reject webusers
# access to any resource.
# This CGI manage permission groups.
# This data its half hard-coded (we check data in code)
# and half database data (to store groups and assign to user)
# To avoid problems, we only ONE user with master permission
# can accesss this settings over web.
#=======================================================
require "include.cgi";




#=======================================================
# logout if no session
#=======================================================
unless ($app{session_status} eq 1) {cgi_redirect("index.cgi");exit;}
unless (&active_user_permission_check("user.group.manager") eq 1) {adm_error("no permission"); exit;}
#=======================================================


#=======================================================
# create dataitem specifications
#=======================================================    
$default_group_id = 0;
&define_all_data_itens(); # i create a sub just to easy fold code... dont need be inside a sub
sub define_all_data_itens() {  
	#--------------------------------
	%hash = ();
	$hash{title}						= "Permission level";
	$hash{sql_key}						= "SELECT 1 FROM system_user_group where id=#KEY# ";
	$hash{sql_del}						= "delete from system_user_group where id=#KEY# ";
	$hash{sql_del_1}					= "delete from system_user_group_permission_value where group_id=#KEY# ";
	$hash{sql_del_1}					= "update system_user set group_id=null where group_id=#KEY# ";
	$hash{sql_add}						= "insert into system_user_group (date_add) values (now()) ";
	$hash{sql_edit_before}				= "";
	$hash{sql_edit_after}				= "";
	$tmp=0;
	$hash{items}{$tmp}{title}				= "Title";
	$hash{items}{$tmp}{type}				= "STRING";
	$hash{items}{$tmp}{sql_get}				= "SELECT title FROM system_user_group where id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "update system_user_group set title=#VALUE# where id=#KEY# ";
	$hash{items}{$tmp}{error_message}		= "Please select group title";
	$tmp++;
	$hash{items}{$tmp}{group}				= "Basic permission";
	$hash{items}{$tmp}{title}				= "Web access";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{flags}				= "USE_DEFAULT_VALUE_IF_EMPTY,ALLOW_EMPTY";
	$hash{items}{$tmp}{default_value}		= "0";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "No";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
	$hash{items}{$tmp}{options}{1}{title}	= "Yes";
	$hash{items}{$tmp}{sql_get}				= "SELECT value from system_user_group_permission_value where dictionary_id='user.webaccess' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "delete from system_user_group_permission_value where dictionary_id='user.webaccess' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set_1}			= "insert into system_user_group_permission_value (dictionary_id,group_id,value) values ('user.webaccess',#KEY#,#VALUE#)  ";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Account profile access";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{flags}				= "USE_DEFAULT_VALUE_IF_EMPTY,ALLOW_EMPTY";
	$hash{items}{$tmp}{default_value}		= "0";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "No";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
	$hash{items}{$tmp}{options}{1}{title}	= "Yes";
	$hash{items}{$tmp}{sql_get}				= "SELECT value from system_user_group_permission_value where dictionary_id='user.profile' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "delete from system_user_group_permission_value where dictionary_id='user.profile' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set_1}			= "insert into system_user_group_permission_value (dictionary_id,group_id,value) values ('user.profile',#KEY#,#VALUE#)  ";
	$tmp++;
	$hash{items}{$tmp}{group}				= "Radio station permission";
	$hash{items}{$tmp}{title}				= "Settings";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{flags}				= "USE_DEFAULT_VALUE_IF_EMPTY,ALLOW_EMPTY";
	$hash{items}{$tmp}{default_value}		= "0";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "Only radios they own";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
 	$hash{items}{$tmp}{options}{1}{title}	= "Access ALL radios";
	$hash{items}{$tmp}{sql_get}				= "SELECT value from system_user_group_permission_value where dictionary_id='radio.manager' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "delete from system_user_group_permission_value where dictionary_id='radio.manager' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set_1}			= "insert into system_user_group_permission_value (dictionary_id,group_id,value) values ('radio.manager',#KEY#,#VALUE#)  ";
	$tmp++;
	$hash{items}{$tmp}{group}				= "Advanced permission";
	$hash{items}{$tmp}{title}				= "Manage accounts";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{flags}				= "USE_DEFAULT_VALUE_IF_EMPTY,ALLOW_EMPTY";
	$hash{items}{$tmp}{default_value}		= "0";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "No";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
	$hash{items}{$tmp}{options}{1}{title}	= "Yes";
	$hash{items}{$tmp}{sql_get}				= "SELECT value from system_user_group_permission_value where dictionary_id='user.manager' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "delete from system_user_group_permission_value where dictionary_id='user.manager' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set_1}			= "insert into system_user_group_permission_value (dictionary_id,group_id,value) values ('user.manager',#KEY#,#VALUE#)  ";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Manage account permissions";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{flags}				= "USE_DEFAULT_VALUE_IF_EMPTY,ALLOW_EMPTY";
	$hash{items}{$tmp}{default_value}		= "0";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "No";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
	$hash{items}{$tmp}{options}{1}{title}	= "Yes";
	$hash{items}{$tmp}{sql_get}				= "SELECT value from system_user_group_permission_value where dictionary_id='user.group.manager' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "delete from system_user_group_permission_value where dictionary_id='user.group.manager' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set_1}			= "insert into system_user_group_permission_value (dictionary_id,group_id,value) values ('user.group.manager',#KEY#,#VALUE#)  ";
	$tmp++;
	$hash{items}{$tmp}{title}				= "Manage system settings";
	$hash{items}{$tmp}{type}				= "SELECT";
	$hash{items}{$tmp}{flags}				= "USE_DEFAULT_VALUE_IF_EMPTY,ALLOW_EMPTY";
	$hash{items}{$tmp}{default_value}		= "0";
	$hash{items}{$tmp}{options}{0}{value}	= "0";
	$hash{items}{$tmp}{options}{0}{title}	= "No";
	$hash{items}{$tmp}{options}{1}{value}	= "1";
	$hash{items}{$tmp}{options}{1}{title}	= "Yes";
	$hash{items}{$tmp}{sql_get}				= "SELECT value from system_user_group_permission_value where dictionary_id='system.manager' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set}				= "delete from system_user_group_permission_value where dictionary_id='system.manager' and group_id=#KEY# ";
	$hash{items}{$tmp}{sql_set_1}			= "insert into system_user_group_permission_value (dictionary_id,group_id,value) values ('system.manager',#KEY#,#VALUE#)  ";
	%dataitemconfig_group = %hash;
}
#=======================================================



#=======================================================
# main loop
#=======================================================    
$my_url = "user.group.manager.cgi";
$action = $form{action};
if 		($action eq "system_group_list")		{ &do_system_group_list();				}
elsif 	($action eq "system_group_add")			{ &do_system_group_add();				}
elsif 	($action eq "system_group_del")			{ &do_system_group_del();				}
elsif 	($action eq "system_group_edit")		{ &do_system_group_edit();				}
else											{ &do_system_group_list();				}
exit;
#=======================================================



#=======================================================
# actions
#=======================================================
sub do_system_group_list(){
    #
    #-------------------------------
    # prepare datatable 
    #-------------------------------
	%datatable = ();
	$datatable{sql}{filter_ids_with_no_search}{get_total} = "SELECT count(*) FROM system_user_group  ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{title} 	= "Last change on top";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{0}{sql} 	= "SELECT id FROM system_user_group order by date_last_change desc limit #LIMIT_1#,#LIMIT_2# ";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{title} 	= "Order by title";
	$datatable{sql}{filter_ids_with_no_search}{order_by}{1}{sql} 	= "SELECT id FROM system_user_group order by web_user limit #LIMIT_1#,#LIMIT_2# ";
    $datatable{sql}{col_names}			= "id,title,count"; # first collumn is the unique key and cannot be addressed in data table. If we need this value, repeat this value in anther collumn
	$datatable{sql}{get_data} 			= "
		SELECT 
			g.id,
			g.id,
			g.title,
			(select count(*) from system_user as u where u.group_id=g.id limit 0,1) 
		FROM 
			system_user_group  as g
		where 
			g.id in (#SELECTED_IDS#)  
	";
	# filter ids by page and order
	# html values	
    #$datatable{html}{title}					= "'".$station_object{data}{items}{0}{value}."' extensions";
    $datatable{html}{col_names}				= "title,count";
    $datatable{html}{col_titles}			= "Permission level,Users count";
	$datatable{html}{message_empty_list}	= "Nothing in the list...";
    $datatable{html}{form}{action}			= "$my_url";
    $datatable{html}{form}{data}{0}{name}	= "action";
    $datatable{html}{form}{data}{0}{value}	= "system_group_list";
    $datatable{html}{line_click_link}		= "$my_url?action=system_group_edit&group_id=#ID#";
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
    $t{title}	= "List permission levels";
    $t{content}	= qq[ 
    	$datatable_html 
    	<br>
    	<a href=$my_url?action=system_group_add>&#187; Add new group</a>
    ];
    &template_print("template.html",%t);
	
}
sub do_system_group_edit(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_group;
	$my_dataitem{data}{key}  = &clean_int(substr($form{group_id},0,100));
	&dataitem_initialize(\%my_dataitem);
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
	# TODO: block edit loged-in group (to avoid lock out problem)
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "EDIT";
    $form_settings{url_button_cancel}	= "$my_url?action=system_group_list&group_id=$my_dataitem{data}{key}";
    $form_settings{url_button_delete}	= "$my_url?action=system_group_del&group_id=$my_dataitem{data}{key}";
    $form_settings{url_form_ok}			= "$my_url?action=system_group_list&group_id=$my_dataitem{data}{key}";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{1}{name}	= "action";
    $form_settings{hidden_elements}{1}{value}	= "system_group_edit";
    $form_settings{hidden_elements}{2}{name}	= "group_id";
    $form_settings{hidden_elements}{2}{value}	= $my_dataitem{data}{key};
    #
    #----------------------------------
    # process form
    #----------------------------------
	&dataitem_web_editform_process(\%my_dataitem,\%form_settings,\%form);
	# TODO: refresh user permissions belong to this group
	$html_form = &dataitem_web_editform_gethtml(\%my_dataitem,\%form_settings,\%form);
    #
    #----------------------------------
    # print page
    #----------------------------------
    %t = &menu_permissions_get_as_template();
    $t{my_url}		= $my_url;
    $t{title}		= "Edit permission level";
    $t{content}		.= qq[<fieldset style="width:450px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
}
sub do_system_group_add(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_group;
	&dataitem_initialize(\%my_dataitem);
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "ADD";
    $form_settings{url_button_cancel}	= "$my_url?action=system_group_list";
    $form_settings{url_form_ok}			= "$my_url?action=system_group_list";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{hidden_elements}{0}{name}	= "action";
    $form_settings{hidden_elements}{0}{value}	= "system_group_add";
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
    $t{title}	= "Add new group";
    $t{content}		.= qq[<fieldset style="width:450px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);
	
}
sub do_system_group_del(){
    #
    #----------------------------------
    # prepare dataitem and check 
    #----------------------------------
	%my_dataitem = ();
	%{$my_dataitem{config}} = %dataitemconfig_group;
	&dataitem_initialize(\%my_dataitem);
	$my_dataitem{data}{key}  = &clean_int(substr($form{group_id},0,100));;
	unless (&dataitem_get(\%my_dataitem)) {adm_error("ERROR: $my_dataitem{status_message}");}
    #
    #----------------------------------
    # set form settings
    #----------------------------------
    %form_settings = ();
    $form_settings{flags}				= "REDIRECT_IF_OK";
    $form_settings{mode}				= "DEL";
    $form_settings{url_button_cancel}	= "$my_url?action=system_group_edit&group_id=$my_dataitem{data}{key}";
    $form_settings{url_form_ok}			= "$my_url?action=system_group_list";
    $form_settings{url_form_action}		= "$my_url";
    $form_settings{message}				= "Do you really want <b>delete '$my_dataitem{data}{items}{0}{value}' group?</b> All users belong to this will be with no group and by default, disabled. This is a no undo action.";
    $form_settings{hidden_elements}{0}{name}	= "action";
    $form_settings{hidden_elements}{0}{value}	= "system_group_del";
    $form_settings{hidden_elements}{1}{name}	= "group_id";
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
    $t{title}	= "Delete permission level";
    $t{content}		.= qq[<fieldset style="width:350px;">$html_form</fieldset><br>];
	&template_print("template.html",%t);

}
#=======================================================



