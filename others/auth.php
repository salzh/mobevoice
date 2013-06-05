<?php
/**
 * Created by Parth Mudgal.
 * Date: 12/7/12
 * Time: 7:54 PM
 */

if(!isset($page)){
    $page = "index.php";
}
$userpass = @$_COOKIE['user'];
$userpass = explode(":", $userpass);

if(isset($_REQUEST['Username']) && isset($_REQUEST['Password'])){
    $userpass[0] = @$_REQUEST['Username'];
    $userpass[1] = @$_REQUEST['Password'];
}

$users = array(
    'parth' => 'parth123',
    'fouad' => 'fouad123',
    'cammisa' => 'cammisa123',
    'baruch' => 'baruch123',
    'veena' => 'veena123',
    'andre' => 'andre123'
);

if(strlen(@$userpass[1])>0 && $users[@$userpass[0]] == @$userpass[1]){
    setcookie("user", $userpass[0] . ":" . $userpass[1], time() + 26400);
}else{

?>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="http://www.zenofon.com/others/design/bootstrap/css/bootstrap.css" rel="stylesheet">

    <style>
        body {
            padding-top: 60px;
            padding-bottom: 40px;
        }

    </style>
</head>
<body>
<div class="container-fluid">
    <div class="span5 offset6">
        <div class=hero-unit>
            <form class="form" method=post action='<?=$page?>'>

                <label class="control-label" for="Username">Username</label>

                <div class="controls">
                    <input style="height: 30px;" type="text" id="Username" placeholder="Username" name="Username">
                </div>


                <label class="control-label" for="inputPassword">Password</label>

                <div class="controls">
                    <input style="height: 30px;" type="password" id="inputPassword" placeholder="Password" name="Password">
                </div>

                <br>

                <div class="controls">
                    <button type="submit" class="btn-primary">Login</button>
                </div>


            </form>
        </div>
    </div>
</div>
</body>
</html>
<?

die();
}
?>