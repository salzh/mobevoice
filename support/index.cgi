#!/usr/bin/perl
#
# fixedredir.cgi
use CGI::Carp qw( fatalsToBrowser );
use strict;
use warnings;

my $URL = "http://zenopbx.com/ticket/";
#print "Status: 302 Moved\nLocation: $URL\n\n";
print "Content-Type: text/html\n\n";
print qq[
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html lang="en">
 <head>
  <title>ZenoFon Support</title>
  <style type="text/css">
   html, body, div, iframe { margin:0; padding:0; height:100%; }
   iframe { display:block; width:100%; border:none; }
  </style>
 </head>
 <body>
  <div>
   <iframe src="$URL" />
  </div>
 </body>
</html>
];



