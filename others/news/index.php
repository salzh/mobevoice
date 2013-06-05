<?php
/**
 * Created by Parth Mudgal.
 * Date: 12/6/12
 * Time: 9:01 PM
 */

include("../auth.php");

$action = isset($_REQUEST['action']) ? $_REQUEST['action'] : "new";
$file = "/usr/local/multilevel/www/news/index.html";
$content = file_get_contents("news.html");
if($action == "update"){
    $content = $_POST['editor1'];
    $template = file_get_contents("news_template.html");
    $html = str_replace("{content}", $content, $template);
    unlink($file);
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
    <title>ZenoFon News Edit</title>
    <link href="../design/bootstrap/css/bootstrap.css" media="screen" type="text/css" rel="stylesheet">
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