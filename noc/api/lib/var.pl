use CGI::Carp qw(fatalsToBrowser);

print "Content-type: text/html; charset=gbk\n\n";

#\\\---------------------------------------------------------------------\\\#
#  Print hash  用途 :   打印哈希数组结构(调试用)                                                            #
#  Example: &Print_hash(%_REQUEST);                                         #
#\\\---------------------------------------------------------------------\\\#
sub print_hash {
	my %HASH = @_;
	
		print "<p align=left><table><tr><td><pre>HASH:(\n";
	
	foreach(sort keys %HASH) {
		print '      {'.$_.'} => '.$HASH{$_}." \n";	
	}

print ")\n</pre></td></tr></table></p>";

}          
#\\\---------------------------------------------------------------------\\\#
# Print_array,用途 :   打印数组结构(调试用)                                 #
# Example:Print_ARRAY(@array);                                              #
#\\\---------------------------------------------------------------------\\\#    
sub print_array {
	
			print "<p align=left><table><tr><td><pre>Array:(\n";
			
			my $i = 0;
	foreach(@_) {
	print ' ['.$i.'] => '.$_." \n";	
	$i++;
	}

print ")\n</pre></td></tr></table></p>";
	
}     

#\\\---------------------------------------------------------------------\\\#
# Print_var,用途 :   打印变量内容(调试用)                                   #
# Example:Print_avr($var);                                                  #
#\\\---------------------------------------------------------------------\\\#
sub print_var {

	print "<p align=left><table><tr><td><pre>Var:(\n";

	print 'var = [' . $_[0] .']';

	print " \n)</pre></td></tr></table></p>";

}


1;