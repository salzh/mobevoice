#!/usr/bin/perl
#print "Content-type:text/html\n\n";
require "include.cgi";
use DBI;
use CGI;
use utf8;
use Encode;
my $q = new CGI;

if (&active_user_permission_check("noc:can_view_reports") ne 1) {adm_error("no permission"); exit;}
use Data::Dumper;

if (&active_user_permission_check("noc:profile_edit") ne 1) {adm_error("no permission"); exit;}


#Get Tinymce textarea content from url path
#======================================================================
my $contents = $q->param ('sms_help');
my $action ="";
my $msg = "";

if ($contents ne "")
{
$contents =~ s/(["'*])/\\$1/g;
my $sql = qq{update cms_page set contents = "$contents" where id = 1};
&database_do($sql);
$msg = "<script>alert('Sms help page updated successfully')</script>";
$action = "sms_help";
&sms_help($msg);
exit;
}
#======================================================================


#Get action value from url path
#=========================================================
my $sms_help = $form{'action'};

$action = ($sms_help ne "") ? $form{'action'} : $action ;

if ($action eq "sms_help") {&sms_help();}
#=========================================================


#Create sms_help page
sub sms_help()
{
my($msg) =@_;
my %t=();
my %hash = database_select_as_hash("select 1,1,contents from cms_page where id = 1","1,contents");
my $contents = $hash{1}{contents};
$t{title}	= "Sms Help Page";
$t{content}	= qq[ $msg
<html>
<title>Sms Help Page</title>
<head>
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
<form method = "post">
	    <div>
		<textarea id="sms_help" name="sms_help" rows="40" cols="100" style="width: 100%">
		$contents			
		</textarea>
		</div>
		<input type="submit" name="submit" value="Submit"/>
		<input type="reset" name="reset" value="Reset" />
	</div>
</form>
</body>
</html>];
&template_print("template.html",%t);
}




