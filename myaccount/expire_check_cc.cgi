#!/usr/bin/perl
#use CGI::Carp qw(fatalsToBrowser); # To Debug on Browsers

require "../include.cgi";
#require "/usr/local/multilevel/www/include.cgi";
#======================================================
use CGI;
use DBI;
use Digest::MD5 qw(md5 md5_hex md5_base64);
use File::Copy;
use HTML::Template;
use LWP 5.69;
use strict;
use warnings;
use lib 'lib';
use Time::Local;
use utf8;
use Encode;
use lib "/usr/local/lib/perl5/site_perl/5.15.4";
use Date::Calc qw(Delta_DHMS);
use DateTime::Format::Strptime;
#use Date::Calc;

my $fmt = '%Y-%m';
my $parser = DateTime::Format::Strptime->new(pattern => $fmt);

my $expired_local = localtime(time);
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);

#to check set manual  
  #$mon = "4";
  #$year = "112";

#year will be current year and month the previous one  
  my $expired_year = $year-100;
  my $expired_mon = $mon;
  my $will_expire_year = $year-100;
  my $will_expire_mon = $mon;
  
   
#if month is january(linux val 0) then check for december of previous year (12)   
    if($expired_mon eq "0")
    {
    $expired_mon = 12;
    $expired_year = $expired_year - 1;
    }
my $expired_current_month = sprintf("%02d", $expired_mon);
my $expired_current_year = sprintf("%02d", $expired_year);
my $expired_month_year = $expired_current_month."".$expired_current_year;

my $expired_sql = "SELECT ani FROM service_profile_cc where active = 1 and cc_date = $expired_month_year";
my @expired_arrayval = &database_select_as_array($expired_sql);
my $expired_count = scalar(@expired_arrayval);

my $i = 0;  
my $expired_body = "Important: The credit card on your ZenoFon account has expired. To add a new credit card, type 'add credit card', or call us at (917) 284-9450.";

while ($i < $expired_count)
{
    my $expired_ani = $expired_arrayval[$i];
    #check user and message status is unmute
				
	my @user_info =&isZenofonUser($expired_ani);
	my @status = &MuteUnmute_status($expired_ani);
	my $StatusValue = $status[0];
        
	if($user_info[0] eq 1 && $StatusValue eq 1)
            {
            &sms_log($expired_ani,$expired_body,"",'Sent');                
            &sendSMS_Twilio($expired_ani,$expired_body);
            }
    $i++;
}

#will expire function   
#if month is december(linux val 11) then check for january of next year (01)   

   if($will_expire_mon eq "11")
   {
    $will_expire_mon = 1;
    $will_expire_year = $will_expire_year + 1;
   }
   else
   {
   $will_expire_mon = $will_expire_mon + 2;
   }

my $will_expire_current_month = sprintf("%02d", $will_expire_mon);
my $will_expire_current_year = sprintf("%02d", $will_expire_year);
my $will_expire_month_year = $will_expire_current_month."".$will_expire_current_year;

my $will_expire_sql = "SELECT ani FROM service_profile_cc where active = 1 and cc_date = $will_expire_month_year";
my @will_expire_arrayval = &database_select_as_array($will_expire_sql);
my $will_expire_count = scalar(@will_expire_arrayval);

$i = 0;  
my $will_expire_body = "Reminder: The credit card on your ZenoFon account will expire soon. When you're ready to change it, type 'add credit card', or call us at (917)284-9450.";

while ($i < $will_expire_count)
{
    my $will_expire_ani = $will_expire_arrayval[$i];
    #check user and message status is unmute
				
	my @user_info =&isZenofonUser($will_expire_ani);
	my @status = &MuteUnmute_status($will_expire_ani);
	my $StatusValue = $status[0];
 
    if($user_info[0] eq 1 && $StatusValue eq 1)
    {
    &sms_log($will_expire_ani,$will_expire_body,"",'Sent');
    &sendSMS_Twilio($will_expire_ani,$will_expire_body);
    }
    $i++;
}

#expire check end here

#functions end here
sub sms_log()
{
	my($sms_number,$sms,$sms_function,$mode)=@_;
	
	my $datetime=&getDatetime();
	$sms =~ s/\'//g;
	
	my $sql="insert into sms_log (log_date_time,sms_number,message,sms_function,mode) values ('$datetime','$sms_number','$sms','$sms_function','$mode')";
    &database_do($sql);
	
}
sub getDatetime()
{
   my $datetime="";
   my $today="";
   my($timediff,$date)=@_;
   my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst);
   
   if(!defined($timediff)){

      ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);
      $year = $year+1900;
        $mon=$mon+1;
      $datetime = "$year-$mon-$mday  $hour:$min:$sec";
   }else{


      if(defined($date)){

         ($year,$mon,$mday,$hour,$min,$sec) = split(/[\s\-:]+/, $date);
         $year=$year-1900;
        $mon=$mon-1;

         $today= mktime($sec,$min,$hour,$mday,$mon,$year)-($timediff*60);
        ( $sec, $min, $hour, $mday, $mon, $year) = localtime($today);
      }else{

         $today = time()-($timediff*60);
         ( $sec, $min, $hour, $mday, $mon, $year) = gmtime($today);
      }

      $year = $year+1900;
      $mon=$mon+1;
      $datetime = "$year-$mon-$mday  $hour:$min:$sec";
   }

  return $datetime;
}
sub isZenofonUser(){
	
	my ($fromnumber) = @_;
	
	my $isValidUser = 0;
	my $error = 0;
	
	$fromnumber = &trim($fromnumber);
	my $form_key_int = clean_int($fromnumber);
	
	my $firstrecordid;
    my $firstrecordflag;
    my $firstrecordname;
    my $firstrecordemail;
    my $firstrecordani;

    my $service_found;
    my $service_id;
    my $service_name;
    my $service_email;
    my $service_ani;
	
	if (($fromnumber ne ""))
   {
		my ($form_key_flag,$form_key_e164,$tform_key_country) = &multilevel_check_E164_number($form_key_int);
		
		if ( ($form_key_flag eq "OK") && ($form_key_int ne "") )
         {
			my $sql = "
            SELECT service.id,1,service.id,service.name,service.email,service_ani.ani
            FROM service,service_pin,service_status,product,service_ani
            WHERE
             service_pin.service_id = service_ani.service_id AND
            service_ani.ani = '$form_key_e164' and
            service_pin.service_id = service.id AND
            service.status = service_status.id AND
            service.product_id = product.id AND
            #service_status.can_web_access = 1 AND
            service_status.deleted = 0 AND
            service_ani.service_id  = service.id
            ";
            my %hash = database_select_as_hash($sql,"flag,id,name,email,ani");

            foreach (sort keys %hash)
            {
               $firstrecordid    = $hash{$_}{id};
               $firstrecordflag    = $hash{$_}{flag};
               $firstrecordname    = $hash{$_}{name};
               $firstrecordemail    = $hash{$_}{email};
               $firstrecordani    = $hash{$_}{ani};
               last;
            }
            my $num_records =  keys( %hash ) ;
            if ($num_records > 1)
            {
               #duplicate ANI+PIN ,ask user retry login with EMAIL+PIN
               $isValidUser=1;
               $error=0;
               return ($isValidUser,$error,$firstrecordid,$firstrecordname,$firstrecordemail,$firstrecordani);

            }
            elsif ((defined $firstrecordflag) && $firstrecordflag eq 1)
            {
               $service_found    = 1;
               $service_id        = $firstrecordid;
               $service_name    = $firstrecordname;
               $service_email    = $firstrecordemail;
               $service_ani        = $firstrecordani;
               $error             = 0;
               $isValidUser=1;             
               
            }            
		 }
   }   
   
   return ($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani);
}
sub Message()
 {

   my ($msg,$From) = @_;
   my $rtnmsg = "";
  
   my $sql = "";
   my $language_status	 = "";
   my $message = "";
       
	   $sql = "select language_status from SMS_Client where sms_ani='$From'";

       my @language = database_select_as_array($sql);
      
	    if (@language gt 0)
        {
		   $language_status = $language[0];
		}
		else
	    {
	      $language_status = "1";
	    }
   
  $sql = "select count(*) from SMS_Client";
  my @count = database_select_as_array($sql);
  my $count = $count[0];
  
  if ($count eq 0)
  {
      $sql = "select messages from sms_messages where language_id = '$language_status' and message_type ='$msg'";
	  my @info = database_select_as_array($sql);
	  $message = $info[0];
  }
  else
  {
	 $sql = qq [select 1,1,1,sms_messages.messages from SMS_Client,sms_languages,sms_messages
	         where
			 SMS_Client.language_status = sms_languages.id  and
			 sms_messages.language_id = '$language_status' and
			 sms_messages.message_type ='$msg'];
	
	my %hash = database_select_as_hash($sql,"1,1,messages");
	$message = $hash{1}{'messages'};
  }	
	return $message;	 
}

sub MuteUnmute_status()
 {
    my ($fromnumber) = @_;
    my $Statusvalue=1;
    $fromnumber =~ tr/+/ /;
    my $UserNo = &trim($fromnumber);
    my @Status = database_select_as_array("SELECT sms_status FROM SMS_Client WHERE sms_ani = '$UserNo'","sms_status");


    if(@Status > 0){
      $Statusvalue = $Status[0];
    }
   return ($Statusvalue);
 }