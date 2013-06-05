#!/usr/bin/perl
require "include.cgi";

$id   = &clean_int($form{id});
%hash = &database_select_as_hash("select id,id,title,short_descr,big_description,logo from radio_data_station where id='$id'", "id,title,short_descr,big_description,logo"); 
%t    = ();
$t{id} = $id;
if ($hash{$id} && $hash{$id}{id}) {    
    $t{title}           = $hash{$id}{title};
    $t{short_descr}     = $hash{$id}{short_descr};
    $t{did_list}        = join (",", database_select_as_array("select did  from radio_data_did where radio_data_station_id='$id'"));
    $t{big_description} = $hash{$id}{big_description};
    $t{logo}            = $hash{$id}{logo};
} else {
    $t{stations_loop_has_no_itens} = 1;
} 
#
# -----------------------------
# print page
# -----------------------------
&website_template_print("station.html",%t);