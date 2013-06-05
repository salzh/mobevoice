<?php
/**
 * Created by Parth Mudgal.
 * Date: 12/6/12
 * Time: 9:01 PM
 */

$userpass = @$_COOKIE['user'];
$userpass = explode(":", $userpass);

if(isset($_REQUEST['user']) && isset($_REQUEST['password'])){
    $userpass[0] = @$_REQUEST['user'];
    $userpass[1] = @$_REQUEST['password'];
}

$users = array(
    'parth' => 'parth123',
    'fouad' => 'fouad123',
    'cammisa' => 'cammisa'
);

if(strlen(@$userpass[1])>0 && $users[@$userpass[0]] == @$userpass[1]){
    setcookie("user", $userpass[0] . ":" . $userpass[1], time() + 26400);
}else{
    echo <<< endo
<script>
var username = window.prompt("Username ?");
var password = window.prompt("Password ?");
top.location = "news.php?user=" + username + "&password=" + password;
</script>
endo;
die();
}

$action = isset($_REQUEST['action']) ? $_REQUEST['action'] : "new";
$file = "/usr/local/multilevel/www/news/index.html";
$content = file_get_contents("news.html");
if($action == "update"){
    $content = $_POST['editor1'];
    $template = file_get_contents("news_template.html");
    $html = str_replace("{content}", $content, $template);
    @unlink($file);
    @unlink("news.html");
    $file = fopen($file, "w+");
    fwrite($file, $html);
    fclose($file);
    $file = fopen("news.html", "w+");
    fwrite($file, $content);
    fclose($file);
}
?>
<html>
<head>
    <link href="design/bootstrap/css/bootstrap.css" media="screen" type="text/css" rel="stylesheet">
    <script src="ckeditor.js"></script>
    <style type="text/css">
        body {
            padding-top: 60px;
            padding-bottom: 40px;
        }

        .sidebar-nav {
            padding: 9px 0;
        }
    </style>
</head>
<body>
<div class="container-fluid">
    <h1>News Page</h1>
    <div class="row-fluid">
        <!--/span-->
        <div class="span12 well">
            <form method=post>
                <textarea cols="80" id="editor1" name="editor1" rows="70">
                    <? echo $content?>
                </textarea><br>
                <input type=hidden name=action value=update>
                <input type="submit" value="Submit">
            </form>
        </div>
    </div>
</div>
</body>
<script>
    CKEDITOR.replace( 'editor1' , {height: 500});
</script>
</html>