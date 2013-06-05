#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_view_reports") ne 1) {adm_error("no permission"); exit;}
#=======================================================


#=======================================================
# main loop
#=======================================================
$my_url = "status.cgi";
$action = $form{action};
if    ($action eq "money_overview")		{ &do_index();	}
elsif ($action eq "calls_overview")		{ &do_index();	}
elsif ($action eq "calls_country")		{ &do_index();	}
else 									{ &do_index();	}
exit;
#=======================================================



#========================================================================
# outras acoes
#========================================================================
sub do_index(){
    %t = ();
    $t{dic}{title}		= "Workgroup";
    $t{dic}{content}	.= qq[
    Vamos tentar status
    ];
	&template_print("template.html",%t);
}
#=======================================================



