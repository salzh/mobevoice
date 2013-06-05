#!/usr/bin/perl
use CGI;
 use lib "/usr/local/lib/perl5/site_perl/5.15.4";
 use Spreadsheet::WriteExcel;
 use JSON;
 use LWP::Simple;

$cgi = new CGI;
my $today=&getDatetime();
my $file_name = $cgi->param("title")."_$today";
#print $cgi->header(-type => "text/html", -charset => "utf-8");
print "Content-Type:application/vnd.ms-excel\n";
print "Content-Disposition:attachment;filename=\"$file_name.xls\"\n\n";

my $caption = $cgi->param("title");

    my $workbook  = Spreadsheet::WriteExcel->new("$file_name.xls");
    my $worksheet = $workbook->add_worksheet($caption);	
	
    my $heading  = $workbook->add_format(
                                            bold    => 1,
                                            color   => 'blue',
                                            size    => 16,
                                            merge   => 1,
                                            align  => 'vcenter',
                                            );
    
    #my @headings = ($caption, '');
    #$worksheet->write_row('A1', \@headings, $heading); 
	#=================================================================
	# Create a format for the headings
    my $format = $workbook->add_format();
	 $format->set_pattern();
	 $format->set_color('white');
	 $format->set_bg_color('gray');
     $format->set_bold();
	
	 my $format1 = $workbook->add_format();
	 $format1->set_num_format(1);
	 
     my $column = $cgi->param("csvHeading");
 	 my @columnNames=split(/,/,$column);
 	 my $columnLength=@columnNames;
	
	
		for($i=0;$i<$columnLength;$i++){
		 
		 $worksheet->set_column(0,0,10);
		 $worksheet->set_column(1,1,10);
		 $worksheet->set_column(2,2,20);
		 $worksheet->set_column(3,3,20);
		 $worksheet->set_column(4,4,20);
		 $worksheet->set_column(5,5,10);
		 $worksheet->set_column(6,6,10);
		 $worksheet->set_column(7,7,20);
		 $worksheet->set_column(8,8,15);
		 $worksheet->set_column(9,9,35);
		 $worksheet->set_column(10,10,20);
		 $worksheet->set_column(11,11,15);
		  
		 $worksheet->write(0, $i, $columnNames[$i], $format);
		  
	    }
    #=================================================================
    my $buffer = $cgi->param("csvBuffer");
    my $row = $cgi->param("row");

	my $json_object=decode_json($buffer);
	my $k=1;
	
	    for($i=0;$i<$row;$i++){
		
		for($j=0;$j<$columnLength;$j++){			
	        
			if ($j eq 3)
			{
				$worksheet->write($k, $j,$json_object->{Data}[$i]->[$j],$format1);
			}
			else
			{
			   $worksheet->write($k, $j,$json_object->{Data}[$i]->[$j]);
			}
		}
		$k++;
				
	}
	#==================================================================
	
$workbook->close;
#~~~~~~~~~~~~~~~~~
my @fileholder;

open(FILE,"<$file_name.xls");
@fileholder=<FILE>;
close(FILE);

print @fileholder;


sub getDatetime()
{
   my $datetime="";
    
   my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst);
   
      ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);
      $year = $year+1900;
      $mon=$mon+1;
      $datetime = "$year-$mon-$mday  $hour:$min:$sec";
  
  return $datetime;
}
