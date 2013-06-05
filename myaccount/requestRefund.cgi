#!/usr/bin/perl
require "../include.cgi";

$action = $form{action};
print "Content-type: text/plain\n\n";
if			($action eq "requestRefund")		{&do_request_refund();}
else 											{&do_fail();}

sub do_fail(){
		
		print "failed";
		exit;
}

sub do_request_refund(){
	$service_id = &clean_int($app{session_cookie_u});
	
	$callId = $form{id};
	
	$sql = "select 1,1 from call_refund where call_id='$callId' and service_id='$service_id'";
	%hash = database_select_as_hash($sql, "flag");
	if($hash{1}{flag} eq "1"){
		print "success";
		exit;
	}
	
	$sql = "select 1,1,c.id,c.value from calls c where id='$callId' and service_id='$service_id'";
	%hash = database_select_as_hash($sql, "flag,id,amount");
	
	$output = "failed";
	if($hash{1}{flag} eq "1"){
		$sql = "insert into call_refund (service_id, call_id, amount) values ('$service_id', '$callId', '$hash{1}{amount}')";
		$refundId = database_do_insert($sql);
		if($refundId ne ""){
			$output = "success";
		}else{
			$output = "could not insert";
		}
	}else{
		$output = "bad call";
	}
	print "$output";
}