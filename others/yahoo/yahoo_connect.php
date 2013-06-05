<?php

// Include the YOS library.
require 'lib/Yahoo.inc';
include 'db_config.php';

session_start();

define('OAUTH_CONSUMER_KEY', ''); // Place Yoru Consumer Key here
define('OAUTH_CONSUMER_SECRET', ''); // Place your Consumer Secret
define('OAUTH_APP_ID', ''); // Place Your App ID here

if (array_key_exists("login", $_GET)) {
    $session = YahooSession::requireSession(OAUTH_CONSUMER_KEY, OAUTH_CONSUMER_SECRET, OAUTH_APP_ID);
    if (is_object($session)) {
        $user = $session->getSessionedUser();
        $profile = $user->getProfile();
        $name = $profile->nickname; // Getting user name
        $guid = $profile->guid; // Getting Yahoo ID

        // Creating session variable for User
        $_SESSION['login'] = true;
        $_SESSION['name'] = $name;
        $_SESSION['guid'] = $guid;
        $_SESSION['oauth_provider'] = 'yahoo';
    }
}

if (array_key_exists("logout", $_GET)) {
    // User logging out and Clearing all Session data
    YahooSession::clearSession();
    unset ($_SESSION['login']);
    unset($_SESSION['name']);
    unset($_SESSION['guid']);
    unset($_SESSION['oauth_provider']);
    // After logout Redirection here
    header("Location: index.php");
}
?>
