<?php
/**
 * Created by Parth Mudgal.
 * Date: 11/2/12
 * Time: 12:30 AM
 */

function getDataFileName(){
    return "/home/parth/data/cache.json";
}

include ("auth.php");
/*if($_COOKIE['pass'] != "veena123"){
die("error");
}*/

header("Content-type: text/json");
$fname = getDataFileName();
$data = file_get_contents($fname);
$data = json_decode($data, 1);

$final = array();
foreach ($data as $date => $values) {
    $date = explode("T", $date);
    $date = $date[0];
    $final[] = array_merge(
        array(
            'date' => $date,
            'month' => date('Y-m', strtotime($date) + 30000),
            'Total-Minutes' => $values['IDT-minutes'] + $values['RNK-Minutes'] + $values['Nobel-Minutes'],
            'Total-Cost' => $values['Nobel-Cost'] + $values['RNK-Total'] + $values['IDT-spend']
        ),
        $values
    );
}
echo json_encode($final);
