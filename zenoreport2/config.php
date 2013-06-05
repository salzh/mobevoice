<?php

session_start();
set_include_path("lib");
include("functions.php");
include ("lib/Zend/Loader/Autoloader.php");
$dbData = include ("db.php");

if (isset($_GET['schema']) || !isset($_SESSION['dbname'])) {
    $dbName = isset($_GET['schema']) && isset($dbData[$_GET['schema']]) ? $_GET['schema'] : "zenofon";
    $_SESSION['dbname'] = $dbName;
} else {
    $dbName = @$_SESSION['dbname'];
}

$dbDetails = $dbData[$dbName];


if (isset($_SESSION['executeDB']) && $_SESSION['executeDB'] != "-") {
    $dbName = $_SESSION['executeDB'];
    $dbDetails = $dbData[$dbName];
    $_SESSION['executeDB'] = "-";
}

$autoloader = Zend_Loader_Autoloader::getInstance();
$autoloader->isFallbackAutoloader(true);

$db = Zend_Db::factory('Pdo_Mysql', $dbDetails);

$reportDb = $dbData['zenoreport'];

$reportDb = new Zend_Db_Adapter_Mysqli($reportDb);

if (isset($_REQUEST['action']) && $_REQUEST['action'] == "login") {
    $user = $_REQUEST['username'];
    $pass = $_REQUEST['password'];
    if (!loginUserPass($user, $pass)) {
        die(json_encode(array(
            'result' => 'error',
            'error' => 'failed'
        )));
    } else {
        die(json_encode(array(
            'result' => 'success',
            'redirect' => 'index.html'
        )));
    }
} else if (isset($_COOKIE['userpass'])) {
    $userpass = $_COOKIE['userpass'];
    $userpass = explode(":", $userpass);
    if (count($userpass) != 2) {
        header("HTTP/1.0 302 Not Found");
        die("login.html");
    } else if (!isset($_REQUEST['action']) || $_REQUEST['action'] != "login") {
        $user = $userpass[0];
        $pass = $userpass[1];
        if (!loginUserPass($user, $pass)) {
            header("HTTP/1.0 302 Not Found");
            die("login.html");
        }
    }
} else {
    header("HTTP/1.0 302 Not Found");
    die("login.html");
}


function loginUserPass($user, $pass)
{
    global $reportDb;
    $row = $reportDb->select()->from("report_users", array("password"))->where("username=?", $user)->query()->fetch();
    if ($pass == $row['password']) {
        setcookie("userpass", $user . ":" . $pass, time() + 3600 * 24 * 30);
        return true;
    } else {
        return false;
    }
}

$template = "template/";
Zend_Db_Table::setDefaultAdapter($db);

$defaultDb = Zend_Db_Table::getDefaultAdapter();


