#!/usr/bin/perl
#=======================================================
# inicializa perl e dependencias inicializa umas coisa
# que vou usar a frente, verifica login secao, user, etc etc
#=======================================================
use CGI;
use HTML::Template; 
use HTTP::Request::Common qw( POST );
%app = ();
require "/usr/local/multilevel/default.include.pl";
#
#------------------------------------
# hack $template_folder to match correct folder in correct webhost
#------------------------------------
$template_folder = "$app_root/www/design/";
#$template_folder = (index($ENV{SERVER_NAME},".dial2skype.com") ne -1) ? "$app_root/www/design.dial2skype/" : $template_folder ;
#print "content-type: text/html\n\n"; foreach (sort keys %ENV) {print "$_=$ENV{$_}<br>";} exit;
#------------------------------------
#
$app{users_table}				= "service";
$app{users_col_id}				= "id";
$app{users_options_table}		= "service_data";
$app{session_table}				= "service_session";
$app{session_cookie_k_name}		= "sk";
$app{session_cookie_u_name}		= "su";
$app{session_logout_on_timeout} = 1;
$app{session_timeout_seconds}	= 60*30*99;
$app{session_active_service_id}	= "";
$app{session_status}			= 0;
$app{use_imagecheck}			= 1;
$cgi 							= new CGI;
%today 							= &get_today();
%form							= (); for $a ($cgi->param) {$v = $cgi->param($a);$form{$a} = &trim($v);}
%cookie							= &cookie_read();
%template_default				= ();
$app{session_status}			= &session_init();
if ($app{session_status} eq 1) {
	$app{service_id}			= &clean_int(substr($app{session_cookie_u},0,100));
	$app{service_name}			= &session_get($app{session_cookie_k},"service_name");
	$app{service_email}			= &session_get($app{session_cookie_k},"service_email");
	$app{service_ani}			= &session_get($app{session_cookie_k},"service_ani");
	$app{service_ani_e164}		= &session_get($app{session_cookie_k},"service_ani_e164");
	$app{service_alert}			= &session_get($app{session_cookie_k},"service_alert");
	$app{service_credits}		= 0;
	#$app{service_credits_bar}	= 0;
	%hash = &database_select_as_hash("select 1,1,balance,service.limit from service where id='$app{service_id}' ","flag,balance,limit");
	if ($hash{1}{flag} eq 1) {
		$app{service_credits}		= ($hash{1}{balance}-$hash{1}{limit});
		#if ($app{service_credits}>0) {
		#	$lbac = &active_user_get("LBAC");
		#	$app{service_credits_bar} = ($lbac<=0) ? 10 : int(($app{service_credits}/$lbac)*10);
		#	$app{service_credits_bar} = ($app{service_credits_bar} > 10) ? 10 : $app{service_credits_bar};
		#	$app{service_credits_bar} = ($app{service_credits_bar} < 0) ? 0 : $app{service_credits_bar};
		#} else {
		#	$app{service_credits_bar}	= 0;
		#}
	}
	$template_default{my_url}				= $ENV{SCRIPT_NAME};
	$template_default{service_id}			= $app{service_id};
	$template_default{service_name}			= $app{service_name};
	$template_default{service_email}		= $app{service_email};
	$template_default{service_ani}			= $app{service_ani};
	$template_default{service_ani_e164}		= $app{service_ani_e164};
	$template_default{service_alert}		= $app{service_alert};
	$template_default{"service_alert_".$app{service_alert}}	= 1;
	$template_default{service_credit}		= &format_number($app{service_credits},2);
	#$template_default{service_credits_bar}	= $app{service_credits_bar};
}
return 1;
#=======================================================





# support libs
