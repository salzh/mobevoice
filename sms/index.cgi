#!/usr/bin/perl
print "Content-type: text/html\n\n";
require "/usr/local/multilevel/default.include.pl";
use CGI;
use DBI;
my %hash = database_select_as_hash("select 1,1,contents from cms_page where id = 1", "1,contents");
my $contents = $hash{1}{contents};

print qq[<html>
	
	<title>ZenoFon - SMS Help page</title>
    <head>
	<script	src="/design/template.js"	type="text/javascript" ></script>
	<link 	href="/design/template.css"	type="text/css" rel="stylesheet" />
	<script src="/design/jquery.min.js" type="text/javascript"></script>
    <style>
		#helptable {				
			
			border: 1px solid #cccccc;
			background: #FFFFFF;	
			border-collapse:collapse;
	
		}
		#helptable th{
			font: bold;        
			border-right: 1px solid #cccccc;			           
			text-align:center;
			padding: 8px 12px 4px 12px;     
			
        }
		#helptable td{   	
			font-size:14px;
			border: 1px solid #cccccc;			
			padding: 10px 12px 10px 12px;        
      
        }
		
	</style>
	</head>

<body>
	<div class=page>
		<div class=page-content>
			<div class=clear style="width:100%; height:127px; overflow:hidden; background-image:url(/design/img/page-top.png); background-repeat:no-repeat; text-align:left;">
			<a href=http://www.zenofon.com/ Title=ZenoFon><img src=/design/img/spc.gif width=270 height=120 hspace=0 vspace=0 border=0 align=left></a>
			<div class=clear style="float:right; width:570px; ">
				<div class=clear style=" height:70px; overflow:hidden; padding-right:20px; text-align:right; line-height:120%;  " id=page-content-top-info>
				</div>
				<div class=clear style=" height:80px; overflow:hidden; padding-right:20px;" >
				<div class="topmenu-item topmenu-item-help"		><a href=/help/ 		>Help</a></div>
				<div class="topmenu-item topmenu-item-myaccount"><a href=/myaccount/	>My account</a></div>
				<div class="topmenu-item topmenu-item-phone"	><a href=/services/ 	>Phone</a></div>
			</div>
		</div>
	</div>
	<div class=page-content-mid>
	$contents
	</div>
	</div>
		

</body>
</html>];

