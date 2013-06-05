<?php
/**
 * Created by Parth Mudgal.
 * Date: 12/7/12
 * Time: 7:48 PM
 */

function postToWall($status, $email = "pica587pyx@m.facebook.com")
{
    if (mail($email, $status, "")) {
        echo "Mail sent";
    } else {
        echo "Mail failed";
    }

}