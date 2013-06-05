#!/usr/bin/perl

use CGI;
use DBI;
use Digest::MD5 qw(md5 md5_hex md5_base64);
use LWP 5.69;
use strict;
use warnings;
use lib 'lib';

# read the CGI params
my $cgi = CGI->new;
my $MessageType= $cgi->param("type");
my $Message = $cgi->param("message");
my $Flagname = $cgi->param("hdnflag");
my $result = "";
my $strlen = length $Message;
my $errormsg = ""; 
# connect to the database multilevel $sth->fetchrow_array;
my $dbh = DBI->connect("DBI:mysql:database=multilevel;host=127.0.0.1;port=3306","multilevel", "multilevel") or die $DBI::errstr;



if($Flagname eq "FlagSave")
{	
	# check the Messagetype in the database
	my $statement = qq{SELECT COUNT(*) AS cnt FROM sms_customtext WHERE msg_type=?};
	my $sth = $dbh->prepare($statement) or die $dbh->errstr;
	$sth->execute($MessageType) or die $sth->errstr;	
	if($strlen <= 160)
	{
		if($sth->fetchrow_array eq 0)
		{
			my $sqlinsert = qq{INSERT INTO sms_customtext (msg_type,msg_text) VALUES ("$MessageType","$Message")};
			my $Resins = $dbh->prepare($sqlinsert) or die $dbh->errstr;
			$Resins->execute() or die $sth->errstr;	
			$result = "inserted";
		}
		else
		{
			my $sqlinsert = qq{UPDATE sms_customtext SET msg_text = '$Message' WHERE msg_type = '$MessageType'};
			my $Resins = $dbh->prepare($sqlinsert) or die $dbh->errstr;
			$Resins->execute() or die $sth->errstr;	
			$result = "updated";
		}
	}
	else
	{   
		#$errormsg = "Please enter maximum of 160 characters including spaces";
		$result = "LenError";
	}
	my ($userID) = $result;
	
	
	# create a JSON string according to the database result
	my $json = ($userID) ? 
	  qq{{"success" : "Successfully", "Text" : "$userID", "hdnflag" : "$Flagname"}} : 
	  qq{{"error" : "AJAXERROR"}};
	  
	# return JSON string
	print $cgi->header(-type => "application/json", -charset => "utf-8");
	print $json;
}
elsif($Flagname eq "FlagEdit")
{
	my $Selstament= qq{SELECT msg_text FROM sms_customtext};
	my $sth = $dbh->prepare($Selstament) or die $dbh->errstr;
	$sth->execute() or die $sth->errstr;	
	
    my $val = "";
	while (my $ref = $sth->fetchrow_hashref())
	{
	   $val .=$ref->{'msg_text'}."@@";
	}
	
	my ($userID) = $val;
	
	
	# create a JSON string according to the database result
	my $json = ($userID) ? 
	  qq{{"success" : "$val"}} : 
	  qq{{"error" : "Error"}};
	  
	# return JSON string
	print $cgi->header(-type => "application/json", -charset => "utf-8");
	print $json;
	
}
