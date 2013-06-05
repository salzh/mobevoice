#!/usr/bin/perl
require "include.cgi";

use CGI;
use DBI;
use Digest::MD5 qw(md5 md5_hex md5_base64);
use LWP 5.69;
use lib 'lib';

# read the CGI params
my $cgi = CGI->new;
my $MessageType= $cgi->param("type");
my $Message = $cgi->param("message");
my $Flagname = $cgi->param("hdnflag");
# connect to the database multilevel $sth->fetchrow_array;

if($Flagname eq "FlagSave")
{

	my $statement = qq{SELECT COUNT(*) AS cnt FROM sms_customtext WHERE msg_type=?};
	my $sth = $database->prepare($statement) or die $database->errstr;
	$sth->execute($MessageType) or die $sth->errstr;
	
	if($sth->fetchrow_array eq 0)
	{
		my $sqlinsert = qq{INSERT INTO sms_customtext (msg_type,msg_text) VALUES ("$MessageType","$Message")};
		my $Resins = $database->prepare($sqlinsert) or die $database->errstr;
		$Resins->execute() or die $sth->errstr;		
	}
	else
	{
		my $sqlinsert = qq{UPDATE sms_customtext SET msg_text = '$Message' WHERE msg_type = '$MessageType'};
		my $Resins = $database->prepare($sqlinsert) or die $database->errstr;
		$Resins->execute() or die $sth->errstr;			
	}
		
	my ($userID) = "Updated";
	
	
	# create a JSON string according to the database result
	my $json = ($userID) ? 
	  qq{{"success" : "Successfully", "Text" : "$userID", "hdnflag" : "$Flagname"}} : 
	  qq{{"error" : "AJAXERROR"}};
	  
	# return JSON string
	print $cgi->header(-type => "application/json", -charset => "utf-8");
	print $json;
}






