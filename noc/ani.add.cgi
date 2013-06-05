#!/usr/bin/perl
require "include.cgi";
use Data::Dumper;
$Data::Dumper::Sortkeys = 1;
#require "../include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_manage_services") ne 1) {adm_error("no permission"); exit;}
#=======================================================



#=======================================================
# main loop
#=======================================================
$my_url = "ani.add.cgi";
$action = $form{action};
#adm_error($action);
if		($action eq "add_ani")		{&do_add_ani();}
else								{&view_add_ani();}

sub view_add_ani(){
	%t = ();
	$t{dic}{title} = "Bulk Add ANI's";
	$t{dic}{content} = qq[
		<form method="post">
		Only ANI is required, rest is Optional<br>
		ANI List :
		<textarea name='anilist' cols=80 rows=30>ANI[,EMAIL[,NAME[,DST]]]\nANI[,EMAIL[,NAME[,DST]]]</textarea><br>
		Invited By : <input type=text name=inviter><br>
		Make PIN Calls : <select name=makecall><option value=yes>yes</option><option value=no>no</option></select><br>
		Carrier : <input type=text name=carrier><br>
		Radio Name/Number <input type=text name=radio><br>
		<input type=hidden name=action value=add_ani><br>
		<input type=submit><br>
		
		</form>
	];
	&template_print("template.html",%t);
}

sub do_tag_add_silent(){
	my($tagname) = @_;
    $value = trim(clean_str(substr($tagname,0,100),"\@. ()-_[]:"));
	
	$sql = "select 1, 1, id from service_tag_string where tag like '$value'";
	
	%hash = database_select_as_hash($sql, "found,id");

	if($hash{1}{found} ne "1"){
		$id = &database_do_insert("insert service_tag_string (tag) values ('$value') ");
		&action_history("noc:tag:edit",('service_id'=>$service_id, 'adm_user_id'=>$app{session_cookie_u}, 'value_old'=>"add", 'value_new'=>$value ));
		return $id;
	}else{
		return $hash{1}{id};
	}
}

sub add_service_tag(){
	my($service_id, $tag_id) = @_;
	database_do ("insert into service_tag (service_id,tag_string_id) values ('$service_id','$tag_id') ");
	return;
}

sub do_add_ani(){
	%t = ();
	$anilist = $form{anilist};
	$inviter = $form{inviter};
	$makecall = $form{makecall};
	$carrier = $form{carrier};
	$radio = $form{radio};
	
	$carrierTag = &do_tag_add_silent($carrier);
	$radioTag = &do_tag_add_silent($radio);
	@anilist = split(/\n/, $anilist);
	$str = "";
	$t{dic}{content} = "";
	
	for $str(@anilist){
		$str =~ s/[\ \r]//g;
		@str = split(/,/, $str);
		my($ani, $email, $name, $dst) = @str;
		open(MASS_ANI_ADD, ">autosignup_log/ani_$ani.log");
		
		if($dst eq ""){
			$dst = $ani;
		}
		%output = do_add($inviter, $ani, $dst, "", $name, $email, $makecall);
		print MASS_ANI_ADD $ani . "---" . Dumper(\%output) . "\n";
		
		$service_id = $output{service_id};
		
		#%credit_log = &do_credit_add($service_id, 3, "Free Credit");
		#print MASS_ANI_ADD Dumper(\%credit_log) . "\n------------------------------------------------\n";
		close MASS_ANI_ADD;
		
		&add_service_tag($service_id, $carrierTag);
		&add_service_tag($service_id, $radioTag);
	}
	
	$t{dic}{title} = "Mass Registration Output";
	$t{dic}{content} = "Completed";
	&template_print("template.html", %t)
}


sub do_credit_add(){
	my($service_id, $value, $text) = @_;

		# confere valor
		$value++;
		$value--;
		#
		# adiciona o credito
				%order = ();
				$order{service_id}	= $service_id;
				$order{value_credit}= $value;
				$order{value_money}	= 0;
				$order{type}		= "FREE";
				$order{text}		= "$text";
				$order{ok}			= 0;
				%order = multilevel_credit_add(%order);
				
				if ($order{ok} eq 1)  {
					&action_history("noc:service:credit:free",('service_id'=>$service_id,'credit_id'=>$order{new_credit_id},'adm_user_id'=>$app{session_cookie_u}));
				}
				return %order;
}


sub do_add(){
	%form = ();
	my($forminvite, $formani, $formdst, $formpin, $formaniName, $formaniEmail, $makecall) = @_;
	$form{invite} = $forminvite;
	$form{ani} = $formani;
	$form{dst} = $formdst;
	$form{terms} = 1;
	$form{pin} = $formpin;
	$form{aniName} = $formaniName;
	$form{aniEmail} = $formaniEmail;
	$form{coupon_error_accepted} = 1;

    #
	#============================================
    # start default values
	#============================================
    %t = ();
    $t{mode} = "";
	#
	#============================================
	# pega invite
	#============================================
	$t{invite_ok} = 0;
	$buf = $form{invite};
	$buf = clean_str(substr($buf,0,100),"-_","MINIMAL");
	$buf = (length($buf) < 3) ? "" : $buf;
	$buf = (length($buf) > 20) ? "" : $buf;
	if ($buf ne "") {
		$sql = "
			select 
				1,1,
				service.id,
				service.name,
				service_status.refer_status,
				service_status.refer_status_premium,
				service_status.signin_coupon_premium_id,
				service_status.signin_coupon_default_id
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
		%hash = database_select_as_hash($sql,"flag,id,name,signin_status,signin_status_premium,signin_coupon_premium_id,signin_coupon_default_id");
		if ($hash{1}{flag} eq 1) {
			$t{invite_ok}						= 1;
			$t{invite_id}						= $buf;
			$t{invite_service_id}				= $hash{1}{id};
			$t{invite_service_name}				= $hash{1}{name};
			$t{invite_signin_status}			= $hash{1}{signin_status};
			$t{invite_signin_status_default}	= $hash{1}{signin_status};
			$t{invite_signin_status_premium}	= $hash{1}{signin_status_premium};
			$t{invite_signin_coupon_premium_id}	= $hash{1}{signin_coupon_premium_id};
			$t{invite_signin_coupon_default_id}	= $hash{1}{signin_coupon_default_id};
		}
	}
	#
	#============================================
	# get default coupon
	#============================================
	%coupon = ();
	$t{coupon_default_exists}		= 0;
	$t{coupon_default_in_stock}		= 0;
	$t{coupon_default_stock_qtd}	= 0;
	$t{coupon_default_ani_locked}	= 0;
	$t{coupon_default_error}		= 0;
	if ( ($t{invite_ok} eq 1) && ($t{invite_signin_coupon_default_id} ne "") && ($t{invite_signin_coupon_default_id} > 0) ) {
		$sql = "
		select 
			1,1,
			service_coupon_type.id,
			service_coupon_type.title
		from 
			service_coupon_type,service_coupon_type_status
		where 
			service_coupon_type.id = '$t{invite_signin_coupon_default_id}' and 
			service_coupon_type.status = service_coupon_type_status.id and 
			service_coupon_type_status.is_active = 1
		";
		%hash = database_select_as_hash($sql,"flag,id,title");
		if ($hash{1}{flag} eq 1) {
			$t{coupon_default_exists}		= 1;
			$t{coupon_default_type_id}		= $hash{1}{id};
			$t{coupon_default_title}		= $hash{1}{title};
			$sql = "
			select 1,1,count(*)
			from 
				service_coupon_stock,
				service_coupon_stock_status
			where 
				service_coupon_stock.coupon_type_id='$t{coupon_default_type_id}' and 
				service_coupon_stock.status = service_coupon_stock_status.id and 
				service_coupon_stock_status.is_ready_to_assign
			";
			%hash = database_select_as_hash($sql,"flag,value");
			if ($hash{1}{flag} eq 1) {
				$t{coupon_default_in_stock}		= ($hash{1}{value}>0) ? 1 : 0;
				$t{coupon_default_stock_qtd}	= $hash{1}{value};
			}
		}
	}
	#
	#============================================
	# get premium coupon
	#============================================
	%coupon = ();
	$t{coupon_premium_exists}		= 0;
	$t{coupon_premium_in_stock}		= 0;
	$t{coupon_premium_stock_qtd}	= 0;
	$t{coupon_premium_ani_locked}	= 0;
	$t{coupon_premium_error}		= 0;
	if ( ($t{invite_ok} eq 1) && ($t{invite_signin_coupon_premium_id} ne "") && ($t{invite_signin_coupon_premium_id} > 0) ) {
		$sql = "
		select 
			1,1,
			service_coupon_type.id,
			service_coupon_type.title
		from 
			service_coupon_type,service_coupon_type_status
		where 
			service_coupon_type.id = '$t{invite_signin_coupon_premium_id}' and 
			service_coupon_type.status = service_coupon_type_status.id and 
			service_coupon_type_status.is_active = 1
		";
		%hash = database_select_as_hash($sql,"flag,id,title");
		if ($hash{1}{flag} eq 1) {
			$t{coupon_premium_exists}		= 1;
			$t{coupon_premium_type_id}		= $hash{1}{id};
			$t{coupon_premium_title}		= $hash{1}{title};
			$sql = "
			select 1,1,count(*)
			from 
				service_coupon_stock,
				service_coupon_stock_status
			where 
				service_coupon_stock.coupon_type_id='$t{coupon_premium_type_id}' and 
				service_coupon_stock.status = service_coupon_stock_status.id and 
				service_coupon_stock_status.is_ready_to_assign
			";
			%hash = database_select_as_hash($sql,"flag,value");
			if ($hash{1}{flag} eq 1) {
				$t{coupon_premium_in_stock}		= ($hash{1}{value}>0) ? 1 : 0;
				$t{coupon_premium_stock_qtd}	= $hash{1}{value};
			}
		}
	}
	#
	#============================================
	# pega rate table a ser usada como route 1 do status que supostamente devera ser atribuido com esse convite
	#============================================
	$t{rate_table_for_ani} = 9;
	$t{rate_table_for_dst} = 10;
	if ( ($t{invite_ok} eq 1) && ($t{invite_signin_status} ne "") && ($t{invite_signin_status} > 0) ) {
		$sql = "select  1,1,rate_slot_1,rate_slot_callback from service_status where id = '$t{invite_signin_status}' ";
		%hash = database_select_as_hash($sql,"flag,value1,value2");
		if ($hash{1}{flag} eq 1) {
			$t{rate_table_for_ani} = $hash{1}{value2};
			$t{rate_table_for_dst} = $hash{1}{value1};
		}
	}
    #
	#============================================
    # Check ANI
	#============================================
    $t{ani} 				= substr($form{ani},0,100);
	#$t{aniName}				= clean_str(substr($form{aniName}, 0, 100));
	#$t{aniEmail}			= substr($form{aniEmail}, 0, 100);
    $t{ani_ok} 				= 0;
    $t{ani_error} 			= 0;
    $t{ani_error_format} 	= 0;
    $t{ani_error_no_rate} 	= 0;
    $t{ani_error_in_use} 	= 0;
    $t{ani_error_locked} 	= 0;
	

    if ($t{ani} ne "") {
		# check format 
		($tmp0,$tmp1,$tmp2) = &multilevel_check_E164_number(&clean_int($t{ani}));
		if ($tmp0 eq "OK") {
			$t{ani} = $tmp1;
		} else {
			$t{error_string} = "ANI Not correct";
		    $t{ani_error} 			= 1;
		    $t{ani_error_format} 	= 1;
		}
		# check rate
		if ($t{ani_error} eq 0) {
			%hash = &multilevel_rate_table_get($t{ani},$t{rate_table_for_ani});
			if ($hash{ok_to_use} ne 1) {
				$t{error_string} = "ANI Proper rate not found";
			    $t{ani_error} 			= 1;
			    $t{ani_error_no_rate} 	= 1;
			}
		}
		# second level check ANI list
		if ($t{ani_error} eq 0) {
			%hash = database_select_as_hash("select 1,1,count(*) from service_ani where ani='$number' and service_id<>'$app{service_id}'","flag,qtd");
			unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ) {
				$t{error_string} = "ANI Second Level Check Failed";	
			    $t{ani_error} 			= 1;
			    $t{ani_error_in_use} 	= 1;
			}
		}
	    # Se ANI ta ok flag ele
		if ($t{ani_error} eq 0) {
		    $t{ani_ok} = 1;
		    $t{ani_E164} = $t{ani};
		    $t{ani} = &format_E164_number($t{ani},"USA");
		}
    }
	#
	#============================================
	# Get provider by ani
	#============================================
    $t{ani_provider_found} = 0;
    if ( ($t{ani_ok} eq 1) && ($t{ani_E164} ne "") ) {
	    %hash = &get_carrier_by_number($t{ani_E164});
		if ($hash{found} eq 1) {
		    $t{ani_provider_found}					= 1;
			$t{ani_provider_id}						= $hash{carrier_id};
			$t{ani_provider_name} 					= $hash{carrier_name};
			$t{ani_provider_is_mobile} 				= ($hash{carrier_is_mobile} eq 1) ? 1 : 0;
			$t{ani_provider_is_premium} 			= ($hash{flag_premium_signin} eq 1) ? 1 : 0;
			$t{"ani_provider_type_".$hash{type}} 	= 1;
		}
    }
	#
	#============================================
	# choose premium/default signin_status
	#============================================
	$t{invite_signin_status} = $t{invite_signin_status_default};
	if ( ($t{ani_provider_is_premium} eq 1) && ($t{invite_signin_status_premium} ne "") ) {
		$t{invite_signin_status} = $t{invite_signin_status_premium};
	}
	#
	#============================================
	# choose premium/default cooupon
	#============================================
	$t{coupon_error}		= 0;
	$t{coupon_exists}		= $t{coupon_default_exists};
	$t{coupon_type_id}		= $t{coupon_default_type_id};
	$t{coupon_title}		= $t{coupon_default_title};
	$t{coupon_in_stock}		= $t{coupon_default_in_stock};
	$t{coupon_stock_qtd}	= $t{coupon_default_stock_qtd};
	$t{coupon_is_premium}	= 0;
	if ( ($t{coupon_premium_in_stock} eq 1) && ($t{ani_provider_is_premium} eq 1) ) {
		$t{coupon_exists}		= $t{coupon_premium_exists};
		$t{coupon_type_id}		= $t{coupon_premium_type_id};
		$t{coupon_title}		= $t{coupon_premium_title};
		$t{coupon_in_stock}		= $t{coupon_premium_in_stock};
		$t{coupon_stock_qtd}	= $t{coupon_premium_stock_qtd};
		$t{coupon_is_premium}	= 1;
	}
	#
	#============================================
	# re-check coupon: one coupon per ANI
	#============================================
	# new logic limitation
	if ( ($t{ani_ok} eq 1) && ($t{coupon_in_stock} eq 1)  ) {
		%hash = database_select_as_hash("select 1,1,count(*) from service_signin where ani='$t{ani_E164}' and service_id is not null ","flag,qtd");
		unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} eq 0) ) {
			$t{coupon_error}			= 1;
			$t{coupon_error_ani_locked}	= 1;
		}
	}
    #
	#============================================
    # Check DST
	#============================================
    $t{dst} 				= substr($form{dst},0,100);
    $t{dst_ok} 				= 0;
    $t{dst_error} 			= 0;
    $t{dst_error_format} 	= 0;
    $t{dst_error_no_rate} 	= 0;
	
		
    if ($t{dst} ne "") {
		# check format 
		($tmp0,$tmp1,$tmp2) = &multilevel_check_E164_number(&clean_int($t{dst}));
		if ($tmp0 eq "OK") {
			$t{dst} = $tmp1;
		} else {
		    $t{dst_error} 			= 1;
		    $t{dst_error_format} 	= 1;
		}
		# check rate
		if ($t{dst_error} eq 0) {
			%hash = &multilevel_rate_table_get($t{dst},$t{rate_table_for_dst});
			if ($hash{ok_to_use} ne 1) {
			    $t{dst_error} 			= 1;
			    $t{dst_error_no_rate} 	= 1;
			}
		}
	    # Se dst ta ok flag ele
		if ($t{dst_error} eq 0) {
		    $t{dst_ok} = 1;
		    $t{dst_E164} = $t{dst};
		    $t{dst} = &format_E164_number($t{dst},"USA");
		}
    }
	#
	#============================================
	# re-check coupon: no coupon if multiple DST
	#============================================
	if ( ($t{dst_ok} eq 1) && ($t{coupon_in_stock} eq 1)  ) {
		$sql = "
		SELECT 1,1,count(*) FROM calls 
		where dst='$t{dst_E164}' and date>date_sub(now(), interval 90 day) and value>0 
		";
		%hash = database_select_as_hash($sql,"flag,qtd");
		unless ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd} < 30) ) {
			$t{coupon_error}			= 1;
			$t{coupon_error_dst_locked}	= 1;
		}
	}
    #
	#============================================
    # pega o signin caso tenha ani
	#============================================
	$t{signin_found} 			= 0;
	$t{signin_pin_found} 		= 0;
	$t{signin_ok} 				= 0;
    if ( ($t{ani_ok} eq 1) && ($t{ani_E164} ne "") ) {
		$sql = "
		SELECT 1,1,id,dst,pin
		FROM service_signin
		where ani='$t{ani_E164}' and service_id is null
		order by date_start desc limit 0,1
		";
		%hash = database_select_as_hash($sql,"flag,id,dst,pin");
		if ($hash{1}{flag} eq 1) {
			$t{signin_found}= 1;
			$t{signin_id} 	= $hash{1}{id};
			$t{signin_ani} 	= $t{ani_E164};
			$t{signin_dst} 	= $hash{1}{dst};
			$t{signin_pin} 	= $hash{1}{pin};
			$t{signin_ok} 	= 1;
		}
	}
    #
	#============================================
    # pega o servico caso tenha ani e signin 
	#============================================
	$t{service_found} 				= 0;
    if ( ($t{ani_ok} eq 1) && ($t{ani_E164} ne "") ) {
		$sql = "
		select 1,1,service.id,service.name,service.email
		from service,service_ani
		where service.id = service_ani.service_id and service_ani.ani='$t{ani_E164}'
		";
		%hash = database_select_as_hash($sql,"flag,id,name,email");
		if ($hash{1}{flag} eq 1) {
			$t{service_found} 	= 1;
			$t{service_id} 		= $hash{1}{id};
			$t{service_name} 	= $hash{1}{name};
			$t{service_email} 	= $hash{1}{email};
		}
    }
	
				
    #
	#============================================
    # check pin
	#============================================
	$t{pin} 		= substr($form{pin},0,100);
	$t{aniName}		= clean_str(substr($form{aniName}, 0, 100));
	$t{aniEmail} 	= clean_str(substr($form{aniEmail},0,100),"+.()-=[]?><#\@");
	
    #
	#============================================
    # check term
	#============================================
	$t{terms} = ($form{terms} eq 1) ? 1 : 0;
    #
	#============================================
    # check accept coupon error
	#============================================
	$t{coupon_error_accepted} = ($form{coupon_error_accepted} eq 1) ? 1 : 0;
    #
	#============================================
    # action
	#============================================
    $t{mode} = "unknown";
    if ($t{invite_ok} ne 1) {    
    	#
	    # verifica se tem invite. Se nao tem para
    	$t{mode} = "no_invite";
    	#
    } elsif ($t{service_found} eq 1) {    
    	#
    	# se tem servico com esse ani, avisar ele tem que login
    	$t{mode} = "ani_in_use";
    	#
    } else {
		if ($t{signin_ok} eq 0){
			# 
			# nao tem sign in, ja sei eh step 1
			$t{mode} = "signin_step_1";
			#
			# extra errors
			
			if ($t{ani}.$t{dst} ne "") {
				if ( ($t{ani_error} eq 0) && ($t{ani} eq "") )  { $t{error_string} = "ANI is Empty";$t{ani_error}=1; $t{ani_error_empty}=1; }
				if ( ($t{dst_error} eq 0) && ($t{dst} eq "") )  { $t{dst_error}=1; $t{dst_error_empty}=1; }
				####################################################
				#  since we are sign in ,the ani should be mobile
				####################################################
				if ( 0 && $t{ani_provider_is_mobile} ne 1 ) {
					$t{error_string} = "ANI Provider is not mobile";
					$t{ani_error}	= 1;
					$t{form_error_ani_needmobile}	= 1;
 					warning('not a mobile'.$t{ani});
				}   
				if ($t{ani_error} eq 1) {
				    $t{form_error} 				= 1;
				    $t{form_error_ani_empty} 	= $t{ani_error_empty};
				    $t{form_error_ani_format} 	= $t{ani_error_format};
				    $t{form_error_ani_no_rate}	= $t{ani_error_no_rate};
		    		$t{form_error_ani_in_use}	= $t{ani_error_in_use};
		    		$t{form_error_ani_locked}	= $t{ani_error_locked};
				}
				if ($t{dst_error} eq 1) {
				    $t{form_error} 				= 1;
				    $t{form_error_dst_empty} 	= $t{dst_error_empty};
				    $t{form_error_dst_format} 	= $t{dst_error_format};
				    $t{form_error_dst_no_rate}	= $t{dst_error_no_rate};
	    			$t{form_error_dst_locked}	= $t{dst_error_locked};
				}
				if ( $t{terms} ne 1)  {
					$t{form_error} = 1;
					$t{form_error_terms}	= 1;
				}
				
			}
			
			if ( ($t{coupon_error} eq 1) && ($t{coupon_in_stock} eq 1) ) {
				if ($t{coupon_error_accepted} eq 0) {
					$t{form_error} = 1;
					$t{form_error_coupon_error_accepted} = 1;
				}
			}
			#
			# seguindo o que tem que se fazer
		    if ( ($t{form_error} ne 1) &&  ($t{ani_ok} eq 1) && ($t{dst_ok} eq 1) ) {
		    	#
		    	###################################################
		    	# criar sign-in - START
		    	###################################################
		    	#
		    	# criando sign-in
				$t{signin_pin} = &multilevel_pin_generate();
				if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
				if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
				if ($t{signin_pin} eq "")  {
					# erro criando pin
					$t{form_error}	= 1;
					$t{form_error_system}	= 1;
				} else {
					$sql = " 
					insert into service_signin  
					(date_start,  date_last_change,  ani,             dst,           pin               ) values 
					(now(),       now(),             '$t{ani_E164}', '$t{dst_E164}', '$t{signin_pin}'  ) 
					";
					$t{signin_id} = database_do_insert($sql);
					
				
					if ($t{signin_id} eq "") {
						# erro criando signin
						$t{form_error}	= 1;
						$t{form_error_system}	= 1;
					} else {
						&action_history("status:signin:new",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=>$t{signin_pin}));
						&database_do("update service_pin set signin_id='$t{signin_id}' where pin='$t{signin_pin}' ");
						$t{mode} = "signin_step_2";
						$t{debug} .= "ENVIANDO PIN<br>";	
								    	
						# send pin, we only send last 4 digits of the pin (trac ticket #40)
						$confirmcode = substr($t{signin_pin},-4,4) ;
						if($makecall eq "yes"){
							&dial_and_play_code($t{ani_E164}, $confirmcode );
						}
						$t{pin_send}		= 1;
						&action_history("status:signin:pin:did",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=>$confirmcode));
					}
				}
				#
		    	###################################################
		    	# criar sign-in - STOP
		    	###################################################
		    	#
		    }
		} 
		if(1){
			# 
			# ja tem sign in, entao eh step 2
			$t{mode} = "signin_step_2";
			#
			# confere se PIN_DID ainda existe e recria se necessario
			$sql = "select 1,1 from service_pin where pin='$t{signin_pin}' and service_id is null and signin_id='$t{signin_id}' and free=1 ";
			%hash = database_select_as_hash($sql,"flag,pin");
			if ($hash{1}{flag} ne 1) {
				$t{signin_pin} = &multilevel_pin_generate();
				if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
				if ($t{signin_pin} eq "") {$t{signin_pin} = &multilevel_pin_generate();}
				&database_do("update service_pin set signin_id='$t{signin_id}' where pin='$t{signin_pin}' ");
			}
			#
			# update dst se necessario
			if ($t{dst_E164} eq "") {
				$t{dst_E164} = $t{signin_dst};
				$t{dst} = &format_E164_number($t{signin_dst},"E164");
			} else {
				if ($t{dst_ok} eq 1){
					&database_do(" update service_signin set dst='$t{dst_E164}' where id='$t{signin_id}' ");
				}				
			}
			#
			# extra errors
			if ( ($t{ani_error} eq 0) && ($t{ani} eq "") )  {$t{error_string} = "ANI is Empty Error"; $t{ani_error}=1; $t{ani_error_empty}=1; }
			if ( ($t{dst_error} eq 0) && ($t{dst} eq "") )  { $t{dst_error}=1; $t{dst_error_empty}=1; }
			if ($t{ani_error} eq 1) {
			    $t{form_error} 				= 1;
			    $t{form_error_ani_empty} 	= $t{ani_error_empty};
			    $t{form_error_ani_format} 	= $t{ani_error_format};
			    $t{form_error_ani_no_rate}	= $t{ani_error_no_rate};
	    		$t{form_error_ani_in_use}	= $t{ani_error_in_use};
	    		$t{form_error_ani_locked}	= $t{ani_error_locked};
			}
			if ($t{dst_error} eq 1) {
			    $t{form_error} 				= 1;
			    $t{form_error_dst_empty} 	= $t{dst_error_empty};
			    $t{form_error_dst_format} 	= $t{dst_error_format};
			    $t{form_error_dst_no_rate}	= $t{dst_error_no_rate};
    			$t{form_error_dst_locked}	= $t{dst_error_locked};
			}
			#if ( ($t{coupon_error} eq 1) && ($t{coupon_in_stock} eq 1) ) {
			#	if ($t{coupon_error_accepted} eq 0) {
			#		$t{form_error} = 1;
			#		$t{form_error_coupon_error_accepted} = 1;
			#	}
			#}
			#
			# so executa as acoues e nao tem erro
			if ($t{form_error} ne 1) {
				# 
				# re-enviar PIN 
				if ($form{re_send_pin} eq 1) {
					# send pin, we only send last 4 digits of the pin (ticket #40)
					$confirmcode = substr($t{signin_pin},-4,4) ;						
					&dial_and_play_code($t{ani_E164}, $confirmcode );
					$t{pin_send} = 1;
					&action_history("status:signin:pin:did",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=>$confirmcode));
				}
				#
				# verificar user input pin
				$t{pin} = substr($t{signin_pin},-4,4);
				if ($t{pin} ne "") {
					if (&clean_int(substr($t{pin},0,100)) ne substr($t{signin_pin},-4,4)) {
						#
						# se pin ta errado, informar o erro
						$t{form_error}		= 1;
						$t{form_error_pin}	= 1;
					}else {
						$t{pin_ok} = 1;
						$confirmcode = substr($t{signin_pin},-4,4) ;
						&action_history("status:signin:pin:did:ok",('signin_id'=>$t{signin_id},'value_old'=>$t{ani_E164},'value_new'=> $confirmcode));
						#
				    	###################################################
				    	# criar SERVICE - START
				    	###################################################
				    	#
						#
						# criar servico (default status=new)
						$sql  = "
							insert into service 
							(product_id,  status, 					name, 				email, 		 creation_date,  last_change  ) values 
							('1',         '$t{invite_signin_status}',  '$t{aniName}', '$t{aniEmail}', now(),          now()        ) 
						";
						$t{service_id} 		= &database_do_insert($sql);
						
						
						%email = ();
						$email{to}				= $service_email;
						$email{template}		= "service.add";
						$email{dic}{pin}		= $t{signin_pin};
						$email{dic}{email}		= $service_email;
						&multilevel_send_email(%email);
						&action_history("status:signin:pin:email:ok",('service_id'=>$service_id,,'value_old'=>$email{dic}{email},'value_new'=>$email{dic}{pin}));

				
						
						#
						# se ok, terminar o trabalho e login
						if ($t{service_id} ne "") {
							#
							# add on tree
							$sql  = " 
							insert into service_tree 
							(service_id,        parent_service_id        )  values 
							('$t{service_id}',  '$t{invite_service_id}'  ) 
							";
							database_do($sql);
							&data_set("service_data",$t{invite_service_id},"last_friend_time",time);
							#
							# update pin
							&database_do("update service_pin set service_id='$t{service_id}' where pin='$t{signin_pin}' ");
							#
							# update signin
							&database_do("update service_signin set service_id='$t{service_id}' where id='$t{signin_id}' ");
							#
							# update action_log 
							&database_do("update action_log set service_id='$t{service_id}' where signin_id='$t{signin_id}' and service_id is null ");
							#
							# criar invite
							$tmp= &multilevel_invite_create($t{service_id});
							#
							# adicionar primeiro ANI
							&data_set("service_data",$t{service_id},"ani_1_number"		,$t{ani_E164});
							&data_set("service_data",$t{service_id},"ani_1_provider"	,$t{form_provider});
							&multilevel_anicheck_touch($t{service_id},$t{dst_E164});
							&database_do("insert into service_ani (ani,service_id) values ('$t{ani_E164}', '$t{service_id}') ");
							#
							# adicionar primeiro DST
							&data_set("service_data",$t{service_id},"dst_1_number"	,$t{dst_E164});
							&data_set("service_data",$t{service_id},"dst_1_name"	,$t{dstName});
							&data_set("service_data",$t{service_id},"dst_1_rslot"	,1);
							#
							# adicionar defaults
							&data_set("service_data",$t{service_id},"trigger_nf",1);
							&data_set("service_data",$t{service_id},"trigger_nfof",1);
							&data_set("service_data",$t{service_id},"trigger_nc",1);
							&data_set("service_data",$t{service_id},"trigger_ec",1);
							&data_set("service_data",$t{service_id},"trigger_lb",1);
							&data_set("service_data",$t{service_id},"email_news",1);
							#
							# adicionar coupon se possivel
							if ( ($t{coupon_type_id} ne "") && ($t{coupon_in_stock} eq 1) && ($t{coupon_exists} eq 1) && ($t{coupon_error} ne 1) ) {
								# tenta add coupon
								%coupon = ();
								$coupon{service_id}		= $t{service_id};
								$coupon{coupon_type_id}	= $t{coupon_type_id};
								%coupon = &multilevel_coupon_assign(%coupon);
								if ($coupon{ok} eq 1) {
									if (&multilevel_coupon_next_slice($coupon{coupon_stock_id})>0){
										$t{coupon_assigned}	= 1;
									}
								}
							}
							#
							# delete request code
							&database_do("update service_signin set date_last_change=now(), date_stop=now() where id='$t{signin_id}' ");
							#
							# apply commission
							#%commission_data = ();
							#$commission_data{service_id}				= $t{invite_service_id};
							#$commission_data{from_service_id}			= $t{service_id};
							#$commission_data{commission_type_engine} 	= "REFERRAL_SIGNIN";
							#%commission_data = &multilevel_commission_new(%commission_data);
							#
							# email parent tree sobre new friend
							$notification_service_id = $t{invite_service_id};
							foreach $notification_proximity_level (0..20) {
								next;
								%tmp_hash = database_select_as_hash("select 1,1,name,email from service where service.id='$notification_service_id' ","flag,name,email");
								if ($tmp_hash{1}{flag} eq 1) {
									$notification_service_email	= $tmp_hash{1}{email};
									$notification_flag_type 	= ($notification_proximity_level eq 0) ? "trigger_nf" : "trigger_nfof";
									$notification_flag 			= &data_get("service_data",$notification_service_id,$notification_flag_type);
									if ( ($notification_flag eq 1) && ($notification_service_email ne "") ){
										%email = ();
										$email{template}					= ($notification_proximity_level eq 0) ? "alert.new.friend" : "alert.new.friend.of.friend";
										$email{to}							= $notification_service_email;
										$email{dic}{invite_branch_distance}	= "you";
										$email{dic}{invite_branch_distance}	= ($notification_proximity_level eq 1) ? "your friend" : $email{dic}{invite_branch_distance};
										$email{dic}{invite_branch_distance}	= ($notification_proximity_level eq 2) ? "one person away" : $email{dic}{invite_branch_distance};
										$email{dic}{invite_branch_distance}	= ($notification_proximity_level > 2) ? ($notification_proximity_level-1)." people away" : $email{dic}{invite_branch_distance};
										&multilevel_send_email(%email);
									}
								}
								%tmp_hash = database_select_as_hash("select 1,1,parent_service_id from service_tree where service_id='$notification_service_id'","flag,value");
								if ( ($tmp_hash{1}{flag} eq 1) && ($tmp_hash{1}{value} ne "") ) {
									$notification_service_id = $tmp_hash{1}{value};
								} else {
									last;
								}
							}
							
							#send New friend joined message to referrer
							
							#my $referral_number=&data_get("service_data",$t{invite_service_id},"ani_1_number");							
							
							
							#my %hash = database_select_as_hash("SELECT 1,1,msg_type,msg_text FROM sms_customtext","1,msg_type,msg_text");
							#my $joinmessage = $hash{1}{msg_text};
										
							#$joinmessage =~ s/xxxx/$t{ani}/i;
							
							#&sendSMS_Twilio($referral_number,$joinmessage);
							#
							# log-in
							session_attach($t{service_id});
							#&session_set($app{session_cookie_k},"service_alert"	,"emailquestion");
							&session_set($app{session_cookie_k},"flag_first_login"	,1);
							&active_session_set("service_name",$t{aniName});
							&active_session_set("service_email",$t{aniEmail});
							&session_set($app{session_cookie_k},"service_email",$t{aniEmail});
							&session_set($app{session_cookie_k},"service_name",$t{aniName});
							&session_set($app{session_cookie_k},"service_alert"	,"");
							#
							# log action
							&action_history("status:new",('signin_id'=>$t{signin_id},'service_id'=>$t{service_id},'value_old'=>$t{ani_E164}));
							#
							# mostrar dados
							$t{mode} = "add_ok";
							#
						} else {
							$t{form_error}			= 1;
							$t{form_error_system}	= 1;
						}
						#
				    	###################################################
				    	# criar SERVICE - STOP
				    	###################################################
				    	#
					}
				}
			}
		}
    }
    #
	#============================================
    # preare page
	#============================================
    $t{"mode_".$t{mode}} = 1;
    $t{"my_url"} = $my_url;
    $t{signin_pin_formated} = &format_pin($t{signin_pin});
    $t{form_error} = ( ($t{ani_error} eq 1) || ($t{dst_error} eq 1) || ($t{form_pin_error} eq 1) ) ? 1 : $t{form_error};
	#$tmp=""; foreach(sort keys %t) {if ($_ eq "debug") {next} $tmp .= "$_=$t{$_}<br>";}$t{debug} .= $tmp;
	return %t;
    &template_print("template.pbx.add.html",%t);
}
