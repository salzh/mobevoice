#!/usr/bin/perl
#print "Content-type:text/html\n\n";
require "include.cgi";
use DBI;
use CGI;
use utf8;
use Encode;
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

if    ($action eq "mute_unmute")		{ &mute_unmute(); }
if    ($action eq "reroute")		    { &reroute(); }
if    ($action eq "add_contact")		{ &add_contact(); }
if    ($action eq "refer")              { &refer();}
if    ($action eq "automated_msg")      { &automated_msg();}
if    ($action eq "reroute_last_call")  { &reroute_last_call();}
if    ($action eq "menu")               { &menu();}
if    ($action eq "language")           { &language();}
if    ($action eq "last_call")          { &last_call();}
if    ($action eq "call_history")       { &call_history();}
if    ($action eq "help")               { &help();}
if    ($action eq "add_ani")            { &add_ani();}
if    ($action eq "refund")             { &refund();}
if    ($action eq "pin_info")           { &pin_info();}
if    ($action eq "search")             { &search();}
if    ($action eq "delete")             { &delete_contact();}
if    ($action eq "forward")            { &forward();}
if    ($action eq "general_message")    { &general_message();}
exit;
#=======================================================
sub mute_unmute(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='MUTE_UNMUTE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='MUTE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='MUTE_STATUS_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='UNMUTE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	
	$t{dic}{title}		= "Mute/Unmute";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Mute and Unmute Message</label><br>
			  
			<div id="header">
            <ul >
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="MUTE_UNMUTE_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_2">Mute Command Response</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li>  
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="MUTE_INFO">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="message_save(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">Mute Status Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="MUTE_STATUS_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="message_save(3)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_4">Unmute Command Response</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="UNMUTE_INFO">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="message_save(4)" disabled="true"><br>
			  </span>
			</div>
			</form>
	];
    &template_print("template.html",%t);	
}

sub reroute(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REROUTE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CONTACT_NOT_FOUND_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ROUTE_SELECTION_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ROUTE_CHANGE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ROUTE_ERROR_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id5 = $hash{1}{id};
	my $language_id5 = $hash{1}{language_id};
	my $messages5 = $hash{1}{messages};
	$messages5 = encode("utf8" ,$messages5);
	my $message_type5= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CUSTOMER_SUPPORT_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id6 = $hash{1}{id};
	my $language_id6 = $hash{1}{language_id};
	my $messages6 = $hash{1}{messages};
	$messages6 = encode("utf8" ,$messages6);
	my $message_type6= $hash{1}{message_type};
	
	$t{dic}{title}		= "Reroute";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Reroute Response Message</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li>  
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="REROUTE_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_2">Contact Not Found Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li>  
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="CONTACT_NOT_FOUND_INFO">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="message_save(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">Route Selection Details</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="ROUTE_SELECTION_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="message_save(3)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_4">Route Change Response Message</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="ROUTE_CHANGE_INFO">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="check_message(4)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_5">Route Error Information</label><br>
			<div id="header">
            <ul>
	       <li ><a id="English_5" onclick = "change_language(5,1)">English</a></li>
	        <li ><a id="French_5" onclick = "change_language(5,2)">French</a></li>
	        <li><a id="Spanish_5" onclick = "change_language(5,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_5" disabled="true">$messages5</textarea>
			  <input type="hidden" id = "language_id_5" value="$language_id5">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_5" value="ROUTE_ERROR_INFO">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan" id="Error_5">
			  <input type="button" value="Edit" id="edit_5" onclick="message_edit(5)"><input type="button" value="Save" id="save_5" onclick="message_save(5)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_6">Customer Support Information</label><br>
			<div id="header">
            <ul>
	       <li ><a id="English_6" onclick = "change_language(6,1)">English</a></li>
	        <li ><a id="French_6" onclick = "change_language(6,2)">French</a></li>
	        <li><a id="Spanish_6" onclick = "change_language(6,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_6" disabled="true">$messages6</textarea>
			  <input type="hidden" id = "language_id_6" value="$language_id6">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_6" value="CUSTOMER_SUPPORT_INFO">
			  <span class="errorText" id="Error_6"></span>
			  <span class="btnspan" id="Error_6">
			  <input type="button" value="Edit" id="edit_6" onclick="message_edit(6)"><input type="button" value="Save" id="save_6" onclick="message_save(6)" disabled="true"><br>
			  </span>
			</div>
			</form>
	];
    &template_print("template.html",%t);	
}


sub add_contact(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ADD_CONTACT_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ADD_CONTACT_RESP_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ADD_CONTACT_INVALID_FORMAT' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ADD_CONTACT_CUSTOM_SUP' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CONTACT_LIMIT_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id5 = $hash{1}{id};
	my $language_id5 = $hash{1}{language_id};
	my $messages5 = $hash{1}{messages};
	$messages5 = encode("utf8" ,$messages5);
	my $message_type5= $hash{1}{message_type};
	
	$t{dic}{title}		= "Add New Contact";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Add New Contact Format Message</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="ADD_CONTACT_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			<label id="lbl_2">Add New Contact Response Message</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="ADD_CONTACT_RESP_INFO">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="check_message(2)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			
			<label id="lbl_3">Add New Contact Invalid Format</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="ADD_CONTACT_INVALID_FORMAT">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="message_save(3)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_4">Add New Contact Customer support Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="ADD_CONTACT_CUSTOM_SUP">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="message_save(4)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_5">Add Contact Limit Message</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_5" onclick = "change_language(5,1)">English</a></li>
	        <li ><a id="French_5" onclick = "change_language(5,2)">French</a></li>
	        <li><a id="Spanish_5" onclick = "change_language(5,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_5" disabled="true">$messages5</textarea>
			  <input type="hidden" id = "language_id_5" value="$language_id5">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_5" value="CONTACT_LIMIT_INFO">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan" id="Error_5">
			  <input type="button" value="Edit" id="edit_5" onclick="message_edit(5)"><input type="button" value="Save" id="save_5" onclick="message_save(5)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub refer(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_FRIEND_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_RESP_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_DUP_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='WELCOME_USER_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='INVALID_REFER_FORMAT' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id5 = $hash{1}{id};
	my $language_id5 = $hash{1}{language_id};
	my $messages5 = $hash{1}{messages};
	$messages5 = encode("utf8" ,$messages5);
	my $message_type5= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='INVITE_EXPIRE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id6 = $hash{1}{id};
	my $language_id6 = $hash{1}{language_id};
	my $messages6 = $hash{1}{messages};
	$messages6 = encode("utf8" ,$messages6);
	my $message_type6= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='NUMBER_FORMAT_ERROR_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id7 = $hash{1}{id};
	my $language_id7 = $hash{1}{language_id};
	my $messages7 = $hash{1}{messages};
	$messages7 = encode("utf8" ,$messages7);
	my $message_type7= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_NUMBER_ERROR' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id8 = $hash{1}{id};
	my $language_id8 = $hash{1}{language_id};
	my $messages8 = $hash{1}{messages};
	$messages8 = encode("utf8" ,$messages8);
	my $message_type8= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_INCORRECT_NUMBER_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id9 = $hash{1}{id};
	my $language_id9 = $hash{1}{language_id};
	my $messages9 = $hash{1}{messages};
	$messages9 = encode("utf8" ,$messages9);
	my $message_type9= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='NOT_VALID_NUM_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id10 = $hash{1}{id};
	my $language_id10 = $hash{1}{language_id};
	my $messages10 = $hash{1}{messages};
	$messages10 = encode("utf8" ,$messages10);
	my $message_type10= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='NOT_ALLOW_NUM_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id11 = $hash{1}{id};
	my $language_id11 = $hash{1}{language_id};
	my $messages11 = $hash{1}{messages};
	$messages11 = encode("utf8" ,$messages10);
	my $message_type11= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='INVALID_JOIN_FORMAT' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id12 = $hash{1}{id};
	my $language_id12 = $hash{1}{language_id};
	my $messages12 = $hash{1}{messages};
	$messages12 = encode("utf8" ,$messages12);
	my $message_type12= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_CUSTOM_SUP' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id13 = $hash{1}{id};
	my $language_id13 = $hash{1}{language_id};
	my $messages13 = $hash{1}{messages};
	$messages13 = encode("utf8" ,$messages13);
	my $message_type13= $hash{1}{message_type};
	
	$t{dic}{title}		= "Refer Friend";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Refer Friend Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="REFER_FRIEND_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_2">Refer Friend Response Message</label><br>
			<div id="header">
            <ul >
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="REFER_RESP_INFO">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="check_message(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">Refer Friend Duplicate Contact Message</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="REFER_DUP_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="message_save(3)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_4">Welcome Message to New Friend</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="WELCOME_USER_MSG">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="message_save(4)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_5">Refer Friend Invalid Format Message</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_5" onclick = "change_language(5,1)">English</a></li>
	        <li ><a id="French_5" onclick = "change_language(5,2)">French</a></li>
	        <li><a id="Spanish_5" onclick = "change_language(5,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_5" disabled="true">$messages5</textarea>
			  <input type="hidden" id = "language_id_5" value="$language_id5">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_5" value="INVALID_REFER_FORMAT">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan" id="Error_5">
			  <input type="button" value="Edit" id="edit_5" onclick="message_edit(5)"><input type="button" value="Save" id="save_5" onclick="message_save(5)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_6">Invitation Expire Message</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_6" onclick = "change_language(6,1)">English</a></li>
	        <li ><a id="French_6" onclick = "change_language(6,2)">French</a></li>
	        <li><a id="Spanish_6" onclick = "change_language(6,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_6" disabled="true">$messages6</textarea>
			  <input type="hidden" id = "language_id_6" value="$language_id6">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_6" value="INVITE_EXPIRE_INFO">
			  <span class="errorText" id="Error_6"></span>
			  <span class="btnspan" id="Error_6">
			  <input type="button" value="Edit" id="edit_6" onclick="message_edit(6)"><input type="button" value="Save" id="save_6" onclick="message_save(6)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_7">Number Format Error</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_7" onclick = "change_language(7,1)">English</a></li>
	        <li ><a id="French_7" onclick = "change_language(7,2)">French</a></li>
	        <li><a id="Spanish_7" onclick = "change_language(7,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_7" disabled="true">$messages7</textarea>
			  <input type="hidden" id = "language_id_7" value="$language_id7">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_7" value="NUMBER_FORMAT_ERROR_INFO">
			  <span class="errorText" id="Error_7"></span>
			  <span class="btnspan" id="Error_7">
			  <input type="button" value="Edit" id="edit_7" onclick="message_edit(7)"><input type="button" value="Save" id="save_7" onclick="message_save(7)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_8">Refer Number Error Message</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_8" onclick = "change_language(8,1)">English</a></li>
	        <li ><a id="French_8" onclick = "change_language(8,2)">French</a></li>
	        <li><a id="Spanish_8" onclick = "change_language(8,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_8" disabled="true">$messages8</textarea>
			  <input type="hidden" id = "language_id_8" value="$language_id8">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_8" value="REFER_NUMBER_ERROR">
			  <span class="errorText" id="Error_8"></span>
			  <span class="btnspan" id="Error_8">
			  <input type="button" value="Edit" id="edit_8" onclick="message_edit(8)"><input type="button" value="Save" id="save_8" onclick="message_save(8)" disabled="true"><br>
			  </span>
			</div>
			
		  
		  <br><br>
			<label id="lbl_9">Incorrect Number Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_9" onclick = "change_language(9,1)">English</a></li>
	        <li ><a id="French_9" onclick = "change_language(9,2)">French</a></li>
	        <li><a id="Spanish_9" onclick = "change_language(9,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_9" disabled="true">$messages9</textarea>
			  <input type="hidden" id = "language_id_9" value="$language_id9">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_9" value="REFER_INCORRECT_NUMBER_INFO">
			  <span class="errorText" id="Error_9"></span>
			  <span class="btnspan" id="Error_9">
			  <input type="button" value="Edit" id="edit_9" onclick="message_edit(9)"><input type="button" value="Save" id="save_9" onclick="message_save(9)" disabled="true"><br>
			  </span>
			</div>	
			
		<br><br>
			<label id="lbl_10">Not a Valid Number Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_10" onclick = "change_language(10,1)">English</a></li>
	        <li ><a id="French_10" onclick = "change_language(10,2)">French</a></li>
	        <li><a id="Spanish_10" onclick = "change_language(10,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_10" disabled="true">$messages10</textarea>
			  <input type="hidden" id = "language_id_10" value="$language_id10">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_10" value="NOT_VALID_NUM_INFO">
			  <span class="errorText" id="Error_10"></span>
			  <span class="btnspan" id="Error_10">
			  <input type="button" value="Edit" id="edit_10" onclick="message_edit(10)"><input type="button" value="Save" id="save_10" onclick="message_save(10)" disabled="true"><br>
			  </span>
			</div>
			
		   <br><br>
			<label id="lbl_11">Not allow Number Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_11" onclick = "change_language(11,1)">English</a></li>
	        <li ><a id="French_11" onclick = "change_language(11,2)">French</a></li>
	        <li><a id="Spanish_11" onclick = "change_language(11,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_11" disabled="true">$messages11</textarea>
			  <input type="hidden" id = "language_id_11" value="$language_id11">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_11" value="NOT_ALLOW_NUM_INFO">
			  <span class="errorText" id="Error_11"></span>
			  <span class="btnspan" id="Error_11">
			  <input type="button" value="Edit" id="edit_11" onclick="message_edit(11)"><input type="button" value="Save" id="save_11" onclick="message_save(11)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_12">Invalid Join Format</label><br>
			<div id="header">
            <ul>
	       <li ><a id="English_12" onclick = "change_language(12,1)">English</a></li>
	        <li ><a id="French_12" onclick = "change_language(12,2)">French</a></li>
	        <li><a id="Spanish_12" onclick = "change_language(12,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_12" disabled="true">$messages12</textarea>
			  <input type="hidden" id = "language_id_12" value="$language_id12">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_12" value="INVALID_JOIN_FORMAT">
			  <span class="errorText" id="Error_12"></span>
			  <span class="btnspan" id="Error_12">
			  <input type="button" value="Edit" id="edit_12" onclick="message_edit(12)"><input type="button" value="Save" id="save_12" onclick="message_save(12)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_13">Refer Friend customer support</label><br>
			<div id="header">
            <ul>
	       <li ><a id="English_13" onclick = "change_language(13,1)">English</a></li>
	        <li ><a id="French_13" onclick = "change_language(13,2)">French</a></li>
	        <li><a id="Spanish_13" onclick = "change_language(13,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_13" disabled="true">$messages13</textarea>
			  <input type="hidden" id = "language_id_13" value="$language_id13">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_13" value="REFER_CUSTOM_SUP">
			  <span class="errorText" id="Error_13"></span>
			  <span class="btnspan" id="Error_13">
			  <input type="button" value="Edit" id="edit_13" onclick="message_edit(13)"><input type="button" value="Save" id="save_13" onclick="message_save(13)" disabled="true"><br>
			  </span>
			</div>
			</form>
	];
    &template_print("template.html",%t);	
}

sub automated_msg(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_INVITATION_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_INVITATION_24H' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_INVITATION_48H' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_INVITATION_10D' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_NOT_JOINED_11D' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id5 = $hash{1}{id};
	my $language_id5 = $hash{1}{language_id};
	my $messages5 = $hash{1}{messages};
	$messages5 = encode("utf8" ,$messages5);
	my $message_type5= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFER_PROMOTION_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id6 = $hash{1}{id};
	my $language_id6 = $hash{1}{language_id};
	my $messages6 = $hash{1}{messages};
	$messages6 = encode("utf8" ,$messages6);
	my $message_type6= $hash{1}{message_type};
	
	
	$t{dic}{title}		= "Automatted Message";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Invitation Message</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li>  
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="REFER_INVITATION_MSG">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="refer_msgCheck(1)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_2">Invitation Message of 24 hours</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li>  
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="REFER_INVITATION_24H">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="refer_msgCheck(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">Invitation Message of 48 hours</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="REFER_INVITATION_48H">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="refer_msgCheck(3)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_4">Invitation Message of 10 Days</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="REFER_INVITATION_10D">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="refer_msgCheck(4)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_5">Refer Friend Not Joined after 11 Days</label><br>
			<div id="header">
            <ul>
	       <li ><a id="English_5" onclick = "change_language(5,1)">English</a></li>
	        <li ><a id="French_5" onclick = "change_language(5,2)">French</a></li>
	        <li><a id="Spanish_5" onclick = "change_language(5,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_5" disabled="true">$messages5</textarea>
			  <input type="hidden" id = "language_id_5" value="$language_id5">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_5" value="REFER_NOT_JOINED_11D">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan" id="Error_5">
			  <input type="button" value="Edit" id="edit_5" onclick="message_edit(5)"><input type="button" value="Save" id="save_5" onclick="refer_msgCheck(5)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_6">Refer Friend Promotional Message</label><br>
			<div id="header">
            <ul>
	       <li ><a id="English_6" onclick = "change_language(6,1)">English</a></li>
	        <li ><a id="French_6" onclick = "change_language(6,2)">French</a></li>
	        <li><a id="Spanish_6" onclick = "change_language(6,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_6" disabled="true">$messages6</textarea>
			  <input type="hidden" id = "language_id_6" value="$language_id6">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_6" value="REFER_PROMOTION_MSG">
			  <span class="errorText" id="Error_6"></span>
			  <span class="btnspan" id="Error_6">
			  <input type="button" value="Edit" id="edit_6" onclick="message_edit(6)"><input type="button" value="Save" id="save_6" onclick="refer_msgCheck(6)" disabled="true"><br>
			  </span>
			</div>
			</form>
	];
    &template_print("template.html",%t);	
}

sub reroute_last_call(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='LAST_CALL_ROUTE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	   
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='LAST_CALL_ROUTE' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='RRLC_RESP_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CALL_ROUTE_SELECTION' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='RRLC_UNRESP_ROUTE' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id5 = $hash{1}{id};
	my $language_id5 = $hash{1}{language_id};
	my $messages5 = $hash{1}{messages};
	$messages5 = encode("utf8" ,$messages5);
	my $message_type5= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='RRLC_FUTURE_ROUTE' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id6 = $hash{1}{id};
	my $language_id6 = $hash{1}{language_id};
	my $messages6 = $hash{1}{messages};
	$messages6 = encode("utf8" ,$messages6);
	my $message_type6= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='FUTURE_ROUTE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id7 = $hash{1}{id};
	my $language_id7 = $hash{1}{language_id};
	my $messages7 = $hash{1}{messages};
	$messages7 = encode("utf8" ,$messages7);
	my $message_type7= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='RRLC_CUSTOM_SUP' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id8 = $hash{1}{id};
	my $language_id8 = $hash{1}{language_id};
	my $messages8 = $hash{1}{messages};
	$messages8 = encode("utf8" ,$messages8);
	my $message_type8= $hash{1}{message_type};
	
	$t{dic}{title}		= "Reroute Last Call";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Last Call Route Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="LAST_CALL_ROUTE_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="reroute_last_call(1)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_2">Last Call Route Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="LAST_CALL_ROUTE">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="reroute_last_call(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">Reroute Last call Response Message</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="RRLC_RESP_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="reroute_last_call(3)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_4">Call Route Selection</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="CALL_ROUTE_SELECTION">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="reroute_last_call(4)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_5">Reroute Last Call Unresponse Route</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_5" onclick = "change_language(5,1)">English</a></li>
	        <li ><a id="French_5" onclick = "change_language(5,2)">French</a></li>
	        <li><a id="Spanish_5" onclick = "change_language(5,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_5" disabled="true">$messages5</textarea>
			  <input type="hidden" id = "language_id_5" value="$language_id5">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_5" value="RRLC_UNRESP_ROUTE">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan" id="Error_5">
			  <input type="button" value="Edit" id="edit_5" onclick="message_edit(5)"><input type="button" value="Save" id="save_5" onclick="message_save(5)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_6">Reroute Last Call Future Route Details</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_6" onclick = "change_language(6,1)">English</a></li>
	        <li ><a id="French_6" onclick = "change_language(6,2)">French</a></li>
	        <li><a id="Spanish_6" onclick = "change_language(6,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_6" disabled="true">$messages6</textarea>
			  <input type="hidden" id = "language_id_6" value="$language_id6">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_6" value="RRLC_FUTURE_ROUTE">
			  <span class="errorText" id="Error_6"></span>
			  <span class="btnspan" id="Error_6">
			  <input type="button" value="Edit" id="edit_6" onclick="message_edit(6)"><input type="button" value="Save" id="save_6" onclick="reroute_last_call(6)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_7">Future Route Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_7" onclick = "change_language(7,1)">English</a></li>
	        <li ><a id="French_7" onclick = "change_language(7,2)">French</a></li>
	        <li><a id="Spanish_7" onclick = "change_language(7,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_7" disabled="true">$messages7</textarea>
			  <input type="hidden" id = "language_id_7" value="$language_id7">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_7" value="FUTURE_ROUTE_INFO">
			  <span class="errorText" id="Error_7"></span>
			  <span class="btnspan" id="Error_7">
			  <input type="button" value="Edit" id="edit_7" onclick="message_edit(7)"><input type="button" value="Save" id="save_7" onclick="reroute_last_call(7)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_8">Reroute Last Call Customer support Message</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_8" onclick = "change_language(8,1)">English</a></li>
	        <li ><a id="French_8" onclick = "change_language(8,2)">French</a></li>
	        <li><a id="Spanish_8" onclick = "change_language(8,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_8" disabled="true">$messages8</textarea>
			  <input type="hidden" id = "language_id_8" value="$language_id8">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_8" value="RRLC_CUSTOM_SUP">
			  <span class="errorText" id="Error_8"></span>
			  <span class="btnspan" id="Error_8">
			  <input type="button" value="Edit" id="edit_8" onclick="message_edit(8)"><input type="button" value="Save" id="save_8" onclick="message_save(8)" disabled="true"><br>
			  </span>
			</div>
			</form>
	];
    &template_print("template.html",%t);	
}

sub menu(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='MENU_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	
	$t{dic}{title}		= "Main Menu";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Main Menu</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="MenuTextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="MENU_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}


sub last_call(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='LASTCALL_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	
	$t{dic}{title}		= "Last Call";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Last Call Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="LASTCALL_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="check_message(1)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub call_history(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CALL_HISTORY_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	
	$t{dic}{title}		= "Call History";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Call History Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="CALL_HISTORY_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="check_message(1)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub language(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='LANGUAGE_MENU' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='LANGUAGE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	
	$t{dic}{title}		= "Select Language";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Language Menu Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="LangTextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="LANGUAGE_MENU">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div>
			
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="LANGUAGE_INFO">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="message_save(2)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub help(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='HELP_MSG_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='HELP_2_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='HELP_3_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='HELP_4_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	
	$t{dic}{title}		= "Help";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Help Message</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="HELP_MSG_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_2">Help Message 2</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="HELP_2_MSG">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="message_save(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">Help Message 3</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="HELP_3_MSG">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="message_save(3)" disabled="true"><br>
			  </span>
			</div>
			<br><br>
			<label id="lbl_4">Help Message 4</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="HELP_4_MSG">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="message_save(4)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}


sub add_ani(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ADD_ANI_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ANI_RESP_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ADD_ANI_INVALID_FORMAT' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='DUPLICATE_ANI_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='EXISTS_ZENO_USER' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id5 = $hash{1}{id};
	my $language_id5 = $hash{1}{language_id};
	my $messages5 = $hash{1}{messages};
	$messages5 = encode("utf8" ,$messages5);
	my $message_type5= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='ADD_ANI_CUSTOM_SUP' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id6 = $hash{1}{id};
	my $language_id6 = $hash{1}{language_id};
	my $messages6 = $hash{1}{messages};
	$messages6 = encode("utf8" ,$messages6);
	my $message_type6= $hash{1}{message_type};
	
	$t{dic}{title}		= "Add ANI";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Add ANI Number Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="ADD_ANI_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			
			<label id="lbl_2">Add ANI Number Response</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="ANI_RESP_INFO">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="add_ani(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">Add ANI Number Invalid Format</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="ADD_ANI_INVALID_FORMAT">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="message_save(3)" disabled="true"><br>
			  </span>
			</div>
		
			<br><br>
			<label id="lbl_4">Duplicate ANI Number</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="DUPLICATE_ANI_INFO">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="add_ani(4)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_5">Exists User Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_5" onclick = "change_language(5,1)">English</a></li>
	        <li ><a id="French_5" onclick = "change_language(5,2)">French</a></li>
	        <li><a id="Spanish_5" onclick = "change_language(5,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_5" disabled="true">$messages5</textarea>
			  <input type="hidden" id = "language_id_5" value="$language_id5">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_5" value="EXISTS_ZENO_USER">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan" id="Error_5">
			  <input type="button" value="Edit" id="edit_5" onclick="message_edit(5)"><input type="button" value="Save" id="save_5" onclick="add_ani(5)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_6">Add ANI Number Customer Support Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_6" onclick = "change_language(6,1)">English</a></li>
	        <li ><a id="French_6" onclick = "change_language(6,2)">French</a></li>
	        <li><a id="Spanish_6" onclick = "change_language(6,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_6" disabled="true">$messages6</textarea>
			  <input type="hidden" id = "language_id_6" value="$language_id6">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_6" value="ADD_ANI_CUSTOM_SUP">
			  <span class="errorText" id="Error_6"></span>
			  <span class="btnspan" id="Error_6">
			  <input type="button" value="Edit" id="edit_6" onclick="message_edit(6)"><input type="button" value="Save" id="save_6" onclick="message_save(6)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub general_message(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CALL_NOT_FOUND_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='NOT_ZENO_USER_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='DUPLICATE_CONTACT_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id5 = $hash{1}{id};
	my $language_id5 = $hash{1}{language_id};
	my $messages5 = $hash{1}{messages};
	$messages5 = encode("utf8" ,$messages5);
	my $message_type5= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='SYSTEM_ERROR_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id6 = $hash{1}{id};
	my $language_id6 = $hash{1}{language_id};
	my $messages6 = $hash{1}{messages};
	$messages6 = encode("utf8" ,$messages6);
	my $message_type6= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='WRONG_DIAL_NUMBER' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id7 = $hash{1}{id};
	my $language_id7 = $hash{1}{language_id};
	my $messages7 = $hash{1}{messages};
	$messages7 = encode("utf8" ,$messages7);
	my $message_type7= $hash{1}{message_type};
	
	
	
	$t{dic}{title}		= "General Message";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_2">Call Not Found</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="CALL_NOT_FOUND_INFO">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="message_save(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">Not Zenofon User</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="NOT_ZENO_USER_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="message_save(3)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_5">Duplicate Contact Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_5" onclick = "change_language(5,1)">English</a></li>
	        <li ><a id="French_5" onclick = "change_language(5,2)">French</a></li>
	        <li><a id="Spanish_5" onclick = "change_language(5,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_5" disabled="true">$messages5</textarea>
			  <input type="hidden" id = "language_id_5" value="$language_id5">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_5" value="DUPLICATE_CONTACT_INFO">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan" id="Error_5">
			  <input type="button" value="Edit" id="edit_5" onclick="message_edit(5)"><input type="button" value="Save" id="save_5" onclick="check_message(5)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_6">System Error Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_6" onclick = "change_language(6,1)">English</a></li>
	        <li ><a id="French_6" onclick = "change_language(6,2)">French</a></li>
	        <li><a id="Spanish_6" onclick = "change_language(6,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_6" disabled="true">$messages6</textarea>
			  <input type="hidden" id = "language_id_6" value="$language_id6">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_6" value="SYSTEM_ERROR_INFO">
			  <span class="errorText" id="Error_6"></span>
			  <span class="btnspan" id="Error_6">
			  <input type="button" value="Edit" id="edit_6" onclick="message_edit(6)"><input type="button" value="Save" id="save_6" onclick="message_save(6)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_7">Wrong Dial Number Reply</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_7" onclick = "change_language(7,1)">English</a></li>
	        <li ><a id="French_7" onclick = "change_language(7,2)">French</a></li>
	        <li><a id="Spanish_7" onclick = "change_language(7,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_7" disabled="true">$messages7</textarea>
			  <input type="hidden" id = "language_id_7" value="$language_id7">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_7" value="WRONG_DIAL_NUMBER">
			  <span class="errorText" id="Error_7"></span>
			  <span class="btnspan" id="Error_7">
			  <input type="button" value="Edit" id="edit_7" onclick="message_edit(7)"><input type="button" value="Save" id="save_7" onclick="message_save(7)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub refund(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFUND_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFUND_APPROVAL_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='REFUND_DECLINE_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	$t{dic}{title}		= "Refund";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Refund Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="REFUND_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			<label id="lbl_2">Refund Approval Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="REFUND_APPROVAL_INFO">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="check_message(2)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			
			<label id="lbl_3">Refund Decline Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="REFUND_DECLINE_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="check_message(3)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub pin_info(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='USER_PIN_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CHANGE_PIN_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='NEW_PIN_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CC_NOT_FOUND' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CC_INVALID_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id5 = $hash{1}{id};
	my $language_id5 = $hash{1}{language_id};
	my $messages5 = $hash{1}{messages};
	$messages5 = encode("utf8" ,$messages5);
	my $message_type5= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CC_FORMAT_ERROR' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id6 = $hash{1}{id};
	my $language_id6 = $hash{1}{language_id};
	my $messages6 = $hash{1}{messages};
	$messages6 = encode("utf8" ,$messages6);
	my $message_type6= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CC_AUTHENTICATION_FAILED' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id7 = $hash{1}{id};
	my $language_id7 = $hash{1}{language_id};
	my $messages7 = $hash{1}{messages};
	$messages7 = encode("utf8" ,$messages7);
	my $message_type7= $hash{1}{message_type};
	
	$t{dic}{title}		= "Change PIN";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">User PIN Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="USER_PIN_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="check_message(1)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			
			<label id="lbl_2">Change PIN Message</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="CHANGE_PIN_MSG">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="message_save(2)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_3">New PIN Information</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="NEW_PIN_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="check_message(3)" disabled="true"><br>
			  </span>
			</div>
		
			<br><br>
			<label id="lbl_4">Credit Card Details Not Found</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="CC_NOT_FOUND">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="message_save(4)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_5">Invalid Credit Card</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_5" onclick = "change_language(5,1)">English</a></li>
	        <li ><a id="French_5" onclick = "change_language(5,2)">French</a></li>
	        <li><a id="Spanish_5" onclick = "change_language(5,3)">Spanish</a></li>
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_5" disabled="true">$messages5</textarea>
			  <input type="hidden" id = "language_id_5" value="$language_id5">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_5" value="CC_INVALID_MSG">
			  <span class="errorText" id="Error_5"></span>
			  <span class="btnspan" id="Error_5">
			  <input type="button" value="Edit" id="edit_5" onclick="message_edit(5)"><input type="button" value="Save" id="save_5" onclick="message_save(5)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_6">Credit Card Format Error Message</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_6" onclick = "change_language(6,1)">English</a></li>
	        <li ><a id="French_6" onclick = "change_language(6,2)">French</a></li>
	        <li><a id="Spanish_6" onclick = "change_language(6,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_6" disabled="true">$messages6</textarea>
			  <input type="hidden" id = "language_id_6" value="$language_id6">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_6" value="CC_FORMAT_ERROR">
			  <span class="errorText" id="Error_6"></span>
			  <span class="btnspan" id="Error_6">
			  <input type="button" value="Edit" id="edit_6" onclick="message_edit(6)"><input type="button" value="Save" id="save_6" onclick="message_save(6)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_7">Credit Card Authentication Failed</label><br>
			<div id="header">
            <ul>
	        <li ><a id="English_7" onclick = "change_language(7,1)">English</a></li>
	        <li ><a id="French_7" onclick = "change_language(7,2)">French</a></li>
	        <li><a id="Spanish_7" onclick = "change_language(7,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_7" disabled="true">$messages7</textarea>
			  <input type="hidden" id = "language_id_7" value="$language_id7">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_7" value="CC_AUTHENTICATION_FAILED">
			  <span class="errorText" id="Error_7"></span>
			  <span class="btnspan" id="Error_7">
			  <input type="button" value="Edit" id="edit_7" onclick="message_edit(7)"><input type="button" value="Save" id="save_7" onclick="message_save(7)" disabled="true"><br>
			  </span>
			</div>
			
			</form>
			];
			&template_print("template.html",%t);	
}



sub search(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='SEARCH_CONTACT_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='SEARCH_CONTACT_NOT_FOUND' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='SEARCH_RESP_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	$t{dic}{title}		= "Search";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Search Contact Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="SEARCH_CONTACT_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			<label id="lbl_2">Search Contact Not Found</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="SEARCH_CONTACT_NOT_FOUND">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="check_message(2)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			
			<label id="lbl_3">Search Contact Response</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="SEARCH_RESP_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="check_message(3)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub delete_contact(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='DELETE_CONTACT_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='DELETE_CONTACT_NOT_FOUND' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='DELETE_RESP_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='DELETE_CUSTOM_SUP' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id4 = $hash{1}{id};
	my $language_id4 = $hash{1}{language_id};
	my $messages4 = $hash{1}{messages};
	$messages4 = encode("utf8" ,$messages4);
	my $message_type4= $hash{1}{message_type};
	
	$t{dic}{title}		= "Delete Contact";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Delete Contact Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="DELETE_CONTACT_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="message_save(1)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			<label id="lbl_2">Delete Contact Not Found</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="DELETE_CONTACT_NOT_FOUND">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="check_message(2)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			
			<label id="lbl_3">Delete Contact Response</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="DELETE_RESP_INFO">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="check_message(3)" disabled="true"><br>
			  </span>
			</div>
			
			<br><br>
			<label id="lbl_4">Delete Contact Customer Support Message</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_4" onclick = "change_language(4,1)">English</a></li>
	        <li ><a id="French_4" onclick = "change_language(4,2)">French</a></li>
	        <li><a id="Spanish_4" onclick = "change_language(4,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_4" disabled="true">$messages4</textarea>
			  <input type="hidden" id = "language_id_4" value="$language_id4">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_4" value="DELETE_CUSTOM_SUP">
			  <span class="errorText" id="Error_4"></span>
			  <span class="btnspan" id="Error_4">
			  <input type="button" value="Edit" id="edit_4" onclick="message_edit(4)"><input type="button" value="Save" id="save_4" onclick="message_save(4)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}

sub forward(){
	if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}
	#
	# start 
    %t = ();
    #%hash = database_select_as_hash("SELECT msg_text FROM multilevel.sms_customtext where msg_type='InitiateAction'","msg_text");
	#%user_data = %{$hash{1}};
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='FORWARD_RESP_INFO' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id1 = $hash{1}{id};
	my $language_id1 = $hash{1}{language_id};
	my $messages1 = $hash{1}{messages};
	$messages1 = encode("utf8" ,$messages1);
	my $message_type1= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='CONTACT_NOT_FOUND_MSG' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id2 = $hash{1}{id};
	my $language_id2 = $hash{1}{language_id};
	my $messages2 = $hash{1}{messages};
	$messages2 = encode("utf8" ,$messages2);
	my $message_type2= $hash{1}{message_type};
	
	%hash = database_select_as_hash("SELECT 1,1,1,id,language_id,messages,message_type FROM sms_messages WHERE message_type ='EXISTS_FORWARD_NUMBER' and language_id =1","1,1,id,language_id,messages,message_type");
	
	my $id3 = $hash{1}{id};
	my $language_id3 = $hash{1}{language_id};
	my $messages3 = $hash{1}{messages};
	$messages3 = encode("utf8" ,$messages3);
	my $message_type3= $hash{1}{message_type};
	

	$t{dic}{title}		= "Forward Number";
    $t{dic}{content}	.= qq[
   	       
			<form action=index.cgi method=post style="padding-left:20px;" id="SMS_Message">
			<label id="lbl_1">Add Forward Number Response</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_1" onclick = "change_language(1,1)">English</a></li>
	        <li ><a id="French_1" onclick = "change_language(1,2)">French</a></li>
	        <li><a id="Spanish_1" onclick = "change_language(1,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_1" disabled="true">$messages1</textarea>
			  <input type="hidden" id = "language_id_1" value="$language_id1">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_1" value="FORWARD_RESP_INFO">
			  <span class="errorText" id="Error_1"></span>
			  <span class="btnspan" id="Error_1">
			  <input type="button" value="Edit" id="edit_1" onclick="message_edit(1)"><input type="button" value="Save" id="save_1" onclick="check_message(1)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			<label id="lbl_2">Contact Not Found</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_2" onclick = "change_language(2,1)">English</a></li>
	        <li ><a id="French_2" onclick = "change_language(2,2)">French</a></li>
	        <li><a id="Spanish_2" onclick = "change_language(2,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_2" disabled="true">$messages2</textarea>
			  <input type="hidden" id = "language_id_2" value="$language_id2">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_2" value="CONTACT_NOT_FOUND_MSG">
			  <span class="errorText" id="Error_2"></span>
			  <span class="btnspan" id="Error_2">
			  <input type="button" value="Edit" id="edit_2" onclick="message_edit(2)"><input type="button" value="Save" id="save_2" onclick="check_message(2)" disabled="true"><br>
			  </span>
			</div><br><br>
			
			
			<label id="lbl_3">Exists Forward Number Information</label><br>
			  
			<div id="header">
            <ul>
	        <li ><a id="English_3" onclick = "change_language(3,1)">English</a></li>
	        <li ><a id="French_3" onclick = "change_language(3,2)">French</a></li>
	        <li><a id="Spanish_3" onclick = "change_language(3,3)">Spanish</a></li> 
            </ul>
            </div>
			<br><br>
			  <textarea  read-only  class="TextArea" name="InitiateAction" id="txt_3" disabled="true">$messages3</textarea>
			  <input type="hidden" id = "language_id_3" value="$language_id3">
			<br>
			<div class="errorDiv">
			  <input type="hidden" id = "Msg_3" value="EXISTS_FORWARD_NUMBER">
			  <span class="errorText" id="Error_3"></span>
			  <span class="btnspan" id="Error_3">
			  <input type="button" value="Edit" id="edit_3" onclick="message_edit(3)"><input type="button" value="Save" id="save_3" onclick="check_message(3)" disabled="true"><br>
			  </span>
			</div>
			</form>
			];
			&template_print("template.html",%t);	
}
