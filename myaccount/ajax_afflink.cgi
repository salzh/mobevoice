#!/usr/bin/perl
require "../include.cgi";

 
#=======================================================
# main loop
#=======================================================
$my_url = "ajax_afflink.cgi";
 
 
if (length ($ENV{'QUERY_STRING'}) > 0){
      $buffer = $ENV{'QUERY_STRING'};
      @pairs = split(/&/, $buffer);
      foreach $pair (@pairs){
           ($name, $value) = split(/=/, $pair);
           $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
           $in{$name} = $value; 
      }
 }
 
$value = clean_str( substr($in{'value'} ,0,10),"+.()-=[]?><#\@");
$value = &database_escape($value);
$service_id = $app{service_id} ;

	%hash = database_select_as_hash(
	"SELECT 1,1,service_id FROM service_invite where id='$value' and service_id <>'$service_id' ",
	"flag,service_id");
	 

	print "Content-type:application/json\n\n";

	if ($hash{1}{flag} eq 1) {
		print '{"error":1,"newvalue":"'.$value.'"}' ;
	}else {
		
		&database_do("update service_invite set id='$value' where service_id='$service_id' ");
	 	
		print '{"error":0,"newvalue":"'.$value.'"}' ;
	}
 exit;
 

#=======================================================
  

