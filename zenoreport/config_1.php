<?php

session_start();

include("functions.php");
include ("Zend/Loader/Autoloader.php");
$dbData = include ("db.php");

if (isset($_GET['schema']) || !isset($_SESSION['dbname'])) {
    $dbName = isset($_GET['schema']) && isset($dbData[$_GET['schema']]) ? $_GET['schema'] : "zenofon";
    $_SESSION['dbname'] = $dbName;
}else{
    $dbName = @$_SESSION['dbname'];
}

$dbDetails = $dbData[$dbName];

$autoloader = Zend_Loader_Autoloader::getInstance();
//$autoloader->registerNamespace("Application_$dbName");
$autoloader->isFallbackAutoloader(true);

$db = Zend_Db::factory('Pdo_Mysql', array(
    'host' => $dbDetails['host'],
    'username' => $dbDetails['user'],
    'password' => $dbDetails['pass'],
    'dbname' => $dbDetails['dbname']
));

$template = "template/";
Zend_Db_Table::setDefaultAdapter($db);

$defaultDb = Zend_Db_Table::getDefaultAdapter();

