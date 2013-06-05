#!/usr/bin/perl
require "include.cgi";
use Data::Dumper;
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_manage_rate") ne 1) {adm_error("no permission"); exit;}
#=======================================================


sleep(3);

#=======================================================
# main loop
#=======================================================
$my_url = "rate.cgi";
$action = $form{action};
if 		($action eq "rates_list")		{ &do_rates_list();		}
elsif 	($action eq "rate_add")			{ &do_rate_add();		}
elsif 	($action eq "rate_edit")		{ &do_rate_edit();		}
elsif 	($action eq "rate_del")			{ &do_rate_del();		}
elsif 	($action eq "rates_matrix")		{ &do_rates_matrix();	}
elsif 	($action eq "rate_public")		{ &do_rate_public();	}
elsif 	($action eq "rate_play_code")	{ &do_rate_play_code();	}
elsif 	($action eq "rate_download")	{ &do_rate_download();	}
elsif 	($action eq "rate_upload")		{ &do_rate_upload();	}
elsif 	($action eq "rate_check")		{ &do_rate_check();		}
else									{ &do_rates_list(); 	}
exit;
#=======================================================


sub do_rates_list(){
	#
	# pega a listal
	%hash = database_select_as_hash("SELECT id,name FROM product_rate_table","title");
	$html_rates_list = "";
    foreach $id (sort{$hash{$a}{title} cmp $hash{$b}{title}} keys %hash) {
		#$html_list .= "<li><a href=$my_url?action=rate_edit&rate_id=$id>$hash{$id}{title}</a></li>";
		$html_rates_list .= "<option value=$id>$hash{$id}{title}</option>";
	}
	#
	# pega public
	$public_id = &data_get("adm_data","rate","public");
	$public_name = $hash{$public_id}{title} || "(disabled)";
	#
	# pega public
	$play_code_id = &data_get("adm_data","rate","play_code");
	$play_code_name = $hash{$play_code_id}{title} || "(disabled)";
	#
	# pega matrix
	%html_data = ();
	$html_final = "";
	$sql = "
	select id,rate_slot_callback, 
	rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9,
	rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,rate_slot_5_name,rate_slot_6_name,rate_slot_7_name,rate_slot_8_name,rate_slot_9_name
	from service_status	
	";
	%hash = database_select_as_hash($sql,"c,s1,s2,s3,s4,s5,s6,s7,s8,s9,n1,n2,n3,n4,n5,n6,n7,n8,n9");
    foreach $id (keys %hash) { 
    	$html_data{db_r}{$id}{c} = $hash{$id}{"c"};
    	foreach(1..9) { $html_data{db_r}{$id}{$_} = $hash{$id}{"s$_"};  } 
    }
	%hash = database_select_as_hash("SELECT id,name FROM product_rate_table","title");
    foreach $id (keys %hash) {$html_data{select}{$id} = $hash{$id}{title}; }
	%hash = database_select_as_hash("SELECT id,ui_order,ui_group,name FROM service_status where deleted=0","ui_order,ui_group,name");
    foreach $id (sort{$hash{$a}{ui_order} <=> $hash{$b}{ui_order}} keys %hash) {
    	$group = $hash{$id}{ui_group};
    	$name = $hash{$id}{name};
		foreach $route (1..9){
			$html_data{group}{$group} = $hash{$id}{ui_order};
			$html_data{name}{$id} = $hash{$id}{name};
			$html_data{order}{$group}{$id} = $hash{$id}{ui_order};
		}
	}
	foreach $group (sort{$html_data{group}{$a} <=> $html_data{group}{$b}} keys %{$html_data{group}}){
		$html_final .= "<table class=WindowsTable border=0 colspan=0 cellpadding=0 cellspacing=0 >";
		$html_final .= "<thead>";
		$html_final .= "<tr><td colspan=99><h1>$group</h1></td></tr>";
		$html_final .= "<tr>";
		$html_final .= "<td>&nbsp;</td>";
		foreach $id (sort{$html_data{order}{$group}{$a} <=> $html_data{order}{$group}{$b}} keys %{$html_data{order}{$group}}){
			$html_final .= "<td>$html_data{name}{$id}</td>";
		}
		$html_final .= "</tr>";
		$html_final .= "</thead>";
		$html_final .= "<tbody>";
		#
		# linha de callback
		$html_final .= "<tr>";
		$html_final .= "<td>Callback</td>";
		foreach $id (sort{$html_data{order}{$group}{$a} <=> $html_data{order}{$group}{$b}} keys %{$html_data{order}{$group}}){
			$html_final .= "<td>";
			$html_final .= "<input class=rate_select value=\"$html_data{select}{$html_data{db_r}{$id}{c}}\" disabled readonly>";
			$html_final .= "</td>";
		}
		$html_final .= "</tr>";
		#
		# linhas de rotas
		foreach $route (1..9){
			$html_final .= "<tr>";
			$html_final .= "<td>Rote $route</td>";
			foreach $id (sort{$html_data{order}{$group}{$a} <=> $html_data{order}{$group}{$b}} keys %{$html_data{order}{$group}}){
				$html_final .= "<td>";
				$html_final .= "<input class=rate_select value=\"$html_data{select}{$html_data{db_r}{$id}{$route}}\" disabled readonly>";
				$html_final .= "</td>";
			}
			$html_final .= "</tr>";
		}
		$html_final .= "</tbody>";
		$html_final .= "</table><br>";
	}
	#$html_final .= "<pre>".Dumper(%html_data)."</pre>";
    #
    # print page
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Calls rate/route";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Calls rate/route";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{content}	= qq[
    <style>
	    .rate_select{
    	width:150px;
    	padding:0px;
    	margin:0px;
    	background-color:transparent;
    	border:0px;
	    }
    </style>
	<script>
		function check_loading(){
			MyHTML("check_data","<img src=/design/img/loading.gif align=left>&nbsp;Please wait!")
		}
		function check_ready(html){
			MyHTML("check_data",html);
		}
	</script>




    <table class=clear border=0 colspan=0 cellpadding=0 cellspacing=0 ><tr>

	    <td width=280 valign=top><div class=clear style=width:280px>
			<fieldset class=config_select_list><legend>Rate tables</legend>
				<form action=$my_url name=edit_rate>
				<select size=16 style=width:100% name=rate_id id=rate_id ondblclick="this.form.submit();" >$html_rates_list</select>
				<button class="cancel" type=button onclick="window.location='$my_url?action=rate_add'">New</button>
				<button class="cancel" type=button onclick="if(this.form.elements[0].selectedIndex>=0){window.location='$my_url?action=rate_del&rate_id='+this.form.elements[0].options[this.form.elements[0].selectedIndex].value;}">Delete</button>
				<button class="save" type=submit>Edit</button>
				<input type=hidden name=action value=rate_edit >
				</form>
			</fieldset>
		</div></td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>

	    <td width=280 valign=top><div class=clear style=width:280px>
			<fieldset style=width:auto;><legend>Public rate</legend>
				Rate table in use at <a href=/about/rate.cgi target=_blank>public rate search</a>
				<form action=$my_url >
				<input type=hidden name=action value=rate_public>
				<input style=width:100% radonly disabled value="$public_name"><br>
				<button class="save" type=submit>Edit</button>
				</form>
			</fieldset><br>
			<fieldset style=width:auto;><legend>Play code rate</legend>
				Rate table in use when system need dial a client and play code like pin request, sign, ani confirm, etc.
				<form action=$my_url >
				<input type=hidden name=action value=rate_play_code>
				<input style=width:100% radonly disabled value="$play_code_name"><br>
				<button class="save" type=submit>Edit</button>
				</form>
			</fieldset><br>
		</div></td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>

	    <td width=350 valign=top><div class=clear style=width:350px>
			<fieldset class=config_select_list style="padding-right:0px"><legend>Test</legend>
			<div style="height:270px;overflow-x:hidden; overflow-y:auto; padding-right:20px; ">
				<form action=$my_url target=check_io> 
				Number to test (E164 format):<br>
				<input name=number style=width:100%><br>
				<button type=submit class="button button_positive "	onclick="check_loading()";>Test</button>
				<input type=hidden name=action value=rate_check>
				</form>
				<br>
				<div class=clear id=check_data style="font-size:10px; line-height:150%; overflow:hidden; white-space: nowrap; border:0px solid green;"></div>
				<iframe id=check_io name=check_io style="display:none;"></iframe>
			</div>
			</fieldset>
		</div></td>

	</tr></table>







	<br>

	<div class=clear style=width:auto;>
	<fieldset style=width:auto;><legend>'Service status X Rote' Matrix</legend>
		<form action=$my_url >
		<input type=hidden name=action value=rates_matrix>
		$html_final 
		<button class="save" type=submit>Edit 'Service status X Rote' Matrix</button>
		</form>
	</fieldset>
	</div>


    ];
    &template_print("template.html",%t);
}
sub do_rate_play_code(){
	#
	# pega rates_list
	%rates_list = database_select_as_hash("SELECT id,name FROM product_rate_table","title");
	#
	# try to save
	$error_message = "";
	if ($form{save} ne "") {
		if (&multilevel_clickchain_check("rra",$form{save}) eq 1) {
			if ($form{id} eq "DISABLE") {
				&data_delete("adm_data","rate","play_code");
				cgi_redirect("$my_url");
				exit;
			} else {
				$form{id} = &clean_int(substr($form{id},0,255));
				if ($form{id} eq "") { $error_message = "Wrong rate table";}
				unless (exists($rates_list{$form{id}})) { $error_message = "unknown rate table";}
				if ($error_message eq "") {
					&data_set("adm_data","rate","play_code",$form{id});
					cgi_redirect("$my_url");
					exit;
				}
			}
		} else {
			$error_message = "Try to save again";
		}
	}
	#
	# popula formulario
	if ($form{save} eq "") {
		$form{id} = &data_get("adm_data","rate","play_code");
	}
	#
	# monta a lista
	$html_rates_list = "";
    foreach $id (sort{$rates_list{$a}{title} cmp $rates_list{$b}{title}} keys %rates_list) {
    	$tmp = ($form{id} eq $id) ? "selected" : "";
		$html_rates_list .= "<option $tmp value=$id>$rates_list{$id}{title}</option>";
	}
	#
    #
    # print page
    $error_message = ($error_message eq "") ? $error_message  : "$error_message<br><br>";
    %t = ();
    $save_id = &multilevel_clickchain_set("rrp");
    $t{my_url}	= $my_url;
    $t{title}	= "<a href=$my_url>Settings</a> &#187; <a href=$my_url?action=rates_list>Calls rate/route</a> &#187; play code rate";
    $t{title}	= "Select rate for play code action";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Calls rate/route";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{breadcrumb}{3}{title}	= "Select rate for play code action";
    $t{breadcrumb}{3}{url}		= "$my_url?action=rate_play_code";
    $t{content}	= qq[
		<fieldset style=width:300px;><legend>Play code rate</legend>
			Select rate table in use when system need dial a client and play code like pin request, sign, ani confirm, etc.<br>
			<br>
			<form action=$my_url >
			<select name=id>
				<option value=DISABLE>(disabled)</option>
				<option value=DISABLE></option>
				$html_rates_list
			</select><br>
			<br>
			<input type=hidden name=action value=rate_play_code>
			<input type=hidden name=save value=$save_id>
			$error_message 
			<button type=button class="cancel"	onclick="window.location='$my_url'">Cancel</button>
			<button type=submit class="save"  	onclick="modal_loadingblock()" >Save</button>
			</form>
		</fieldset><br>
    ];
    &template_print("template.html",%t);
	
}
sub do_rate_public(){
	#
	# pega rates_list
	%rates_list = database_select_as_hash("SELECT id,name FROM product_rate_table","title");
	#
	# try to save
	$error_message = "";
	if ($form{save} ne "") {
		if (&multilevel_clickchain_check("rra",$form{save}) eq 1) {
			if ($form{id} eq "DISABLE") {
				&data_delete("adm_data","rate","public");
				cgi_redirect("$my_url");
				exit;
			} else {
				$form{id} = &clean_int(substr($form{id},0,255));
				if ($form{id} eq "") { $error_message = "Wrong rate table";}
				unless (exists($rates_list{$form{id}})) { $error_message = "unknown rate table";}
				if ($error_message eq "") {
					&data_set("adm_data","rate","public",$form{id});
					cgi_redirect("$my_url");
					exit;
				}
			}
		} else {
			$error_message = "Try to save again";
		}
	}
	#
	# popula formulario
	if ($form{save} eq "") {
		$form{id} = &data_get("adm_data","rate","public");
	}
	#
	# monta a lista
	$html_rates_list = "";
    foreach $id (sort{$rates_list{$a}{title} cmp $rates_list{$b}{title}} keys %rates_list) {
    	$tmp = ($form{id} eq $id) ? "selected" : "";
		$html_rates_list .= "<option $tmp value=$id>$rates_list{$id}{title}</option>";
	}
	#
    #
    # print page
    $error_message = ($error_message eq "") ? $error_message  : "$error_message<br><br>";
    %t = ();
    $save_id = &multilevel_clickchain_set("rrp");
    $t{my_url}	= $my_url;
    $t{title}	= "<a href=$my_url>Settings</a> &#187; <a href=$my_url?action=rates_list>Calls rate/route</a> &#187; Public rate";
    $t{title}	= "Select public rate to web query";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Calls rate/route";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{breadcrumb}{3}{title}	= "Select public rate to web query";
    $t{breadcrumb}{3}{url}		= "$my_url?action=rate_public";


    $t{content}	= qq[
		<fieldset style=width:300px;><legend>Public rate</legend>
			Select rate table to use in Public web query<br>
			<br>
			<form action=$my_url >
			<select name=id>
				<option value=DISABLE>(disabled)</option>
				<option value=DISABLE></option>
				$html_rates_list
			</select><br>
			<br>
			<input type=hidden name=action value=rate_public>
			<input type=hidden name=save value=$save_id>
			$error_message 
			<button type=button class="cancel"	onclick="window.location='$my_url'">Cancel</button>
			<button type=submit class="save"  	onclick="modal_loadingblock()" >Save</button>
			</form>
		</fieldset><br>
    ];
    &template_print("template.html",%t);
}
sub do_rates_matrix(){
	#
	# pega dados
	%rates_list = database_select_as_hash("SELECT id,name FROM product_rate_table","title");
	%status_list = database_select_as_hash("SELECT id,ui_order,ui_group,name FROM service_status where deleted=0","ui_order,ui_group,name");
	#
	# try to save
	$error_message = "";
	if ($form{save} ne "") {
		if (&multilevel_clickchain_check("rra",$form{save}) eq 1) {
			#
			# coleta dados do form, valida e coloca nesse hash
			$data_save = ();
			foreach $key (keys %form) {
				$value = $form{$key};
				($key0,$key1,$key2) = split(/\_/,$key);
				$key1 = &clean_int($key1);
				$key2 = &clean_int($key2);
				if ($key1 ne "") {$data_save{$key1}{ping}=1;}
				if ($key0 eq "callbackid") {
					unless (exists($rates_list{$value})) {next}
					unless (exists($status_list{$key1})) {next}
					$data_save{$key1}{callback_id} = $value; 
				} elsif ($key0 eq "rateid") {
					unless (exists($rates_list{$value})) {next}
					unless (exists($status_list{$key1})) {next}
					if ( ($key2>9) || ($key2<1) || ($key2 eq "")) {next}
					$data_save{$key1}{rate_id}{$key2} = $value; 
				} elsif ($key0 eq "ratename") {
					unless (exists($status_list{$key1})) {next}
					if ( ($key2>9) || ($key2<1) || ($key2 eq "")) {next}
					$data_save{$key1}{rate_name}{$key2} = &trim(&clean_str(substr($value,0,100))); 
				}
			}
			#
			# monta os sql conforme data_save
			foreach $id (keys %data_save) {
				$sql  = " update service_status set ";
				foreach $i (1..9) {
					$sql .= ($data_save{$id}{rate_id}{$i} eq "") ? " rate_slot_$i = null, " : " rate_slot_$i = '$data_save{$id}{rate_id}{$i}', ";
					$sql .= " rate_slot_".$i."_name =  '$data_save{$id}{rate_name}{$i}', ";
				}
				$sql .= ($data_save{$id}{callback_id} eq "") ? " rate_slot_callback=null " : " rate_slot_callback='$data_save{$id}{callback_id}' ";
				$sql .= " where id='$id' ";
				&database_do($sql);
			}
			#
			# redireciona
			cgi_redirect("$my_url");
			exit;
		} else {
			$error_message = "Try to save again";
		}
	}
	#
	# popular form se nao save
	if ($form{save} eq "") {
		$sql = "
		select id,rate_slot_callback, 
		rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9,
		rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,rate_slot_5_name,rate_slot_6_name,rate_slot_7_name,rate_slot_8_name,rate_slot_9_name
		from service_status	
		";
		%hash = database_select_as_hash($sql,"c,s1,s2,s3,s4,s5,s6,s7,s8,s9,n1,n2,n3,n4,n5,n6,n7,n8,n9");
	    foreach $id (keys %hash) { 
	    	$form{"callbackid_".$id} = $hash{$id}{"c"};
	    	foreach(1..9) { 
		    	$form{"rateid_".$id."_".$_} = $hash{$id}{"s$_"};  
		    	$form{"ratename_".$id."_".$_} = $hash{$id}{"n$_"};  
	    	} 
	    }
	}
	#
	# matrix
	%matrix_data = ();
	$matrix_html = "";
    foreach $id (keys %rates_list) {$matrix_data{select}{$id} = $rates_list{$id}{title}; }
    foreach $id (sort{$status_list{$a}{ui_order} <=> $status_list{$b}{ui_order}} keys %status_list) {
    	$group = $status_list{$id}{ui_group};
    	$name = $status_list{$id}{name};
		foreach $route (1..9){
			$matrix_data{group}{$group} = $status_list{$id}{ui_order};
			$matrix_data{name}{$id} = $status_list{$id}{name};
			$matrix_data{order}{$group}{$id} = $status_list{$id}{ui_order};
		}
	}
	foreach $group (sort{$matrix_data{group}{$a} <=> $matrix_data{group}{$b}} keys %{$matrix_data{group}}){
		$matrix_html .= "<table class=WindowsTable border=0 colspan=0 cellpadding=0 cellspacing=0 >";
		$matrix_html .= "<thead>";
		$matrix_html .= "<tr><td colspan=99><h1>$group</h1></td></tr>";
		$matrix_html .= "<tr>";
		$matrix_html .= "<td>&nbsp;</td>";
		foreach $id (sort{$matrix_data{order}{$group}{$a} <=> $matrix_data{order}{$group}{$b}} keys %{$matrix_data{order}{$group}}){
			$matrix_html .= "<td>$matrix_data{name}{$id}</td>";
		}
		$matrix_html .= "</tr>";
		$matrix_html .= "</thead>";
		$matrix_html .= "<tbody>";
		#
		# linha de callback
		$matrix_html .= "<tr>";
		$matrix_html .= "<td style='padding:7px;'>Callback</td>";
		foreach $id (sort{$matrix_data{order}{$group}{$a} <=> $matrix_data{order}{$group}{$b}} keys %{$matrix_data{order}{$group}}){
			$matrix_html .= "<td style='padding:7px;'>";
			$matrix_html .= "<select class=rate_select name='callbackid_".$id."'>";
			$matrix_html .= "<option>(Disabled)</option>";
			$matrix_html .= "<option></option>";
			foreach $select_id (sort{$matrix_data{select}{$a} cmp $matrix_data{select}{$b}} keys %{$matrix_data{select}}){
				$tmp = ($select_id eq $form{"callbackid_".$id}) ? "selected" : "";
				$matrix_html .= "<option $tmp value=$select_id>$matrix_data{select}{$select_id}</option>";
			}
			$matrix_html .= "</select>";
			$matrix_html .= "</td>";
		}
		$matrix_html .= "</tr>";
		#
		# linhas de rotas
		foreach $route (1..9){
			$matrix_html .= "<tr>";
			$matrix_html .= "<td style='border-top:1px solid #c0c0c0; padding:7px;' valign=top>Route $route</td>";
			foreach $id (sort{$matrix_data{order}{$group}{$a} <=> $matrix_data{order}{$group}{$b}} keys %{$matrix_data{order}{$group}}){
				$matrix_html .= "<td style='border-top:1px solid #c0c0c0; padding:7px;'>";
				#$matrix_html .= "<input  class=rate_name  	xstyle='width:30%;float:left;'	name='ratename_".$id."_".$route."' value='". $form{"ratename_".$id."_".$route} ."'><br>";
				$matrix_html .= "<select class=rate_select	xstyle='width:65%;float:right;'	name='rateid_".$id."_".$route."'>";
				$matrix_html .= "<option>(Disabled)</option>";
				$matrix_html .= "<option></option>";
				foreach $select_id (sort{$matrix_data{select}{$a} cmp $matrix_data{select}{$b}} keys %{$matrix_data{select}}){
					$tmp = ($select_id eq $form{"rateid_".$id."_".$route}) ? "selected" : "";
					$matrix_html .= "<option $tmp value=$select_id>$matrix_data{select}{$select_id}</option>";
				}
				$matrix_html .= "</select>";
				$matrix_html .= "</td>";
			}
			$matrix_html .= "</tr>";
		}
		$matrix_html .= "</tbody>";
		$matrix_html .= "</table><br>";
	}
    #
    # print page
    $error_message = ($error_message eq "") ? $error_message  : "$error_message<br><br>";
    $save_id = &multilevel_clickchain_set("rrp");
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit rate/route alocation matrix";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Calls rate/route";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{breadcrumb}{3}{title}	= "Edit rate/route alocation Matrix";
    $t{breadcrumb}{3}{url}		= "$my_url?action=rates_matrix";
    $t{content}	= qq[
    <style>
    .rate_select, .rate_name{
    	width:100%;
    	padding:0px;
    	margin:0px;
    }
    </style>
		<fieldset style="width:900px;"><legend>Alocation Matrix</legend>
			Assign rate tables to each Service status and route<br>
			<br>
			<form action=$my_url >
			$matrix_html 
			<br>
			<input type=hidden name=action value=rates_matrix>
			<input type=hidden name=save value=$save_id>
			$error_message 
			<button type=button class="cancel"	onclick="window.location='$my_url'">Cancel</button>
			<button type=submit class="save"    onclick="modal_loadingblock()"	>Save rate/route alocation matrix</button>
			</form>
		</fieldset>
	<br>
<pre>$dney</pre>
    ];
    &template_print("template.html",%t);
}
sub do_rate_download(){
	#
	#-------------------------------------------------
	# check rate_id
	#-------------------------------------------------
	$rate_id = &clean_int(substr($form{rate_id},0,100));
	%hash = database_select_as_hash("SELECT 1,1,name FROM product_rate_table where id='$rate_id' ","flag,name");
	if ($hash{1}{flag} ne 1) { &cgi_redirect("$my_url?action=rates_list"); exit; }
	$rate_name = $hash{1}{name};
	%country_codes = database_select_as_hash("SELECT code,name FROM country");
	$rate_country = &clean_int(substr($form{country},0,100));
	$rate_country = (exists($country_codes{$rate_country})) ? $rate_country : "";
	$rate_country_name =(exists($country_codes{$rate_country})) ? $country_codes{$rate_country} : "All";
	#
	#-------------------------------------------------
	# output header
	#-------------------------------------------------
    $external_file = "E164 rate - ".&clean_str($rate_name,"-_()","MINIMAL")." - ".&clean_str($rate_country_name,"-_()","MINIMAL").".csv";
    print "Pragma: public\n";
    print "Expires: 0\n";
    print "Cache-Control: must-revalidate, post-check=0, pre-check=0\n";
    print "Content-type: application/octet-stream\n";
    print "Content-Disposition: attachment; filename=\"$external_file\"\n";
    print "Content-Description: File Transfert\n";
    print "\n";
    print "country,";
    print "areacode,";
    print "name,";
    print "resolution,";
    print "min_call_seconds,";
    print "grace_seconds,";
    print "call_limit,";
    print "rate_per_call,";
    print "rate_per_minute,";
    print "asterisk_string\n";
    #
	#-------------------------------------------------
    # dump data
	#-------------------------------------------------
	$filter_sql = (exists($country_codes{$rate_country})) ? " and country='$rate_country' " : "";
	$sql = "
    select country,areacode,name,resolution,min_call_seconds,grace_seconds,rate_per_call,rate_per_minute,asterisk_string,max_call_seconds
	from product_rate_table_data 
	where rate_id='$rate_id' $filter_sql 
	order by country,areacode 
	";
    %rates = database_select_as_hash_with_auto_key($sql,"country,areacode,name,resolution,min_call_seconds,grace_seconds,rate_per_call,rate_per_minute,asterisk_string,max_call_seconds");
	foreach $id (sort{$a <=> $b} keys %rates){
		$rates{$id}{max_call_seconds} = ($rates{$id}{max_call_seconds}<=0)?0 : $rates{$id}{max_call_seconds};
		print "\"$rates{$id}{country}\",";
		print "\"$rates{$id}{areacode}\",";
		print "$rates{$id}{name},";
		print "$rates{$id}{resolution},";
		print "$rates{$id}{min_call_seconds},";
		print "$rates{$id}{grace_seconds},";
		print "$rates{$id}{max_call_seconds},";
		print "$rates{$id}{rate_per_call},";
		print "$rates{$id}{rate_per_minute},";
		print "$rates{$id}{asterisk_string}\n";
    }
}
sub do_rate_upload(){
	#
	#-------------------------------------------------
	# check rate_id / country
	#-------------------------------------------------
	$rate_id = &clean_int(substr($form{rate_id},0,100));
	%hash = database_select_as_hash("SELECT 1,1,name FROM product_rate_table where id='$rate_id' ","flag,name");
	if ($hash{1}{flag} ne 1) { &cgi_redirect("$my_url?action=rates_list"); exit; }
	$rate_name = $hash{1}{name};
	%country_codes = database_select_as_hash("SELECT code,name FROM country");
	$country = &clean_int(substr($form{country},0,100));
	$country = (exists($country_codes{$country})) ? $country : "";
	$country_name =(exists($country_codes{$country})) ? $country_codes{$country} : "All";
	unless ( ($form{save} ne "") && (&multilevel_clickchain_check("cre",$form{save}) eq 1) ) {&cgi_redirect("$my_url?error=clickchain&action=rate_edit&rate_id=$rate_id&filter_country=$country");}
    #
	#-------------------------------------------------
    # prepare country buffer
	#-------------------------------------------------
	$country_codes_max_lenght = 1;
    $country_codes_buffer = "|";
    foreach (keys %country_codes) {
		$l = length($_);
		$country_codes_buffer .= "$_|";
		$country_codes_max_lenght = ($l>$country_codes_max_lenght) ? $l : $country_codes_max_lenght;
	}
    #
	#-------------------------------------------------
    # pega o file e abre ele
	#-------------------------------------------------
    $temp_file = "/tmp/.upload.rate.".time.".tmp";
    $filehandle = $cgi->param("FileUpload");
    open(LOCAL, ">$temp_file");
    while($bytesread=read($filehandle,$buffer,1024)) { print LOCAL $buffer; }
    close(LOCAL);
    $status_ok = 0;
    $status_message = "";
	$status_has_block = 0;
    #
	#-------------------------------------------------
    # confere o head
	#-------------------------------------------------
    open(LOCAL,$temp_file);
    $line = <LOCAL>;
    chomp($line);
    chomp($line);
    if (index($line,",") eq -1) {
		$tmp1 = "\t"; 
		$tmp2=","; 
		$line =~ s/$tmp1/$tmp2/eg;    	
    }
	($data1,$data2,$data3,$data4,$data5,$data6,$data7,$data8,$data9,$dataa) = split(/\,/,$line);
    $tmp1 = "\""; $tmp2=" "; $data1 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data1 =~ s/$tmp1/$tmp2/eg; $data1 = trim($data1);
    $tmp1 = "\""; $tmp2=" "; $data2 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data2 =~ s/$tmp1/$tmp2/eg; $data2 = trim($data2);
    $tmp1 = "\""; $tmp2=" "; $data3 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data3 =~ s/$tmp1/$tmp2/eg; $data3 = trim($data3);
    $tmp1 = "\""; $tmp2=" "; $data4 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data4 =~ s/$tmp1/$tmp2/eg; $data4 = trim($data4);
    $tmp1 = "\""; $tmp2=" "; $data5 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data5 =~ s/$tmp1/$tmp2/eg; $data5 = trim($data5);
    $tmp1 = "\""; $tmp2=" "; $data6 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data6 =~ s/$tmp1/$tmp2/eg; $data6 = trim($data6);
    $tmp1 = "\""; $tmp2=" "; $data7 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data7 =~ s/$tmp1/$tmp2/eg; $data7 = trim($data7);
    $tmp1 = "\""; $tmp2=" "; $data8 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data8 =~ s/$tmp1/$tmp2/eg; $data8 = trim($data8);
    $tmp1 = "\""; $tmp2=" "; $data9 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data9 =~ s/$tmp1/$tmp2/eg; $data9 = trim($data9);
    $tmp1 = "\""; $tmp2=" "; $dataa =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $dataa =~ s/$tmp1/$tmp2/eg; $dataa = trim($dataa);
    if ("\L$data1,$data2,$data3,$data4,$data5,$data6,$data7,$data8,$data9,$dataa" eq "country,areacode,name,resolution,min_call_seconds,grace_seconds,call_limit,rate_per_call,rate_per_minute,asterisk_string") {
	    $status_ok = 1;
    } else {
	    $status_ok = 0;
	    $status_message = "Bad file. Please check header and CSV format.";
    }
    #
	#-------------------------------------------------
    # confere linha a linha
	#-------------------------------------------------
    if ($status_ok eq 1) {
		$total_errors = 0;
		$actual_line = 1;
		while(<LOCAL>){
			chomp;
			$line = $_;
			$actual_line++;
			$line_error=0;
			$line_error_message="";
			if ($total_errors > 5) {last;}
		    # 1-country
		    # 2-areacode
		    # 3-name
		    # 4-resolution
		    # 5-min_call_seconds
		    # 6-grace_seconds
		    # 7-call_limit
		    # 8 (7) -rate_per_call
		    # 9 (8) -rate_per_minute
		    # a (9) -asterisk_string
		    if (index($line,",") eq -1) {
				$tmp1 = "\t"; 
				$tmp2=","; 
				$line =~ s/$tmp1/$tmp2/eg;    	
		    }
			if (index($line,",") eq -1) {next}
		    ($data1,$data2,$data3,$data4,$data5,$data6,$data7,$data8,$data9,$dataa) = split(/\,/,$line);
			$tmp1 = "\""; $tmp2=" "; $data1 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data1 =~ s/$tmp1/$tmp2/eg; $data1 = trim($data1);
			$tmp1 = "\""; $tmp2=" "; $data2 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data2 =~ s/$tmp1/$tmp2/eg; $data2 = trim($data2);
			$tmp1 = "\""; $tmp2=" "; $data3 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data3 =~ s/$tmp1/$tmp2/eg; $data3 = trim($data3);
			$tmp1 = "\""; $tmp2=" "; $data4 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data4 =~ s/$tmp1/$tmp2/eg; $data4 = trim($data4);
			$tmp1 = "\""; $tmp2=" "; $data5 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data5 =~ s/$tmp1/$tmp2/eg; $data5 = trim($data5);
			$tmp1 = "\""; $tmp2=" "; $data6 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data6 =~ s/$tmp1/$tmp2/eg; $data6 = trim($data6);
			$tmp1 = "\""; $tmp2=" "; $data7 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data7 =~ s/$tmp1/$tmp2/eg; $data7 = trim($data7);
			$tmp1 = "\""; $tmp2=" "; $data8 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data8 =~ s/$tmp1/$tmp2/eg; $data8 = trim($data8);
			$tmp1 = "\""; $tmp2=" "; $data9 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data9 =~ s/$tmp1/$tmp2/eg; $data9 = trim($data9);
			$tmp1 = "\""; $tmp2=" "; $dataa =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $dataa =~ s/$tmp1/$tmp2/eg; $dataa = trim($dataa);
			#
			# separa country/areacode
			# sometimes clients use one field only
			#  for 
			$v1 = clean_int($data1);
			$v2 = clean_int($data2);
			$v3 = $v1.$v2;
			if (  (($v1 eq "") && ($v2 ne ""))  || (($v1 ne "") && ($v2 eq "")) )   {
				$v4 = "";
				foreach (1..10) {
					$v5 = substr($v3,0,$_);
					if (index($country_codes_buffer,"|$v5|") ne -1) {$v4=$v5;}
				}
				if ($v4 ne "") {
					$data1 = $v4;
					$data2 = substr($v3,length($v4),1000);
				}
			}
			#
			# verifica country
			if ($line_error eq 0) {
				$data = $data1;
				if ( ($data eq "") || (clean_int($data) ne $data) )  {$line_error++; $line_error_message="Incorrect country code.";}
				if ($country ne "") {
					if ($data ne $country) {$line_error++; $line_error_message="Incorrect country code. You can only upload rates for country ($country) $country_name";}
				} 
			}
			# verifica arreacode
			if ($line_error eq 0) {
				$data = $data2;
				if (clean_int($data) ne $data)  {$line_error++; $line_error_message="Incorrect area code. ";}
			}
			# verifica name
			if ($line_error eq 0) {
				$data = $data3;
				$data = clean_str($data,"<>_-() ","MINIMAL");
				if ( ($data eq "") || (clean_str($data,"<>_- ","MINIMAL") ne $data) )  {$line_error++; $line_error_message="Incorrect area name. ";}
			}
			# verifia resolution
			if ($line_error eq 0) {
				$data = $data4;
				if ( (clean_int($data) ne $data) ||  ( (clean_int($data) eq $data) && (($data<1) || ($data>86400)) ) ){$line_error++; $line_error_message="Incorrect resolution. ";}
			}
			# verifica min_call_sec
			if ($line_error eq 0) {
				$data = $data5;
				if ( (clean_int($data) ne $data) ||  ( (clean_int($data) eq $data) && (($data<0) || ($data>86400)) ) ){$line_error++; $line_error_message="Incorrect minimum seconds. ";}
			}
			# verifica grace_seconds
			if ($line_error eq 0) {
				$data = $data6;
				if ( (clean_int($data) ne $data) ||  ( (clean_int($data) eq $data) && (($data<0) || ($data>86400)) ) ){$line_error++; $line_error_message="Incorrect grace seconds. ";}
			}
			# verifica call_limit
			if ($line_error eq 0) {
				$data = $data7;
				if ( (clean_int($data) ne $data) ||  ( (clean_int($data) eq $data) && (($data<0) || ($data>86400)) ) ){$line_error++; $line_error_message="Incorrect call_limit. ";}
			}
			# verifica rate_per_call
			if ($line_error eq 0) {
				$data = $data8;
				$data = sprintf("%f",$data);
				if ( ($data eq "") || ($data<0) || ($data>1000) ){ $line_error++; $line_error_message="Incorrect rate per call";}
			}
			# verifica rate_by_minute
			if ($line_error eq 0) {
				$data = $data9;
				$data = sprintf("%f",$data);
				if ( ($data eq "") || ($data<0) || ($data>1000) ){ $line_error++; $line_error_message="Incorrect rate per minute";}
			}
			# verifica asterisk string
			if ($line_error eq 0) {
				if ($dataa ne "") {
					$data = $dataa;
					$data = clean_str($data,"<>/[]_-()\@#. ","MINIMAL");
					if ( ($data eq "") || ($dataa ne $data) )  {$line_error++; $line_error_message="Incorrect asterisk_string. ";}
				}
			}
			# verifica country-areacode igual country
			if ($line_error eq 0) {
				$data = "|".$data1.$data2."|";
				if ($data2 ne "") {
					if (index($country_codes_buffer,$data) ne -1) {
						$line_error++; $line_error_message="I cannot use country $data1 with areacode $data2 because we have a country $data1$data2 ";
					}
				}
			}
			# verifica countr 1 vazio
			#if ($line_error eq 0) {
			#	if ( ($data1 eq "1") && ($data2 eq "") ) {
			#		$line_error++; $line_error_message="I cannot use country 1 with no areacode because we have many country start with 1";
			#	}
			#}
			# se tem erro, marcar o erro 
			if ($line_error eq 0) {
			} else {
				$total_errors++;
				$status_ok=0;
				$status_message="Error in CSV line $actual_line. ".$line_error_message." ";
				last;
			}
		}
		#
		# verifica se country=all and only one contry in this file
    }
    close(LOCAL);
    #
	#-------------------------------------------------
    # se ok, adiciona a database
	#-------------------------------------------------
    if ($status_ok eq 1) {
		$status_ok = 1;
		$status_message = "";
		if ($country eq "") {
			database_do("delete from product_rate_table_data where rate_id='$rate_id' ");
		} else {
			database_do("delete from product_rate_table_data where rate_id='$rate_id' and country='$country'  ");
		}
		open(LOCAL,$temp_file);
		$line = <LOCAL>;
		my @values;
		$i=0;
		while(<LOCAL>){
			chomp;
			$i++;
			$line = $_;
		    if (index($line,",") eq -1) {
				$tmp1 = "\t"; 
				$tmp2=","; 
				$line =~ s/$tmp1/$tmp2/eg;    	
		    }
			if (index($line,",") eq -1) {next}
			($data1,$data2,$data3,$data4,$data5,$data6,$data7,$data8,$data9,$dataa) = split(/\,/,$line);
			$tmp1 = "\""; $tmp2=" "; $data1 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data1 =~ s/$tmp1/$tmp2/eg; $data1 = trim($data1);
			$tmp1 = "\""; $tmp2=" "; $data2 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data2 =~ s/$tmp1/$tmp2/eg; $data2 = trim($data2);
			$tmp1 = "\""; $tmp2=" "; $data3 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data3 =~ s/$tmp1/$tmp2/eg; $data3 = trim($data3);
			$tmp1 = "\""; $tmp2=" "; $data4 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data4 =~ s/$tmp1/$tmp2/eg; $data4 = trim($data4);
			$tmp1 = "\""; $tmp2=" "; $data5 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data5 =~ s/$tmp1/$tmp2/eg; $data5 = trim($data5);
			$tmp1 = "\""; $tmp2=" "; $data6 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data6 =~ s/$tmp1/$tmp2/eg; $data6 = trim($data6);
			$tmp1 = "\""; $tmp2=" "; $data7 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data7 =~ s/$tmp1/$tmp2/eg; $data7 = trim($data7);
			$tmp1 = "\""; $tmp2=" "; $data8 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data8 =~ s/$tmp1/$tmp2/eg; $data8 = trim($data8);
			$tmp1 = "\""; $tmp2=" "; $data9 =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $data9 =~ s/$tmp1/$tmp2/eg; $data9 = trim($data9);
			$tmp1 = "\""; $tmp2=" "; $dataa =~ s/$tmp1/$tmp2/eg; $tmp1 = "\'"; $tmp2=" "; $dataa =~ s/$tmp1/$tmp2/eg; $dataa = trim($dataa);
			$v1 = clean_int($data1);
			$v2 = clean_int($data2);
			$v3 = $v1.$v2;
			if (  (($v1 eq "") && ($v2 ne ""))  || (($v1 ne "") && ($v2 eq "")) )   {
				$v4 = "";
				foreach (1..10) {
					$v5 = substr($v3,0,$_);
					if (index($country_codes_buffer,"|$v5|") ne -1) {$v4=$v5;}
				}
				if ($v4 ne "") {
					$data1 = $v4;
					$data2 = substr($v3,length($v4),1000);
				}
			}
			$query_search = $data1.$data2;
			#$sql  = "insert into product_rate_table_data  "; 
			#$sql .= "       (rate_id,     asterisk_string,  query_search,      country,   areacode, name,     resolution, min_call_seconds, grace_seconds, rate_per_call, rate_per_minute, rate_per_call_peak, rate_per_minute_peak, rate_per_call_reduced, rate_per_minute_reduced,  max_call_seconds,  max_call_seconds_peak,  max_call_seconds_reduced  ) "; 
			push(@values, " ('$rate_id',  '$dataa',         '$query_search',   '$data1',  '$data2', '$data3', '$data4',   '$data5',         '$data6',      '$data8',      '$data9',        '$data8',           '$data9',             '$data8',              '$data9',                 '$data7',          '$data7',               '$data7'                  )");
			#database_do($sql);
			if($i % 100 == 0){
				$sql  = "insert into product_rate_table_data  "; 
				$sql .= "       (rate_id,     asterisk_string,  query_search,      country,   areacode, name,     resolution, min_call_seconds, grace_seconds, rate_per_call, rate_per_minute, rate_per_call_peak, rate_per_minute_peak, rate_per_call_reduced, rate_per_minute_reduced,  max_call_seconds,  max_call_seconds_peak,  max_call_seconds_reduced  ) ";
				$sql .= " values " . join ", ", @values;
				database_do($sql);
				@values = ();
			}
		}
		$sql  = "insert into product_rate_table_data  "; 
		$sql .= "       (rate_id,     asterisk_string,  query_search,      country,   areacode, name,     resolution, min_call_seconds, grace_seconds, rate_per_call, rate_per_minute, rate_per_call_peak, rate_per_minute_peak, rate_per_call_reduced, rate_per_minute_reduced,  max_call_seconds,  max_call_seconds_peak,  max_call_seconds_reduced  ) ";
		$sql .= " values " . join ", ", @values;
		database_do($sql);
		$status_message = "Rate uploaded sucessfuly! <!-- $sql -->";
    }
    close(LOCAL);
    unlink ($temp_file);
	#
	#-------------------------------------------------
	# print page
	#-------------------------------------------------
    %t = ();
	$status = ($status_ok eq 1) ? "<font color=green><b>OK</b></font>" : "<font color=red><b>ERROR</b></font>";
    $t{my_url}	= $my_url;
    $t{title}	= "<a href=$my_url>Config</a> &#187; <a href=$my_url?action=rates_list>Calls rate/route</a> &#187; <a href=$my_url?action=rate_edit&rate_id=$rate_id&filter_country=$country>Edit</a> &#187; Upload rate";
    $t{title}	= "Upload CSV file to rate/route '$rate_name'";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Calls rate/route";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{breadcrumb}{3}{title}	= "Edit rate/route '$rate_name'";
    $t{breadcrumb}{3}{url}		= "$my_url?action=rate_edit&rate_id=$rate_id";
    $t{breadcrumb}{4}{title}	= "Upload CSV file";
    $t{breadcrumb}{4}{url}		= "";
    $t{content}	= qq[
	<br>
	<div class=clear style=width:300px;>
	<div class=alert_box>
	<div class=alert_box_inside>
	$status<br>$status_message
	</div>
	</div>
	</div><br>
	<a href=$my_url?action=rate_edit&rate_id=$rate_id&filter_country=$country>Return</a>
	];
    &template_print("template.html",%t);
}
sub do_rate_check(){
	#
	#-------------------------------------------------
	# check rate_id
	#-------------------------------------------------
	$number = &clean_int(substr($form{number},0,100));
	$rate_id = &clean_int(substr($form{rate_id},0,100));
	#
	#-------------------------------------------------
	# start search
	#-------------------------------------------------
	if ($rate_id eq "") {
		#
		#-------------------------------------------------
		# multiple rate_table check
		#-------------------------------------------------
		$html = "";
		$number_format_e164 = &format_E164_number($number,"E164");
		%hash = database_select_as_hash("SELECT id,name FROM product_rate_table","title");
	    foreach $rate_id (sort{$hash{$a}{title} cmp $hash{$b}{title}} keys %hash) {
	    	$rate_title = $hash{$rate_id}{title};
	    	$rate_value = "Not found";
	    	$rate_limit = "&nbsp;";
			%call_rate_data = &multilevel_rate_table_get($number,$rate_id);
			if ($call_rate_data{ok_to_use} eq 1) {
		    	$rate_value = "\$".&format_number($call_rate_data{rate_per_minute},2);
				$rate_limit	= "no limit";
				$rate_limit	= ($call_rate_data{rate_max_call_seconds}>0) ? &format_number($call_rate_data{rate_max_call_seconds},0)."Sec" : $rate_limit;
				$html .= qq[
					<tr>
					<td style="font-size:10px;" ><a target=check_io onclick="check_loading();" href="$my_url?action=rate_check&number=$number&rate_id=$rate_id">$rate_title</a></td>
					<td style="font-size:10px;" class=ar>$rate_value</td>
					<td style="font-size:10px;" class=ar>$rate_limit</td>
					</tr>
				];
			} else {
				$html .= qq[
					<tr>
					<td style="font-size:10px;" ><a target=check_io onclick="check_loading();" href="$my_url?action=rate_check&number=$number_format_e164&rate_id=$rate_id">$rate_title</a></td>
					<td style="font-size:10px;color: #c0c0c0;" class=ar colspan=2>Not found</td>
					</tr>
				];
			}
		}
		$html = qq[
			Search: $number <br>
			E164 format: $number_format_e164 <br>
			<hr>
			<table width=100%>
			<thead>
				<tr>
				<td style="font-size:10px;" ><b>Rate table</b></td>
				<td style="font-size:10px;" class=ar><b>Rate</b></td>
				<td style="font-size:10px;" class=ar><b>Limit</b></td>
				</tr>
			</thead>
			<tbody>$html</tbody>
			</table>
		];
	} else {
		#
		#-------------------------------------------------
		# single rate_table check
		#-------------------------------------------------
		%hash = database_select_as_hash("SELECT 1,1,name FROM product_rate_table where id='$rate_id' ","flag,name");
		if ($hash{1}{flag} ne 1) { 
		    %t = ();
		    $t{dic}{content}	= qq[
			<div id=data>Error</div>
			<script>
			obj = document.getElementById("data");
			parent.check_ready(obj.innerHTML);
			</script>
		    ];
		    &template_print("template.html",%t);
			exit; 
		}
		$rate_name = $hash{1}{name};
		%country_codes = database_select_as_hash("SELECT code,name FROM country");
		#
		#-------------------------------------------------
		# check rate_id
		#-------------------------------------------------
		$number_format_usa = &format_E164_number($number,"USA");
		$number_format_e164 = &format_E164_number($number,"E164");
		%call_rate_data = &multilevel_rate_table_get($number,$rate_id);
		if ($call_rate_data{ok_to_use} eq 1) {
			$tmp = $call_rate_data{asterisk_string_raw};
			$tmp1=">"; $tmp2="&gt;"; $tmp =~ s/$tmp1/$tmp2/g;
			$tmp1="<"; $tmp2="&lt;"; $tmp =~ s/$tmp1/$tmp2/g;
			if ($call_rate_data{ok_to_use} eq 1) {
				$value_per_1hr	= &format_number($call_rate_data{rate_per_minute}*60,2);
				$time_per_1 	= &format_time(60*(1/$call_rate_data{rate_per_minute}));
				$rate_per_minute= &format_number($call_rate_data{rate_per_minute},2);
				$rate_per_call 	= &format_number($call_rate_data{rate_per_call},2);
				$tmp_limit 		= "No limit (limit by balance)";
				$tmp_limit 		= ($call_rate_data{rate_max_call_seconds}>0) ? &format_number($call_rate_data{rate_max_call_seconds},0)." Seconds" : $tmp_limit;
				
				$html = qq[
				Status: <b>Rate found and ok</b><br>
				Search: $number <br>
				E164 format: $number_format_e164 <br>
				rete table id: $rate_id<br>
				<hr>
				Country: $call_rate_data{rate_country} '$country_codes{$call_rate_data{rate_country}}'<br>
				Areacode: $call_rate_data{rate_areacode} '$call_rate_data{rate_name}'<br>
				Rate per call: us\$$rate_per_call<br>
				Rate per minute: us\$$rate_per_minute<br>
				Call limit: $tmp_limit<br>
				<hr>
				Time per us\$1,00: $time_per_1<br>
				One hour for: us\$$value_per_1hr<br>
				<hr>
				DST dial template: $tmp<br>
				DST dial: $call_rate_data{asterisk_string}<br>
				];
			} else {
				$html = qq[
				Status: <b>Rate found but blocked</b><br>
				Search: $number <br>
				E164 format: $number_format_e164 <br>
				Country: $call_rate_data{rate_country} '$country_codes{$call_rate_data{rate_country}}'<br>
				Areacode: $call_rate_data{rate_areacode} '$call_rate_data{rate_name}'<br>
				DST format: $tmp<br>
				DST dial: $call_rate_data{asterisk_string}<br>
				];
			}
		} else {
			$html = qq[
			Status: <b>Rate NOT found</b><br>
			Search: $number <br>
			E164 format: $number_format_e164 <br>
			];
		}
	}
	#
	#-------------------------------------------------
	# print page
	#-------------------------------------------------
    %t = ();
    $t{dic}{my_url}	= $my_url;
    $t{dic}{title}	= "<a href=$my_url>Config</a> &#187; <a href=$my_url?action=rates_list>Calls rate/route</a> &#187; <a href=$my_url?action=rate_edit&rate_id=$rate_id>Edit</a> &#187; Check rate";
    $t{dic}{content}	= qq[
	<div id=data>$html</div>
	<script>
	obj = document.getElementById("data");
	parent.check_ready(obj.innerHTML);
	</script>
    ];
    &template_print("template.html",%t);

}
sub do_rate_edit(){
	#
	#-------------------------------------------------
	# check rate_id
	#-------------------------------------------------
	$rate_id = &clean_int(substr($form{rate_id},0,100));
	%hash = database_select_as_hash("SELECT 1,1,name FROM product_rate_table where id='$rate_id' ","flag,name");
	if ($hash{1}{flag} ne 1) { &cgi_redirect("$my_url?action=rates_list"); exit; }
	$rate_name = $hash{1}{name};
	#
	#-------------------------------------------------
	# get basic data
	#-------------------------------------------------
	%country_codes = database_select_as_hash("SELECT code,name FROM country");
	#
	#-------------------------------------------------
	# try to save rate basic data
	#-------------------------------------------------
	$error_message = "";
	if ($form{save} ne "") {
		if (&multilevel_clickchain_check("cre",$form{save}) eq 1) {
			$form{name} = &clean_str(substr($form{name},0,255)," ()[],-_.");
			if ($form{name} eq "") { $error_message = "I need a name";}
			if ($error_message eq "") {
				$sql = "update product_rate_table set name='$form{name}' where id='$rate_id' ";
				&database_do($sql);
				cgi_redirect("$my_url?action=rates_list");
				exit;
			}
		}
	}
	#
	#-------------------------------------------------
	# load data on form
	#-------------------------------------------------
	if ($form{save} eq "") {
		$form{name} = $rate_name;
	}
	#
	#-------------------------------------------------
	# get rate list
	#-------------------------------------------------
	$form{filter_country} = &clean_int(substr($form{filter_country},0,100));
	$form{filter_country} = (exists($country_codes{$form{filter_country}})) ? $form{filter_country} : "";
	$form{filter_country_name} =(exists($country_codes{$form{filter_country}})) ? $country_codes{$form{filter_country}} : "All";
	#
	# select filter
	%hash = database_select_as_hash("SELECT distinct country,1 FROM product_rate_table_data where rate_id='$rate_id' ","flag");
	$tmp1= "";
	$tmp2= "";
	foreach $id (sort{$country_codes{$a} cmp $country_codes{$b}} keys %country_codes){
		$tmp = ($form{filter_country} eq $id) ? "selected" : "";
		if (exists($hash{$id})) {
			$tmp1 .= "<option $tmp value=$id>&nbsp;&nbsp;$country_codes{$id}</option>";
		} else {
			$tmp2 .= "<option $tmp value=$id>&nbsp;&nbsp;$country_codes{$id}</option>";
		}
	}
	$select_country = "<option>All rates</option>";
	$select_country .= "<option>&nbsp;</option>";
	$select_country .= "<option>&#187; Country with rate</option>$tmp1";
	$select_country .= "<option>&nbsp;</option>";
	$select_country .= "<option>&#187; Country without rate</option>$tmp2";
	$select_country .= "<option>&nbsp;</option>";
	#
	# sql filter
	$filter_sql = "";
	$filter_sql = (exists($country_codes{$form{filter_country}})) ? " and country='$form{filter_country}' " : $filter_sql;
	#
	# separa por paginacao
	%hash = database_select_as_hash("SELECT 1,1,count(*) FROM product_rate_table_data where rate_id='$rate_id' $filter_sql ","flag,qtd");
	$quantity 	= ( ($hash{1}{flag} eq 1) && ($hash{1}{qtd}>0) ) ? $hash{1}{qtd} : 0;
	$page_size	= 12;
	$page_min	= 1;
	$page_max	= int(($quantity-1)/$page_size)+1;
	$page_max	= ($page_max<$page_min) ? $page_min : $page_max;
	$page 		= clean_int($form{page});
	$page 		= ($form{next} eq 1) ? $page+1 : $page;
	$page 		= ($form{previous} eq 1) ? $page-1 : $page;
	$page 		= ($page<$page_min) ? $page_min : $page;
	$page 		= ($page>$page_max) ? $page_max : $page;
	$sql_limit	= ($page-1)*$page_size;
	#
	# monta query
	$sql = "
	select country,areacode,name,resolution,min_call_seconds,rate_per_minute,asterisk_string,max_call_seconds,rate_per_call
	from product_rate_table_data 
	where rate_id='$rate_id' $filter_sql
	order by country,areacode
	limit $sql_limit,$page_size
	";
	%rates = database_select_as_hash_with_auto_key($sql, "country,areacode,name,resolution,min_call_seconds,rate_per_minute,asterisk_string,max_call_seconds,rate_per_call");
	$rate_list  = "";
	$rate_list_empty = "<tr><td colspan=7><center>Empty...</center></td></tr>";
	foreach $id (sort{$a <=> $b} keys %rates){
		$rate_list_empty ="";
		$country_name = (exists($country_codes{$rates{$id}{country}})) ? $country_codes{$rates{$id}{country}} : "(Unknown country)";
		$rate_list .= "<tr>";
		$rate_list .= "<td class=al>($rates{$id}{country}) $country_name</td>";
		$rate_list .= "<td class=al>($rates{$id}{areacode}) $rates{$id}{name}</td>";
		if ($rates{$id}{asterisk_string} eq "") {
			$rate_list .= "<td colspan=5 class=ac>blocked</td>";
		} else {
			$tmp = $rates{$id}{asterisk_string};
			$tmp1=">"; $tmp2="&gt;"; $tmp =~ s/$tmp1/$tmp2/g;
			$tmp1="<"; $tmp2="&lt;"; $tmp =~ s/$tmp1/$tmp2/g;
			$tmplimit = $rates{$id}{max_call_seconds} || "";
			$tmplimit = ( ($tmplimit eq "") || ($tmplimit<=0) ) ? "&nbsp;" : &format_number($tmplimit,0)."sec";
			$rate_list .= "<td class=ar>".format_number($rates{$id}{resolution},0)."/".format_number($rates{$id}{min_call_seconds},0)."</td>";
			$rate_list .= "<td class=ar>$tmplimit</td>";
			$rate_list .= "<td class=ar>\$".format_number($rates{$id}{rate_per_call},5).	"</td>";
			$rate_list .= "<td class=ar>\$".format_number($rates{$id}{rate_per_minute},5).	"</td>";
			$rate_list .= "<td class=ar>$tmp</td>";
		}
		$rate_list .= "</tr>";
	}
	$rate_list .= $rate_list_empty;
	#
	#-------------------------------------------------
	# print page
	#-------------------------------------------------
	$select_pages = "";
	$tmp1 = &format_number($page_max,0);
	foreach($page_min..$page_max) {
		$tmp = ($_ eq $page) ? "selected" : ""; 
		$select_pages .= "<option $tmp value=$_>Page: ". &format_number($_,0). " of $tmp1</option>";
	}
	$save_id = &multilevel_clickchain_set("cre");
	$error_message = ($error_message eq "") ? "" : "<div class=alert_box><div>$error_message</div></div><br>";
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Edit rate/route '$rate_name'";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Calls rate/route";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{breadcrumb}{3}{title}	= "Edit rate/route '$rate_name'";
    $t{breadcrumb}{3}{url}		= "$my_url?action=rate_edit&rate_id=$rate_id";
    $t{content}	= qq[
    
	<script>
	function check_loading(){
		MyHTML("check_data","<img src=/design/img/loading.gif align=left>&nbsp;Please wait!")
	}
	function check_ready(html){
		MyHTML("check_data",html);
	}
	</script>
    
    
    <table class=clear border=0 colspan=0 cellpadding=0 cellspacing=0 ><tr>

	    <td width=280 valign=top><div class=clear style=width:280px>
			<fieldset style=width:auto;><legend>Name</legend>
				<div id=change_question >
					<form action=$my_url>
					Name:<br><input name=name value="$form{name}" readonly disabled style="width:100%"><br>
					<button type=button onclick="MyDisplay('change_question',0);MyDisplay('change_form',1);">Edit</button>
					</form>
				</div>
				<div id=change_form style=display:none>
					<form action=$my_url>
					Name:<br><input name=name value="$form{name}" style="width:100%"><br>
					<input type=hidden name=action value=rate_edit>
					<input type=hidden name=save value=$save_id>
					<input type=hidden name=rate_id value=$rate_id>
					$error_message 
					<button type=button class="button button_positive button_cancel"	onclick="MyDisplay('change_question',1);MyDisplay('change_form',0);">Cancel</button>
					<button type=submit class="button button_positive button_save"  	onclick="modal_loadingblock()" >Save</button>
					</form>
				</div>
			</fieldset>
			<br>
			<fieldset style="width:auto;height:140px;"><legend>Tools</legend>
				<div class=clear id=down>
					Upload and download rate table as CSV file.<br><br>
					<form action=$my_url> 
					<input type=hidden name=country value=$form{filter_country}>
					<input type=hidden name=action value=rate_download>
					<input type=hidden name=rate_id value=$rate_id>
					<button type=submit class="button button_positive "  >Download CSV</button>
					<button type=button class="button button_positive "	onclick="MyDisplay('up',1);MyDisplay('down',0);">Upload CSV</button>
					</form>
				</div>
				<div class=clear id=up style=display:none;>
					All current date will be replaced with CSV data you upload..<br><br>
					<form action=$my_url method=post enctype="multipart/form-data" >
					Select CSV file with rates to upload:<br>
					<input name=FileUpload type=file><br>
					<input type=hidden name=country value=$form{filter_country}>
					<input type=hidden name=action value=rate_upload>
					<input type=hidden name=rate_id value=$rate_id>
					<input type=hidden name=save value=$save_id>
					<button type=button class=""	onclick="MyDisplay('up',0);MyDisplay('down',1);">Cancel</button>
					<button type=submit class="" onclick="modal_loadingblock();" >Upload and replace data</button>
					</form>
				</div>
				<div class=clear id=wait style=display:none;>
				<img src=/design/img/loading.gif align=left>&nbsp;Upload rates... please wait!
				</div>
			</fieldset>
		</div></td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>

	    <td width=280 valign=top><div class=clear style=width:280px>
			<fieldset style="width:auto;height:300px;"><legend>Statistics</legend>
			<font color=#c0c0c0>not finished...</font>
			</fieldset>
		</div></td>
		<td>&nbsp;&nbsp;&nbsp;&nbsp;</td>

	    <td width=350 valign=top><div class=clear style=width:350px>
			<fieldset class=config_select_list style="padding-right:0px"><legend>Test</legend>
			<div style="height:270px;overflow-x:hidden; overflow-y:auto; padding-right:20px; ">
				<form action=$my_url target=check_io> 
				Number to test (E164 format):<br>
				<input name=number style=width:100%><br>
				<button type=submit class="button button_positive "	onclick="check_loading()";>Test</button>
				<input type=hidden name=action value=rate_check>
				<input type=hidden name=rate_id value=$rate_id>
				</form>
				<br>
				<div class=clear id=check_data style="font-size:10px; line-height:150%; overflow:hidden; white-space: nowrap; border:0px solid green;"></div>
				<iframe id=check_io name=check_io style="display:none;"></iframe>
			</div>
			</fieldset>
		</div></td>

	</tr></table>
	<br>
    
    
		
	<a name=rate ></a>
	<form action=$my_url#rate>
		<table border=0 colspan=0 cellpadding=0 cellspacing=0 class=WindowsTable width=940 >
		<thead>
			<tr>
			<td>Country</td>
			<td>Areacode</td>
			<td width=50>Round<br>res/min</td>
			<td width=50>Call<br>limit</td>
			<td width=50>Rate per<br>call</td>
			<td width=50>Rate per<br>minute</td>
			<td width=170>Asterisk string</td>
			</tr>
		</thead>
		<tbody >
			$rate_list 
		</tbody>
		<tfoot>
			<tr><td colspan=8 style=border:0px><h1>
			<button style="float:left;" type=submit name=previous value=1><img src=/design/icons/bullet_arrow_left.png hspace=0 vspace=0 border=0 width=16 height=16></button>
			<select style="float:left;" name=filter_country onchange="this.form.submit()">$select_country</select>
			<select style="float:left;" name=page onchange="this.form.submit()">$select_pages</select>
			<button style="float:left;" type=submit name=next value=1><img src=/design/icons/bullet_arrow_right.png hspace=0 vspace=0 border=0 width=16 height=16></button>
			&nbsp;&nbsp;
			</h1></td></tr>
		</tfoor>
		</table>
	<input type=hidden name=action value=rate_edit>
	<input type=hidden name=rate_id value=$rate_id>
	</form>



    ];
    &template_print("template.html",%t);
}
sub do_rate_add(){
	#
	# try to save
	$error_message = "";
	if ($form{save} ne "") {
		if (&multilevel_clickchain_check("cra",$form{save}) eq 1) {
			$form{name} = &clean_str(substr($form{name},0,255)," ()[],-_.");
			if ($form{name} eq "") { $error_message = "I need a name";}
			if ($error_message eq "") {
				$sql = "insert into product_rate_table (name) values ('$form{name}') ";
				&database_do($sql);
				cgi_redirect("$my_url?action=rates_list");
				exit;
			}
		}
	}
    #
    # print page
	$save_id = &multilevel_clickchain_set("cra");
	$error_message = ($error_message eq "") ? "" : "<div class=alert_box><div>$error_message</div></div><br>";
    %t = ();
    $t{my_url}	= $my_url;
    $t{title}	= "Create new rate/route table";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Calls rate/route";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{breadcrumb}{3}{title}	= "Create new rate/route table";
    $t{breadcrumb}{3}{url}		= "$my_url?action=rate_add";
    $t{content}	= qq[
	<div class=clear style=width:300px>
		<fieldset class=config_select_list><legend>Create new calls rates/route</legend>
			Select name for this new rates/route and click save.<br>
			<br>
			<form action=$my_url>
			<input name=name value="$form{name}" style="width:100%"><br>
			<br>
			<input type=hidden name=action value=rate_add>
			<input type=hidden name=save value=$save_id>
			$error_message 
			<button type=button class="cancel"	onclick="window.location='$my_url?action=rates_list'">Cancel</button>
			<button type=submit class="save"  	onclick="modal_loadingblock()">Save</button>
			</form>
		</fieldset>
	</div>
    ];
    &template_print("template.html",%t);
}
sub do_rate_del(){
	#
	# check rate_id
	$rate_id = &clean_int(substr($form{rate_id},0,100));
	%hash = database_select_as_hash("SELECT 1,1,name FROM product_rate_table where id='$rate_id' ","flag,name");
	if ($hash{1}{flag} ne 1) { &cgi_redirect("$my_url?action=rates_list"); exit; }
	$rate_name = $hash{1}{name};
	#
	# get data
	$error_message = "";
	$rate_in_use = 0;
	foreach $index (1..9) {
		$sql = "select 1,1,count(*) from service_status	where rate_slot_$index = '$rate_id' ";
		%hash = database_select_as_hash($sql,"flag,value");
		if ($hash{1}{flag} eq 1) {
			$rate_in_use += $hash{1}{value};
		} else {
			$rate_in_use++;
		}
	}
	$tmp = &data_get("adm_data","rate","public");
	$rate_in_use += ($tmp eq $rate_id) ? 1 : 0;
	if ($rate_in_use > 0) { $error_message = "This rate/route table is in use in $rate_in_use points. I cannot delete";}
	#
	# try to save
	if ( ($form{save_id} ne "") && ($error_message eq "") ) {
		if (&multilevel_clickchain_check("rd",$form{save_id}) eq 1) {
			database_do("delete from product_rate_table_data where rate_id='$rate_id' ");
			database_do("delete from product_rate_table where id='$rate_id' ");
			cgi_redirect("$my_url");
			return;
		} else {
			$error_message = "Internal error. I cannot delete this rate. Try again";
		}
	}
	$error_message = ($error_message ne "") ? "<div class=alert_box><div>$error_message</div></div><br>" : "";
    %t = ();
	$t{save_id} = &multilevel_clickchain_set("rd");
    $t{my_url}	= $my_url;
    $t{title}	= "<a href=$my_url>Config</a> &#187; <a href=$my_url?action=rates_list>Calls rate/route</a> &#187; Edit";
    $t{title}	= "Delete rate/route '$rate_name'";
    $t{breadcrumb}{1}{title}	= "System settings";
    $t{breadcrumb}{1}{url}		= "config.cgi";
    $t{breadcrumb}{2}{title}	= "Calls rate/route";
    $t{breadcrumb}{2}{url}		= "$my_url";
    $t{breadcrumb}{3}{title}	= "Delete rate/route '$rate_name'";
    $t{breadcrumb}{3}{url}		= "$my_url?action=rate_edit&rate_id=$rate_id";
    $t{content}	= qq[
	<div class=clear style=width:300px>
		$error_message
		<fieldset>
			Do you really want delete rate/route '$rate_name'? This action cannot be undone.<br><br>
			<form action=$my_url>
			<input type=hidden name=action value=rate_del>
			<input type=hidden name=rate_id value=$rate_id>
			<input type=hidden name=save_id value=$t{save_id}>
			<button type=button class="cancel"	onclick="window.location='$my_url'">Cancel</button>
			<button type=submit class="save"  	onclick="modal_loadingblock()">Delete</button>
			</form>
		</fieldset>
	</div>
    ];
    &template_print("template.html",%t);
}

#=======================================================
