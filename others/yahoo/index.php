<?php
include 'yahoo_connect.php';
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
    <head>
        <title>Yahoo Oauth Login Connect</title>
        <style type="text/css">
            a img, a:hover img, a:focus img{
                border: none;
            }
        </style>
    </head>
    <body>
        <?php
        if ($_SESSION['login'] == true) {
            echo "You are : " . $_SESSION['name'] . "<br/>";
            echo "GUID : " . $_SESSION['guid'];
            echo '<br/><a href="?logout"><img src="images/logout_btn.png" alt="Yahoo Logout"/></a>';
        } else {
            echo '<a href="?login"><img src="images/login_btn.png" alt="Yahoo Login"/></a>';
        }
        ?>


    </body>
</html>