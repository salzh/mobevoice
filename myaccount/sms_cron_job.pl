#!/usr/bin/perl

require "/usr/local/multilevel/www/include.cgi";



my $dbh = DBI->connect($database_dsn,$database_user,$database_password);


#---------------------------------------------------------------
# Sending invitation afer 24 hrs
#---------------------------------------------------------------

		$sql= "SELECT ani,dst,id,now(),name
				from service_signin
				where TIMESTAMPDIFF(hour,date_start,now()) >24
				and TIMESTAMPDIFF(hour,date_start,now()) <48  and sms_status is null and service_id is null group by ani order by id desc";
				
		 my $sth = $dbh->prepare($sql);
		$sth->execute();
		
		 while (my @row = $sth->fetchrow_array()){
			my $ani=$row[0];
			my $referrer=$row[1];
			my $signin_id=$row[2];
			my $now=$row[3];
			my $name=$row[4];
			
			my @friend_info =&isZenofonUser($ani);
			
			if($friend_info[0] eq 0) {
				my @referrer_info =&isZenofonUser($referrer);
				my $referrer_name=$referrer_info[3];
				my $set_message = &Message('REFER_INVITATION_24H',$ani);
				$set_message =~ s/xxxx/$name/i;
				$set_message =~ s/xxxxx/$referrer_name/i;
				
			
				&sendSMS_Twilio($ani,$set_message);
				&sms_log($ani,$set_message,"",'Sent');
				
				
				my $res = $dbh->prepare("update service_signin set sms_status=1 where ani='$ani'");
				$res->execute();
			}
		 }

#---------------------------------------------------------		 
# Sending invitation afer 48 hrs
#---------------------------------------------------------

		$sql= "SELECT distinct ani,dst,id,now(),name from service_signin where (TIMESTAMPDIFF(hour,date_start,now()) >48 and TIMESTAMPDIFF(hour,date_start,now()) <96)  and (sms_status is null or sms_status=1)  and service_id is null group by ani order by id desc";
				
		$sth = $dbh->prepare($sql);
		$sth->execute();
		
		 while (my @row = $sth->fetchrow_array()){
			my $ani=$row[0];
			my $referrer=$row[1];
			my $signin_id=$row[2];
			my $now=$row[3];
			my $name=$row[4];
			
			my @friend_info =&isZenofonUser($ani);
			
			if($friend_info[0] eq 0) {
				my @referrer_info =&isZenofonUser($referrer);
				$name = substr($name ,0,17);
				my $referrer_name=$referrer_info[3];
				$referrer_name = substr($referrer_name ,0,17);
				
				my $set_message = &Message('REFER_INVITATION_48H',$ani);
				$set_message =~ s/xxxx/$name/i;
				$set_message =~ s/xxxxx/$referrer_name/i;
				
   				&sms_log($ani,$set_message,"",'Sent');
				&sendSMS_Twilio($ani,$set_message);
				
				my $res = $dbh->prepare("update service_signin set sms_status=2  where ani='$ani'");
				$res->execute();
				
		
			}
		 }
		 
#------------------------------------------------------
# Sending invitation afer 10 days
#------------------------------------------------------

		$sql= "SELECT distinct ani,dst,id,now(),name from service_signin where (TIMESTAMPDIFF(hour,date_start,now()) >240 and TIMESTAMPDIFF(hour,date_start,now()) <264)  and ( sms_status is null or sms_status < 10)  and service_id is null group by ani order by id desc";
				
		$sth = $dbh->prepare($sql);
		$sth->execute();
		
		 while (my @row = $sth->fetchrow_array()){
			my $ani=$row[0];
			my $referrer=$row[1];
			my $signin_id=$row[2];
			my $now=$row[3];
			my $name=$row[4];
			
			my @friend_info =&isZenofonUser($ani);
			
			if($friend_info[0] eq 0) {
				my @referrer_info =&isZenofonUser($referrer);
				my $referrer_name=$referrer_info[3];
				
				my $set_message = &Message('REFER_INVITATION_10D',$ani);
				$set_message =~ s/xxxx/$name/i;
				$set_message =~ s/xxxxx/$referrer_name/i;
				
				#my $set_message ="Hi $name, your friend $referrer_name said you may want to join Zenofon to make the cheapest long distance calls. Simply reply with 'yes' to join.";
			    &sms_log($ani,$set_message,"",'Sent');
				&sendSMS_Twilio($ani,$set_message);
				
				my $res = $dbh->prepare("update service_signin set sms_status=10  where ani='$ani'");
				$res->execute();
		
			}
		 }
#--------------------------------------------------	 
# Sending invitation afer 11 days
#--------------------------------------------------

		$sql= "SELECT distinct ani,dst,id,now(),name from service_signin where (TIMESTAMPDIFF(hour,date_start,now()) > 264 && TIMESTAMPDIFF(hour,date_start,now()) <288 )  and ( sms_status is null or sms_status < 11)  and service_id is null group by ani order by id desc";
				
		$sth = $dbh->prepare($sql);
		$sth->execute();
		
		 while (my @row = $sth->fetchrow_array()){
			my $ani=$row[0];
			my $referrer=$row[1];
			my $signin_id=$row[2];
			my $now=$row[3];
			my $name=$row[4];
			
			#chack user and message status is unmute
			
			my @user_info =&isZenofonUser($referrer);
			my @status = &MuteUnmute_status($referrer);
			my $StatusValue = $status[0];
			
			if($user_info[0] eq 1 && $StatusValue eq 1) {
				my @referrer_info =&isZenofonUser($referrer);
				my $referrer_name=$referrer_info[3];
				
				my $set_message =&Message('REFER_NOT_JOINED_11D');
			    $set_message =~ s/xxxx/$referrer_name/i;
				 $set_message =~ s/xxxxx/$name/i;
				&sms_log($referrer,$set_message,"",'Sent');
			   
				&sendSMS_Twilio($referrer,$set_message);
				
				my $res = $dbh->prepare("update service_signin set sms_status=11  where ani='$ani'");
				$res->execute();
		
			}
		 }		 
		 
		 
	
#--------------------------------------------------------		
   # For Low balance remainder added by zenofon SMS Team
#---------------------------------------------------------



		$sql="select distinct service_id from calls_log where TIMESTAMPDIFF(hour,calls_log.datetime_stop,now()) <24";
	    $sth = $dbh->prepare($sql);
		$sth->execute();
		
		
		 while (my @row = $sth->fetchrow_array()){
			
			my $service_id=$row[0];
			
			$sql = "select name,balance,id  from service where id  = $service_id and balance<2 and balance_reminder is null";
			$rth = $dbh->prepare($sql);
			$rth->execute();
			
			my @info = $rth->fetchrow_array();
			my $data_count=@info;
			
			if($data_count > 0){			 
			   
			   my $name=$info[0];				 
			   my $balance=$info[1];
			   my $service_id=$info[2];
			   
			    my $ani=&data_get("service_data",$service_id,"ani_1_number");
				
				#chack user and message status is unmute
				
				my @user_info =&isZenofonUser($ani);
			   my @status = &MuteUnmute_status($ani);
			   my $StatusValue = $status[0];
			   
			   if($user_info[0] eq 1 && $StatusValue eq 1) {
				  
				  my $set_message =&Message('LOW_BALANCE_MSG');
			      $set_message =~ s/xxxx/$name/i;				 
				  
			  	  &sms_log($ani,$set_message,"",'Sent');
				  &sendSMS_Twilio($ani,$set_message);
				  my $res = $dbh->prepare("update service set balance_reminder=1  where id='$service_id'");
				  $res->execute();
			   }
			   
			}
		 }
		  $sql = "select service.id,service_ani.ani  from service,service_ani where service_ani.service_id  = service.id and service.balance>=2 and balance_reminder=1";
		 $sth = $dbh->prepare($sql);
		 $sth->execute();
		
		 while (my @row = $sth->fetchrow_array()){
			
			my $service_id=$row[0];
			my $ani=$row[1];
			
			my $res = $dbh->prepare("update service set balance_reminder=null  where id='$service_id'");
			$res->execute();
		 }	
   
#Low balance remainder end here

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