#!/usr/bin/perl
use CGI;
use WWW::Twilio::API;
use CGI::Session;

# Twilio Account details
my $twilioaccount_sid = 'ACc0d95bda6c7bed59a113a9bd5c9ce956';
my $twilioauth_token  = '474e7c48ead04865d19d0be32165f2c0';
my $twilio_from_number  = '+19173384580';


#Twilio Receive SMS Fileds
my $AccountSid  = "";
my $Body  =   "";
my $ToZip  =   "";
my $FromState  =   "";
my $ToCity  =   "";
my $SmsSid  =   "";
my $ToState  =   "";
my $To  =   "";
my $ToCountry  =   "";
my $FromCountry  =   "";
my $SmsMessageSid  =   "";
my $ApiVersion  =   "";
my $FromCity  =   "";
my $SmsStatus  =   "";
my $From  =   "";
my $FromZip  =   "";

#Get the Twilio Receive SMS details
my $q=CGI::Vars();
$AccountSid = $q-> {AccountSid};
$Body = $q-> {Body};
$ToZip = $q-> {ToZip};
$FromState = $q-> {FromState};
$ToCity = $q-> {ToCity};
$SmsSid = $q-> {SmsSid};
$ToState = $q-> {ToState};
$To = $q-> {To};
$ToCountry = $q-> {ToCountry};
$FromCountry = $q-> {FromCountry};
$SmsMessageSid = $q-> {SmsMessageSid};
$ApiVersion = $q-> {ApiVersion};
$FromCity = $q-> {FromCity};
$SmsStatus = $q-> {SmsStatus};
$From = $q-> {From};
$FromZip = $q-> {FromZip};

$cgi=new CGI;

$ssid=$cgi->cookie('ID');
$counter=0;


my @getsession=&session($ssid,$Body);

&sendSMS_Twilio($From,$getsession[0]);	



sub session()
{
	my ($ssid,$Body) = @_;
	
	if($ssid eq ""){
		
		$session=new CGI::Session();
		$sid=$session->id;
		$cookie=$cgi->cookie(ID => $sid);	
		
		$session->param("Counter",$counter);
		
		print $cgi->header(-cookie =>$cookie);
		
		
	}else{
		
		print "Content-type:text/html; charst=iso-8859-1\n\n";
		
		$ssid=$cgi->cookie('ID');
		$session=new CGI::Session(undef,$ssid);
	
		
	}
	
	if($Body eq "mani"){
		
		print "Yes";
		$counter=0;	
		$session->param("Counter",$counter);
		
	}else{
		$counter=$session->param("Counter");
		
		$counter++;
		
		if($counter ge 5){
			
			print "Exceed maximim Limit";
			$counter=0;
			
		}else{
						
			
		}
		
		$session->param("Counter",$counter);
	}
	return ($counter);
}
#This function sends an sms to mobile numbers using Twilio API
sub sendSMS_Twilio()
{    
    #local($tonumber,$smsbody) = @_;
    my ($tonumber,$smsbody) = @_;
    
    ## usage: examples.pl account_sid authtoken action parameters (see examples)
    my $account_sid = 'ACc0d95bda6c7bed59a113a9bd5c9ce956';
    my $auth_token  = '474e7c48ead04865d19d0be32165f2c0';
    my $action      ='SMS' ;
    my $twilio = new WWW::Twilio::API( AccountSid => $twilioaccount_sid,
                                   AuthToken  => $twilioauth_token, );
    if( $action eq 'SMS' )
    {
        my $response = $twilio->POST('SMS/Messages',
                                     #From => '+19173384580',
				    From => $twilio_from_number,
                                    To   =>$tonumber,
                                    Body =>$smsbody);
        $response->{content};	
    }
    else
    {
        #print "Unknown action.\n";
    }           
}


