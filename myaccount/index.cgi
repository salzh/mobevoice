#!/usr/bin/perl
require "../include.cgi";




#=======================================================
# main loop
#=======================================================
$my_url = "index.cgi";
$action = $form{action};
if ($app{session_status} eq 1) {
	if    ($action eq "overview")					{ &do_overview();					}
	elsif ($action eq "get_real_ani")				{ &do_get_real_ani();				}
	elsif ($action eq "setup")						{ &do_setup();						}
	elsif ($action eq "calls")						{ &do_calls();						}
	elsif ($action eq "alerts")						{ &do_alerts();						}
	elsif ($action eq "commissions")				{ &do_commissions();				}
	elsif ($action eq "commissions_request_check")	{ &do_commissions_request_check();	}
	elsif ($action eq "friends")					{ &do_friends();					}
	elsif ($action eq "friends_js")					{ &do_friends_js();					}
	elsif ($action eq "credits")					{ &do_credits();					}
	elsif ($action eq "credits_profile")			{ &ip_flood_surge_protection("Credits profile"); 			&do_credits_profile();				}
	elsif ($action eq "credits_buy_cim_manual")		{ &ip_flood_surge_protection("Credits buy manual"); 		&do_credits_buy_cim_manual();		}
	elsif ($action eq "credits_buy_cim_automatic")	{ &ip_flood_surge_protection("Credits buy automatic"); 		&do_credits_buy_cim_automatic();	}
	elsif ($action eq "credits_buy_commission")		{ &ip_flood_surge_protection("Credits buy commission"); 	&do_credits_buy_commission();		}
	elsif ($action eq "credits_affiliate")			{ &do_credits_affiliate();																		}
	elsif ($action eq "profile")					{ &do_profile();																				}
	elsif ($action eq "sendemail")					{ &ip_flood_surge_protection("Send email"); 				&do_sendemail();					}
	elsif ($action eq "logout")						{ &do_logout();																					}
	elsif ($action eq "imagecheck")					{ &imagecheck_get_image($form{id});exit;														}
	elsif ($action eq "service_add")				{ &do_service_add();																			}
	elsif ($action eq "login")					{ &ip_flood_surge_protection("Login");  &do_login();											}
	elsif ($action eq "login_restore")				{ &ip_flood_surge_protection("restore password"); 			&do_login_restore();				}
	elsif ($action eq "coupons")					{ &do_coupons();																				}	
	elsif ($action eq "service_alert_unset")		{ &do_service_alert_unset();																	}
	elsif ($action eq "service_alert_emailquestion"){ &do_service_alert_emailquestion();															}
	elsif ($action eq "service_alert_namequestion") { &do_service_alert_namequestion();																}
	elsif ($action eq "credits_buy_cim_phone") 		{ &ip_flood_surge_protection("Credits enable phone"); 		&do_credits_buy_cim_phone();		}
	else											{ &do_overview();																				}
} else {
	if 		($action eq "logout")					{ &do_logout();																					}
	elsif	($action eq "imagecheck")				{ &imagecheck_get_image($form{id});exit;														}
	elsif 	($action eq "service_add")				{ &ip_flood_surge_protection("Service add"); 				&do_service_add();					}
	elsif 	($action eq "login")					{ &ip_flood_surge_protection("Login");	&do_login();						}	
	elsif 	($action eq "login_restore")			{ &ip_flood_surge_protection("Restore password"); 			&do_login_restore();				}
	else											{ &ip_flood_surge_protection("Login");  &do_login();						}
}
exit;
#=======================================================



#=======================================================
# service_alert
#=======================================================
# we have a yellow tab at top of all myaccount pages
# to always ask email and name in case no service email 
# or name in databas. We use this litle guys bellow to 
# handle this task. 
# Login action use this things to setup top yellow box question
#=======================================================
sub do_service_alert_check_email_or_name_question(){
	local($service_name,$service_email,$service_id,$tmp1,$tmp2,$tmp3,$tmp,$sql,%hash,$refer);
	$service_id = &clean_int($app{session_cookie_u});
	%hash = database_select_as_hash("SELECT 1,1,name,email FROM service where id='$service_id' ","flag,name,email");
	if ($hash{1}{flag} eq 1) {
		$service_name	= $hash{1}{name};
		$service_email	= $hash{1}{email};
		$tmp = "";
		$tmp = ($service_name eq "") ? "namequestion" : $tmp;
		$tmp = ($service_email eq "") ? "emailquestion" : $tmp;
		&session_set($app{session_cookie_k},"service_alert"	,$tmp);
	}
}
sub do_service_alert_unset(){
	local($tmp1,$tmp2,$tmp3,$tmp,$sql,%hash,$refer);
	$refer = $ENV{HTTP_REFERER} || "index.cgi";
	&session_set($app{session_cookie_k},"service_alert","");
	&cgi_redirect($refer);
}
sub do_service_alert_emailquestion(){
	local($service_name,$service_email,$service_id,$tmp1,$tmp2,$tmp3,$tmp,$sql,%hash,$refer);
	$refer = $ENV{HTTP_REFERER} || "index.cgi";
	#
	# we gonna disable the hability to return to previous page in this form so we can use it in sign-in page and at yellow top bar also
	# its just to avoid send client back to sign-in page in case he enter email at sign-in page
	$refer = "index.cgi";
	#
	$service_id = &clean_int($app{session_cookie_u});
	%hash = database_select_as_hash("SELECT 1,1,name,email FROM service where id='$service_id' ","flag,name,email");
	if ($hash{1}{flag} eq 1) {
		$service_name	= $hash{1}{name};
		$service_email	= $hash{1}{email};
		if ($service_email eq "") {
			$user_email = clean_str(substr($form{email},0,100),"+.()-=[]?><#\@");
			if ( ($user_email ne "") && (index($user_email,"\@") ne -1) && (index($user_email,"\@") eq rindex($user_email,"\@"))  && (index($user_email,".") ne -1) ){
				$tmp = &database_escape($user_email);
				&database_do("update service set email='$tmp' where id='$service_id' ");
				$service_email = $user_email;
				&session_set($app{session_cookie_k},"service_email",$service_email);
				#
				# sounds its first time we apply email on this service. 
				# better send welcome message with PIN
				%hash = database_select_as_hash("SELECT 1,1,pin FROM service_pin where service_id='$service_id' ","flag,pin");
				$service_pin = ($hash{1}{flag} eq 1) ? &format_pin($hash{1}{pin}) : "";
				%email = ();
				$email{to}				= $service_email;
				$email{template}		= "service.add";			 
				$email{dic}{pin}		= $service_pin;
				$email{dic}{email}		= $service_email;			 
				&multilevel_send_email(%email);
				&action_history("status:signin:pin:email:ok",('service_id'=>$service_id,,'value_old'=>$email{dic}{email},'value_new'=>$email{dic}{pin}));
			}
		}
		$tmp = "";
		$tmp = ($service_name eq "") ? "namequestion" : $tmp;
		$tmp = ($service_email eq "") ? "emailquestion" : $tmp;
		&session_set($app{session_cookie_k},"service_alert"	,$tmp);
	}
	&cgi_redirect($refer);
}
sub do_service_alert_namequestion(){
	local($service_name,$service_email,$service_id,$tmp1,$tmp2,$tmp3,$tmp,$sql,%hash,$refer);
	$refer = $ENV{HTTP_REFERER} || "index.cgi";
	$service_id = &clean_int($app{session_cookie_u});
	%hash = database_select_as_hash("SELECT 1,1,name,email FROM service where id='$service_id' ","flag,name,email");
	if ($hash{1}{flag} eq 1) {
		$service_name	= $hash{1}{name};
		$service_email	= $hash{1}{email};
		if ($service_name eq "") {
			$user_name = clean_str(substr($form{name},0,100),"+.()-=[]?><#\@ ");
			if ( ($user_name ne "") ){
				$tmp = &database_escape($user_name);
				&database_do("update service set name='$tmp' where id='$service_id' ");
				$service_name = $user_name;
				&session_set($app{session_cookie_k},"service_name",$service_name);
			}
		}
		$tmp = "";
		$tmp = ($service_name eq "") ? "namequestion" : $tmp;
		$tmp = ($service_email eq "") ? "emailquestion" : $tmp;
		&session_set($app{session_cookie_k},"service_alert"	,$tmp);
	}
	&cgi_redirect($refer);
}
#=======================================================


#=======================================================
# actions
#=======================================================
sub do_coupons(){
	#
	#-----------------------------------------------------------
	# In future, show all coupons and request new ones.
	# Now, only request auto recharge coupon.
	# Status will be in auto recharge page.
	#-----------------------------------------------------------
	#
	#-----------------------------------------------------------
	# start 
	#-----------------------------------------------------------
    %t = %template_default;
	%coupon_to_assign = ();
	$coupon_to_assign{found} = 0;
	$coupon_to_assign{ok_to_assign} = 0;
	#
	#-----------------------------------------------------------
	# check if we can ofer auto-recharge coupon
	#-----------------------------------------------------------
	if (&multilevel_coupon_engine_autorecharge_can_assign($app{service_id}) eq 1) {
		#--------------------------
		# le os dados do coupon
		#--------------------------
		$sql = "
		select
			1,1,
			service_coupon_type.id,
			service_coupon_type.ui_msg_in_stock,
			service_coupon_type.ui_msg_out_stock,
			service_coupon_type.ui_msg_assigned
		from
			service,service_status,service_coupon_type
		where
			service.id='$app{service_id}'
			and service.status=service_status.id 
			and service_status.coupon_id_auto_recharge_signin = service_coupon_type.id
			and service_coupon_type.auto_pause_engine='autorecharge'
		";
		%hash = database_select_as_hash($sql,"flag,type_id,msg_in_stock,msg_out_stock,msg_assigned");
		if ($hash{1}{flag} eq 1) {
			$coupon_to_assign{found} = 1;
			$coupon_to_assign{type_id}			= $hash{1}{type_id};
			$coupon_to_assign{msg_in_stock}		= $hash{1}{msg_in_stock};
			$coupon_to_assign{msg_out_stock}	= $hash{1}{msg_out_stock};
			$coupon_to_assign{msg_assigned}		= $hash{1}{msg_assigned};
			#--------------------------
			# pre-rquisitos: in stock
			#--------------------------
			$sql = "
			select
				1,1,count(*)
			from
				service,
				service_status,
				service_coupon_type,
				service_coupon_stock,
				service_coupon_stock_status
			where
				service.id='$app{service_id}'
				and service.status=service_status.id 
				and service_status.coupon_id_auto_recharge_signin = service_coupon_type.id
				and service_coupon_type.auto_pause_engine='autorecharge'
				and service_coupon_stock.coupon_type_id = service_coupon_type.id
				and service_coupon_stock.status = service_coupon_stock_status.id
				and service_coupon_stock_status.is_ready_to_assign = 1
			";
			%hash = database_select_as_hash($sql,"flag,qtd");
			$coupon_to_assign{in_stock} = ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} >=1 ) ) ? 1 : 0;
			$coupon_to_assign{stock_qtd} = ($hash{1}{flag} eq 1) ? $hash{1}{qtd} : 0;
			$coupon_to_assign{pre_requisite_1} = $coupon_to_assign{in_stock};
			#--------------------------
			# pre-rquisitos: Its a new client (never got this coupon)
			#--------------------------
			$coupon_to_assign{pre_requisite_2} = 1;
			#--------------------------
			# pre-rquisitos: tem CC profile
			#--------------------------
			%hash = &multilevel_securedata_cc_get($app{service_id});
			$coupon_to_assign{pre_requisite_3} = ($hash{status_ok} eq 1) ? 1 : 0;
			#--------------------------
			# pre-rquisitos: auto recharge ta enabled
			#--------------------------
			%hash = database_select_as_hash("SELECT 1,1,cc_fingerprint,is_auto_recharge FROM service_profile_cc where service_id='$app{service_id}' and active=1","flag,cc_fingerprint,value");
			$coupon_to_assign{pre_requisite_5} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} eq 1) ) ? 1 : 0;
			$coupon_to_assign{autorecharge_cc_fingerprint} = ($hash{1}{flag} eq 1) ? $hash{1}{cc_fingerprint} : "";
			#--------------------------
			# pre-rquisitos: its a new card
			#--------------------------
			%hash = database_select_as_hash("select 1,1,count(*) from service_coupon_stock where cc_fingerprint='$coupon_to_assign{autorecharge_cc_fingerprint}'","flag,qtd");
			$coupon_to_assign{pre_requisite_4} = ( ($coupon_to_assign{pre_requisite_3} eq 1) && ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ) ? 1 : 0;
			#$coupon_to_assign{pre_requisite_4} = ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ) ? 1 : 0;
			#--------------------------
			# pre-rquisitos: check all 
			#--------------------------
			$coupon_to_assign{ok_to_assign} = ($coupon_to_assign{pre_requisite_1}.$coupon_to_assign{pre_requisite_2}.$coupon_to_assign{pre_requisite_3}.$coupon_to_assign{pre_requisite_4}.$coupon_to_assign{pre_requisite_5} eq "11111") ? 1 : 0;
		}
		#--------------------------
		# coloca no template
		#--------------------------
		foreach (sort keys %coupon_to_assign) {
			$t{dic}{"coupon_to_assign_".$_} = $coupon_to_assign{$_};
			$t{dic}{debug} .= "coupon_to_assign ($_) = ($coupon_to_assign{$_})<br>";
		}
	}
	#
	#-----------------------------------------------------------
	# try to assign auto recharge
	#-----------------------------------------------------------
	if ( ($form{assign} eq 1) && ($coupon_to_assign{ok_to_assign} eq 1) ) {
		# assigna o auto recharge coupon
		%coupon_now = ();
		$coupon_now{service_id}		= $app{service_id};
		$coupon_now{coupon_type_id}	= $coupon_to_assign{type_id};
		$coupon_now{cc_fingerprint}	= $coupon_to_assign{autorecharge_cc_fingerprint};
		%coupon_now = &multilevel_coupon_assign(%coupon_now);
		if ($coupon_now{ok} eq 1) {
		#---------------------------------
		# by yang ,if auto recharge coupon ,the value is  minutes,so cannot use _next_slice function now
		#	if (&multilevel_coupon_next_slice($coupon_now{coupon_stock_id})>0){
		#---------------------------------
			if (1)  {
				&active_session_delete("service_message");
				&cgi_redirect("$my_url?action=coupons&assigned=1");
				exit;
			}
		}
	}
	#
	#-----------------------------------------------------------
	# pega coupons ativos
	#-----------------------------------------------------------
	$sql = "
	select
		service_coupon_stock.id,
		unix_timestamp(service_coupon_stock.slice_timestamp),
		service_coupon_type.title,
		service_coupon_stock_status.title
	from
		service,
		service_coupon_type,
		service_coupon_stock,
		service_coupon_stock_status
	where
		service.id='$app{service_id}'
		and service.id = service_coupon_stock.service_id
		and service_coupon_stock.coupon_type_id = service_coupon_type.id
		and service_coupon_stock.status = service_coupon_stock_status.id
	";
	%hash = database_select_as_hash($sql,"timestamp,title,status");
	$tmp  = "<tr><td colspan=4><center>Empty...</center></td></tr>";
	foreach $id (sort{$hash{$b}{timestamp} <=> $hash{$a}{timestamp}} keys %hash){
		$tmp = "";
		$t{dic}{coupons_list} .= "<tr>";
		$t{dic}{coupons_list} .= "<td class=al style='border-left:0px;'>".&format_time_gap($hash{$id}{timestamp})."</td>";
		$t{dic}{coupons_list} .= "<td>$hash{$id}{title}</td>";
		$t{dic}{coupons_list} .= "<td>$hash{$id}{status}</td>";
		$t{dic}{coupons_list} .= "</tr>";
	}
	$t{dic}{coupons_list} .= $tmp;
	#
	#-----------------------------------------------------------
	# print page
	#-----------------------------------------------------------
	$t{dic}{coupon_to_assign_was_assigned} = ($form{assigned} eq 1) ? 1 : "";
    &template_print("template.myaccount.coupons.html",%t);
}
sub do_get_real_ani(){
	#
	#--------------------
	# print page
	#--------------------
	%t = %template_default;
	$t{dic}{my_url}			= $my_url;
	&template_print("template.get.real.ani.html",%t);
	exit;	
}
sub do_login_restore(){
	#
	#--------------------
	# start
	#--------------------
	$query = trim(substr(&clean_str($form{query},"._-@+"),0,100));
	%t = %template_default;
	$t{error}		= 0;
	#
	#--------------------
	# check data
	#--------------------
	if ($query ne "") {
		#
		#--------------------
		# imagecheck
		#--------------------
		if ($app{use_imagecheck} eq 1) {
			if 		($form{img_key} eq "")  								{$t{error}=1;}
			elsif	($form{img_uid} eq "") 									{$t{error}=1;}
			elsif 	(imagecheck_check($form{img_uid},$form{img_key}) ne 1)	{$t{error}=1;}
			&imagecheck_check($form{img_uid});
		}
		#
		#--------------------
		# query by ani
		#--------------------
		if ($t{error} eq 0)  {
			$t{DEBUG} .= "serch service by ani<br>";
			($e164flag,$e164number,$e164country) = multilevel_check_E164_number(&clean_int($query)); 
			$sql = "
			SELECT  
				1,1,service.id,service_pin.pin,service.name,service.email
			FROM 
				service,service_ani,service_pin,service_status
			WHERE
				service.id=service_ani.service_id and 
				service.id=service_pin.service_id and 
				service.status = service_status.id and 
				service_status.can_web_access = 1 and 
				service_ani.ani = '$e164number'
			";
			%hash = database_select_as_hash($sql,"flag,id,pin,name,email");
			if ( ($hash{1}{flag} eq 1) && ($hash{1}{id} ne "") && ($hash{1}{pin} ne "") ) {
				&dial_and_play_code($e164number, &format_pin($hash{1}{pin}) );
				&action_history("login:requestpin",('service_id'=>$hash{1}{id},'value_old'=>$e164number,'value_new'=>$ENV{REMOTE_ADDR}));
				&cgi_redirect("$my_url?action=login&message=pin_by_dial&key=".&format_E164_number($e164number,"USA"));
				exit;
			} else {
				&action_history("login:requestpin:error",('value_old'=>$e164number,'value_new'=>$ENV{REMOTE_ADDR}));
				$t{error} = 2;
			}
		}
	}
	#
	#--------------------
	# print restore page
	#--------------------
	$t{img_uid}		= imagecheck_new();
	$t{my_url}		= $my_url;
	&template_print("template.myaccount.login.restore.html",%t);
	exit;
}
sub do_login() {
	%t = %template_default;
	$t{error}	= 0;
	$t{ok_pin}	= 0;
	$t{ok_key}	= 0;
	$t{duplicate_email} =0;
	$t{duplicate_ani} = 0;
	#
	#--------------------------------
	# imagecheck if flood
	#--------------------------------
	($ip_flood_counter_minute,$tmp) = &ip_flood_counter();
	$app{use_imagecheck} = ($ip_flood_counter_minute>=3) ? 1 : 0;
	$suspicious_ips = &data_get("adm_data","security","suspicious_ips");
	$app{use_imagecheck} = (index($suspicious_ips,",$ENV{REMOTE_ADDR},") ne -1) ? 1 : $app{use_imagecheck};
	$t{need_full_pin} = ($app{use_imagecheck} eq 1) ? 1 : 0;
	#
	#
	#--------------------------------
	# login
	#--------------------------------
	if (  ($form{key} ne "") && ($form{pin} ne "")  ) {
		#
		#--------------------------------
		# image check
		#--------------------------------
		if ($app{use_imagecheck} eq 1) {
			if 		($form{img_key} eq "")  								{$t{error}=1}
			elsif	($form{img_uid} eq "") 									{$t{error}=1}
			elsif 	(imagecheck_check($form{img_uid},$form{img_key}) ne 1)	{$t{error}=1}
			&imagecheck_check($form{img_uid});
		}
		#
		#--------------------------------
		# check basic
		#--------------------------------
		if ($t{error} eq 0) {
			$form{pin} = &trim($form{pin});
			$form{key} = &trim($form{key});
			if ($form{key} eq "") {	$t{error} = 2; }
			if ($form{pin} eq "") { $t{error} = 2; }
		}
		#
		#--------------------------------
		# check pin
		#--------------------------------
		$form{pin} = substr(&clean_int($form{pin}),0,100);
		#--------------------------------
		# check key is email or ANI
		#--------------------------------
		$t{form_key} = substr($form{key},0,100);
		$t{form_key_clean} = clean_str($t{form_key},"._-()[]\@");
		$t{form_key_int} = clean_int($t{form_key});
		$keyisemail = (index($t{form_key_clean},"\@") ne -1) ? 1: 0;
		if ($t{error} eq 0) {
			$t{error} = 3;
			if ($keyisemail) {
				$tmp = &database_escape($t{form_key_clean});
				if ( (length($form{pin}) ne 4) || ($t{need_full_pin} eq 1) ) {
					$sql = "
					SELECT service.id,1,service.id,service.name,service.email 
					FROM service,service_pin,service_status,product
					WHERE 
					service_pin.pin = '$form{pin}' and			
					service_pin.service_id = service.id and 
					service.status = service_status.id and 
					service.product_id = product.id and 
					service_status.can_web_access = 1 and 
					service_status.deleted = 0 and
					service.email ='$tmp' 
					";
				} else {
					$sql = "
					SELECT service.id,1,service.id,service.name,service.email 
					FROM service,service_pin,service_status,product
					WHERE 
					right(service_pin.pin,4) = '$form{pin}' and			
					service_pin.service_id = service.id and 
					service.status = service_status.id and 
					service.product_id = product.id and 
					service_status.can_web_access = 1 and 
					service_status.deleted = 0 and
					service.email ='$tmp' 
					";
				}
				%hash = database_select_as_hash($sql,"flag,id,name,email");
			 	foreach (sort keys %hash) {
						$firstrecord{id} 	= $hash{$_}{id};
						$firstrecord{flag}	= $hash{$_}{flag};
						$firstrecord{name}	= $hash{$_}{name};
						$firstrecord{email}	= $hash{$_}{email};
						#$firstrecord{ani}	= $hash{$_}{ani};
						last;
				}
				$num_records =  keys( %hash ) ;
				#warning( "size of hash:  " . $num_records . ".\n");
				if ($num_records > 1) {
					# duplicate PIN+EMAIL ,we need ask user retry with ANI+PIN
					$t{error} 			= 17;
					$t{duplicate_email}	= 1;
					$t{need_full_pin}	= 1;
  				} elsif ($firstrecord{flag} eq 1) {
					$t{service_found}	= 1;
					$t{service_id}		= $firstrecord{id};
					$t{service_name}	= $firstrecord{name};
					$t{service_email}	= $firstrecord{email};
					$t{error} 			= 0;
					$t{ok_pin}			= 1;
					$t{ok_key}          = 1;
				}else {
					# no such record(PIN+EMAIL)			 
					$t{error} = 16;
				}
			} else {
				#
				# busca por ANI
				($t{form_key_flag},$t{form_key_e164},$t{form_key_country}) = &multilevel_check_E164_number($t{form_key_int});
				if ( ($t{form_key_flag} eq "OK") && ($t{form_key_int} ne "") ) {
					if ( (length($form{pin}) ne 4) || ($t{need_full_pin} eq 1) ) {
						$sql = "
						SELECT service.id,1,service.id,service.name,service.email,service_ani.ani 
						FROM service,service_pin,service_status,product,service_ani 
						WHERE 
						service_pin.pin = '$form{pin}' and
						service_ani.ani = '$t{form_key_e164}' and
						service_pin.service_id = service.id and 
						service.status = service_status.id and 
						service.product_id = product.id and 
						service_status.can_web_access = 1 and 
						service_status.deleted = 0 and
						service_ani.service_id  = service.id  
						";
					} else {
						$sql = "
						SELECT service.id,1,service.id,service.name,service.email,service_ani.ani 
						FROM service,service_pin,service_status,product,service_ani 
						WHERE 
						right(service_pin.pin,4) = '$form{pin}' and
						service_ani.ani = '$t{form_key_e164}' and
						service_pin.service_id = service.id and 
						service.status = service_status.id and 
						service.product_id = product.id and 
						service_status.can_web_access = 1 and 
						service_status.deleted = 0 and
						service_ani.service_id  = service.id  
						";
					}
					%hash = database_select_as_hash($sql,"flag,id,name,email,ani");
					foreach (sort keys %hash) {
						$firstrecord{id}	= $hash{$_}{id};
						$firstrecord{flag}	= $hash{$_}{flag};
						$firstrecord{name}	= $hash{$_}{name};
						$firstrecord{email}	= $hash{$_}{email};
						$firstrecord{ani}	= $hash{$_}{ani};
						last;
					}
					#$debug .= "CALL DUMP =$firstrecord{flag},$firstrecord{id},$firstrecord{name},$firstrecord{email}<br>";
					#$debug .= "<br>";
					#warning( "debug:  " . $debug . ".\n");
					$num_records =  keys( %hash ) ;
					#warning( "size of hash:  " . $num_records .".\n");
					if ($num_records > 1) {
						#duplicate ANI+PIN ,ask user retry login with EMAIL+PIN
						$t{error} 			= 18;
						$t{duplicate_ani}   = 1;
						$t{need_full_pin}	= 1;
  					}  elsif ($firstrecord{flag} eq 1) {				 
						$t{service_found}	= 1;
						$t{service_id}		= $firstrecord{id};
						$t{service_name}	= $firstrecord{name};
						$t{service_email}	= $firstrecord{email};
						$t{service_ani}	    = $firstrecord{ani};
						$t{error} 			= 0;
						$t{ok_pin}			= 1;
						$t{ok_key}          = 1;
					} else {
						# PIN+ ANi not found
						$t{error} = 5;
					}
				} else {
					# unknown ANI format
					$t{error} = 4;
				}
			}
		}
		#
		#--------------------------------
		# if ok, atach session and kick user to first page
		#--------------------------------
		if ( ($t{error} eq 0) && ($t{ok_pin} eq 1) && ($t{ok_key} eq 1) ){
			#
			# try to attach session
			if (&session_attach($t{service_id}) eq 1) {
				&action_history("login:ok",('service_id'=>$t{service_id}));
				#
				# add some extra values to session (and avoid re-query each access)
				&session_set($app{session_cookie_k},"service_name"	    ,$t{service_name});
				&session_set($app{session_cookie_k},"service_email"	    ,$t{service_email});
				if ($t{form_key_e164} ne "") {
					&session_set($app{session_cookie_k},"service_ani"	    ,&format_E164_number($t{form_key_e164},"USA"));
					&session_set($app{session_cookie_k},"service_ani_e164"	,$t{form_key_e164});
				}
				#
				# add flags to ask email and/or name at top yellow bar
				$tmp = "";
				$tmp = ($t{service_name} 	eq "") ? "namequestion" : $tmp;
				$tmp = ($t{service_email} 	eq "") ? "emailquestion" : $tmp;
				&session_set($app{session_cookie_k},"service_alert"	,$tmp);
				#
				# strong redirect and stop program
				$url_to_send = "index.cgi";
				print "content-type: text/html\n\n"; 
				print qq[
				<html><head>
				<META HTTP-EQUIV="Expires" CONTENT="0">
				<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate">
				<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
				<META HTTP-EQUIV="Refresh" CONTENT="0;URL=$url_to_send">
				</head><body><script>window.location='$url_to_send'</script></body></html>	
				];
				exit;
			} else {
				# 
				# oops! problems try to attach session. 
				# because we have service_id, lets just log
				if ($t{service_id} ne "") {
					&action_history("login:error",('service_id'=>$t{service_id}, 'value_old'=>$form{key},'value_new'=>$ENV{REMOTE_ADDR}));
				} else {
					&action_history("login:error",('value_old'=>$form{key},'value_new'=>$ENV{REMOTE_ADDR}));
				}
				$t{error} = 7;
			}
		} else {
			# 
			# we have a login fail by user input.
			# to make log usefull, lets try to guess service_id 
			#
			$tmp_service_id = $t{service_id};
			#
			# try guess service_id by ANI
			if ( ($tmp_service_id eq "") && (index($t{form_key_clean},"\@") eq -1) && (length($t{form_key_int})>4) ) {
				($tmp1,$tmp2,$tmp3) = &multilevel_check_E164_number($t{form_key_int});
				if ($tmp1 eq "OK") {
					$sql = "SELECT 1,1,service_id FROM service_ani WHERE ani = '$tmp2' ";
					%hash = database_select_as_hash($sql,"flag,id");
					$tmp_service_id = ( ($hash{1}{flag} eq 1) && ($hash{1}{id} ne "") ) ? $hash{1}{id} : "";
				}
			}
			#
			# try guess service_id by PIN 
			if ( ($tmp_service_id eq "") && (length($form{pin})>4) ) {
				$sql = " SELECT 1,1,service_id FROM service_pin WHERE pin = '$form{pin}' ";
				%hash = database_select_as_hash($sql,"flag,id");
				$tmp_service_id = ( ($hash{1}{flag} eq 1) && ($hash{1}{id} ne "") ) ? $hash{1}{id} : "";
			}
			#
			# try guess by email
			if ( ($tmp_service_id eq "") && (index($t{form_key_clean},"\@") ne -1) && (length($t{form_key_clean})>4) ) {
				$tmp = &database_escape($t{form_key_clean});
				$sql = "SELECT 1,1,id FROM service WHERE email='$tmp' order by last_change desc limit 0,1 ";
				%hash = database_select_as_hash($sql,"flag,id");
				$tmp_service_id = ( ($hash{1}{flag} eq 1) && ($hash{1}{id} ne "") ) ? $hash{1}{id} : "";
			}
			#
			# log
			if ($tmp_service_id ne "") {
	 			&action_history("login:error",('service_id'=>$tmp_service_id, 'value_old'=>$t{form_key_clean},'value_new'=>$ENV{REMOTE_ADDR}));
			} else {
				&action_history("login:error",('value_old'=>$t{form_key_clean},'value_new'=>$ENV{REMOTE_ADDR}));
			}
			$t{error} = ($t{error} eq 0) ? 8 : $t{error};
		}
		$form{key} = "";
	}
	#
	# print page
	$t{imagecheck_active}		= $app{use_imagecheck};
	$t{form_key}				= $form{key};
	if ($app{use_imagecheck} eq 1){
		$t{img_uid}					= imagecheck_new();
	} 
	#
	# pin restore page send this flags by url so we can adjust UI to make system more user-friend
	$t{message_pin_by_dial}		= ($form{message} eq "pin_by_dial") ? 1 : 0;
	$t{message_pin_by_email}	= ($form{message} eq "pin_by_email") ? 1 : 0;
	$t{my_url}					= $my_url;
	#
	# debug that we need only at emergency
	#foreach (sort keys %form){$t{debug}.="FORM --- $_=$form{$_}<Br>"}
	#foreach (sort keys %t){ if ($_ eq "debug"){next}  $t{debug}.="TEMPLATE --- $_=$t{$_}<br>"}
	#foreach (sort keys %ENV){$t{debug}.="ENV --- $_=$ENV{$_}<Br>"}
	#
	# print template
	&template_print("template.myaccount.login.html",%t);
}
sub do_logout(){
	session_detach();
	$url = $my_url;
	#if ($form{url} eq "") {$url = $ENV{HTTP_REFERER};}
	print "content-type: text/html\n\n"; 
	print qq[
	<html><head>
	<META HTTP-EQUIV="Expires" CONTENT="0">
	<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate">
	<META HTTP-EQUIV="Pragma" CONTENT="no-cache">
	<script>window.location="$url"</script>
	</head><body>logout</body></html>	
	];
	exit;
}
sub do_service_add() {
	 $refcode = $form{referal};
     print "location:/myaccount/service.pbx.cgi?action=add&referal=$refcode\n\n";
        
	exit;
    #
    # start some things
    %t = %template_default;
	#
	#--------------------------------
	# pega invite
	#--------------------------------
	%invite = ();
	$invite{ok} = 0;
	$buf = $cookie{"i"};
	$buf = ($buf eq "") && ($form{invite} ne "") ? $form{invite} : $buf;
	$buf = clean_str(substr($buf,0,100),"-_","MINIMAL");
	$buf = (length($buf) < 3) ? "" : $buf;
	$buf = (length($buf) > 20) ? "" : $buf;
	if ($buf ne "") {
		$sql = "
			select 
				1,1,
				service.id,
				service.name,
				service_status.refer_status
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
				service_invite.id = '$buf'
			";
		%hash = database_select_as_hash($sql,"flag,id,name,referral_status");
		if ($hash{1}{flag} eq 1) {
			$invite{ok}				= 1;
			$invite{id}				= $buf;
			$invite{service_id}		= $hash{1}{id};
			$invite{service_name}	= $hash{1}{name};
			$invite{service_referral_status}= $hash{1}{referral_status};
		}
        $invite{no_invite}=0;
        if( $buf eq "soup" ) {$invite{no_invite}=1;};
        
	}
	#
	#--------------------------------
	# get coupon
	#--------------------------------
	%coupon = ();
	$coupon{exists}		= 0;
	$coupon{in_stock}	= 0;
	$coupon{stock_qtd}	= 0;
	if ( ($invite{ok} eq 1) && ($invite{service_referral_status} ne "") && ($invite{service_referral_status} > 0) ) {
		$sql = "
		select 
			1,1,
			service_coupon_type.id,
			service_coupon_type.title,
			service_coupon_type.ui_msg_in_stock,
			service_coupon_type.ui_msg_out_stock,
			service_coupon_type.ui_msg_assigned
		from 
			service_status,service_coupon_type,service_coupon_type_status
		where 
			service_status.id='$invite{service_referral_status}' and 
			service_status.coupon_id_new_service = service_coupon_type.id and 
			service_coupon_type.status = service_coupon_type_status.id and 
			service_coupon_type_status.is_active = 1
		";
		%hash = database_select_as_hash($sql,"flag,id,title,msg_in_stock,msg_out_stock,msg_assigned");
		if ($hash{1}{flag} eq 1) {
			$coupon{exists}			= 1;
			$coupon{type_id}		= $hash{1}{id};
			$coupon{title}			= $hash{1}{title};
			$coupon{msg_in_stock}	= $hash{1}{msg_in_stock};
			$coupon{msg_out_stock}	= $hash{1}{msg_out_stock};
			$coupon{msg_assigned}	= $hash{1}{msg_assigned};
			#$sql = "
			#select 1,1,count(*)
			#from 
			#	service,
			#	service_status,
			#	service_coupon_type,
			#	service_coupon_type_status,
			#	service_coupon_stock,
			#	service_coupon_stock_status
			#where 
			#	service.id='$invite{service_id}' and 
			#	service.status=service_status.id and 
			#	service_status.coupon_id_new_service = service_coupon_type.id and 
			#	service_coupon_type.status = service_coupon_type_status.id and 
			#	service_coupon_type_status.is_active = 1 and 
			#	service_coupon_type.id = service_coupon_stock.coupon_type_id and 
			#	service_coupon_stock.status = service_coupon_stock_status.id and 
			#	service_coupon_stock_status.is_ready_to_assign
			#";
			$sql = "
			select 1,1,count(*)
			from 
				service_coupon_stock,
				service_coupon_stock_status
			where 
				service_coupon_stock.coupon_type_id='$coupon{type_id}' and 
				service_coupon_stock.status = service_coupon_stock_status.id and 
				service_coupon_stock_status.is_ready_to_assign
			";
			%hash = database_select_as_hash($sql,"flag,value");
			if ($hash{1}{flag} eq 1) {
				$coupon{in_stock}	= ($hash{1}{value}>0) ? 1 : 0;
				$coupon{stock_qtd}	= $hash{1}{value};
			}
		}
	}
#warning("coupon_in_stock=$coupon{in_stock}");
#warning("coupon_type_id=$coupon{type_id} - $coupon{stock_qtd}");
#warning("coupon_title=$coupon{title}");
#warning("invite_id=$invite{id}");
#warning("invite_service_id=$invite{service_id}");
#warning("invite_service_name=$invite{service_name}");
#warning("invite_service_referral_status=$invite{service_referral_status}");
	#
	#--------------------------------
	# clean email
	#--------------------------------
	# * Uppercase and lowercase English letters (a-z, A-Z)
    # * Digits 0 through 9
    # * Characters ! # $ % & ' * + - / = ? ^ _ ` { | } ~
    # * Character . (dot, period, full stop) provided that it is not the first or last character, and provided also that it does not appear two or more times consecutively.
	if ( ($form{email} ne "") && (index("$form{email}","\@") eq rindex("$form{email}","\@"))  ){
		($slice1,$slice2) = split(/\@/,$form{email});
		$slice1 = &clean_str(substr("\L$slice1",0,255),"+-_.","MINIMAL");
		$slice2 = &clean_str(substr("\L$slice2",0,255),".-","MINIMAL");
		if ($slice2 eq "gmail.com")  {
			$slice1 = &clean_str("\L$slice1","-_+","MINIMAL");
			if (index($slice1,"+") ne -1) {
				$slice1 = substr($slice1,0,index($slice1,"+"));
			}
		}
		if ($form{email} ne "$slice1\@$slice2") {
			&action_history("security:emailtrick",('value_old'=>$form{email}));
		}

		$form{email} = "$slice1\@$slice2";
	}
	#
	#--------------------------------
	# get mode
	#--------------------------------
	$request_id_from_cookie = substr(&clean_int($cookie{"ir"}),0,255);
	if ($request_id_from_cookie ne ""){
		%hash = database_select_as_hash("select 1,1 from service where id='$request_id_from_cookie' ");
		$request_id_from_cookie = ($hash{1} eq 1) ? $request_id_from_cookie  :   "";
	}
    $t{dic}{mode} = "public_invite_request";
	$t{dic}{mode} = ($form{mode} eq "public_invite_request") ? "public_invite_request" :  $t{dic}{mode};
	$t{dic}{mode} = ($form{mode} eq "public_invite_confirm") ? "public_invite_confirm" :  $t{dic}{mode};
	$t{dic}{mode} = ($invite{ok} ne 1) ? "no_invite" :  $t{dic}{mode};
	$t{dic}{mode} = ($request_id_from_cookie ne "") ? "public_invite_confirm" : $t{dic}{mode};
	$t{dic}{mode} = ($form{mode} eq "public_invite_cancel") ? "public_invite_cancel" :  $t{dic}{mode};
	$t{dic}{mode} = ($form{mode} eq "public_invite_resend") ? "public_invite_resend" :  $t{dic}{mode};
	#
	#--------------------------------
	# mode public_invite_request
	#--------------------------------
    if ($t{dic}{mode} eq "public_invite_request") {
		$t{dic}{ok}						= 0;
		$t{dic}{warning}				= 0;
		$t{dic}{warning_existent_email}	= 0;
		$t{dic}{error}					= 0;
		$t{dic}{error_bad_email}		= 0;
		$form{email} = substr($form{email},0,1024);
		if ($form{save} eq 1) {
			$t{dic}{ok}	= 1;
			#
			# check email
			if ($t{dic}{ok} eq 1){
				if (&form_check_email($form{email}) ne 1){
					$t{dic}{ok}				= 0;
					$t{dic}{error}			= 1;
					$t{dic}{error_bad_email}= 1;
				}
				if (index("$form{email}","\@") ne rindex("$form{email}","\@")) {
					$t{dic}{ok}				= 0;
					$t{dic}{error}			= 1;
					$t{dic}{error_bad_email}= 1;
				}
			}
			#
			# check if email already exist
			if ($t{dic}{ok} eq 1){
				%hash = database_select_as_hash("select 1,1,count(*) from service where email='$form{email}' ", "flag,qtd");
				unless ($hash{1}{flag}.$hash{1}{qtd} eq "10") {
					$t{dic}{ok}						= 0;
					$t{dic}{warning}				= 1;
					$t{dic}{warning_existent_email}	= 1;
				}
			}
			#
			# check bad domains
			if ($t{dic}{ok} eq 1){
				open(IN,"$app_root/data/blocked.email.domains.txt");
				while (<IN>){
					chomp($_);
					$bad_domain = "\@".&trim($_)."|";
					if (index("\L$form{email}|","\L$bad_domain") ne -1) {
						$t{dic}{ok}				= 0;
						$t{dic}{error}			= 1;
						$t{dic}{error_bad_email}= 1;
						last;
					}
				}
				close(IN);
			}
			#
			# try to save
			if ($t{dic}{ok} eq 1){
				#
				# verifica se existe o request
				%hash = database_select_as_hash("SELECT 1,1,id,service_request.key from service_request where email='$form{email}' limit 0,1", "flag,id,key");
				$request_id  = ($hash{1}{flag} eq 1) ? $hash{1}{id} : "";
				$request_key = ($hash{1}{flag} eq 1) ? $hash{1}{key} : "";
				if ($request_id ne "") {
					#
					# se ja existe, atualizar
					database_do("update service_request set date=now(), invite_service_id='$invite{service_id}' where email='$form{email}' "); 
				} else {
					#
					# decidir um confirmation code
					my @chars=('0'..'9');
					$request_key = "";
					foreach (1..4) {$request_key .= $chars[rand @chars];}
					#
					# se nao existe, criar
					$sql = " 
					insert into service_request 
					(  date,   service_request.key,   email,           invite_service_id      ) values 
					(  now(),  '$request_key',        '$form{email}',  '$invite{service_id}'  )
					"; 
					database_do($sql);
					%hash = database_select_as_hash("SELECT 1,LAST_INSERT_ID();");
					$request_id = $hash{1};
				}
				if ($request_id > 1) {
					#
					# envia request por email
					%email = ();
					$email{to}						= $form{email};
					$email{template}				= "service.request";
					$email{dic}{invite_name}		= $invite{name};
					$email{dic}{confirmation_code}	= $request_key;
					$email{dic}{email}				= $form{email};
					&multilevel_send_email(%email);
					&action_history("new:service:request",('value_new'=>$form{email},'value_old'=>$request_key));			
					#
					# grava cookie
					&cookie_save("ir",$request_id,"expires=Sun, 26-Jun-2013 00:00:00 GMT;");
				}
				#
				# redireciona mais uma vez
				&cgi_redirect("$my_url?action=service_add&mode=public_invite_confirm&email=$form{email}");
				exit;
			}
		}
		$t{dic}{form_email}	= $form{email};
	}
	#
	#--------------------------------
	# mode public_invite_cancel
	#--------------------------------
    if ($t{dic}{mode} eq "public_invite_cancel") {
		&cookie_save("ir","","expires=Thu, 31-Dec-2020 00:00:00 GMT;");
		&cgi_redirect("$my_url?action=service_add");
		exit;
	}
	#
	#--------------------------------
	# mode public_invite_resend
	#--------------------------------
    if ($t{dic}{mode} eq "public_invite_resend") {
		#
		# load
		if ($request_id_from_cookie ne "") {
			%hash = database_select_as_hash("select 1,1,email,service_request.key from service_request where id='$request_id_from_cookie' ", "flag,email,key");
			if ($hash{1}{flag} eq 1) {
				if ($hash{1}{email} ne "") {
					%email = ();
					$email{to}						= $hash{1}{email};
					$email{template}				= "service.request";
					$email{dic}{invite_name}		= $invite{name};
					$email{dic}{confirmation_code}	= $hash{1}{key};
					$email{dic}{email}				= $hash{1}{email};
					&multilevel_send_email(%email);
					&action_history("new:service:request");			
				}
			}
		}
		&cgi_redirect("$my_url?action=service_add");
		exit;
	}
	#
	#--------------------------------
	# mode public_invite_confirm
	#--------------------------------
    if ($t{dic}{mode} eq "public_invite_confirm") {
		$t{dic}{ok}						= 0;
		$t{dic}{warning}				= 0;
		$t{dic}{warning_existent_email}	= 0;
		$t{dic}{error}					= 0;
		$t{dic}{error_bad_name}			= 0;
		$t{dic}{error_bad_email}		= 0;
		$t{dic}{error_bad_key}			= 0;
		$t{dic}{error_bad_accept}		= 0;
		$t{dic}{error_unknown_request}	= 0;
		$t{dic}{error_wrong_request}	= 0;
		$t{dic}{error_system}			= 0;
		$t{dic}{request_id}				= "";
		$t{dic}{request_key}			= "";
		$t{dic}{request_invite_service_id}= "";
		$form{email} = substr($form{email},0,1024);
		$form{name} = substr($form{name},0,1024);
		$form{key} = substr($form{key},0,1024);
		if ($form{save} eq 1) {
			$t{dic}{ok}	= 1;
			#
			# check name, email and key
			if ($t{dic}{ok} eq 1){
				if (&form_check_email($form{email}) ne 1){
					$t{dic}{ok}				= 0;
					$t{dic}{error}			= 1;
					$t{dic}{error_bad_email}= 1;
				}
				if (&form_check_string($form{name}) ne 1){
					$t{dic}{ok}				= 0;
					$t{dic}{error}			= 1;
					$t{dic}{error_bad_name}	= 1;
				}
				if (&form_check_string($form{key}) ne 1){
					$t{dic}{ok}				= 0;
					$t{dic}{error}			= 1;
					$t{dic}{error_bad_key}	= 1;
				}
				if ($form{accept} ne 1){
					$t{dic}{ok}					= 0;
					$t{dic}{error}				= 1;
					$t{dic}{error_bad_accept}	= 1;
				}
			}
			#
			# check if email already exist
			if ($t{dic}{ok} eq 1){
				%hash = database_select_as_hash("select 1,1,count(*) from service where email='$form{email}' ", "flag,qtd");
				unless ($hash{1}{flag}.$hash{1}{qtd} eq "10") {
					$t{dic}{ok}						= 0;
					$t{dic}{warning}				= 1;
					$t{dic}{warning_existent_email}	= 1;
				}
			}
			#
			# check request
			if ($t{dic}{ok} eq 1){
				%hash = database_select_as_hash("select 1,1,id,service_request.key,invite_service_id from service_request where email='$form{email}' limit 0,1", "flag,id,key,invite_service_id");
				$t{dic}{request_id}					= ($hash{1}{flag} eq 1) ? $hash{1}{id} : "";
				$t{dic}{request_key}				= ($hash{1}{flag} eq 1) ? $hash{1}{key} : "";
				$t{dic}{request_invite_service_id}	= ($hash{1}{flag} eq 1) ? $hash{1}{invite_service_id} : "";
				if ($t{dic}{request_id} eq "") {
					$t{dic}{ok}						= 0;
					$t{dic}{error}					= 1;
					$t{dic}{error_unknown_request}	= 1;
				} else {
					if ($t{dic}{request_key} ne $form{key}) {
						$t{dic}{ok}						= 0;
						$t{dic}{error}					= 1;
						$t{dic}{error_wrong_request}	= 1;
					}
				}
			}
			#
			# try to save
			if ($t{dic}{ok} eq 1){
				#
				################################################################
				#
				# ADD ACCOUNT FOR PUBLIC INVITE WITH REQUEST OK
				#
				################################################################
				#
				# criar servico (default status=new)
				%data = ();
				$data{name}   				= $form{name};
				$data{email}  				= $form{email};
				$data{parent_service_id} 	= $t{dic}{request_invite_service_id};
				%data = &multilevel_service_create(%data);
				#
				# se ok, terminar o trabalho e login
				if ($data{ok} eq 1) {
					#
					#
					# log action
					&action_history("status:new",('service_id'=>$data{service_id}));
					#
					# verifica se precisa de coupon
#warning("---Servico adicionado---");
#foreach(sort keys %data){warning("DATA $_=$data{$_}");}
#warning("---add coupon---");
#warning("coupon_in_stock=$coupon{in_stock}");
#warning("coupon_type_id=$coupon{type_id}");
#warning("coupon_title=$coupon{title}");
					if ( ($coupon{type_id} ne "") && ($coupon{in_stock} eq 1)  ) {
						# tenta add coupon
						%coupon2 = ();
						$coupon2{service_id}		= $data{service_id};
						$coupon2{coupon_type_id}	= $coupon{type_id};
						%coupon2 = &multilevel_coupon_assign(%coupon2);
#foreach(sort keys %coupon2){warning("coupon2 $_=$coupon2{$_}");}
						if ($coupon2{ok} eq 1) {
							if (&multilevel_coupon_next_slice($coupon2{coupon_stock_id})>0){
								$coupon{assigned}	= 1;
							}
						}
					}
					#
					# mandar email
					%email = ();
					$email{to}				= $data{email};
					$email{template}		= "service.add";
					$email{dic}{invite_ok}	= $invite{ok};
					$email{dic}{invite_id}	= $invite{id};
					$email{dic}{invite_name}= $invite{service_name};
					$email{dic}{pin}		= &format_pin($data{service_pin});
					$email{dic}{email}		= $data{email};
					$email{dic}{name}		= $data{name};
					$email{dic}{free_credit}= ($data{free_credit} > 0) ? &format_number($data{free_credit},2) : "" ;
					&multilevel_send_email(%email);
					&data_set("service_data",$data{service_id},"trigger_nf",1);
					&data_set("service_data",$data{service_id},"trigger_nfof",1);
					&data_set("service_data",$data{service_id},"trigger_nc",1);
					&data_set("service_data",$data{service_id},"trigger_ec",1);
					&data_set("service_data",$data{service_id},"trigger_lb",1);
					&data_set("service_data",$data{service_id},"email_news",1);
					#
					#---------------------------------------------------------------
					# new friend notification
					#---------------------------------------------------------------
					# e avisar por email os que necessitam
					%tmp_hash 			= database_select_as_hash("select 1,1,service.name from service where service.id='$data{invite_service_id}' ","flag,name");
					$notification_invite_name		= ( ($tmp_hash{1}{flag} eq 1) && ($tmp_hash{1}{name} ne "") ) ? $tmp_hash{1}{name} : "";
					$notification_new_friend_name	= $data{name};
					$notification_service_id 		= $data{invite_service_id};
					foreach $notification_proximity_level (0..20) {
						%tmp_hash 					= database_select_as_hash("select 1,1,name,email from service where service.id='$notification_service_id' ","flag,name,email");
						if ($tmp_hash{1}{flag} eq 1) {
							$notification_service_name	= $tmp_hash{1}{name};
							$notification_service_email	= $tmp_hash{1}{email};
							$notification_flag_type 	= ($notification_proximity_level eq 0) ? "trigger_nf" : "trigger_nfof";
							$notification_flag 			= &data_get("service_data",$notification_service_id,$notification_flag_type);
							if ( ($notification_flag eq 1) && ($notification_service_email ne "") ){
								%email = ();
								$email{template}					= ($notification_proximity_level eq 0) ? "alert.new.friend" : "alert.new.friend.of.friend";
								$email{to}							= $notification_service_email;
								$email{dic}{service_name}			= $notification_service_name;
								$email{dic}{new_friend_name}		= &format_trim_name($notification_new_friend_name,	($notification_proximity_level>1)?1:0);
								$email{dic}{invite_name}			= &format_trim_name($notification_invite_name,		($notification_proximity_level>2)?1:0);
								$email{dic}{invite_branch_distance}	= "you";
								$email{dic}{invite_branch_distance}	= ($notification_proximity_level eq 1) ? "your friend" : $email{dic}{invite_branch_distance};
								$email{dic}{invite_branch_distance}	= ($notification_proximity_level eq 2) ? "one person away" : $email{dic}{invite_branch_distance};
								$email{dic}{invite_branch_distance}	= ($notification_proximity_level > 2) ? ($notification_proximity_level-1)." people away" : $email{dic}{invite_branch_distance};
								&multilevel_send_email(%email);
							}
						}
						# get next parent_id
						%tmp_hash = database_select_as_hash("select 1,1,parent_service_id from service_tree where service_id='$notification_service_id'","flag,value");
						if ( ($tmp_hash{1}{flag} eq 1) && ($tmp_hash{1}{value} ne "") ) {
							$notification_service_id = $tmp_hash{1}{value};
						} else {
							last;
						}
					}
					#
					# delete request code
					database_do("delete from service_request where email='$form{email}' "); 
					&cookie_save("ir","","expires=Thu, 31-Dec-2020 00:00:00 GMT;");
					#
					# logar 
					session_attach($data{service_id});
					&session_set($app{session_cookie_k},"service_email"	    ,$data{email});
					&session_set($app{session_cookie_k},"service_name"	    ,$data{name});
					&session_set($app{session_cookie_k},"flag_first_login"	,1);
					#if (&multilevel_coupon_engine_autorecharge_can_assign($data{service_id}) eq 1) {
					#	$sql = "
					#		select 1,1,service_coupon_type.ui_msg_out_stock
					#		from service,service_status,service_coupon_type
					#		where
					#		service.id='$data{service_id}'
					#		and service.status=service_status.id 
					#		and service_status.coupon_id_auto_recharge_signin = service_coupon_type.id
					#		and service_coupon_type.auto_pause_engine='autorecharge'
					#	";
					#	%hash = database_select_as_hash($sql,"flag,msg");
					#	$tmp = ($hash{1}{flag} eq 1) ? $hash{1}{msg} : "You have one promotion waiting for you! <a href=/myaccount/index.cgi?action=coupons>Check it now!</a>";
					#	&session_set($app{session_cookie_k},"service_message",$tmp);
					#}
					#
					# mostrar dados
					$t{dic}{service_name}	= $data{name};
					$t{dic}{service_email}	= $data{email};
					$t{dic}{service_pin}	= &format_pin($data{service_pin});
					$t{dic}{mode} 			= "service_add_ok";
				} else {
					$t{dic}{error}			= 1;
					$t{dic}{error_system}	= 1;
				}
				################################################################
				#
			}
		} else {
			#
			# load
			if ($form{email} eq "") {
				if ($request_id_from_cookie ne "") {
					%hash = database_select_as_hash("select 1,1,email from service_request where id='$request_id_from_cookie' ", "flag,email");
					$form{email} = ($hash{1}{flag} eq 1) ? $hash{1}{email} : "";
				}
			}
		}
		$t{dic}{form_name}	= $form{name};
		$t{dic}{form_email}	= $form{email};
		$t{dic}{form_key}	= $form{key};
		$t{dic}{form_accept}= $form{accept};
	}
    #
	#--------------------------------
    # print page
	#--------------------------------
	$t{dic}{coupon_exists}			= $coupon{exists};
	$t{dic}{coupon_in_stock}		= $coupon{in_stock};
	$t{dic}{coupon_stock_qtd}		= &format_number($coupon{stock_qtd},0);
	$t{dic}{coupon_assigned}		= $coupon{assigned};
	$t{dic}{coupon_type_id}			= $coupon{type_id};
	$t{dic}{coupon_title}			= $coupon{title};
	$t{dic}{coupon_msg_in_stock}	= $coupon{msg_in_stock};
	$t{dic}{coupon_msg_out_stock}	= $coupon{msg_out_stock};
	$t{dic}{coupon_msg_assigned}	= $coupon{msg_assigned};
    $t{dic}{"mode_".$t{dic}{mode}} 	= 1;
    $t{dic}{invite_ok}				= $invite{ok};
    $t{dic}{invite_id}				= $invite{id};
    $t{dic}{invite_name}			= $invite{service_name};
    $t{dic}{my_url}					= $my_url;
    $t{dic}{form_name}				= $form{name};
    $t{dic}{form_email}				= $form{email};
    &template_print("template.services.add.html",%t);
}
sub do_setup(){
	#do_overview();
	cgi_redirect("service.pbx.cgi");
}
sub do_overview() {
	cgi_redirect("service.pbx.cgi");return;
}
sub DELETE_do_profile_cc() {
	#
	#--------------------------
	# start
	#--------------------------
	$answer = 0;
	%hash = database_select_as_hash("select 1,1,service_status.need_ani_check from service,service_status where service.id='$app{service_id}' and service.status=service_status.id ","flag,value");
	$need_ani_confirmation			= ( ($hash{1}{flag} eq 1) && ($hash{1}{value} eq 1) ) ? 1 : 0;
	$need_ask_confirmation_code 	= 0;
	$action_is_confirmation_code	= ($form{form_action} eq "dial") ? 1 : 0;
	$action_is_delete				= ($form{form_action} eq "delete") ? 1 : 0;
	$action_is_save 				= ( ($action_is_confirmation_code eq 0) && ($action_is_delete eq 0) ) ? 1 : 0;
	#
	# CC profile ALWAYS need ani conirmation..
	# sure we did not need ask for already confirmated numbers
	$need_ani_confirmation			= 1;
	#cgi_hearder_html();
	#print "<script>parent.billing_cc_answer(1000);</script><font size=1>$form{form_action} - dial=$is_confirmation_code - delete=$is_delete - save=$is_save<br>";
	#foreach (sort keys %form) {print "FORM $_=$form{$_}<br>"}
	#exit;
	#
	#--------------------------
	# check lockers
	#--------------------------
	%hash = &multilevel_securedata_cc_get($app{service_id},"DO_NOT_CHECK_CC_ERROR");
	$cc_is_active 			= ($hash{status_ok} eq 1) ? 1 : 0;
	$cc_is_auto_recharge	= ( ($hash{status_ok} eq 1) && ($hash{is_auto_recharge} eq 1) ) ? 1 : 0;
	$cc_error				= ($hash{cc_error} eq 0) ? 0 : 1;
	#
	if (
		($cc_is_active eq 1) &&
		(  ($cc_error.$cc_is_auto_recharge eq "00") || ($cc_error eq 1) )&&
		($action_is_delete eq 1)
		) {
		#--------------------------
		# delete 
		#--------------------------
		&data_delete("service_data",$app{service_id},"profile_cc_ani_number");
		&data_delete("service_data",$app{service_id},"profile_cc_ani_code");
		if (&multilevel_securedata_cc_del($app{service_id}) eq 1) {
			&action_history("cim:payment:del",('service_id'=>$app{service_id}));
			$answer = 20;
		} else {
			$answer = 21;
		}
		#
	} elsif ( ($need_ani_confirmation eq 1) && ($action_is_confirmation_code eq 1) ) {
		#--------------------------
		# confirmation code action
		#--------------------------
		#
		# first check
		$answer = (&form_check_string($form{cc_contact_number}) 	ne 1) ? 111 : $answer;
		$form{cc_contact_number_fixed} = $form{cc_contact_number};
		#
		# second check
		if ($answer eq 0) {
			$number = clean_int(substr($form{cc_contact_number},0,1024));
			($flag,$number_e164,$tmp2) = &multilevel_check_E164_number($number);
			if 		($flag eq "USANOAREACODE") 			{ $answer = 1111;	}
			elsif	($flag eq "UNKNOWNCOUNTRY") 		{ $answer = 1112;	}
			elsif 	($flag eq "OK") 					{
				$number = $number_e164;
				$form{cc_contact_number_fixed} = $number;
				%callback_price = &multilevel_call_get_rate($number,1,"product_rate_callback");
				if ($callback_price{rate_found} ne 1)	{ $answer = 1114;	}
			} else 										{ $answer = 1113;	}
		}
		#
		# try to dial
		if ($answer eq 0) {
			$confirmation_code 		= &active_session_get("anicheck_code");
			$confirmation_number  	= &active_session_get("anicheck_number");
			if ( ($confirmation_number ne $form{cc_contact_number_fixed}) || ($confirmation_number eq "") || ($confirmation_code eq "") ) {
				@chars=('0'..'9');
				$confirmation_code  = "";
				foreach (1..4) {$confirmation_code  .= $chars[rand @chars];}
				&active_session_set("anicheck_code",$confirmation_code);
				&active_session_set("anicheck_number",$form{cc_contact_number_fixed});
			}
			&action_history("security:ani_check_request",('service_id'=>$app{service_id},'value_old'=>$confirmation_code,'value_new'=>$form{cc_contact_number_fixed}));
			&dial_and_play_code($form{cc_contact_number_fixed},$confirmation_code);
			#$callback_queue_folder =  "/var/spool/asterisk/outgoing/";
			#$channel_string		= &multilevel_dialstring_get($form{cc_contact_number_fixed});
			#$callback_file		= time.$form{cc_contact_number_fixed} .".sendcode.call"; 
			#$callback_file_buf 	=  "Channel: $channel_string\n";
			#$callback_file_buf 	.= "MaxRetries: 2\n";
			#$callback_file_buf 	.= "RetryTime: 5\n";
			#$callback_file_buf 	.= "WaitTime: 40\n";
			#$callback_file_buf 	.= "Application: DeadAGI\n";
			#$callback_file_buf 	.= "Data: play_code.pl,code=$confirmation_code\n";
			#$callback_file_buf 	.= "AlwaysDelete:Yes\n";
			#$callback_file_buf 	.= "Archive:No\n";
			#%my_timestamp = &get_today(time+5);
			#$timestamp_future = substr("0000".$my_timestamp{YEAR},-4,4) . substr("00".$my_timestamp{MONTH},-2,2) . substr("00".$my_timestamp{DAY},-2,2) . substr("00".$my_timestamp{HOUR},-2,2) . substr("00".$my_timestamp{MINUTE},-2,2) .".".substr("00".$my_timestamp{SECOND},-2,2);
			#open (OUT,">/tmp/$callback_file");
			#print OUT $callback_file_buf;
			#close (OUT);
			#$cmd = "chmod 666 /tmp/$callback_file; ";
			#$cmd .= "touch -t $timestamp_future /tmp/$callback_file; ";
			#$cmd .= "mv /tmp/$callback_file $callback_queue_folder; ";
			#$tmp = `$cmd`;
			$answer = 10;
		}
	} elsif ( ($cc_is_active eq 0) && ($action_is_save eq 1) ) {
		#--------------------------
		# save action
		#--------------------------
		#
		# first clean
		foreach ( qw(cc_type cc_number cc_date_1 cc_date_2 cc_code cc_first_name cc_last_name cc_address cc_country cc_city cc_state cc_zip cc_contact_number)) {
			$form{$_} = trim(&clean_str(substr($form{$_},0,255)," -_–(\@)-,=+;.[]:?<>\&","MINIMAL"));
		}
		#
		# first check
		$answer = (&form_check_string($form{cc_type}) 		ne 1) ? 101 : $answer;
		$answer = (&form_check_string($form{cc_number}) 	ne 1) ? 102 : $answer;
		$answer = (&form_check_string($form{cc_date_1}) 	ne 1) ? 103 : $answer;
		$answer = (&form_check_string($form{cc_date_2}) 	ne 1) ? 103 : $answer;
		$answer = (&form_check_string($form{cc_code}) 		ne 1) ? 104 : $answer;
		$answer = (&form_check_string($form{cc_first_name})	ne 1) ? 105 : $answer;
		$answer = (&form_check_string($form{cc_last_name})	ne 1) ? 106 : $answer;
		$answer = (&form_check_string($form{cc_address}) 	ne 1) ? 107 : $answer;
		$answer = (&form_check_string($form{cc_country}) 	ne 1) ? 113 : $answer;
		$answer = (&form_check_string($form{cc_city}) 		ne 1) ? 108 : $answer;
		$answer = (&form_check_string($form{cc_state}) 		ne 1) ? 109 : $answer;
		$answer = (&form_check_string($form{cc_zip}) 		ne 1) ? 110 : $answer;
		$answer = (&form_check_string($form{cc_contact_number}) 	ne 1) ? 111 : $answer;
		#$answer = (&form_check_string($form{cc_confirmation_code}) 	ne 1) ? 112 : $answer;
		#
		# second if contact number is valid
		$form{cc_contact_number_fixed} = $form{cc_contact_number};
		if ($answer eq 0) {
			$number = clean_int(substr($form{cc_contact_number},0,1024));
			($flag,$number_e164,$tmp2) = &multilevel_check_E164_number($number);
			if 		($flag eq "USANOAREACODE") 			{ $answer = 1111;	}
			elsif	($flag eq "UNKNOWNCOUNTRY") 		{ $answer = 1112;	}
			elsif 	($flag eq "OK") 					{
				$number = $number_e164;
				$form{cc_contact_number_fixed} = $number;
				%callback_price = &multilevel_call_get_rate($number,1,"product_rate_callback");
				if ($callback_price{rate_found} ne 1)	{ $answer = 1114;	}
			} else 										{ $answer = 1113;	}
		}
		#
		# check if we need ani confirmation
		if ( ($need_ani_confirmation eq 1) && ($answer eq 0) )  {
			# we need check this ani
			if (&multilevel_anicheck_check($app{service_id},$form{cc_contact_number_fixed}) eq 1) {
				# ani preiously checked.. no need ask confirmation
			} else {
				# ani not previously checked, lets enable ask_confirmation
				# and check if we already got confirmation from form				
				$need_ask_confirmation_code = 1;
				if ($form{cc_confirmation_code} ne "") {
					$confirmation_code 		= &active_session_get("anicheck_code");
					$confirmation_number  	= &active_session_get("anicheck_number");
					if (
						($confirmation_number eq $form{cc_contact_number_fixed}) &&
						($confirmation_code eq $form{cc_confirmation_code}) &&
						($confirmation_number ne "") &&
						($confirmation_code ne "")
						) {
						# ani need confirmation, we have confirmation
						# from section and form and they match. OK!
					} else {
						# ani need confirmation, we have from form
						# and session but they dont match
						$answer = 11;
					}
				} else {
					# we need confirmation but we dont 
					# have it from form
					$answer = 12;
				}
			}
		} else {
			# we don need ani confirmation
			# probably trust client 
		}
		#
		# try to save
		if ($answer eq 0) {
			#
			# tenta update no CIM
			%order = ();
			$order{cc_type} 		= $form{cc_type};
			$order{cc_number} 		= $form{cc_number};
			$order{cc_date}			= substr("00".$form{cc_date_1},-2,2).substr("00".$form{cc_date_2},-2,2);
			$order{cc_code} 		= $form{cc_code};
			$order{first_name}		= $form{cc_first_name};
			$order{last_name}		= $form{cc_last_name};
			$order{address} 		= $form{cc_address};
			$order{country} 		= $form{cc_country};
			$order{city} 			= $form{cc_city};
			$order{state} 			= $form{cc_state};
			$order{zip} 			= $form{cc_zip};
			$order{contact_number}	= $form{cc_contact_number_fixed};
			$order{service_id} 		= $app{service_id};
			%order = multilevel_securedata_cc_set(%order);
			if ($order{status_ok} eq 1) {
				&action_history("cim:payment:set",('service_id'=>$app{service_id}));
				if ($need_ani_confirmation eq 1) {
					&action_history("security:ani_checked",('service_id'=>$app{service_id},'value_new'=>$form{cc_contact_number_fixed}));
					&active_session_delete("anicheck_code");
					&active_session_delete("anicheck_number");
					&multilevel_anicheck_touch($app{service_id},$form{cc_contact_number_fixed});
				}
				$answer = 1;
			} else {
				$answer = ($order{status_code} eq 7) ? 201 : 200;
			}
			&multilevel_coupon_engine_autorecharge($app{service_id});
			#
			# log in txt for debug
			$buf = "\n\n-------------------------------------------\n";
			$buf .= "TIME=".time."\n";
			$buf .= "SERVICE_ID=$app{service_id}\n";
			foreach (sort keys %order) {
				if ($_ eq "debug"){next}
				$v = $order{$_};
				if (index($_,"cc_") ne -1){$v = "length-".length($v);}
				$buf .= "ORDER DUMP $_=$v\n";
			}
			foreach (split(/\|/,$order{debug})) {
				$buf .= "DEBUG $_=$order{$_}\n";
			}
			if ($order{status_ok} eq 1) {
				open(OUT,">>/usr/local/multilevel/data/logs/multilevel_securedata_cc_set.log");
			} else {
				open(OUT,">>/usr/local/multilevel/data/logs/multilevel_securedata_cc_set.error.log");
			}
			print OUT $buf;
			close(OUT);
		}
	}
	#
	#--------------------------
	# print page
	#--------------------------
	cgi_hearder_html();
	print qq[
		<script>
		parent.billing_cc_answer($answer);
		</script>
		<font size=1>
	];
	#foreach (sort keys %form) {print "FORM $_=$form{$_}<br>"}
	#foreach (sort keys %app) {print "APP $_=$app{$_}<br>"}
}
sub do_profile() {
	#
	#---------------------------------------------------------------------------
	# defaults
	#---------------------------------------------------------------------------
    %t = %template_default;
	#
	#---------------------------------------------------------------------------
	# name
	#---------------------------------------------------------------------------
    $t{dic}{name_error}				= 0;
    $t{dic}{name_ok}				= 0;
	if ($form{save} eq "name") {
		#
		# check name
		$v1 = trim(substr($form{name},0,1024)); 
		$v2 = clean_str($v1,"()-=[]?><#\@");
		$t{dic}{name_error} = ($v1 eq "") ? 1 : $t{dic}{name_error};
		$t{dic}{name_error} = ($v1 ne $v2) ? 1 : $t{dic}{name_error};
		$name = $v2;
		#
		# save if possible
		if ($t{dic}{name_error} eq 0) {
			database_do("update service set name='$name' where id='$app{service_id}' ");
			&active_session_set("service_name",$name);
			$app{service_name}=$name;
			$t{dic}{name_ok} = 1;
		}
	}
	$t{dic}{service_name}  		= $app{service_name};
	$t{dic}{service_name_cut}  	= &format_trim_name($app{service_name},1);
    $t{dic}{form_name}			= $form{name};
	#
	#---------------------------------------------------------------------------
	# save process email request
	#---------------------------------------------------------------------------
	$new_email 		= &active_user_get("new_email");
	$new_email_key	= &active_user_get("new_email_key");
	$new_email_time	= &active_user_get("new_email_time");
	$new_email_step	= ( (time-$new_email_time) > (60*60*24*7) ) ? 1 : 2;
    $t{dic}{email_request}			= ($new_email_step eq 1) ? 1 : 0;
    $t{dic}{email_request_error}	= 0;
    $t{dic}{email_request_ok}		= 0;
    $t{dic}{email_confirm}			= ($new_email_step eq 2) ? 1 : 0;
    $t{dic}{email_confirm_error}	= 0;
    $t{dic}{email_confirm_ok}		= 0;
    $t{dic}{new_email}				= $new_email;
    $t{dic}{new_key}				= $new_email_key;
    $t{dic}{new_time}				= $new_email_time;
	if ( ($t{dic}{email_request} eq 1) && ($form{save} eq "email_request") ) {
		# check email
		if ( index("|EMPTY|NULL|CLEAR|NONE|","\U|$form{email}|") ne -1  ) {
			$form{email} = "";
			$email = "";
		} else {
			if ( ($form{email} ne "") && (index("$form{email}","\@") eq rindex("$form{email}","\@"))  ){
				($slice1,$slice2) = split(/\@/,$form{email});
				$slice1 = &clean_str(substr("\L$slice1",0,255),"+-_.","MINIMAL");
				$slice2 = &clean_str(substr("\L$slice2",0,255),".-","MINIMAL");
				if ($slice2 eq "gmail.com")  {
					$slice1 = &clean_str("\L$slice1","-_+","MINIMAL");
					if (index($slice1,"+") ne -1) {
						$slice1 = substr($slice1,0,index($slice1,"+"));
					}
				}
				if ($form{email} ne "$slice1\@$slice2") {
					&action_history("security:emailtrick",('service_id'=>$app{service_id},'value_old'=>$form{email}));
				}
				$form{email} = "$slice1\@$slice2";
			}		
			$v1 = trim(substr($form{email},0,1024)); 
			$v2 = clean_str($v1,"+.()-=[]?><#\@");
			$t{dic}{email_request_error} = ($v1 eq "") ? 1 : $t{dic}{email_request_error};
			$t{dic}{email_request_error} = ($v1 ne $v2) ? 1 : $t{dic}{email_request_error};
			$t{dic}{email_request_error} = (index($v2,"\@") eq -1) ? 1 : $t{dic}{email_request_error};
			$t{dic}{email_request_error_msg_generic} = $t{dic}{email_request_error};
			$email = $v2;
		}
		# 2rd level check - same email
		if ($t{dic}{email_request_error} eq 0) {
			if  ($form{email} eq $app{service_email}) {
				$t{dic}{email_request_error_msg_generic} = 0;
				$t{dic}{email_request_error_msg_sameemail} = 1;
				$t{dic}{email_request_error} = 1;
			}
		}
		# 3rd level check - verifica email duplicado
		#if ($t{dic}{email_request_error} eq 0) {
		#	%tmp_hash = database_select_as_hash("SELECT 1,1,count(*) FROM service where email='$form{email}' and id != '$app{service_id}' ","flag,count");
		#	unless ($tmp_hash{1}{flag}.$tmp_hash{1}{count} eq "10") {
		#		$t{dic}{email_request_error_msg_generic} = 0;
		#		$t{dic}{email_request_error_msg_inuse} = 1;
		#		$t{dic}{email_request_error} = 1;
		#	}
		#}
		# save if possible
		#if ($t{dic}{email_request_error} eq 0) {
		#	$t{dic}{new_email}			= $email;
		#	my @digits=('0'..'9');
		#	$t{dic}{new_key} = "";
		#	$t{dic}{new_key} .= $digits[rand @digits];
		#	$t{dic}{new_key} .= $digits[rand @digits];
		#	$t{dic}{new_key} .= $digits[rand @digits];
		#	$t{dic}{new_key} .= $digits[rand @digits];
		#	$t{dic}{email_request_ok}	= 1;
		#	$t{dic}{email_request}		= 0;
		#	$t{dic}{email_confirm}		= 1;
		#	&active_user_set("new_email",$email);
		#	&active_user_set("new_email_key",$t{dic}{new_key});
		#	&active_user_set("new_email_time",time);
		#	# SEND EMAIL
		#	%email = ();
		#	$email{to}			= $email;
		#	$email{template}	= "change.email";
		#	$email{dic}{code}	= $t{dic}{new_key};
		#	$email{dic}{name}	= $app{service_name};
		#	$email{dic}{email}	= $email;
		#	&multilevel_send_email(%email);
		#}
		#
		# NEW save if possible (no more multiple steps)
		if ($t{dic}{email_request_error} eq 0) {
			database_do("update service set email='$email' where id='$app{service_id}' ");
			&active_session_set("service_email",$email);
			$app{service_email} = $email;
			$t{dic}{email_request}		= 1;
			$t{dic}{email_request_error}= 0;
			$t{dic}{email_request_ok}	= 0;
			$t{dic}{email_confirm}		= 0;
			$t{dic}{email_confirm_error}= 0;
			$t{dic}{email_confirm_ok}	= 1;
			&do_service_alert_check_email_or_name_question();
		}
	}
	if ( ($t{dic}{email_confirm} eq 1) && ($form{save} eq "email_confirm") )  {
		# check key
		$v1 = clean_int(substr($form{key},0,1024)); 
		$t{dic}{email_confirm_error} = ($v1 eq "") ? 1 : $t{dic}{email_confirm_error};
		$t{dic}{email_confirm_error} = ($new_email_key ne $v1) ? 1 : $t{dic}{email_confirm_error};
		# save if possible
		if ($t{dic}{email_confirm_error} eq 0) {
			database_do("update service set email='$new_email' where id='$app{service_id}' ");
			&active_session_set("service_email",$new_email);
			$app{service_email} = $new_email;
			data_delete($app{users_options_table},$app{session_cookie_u},"new_email");
			data_delete($app{users_options_table},$app{session_cookie_u},"new_email_key");
			data_delete($app{users_options_table},$app{session_cookie_u},"new_email_time");
			$t{dic}{new_email}			= "";
			$t{dic}{new_key}			= "";
			$t{dic}{email_request}		= 1;
			$t{dic}{email_request_error}= 0;
			$t{dic}{email_request_ok}	= 0;
			$t{dic}{email_confirm}		= 0;
			$t{dic}{email_confirm_error}= 0;
			$t{dic}{email_confirm_ok}	= 1;
		}
	} else {
		$form{email}  = "";
	}
	if ( ($t{dic}{email_confirm} eq 1) && ($form{save} eq "cancel_email_request") )  {
		data_delete($app{users_options_table},$app{session_cookie_u},"new_email");
		data_delete($app{users_options_table},$app{session_cookie_u},"new_email_key");
		data_delete($app{users_options_table},$app{session_cookie_u},"new_email_time");
		$t{dic}{new_email}			= "";
		$t{dic}{new_key}			= "";
		$t{dic}{email_request}		= 1;
		$t{dic}{email_request_error}= 0;
		$t{dic}{email_request_ok}	= 0;
		$t{dic}{email_confirm}		= 0;
		$t{dic}{email_confirm_error}= 0;
		$t{dic}{email_confirm_ok}	= 0;
	}
	if ( ($t{dic}{email_confirm} eq 1) && ($form{save} eq "resend_email_request") )  {
		$t{dic}{email_request}		= 0;
		$t{dic}{email_request_error}= 0;
		$t{dic}{email_request_ok}	= 1;
		$t{dic}{email_confirm}		= 1;
		$t{dic}{email_confirm_error}= 0;
		$t{dic}{email_confirm_ok}	= 0;
		#
		# SEND EMAIL
		%email = ();
		$email{to}			= $t{dic}{new_email};
		$email{template}	= "change.email";
		$email{dic}{code}	= $t{dic}{new_key};
		$email{dic}{name}	= $app{service_name};
		$email{dic}{email}	= $t{dic}{new_email};
		&multilevel_send_email(%email);
	}
    $t{dic}{form_email}				= $form{email};
    $t{dic}{form_key}				= $form{key};
	$t{dic}{service_email}  		= $app{service_email};
	#
	#---------------------------------------------------------------------------
	# read alerts
	#---------------------------------------------------------------------------
    $t{dic}{email_alert_new_friends}			= (&data_get("service_data",$app{service_id},"trigger_nf") eq 1) ? 1 : 0;
    $t{dic}{email_alert_new_friends_of_friends}	= (&data_get("service_data",$app{service_id},"trigger_nfof") eq 1) ? 1 : 0;
    $t{dic}{email_alert_new_commission}			= (&data_get("service_data",$app{service_id},"trigger_nc") eq 1) ? 1 : 0;
    $t{dic}{email_alert_each_call}				= (&data_get("service_data",$app{service_id},"trigger_ec") eq 1) ? 1 : 0;
    $t{dic}{email_alert_low_balance}			= (&data_get("service_data",$app{service_id},"trigger_lb") eq 1) ? 1 : 0;
    $t{dic}{email_news}							= (&data_get("service_data",$app{service_id},"email_news") eq 1) ? 1 : 0;
	#
	#---------------------------------------------------------------------------
	# print page
	#---------------------------------------------------------------------------
    $t{dic}{my_url}					= $my_url;
	$t{dic}{service_id}				= $app{service_id};	
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
    $t{dic}{profile_has_errors}		= ($t{dic}{ss_status_error} eq 1) ? 1 : 0;
    &template_print("template.myaccount.profile.html",%t);
}
sub do_credits_affiliate() {
	#
	#---------------------------------------------------------------------------
	# defaults
	#---------------------------------------------------------------------------
    %t = %template_default;
	#
	#---------------------------------------------------------------------------
	# SS process
	#---------------------------------------------------------------------------
    $t{ss_status_error}				= 0;
    $t{ss_status_ok}				= 0;
    $t{ss_status_error_type_user}	= 0;
    $t{ss_status_error_type_system}	= 0;
    $t{ss_status_del}				= 0;
	$t{ss_flags} 			= &data_get("service_data",$app{service_id},"ss_flags");
	$t{ss_empty}			= ($t{ss_flags} eq "") ? 1 : 0;
	$t{ss_flags}			= ($t{ss_flags} eq "") ? ",DEL,DATA,HEAD," : $t{ss_flags};
	$t{ss_flag_edit_data}	= (index($t{ss_flags},",DATA,") ne -1) ? 1 : 0;
	$t{ss_flag_edit_head}	= (index($t{ss_flags},",HEAD,") ne -1) ? 1 : 0;
	$t{ss_flag_delete}		= (index($t{ss_flags},",DEL,") ne -1) ? 1 : 0;
	%hash = database_select_as_hash("SELECT 1,1,service_status.can_request_commission_check FROM service,service_status where service.status=service_status.id and service.id='$app{service_id}' ","flag,can_request_commission_check");
	$t{ss_enabled}			= ( ($hash{1}{flag} eq 1) && ($hash{1}{can_request_commission_check} eq 1) ) ? 1 : 0;
	if ($form{save} eq "ss_edit") {
		#
		$secure_id_to_save = "";
		#
		#-----------------------
		# check data format
		#-----------------------
		if ($t{ss_flag_edit_data} eq 1) {
			foreach $n (qw(ss_addr1 ss_country ss_city ss_state ss_zip)) {
				$v1 = trim(substr($form{$n},0,1024)); 
				$v2 = clean_str($v1,"*()-=[]?><#\@");
				$t{$n."_error"} = ($v1 eq "") ? 1 : $t{$n."_error"};
				$t{$n."_error"} = ($v1 ne $v2) ? 1 : $t{$n."_error"};
				$t{ss_status_error} = ($t{$n."_error"} eq 1) ? 1 : $t{ss_status_error};
				$t{ss_status_error_type_user} = ($t{$n."_error"} eq 1) ? 1 : $t{ss_status_error_type_user};
			}
			foreach $n (qw(ss_addr2)) {
				$v1 = trim(substr($form{$n},0,1024)); 
				$v2 = clean_str($v1,"*()-=[]?><#\@");
				$t{$n."_error"} = ($v1 ne $v2) ? 1 : $t{$n."_error"};
				$t{ss_status_error} = ($t{$n."_error"} eq 1) ? 1 : $t{ss_status_error};
				$t{ss_status_error_type_user} = ($t{$n."_error"} eq 1) ? 1 : $t{ss_status_error_type_user};
			}
		}
		#
		#-----------------------
		# check link format
		#-----------------------
		if ($t{ss_flag_edit_head} eq 1) {
			foreach $n (qw(ss_name)) {
				$v1 = trim(substr($form{$n},0,1024)); 
				$v2 = clean_str($v1,"*()-=[]?>.<#\@");
				$t{$n."_error"} = ($v1 eq "") ? 1 : $t{$n."_error"};
				$t{$n."_error"} = ($v1 ne $v2) ? 1 : $t{$n."_error"};
				$t{ss_status_error} = ($t{$n."_error"} eq 1) ? 1 : $t{ss_status_error};
				$t{ss_status_error_type_user} = ($t{$n."_error"} eq 1) ? 1 : $t{ss_status_error_type_user};
			}
			foreach $n (qw(ss_paypal ss_ss)) {
				$v1 = trim(substr($form{$n},0,1024)); 
				$v2 = clean_str($v1,"*()-=[]?>.<#\@");
				$t{$n."_error"} = ($v1 ne $v2) ? 1 : $t{$n."_error"};
				$t{ss_status_error} = ($t{$n."_error"} eq 1) ? 1 : $t{ss_status_error};
				$t{ss_status_error_type_user} = ($t{$n."_error"} eq 1) ? 1 : $t{ss_status_error_type_user};
			}
		}
		#
		#-----------------------
		# check link content
		#-----------------------
		if ($t{ss_flag_edit_head} eq 1) {
			if ($t{ss_status_error} eq 0) {
				$old = &data_get("service_data",$app{service_id},"ss_ss");
				$new = $form{ss_ss};
				$secure_id_to_save = ( ($old eq $new) || ($new eq "") ) ? "" : $new;
				$secure_id_to_save = ($old eq  "") ? $new : $secure_id_to_save;
				if ($secure_id_to_save ne "")  {
					if (&multilevel_ss_check($secure_id_to_save) ne 1) {
						$t{ss_ss_error} = 1;
						$t{ss_status_error} = 1;
						$t{ss_status_error_type_user} = 1;
					}
				}
			}
		}
		#
		#-----------------------
		# save link if possible
		#-----------------------
		if (  ($t{ss_flag_edit_head} eq 1) and ($t{ss_status_error} eq 0)  ) {
			if ($secure_id_to_save ne "") {
				if (multilevel_securedata_ss_set($app{service_id},$secure_id_to_save) eq 1) {
					$l1 = length($secure_id_to_save);
					$l2 = 0-$l1;
					$ss_obfuscated = substr("********************************".substr($secure_id_to_save,-3,3) , $l2,$l1);
					&data_set("service_data",$app{service_id},"ss_ss",$ss_obfuscated);
					&data_set("service_data",$app{service_id},"ss_paypal",$form{ss_paypal});
					&data_set("service_data",$app{service_id},"ss_name",$form{ss_name});
					$form{ss_ss}=$ss_obfuscated;
					$can_save_other_data = 1;
				} else {
					$t{ss_status_error} = 1;
					$t{ss_status_error_type_system} = 1;
					$can_save_other_data = 0;					
				}
			} else {
				&data_set("service_data",$app{service_id},"ss_name",$form{ss_name});
				&data_set("service_data",$app{service_id},"ss_paypal",$form{ss_paypal});
			}
		}
		#
		#-----------------------
		# save data if possible
		#-----------------------
		if (  ($t{ss_flag_edit_data} eq 1) and ($t{ss_status_error} eq 0)  ) {
			foreach (qw(ss_addr1 ss_addr2 ss_country ss_city ss_state ss_zip)) {
				&data_set("service_data",$app{service_id},$_,$form{$_});
			}
		}
		#
		#-----------------------
		# save status 
		#-----------------------
		if ($t{ss_status_error} eq 0) {
			&data_set("service_data",$app{service_id},"ss_flags",$t{ss_flags});
		    $t{ss_status_ok} = 1;
		}
		#
		#-----------------------
		# redireciona se ok
		#-----------------------
		if ($t{ss_status_error} eq 0) {
			$t{ss_status_ok} = 1;
		}
	} elsif ( ($t{ss_flag_delete} eq 1) && ($form{save} eq "ss_del") ) {
		#
		#-----------------------
		# delete
		#-----------------------
		foreach (qw(ss_flags ss_ss ss_paypal ss_country ss_name ss_bname ss_addr1 ss_addr2 ss_city ss_state ss_zip)) {
			&data_delete("service_data",$app{service_id},$_);
		}
		#
		#-----------------------
		# redireciona se ok
		#-----------------------
		if ($t{ss_status_error} eq 0) {
			$t{ss_status_ok} = 1;
		}
	} else {
		#
		#-----------------------
		# load form		
		#-----------------------
		foreach (qw(name country bname addr1 addr2 city state zip)) {
			$name_1 = "ss_$_";
			$name_2 = "cc_$_";
			$value = &data_get("service_data",$app{service_id},$name_1);
			if ($value eq "") {
				$value = &data_get("service_data",$app{service_id},$name_2);
			}
			$form{$name_1} = $value;
		}
		$form{ss_ss} = &data_get("service_data",$app{service_id},"ss_ss");
		$form{ss_paypal} = &data_get("service_data",$app{service_id},"ss_paypal");
	}
	foreach (qw(ss_ss ss_country ss_paypal ss_name ss_bname ss_addr1 ss_addr2 ss_city ss_state ss_zip)) {$t{$_}	= $form{$_};}
	$t{"ss_state_is_".&clean_str($form{ss_state},"MINIMAL")} = "selected";
	$t{"ss_country_is_".&clean_str($form{ss_country},"MINIMAL")} = "selected";
	#
	#---------------------------------------------------------------------------
	# print page
	#---------------------------------------------------------------------------
    $t{my_url}					= $my_url;
	$t{service_id}				= $app{service_id};	
	$t{service_credit}			= &format_number($app{service_credits},2);
	$t{service_credits_bar}	= $app{service_credits_bar};
    $t{profile_has_errors}		= ($t{ss_status_error} eq 1) ? 1 : 0;
    &template_print("template.myaccount.credits.affiliate.html",%t);
}
sub do_credits_buy_commission(){
    #
    # start
    %t = %template_default;
	$t{dic}{status_ok}						= 0;
    $t{dic}{status_error}					= 0;
	$t{dic}{enable_5_dollars}				= 0;
	$t{dic}{enable_10_dollars}				= 0;
	$t{dic}{enable_20_dollars}				= 0;
	$t{dic}{can_add_credit}					= 0;
	$t{dic}{limit_max_balance}				= 0;
	$t{dic}{balance}						= 0;
	#
	# pega dados do status
	$sql = "
	SELECT 1, 1, service.balance,service.limit, service_status.can_add_credit, service_status.limit_max_balance
	FROM service, service_status
	where service.status=service_status.id and service.id='$app{service_id}'
	";
	%hash = database_select_as_hash($sql,"flag,balance,limit,can_add_credit,limit_max_balance");
	if ($hash{1}{flag} eq 1) {
		$t{dic}{can_add_credit}			= ($hash{1}{can_add_credit} eq 1) ? 1 : 0;
		$t{dic}{max_balance}			= $hash{1}{limit_max_balance};
		$t{dic}{balance}				= $hash{1}{balance}-$hash{1}{limit};
		$t{dic}{balance_formated}		= &format_number($t{dic}{balance},2);
		$t{dic}{max_balance_formated}	= &format_number($t{dic}{max_balance},2);
		$t{dic}{enable_5_dollars}		= ($hash{1}{limit_max_balance}>5) ? 1 : 0;
		$t{dic}{enable_10_dollars}		= ($hash{1}{limit_max_balance}>10) ? 1 : 0;
		$t{dic}{enable_20_dollars}		= ($hash{1}{limit_max_balance}>20) ? 1 : 0;
	}
	#
	# get all commissions
    %list = database_select_as_hash("SELECT 1,1,count(*),sum(value) FROM service_commission WHERE status=1 and service_id = '$app{service_id}' and invoice_id is null","flag,qtd,value");
	$t{dic}{commissions_all_value} 			= ($list{1}{flag} eq 1) ? $list{1}{value} : 0;
	$t{dic}{commissions_all_value_formated} = &format_number($t{dic}{commissions_all_value},2);
	#
	# get ok commissions
    %list = database_select_as_hash("SELECT 1,1,count(*),sum(value) FROM service_commission WHERE status=1 and service_id = '$app{service_id}' and invoice_id is null and now()>=activation_date_1 ","flag,qtd,value");
	$t{dic}{commissions_ok_value} 			= ($list{1}{flag} eq 1) ? $list{1}{value} : 0;
	$t{dic}{commissions_ok_value_formated} 	= &format_number($t{dic}{commissions_ok_value},2);
	#
	# split in slices (5,10,20,50,all)
    $sql = "
		SELECT id,value 
		FROM service_commission 
		WHERE status=1 and service_id = '$app{service_id}' and (invoice_id is null or invoice_id ='')and now()>activation_date_1
	    ";
    %list = database_select_as_hash($sql);
	$value = 0;
	$qtd = 0;
	$t{dic}{no_slice} = 0;
    foreach $id (sort{$a <=> $b} keys %list) {
		$value += $list{$id};
		$qtd++;
		$t{dic}{slice_all_flag} = 1;
		$t{dic}{slice_all_id} .= "$id,";
		$t{dic}{slice_all_value} = $value;
		if ( ($t{dic}{enable_5_dollars} eq 1) && ($value >= 5) && ($t{dic}{slice_1_flag} eq "")) {
			$t{dic}{slice_1_flag}			= 1;
			$t{dic}{slice_1_id}				= $t{dic}{slice_all_id};
			$t{dic}{slice_1_value}			= $value;
			$t{dic}{slice_1_value_formated}	= &format_number($value,2);
		} elsif ( ($t{dic}{enable_10_dollars} eq 1) && ($value >= 10) && ($t{dic}{slice_2_flag} eq "")) {
			$t{dic}{slice_2_flag}			= 1;
			$t{dic}{slice_2_id}				= $t{dic}{slice_all_id};
			$t{dic}{slice_2_value}			= $value;
			$t{dic}{slice_2_value_formated}	= &format_number($value,2);
		} elsif ( ($t{dic}{enable_20_dollars} eq 1) && ($value >= 20) && ($t{dic}{slice_3_flag} eq "")) {
			$t{dic}{slice_3_flag}			= 1;
			$t{dic}{slice_3_id}				= $t{dic}{slice_all_id};
			$t{dic}{slice_3_value}			= $value;
			$t{dic}{slice_3_value_formated}	= &format_number($value,2);
		}
    }
	if ($qtd > 0) {
		$t{dic}{slice_all_value_formated}	= &format_number($t{dic}{slice_all_value},2);
		$t{dic}{slice_1_flag}	= ($t{dic}{slice_1_value} eq $t{dic}{slice_all_value}) ? 0 : $t{dic}{slice_1_flag};
		$t{dic}{slice_2_flag}	= ($t{dic}{slice_2_value} eq $t{dic}{slice_all_value}) ? 0 : $t{dic}{slice_2_flag};
		$t{dic}{slice_3_flag}	= ($t{dic}{slice_3_value} eq $t{dic}{slice_all_value}) ? 0 : $t{dic}{slice_3_flag};
		$t{dic}{slice_1_id}		= substr($t{dic}{slice_1_id},0,-1);
		$t{dic}{slice_2_id}		= substr($t{dic}{slice_2_id},0,-1);
		$t{dic}{slice_3_id}		= substr($t{dic}{slice_3_id},0,-1);
		$t{dic}{slice_4_id}		= substr($t{dic}{slice_4_id},0,-1);
		$t{dic}{slice_all_id}	= substr($t{dic}{slice_all_id},0,-1);
	} else {
		$t{dic}{no_slice} = 1;
	}
	#
	# try to add
	if ( ($form{save} eq 1) && ($t{dic}{can_add_credit} eq 1) ) {
		$t{dic}{status_ok} = 1;
		#
		# click check
		$tmp = &active_session_get("click_check_addc");
		unless ( ($form{click_check} ne "") && ($tmp ne "") && ($form{click_check} eq $tmp)  ) {
			$t{dic}{status_ok} 		= 0;
			$t{dic}{status_error}	= 1;
			$t{dic}{error_message_no_click_check} = 1;
		}
		#
		# value
		unless ( (index("|1|2|3|all|","|$form{slice}|") ne -1) && ($t{dic}{"slice_".$form{slice}."_flag"} eq 1) ) {
			$t{dic}{status_ok} 		= 0;
			$t{dic}{status_error}	= 1;
			$t{dic}{error_message_wrong_value} = 1;
		}
		#
		# agree
		if ( $form{agree} ne 1 ) {
			$t{dic}{status_ok} 		= 0;
			$t{dic}{status_error}	= 1;
			$t{dic}{error_message_no_agree} = 1;
		}
		#
		# max balance
		if ($t{dic}{status_ok} eq 1) {
			if ($t{dic}{balance}+$t{dic}{"slice_".$form{slice}."_real"} > $t{dic}{max_balance}) {
				$t{dic}{status_ok} 		= 0;
				$t{dic}{status_error}	= 1;
				$t{dic}{error_message_max_balance} = 1;
			}
		}
		#
		# save if all ok
		if ($t{dic}{status_ok} eq 1) {
			%order = ();
			$order{service_id}			= $app{service_id};
			$order{value_credit}		= $t{dic}{"slice_".$form{slice}."_value"};
			$order{value_money}			= 0;
			$order{commissions_ids}		= $t{dic}{"slice_".$form{slice}."_id"};
			$order{type}				= "COMMISSION_CRED";
			$order{from_type}			= "WEB";
			%answer = &multilevel_credit_add(%order);
			if ($answer{ok} eq 1) {
				$t{dic}{status_ok} 		= 1;
				$t{dic}{status_error}	= 0;
			} else {
				$t{dic}{status_ok} 		= 0;
				$t{dic}{status_error}	= 1;
				$t{dic}{error_message_credit_error} = 1;
			}
		}
	}
    #
    # print page
    $t{dic}{click_check} = time;
	&active_session_set("click_check_addc",$t{dic}{click_check});
    $t{dic}{my_url}					= $my_url;
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
    &template_print("template.myaccount.credits.add.commission.html",%t);
	
}
sub do_credits_buy_cim_automatic(){
	#
	# start
	%t = %template_default;
	$t{auto_recharge_default_threshold}		= "balance_2";
	$t{auto_recharge_default_value}			= "10";
	$t{auto_recharge_default_but}				= "30days_60";
	$t{auto_recharge_valid_values_threshold}	= "|balance_2|balance_5|";
	$t{auto_recharge_valid_values_value}		= "|5|10|20|";
	$t{auto_recharge_valid_values_but}			= "|30days_30|30days_60|30days_90|";
	$t{status_ok}			= 0;
    $t{status_error}		= 0;
	$t{can_add_credit}		= 0;
	$t{can_auto_recharge}	= 0;
	$t{enable_5_dollars}	= 0;
	$t{enable_10_dollars}	= 0;
	$t{enable_20_dollars}	= 0;
	#
	# pega dados do status
	$sql = "
	SELECT 1,1,service_status.can_add_credit, service_status.can_auto_recharge, service_status.limit_max_balance 
	FROM service, service_status 
	where service.status=service_status.id and service.id='$app{service_id}' 
	";
	%hash = database_select_as_hash($sql,"flag,can_add_credit,can_auto_recharge,limit_max_balance");
	if ($hash{1}{flag} eq 1) {
		$t{can_add_credit}		= ($hash{1}{can_add_credit} eq 1) ? 1 : 0;
		$t{can_auto_recharge}	= ($hash{1}{can_auto_recharge} eq 1) ? 1 : 0;
		#$t{enable_5_dollars}	= ($hash{1}{limit_max_balance}>=5) ? 1 : 0;
		#$t{enable_10_dollars}	= ($hash{1}{limit_max_balance}>=10) ? 1 : 0;
		#$t{enable_20_dollars}	= ($hash{1}{limit_max_balance}>=20) ? 1 : 0;
		$t{enable_5_dollars}	= 1;
		$t{enable_10_dollars}	= 1;
		$t{enable_20_dollars}	= 1;
	}
	#
	# check CIM profile
	#%tmp_hash = &multilevel_securedata_cc_get($app{service_id});
	#$t{cim_profile_is_ok} 		= ($tmp_hash{status_ok} eq 1) ? 1 : 0;
	#$t{cc_number}				= $tmp_hash{cc_number};
	#$t{cc_first_name}			= $tmp_hash{first_name};
	#$t{cc_last_name}			= $tmp_hash{last_name};
	%tmp_hash = &multilevel_securedata_cc_get($app{service_id},"DO_NOT_CHECK_CC_ERROR");
	$t{profile_exists} 			= ($tmp_hash{status_ok} eq 1) ? 1 : 0;
	$t{profile_with_cc_errors}	= ($tmp_hash{cc_error} eq 1) ? 1 : 0;
	$t{profile_ok}				= ($t{profile_exists}.$t{profile_with_cc_errors} eq "10") ? 1 : 0; 
	$t{profile_cc_number}		= $tmp_hash{cc_number};
	$t{profile_cc_first_name}	= $tmp_hash{first_name};
	$t{profile_cc_last_name}	= $tmp_hash{last_name};
	$t{auto_recharge_threshold}	= &data_get("service_data",$app{service_id},"ar_threshold");
	$t{auto_recharge_value}		= &data_get("service_data",$app{service_id},"ar_value");
	$t{auto_recharge_but}		= &data_get("service_data",$app{service_id},"ar_limit");
	$t{auto_recharge_threshold}	= ($t{auto_recharge_threshold}	eq "") ? $t{auto_recharge_default_threshold}	: $t{auto_recharge_threshold};
	$t{auto_recharge_value}		= ($t{auto_recharge_value} 	eq "") ? $t{auto_recharge_default_value} 		: $t{auto_recharge_value};
	$t{auto_recharge_but}		= ($t{auto_recharge_but} 		eq "") ? $t{auto_recharge_default_but}			: $t{auto_recharge_but};
	$t{auto_recharge_but}		= ($t{auto_recharge_but} 		eq "") ? $t{auto_recharge_default_but}			: $t{auto_recharge_but};
	#
	# check auto_recharge data
	%hash = database_select_as_hash("SELECT 1,1,is_auto_recharge FROM service_profile_cc where service_id='$app{service_id}' and active=1","flag,value");
	$t{auto_recharge_enabled} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} eq 1) ) ? 1 : 0;
    #
    # action save
	if ( ($t{status_error} eq 0) && ($t{can_auto_recharge} eq 1) && ($t{profile_ok} eq 1) && ($form{save} eq 1) ){
		#
		# click check
		$tmp = &active_session_get("click_check_cim_automatic");
		unless ( ($form{click_check} ne "") && ($tmp ne "") && ($form{click_check} eq $tmp)  ) {
			$t{status_error} = 1;
			$t{error_message_no_click_check} = 1;
		}
		#
		# auto recarge values check
		$form{enabled}	= ($form{enabled} eq 1) ? 1 : 0;
		$form{threshold}= (index($t{auto_recharge_valid_values_threshold},"|$form{threshold}|") 	eq -1) ? $t{auto_recharge_default_threshold} 	: $form{threshold};
		$form{value} 	= (index($t{auto_recharge_valid_values_value},"|$form{value}|") 			eq -1) ? $t{auto_recharge_default_value} 		: $form{value};
		$form{but} 		= (index($t{auto_recharge_valid_values_but},"|$form{but}|") 				eq -1) ? $t{auto_recharge_default_but} 		: $form{but};
 	 
		#
		# save change
		if ($t{status_error} eq 0) {
			#
			# update autorecharge data
			$sql = "update service_profile_cc set is_auto_recharge='$form{enabled}' where service_id='$app{service_id}' and active=1";
			&database_do($sql);
			if ($form{enabled} eq 1) {
				&data_set("service_data",$app{service_id},"ar_threshold",$form{threshold});
				&data_set("service_data",$app{service_id},"ar_value",$form{value});
				&data_set("service_data",$app{service_id},"ar_limit",$form{but});
				&action_history("ar:status:on",('service_id'=>$app{service_id}));		
				&multilevel_change_service_status_by_switch_on_data($app{service_id},"switch_on_autorecharge_in");
			} else {
				&data_delete("service_data",$app{service_id},"ar_threshold");
				&data_delete("service_data",$app{service_id},"ar_value");
				&data_delete("service_data",$app{service_id},"ar_limit");
				&action_history("ar:status:off",('service_id'=>$app{service_id}));			
				&multilevel_change_service_status_by_switch_on_data($app{service_id},"switch_on_autorecharge_out");
			}
			#
			# update coupon engine
			&multilevel_coupon_engine_autorecharge($app{service_id});
			#
			# redirect to to credit or autoapply autorecharge bouton (over web) ## bulshit! no more complex promotion logics
			#if (&multilevel_coupon_engine_autorecharge_can_assign($app{service_id}) eq 1) {
			#	&cgi_redirect("$my_url?action=coupons&assign=1");
			#} else {
			#	&cgi_redirect("$my_url?action=credits");
			#}
			#
			# flag save is ok, so template can prompt message and reload if want
			$t{status_save_ok} = 1;
		}
	}
    #
    # load form
	if ($form{save} ne 1){
		$form{enabled}	= $t{auto_recharge_enabled};
		$form{threshold}= $t{auto_recharge_threshold};
		$form{value}	= $t{auto_recharge_value};
		$form{but}		= $t{auto_recharge_but};
	}
    #
    # monta o form
 	$t{form_enabled} 	= $form{enabled}; 
 	$t{form_threshold}	= $form{threshold}; 
 	$t{form_value} 	= $form{value}; 
 	$t{form_but} 		= $form{but};
	$t{"form_select_threshold_".$form{threshold}}	= "selected";
	$t{"form_select_value_".$form{value}} 			= "selected";
	$t{"form_select_but_".$form{but}} 				= "selected";
	$t{click_check} = time;
	&active_session_set("click_check_cim_automatic",$t{click_check});
    #
    # print page
	$t{debug} .= " <br>";
	$t{debug} .= " <br>";
    $t{my_url}					= $my_url;
	$t{service_id}				= $app{service_id};
	$t{service_alert}			= $app{service_alert};
	$t{service_name}			= $app{service_name};
	$t{service_email}			= $app{service_email};
	$t{service_credit}			= &format_number($app{service_credits},2);
	$t{service_credits_bar}	= $app{service_credits_bar};
    &template_print("template.myaccount.credits.add.cim.automatic.html",%t);	
}
sub do_credits_buy_cim_manual(){
	#
	# start
	%t = %template_default;
	$t{status_ok}						= 0;
    $t{status_error}					= 0;
	$t{enable_2_dollars}				= 1;
	$t{enable_3_dollars}				= 1;
	$t{enable_5_dollars}				= 1;
	$t{enable_10_dollars}				= 1;
	$t{enable_20_dollars}				= 1;
	$t{can_add_credit}					= 0;
	$t{limit_max_balance}				= 0;
	$t{limit_max_recharges_in_7days}	= 0;
	$t{balance}							= 0;
	$t{all_credits_sum}					= 0;
	$t{switch_on_first_credit}			= "";
	#
	# enable os valores de acordo com as recargas
	#%hash = database_select_as_hash("SELECT 1,1,count(*) FROM credit where service_id='$app{service_id}' and value>0","flag,count");
	#if ($hash{1}{flag} eq 1) {
	#	if ($hash{1}{count} eq 0){
	#		$t{enable_2_dollars}				= 1;
	#		$t{enable_3_dollars}				= 1;
	#		$t{enable_5_dollars}				= 1;
	#		$t{enable_10_dollars}				= 0;
	#		$t{enable_20_dollars}				= 0;
	#	} elsif ($hash{1}{count} <= 3){
	#		$t{enable_2_dollars}				= 0;
	#		$t{enable_3_dollars}				= 1;
	#		$t{enable_5_dollars}				= 1;
	#		$t{enable_10_dollars}				= 1;
	#		$t{enable_20_dollars}				= 0;
	#	} else {
	#		$t{enable_2_dollars}				= 0;
	#		$t{enable_3_dollars}				= 0;
	#		$t{enable_5_dollars}				= 1;
	#		$t{enable_10_dollars}				= 1;
	#		$t{enable_20_dollars}				= 1;
	#	}
	#}
	$t{enable_2_dollars}				= 0;
	$t{enable_3_dollars}				= 0;
	$t{enable_5_dollars}				= 1;
	$t{enable_10_dollars}				= 1;
	$t{enable_20_dollars}				= 1;
	$t{enable_50_dollars}				= 1;
	#
	# pega dados do status
	$sql = "
	SELECT
		1, 1,
		service_status.can_add_credit, service_status.switch_on_first_credit, 
		service_status.limit_max_balance, service_status.limit_max_recharges_in_7days,
		service.balance, service.limit
	FROM service, service_status
	where service.status=service_status.id and service.id='$app{service_id}'
	";
	%hash = database_select_as_hash($sql,"flag,can_add_credit,switch_on_first_credit,limit_max_balance,limit_max_recharges_in_7days,balance,limit");
	if ($hash{1}{flag} eq 1) {
		if ($hash{1}{limit_max_balance} < 11){
			$t{enable_2_dollars}				= 0;
			$t{enable_3_dollars}				= 0;
			$t{enable_5_dollars}				= 1;
			$t{enable_10_dollars}				= 1;
			$t{enable_20_dollars}				= 0;
			$t{enable_50_dollars}				= 0;
		}
		$t{enable_2_dollars}				= ($hash{1}{limit_max_balance}<=2) ? 0 : $t{enable_2_dollars};
		$t{enable_3_dollars}				= ($hash{1}{limit_max_balance}<=3) ? 0 : $t{enable_3_dollars};
		$t{enable_5_dollars}				= ($hash{1}{limit_max_balance}<=5) ? 0 : $t{enable_5_dollars};
		$t{enable_10_dollars}				= ($hash{1}{limit_max_balance}<=10) ? 0 : $t{enable_10_dollars};
		$t{enable_20_dollars}				= ($hash{1}{limit_max_balance}<=20) ? 0 : $t{enable_20_dollars};
		$t{enable_50_dollars}				= ($hash{1}{limit_max_balance}<=50) ? 0 : $t{enable_50_dollars};
		$t{can_add_credit}					= ($hash{1}{can_add_credit} eq 1) ? 1 : 0;
		$t{limit_max_balance}				= $hash{1}{limit_max_balance};
		$t{limit_max_recharges_in_7days}	= $hash{1}{limit_max_recharges_in_7days};
		$t{balance}							= $hash{1}{balance}-$hash{1}{limit};
		$t{switch_on_first_credit}			= $hash{1}{switch_on_first_credit};
	}
	$sql = "
	SELECT 1,1,sum(value)
	FROM credit 
	where service_id='$app{service_id}' and date>date_sub(now(), interval 7 day) and value>0
	";
	%hash = database_select_as_hash($sql,"flag,value");
	$hash{1}{value} = ($hash{1}{value} eq "") ? 0: $hash{1}{value}; 
	$t{recharges_in_7_days} = ($hash{1}{flag} eq 1) ? $hash{1}{value} : 0; 
	$sql = "
	SELECT 1,1,sum(value)
	FROM credit 
	where service_id='$app{service_id}' and value>0
	";
	%hash = database_select_as_hash($sql,"flag,value");
	$hash{1}{value} = ($hash{1}{value} eq "") ? 0: $hash{1}{value}; 
	$t{all_credits_sum} = ($hash{1}{flag} eq 1) ? $hash{1}{value} : 0; 
	#
	# check CIM profile
	%tmp_hash = &multilevel_securedata_cc_get($app{service_id},"DO_NOT_CHECK_CC_ERROR");
	$t{profile_exists} 			= ($tmp_hash{status_ok} eq 1) ? 1 : 0;
	$t{profile_with_cc_errors}	= ($tmp_hash{cc_error} eq 1) ? 1 : 0;
	$t{profile_ok}				= ($t{profile_exists}.$t{profile_with_cc_errors} eq "10") ? 1 : 0; 
	$t{profile_cc_number}		= $tmp_hash{cc_number};
	$t{profile_cc_first_name}	= $tmp_hash{first_name};
	$t{profile_cc_last_name}	= $tmp_hash{last_name};
	#%tmp_hash = &multilevel_securedata_cc_get($app{service_id});
	#$t{cim_profile_is_ok} 	= ($tmp_hash{status_ok} eq 1) ? 1 : 0;
	#$t{cc_contact_number}	= $tmp_hash{contact_number};
	#$t{cc_type}			= $tmp_hash{cc_type};
	#$t{cc_number}			= $tmp_hash{cc_number};
	#$t{cc_date}			= $tmp_hash{cc_date};
	#$t{cc_code}			= $tmp_hash{cc_code};
	#$t{cc_first_name}		= $tmp_hash{first_name};
	#$t{cc_last_name}		= $tmp_hash{last_name};
	#$t{cc_address}			= $tmp_hash{address};
	#$t{cc_country}			= $tmp_hash{country};
	#$t{cc_city}			= $tmp_hash{city};
	#$t{cc_state}			= $tmp_hash{state};
	#$t{cc_zip}				= $tmp_hash{zip};
    #
    # confere form
	if ( ($t{status_error} eq 0) && ($t{can_add_credit} eq 1) && ($t{profile_ok} eq 1) && ($form{save} eq 1) ){
		#
		# click check
		unless ($form{agree} eq 1) {
			$t{status_error} = 1;
			$t{error_message_no_agree} = 1;
		}
		#
		# click check
		$tmp = &active_session_get("click_check_cim_manual");
		unless ( ($form{click_check} ne "") && ($tmp ne "") && ($form{click_check} eq $tmp)  ) {
			$t{status_error} = 1;
			$t{error_message_no_click_check} = 1;
		}
		#
		# check value
		unless (
			( ($form{value} eq 2)	&& ($t{enable_2_dollars}	eq 1) ) || 
			( ($form{value} eq 3)	&& ($t{enable_3_dollars}	eq 1) ) || 
			( ($form{value} eq 5)	&& ($t{enable_5_dollars}	eq 1) ) || 
			( ($form{value} eq 10)	&& ($t{enable_10_dollars}	eq 1) ) || 
			( ($form{value} eq 20)	&& ($t{enable_20_dollars}	eq 1) ) ||  
			( ($form{value} eq 50)	&& ($t{enable_50_dollars}	eq 1) ) 
			) {
			$t{status_error} = 1;
			$t{error_message_wrong_value} = 1;
		}
	}
	#
	# second check (limits)
	if ( ($t{status_error} eq 0) && ($t{can_add_credit} eq 1) && ($t{profile_ok} eq 1) && ($form{save} eq 1) ){
		if ( ($t{limit_max_recharges_in_7days} > 0) && ($t{recharges_in_7_days} > $t{limit_max_recharges_in_7days}) ) {
			$t{status_error} = 1;
			$t{error_message_max_recharges_in_7days} = 1;
		} elsif ( ($t{limit_max_balance} > 0) && ($t{balance}+$form{value} > $t{limit_max_balance}) ) {
			$t{status_error} = 1;
			$t{error_message_max_balance} = 1;
		}
	}
    #
    # add charge
	if ( ($t{status_error} eq 0) && ($t{can_add_credit} eq 1) && ($t{profile_ok} eq 1) && ($form{save} eq 1) ){
		%order = ();
		$order{service_id}			= $app{service_id};
		$order{value_credit}		= $form{value};
		$order{value_money}			= $form{value};
		$order{type}				= "AUTHORIZE_CIM";
		$order{from_type}			= "WEB";
		%answer = &multilevel_credit_add(%order);
		if ($answer{ok} ne 1)  {
			$t{status_error} = 1;
			$t{error_message_not_aproved} = 1;
			&action_history("cim:payment:recharge:error",('service_id'=>$app{service_id}));
		} else {
			$t{status_ok} = 1;
			&action_history("cim:payment:recharge",('service_id'=>$app{service_id},'credit_id'=>$answer{new_credit_id}));
			if ( ($t{all_credits_sum} eq 0)  && ($t{switch_on_first_credit} ne "") ) {
				&database_do("update service set last_change=now(), status='$t{switch_on_first_credit}' where id='$app{service_id}'");
				&action_history("status:first_recharge",('service_id'=>$app{service_id}));
				%answer = &multilevel_suspicious_check(('service_id'=>$app{service_id}, 'force_suspicious_if_no_validated_ani'=>1));
			} else {
				%answer = &multilevel_suspicious_check(('service_id'=>$app{service_id}));
			}
		}
	}
    #
    # monta o form
    $t{click_check} = time;
	&active_session_set("click_check_cim_manual",$t{click_check});
	$t{balance} 						= &format_number($t{balance},2);
	$t{limit_max_balance} 				= &format_number($t{limit_max_balance},2);
	$t{recharges_in_7_days} 			= &format_number($t{recharges_in_7_days},2);
	$t{limit_max_recharges_in_7days} 	= &format_number($t{limit_max_recharges_in_7days},2);
    #
    # print page
    $t{my_url}					= $my_url;
	$t{service_id}				= $app{service_id};
	$t{service_alert}			= $app{service_alert};
	$t{service_name}			= $app{service_name};
	$t{service_email}			= $app{service_email};
	$t{service_credit}			= &format_number($app{service_credits},2);
	$t{service_credits_bar}		= $app{service_credits_bar};
    &template_print("template.myaccount.credits.add.cim.manual.html",%t);	
}
sub do_credits_buy_cc() {
	#
	# pega dados do status
    %t = %template_default;
	$sql = "
	SELECT 1, 1, service_status.can_add_credit, service_status.limit_max_balance, service_status.limit_max_recharges_in_7days
	FROM service, service_status
	where service.status=service_status.id and service.id='$app{service_id}'
	";
	%hash = database_select_as_hash($sql,"flag,can_add_credit,limit_max_balance,limit_max_recharges_in_7days");
	if ($hash{1}{flag} eq 1) {
		$t{dic}{enable_5_dollars}	= ($hash{1}{limit_max_balance}>5) ? 1 : 0;
		$t{dic}{enable_10_dollars}	= ($hash{1}{limit_max_balance}>10) ? 1 : 0;
		$t{dic}{enable_20_dollars}	= ($hash{1}{limit_max_balance}>20) ? 1 : 0;
		$t{dic}{recharge_disabled}	= ($hash{1}{can_add_credit} eq 1) ? 0 : 1;
	} else {
		$t{dic}{enable_5_dollars}	= 0;
		$t{dic}{enable_10_dollars}	= 0;
		$t{dic}{enable_20_dollars}	= 0;
		$t{dic}{recharge_disabled}	= 1;
	}
	#
	# tenta add o credito
	$answer_ok 		= 0;
	$answer_message	= "";
	if ( ($form{save} eq 1) && ($t{dic}{recharge_disabled} eq 0) ) {
		$allow_values	= "|";
		$allow_values	.= ($t{dic}{enable_5_dollars} eq 1) ? "5|" : "";
		$allow_values	.= ($t{dic}{enable_10_dollars} eq 1) ? "10|" : "";
		$allow_values	.= ($t{dic}{enable_20_dollars} eq 1) ? "20|" : "";
		$answer_ok = 0;
		$answer_message= "Unknown error";
		$html = "<script>parent.iframe_answer(0,'Unknown error')</script>";
		#
		# pega dados do form
		$form{cc_number}	= trim(clean_int(substr($form{cc_number},0,100)));;
		$form{cc_date_1}	= trim(clean_int(substr($form{cc_date_1},0,100)));
		$form{cc_date_1}	= trim(clean_int(substr($form{cc_date_1},0,100)));
		$form{cc_fname}		= trim(clean_str(substr($form{cc_fname},0,100)));
		$form{cc_lname}		= trim(clean_str(substr($form{cc_lname},0,100)));
		$form{cc_code}		= trim(clean_int(substr($form{cc_code},0,100)));
		$form{address}		= trim(clean_str(substr($form{address},0,100)));
		$form{city}			= trim(clean_str(substr($form{city},0,100)));
		$form{state}		= trim(clean_str(substr($form{state},0,100)));
		$form{zip}			= trim(clean_str(substr($form{zip},0,100)));
		#
		# pega dados do servico
		%service_info = ();
		$service_info{switch_on_first_credit}		= "";
		$service_info{limit_max_balance} 			= 0;
		$service_info{limit_max_recharges_in_7days} = 0;
		$service_info{all_credits_qtd} 				= -1; 
		$service_info{all_credits_sum} 				= -1;
		$service_info{week_credits_qtd} 			= -1; 
		$service_info{week_credits_sum} 			= -1;
		%hash = database_select_as_hash("
			SELECT
				1,
				1,
				service_status.switch_on_first_credit,
				service_status.limit_max_balance,
				service_status.limit_max_recharges_in_7days
			FROM
				service,
				service_status
			where
				service.status=service_status.id and
				service.id='$app{service_id}'
			","flag,switch_on_first_credit,limit_max_balance,limit_max_recharges_in_7days"
			);
		if ($hash{1}{flag} eq 1) {
			$service_info{switch_on_first_credit}		= $hash{1}{switch_on_first_credit};
			$service_info{limit_max_balance} 			= $hash{1}{limit_max_balance};
			$service_info{limit_max_recharges_in_7days} = $hash{1}{limit_max_recharges_in_7days};
		}
		%hash = database_select_as_hash("
			SELECT 1,1,count(*),sum(value)
			FROM credit 
			where service_id='$app{service_id}' and date>date_sub(now(), interval 7 day) and value>0
			","flag,qtd,value"
			);
		if ($hash{1}{flag} eq 1) {
			$service_info{week_credits_qtd} = $hash{1}{qtd}; 
			$service_info{week_credits_sum} = $hash{1}{value};
		}
		%hash = database_select_as_hash("
			SELECT 1,1,count(*),sum(value)
			FROM credit 
			where service_id='$app{service_id}' and value>0
			","flag,qtd,value"
			);
		if ($hash{1}{flag} eq 1) {
			$service_info{all_credits_qtd} = $hash{1}{qtd}; 
			$service_info{all_credits_sum} = $hash{1}{value};
		}
		#
		# confere os dados
		if ($form{cc_number} eq "") {
			$answer_ok = 0;
			$answer_message= "Please fill card number";
		} elsif ( ($form{cc_date_1} eq "") || ($form{cc_date_2} eq "") ){
			$answer_ok = 0;
			$answer_message= "Please fill expiration date ($form{cc_date_1})($form{cc_date_2})";
		} elsif ($form{cc_code} eq "") {
			$answer_ok = 0;
			$answer_message= "Please fill card code";
		} elsif ($form{cc_fname} eq "") {
			$answer_ok = 0;
			$answer_message= "Please fill first name";
		} elsif ($form{cc_lname} eq "") {
			$answer_ok = 0;
			$answer_message= "Please fill last name";
		} elsif ($form{address} eq "") {
			$answer_ok = 0;
			$answer_message= "Please fill address";
		} elsif ($form{city} eq "") {
			$answer_ok = 0;
			$answer_message= "Please fill city";
		} elsif ($form{state} eq "") {
			$answer_ok = 0;
			$answer_message= "Please fill state";
		} elsif ($form{zip} eq "") {
			$answer_ok = 0;
			$answer_message= "Please fill zip";
		} elsif (index($allow_values,"|$form{value}|") eq -1) {
			$answer_ok = 0;
			$answer_message= "Incorrect value";
		} elsif ( ($service_info{limit_max_recharges_in_7days} > 0) && ($service_info{week_credits_sum} > $service_info{limit_max_recharges_in_7days}) ) {
			$answer_ok = 0;
			$answer_message= "Week Credit Card recharge limit is is \$".$service_info{limit_max_recharges_in_7days};
		} elsif ( ($service_info{limit_max_balance} > 0) && ($app{service_credits}+$form{value} > $service_info{limit_max_balance}) ) {
			$answer_ok = 0;
			$answer_message= "Your maximum balance limit is \$".$service_info{limit_max_balance};
		} else {
			%order = ();
			$order{service_id}			= $app{service_id};
			$order{value_credit}		= $form{value};
			$order{value_money}			= $form{value};
			$order{card_number}			= $form{cc_number};
			$order{card_date}			= substr("00".$form{cc_date_1},-2,2). substr("00".$form{cc_date_2},-2,2);
			$order{card_first_name}		= $form{cc_fname};
			$order{card_last_name}		= $form{cc_lname};
			$order{card_code}			= $form{cc_code};
			$order{card_address}		= $form{address};
			$order{card_city}			= $form{city};
			$order{card_sate}			= $form{state};
			$order{card_zip}			= $form{zip};
			$order{card_check_detail} 	= 0;
			$order{type}				= "AUTHORIZE_CC";
			$order{from_type}			= "WEB";
			%answer = &multilevel_credit_add(%order);
			$answer_ok = $answer{ok};
			$answer_message= ($answer{message} eq "Aproved") ? "Your credit was approved": "I can not approve this credit. ".$answer{message};
			#
			# log CC errors
			if ($answer_ok ne 1)  {
				&action_history("security:bad_cc_recharge",('service_id'=>$app{service_id}));
			} else {
				&action_history("security:cc_recharge",('service_id'=>$app{service_id}));
			}
			#
			# unlock pin if add value and first credit
			if ($answer_ok eq 1) {
				if ( ($service_info{all_credits_qtd} eq 0)  && ($service_info{switch_on_first_credit} ne "") ) {
					&database_do("update service set last_change=now(), status='$service_info{switch_on_first_credit}' where id='$app{service_id}'");
					&action_history("status:first_recharge",('service_id'=>$app{service_id}));
					%answer = &multilevel_suspicious_check(('service_id'=>$app{service_id}, 'force_suspicious_if_no_validated_ani'=>1));
				} else {
					%answer = &multilevel_suspicious_check(('service_id'=>$app{service_id}));
				}
			}
		}
	}
    #
    # print page
    $t{dic}{my_url}					= $my_url;
    $t{dic}{answer_ok}				= $answer_ok;
    $t{dic}{answer_message}			= $answer_message;
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
    &template_print("template.myaccount.credits.add.cc.html",%t);
	#&cgi_hearder_html();
	#print qq[
	#$answer_reload<br>
	#$answer_message<br>
	#<script>parent.iframe_answer($answer_reload,"$answer_message");</script>
	#];
	#foreach (sort keys %form) { print "FORM $_=$form{$_}<br>" } 
}
sub do_credits_profile(){
	#
   	#----------------------------------------------------- 
	# start and load some basic data
   	#----------------------------------------------------- 
	%t = %template_default;
	$t{status_code}			= "";
	$t{status_is_ok}		= 0;
    $t{status_is_error}		= 0;
	$t{status_is_alert}		= 0;
    $t{click_id_prefix}		= "Cp";
    $t{user_action}			= "ADD";
    $t{user_action}			= ($form{delete_profile} 	eq 1) ? "DEL" 		: $t{user_action};
    $t{user_action}			= ($form{dial_code} 		eq 1) ? "DIAL_CODE"	: $t{user_action};
    #
   	#----------------------------------------------------- 
    # load some permissions by status
   	#----------------------------------------------------- 
	%hash 								= database_select_as_hash("select 1,1,service_status.need_ani_check,service_status.can_add_credit from service,service_status where service.id='$app{service_id}' and service.status=service_status.id ","flag,need_ani_check,can_add_credit");
	$t{service_need_ani_check}	= ( ($hash{1}{flag} eq 1) && ($hash{1}{need_ani_check} eq 1) ) ? 1 : 0;
	$t{service_can_add_credit}	= ( ($hash{1}{flag} eq 1) && ($hash{1}{can_add_credit} eq 1) ) ? 1 : 0;
	#

	#----------------------------------------------------- 
        # load referral name
   	#----------------------------------------------------- 
	 %hash = database_select_as_hash("select 1,1, service.name,service_status.name from service,service_tree,service_status where service_tree.service_id='$app{service_id}' and service.id=service_tree.parent_service_id  and service_status.id = service.status","flag,name,status");
	$referer_name=  ($hash{1}{flag} eq 1)   ? $hash{1}{name} : '';
	$referer_status =  ($hash{1}{flag} eq 1)   ? $hash{1}{status} : '';
 	#

   	#----------------------------------------------------- 
	# load cc profile 
   	#----------------------------------------------------- 
	%hash = &multilevel_securedata_cc_get($app{service_id},"DO_NOT_CHECK_CC_ERROR");
	$t{user_action_allow_add}= 1;
	$t{user_action_allow_del}= 0;
	$t{active_profile_exists}			= 0;
	$t{active_profile_exists} 			= ($hash{status_ok} eq 1) ? 1 : 0;
	$t{active_profile_with_cc_errors}	= ($hash{cc_error} eq 1) ? 1 : 0;
	$t{active_profile_ok}				= ($t{active_profile_exists}.$t{active_profile_with_cc_errors} eq "10") ? 1 : 0; 
	$t{active_profile_is_auto_recharge}	= ( ($hash{status_ok} eq 1) && ($hash{is_auto_recharge} eq 1) ) ? 1 : 0;
	$t{active_profile_type}				= $hash{cc_type};
	$t{active_profile_cc_number}		= ($hash{cc_number} eq "") ? "" : substr("******************************".$hash{cc_number},-16,16);
	$t{active_profile_cc_date}			= $hash{cc_date};
	$t{active_profile_cc_date_1}		= substr($hash{cc_date},0,2);
	$t{active_profile_cc_date_2}		= substr($hash{cc_date},2,2);
	$t{active_profile_cc_code}			= ($hash{cc_number} eq "") ? "" : "*****";
	$t{active_profile_cc_first_name}	= $hash{first_name};
	$t{active_profile_cc_last_name}		= $hash{last_name};
	$t{active_profile_contact_number}	= $hash{contact_number};
	$t{active_profile_address}			= $hash{address};
	$t{active_profile_country}			= $hash{country};
	$t{active_profile_city}				= $hash{city};
	$t{active_profile_state}			= $hash{state};
	$t{active_profile_zip}				= $hash{zip};
	if ($hash{status_ok} eq 1) {
		$t{user_action_allow_add}	= 0;
		$t{user_action_allow_del}	= 1;
	}
    #
   	#----------------------------------------------------- 
    # validate form format
   	#----------------------------------------------------- 
   	if ($form{click_id} eq "") {
   		# do nothing, no data posted, just load data into form and print page
   	} else {
	    if ($ENV{REQUEST_METHOD} ne "POST"){
			$t{status_is_error}	= 1;
			$t{status_code}	= 401;
	    } else {
 	 	  	if (&multilevel_clickchain_check($t{click_id_prefix},$form{click_id}) ne 1) {
				$t{status_is_error}	= 1;
				$t{status_code}	= 403;
 	 	  	}
	    	
	    }
   	}
    #
   	#----------------------------------------------------- 
    # check add action
   	#----------------------------------------------------- 
 	if ( ($form{click_id} ne "") && ($t{user_action} eq "ADD") && ($t{status_code} eq "") ) {
 		#
	   	#--------------------------
 		# check basic things
	   	#--------------------------
		foreach (qw(contact_zip contact_state contact_city contact_country contact_address contact_number profile_type pp_name pp_id cc_last_name cc_first_name cc_code cc_date_2 cc_date_1 cc_number)){ $form{$_} = &trim(substr($form{$_},0,254)); }
		$form{profile_type} = (index("|amex|discovery|master|visa|paypal|","|$form{profile_type}|") eq -1) ? "" : $form{profile_type};
		$tmp = "";
		$tmp = ($form{contact_zip} 		eq "") ? 110 : $tmp ;
		$tmp = ($form{contact_state} 	eq "") ? 109 : $tmp ;
		$tmp = ($form{contact_city} 	eq "") ? 108 : $tmp ;
		$tmp = ($form{contact_country} 	eq "") ? 113 : $tmp ;
		$tmp = ($form{contact_address} 	eq "") ? 107 : $tmp ;
		$tmp = ($form{contact_number} 	eq "") ? 111 : $tmp ;
		$tmp = ($form{profile_type} 	eq "") ? 101 : $tmp ;
		$tmp = ($form{cc_last_name} 	eq "") ? 106 : $tmp ;
		$tmp = ($form{cc_first_name}	eq "") ? 105 : $tmp ;
		$tmp = ($form{cc_code} 			eq "") ? 104 : $tmp ;
		$tmp = ($form{cc_date_2} 		eq "") ? 103 : $tmp ;
		$tmp = ($form{cc_date_1} 		eq "") ? 103 : $tmp ;
		$tmp = ($form{cc_number} 		eq "") ? 102 : $tmp ;
		$tmp = ($form{profile_type} 	eq "") ? 101 : $tmp ;
		$tmp = ($t{user_action_allow_add} ne 1) ? 100 : $tmp ;
		if ($tmp ne "") {
			$t{status_is_error}	= 1;
			$t{status_code}		= $tmp;
		}
		#
		#--------------------------
		# clean form
		#--------------------------
		# BUG-FIXED: if we dont clean, API will reject data and user interface will not accept data
		foreach (qw(contact_zip contact_state contact_city contact_country contact_address contact_number profile_type cc_last_name cc_first_name cc_code cc_date_2 cc_date_1 cc_number profile_type)) {
			$form{$_} = &clean_str($form{$_}," /-_–(\@)-,=+;.<>[]:?<>","MINIMAL");
		}
 		#
	   	#--------------------------
 		# check extra things
	   	#--------------------------
		if ( ($t{status_is_error} eq 0) && ($t{status_code} eq "") ) {
			$tmp = "";
			$number = clean_int(substr($form{contact_number},0,1024));
			($flag,$number_e164,$tmp2) = &multilevel_check_E164_number($number);
			if 		($flag eq "USANOAREACODE") 			{ $tmp = 1111;	}
			elsif	($flag eq "UNKNOWNCOUNTRY") 		{ $tmp = 1112;	}
			elsif 	($flag ne "OK") 					{ $tmp = 1113;	}
			else 	{
				$form{contact_number_fixed} = $number_e164;
				$number 					= $number_e164;
				%hash 						= database_select_as_hash("select 1,1,service_status.rate_slot_callback from service, service_status where service.id='$app{service_id}' and service.status = service_status.id  and service_status.deleted = 0 ","flag,id");
				$number_rate_id				= ( ($hash{1}{flag} eq "1") && ($hash{1}{id} ne "") ) ? $hash{1}{id} : "";
				if ($number_rate_id eq "") { 
					$tmp = 1114;
				} else {
					%hash = &multilevel_rate_table_get($number,$number_rate_id);
					if ($hash{ok_to_use} ne 1) 			{ $tmp = 1114;	}
				}
			}
			if ($tmp ne "") {
				$t{status_is_error}	= 1;
				$t{status_code}		= $tmp;
			}
		}
 		#
	   	#--------------------------
 		# create securedata_cc
	   	#--------------------------
		%securedata_cc = ();
		if ( ($t{status_is_error} eq 0) && ($t{status_code} eq "") ) {
			$securedata_cc{cc_type} 		= $form{profile_type};
			$securedata_cc{cc_number} 		= $form{cc_number};
			$securedata_cc{cc_date}			= substr("00".$form{cc_date_1},-2,2).substr("00".$form{cc_date_2},-2,2);
			$securedata_cc{cc_code} 		= $form{cc_code};
			$securedata_cc{first_name}		= $form{cc_first_name};
			$securedata_cc{last_name}		= $form{cc_last_name};
			$securedata_cc{address} 		= $form{contact_address};
			$securedata_cc{country} 		= $form{contact_country};
			$securedata_cc{city} 			= $form{contact_city};
			$securedata_cc{state} 			= $form{contact_state};
			$securedata_cc{zip} 			= $form{contact_zip};
			$securedata_cc{contact_number}	= $form{contact_number_fixed};
			$securedata_cc{service_id} 		= $app{service_id};
		}
 		#
	   	#--------------------------
 		# check switch_on_enter_blacklisted_CC and can_enter_blacklisted_CC
	   	#--------------------------
		if ( ($t{status_is_error} eq 0) && ($t{status_code} eq "") ) {
			$securedata_cc{cc_fingerprint}	= key_md5("CC|$securedata_cc{cc_number}|$securedata_cc{cc_date}");
			$securedata_cc{cc_is_blocked}	= &multilevel_securedata_cc_block_is_fingerprint_blocked($securedata_cc{cc_fingerprint});
			if ($securedata_cc{cc_is_blocked} eq 1) {
				if (&multilevel_service_status_get_value($securedata_cc{service_id},"can_enter_blacklisted_CC") ne 1) {
					$t{status_is_error}	= 1;
					$t{status_code}		= 2001;
					&log_debug_add("type=securedata_cc_set,error=blacklisted_CC,service_id=$securedata_cc{service_id}",%securedata_cc);
					&action_history("suspicious:addblockcard",('value_old'=>$securedata_cc{cc_fingerprint},'service_id'=>$securedata_cc{service_id}));
				}
				&multilevel_service_status_change_if_need($securedata_cc{service_id},"switch_on_enter_blacklisted_CC");
			}
		}
 		#
	   	#--------------------------
 		# check switch_on_enter_CC_active_in_another_service and can_enter_CC_active_in_another_service
	   	#--------------------------
		if ( ($t{status_is_error} eq 0) && ($t{status_code} eq "") ) {
			# how many times this card was used by other service_ids
			$sql = "SELECT 1,1,count(*) FROM credit_detail_authorize where card_fingerprint='$securedata_cc{cc_fingerprint}' and credit_id is not null and service_id <> '$securedata_cc{service_id}' ";
			%hash = database_select_as_hash($sql,"flag,value");
			$tmp_used_by_other_service_ids = (($hash{1}{flag} eq 1) && ($hash{1}{value} eq 0)) ? 0 : 1;
			#
			# how many times this card is ACTIVE in another CC profiles
			$sql = "SELECT 1,1,count(*)	FROM service_profile_cc where cc_fingerprint = '$securedata_cc{cc_fingerprint}' and service_id <> '$securedata_cc{service_id}' and active = 1";
			%hash = database_select_as_hash($sql,"flag,value");
			$tmp_active_in_other_service_ids = (($hash{1}{flag} eq 1) && ($hash{1}{value} eq 0)) ? 0 : 1;
			#
			# do the action
			if ( ($tmp_used_by_other_service_ids eq 1) || ($tmp_active_in_other_service_ids eq 1) )  {
				if (&multilevel_service_status_get_value($securedata_cc{service_id},"can_enter_CC_active_in_another_service") ne 1) {
					$t{status_is_error}	= 1;
					$t{status_code}		= 2002;
					&log_debug_add("type=securedata_cc_set,error=CC_active_in_another_service,service_id=$securedata_cc{service_id}",%securedata_cc);
					&action_history("suspicious:addopcard",('value_old'=>$securedata_cc{cc_fingerprint},'service_id'=>$securedata_cc{service_id}));
				}
				&multilevel_service_status_change_if_need($securedata_cc{service_id},"switch_on_enter_CC_active_in_another_service");
			}
		}
 		#
	   	#--------------------------
 		# add if ok
	   	#--------------------------
		if ( ($t{status_is_error} eq 0) && ($t{status_code} eq "") ) {
			%securedata_cc = &multilevel_securedata_cc_set(%securedata_cc);
			$debug .= "START multilevel_securedata_cc_set<br><pre>";
			$debug .= &log_debug_convert_hash_to_text(%securedata_cc);	
			$debug .= "</pre>STOP multilevel_securedata_cc_set<br>";
			if ($securedata_cc{status_ok} eq 1) {
				&action_history("cim:payment:set",('service_id'=>$app{service_id}));
				$t{status_code}			= 1;
				$t{status_is_ok}		= 1;
			
					
				# now let's send alert email
			 
				%email = ();
				$email{to}						= 'ccalert@zenofon.com';
				$email{from}                            = 'support@zenofon.com';
				$email{template}				= "creditprofile.add";
				$email{dic}{service_id}		=	$app{service_id}; 
				$email{dic}{first_name}              = $form{cc_first_name};
             		        $email{dic}{last_name}               = $form{cc_last_name};
               			$email{dic}{address}                 = $form{contact_address};
                       		$email{dic}{country}                 = $form{contact_country};
    		                $email{dic}{city}                    = $form{contact_city};
                	        $email{dic}{state}                   = $form{contact_state};
                       		$email{dic}{zip}                     = $form{contact_zip};
				$email{dic}{phone} =  $form{contact_number_fixed};
			 	$email{dic}{refer}                     = $referer_name.','.$referer_status; 

				$email{dic}{email}				= 'yang@zenonetwork.net';
				&multilevel_send_email(%email);		
			

		

			} else {
				$t{status_is_error}	= 1;
				if ($securedata_cc{status_code} eq 7) {
					$t{status_code}	= 201;
					&log_debug_add("type=securedata_cc_set,error=CIM_authorize_reject_card,service_id=$securedata_cc{service_id}",%securedata_cc);
					&action_history("cim:detail:201",				('service_id'=>$app{service_id},'value_old'=>$securedata_cc{status_message}));
				} else {
					$t{status_code}	= 200;
					&log_debug_add("type=securedata_cc_set,error=CIM_authorize_error,service_id=$securedata_cc{service_id}",%securedata_cc);
                                        &action_history("cim:detail:200",                               ('service_id'=>$app{service_id},'value_old'=>$securedata_cc{status_message}));

				}
					# now let's send alert email
			 
				%email = ();
				$email{to}						= 'ccalert@zenofon.com';
				 $email{from}                            = 'support@zenofon.com';
				$email{template}				= "creditprofile.addfail";
				$email{dic}{service_id}		=	$app{service_id}; 
				$email{dic}{first_name}              = $form{cc_first_name};
             			$email{dic}{last_name}               = $form{cc_last_name};
		               	$email{dic}{address}                 = $form{contact_address};
               			$email{dic}{country}                 = $form{contact_country};
		                $email{dic}{city}                    = $form{contact_city};
               			$email{dic}{state}                   = $form{contact_state};
 		                $email{dic}{zip}                     = $form{contact_zip};
				$email{dic}{phone} =  $form{contact_number_fixed};
			 	$email{dic}{refer}                     = $referer_name.','.$referer_status; 
				$email{dic}{email}				= 'yang@zenonetwork.net';
				&multilevel_send_email(%email);		
				
				
                       		%hash2 = database_select_as_hash("SELECT 1,1,name,email FROM service where id='$app{service_id}' ","flag,name,email");
			        if ($hash2{1}{flag} eq 1) {
   			             $service_name   = $hash2{1}{name};
			             $service_email  = $hash2{1}{email};
       				 }
			         $service_email = clean_str(substr($service_email ,0,100),"+.()-=[]?><#\@");
			         if ( ($service_email eq "") || (index($service_email,"\@") eq -1) || (index($service_email,"\@") ne rindex($service_email,"\@"))  || (index($service_email,".") eq -1) ){
		                        $service_email ="";
         			 }
			         if ($service_email ne "")  {
    			              $email{to}        = $service_email;
			              &multilevel_send_email(%email);

        			}




			}

			

	 	}

		

 	}
    #
   	#----------------------------------------------------- 
    # check check delete action
   	#----------------------------------------------------- 
 	if ( ($form{click_id} ne "") && ($t{user_action} eq "DEL") && ($t{status_code} eq "") ) {
		$tmp = "";
		$tmp = ( ($t{active_profile_with_cc_errors} ne 1) && ($t{active_profile_is_auto_recharge} eq 1) ) ? 22 : $tmp ;
		$tmp = ($t{active_profile_exists} 			ne 1) ? 99 : $tmp ;
		if ($tmp ne "") {
			$t{status_is_error}	= 1;
			$t{status_code}		= $tmp;
		}
		#
		# delete 
		if ( ($t{status_is_error} eq 0) && ($t{status_code} eq "") ) {
			if (&multilevel_securedata_cc_del($app{service_id}) eq 1) {
				&action_history("cim:payment:del",('service_id'=>$app{service_id}));
				$t{status_code}			= 1;
				$t{status_is_ok}		= 1;
			} else {
				$t{status_code}			= 21;
				$t{status_is_error}		= 1;
			}
		}
			
 	}
 	#
   	#----------------------------------------------------- 
 	# log fails 
   	#----------------------------------------------------- 
	if ($t{status_code} ne "") {
		# some status dont need log
		if ( index("|200|201|2001|2002|","|$t{status_code}|") eq -1 ) {
			&action_history("cim:detail:$t{status_code}",('service_id'=>$app{service_id}));
			
		}
	}
    #
   	#----------------------------------------------------- 
    # load values if its first time in page
   	#----------------------------------------------------- 
 	if ( ($form{click_id} eq "") && ($t{active_profile_exists} eq 1) && ($t{status_code} eq "") ) {
		$form{cc_number}		= $t{active_profile_cc_number};
		$form{cc_date}			= $t{active_profile_cc_date};
		$form{cc_date_1}		= $t{active_profile_cc_date_1};
		$form{cc_date_2}		= $t{active_profile_cc_date_2};
		$form{cc_code}			= $t{active_profile_cc_code};
		$form{cc_first_name}	= $t{active_profile_cc_first_name};
		$form{cc_last_name}		= $t{active_profile_cc_last_name};
		$form{contact_number}	= $t{active_profile_contact_number};
		$form{contact_address}	= $t{active_profile_address};
		$form{contact_country}	= $t{active_profile_country};
		$form{contact_city}		= $t{active_profile_city};
		$form{contact_state}	= $t{active_profile_state};
		$form{contact_zip}		= $t{active_profile_zip};
		$form{profile_type} 	= $t{active_profile_type}; 
 	}
    #
   	#----------------------------------------------------- 
    # warn if cc profile has error 
   	#----------------------------------------------------- 
#warning("(E)(O)(A)=($t{status_is_error})($t{status_is_ok})($t{status_is_alert})");
	if ( ($t{status_is_error} eq 0) && ($t{status_is_ok} eq 0) && ($t{status_is_alert} eq 0) ) {
#warning("(E)(O)(A)=HIT");
#warning("(PER)(PEX)=($t{active_profile_with_cc_errors})($t{active_profile_exists})");
		if ( ($t{active_profile_with_cc_errors} eq 1) && ($t{active_profile_exists} eq 1) ) {
#warning("(PER)(PEX)=HIT");
			$t{status_code}			= 500;
			$t{status_is_alert}		= 1;
		}
	}
    #
   	#----------------------------------------------------- 
    # fill always present data
   	#----------------------------------------------------- 
	foreach (qw(contact_zip contact_state contact_city contact_country contact_address contact_number profile_type cc_last_name cc_first_name cc_code cc_date_2 cc_date_1 cc_number)){ 
		$t{$_} = $form{$_}; 
	}
    $t{click_id}									= &multilevel_clickchain_set($t{click_id_prefix});
    $t{"profile_type_select_".$t{profile_type}} 	= "SELECTED";
    $t{"cc_date_1_select_".$t{cc_date_1}} 			= "SELECTED";
    $t{"cc_date_2_select_".$t{cc_date_2}} 			= "SELECTED";
    $t{"status_code_is_".$t{status_code}}			= 1;
	#
   	#----------------------------------------------------- 
    # print page
   	#----------------------------------------------------- 
    #foreach (sort keys %form) 	{$t{debug} .= "DUMP --> FORM --> $_=$form{$_}<br>"}
    #foreach (sort keys %t) 		{if($_ eq "debug"){next} $t{debug} .= "DUMP --> TEMPLATE --> $_=$t{$_}<br>"}
    #foreach (sort keys %ENV) 	{$t{debug} .= "DUMP --> ENV --> $_=$ENV{$_}<br>"}
    &template_print("template.myaccount.credits.profile.html",%t);	
}
sub do_credits() {
	#
	# start
    %t = %template_default;
	#
	# calcula paginas
    %hash = database_select_as_hash("select 1,1,count(*) from credit where service_id='$app{service_id}'","flag,value");
	$pg_itens_qtd	= ($hash{1}{flag} eq 1) ? $hash{1}{value} : 0;
	$pg_page_size	= 8;
	$pg_page_min	= 1;
	$pg_page_max	= int(($pg_itens_qtd-1)/$pg_page_size)+1;
	$pg_page_max	= ($pg_page_max<$pg_page_min) ? $pg_page_min : $pg_page_max;
	$pg_page_now 	= clean_int($form{page});
	$pg_page_now	= ($form{page_go_next} eq 1) ? $pg_page_now+1 : $pg_page_now;
	$pg_page_now	= ($form{page_go_revious} eq 1) ? $pg_page_now-1 : $pg_page_now;
	$pg_page_now	= ($pg_page_now<$pg_page_min) ? $pg_page_min : $pg_page_now;
	$pg_page_now	= ($pg_page_now>$pg_page_max) ? $pg_page_max : $pg_page_now;
	$pg_sql_limit_1	= ($pg_page_size*($pg_page_now-1));
	$pg_sql_limit_2	= $pg_page_size;
    $t{pg_now} 		= $pg_page_now;
    $t{pg_max} 		= $pg_page_max;
    $t{pg_min} 		= $pg_page_min;
    $t{pg_min} 		= $pg_page_min;
    $t{pg_previous}	= ($pg_page_now eq $pg_page_min) ? $pg_page_now : $pg_page_now-1;
    $t{pg_has_previous}= ($pg_page_now eq $pg_page_min) ? 0 : 1;
    $t{pg_next}		= ($pg_page_now eq $pg_page_max) ? $pg_page_now : $pg_page_now+1;
    $t{pg_has_next}	= ($pg_page_now eq $pg_page_max) ? 0 : 1;
    #
    # credits query
    $sql = "
        select id,unix_timestamp(credit.date),status,credit_type,credit,value,text 
        from credit where service_id='$app{service_id}'
        order by credit.date desc limit $pg_sql_limit_1,$pg_sql_limit_2
    ";
    %list = database_select_as_hash($sql,"date,status,credit_type,credit,value,text");
    $t{credit_list_is_empty} = 1;
    $index = 1;
    foreach $id (sort{$list{$b}{date} <=> $list{$a}{date}} keys %list) {
	    $t{credit_list_is_empty} = 0;
	    $t{credit_list}{$index}{id}		= $id;
        $tmp = "\U$list{$id}{credit_type}";
        $tmp = (index("|COMMISSION_CRED|AUTHORIZE_CC|AUTHORIZE_CIM|AUTHORIZE_ACIM|AUTHORIZE_PCIM|FREE|CASH|","|$tmp|") eq -1) ? "" : $tmp;
        $tmp = ($tmp eq "") ? "UNKNOWN" : $tmp;
	    $t{credit_list}{$index}{type} = $tmp;
	    $t{credit_list}{$index}{"type_".$tmp} = 1;
        $tmp = $list{$id}{credit};
        $tmp++;
        $tmp--;
        $tmp = format_number($tmp,2);
	    $t{credit_list}{$index}{credit} = $tmp;
		$tmp = "OK";
		$tmp = ($list{$id}{status} eq 0) ? "NOT_READY" : $tmp;
		$tmp = ($list{$id}{status} eq -1) ? "DELETED" : $tmp;
	    $t{credit_list}{$index}{status} = $tmp;
	    $t{credit_list}{$index}{"status_".$tmp} = 1;
	    $t{credit_list}{$index}{"date"} = &format_time_gap($list{$id}{date});
		$index++;
    }
	#
	# check CIM profile
	%tmp_hash = &multilevel_securedata_cc_get($app{service_id},"DO_NOT_CHECK_CC_ERROR");
	$t{profile_exists} 			= ($tmp_hash{status_ok} eq 1) ? 1 : 0;
	$t{profile_with_cc_errors}	= ($tmp_hash{cc_error} eq 1) ? 1 : 0;
	#
	# check auto_recharge data
	%hash = database_select_as_hash("SELECT 1,1,is_auto_recharge FROM service_profile_cc where service_id='$app{service_id}' and active=1","flag,value");
	$t{auto_recharge_enabled} = ( ($hash{1}{flag} eq 1) && ($hash{1}{value} eq 1) ) ? 1 : 0;
	#
	# get disable_recharge_over_phone
	$t{disable_recharge_over_phone}	= &data_get("service_data",$app{service_id},"disable_recharge_over_phone");
	$t{disable_recharge_over_phone}	= ($t{disable_recharge_over_phone} eq 1) ? 1 : 0;	
	#
	# pega dados do status
	$sql = "SELECT 1,1,service_status.can_add_credit FROM service,service_status where service.status=service_status.id and service.id='$app{service_id}'";
	%hash = database_select_as_hash($sql,"flag,can_add_credit");
	$t{can_add_credit}	= ( ($hash{1}{flag} eq 1) && ($hash{1}{can_add_credit} eq 1) ) ? 1 : 0;
    #
	# check phone_recharge data
	#
	$t{enable_recharge_over_phone}		= &data_get("service_data",$app{service_id},"enable_recharge_over_phone");
 	#
    # print page
    $t{my_url}					= $my_url;
	$t{service_id}				= $app{service_id};
	$t{service_alert}			= $app{service_alert};
	$t{service_name}			= $app{service_name};
	$t{service_email}			= $app{service_email};
	$t{service_credit}			= &format_number($app{service_credits},2);
	$t{service_credits_bar}	= $app{service_credits_bar};
    #foreach (sort keys %form) 	{$t{debug} .= "DUMP --> FORM --> $_=$form{$_}<br>"}
    #foreach (sort keys %t) 		{if($_ eq "debug"){next} $t{debug} .= "DUMP --> TEMPLATE --> $_=$t{$_}<br>"}
    #foreach (sort keys %ENV) 	{$t{debug} .= "DUMP --> ENV --> $_=$ENV{$_}<br>"}
    &template_print("template.myaccount.credits.html",%t);
}
sub do_calls(){
	#
	# pega DST names
	# TODO: change that to multiple products in future
	# its ok now, because we have just one product
    %number_to_names = ();
	#changed by Yassine to add 95 new DID 53->148
	
	$sql = "select name, value from service_data where target='$app{service_id}' and name like 'dst_%_name'";
	%dstName = database_select_as_hash($sql, "value");
	
	$sql = "select name, value from service_data where target='$app{service_id}' and name like 'dst_%_number'";
	%dstNumber = database_select_as_hash($sql, "value");
	
    foreach $index (1..148) {
		$name = $dstName{"dst_".$index."_name"}{value}; #&data_get("service_data",$app{service_id},"dst_".$index."_name");
		$number = $dstNumber{"dst_".$index."_number"}{value}; #&data_get("service_data",$app{service_id},"dst_".$index."_number");
		$number_to_names{$number} = $name;
    }
	#
	#===========================================================================
	# pega history
	#===========================================================================
	# prepara pega ids
	%data_history = ();
	%data_history_calls = ();
	%data_history_credits = ();
	$data_history_index=0;
	$data_history_overflow_flag=0;
	$html_history = "";
	$html_history_select_pages = "";
	$html_history_empty = "<tr><td colspan=10><center>No calls...</center></td></tr>";
	# pega ids calls
	if ($form{hide_calls} ne 1){
		%hash = database_select_as_hash("SELECT id,unix_timestamp(date) FROM calls where service_id='$app{service_id}' order by id desc limit 0,2003");
		$c++;
		foreach(keys %hash){
			$data_history{$data_history_index}{i}=$_;
			$data_history{$data_history_index}{t}=$hash{$_};
			$data_history{$data_history_index}{m}="A";
			$data_history_index++;$c++;
		}
		$data_history_overflow_flag = ($c>2000) ? 1 : $data_history_overflow_flag;
	}
	# pega ids de creditos
	if ($form{hide_credits} ne 1){
		%hash = database_select_as_hash("SELECT id,unix_timestamp(date) FROM credit where service_id='$app{service_id}' order by id desc limit 0,503");
		$c++;
		foreach(keys %hash){
			$data_history{$data_history_index}{i}=$_;
			$data_history{$data_history_index}{t}=$hash{$_};
			$data_history{$data_history_index}{m}="R";
			$data_history_index++;$c++;
		}
		$data_history_overflow_flag = ($c>500) ? 1 : $data_history_overflow_flag;
	}
	# calcula paginas
	$page_size	= 20;
	$quantity 	= keys %data_history;
	$page_min	= 1;
	$page_max	= int(($quantity-1)/$page_size)+1;
	$page_max	= ($page_max<$page_min) ? $page_min : $page_max;
	$page 		= clean_int($form{history_page});
	$page 		= ($form{next} eq 1) ? $page+1 : $page;
	$page 		= ($form{previous} eq 1) ? $page-1 : $page;
	$page 		= ($page<$page_min) ? $page_min : $page;
	$page 		= ($page>$page_max) ? $page_max : $page;
	$selected_start	= ($page-1)*$page_size;
	$selected_stop	= $selected_start+($page_size-1);
	@selected_ids	= (sort{$data_history{$b}{t} <=> $data_history{$a}{t}} keys %data_history)[$selected_start..$selected_stop];
	$selected_ids_raw	= join(",",@selected_ids);
	$selected_ids_raw_a = "";
	$selected_ids_raw_r = "";
	@selected_ids 		= ();
	foreach (split(/\,/,$selected_ids_raw)) {
		if($_ eq "") {next}
		@selected_ids = (@selected_ids,$_);
		if ($data_history{$_}{m} eq "A") {$selected_ids_raw_a .= "$data_history{$_}{i},";}
		if ($data_history{$_}{m} eq "R") {$selected_ids_raw_r .= "$data_history{$_}{i},";}
	}
	# pega dados de calls
	$ids_raw = $selected_ids_raw_a;
	if ($ids_raw ne "") {
		$ids_raw = substr($ids_raw,0,-1);
		$sql = "
		SELECT c.id,c.ani,c.did,c.dst,c.extra,c.seconds,c.value,c.balance_before,cr.status,cr.amount
		FROM calls c left join call_refund cr
		on c.id=cr.call_id
		where c.id in ($ids_raw) 
		limit 0,100
		";
		%data_history_calls = database_select_as_hash($sql, "ani,did,dst,extra,seconds,value,balance_before,refundstatus,refundamount");
	}
	# pega dados de creditos
	$ids_raw = $selected_ids_raw_r;
	if ($ids_raw ne "") {
		$ids_raw = substr($ids_raw,0,-1);
		$sql = "
		SELECT id,unix_timestamp(date),status,credit_type,source_type,credit,value,text 
		FROM credit where id in ($ids_raw) 
		limit 0,100
		";
		%data_history_credits = database_select_as_hash($sql, "date,status,credit_type,source_type,credit,value,text");
	}
	# monta o html
	foreach $list_id (@selected_ids) {
		$col_tr_style = "";
		$col_icon = "";
		$col_title = "";
		$col_text = "";
		$col_1 = "";
		$col_2 = "";
		$col_3 = "";
		$col_4 = "";
		if ($data_history{$list_id}{m} eq "A") {
			$id = $data_history{$list_id}{i};
			$destination = &format_E164_number($data_history_calls{$id}{dst},"USA");
			$destination = ($number_to_names{$data_history_calls{$id}{dst}} ne "") ? $number_to_names{$data_history_calls{$id}{dst}}: $destination;
			$col_icon  = "<img src=/design/icons/phone_sound.png hspace=0 vspace=0 border=0 width=16 height=16 align=left style=margin-right:3px;>";
			$col_title = "Call connected to $destination";
			$col_text .= "Dial from: ". 		&format_E164_number($data_history_calls{$id}{ani},"USA") ."<br>";
			$col_text .= "Dial to: ". 	&format_E164_number($data_history_calls{$id}{did},"USA") ."<br>";
			if ($list{$id}{extra} ne "") {$col_text .= "Contact index number: $list{$id}{extra}<br>";}
			$col_text .= "Connect to: ".&multiformat_phone_number_format_for_user($data_history_calls{$id}{dst},"USA")."<br>";
			if ($data_history_calls{$id}{refundstatus} ne ""){
				$refundText = "";
				if($data_history_calls{$id}{refundstatus} eq "pending"){
					$refundText = "<button disabled=disabled>Refund Request Pending</button>";
				}elsif($data_history_calls{$id}{refundstatus} eq "full"){
					$refundText = "<button disabled=disabled>Refunded Full amount</button>";
				}elsif($data_history_calls{$id}{refundstatus} eq "decline"){
					$refundText = "<button disabled=disabled>Refund Declined</button>";
				}elsif($data_history_calls{$id}{refundstatus} eq "partial"){
					$refundText = "<button disabled=disabled>Refunded \$$data_history_calls{$id}{refundamount}</button>";
				}
				$col_text .= "$refundText <br>";
			}else{
				$col_text .= "<button onclick='requestRefund($id, this)' name=requestRefund id='call_$id'>Request Refund</button><br>";
			}
			$col_1 = $data_history_calls{$id}{balance_before};
			$col_2 = $data_history_calls{$id}{value};
			$col_3 = ($data_history_calls{$id}{balance_before} eq "") ? "" : $data_history_calls{$id}{balance_before}-$data_history_calls{$id}{value};
			$col_4 = &format_time($data_history_calls{$id}{seconds});
		} elsif ($data_history{$list_id}{m} eq "R") {
			$id = $data_history{$list_id}{i};
			$col_icon  = "<img src=/design/icons/money.png hspace=0 vspace=0 border=0 width=16 height=16 align=left style=margin-right:3px;>";
			$type = $data_history_credits{$id}{credit_type};
			$type = ($type eq "FREE") ? "Free" : $type;
			$type = ($type eq "COMMISSION_CRED") ? "Commission" : $type;
			$type = ($type eq "AUTHORIZE_CC") ? "Credit card" : $type;
			$type = ($type eq "AUTHORIZE_CIM") ? "Credit card" : $type;
			$type = ($type eq "AUTHORIZE_ACIM") ? "Auto" : $type;
			$type = ($type eq "AUTHORIZE_PCIM") ? "By Phone " : $type;
			$type = ($type eq "CASH") ? "Cash" : $type;
			$col_title = ($data_history_credits{$id}{status} eq 1) ? "$type recharge" : "Recharge";
			$col_title = ($data_history_credits{$id}{text} ne "") ? $data_history_credits{$id}{text} : $col_title;
			$col_tr_style = ($data_history_credits{$id}{status} eq 1) ? "background-color:f4f4f4;" : "background-color:red;color:#ffffff;";
			$col_text .= "Recharge type: $type<br>";
			$col_text .= "Value: \$".&format_number($data_history_credits{$id}{value},2)."<br>";
			$col_2 = $data_history_credits{$id}{credit};
		} else {
			$col_title = "UNKNOWN $data_history{$list_id}{m}-$list_id ($data_history{$list_id}{i})";
		}
		$html_history .= "<tr style='$col_tr_style' >";
		$html_history .= "<td valign=top>".&format_time_gap($data_history{$list_id}{t})."</td>";
		$html_history .= "<td valign=top>";
		$html_history .= "<a href=\"javascript:MyDisplay('item$list_id')\">$col_icon$col_title</a>";
		$html_history .= "<div id=item$list_id class=clear style=display:none;padding-left:19px;padding-bottom:10px;>$col_text</div>";
		$html_history .= "</td>";
		$tmp = ($col_1 < 0) ? "style='background-color:red; color=#ffffff;'" : ""; $html_history .= ($col_1 eq "") ? "<td $tmp class=ar valign=top>&nbsp;</td>" : "<td $tmp class=ar valign=top>\$".&format_number($col_1,2)."</td>";
		$html_history .= ($col_4 eq "") ? "<td $tmp class=ar valign=top>&nbsp;</td>" : "<td $tmp class=ar valign=top>$col_4</td>";
		$tmp = ($col_2 < 0) ? "style='background-color:red; color=#ffffff;'" : ""; $html_history .= ($col_2 eq "") ? "<td $tmp class=ar valign=top>&nbsp;</td>" : "<td $tmp class=ar valign=top>\$".&format_number($col_2,2)."</td>";
		$tmp = ($col_3 < 0) ? "style='background-color:red; color=#ffffff;'" : ""; $html_history .= ($col_3 eq "") ? "<td $tmp class=ar valign=top>&nbsp;</td>" : "<td $tmp class=ar valign=top>\$".&format_number($col_3,2)."</td>";
		$html_history .= "</tr>";
		$html_history_empty = "";
	}
    #
    # select de paginas
	$html_history_select_pages = "";
	$tmp1 = &format_number($page_max,0);
	foreach($page_min..$page_max) {
		$tmp = ($_ eq $page) ? "selected" : ""; 
		$html_history_select_pages .= "<option $tmp value=$_>Page: ". &format_number($_,0). " of $tmp1</option>";
	}
    #
    # imprime a pagina
    %t = %template_default;
    $t{dic}{calls_table}			= "$html_history $html_history_empty";
    $t{dic}{select_page}			= "$html_history_select_pages";
    $t{dic}{my_url}					= $my_url;
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
	
 
    &template_print("template.myaccount.calls.html",%t);
}
sub do_alerts() {
    # start 
    %t = %template_default;
    #
    # save data
    if ($form{save} eq 1) {
		$tmp = ($form{email_alert_new_friends} eq 1)?1:0; 				&data_set("service_data",$app{service_id},"trigger_nf",$tmp);
		$tmp = ($form{email_alert_new_friends_of_friends} eq 1)?1:0; 	&data_set("service_data",$app{service_id},"trigger_nfof",$tmp);
		$tmp = ($form{email_alert_new_commission} eq 1)?1:0; 			&data_set("service_data",$app{service_id},"trigger_nc",$tmp);
		$tmp = ($form{email_alert_each_call} eq 1)?1:0; 				&data_set("service_data",$app{service_id},"trigger_ec",$tmp);
		$tmp = ($form{email_alert_low_balance} eq 1)?1:0; 				&data_set("service_data",$app{service_id},"trigger_lb",$tmp);
		$tmp = ($form{email_news} eq 1)?1:0; 							&data_set("service_data",$app{service_id},"email_news",$tmp);
		&cgi_redirect("$my_url?action=profile&alert_ui_saved_ok=1");
		exit;
    }
	#
	# redirect to profile
	&cgi_redirect("$my_url?action=profile");
	exit;
    #
    # load data
    $t{dic}{email_alert_new_friends}			= (&data_get("service_data",$app{service_id},"trigger_nf") eq 1) ? 1 : 0;
    $t{dic}{email_alert_new_friends_of_friends}	= (&data_get("service_data",$app{service_id},"trigger_nfof") eq 1) ? 1 : 0;
    $t{dic}{email_alert_new_commission}			= (&data_get("service_data",$app{service_id},"trigger_nc") eq 1) ? 1 : 0;
    $t{dic}{email_alert_each_call}				= (&data_get("service_data",$app{service_id},"trigger_ec") eq 1) ? 1 : 0;
    $t{dic}{email_alert_low_balance}			= (&data_get("service_data",$app{service_id},"trigger_lb") eq 1) ? 1 : 0;
    $t{dic}{email_news}							= (&data_get("service_data",$app{service_id},"email_news") eq 1) ? 1 : 0;
    #
    # print page
    $t{dic}{my_url}				= $my_url;
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
    &template_print("template.myaccount.alerts.html",%t);
}
sub do_commissions_request_check(){
    #
    # start
    %t = %template_default;
	$answer_ok = 0;
	$answer_message = "";
	#
	#---------------------------------
	# get all commissions
	#---------------------------------
    %list = database_select_as_hash("SELECT 1,1,count(*),sum(value) FROM service_commission WHERE status=1 and service_id = '$app{service_id}' and invoice_id is null","flag,qtd,value");
	$qtd = ($list{1}{flag} eq 1) ? $list{1}{qtd} : 0;
	$val = ($list{1}{flag} eq 1) ? $list{1}{value} : 0;
	$t{dic}{commissions_all_qtd} 	= &format_number($qtd,0);
	$t{dic}{commissions_all_value} 	= &format_number($val,2);
	#
	#---------------------------------
	# get ok commissions
	#---------------------------------
    %list = database_select_as_hash("SELECT 1,1,count(*),sum(value) FROM service_commission WHERE status=1 and service_id = '$app{service_id}' and invoice_id is null and now()>=activation_date_2 ","flag,qtd,value");
	$qtd = ($list{1}{flag} eq 1) ? $list{1}{qtd} : 0;
	$val = ($list{1}{flag} eq 1) ? $list{1}{value} : 0;
	$t{dic}{commissions_ok_qtd} 	= &format_number($qtd,0);
	$t{dic}{commissions_ok_value} 	= &format_number($val,2);
	$t{dic}{has_minimum_value_commissions} 	= ($val >= 75) ? 1 : 0;
	$t{dic}{has_commissions} 				= ($val > 0) ? 1 : 0;
	#
	#---------------------------------
	# get affiliate profile
	#---------------------------------
	$t{dic}{affiliate_flags} 	= &data_get("service_data",$app{service_id},"ss_flags");
	$t{dic}{affiliate_empty}	= ($t{dic}{affiliate_flags} eq "") ? 1 : 0;
	$t{dic}{affiliate_unlocked}	= (index($t{dic}{affiliate_flags},",DEL,") ne -1) ? 1 : 0;
	$t{dic}{affiliate_name}		= &data_get("service_data",$app{service_id},"ss_name");
	$t{dic}{affiliate_ss}		= &data_get("service_data",$app{service_id},"ss_ss");
	$t{dic}{affiliate_addr1}	= &data_get("service_data",$app{service_id},"ss_addr1");
	$t{dic}{affiliate_addr2}	= &data_get("service_data",$app{service_id},"ss_addr2");
	$t{dic}{affiliate_city}		= &data_get("service_data",$app{service_id},"ss_city");
	$t{dic}{affiliate_state}	= &data_get("service_data",$app{service_id},"ss_state");
	$t{dic}{affiliate_zip}		= &data_get("service_data",$app{service_id},"ss_zip");
	%hash = database_select_as_hash("SELECT 1,1,service_status.can_request_commission_check FROM service,service_status where service.status=service_status.id and service.id='$app{service_id}' ","flag,can_request_commission_check");
	$t{dic}{can_request_check}	= ( ($hash{1}{flag} eq 1) && ($hash{1}{can_request_commission_check} eq 1) ) ? 1 : 0;
	#
	#---------------------------------
	# split in slices (5,10,20,50,all)
	#---------------------------------
    $sql = "
		SELECT id,value 
		FROM service_commission 
		WHERE status=1 and service_id = '$app{service_id}' and invoice_id is null and now()>activation_date_2 
		ORDER BY id
	    ";
    %list = database_select_as_hash($sql);
	$value = 0;
	$qtd = 0;
	$t{dic}{no_slice} = 0;
    foreach $id (keys %list) {
		$value += $list{$id};
		$qtd++;
		$t{dic}{slice_all_flag} = 1;
		$t{dic}{slice_all_id} .= "$id,";
		$t{dic}{slice_all_qtd}++;
		$t{dic}{slice_all_real} += $list{$id};
		if ( ($value > 75) && ($t{dic}{slice_1_flag} eq "")) {
			$t{dic}{slice_1_flag}	= 1;
			$t{dic}{slice_1_id}		= $t{dic}{slice_all_id};
			$t{dic}{slice_1_qtd}	= &format_number($qtd,0);
			$t{dic}{slice_1_value}	= &format_number($value,2);
			$t{dic}{slice_1_real}	= $value;
		} elsif ( ($value > 100) && ($t{dic}{slice_2_flag} eq "")) {
			$t{dic}{slice_2_flag}	= 1;
			$t{dic}{slice_2_id}		= $t{dic}{slice_all_id};
			$t{dic}{slice_2_qtd}	= &format_number($qtd,0);
			$t{dic}{slice_2_value}	= &format_number($value,2);
			$t{dic}{slice_2_real}	= $value;
		} elsif ( ($value > 150) && ($t{dic}{slice_3_flag} eq "")) {
			$t{dic}{slice_3_flag}	= 1;
			$t{dic}{slice_3_id}		= $t{dic}{slice_all_id};
			$t{dic}{slice_3_qtd}	= &format_number($qtd,0);
			$t{dic}{slice_3_value}	= &format_number($value,2);
			$t{dic}{slice_3_real}	= $value;
		}
    }
	if ($qtd > 0) {
		$t{dic}{slice_all_qtd}	= &format_number($t{dic}{slice_all_qtd},0);
		$t{dic}{slice_all_value}= &format_number($t{dic}{slice_all_real},2);
		$t{dic}{slice_1_id}		= substr($t{dic}{slice_1_id},0,-1);
		$t{dic}{slice_2_id}		= substr($t{dic}{slice_2_id},0,-1);
		$t{dic}{slice_3_id}		= substr($t{dic}{slice_3_id},0,-1);
		$t{dic}{slice_all_id}	= substr($t{dic}{slice_all_id},0,-1);
		$t{dic}{slice_1_flag}	= ($t{dic}{slice_1_real} eq $t{dic}{slice_all_real} ) ? 0 : $t{dic}{slice_1_flag};
		$t{dic}{slice_2_flag}	= ($t{dic}{slice_2_real} eq $t{dic}{slice_all_real} ) ? 0 : $t{dic}{slice_2_flag};
		$t{dic}{slice_3_flag}	= ($t{dic}{slice_3_real} eq $t{dic}{slice_all_real} ) ? 0 : $t{dic}{slice_3_flag};
	} else {
		$t{dic}{no_slice} 		= 1;
		$t{dic}{slice_1_flag}	= 0;
		$t{dic}{slice_2_flag}	= 0;
		$t{dic}{slice_3_flag}	= 0;
		$t{dic}{slice_all_flag}	= 0;
	}
	if ($t{dic}{slice_all_real} < 75){
		$t{dic}{no_slice} 		= 1;
		$t{dic}{slice_1_flag}	= 0;
		$t{dic}{slice_2_flag}	= 0;
		$t{dic}{slice_3_flag}	= 0;
		$t{dic}{slice_all_flag}	= 0;
	}
	$t{dic}{is_ok_to_request} = 1;
	$t{dic}{is_ok_to_request} = ($t{dic}{has_minimum_value_commissions} ne 1) ? 0 : $t{dic}{is_ok_to_request};
	$t{dic}{is_ok_to_request} = ($t{dic}{no_slice} eq 1) ? 0 : $t{dic}{is_ok_to_request};
	$t{dic}{is_ok_to_request} = ($t{dic}{affiliate_empty} eq 1) ? 0 : $t{dic}{is_ok_to_request};
	#
	#---------------------------------
	# try to add
	#---------------------------------
    $t{dic}{error}					= 0;
    $t{dic}{error_bad_slice}		= 0;
    $t{dic}{error_no_accept_data}	= 0;
    $t{dic}{error_no_accept_head}	= 0;
    $t{dic}{error_system}			= 0;
    $t{dic}{ok}						= 0;
    $t{dic}{ok_accepted}			= 0;
	if ( ($t{dic}{is_ok_to_request} eq 1) && ($form{save} eq 1) ) {
		#
		# check sclice selection
		if (index("|1|2|3|4|all|","|$form{slice}|") eq -1) {
			$t{dic}{error}			= 1;
			$t{dic}{error_bad_slice}= 1;
		} else {
			# check sclice value
			if ($t{dic}{"slice_".$form{slice}."_flag"} ne 1) {
				$t{dic}{error}			= 1;
				$t{dic}{error_bad_slice}= 1;
			}
		}
		#
		# check i agree head
		if ($t{dic}{affiliate_unlocked} eq 1) {
			if ($form{i_agree_head} ne 1) {
				$t{dic}{error}					= 1;
				$t{dic}{error_no_accept_head}	= 1;
			}
		}
		#
		# check i agree data
		if ($form{i_agree_data} ne 1) {
			$t{dic}{error}					= 1;
			$t{dic}{error_no_accept_data}	= 1;
		}
		#
		# try to save
		if ($t{dic}{error} eq 0) {
			#
			# cria invoice com status=0 e pega id da invoice
			$value = $t{dic}{"slice_".$form{slice}."_real"};
			$sql = "
				insert into service_commission_invoice 
				(  creation_date,  send_to,   status,  value,     service_id          ) values 
				(  now(),          'CHECK',   '0',     '$value',  '$app{service_id}'  )
			"; 
			database_do($sql);
			%hash = database_select_as_hash("SELECT 1,LAST_INSERT_ID();");
			$commission_invoice_id = $hash{1};
			#
			# verifica se invoice foi criada
			if ($commission_invoice_id ne "") {
				#
				# add as comissoes na invoice
				$ids = $t{dic}{"slice_".$form{slice}."_id"};
				$sql = "
					UPDATE service_commission 
					SET invoice_id='$commission_invoice_id' 
					WHERE service_id='$app{service_id}' and invoice_id is null and id in ($ids)
					";
				database_do($sql);
				#
				# trava affiliate profile 
				&data_set("service_data",$app{service_id},"ss_flags",",");
				#
				# log
				&action_history("com:chk:request",('service_id'=>$app{service_id},'commission_invoice_id'=>$commission_invoice_id));
				#
				# flag ok
			    $t{dic}{ok}			= 1;
			    $t{dic}{ok_accepted}= 1;
			} else {
				#
				# deu erro
			    $t{dic}{error}			= 0;
			    $t{dic}{error_system}	= 0;
			}
		}
	}
	#
	#---------------------------------
	# load form 
	#---------------------------------
    #
	#---------------------------------
    # print page
	#---------------------------------
    $t{dic}{my_url}					= $my_url;
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
    &template_print("template.myaccount.commission.request.check.html",%t);
}
sub do_friends() {
	#
	#=====================================================
    # start 
	#=====================================================
	&active_session_set("sm_touch",0);
	&active_session_set("sm_last","");
    %t = %template_default;
	$html = "";
    #
    # get invite code for active service
    %invite_list= database_select_as_hash("select 1,id from service_invite where free=0 and service_id='$app{service_id}' ");
    $t{invite_code} = $invite_list{1};
    $t{invite_link}= 'http://www.zenofon.com/'.$invite_list{1};
	#
	#=====================================================
	# commissions by engine
	#=====================================================
	%hash = &database_select_as_hash("SELECT ID,1 FROM service_commission_type_engine");
    $sql = "SELECT engine,count(*),sum(value) FROM service_commission where service_id='$app{service_id}' and invoice_id is null and status=1 group by engine ";
	%hash = &database_select_as_hash($sql,"qtd,value");
	foreach $engine (keys %hash) {
		$target_engine = "";
		$target_engine = ($engine eq "REFERRAL_SIGNIN") 		? "REFERRAL_SIGNIN" : $target_engine;
		$target_engine = ($engine eq "REFERRAL_FIRST_CALL")		? "REFERRAL_FIRST_CALL" : $target_engine;
		$target_engine = ($engine eq "REFERRAL_RECHARGE")		? "REFERRAL_RECHARGE" : $target_engine;
		$target_engine = ($engine eq "RADIO_LISTEN")			? "RADIO" : $target_engine;
		$target_engine = ($engine eq "RADIO_OWNER")				? "RADIO" : $target_engine;
		$target_engine = ($engine eq "SERVICE_DIALOUT_DID")		? "SERVICE_DIALOUT" : $target_engine;
		$target_engine = ($engine eq "SERVICE_DIALOUT_DST")		? "SERVICE_DIALOUT" : $target_engine;
		$target_engine = ($engine eq "REFERRAL_DIALOUT_DID")	? "REFERRAL_DIALOUT" : $target_engine;
		$target_engine = ($engine eq "REFERRAL_DIALOUT_DST")	? "REFERRAL_DIALOUT" : $target_engine;
		$target_engine = ($target_engine eq "") ? "MANUAL" : $target_engine;
		$t{"commissions_by_engine_".$target_engine."_found"} 		= 1;
		$t{"commissions_by_engine_".$target_engine."_quantity"}	+= $hash{$engine}{qtd};
		$t{"commissions_by_engine_".$target_engine."_value"} 	+= $hash{$engine}{value};
	}
	foreach (split(/\|/,"MANUAL|REFERRAL_SIGNIN|REFERRAL_FIRST_CALL|REFERRAL_RECHARGE|SERVICE_DIALOUT|REFERRAL_DIALOUT|RADIO")){
		$t{"commissions_by_engine_".$_."_quantity"}	= &format_number($t{"commissions_by_engine_".$_."_quantity"},0);
		$t{"commissions_by_engine_".$_."_value"} 	= &format_number($t{"commissions_by_engine_".$_."_value"},2);
	}
	#
	#=====================================================
	# commissions available and slice
	#=====================================================
	$sql = "select 1,1,count(*),sum(value) from service_commission where status=1 and invoice_id is null and service_id=$app{service_id} and now()<activation_date_1 and now()<activation_date_2 ";
	%hash = &database_select_as_hash($sql,"flag,qtd,value");
	$t{"commissions_available_slice_0_value"} 		= ($hash{1}{flag} ne 1) ? 0 : &format_number($hash{1}{value},2);
	$t{"commissions_available_slice_0_quantity"} 	= ($hash{1}{flag} ne 1) ? 0 : &format_number($hash{1}{qtd},0);
	$sql = "select 1,1,count(*),sum(value) from service_commission where status=1 and invoice_id is null and service_id=$app{service_id} and now()>=activation_date_1 ";
	%hash = &database_select_as_hash($sql,"flag,qtd,value");
	$t{"commissions_available_slice_1_value"} 		= ($hash{1}{flag} ne 1) ? 0 : &format_number($hash{1}{value},2);
	$t{"commissions_available_slice_1_quantity"} 	= ($hash{1}{flag} ne 1) ? 0 : &format_number($hash{1}{qtd},0);
	$sql = "select 1,1,count(*),sum(value) from service_commission where status=1 and invoice_id is null and service_id=$app{service_id} and now()>=activation_date_2 ";
	%hash = &database_select_as_hash($sql,"flag,qtd,value");
$t{debug} .= "SQL=$sql<br>";
$t{debug} .= "FLAG=$hash{1}{flag}<br>";
$t{debug} .= "VALUE=$hash{1}{value}<br>";
	$t{"commissions_available_slice_2_value"} 		= ($hash{1}{flag} ne 1) ? 0 : &format_number($hash{1}{value},2);
	$t{"commissions_available_slice_2_quantity"} 	= ($hash{1}{flag} ne 1) ? 0 : &format_number($hash{1}{qtd},0);
	$sql = "select 1,1,count(*),sum(value) from service_commission where status=1 and invoice_id is null and service_id=$app{service_id} ";
	%hash = &database_select_as_hash($sql,"flag,qtd,value");
	$t{"commissions_available_value"} 				= ($hash{1}{flag} ne 1) ? 0 : &format_number($hash{1}{value},2);
	$t{"commissions_available_quantity"} 			= ($hash{1}{flag} ne 1) ? 0 : &format_number($hash{1}{qtd},0);
	#
	#=====================================================
	# referral total
	#=====================================================
    %data = ();
    $loop_ids = "$app{service_id}";
	foreach $loop_deep (1..51) {
		$sql = "SELECT service_id,1 FROM service_tree where parent_service_id in ($loop_ids) ";
		%tmp_hash = &database_select_as_hash($sql);
		$loop_next_ids = "";
		foreach $loop_child_id (keys %tmp_hash){
			$loop_next_ids .= "$loop_child_id,";
			$data{$loop_deep}++;
		}
		if ($loop_next_ids eq "") {
			last;
		} else {
			$loop_ids = substr($loop_next_ids,0,-1);
		}
	}
	$t{"referral_quantity"}			= 0;
	$t{"referral_found"}			= 0;
	$tmp = 1;
	foreach (sort{$a <=> $b} keys %data) {
		$t{"referral_found"} 					= 1;
		$t{"referral_quantity"}					+= $data{$_};
		$t{"referral_summary"}{$tmp}{"deep"} 	= $_;
		$t{"referral_summary"}{$tmp}{"deep_".$_}= 1;
		$t{"referral_summary"}{$tmp}{quantity}	= $data{$_};
		$tmp++;
	}
	#
	#=====================================================
	# commissions invoices
	#=====================================================
	$sql = "
	SELECT id,unix_timestamp(creation_date),send_to,status,value 
	FROM service_commission_invoice 
	where service_id='$app{service_id}' 
	order by creation_date desc
	LIMIT 0,10 
	";
	%hash = &database_select_as_hash($sql,"date,send_to,status,value");
	$tmp = 1;
	$t{"invoices_found"} = 0;
	foreach $id (keys %hash) {
	    $t{credit_list_is_empty} = 0;
	    $t{invoices}{$tmp}{id}		= $id;
        $tmp = "\U$hash{$id}{send_to}";
        $tmp = (index("|CHECK|CREDIT|","|$tmp|") eq -1) ? "CREDIT" : $tmp;
        $t{invoice}{$tmp}{type} = $tmp;
	    $t{invoice}{$tmp}{"type_".$tmp} = 1;
        $tmp = $hash{$id}{value};
        $tmp++;
        $tmp--;
        $tmp = format_number($tmp,2);
	    $t{invoice}{$tmp}{value} = $tmp;
		$tmp = "OK";
		$tmp = ($list{$id}{status} eq 0) ? "NOT_READY" : $tmp;
		$tmp = ($list{$id}{status} eq -1) ? "DELETED" : $tmp;
	    $t{invoice}{$tmp}{status} = $tmp;
	    $t{invoice}{$tmp}{"status_".$tmp} = 1;
	    $t{invoice}{$tmp}{"date"} = &format_time_gap($hash{$id}{date});
		$tmp++;
	}
	#
	#
	#=====================================================
    # print page
	#=====================================================
	foreach(sort keys %t) {
	if ($_ eq "debug") {next}
	$t{debug} .= "TEMPLATE DUMP $_ = $t{$_}<br>";
	}
    &template_print("template.myaccount.friends.html",%t);
}
sub do_friends_OLD() {
	#
	#=====================================================
    # start 
	#=====================================================
	&active_session_set("sm_touch",0);
	&active_session_set("sm_last","");
    %t = %template_default;
	$html = "";
    #
    # get invite code for active service
    %invite_list= database_select_as_hash("select 1,id from service_invite where free=0 and service_id='$app{service_id}' ");
    $t{dic}{invite_code} = $invite_list{1};
	#
	#=====================================================
	# get friends summary 
	#=====================================================
    %data = ();
    $loop_ids = "$app{service_id}";
	foreach $loop_deep (0..50) {
		$sql = "SELECT service_id,1 FROM service_tree where parent_service_id in ($loop_ids) ";
		%tmp_hash = &database_select_as_hash($sql);
		$loop_next_ids = "";
		foreach $loop_child_id (keys %tmp_hash){
			$loop_next_ids .= "$loop_child_id,";
			$data{$loop_deep}++;
		}
		if ($loop_next_ids eq "") {
			last;
		} else {
			$loop_ids = substr($loop_next_ids,0,-1);
		}
	}
	$t{dic}{friends_summary} = "";
	$t{dic}{friends_total} = 0;
	foreach (sort{$a <=> $b} keys %data) {
		$tmp = "referral from $_ people away";
		$tmp = ($_ eq 0) ? "friends invited by you" : $tmp;
		$tmp = ($_ eq 1) ? "referral invited by your friends" : $tmp;
	    $t{dic}{friends_summary} .= "$data{$_} $tmp<br>";
		$t{dic}{friends_total} += $data{$_};
	}
	#
	#=====================================================
	# get commission summary
	#=====================================================
    %data = ();
	$t{dic}{commission_summary} = "";
	#--- pega total
	$sql = "select engine,count(*),sum(value) from service_commission where status=1 and invoice_id is null and service_id=$app{service_id} group by engine";
	%tmp_hash = &database_select_as_hash($sql,"qtd,value");
	foreach (keys %tmp_hash) {
		$data{type}{$_}{all}{qtd} += $tmp_hash{$_}{qtd};
		$data{order}{$_} = 99;
	}
	#--- pega slice 0
	$sql = "select engine,count(*),sum(value) from service_commission where status=1 and invoice_id is null and service_id=$app{service_id} and now()<activation_date_1 and now()<activation_date_2 group by engine";
	%tmp_hash = &database_select_as_hash($sql,"qtd,value");
	foreach (keys %tmp_hash) {$data{type}{$_}{slice_0}{value} += $tmp_hash{$_}{value};}
	#--- pega slice 1
	$sql = "select engine,count(*),sum(value) from service_commission where status=1 and invoice_id is null and service_id=$app{service_id} and now()>=activation_date_1 group by engine";
	%tmp_hash = &database_select_as_hash($sql,"qtd,value");
	foreach (keys %tmp_hash) {$data{type}{$_}{slice_1}{value} += $tmp_hash{$_}{value};}
	#--- pega slice 2
	$sql = "select engine,count(*),sum(value) from service_commission where status=1 and invoice_id is null and service_id=$app{service_id} and now()>=activation_date_2 group by engine";
	%tmp_hash = &database_select_as_hash($sql,"qtd,value");
	foreach (keys %tmp_hash) {$data{type}{$_}{slice_2}{value} += $tmp_hash{$_}{value};}
	#
	# SERVICE_DIALOUT = SERVICE_DIALOUT_DID + SERVICE_DIALOUT_DST;
	foreach $type (keys %{$data{type}}) {
		$data{type}{SERVICE_DIALOUT}{slice_0}{value} = $data{type}{SERVICE_DIALOUT_DST}{slice_0}{value} + $data{type}{SERVICE_DIALOUT_DID}{slice_0}{value};
		$data{type}{SERVICE_DIALOUT}{slice_1}{value} = $data{type}{SERVICE_DIALOUT_DST}{slice_1}{value} + $data{type}{SERVICE_DIALOUT_DID}{slice_1}{value};
		$data{type}{SERVICE_DIALOUT}{slice_2}{value} = $data{type}{SERVICE_DIALOUT_DST}{slice_2}{value} + $data{type}{SERVICE_DIALOUT_DID}{slice_2}{value};
	}
	delete($data{type}{SERVICE_DIALOUT_DST});
	delete($data{type}{SERVICE_DIALOUT_DID});
	# 
	$data{order}{REFERRAL_SIGNIN} 		= 1;
	$data{order}{REFERRAL_FIRST_CALL} 	= 2;
	$data{order}{REFERRAL_RECHARGE} 	= 3;
	$data{order}{SERVICE_DIALOUT_DST} 	= 4;
	$data{order}{SERVICE_DIALOUT_DID} 	= 5;
	$data{order}{SERVICE_DIALOUT} 		= 6;
	$data{order}{MANUAL} 				= 7;
	foreach $type (sort{$data{order}{$a} <=> $data{order}{$b}} keys %{$data{type}}) {
		$title = "type: $type";
		$title = ($type eq "REFERRAL_SIGNIN") ? "New friend" : $title;
		$title = ($type eq "REFERRAL_FIRST_CALL") ? "Friend first call" : $title;
		$title = ($type eq "REFERRAL_RECHARGE") ? "Friend credit" : $title;
		$title = ($type eq "SERVICE_DIALOUT_DST") ? "Call bonus" : $title;
		$title = ($type eq "SERVICE_DIALOUT_DID") ? "Call bonus" : $title;
		$title = ($type eq "SERVICE_DIALOUT") ? "Call bonus" : $title;
		$title = ($type eq "MANUAL") ? "Manual" : $title;
		#$title = ($type eq "") ? "" : $title;
		$t{dic}{commission_summary} .= "<tr>";
		$t{dic}{commission_summary} .= "<td class=al style='border-left:0px;white-space: nowrap;'>$title</td>";
		#$t{dic}{commission_summary} .= "<td class=ar>".format_number($data{type}{$type}{all}{qtd},0)."</td>";
		$t{dic}{commission_summary} .= "<td class=ar>\$".format_number($data{type}{$type}{slice_0}{value},2)."</td>";
		$t{dic}{commission_summary} .= "<td class=ar>\$".format_number($data{type}{$type}{slice_1}{value},2)."</td>";
		$t{dic}{commission_summary} .= "<td class=ar>\$".format_number($data{type}{$type}{slice_2}{value},2)."</td>";
		$t{dic}{commission_summary} .= "</tr>";
		$data{total}{slice_0} += $data{type}{$type}{slice_0}{value};
		$data{total}{slice_1} += $data{type}{$type}{slice_1}{value};
		$data{total}{slice_2} += $data{type}{$type}{slice_2}{value};
		$data{total}{qtd} += $data{type}{$type}{all}{qtd};
	}
	if ($t{dic}{commission_summary} ne ""){
		$t{dic}{commission_summary} .= "<tr style='border-top:1px solid #c0c0c0;'>";
		$t{dic}{commission_summary} .= "<td class=al style=border-left:0px;><b>Total</b></td>";
		#$t{dic}{commission_summary} .= "<td class=ar><b>".format_number($data{total}{qtd},0)."</b></td>";
		$t{dic}{commission_summary} .= "<td class=ar><b>\$".format_number($data{total}{slice_0},2)."</b></td>";
		$t{dic}{commission_summary} .= "<td class=ar><b>\$".format_number($data{total}{slice_1},2)."</b></td>";
		$t{dic}{commission_summary} .= "<td class=ar><b>\$".format_number($data{total}{slice_2},2)."</b></td>";
		$t{dic}{commission_summary} .= "</tr>";
	}
	$t{dic}{commission_slice_0_total} .= format_number($data{total}{slice_0},2);
	$t{dic}{commission_slice_1_total} .= format_number($data{total}{slice_1},2);
	$t{dic}{commission_slice_2_total} .= format_number($data{total}{slice_2},2);
	$t{dic}{commission_total} .= format_number($data{total}{slice_0}+$data{total}{slice_1}+$data{total}{slice_2},2);
	$t{dic}{commission_slice_1_flag} .= ($data{total}{slice_1} > 0) ?1 : 0;
	$t{dic}{commission_slice_2_flag} .= ($data{total}{slice_2} > 0) ?1 : 0;
	#
	#=====================================================
	# get commissions.. INVOICED
	#=====================================================
    $sql = "
		SELECT id,unix_timestamp(creation_date),credit_id,send_to,status,value 
		FROM service_commission_invoice 
		WHERE service_id='$app{service_id}' 
		order by id desc
		limit 0,103
	    ";
    %list = database_select_as_hash($sql,"date,credit_id,type,status,value");
    $c=0;
    $html = "";
    $html_empty = "<tr><td style=border-left:0px; colspan=8><center>nothing...</td></tr>";
    foreach $list_id (sort{$list{$b}{date} <=> $list{$a}{date}} keys %list) {
		$c++;
		$value = &format_number($list{$list_id}{value},2);
		if ($list{$list_id}{type} eq "CREDIT") {
			$text = "Recharge unfinished";
			$text = ($list{$list_id}{status} eq 1) ? "Recharge approved" : $text;
			$text = (($list{$list_id}{status} eq 1) && ($list{$list_id}{credit_id} eq "")) ? "<font color=red>Recharge failed</font>" : $text;
			$text = ($list{$list_id}{status} eq -1) ? "<font color=red>Recharge rejected</font>" : $text;
			$value= ($list{$list_id}{status} >= 0) ? $value : ""; 
		} elsif ($list{$list_id}{type} eq "CHECK") {
			$text = "Check requested";
			$text = ($list{$list_id}{status} eq 1) ? "Check approved" : $text;
			$text = ($list{$list_id}{status} eq -1) ? "<font color=red>Check rejected</font>" : $text;
			$value= ($list{$list_id}{status} >= 0) ? $value : ""; 
		} else {
			next;
		}
		$html .= "<tr>";
		$html .= "<td style=border-left:0px; class=al>". &format_time_time($date)."</td>";
		$html .= "<td class=al><a title=\"View commissions for invoice $list_id\" href=$my_url?action=commissions&filter=i$list_id>$text</td>";
		#$html .= "<td class=al>$text</td>";
		if ($value ne "") {
			$html .= "<td class=ar>\$".&format_number($value,2)."</td>";
		} else {
			$html .= "<td class=ar>&nbsp;</td>";
		}
		$html .= "</tr>";
        $html_empty = "";
    }
	$html_overflow = ($c<100) ? "" : "<tr><td style=border-left:0px; colspan=8><center><font color=red><b>Warning:</b> Show only last 100 itens</font></td></tr>";
	$t{dic}{invoices_summary} = "$html $html_overflow $html_empty";
	#
	#
	#=====================================================
    # print page
	#=====================================================
	$t{dic}{service_id}				= $app{service_id};
	$t{dic}{service_alert}			= $app{service_alert};
	$t{dic}{service_name}			= $app{service_name};
	$t{dic}{service_email}			= $app{service_email};
	$t{dic}{service_credit}			= &format_number($app{service_credits},2);
	$t{dic}{service_credits_bar}	= $app{service_credits_bar};
    $t{dic}{my_url}					= $my_url;
    &template_print("template.myaccount.friends.html",%t);
}

sub do_friends_js() {
    &cgi_hearder_html();
    $service_id = clean_int(substr($form{id},0,100));
    #
    # busca em que nivel deep estamos
    $deep_level = 1;
    $next_ids = "$app{service_id},";
    foreach $deep (1..50) {
	$next_ids = substr($next_ids,0,-1);
	$sql = "SELECT service_id,1 FROM service_tree where parent_service_id in ($next_ids)";
	%list = database_select_as_hash($sql);
	$next_ids = "";
	foreach $id (keys %list) {
	    $next_ids .= "$id,";
	    if ($service_id eq $id) {
	        $deep_level = $deep+1;
		$next_ids = "";
		last;
	    }
	}
	if ($next_ids eq "") {last}
    }
    #
    # busca lista de child ids desse parent
    $sql = "
	SELECT
	    service_tree.service_id,
	    unix_timestamp(service.creation_date),
	    service.name,
	    service_status.deleted 
	FROM
	    service_tree,
	    service,
	    service_status 
	where
	    service_tree.parent_service_id='$service_id' and
	    service_tree.service_id = service.id and
	    service.status=service_status.id 
	";
    %list = database_select_as_hash($sql,"date,name,deleted");
    #
    # busca somatorio dos dados
    $ids = "";
    foreach (keys %list) {$ids .= "$_,"}
    if ($ids ne "") {
	$ids = substr($ids,0,-1);
	$sql = "
	    select parent_service_id,count(*) 
	    from service_tree 
	    where parent_service_id in ($ids)
	    group by parent_service_id
	";
	%sum = database_select_as_hash($sql);
	foreach(keys %sum) {$list{$_}{friends} = $sum{$_};}
	$sql = "
	    select from_service_id,sum(value) 
	    from service_commission 
	    where status=1 and service_id='$app{service_id}' and from_service_id in ($ids)
	    group by from_service_id
	";
	%sum = database_select_as_hash($sql);
	foreach(keys %sum) {$list{$_}{comissions} = $sum{$_};}
    }
    #
    # imprime em js pra popular a tabela
    print "<script>parent.ContainerClean('".$service_id."_box');</script>";
    $size = scalar keys %list;
    $c=0;
    foreach $id (sort{$list{$b}{date} <=> $list{$a}{date} } keys %list) {
		#
		# calcula extras
		$friends = "$list{$id}{friends} friends";
		$friends = ($list{$id}{friends} eq 1) ? "one friend" : $friends;
		$friends = ($list{$id}{friends} eq "") ? "" : $friends;
		$comissions = "\$".&format_number($list{$id}{comissions},2)." in commissions ";
		$comissions = ($list{$id}{comissions} eq "") ? "" : $comissions;
		$border1 = ($comissions.$friends ne "") ? "<font color=#999999>( " : "";
		$border2 = ($comissions.$friends ne "") ? " )</font>" : "";
		$and = ( ($comissions ne "") && ($friends ne "") ) ? "and" : "";
		$c++;
		#
		# calcula nome
		$tmp = ($deep_level>2)?1:0;
		$name = &format_trim_name($list{$id}{name},$tmp);
		$name = ($name eq "") ? "<font color=#c0c0c0>(No name $id)</font>" : $name;
		#
		# calcula url
		$url = ($friends ne "") ? "javascript:ClickItem($id)" : "javascript:void(0);";
		#
		# calcula class
		if ($c eq $size) {
		    $class = ($friends ne "")  ? "tree_plus_end" : "tree_line_end";
		} else {
		    $class = ($friends ne "")  ? "tree_plus" : "tree_line";
		}
		#
		# imprime node
		# $border1 $comissions $and $friends $border2
		$html = "<a href='$url'><img src=/design/icons/user.png hspace=0 vspace=0 border=0 style='margin-right:5px;' align=left>$name</a>";
        print "<script>parent.ContainerAppend('".$service_id."_box','$id',\"$html\",'$class');</script>";
    }
}
sub do_commissions() {
	#&cgi_redirect("$my_url?action=friends");
	#return;
	#
	#=====================================================
    # start 
	#=====================================================
    %t = %template_default;
	$html = "";
	#
	#=====================================================
	# commission list
	#=====================================================
	#
	#------------------------
	# engine select 
	#------------------------
	$sql_engine = "";
	$sql_engine = ($form{engine} eq "REFERRAL_SIGNIN")		? " and engine='REFERRAL_SIGNIN' " 		: $sql_engine;
	$sql_engine = ($form{engine} eq "REFERRAL_FIRST_CALL")	? " and engine='REFERRAL_FIRST_CALL' " 	: $sql_engine;
	$sql_engine = ($form{engine} eq "REFERRAL_RECHARGE")	? " and engine='REFERRAL_RECHARGE' " 	: $sql_engine;
	$sql_engine = ($form{engine} eq "SERVICE_DIALOUT")		? " and (engine='SERVICE_DIALOUT_DID' or engine='SERVICE_DIALOUT_DST') " 	: $sql_engine;
	$sql_engine = ($form{engine} eq "REFERRAL_DIALOUT")		? " and (engine='REFERRAL_DIALOUT_DID' or engine='REFERRAL_DIALOUT_DST') " 	: $sql_engine;
	$sql_engine = ($form{engine} eq "RADIO")				? " and (engine='RADIO_LISTEN' or engine='RADIO_OWNER') " 					: $sql_engine;
	$sql_engine = ($form{engine} eq "RADIO_LISTEN")			? " and engine='RADIO_LISTEN' " 		: $sql_engine;
	$sql_engine = ($form{engine} eq "RADIO_OWNER")			? " and engine='RADIO_OWNER'  " 		: $sql_engine;
	$sql_engine = ($form{engine} eq "MANUAL")				? " and engine='MANUAL' " 				: $sql_engine;
	$form{engine} = ($sql_engine eq "") ? "" : $form{engine}; 
	$t{form_engine} = $form{engine};
	$t{"form_engine_select_".$form{engine}} = 1;
	#
	#------------------------
	# filter select
	#------------------------
	$sql_filter = "";
	$sql_filter = ($form{filter} eq 0) ? " and invoice_id is null and now()<activation_date_1 and now()<activation_date_2 " : $sql_filter;
	$sql_filter = ($form{filter} eq 1) ? " and invoice_id is null and now()>=activation_date_1 " : $sql_filter;
	$sql_filter = ($form{filter} eq 2) ? " and invoice_id is null and now()>=activation_date_2 " : $sql_filter;
	$sql_filter = ($form{filter} eq 3) ? " and invoice_id is null and (now()>=activation_date_1 or now()>=activation_date_2) " : $sql_filter;
	$sql_filter = ($form{filter} eq 6) ? " and invoice_id is not null " : $sql_filter;
	$sql_filter = ($form{filter} eq 7) ? " and invoice_id is null " : $sql_filter;
    $sql = "
		SELECT id,unix_timestamp(creation_date),credit_id,send_to,status,value 
		FROM service_commission_invoice 
		WHERE service_id='$app{service_id}' 
		order by id desc
		limit 0,200
	    ";
    %hash = database_select_as_hash($sql,"date,credit_id,type,status,value");
    $loop_index = 1;
    $t{invoices_found} = 0;
    foreach $id (sort{$hash{$b}{date} <=> $hash{$a}{date}} keys %hash) {
    	$t{invoices_found} 					= 1;
		$t{invoices}{$loop_index}{"id"}		= $id;
		$t{invoices}{$loop_index}{"value"}	= &format_number($hash{$id}{value},2);
		$t{invoices}{$loop_index}{"date"}	= &format_time_time($hash{$id}{date});
		$t{invoices}{$loop_index}{"type"}	= $hash{$id}{type};
		$t{invoices}{$loop_index}{"type_is_".$t{invoices}{$loop_index}{"type"}} = 1;
		$t{invoices}{$loop_index}{"status"}	= "UNKNOWN";
		$t{invoices}{$loop_index}{"status"}	= ($hash{$id}{status} eq 1) ? "OK" : $t{invoices}{$loop_index}{"status"};
		$t{invoices}{$loop_index}{"status"}	= ($hash{$id}{status} eq 0) ? "REQUESTED" : $t{invoices}{$loop_index}{"status"};
		$t{invoices}{$loop_index}{"status"}	= ($hash{$id}{status} eq -1) ? "REJECTED" : $t{invoices}{$loop_index}{"status"};
		$t{invoices}{$loop_index}{"status"}	= (($hash{$id}{type} eq "CREDIT") && ($hash{$id}{status} eq 1) && ($hash{$id}{credit_id} eq "")) ? "FAIL" : $t{invoices}{$loop_index}{"status"};
		$t{invoices}{$loop_index}{"status_is_".$t{invoices}{$loop_index}{"status"}} = 1;
		if ($form{filter} eq "i$id") {
			$t{invoices}{$loop_index}{"is_form_selected"} = 1;
			$sql_filter = " and invoice_id = '$id' "  ;
		}
	    $loop_index++;
    }
	$form{filter} = ($sql_filter eq "") ? "" : $form{filter}; 
	$t{form_filter} = $form{filter};
	$t{"form_filter_select_".$form{filter}} = 1;
	#
	#------------------------
	# get total
	#------------------------
	%hash = database_select_as_hash("SELECT 1,1,count(*),sum(value) FROM service_commission where service_id='$app{service_id}' $sql_filter $sql_engine ","flag,qtd,value");
	$quantity 	= ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd}>0) ) ? $hash{1}{qtd} : 0;
	$value		= ( ($hash{1}{flag} eq 1) && ($hash{1}{value}>0) ) ? $hash{1}{value} : 0;
	$t{total_qtd} 		= &format_number($quantity,0);
	$t{total_value} 	= &format_number($value,2);
	#
	#------------------------	
	# count pages
	#------------------------
	$page_size	= 20;
	$page_min	= 1;
	$page_max	= int(($quantity-1)/$page_size)+1;
	$page_max	= ($page_max<$page_min) ? $page_min : $page_max;
	$page 		= clean_int($form{page});
	$page 		= ($form{next} eq 1) ? $page+1 : $page;
	$page 		= ($form{previous} eq 1) ? $page-1 : $page;
	$page 		= ($page<$page_min) ? $page_min : $page;
	$page 		= ($page>$page_max) ? $page_max : $page;
	$sql_limit	= ($page-1)*$page_size;
	$tmp1 = &format_number($page_max,0);
	foreach $id ($page_min..$page_max) {
		$t{pages_count}{$id}{page} 		= &format_number($id,0);
		$t{pages_count}{$id}{pages_max} = $tmp1;
		$t{pages_count}{$id}{selected} 	= ($id eq $page) ? 1 : 0;
	}
	#
	#------------------------	
	# query data
	#------------------------
	$sql = "
	SELECT
		unix_timestamp(creation_date),IF(now()>=activation_date_1,1,0),IF(now()>=activation_date_2,1,0),
		id,status,from_service_id,credit_id,deep,value,invoice_id,title,engine
	FROM service_commission 
	where service_id='$app{service_id}' $sql_filter $sql_engine 
	order by  invoice_id,creation_date desc
	limit $sql_limit,$page_size
	";
	%hash = database_select_as_hash_with_auto_key($sql, "creation_date,date_1,date_2,id,status,from_service_id,credit_id,deep,value,invoice_id,title,type");
	#
	#------------------------	
	# monta os selecionados
	#------------------------
	%from_services = ();
    $t{commissions_found} = 0;
    $loop_index = 1;
    %service_ids_to_find_name = ();
	foreach $id (sort{$a <=> $b} keys %hash) {
	    $t{commission_found} = 1;
		$t{commissions}{$loop_index}{"id"}					= $hash{$id}{id};
		$t{commissions}{$loop_index}{"date"}				= &format_time_time($hash{$id}{creation_date});
		$t{commissions}{$loop_index}{"date_1_is_ok"}		= $hash{$id}{date_1};
		$t{commissions}{$loop_index}{"date_2_is_ok"}		= $hash{$id}{date_2};
		#$t{commissions}{$loop_index}{"date_1_gap_days"}		= int((time-$hash{$id}{date_1})/(60*60*24));
		#$t{commissions}{$loop_index}{"date_2_gap_days"}		= int((time-$hash{$id}{date_2})/(60*60*24));
		#$t{commissions}{$loop_index}{"date_1_gap_days"}		= ($t{commissions}{$loop_index}{"date_1_gap_days"}<0) ? clean_int($t{commissions}{$loop_index}{"date_1_gap_days"}) : $t{commissions}{$loop_index}{"date_1_gap_days"};
		#$t{commissions}{$loop_index}{"date_2_gap_days"}		= ($t{commissions}{$loop_index}{"date_2_gap_days"}<0) ? clean_int($t{commissions}{$loop_index}{"date_2_gap_days"}) : $t{commissions}{$loop_index}{"date_2_gap_days"};
		$t{commissions}{$loop_index}{"title"}				= $hash{$id}{title};
		$t{commissions}{$loop_index}{"deep"}				= $hash{$id}{deep};
		$t{commissions}{$loop_index}{"from_service_id"}		= $hash{$id}{from_service_id};
		$t{commissions}{$loop_index}{"from_service_name"}	= "";
		$t{commissions}{$loop_index}{"from_service_found"}	= 0;
		$t{commissions}{$loop_index}{"credit_id"}			= $hash{$id}{credit_id};
		$t{commissions}{$loop_index}{"invoice_id"}			= $hash{$id}{invoice_id};
		$t{commissions}{$loop_index}{"value"}				= &format_number($hash{$id}{value},2);
		$t{commissions}{$loop_index}{"type"}				= $hash{$id}{type};
		$t{commissions}{$loop_index}{"status"}				= "UNKNOWN";
		$t{commissions}{$loop_index}{"status"}				= ($hash{$id}{status} eq 1) ? "OK" : $t{commissions}{$loop_index}{"status"};
		$t{commissions}{$loop_index}{"status"}				= ($hash{$id}{status} eq 0) ? "REQUESTED" : $t{commissions}{$loop_index}{"status"};
		$t{commissions}{$loop_index}{"status"}				= ($hash{$id}{status} eq -1) ? "REJECTED" : $t{commissions}{$loop_index}{"status"};
		$t{commissions}{$loop_index}{"is_invoiced"}			= ($hash{$id}{invoice_id} ne "") ? 1 : 0;
		$t{commissions}{$loop_index}{"type"} 				= ( index("|UNKNOWN|MANUAL|REFERRAL_SIGNIN|REFERRAL_FIRST_CALL|REFERRAL_RECHARGE|SERVICE_DIALOUT_DID|SERVICE_DIALOUT_DST|REFERRAL_DIALOUT_DID|REFERRAL_DIALOUT_DST|RADIO_LISTEN|RADIO_OWNER|","$t{commissions}{$loop_index}{type}") eq -1) ? "UNKNOWN" : $t{commissions}{$loop_index}{"type"};
		$t{commissions}{$loop_index}{"status_is_".$t{commissions}{$loop_index}{"status"}} = 1;
		$t{commissions}{$loop_index}{"type_is_".$t{commissions}{$loop_index}{"type"}} = 1;
		$t{commissions}{$loop_index}{"deep_is_".$t{commissions}{$loop_index}{"deep"}} = 1;
		if ($hash{$id}{from_service_id} ne "") {
			$service_id = $hash{$id}{from_service_id};
			if (exists($service_ids_to_find_name{$service_id})) {
				$t{commissions}{$loop_index}{"from_service_name"}	= $service_ids_to_find_name{$service_id};
				$t{commissions}{$loop_index}{"from_service_found"}	= 1;
			} else {
				%hash2 = database_select_as_hash("SELECT 1,1,name from service where id='$service_id' ","flag,value");
				if ($hash2{1}{flag} eq 1) {
					$service_ids_to_find_name{$service_id} = $hash2{1}{value};
					$t{commissions}{$loop_index}{"from_service_name"}	= $service_ids_to_find_name{$service_id};
					$t{commissions}{$loop_index}{"from_service_found"}	= 1;
				}
			}
		}
		$loop_index++;
	}
	#
	#
	#=====================================================
    # print page
	#=====================================================
    $t{my_url}					= $my_url;
    &template_print("template.myaccount.commissions.html",%t);
}
sub do_sendemail(){
	#
	# verifica quantidade touch pra evitar os spammers
	# e mais paranoia que realidade.. mas e simples implementar
	$t = &active_session_get("sm_touch");
	$t = ($t eq "") ? 0 : $t;
	$t++;
	&active_session_set("sm_touch",$t);
	if ($t>50) {sleep(30)}
	if ($t>200) {sleep(90)}
	#
	# inicializa
	$message = "";
	$options = "";
	$sm_last = "";
	#
	# clear (just for debug)
	if ($form{email} eq "clear"){
		&active_session_set("sm_touch",0);
		&active_session_set("sm_last","");
		$message = "CLEAR";
	}
	#
	# check service email
	if ($message eq "") {
		$v1 = trim(substr($app{service_email},0,1024)); 
		$v2 = clean_str($v1,"()-=[]?><#\@");
		if ( ($v2 eq "") || (index($v2,"\@") eq -1) || (index($v2,"\@") ne rindex($v2,"\@")) || (index($v2," ") ne -1) || ($v1 ne $v2) ) {$message = "ERROR_SRC_EMAIL";}
	}
	#
	# check email
	if ($message eq "") {
		$v1 = trim(substr($form{email},0,1024)); 
		$v2 = clean_str($v1,"()-=[]?><#\@");
		if ( ($v2 eq "") || (index($v2,"\@") eq -1) || (index($v2,"\@") ne rindex($v2,"\@")) || (index($v2," ") ne -1) || ($v1 ne $v2) ) {$message = "ERROR_DST_EMAIL";}
		if ($message eq "") {
			$sm_last = &active_session_get("sm_last");
			if (index("\&$sm_last\&","\&$form{email}\&") ne -1) { $message = "ERROR_DST_EMAIL_DUPLICATED";}
		}
		$form{email} = $v1;
	}
	#
	# check subject
	if ($message eq "") {
		$v1 = trim(substr($form{subject},0,1024)); 
		$v2 = clean_str($v1,"()-=[]?><# \@");
		if ( ($v2 eq "") || ($v1 ne $v2) ) {$message = "ERROR_SUBJECT";}
		$form{subject} = $v1;
	}
	#
	# check message
	if ($message eq "") {
		$v1 = trim(substr($form{message},0,8*1024)); 
		$v2 = clean_str($v1,"()-=[]?><# \@\n\r\t");
		if ($v2 eq "")  {$message = "ERROR_MESSAGE";}
		if (index("\L$v1","http://www.zenofon.com/?") eq -1) {$message = "ERROR_MESSAGE_NO_INVITE";}
		$form{message} = $v1;
	}
	#
	# se tudo ok, envia email
	if ($message eq "") {
		%email = ();
		send_email($app{service_email},$form{email},$form{subject},$form{message});
		$sm_last = substr($sm_last."\&".$form{email},0,256);
		&active_session_set("sm_last",$sm_last);
		$message = "OK";
		$options = "clear";
	}
	#
	# print page
    &cgi_hearder_html();
	print "<script>parent.sendemail_answer('$message','$options')</script>";

}
 sub do_credits_buy_cim_phone(){
	#
    #------------------------------------------------------------------
    # START 
    #------------------------------------------------------------------
    #
	# To make simple, i store all things (variables, loops) that i want export 
	# to template into %t hash (can be any hash). At the end i call template
	# function with this hash and template to use. 
	#
	# Each time a CGI start, create a %template_default hash with lot of info
	# that i know will use in any cgi. Things like service name, email, balance
	# and future, other things. You can check at www/include.cgi
	#
	# another point: Template hash is like this %HASH{ITEM_NAME}=ITEM_VALUE
	# but old way was %HASH{dic}{ITEM_NAME}=ITEM_VALUE. Both ways work,
	# we have a hack into template function to understand old and new ways
	#
	# so lets start with variables to use in this template
	%t = %template_default;
 	$t{status_save_ok}					= 0;
 	$t{status_save_error}				= 0;
 	$t{status_save_error_clickchain}	= 0;
	#
	#
    #------------------------------------------------------------------
    # READ ORIGINAL DATA FROM DATABASE
    #------------------------------------------------------------------
    #
	# We need check credit card profile for this user. 
	# if no credit card, we need disable forms at template and 
	# do action in the right way bellow
	%tmp_hash = &multilevel_securedata_cc_get($app{service_id},"DO_NOT_CHECK_CC_ERROR");
	$t{profile_exists} 			= ($tmp_hash{status_ok} eq 1) ? 1 : 0;
	$t{profile_with_cc_errors}	= ($tmp_hash{cc_error} eq 1) ? 1 : 0;
	$t{profile_ok}				= ($t{profile_exists}.$t{profile_with_cc_errors} eq "10") ? 1 : 0; 
	$t{profile_cc_number}		= $tmp_hash{cc_number};
	$t{profile_cc_first_name}	= $tmp_hash{first_name};
	$t{profile_cc_last_name}	= $tmp_hash{last_name};
	#
	# now lets load and normalize actual disable_recharge_over_phone
	$t{disable_recharge_over_phone}	= &data_get("service_data",$app{service_id},"disable_recharge_over_phone");
	$t{disable_recharge_over_phone}	= ($t{disable_recharge_over_phone} eq 1) ? 1 : 0;
	#
    #------------------------------------------------------------------
    # TRY TO SAVE DATA IF ITS SECOND ACCESS
    #------------------------------------------------------------------
    #
	# one point about security: We know only log-in people enter this page,
	# but crocks can send URL to other people to force web actions. Then to
	# make perfect safe, we need be SURE that this form data comes from legitm 
	# form we build and not a outside url. 
	# 
	# to do that, each time we build a form, we create a saveid, add in the form
	# and store saveid in user session. Later, we need check this saveid with 
	# session saveid. If its ok, means this actions really comes from the form
	# we give to user. If not ok, we silently ignore action.
	#
	# I alreade create 2 functions to handle this. We just need use a 3 digits 
	# length signature to avoid saveid colision with other forms that (maybe) user can 
	# navigate at same time (using multiple tabs or browsers)
	#
	# multilevel_clickchain_set gets a signature and return saveid to store in form
	# multilevel_clickchain_check gets signature,saveid and return 1 if ok 0 if problem
    #
    # Ok, befor print page, we need check if user is try to save data
    # remember we just do action if user has cc profile ok
	if (  ($t{profile_ok} eq 1) && ($form{saveid} ne "") ){
		#
		# lets check if saveid is ok.
		# remember to use same signature as we use below to generate saveid
		if (&multilevel_clickchain_check("bcp",$form{saveid}) ne 1) {
			#
			# wrong saveid! Or user try to save by build url, or some crock try to inject url
			# or we use same signature in other form and user open both forms at same time
			# lets just silently ignore save
			#
 			$t{status_save_error}				= 1;
		 	$t{status_save_error_clickchain}	= 1;
		} else {
			#
			# ok to save, lets do work
			if ($form{disable_recharge_over_phone_user_select} eq 1) {
				#
				# ok, user want disable, so lets create this flag  and set 1
				&data_set("service_data",$app{service_id},"disable_recharge_over_phone",1);
				#
				# we log each action. Each action has one id. Check action_log_type table 
				# we can send some extra info to this log, check function code to understand
				&action_history("cim:disrecoverphone:on",('service_id'=>$app{service_id}));		
 			} else {
 				#
 				# he allow phone recharge. Because we knwo defalt is allow, lets remove flag from database to save space
				&data_delete("service_data",$app{service_id},"disable_recharge_over_phone");
				&action_history("cim:disrecoverphone:off",('service_id'=>$app{service_id}));		
 			}
 			#
 			# lets flag we save ok, so template team can display messages, redirect page or whatever
		 	$t{status_save_ok} = 1;
		}
	}
	#
    #------------------------------------------------------------------
    # POPULATE FORM IF ITS FIRST ACCESS
    #------------------------------------------------------------------
    #
    # if its not save (no saveid) we need load data from database into form
    # usualy, if no save_id means its first time user enter in this action
    if ($form{saveid} eq ""){
		$form{disable_recharge_over_phone_user_select}	=  $t{disable_recharge_over_phone};
 	}
	#
    #------------------------------------------------------------------
    # PRINT PAGE
    #------------------------------------------------------------------
    #
    # now, we need move form values to template hash, so template
    # can be populate form with data we load (if its first enter) or
    # data modified by the user (subsequent requests)
    # we prefix "form_" into all form variables we add to template
 	$t{form_disable_recharge_over_phone_user_select} 	= $form{disable_recharge_over_phone_user_select}; 
 	#
 	# remember the saveid trick on top? now its time to create this thing
 	# try to use unique signature. Think this example:
 	# we have two pages (edit name and edit email) and at each page
 	# we use same signature at saveid. If user open both pages at same time
 	# (one in each tab or browser window) and try save both at same time, 
 	# first one will be accepted, and second one will be rejected, because
 	# saveid will be already used in second save. To avoid this colisions
 	# we add a "almost unique" prefix at *clickchain* functions.
 	$t{saveid} = &multilevel_clickchain_set("bcp");
 	#
 	# my_url is this cgi name. We use variable so we can change cgi name
 	# without need edit template file. 
    $t{my_url} = $my_url;
    #
    # Now that we have all information (service data from database, saveid, 
    # form data, form status) at %t hash and we can call template 
	#foreach (sort keys %form) 	{$t{debug} .= "DUMP --> FORM --> $_=$form{$_}<br>"}
    #foreach (sort keys %t) 		{if($_ eq "debug"){next} $t{debug} .= "DUMP --> TEMPLATE --> $_=$t{$_}<br>"}
    #foreach (sort keys %ENV) 	{$t{debug} .= "DUMP --> ENV --> $_=$ENV{$_}<br>"}	
    &template_print("template.myaccount.credits.add.cim.phone.html",%t);	
}
#=======================================================




sub TEMPLATE_ACTION(){
	#
   	#----------------------------------------------------- 
	# start and load some basic data
   	#----------------------------------------------------- 
	%t = %template_default;
	$t{status_save_ok}					= 0;
    $t{status_save_error}				= 0;
    $t{form_disabled}					= 0;
    $t{click_id_prefix}					= "Cp";
    #
   	#----------------------------------------------------- 
   	# load global and disable form if need
   	#----------------------------------------------------- 
   	#$t{form_disabled} = 1;
    $t{text} = &active_user_get("TEXT");
    #
   	#----------------------------------------------------- 
   	# User try to save form. lets process form
   	#----------------------------------------------------- 
    if ($ENV{REQUEST_METHOD} eq "POST"){
    	if ($form{click_id} eq "") {
		    $t{status_save_error} = 1;
		    $t{status_save_error_clickid} = 1;
    	} else {
 	 	  	if (&multilevel_clickchain_check($t{click_id_prefix},$form{click_id}) ne 1) {
			    $t{status_save_error} = 1;
			    $t{status_save_error_clickid} = 1;
 	 	  	} else {
	    		#
				#----------------------------------------------------- 
	    		# click_id is ok, lets check form
			   	#----------------------------------------------------- 
		    	if ($form{text} eq "") {
				    $t{status_save_error} = 1;
				    $t{status_save_error_invalidtext} = 1;
		    	} 
		    	#
   				#----------------------------------------------------- 
		    	# Save if approved
				#----------------------------------------------------- 
		    	if ($t{status_save_error} eq 0) {
		    		&active_user_set("TEXT",$form{text});
					$t{status_save_ok} = 1;
		    	}
 	 	  	}
    	}
    }
    #
   	#----------------------------------------------------- 
   	# its first time we see this person. pupulate form
   	#----------------------------------------------------- 
    if ($ENV{REQUEST_METHOD} ne "POST"){
    	$form{text} = $t{text};
    }
    #
   	#----------------------------------------------------- 
    # fill always present data
   	#----------------------------------------------------- 
    $t{click_id}	= &multilevel_clickchain_set($t{click_id_prefix});
    #foreach (sort keys %form) 	{$t{"form_".$_}	= $form{$_}} # not safe but ok to dev
	$t{form_text}	= $form{text};
    #
   	#----------------------------------------------------- 
    # print page
   	#----------------------------------------------------- 
    foreach (sort keys %form) 	{$t{debug} .= "DUMP --> FORM --> $_=$form{$_}<br>"}
    foreach (sort keys %t) 		{if($_ eq "debug"){next} $t{debug} .= "DUMP --> TEMPLATE --> $_=$t{$_}<br>"}
    foreach (sort keys %ENV) 	{$t{debug} .= "DUMP --> ENV --> $_=$ENV{$_}<br>"}
    &template_print("TEMPLATE_FILE_LIKE EXAMPLE BELLOW",%t);	
	$TEMPLATE_FILE = qq[
	<script>
	function form_check(){
		MyDisplay('loading_form',1);
		document.forms[0].elements[0].readonly = true;
		document.forms[0].elements[1].disabled = true;
		document.forms[0].elements[1].readonly = true;
		document.forms[0].elements[2].disabled = true;
		document.forms[0].elements[2].readonly = true;
		return true;
	}
	</script>
	<div class=clear style="width:400px;">
		<h3>Action title</h3>
		Some text to let user know how to use and why use this tool<br> 
		<br>
		<form action="index.cgi"  method=post onsubmit="return form_check();">
			Text: <input type=text name=text value="%form_text%"><br>
					
			<TMPL_IF NAME="status_save_error">
				<div class=alert_box ><div class=alert_box_inside>
				<font color=red><b>I cannot save:</b></font> 
				<TMPL_IF NAME="status_save_error_clickid">Internal error. Try again.</TMPL_IF>
				<TMPL_IF NAME="status_save_error_invalidtext">Please enter valid text.</TMPL_IF>
				</div></div>
				<br>
			</TMPL_IF>
	
			<TMPL_IF NAME="status_save_ok">
				<div class=alert_box ><div class=alert_box_inside>
				<font color=green><b>Save OK:</b></font> Message dismiss in 5 seconds
				</div></div>
				<br>
				<script>setTimeout("window.location='./?action=credits';", 3000); </script>
			</TMPL_IF>
	
			<div id=loading_form style="Display:none; ">
				<div class=alert_box ><div class=alert_box_inside style="background-image:url(/design/img/loading.gif);background-repeat:no-repeat;">
				Please wait...
				</div></div>
				<br>
			</div>
	
			<TMPL_IF NAME="form_disabled">
				<div class=alert_box ><div class=alert_box_inside>
				Sorry, but this tool is disabled
				</div></div>
				<br>
			</TMPL_IF>
	
			<button style="padding:3px;" type=button onclick="window.location='?action=credits'"><img src=/design/icons/delete.png hspace=0 vspace=0 border=0 width=16 height=16 align=left> Cancel</button>
			<button style="padding:3px;" type=submit <TMPL_IF NAME="form_disabled">disabled readonly</TMPL_IF> ><img src=/design/icons/accept.png hspace=0 vspace=0 border=0 width=16 height=16 align=left> Save</button>
			<input type=hidden name=action value=ACTION_ID>
			<input type=hidden name=click_id value=%click_id%>
		</form>
	</div>
	];
}
