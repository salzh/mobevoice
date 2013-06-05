#!/usr/bin/perl
print "Content-type:text/html\n\n";
#use CGI::Carp qw(fatalsToBrowser); # To Debug on Browsers
require "include.cgi";
use DBI;
use CGI;
use POSIX;
#use WWW::Twilio::API;
#
##===========Twilio Account details=======
#my $twilioaccount_sid = 'ACc0d95bda6c7bed59a113a9bd5c9ce956';
#my $twilioauth_token  = '474e7c48ead04865d19d0be32165f2c0';
#my $twilio_from_number  = '+19173384580';
##========================================

#if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_view_reports") ne 1) {adm_error("no permission"); exit;}
use Data::Dumper;

if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
$cgi = new CGI;

#get 
my $datetime="";
my $today="";
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst);
   
($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);
$year = $year+1900;
$mon=$mon+1;
$datetime = sprintf("%02d/%02d %02d:%02d", $mon, $mday, $hour, $min);

#$datetime = "$mon/$mday  $hour:$min";

if(defined($form{'call_id'}) && defined($form{'rate_value'}) && defined($form{'refund_action'}) && defined($form{'refund_amount'})){
	

	my $sth = "";
	my $call_id=$form{'call_id'};
	my $rate_value = $form{'rate_value'};
	my $refund_action=$form{'refund_action'};
	my $refund_amount=$form{'refund_amount'};
	  
	  if ($refund_action eq "Partial Refund")
	  {
		if ($refund_amount =~ /^[0-9]+(\.[0-9]{1,2})?$/)
		{
		    if ($refund_amount lt $rate_value)
	        {
				
	        my $sth = $database->prepare("update sms_call_refund set refund_response_time = now(),refund_status = '$refund_action',refund_amount = '$refund_amount' where call_id='$call_id'");
	        $sth->execute();
	    
	        $sth = $database->prepare("select * from calls,sms_call_refund where (calls.id = sms_call_refund.call_id) and sms_call_refund.call_id='$call_id'");
	        $sth->execute();
	        my $ref = $sth->fetchrow_hashref();
	        my $id = "$ref->{id}";
	        my $date = "$ref->{date}";
	        my $ani = "$ref->{ani}";
	        my $did = "$ref->{did}";
	        my $dst = "$ref->{dst}";
	        my $service_id = "$ref->{service_id}";
	        my $balance_before = "$ref->{balance_before}";
	        my $rate_val = "$ref->{rate_value}";
	        my $refund_status = "$ref->{refund_status}";
	        my $refund_amt = "$ref->{refund_amount}";
	      
	        $sth = $database->prepare("update service set balance = balance+$refund_amt where id='$service_id'");
	        $sth->execute();
		  
		    #Send refund sms to user via twilio
		    my %hash = &database_select_as_hash("select 1,1,1,balance,email,name from service where id='$service_id'","1,1,balance,email,name");
		    my $current_balance = $hash{1}{balance};
		    my $email_id = $hash{1}{email};
		    my $name = $hash{1}{name};
			
		    if ($current_balance =~ m/((\d+)\.(\d{2}))/)
            {
            $current_balance = $1;
            }
			
			$dst = &format_E164_number($dst,"E164");
			
			my $body =&Message('REFUND_APPROVAL_INFO',$ani);
			$body =~ s/xxxx/$refund_amt/i;
			$body =~ s/xxxxx/$dst/i;
			$body =~ s/xxxxxx/$datetime/i;
			$body =~ s/xxxxxxx/$current_balance/i;
			#my $body = "We have Refunded \$$refund_amt for your call to $dst on $datetime to your Zenofon account. Your current balance is \$$current_balance.";
		  
			
			#call twilio subroutine
			&sendSMS_Twilio($ani,"$body");
			  
				#Send email for response of call refund 
				if(keys(%hash) > 0){				 
				#Call Refund response message to user email 
					my %email=();
					$email{'to'}=$hash{1}{email};
					$email{'from'}= "support\@zenofon.com";
					$email{template}			  = "response.call.refund";
					$email{dic}{first_name}       = ($hash{1}{name} eq "")?'Customer': $hash{1}{name};
					$email{dic}{body}             = $body;
					&multilevel_send_email(%email);
				   
				}
				print "success";
		    }
			else
			{
				print "Refund amount value should not be more than call charge";
			}
		}
		else
		{
			print "Please enter numeric values only";
		}
	  }
	  elsif ($refund_action eq "Full Refund")
	  {
	      
		if ($refund_amount =~ /^[0-9]+(\.[0-9]{1,2})?$/)
		{
		    
		   if ($refund_amount eq $rate_value)
	       {
			
		    my $sth = $database->prepare("update sms_call_refund set refund_response_time = now(),refund_status = '$refund_action',refund_amount = '$rate_value' where call_id='$call_id'");
	        $sth->execute();
	      
		    
	        $sth = $database->prepare("select * from calls,sms_call_refund where (calls.id = sms_call_refund.call_id) and sms_call_refund.call_id='$call_id'");
	        $sth->execute();
	        my $ref = $sth->fetchrow_hashref();
	        my $id = "$ref->{id}";
	        my $date = "$ref->{date}";
	        my $ani = "$ref->{ani}";
	        my $did = "$ref->{did}";
	        my $dst = "$ref->{dst}";
	        my $service_id = "$ref->{service_id}";
	        my $balance_before = "$ref->{balance_before}";
	        my $rate_val = "$ref->{rate_value}";
	        my $refund_status = "$ref->{refund_status}";
	        my $refund_amt = "$ref->{refund_amount}";
		  	      
		    $sth = $database->prepare("update service set balance = balance+$refund_amt where id='$service_id'");
	        $sth->execute();
		    
		    #Send refund sms to user via twilio
		    my %hash = &database_select_as_hash("select 1,1,1,balance,email,name from service where id='$service_id'","1,1,balance,email,name");
	        my $current_balance = $hash{1}{balance};
		    my $email_id = $hash{1}{email};
		    my $name = $hash{1}{name};
			
			
			if ($current_balance =~ m/((\d+)\.(\d{2}))/)
            {
            $current_balance = $1;
            }
			
			$dst = &format_E164_number($dst,"E164");
			
			my $body =&Message('REFUND_APPROVAL_INFO',$ani);
			$body =~ s/xxxx/$refund_amt/i;
			$body =~ s/xxxxx/$dst/i;
			$body =~ s/xxxxxx/$datetime/i;
			$body =~ s/xxxxxxx/$current_balance/i;
			
		    #my $body = "We have Refunded \$$refund_amt for your call to $dst on $datetime to your Zenofon account. Your current balance is \$$current_balance.";
				
				
				#call twilio subroutine
				&sendSMS_Twilio($ani,"$body");
			  
			    #Send email for response of call refund 
				if(keys(%hash) > 0){				 
				#Call Refund response message to user email 
					my %email=();
					$email{'to'}=$hash{1}{email};
					$email{'from'}= "support\@zenofon.com";
					$email{template}			  = "response.call.refund";
					$email{dic}{first_name}       = ($hash{1}{name} eq "")?'Customer': $hash{1}{name};
					$email{dic}{body}             = $body; 
					&multilevel_send_email(%email);
				
				}
				  print "success";
		    }
		    else
		    {
			  print "Refund amount must be equal to call charge";
		    }
		   
		}
		else
		{
			print "Please enter numeric values only";
		}
		  	  
	  }
	  elsif ($refund_action eq "Decline")
	  {
		
		 if ($refund_amount =~ /^[0-9]+(\.[0-9]{1,2})?$/)
		 {
		    
		   if ($refund_amount eq 0)
	       {
			
		    my $sth = $database->prepare("update sms_call_refund set refund_response_time = now(),refund_status = '$refund_action',refund_amount = '$refund_amount' where call_id='$call_id'");
	        $sth->execute();
	        
	        $sth = $database->prepare("select * from calls,sms_call_refund where (calls.id = sms_call_refund.call_id) and sms_call_refund.call_id='$call_id'");
	        $sth->execute();
	        my $ref = $sth->fetchrow_hashref();
	        my $id = "$ref->{id}";
	        my $date = "$ref->{date}";
	        my $ani = "$ref->{ani}";
	        my $did = "$ref->{did}";
	        my $dst = "$ref->{dst}";
	        my $service_id = "$ref->{service_id}";
	        my $balance_before = "$ref->{balance_before}";
	        my $rate_val = "$ref->{rate_value}";
	        my $refund_status = "$ref->{refund_status}";
	        my $refund_amt = "$ref->{refund_amount}";
		  
			my %hash = &database_select_as_hash("select 1,1,1,balance,email,name from service where id='$service_id'","1,1,balance,email,name");
			my $current_balance = $hash{1}{balance};
			my $email_id = $hash{1}{email};
			my $name = $hash{1}{name};
			
			if ($rate_value =~ m/((\d+)\.(\d{2}))/)
            {
            $rate_value = $1;
            }
			
			$dst = &format_E164_number($dst,"E164");
			#Send refund sms to user via twilio
			
			my $body =&Message('REFUND_DECLINE_INFO',$ani);
			$body =~ s/xxxx/$rate_value/i;
			$body =~ s/xxxxx/$dst/i;
			$body =~ s/xxxxxx/$datetime/i;
			
		   
			        #call twilio subroutine
		            &sendSMS_Twilio($ani,"$body");
		            
					#Send email for response of call refund 
					if(keys(%hash) > 0)
					{				 
					#Call Refund response message to user email  
						my %email=();
						$email{'to'}      =$hash{1}{email};
						$email{'from'}    = "support\@zenofon.com";
						$email{template}	      = "response.call.refund";
						$email{dic}{first_name}   = ($hash{1}{name} eq "")?'Customer': $hash{1}{name};
						$email{dic}{body}         = $body;
						&multilevel_send_email(%email);	
						
					}
					print "success";
		    }
		    else
		    {
			print "Please enter refund amount as '0'.";
		    }
		  
		}
		else
		{
			print "Please enter numeric values only";
		}
	  }
	
}else{
	print "nothing";
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

	
