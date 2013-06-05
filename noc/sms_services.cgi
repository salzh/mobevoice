#!/usr/bin/perl
use CGI::Carp qw(fatalsToBrowser);
#print "Content-type:text/html\n\n";
require "include.cgi";
use DBI;
use JSON;
use POSIX;
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_view_reports") ne 1) {adm_error("no permission"); exit;}
use Data::Dumper;
#=======================================================


#=======================================================
# main loop
#=======================================================
$my_url = "sms_services.cgi";
$action = $form{action};

if    ($action eq "add_new")		{ &SMS_AddNew(); }

elsif ($action eq "sms_refund")		{&SMS_call_refund();}
elsif ($action eq "sms_log")        {&SMS_log();}
else         { &do_select(); }
exit;
#=======================================================



#=======================================================
# report select
#=======================================================
sub do_select(){
	#
	&cgi_redirect("index.cgi#SMS");
	exit;
	#
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Reports";
    $t{breadcrumb}{0}{title}	= "Reports";
    $t{breadcrumb}{0}{url}		= "";
    $t{content}	= qq[
	<style>
	.local_div{
		padding:0px;
		margin:0px;
		border:0px;
		float:left; 
		margin-right:10px; 
		margin-bottom:15px;
	}
	.local_fieldset {
		margin:0px;
		padding:10px;
		width:200px;
		height:150px;
	}
	.error { color:red; }
	.success { color:green;}
	
	</style>
	
	<div class=local_div><fieldset class=local_fieldset><legend>Calls</legend>
		<a target=_top href="reports.cgi?action=calls_now"				>&#187; Calls sessions now</a><br>
		<a target=_top href="reports.cgi?action=calls_overview"			>&#187; Calls overview</a><br>
		<a target=_top href="reports.cgi?action=calls_error"			>&#187; Calls error</a><br>
		<a target=_top href="reports.cgi?action=calls_country"			>&#187; Calls per country</a><br>
		<a target=_top href="reports.cgi?action=calls_cdr"				>&#187; Calls CDR</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Radio</legend>
		<a target=_top href="reports.cgi?action=radio_now"		>&#187; Radio sessions now</a><br>
		<a target=_top href="reports.cgi?action=radio_overview"	>&#187; Radio overview</a><br>
		<a target=_top href="reports.cgi?action=radio_top"		>&#187; Top radios</a><br>
		<a target=_top href="reports.cgi?action=radio_cdr"		>&#187; Radio CDR</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>Actions</legend>
		<a target=_top href="reports.cgi?action=history_log&display=list"	>&#187; Actions now</a><br>
		<a target=_top href="reports.cgi?action=history_log"				>&#187; Actions overview</a><br>
	</fieldset></div>

	<div class=local_div><fieldset class=local_fieldset><legend>System</legend>
		<a target=_top href="reports.cgi?action=services_overview"				>&#187; Services/reachrges overview</a><br>
		<a target=_top href="reports.cgi?action=commission_contest"				>&#187; Commission contest</a><br>
		<a target=_top href="index.cgi?action=set_frame&title=Servers status&url=/noc/status/">&#187; Servers status</a><br>
		<a target=_top href="reports.cgi?action=test_ney"						>&#187; Test ney</a><br>
	</fieldset></div>

	];
	&template_print("template.html",%t);
}
#=======================================================

#=======================================================
# Sms Add New User Message 
#=======================================================

sub SMS_AddNew(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT id,msg_type,msg_text FROM sms_customtext","msg_type,msg_text");
	%initiate = %{$hash{1}};
	%addnew = %{$hash{2}};
	%confirmation = %{$hash{3}};
	%errormessage = %{$hash{4}};
	%newfriendjoin = %{$hash{5}};
	 	
    $t{dic}{title}		= "Change sms syntax";
    $t{dic}{content}	.= qq[
	
     <style>
	.TextArea{
		width:505px;
		height:65px;
	}
	.errorDiv
	{
	  border:0px red solid;
	  width:500px;
	  height:30px;
	  padding-left:5px;
	  padding-right:8px;
	}
	.errorText
	{
		float:left;
		border:0px red solid;
	}
	.btnspan
	{
		float:right;
		border:0px red solid;
	}
	.error { color:red; }	
	.success { color:green; }	
	</style>
   
	       
			<form action=index.cgi method=post style="padding-left:20px;" id="Form_SMS">
			  <label id="lbl_1">&nbsp;&nbsp;Text for initiate the action</label><br>			  
              <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1">$initiate{msg_text}</textarea>			  
			<br>
			<div class="errorDiv">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1"><input type="button" value="Save" id="save_1"><br>
			  </span>
			</div>
			<br><br>			
			  <label id="lbl_2">&nbsp;&nbsp;Add New contact message</label><br>			  
              <textarea  read-only  class="TextArea" name="AddNewMessage" id="txt_2">$addnew{msg_text}</textarea>			  
			<br>
			<div class="errorDiv">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan">
			  <input type="button" value="Edit" id="edit_2"><input type="button" value="Save" id="save_2"><br>
			  </span>
			</div>
			<br><br>
			  <label id="lbl_3">&nbsp;&nbsp;New contact confirmation message</label><br>			  
              <textarea read-only  class="TextArea" name="ConfirmationMessage" id="txt_3">$confirmation{msg_text}</textarea>			  
			<br>
			<div class="errorDiv">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan">
			   <input type="button" value="Edit" id="edit_3"><input type="button" value="Save" id="save_3"><br>		  </span>
			</div>		
            <br><br>
			  <label id="lbl_4">&nbsp;&nbsp;Control the unrecognized command message</label><br>			  
              <textarea read-only  class="TextArea" name="ErrorMessage" id="txt_4">$errormessage{msg_text}</textarea>			  
			<br>
			<div class="errorDiv">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan">
			   <input type="button" value="Edit" id="edit_4"><input type="button" value="Save" id="save_4"><br>		  </span>
			</div>
			<br><br>
			  <label id="lbl_5">&nbsp;&nbsp;New Friend Join Message</label><br>			  
              <textarea read-only  class="TextArea" name="NewFriendJoin" id="txt_5">$newfriendjoin{msg_text}</textarea>			  
			<br>
			<div class="errorDiv">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan">
			   <input type="button" value="Edit" id="edit_5"><input type="button" value="Save" id="save_5"><br>		  </span>
			</div>
		</form>
	];
    &template_print("template.html",%t);
	
}

sub SMS_call_refund(){
	
	# print start form
	
	my $sub_action = $form{sub_action};
	
	if($sub_action eq "load_data"){
		print $cgi->header(-type => "application/json", -charset => "utf-8");
		
		my $page = $form{page}; # get the requested page 
		my $limit = $form{rows}; # get how many rows we want to have into the grid 
		my $sidx = $form{sidx}; # get index row - i.e. user click to sort
		my $sord = $form{sord}; # get the direction
		my $search = $form{_search};
		my $searchField = $form{searchField};
		my $searchOper = $form{searchOper};
		my $searchString = $form{searchString};
		my $oper = $form{oper};
		my $where;
		
		
		$result =  $database->prepare("SELECT COUNT(*) AS count FROM sms_call_refund");
		$result->execute();
		@row =$result->fetchrow_array();
	  
		$count = $row[0];
		
		if( $count gt 0 ) { $total_pages = ceil($count/$limit); } 
		else { $total_pages = 0; } 
 
		if($page gt  $total_pages){ $page=$total_pages; }
  
		my $start = $limit*$page - $limit; # do not put $limit*($page - 1)
		
		my $response = {};
   
		$response->{page} = $page; 
		$response->{total} = $total_pages;
		$response->{records} = $count;
   
		if($search eq "true"){
	  
			$where = "and $searchField ";
			$where .= &searchOper($searchOper,$searchString);
		}
		
	    my $query = qq(select sms_call_refund.id,sms_call_refund.service_id,sms_call_refund.call_id,sms_call_refund.refund_request_time,sms_call_refund.refund_response_time,sms_call_refund.refund_status,sms_call_refund.refund_amount,calls.date,calls.dst,calls.seconds,calls.balance_before,calls.rate_value,service.name from sms_call_refund,calls,service where sms_call_refund.call_id = calls.id and sms_call_refund.service_id = service.id $where ORDER BY $sidx $sord LIMIT $start , $limit);

		my $sth = $database->prepare($query);
		$sth->execute();
		my $i=0;
		$j=$start;

		while(my @row =$sth->fetchrow_array()){

			$j++;
			  
			my $id = $row[0];
			my $service_id = $row[1];
			my $call_id = $row[2];
			my $refund_request_time = $row[3];
			my $refund_status = $row[5];
			my $refund_amount = $row[6];
			my $date = $row[7];
			my $dst = $row[8];
			my $seconds = $row[9];
			my $balance_before = $row[10];
			my $rate_value = $row[11];
			my $name = $row[12];
      
            if ($balance_before =~ m/((\d+)\.(\d{2}))/)
            {
             $balance_before = $1;
            }
      
            if ($rate_value =~ m/((\d+)\.(\d{2}))/)
            {
            $rate_value = $1;
            }
      
			if ($refund_status eq "Pending")
			{
	          $action = "<input type='button' value='submit' name='submit$i' id='submit$i' onclick='update($i)'>          submit";
			}
			else
			{
			  $action = "<input type='button' value='Processed' name='submit$i' id='submit$i' disabled='true'>            Processed";
			}
			
			$service_id = "<a href='https://www.zenofon.com/noc/services.cgi?action=view&service_id=$service_id'>$service_id</a>";
			$call_id = "<span id='callid$i'>$call_id</span>";
            $rate_value = "<span name='rate$i' id='rate$i'>$rate_value</span>";
			$refund_status ="<span id='refund_status$i'>$refund_status</span>";
			$refund_action = "<select name='sel$i' id='sel$i' onchange='display($i)'><option value='Pending'>Pending<option value='Full Refund'>Full Refund<option value='Decline'>Decline<option value='Partial Refund'>Partial Refund</select>";
			$refund_amount ="<input type='text' name='refund$i' id='refund$i' value='$refund_amount' disabled='true' size='10'>         $refund_amount";

			$response->{rows}[$i]{id}=$row[0];
			
			$response->{rows}[$i]{cell}=[$service_id,$call_id,$name,$dst,$date,$seconds,$rate_value,$refund_request_time,$refund_status,$refund_action,$refund_amount,$action];

			$i++;
		}

		my $json = JSON->new;

		my $json_text=$json->encode($response);

		print $json_text;
	
	}else{
	
		%t = ();
	
	    $t{dic}{my_url}	= $my_url;
	
	    $t{dic}{content}.= qq[
	
		];
		
		$t{dic}{col_names}="['Id','Call Id','User Name','DST Number','Call Time','Call Duration','Call Charge','Refund Request Time','Refund Status','Refund Action','Refund Amount','Action']";
		$t{dic}{col_model}="[ {name:'Id',index:'sms_call_refund.service_id',width:80},
		            {name:'Call Id',index:'sms_call_refund.call_id',width:80},
		            {name:'User Name',index:'service.name',width:130},
					{name:'DST Number',index:'calls.dst',width:130},
					{name:'Call Time',index:'calls.date',width:130},
					{name:'Call Duration',index:'calls.seconds',width:100},
					{name:'Call Charge',index:'calls.rate_value',width:100}, 
					{name:'Refund Request Time',index:'sms_call_refund.refund_request_time',width:180}, 
					{name:'Refund Status',index:'sms_call_refund.refund_status',width:100},
					{name:'Refund Action',index:'refund_action',width:120,sortable:false},
					{name:'Refund Amount',index:'sms_call_refund.refund_amount',width:110},
					{name:'Action',index:'action',width:80,sortable:false},
					 ]";
		$t{dic}{title}	="Call Refund";
		$t{dic}{sort_name}	="id";
		$t{dic}{export_title}	="Call Refund";
		$t{dic}{action}	="sms_refund";
		
		
		&template_print("template.refund.html",%t);
	}

}

sub SMS_log(){
	
	# print start form
	
	my $sub_action = $form{sub_action};
	
	if($sub_action eq "load_data"){
		print $cgi->header(-type => "application/json", -charset => "utf-8");
		
		my $page = $form{page}; # get the requested page 
		my $limit = $form{rows}; # get how many rows we want to have into the grid 
		my $sidx = $form{sidx}; # get index row - i.e. user click to sort
		my $sord = $form{sord}; # get the direction
		my $search = $form{_search};
		my $searchField = $form{searchField};
		my $searchOper = $form{searchOper};
		my $searchString = $form{searchString};
		my $oper = $form{oper};
		my $where;
		
		
		$result =  $database->prepare("SELECT COUNT(*) AS count FROM sms_log");
		$result->execute();
		@row =$result->fetchrow_array();
	  
		$count = $row[0];
		
		if( $count gt 0 ) { $total_pages = ceil($count/$limit); } 
		else { $total_pages = 0; } 
 
		if($page gt  $total_pages){ $page=$total_pages; }
  
		my $start = $limit*$page - $limit; # do not put $limit*($page - 1)
		
		my $response = {};
   
		$response->{page} = $page; 
		$response->{total} = $total_pages;
		$response->{records} = $count;
   
		if($search eq "true"){
	  
			$where = "where $searchField";
			$where .= &searchOper($searchOper,$searchString);
		}
		
		my $query=qq(select id,log_date_time,sms_number,REPLACE(REPLACE(message,"\n",""),"\r",""),sms_function,mode from sms_log $where ORDER BY $sidx $sord LIMIT $start , $limit);
		
		
		my $sth = $database->prepare($query);
		$sth->execute();
		my $i=0;
		$j=$start;

		while(my @row =$sth->fetchrow_array()){

			$j++;
			$response->{rows}[$i]{id}=$row[0]; 
			$response->{rows}[$i]{cell}=[$row[1],$row[2],$row[3],$row[4],$row[5]];
			
			$i++;
		}

		my $json = JSON->new;

		my $json_text=$json->encode($response);

		print $json_text;
	}else{
		%t = ();
	
	$t{dic}{my_url}	= $my_url;
	
	$t{dic}{content}.= qq[
	
		];
		
		$t{dic}{col_names}="['Date', 'SMS Number', 'SMS','SMS Function','Mode']";
		$t{dic}{col_model}="[ {name:'log_date_time',index:'log_date_time',width:140},
					{name:'sms_number',index:'sms_number',width:90}, 
					{name:'message',index:'message',width:900},
					{name:'sms_function',index:'sms_function',width:120}, 
					{name:'mode',index:'mode',width:80}, 
					 ]";
		$t{dic}{title}	="SMS Log";
		$t{dic}{sort_name}	="id";
		$t{dic}{export_title}	="sms_log";
		$t{dic}{action}	="sms_log";
		
		
		&template_print("template.sms.html",%t);
	}
		
	
}
sub searchOper(){
   my ($foper,$fldata)=@_;
   
   my $where;
   
   if ($foper eq "bw"){
	  
	  $fldata .= "%";
	  
	  $where = " LIKE '".$fldata."'";
	  
   }elsif ($foper eq "bn"){
	  
	  $fldata .= "%";
	  
	  $where = " NOT LIKE '".$fldata."'";
	  
   }elsif ($foper eq "eq"){ 
	  
	  $where .= "='".$fldata."'";
	  
   }elsif ($foper eq "ne"){	 
	  
	  $where = "<>'".$fldata."'";
	  
   }elsif ($foper eq "lt"){
	 
	  $where = "<'".$fldata."'";
   }
   elsif ($foper eq "le"){
	  
	  
	  $where .= "<='".$fldata."'";
   }
   elsif ($foper eq "gt"){
	 
	  $where = ">'".$fldata."'";
   }
   elsif ($foper eq "ge"){  
	  
	  $where = ">='".$fldata."'";
	  
   }elsif ($foper eq "ew"){	  
	  
	  $where = "Like '%".$fldata."'";
	  
   }
   elsif ($foper eq "en"){ 
	  
	  $where = "NOT Like '%".$fldata."'";
	  
   }elsif ($foper eq "cn"){
	  
	  $where = "Like '%".$fldata."%'";
	  
   }elsif ($foper eq "nc"){
	  
	  $where = "NOT  Like '%".$fldata."%'";
	  
   }elsif ($foper eq "nu"){
	 
	  $where = "is NULL";
	  
   }elsif ($foper eq "nn"){	 
	  
	  $where = "is NOT NULL";
   }
   elsif ($foper eq "in"){	 
	  
	  $where = "in ($fldata)";
   }
   elsif ($foper eq "ni"){	 
	  
	  $where = "not in ($fldata)";
   }
   
   return $where;

}