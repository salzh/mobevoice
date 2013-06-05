<?php
/**
 * Created by Parth Mudgal.
 * Date: 12/7/12
 * Time: 8:14 PM
 */

$host = "127.0.0.1";
$user = "radio";
$pass = "radio";

$db = "multilevel";
$dsn = "mysql:host=$host;dbname=$db";

$conn = new PDO($dsn, $user, $pass);
?>