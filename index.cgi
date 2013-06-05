#!/usr/bin/perl
require "include.cgi";

#commit by yang

#=======================================================
# clear cookie se necessario
#=======================================================
if ($form{delete_invite_cookie} eq 1) {
    &cookie_save("i","","expires=Sun, 26-Jun-2011 00:00:00 GMT;");
    print "content-type: text/html\n\n"; 
    print qq[
    <html><head>
    <META HTTP-EQUIV="Expires" CONTENT="0">
    <META HTTP-EQUIV="Cache-Control" CONTENT="no-cache, must-revalidate">
    <META HTTP-EQUIV="Pragma" CONTENT="no-cache">
    <META HTTP-EQUIV="Refresh" CONTENT="0;URL=/">
    </head><body><script>window.location='/'</script></body></html>	
    ];
    exit;
}
#=======================================================




#=======================================================
# do the magic
#=======================================================
%t = ();
#
#--------------------------------
# get invite
#--------------------------------
%invite = ();
$invite{ok} = 0;
$buf = $ENV{REQUEST_URI};
$refcode=$form{referal};

$t{dic}{referal_code}="";
$t{dic}{referal_default}="soup";


if( $refcode eq ""  )

{
  $t{dic}{referal_error}=0; 
  $t{dic}{referal_code}=""; 
}
else
{
  $t{dic}{referal_error}=1; 
  $t{dic}{referal_code}=$refcode; 
  
}



$invite{no_invite}=1;


if( ($buf eq "/"  ) ||  ( $buf eq ""  ) )  { $buf = "soup" ; $invite{no_invite} = 1;};
if ( ($buf ne "") && (index($buf,"=") eq -1) && (index($buf,"&") eq -1) ) {
	#
	# tentar pegar invite pela url
	warning($buf);
	$buf = (index($buf,"?") ne -1) ? substr($buf,index($buf,"?")+1,100) : $buf;
	warning("2:".$buf);
	$buf = (index($buf,"=") ne -1) ? substr($buf,0,index($buf,"=")) : $buf;
	   warning("3:".$buf);
	$buf = (index($buf,"&") ne -1) ? substr($buf,0,index($buf,"&")) : $buf;
   warning("5:".$buf);
	$buf = (length($buf) < 5) ? "" : $buf;
	$buf = (length($buf) > 10) ? "" : $buf;
	if ($buf ne "") {

     if( $buf ne "soup" )  { $invite{no_invite} = 0};
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
		if ($hash{1}{flag} eq 1) 
		                {
			$invite{ok}				= 1;
			$invite{id}				= $buf;
			$invite{service_name}	= $hash{1}{name};
			$invite{service_id}		= $hash{1}{id};
			$invite{service_referral_status}= $hash{1}{referral_status};
			&cookie_save("i",$invite{id},"expires=Thu, 31-Dec-2020 00:00:00 GMT;");
		} 
	}
}
if ($invite{ok} eq 0) {
	#
	# se nao veio por url, tentar por cookie
	$buf = $cookie{"i"};
	$buf = ($buf eq "") && ($form{invite} ne "") ? $form{invite} : $buf;
	$buf = clean_str(substr($buf,0,100),"MINIMAL");
	$buf = (length($buf) < 5) ? "" : $buf;
	$buf = (length($buf) > 20) ? "" : $buf;
    if( $buf eq "soup" )  { $invite{no_invite} = 1; }
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
			$invite{service_name}	= $hash{1}{name};
			$invite{service_id}		= $hash{1}{id};
			$invite{service_referral_status}= $hash{1}{referral_status};
			&cookie_save("i",$invite{id},"expires=Thu, 31-Dec-2020 00:00:00 GMT;");
		}
	}
}
#
#--------------------------------
# get coupon
#--------------------------------
%coupon = ();
$coupon{exists}		= 0;
$coupon{in_stock}	= 0;
$coupon{stock_qtd}	= 0;
$coupon{assigned}	= 0;
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
#
#--------------------------------
# print page
#--------------------------------
$t{dic}{my_url} = "index.cgi";
$t{dic}{coupon_exists}			= $coupon{exists};
$t{dic}{coupon_in_stock}		= $coupon{in_stock};
$t{dic}{coupon_stock_qtd}		= &format_number($coupon{stock_qtd},0);
$t{dic}{coupon_type_id}			= $coupon{type_id};
$t{dic}{coupon_title}			= $coupon{title};
$t{dic}{coupon_msg_in_stock}	= $coupon{msg_in_stock};
$t{dic}{coupon_msg_out_stock}	= $coupon{msg_out_stock};
$t{dic}{coupon_msg_assigned}	= $coupon{msg_assigned};
$t{dic}{invite_ok} 				= $invite{ok};
$t{dic}{invite_id} 				= $invite{id};
$t{dic}{invite_service_id} 		= $invite{service_id};
$t{dic}{invite_service_name} 	= $invite{service_name};
$t{dic}{no_invite_service}          = $invite{no_invite};
&template_print("template.services.html",%t);
exit;
#=======================================================



