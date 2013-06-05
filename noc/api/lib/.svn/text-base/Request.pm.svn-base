######################################################################################################
#PERL COOKIE  FORM 函数  精彩奇讯 麻辣 2011 年 9月
######################################################################################################
#                                                                           #
#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   获取所有Cookies值,同时为汉字解码                        #
#\\\---------------------------------------------------------------------\\\#
sub GET_COOKIES {
	foreach ( split( /; /, $ENV{'HTTP_COOKIE'} ) ) {
		( $cookie, $value ) = split(/=/);
		$_COOKIE{$cookie} = $value;
	}
	
	
	if($ENV{'QUERY_STRING'}){my $get_url = "?$ENV{'QUERY_STRING'}";};
	#print_var($ENV{HTTP_REFERER});
	unless($_COOKIE{admname}){
	if ("$SET{url_script_path}$SET{script_name}$get_url" eq $ENV{HTTP_REFERER}) {
		if(($SET{now_time_id}-$_COOKIE{lasttime}) < $S_cfg{Reload_time}){
			&stop_view("系统提示，连续刷新同一页面不能小于$S_cfg{Reload_time}秒");
			exit;
		}
	}
	
}
}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   Cookies写入                                             #
#\\\---------------------------------------------------------------------\\\#
sub Set_user_cookie {
    if ( $_REQUEST{savepassword} eq "1" or $_COOKIE{savepassword} eq 1 ) {
        $savechecked = 1;
        $savetime    = "expires=\"+expireDate.toGMTString()+\";";
    }
    $_REQUEST{u_username}=&URL_encode_16hex($_REQUEST{u_username});
    
    print <<HTML;
<SCRIPT>
expireDate=new Date;
expireDate.setFullYear(expireDate.getFullYear()+1);
document.cookie="username="+"$_REQUEST{u_username}"+";$savetime";
document.cookie="password="+"$_REQUEST{u_password}"+";$savetime";
document.cookie="savepassword="+"$savechecked"+";$savetime";
</SCRIPT>
HTML
}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   获取表单信息                                            #
#\\\---------------------------------------------------------------------\\\#
sub GET_REQUEST {
	 #---------------------------------解析域名绑定
	 if($S_cfg{$ENV{'HTTP_HOST'}}){
	 unless($ENV{'QUERY_STRING'}) {
	 my	(undef,$STRING)=split(/\?/,$S_cfg{$ENV{'HTTP_HOST'}});
	 	$ENV{'QUERY_STRING'}=$STRING;
		}
	}
	#-----------------------------------解析结束
	 
	unless($ENV{'CONTENT_TYPE'}=~ /multipart\/form-data/) {
	
	if ( $ENV{'REQUEST_METHOD'} eq "POST" ) {
		read( STDIN, $_FORM_BUFFER, $ENV{'CONTENT_LENGTH'} );
	}
	else {
		$_FORM_BUFFER = $ENV{'QUERY_STRING'};
	        $_FORM_BUFFER =~ s/\.\.\///g;#--------防黑客,过滤相对路径请求
	}
	
	@pairs = split( /&/, $_FORM_BUFFER );
	
	foreach $pair (@pairs) {
		my ( $name, $value ) = split( /=/, $pair );
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =&Regular_text($value);
		
		if ( $_REQUEST{$name} ) { 
			$_REQUEST{$name} = $_REQUEST{$name} . "," . $value; 
			
			}
		else { $_REQUEST{$name} = $value;$_GET{$name} = $value;  }
	
	}
}
else {
	&GET_AFFIX();#获取上传附件方式
}
	
	

#stop_view($_FORM_BUFFER);
}
#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   获取表单信息, 获取上传附件方式                             #
#\\\---------------------------------------------------------------------\\\#

sub GET_AFFIX {

	my $buffer;
	
	binmode STDIN;
		read( STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	
		( $boundary = $ENV{'CONTENT_TYPE'} ) =~ s/^.*boundary=(.*)$/$1/;
		
		@pairs = split( /--$boundary/, $buffer );
		
		foreach $pair (@pairs) {
			my( $dump, $line, $value ) = split( /\r\n/, $pair, 3 );
			if ( $line =~ /filename/ ) {
				$_REQUEST{User_file_name} = $line;
			}
			
				next if $line =~ /filename=\"\"/;
				$line =~ s/^Content-Disposition: form-data; //;
				
			(@column) = split( /;\s+/, $line );
			( $name = $column[0] ) =~ s/^name="([^\"]+)"$/$1/g;#加反斜杠 2011.5.12
			
			if ( $#column > 0 ) {
				( $dump, $dump, $value ) = split( /\r\n/, $value, 3 );
			}
			else {
				( $dump, $value ) = split( /\r\n/, $value, 2 );
				next if $value =~ /^\s*$/;
				chop( $value );
				chop( $value );
				
				$value =&Regular_text($value);#
				$_REQUEST{$name} = $value;
				
				next;
			}
			$_REQUEST{$name} = $value;
	}
  
}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   通用信息过滤                                            #
#\\\---------------------------------------------------------------------\\\#
sub Regular_text {
        my $Regular_text = shift;
        $Regular_text =~ s/&nbsp;/&amp;nbsp;/g;
        $Regular_text =~ s/\t/          /g;
        $Regular_text =~ s/\032//isg;
        $Regular_text =~ s/>/&gt;/g;
        $Regular_text =~ s/</&lt;/g;
        $Regular_text =~ s/\r//g;
        $Regular_text =~ s/\n/\<br\>/g;
	$Regular_text =~ s/noncgi\/$S_cfg{affix_rand_path}\//noncgi\/\$S_cfg{affix_rand_path}\//gi;
return $Regular_text;
}
1;