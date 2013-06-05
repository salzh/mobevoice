######################################################################################################
#PERL-DBI-mysql模块,表创建,连接,和增,删,改常见操作函数  精彩奇讯 麻辣 2005 年 9月
######################################################################################################

package SQL;

use DBI;

use strict;

my $_cbb_path=$main::SET{script_path};

my $_data_path=$main::SET{data_path};

my $_now_time=$main::SET{now_time};

my %attr=(RaiseError => 0, PrintError => 1, AutoCommit => 1);

#my $connect_status = $main::SET{connect_status};

sub new {
my $this = {};
bless $this; 
return $this; 
}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   测试数据库环境                                          #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#


sub Test_db {
	my $self =shift;
my $p =shift;

my %param =%$p;

my $DRIVERS_HOST_POST="DBI:mysql:host=$param{DB_url}:port=$param{DB_port}";

my $dbh=DBI->connect("$DRIVERS_HOST_POST","$param{DB_user}","$param{DB_pass}") or return 0;

$dbh->disconnect;

return  1;

}

sub Test_db_exists {
	my $self =shift;
my $p =shift;

my %param =%$p;

my $DRIVERS_HOST_POST="DBI:mysql:host=$param{DB_url}:port=$param{DB_port}";

my $dbh=DBI->connect("$DRIVERS_HOST_POST:database=$param{DB_name}","$param{DB_user}","$param{DB_pass}") or return 0;	

$dbh->disconnect;

return 1;

}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   打开已知数据库连接                                      #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub connect_db {

my $self =shift;

my $p =shift;

my %param =%$p;
#$param{charset} = 'gb2312';
#print "==$param{charset}==";

	my $dbh;
	
	my $DRIVERS_HOST_POST="DBI:mysql:host=$param{DB_url}:port=$param{DB_port}";

	$dbh=DBI->connect("$DRIVERS_HOST_POST:database=$param{DB_name}","$param{DB_user}","$param{DB_pass}",\%attr) or return;

	my $sql ="SET NAMES '$param{charset}'";

	my $sth=$dbh->prepare($sql);

	$sth->execute;

	return $dbh;

}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   关闭数据库连接                                          #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub disconnect_db {
	my $self =shift;
my $dbh=shift;

$dbh->disconnect;

return 1;

}
#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   创建新数据库                                            #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub create_db {
	
my $self =shift;

my $p =shift;

my %param =%$p;

my $DRIVERS_HOST_POST="DBI:mysql:host=$param{DB_url}:port=$param{DB_port}";

my $dbh=DBI->connect("$DRIVERS_HOST_POST","$param{DB_user}","$param{DB_pass}") or &sql_log();

my $query= "CREATE DATABASE IF NOT EXISTS $param{DB_name}";

my $sth=$dbh->prepare($query) or die "$dbh->errstr<br>";

$sth->execute or die "$dbh->errstr<br>";

$sth->finish;

$dbh->disconnect;

return 1;
}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   单个建表                                                #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub create_table {
my $self =shift;
my $p =shift;

my %param =%$p;

my $query= "CREATE TABLE IF NOT EXISTS $param{table_name}";

my $sth=$param{dbh}->prepare($query);#or  die "Can't CREATE TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";

$sth->execute;

$sth->finish;

$param{dbh}->disconnect;

return 1;

}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   批量创建导出的表                                        #
# 所需元素      :    phpmyadmin 导出的表结构                                #
#\\\---------------------------------------------------------------------\\\#

sub create_tables {
	my $self =shift;
	my $p =shift;
	my %param =%$p;
	
	my $DRIVERS_HOST_POST="DBI:mysql:host=$param{DB_url}:port=$param{DB_port}";
	
	my $dbh=DBI->connect("$DRIVERS_HOST_POST:database=$param{DB_name}","$param{DB_user}","$param{DB_pass}") or &sql_log();
	
	my $query;
	
	my $creat_info="<br><b> <font color=red>$param{DB_type}</font> 数据库创建信息: </b><br><br><b>数据库名:<font color=red>$param{DB_name}</font></b><br><br>";
	
	my $table_name="";
	#--地址:端口:数据库名,数据库用户名:密码--#

	open QF, "$_cbb_path/sql/$param{DB_type}/$param{cbb_tables}";

	while (defined (my $line = <QF>)) {
		next if ($line=~/--/);
		if ($line=~/CREATE TABLE/) {
			$table_name=$line;
			$table_name=~s/\(//;

		}
		my $isComment = 0;
		my $isBlankLine = 0;
		if ($line =~ /^\s*#/)  {$isComment   = 1}
		if ($line =~ /^\s*\n/) {$isBlankLine = 1}
		if (!$isComment and !$isBlankLine) { $query .= " $line"; }
		if ($line =~ /;\s*(\n|$)/) {
			$query =~ s/^\s+//;
			$query =~ s/\s+$//;
			$query =~ s/(\r|\n)+/ /g;
			if ($query ne ';') {

				my $er=0;

				$dbh->do($query) or $er=1;

				if ($er ==1) {
					$creat_info = "$creat_info Can't CREATE TABLE $param{DB_name}:$table_name" .$dbh->errstr."<br>";
				}
				else {
					$creat_info  = qq($creat_info table:<font color=red>$table_name</font> create successful!<br>);
				}
			}
			$query = '';
		}
	}
	close QF;

	return $creat_info;
}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   更新单条数据                                            #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub DB_update {

my $self =shift;

my $p =shift;

my %param =%$p;

my $sql = qq(update `$param{table_name}` set $param{DB_update} where $param{key}='$param{value}');

my $sth=$param{dbh}->prepare($sql) or  die "Can't DB_update TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";

$sth->execute or  die "$sql Can't DB_update TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";;

$sth->finish;

return $param{dbh};
}
#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   更新单条数据                                            #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub DB_update_1 {

my $self =shift;

my $p =shift;

my %param =%$p;

my $sql = qq(update `$param{table_name}` set $param{DB_update} where $param{where});

#print $sql;

my $sth=$param{dbh}->prepare($sql) or  die "Can't DB_update TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";

$sth->execute or  die "$sql Can't DB_update TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";;

$sth->finish;

return $param{dbh};
}
#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   按照键插入单条数据  单次连接                            #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub DB_insert {

my $self =shift;

my $p =shift;

my %param =%$p;

my $sql = qq(INSERT INTO $param{table_name} ($param{key}) values ($param{insert}););

#print $sql;

my $sth=$param{dbh}->prepare($sql) or  die "Can't Insert TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";

$sth->execute  or  die "[$sql]Can't Insert TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";

$sth->finish;

return $param{dbh};

}


#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   按键删除行                                              #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#


sub DB_delete {

my $p =shift;

my %param =%$p;

my $sql="DELETE FROM $param{table_name} where $param{key}='$param{value}'";

my $sth=$param{dbh}->prepare($sql) or die "Can't del TABLE $param{DB_name}:$param{table_name}".$param{dbh}->errstr."<br>";

$sth->execute or die "Can't del TABLE $param{value} <br>".$param{dbh}->errstr."<br>";;

$sth->finish;

return $param{dbh};

}
#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   更新整条数据    单次连接关闭                            #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub DB_replace {

my $self =shift;

my $p =shift;

my %param =%$p;

#main::print_hash(%$p);

my $sql = qq(REPLACE INTO $param{table_name} ($param{key}) values ($param{insert}));

#print "$sql";

 my $sth=$param{dbh}->prepare($sql) or  die "Can't REPLACE TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";

$sth->execute  or  die "Can't REPLACE TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>$sql";

$sth->finish;

return 1;

}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   按其键表查询                                            #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub DB_fetchrow_hashref {
	
my $self =shift;

my $p =shift;

my %param =%$p;

my $sql = $param{sql};


my $sth=$param{dbh}->prepare($sql);

$sth->execute or die "Can't execute [$sql]" .$param{dbh}->errstr."<br>";;

#$sth->fetchrow_hashref();

#$sth->finish;

#my $a;

#$a = $sth->fetchrow_hashref;
	
#main::print_hash(%$a);

return $sth;

}
#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   查询                                                    #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub DB_select_1 {
my $self =shift;
my $p =shift;

my %param =%$p;

my $where=qq( where $param{key}='$param{value}') if ($param{key});#

my	$sql = "SELECT * FROM $param{table_name}$where";

my $sth=$param{dbh}->prepare($sql) or die "Can't Select TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";

$sth->execute;

my $data=$sth->fetchall_arrayref;#------------数组指针

my $arry="";

foreach (@$data) {

$arry=join("\t",@$_);

}

$sth->finish;

return $arry;

}

#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   求和                                                    #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

sub DB_sum {

my $p =shift;

my %param =%$p;

my $sql="SELECT $param{SELECT} FROM $param{table_name} $param{where}";

my $sth=$param{dbh}->prepare($sql) or die "Can't Select TABLE $param{DB_name}:$param{table_name}" .$param{dbh}->errstr."<br>";

$sth->execute;

my @data=$sth->fetchrow_array();#------------返回数组


return @data;

}
#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   字符格式化                                              #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#
sub db_quote 
{
	my $p =shift;

my %param =%$p;

	return $param{dbh}->quote($param{text});
}


#\\\---------------------------------------------------------------------\\\#
# 函数用途      :   错误日志记录                                            #
# 所需元素      :                                                           #
#\\\---------------------------------------------------------------------\\\#

#--------------------------------------------------------------------------错误日志
sub sql_log {
	&main::WriteFile_add("$_data_path/sql/sql.log","$_now_time:找不到数据库 $DBI::errstr\n");
	&main::stop_view( "找不到数据库 $DBI::errstr\n");
}
1;