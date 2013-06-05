#!/usr/bin/perl

#!c:\Perl\bin\Perl
use strict;
use warnings;
use CGI;
use lib 'lib';
use WWW::Twilio::API;

print "Content-type: text/xml\n\n";
my $q=CGI::Vars();

my $tonumber = $q-> {tonumber};

my $smsbody = $q-> {smsbody};

## usage: examples.pl account_sid authtoken action parameters (see examples)
my $account_sid = 'ACc0d95bda6c7bed59a113a9bd5c9ce956';
my $auth_token  = '474e7c48ead04865d19d0be32165f2c0';
my $action      ='SMS' ;

my $twilio = new WWW::Twilio::API( AccountSid => $account_sid,
                                   AuthToken  => $auth_token, );

if( $action eq 'SMS' ) {
    my $response = $twilio->POST('SMS/Messages',
                                 From => '+19173384580',
								 To   =>$tonumber,
                                 Body =>$smsbody);
    print $response->{content};
	
	open FH, ">>TestSMSSend2Logs.txt";
    print FH $response->{content};
    close FH; 
}

else {
    print "Unknown action.\n";
}

#print $tonumber;

#print "\n \n";

#print $smsbody;

exit;





