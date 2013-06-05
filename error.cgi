#!/usr/bin/perl
#-------------------------------------------------------
# We cannot use default include here.
# if we do, and default include is wrong, even error pages at website will be broken
# error page need survive without dependences
#-------------------------------------------------------
use HTML::Template;
use Text::ParseWords;
use DBI;
$database 							= null;
$conection 							= null;
$database_connected					= 0;
$database_last_error				= "";
$database_dsn						= "dbi:mysql:multilevel:127.0.0.1";
$database_user						= "multilevel";
$database_password					= "multilevel";
$template_folder= "/usr/local/multilevel/www/design/";
#-------------------------------------------------------


#-------------------------------------------------------
# oops.. its ney :) let me detail
#-------------------------------------------------------
if ( ($ENV{REMOTE_ADDR} eq "127.0.0.1") && ($ENV{REDIRECT_STATUS} ne "404"))  {
	cgi_hearder_html();
	print "<font face=verdana,arial size=2>";
	print "<font size=6><b>Error $ENV{REDIRECT_STATUS}<br>$ENV{REDIRECT_ERROR_NOTES}</b></font><br>";
	open(IN, "tail -n 20 /var/log/apache2/error.log |");
	@buf = (<IN>);
	@buf = reverse(@buf);
	$display_date = "";
	foreach(@buf){
		chomp;
		$date = substr($_,1,24); 
		$msg = substr($_,54,1000); 
		if ($display_date ne $date) {print "<BR><BR><b>$date</b><hr size=1 noshade color=#c0c0c0>"}
		print "$msg<br>";
		$display_date = $date;
	}
	print "<br><br><br><b>ENV dump</b><hr size=1 noshade color=#c0c0c0>";
	foreach(sort keys %ENV) {print "ENV $_ = $ENV{$_}<br>";}
	exit;
}
#-------------------------------------------------------



#-------------------------------------------------------
# verifica se o erro e um invite
#-------------------------------------------------------
$buf = &clean_str(substr($ENV{REQUEST_URI},0,100),"-_","MINIMAL");
$sql = "select 1,1 from service_invite where service_invite.free = 0 and service_invite.id = '$buf' ";
%hash = &database_select_as_hash($sql,"flag");
if ($hash{1}{flag} eq 1) {
	#
	#--------------------------------
	# get invite
	#--------------------------------
	%invite = ();
	$invite{ok} = 0;
	$invite{id} = "";
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
	%hash = &database_select_as_hash($sql,"flag,id,name,referral_status");
	if ($hash{1}{flag} eq 1) {
		$invite{id}						= $buf;
		$invite{ok}						= 1;
		$invite{service_name}			= $hash{1}{name};
		$invite{service_id}				= $hash{1}{id};
		$invite{service_referral_status}= $hash{1}{referral_status};
		&cookie_save("i",$invite{id},"expires=Thu, 31-Dec-2020 00:00:00 GMT;");
	} 
	#
	#--------------------------------
	# get coupon
	#--------------------------------
	%coupon = ();
	$coupon{ok}			= 0;
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
		%hash = &database_select_as_hash($sql,"flag,id,title,msg_in_stock,msg_out_stock,msg_assigned");
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
			%hash = &database_select_as_hash($sql,"flag,value");
			if ($hash{1}{flag} eq 1) {
				$coupon{in_stock}	= ($hash{1}{value}>0) ? 1 : 0;
				$coupon{stock_qtd}	= $hash{1}{value};
			}
		}
	}
	$t{dic}{coupon_exists}			= $coupon{exists};
	$t{dic}{coupon_in_stock}		= $coupon{in_stock};
	$t{dic}{coupon_stock_qtd}		= $coupon{stock_qtd};
	$t{dic}{coupon_type_id}			= $coupon{type_id};
	$t{dic}{coupon_title}			= $coupon{title};
	$t{dic}{coupon_msg_in_stock}	= $coupon{msg_in_stock};
	$t{dic}{coupon_msg_out_stock}	= $coupon{msg_out_stock};
	$t{dic}{coupon_msg_assigned}	= $coupon{msg_assigned};
	$t{dic}{invite_ok} 				= $invite{ok};
	$t{dic}{invite_id} 				= $invite{id};
	$t{dic}{invite_service_id} 		= $invite{service_id};
	$t{dic}{invite_service_name} 	= $invite{service_name};
	$t{dic}{my_url} 				= "index.cgi";
	&template_print("template.services.html",%t);
	exit;
}
#-------------------------------------------------------




#-------------------------------------------------------
# infelizmente e um erro
#-------------------------------------------------------
%t = ();
$t{dic}{title} = "Im sorry";
$t{dic}{info} = "We detect one error.";
$t{dic}{content} = qq[
	<div class=clear style="padding:50px;>
	<img src=/design/icons/error.png hspace=0 vspace=0 border=0 align=left style="margin-right:5px;">
	<h2>We detect one error code $ENV{REDIRECT_STATUS}</h2><br>
	<br>
	You can 
	<a href=javascript:history.reload()>retry</a>, 
	<a href=javascript:history.back()>return</a> or
	<a href=/>restart</a><br>
	</div>
];
template_print("template.html",%t);
exit;
#-------------------------------------------------------





#-------------------------------------------------------
# my lib
#-------------------------------------------------------
sub template_print(){
    my ($template_file,%template_data) = @_;
    my ($buf,$n,$tmp1,$tmp2,%hash);
    $template_file = $template_folder.$template_file;
    unless(-e $template_file) {print "Content-type: text/html\n\nNo file $template_file\n";return}
    my $template = HTML::Template->new(filename => $template_file, die_on_bad_params=>0, strict=>0, vanguard_compatibility_mode=>1);
    foreach(sort keys %{$template_data{dic}}) {
	$template->param($_ => $template_data{dic}{$_} );
    }
    &cgi_hearder_html();
    print $template->output();
}
sub cgi_hearder_html {
    print "Content-type: text/html\n";
    print "Cache-Control: no-cache, must-revalidate\n";
    print "Pragma: no-cache\n";
    print "status: 200\n";
    print "\n";
}
sub clean_str() {
  #limpa tudo que nao for letras e numeros
  local ($old)=@_;
  local ($new,$i);
  $old=$old."";
  $new="";
  $caracterok="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890";
  for ($i=0;$i<length($old);$i++) {if (index($caracterok,substr($old,$i,1))>-1) {$new=$new.substr($old,$i,1);} }
  return $new;
}
sub database_connect(){
	if ($database_connected eq 0) {
		$database = DBI->connect($database_dsn, $database_user, $database_password); 
		$database_connected = 1;
	}
}
sub database_select(){
	if ($database_connected ne 1) {database_connect()}
	local ($sql)=@_;
	local (@rows,$connection,%output,$row,$col);
	if ($database_connected eq 1) {
		$connection = $database->prepare($sql);
		$connection->execute;
		$row=0;
		while ( @rows = $connection->fetchrow_array(  ) ) {
			$col=0;
			foreach (@rows){
				$output{DATA}{$row}{$col}= &database_scientific_to_decimal($_);
				$col++;
			}
			$row++;
		}
		$output{ROWS}=$row;
		$output{COLS}=$col;
		$output{OK}=1;
	} else {
		$output{ROWS}=0;
		$output{COLS}=0;
		$output{OK}=0;
	}
	return %output;
}
sub database_select_as_hash(){
	if ($database_connected ne 1) {database_connect()}
	local ($sql,$rows_string)=@_;
	local (@rows,@rows_name,$i,%output);
	@rows_name = split(/\,/,$rows_string);
	if ($database_connected eq 1) {
		$connection = $database->prepare($sql);
		$connection->execute;
		while ( @rows = $connection->fetchrow_array(  ) ) {
			if ($rows_string eq "") {
				$output{(@rows)[0]}=(@rows)[1];
			} else {
				$i=0;
				foreach (@rows_name) {
					##$output{(@rows)[0]}{$_} = &database_scientific_to_decimal((@rows)[$i+1]);
					$output{(@rows)[0]}{$_} = (@rows)[$i+1];
					$i++;
				}
			}
		}
	}
	return %output;
}
sub database_select_as_hash_with_auto_key(){
	if ($database_connected ne 1) {database_connect()}
	local ($sql,$rows_string)=@_;
	local (@rows,@rows_name,$i,%output,$line_id);
	@rows_name = split(/\,/,$rows_string);
	if ($database_connected eq 1) {
		$connection = $database->prepare($sql);
		$connection->execute;
		$line_id = 0;
		while ( @rows = $connection->fetchrow_array(  ) ) {
			$i=0;
			foreach (@rows_name) {
				$output{$line_id}{$_} = &database_scientific_to_decimal((@rows)[$i]);
				$i++;
			}
			$line_id++;
		}
	}
	return %output;
}
sub database_select_as_array(){
	if ($database_connected ne 1) {database_connect()}
	local ($sql,$rows_string)=@_;
	local (@rows,@rows_name,$i,@output);
	@rows_name = split(/\,/,$rows_string);
	if ($database_connected eq 1) {
		$connection = $database->prepare($sql);
		$connection->execute;
		while ( @rows = $connection->fetchrow_array(  ) ) {
			@output = ( @output , &database_scientific_to_decimal((@rows)[0]) );
		}
	}
	return @output;
}
sub database_do(){
	if ($database_connected ne 1) {database_connect()}
	local ($sql)=@_;
	local ($output);
	$output = "";
	if ($database_connected eq 1) {	$output = $database->do($sql) }
	if ($output eq "") {$output =-1;}
	return $output;
}
sub database_scientific_to_decimal(){
	local($out)=@_;
	local($tmp1,$tmp2);
	if ( index("\U$out","E-") ne -1) {
		($tmp1,$tmp2) = split("E-","\U$out");
 		$tmp1++;
		$tmp2++;
		$tmp1--;
		$tmp2--;
		if (  (&is_numeric($tmp1) eq 1) && (&is_numeric($tmp2) eq 1)  )  {
			$out=sprintf("%f",$out);
		} 
	}
	if ( index("\U$out","E+") ne -1) {
		($tmp1,$tmp2) = split("E","\U$out");
		$tmp2 = substr($tmp2,1,10);
		$tmp1++;
		$tmp2++;
		$tmp1--;
		$tmp2--;
		if (  (&is_numeric($tmp1) eq 1) && (&is_numeric($tmp2) eq 1)  )  {
			$out=int(sprintf("%f",$out));
		}
	}
	return $out;
}
sub database_escape {
	my $string = @_[0];
	$string =~ s/\\/\\\\/g ; # first escape all backslashes or they disappear
	$string =~ s/\n/\\n/g ; # escape new line chars
	$string =~ s/\r//g ; # escape carriage returns
	$string =~ s/\'/\\\'/g; # escape single quotes
	$string =~ s/\"/\\\"/g; # escape double quotes
	return $string ;
}
sub cookie_save($$) {
	local($name,$value,$flags)=@_;
	$flags = ($flags eq "") ? "" : "$flags;";
	print "Set-Cookie: ";
	print $name."=".$value."; path=/; $flags  \n";
	#print $name."=".$value."; path=/; $flags expires=Sun, 26-Jun-2011 00:00:00 GMT; \n";
	#print $name."=".$value."; path=/; $flags expires=Sun, 26-Jun-2011 00:00:00 GMT; domain=$ENV{SERVER_NAME};\n";
	#print ($name,"=",$value,"; path=/; \n");
}
sub cookie_read{
	local(@rawCookies) = split (/; /,$ENV{'HTTP_COOKIE'});
	local(%r);
	foreach(@rawCookies){
		($key, $val) = split (/=/,$_);
		$r{$key} = $val;
	} 
	return %r;
} 
#=======================================================



