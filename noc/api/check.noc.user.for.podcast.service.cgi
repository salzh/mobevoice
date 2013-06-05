#!/usr/bin/perl

#api for pocast,share user acctounts  kevin 2012.1.14

# smple:https://version2.zenoradio.com/noc/podcast-api.cgi?web_user=neyfrota&web_password=_01834dc162f86386316040c17f17c743
# return trun or flase or nor not exist
#password = '_' . md5_hex($account.$pass)

use CGI::Carp qw(fatalsToBrowser);

#print "Content-type: text/html; charset=utf-8\n\n";

require "lib/var.pl";
require "lib/SQL.pm";
require "lib/Request.pm";

$DB_cfg{DB_user} = 'radio';
$DB_cfg{DB_pass} = 'radio';
$DB_cfg{DB_url} = '127.0.0.1';
$DB_cfg{DB_name} = 'owsline';
$DB_cfg{DB_port} = '';

&GET_COOKIES;
&GET_REQUEST;

#print_hash(%_REQUEST);
	
#-----------------------------------------connect mysql

my $this = new SQL;

$param{dbh} = $this->connect_db(\%DB_cfg);  
 
$sql = "select * from system_user where web_user = '$_REQUEST{web_user}'";

%param =(
 dbh => $param{dbh},
 sql => $sql
);


$sth = $this->DB_fetchrow_hashref(\%param);
  
$self = $sth->fetchrow_hashref;

#-----------------------------------------fetch user info
%system_user = %$self;

#print_hash(%system_user);


$this->disconnect_db($param{dbh});

if ($system_user{web_password} ne '') {
	
	if ($system_user{web_password} eq $_REQUEST{web_password}) {
		 #key_md5($form{web_password});
	
	print 'ture|' . "$system_user{id}|$system_user{group_id}|$system_user{name}|$system_user{creation_date}|$system_user{email}";
	
	
	}
	else {
	print 'flase';	
	}

}
else {
	print "not exist!";	
}

#end








