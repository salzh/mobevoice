#!/usr/bin/perl
use Data::Dumper;
require "../include.cgi";



#=======================================================
# main loop
#=======================================================
&ip_flood_surge_protection("Public rate search");
&do_search_number_and_list_country();
exit;
#=======================================================




#=======================================================
# actions
#=======================================================
sub do_search_number_and_list_country(){
	#
	# start 
    %t = ();
   
   #the config target is rate,not public_rate,the name is public ,not rate_id_country_list
#	$rate_id_country_list 	= &data_get("adm_data","public_rate","rate_id_country_list");
	$rate_id_country_list 	= &data_get("adm_data","rate","public");
	$rate_id_country_list	= $rate_id_country_list || 14; # for web only
	
	

	$status_id_search_rate	= &data_get("adm_data","public_rate","status_id_search_rate");
	$status_id_search_rate	= $status_id_search_rate || 21; # pay as you go good client

	#
	# get and clean number input 
	$t{number_user_input} = &clean_int(substr($form{number},0,100));
	($t{number_status},$t{number_e164},$t{number_country}) = &multilevel_check_E164_number($t{number_user_input});
	$t{number} = ($t{number_status} eq "OK") ? &format_E164_number($t{number_e164},"USA") : $t{number_user_input}; 
	#
	# try to search rates for this number
	if ($t{number_user_input} ne "") {
		$t{search_exists} = 1;		
		if ($t{number_status} eq "OK") {
			#
			# get country list
			%country_list = database_select_as_hash("SELECT code,name,iso FROM country","name,iso");
			#
			# get rate tables for status we want
			$sql  = "
			SELECT 1,1,
			rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9,
			rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,rate_slot_5_name,rate_slot_6_name,rate_slot_7_name,rate_slot_8_name,rate_slot_9_name
			FROM service_status where id='$status_id_search_rate'
			";
			%route_slots = database_select_as_hash($sql,"flag,rate_slot_1,rate_slot_2,rate_slot_3,rate_slot_4,rate_slot_5,rate_slot_6,rate_slot_7,rate_slot_8,rate_slot_9,rate_slot_1_name,rate_slot_2_name,rate_slot_3_name,rate_slot_4_name,rate_slot_5_name,rate_slot_6_name,rate_slot_7_name,rate_slot_8_name,rate_slot_9_name");
			#
			# clean some data before loop all rates
			$t{search_ok} = 0;
			$t{search_unique_country_code} 	= "";
			$t{search_unique_country_iso} 	= "";
			$t{search_unique_country_name}	= "";
			#
			# loop each route, search number in the right rate_id, add data into template
			$loop_index = 1;
			foreach $route (1..9) {
				$rate_id	= $route_slots{1}{"rate_slot_".$route};
				$rate_name	= $route_slots{1}{"rate_slot_".$route."_name"};
				if ($rate_id ne "") {
					%rate_search = multilevel_rate_table_get($t{number_e164},$rate_id);
					if ($rate_search{ok_to_use} eq 1){
						$t{search_ok} = 1;
						$t{search_unique_country_code} = ($rate_search{rate_country} ne "") ? $rate_search{rate_country} : $t{search_unique_country_code};
						$t{search_rates}{$loop_index}{route}				= $route;
						$t{search_rates}{$loop_index}{rate_id}				= $rate_id;
						$t{search_rates}{$loop_index}{rate_name}			= $rate_name;
						$t{search_rates}{$loop_index}{country_code}			= $rate_search{rate_country} || "";
						$t{search_rates}{$loop_index}{country_iso}			= $country_list{$rate_search{rate_country}}{iso} || "";
						$t{search_rates}{$loop_index}{country_name}			= $country_list{$rate_search{rate_country}}{name} || "";
						$t{search_rates}{$loop_index}{area_code}			= $rate_search{rate_areacode} || "";
						$t{search_rates}{$loop_index}{area_name}			= $rate_search{rate_name} || "";
						$t{search_rates}{$loop_index}{rate_per_minute_raw}	= $rate_search{rate_per_minute} || 0;
						$t{search_rates}{$loop_index}{rate_per_minute}		= &format_number($rate_search{rate_per_minute},2);
						$t{search_rates}{$loop_index}{rate_per_call_raw}	= $rate_search{rate_per_call} || 0;
						$t{search_rates}{$loop_index}{rate_per_call}		= &format_number($rate_search{rate_per_call},2);
						$t{search_rates}{$loop_index}{seconds_per_dollar}	= ($rate_search{rate_per_minute} >0) ? int((1/$rate_search{rate_per_minute})*60) : 0;
						$t{search_rates}{$loop_index}{time_per_dollar}		= &format_time($t{search_rates}{$loop_index}{seconds_per_dollar});
						$loop_index++;
					}
				}
			}
			#
			# normalize unique country data (i hope one countr only.. make no sense multiple country for same number)
			if ($t{search_unique_country_code} ne "") {
				$t{search_unique_country_iso} 	= $country_list{$t{search_unique_country_code}}{iso} || "";
				$t{search_unique_country_name}	= $country_list{$t{search_unique_country_code}}{name} || "";
			}
			#
			# rise no_rate_found message
			if ($t{search_ok} eq 0){
				$t{search_error} = 1;
				$t{search_error_no_rate_found} = 1;
			}
		} else {
			#
			# rise bad_format number message
			$t{search_error} = 1;
			$t{search_error_bad_format} = 1;
		}
	}
    #
    # query country data
	#commented for autocomplete jquery country selection
	#$sql = "
	#SELECT 
	#product_rate_table_data.id,
	#product_rate_table_data.rate_per_minute,
	#product_rate_table_data.areacode,
	#product_rate_table_data.name,
	#country.name,
	#country.iso,
	#country.code
	#FROM product_rate_table_data,country
	#where product_rate_table_data.country = country.code and product_rate_table_data.rate_id='$rate_id_country_list'  
	#";
	#%data = ();
	#%hash = database_select_as_hash($sql,"rate,ac,an,country,iso,cc");
	#foreach $id (keys %hash){
	#	#
	#	# hacks
	#	if (substr($hash{$id}{ac},0,9) eq "212000000"){next}
	#	if ($hash{$id}{rate} eq "100"){next}
	#	#
	#	$iso = $hash{$id}{iso};
	#	$data{$iso}{name} = $hash{$id}{country};
	#	$data{$iso}{cc}{$hash{$id}{cc}}++;
	#	$key = $hash{$id}{an}.$hash{$id}{rate};
	#	$data{$iso}{ac}{$key}{n} = $hash{$id}{an};
	#	$data{$iso}{ac}{$key}{r} = $hash{$id}{rate};
	#
	#}
	#
	##
	## move country data to template
	#$i1 = 1;
	#$t{country_loop_exists} = 0;
	#foreach $iso (sort{$data{$a}{name} cmp $data{$b}{name}} keys %data) {
	#	$t{country_loop_exists} = 1;
	#	$t{country_loop}{$i1}{country_iso} = $iso;
	#	$t{country_loop}{$i1}{country_name} = $data{$iso}{name};
	#	$t{country_loop}{$i1}{country_codes} = join(",",(sort{$a <=> $b} keys %{$data{$iso}{cc}}));
	#	$i2=1;
	#	foreach $ac (sort{$a cmp $b} keys %{$data{$iso}{ac}}) {
	#		$t{country_loop}{$i1}{areacode_loop}{$i2}{area_name} = $data{$iso}{ac}{$ac}{n};
	#		$t{country_loop}{$i1}{areacode_loop}{$i2}{rate_per_minute} = &format_number($data{$iso}{ac}{$ac}{r},2);
	#		$tmp = ($data{$iso}{ac}{$ac}{r} >0) ? (1/$data{$iso}{ac}{$ac}{r})*60 : 0;
	#		$t{country_loop}{$i1}{areacode_loop}{$i2}{time_per_dollar} = &format_time($tmp);
	#		$i2++;
	#	
	#		if ($i2>50){last}
	#	}
	#		
	#
	#	$i1++;
	#}
	#
	# print page
    &template_print("template.about.rate.html",%t);
}
#=======================================================
