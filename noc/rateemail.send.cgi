#!/usr/bin/perl
require "include.cgi";

if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_manage_services") ne 1) {adm_error("no permission"); exit;}

$my_url = "rateemail.send.cgi";
$action = $form{action};

if 		($action eq "logout")		{&do_logout();		}
elsif	($action eq "filter")		{&do_show_form();}
elsif 	($action eq "initSend")		{&do_send_emails();}
elsif 	($action eq "testEmail")	{&do_test_email();}
elsif	($action eq "simpleEmail") 	{&do_simple_email();}
else								{&do_show_form();}
exit;


sub do_test_email(){
	
	local (%t) = @_;
	$mincalls = $form{mincalls};
	$route = $form{route};
	$from = $form{fromemail};
	$test = $form{testemail};
	

	
	%data = ();
	$data{$test} = "Test";
	if($test ne ""){
	for $emailid (keys %data){
		$email = qq[
We've just changed our rates!

To view our new rates please visit us at http://www.zenofon.com/about/rate.cgi , and enter the phone number you want to call to see our new rates.

Thanks, ZenoFon.
		];
		#print $email . "\n\n";
		$t{dic}{content} .= "Email sent : $emailid <br>";
		%newEmail = ();
		$newEmail{from} = $from;
		$newEmail{subject} = "Zenofon rate update";
		$newEmail{to} = $emailid;
		$newEmail{template} = "rates.update";
		multilevel_send_email(%newEmail);
		#&send_email("support\@zenofon.com", $id, "Rate update at Zenofon", $email, 1);
	}
	}
	&template_print("template.html", %t);
	
}

sub do_simple_email(){
		#print "Content-type: text/plain\n";
	%t = ();
	$mincalls = $form{mincalls};
	$route = $form{route};
	$from = $form{fromemail};
	
	$sql = qq[
SELECT
s.email
FROM 
calls_log cl
join service s on s.id=cl.service_id
where datetime_start > DATE_SUB(NOW(), INTERVAL 2 month)
and length(s.email)>0
and s.email is not null
group by email
	];
	
	%hash = database_select_as_hash($sql);
	%data = ();
	%countries = ();
	for $id(keys %hash){
		$data{$id}{email} = $id;
	}
	
	for $emailid(keys %data){
		$t{dic}{content} .= "Email sent : $emailid <br>";
		%newEmail = ();
		$newEmail{from} = $from;
		$newEmail{subject} = "Zenofon rate Update";
		$newEmail{to} = $emailid;
		$newEmail{template} = "rates.update";
		multilevel_send_email(%newEmail);
		#&send_mail($from, $emailid, "Rate update at Zenofon", $email, 1);
	}
	&do_test_email(%t);
	#&template_print("template.html", %t);
	
}

sub do_send_emails(){
	#print "Content-type: text/plain\n";
	%t = ();
	$mincalls = $form{mincalls};
	$route = $form{route};
	$from = $form{fromemail};
	
	$sql = qq[
SELECT
concat(s.name, c.name),
s.name,
c.code,
s.email,
c.name
FROM 
calls_log cl
join country c on cl.dst like concat(c.code, '%')
join service s on s.id=cl.service_id
where datetime_start > DATE_SUB(NOW(), INTERVAL 2 month)
and length(s.name)>0
and s.email is not null
group by email, c.name
having count(c.name)>$mincalls
limit 20
	];
	
	%hash = database_select_as_hash($sql, "name,ccode,email,cname");
	%data = ();
	%countries = ();
	for $id(keys %hash){
		$data{$hash{$id}{name}}{country}{$hash{$id}{ccode}}++;
		$data{$hash{$id}{name}}{email} = $hash{$id}{email};
		#$countries{$hash{$id}{ccode}} = $hash{$id}{cname};
	}
	
	for $name(keys %data){
		$email = qq[
		Hello $name,
		
		Checkout the rates :
		
		Country : Rate per minute : Time in \$1
		
		];
		$countries = join(",", keys %{$data{$name}{country}});
		$sql = qq[
SELECT
prtd.country,
prtd.rate_per_minute
FROM 
product_rate_table_data prtd 
where prtd.rate_id=$route
and prtd.country in ($countries)
group by country
order by prtd.country
	];

		%hash = database_select_as_hash($sql, "rate");
		for $ccode(sort{$a cmp $b} keys %hash){
			$mins = &format_time( 60*($hash{$ccode}{rate}>0?1/$hash{$ccode}{rate}:0));
			$rate = &format_number($hash{$ccode}{rate},2);
			$email .= qq[
		$countries{$ccode} : $rate : $mins
		];
		}
		

		$t{dic}{content} .= "Email sent : $data{$name}{email} <br>";
		$t{dic}{content} .= "Email sent : $id <br>";
		%newEmail = ();
		$newEmail{from} = $from;
		$newEmail{subject} = "Zenofon rate update";
		$newEmail{to} = $id;
		$newEmail{template} = "rates.update";
		multilevel_send_email(%newEmail);
		
		#&send_mail($from, $data{$name}{email}, "Rate update at Zenofon", $email, 1);
	}
	do_test_email();
	#&template_print("template.html", %t);
	
}


sub do_show_form(){
	
	$mincalls = $form{mincalls};
	if(!$mincalls){
		$mincalls=0;
	}
	%t = ();
$t{dic}{scripts} = qq[
<script src="https://ajax.aspnetcdn.com/ajax/jquery.dataTables/1.9.1/jquery.dataTables.min.js"></script>

];


$sql = qq[
	select id, name from product_rate_table;
];
%hash = database_select_as_hash($sql, "name");
$select = qq[
	<select name=route>
];
for( sort{$hash{$a}{name} cmp $hash{$b}{name}} keys %hash){
	$select .= qq[
		<option value=$_>$hash{$_}{name}</option>
		
	];
}
$select .= "</select>";

$t{dic}{content} = qq[

<div id="tablehold">
<table id="datatable" border=1>
<thead>
<tr>
<th>Name</th>
<th>Email</th>
<th>Country</th>
<th>Call Count</th>
</tr>
</thead>
<tbody>
];
	
	$sql = qq[
SELECT
concat(s.name, c.name),
s.name,
c.name,
s.email,
count(c.name)
FROM 
calls_log cl
join country c on cl.dst like concat(c.code, '%')
join service s on s.id=cl.service_id
where datetime_start > DATE_SUB(NOW(), INTERVAL 2 month)
and length(s.name)>0
and email is not null
group by email, c.name
having count(c.name)>$mincalls
limit 20
	];
	%hash = database_select_as_hash($sql, "service,country,email,count");

	for $id(keys %hash){
		$t{dic}{content} .= qq[
			<tr>
				<td>$hash{$id}{service}</td>
				<td>$hash{$id}{email}</td>
				<td>$hash{$id}{country}</td>
				<td>$hash{$id}{count}</td>
			</tr>
		];
	}
	
	$t{dic}{content} .= qq[
	</tbody>
	</table>
	</div>
	<br>
	<script>
	\$(document).ready(function(){
    \$('#datatable').dataTable();
});
	</script>
<br><br>
		<form method=get>
		<!-- Minimum Call Count : <input type=text name=mincalls value=$mincalls><br>
		Route : $select <br> -->
		From : <input type=text name='fromemail' value='system\@zenofon.com'><br>
		Test Email : <input type=text name='testemail' value='parth\@zenofon.com'><br>
		<button name="action" value="filter">Filter</button>
		<button name="action" value="simpleEmail">Send Emails</button>
		<button name="action" value="testEmail">Send Test Email</button>
		</form>
	];
	&template_print("template.html", %t);
	return;
}

