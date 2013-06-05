#!/usr/bin/perl
use Net::Google::DataAPI::Auth::OAuth2;
use Net::Google::AuthSub;
use CGI;
use CGI::Carp qw(fatalsToBrowser);
use LWP::UserAgent;
use Data::Dumper;
use XML::Simple;
my $q = new CGI;

use HTML::Template; 
use HTTP::Request::Common qw( POST );

require "../include.cgi";
$my_url = "invite.cgi";
$action = $form{action};


if (!($app{session_status} eq 1)) {
    print "Location: /myaccount/\n\n";
    exit;
}

my $oauth2 = Net::Google::DataAPI::Auth::OAuth2->new(
  client_id => '792435373603.apps.googleusercontent.com',
  client_secret => 'eDfnhVB0lYtkmQRSLj4m-5kQ',
  scope => ['https://www.google.com/m8/feeds'],

  # with web apps, redirect_uri is needed:
  #
  redirect_uri => 'https://www.zenofon.com/myaccount/invite.cgi',

);
$code = $q->param("code");


if($code eq ""){
  my $url = $oauth2->authorize_url();
  print "Location: $url\n\n";
  exit;
}

my $token = $oauth2->get_access_token($code);

my $contacts = Net::Google::AuthSub->new(auth => $oauth2);
$url = "https://www.google.com/m8/feeds/contacts/default/full?v=3.0&max-results=1000";
my $content  =  $token->get($url);
$xml = new XML::Simple();
$data = $xml->XMLin($content->decoded_content);
%final = ();

print "Content-type: text/html\n\n";
foreach my $entry(%{$data->{'entry'}}){
  $final{$entry->{'title'}}{'name'} = $entry->{title};
  $final{$entry->{'title'}}{'phone'} = $entry->{'gd:phoneNumber'};
  $final{$entry->{'title'}}{'email'} = $entry->{'gd:email'};
}

$service_id = &clean_int($app{session_cookie_u});
$sql = "insert into service_contacts (service_id, name, email, phone) values ";
$string = "('$service_id', '%s', '%s', '%s')";
$i = 0;
@array = ();
for $id(keys %final){
  $i++;
  $phone = eval{$final{$id}{phone}{content}};
  $email = eval{$final{$id}{email}{address}};
  $execute = sprintf($sql, $id, $email, $phone);
  
  push(@array, sprintf($string, $id, $email, $phone));
  if($i%100 == 0){
    $execute = $sql . join(", ", @array);
    &database_do( $execute );
    @array = ();
  }
}
$execute = $sql . join(", ", @array);
&database_do( $execute );
print " $i Contacts Imported"
