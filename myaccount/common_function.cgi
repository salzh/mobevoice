#!/usr/bin/perl
#=======================================================
# SMS Subroutines are included here.
#=======================================================

require "../include.cgi";
#require "/usr/local/multilevel/www/include.cgi"; # To run on local machine

#=============Required Packages=========================
use strict;
use feature qw(switch say);
use DBI;
use Digest::MD5 qw(md5 md5_hex md5_base64);
use File::Copy;
use POSIX;
use HTML::Template; 
use LWP 5.69;
use strict;
use warnings;
use lib 'lib';
use CGI::Session;
use CGI;
#=======================================================
#Set session value
my $cgi=new CGI;
my $ssid=$cgi->cookie('ID');
my $counter=0;


my %carriers_list = ();
$carriers_list{"USAATT"}		= "At&t";
$carriers_list{"USAALLTEL"}		= "Alltel";
$carriers_list{"USABOOST"}		= "Boost mobile";
$carriers_list{"USAONE"}		= "Cellular One";
$carriers_list{"USACRICKET"}	= "Cricket";
$carriers_list{"USACINGULAR"}	= "Go/Cingular (prepaid)";
$carriers_list{"USAMETROPCS"}	= "Metro PCS";
$carriers_list{"USASPRINT"}		= "Sprint/Nextel";
$carriers_list{"USATMOBILE"}	= "T-mobile";
$carriers_list{"USATMOBILETOGO"}= "T-mobile ToGo";
$carriers_list{"USATRACKFONE"}	= "Tracfone";
$carriers_list{"USAUS"}			= "U.S. Cellular";
$carriers_list{"USAVERIZON"}	= "Verizon Wireless";
$carriers_list{"USAVERIZONPAYG"}= "Verizon Wireless Pay as you go";
$carriers_list{"USAVIRGIN"}		= "Virgin Mobile";
$carriers_list{"UNKNOWN"}		= "Unknown";
$carriers_list{"LANDLINE"}		= "Landline";
$carriers_list{"NOTLISTED"}		= "Not listed";


#======================sms_services()========================
#The core function which recieves sms through TWILIO and sends
#sms through TWILIO API
#==============================================================
sub sms_services()
{
   my ($fromnumber,$smsbodytext) = @_;
   my $returnval = "";
   my $StatusValue = "";
   my $isValidUser = "";
   
   #valid User status
   my @isValidUserArray = &isZenofonUser($fromnumber,$smsbodytext); #  my ($FromNumber,$BodyText) = @_;  return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)  
   $isValidUser=$isValidUserArray[0];
   
   if ($isValidUser eq 0)
   {
	  $returnval = "You are not zenofon user,please registered in www.zenofon.com";
	  exit;
   }
   
   # Mute and Unmute status Update   
   &sms_client_status($isValidUser,lc(&trim($smsbodytext)),&trim($fromnumber));  
   
   # Mute and Unmute status value  
   my @status = &MuteUnmute_status(&trim($fromnumber));
     $StatusValue = $status[0];
	 
   #***********Get Change SMS Syntax**********************#
   my %hash = database_select_as_hash("SELECT id,msg_type,msg_text FROM sms_customtext","msg_type,msg_text");
   my %initiate = %{$hash{1}};
   my %addnew = %{$hash{2}};
   my %confirmation = %{$hash{3}};
   
   my $initiateaction=$initiate{msg_text};
   my $AddNew=$addnew{msg_text};
   my $confirmation=$confirmation{msg_text};
   #***************************************************************************#
      
   my @getbodylen = split(/\,/, $smsbodytext);
   my $size = scalar @getbodylen;  
   
   my $reroutecount = "";
   my $reroutemeessage = "";
   my $val= "";
    if(lc(&trim($smsbodytext)) ne 1 && lc(&trim($smsbodytext)) ne 2 && lc(&trim($smsbodytext)) ne "reroute last call")
	  {
		 if((lc(&trim($smsbodytext)) ne lc(&trim($initiateaction))) && (($size) ne 2 && ($size eq 1)) || (lc(&trim($smsbodytext)) =~ m/^(\w[route]+)+\s?(\d)$/) || lc(&trim($smsbodytext)) eq "no" )
		 {		   
			  my @getUserroute=&userReroute($isValidUser,$StatusValue,lc(&trim($smsbodytext)),&trim($fromnumber));
			  $reroutecount=$getUserroute[0];
			  $reroutemeessage=$getUserroute[1];		  
		 }
		 
	  }  
    if($isValidUser eq 1)
	{
	  if( lc(&trim($smsbodytext)) eq lc(&trim($initiateaction)))
	  {		
		$returnval = &Message();		
	  }
	  elsif (lc(&trim($smsbodytext)) eq "1") #****************************************************************
	  {		
		$returnval = &Message("1");
	  }elsif (lc(&trim($smsbodytext)) eq "reroute last call")
	  {
			   $returnval = &rerouteLastCall(&trim($fromnumber),lc(&trim($smsbodytext)));
			   
			   
	  }elsif (lc(&trim($smsbodytext)) eq "yes") #****************************************************************
	  {
		 my $sql="";
		 
		 my @rerouteStatusArray = database_select_as_array("SELECT sms_status_value FROM sms_status","sms_status_value");
		 my $reroutestatusvalue = &getSMSStatus(2,$fromnumber);
		 
		 if($reroutestatusvalue eq 1){
			
			&getSMSStatus(1,$fromnumber);
		 
			my(%sms_data)=&getLastrequest($fromnumber);
		 
			my $route_temp=$sms_data{sms_next_route};
		
			 if($route_temp gt 0){
			
				  my $sms_route_id=$sms_data{sms_route_id};
				  my $sms_current_route=$sms_data{sms_value};
				  my $sms_dst_no=$sms_data{sms_contact_number};
			
			
				  my $deleteroute = "DELETE FROM sms_route_temp where sms_route_id='$sms_route_id'";
				  database_do($deleteroute);
			
				  $returnval ="All Future Calls to  $sms_dst_no will now be routed through route $sms_current_route.";
			   }
		 }
	  }
	  else
	  {		
		if (lc(&trim($smsbodytext)) eq "mute" || lc(&trim($smsbodytext)) eq "unmute" || lc(&trim($smsbodytext)) eq "reroute"  || ($reroutecount ne "" && $reroutemeessage ne "") || lc(&trim($smsbodytext)) eq 2)
		 {
			
		   if(lc(&trim($smsbodytext)) eq "mute" && $StatusValue eq 0)
		   {
			   if (lc(&trim($smsbodytext)) eq "mute" && $isValidUser eq 1)
			   {
				 $returnval = &Message("3");			
			   }
			   else
			   {
				  $returnval = &Message("8");					
			   }
		   }
		   elsif($StatusValue eq 1)
		   {
			  if (lc(&trim($smsbodytext)) eq "unmute")
			  {
				  if (lc(&trim($smsbodytext)) eq "unmute" && $isValidUser eq 1) 
				  {
					  if($isValidUser==1)
					  {
	  					  #$returnval = $AddNew;
						  $returnval = "Thank you, You will start receiving SMS from Zenofon now";
					  }
					  else
					  {						
						  $returnval = &Message("5");
					  }
				  }
				  else
				  {					
					$returnval = &Message("6");
				  }	
			  }
			  elsif(lc(&trim($smsbodytext)) eq "reroute" || lc(&trim($smsbodytext)) eq  2)
			   {
				  &getSMSStatus(0,$fromnumber);
				  $returnval = &Message("13");
			   }
			   elsif(lc(&trim($smsbodytext)) eq "addnew" || lc(&trim($smsbodytext)) eq  3)
			   {
				  $returnval = $AddNew;  
			   }
			   elsif($reroutecount eq 0)
			   {
			   $returnval = $reroutemeessage;
			   }
			   elsif($reroutecount gt 0)
			   {
			    $returnval = $reroutemeessage;
			   }
			  
		    }
		 }		 
		 else
		 {
		   if (($size gt 1) && ($StatusValue eq 1))
		   {
			  if(lc(&trim($smsbodytext)) =~ m/^(\w[a-zA-Z]+)+\,+(\s?\+?(\d+))$/) #Add New Contact Format
				 {
					my @isValidUserArray1 = &isZenofonUser(&trim($fromnumber),$smsbodytext); # return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
					my $isValidUser1=$isValidUserArray1[0];
					my $service_id=$isValidUserArray1[2];
					if($isValidUser1==1)
					{
					   if($service_id ne "")
					   {
						  my @contactinfo = split(/,/, $smsbodytext);
						  my $contactname = $contactinfo[0];
						  my $contactnumber = &trim($contactinfo[1]);		
						  my @addContactResult =  &addContact($service_id,$contactname,$contactnumber);  #my ($aservice_id,$fname,$fnumber) = @_; return ($ok,$name,$number,$activenumber[$index-1]);
						  my $ok1=$addContactResult[0];
						  my $name1=$addContactResult[1];
						  my $number1=$addContactResult[2];
						  my $activenumber1=$addContactResult[3];
						  if($ok1==1)
						  {
							 if (($confirmation =~ s/\+?xxxxxxxxxx/$number1/i) && ($confirmation =~ s/\+?xxxxxxxx/$activenumber1/i))  						
							 {							  					                
							   $returnval = $confirmation;
							 }
							 else
							 {
								$returnval = &Message("10");														 
							 }
						  }
						  else
						  {
							 $returnval = &Message("11");						   
						  }
					   }
					}
					else
					{
					   $returnval = &Message("9");				   
					}
				 }
				 else
				 {
					$returnval = &Message("12");					  
				 }
		    }
		    elsif ($size eq 1 && $StatusValue ne 0)
		    {
			  $returnval = &Message("7");	
		    }
		    elsif ($StatusValue eq 0)
		    {
			  $returnval = &Message("8");
			  
		    }
		 }	     
	  }
	}
	else
	{
	   $returnval = "invalid from number";	
	}
	
   return ($fromnumber,$returnval);
}


#======================isZenofonUser()=========================
# This function checks the sms sender is valid Zenofon user
#==============================================================
sub isZenofonUser()
{
   #return ($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani);	# For Testing
   my ($fromnumber,$smsbody) = @_;
   my $isValidUser = 0;
   my $error = 0;
   
   my $ok_key	= 0;
   my $duplicate_email =0;
   my $tduplicate_ani = 0;
   my $form_key_clean="";
   my $form_key_int;
   my $keyisemail;
   my $sql="";
   
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
        
   #$t{ok_key}	= 0;
   #$t{duplicate_email} =0;
   #$t{duplicate_ani} = 0; 
	        
   if (($fromnumber ne ""))
   {
   if ($error eq 0)
	  {
		 $fromnumber = &trim($fromnumber);
		 if ($fromnumber eq "")
		 {
			$error=1;
			return (0,$error,"","","","");
		 }		
	  }
	  
	  # check key is email or ANI
	  $fromnumber = substr($fromnumber,0,100);
	  $form_key_clean = clean_str($fromnumber,"._-()[]\@");
	  $form_key_int = clean_int($fromnumber);
	  $keyisemail = (index($form_key_clean,"\@") ne -1) ? 1: 0;   #  $keyisemail=0    => Key is Phone Number,  $keyisemail=1    => Key is Email	
	  
	  if ($error eq 0)
	  {               
		 # ($t{form_key_flag},$t{form_key_e164},$t{form_key_country}) = &multilevel_check_E164_number($t{form_key_int});
		 my ($form_key_flag,$form_key_e164,$tform_key_country) = &multilevel_check_E164_number($form_key_int);
		 
		 if ( ($form_key_flag eq "OK") && ($form_key_int ne "") ) 
		 {
			$sql = "
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
			   $firstrecordid	= $hash{$_}{id};
			   $firstrecordflag	= $hash{$_}{flag};
			   $firstrecordname	= $hash{$_}{name};
			   $firstrecordemail	= $hash{$_}{email};
			   $firstrecordani	= $hash{$_}{ani};
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
			   $service_found	= 1;
			   $service_id		= $firstrecordid;
			   $service_name	= $firstrecordname;
			   $service_email	= $firstrecordemail;
			   $service_ani	    = $firstrecordani;
			   $error 			= 0;						
			   $ok_key          = 1;
			   $isValidUser=1;
			   $error=0;
			   return ($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani);
			}
			else 
			{
			   $isValidUser=0;
			   $error=1;
			   return (0,$error,"","","","");
			}
		 } 
		 else
		 {
			$isValidUser=0;
			$error=1;
			return (0,$error,"","","","");
		 }
	  }
	  else
	  {
		 $isValidUser=0;
		 $error=1;
		 return (0,$error,"","","","");
	  }
   }
   else
   {
	  $error=1;
	  return (0,$error,"","","","");
   }
	return ($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani);
}

#======================sms_client_status()=========================
# Updates the mute or unmute status of a user
#==================================================================

 sub sms_client_status()
 {
	my ($Isvaliduser,$Body,$From) = @_;
	if($Isvaliduser eq 1 && ($Body eq "mute" || $Body eq "unmute" ))
	{	
		$From =~ tr/+/ /;
		$From = &trim($From);
		my @ArryCnt = database_select_as_array("SELECT count(*) AS Cnt FROM SMS_Client WHERE sms_ani = '$From'","Cnt");
		my $count = $ArryCnt[0];
		my $Status="";
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
			my $sql="UPDATE SMS_Client SET sms_status = '$Status' WHERE sms_ani = '$From'";
			database_do($sql);			
		}
		else
		{
			my $sql="INSERT INTO SMS_Client (sms_ani,sms_status) VALUES ($From,'$Status')";			
			database_do($sql);		
		}		
	}	
	
 }
#======================MuteUnmute_status()=========================
# checking the Mute & UnMute status of a user
#==================================================================
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
 sub Message()
 {
   my ($msg) = @_;
   my $rtnmsg = "";
   my $errorStatus=0;
  # my @getcounter = &session($ssid,$msg);
   given ($msg) {
	#SMS content flown from here - Customized text
		 when ('1') { $rtnmsg = "Reply 'mute' to stop receiving SMS from zenofon or Reply 'Unmute' to start receiving SMS from zenofon" }
		 when ('2') { $rtnmsg = ''}
		 when ('3') { $rtnmsg = 'Here after you don’t receive SMS from Zenofon. If you want to receive SMS just text unmute to zenofon' }
		 when ('4') { $rtnmsg = 'Sorry, You can\'t mute, This is not valid Number';$errorStatus=1;}
		 when ('5') { $rtnmsg = 'Sorry, You can\'t unmute, This is not valid Number';$errorStatus=1; }
		 when ('6') { $rtnmsg = 'Sorry, We don\t recognize your cell number';$errorStatus=1; }
		 when ('7') { $rtnmsg = 'Invalid Text Initiate';$errorStatus=1;}
		 when ('8') { $rtnmsg = 'Your current status \'mute\'. If you want to receive SMS just text \'unmute\' to zenofon' ;$errorStatus=1;}
		 when ('9') { $rtnmsg = 'Sorry, We don\'t recognize your cell number';$errorStatus=1; }
		 when ('10') { $rtnmsg = 'Please use +xxxxxxxxxx to talk with number and xxxxxxxx to dial number';$errorStatus=1; }
		 # changed By Yassine to add 95 new DID 53-> 148 
		 when ('11') { $rtnmsg = 'Sorry you Can\'t add new number. You have added maximum number(148) of contacts' ;$errorStatus=1;}
		 when ('12') { $rtnmsg = 'Invalid Format (Please use this format: Name,International Number)';$errorStatus=1; }
		 when ('13') { $rtnmsg = 'Please enter the phone number, or the name of the contact you wish to change the route for.';$errorStatus=1; }
		 when ('14') { $rtnmsg = 'That contact was not found, please re-enter the phone number or the name of the contact you wish to change the route for.';$errorStatus=1;}
		 when ('15') { $rtnmsg = "Please respond with the route number (1, 2, 3, 4, 5, 6, 7) you would like to change to. (ie. route 1, route 2, etc.)"}
		 when ('16') { $rtnmsg = "Please contact customer support at 917-284-9450 for help, or you may control your account online at www.zenofon.com"}
		 when ('17') { $rtnmsg = "ZenoFon texts user:'I’m sorry, I did not understand your response. Please select the route you want by typing one of the following: 'route 1', 'route 2', 'route 3', 'route 4', 'route 5', 'route 6', 'route 7'. Max 5 attempts.'";$errorStatus=1;}
		 default { $rtnmsg = "Select your option \n 1) Mute/Unmute \n 2) Reroute \n 3) Add New Contact" }
	   
	   
   }
   my @getcounter = &errorCounter($errorStatus);
	   
	    if($getcounter[0] eq 5)
		 {
		   $rtnmsg = "Please contact customer support at 917-284-9450 for help, or you may control your account online at www.zenofon.com";
		 }
		 return $rtnmsg;
}
 
#======================addContact()================================
# Adds a new contact into the customer's account
#================================================================== 
 
 sub addContact()
 {
    my ($aservice_id,$fname,$fnumber) = @_;   #  &addContact($service_id,$contactname,$contactnumber);  return ($ok,$name,$number,$activenumber[$index-1]);

    #my $aservice_id;
    #my $fname;
    #my $fnumber;
    my $frslot="Dial using route 1";
    my $fcallback="Play beep beep";
    my $frouteann="Don't choose route during call";
    my $findex_new="Speed number is 1"; 
    my $fcallid="";
    my $fbalanceann="Don't play balance";    
    my $fsave=1;
    my $faction="dst";    
    my $fcarrier="";
    
    my $ok = 1;
    my $index = "";
    #%t = %template_default;
    my $tmy_url	= 'servicetwilio.cgi';
    my $terror	= 0;
    my $terror_number_format	= 0;
    my $terror_number_e164_format 	= 0;
    my $terror_number_skype_format	= 0;
    my $terror_number_no_rate 		= 0;
    my $terror_number_unknown_country = 0;
    my $terror_no_more_index		= 0;
    my $terror_bad_index 				= 0;
    my $tnumber						= "";
    my $tname						= "";
    my $tcallid						= "";
    my $tcarrier						= "";
    my $tcallback                                          = "";
    my $routeann                                          = "";
    my $tbalanceann                                         = "";
    my $tindex 						= "";
    my $tindex_new 					= "";
    my $index_range_low	= 1;
	#change by Yassine to add 95 new DID  53->148 
    my $index_range_hi		= 148;    
    
    # List of active numbers.
	#changed by Yassine 95 new DID 
    my @activenumber = ("(646)434-4612","(646)434-4613","(646)434-4614","(646)434-4615","(646)434-4616","(646)434-4617","(646)434-4618","(646)434-4619","(646)434-4620","(646)434-4621","(646)434-4622","(646)434-4623","(646)434-4624","(646)434-4625","(646)434-4626","(646)434-4627","(646)434-4628","(646)434-4629","(646)434-4630","(646)434-4631","(917)284-9432","(646)873-6314","(646)873-6324","(646)873-6341","(413)749-4735","(646)873-6374","(646)873-6394","(646)873-6913","(646)873-6914","(646)873-6927","(646)873-6928","(646)873-6929","(646)873-6934","(201)204-1821","(201)204-1822","(201)204-1823","(201)204-1824","(201)204-1825","(201)204-1826","(201)204-1827","(201)204-1828","(201)204-1829","(201)204-1830","(201)204-1831","(201)204-1832","(201)204-1833","(201)204-1834","(201)204-1835","(201)204-1836","(201)204-1838","(201)204-1839","(201)204-1840","(201)204-1841","(646)873-6342","(413)749-4734","(413)749-4733","(413)749-4730","(413)749-2684","(413)749-2683","(413)749-2682","(413)749-2681","(413)749-2679","(484)350-4836","(484)350-4835","(484)350-4834","(484)350-4833","(484)350-4832","(484)350-4831","(484)350-4830","(484)350-4829","(484)350-4828","(401)859-3905","(401)859-3904","(401)859-3902","(401)859-3901","(401)859-2901","(401)859-3899","(401)859-2899","(401)859-2898","(401)859-3897","(401)859-2897","(561)692-6931","(561)692-6929","(561)692-6928","(561)692-6927","(561)692-6926","(561)692-6925","(561)692-6924","(561)692-6923","(561)692-6922","(240)389-9723","(240)389-9722","(240)389-9721","(240)389-9718","(240)389-9717","(240)389-9716","(240)389-9715","(240)389-9714","(202)524-3598","(202)524-3596","(202)524-3594","(202)524-3587","(202)524-3576","(202)747-2417","(202)595-9417","(202)747-2416","(202)747-2415","(202)747-2414","(603)835-4192","(603)835-4191","(603)835-4190","(603)835-4189","(603)835-4188","(603)835-4187","(603)835-4186","(603)835-4185","(603)835-4184","(603)835-4183","(703)249-6939","(703)249-6938","(703)249-6937","(703)249-6936","(703)249-6935","(703)249-6934","(703)249-6933","(703)249-6932","(703)249-6931","(703)249-6930","(973)446-5425","(973)446-5424","(973)446-5423","(973)446-5422","(973)446-5421","(973)446-5420","(973)446-5419","(973)446-5418","(973)446-5417","(973)446-5416","(978)364-3955","(978)364-4787","(978)364-4786","(978)364-4654","(978)614-0453","(978)614-0452","(978)614-0451","(978)614-0450","(978)614-0449","(978)614-0448",);
    
    #
    #--------------------------------------------------
    # get index by form or find a free one if new=1
    #--------------------------------------------------
    my $tindex_is_new = 0;
    
    # Save new contact
    my  $formnew=1;
	
    if ($formnew eq 1)
    {
	foreach my $loop ($index_range_low..$index_range_hi) 
	{
	    if (&data_get("service_data",$aservice_id,"dst_".$loop."_number") eq "") {$index = $loop;last;}
	}
	
	if ($index eq "")
	{
	    $terror = 1;
	    $terror_no_more_index = 1;
	    $ok = 0;		
	    return ($ok,"","","");
	}
	$tindex_is_new = 1;
    }
    
    $tindex = $index;
	
    my $index_new = &clean_int(substr($findex_new,0,10));
    if ( ($index_new lt $index_range_low) || ($index_new gt $index_range_hi) || ($index_new eq "") ) 
    {
	$index_new = "";
    }
    $tindex_new = $index_new;	
	
    #
    #--------------------------------------------------
    # try to save
    #--------------------------------------------------
	if ( ($ok eq 1) && ($fsave eq 1) ) 
	{
		my $number	= clean_str(substr($fnumber,0,1024),":-_()+.");
		my $name	= clean_str(substr($fname,0,1024),"-_():<>\@.");
		my $callid	= clean_int(substr($fcallid,0,1024));
		my $carrier= clean_str(substr($fcarrier,0,1024));
		$carrier= (exists($carriers_list{$carrier})) ? $carrier : "";
		my $callback = clean_int(substr($fcallback,0,1024));
		$routeann = clean_int(substr($frouteann,0,1024));
		my $balanceann = clean_int(substr($fbalanceann,0,1024));
		my $rslot	= clean_int(substr($frslot,0,1024));
		$rslot	= (index("|1|2|3|4|5|6|7|8|9|","|$rslot|") eq -1) ? 1 : $rslot;
		#$rslot	= &data_get("service_data",$app{service_id},"dst_".$index."_rslot");
		#		
		# check and format number
		my ($number_status,$number_format,$number_clean) = &multiformat_phone_number_check_user_input($number);
		my $tnumber_status 				= $number_status;
		my $tnumber_raw				= $number;
		my $tnumber_clean 				= $number_clean;
		my $tnumber_format 				= $number_format;
		my $tnumber_format_skype		= ($number_format eq "SKYPE") ? 1 : 0;
		my $tnumber_format_sip			= ($number_format eq "SIP") ? 1 : 0;
		
		if ($number_status ne "OK") 
		{
			$ok = 0;
			$terror = 1;
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
			}
			else 
			{
			    $terror_number_format = 1;
			}
			
			return ($ok,"","","");
		}
		else
		{
			$number = $number_clean;
		}

		#		
		# check rate
		if ($ok eq 1)
		{
			#
			# pega rate_table, baseado no status do servico e slot da extensao
			my $rate_table_id = "";
			my $sql = "select 1,1,service_status.rate_slot_1,service_status.rate_slot_2,service_status.rate_slot_3,service_status.rate_slot_4,service_status.rate_slot_5
			,service_status.rate_slot_6,service_status.rate_slot_7,service_status.rate_slot_8,service_status.rate_slot_9 from service, service_status
			where service.id='$aservice_id' and service.status = service_status.id  and service_status.deleted = 0 ";
			my %hash = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9");
			if ($hash{1}{flag} eq "1") 
			{
				my $user_slot = &data_get("service_data",$aservice_id,"dst_".$index."_rslot") || 1;
				$rate_table_id = $hash{1}{rate_slot_1};
				$rate_table_id = ( ($user_slot eq 1) && ($hash{1}{rate_slot_1} ne "") ) ? $hash{1}{rate_slot_1} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 2) && ($hash{1}{rate_slot_2} ne "") ) ? $hash{1}{rate_slot_2} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 3) && ($hash{1}{rate_slot_3} ne "") ) ? $hash{1}{rate_slot_3} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 4) && ($hash{1}{rate_slot_4} ne "") ) ? $hash{1}{rate_slot_4} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 5) && ($hash{1}{rate_slot_5} ne "") ) ? $hash{1}{rate_slot_5} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 6) && ($hash{1}{rate_slot_6} ne "") ) ? $hash{1}{rate_slot_6} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 7) && ($hash{1}{rate_slot_7} ne "") ) ? $hash{1}{rate_slot_7} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 8) && ($hash{1}{rate_slot_8} ne "") ) ? $hash{1}{rate_slot_8} : $rate_table_id;
				$rate_table_id = ( ($user_slot eq 9) && ($hash{1}{rate_slot_9} ne "") ) ? $hash{1}{rate_slot_9} : $rate_table_id;
			}
			
			#
			# agora tenta pegar rate
			if ($rate_table_id ne "") 
			{
				%hash = &multilevel_rate_table_get($number,$rate_table_id);
				if ($hash{ok_to_use} ne 1)
				{
				    $terror = 1;
				    $terror_number_no_rate = 1;
				    #$ok = 0; #Temp
				}
			}
			else 
			{
			    $terror = 1;
			    $terror_number_no_rate = 1;
			    #$ok = 0; #Temp
			}
		}
		
		#
		# if all ok, lets save data
		if ($ok eq 1) 
		{
			if ( ($index_new ne "") && ($index_new ne $index) )
			{
				my $v1 = &data_get("service_data",$aservice_id,"dst_".$index_new."_callid");
				my $v2 = &data_get("service_data",$aservice_id,"dst_".$index_new."_number");
				my $v3 = &data_get("service_data",$aservice_id,"dst_".$index_new."_name");
				my $v4 = &data_get("service_data",$aservice_id,"dst_".$index_new."_carrier");
				my $v5 = &data_get("service_data",$aservice_id,"dst_".$index_new."_rslot");
				&data_set("service_data",$aservice_id,"dst_".$index_new."_name"		,$name);
				&data_set("service_data",$aservice_id,"dst_".$index_new."_callid"	,$callid);
				&data_set("service_data",$aservice_id,"dst_".$index_new."_number"	,$number);
				&data_set("service_data",$aservice_id,"dst_".$index_new."_carrier"	,$carrier);
				&data_set("service_data",$aservice_id,"dst_".$index_new."_rslot"	,$rslot);
				&data_set("service_data",$aservice_id,"dst_".$index."_name"		,$v3);
				&data_set("service_data",$aservice_id,"dst_".$index."_callid"	,$v1);
				&data_set("service_data",$aservice_id,"dst_".$index."_number"	,$v2);
				&data_set("service_data",$aservice_id,"dst_".$index."_carrier"	,$v4);
				&data_set("service_data",$aservice_id,"dst_".$index."_rslot"	,$v5);
				&data_set("service_data",$aservice_id,"dst_".$index."_callback"        ,$callback);
				&data_set("service_data",$aservice_id,"dst_".$index."_routeann"        ,$routeann);
				&data_set("service_data",$aservice_id,"dst_".$index."_balanceann"        ,$balanceann);	
			}
			else 
			{
				&data_set("service_data",$aservice_id,"dst_".$index."_name"		,$name);
				&data_set("service_data",$aservice_id,"dst_".$index."_callid"	,$callid);
				&data_set("service_data",$aservice_id,"dst_".$index."_number"	,$number);
				&data_set("service_data",$aservice_id,"dst_".$index."_carrier"	,$carrier);
				&data_set("service_data",$aservice_id,"dst_".$index."_rslot"	,$rslot);
				&data_set("service_data",$aservice_id,"dst_".$index."_callback"        ,$callback);
				&data_set("service_data",$aservice_id,"dst_".$index."_routeann"        ,$routeann);
				&data_set("service_data",$aservice_id,"dst_".$index."_balanceann"        ,$balanceann);
			}
			
			return ($ok,$name,$number,$activenumber[$index-1]);
			# save data
			# return to status
			#cgi_redirect("servicetwilio.cgi#dst");
			#exit;
		}
		else
		{
		    $ok=0;
		    return ($ok,"","","");
		}
	}		 
 }

#======================userReroute()===========================
#Reroute the path of the use
#==============================================================
sub userReroute()
{  
	  my ($isValidUser,$StatusValue,$smsbodytext,$fromnumber,$route_to_change) = @_;	  
	  my @isValidUserArray1 = &isZenofonUser(&trim($fromnumber),$smsbodytext); # return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
	  my $isValidUser1=$isValidUserArray1[0];
	  my $service_id=$isValidUserArray1[2];
	  
      
	  
	  my $name= "";
	  my $value = "";
	  my $index="";	 
	  my $count=0;
	  my $returnval="";
	  my $sql = "";
	  my $sel = "";
	  my $dst;
	  my $getname;
	  my $finalval;
	  my $dial_number;
	  my $dublicateindex;
	  my $flag = 0 ;	  
      my $cnt="";
	  
	  #reroute status value
	  #my @rerouteStatusArray = database_select_as_array("SELECT sms_status_value FROM sms_status","sms_status_value");
	  #my $reroutestatusvalue = $rerouteStatusArray [0];
	  my $reroutestatusvalue =&getSMSStatus(2,$fromnumber);
	  
	  $fromnumber =~ tr/+/ /;
	  my $drh = DBI->install_driver("mysql");	  
	  my $dsn = "DBI:mysql:database=multilevel;host=127.0.0.1:3306";	    
	  my $dbh = DBI->connect($dsn,"root","root");
	
	  my $sth = $dbh->prepare("SELECT target,name,value FROM service_data WHERE value = '$smsbodytext' and target = $service_id");
      $sth->execute();
	  
	  #changed by Yassine 95 new DID 
	  my @activenumber   = ("(646)434-4612","(646)434-4613","(646)434-4614","(646)434-4615","(646)434-4616","(646)434-4617","(646)434-4618","(646)434-4619","(646)434-4620","(646)434-4621","(646)434-4622","(646)434-4623","(646)434-4624","(646)434-4625","(646)434-4626","(646)434-4627","(646)434-4628","(646)434-4629","(646)434-4630","(646)434-4631","(917)284-9432","(646)873-6314","(646)873-6324","(646)873-6341","(413)749-4735","(646)873-6374","(646)873-6394","(646)873-6913","(646)873-6914","(646)873-6927","(646)873-6928","(646)873-6929","(646)873-6934","(201)204-1821","(201)204-1822","(201)204-1823","(201)204-1824","(201)204-1825","(201)204-1826","(201)204-1827","(201)204-1828","(201)204-1829","(201)204-1830","(201)204-1831","(201)204-1832","(201)204-1833","(201)204-1834","(201)204-1835","(201)204-1836","(201)204-1838","(201)204-1839","(201)204-1840","(201)204-1841","(646)873-6342","(413)749-4734","(413)749-4733","(413)749-4730","(413)749-2684","(413)749-2683","(413)749-2682","(413)749-2681","(413)749-2679","(484)350-4836","(484)350-4835","(484)350-4834","(484)350-4833","(484)350-4832","(484)350-4831","(484)350-4830","(484)350-4829","(484)350-4828","(401)859-3905","(401)859-3904","(401)859-3902","(401)859-3901","(401)859-2901","(401)859-3899","(401)859-2899","(401)859-2898","(401)859-3897","(401)859-2897","(561)692-6931","(561)692-6929","(561)692-6928","(561)692-6927","(561)692-6926","(561)692-6925","(561)692-6924","(561)692-6923","(561)692-6922","(240)389-9723","(240)389-9722","(240)389-9721","(240)389-9718","(240)389-9717","(240)389-9716","(240)389-9715","(240)389-9714","(202)524-3598","(202)524-3596","(202)524-3594","(202)524-3587","(202)524-3576","(202)747-2417","(202)595-9417","(202)747-2416","(202)747-2415","(202)747-2414","(603)835-4192","(603)835-4191","(603)835-4190","(603)835-4189","(603)835-4188","(603)835-4187","(603)835-4186","(603)835-4185","(603)835-4184","(603)835-4183","(703)249-6939","(703)249-6938","(703)249-6937","(703)249-6936","(703)249-6935","(703)249-6934","(703)249-6933","(703)249-6932","(703)249-6931","(703)249-6930","(973)446-5425","(973)446-5424","(973)446-5423","(973)446-5422","(973)446-5421","(973)446-5420","(973)446-5419","(973)446-5418","(973)446-5417","(973)446-5416","(978)364-3955","(978)364-4787","(978)364-4786","(978)364-4654","(978)614-0453","(978)614-0452","(978)614-0451","(978)614-0450","(978)614-0449","(978)614-0448",);
	  my $size = @activenumber;	  	
	     
	  while (my @row = $sth->fetchrow_array()){        	
		 my @indexval = split(/_/,$row[1]);
		 $dst = $indexval[0];
		 $index = $indexval[1];
		 $getname = $indexval[2];
		 $finalval =$row[1];
		 $dial_number = $activenumber[$index];
		 $dial_number =~ s/[^0-9]*//g;
		 $count++;
		 $name .=  $count.")".$row[2]." - ".$activenumber[$index]."\n" ;
	  }	  
	  $name = "We found few duplicate names \n".$name."Please reply with dial number to identify the contact.";  
	  
	  for ( my $i=0; $i<$size; $i++) 
	  {
		 my $a = $activenumber[$i];		 
		 if($smsbodytext =~ m/^(\((\d{0,3})\)(\d{0,3})(\-)(\d{0,4}))/)
		 {
		   if($a eq $smsbodytext)
			{
			   $dublicateindex = $i+1;
			   $flag = 1;
			}
		 }
		 else
		 {
			$a =~ s/[^0-9]*//g;
			if($a eq $smsbodytext)
			{
			   $dublicateindex = $i+1;
			   $flag = 1;
			}
		 }
	  }
	  
	  if($flag eq 1)
	  {
		 $index = $dublicateindex;		
		 $dial_number = $activenumber[$index];
		 $dial_number =~ s/[^0-9]*//g;
		 $count = 1;
	  } 

	  my $_name = &data_get("service_data",$service_id,"dst_".$index."_name");
	  my $_number = &data_get("service_data",$service_id,"dst_".$index."_number");
	  my $_rslot = &data_get("service_data",$service_id,"dst_".$index."_rslot");
  
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
			      $sel="select value from service_data where target = $service_id and name = 'dst_".$index."_rslot'";
			      my @Status = database_select_as_array($sel,"value");
	              my $Getrslot = $Status[0];
				  my $delsql= "select count(*) AS Cnt from sms_route_temp where sms_target = $service_id and sms_name = 'dst_".$index."_rslot'";
				  my @delCnt = database_select_as_array($delsql,"Cnt");
		          my $count = $delCnt[0];		  
				 
				  if($count gt 0)
				  {
					 my $deleteroute = "DELETE FROM sms_route_temp where sms_target = $service_id and sms_name = 'dst_".$index."_rslot'";
					 database_do($deleteroute);
				  }			  
				  my $datetime=&getDatetime();
				  if(defined($route_to_change)){
					 
					 $sql= "INSERT INTO sms_route_temp(sms_target,sms_name,sms_value,sms_ani,sms_dial_number,sms_contact_name,sms_contact_number,sms_date_time,sms_next_route,sms_confirmation) values ('$service_id','dst_".$index."_rslot','$Getrslot','".&trim($fromnumber)."','$dial_number','$_name','$_number','$datetime','$route_to_change','0') ";
				  
				  }else{
					 
					 $sql= "INSERT INTO sms_route_temp(sms_target,sms_name,sms_value,sms_ani,sms_dial_number,sms_contact_name,sms_contact_number,sms_date_time,sms_confirmation) values ('$service_id','dst_".$index."_rslot','$Getrslot','".&trim($fromnumber)."','$dial_number','$_name','$_number','$datetime','0') ";
				  }
				
				  
				  database_do($sql);				 
			      $returnval = &Message(15);
			   }
			   else
			   {
			     $returnval = $name;
			   }
			}
			elsif( lc(&trim($smsbodytext)) =~ m/^(\w[a-zA-Z]+)+\s?(\d)$/ || lc(&trim($smsbodytext)) eq "no")
			{
			 
			if(lc(&trim($smsbodytext)) =~ m/^(\w[route]+)+\s?(\d)$/ || lc(&trim($smsbodytext)) eq "no")
			{
			if($reroutestatusvalue gt 0)
			   {
				   my $routetxt ="";
				   my $routeval="";
				 if(lc(&trim($smsbodytext)) =~ m/^(\w[route]+)+\s?(\d)$/){
				  
					 my @reroute = split(/\s?(\d+)$/ , $smsbodytext); #split reoute and value eg: reroute 1  
					  $routetxt = $reroute[0];
					  $routeval = $reroute[1];
				 }
			      
				     $routeval =~ /^(\d)/;
				  my $finalrouteval = $1;
				  my $returnval1 = $smsbodytext;			
				  
				  
				   my $_rslot = &data_get("service_data",$service_id,"dst_".$index."_rslot");
				  
				 $sel = "select 1,1,1,sms_route_id,sms_name,sms_value,sms_dial_number,sms_contact_name,sms_contact_number,sms_next_route from sms_route_temp where sms_ani = ".&trim($fromnumber)." order by sms_route_id DESC limit 0,1 ";
				  my %hashval = &database_select_as_hash($sel,"1,1,sms_route_id,sms_name,sms_value,sms_dial_number,sms_contact_name,sms_contact_number,sms_next_route");
				  my $sms_id = $hashval{1}{sms_route_id};
				  my $rslot_name = $hashval{1}{sms_name};
				  my $rsloat_value = $hashval{1}{sms_value};
				  my $dailnumber = $hashval{1}{sms_dial_number};
				  my $contact_name = $hashval{1}{sms_contact_name};
				  my $contact_no = $hashval{1}{sms_contact_number};
				  my $route_next=$hashval{1}{sms_next_route};
				 
				
				  if(lc(&trim($smsbodytext)) eq  "no"){		
					  
					  $routetxt = "route";
					 $finalrouteval=$routeval= $route_next; 
					  
				 }
				
				  
				  $sql="update service_data set value = $finalrouteval where target = $service_id and name='$rslot_name'";				  
				  database_do($sql);
				  
				   $sql="update sms_route_temp set sms_confirmation = 1 where sms_route_id = $sms_id ";				  
				  database_do($sql);
				  
				  $returnval = "Thank you, we have changed you over to route [$finalrouteval] for any calls to [$contact_no]/[$contact_name].";
                  &getSMSStatus(1,$fromnumber);
				  
			   }
			   else
			   {
				  $returnval = &Message();			  
			   }
			}else{
			   $returnval = &Message(17);	
			}
			}
			else
			{
			   $returnval = &Message(14);			  
			}
		 }
		 else
		 {
			$returnval  = "";
		 }
	  }
	  else
	  {
	  $count = 0;
	  $returnval = &Message(8);	 
	  }
   }  
   return ($count,$returnval);
}
#======================getSessionObj()=========================
#Session creation for the error counter
#==============================================================
sub getSessionObj(){
   
   my $sid=$cgi->cookie('ID');
   my $session='';
  
   
   if(!defined($sid)){
	 
	  $session=new CGI::Session();
	  $sid=$session->id;
	  
	  my $cookie=$cgi->cookie(ID => $sid);	  
	  		
	  print $cgi->header(-cookie =>$cookie);
   }else{
	  
	   		
		$session=new CGI::Session(undef,$sid);
   }
   return $session;
}
#======================errorCounter()========================
#Increments the session's error counter
#==============================================================
sub errorCounter(){
   
   my ($errid) = @_;
   
  
   my $session=&getSessionObj;
   
  
   if($errid eq 0){	
	
		#$counter=0;	
		#$session->param("Counter",$counter);
		$session->clear(["error_counter"]);
		
	}else{
		$counter=$session->param("error_counter");		
		$counter++;
		
		
		if($counter ge 5){			
			$session->param("error_counter",0);		
		}else{
		 $session->param("error_counter",$counter);
		}
		
		
	}
	return ($counter);
}
#======================sendSMS_Twilio()========================
#This function rerouteLastCall
#==============================================================
sub rerouteLastCall()
{
      
	  my ($fromnumber,$smsbodytext) = @_;
	   
	  my @isValidUserArray1 = &isZenofonUser(&trim($fromnumber),$smsbodytext); # return($isValidUser,$error,$service_id,$service_name,$service_email,$service_ani)
	  my $isValidUser1=$isValidUserArray1[0];
	  my $service_id=$isValidUserArray1[2];
	   
      my @status = &MuteUnmute_status(&trim($fromnumber));
      my $StatusValue = $status[0];
	  
	  my $returnval='';
	  if ($StatusValue eq 1){  
	 my $sql="";
		
	  # set sms_status value for from number
	  
		 &getSMSStatus(0,$fromnumber);
      
      $sql = "select 1,1,1,calls_log.id,calls_log.datetime_start,calls_log.datetime_stop,calls_log.ani,calls_log.did,calls_log.dst,calls_log.service_id,calls_log.rate_slot,calls.seconds from calls_log,calls where (calls_log.billing_id=calls.id)and calls_log.ani = '$fromnumber' and calls.seconds >11 and calls.seconds<60 order by id desc limit 1";
   
      
	  my %hash = database_select_as_hash($sql,"1,1,id,datetime_start,datetime_stop,ani,did,dst,service_id,rate_slot,seconds");
      
   if(%hash > 0){
	  
	  my $call_log_id = $hash{1}{id};
	  my $datetime_start = $hash{1}{'datetime_start'};
      my $datetime_stop = $hash{1}{datetime_stop};
	  my $fromnumber = $hash{1}{ani};
	  my $dialnumber = $hash{1}{did};
	  my $tonumber = $hash{1}{dst};
	  my $rate_slot = $hash{1}{rate_slot};
	  my $seconds = $hash{1}{seconds};
   
	  my $incomplete_erorr_counter=&getIncomplete_counter($fromnumber,$tonumber);
	
	  
	  $returnval=&userReroute($isValidUser1,$StatusValue,$tonumber,$fromnumber);	  
	  &errorCounter(1);
	  
	  if($incomplete_erorr_counter>=5){
		 
		 $returnval=&Message(16);

	  }elsif(($incomplete_erorr_counter <= 1) && ($rate_slot ne 4)){
		 
		 $returnval="Your last call was incomplete, if you would like to try calling [$tonumber] using route 4, type 'route 4'";
	  }elsif(($incomplete_erorr_counter <= 1) && ($rate_slot eq 4)){
	  
		 $returnval="Your last call was incomplete, if you would like to try calling [$tonumber] using route 7, type 'route 7'";
	  }else{
		 
		$returnval="Your call to [$tonumber] was incomplete using [route $rate_slot]. If you would like to use a different route, please select the route you want by typing one of the following: 'route 1', 'route 2', 'route 3', 'route 4', 'route 5', 'route 6', 'route 7'";
	  }

	  }else{
		 $returnval="No Incomplete Calls Found!";
		 
	  }
	  }else{#mute message
		 $returnval=&Message(8);
	  }
	
	  return $returnval;
}
#======================getIncomplete_counter()========================
#Gets incomplete call counter
#=====================================================================
sub getIncomplete_counter(){
   
   (my $fromnumber,my $tonumber)=@_;
   my $today=&getDatetime();#"2012-05-12 12:05:56";
	my $prev_time=&getDatetime(5);#"2012-05-12 11:50:25";
	
	  my @StatusCnt = database_select_as_array("SELECT count(*) AS count  from calls_log,calls where calls_log.ani = '$fromnumber' and calls.seconds = 50 and calls_log.dst = '$tonumber' and datetime_stop >='$prev_time' and datetime_stop <='$today'","count");
	  my $incomplete_erorr_counter=$StatusCnt[0];
	  
	  return $incomplete_erorr_counter;
   
}
#======================getDatetime()===========================
#Returns the time difference
#==============================================================
sub getDatetime(){
 
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
#======================getLastrequest()=================================
#This function checks the recent SMS functionality initiated by the user.
#=======================================================================
sub getLastrequest(){
   
   my ($fromnumber)=@_;
   my %sms=();
  
   my $sql = "select 1,1,sms_route_id,sms_target,sms_name,sms_value,sms_ani,sms_dial_number,sms_contact_name,sms_contact_number,sms_date_time,sms_next_route from sms_route_temp where  sms_ani='$fromnumber' order by sms_route_id desc limit 1";
   my %hash = &database_select_as_hash($sql,"1,sms_route_id,sms_target,sms_name,sms_value,sms_ani,sms_dial_number,sms_contact_name,sms_contact_number,sms_date_time,sms_next_route");
   
   $sms{sms_route_id}=$hash{1}{sms_route_id};
   $sms{sms_target}=$hash{1}{sms_target};
   $sms{sms_name}=$hash{1}{sms_name};
   $sms{sms_value}=$hash{1}{sms_value};
   $sms{sms_ani}=$hash{1}{sms_ani};
   $sms{sms_dial_number}=$hash{1}{sms_dial_number};
   $sms{sms_contact_name}=$hash{1}{sms_contact_name};
   $sms{sms_contact_number}=$hash{1}{sms_contact_number};
   $sms{sms_date_time}=$hash{1}{sms_date_time};
   $sms{sms_next_route}=$hash{1}{sms_next_route};
   
   return %sms;
}
#======================getSMSStatus()===================================
#Maintains the command request from the user in the table(sms_route_temp)
#=======================================================================
sub getSMSStatus(){
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
#return 1;
