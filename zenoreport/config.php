<?php

session_start();

if(isset($_GET['password'])){
    $pass = $_GET['password'];
    if($pass == "z3n0r3p0r1"){
        $_SESSION['user'] = 1;
    }else{
        $_SESSION['user'] = 0;
    }
}

if(!isset($_SESSION['user']) || $_SESSION['user']!=1){
    echo <<< endo
<html>
<head>
<script>
var p = prompt("Password");
top.location = "database.php?action=login&password=" + p;
</script>
</head>
</html>
endo;
die();
}

include("functions.php");
include ("Zend/Loader/Autoloader.php");
$dbData = include ("db.php");

if (isset($_GET['schema']) || !isset($_SESSION['dbname'])) {
    $dbName = isset($_GET['schema']) && isset($dbData[$_GET['schema']]) ? $_GET['schema'] : "zenofon";
    $_SESSION['dbname'] = $dbName;
} else {
    $dbName = @$_SESSION['dbname'];
}

$dbDetails = $dbData[$dbName];



if(isset($_SESSION['executeDB']) && $_SESSION['executeDB']!="-"){
    $dbName = $_SESSION['executeDB'];
    $dbDetails = $dbData[$dbName];
    $_SESSION['executeDB'] = "-";
}

$autoloader = Zend_Loader_Autoloader::getInstance();
//$autoloader->registerNamespace("Application_$dbName");
$autoloader->isFallbackAutoloader(true);

$db = Zend_Db::factory('Pdo_Mysql', $dbDetails);

$reportDb = $dbData['www-zenoradio']; /*array(
    'host' => '127.0.0.1',
    'username' => 'root',
    'password' => 'root',
    'dbname' => 'zenoreport'
);*/

$reportDb = new Zend_Db_Adapter_Mysqli($reportDb);

$template = "template/";
Zend_Db_Table::setDefaultAdapter($db);

$defaultDb = Zend_Db_Table::getDefaultAdapter();


