#!/usr/bin/perl
#
# TODO: what is this code? just a test? can we delete to avoid this code reach production servers and expose bussines data?
#
# let me disable until we learn why

#return 1;#---------------------why return? if return ,it will can't load session,kevin2012.1.1 


################################################################################
#
# global libs for AGI, perl scripts and CGI
# extra libs for multilevel services
# developed for years to zenofon
#
################################################################################
$|=1;$!=1; # disable buffer

use LWP::Simple;
require "include.cgi";

$user = "neyfrota"; #"zweixiang";
$pass = "dt1014gb" ;#"12345678";

sub lookup (){
	$ani = shift || return {};
	return {} unless length($ani) > 6;    #ignore invalid ani

	$ani =~ s/ //g;
	warn "lookup ani=$ani";
	#return;
	$ani    = "+$ani" unless $ani =~ /^\+/;
	%h		= database_select_as_hash("SELECT 1, ani,carrierid,carriername,iswireless,countrycode,name,lasteditname FROM ani_lookup " .
									  " WHERE ani='$ani'", 'ani,carrierid,carriername,iswireless,countrycode,name,lasteditname');

	return {ani => $h{1}{ani}, carrierid => $h{1}{carrierid}, carriername => $h{1}{carriername}, isindb => 1,
			iswireless => $h{1}{iswireless}, countrycode => $h{1}{countrycode},
			name => $h{1}{lasteditname} || $h{1}{name}} if $h{1}{ani};

	$xml	= _get ("https://api.data24-7.com/carrier.php?username=$user&password=$pass&p1=$ani");
	warn "carrier: $xml";
	$carrierid		= getvalue('carrier_id', $xml);
	$carriername	= database_clean_string(getvalue('carrier_name', $xml));
	$iswireless		= getvalue('wless', $xml);
	$countrycode	= database_clean_string(getvalue('country', $xml));
	$balance		= getvalue('balance', $xml);

	warn "balance: $balance";
	$xml	= '';
	#name service is only for phone number of USA
	if ($ani =~ /^(?:|\+)1/) {
		$xml = _get ("https://api.data24-7.com/id.php?username=$user&password=$pass&&p1=$ani");
	}
	warn "id: $xml";
	$name			= database_clean_string(getvalue('name', $xml));

	return {} unless $balance > 0;

	$sql = "INSERT into ani_lookup (ani,carrierid,carriername,iswireless,countrycode,name) VALUES ".
			"('$ani', '$carrierid', '$carriername', '$iswireless', '$countrycode', '$name')";

	warn $sql;
	database_do_insert($sql);

	return {ani => $ani, 'carrierid' => $carrierid, 'carriername' => $carriername, 'iswireless' => $iswireless,
			countrycode => $countrycode, name => $name};

}

sub _get {
	my $url = shift;
	warn "get $url";
	return get($url);
}

sub getvalue () {
	($key, $xml) = @_;
	return '' unless $key && $xml;
	#warn "try to getvalue for $key from $xml";
	my($value) =  $xml =~ m{<$key>(.*?)</$key>}s;
	return defined $value ? $value : '';
}
