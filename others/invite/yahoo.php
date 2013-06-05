<?php
require("yahoo/Yahoo.inc");


mysql_connect("127.0.0.1", "multilevel", "multilevel");
mysql_select_db("multilevel");

// When you replaced with your own keys here and once run this should go to Yahoo login page else some thing went wrong in your app registration and keys

// Your Consumer Key (API Key) goes here.
define('CONSUMER_KEY', "dj0yJmk9eVZ6UlBiU1d1UG5FJmQ9WVdrOU5GTlJia3RXTlRRbWNHbzlOak0xTWpBd01EWXkmcz1jb25zdW1lcnNlY3JldCZ4PTQw");

// Your Consumer Secret goes here.
define('CONSUMER_SECRET', "dcb850224eb4f344d9f9075b17f824dd6484bc19");

// Your application ID goes here.
define('APPID', "4SQnKV54");

$session = YahooSession::requireSession(CONSUMER_KEY, CONSUMER_SECRET, APPID);

if (is_object($session)) {
    $user = $session->getSessionedUser();

    // Creating session variable for User
    $_SESSION['login'] = true;

    $query = sprintf("SELECT * FROM social.contacts.sync WHERE guid=me AND rev=0");
    $response = $session->query($query);


    $data = objectToArray($response->query->results->contactsync->contacts);
    $values = array();
    $service_id = $_COOKIE['su'];
    $sql = "insert into service_contacts (service_id, name, email, phone) values ";
    $string = "('$service_id', '%s', '%s', '%s')";
    $i = 0;
    foreach ($data as $contact) {
        $i++;
        $new = array();
        $name = "";
        $email = "";
        $phone = "";
        if ($contact['fields']['created']) {
            $contact['fields'] = array($contact['fields']);
        }
        foreach ($contact['fields'] as $field) {
            switch ($field['type']) {
                case 'email':
                    $email = $field['value'];
                    break;
                case 'name':
                    if (is_array($field['value'])) {
                        $name = $field['value']['givenName'] . " " . $field['value']['familyName'];
                    } else {
                        $name = $field['value'];
                    }
                    $name = trim($name);
                    break;
                case "phone":
                    $phone = $field['value'];
                    break;
                case "yahooid";
                    $email = $field['value'] . "@yahoo.com";
                    break;
                case 'nickname':
                    if (isset($name) && $name != "") {
                        $name = $field['value'];
                    }
                    break;
                default:
                    break;
            }
        }
        $value = sprintf($string,
            mysql_real_escape_string($name),
            mysql_real_escape_string($email),
            mysql_real_escape_string($phone)
        );
        if (!in_array($value, $values)) {
            $values[] = $value;
        }
        if ($i % 100 == 0) {
            $execute = $sql . implode(", ", $values);
            mysql_query($execute);
            $values = array();
        }
    }
    $execute = $sql . implode(", ", $values);
    mysql_query($execute);
    print " <script> alert('Friends imported'); top.location='/myaccount/';</script>";
}

function objectToArray($d)
{
    if (is_object($d)) {
        // Gets the properties of the given object
        // with get_object_vars function
        $d = get_object_vars($d);
    }

    if (is_array($d)) {
        /*
              * Return array converted to object
              * Using __FUNCTION__ (Magic constant)
              * for recursive call
              */
        return array_map(__FUNCTION__, $d);
    } else {
        // Return array
        return $d;
    }
}

?>