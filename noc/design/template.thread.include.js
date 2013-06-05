
function thread_create(div_id,thread_id){
	html = "";
	html += "<div class=thread_messages id='thread_"+thread_id+"_messages'>loading...</div>";
	$('#'+div_id).html(html);
	thread_messages_get(thread_id);
}
function thread_message_add(thread_id,message){
	$.ajax({
		type: 'GET',
		url: '/noc/thread.cgi',
		data: 'thread_id='+thread_id+'&action=message_add&message='+message,
		//data: 'thread_id='+thread_id+'&action=message_add&message='+encodeURI(message),
		success: function(html){  
			thread_messages_get(thread_id);
			MyDisplay('thread_'+thread_id+'_form',0);
		}
	});
}
function thread_messages_get(thread_id,page){
	//$('#thread_'+thread_id+'_messages').html("Loading...");
	$.ajax({
		type: 'GET',
		url: '/noc/thread.cgi',
		data: 'thread_id='+thread_id+'&thread_page='+page+'&action=messages_list',
		success: function(html){  $('#thread_'+thread_id+'_messages').html(html);}
	});
	
}



	


