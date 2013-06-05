#!/usr/bin/perl
require "include.cgi";
#=======================================================
# logout if no session
#=======================================================
if ($app{session_status} ne 1) {cgi_redirect("index.cgi");exit;}
if (&active_user_permission_check("noc:can_edit_pages") ne 1) {adm_error("no permission"); exit;}
#=======================================================




#=======================================================
# settings
#=======================================================
%data = ();
$data{"0.Website"}{"0.About"}{"0.About ZenoFon"}	= "about/index.html";
$data{"0.Website"}{"0.About"}{"1.Terms of Service"}	= "about/termsofservice.html";
$data{"0.Website"}{"0.About"}{"2.Privacy Policy"}	= "about/privacypolicy.html";
$data{"0.Website"}{"0.About"}{"3.Contact us"}		= "contact/index.html";
$data{"0.Website"}{"0.About"}{"4.Public rate page"}	= "design/template.about.rate.html";
$data{"0.Website"}{"0.About"}{"5.Public radio page"}	= "design/template.about.radio.html";
$data{"0.Website"}{"1.Services"}{"0.View"} 		= "design/template.services.html";
$data{"0.Website"}{"1.Services"}{"1.Sign-in"} 	= "design/template.pbx.add.html";
$data{"0.Website"}{"2.My account"}{"0.Login"} 					= "design/template.myaccount.login.html";
$data{"0.Website"}{"2.My account"}{"1.Login - Restore PIN"}		= "design/template.myaccount.login.restore.html";
$data{"0.Website"}{"2.My account"}{"2.Setup"}					= "design/template.pbx.overview.html";
$data{"0.Website"}{"2.My account"}{"3.Setup - ANI"}				= "design/template.pbx.ani.html"; 
$data{"0.Website"}{"2.My account"}{"4.Setup - Phone DST"}		= "design/template.pbx.dst.html";
$data{"0.Website"}{"2.My account"}{"5.Setup - Skype DST"}		= "design/template.pbx.dst.skype.html";
$data{"0.Website"}{"2.My account"}{"6.Friends"}					= "design/template.myaccount.friends.html";
$data{"0.Website"}{"2.My account"}{"7.Calls"}					= "design/template.myaccount.calls.html";
$data{"0.Website"}{"2.My account"}{"8.Credits"}					= "design/template.myaccount.credits.html";
$data{"0.Website"}{"2.My account"}{"9.credits - CC Profile"}	= "design/template.myaccount.credits.profile.html";
$data{"0.Website"}{"2.My account"}{"a.Credits - Auto recharge"}	= "design/template.myaccount.credits.add.cim.automatic.html";
$data{"0.Website"}{"2.My account"}{"b.Credits - Credit card"}	= "design/template.myaccount.credits.add.cim.manual.html";
$data{"0.Website"}{"2.My account"}{"c.Credits - Commission"}	= "design/template.myaccount.credits.add.commission.html";
$data{"0.Website"}{"2.My account"}{"d.Credits - Phone recharge"}= "design/template.myaccount.credits.add.cim.phone.html";
$data{"0.Website"}{"2.My account"}{"e.Promotions"}				= "design/template.myaccount.coupons.html";
$data{"0.Website"}{"2.My account"}{"5.Setup - Radio DST"}		= "design/template.pbx.dst.radio.html";
$data{"0.Website"}{"2.My account"}{"f.Setup - Add Your Radio Station"}		= "design/template.pbx.radio.html";
$data{"0.Website"}{"3.Help"}{"0.Main help"}		= "design/template.help.start.html";
$data{"0.Website"}{"3.Help"}{"1.Show group"}	= "design/template.help.group.html";
$data{"0.Website"}{"3.Help"}{"2.Show search"}	= "design/template.help.search.html";
$data{"0.Website"}{"3.Help"}{"3.Show topic"}	= "design/template.help.topic.html";
$data{"0.Website"}{"4.Radio"}{"0.Public radio list"}	= "design/template.radio.html";
$data{"1.Global texts"}{"0.Top page messages"}	= "design/template.js";
$data{"1.Global texts"}{"1.Top menu"}{"0.Disabled"}	= "design/template.include.top.menu.0.html";
$data{"1.Global texts"}{"1.Top menu"}{"1.My account selected"}	= "design/template.include.top.menu.3.html";
$data{"1.Global texts"}{"1.Top menu"}{"2.Help selcted"}	= "design/template.include.top.menu.4.html";
$data{"1.Global texts"}{"2.Include footer"}	= "design/template.include.bot.html";
%data_files = ();
%data_names = ();
$data_files_index = 0;
sub data_tree_loop(){
	local ($div_id,%hash) = @_;
	local ($html,$n,$v);
    $html = "";
    $html .= "<ul id=$div_id style='list-style-type:none; padding:0px; margin:0px;' >";
	foreach $n (sort{$a cmp $b} keys %hash) {
	    $v = $hash{$n}."";
	    $html .= "<li style='padding:1px;padding-left:19px;'>";
	    if (  (index($v,".html") ne -1) || (index($v,".txt") ne -1) || (index($v,".js") ne -1) || (index($v,".css") ne -1) )  {
	    	if ($form{id} eq $data_files_index) {
			    $html .= "<a class=link_selected href=$my_url?action=edit&id=$data_files_index><img src=/design/icons/page.png border=0 hspace=0 vspace=0 style='float:left; padding-top:1px;margin-right:3px;'>".substr($n,2,100)."</a>";
	    	} else {
			    $html .= "<a href=$my_url?action=edit&id=$data_files_index><img src=/design/icons/page.png border=0 hspace=0 vspace=0 style='float:left; padding-top:1px;margin-right:3px;'>".substr($n,2,100)." </a>";
	    	}
			$data_files{$data_files_index} = $v;
			$data_names{$data_files_index} = substr($n,2,100);
		    $data_files_index++;
	    } else {
		    $html .= "<a href=javascript:MyDisplay('dt_$v')><img src=/design/icons/folder.png border=0 hspace=0 vspace=0 style='float:left; margin-top:1px;margin-right:3px;'>".substr($n,2,100)."</a>";
	    }
	    $html .= &data_tree_loop("dt_$v",%{$hash{$n}});
	    $html .= "</li>";
	}
    $html .= "</ul>";
    return $html;
}
$files_list_html = &data_tree_loop("dv_root",%data);
$selected_file_id = $form{id};
$selected_file_found = 0;
$selected_file_path = "";
$selected_file_name = "";
if (exists($data_files{$selected_file_id})){
    $selected_file_path =$app_root."/www/".$data_files{$selected_file_id};
	$selected_file_name = $data_names{$selected_file_id};
    if (-e $selected_file_path){
		$selected_file_found = 1;
    }
}
#=======================================================





#=======================================================
# main loop
#=======================================================
$my_url = "website.pages.cgi";
$action = $form{action};
if 		($action eq "save")		{ &do_save(); } 
elsif 	($action eq "edit")		{ &do_edit(); }
else							{ &do_list(); }
exit;
#=======================================================



#========================================================================
# actions
#========================================================================
sub do_list(){
    #
    # print page
    %t = ();
	$t{dic}{title}		= "<a href=config.cgi>Settings</a> &#187; <a href=$my_url>Website pages</a>";
    $t{dic}{content}	= qq[
    <fieldset style=width:250px;>$files_list_html</fieldset>
    ];
    &template_print("template.html",%t);
}
sub do_edit(){
	local ($msg) = @_;
    #
    # no file, no edit
    if ($selected_file_found ne 1) {&do_list();return}
    #
    # get backup list
    $bkp_path = $app_root."/data/templates-backup/". clean_str($selected_file_path,"MINIMAL") .".*";
    $cmd  = "ls -1t $bkp_path | head -n 100";
    $backup_select = "";
    $backup_id = "";
    $backup_name = "";
    foreach $line (`$cmd`){
    	chomp($line);
    	($tmp1,$tmp2) = split(/\./,$line);
    	$tmp3 = &format_time_time($tmp2);
	    $backup_select .= "<option value=$tmp2>$tmp3</option>";
		if ($tmp2 eq $form{load_from_backup}) {
			$backup_id = $tmp2;
			$backup_name = $tmp3;
		}
    }
    #
    # check and load template
    $file = $selected_file_path;
    $buf = "";
    if ($backup_id eq "") {
	    open(IN,$file);
	    while(<IN>){$buf .= $_;}
	    close(IN);
    } else {
	    $backup_file = $app_root."/data/templates-backup/". clean_str($selected_file_path,"MINIMAL") .".$backup_id";
	    open(IN,$backup_file);
	    while(<IN>){$buf .= $_;}
	    close(IN);
	    $msg = "Loaded from backup ". $backup_name;
    }
    $tmp1 = "<textarea";
    $tmp2 = "&lt;textarea";
    $buf =~ s/$tmp1/$tmp2/eg;
    $tmp1 = "</textarea";
    $tmp2 = "&lt;/textarea";
    $buf =~ s/$tmp1/$tmp2/eg;
    $tmp1 = "&";
    $tmp2 = "&amp;";
    $buf =~ s/$tmp1/$tmp2/eg;
    #
    # create form
	$msg = ($msg eq "") ? "" : "<script>alert('$msg')</script>";
    $html = qq[

<style>
.link_selected{
	background-color:#5d788c;
	color:#ffffff;
	padding:3px;
	font-weight:bold;
	padding-bottom:3px;	
	padding-top:3px;	
}
.link_selected:hover{
	color:#ffffff;
}
</style>


	<table width=100% border=0 colspan=0 cellpadding=0 cellspacing=0 class=clear >
	<td valign=top width=250>
	    <fieldset style=width:250px;>$files_list_html</fieldset>
	</td>
	<td width=20>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>    
	<td valign=top>
	    <h2>Edit page '$selected_file_name'</h2>
	    Path: $selected_file_path<br>
	    <form action=$my_url method=post>
	    <input type=hidden name=start value=1>
	    <textarea wrap=off name=text style="width:100%; height:300px;">$buf</textarea><br>
	    <input type=hidden name=id value=$selected_file_id>
	    <input type=hidden name=backupid value=$form{backupid}>
	    <input type=hidden name=action value=save>
	    <button style=float:right type=submit class=save >Save changes</button>
	    <button style=float:right type=button class=cancel onclick="window.location='$my_url'">Close file</button>
	    <input type=hidden name=stop value=1>
	    </form>

		<div id=load_question style=float:left >
	    <button style=float:left type=button onclick="MyDisplay('load_question',0);MyDisplay('load_form',1);">Load from backup</button>
		</div>
		<div id=load_form style=float:left;display:none >
		    <form action=$my_url method=post>
		    <input type=hidden name=id value=$selected_file_id>
		    <input type=hidden name=action value=edit>
		    <select style=float:left; name=load_from_backup>
			    <option>Select backup file...</option>
			    <option> </option>
			    $backup_select 
			    <option> </option>
		    </select>
		    <button style=float:left; type=button onclick="MyDisplay('load_question',1);MyDisplay('load_form',0);">Cancel</button>
		    <button style=float:left; type=submit >Load</button>
		    </form>
		</div>
	</td>
	</table>
	$msg 
    ];
    #
    # print page
    %t = ();
	$t{dic}{title}	= "<a href=config.cgi>Settings</a> &#187; <a href=$my_url>Website pages</a> &#187; Edit '$selected_file_name'";
    $t{dic}{content}	= $html;
    &template_print("template.html",%t);
    
}
sub do_save(){
    #
    # no file, no edit
    if ($selected_file_found ne 1) {&do_list();return}
    if ($form{start}.$form{stop} ne "11") {adm_error("Internal error. Try again.");return}
    #
    # check and load template
    $file = $selected_file_path;
    #
    # save and backup
    $msg = "File saved";
    $tmp = substr(&clean_int($form{backupid}),0,100);
    if ( ($tmp eq "") || ($tmp ne $form{backupid}) ){
    	$form{backupid} = time;
	    $msg = "First save. New backup created.";
    }
    $file_bkp = $app_root."/data/templates-backup/". clean_str($file,"MINIMAL") .".". $form{backupid};
    copy($file,$file_bkp);
    open(OUT,">$file");
    print OUT $form{text};
    close(OUT);
    #
    # manda pra listar
    &do_edit($msg);
}
#========================================================================



