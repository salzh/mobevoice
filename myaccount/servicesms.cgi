#!/usr/bin/perl
#use CGI::Carp qw(fatalsToBrowser); # To Debug on Browsers

require "../include.cgi";

#======================================================
use CGI;
use DBI;
use strict;
use warnings;
use lib 'lib';
use Time::Local;
use utf8;
use Encode;
#=======================================================

#=============Required Packages=========================
#use feature qw(switch say);
use POSIX;
use CGI::Session;
use lib "/usr/local/lib/perl5/site_perl/5.15.4";
use Date::Calc qw(Delta_DHMS);
#=======================================================

#=======================================================
#Set session value
my $cgi      = new CGI;
my $sid      = $cgi->cookie('ID');
my $counter  = 0;
#=======================================================

#=======================================================
#carriers list
my %carriers_list               = ();
$carriers_list{"USAATT"}        = "At&t";
$carriers_list{"USAALLTEL"}     = "Alltel";
$carriers_list{"USABOOST"}      = "Boost mobile";
$carriers_list{"USAONE"}        = "Cellular One";
$carriers_list{"USACRICKET"}    = "Cricket";
$carriers_list{"USACINGULAR"}   = "Go/Cingular (prepaid)";
$carriers_list{"USAMETROPCS"}   = "Metro PCS";
$carriers_list{"USASPRINT"}     = "Sprint/Nextel";
$carriers_list{"USATMOBILE"}    = "T-mobile";
$carriers_list{"USATMOBILETOGO"}= "T-mobile ToGo";
$carriers_list{"USATRACKFONE"}  = "Tracfone";
$carriers_list{"USAUS"}         = "U.S. Cellular";
$carriers_list{"USAVERIZON"}    = "Verizon Wireless";
$carriers_list{"USAVERIZONPAYG"}= "Verizon Wireless Pay as you go";
$carriers_list{"USAVIRGIN"}     = "Virgin Mobile";
$carriers_list{"UNKNOWN"}       = "Unknown";
$carriers_list{"LANDLINE"}      = "Landline";
$carriers_list{"NOTLISTED"}     = "Not listed";

#========Declaring Twilio Receive SMS Fields==============
my $AccountSid    =   "";
my $Body          =   "";
my $ToZip         =   "";
my $FromState     =   "";
my $ToCity        =   "";
my $SmsSid  	  =   "";
my $ToState  	  =   "";
my $To            =   "";
my $ToCountry  	  =   "";
my $FromCountry   =   "";
my $SmsMessageSid =   "";
my $ApiVersion    =   "";
my $FromCity  	  =   "";
my $SmsStatus  	  =   "";
my $From          =   "";
my $FromZip  	  =   "";
#=========================================================
#=============Get the Twilio Receive SMS details==========
my $q	        = CGI::Vars();
$AccountSid     = $q-> {AccountSid};
$Body 	        = $q-> {Body};
$ToZip 	        = $q-> {ToZip};
$FromState      = $q-> {FromState};
$ToCity         = $q-> {ToCity};
$SmsSid         = $q-> {SmsSid};
$ToState        = $q-> {ToState};
$To 	        = $q-> {To};
$ToCountry      = $q-> {ToCountry};
$FromCountry    = $q-> {FromCountry};
$SmsMessageSid  = $q-> {SmsMessageSid};
$ApiVersion     = $q-> {ApiVersion};
$FromCity       = $q-> {FromCity};
$SmsStatus      = $q-> {SmsStatus};
$From 	        = $q-> {From};
$FromZip        = $q-> {FromZip};
$From 	        =~ tr/+/ /;
$From           = &trim($From);
#===================For Testing===========================
#$From = "12016829054";
#$Body = "zenofon";
#=========================================================

if (defined $From && $From ne "" && defined $AccountSid && $AccountSid eq "ACc0d95bda6c7bed59a113a9bd5c9ce956")
{
	
	#sms_log mode recieve
	&sms_log($From,$Body,'','Received');


        my @GetSmsValue  =  &sms_services(&trim($From),$Body);
        my $FrmNumber    =  $GetSmsValue[0];
        my $Message      =  $GetSmsValue[1];
        my $len          =  length($Message);
        my $sms_function =  $GetSmsValue[2];
	
	print "Content-type: text/xml; charset=UTF-8 \n\n";
	#Get Sms Message
 
	#More than 160 character message split and send via twilio
	if ($len > 160)
	{
		my $position 	=  rindex(substr($Message,0,160), " ");	    
		my $firstmsg 	=  substr($Message,0,$position);
		my $msg         =  encode("utf8" ,$firstmsg);
		&sendSMS_Twilio($FrmNumber,$msg);
		my $secondmsg   =  substr($Message,$position,$len);
		&trim($secondmsg);
		my $secmsg      =  encode("utf8" ,$secondmsg);
		&sendSMS_Twilio($FrmNumber,$secmsg);
		
	}
	else
	{
		my $Message = encode("utf8" ,$Message);
		&sendSMS_Twilio($FrmNumber,$Message);
		
	}  	
    #sms_log mode sent
    $Message = encode("utf8" , $Message); 
    &sms_log($From,$Message,$sms_function,'Sent');
}

#==========================sms_log()========================
# This function track each message recieved and sent to the user.
#==============================================================
sub sms_log()
{
	my($sms_number,$sms,$sms_function,$mode)=@_;
	my $datetime    =  &getDatetime();
	$sms 	        =~ s/(["'*])/\\$1/g;
	my $sql	        =  "insert into sms_log (log_date_time,sms_number,message,sms_function,mode) values ('$datetime','$sms_number','$sms','$sms_function','$mode')";
    &database_do($sql);
}

#==========================sms_services()========================
# The core function which recieves sms through TWILIO and sends
# sms through TWILIO API
#==============================================================

sub sms_services()
{
   my ($fromnumber,$smsbodytext) = @_;
   my $returnval   = "";
   my $StatusValue = "";
   my $isValidUser = "";
   my $sms_function= "";
   
   #valid User status
   my @isValidUserArray =  &isZenofonUser($fromnumber,$smsbodytext); #  my ($FromNumber,$BodyText) = @_;  return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
   $isValidUser	        =  $isValidUserArray[0];
   my $service_id       =  $isValidUserArray[2];
   
#===========================================================================================
# Checking any invitation if message body text is null and from number not a zenofon user
#===========================================================================================
   my %sms_info;
   my $day_diff	        =0;
   my $refer_status     =0;
   my $invite_service_id="";
   my $refferer_no      ="";
   my $signin_pin_id;
   my $ani_name;
 
      if(((&trim($smsbodytext)) eq "" || lc((&trim($smsbodytext))) eq "accept" || lc((&trim($smsbodytext))) eq "yes") && $isValidUser eq 0)
    {
	my %signin_info=&getsigninRequest($fromnumber);
	if(%signin_info){
							
			my $date_time	   =  $signin_info{1}{'date_start'};
			$signin_pin_id	   =  $signin_info{1}{'id'};
			$refferer_no	   =  $signin_info{1}{'dst'};
			$ani_name          =  $signin_info{1}{'name'};
			$day_diff          =  &get_time_difference($date_time);
            my @dstInfo        =  &isZenofonUser($signin_info{1}{'dst'},$smsbodytext);     
			$invite_service_id =  $dstInfo[2];
            $refer_status	   =  1;
				
	}
    }
   
   #==============Checking invitation ends here==============#
   
   if($isValidUser eq 0)
   {
	 #checking invitation		 
	if($refer_status eq 1 &&  $day_diff > 11){
				
			# invitation expired
				$returnval = &Message("INVITE_EXPIRE_INFO",1);
				
	}elsif($refer_status eq 1){
						
			#add user if invitation is valid
					
				$returnval = &addFriend($invite_service_id,$fromnumber,$refferer_no,$signin_pin_id,$ani_name);
				$sms_function= "addFriend";
						
	}elsif((my %signin_info=&getsigninRequest($fromnumber))){
						
			# if non zenofon user send some invalid sms other than yes and
			# user have pending invitation to join zenofon
						
				$returnval = &Message("INVALID_JOIN_FORMAT",1);
						
	}elsif(lc(&trim($smsbodytext)) eq "join"){
								
			#add user if non zenofon user send sms 'join'
							
				$returnval = &new_user_join(&trim($fromnumber),lc(&trim($smsbodytext)));
						
    }else{
						
			#if all condition fails send not zenofon user message
						
				$returnval = &Message("NOT_ZENO_USER_INFO",1);
						
	}
					 
			#return fromnumber,sms to be sent,sms_function processed.
						
			return ($fromnumber,$returnval,$sms_function);		 
					  
    }
   
	# Mute and Unmute status value  
						
		my @status   =  &MuteUnmute_status(&trim($fromnumber));
		$StatusValue =  $status[0];
					 
	# if status is mute
	
		if(($StatusValue eq 0) && (lc(&trim($smsbodytext)) ne "mute") && (lc(&trim($smsbodytext)) ne "unmute") && (&trim($smsbodytext) ne "1")){
		
			$returnval = &Message("MUTE_STATUS_INFO",1);
			return ($fromnumber,$returnval,$sms_function);
	 
		}
	 
#***********Get Change SMS Syntax*******************************************#
						
	my %hash                =  database_select_as_hash("SELECT id,msg_type,msg_text FROM sms_customtext","msg_type,msg_text");
	my %initiate            =  %{$hash{1}};
	my %addnew              =  %{$hash{2}};
	my %confirmation        =  %{$hash{3}};
	my %errormessage        =  %{$hash{4}};
	my $initiateaction      =  $initiate{msg_text};
	my $AddNew              =  $addnew{msg_text};
	my $confirmation        =  $confirmation{msg_text};
	my $errormessage        =  $errormessage{msg_text};
				
#***************************************************************************#
					
	my $reroutecount        =  "";
	my $reroutemeessage     =  "";
	
	#getLast SMS from session
	my $last_sms            =  &get_sms_session();
	my $sms_session	        =  1;
	my @session_msg         =  split(/\s/,$last_sms);
	my $msg_info            =  $session_msg[0];
					 
	if(lc(&trim($smsbodytext)) eq lc(&trim($initiateaction)) || lc(&trim($smsbodytext)) eq 0)
	{
	    #send initial sms
						    
		$returnval = &Message("");
							
	}elsif (lc(&trim($smsbodytext)) eq "1"){
						    
	    #if user select 1 from main menu send mute unmute status sms.
							
		$returnval = &Message("MUTE_UNMUTE_INFO");
							
	}elsif ((lc(&trim($smsbodytext)) eq "reroute last call") || (lc(&trim($smsbodytext)) eq 10)){
						   
	    #user send reroute last call sms to know user last incomplete call
							    
		my @array       =  &rerouteLastCall(&trim($fromnumber),lc(&trim($smsbodytext)));
		$returnval      =  $array[0];
		$sms_session    =  $array[1];
		my $error       =  $array[2];
							   
	    #set error counter if user send invalid sms
						    
		my @getCounter  =  &errorCounter($error);
			if ($getCounter[0] eq 5)
			{
				#send customer support message if user send invalid sms  5 times
							
				    my $message    =  &Message("CUSTOMER_SUPPORT_INFO");
				    $returnval     =  "$message";
				    $sms_session   =  1;
							
			}
							
			my $session_value =  &getSessionObj;
			$session_value->clear(["error_reroutelastcall"]);
			$sms_function	  =  "rerouteLastCall";
							
	}elsif (lc(&trim($smsbodytext)) eq "yes" && lc(&trim($last_sms)) eq "reroute last call"){
						    
	    #if user wants to use the change route for future calls
							
		my $sql="";
							    
	    #my @rerouteStatusArray = database_select_as_array("SELECT sms_status_value FROM sms_status","sms_status_value");
		my $reroutestatusvalue = &getSMSStatus(2,$fromnumber);
							 
	    if($reroutestatusvalue eq 1){
							        
		&getSMSStatus(1,$fromnumber);
								
				#get last request to change route
								
			my(%sms_data)	=  &getLastrequest($fromnumber);
			my $route_temp	=  $sms_data{sms_next_route};
								
									
		     if($route_temp gt 0){
				
		          my $sms_route_id	  =  $sms_data{sms_route_id};
		          my $sms_current_route =  $sms_data{sms_value};
		          my $sms_dst_no	      =  $sms_data{sms_contact_number};
							
		          my $deleteroute 	  =  "DELETE FROM sms_route_temp where sms_route_id='$sms_route_id'";
		          database_do($deleteroute);
							
		         #send future route info to user.
							
			     my $message   =  &Message("FUTURE_ROUTE_INFO");
			     $message 	  =~ s/xxxx/$sms_dst_no/i;
			     $message 	  =~ s/xxxxX/$sms_current_route/i;
			     $returnval    = $message; 
		    }
			 
	    }else{
							
		  my $message  =  $errormessage;
		  $message     =~ s/xxxxxxx/$smsbodytext/i;
		  $returnval   =  $message;
		  $sms_session =  0;
							
	    }
							
	}elsif (lc(&trim($smsbodytext)) eq "call history" || lc(&trim($smsbodytext)) eq "callhistory" || lc(&trim($smsbodytext)) eq 4){
							
	    #send last 3 calls details to user
							
		my $limit       =  2;
		$returnval      =  &callHistory(&trim($fromnumber),lc(&trim($smsbodytext)),$limit);
		$sms_function   =  "callHistory";
							
	}elsif(lc(&trim($smsbodytext)) =~ m/^(next)(\s)?([2])?$/){
	    
	    #send  second last call details if user send next
	    #send third last call details if user send next 2
	    
	    my $limit	   =  "";
	    my @split_sms  =  split(/[t]/,(substr($smsbodytext,3)));
	    
	    if(defined($split_sms[1])){
	
			$limit  =  "1,2";
	
	    }else{
	
			$limit	=  "1,1";
	
	    }
	    
	    $returnval = &callHistory(&trim($fromnumber),lc(&trim($smsbodytext)),$limit);
	    $sms_function="callHistory"; 
	
	}elsif (lc(&trim($smsbodytext)) eq "mute"){
	
	    # Mute and Unmute status Update
		    &sms_client_status($isValidUser,lc(&trim($smsbodytext)),&trim($fromnumber));
		    $sms_function  =  "sms_client_status";
		    $returnval 	   =  &Message("MUTE_INFO");	
	
	}elsif (lc(&trim($smsbodytext)) eq "unmute"){
	
	    # Mute and Unmute status Update
	
		    &sms_client_status($isValidUser,lc(&trim($smsbodytext)),&trim($fromnumber));
		    $sms_function  =  "sms_client_status";
		    $returnval 	   =  &Message("UNMUTE_INFO");
	
	}elsif(lc(&trim($smsbodytext)) =~ m/^(help)(\s)?(\d)*$/ || lc(&trim($smsbodytext)) eq  7){
	
	    #send help instructions to user
	
		    $returnval	  =  &help();
		    $sms_function =  "help";
	
	}elsif(lc(&trim($smsbodytext)) eq "reroute" || lc(&trim($smsbodytext)) eq  2){
	
	    #reroute instructions to user
		
		&getSMSStatus(0,$fromnumber);
		
		$sms_function  =  "getSMSStatus";
		my $session = &getSessionObj;
		$session->clear(["duplicate"]);
		$session->clear(["error_counter"]);
		$session->clear(["error_type"]);
		$session->clear(["reroute"]);
		$session->clear(["error"]);
		$session->clear(["contact_error"]);
		
		$returnval = &Message("REROUTE_INFO");
		
        }elsif(lc(&trim($smsbodytext)) =~ m/^(refer)/ || lc(&trim($smsbodytext)) eq  5 || ((lc(&trim($last_sms)) eq "refer") && ((lc(&trim($smsbodytext))) =~ m/^((\w[a-zA-z]+)(\s?))+\,+((\s?)(\+?)((\w[a-zA-Z]?)|(\w[a-zA-Z]+?))(\d+)[(\w+?)(\d)(\s)(\-)]*)$/))){
	    
	    #step 1 - send refer format if user send 'refer' keyword
	    #step 2 - send invitation to friend number if user send name,number and prev sms is 'refer'
	    
	    my  @referInfo = &referFriend($fromnumber,$smsbodytext,$isValidUserArray[3],$service_id);
	    
	    $returnval  =  $referInfo[0];
	    my $error   =  $referInfo[1];	 
	    my $session = $referInfo[2];
	    
	    if ($session ne "")
	    {
		  $sms_session = $session;
	    }
	    
	    if($error eq 1 || lc(&trim($smsbodytext)) eq  5){		
		    #For store sms as refer in session
	    
		    $smsbodytext  =  "refer";
	    }
	
	    $sms_function="referFriend";
        
	}elsif(lc(&trim($smsbodytext)) eq "addnew" || lc(&trim($smsbodytext)) eq "add new" || lc(&trim($smsbodytext)) eq  3){
	
	    #send add new contact format message if user send 'addnew'
		
	        my $session_value =  &getSessionObj;
		    $session_value->clear(["error_addnew"]);
		    $returnval 	      =  &Message("ADD_CONTACT_INFO");			  
	
	}elsif((lc(&trim($smsbodytext)) =~ m/^(\w)(\s?)(\d{1,2})$/i) || lc(&trim($smsbodytext)) eq "no"){
	
	    #change route information of selected contact with selected route number.
	    #here route information is send in format r[1,2,3........,9]
	
		    my @getUserroute    =  &userReroute($isValidUser,$StatusValue,lc(&trim($smsbodytext)),&trim($fromnumber));
		    $reroutecount       =  $getUserroute[0];
		    $returnval	        =  $getUserroute[1];
		    my $error 	        =  $getUserroute[2];
		    $sms_session        =  $getUserroute[3];
			
	    if ($error eq 1)
		{
			$sms_session = 0 ;
		}
		
	    my @getCounter = &errorCounter($error);
			
	    if ($getCounter[0] eq 4)
		{
			my $message     =  &Message("CUSTOMER_SUPPORT_INFO");    
			$returnval      =  "$message";
			$sms_session    =  1;
		}
	
	    $sms_function="userReroute";	
	
	}elsif((lc(&trim($smsbodytext)) =~ m/^((\w[a-zA-Z]+)(\s?))+\,+(\s?\+?(\d+))$/) && (lc(&trim($smsbodytext)) !~ m/^(refer)/)  && (lc(&trim($smsbodytext))!~ m/^(forward)/) && ((lc(&trim($last_sms)) eq "addnew") || (lc(&trim($last_sms)) eq "add new") || ($last_sms eq 3))){
	
	    #add new contact if user send contact name,contact number
	    #here checking prev sms is add new or 3.
	    
	    $returnval 	  =  &addContact($fromnumber,lc(&trim($smsbodytext)),$service_id,$confirmation);
	    $sms_function =  "addContact";
	
	}elsif ((lc(&trim($smsbodytext)) eq "last call") || (lc(&trim($smsbodytext)) eq "lastcall") || (lc(&trim($smsbodytext)) eq 6)){
	
	    #send last call information
	
	    $returnval     =  &lastCall(&trim($fromnumber),lc(&trim($smsbodytext)));
	    $sms_function  =  "lastCall";
	
	}elsif (lc(&trim($smsbodytext)) eq "refund"){
	
	    #user request to refund the amount of last call she/he made.
	
	    $returnval     =  &refund(&trim($fromnumber),lc(&trim($smsbodytext)));
	    $sms_function  =  "refund";
	
	}elsif ((lc(&trim($smsbodytext)) eq "add ani") || (lc(&trim($last_sms)) eq "add ani")){
	
	    # add new user number to zenofon user exisitng profile.
	
	    my @array 	  =  &do_ani(&trim($fromnumber),lc(&trim($smsbodytext)));
	    $returnval 	  =  $array[0];
	    $sms_session  =  $array[1];
	    my $error 	  =  $array[2];
	
	    my @getCounter = &errorCounter($error);
	
	    if ($getCounter[0] eq 5)
		{
			my $message  =  &Message("ADD_ANI_CUSTOM_SUP");    
			$returnval   =  "$message";
			$sms_session = 1;
		}
	
	    $sms_function="do_ani";
	
	}elsif (lc(&trim($smsbodytext)) =~ m/^(language)$/ || lc(&trim($smsbodytext)) eq "8"){
	
	    #laungague menu
	
		    $returnval = &Message("LANGUAGE_MENU");
	
	}elsif ((lc(&trim($smsbodytext)) eq "english") || (lc(&trim($smsbodytext)) eq "french") || (lc(&trim($smsbodytext)) eq "spanish") || (lc(&trim($smsbodytext)) eq "francais") || (lc(&trim($smsbodytext)) eq "espaniol") || (lc(&trim($smsbodytext)) eq "ingles") || (lc(&trim($smsbodytext)) eq "frances") || (lc(&trim($smsbodytext)) eq "espanol")){
	
	    #set user sms language to selected language.
	
		    $returnval 	   =  &language_status(&trim($fromnumber),lc(&trim($smsbodytext)));
		    $sms_function  =  "language_status";
	
	}elsif (lc(&trim($smsbodytext)) eq "pin" || (lc(&trim($smsbodytext)) =~ m/^(changepin)/ || lc(&trim($smsbodytext)) =~ m/^(change pin)/) || (((lc(&trim($last_sms))) eq "changepin" || (lc(&trim($last_sms))) eq "change pin") && (&trim($smsbodytext) =~ m/^(\d)+$/))){
	
	    #send pin information to user if user send 'pin'
	    #authenticate user by credit card and change pin number  if user send'changepin'
	
	    if((&trim($smsbodytext)) =~ m/^(\d)+$/){			
	
		        $sms_session=0;
	    }
	
	     my @pinInfo = &process_pin($service_id);
	
	    if($pinInfo[1] eq 1 || $pinInfo[1] eq -1){			
	
			$sms_session  =  1;
			$smsbodytext  =  "processed_pin";
	    }
	
	    $returnval=$pinInfo[0];
	    $sms_function="process_pin";
		 
	}elsif ((lc(&trim($smsbodytext))=~ m/^(forward)+\s+((\w[a-zA-Z]+)(\s?))+\,+(\s?)+(\d+)$/) || (lc(&trim($msg_info)) eq "forward") && (lc(&trim($smsbodytext))=~ m/^(\d+)$/)){
	    
	    #add forwarding number to existing contact.
	    
		    my @array 	  =  &addnew_forward_number(&trim($fromnumber),lc(&trim($smsbodytext)),$service_id);
		    $returnval    =  $array[0];
		    $sms_session  =  $array[1];
		
		    $sms_function =  "addnew_forward_number";
	
	}elsif ((lc(&trim($smsbodytext)) eq "delete") || ( lc(&trim($last_sms)) eq "delete" && lc(&trim($smsbodytext))=~ m/^(delete)+\s+((\w[a-zA-Z]+)(\s?)+(\w+)?)$/) || (lc(&trim($last_sms)) eq "delete" && lc(&trim($smsbodytext))=~ m/^(delete)+\s+(\d+)$/)){
	    
	    #delete existing contact number  
	    
		my @array       =  &do_delete(&trim($fromnumber),lc(&trim($smsbodytext)),$service_id,lc(&trim($last_sms)));
		$returnval      =  $array[0];
		$sms_session    =  $array[1];
		my $error       =  $array[2];
		my @getCounter  =  &errorCounter($error);
	    
	    if ($getCounter[0] eq 5)
	    {
			my $message  =  &Message("DELETE_CUSTOM_SUP");    
			$returnval   =  "$message";
			$sms_session =  1;
	    }
	    
	    $sms_function="do_delete";
	
	}elsif ((lc(&trim($smsbodytext)) eq "search" ) || (lc(&trim($last_sms)) eq "search" )){
	
	    #search an existing contact by name or dialnumber.
		    my @returnval  =  &do_search(&trim($fromnumber),lc(&trim($smsbodytext)),$service_id,$last_sms);
	
	    $returnval 	   =  $returnval[0];
	    $sms_session   =  $returnval[1];
	    my $error      =  $returnval[2];
	    my @getCounter = &errorCounter($error);
	
		    if ($getCounter[0] eq 3)
		    {
				$sms_session = 1;
		    }
	
	    $sms_function="do_search";
	
	}elsif (lc(&trim($smsbodytext)) eq "add credit card" || lc(&trim($last_sms)) eq "add credit card"){
	
	    #add credit card details to user profile
	
		    my @array 	  =  &add_credit_card(&trim($fromnumber),lc(&trim($smsbodytext)),$service_id,$last_sms);
		    $returnval 	  =  $array[0];
		    $sms_session  =  $array[1];
		    my $error 	  =  $array[2];
	
	    my @getCounter = &errorCounter($error);
	
		    if ($getCounter[0] eq 3)
		    {
				$sms_session = 1;
		    }
	    $sms_function = "add_credit_card";
	
	}elsif ( (lc(&trim($smsbodytext)) eq "recharge") || ((lc(&trim($smsbodytext)) =~ m/^\$(\d)+$/) && (lc(&trim($last_sms)) eq "recharge")) || ((lc(&trim($smsbodytext)) eq "yes") && (lc(&trim($last_sms)) eq "recharge")) || ((lc(&trim($smsbodytext)) eq "no") && (lc(&trim($last_sms)) eq "recharge")) ){
	
	    #recharge user account
	
	    my @array 	  =  &do_recharge(&trim($fromnumber),lc(&trim($smsbodytext)),$service_id,$last_sms);
	    $returnval 	  =  $array[0];
	    $sms_session  =  $array[1];
	    my $error 	  =  $array[2];
	
	    my @getCounter = &errorCounter($error);
	
		    if ($getCounter[0] eq 5)
		    {
	
			my $message     =  &Message("CUSTOMER_SUPPORT_INFO");
			$returnval      =  "$message";
			$sms_session    =  1;
	
		    }
	   $sms_function   = "do_recharge";
	   
	}elsif (lc(&trim($smsbodytext)) eq "auto recharge" || lc(&trim($last_sms)) eq "auto recharge" || (lc(&trim($last_sms)) eq "\$5") || (lc(&trim($last_sms)) eq "\$2")){
	
	    #auto recharge user account
            my @array = &auto_recharge($fromnumber,$smsbodytext,$service_id,$last_sms); # return returnval,session,error
	
	    $returnval 	        =  $array[0];
	    $sms_session        =  $array[1];
	    my $error 	        =  $array[2];
	    my @getCounter      =  &errorCounter($error);
	
	    if ($getCounter[0] eq 5)
	    {
		    	$returnval      =  &Message("AR_CUSTOMER_INFO");
			    $sms_session    =  1;
	    }
	
	    if (lc(&trim($smsbodytext)) eq "auto recharge")
	    {
		        my $session 	  =  &getSessionObj;	
		        my $auto 	      =  $session->param("auto");
		        my $low_balance   =  $session->param("low_balance");
		        my $recharge_amt  =  $session->param("recharge_amount");
		        
			if (defined($auto))		{$session->clear(["auto"]);}
		        if (defined($low_balance))	{$session->clear(["low_balance"]);}
		        if (defined($recharge_amt))	{$session->clear(["recharge_amount"]);}
	    }
	    $sms_function   = "auto_recharge";
	#all the invalid format loops
	}else
	{
	    
	    #if all condition invalid
	    
		$sms_session    =  0;
		my $error       =  "";
	    
	    #error in reroute format
	    
		if ((lc(&trim($last_sms)) eq "reroute") || (lc(&trim($last_sms)) eq "2"))
		{
			my @getUserroute  =  &userReroute($isValidUser,$StatusValue,lc(&trim($smsbodytext)),&trim($fromnumber));
			$reroutecount	  =  $getUserroute[0];
			$reroutemeessage  =  $getUserroute[1];
		}
	    
		my $session_value  =  &getSessionObj;
		my $action         =  $session_value->param("reroute");
		
		
		if($reroutecount gt 0 && (&trim($smsbodytext))){
				
			$returnval     =  $reroutemeessage;
			$session_value->param("reroute" ,"action1");
		        $session_value->clear(["duplicate"]);
			$sms_function  =  "userReroute";
		}
	    
	    #if incorect format in reroute 
	    
		elsif((defined $action) && (defined $last_sms) && (lc(&trim($last_sms))) eq "reroute" || (lc(&trim($last_sms))) eq 2 && $action eq "action1")
		{
		    my $duplicate = $session_value->param("duplicate");
		
		    if($duplicate eq 1)
		    {
		        $returnval =&Message("WRONG_DIAL_NUMBER");	
		
		        my $value	=  $session_value->param("error");
		        $value          =  $value + 1;
		        $session_value->param("error",$value);
		   
		        if ($value eq 5)
		        {
			
		          $returnval   = &Message("CUSTOMER_SUPPORT_INFO");
		          $session_value->clear(["error"]);
		          $session_value->clear(["duplicate"]);
		          $sms_session = 1;
		        }
		
		   }
		  else
		  {
				$returnval  =  &Message("ROUTE_ERROR_INFO");
				my $value   =  $session_value->param("error");
				$value      =  $value + 1;
				$session_value->param("error",$value);
				
				if ($value eq 5)
				{
			
						$returnval   =  &Message("CUSTOMER_SUPPORT_INFO");
						$session_value->clear(["error"]);
						$session_value->clear(["error_counter"]);
						$sms_session =  1;
			
				}
		  }
	    }elsif($reroutecount eq 0){
			
			$returnval  =  &Message("CONTACT_NOT_FOUND_INFO");
			my $value   =  $session_value->param("contact_error");
			$value 	    =  $value + 1;
			$session_value->param("contact_error",$value);
				
		    if ($value eq 5)
		    {
			  $returnval      =  &Message("CUSTOMER_SUPPORT_INFO");
			  $session_value->clear(["contact_error"]);
			  $sms_session    =  1;
		    }
			    
	    #if incorect format in reroute last call
			    
	    }elsif((lc(&trim($last_sms)) eq "reroute last call") || (lc(&trim($last_sms)) eq 10)){
				
			$returnval      =  &Message("ROUTE_ERROR_INFO");
			my $value       =  $session_value->param("error_reroutelastcall");
			$value 	        =  $value + 1;
			$session_value->param("error_reroutelastcall",$value);
				
		    if ($value eq 5)
		    {
               $returnval      =  &Message("CUSTOMER_SUPPORT_INFO");
               $session_value->clear(["error_reroutelastcall"]);
	       $sms_session    =  1;
		    }
				    
	    #if incorect format in refer a friend
				    
	    }elsif((lc(&trim($last_sms)) eq "refer") || (lc(&trim($last_sms)) eq 5)){
					
			$returnval       =  &Message("INVALID_REFER_FORMAT");
			my $value        =  $session_value->param("error_refer");
			$value 	         =  $value + 1;
			$session_value->param("error_refer",$value);
				
		    if ($value eq 5)
	        {
		      $returnval 	  =  &Message("REFER_CUSTOM_SUP");
		      $session_value->clear(["error_refer"]);
		      $sms_session        =  1;
		    }
			
	    # Invalid format in add new contact
				
	    }elsif((lc(&trim($last_sms)) eq "addnew") || (lc(&trim($last_sms)) eq "add new") || ($last_sms eq 3)){
					
			$returnval      =  &Message("ADD_CONTACT_INVALID_FORMAT");
			my $value       =  $session_value->param("error_addnew");
			$value 	        =  $value + 1;
			$session_value->param("error_addnew",$value);
				
		     if ($value eq 5)
	            {
		      $returnval 	  =  &Message("ADD_CONTACT_CUSTOM_SUP");
		      $session_value->clear(["error_addnew"]);
		      $sms_session        =  1;
		    }
			
	    #default error message
	    
	    }else{		
			
		     my $message    =  $errormessage;
		     $message       =~ s/xxxxxxx/$smsbodytext/i;
		     $returnval     =  $message;
			
		}
			
	}
		
	 #set SMS in session
		
	if($sms_session eq 1){	
				
		    &set_sms_session($smsbodytext);
				
	}
				
	#return from number,sms to be send and function processed info
				
	return ($fromnumber,$returnval,$sms_function);
}

#======================isZenofonUser()=========================
# This function checks the sms sender is valid Zenofon user
#==============================================================

sub isZenofonUser(){
    my ($fromnumber,$smsbody)   =  @_;
    my $isValidUser             =  0;
    my $error                   =  0;
    $fromnumber                 =  &trim($fromnumber);
    my $form_key_int            =  clean_int($fromnumber);
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
			    my $sql 	=  "select 1,1,service.id,service.name,service.email,service_ani.ani from service join service_ani on (service.id = service_ani.service_id) where service_ani.ani = '$form_key_e164'";
			    my %hash 	=  database_select_as_hash($sql,"flag,id,name,email,ani");
			    foreach (sort keys %hash)
			    {
					$firstrecordid      =  $hash{$_}{id};
					$firstrecordflag    =  $hash{$_}{flag};
					$firstrecordname    =  $hash{$_}{name};
					$firstrecordemail   =  $hash{$_}{email};
					$firstrecordani     =  $hash{$_}{ani};
					last;
			    }	
						    
		            my $num_records =  keys( %hash ) ;
						
                    if ($num_records > 1)
                    {
						
	               #duplicate ANI+PIN ,ask user retry login with EMAIL+PIN
						
	               $isValidUser  =  1;
	               $error        =  0;
	               return ($isValidUser,$error,$firstrecordid,$firstrecordname,$firstrecordemail,$firstrecordani);
				
                    }
				
                    elsif ((defined $firstrecordflag) && $firstrecordflag eq 1)
                    {
				
	               $service_found    =  1;
	               $service_id       =  $firstrecordid;
	               $service_name     =  $firstrecordname;
	               $service_email    =  $firstrecordemail;
	               $service_ani      =  $firstrecordani;
	               $error            =  0;
	               $isValidUser      =  1;             
				
                    }            
				
	        }
				
     }
				
    return ($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani);
}

#======================sms_client_status()=========================
# Updates the mute or unmute status of a user
#==================================================================
sub sms_client_status()
{
				    
    my ($Isvaliduser,$Body,$From)  =  @_;
    if($Isvaliduser eq 1 && ($Body eq "mute" || $Body eq "unmute" ))
    {
				    
	    $From        =~ tr/+/ /;
	    $From        =  &trim($From);
	    my @ArryCnt  =  database_select_as_array("SELECT count(*) AS Cnt FROM SMS_Client WHERE sms_ani = '$From'","Cnt");
	    my $count    =  $ArryCnt[0];
	    my $Status   =  "";
					
	    if($Body eq "mute")
	    {
		        $Status = 0;
	    }
	    else
	    {
			$Status = 1;
        }
				        
	if($count > 0)
        {
				        
		    my $sql  =  "UPDATE SMS_Client SET sms_status = '$Status' WHERE sms_ani = '$From'";
		    database_do($sql);
        }
        else
        {
				        
		    my $sql  =  "INSERT INTO SMS_Client (sms_ani,sms_status,language_status) VALUES ($From,'$Status','1')";
		    database_do($sql);
        }
				    
    }
					
}

#======================MuteUnmute_status()=========================
# checking the Mute & UnMute status of a user
# checks users status with the fromnumber to know whether he is in mute status or not
# returns the status value
#==================================================================
 
sub MuteUnmute_status()
{
    my ($fromnumber)    =  @_;
    my $Statusvalue     =  1;
    $fromnumber         =~ tr/+/ /;
    my $UserNo          =  &trim($fromnumber);
					    
    my @Status 	        =  database_select_as_array("SELECT sms_status FROM SMS_Client WHERE sms_ani = '$UserNo'","sms_status");
					    
    if(@Status > 0){
					    
		  $Statusvalue = $Status[0];
    }
					    
    return ($Statusvalue);
}

#========================sub Message()==============================
# SMS content flow from here - Customized text
#===================================================================
 
sub Message()
{
						
    my ($msg,$errorStatus,$error_type) 	= @_;
    my $rtnmsg 	                        = "";
    my $sql                             = "";
    my $language_status	                = "";
    my $message                         = "";
						   
    $sql           =  "select language_status from SMS_Client where sms_ani='$From'";
    my @language   =  database_select_as_array($sql);
							
    if (@language gt 0)
    {
							
		$language_status = $language[0];
    }else{
							
		$language_status = "1";
    } 
						    
    $sql      = "select count(*) from SMS_Client";
    my @count = database_select_as_array($sql);
							    
    my $count = $count[0];
						    
    if ($count eq 0)
    {
		$sql 	 =  "select messages from sms_messages where language_id = '$language_status' and message_type ='$msg'";
		my @info =  database_select_as_array($sql);
		$message =  $info[0];
    }else{
							
		$sql = qq [select 1,1,1,sms_messages.messages from SMS_Client,sms_languages,sms_messages
		where
		SMS_Client.language_status = sms_languages.id  and
		sms_messages.language_id = '$language_status' and
		sms_messages.message_type ='$msg'];
		
		my %hash = database_select_as_hash($sql,"1,1,messages");
		$message = $hash{1}{'messages'};
						    
    }
    if ($msg eq "") {$message = &Message("MENU_INFO");}#"Select your option \n 1) Mute/Unmute \n 2) Reroute \n 3) Add New Contact \n 4) Call History \n 5) Refer Friend \n 6) Last Call \n 7) Help \n 8) Select Language";}
							
	if(defined($errorStatus)) {
		    my @getcounter = &errorCounter($errorStatus,$error_type);
		    if($getcounter[0] eq 5){
							
		        $message = &Message("CUSTOMER_SUPPORT_INFO");
		    }
	}
						    
    return $message;	 
}


#======================addContact()================================
# Adds a new contact into the customer's account
#==================================================================
sub addContact()
{
    my ($fromnumber,$smsbodytext,$aservice_id,$confirmation) = @_;
    my @contactinfo     =   split(/\,/, $smsbodytext);
    my $fname 	        =   $contactinfo[0];
    my $fnumber	        =   &trim($contactinfo[1]);
    my $activenumber    =   "";    
    my $number	        =   "";
    my $returnval       =   "";
    my $count 	        =   1;
    my $frslot	        =   "Dial using route 1";
    my $fcallback       =   "Play beep beep";
    my $frouteann       =   "Don't choose route during call";
    my $findex_new      =   "Speed number is 1";
    my $fcallid	        =   "";
    my $fbalanceann     =   "Don't play balance";
    my $fsave           =   1;
    my $faction	        =   "dst";
    my $fcarrier        =   "";
    my $ok              =   1;
    my $index           =   "";
    #%t = %template_default;
					    
    my $tmy_url                         =  'servicetwilio.cgi';
    my $terror                          =  0;
    my $terror_number_format            =  0;
    my $terror_number_e164_format       =  0;
    my $terror_number_skype_format      =  0;
    my $terror_number_no_rate           =  0;
    my $terror_number_unknown_country   =  0;
    my $terror_no_more_index            =  0;
    my $terror_bad_index                =  0;
						    
    my $tnumber         = "";
    my $tname           = "";
    my $tcallid         = "";
    my $tcarrier        = "";
    my $tcallback       = "";
    my $routeann        = "";
    my $tbalanceann     = "";
    my $tindex          = "";
    my $tindex_new      = "";
    my $index_range_low = 1;
    my $index_range_hi  = 53;
					   
    # List of active numbers.
    my @activenumber = ("(646)434-4612","(646)434-4613","(646)434-4614","(646)434-4615","(646)434-4616","(646)434-4617","(646)434-4618","(646)434-4619","(646)434-4620","(646)434-4621","(646)434-4622","(646)434-4623","(646)434-4624","(646)434-4625","(646)434-4626","(646)434-4627","(646)434-4628","(646)434-4629","(646)434-4630","(646)434-4631","(917)284-9432","(646)873-6314","(646)873-6324","(646)873-6341","(646)873-6342","(646)873-6374","(646)873-6394","(646)873-6913","(646)873-6914","(646)873-6927","(646)873-6928","(646)873-6929","(646)873-6934","(201)204-1821","(201)204-1822","(201)204-1823","(201)204-1824","(201)204-1825","(201)204-1826","(201)204-1827","(201)204-1828","(201)204-1829","(201)204-1830","(201)204-1831","(201)204-1832","(201)204-1833","(201)204-1834","(201)204-1835","(201)204-1836","(201)204-1838","(201)204-1839","(201)204-1840","(201)204-1841",);
						
     #--------------------------------------------------
     # get index by form or find a free one if new=1
     #--------------------------------------------------
	 
    my $tindex_is_new = 0;
	
    # Save new contact
	
    my  $formnew  =  1;
	
    if ($formnew eq 1)
    {
		while ($count <= 53){
			    
			    my $value_to_check = "dst_".$count."_number";
					
			    my @array = database_select_as_array(qq(select value from service_data where target="$aservice_id" and name like "$value_to_check"));
			    if(! defined ($array[0]) ){
						
					$index = $count;
					last;
			    }
			    $count++;
		}
					    
		if ($index eq "")
		{
						
				$terror                 =  1;
				$terror_no_more_index 	=  1;
				$ok                     =  0;
        }
						
		$tindex_is_new = 1;
    }
					    
    $tindex             =  $index;
    my $index_new       =  &clean_int(substr($findex_new,0,10));
						    
    if ( ($index_new lt $index_range_low) || ($index_new gt $index_range_hi) || ($index_new eq "") )
    {
					 
		    $index_new = "";
    }
						
    $tindex_new = $index_new;
	
    #--------------------------------------------------
    # try to save
    #--------------------------------------------------
	
    if ( ($ok eq 1) && ($fsave eq 1) )
		{
					
		    $number    	        =  clean_str(substr($fnumber,0,1024),":-_()+.");	
		    my $name            =  clean_str(substr($fname,0,1024),"-_():<>\@.");
		    my $callid          =  clean_int(substr($fcallid,0,1024));
		    my $carrier	        =  clean_str(substr($fcarrier,0,1024));
		    $carrier	        =  (exists($carriers_list{$carrier})) ? $carrier : "";
		    my $callback        =  clean_int(substr($fcallback,0,1024));
		    $routeann 	        =  clean_int(substr($frouteann,0,1024));
		    my $balanceann      =  clean_int(substr($fbalanceann,0,1024));
		    my $rslot           =  clean_int(substr($frslot,0,1024));
		    $rslot    	        =  (index("|1|2|3|4|5|6|7|8|9|","|$rslot|") eq -1) ? 1 : $rslot;
		    #$rslot    = &data_get("service_data",$app{service_id},"dst_".$index."_rslot");
			#
				    
				# check and format number
					
		my ($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($number);
	        my $tnumber_status             =  $number_status;
	        my $tnumber_raw                =  $number;
	        my $tnumber_clean              =  $number_clean;
	        my $tnumber_format             =  $number_format;
	        my $tnumber_format_skype       =  ($number_format eq "SKYPE") ? 1 : 0;
	        my $tnumber_format_sip         =  ($number_format eq "SIP") ? 1 : 0;
					
				if ($number_status ne "OK")
				{
					
						$ok 	        =  0;
						$terror 	=  1;
						
						if ($number_format eq "SKYPE")
			                        {
			                                $terror_number_skype_format = 1;
						}
						elsif ($number_format eq "SIP")
						{
				            
								if ($number_status eq "UNKNOWNCOUNTRY")
								{
							
										 $terror_number_unknown_country = 1;
								}
								else
				             
								{
										 $terror_number_e164_format = 1;
								}
						}else{
					
								$terror_number_format = 1;
						}
						
				}else{
						$number = $number_clean;
				}
					     
				# check rate
					     
				if ($ok eq 1)
				{
						
						# pega rate_table, baseado no status do servico e slot da extensao
						my $rate_table_id = "";
						my $sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5
								,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9 from service, service_status
								where service.id='$aservice_id' and service.status = service_status.id  and service_status.deleted = 0 ";
		   
						 my %hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9");
					     
						if ($hash{1}{flag} eq "1")
						{
						
								my $user_slot 	=  &data_get("service_data",$aservice_id,"dst_".$index."_rslot") || 1;
								$rate_table_id 	=  $hash{1}{rate_slot_1};
								$rate_table_id 	=  ( ($user_slot eq 1) && ($hash{1}{rate_slot_1} ne "") ) ? $hash{1}{rate_slot_1} : $rate_table_id;
								$rate_table_id 	=  ( ($user_slot eq 2) && ($hash{1}{rate_slot_2} ne "") ) ? $hash{1}{rate_slot_2} : $rate_table_id;
								$rate_table_id 	=  ( ($user_slot eq 3) && ($hash{1}{rate_slot_3} ne "") ) ? $hash{1}{rate_slot_3} : $rate_table_id;
								$rate_table_id 	=  ( ($user_slot eq 4) && ($hash{1}{rate_slot_4} ne "") ) ? $hash{1}{rate_slot_4} : $rate_table_id;
								$rate_table_id 	=  ( ($user_slot eq 5) && ($hash{1}{rate_slot_5} ne "") ) ? $hash{1}{rate_slot_5} : $rate_table_id;
								$rate_table_id 	=  ( ($user_slot eq 6) && ($hash{1}{rate_slot_6} ne "") ) ? $hash{1}{rate_slot_6} : $rate_table_id;
								$rate_table_id 	=  ( ($user_slot eq 7) && ($hash{1}{rate_slot_7} ne "") ) ? $hash{1}{rate_slot_7} : $rate_table_id;
								$rate_table_id 	=  ( ($user_slot eq 8) && ($hash{1}{rate_slot_8} ne "") ) ? $hash{1}{rate_slot_8} : $rate_table_id;
								$rate_table_id 	=  ( ($user_slot eq 9) && ($hash{1}{rate_slot_9} ne "") ) ? $hash{1}{rate_slot_9} : $rate_table_id;
						}
					     
						# agora tenta pegar rate
					     
						if ($rate_table_id ne "")
						{
								%hash = &multilevel_rate_table_get($number,$rate_table_id);
								if ($hash{ok_to_use} ne 1)
								{
										 $terror                = 1;
										 $terror_number_no_rate = 1;
										 #$ok = 0; #Temp
								}
						}
				         
						else
						{
								$terror                = 1;
								$terror_number_no_rate = 1;
								#$ok = 0; #Temp
						}
				     
				}
				     
				# if all ok, lets save data
					     
				if ($ok eq 1)
				{
						if ( ($index_new ne "") && ($index_new ne $index) )
						{
								 my $v1  =  &data_get("service_data",$aservice_id,"dst_".$index_new."_callid");
								 my $v2  =  &data_get("service_data",$aservice_id,"dst_".$index_new."_number");
								 my $v3  =  &data_get("service_data",$aservice_id,"dst_".$index_new."_name");
								 my $v4  =  &data_get("service_data",$aservice_id,"dst_".$index_new."_carrier");
								 my $v5  =  &data_get("service_data",$aservice_id,"dst_".$index_new."_rslot");
			        
								&data_set("service_data",$aservice_id,"dst_".$index_new."_name"     ,$name);
								&data_set("service_data",$aservice_id,"dst_".$index_new."_callid"   ,$callid);
								&data_set("service_data",$aservice_id,"dst_".$index_new."_number"   ,$number);
								&data_set("service_data",$aservice_id,"dst_".$index_new."_carrier"  ,$carrier);
						
								&data_set("service_data",$aservice_id,"dst_".$index_new."_rslot"   ,$rslot);
								&data_set("service_data",$aservice_id,"dst_".$index."_name"        ,$v3);
								&data_set("service_data",$aservice_id,"dst_".$index."_callid"      ,$v1);
								&data_set("service_data",$aservice_id,"dst_".$index."_number"      ,$v2);
								&data_set("service_data",$aservice_id,"dst_".$index."_carrier"     ,$v4);
								&data_set("service_data",$aservice_id,"dst_".$index."_rslot"       ,$v5);
								&data_set("service_data",$aservice_id,"dst_".$index."_callback"    ,$callback);
								&data_set("service_data",$aservice_id,"dst_".$index."_routeann"    ,$routeann);
								&data_set("service_data",$aservice_id,"dst_".$index."_balanceann"  ,$balanceann);
						}
						else
						{
				             
								&data_set("service_data",$aservice_id,"dst_".$index."_name"       ,$name);
								&data_set("service_data",$aservice_id,"dst_".$index."_callid"     ,$callid);
								&data_set("service_data",$aservice_id,"dst_".$index."_number"     ,$number);
								&data_set("service_data",$aservice_id,"dst_".$index."_carrier"    ,$carrier);
								&data_set("service_data",$aservice_id,"dst_".$index."_rslot"      ,$rslot);
								&data_set("service_data",$aservice_id,"dst_".$index."_callback"   ,$callback);
								&data_set("service_data",$aservice_id,"dst_".$index."_routeann"   ,$routeann);
								&data_set("service_data",$aservice_id,"dst_".$index."_balanceann" ,$balanceann);
						}
						
						$activenumber=$activenumber[$index-1];
					       
				}
				else
				{
					     
						$ok=0;
					       
				}
					 
		}
					 
		if($ok==1){
						
				$fname  = ucfirst($fname);
				$number = &multiformat_phone_number_format_for_user($number);
						
		  #set contact added message
						
				$returnval = &Message("ADD_CONTACT_RESP_INFO");
				$returnval =~ s/xxxx/$fname/i;
				$returnval =~ s/xxxxx/$number/i;
				$returnval =~ s/xxxxxx/$activenumber/i;
					     
	
					 
		}elsif($terror_no_more_index eq 1){
					 
				 $returnval = &Message("CONTACT_LIMIT_INFO");
					 
		}elsif($terror_number_format eq 1){
						
				 $returnval = &Message("REFER_INCORRECT_NUMBER_INFO");
					 
		}else{
						
				$returnval = &Message("ADD_CONTACT_CUSTOM_SUP");
		}
					 
    return $returnval;
}
	
#======================userReroute()===========================
# Reroute the path of the user
#==============================================================

sub userReroute()
{
    my ($isValidUser,$StatusValue,$smsbodytext,$fromnumber,$route_to_change) = @_;
    $smsbodytext          =  lc(&trim($smsbodytext));
						 
    my @isValidUserArray1 =  &isZenofonUser(&trim($fromnumber),$smsbodytext);   
    my $isValidUser1      =  $isValidUserArray1[0];
    my $service_id        =  $isValidUserArray1[2];
						 
    my $name	          =  "";
    my $orginal_smstext	  =  $smsbodytext;
    my $value             =  "";
    my $index	          =  "";
    my $count             =  0;
    my $returnval         =  "";
						 
    my $sql 		      =  "";
    my $sel 		      =  "";
    my $dst;
    my $getname;
    my $finalval;
    my $dial_number;
    my $dublicateindex;
    my $flag              =  0 ;
    my $cnt               =  "";
    my $error             =  "";
    my $session           =  "";
    my $i                 =  0;
	
    #reroute status value    
					 
    my $reroutestatusvalue =  &getSMSStatus(2,$fromnumber);
    $fromnumber            =~ tr/+/ /;
		
     #if SMS is contact number, check number format.			 
    if($smsbodytext =~ m/\d/){
						
			my ($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($smsbodytext);
			$smsbodytext=$number_clean;
    }
					 
	#checking duplicate contact
	
    my @activenumber    = ("(646)434-4612","(646)434-4613","(646)434-4614","(646)434-4615","(646)434-4616","(646)434-4617","(646)434-4618","(646)434-4619","(646)434-4620","(646)434-4621","(646)434-4622","(646)434-4623","(646)434-4624","(646)434-4625","(646)434-4626","(646)434-4627","(646)434-4628","(646)434-4629","(646)434-4630","(646)434-4631","(917)284-9432","(646)873-6314","(646)873-6324","(646)873-6341","(646)873-6342","(646)873-6374","(646)873-6394","(646)873-6913","(646)873-6914","(646)873-6927","(646)873-6928","(646)873-6929","(646)873-6934","(201)204-1821","(201)204-1822","(201)204-1823","(201)204-1824","(201)204-1825","(201)204-1826","(201)204-1827","(201)204-1828","(201)204-1829","(201)204-1830","(201)204-1831","(201)204-1832","(201)204-1833","(201)204-1834","(201)204-1835","(201)204-1836","(201)204-1838","(201)204-1839","(201)204-1840","(201)204-1841",);
    my $size = @activenumber;
					  
    my @reroute         =  database_select_as_array("SELECT name FROM service_data WHERE value = '$smsbodytext' and target = '$service_id' and name like 'dst%'");
    my @reroute_name    =  database_select_as_array("SELECT value FROM service_data WHERE value = '$smsbodytext' and target = '$service_id' and name like 'dst%'");
    my $val             =  scalar (@reroute);
					 
    while ($i < $val){
							
			my @indexval  = split(/_/,$reroute[$i]);
			$dst 	      = $indexval[0];
						
			$index 	      = $indexval[1];
						
			$getname      = $indexval[2];
						
			$finalval     = $reroute[$i];
						
			$dial_number  = $activenumber[$index-1];
						
			$dial_number  =~ s/[^0-9]*//g;
						
			$count++;
						
			$name .=  $count.")".$reroute_name[$i]." - ".$activenumber[$index-1].",\n" ;
						
			$i++;
    }
						
	my $message     = &Message("DUPLICATE_CONTACT_INFO");
	$message        =~ s/xxxx/$name/i;
	$name           = $message;
	
	#get index value if SMS is dial number
	
	for ( my $i=0; $i<$size; $i++)
	{
					 
	    my $a = $activenumber[$i];
						
	    if($orginal_smstext =~ m/^(\((\d{0,3})\)(\d{0,3})(\-)(\d{0,4}))/){
						
				    if($a eq $orginal_smstext)
					     
					    {
					       $dublicateindex = $i+1;
					       $flag           = 1;
					    }
	    }else{
					        
			 $a =~ s/[^0-9]*//g;
			 if($a eq $orginal_smstext)
						
				{
					$dublicateindex = $i+1;
					$flag           = 1;
				 }
        }
    }
						
    if($flag eq 1)
    {
		#set index value
		$index 	        =  $dublicateindex;
		$dial_number    =  $activenumber[$index];
		$dial_number    =~ s/[^0-9]*//g;
		$count 	        =  1;
    }
	#get name,number, and route value for selected contact.
	
	my $_name       =  &data_get("service_data",$service_id,"dst_".$index."_name");
	my $_number     =  &data_get("service_data",$service_id,"dst_".$index."_number");
	my $_rslot      =  &data_get("service_data",$service_id,"dst_".$index."_rslot");
					 
    if($isValidUser eq 1)
	{
		if($StatusValue eq 1)
		{
		    if($smsbodytext ne ("mute" || "unmute"))
		    {
				if($count>0)
				{
				    if($count eq 1)
					    {
						#if single contact found 
						
						$sel            =  "select value from service_data where target = $service_id and name = 'dst_".$index."_rslot'";
						my @Status      =  database_select_as_array($sel,"value");
						my $Getrslot    =  $Status[0];
						my $delsql      =  "select count(*) AS Cnt from sms_route_temp where sms_target = $service_id and sms_name = 'dst_".$index."_rslot'";
						my @delCnt      =  database_select_as_array($delsql,"Cnt");
						my $count       =  $delCnt[0];
						
						if($count gt 0)
							{
							    #delete old request
							    my $deleteroute = "DELETE FROM sms_route_temp where sms_target = $service_id and sms_name = 'dst_".$index."_rslot'";
							    database_do($deleteroute);
							}
								
						my $datetime = &getDatetime();
						#save request
						if(defined($route_to_change)){
								#request from reroute last call			
							    $sql = "INSERT INTO sms_route_temp(sms_target,sms_name,sms_value,sms_ani,sms_dial_number,sms_contact_name,sms_contact_number,sms_date_time,sms_next_route,sms_confirmation) values ('$service_id','dst_".$index."_rslot','$Getrslot','".&trim($fromnumber)."','$dial_number','$_name','$_number','$datetime','$route_to_change','0') ";
						}else{
								#request for reroute SMS			
							    $sql = "INSERT INTO sms_route_temp(sms_target,sms_name,sms_value,sms_ani,sms_dial_number,sms_contact_name,sms_contact_number,sms_date_time,sms_confirmation) values ('$service_id','dst_".$index."_rslot','$Getrslot','".&trim($fromnumber)."','$dial_number','$_name','$_number','$datetime','0') ";
						}		
						database_do($sql);
						
						#set route selection message to user.					
						$returnval = &Message("ROUTE_SELECTION_INFO");
										   
					   }else{
						
						#For duplicate contacts.			
								$returnval         =  $name;
								my $session_value  =  &getSessionObj();
								$session_value->param("duplicate","1");
					   }
				}
											
				elsif( lc(&trim($smsbodytext)) =~ m/^(\w)(\s?)(\d{1,2})$/i || lc(&trim($smsbodytext)) eq "no")											
				{
					#if user select route value for selected contact.
					
					if(lc(&trim($smsbodytext)) =~ m/(^r(\s?)(\d))$/i || lc(&trim($smsbodytext)) eq "no")
					{
											
					    if($reroutestatusvalue gt 0)
						{
								#change route value for selected contact.
								
								my $routetxt    =  "";
								my $routeval    =  "";
								
								if(lc(&trim($smsbodytext)) =~ m/(^r(\s?)(\d))$/i){
											
										my @reroute     =  split(/\s?(\d+)$/ , $smsbodytext); #split reoute and value eg: r1
										$routetxt       =  $reroute[0];
										$routeval       =  $reroute[1];
								}				
										
						         $routeval              =~ /^(\d)/;
						         my $finalrouteval      =  $1;
						         my $returnval1         =  $smsbodytext;
						         my $_rslot             =  &data_get("service_data",$service_id,"dst_".$index."_rslot");
									                
						         $sel = "select 1,1,1,sms_route_id,sms_name,sms_value,sms_dial_number,sms_contact_name,sms_contact_number,sms_next_route from sms_route_temp where sms_ani = ".&trim($fromnumber)." order by sms_route_id DESC limit 0,1 ";
											
						         my %hashval = &database_select_as_hash($sel,"1,1,sms_route_id,sms_name,sms_value,sms_dial_number,sms_contact_name,sms_contact_number,sms_next_route");
											
						         my $sms_id             =  $hashval{1}{sms_route_id};
						         my $rslot_name         =  $hashval{1}{sms_name};
						         my $rsloat_value       =  $hashval{1}{sms_value};
						         my $dailnumber         =  $hashval{1}{sms_dial_number};
						         my $contact_name       =  $hashval{1}{sms_contact_name};
						         my $contact_no         =  $hashval{1}{sms_contact_number};
						         my $route_next	        =  $hashval{1}{sms_next_route};
									                
					             if(lc(&trim($smsbodytext)) eq  "no"){
											
							       $routetxt        = "route";
							       $finalrouteval=$routeval= $route_next;
					            }
									                
											
					             $sql="update service_data set value = $finalrouteval where target = $service_id and name='$rslot_name'";
					             database_do($sql);
									                
					             $sql="update sms_route_temp set sms_confirmation = 1 where sms_route_id = $sms_id ";
					             database_do($sql);
											
					             my $message = &Message("ROUTE_CHANGE_INFO");
											
					             $message     =~ s/xxxx/$finalrouteval/i;
					             $message     =~ s/xxxxx/$contact_no/i;
					             $message     =~ s/xxxxxx/$contact_name/i;
					             $returnval   =  $message;
											
					             &getSMSStatus(1,$fromnumber);
											
						}else{
						    $returnval = &Message("MENU_INFO");
						}
											
				   }else{
							
						#send error message if route selection format is incorrect
						
						$returnval        =  &Message("ROUTE_ERROR_INFO");
						my $session_value =  &getSessionObj;
						my $value         =  $session_value->param("error");
						$value            =  $value + 1;
						$session_value->param("error",$value);
											
						if ($value eq 5)
											
							{
								#send customer support message if error repeated 5 times
								
								$returnval = &Message("CUSTOMER_SUPPORT_INFO");
								$session_value->clear(["error"]);		
								$session_value->clear(["error_counter"]);
							}	
											
							$session = 0;
				  }
				}else{
				
											
						$returnval  =  &Message("CONTACT_NOT_FOUND_INFO");
						$error      =  1;
											
				}
		   }else{
											
				$returnval  = "";
											
                   }
		}    else
												
		{
			$count = 0;
											  
			$returnval = &Message("MUTE_STATUS_INFO");
		}
	}
													
   return ($count,$returnval,$error,$session);
													
}

#======================getSessionObj()========================='
# Session creation for the error counter
#==============================================================

sub getSessionObj(){
													
    #my $cgi=new CGI;
    #my $sid=$cgi->cookie('ID');
													
    my $session='';
    if(!defined($sid)){
        #create new session	
													
		$session=new CGI::Session();
		$sid=$session->id;
													
	#store session id in cookie.
		my $cookie=$cgi->cookie(ID => $sid);
		print $cgi->header(-cookie =>$cookie);
													
    }else{
													
		#set session id if session is already set
		$session=new CGI::Session(undef,$sid);
    }
													
    return $session;
}

#======================errorCounter()==========================
# Increments the session's error counter
#==============================================================
sub errorCounter(){
													
    my ($errid,$errtype) = @_;
    my $sess_err_type='';
    my $session=&getSessionObj;
													
    if($errid eq 0)
    {													
		    
		    $session->clear(["error_counter"]);
    }
    else
    {
			#get error_counter and error_type from session										
		    $counter         =  $session->param("error_counter");
		    $sess_err_type   =  $session->param("error_type");
														
		    if($sess_err_type eq $errtype){
				
				#if error type and prev error type equal then increment counter									    
				$counter++;
													
		    }else{
				
				#if error type is new set error counter as 1
				$counter=1;
		    }
													
		    if($counter ge 5){
					
				#if error counter greater than or equal to 5 set error counter as zero.								
			 $session->param("error_counter",0);
			 $session->param("error_type",'');
													
		   }else{
													
			$session->param("error_counter",$counter);
			$session->param("error_type",$errtype); 
                   }
    }
													
    return $counter;
													
}

#======================setSession()============================
# Storing current user SMS in session
#==============================================================
sub set_sms_session(){
													
	    my ($smsbodytext) = @_;
	    $smsbodytext = lc(&trim($smsbodytext));
	    my $session       = &getSessionObj;
	    $session->param("sms_input",$smsbodytext);
													
}


#======================setSession()============================
# Get user Last SMS requset From session
#==============================================================

sub get_sms_session(){
													
		    my $session	        =  &getSessionObj;
		    my $sms_input       =  $session->param("sms_input");
		    return $sms_input;
}

#======================rerouteLastCall()========================
# This function rerouteLastCall
#==============================================================

sub rerouteLastCall()
{
    my ($fromnumber,$smsbodytext) = @_;
													
    my @isValidUserArray1       =  &isZenofonUser(&trim($fromnumber),$smsbodytext); # return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
    my $isValidUser1            =  $isValidUserArray1[0];
    my $service_id              =  $isValidUserArray1[2];
													
    my @status 	        =  &MuteUnmute_status(&trim($fromnumber));
    my $StatusValue     =  $status[0];
    my $session         =  "";
    my $error           =  "";
    my $returnval       =  '';
	
	#check mute unmute status
	
    if ($StatusValue eq 1){
		
		my $sql = "";
													
		# set sms_status value for from number
													
		&getSMSStatus(0,$fromnumber);
			
		#get last call with duration greater than 11 min and less than 60 min
		
		$sql = "select 1,1,1,calls_log.id,calls_log.datetime_start,calls_log.datetime_stop,calls_log.ani,calls_log.did,calls_log.dst,calls_log.service_id,calls_log.rate_slot,calls.seconds from calls_log,calls where (calls_log.billing_id=calls.id)and calls_log.ani = '$fromnumber' and calls.seconds >11 and calls.seconds<60 order by id desc limit 1";
													
		my %hash = database_select_as_hash($sql,"1,1,id,datetime_start,datetime_stop,ani,did,dst,service_id,rate_slot,seconds");
													
		if(%hash gt 0){
													
				my $call_log_id     =  $hash{1}{id};
				my $datetime_start  =  $hash{1}{'datetime_start'};
				my $datetime_stop   =  $hash{1}{datetime_stop};
				my $fromnumber 	    =  $hash{1}{ani};
				my $dialnumber      =  $hash{1}{did};
				my $tonumber 	    =  $hash{1}{dst};
				my $rate_slot 	    =  $hash{1}{rate_slot};
				my $seconds         =  $hash{1}{seconds};
				
				#get call counter with duration less greater than 11 min and less than 60 min
				
				my $incomplete_erorr_counter  =  &getIncomplete_counter($fromnumber,$tonumber);
				$returnval                    =  &userReroute($isValidUser1,$StatusValue,$tonumber,$fromnumber);
				&errorCounter(1);
												    
				if($incomplete_erorr_counter>=5){
									           		        
						$returnval=&Message(16);
						
				}elsif(($incomplete_erorr_counter <= 1) && ($rate_slot ne 4)){
							
						#message to change the route value to r7						
						my $message     =  &Message("LAST_CALL_ROUTE_INFO");
						$message        =~ s/xxxx/$tonumber/i;
						$returnval      =  $message;
						$session        =  1;
						$error 	        =  0;
													
				}elsif(($incomplete_erorr_counter <= 1) && ($rate_slot eq 4)){
						
						#message to change the route value to r4							
						my $message     =  &Message("LAST_CALL_ROUTE");
						$message        =~ s/xxxx/$tonumber/i;
						$returnval      =  $message;
						$session        =  1;
						$error 	        =  0;
													
				}else{
													
					$returnval =  &Message("INCOMPLETE_CALL_INFO");
					$session   =  0;
					$error 	   =  1;
													
				}
		}else{
													
			$returnval  =  &Message("INCOMPLETE_CALL_INFO");
			$session    =  0;
			$error 	    =  1;
		}
    }else{
													
		$returnval = &Message("MUTE_STATUS_INFO");
    }
													
    return $returnval,$session,$error;
}

#======================getIncomplete_counter()========================
# Gets incomplete call counter
#=====================================================================

sub getIncomplete_counter()
{
													
    (my $fromnumber,my $tonumber)=@_;
    my $today      =  &getDatetime();#"2012-05-12 12:05:56";
    my $prev_time  =  &getDatetime(5);#"2012-05-12 11:50:25";
													
    my @StatusCnt = database_select_as_array("SELECT count(*) AS count  from calls_log,calls where calls_log.ani = '$fromnumber' and calls.seconds = 50 and calls_log.dst = '$tonumber' and datetime_stop >='$prev_time' and datetime_stop <='$today'","count");
													
    my $incomplete_erorr_counter=$StatusCnt[0];
    return $incomplete_erorr_counter;
}

#======================getDatetime()==================================
# Returns the time difference
#=====================================================================

sub getDatetime()
{
    my $datetime        = "";
    my $today	        = "";
    my($timediff,$date) =  @_;
    my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst);
													
    if(!defined($timediff)){
													
		    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);
		    $year       =  $year+1900;
		    $mon        =  $mon+1;
		    $datetime   =  "$year-$mon-$mday  $hour:$min:$sec";
    }else{
													
	        if(defined($date)){
													
		            ($year,$mon,$mday,$hour,$min,$sec) = split(/[\s\-:]+/, $date);
			    $year       =  $year-1900;
			    $mon        =  $mon-1;
			    $today      =  mktime($sec,$min,$hour,$mday,$mon,$year)-($timediff*60);
			    ( $sec, $min, $hour, $mday, $mon, $year) = localtime($today);
													
		}else{
												    
			    $today = time()-($timediff*60);
			    ( $sec, $min, $hour, $mday, $mon, $year) = gmtime($today);
		}
													
		$year 	  =  $year+1900;
		$mon      =  $mon+1;
		$datetime =  "$year-$mon-$mday  $hour:$min:$sec";
	}
													
    return $datetime;
													
}
#======================getLastrequest()=================================
# This function checks the recent SMS functionality initiated by the user.
#=======================================================================
sub getLastrequest()
{
	    my ($fromnumber)=@_;
	    my %sms=();
													
	    my $sql = "select 1,1,sms_route_id,sms_target,sms_name,sms_value,sms_ani,sms_dial_number,sms_contact_name,sms_contact_number,sms_date_time,sms_next_route,sms_confirmation from sms_route_temp where  sms_ani='$fromnumber' order by sms_route_id desc limit 1";
													
	    my %hash = &database_select_as_hash($sql,"1,sms_route_id,sms_target,sms_name,sms_value,sms_ani,sms_dial_number,sms_contact_name,sms_contact_number,sms_date_time,sms_next_route,sms_confirmation");
													
	    $sms{sms_route_id}	    =  $hash{1}{sms_route_id};
	    $sms{sms_target}	    =  $hash{1}{sms_target};
	    $sms{sms_name}          =  $hash{1}{sms_name};
	    $sms{sms_value}         =  $hash{1}{sms_value};
	    $sms{sms_ani}           =  $hash{1}{sms_ani};
	    $sms{sms_dial_number}   =  $hash{1}{sms_dial_number};
	    $sms{sms_contact_name}  =  $hash{1}{sms_contact_name};
	    $sms{sms_contact_number}=  $hash{1}{sms_contact_number};
	    $sms{sms_date_time}     =  $hash{1}{sms_date_time};
	    $sms{sms_next_route}    =  $hash{1}{sms_next_route};
	    $sms{sms_confirmation}  =  $hash{1}{sms_confirmation};
	    return %sms;
}

#======================getSMSStatus()===================================
# Maintains the command request from the user in the table(sms_route_temp)
#=======================================================================
sub getSMSStatus()
{
	    my ($action,$fromnumber)=@_;
	    my $sql;
												
    if($action == 0){
												
		        $sql="insert into sms_status (sms_status_value,sms_ani) values (1,'$fromnumber')";
			database_do($sql);
    }elsif($action ==1){
												
		        $sql="delete from sms_status where sms_ani='$fromnumber' ";
		database_do($sql);
												
    }elsif($action ==2){
												
		        my @rerouteStatusArray = database_select_as_array("SELECT sms_status_value FROM sms_status where sms_ani='$fromnumber' order by id desc limit 1","sms_status_value");
			my $reroutestatusvalue = 0;
												
			if(@rerouteStatusArray > 0){
												
					     $reroutestatusvalue = $rerouteStatusArray [0];
			}
												
			return $reroutestatusvalue;
    }
												
}

#======================callHistory()===================================
# Provides the detail of last 2 calls made by the customer
#======================================================================
sub callHistory()
{
	my ($fromnumber,$smsbodytext,$limit) = @_;
	my @isValidUserArray1 	=  &isZenofonUser(&trim($fromnumber),$smsbodytext); # return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
	my $isValidUser1        =  $isValidUserArray1[0];
	my $service_id	        =  $isValidUserArray1[2];
	my $returnval	        =  "";
	my $date                =  "";
	my $dst	                =  "";
	my $balance_before      =  "";
	my $rate_value	        =  "";
	my $name                =  "";
	my $value               =  "";
	my $i                   =  0;
	my $size                =  "";
	my $loop_index          =  1;
	my $keys                =  "";
	my $id 	                =  "";
												
	$i=0;
											 						
	my %ref_lp = "";
	
	#get calls details
	
	my $sql ="select 1,1,calls.date,calls.dst,calls.balance_before,calls.rate_value,service_data.name,service_data.value from calls,service_data where calls.ani = '$fromnumber' and calls.dst = service_data.value and calls.service_id = service_data.target and calls.service_id= '$service_id' order by id desc limit $limit";
												
	%ref_lp = database_select_as_hash_with_auto_key($sql,"1,1,date,dst,balance_before,rate_value,name,value");
	$size   = scalar keys %ref_lp;
												
	if ($size gt 0) {
												
		foreach $id (keys %ref_lp) {          
											  
                            $date               =   $ref_lp{$id}{date};
                            $dst                =   $ref_lp{$id}{dst};
                            $balance_before     =   $ref_lp{$id}{dalance_before};
                            $rate_value	        =   $ref_lp{$id}{rate_value};;
                            $name               =   $ref_lp{$id}{name};
                            $value              =   $ref_lp{$id}{value};
                           my @name             =   split(/_/, $name);
                           my $index            =   $name[1];
				
				#format date time details
				
			    my @t = $date =~ m!(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})!;
			    $t[1]--;
			    my $timestamp  =  timelocal $t[5],$t[4],$t[3],$t[2],$t[1],$t[0];
			    my $datetime   =  scalar localtime $timestamp;
												
			    if ($rate_value =~ m/((\d+)\.(\d{2}))/)
				    {
						    $rate_value = $1;
				    }
												
			    my $sql_next        =  "select value from service_data where target = $service_id and name = 'dst_".$index."_name'";
			    my @nameArray       =  database_select_as_array($sql_next,"value");
			    my $getName         =  $nameArray[0];
			    $sql                =  "select value from service_data where target = $service_id and name='dst_".$index."_rslot'";
			    my @rslotArray      =  database_select_as_array($sql,"value");
			    my $rslot           =  $rslotArray[0];
			    $i                  =  $i+1;
				
				#set message details								     
				$returnval = $returnval." $i. $getName, $value, $datetime, Route $rslot, \$$rate_value,\n";
				$loop_index++;
												
	        }
		
        my $message     = &Message("CALL_HISTORY_INFO");
        $message        =~ s/xxxx/$returnval/i;	    
        return $message;
												
	}
	else{
	
	#if no call details found
	$returnval = &Message("CALL_NOT_FOUND_INFO");
        }
}

#=============================sub lastCall()===================
# Provides the detail of last call made by the customer including
# their current balance
#==============================================================
sub lastCall()
{
    my ($fromnumber,$smsbodytext) = @_;
    my @isValidUserArray1       =  &isZenofonUser(&trim($fromnumber),$smsbodytext); # return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
    my $isValidUser1            =  $isValidUserArray1[0];
    my $service_id              =  $isValidUserArray1[2];
												
    my @status                  = &MuteUnmute_status(&trim($fromnumber));
    my $StatusValue             = $status[0];												
    my $returnval               = '';
    if ($StatusValue eq 1)
	{
												
		my $date            =  "";
		my $dst	            =  " ";
		my $balance_before  =  "";
		my $balance         =  "";
		my $rate_value      =  "";
		my $name            =  "";
		my $value           =  "";
		my $i               =  1;
			
		#get last call details
			
		my $sql = "select 1,1,1,calls.date,calls.dst,calls.balance_before,calls.rate_value,service_data.name,service_data.value from calls,service_data where calls.ani = '$fromnumber' and calls.dst = service_data.value and calls.service_id = service_data.target and calls.service_id='$service_id' order by id desc limit 1";   #$service_id
		my %hash = database_select_as_hash($sql,"1,1,date,dst,balance_before,rate_value,name,value");
												
		my $count       =  keys %hash;
		$date           =  $hash{1}{date};
		$dst 	        =  $hash{1}{dst};
		$balance_before =  $hash{1}{balance_before};
		$rate_value     =  $hash{1}{rate_value};
		$name 	        =  $hash{1}{name};
		$value 	        =  $hash{1}{value};
												
		if ($count gt 0)
		{
				my @name      =  split(/_/, $name);
				my $index     =  $name[1];
				my @t = $date =~ m!(\d{4})-(\d{2})-(\d{2})\s(\d{2}):(\d{2}):(\d{2})!;
				$t[1]--;
				my $timestamp =  timelocal $t[5],$t[4],$t[3],$t[2],$t[1],$t[0];
				my $datetime  =  scalar localtime $timestamp;
											    
				if ($rate_value =~ m/((\d+)\.(\d{2}))/)
				{
												
						$rate_value = $1;
				}
					#Get current balance 
												
					my %hash            = &database_select_as_hash("select 1,1,balance from service where id='$service_id'","1,balance");
					my $current_balance = $hash{1}{balance};
											    
					if ($current_balance =~ m/((\d+)\.(\d{2}))/)
					{
												
						$current_balance = $1;
					}
											    
					#Get user name
												
					$sql            =  "select value from service_data where target = $service_id and name = 'dst_".$index."_name'";
					my @nameArray 	=  database_select_as_array($sql,"value");
					my $getName     =  $nameArray[0];
											    
					#Get rslot value
												
					$sql ="select value from service_data where target = $service_id and name='dst_".$index."_rslot'";
					my @rslotArray = database_select_as_array($sql,"value");
												    
					my $rslot        =  $rslotArray[0];
					$rate_value      =  "\$$rate_value";
					$current_balance =  "\$$current_balance";
					#$returnval = $returnval."$i. $getName, $value, $datetime, \$$rate_value, Now balance is: \$$current_balance\n";
													
					$returnval = &Message("LASTCALL_INFO");
					$returnval =~ s/xx/$i/i;
					$returnval =~ s/xxx/$getName/i;
					$returnval =~ s/xxxx/$value/i;
					$returnval =~ s/xxxxx/$datetime/i;
					$returnval =~ s/xxxxxx/$rate_value/i;
					$returnval =~ s/xxxxxxx/$current_balance/i;
													
					return $returnval;  
		}  else {
					
				#if no call details found						    
				$returnval = &Message("CALL_NOT_FOUND_INFO");
		}
												
	}else{
												
	$returnval = &Message("MUTE_STATUS_INFO");	
												
	}
}
												
#======================sub refund()====================================
# user refund request details insert into new table (sms_call_refund)
#======================================================================

sub refund()
{
    my ($fromnumber,$smsbodytext) = @_;
												
    my @isValidUserArray1 =  &isZenofonUser(&trim($fromnumber),$smsbodytext); # return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
    my $isValidUser1      =  $isValidUserArray1[0];
    my $service_id        =  $isValidUserArray1[2];
												
    my @status 	        =  &MuteUnmute_status(&trim($fromnumber));
    my $StatusValue     =  $status[0];
    my $returnval       =  '';
												
    if ($StatusValue eq 1){
												
		     my $call_id = "";
				
		     #get last call details.								
    	     my $sql = "select 1,1,1,id from calls where ani ='$fromnumber' and service_id='$service_id' order by id desc limit 1";   #get call_id of last call
												
		     my %hash = database_select_as_hash($sql,"1,1,id");
		     my $count= keys %hash;
												
		    $call_id = $hash{1}{id};
												
			if ($count gt 0){
											    
				 #save request to refund the last call
				 
					my $sql      = "select count(*) from sms_call_refund where call_id='$call_id'";
					my @getcount = database_select_as_array($sql);
					my $getcount = $getcount[0];
											    
					if ($getcount eq 0)
					{
												
						$sql	=  "insert into sms_call_refund (service_id,call_id,refund_request_time,refund_status) values ('$service_id','$call_id',now(),'Pending')";
						database_do($sql);
						
					}
					
					$returnval = &Message("REFUND_INFO");
			}else{
				    #if no call details found
												
					$returnval = &Message("CALL_NOT_FOUND_INFO");
			}
    }else{
												
		$returnval = &Message("MUTE_STATUS_INFO");
    }
												
}

#============================================
# get Invitation request
#============================================
 
sub getsigninRequest{
												
	    my ($ani)=@_;
												
	    my $sql="select 1,1,id,date_start,ani,dst,name from service_signin where ani=$ani and service_id is null and pin is null order by id desc limit 1";
	    my %hashval = &database_select_as_hash($sql,"1,id,date_start,ani,dst,name");
												
	    return %hashval;
}

#============================================
# calculating time difference
#============================================
 
sub get_time_difference(){
												
	    my ($date_time)=@_;
	    my ($year1,$mon1,$mday1,$hour1,$min1,$sec1) = split(/[\s\-:]+/, $date_time);
	    my ($sec2,$min2,$hour2,$mday2,$mon2,$year2,$wday2,$yday2,$isdst2) = localtime(time);
												
	    $year2=1900+$year2;
	    $mon2=$mon2+1;
												
		my ($days, $hours, $minutes, $seconds) = Delta_DHMS( $year1, $mon1, $mday1, $hour1, $min1, $sec1,  # earlier
                                           $year2, $mon2, $mday2, $hour2, $min2, $sec2); # later
												
		return ($days);
}

#============================================
# Refer a Friend to Zenofon
#============================================

sub referFriend()
{
    my ($fromnumber,$smsbodytext,$referrer_name,$service_id)=@_;
    my $session_value 	=  &getSessionObj;
    my $returnval       =  "";
    my $friend_name     =  "";
    my $friend_number	=  "";	
    my $error	        =  0;
    my $session         =  "";
												
    #split message and get friend name and number.	 
												
    if((lc(&trim($smsbodytext))) eq "refer" || &trim($smsbodytext) eq 5){
												
		$returnval = &Message("REFER_FRIEND_INFO");
		$session_value->clear(["error_refer"]);
		return $returnval,0;
    }
												
    if(((lc(&trim($smsbodytext))) =~ m/^(refer)+((\,?)(\s?))+((\w[a-zA-z]+)(\s?))+\,+((\s?)(\+?)(\d+)[(\d)(\s)(\-)]*)$/) || ((lc(&trim($smsbodytext))) =~ m/^((\w[a-zA-z]+)(\s?))+\,+((\s?)(\+?)(\d+)[(\d)(\s)(\-)]*)$/)){
												
		$smsbodytext  =  (lc(&trim($smsbodytext)));
		$smsbodytext  =~ s/refer(\s?)(\,?)//i;
												
		my @referInfo   =  split(/,/,(substr($smsbodytext,0)));
		$friend_name    =  ucfirst(&trim($referInfo[0]));
		$friend_number  =  &trim($referInfo[1]);
		$friend_number  =~ s/\-//g;
		$friend_number  =~ s/\s//g;
		$friend_number 	=~ s/\+//g;
												
		(my $number_status,my $number_format,$friend_number) = &multiformat_phone_number_check_user_input($friend_number);
    }
												
    #if input is in wrong format or contain keyword refer only 
												
    if(!$friend_name || !$friend_number){
												
		my $value  =  $session_value->param("error_refer");
		$value     =  $value + 1;
		$session_value->param("error_refer",$value);
		if ($value eq 5){
												
			    $returnval 	=  &Message("REFER_CUSTOM_SUP");
			    $session_value->clear(["error_refer"]);
			    $session    =  1;
			    $error      =  0;
		}else {
												
			    $returnval 	=  &Message("INVALID_REFER_FORMAT");
			    $session    =  0;
			    $error      =  1;
		}
												
		return $returnval,$error,$session;
		exit;
    }         
    my $datetime=&getDatetime();
												
    #checking Friend Number is already zenofon member	
												
    my @alreadymember=&isZenofonUser($friend_number,$smsbodytext);
												
    if($alreadymember[0] eq 0){
		    #if friend number is not a zenofon member
		    #check number format
												
		    ( my $tmp0,$friend_number, my $tmp2) = &multilevel_check_E164_number(&clean_int($friend_number));
			if ($tmp0 eq "OK") {	  
												
				    #checking number is a mobile number
				    my $ani_provider_is_mobile   =  1;
				    my %hash                     =  &get_carrier_by_number($friend_number);			
												
				    if ($hash{found} eq 1) {
												
						$ani_provider_is_mobile	= ($hash{carrier_is_mobile} eq 1) ? 1 : 0;		
				    }
											    
				    if ($ani_provider_is_mobile ne 1 ) {
												
					#if not a mobile number
						$returnval = &Message("NUMBER_FORMAT_ERROR_INFO");
						$error     = 1;
				    }else{
												
												
					#start invitation process
					my $sql = " 
								  insert into service_signin  
								  (date_start,  date_last_change,  ani, dst,name)values 
								  (now(),       now(),             '$friend_number', '$fromnumber','$friend_name' ) 
								   ";
												
					my $signin_id = database_do_insert($sql);
												
					if($signin_id eq ""){
												
							    #error message to user
							    $returnval=&Message("SYSTEM_ERROR_INFO");
												
					}else{
												
							    #respond to REFERRER
							    my $message =  &Message("REFER_RESP_INFO");
							    $message 	=~ s/xxxx/$friend_name/i;
							    $returnval 	=  $message;
												
							    #invitation to friend number
												
							    my $length_f_name   =  length($friend_name);
							    my $length_r_name   =  length($referrer_name);
							    my $name_length     =  $length_f_name+$length_r_name;
													
							if($name_length gt 26){
													
								$friend_name   = ($length_f_name gt 13)?substr($friend_name,0,13):$friend_name;
								$referrer_name = ($length_r_name gt 13)?substr($referrer_name,0,13):$referrer_name;
							}
													
							my $returnval_to_friend = &Message("REFER_INVITATION_MSG");#"Hi $friend_name, Your friend $referrer_name wants to give you \$2 to try Zenofon! Simply reply 'yes' to join.";
							$returnval_to_friend    =~ s/xxxx/$friend_name/i;
							$returnval_to_friend    =~ s/xxxxx/$referrer_name/i;
													
							&sms_log($friend_number,$returnval_to_friend,"referFriend",'Sent');						
							&sendSMS_Twilio($friend_number,$returnval_to_friend);
							&action_history("status:refer:request",('signin_id'=>$signin_id,'value_old'=>$friend_number,'value_new'=>''));
							#send invitation
					}
				    }
													
			}else{
													
				#number not in E164 format
				$returnval =  &Message("REFER_NUMBER_ERROR");
				$error	   =  1;
			}
    }else{	
													
			#already a zenofon member	  
			my $message  =  &Message("REFER_DUP_INFO");
			$returnval   =  $message;
			$error	     =  1;
    }
													
    return $returnval,$error;
}

#============================================
# Add referred friend as Zenofon User
#============================================
  
sub addFriend()
{
    my %t;
    my %hash;
    ($t{invite_service_id},$t{ani},$t{dst},$t{signin_id},$t{name})=@_;
    $t{dst_orginal}     =  $t{dst};
    $t{invite_ok}       =  0;
    $t{form_error}      =  0;
    my $sql             =  '';
    my $return_message	=  '';
											
    if($t{invite_service_id})
    {
		$sql = "
		select 
			1,1,				
			service.name,
			service_status.refer_status,
			service_status.refer_status_premium,
			service_status.signin_coupon_premium_id,
			service_status.signin_coupon_default_id
		from
			service_invite,
			service,
			service_status
		where
			service_invite.free = 0 and 
			service_invite.service_id = service.id and 
			service.status = service_status.id and 
			service_status.deleted = 0 and 
			service_status.can_add_refer = 1 and 
			service.id = '$t{invite_service_id}'
		";
											
	%hash = database_select_as_hash($sql,"flag,name,signin_status,signin_status_premium,signin_coupon_premium_id,signin_coupon_default_id");
											
	if ($hash{1}{flag} eq 1) {
											
		    $t{invite_ok}                       = 1;
		    $t{invite_service_name}             = $hash{1}{name};
		    $t{invite_signin_status}            = $hash{1}{signin_status};
		    $t{invite_signin_status_default}    = $hash{1}{signin_status};
		    $t{invite_signin_status_premium}    = $hash{1}{signin_status_premium};
		    $t{invite_signin_coupon_premium_id}	= $hash{1}{signin_coupon_premium_id};
		    $t{invite_signin_coupon_default_id}	= $hash{1}{signin_coupon_default_id};
	}
											
    }
    
#============================================
# get default coupon
#============================================
    my %coupon = ();
    $t{coupon_default_exists}	        = 0;
    $t{coupon_default_in_stock}	        = 0;
    $t{coupon_default_stock_qtd}        = 0;
    $t{coupon_default_ani_locked}       = 0;
    $t{coupon_default_error}	        = 0;
												
    if ( ($t{invite_ok} eq 1) && ($t{invite_signin_coupon_default_id} ne "") && ($t{invite_signin_coupon_default_id} > 0) ) {
											
	$sql = "
		select 
			1,1,
			service_coupon_type.id,
			service_coupon_type.title
		from 
			service_coupon_type,service_coupon_type_status
		where 
			service_coupon_type.id = '$t{invite_signin_coupon_default_id}' and 
			service_coupon_type.status = service_coupon_type_status.id and 
			service_coupon_type_status.is_active = 1
		";
											
	%hash = database_select_as_hash($sql,"flag,id,title");
											
	if ($hash{1}{flag} eq 1) {
											
		    $t{coupon_default_exists}           = 1;
		    $t{coupon_default_type_id}          = $hash{1}{id};
		    $t{coupon_default_title}            = $hash{1}{title};
											
		    $sql = "
											
			    select 1,1,count(*)
			    from 
				    service_coupon_stock,
				    service_coupon_stock_status
			    where 
				    service_coupon_stock.coupon_type_id='$t{coupon_default_type_id}' and 
				    service_coupon_stock.status = service_coupon_stock_status.id and 
				    service_coupon_stock_status.is_ready_to_assign
			    ";
											
	    %hash = database_select_as_hash($sql,"flag,value");
	    if ($hash{1}{flag} eq 1) {
											
				$t{coupon_default_in_stock}     = ($hash{1}{value}>0) ? 1 : 0;
			    	$t{coupon_default_stock_qtd}    = $hash{1}{value};
	    }
	}
    }

#============================================
# get premium coupon
#============================================
    %coupon = ();
    $t{coupon_premium_exists}           = 0;
    $t{coupon_premium_in_stock}	        = 0;
    $t{coupon_premium_stock_qtd}        = 0;
    $t{coupon_premium_ani_locked}       = 0;
    $t{coupon_premium_error}            = 0;
    if ( ($t{invite_ok} eq 1) && ($t{invite_signin_coupon_premium_id} ne "") && ($t{invite_signin_coupon_premium_id} > 0) ) {
												
	$sql = "
		select 
			1,1,
			service_coupon_type.id,
			service_coupon_type.title
		from 
		    	service_coupon_type,service_coupon_type_status
		where 
			service_coupon_type.id = '$t{invite_signin_coupon_premium_id}' and 
			service_coupon_type.status = service_coupon_type_status.id and 
			service_coupon_type_status.is_active = 1
		";
												
	%hash = database_select_as_hash($sql,"flag,id,title");
												
	if ($hash{1}{flag} eq 1) {
												
			    $t{coupon_premium_exists}           = 1;
			    $t{coupon_premium_type_id}	        = $hash{1}{id};
			    $t{coupon_premium_title}            = $hash{1}{title};
			    $sql = "
				    select 1,1,count(*)
				    from 
					    service_coupon_stock,
					    service_coupon_stock_status
				    where 
					    service_coupon_stock.coupon_type_id='$t{coupon_premium_type_id}' and 
					    service_coupon_stock.status = service_coupon_stock_status.id and 
					    service_coupon_stock_status.is_ready_to_assign
				    ";
												
	    %hash = database_select_as_hash($sql,"flag,value");
												
	    if ($hash{1}{flag} eq 1) {
												
			$t{coupon_premium_in_stock}     = ($hash{1}{value}>0) ? 1 : 0;
			$t{coupon_premium_stock_qtd}    = $hash{1}{value};
												
	    }
	}
    }
#============================================
# pega rate table a ser usada como route 1 do status que supostamente devera ser atribuido com esse convite
# it catches rate table it to be used like route 1 of the status that supposedly should be attributed with that invitation
#============================================
    $t{rate_table_for_ani}  =  9;
    $t{rate_table_for_dst}  =  10;
												
    if ( ($t{invite_ok} eq 1) && ($t{invite_signin_status} ne "") && ($t{invite_signin_status} > 0) ) {
												
	$sql = "select  1,1,rate_slot_1,rate_slot_callback from service_status where id = '$t{invite_signin_status}' ";
												
	%hash = database_select_as_hash($sql,"flag,value1,value2");
												
	if ($hash{1}{flag} eq 1) {
												
		    $t{rate_table_for_ani} = $hash{1}{value2};
		    $t{rate_table_for_dst} = $hash{1}{value1};
	}
    }
#============================================
# Check ANI
#============================================
    $t{ani_ok} 	                = 0;
    $t{ani_error}               = 0;
    $t{ani_error_format}        = 0;
    $t{ani_error_no_rate}       = 0;	
												
    if ($t{ani} ne "") {
        # check format 
												
	my ($tmp0,$tmp1,$tmp2)  = &multilevel_check_E164_number(&clean_int($t{ani}));
	if ($tmp0 eq "OK") {
												
			$t{ani}               =  $tmp1;
	} else {
									
			$t{form_error}        =  1;
			$t{ani_error} 	      =  1;
			$t{ani_error_format}  =  1;
	}
	# check rate
	if ($t{ani_error} eq 0) {
					
		    %hash = &multilevel_rate_table_get($t{ani},$t{rate_table_for_ani});
		    if ($hash{ok_to_use} ne 1) {
					
			        $t{form_error}          = 1;
			        $t{ani_error}           = 1;
			        $t{ani_error_no_rate}   = 1;
		    }
	}	
	if ($t{ani_error} eq 0) {
				
		    $t{ani_ok} 	  =  1;
		    $t{ani_E164}  =  $t{ani};
		    $t{ani}       =  &format_E164_number($t{ani},"USA");
	}
    }
#============================================
# Get provider by ani
#============================================
    $t{ani_provider_found} = 0;
				
    if ( ($t{ani_ok} eq 1) && ($t{ani_E164} ne "") ) {
				
	    %hash = &get_carrier_by_number($t{ani_E164});
		if ($hash{found} eq 1) {
							
                $t{ani_provider_found}                  = 1;
				$t{ani_provider_id}                     = $hash{carrier_id};
				$t{ani_provider_name}                   = $hash{carrier_name};
				$t{ani_provider_is_mobile}              = ($hash{carrier_is_mobile} eq 1) ? 1 : 0;
				$t{ani_provider_is_premium}             = ($hash{flag_premium_signin} eq 1) ? 1 : 0;
				$t{"ani_provider_type_".$hash{type}}    = 1;
		}
    }
#============================================
# choose premium/default signin_status
#============================================
    $t{invite_signin_status} = $t{invite_signin_status_default};
    if (defined($t{ani_provider_is_premium}) && ($t{ani_provider_is_premium} eq 1) && ($t{invite_signin_status_premium} ne "") ) {
									
		 $t{invite_signin_status} = $t{invite_signin_status_premium};
    }

#============================================
# choose premium/default cooupon
#============================================
    $t{coupon_error}            =  0;
    $t{coupon_exists}           =  $t{coupon_default_exists};
    $t{coupon_type_id}          =  $t{coupon_default_type_id};
    $t{coupon_title}            =  $t{coupon_default_title};
    $t{coupon_in_stock}	        =  $t{coupon_default_in_stock};
    $t{coupon_stock_qtd}        =  $t{coupon_default_stock_qtd};
    $t{coupon_is_premium}       =  0;
									
    if ( defined($t{ani_provider_is_premium}) && ($t{coupon_premium_in_stock} eq 1) && ($t{ani_provider_is_premium} eq 1) ) {
									
			$t{coupon_exists}               =  $t{coupon_premium_exists};
			$t{coupon_type_id}              =  $t{coupon_premium_type_id};
			$t{coupon_title}                =  $t{coupon_premium_title};
			$t{coupon_in_stock}             =  $t{coupon_premium_in_stock};
			$t{coupon_stock_qtd}            =  $t{coupon_premium_stock_qtd};
			$t{coupon_is_premium}           =  1;
    }
#============================================
# re-check coupon: one coupon per ANI
#============================================
    # new logic limitation
    if ( ($t{ani_ok} eq 1) && ($t{coupon_in_stock} eq 1)  ) {
									
		%hash = database_select_as_hash("select 1,1,count(*) from service_signin where ani='$t{ani_E164}' and service_id is not null ","flag,qtd");
		unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ) {
									
			    $t{form_error}              =  1;
			    $t{coupon_error}            =  1;
			    $t{coupon_error_ani_locked}	=  1;
		}
    }
#============================================
# Check DST
#============================================
    $t{dst_ok} 	                =  0;
    $t{dst_error}               =  0;    
    $t{dst_error_no_rate}       =  0;
    if ($t{dst} ne "") {
									
		%hash = &multilevel_rate_table_get($t{dst},$t{rate_table_for_dst});
		if ($hash{ok_to_use} ne 1) {
									
			    $t{form_error}              =  1;
			    $t{dst_error}               =  1;
			    $t{dst_error_no_rate}       =  1;
		}
	
	# Se dst ta ok flag ele
	if ($t{dst_error} eq 0) {
									
			    $t{dst_ok} 	        =  1;
			    $t{dst_E164}        =  $t{dst};
			    $t{dst}             =  &format_E164_number($t{dst},"USA");
	}
    }
#============================================
# re-check coupon: no coupon if multiple DST
#============================================
    if ( ($t{dst_ok} eq 1) && ($t{coupon_in_stock} eq 1)  ) {
									
		$sql = "
		SELECT 1,1,count(*) FROM calls 
		where dst='$t{dst_E164}' and date>date_sub(now(), interval 90 day) and value>0 
		";
									
		%hash = database_select_as_hash($sql,"flag,qtd");
		unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} < 30) ) {
					
			    $t{form_error}              =  1;
			    $t{coupon_error}            =  1;
			    $t{coupon_error_dst_locked}	=  1;
		}
    }
	
#===================================================
# User sign-in - START
#===================================================
    if(($t{ani_ok} eq 1)&& ($t{dst_ok} eq 1) && $t{form_error} eq 0){
					
	# Generating signin pin number
	$t{signin_pin} = &multilevel_pin_generate();
					
	if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
	if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
	if ($t{signin_pin} eq "")  {	
						
		    # error in generating pin
					
			$t{form_error}          =  1;
			$t{form_error_system}   =  1;
	}else{		
	    
			&database_do("update service_signin set pin='$t{signin_pin}' where id='$t{signin_id}' ");
			&action_history("status:signin:new",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=>$t{signin_pin}));
			&database_do("update service_pin set signin_id='$t{signin_id}' where pin='$t{signin_pin}' ");
				
			$sql  = "
				insert into service 
				(product_id,  status,                       name,           creation_date,  last_change  ) values 
				('1',         '$t{invite_signin_status}',   '$t{name}',     now(),          now()        ) 
			";
				
			$t{service_id} 	       = &database_do_insert($sql);
			if ($t{service_id} ne "") {
					
				# add on tree
				$sql  = " 
				insert into service_tree 
				(service_id,        parent_service_id        )  values 
				('$t{service_id}',  '$t{invite_service_id}'  ) 
				";
				database_do($sql);
				&data_set("service_data",$t{invite_service_id},"last_friend_time",time);
				
				# update pin
					
					&database_do("update service_pin set service_id='$t{service_id}' where pin='$t{signin_pin}' ");
					
				# update signin
					
					&database_do("update service_signin set service_id='$t{service_id}' where id='$t{signin_id}' ");
					
				# update action_log 
					
					&database_do("update action_log set service_id='$t{service_id}' where signin_id='$t{signin_id}' and service_id is null ");
					
				# criar invite
					
					my $tmp  = &multilevel_invite_create($t{service_id});
					
				# adicionar primeiro ANI
						
					&data_set("service_data",$t{service_id},"ani_1_number",$t{ani_E164});
					&data_set("service_data",$t{service_id},"ani_1_provider",'');
					&multilevel_anicheck_touch($t{service_id},$t{dst_E164});
					&database_do("insert into service_ani (ani,service_id) values ('$t{ani_E164}', '$t{service_id}') ");
							
				# adicionar primeiro DST
						
					&data_set("service_data",$t{service_id},"dst_1_number",$t{dst_E164});
					&data_set("service_data",$t{service_id},"dst_1_rslot",1);
							
				# adicionar defaults
							
					&data_set("service_data",$t{service_id},"trigger_nf",1);
					&data_set("service_data",$t{service_id},"trigger_nfof",1);
					&data_set("service_data",$t{service_id},"trigger_nc",1);
					&data_set("service_data",$t{service_id},"trigger_ec",1);
					&data_set("service_data",$t{service_id},"trigger_lb",1);
					&data_set("service_data",$t{service_id},"email_news",1);
				# adicionar coupon se possivel
								
					if ( ($t{coupon_type_id} ne "") && ($t{coupon_in_stock} eq 1) && ($t{coupon_exists} eq 1) && ($t{coupon_error} ne 1) ) {
								
					    # tenta add coupon
									
						%coupon                 =  ();
						$coupon{service_id}     =  $t{service_id};
						$coupon{coupon_type_id}	=  $t{coupon_type_id};
						%coupon                 =  &multilevel_coupon_assign(%coupon);
						if ($coupon{ok} eq 1) {
										
								if (&multilevel_coupon_next_slice($coupon{coupon_stock_id})>0){
											
										    $t{coupon_assigned}	= 1;
								}
						}	
					}
							
				# delete request code
				&database_do("update service_signin set date_last_change=now(), date_stop=now() where id='$t{signin_id}' ");
						
				# apply commission
				my %commission_data                        =  ();
				$commission_data{service_id}               =  $t{invite_service_id};
				$commission_data{from_service_id}          =  $t{service_id};
				$commission_data{commission_type_engine}   =  "REFERRAL_SIGNIN";
				%commission_data = &multilevel_commission_new(%commission_data);
					
				# email parent tree sobre new friend
				my $notification_service_id = $t{invite_service_id};
				foreach my $notification_proximity_level (0..20) {
								
					    my %tmp_hash = database_select_as_hash("select 1,1,name,email from service where service.id='$notification_service_id' ","flag,name,email");
											
						    if ($tmp_hash{1}{flag} eq 1) {
										
								my $notification_service_email	=  $tmp_hash{1}{email};
								my $notification_flag_type      =  ($notification_proximity_level eq 0) ? "trigger_nf" : "trigger_nfof";
								my $notification_flag 	        =  &data_get("service_data",$notification_service_id,$notification_flag_type);
										
								if ( ($notification_flag eq 1) && ($notification_service_email ne "") ){
												
									    my %email 	                        = ();
									    $email{template}                    = ($notification_proximity_level eq 0) ? "alert.new.friend" : "alert.new.friend.of.friend";
									    $email{to}	                        = $notification_service_email;
									    $email{dic}{invite_branch_distance}	= "you";
									    $email{dic}{invite_branch_distance}	= ($notification_proximity_level eq 1) ? "your friend" : $email{dic}{invite_branch_distance};
									    $email{dic}{invite_branch_distance}	= ($notification_proximity_level eq 2) ? "one person away" : $email{dic}{invite_branch_distance};
									    $email{dic}{invite_branch_distance}	= ($notification_proximity_level > 2) ? ($notification_proximity_level-1)." people away" : $email{dic}{invite_branch_distance};
									    &multilevel_send_email(%email);
								}
						    }
							
					    %tmp_hash = database_select_as_hash("select 1,1,parent_service_id from service_tree where service_id='$notification_service_id'","flag,value");
									
					if ( ($tmp_hash{1}{flag} eq 1) && ($tmp_hash{1}{value} ne "") ) {
									
							$notification_service_id = $tmp_hash{1}{value};
									
					} else {
							last;
					}
				}
										
				my $message      =  &Message("WELCOME_USER_MSG");		                 
				$return_message  =  $message;
										
				#confirmation message to referred person
										
				my @user_info 	=  &isZenofonUser($t{dst_orginal});
				my @status      =  &MuteUnmute_status($t{dst_orginal});
				my $StatusValue =  $status[0];
										
				#chack user and message status is unmute
										
				if($user_info[0] eq 1 && $StatusValue eq 1) {										
					    
										
					    my $joinmessage     =  &Message("REFER_PROMOTION_MSG");
					    $joinmessage        =~ s/xxxx/$t{ani}/i;
					    &sms_log($t{dst_orginal},$joinmessage,"addFriend",'Sent');
					    &sendSMS_Twilio($t{dst_orginal},$joinmessage);
				}
						
			}else {
							
				$t{form_error}	        =  1;	
				$t{form_error_system}   =  1;
			}
		}
    }
    
#============================================
# Setting Error Status
#============================================
    if($t{form_error} eq 1){
							
		if($t{ani_error_format} eq 1) {
							
			    $return_message=&Message("NOT_VALID_NUM_INFO");
				
		}elsif($t{ani_error_no_rate} eq 1 || $t{dst_error_no_rate} eq 1 || (($t{coupon_error} eq 1) && ($t{coupon_in_stock} eq 1) && $t{coupon_error_dst_locked} eq 0)){
							
			    $return_message = &Message("NOT_ALLOW_NUM_INFO");
							
		}else{
								
			    $return_message= &Message("SYSTEM_ERROR_INFO");
		}
    }
							
    return $return_message;
							
}
  
#=======================sub get_carrier_by_number()===========================
# For getting carrier information for phone number 
#=============================================================================
# moved to default.include.pl - Parth

#=====================sub do_ani()====================
# Add new sub number for zenofon user acccount
#=====================================================   
sub do_ani()
{
	
	my ($fromnumber,$smsbodytext) = @_;
	my @isValidUserArray1   =  &isZenofonUser(&trim($fromnumber),$smsbodytext); # return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
	my $isValidUser1        =  $isValidUserArray1[0];
	my $service_id          =  $isValidUserArray1[2];
    my $returnval           =  '';
	my $index               =  "";
	my $loop                =  "";
	my $ok                  =  "";
	my $number              =  "";
	my $name                =  "";
	my $callid              =  "";
	my $carrier             =  "";
	my $sql	                =  "";
	my $session             =  "";
	my $error               =  "";
	my @smsbody             =  split(/\s/,$smsbodytext);
	$number                 =  $smsbody[1];
	$number                 =  &trim($number);
	
	if($smsbodytext eq "add ani"){
	
				$returnval =  &Message("ADD_ANI_INFO");;
				$session   =  1;
				$error     =  0;
		
	}
	elsif ((lc(&trim($smsbodytext))) =~ m/^(add)+\s+(\d+)$/)
	{
		
		# check and format number

		    my ($flag,$number_e164,$country) = &multilevel_check_E164_number($number);
	 	 
		 	if ($flag eq "USANOAREACODE") 	  {$ok = 0;}
		 	elsif ($flag eq "UNKNOWNCOUNTRY") {$ok = 0;}
		 	elsif ($flag eq "OK") 		  {$number = $number_e164; $ok=1;}
		 	else {$ok = 0;}

		# if all ok, save

		if (($ok eq 1 ) && ($number =~ m/(\d{10,})/))
		{
			    foreach $loop (1..20)
					{
						if (&data_get("service_data",$service_id,"ani_".$loop."_number") eq "")
							{
							    $index = $loop;
							    last;
							}
					}
		
						#Get count value
					    $sql = "select count(*) from service_ani where ani = '$number' and service_id = '$service_id'";
			
						my @count = database_select_as_array($sql);
						my $count = $count[0];
		
		
				if ($count eq 0)
				{
					$sql = "select count(*) from service_ani where ani = '$number'";
                    my @getcount = database_select_as_array($sql);
					my $getcount = $getcount[0];
			
					if ($getcount eq 0)
					{
						#---------------------------------------------------			
						# save data
						#---------------------------------------------------
						&database_do("insert into service_ani (ani,service_id) values ('$number', '$service_id')");
						&data_set("service_data",$service_id,"ani_".$index."_name",$name);
						&data_set("service_data",$service_id,"ani_".$index."_callid",$callid);
						&data_set("service_data",$service_id,"ani_".$index."_number",$number);
						&data_set("service_data",$service_id,"ani_".$index."_carrier",$carrier);
							
						&multilevel_anicheck_touch($service_id,$number);
						
						my $message     =  &Message("ANI_RESP_INFO");
						$message        =~ s/xxxx/$number/i;
                        $message        =~ s/xxxxx/$number/i;
						$returnval      =  $message;
                        $session        =  1;
                        $error          =  0;
				
					}
					else
					{
				        
						my $message     =  &Message("EXISTS_ZENO_USER");
                        $message        =~ s/xxxx/$number/i;
						$returnval      =  $message;
                        $session        =  0;
                        $error          =  1;
					}
				}
				else
				{
					my $message     =  &Message("DUPLICATE_ANI_INFO");
					$message        =~ s/xxxx/$number/i;
					$returnval      =  $message;
					$session        =  0;
					$error 	        =  1;				
				}
		}
		else
		{
			
			$returnval  =  &Message("ADD_ANI_INVALID_FORMAT");
			$session    =  0;
			$error 	    =  1;
		}
	}
	else
	{
		$returnval  =  &Message("ADD_ANI_INVALID_FORMAT");
		$session    =  0;
		$error      =  1;
	}
	return $returnval,$session,$error;
}

#====================sub language_status()==================
# Language status update
#===========================================================
sub language_status()
{
    my ($fromnumber,$smsbody)   =  @_;
    my $lan_status              =  "";
    my $returnval               =  "";
		
    if (($smsbody eq "english") || ($smsbody eq "ingles")){
			
		$lan_status = 1;	
			
    }elsif (($smsbody eq "french") ||($smsbody eq "francais") || ($smsbody eq "frances")){
			
		$lan_status = 2;	
			
    }elsif (($smsbody eq "spanish") || ($smsbody eq "espaniol") || ($smsbody eq "espanol")){
			
		$lan_status = 3;	
    }

    my $sql     =  "select count(*) from SMS_Client where sms_ani = '$fromnumber'";
    my @count   =  database_select_as_array($sql);
    my $count   =  $count[0];
    if ($count gt 0){
				
	    	$sql = "update SMS_Client set language_status = '$lan_status' where sms_ani = '$fromnumber'";
			
		&database_do($sql);
		my $message  =  &Message("LANGUAGE_INFO");
		$returnval   =  $message;			
    }else    {
				
			$sql = "insert into SMS_Client (sms_ani,sms_status,language_status) values ($fromnumber,1,$lan_status)";
				
			&database_do($sql);
			my $message  =  &Message("LANGUAGE_INFO");
			$returnval   =  $message;
    }
    return $returnval;	
}

#=====================sub get_pin_number()====================
# This function process the pin related request from user.
#=====================================================

sub process_pin(){

    my ($service_id)= @_;
    my ($returnval,$pin,%hash,$sql,$pin_change);
    $pin_change=0;
    #SMS is PIN

    if (lc(&trim($Body)) eq "pin"){
					
		#retrieve pin number
		$sql="select 1,pin from service_pin where service_id='$service_id'";
			
		%hash          =  database_select_as_hash($sql,"flag,pin");
		$pin           =  $hash{1}{flag};
		$returnval     =  &Message("USER_PIN_INFO");#"Your PIN is $pin, to change the PIN type 'changepin'.";
		$returnval     =~ s/xxxx/$pin/i;
    }elsif(lc(&trim($Body)) eq 'changepin' || lc(&trim($Body)) eq 'change pin'){
			
	#SMS is changepin
	
	#clear error counter			
		&errorCounter(0);
		
		$returnval=&Message("CHANGE_PIN_MSG");#"Change PIN: Please enter last four digit of your credit card number.";
    }else{
				
		#SMS is credit card number
		
		my $error_status=0;
		
		if(&trim($Body) =~ m/^(\d{4})$/){
					
			    #set error variables.Defaultly all error is turned on
				
			    my $system_error            =  1;
			    my $no_cc_details_added     =  1;
			    my $invalid_cc_number       =  1;
				
			    #get user credit card number
				
			    $sql = "
				SELECT 1,1,cc_number
				FROM service_profile_cc
				where service_id='$service_id' and active=1";
			    %hash=database_select_as_hash($sql,"flag,cc_number");
					
			if(keys(%hash) > 0){
				
				#turn off no_cc_added error
					
					$no_cc_details_added=0;
					
				#get last 4 digit of cc number
						
					my $cc_number=substr($hash{1}{cc_number},(length($hash{1}{cc_number})-4));				
						
				#check cc number with user entered cc number
						
					if($cc_number eq &trim($Body)){
								
						    #turn off invalid_cc_number error
						    $invalid_cc_number=0;
							
						    #generating pin number
								
						    my @chars=('0'..'9');	
						    foreach my $loop_count (1..8) {
											
								my $tmp_pin = "";
								foreach (1..8) {$tmp_pin .= $chars[rand @chars];}
															
									my @lookalike = ($tmp_pin);
									my $tmp= join("','",@lookalike);
											
									$sql = "
									SELECT 1,1,count(*) 
									FROM service_pin 
									where  pin ='$tmp_pin'
									";
										
								%hash = &database_select_as_hash($sql,"flag,qtd");
										
								if ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ){
										
										$pin = $tmp_pin;
										last;
								}
						   }
							
						if($pin ne ""){
									
						        #updating pin number						
						        $sql="update service_pin set pin='$pin',last_change=now() where service_id='$service_id'";
								
						        &database_do($sql);
								
						        $returnval=&Message("NEW_PIN_INFO");#$returnval="Your Pin Number has been Changed Successfully. Your New Pin Number is $pin.";
						        $returnval =~ s/xxxx/$pin/i;
								
						        #turn off system error
							    $system_error=0;
								
								#Set pin change status
								$pin_change=1;		
						}	
					}
			}		
				
				#check error turned on and set return error message
					
				if($no_cc_details_added eq 1){
								
						$error_status  =  1;
						$returnval     =  &Message("CC_NOT_FOUND");
						
				}elsif($invalid_cc_number eq 1){
								
						$error_status  =  1;
						$returnval     =  &Message("CC_INVALID_MSG");
						
				}elsif($system_error eq 1){
								
						$error_status  =  1;
						$returnval     =  &Message("SYSTEM_ERROR_INFO");
						
				}	
								
		}else{			
								
			$error_status=1;
							
			#if user enter credit card length != 4
				
			$returnval=&Message("CC_FORMAT_ERROR");#$returnval="Error: To change PIN please enter last four digit of your credit card number.";
		}
			
		#get error counter value for error message
		
		my @getcounter = &errorCounter($error_status);
		
		#if error counter greater than 3 send notification to user as well as customer care
		
		if($getcounter[0] gt 3){			
					
			    #get email address of zenofon user
					
			    my %tmp_hash = database_select_as_hash("select 1,1,name,email from service where service.id='$service_id' and email is not null","flag,name,email");
			    if(keys(%tmp_hash) > 0){				
						    
				#Report cc authetication failed message to user email
					
						my %email               =  ();
						$email{'to'}            =  $tmp_hash{1}{email};
						$email{'from'}          =  "support\@zenofon.com";
						$email{template}        =  "failed.credit.user";
						$email{dic}{first_name} =  ($tmp_hash{1}{name} eq "")?'Customer':$tmp_hash{1}{name};					
						&multilevel_send_email(%email);
			    }
					
			    #Report cc authetication failed message to support zenofon email
					
				my %email               =  ();
				$email{'to'}            =  "ccalert\@zenofon.com";
				$email{'from'}          =  "support\@zenofon.com";
				$email{template}        =  "failed.credit.support";
				$email{dic}{service_id} =  $service_id;
				$email{dic}{name}       =  $tmp_hash{1}{name};
				$email{dic}{phone}      =  $From;
				$email{dic}{user_mail}  =  $tmp_hash{1}{email};					
				&multilevel_send_email(%email);
					
			#clear error counter
			&errorCounter(0);
					
			# alert to authentication failed sms to user via mobile
			$returnval   =  &Message("CC_AUTHENTICATION_FAILED");#$returnval="You are failed to authenticate credit card number. Please contact customer care at 917-284-9450 for help.";
			$pin_change  =  -1;
		}			
    }	
    return ($returnval,$pin_change);
}
#=====================sub help()====================
# This function process help command.
#=====================================================

sub help(){
		
    my $returnval;
    my $message;
				
    #split sms to get the digit part if it included in sms content.	
				
    my @split_sms=&trim(split(/\t/,(substr($Body,4))));
	
    if($split_sms[0] gt 1){
				
			$message=&Message("HELP_$split_sms[0]_MSG");
    }
    if($message eq ""){
			
			$message=&Message("HELP_MSG_INFO");
    }
				
    return $message;
}

#========================sub forward_number()========================
# Adding a new Forward number for existsing user
#====================================================================

sub addnew_forward_number()
{
    my ($fromnumber,$smsbody,$service_id) = @_;
    my $sql                             =  "";
    my $activenumber                    =  "";
    my $number 	                        =  "";
    my $returnval                       =  "";
    my $ok                              =  "";
    my $index                           =  "";
    my $duplicateindex 	                =  "";
    my $flag                            =  "";
    my $dst                             =  "";
    my $getname                         =  "";
    my $finalval                        =  "";
    my $dial_number                     =  "";
    my $name                            =  "";
    my $count                           =  "";
    my $size                            =  "";
    my $tmy_url                         =  'servicetwilio.cgi';
    my $terror                          =  0;
    my $terror_number_format            =  0;
    my $terror_number_e164_format      	=  0;
    my $terror_number_skype_format     	=  0;
    my $terror_number_no_rate         	=  0;
    my $terror_number_unknown_country  	=  0;
    my $terror_no_more_index           	=  0;
    my $terror_bad_index              	=  0;
    my $tnumber                         =  "";
    my $tname                           =  "";
    my $session                         =  "1";
#--------------------------------------------------  
# user reply with dialnumber to find user contact 
#--------------------------------------------------
    
 if ($smsbody =~ m/^(\d+)/){
				
	        my @activenumber     = ("(646)434-4612","(646)434-4613","(646)434-4614","(646)434-4615","(646)434-4616","(646)434-4617","(646)434-4618","(646)434-4619","(646)434-4620","(646)434-4621","(646)434-4622","(646)434-4623","(646)434-4624","(646)434-4625","(646)434-4626","(646)434-4627","(646)434-4628","(646)434-4629","(646)434-4630","(646)434-4631","(917)284-9432","(646)873-6314","(646)873-6324","(646)873-6341","(646)873-6342","(646)873-6374","(646)873-6394","(646)873-6913","(646)873-6914","(646)873-6927","(646)873-6928","(646)873-6929","(646)873-6934","(201)204-1821","(201)204-1822","(201)204-1823","(201)204-1824","(201)204-1825","(201)204-1826","(201)204-1827","(201)204-1828","(201)204-1829","(201)204-1830","(201)204-1831","(201)204-1832","(201)204-1833","(201)204-1834","(201)204-1835","(201)204-1836","(201)204-1838","(201)204-1839","(201)204-1840","(201)204-1841",);
	        $size = @activenumber;
		for ( my $i=0; $i<$size; $i++){
				
			    my $a = $activenumber[$i];
			    if($smsbody =~ m/^(\((\d{0,3})\)(\d{0,3})(\-)(\d{0,4}))/){
					    
					if($a eq $smsbody)	   {
						
						$duplicateindex = $i+1;
						$flag           = 1;
					}
			    }else{
						
					$a =~ s/[^0-9]*//g;
					if($a eq $smsbody){
						
						$duplicateindex = $i+1;
						$flag           = 1;
					}
			    }
		}
			
		if($flag eq 1){
				
			    $index        =  $duplicateindex;
			    $dial_number  =  $activenumber[$index];
			    $dial_number  =~ s/[^0-9]*//g;
			    $count        =  1;
		}
   	
		if ($index eq ""){
				
			   
			    $returnval =&Message("WRONG_DIAL_NUMBER");
			    $session = 0;
		}else	{
					
			    my $_name 	=  &data_get("service_data",$service_id,"dst_".$index."_name");
			    my $_number =  &data_get("service_data",$service_id,"dst_".$index."_number");
			    my $_rslot 	=  &data_get("service_data",$service_id,"dst_".$index."_rslot");
				
			    if($_number eq ""){
						
					$returnval =&Message("CONTACT_NOT_FOUND_MSG");
					$returnval =~ s/xxxx/$smsbody/i;
					return $returnval,0;
			    }
				
			    my $last_info       =  &get_sms_session();
			    my @session_info    =  split(/\,/, $last_info);
			    my $fwd_number      =  $session_info[1];

				# try to save

			    # check and format number
					
			    my ($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($fwd_number);
			    my $tnumber_status             = $number_status;
			    my $tnumber_raw                = $number;
				
			    my $tnumber_clean              = $number_clean;
			    my $tnumber_format             = $number_format;
				
	            my $tnumber_format_skype       = ($number_format eq "SKYPE") ? 1 : 0;				
	            my $tnumber_format_sip         = ($number_format eq "SIP") ? 1 : 0;
				
			    if ($number_status ne "OK"){
						
					$ok     = 0;
					$terror = 1;
					if ($number_format eq "SKYPE")    {
							
						    $terror_number_skype_format = 1;
					}elsif ($number_format eq "SIP")	    {
							
						if ($number_status eq "UNKNOWNCOUNTRY")    {
							
							$terror_number_unknown_country = 1;
						}else{
							
							$terror_number_e164_format = 1;
						}
					}else {
						
						$terror_number_format = 1;
					}
			    } else {
						
					$fwd_number =  $number_clean;
					$ok         =  1;
			    }

				# if all ok, lets save data

			if ($ok eq 1){
						
				$sql 	   =  "select count(*) from service_data where target ='$service_id' and value ='$fwd_number' and name like 'dst%'";
				my @count  =  database_select_as_array($sql);
				$count 	   =  $count[0];
						
				if ($count eq 0){
							
					$sql 	  =  "select count(*) from service_data where target ='$service_id' and name ='dst_".$index."_forward'";
					my @count =  database_select_as_array($sql);
					$count 	  =  $count[0];	
								
						if ($count eq 0)	{
										
							&data_set("service_data",$service_id,"dst_".$index."_forward" ,$fwd_number);							
							$flag = 1;
						}else{
										
							$sql = "update service_data set value ='$fwd_number' where target ='$service_id' and name ='dst_".$index."_forward'";
							&database_do($sql);
							$flag = 1;
						}
							
					        if ($flag eq 1){
						   
						        $returnval =  &Message("FORWARD_RESP_INFO");
						        $returnval =~ s/xxxx/$fwd_number/i;
						        $returnval =~ s/xxxxx/$_name/i;
						        $returnval =~ s/xxxxxx/$fwd_number/i;
						        $returnval =~ s/xxxxxxx/$_name/i;
					        }
				}else{
							
					
					$returnval =  &Message("EXISTS_FORWARD_NUMBER");
					$returnval =~ s/xxxx/$fwd_number/i;
				}
			}
		}
	
	}else{
		#----------------------------------------------------------
		# forward name,number  (or) forward dstnumber, fwdnumber
		#----------------------------------------------------------
		
		my @user_info 	        = "";
		my $sms_details         = "";
		my $forward_number      = "";
		my @user                = "";
		my $user_name           = "";
		if ($smsbody =~ m/^(forward)+\s+((\w[a-zA-Z]+)(\s?))+\,+(\s?)+(\d+)$/)	{
								
			    my $len             =  length($smsbody);
			    $sms_details        =  substr($smsbody ,8,$len);
			    $sms_details        =  &trim($sms_details);
			    @user               =  split(/\,/,$sms_details);
			    $user_name 	        =  $user[0];
			    $user_name 	        =  &trim($user_name);
			    $forward_number     =  $user[1];
			    $forward_number     =  &trim($forward_number);
		}else	{
					
			    @user_info 	        =  split(/\s/, $smsbody);
			    $sms_details        =  $user_info[1];
			    @user               =  split(/\,/,$sms_details);
			    $user_name 	        =  $user[0];
			    $forward_number     =  $user[1];
		}
					
		$sql            =  "select count(*) from service_data where value = '$user_name' and target ='$service_id' and name like 'dst%'";
		my @count       =  database_select_as_array($sql);
		$count 	        =  $count[0];
					
		if ($count eq 0)	{
					
			#$returnval = "Contact $user_name was not found.";
			$returnval  =  &Message("CONTACT_NOT_FOUND_MSG");
			$returnval  =~ s/xxxx/$user_name/i;
		}elsif ($count eq 1){
					
		    #insert forward number
			
		    #--------------------------------------------------------------
		    # get index value from service_data table for existing conatcts
		    #--------------------------------------------------------------
			
			$sql            =  "select 1,1,1,target,name,value from service_data where target='$service_id' and value = '$user_name'";
			my %hash        =  database_select_as_hash($sql,"1,1,target,name,value");
			my $target      =  $hash{1}{'target'};
			my $name        =  $hash{1}{'name'};
			my $value       =  $hash{1}{'value'};
			my @index_val   =  split(/\_/, $name);
			$index 	        =  $index_val[1];
			
			# Save new contact

			# check and format number
				
			my ($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($forward_number);
			my $tnumber_status             = $number_status;
			my $tnumber_raw                = $number;
			my $tnumber_clean              = $number_clean;
			my $tnumber_format             = $number_format;
			my $tnumber_format_skype       = ($number_format eq "SKYPE") ? 1 : 0;
			my $tnumber_format_sip         = ($number_format eq "SIP") ? 1 : 0;
			if ($number_status ne "OK"){
							
						$ok     = 0;
						$terror = 1;
						
				if ($number_format eq "SKYPE"){
									
						$terror_number_skype_format = 1;
						
				}elsif ($number_format eq "SIP"){
										
					if ($number_status eq "UNKNOWNCOUNTRY"){
					                      $terror_number_unknown_country = 1;
					
				        }else {
							
					$terror_number_e164_format = 1;
					
				        }
				}else{
							
					$terror_number_format = 1;
				}
			}else{   
					
				$forward_number = $number_clean;
				$ok             = 1;
			}
				#------------------------------------------  
				# if all ok, lets save data
				#------------------------------------------
			if ($ok eq 1){
						
				$sql      = "select count(*) from service_data where target ='$service_id' and value ='$forward_number' and name like 'dst%'";
				my @count = database_select_as_array($sql);
				$count    = $count[0];
						
				if ($count eq 0)   {
						
				    $sql        =  "select count(*) from service_data where target ='$service_id' and name = 'dst_".$index."_forward'";
				    my @count 	=  database_select_as_array($sql);
				    $count      =  $count[0];	
							
					    if ($count eq 0){
								
						&data_set("service_data",$service_id,"dst_".$index."_forward" ,$forward_number);
						$flag = 1; 
					    }else{
								
						$sql  = "update service_data set value ='$forward_number' where target ='$service_id' and name ='dst_".$index."_forward'";
						&database_do($sql);
						$flag = 1;
					    }
								
					if ($flag eq 1){
								
						
						$returnval =&Message("FORWARD_RESP_INFO");#"Contact [$smsbody] was not found.";
						$returnval =~ s/xxxx/$forward_number/i;
						$returnval =~ s/xxxxx/$user_name/i;
						$returnval =~ s/xxxxxx/$forward_number/i;
						$returnval =~ s/xxxxxxx/$user_name/i;
					}	
				}else{
							
					    $returnval  = &Message("EXISTS_FORWARD_NUMBER");#"Contact [$smsbody] was not found.";
					    $returnval  =~ s/xxxx/$forward_number/i;
					
				}
			}	
		}
		elsif ($count gt 1)		{
							
				    $returnval = &found_duplicate_contact($user_name,$service_id," "," ");
		}
	}
    return $returnval,$session;
}


#===================sub found_duplicate_contact()=============================
# Found duplicate contact
#=============================================================================

sub found_duplicate_contact()
{
    my ($user_info,$service_id,$smsbodytext,$lastsms) = @_;
    my $count           =  0;
    my $size            =  "";
    my $dst             =  "";
    my $index           =  "";
    my $getname         =  "";
    my $finalval        =  "";
    my $dial_number     =  "";
    my $name            =  "";
    my $message         =  "";
    my @duplicate_name 	=  "";
    my @duplicate_dst   =  "";
    my @activenumber    = ("(646)434-4612","(646)434-4613","(646)434-4614","(646)434-4615","(646)434-4616","(646)434-4617","(646)434-4618","(646)434-4619","(646)434-4620","(646)434-4621","(646)434-4622","(646)434-4623","(646)434-4624","(646)434-4625","(646)434-4626","(646)434-4627","(646)434-4628","(646)434-4629","(646)434-4630","(646)434-4631","(917)284-9432","(646)873-6314","(646)873-6324","(646)873-6341","(646)873-6342","(646)873-6374","(646)873-6394","(646)873-6913","(646)873-6914","(646)873-6927","(646)873-6928","(646)873-6929","(646)873-6934","(201)204-1821","(201)204-1822","(201)204-1823","(201)204-1824","(201)204-1825","(201)204-1826","(201)204-1827","(201)204-1828","(201)204-1829","(201)204-1830","(201)204-1831","(201)204-1832","(201)204-1833","(201)204-1834","(201)204-1835","(201)204-1836","(201)204-1838","(201)204-1839","(201)204-1840","(201)204-1841",);
    $size = @activenumber;
			
    @duplicate_name = database_select_as_array("SELECT name FROM service_data WHERE value = '$user_info' and target = $service_id and name like 'dst%'");
    @duplicate_dst  = database_select_as_array("SELECT value FROM service_data WHERE value = '$user_info' and target = $service_id and name like 'dst%'");
			
    my $i   = 0;
    my $val = scalar (@duplicate_name);
			
    while ($i < $val)	{
				
			
		my @indexval = split(/_/,$duplicate_name[$i]);
		$dst      = $indexval[0];
			
		$index 	  = $indexval[1];
			
		$getname  = $indexval[2];
			
		$finalval =$duplicate_name[$i];
			
		$dial_number = $activenumber[$index-1];
			
		$dial_number =~ s/[^0-9]*//g;
			
		$count++;
			
		$name .=  $count.")".$duplicate_dst[$i]." - ".$activenumber[$index-1].",\n" ;
			
		$i++;	
    }	
    
    
#-----------------------------------------------
# Find out duplicate contacts in Contact list
#-----------------------------------------------	
		
	if (($smsbodytext =~ m/^(search)/)){
	
		$message  =  &Message("SEARCH_RESP_INFO");
		$message  =~ s/xxxx/$name/i;
	}elsif($lastsms eq "delete"){
		$message  =  &Message("DUPLICATE_DELETE_CONTACT");
		$message  =~ s/xxxx/$name/i;
	}else{
		$message  =  &Message("DUPLICATE_CONTACT_INFO");
		$message  =~ s/xxxx/$name/i;
			
	}
	return $message;	
}

#========================sub do_delete()===============
# Delete the user contact
#======================================================

sub do_delete()
{	
		
    my ($fromnumber,$smsbodytext,$service_id,$lastsms) = @_;
    my $len       =  length($smsbodytext);
    my $user_info =  substr($smsbodytext ,7,$len);
    $user_info 	  =  &trim($user_info);

    my $returnval       =  "";
    my $duplicateindex 	=  "";
    my $flag            =  "";
    my $dial_number     =  "";
	
#--------------------------------------------------
# start default values
#--------------------------------------------------
    my $ok                              =  0;
    my $sql                             =  " ";
    my $size                            =  "";
    my $error                           =  0;
    my $error_number_format             =  0;
    my $error_number_e164_format        =  0;
    my $error_number_skype_format       =  0;
    my $error_number_no_rate            =  0;
    my $error_number_unknown_country    =  0;
    my $error_no_more_index             =  0;
    my $error_bad_index	                =  0;
    my $index                           =  "";
    my $index_new                       =  "";
    my $index_range_low	                =  1;
    my $index_range_hi 	                =  53;    
    my $count                           =  "";
    my $name                            =  "";
    my $number                          =  "";
    my $session                         =  "1";
    my $type_number                     =  "0";
	
#------------------------------------------------  
# user reply with dialnumber to find user contact 
#--------------------------------------------------
	
    if($smsbodytext eq "delete"){
		
		#SMS is delete
		
		$returnval      =  &Message("DELETE_CONTACT_INFO");;
		$session        =  1;
		$error          =  0;
    }else{
			
		if (($user_info =~ m/^(\d+)/)||($user_info =~ m/^(\((\d{0,3})\)(\d{0,3})(\-)(\d{0,4}))/)){
			
			#checking SMS is dialnumber
			my @activenumber     = ("(646)434-4612","(646)434-4613","(646)434-4614","(646)434-4615","(646)434-4616","(646)434-4617","(646)434-4618","(646)434-4619","(646)434-4620","(646)434-4621","(646)434-4622","(646)434-4623","(646)434-4624","(646)434-4625","(646)434-4626","(646)434-4627","(646)434-4628","(646)434-4629","(646)434-4630","(646)434-4631","(917)284-9432","(646)873-6314","(646)873-6324","(646)873-6341","(646)873-6342","(646)873-6374","(646)873-6394","(646)873-6913","(646)873-6914","(646)873-6927","(646)873-6928","(646)873-6929","(646)873-6934","(201)204-1821","(201)204-1822","(201)204-1823","(201)204-1824","(201)204-1825","(201)204-1826","(201)204-1827","(201)204-1828","(201)204-1829","(201)204-1830","(201)204-1831","(201)204-1832","(201)204-1833","(201)204-1834","(201)204-1835","(201)204-1836","(201)204-1838","(201)204-1839","(201)204-1840","(201)204-1841",);
			$size                = @activenumber;
			
			for ( my $i=0; $i<$size; $i++){
					 	
				my $a = $activenumber[$i];
				
				if($user_info =~ m/^(\((\d{0,3})\)(\d{0,3})(\-)(\d{0,4}))/)	{
							
					if($a eq $user_info)	   {
								
						$duplicateindex = $i+1;
						$flag           = 1;
					}
				} else 	{
							
					$a =~ s/[^0-9]*//g;
					
					if($a eq $user_info)   {
						
						$duplicateindex = $i+1;
						$flag           = 1;
					}
				}
			}
						
			if($flag eq 1)	{
							
				$index_new      =  $duplicateindex;
				$dial_number    =  $activenumber[$index];
				$dial_number    =~ s/[^0-9]*//g;
				$count 	        =  1;
			}			
			
			if($index_new ne "")	   {
								
				$index 	=  $index_new;
				$ok     =  1;
			}
			
		}
				
		#if SMS is not dial number checking SMS is contact number or name.
		
		if($index eq "") {
						
			    if($type_number gt 0) {
						
					if(&trim($user_info) =~ m/^(\d+)/)	{
											
						# check and format number
						my ($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($user_info);
						my $tnumber_status             = $number_status;
						my $tnumber_raw                = $user_info;
						my $tnumber_clean              = $number_clean;
						my $tnumber_format             = $number_format;
						my $tnumber_format_skype       = ($number_format eq "SKYPE") ? 1 : 0;
						my $tnumber_format_sip         = ($number_format eq "SIP") ? 1 : 0;
							
							if ($number_status ne "OK")		{
										
									$ok    = 0;
									$error = 1;
								if ($number_format eq "SKYPE")	{
											
									$error_number_skype_format = 1;
								}elsif ($number_format eq "SIP"){
										
								    if ($number_status eq "UNKNOWNCOUNTRY")	{
										$error_number_unknown_country = 1;
								    }else{
										$error_number_e164_format = 1;
								    }
											
								}else{
									$error_number_format = 1;
								}
							}	else {   
										
								$user_info = $number_clean;
							}
					}
			   }
#--------------------------------------------------
# Get count value for user contact list
#--------------------------------------------------
					
				    $sql      = "select count(*) from service_data where target = '$service_id' and value = '$user_info' and name like 'dst%'";
				    my @count = database_select_as_array($sql);
				    $count    = $count[0];
				    
				    if ($count eq 0) {
							$returnval =  &Message("CONTACT_NOT_FOUND_MSG");
							$returnval =~ s/xxxx/$user_info/i;
							$session   =  0;
							$error 	   =  1;
				    } elsif ($count eq 1) {
							
						#Single contact list
						$sql = "select 1,1,1,target,name,value from service_data where target = '$service_id' and value = '$user_info'";
						my %service_data =  database_select_as_hash($sql, "1,1,target,name,value");
						my $target       =  $service_data{1}{target};
						my $name         =  $service_data{1}{name};
						my $value        =  $service_data{1}{value};
							
						#Get index value
						my @indexVal = split(/\_/ , $name);
						$index       = $indexVal[1];
						$ok          = 1;
				    }elsif ($count gt 1)	{
							
						$returnval =  &found_duplicate_contact($user_info,$service_id," ",$lastsms);
						$session   =  0;
						$error     =  1;
				    }
		}
#--------------------------------------------------
# try to delete
#--------------------------------------------------
		if ($ok eq 1)    {
							
			# delete data
							
			my $forward_number =  &data_get("service_data",$service_id,"dst_".$index."_forward");
			my $name           =  &data_get("service_data",$service_id,"dst_".$index."_name");
			my $number         =  &data_get("service_data",$service_id,"dst_".$index."_number");
							
			if($number eq ""){
							
				#$returnval ="Contact [$smsbodytext] was not found.";
				$returnval =	&Message("CONTACT_NOT_FOUND_MSG");
				$returnval =~   s/xxxx/$smsbodytext/i;
				return $returnval,0,1;
			}
							
			if ($forward_number ne "")	{
				&data_delete("service_data",$service_id,"dst_".$index."_forward");
			}
								
			&data_delete("service_data",$service_id,"dst_".$index."_name");
			&data_delete("service_data",$service_id,"dst_".$index."_number");
			&data_delete("service_data",$service_id,"dst_".$index."_callid");
			&data_delete("service_data",$service_id,"dst_".$index."_carrier");
			&data_delete("service_data",$service_id,"dst_".$index."_rslot");
			&data_delete("service_data",$service_id,"dst_".$index."_callback");
			&data_delete("service_data",$service_id,"dst_".$index."_routeann");
			&data_delete("service_data",$service_id,"dst_".$index."_balanceann");
				
			# $returnval = "Contact [$name - $number] has been deleted.";
			my $result      =  "$name - $number";
			$returnval      =  &Message("DELETE_RESP_INFO"); 
			$returnval      =~ s/xxxx/$result/i;
			$session        =  1;
			$error 	        =  0;
		}
    }
    return $returnval,$session,$error;
}

#===================sub do_search()=================================
# search the user details in contact
#===================================================================

sub do_search()
{
    my ($fromnumber,$smsbody,$service_id,$last_sms) = @_;
    my $returnval       =  "";
    my $len             =  length($smsbody);
    my $user_info       =  substr($smsbody,7,$len);
    $user_info 	        =  &trim($user_info);

    my $ok              =  "";
    my $sql             =  "";
    my $index           =  "";
    my $size            =  "";
    my $duplicateindex 	=  "";
    my $flag            =  "";
    my $dial_number     =  "";
    my $count           =  "";
    my $error           =  "";
    my $error_number_skype_format       =  "";
    my $error_number_unknown_country    =  "";
    my $error_number_e164_format        =  "";
    my $error_number_format             =  "";
    my $session                         =  "";	
		
	if($smsbody eq "search")	{
						
		$returnval =  &Message("SEARCH_CONTACT_INFO");;
		$session   =  1;
		$error     =  0;
			
	} elsif ((lc(&trim($smsbody))=~ m/^(search)+\s+((\w[a-zA-Z]+)(\s?)+(\w+)?)$/) || (lc(&trim($smsbody))=~ m/^(search)+\s+(\d+)$/)) {
			
		if(&trim($user_info) =~ m/^(\d+)/)    {
				
		    # check and format number
		    my ($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($user_info);
		    my $tnumber_status             = $number_status;
		    my $tnumber_raw                = $user_info;
		    my $tnumber_clean              = $number_clean;
		    my $tnumber_format             = $number_format;
		    my $tnumber_format_skype       = ($number_format eq "SKYPE") ? 1 : 0;
		    my $tnumber_format_sip         = ($number_format eq "SIP") ? 1 : 0;
				
		    if ($number_status ne "OK")		{
				$ok    = 0;
				$error = 1;
				if ($number_format eq "SKYPE")	{
						
					$error_number_skype_format = 1;
				} elsif ($number_format eq "SIP") {
						
					if ($number_status eq "UNKNOWNCOUNTRY") {
							
						$error_number_unknown_country = 1;
					}else {
						$error_number_e164_format = 1;
					}
				}else{
							
					$error_number_format = 1;
				}
		   }else{   
				$user_info = $number_clean;
		   }
		}
	
	$sql = "select count(*) from service_data where target = $service_id and value ='$user_info' and name like 'dst%'";
	my @count =database_select_as_array($sql);

	$count = $count[0];
	if ($count eq 0)    {							
		   
		    $returnval 	=  &Message("CONTACT_NOT_FOUND_MSG");
		    $returnval 	=~ s/xxxx/$user_info/i;
		    $session    =  0;
		    $error      =  1;
	}elsif ($count eq 1){
							
		    #Single contact list
							
		    $sql = "select 1,1,1,target,name,value from service_data where target = '$service_id' and value = '$user_info'";
		    my %service_data    =  database_select_as_hash($sql, "1,1,target,name,value");
		    my $target 	        =  $service_data{1}{target};
		    my $name            =  $service_data{1}{name};
		    my $value           =  $service_data{1}{value};
			
		    #Get index value
								
		    my @indexVal  =  split(/\_/ , $name);
		    $index        =  $indexVal[1];
		    my @activenumber     = ("(646)434-4612","(646)434-4613","(646)434-4614","(646)434-4615","(646)434-4616","(646)434-4617","(646)434-4618","(646)434-4619","(646)434-4620","(646)434-4621","(646)434-4622","(646)434-4623","(646)434-4624","(646)434-4625","(646)434-4626","(646)434-4627","(646)434-4628","(646)434-4629","(646)434-4630","(646)434-4631","(917)284-9432","(646)873-6314","(646)873-6324","(646)873-6341","(646)873-6342","(646)873-6374","(646)873-6394","(646)873-6913","(646)873-6914","(646)873-6927","(646)873-6928","(646)873-6929","(646)873-6934","(201)204-1821","(201)204-1822","(201)204-1823","(201)204-1824","(201)204-1825","(201)204-1826","(201)204-1827","(201)204-1828","(201)204-1829","(201)204-1830","(201)204-1831","(201)204-1832","(201)204-1833","(201)204-1834","(201)204-1835","(201)204-1836","(201)204-1838","(201)204-1839","(201)204-1840","(201)204-1841",);
		    $size         =  @activenumber;
								
		    for ( my $i=0; $i<$size; $i++)	{
							
				if ($i==$index) {
							
					    $dial_number = $activenumber[$index-1];					 
					    $ok          = 1;
				}
		    }
				
		    if ($ok eq 1)   {
					
				my $_name       =  &data_get("service_data",$service_id,"dst_".$index."_name");
				my $_number     =  &data_get("service_data",$service_id,"dst_".$index."_number");
				my $_rslot      =  &data_get("service_data",$service_id,"dst_".$index."_rslot");
                my $result      =  "$_name - $dial_number";
				$returnval      =  &Message("SEARCH_RESP_INFO");
				$returnval      =~ s/xxxx/$result/i;
				$session        =  1;
				$error 	        =  0;
		    }
	}elsif ($count gt 1) {
			
		    $returnval 	=  &found_duplicate_contact($user_info,$service_id,$smsbody," ");
		    $session    =  1;
		    $error      =  0;
    	}
			
    }
    return $returnval,$session,$error;  
}

#======================new_user_join()=========================
# This function checks the new request to join zenofon.
#==============================================================

sub new_user_join()
{
    my($fromnumber,$smsbodytext) = @_;
    my $body    =  "We have a new request to join Zenofon from this number $fromnumber";
    my $title   =  "Zenofon";
    my $to      =  "support\@zenofon.com";
    my $from    =  "ccalert\@zenofon.com";
    my $subject	=  "Zenofon New User Join Request";
    &send_email($from,$to,$subject,$body,1);
    #return $body;
}

#=====================================================
# Add credit card
#=====================================================
sub add_credit_card()
{
    my($fromnumber,$smsbodytext,$service_id,$last_sms) = @_;
    my $returnval  =  "";
    my $ok         =  "";
    my $session    =  "";
    my $error      =  "";
		
    #Checks the credit card details in exists user account
			
    if ($smsbodytext eq "add credit card")	{
			
		#get user credit card number
			
		my $sql = "SELECT 1,1,cc_type,cc_number
			FROM service_profile_cc
			WHERE service_id='$service_id' and ani='$fromnumber'";
				
		my %hash=database_select_as_hash($sql,"flag,cc_type,cc_number");
		if (keys(%hash) gt 0)  {
					
			    my $cc_type = $hash{1}{cc_type};
					
			    #get last 4 digit of cc number
					
			    my $cc_number =  substr($hash{1}{cc_number},(length($hash{1}{cc_number})-4));
			    my $message   =  &Message("ADD_CREDIT_CARD_INFO");
			    $message      =~ s/xxxx/$cc_type/i;
			    $message      =~ s/xxxxx/$cc_number/i;
			    $returnval 	  =  $message;			   
			    $session      =  1;
			    $error        =  0;
		}else	{
			    $ok = 1;
		}
    }elsif (lc(&trim($smsbodytext)) eq "yes")	{
		$ok = 1;
    }
					
    if ($ok eq 1) {
					
		$returnval = &Message("ADD_CREDIT_CARD_RESP");	
		$session   = 1;
		$error     = 0;
    }
					
    return $returnval,$session,$error;
}

#=====================================================
#      Recharge with cc
#=====================================================
sub do_recharge()
{
    my($fromnumber,$smsbodytext,$service_id,$last_sms) = @_;
    my $returnval                               =  "";
    my %tmp_hash                                =  "";
    my $session                                 =  "";
    my $error 	                                =  "";
    my $switch_on_first_credit 	                =  "";
    my $limit_max_recharges_in_7days            =  "";
    my $limit_maximum_balance 	                =  "";
    my $recharges_in_7_days                     =  "";
    my $status_error 	                        =  0;
    my $error_message_max_recharges_in_7days    =  0;
    my $balance                                 =  "";
    my $balance_limit 	                        =  "";
    my $error_message_max_balance               =  0;
    my $add_amount                              =  "";
    my $total                                   =  0;
    my %hash 	                                =  "";
    my $sql                                     =  "";
    my $recharged_amount                        =  0;
    my %answer 	                                =  "";
    my $all_credits_qtd                         =  -1; 
    my $all_credits_sum                         =  -1;
    my $week_credits_qtd                        =  -1; 
    my $week_credits_sum                        =  -1;
    my %order                                   =  ""; 
    my $answer_ok                               =  0;
    my $can_add_credit 	                        =  0;
							
    %tmp_hash                 = &multilevel_securedata_cc_get($service_id,"DO_NOT_CHECK_CC_ERROR");
    my $profile_exists 	      = ($tmp_hash{status_ok} eq 1) ? 1 : 0;
			
    #check profile exists or not  
			
    if($profile_exists gt 0)	{	
			
	$sql = "
	SELECT
		1, 1,
		service_status.can_add_credit,service.status, service_status.id FROM service, service_status
	where service.status=service_status.id and service.id='$service_id'
	";
	%hash              = database_select_as_hash($sql,"flag,can_add_credit");
	my $can_add_credit = $hash{1}{can_add_credit};
			
	if($can_add_credit eq 1) {
		
		#sql to get all details
				
		$sql = "SELECT 1,1,service_status.switch_on_first_credit,service_status.limit_max_balance,service_status.limit_max_recharges_in_7days,service.balance,service.limit
			FROM
			    	service,
				service_status
			where
				service.status=service_status.id and
				service.id='$service_id'";
					
		%hash = database_select_as_hash($sql,"flag,switch_on_first_credit,limit_max_balance,limit_max_recharges_in_7days,balance,limit");
		$switch_on_first_credit  	=  $hash{1}{switch_on_first_credit};
		$limit_maximum_balance 		=  $hash{1}{limit_max_balance};
		$limit_max_recharges_in_7days 	=  $hash{1}{limit_max_recharges_in_7days};
		$balance 			=  $hash{1}{balance};
		$balance_limit 			=  $hash{1}{limit};
					
		#get details on recharge value in 7 days	
					
		$sql = "
		    SELECT 1,1,sum(value)
		    FROM credit 
		    where service_id='$service_id' and date>date_sub(now(), interval 7 day) and value>0
		    ";
		%hash                = database_select_as_hash($sql,"flag,value");
		$recharges_in_7_days = ($hash{1}{flag} eq 1) ? $hash{1}{value} : 0; 
					
		#week credit sum for first rechrage pin relesase
					
		%hash = database_select_as_hash("
		    SELECT 1,1,count(*),sum(value)
		    FROM credit 
		    where service_id='$service_id' and date>date_sub(now(), interval 7 day) and value>0
		    ","flag,qtd,value"
		    );
		if ($hash{1}{flag} eq 1) {
						
				    $week_credits_qtd = $hash{1}{qtd}; 
				    $week_credits_sum = $hash{1}{value};
		}
				
		#all credit sum for first rechrage pin relesase	
			
		%hash = database_select_as_hash("
		    SELECT 1,1,count(*),sum(value)
		    FROM credit 
		    where service_id='$service_id' and value>0
		    ","flag,qtd,value"
		    );
		if ($hash{1}{flag} eq 1) {
				
			    $all_credits_qtd = $hash{1}{qtd}; 
			    $all_credits_sum = $hash{1}{value};
		}
				
		#functions coming
		#if sms body is 'recharge'
				
		if($smsbodytext eq "recharge")     {
							
		    my @total_recharge = database_select_as_array("SELECT count(*),sum(value)
		    FROM credit 
		    where service_id='$service_id' and value>0");
		    $recharged_amount = $total_recharge[0];
				
		    #check whether first recharge
				
		    if(($recharged_amount eq 0)  && ($switch_on_first_credit ne ""))       {
				     $returnval = &Message("RECHARGE_FIRST_CREDIT");	
				    
		    }
		    #if not first recharge       
		    else
		    {
				    $returnval = &Message("RECHARGE_AMOUNT");
		    }
		    $session = 1;
		    $error   = 0;
		}
			
		#if sms body is recharge amount '$5' like
		elsif((lc(&trim($smsbodytext)) =~ m/^\$(\d)+$/) && (lc(&trim($last_sms)) eq "recharge")){
			
		    #check match to available recharge options
		    if(((lc(&trim($smsbodytext)) eq "\$5") || (lc(&trim($smsbodytext)) eq "\$10") || (lc(&trim($smsbodytext)) eq "\$20") || (lc(&trim($smsbodytext)) eq "\$50"))) {   
					
			        $add_amount = $smsbodytext;
				$add_amount =~ s/\$//g;
					
				#find total with entered and main balance   
				$total = $balance+$add_amount;	

				#get maximum balance with balance_limit
				if ( ($balance_limit > 0) && ($total > $balance_limit) ) {
					
					    $status_error              = 1;
					    $error_message_max_balance = 1;
				}
					
				#check limited user or not
					
				if($status_error gt 0 && $error_message_max_balance gt 0)  {
					    
					    my $message =  &Message("RECHARGE_CREDIT_DECLINED");
					    $message    =~ s/xxxx/$smsbodytext/i;
					    $returnval  = $message;
					    $session    =  1;
					    $error      =  1;
				}  else     {
							
					    %order = ();
					    $order{service_id}             = $service_id;
					    $order{value_credit}           = $add_amount;
					    $order{value_money}            = $add_amount;
					    $order{type}                   = "AUTHORIZE_CIM";
					    $order{from_type}              = "SMS";
							
					    %answer     =  &multilevel_credit_add(%order);
					    $answer_ok 	=  $answer{ok};
							
					    my $answer_message= ($answer{message} eq "Aproved") ? "Your credit was approved": "I can not approve this credit. ".$answer{message};
							
					    # log CC errors
					    if ($answer_ok ne 1)  {
							
						        &action_history("cim:payment:recharge:error",('service_id'=>$service_id));
							
					    } else {
							
						        &action_history("cim:payment:recharge",('service_id'=>$service_id));
							
					    }
							
					    if ($answer_ok eq 1)    {
							
							my $message     =  &Message("RECHARGE_CREDIT_APPROVED");
							$message        =~ s/xxxx/$smsbodytext/i;
							$total 	        =  "\$$total";
							$message        =~ s/xxxxx/$total/i;
                            $returnval      =  $message;
							$session        =  1;
							$error 	        =  0;
		            
					    }   else     {
							my $message     =  &Message("RECHARGE_CREDIT_DECLINED");
							$message        =~ s/xxxx/$smsbodytext/i;
                            $returnval      =  $message;
							$session        =  1;
							$error 	        =  1;
					    }
				}
		    }#if available recharge loop end
		    else {
				my $message =  &Message("RECHARGE_INVALID_AMOUNT");
				$returnval  =  $message;
                $session    =  0;
				$error      =  1;
		    }
		}	
		
		#if smsbody is 'yes'
		elsif((lc(&trim($smsbodytext)) eq "yes") && (lc(&trim($last_sms)) eq "recharge"))	{
			    $add_amount = 5;
			    $total = $balance+$add_amount;
						
				%order = ();
				$order{service_id}                      = $service_id;
				$order{value_credit}                    = $add_amount;
				$order{value_money}                     = $add_amount;
				$order{type}                            = "AUTHORIZE_CIM";
				$order{from_type}                       = "SMS";
						
				%answer         =  &multilevel_credit_add(%order);
				$answer_ok      =  $answer{ok};
						
				my $answer_message= ($answer{message} eq "Aproved") ? "Your credit was approved": "I can not approve this credit. ".$answer{message};
						
			# log CC errors
			if ($answer_ok ne 1)  {
						
					    &action_history("cim:payment:recharge:error",('service_id'=>$service_id));
			} else {
						
					    &action_history("cim:payment:recharge:error",('service_id'=>$service_id));
			}
						
			# unlock pin if add value and first credit
						
			if ($answer_ok eq 1) {
							
				    if ( ($all_credits_qtd eq 0)  && ($switch_on_first_credit ne "") ) {
						
						&database_do("update service set last_change=now(), status='$switch_on_first_credit' where id='$service_id'");
						&action_history("status:first_recharge",('service_id'=>$service_id));
						%answer = &multilevel_suspicious_check(('service_id'=>$service_id, 'force_suspicious_if_no_validated_ani'=>1));
				    } else {
						
						%answer = &multilevel_suspicious_check(('service_id'=>$service_id));
				    }
			}	
						
			if ($answer_ok eq 1) {
						
                    my $message     =  &Message("RECHARGE_CREDIT_APPROVED");
					$add_amount     =  "\$$add_amount";
					$message        =~ s/xxxx/$add_amount/i;
					$message        =~ s/xxxxx/$add_amount/i;
					$returnval      =  $message;
					$session        =  1;
					$error          =  0;
			} else 	{
					$add_amount 	=  "\$$add_amount";
					my $message 	=  &Message("RECHARGE_CREDIT_DECLINED");
					$message        =~ s/xxxx/$add_amount/i;
					$returnval      =  $message;
					$session        =  1;
					$error          =  1;
			}
		}
		#if smsbody is 'no'	
		elsif((lc(&trim($smsbodytext)) eq "no") && (lc(&trim($last_sms)) eq "recharge"))  {
						
				    $returnval 	=  &Message("MENU_INFO");
				    $session   	=  1;
				    $error      =  0;
		}		
	
	}#can add credit end
	
		
    } else   {
					
				my $message  =  &Message("RECHARGE_CC_NOT_FOUND");
				$returnval   =  $message;
				$session     =  0;
				$error       =  1;
    }
    return $returnval, $session, $error;		
}

#=====================sub auto_recharge()==================
# update the Auto recharge values to user account
#==========================================================
sub auto_recharge()
{
    # start
    my($fromnumber,$smsbodytext,$service_id,$last_sms) = @_;
    my %app             =  ();
    $app{service_id}    =  $service_id;
    my $returnval       =  "";
    my $session         =  "";
    my $error           =  "";
    my %t               =  ();
    my $session_value   =  &getSessionObj;
				
    if (lc(&trim($smsbodytext)) eq "auto recharge") {
				
		my %tmp_hash              =  &multilevel_securedata_cc_get($app{service_id},"DO_NOT_CHECK_CC_ERROR");
		$t{profile_exists}        =  ($tmp_hash{status_ok} eq 1) ? 1 : 0;
			
		if ($t{profile_exists} eq 1)   {
			    
				#to set user min balance for auto recharge
				
			    $returnval 	= &Message("AR_MIN_BALANCE");			    
			    $session    = 1;
			    $error      = 0;
		}  else  {
				
				#if no credit card details found,send format to add credit card to user profile
				
			    $returnval 	= &Message("AR_CC_NOT_FOUND");				  
			    $session    = 1;
			    $error      = 0;
		}
		
	return $returnval,$session,$error;
	exit;
		
    } elsif((lc(&trim($last_sms)) eq "auto recharge")) 	{
		
	# Low balance $5 or $2
		
	if ((lc(&trim($smsbodytext)) eq "\$5" && (lc(&trim($last_sms)) eq "auto recharge")) || (lc(&trim($smsbodytext)) eq "\$2"))    {
				
		    #Add low balance to account
		    my $low_balance = ($smsbodytext eq "\$5") ? "balance_5" : "balance_2";
				
		    #set auto recharge low balance in session 
		    $session_value->param("low_balance",$low_balance);
				
		    #After Adding following msg send
		      $returnval 	= &Message("AR_AMOUNT");
		    #$returnval = "Please enter the amount you would like to auto recharge, Please type '\$5','\$10','\$20','\$50'.";
		    $session_value->param("auto","auto_1");
		    $session        = 1;
		    $error          = 0;
	} else {
		
			$returnval      = &Message("AR_INVALID_MIN_BALANCE");			
			$session        = 0;
			$error 	        = 1;
	}
	
	return $returnval,$session,$error;
	exit;
	
    }
    my $action = $session_value->param("auto");
		
    if ($action eq "auto_1") {
				
	#Add Recharge amount value $5,$10,$20,$50
	if (lc(&trim($smsbodytext)) eq "\$5" || lc(&trim($smsbodytext)) eq "\$10" || lc(&trim($smsbodytext)) eq "\$20" || lc(&trim($smsbodytext)) eq "\$50") {
				
		    my $recharge_amount = substr($smsbodytext,1,2);
		    #set auto recharge amount in session 
					
		    $session_value->param("recharge_amount",$recharge_amount);
			
		    #Add recharge amount value
			
		    $returnval 	= &Message("AR_LIMIT_AMOUNT");			    
		    $session_value->param("auto","auto_2");
		    $session    = 0;
		    $error      = 0;
			
	}else	{
		
		$returnval      = &Message("AR_INVALID_AMOUNT");		
		$session        = 0;
		$error 	        = 1;
	}
					
	return $returnval,$session,$error;
	exit;
	
    }
    elsif ($action eq "auto_2")	{
						
	#Add Auto recharge limit Value
						
	if (lc(&trim($smsbodytext)) eq "\$30" || lc(&trim($smsbodytext)) eq "\$60" || lc(&trim($smsbodytext)) eq "\$90")	{
		    
		    my $recharge_limit = substr($smsbodytext,1,2);
		    my $ok             = 0;
		    my $save 	       = 0 ;
		    
		    if ($recharge_limit eq 30){$recharge_limit = "30days_30";}
		    if ($recharge_limit eq 60){$recharge_limit = "30days_60";}
		    if ($recharge_limit eq 90){$recharge_limit = "30days_90";}
					
		    #get auto recharge values from session
					
			my $ar_threshold =   $session_value->param("low_balance");
			my $ar_value     =   $session_value->param("recharge_amount");
			my $ar_limit     =   $recharge_limit;
					
			if (defined($ar_threshold) && ($ar_threshold ne "") && defined($ar_value) && ($ar_value ne "") && ($ar_limit ne ""))  {
					   $ok = 1;	
			}
						
			if ($ok eq 1) {
						
					my %t               = ();
					$t{status_ok}       = 0;
					$t{status_error}    = 0;
					my $sql = "
							
						SELECT 1,1,service_status.can_add_credit, service_status.can_auto_recharge, service_status.limit_max_balance 
						FROM service, service_status 
						where service.status=service_status.id and service.id='$app{service_id}'";
						
					my %hash = database_select_as_hash($sql,"flag,can_add_credit,can_auto_recharge,limit_max_balance");
						
					$t{can_add_credit}      = ($hash{1}{can_add_credit} eq 1) ? 1 : 0;
					$t{can_auto_recharge}   = ($hash{1}{can_auto_recharge} eq 1) ? 1 : 0;
					$t{limit_max_balance}   = $hash{1}{limit_max_balance};
						
					# check CIM profile
					my %tmp_hash = &multilevel_securedata_cc_get($app{service_id},"DO_NOT_CHECK_CC_ERROR");
						
					$t{profile_exists}              = ($tmp_hash{status_ok} eq 1) ? 1 : 0;
					$t{profile_with_cc_errors}      = ($tmp_hash{cc_error} eq 1) ? 1 : 0;
					$t{profile_ok}                  = ($t{profile_exists}.$t{profile_with_cc_errors} eq "10") ? 1 : 0; 
					$t{profile_cc_number}           = $tmp_hash{cc_number};
					$t{profile_cc_first_name}       = $tmp_hash{first_name};
					$t{profile_cc_last_name}        = $tmp_hash{last_name};
						
					# check auto_recharge data
					%hash = database_select_as_hash("SELECT 1,1,is_auto_recharge FROM service_profile_cc where service_id='$app{service_id}' and active=1","flag,value");
					$t{auto_recharge_enabled}  =  (($hash{1}{flag} eq 1) && ($hash{1}{value} eq 1)) ? 1 : 0;
					$t{auto_recharge_enabled}  =  ($t{auto_recharge_enabled} eq 0) ? 1 : 	$t{auto_recharge_enabled};
						
					# save change
					if ( ($t{status_error} eq 0) && ($t{can_auto_recharge} eq 1) && ($t{profile_ok} eq 1)) {
						
						# update autorecharge data
						$sql = "update service_profile_cc set is_auto_recharge='$t{auto_recharge_enabled}' where service_id='$app{service_id}' and active=1";
						&database_do($sql);
						$t{auto_recharge_threshold}     = &data_get("service_data",$app{service_id},"ar_threshold");
						$t{auto_recharge_value}	        = &data_get("service_data",$app{service_id},"ar_value");
						$t{auto_recharge_but}           = &data_get("service_data",$app{service_id},"ar_limit");
							
						if (($t{auto_recharge_threshold} eq "") && ($t{auto_recharge_value} eq "") && ($t{auto_recharge_but} eq ""))
							
						{	
						        &data_set("service_data",$app{service_id},"ar_threshold",$ar_threshold);
						        &data_set("service_data",$app{service_id},"ar_value",$ar_value);
						        &data_set("service_data",$app{service_id},"ar_limit",$ar_limit);
						        &action_history("ar:status:on",('service_id'=>$app{service_id}));		
						        &multilevel_change_service_status_by_switch_on_data($app{service_id},"switch_on_autorecharge_in");
						}else{					
								
							$sql = qq{update service_data set value ="$ar_limit" where target = $app{service_id} and name = "ar_limit"};
							&database_do($sql);
							$sql = qq{update service_data set value ="$ar_threshold" where target = $app{service_id} and name = "ar_threshold"};
							&database_do($sql);
							$sql = qq{update service_data set value ="$ar_value" where target = $app{service_id} and name = "ar_value"};
							&database_do($sql);
							&action_history("ar:status:on",('service_id'=>$app{service_id}));		
							&multilevel_change_service_status_by_switch_on_data($app{service_id},"switch_on_autorecharge_in");
						}
							
						# update coupon engine
						&multilevel_coupon_engine_autorecharge($app{service_id});
						$ar_threshold   = ($ar_threshold eq "balance_5") ? "\$5" : "\$2";
						$ar_value       = "\$".$ar_value;
						$ar_limit       = substr($ar_limit, 7,);
						$ar_limit       = "\$".$ar_limit;
						my $message     = &Message("AR_RESP_INFO");
						$message        =~ s/xxxx/$ar_threshold/i;
						$message        =~ s/xxxxx/$ar_value/i;
						$message        =~ s/xxxxxx/$ar_limit/i;
						$returnval      = $message;
						
						$session_value->clear(["auto"]);
						$session_value->clear(["low_balance"]);
						$session_value->clear(["recharge_amount"]);
						$session        =  1;
						$error 	        =  0;
					}	
			}else{
					
				$returnval = "Sorry, I didn't understand your response.";
				$session   = 1;
				$error     = 0;
			}
	}else{
			    $returnval 	= &Message("AR_INVALID_LIMIT_AMOUNT");		
			    
			    $session    = 0;
			    $error      = 1;
	}
		
	return $returnval,$session,$error;
	exit;
    }
}