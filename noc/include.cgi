#!/usr/bin/perl
#=======================================================
# captura http e manda pra https
#=======================================================
if (index($ENV{SCRIPT_URI},"http://") eq 0) {
	# if (force_htps) {
		$url = "https".substr($ENV{SCRIPT_URI},4,4096);
		print "Content-type: text/html\n";
		print "Cache-Control: no-cache, must-revalidate\n";
		print "Pragma: no-cache\n";
		print "status: 301\n";
		print "location: $url\n";
		print "\n";
		print "<meta http-equiv='refresh' content='0;URL=$url'>";
		print "\n";
	# }
	exit;
}
#=======================================================
# inicializa perl e dependencias inicializa umas coisa
# que vou usar a frente, verifica login secao, user, etc etc
#=======================================================
use CGI;
use HTML::Template; 
use HTTP::Request::Common qw( POST );
use URI::Escape qw(uri_escape);
%app = ();
require "/usr/local/multilevel/default.include.pl";
#require $ENV{X_app_root}."default.include.pl";
$app_root						= "/usr/local/multilevel/";
$www_root						= "$app_root/www/noc/";
$template_folder				= "$app_root/www/noc/design/";
$app{users_table}				= "adm_users";
$app{users_col_id}				= "id";
$app{users_options_table}		= "adm_users_data";
$app{users_permissions_table}	= "adm_users_permissions";
$app{session_table}				= "adm_users_session";
$app{session_cookie_k_name}		= "admk";
$app{session_cookie_u_name}		= "admu";
$app{session_logout_on_timeout} = 1;
$app{session_timeout_seconds}	= 60*30*99;
$app{session_active_service_id}	= "";
$app{session_status}			= 0;
$app{use_imagecheck}			= 1;
$cgi 							= new CGI;
%today 							= &get_today();
%form = (); 
foreach $form_name ($cgi->param) {
	@form_values = $cgi->param($form_name);
	$form_values_count = @form_values;
	$form{$form_name} = ($form_values_count>1) ? join(",",@form_values) : $form_values[0];
}
%cookie							= &cookie_read(); 
$app{session_status}			= &session_init();
$app{session_is_root}			= 1; #($app{session_cookie_u} eq 0) ? 1 : 0;
#
return 1;
#=======================================================



sub adm_security_check(){
	local($name) = @_;
	return &active_user_permission_check("noc:$name");
}
sub adm_error(){
	($msg) = @_;
    %t = ();
    $t{dic}{title}		= "Error";
    $t{dic}{content}	= $msg;
    &template_print("template.html",%t);
    exit;
}

