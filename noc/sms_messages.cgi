#!/usr/bin/perl
print "Content-type:text/html\n\n";
#use CGI::Carp qw(fatalsToBrowser); # To Debug on Browsers
require "include.cgi";
use DBI;
use CGI;
use utf8;
use Encode;
$database->do('SET NAMES utf8');
$database->{'mysql_enable_utf8'} = 1;


#if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_view_reports") ne 1) {adm_error("no permission"); exit;}
use Data::Dumper;

if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
$cgi = new CGI;

if(defined($form{'message'}) && defined($form{'msg_type'}) && defined($form{'lang_id'})){
	
	my $sth = "";
	my $message = $form{'message'};
	my $msg_type=$form{'msg_type'};
	my $language_id = $form{'lang_id'};
	$message =~ s/(["'*])/\\$1/g;
	$sth = $database->prepare(qq{update sms_messages set messages = "$message" where language_id ="$language_id" and message_type = "$msg_type"});
	$sth->execute();

}else{
	print "nothing";
}

