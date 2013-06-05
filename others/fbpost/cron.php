<?php
/**
 * Created by Parth Mudgal.
 * Date: 12/8/12
 * Time: 12:05 AM
 */

include ("config.php");

$sql = 'select id, text, email, TIMEDIFF(time, now()) from facebook_updates where posted=0  and TIMEDIFF(time, now()) < "00:20"';
$selected = $conn->prepare($sql);
$selected->execute();
$selected = $selected->fetchAll();
foreach ($selected as $post) {
    //if (true || 1) {
    if(mail($post['email'], $post['text'], "")){
        $sql = "update facebook_updates set posted=1 where id=" . $post['id'];
        echo $sql . "<br>";
        $ex = $conn->prepare($sql);
        $ex->execute();
    }
}
