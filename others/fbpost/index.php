<?php
/**
 * Created by Parth Mudgal.
 * Date: 12/7/12
 * Time: 8:02 PM
 */

include "../auth.php";
include "../config.php";
include "functions.php";


$accounts = file_get_contents("accounts.json");
$accounts = json_decode($accounts, 1);

$action = isset($_REQUEST['action']) ? $_REQUEST['action'] : "";

if ($action == "delete") {
    $selected = json_decode($_REQUEST['selected'], 1);

    $selected = implode(", ", $selected);
    $sql = "delete from facebook_updates where id in ($selected)";
    $delete = $conn->prepare($sql);
    $delete->execute();
    if ($delete->errorCode() == 0) {
        die("success");
    } else {
        die($delete->errorInfo());
    }
}

if ($action == "addnew") {
    $text = @$_REQUEST['text'];
    $date = @$_REQUEST['date'];
    $time = @$_REQUEST['time'];
    $gapvalue = @$_REQUEST['gapvalue'];
    $gapunit = @$_REQUEST['gapunit'];
    $email = @$_REQUEST['email'];

    $text = explode("\n", $text);
    $flag = 0;
    for ($i = 0; $i < count($text); $i++) {
        $text[$i] = trim($text[$i]);
        if (strlen($text[$i]) > 0) {
            $flag = 1;
        }
    }
    if (!$flag) {
        $message = "Please enter a Status update";
    }
    if ($date == "") {
        $date = date("Y-m-d");
    }
    if ($time == "") {
        $time = date("H:i");
    }
    $now = $date . " " . $time;
    if (@$message == "") {
        for ($i = 0; $i < count($text); $i++) {
            if (strlen($text[$i]) < 1) continue;
            $val = $gapvalue * $i;
            $sql = "insert into facebook_updates (text, time, email) values ('{$text[$i]}', date_add('{$now}', interval {$val} {$gapunit}), '{$email}')";
            $insert = $conn->prepare($sql);
            //echo $insert->queryString . " -- {$text[$i]}<br>";
            $insert->execute() or print(var_dump($insert->errorInfo()) . "<br>" . $insert->queryString . "<hr>");
        }
    }

}

$posts = $conn->prepare("select id, text, time, posted, email from facebook_updates");
$posts->execute();
$posts = $posts->fetchAll();

?>
<html>
<head>
    <title>FB Wall Scheduler</title>
    <link href="../design/bootstrap/css/bootstrap.css" media="screen" type="text/css" rel="stylesheet">
    <link href="../css/jquery.ui.timepicker.css" media="screen" type="text/css" rel="stylesheet">
    <link href="../css/smoothness/jquery-ui-1.9.2.custom.min.css" media="screen" type="text/css" rel="stylesheet">
    <script src="../js/jquery-1.8.3.min.js"></script>
    <script src="../js/jquery.dataTables.min.js"></script>
    <script src="../js/jquery.ui.timepicker.js"></script>
    <script src="../js/jquery-ui-1.9.2.custom.min.js"></script>
    <link href="../css/demo_table.css" media="screen" type="text/css" rel="stylesheet">
    <link href="../css/jquery.dataTables.css" media="screen" type="text/css" rel="stylesheet">
    <style type="text/css">
        body {
            padding-top: 60px;
            padding-bottom: 40px;
        }

        .sidebar-nav {
            padding: 9px 0;
        }

        select {
            width: 100px;
        }

        table tr.row_selected td {
            background-color: #9FAFD1;
        }
    </style>
</head>
<body>
<div class=container-fluid>
    <div class=row-fluid>
        <div class="span8 well">
            <h3>Scheduled</h3>
            <table id=maintable>
                <thead>
                <tr>
                    <th>ID</th>
                    <th style="width:60%">Text</th>
                    <th style="width:120px">Time</th>
                    <th style="width:20px">Posted</th>
<!--                    <th>Email</th>-->
                </tr>

                </thead>
                <tbody>
                <?php
                foreach ($posts as $post) {
                    echo <<< endo
            <tr class=fbpost id='row-{$post['id']}'>
            <td>{$post['id']}</td>
            <td id='text{$post['id']}'>{$post['text']}</td>
            <td id='time{$post['id']}'>{$post['time']}</td>
            <td id='posted{$post['id']}'>{$post['posted']}</td>
            <!--<td id='email{$post['id']}'>{$post['email']}</td>-->
            </tr>
endo;

                }
                ?>
                </tbody>
            </table>

        </div>
        <div class="span4">

            <div class=well>
                <form method=post class=form-horizontal>
                    <input type=hidden name=action value=addnew>
                    <fieldset>
                        <legend>New Status Update</legend>
                        <label for=text>Status Updates (Multiple in new line)</label>
                        <textarea style="width:360px;height:100px" id=text type="text" name=text
                                  placeholder="Type something"></textarea>
                        <!--                        <span class="help-block">Example block-level help text here.</span>-->
                        <label for=date> Post after </label>
                        <input id=date name=date type="date" style="height:30px">
                        <input id=time name=time style="height:30px" placeholder="Time">

                        <label for=gaps>With gaps of</label>
                        <select id=gaps name=gapvalue>
                            <option>1</option>
                            <option>2</option>
                            <option>3</option>
                            <option>5</option>
                            <option>7</option>
                            <option>10</option>
                            <option>12</option>
                            <option>15</option>
                            <option>18</option>
                            <option>24</option>
                        </select>
                        <select id=gapunit name=gapunit>
                            <option value=minute>Minutes</option>
                            <option value=hour>Hours</option>
                            <option value=day>Days</option>
                            <option value=week>Weeks</option>
                        </select>
                        <label for=email>Account</label>
                        <select name=email id=email style="width:200px">

                            <?php
                            foreach ($accounts as $account) {
                                echo <<< endo
                                    <option value="{$account['email']}">{$account['name']}</option>

endo;
                            }
                            ?>
                        </select>
                        <br><Br>
                        <button type="submit" class="btn-primary">Submit</button>
                        <input type="reset" class="btn" value="Clear">
                    </fieldset>
                </form>
            </div>
            <div class=row-fluid>
                <button id=delete style="display:none" class="btn-danger">Delete</button>
            </div>


        </div>
    </div>
</div>
<script>
    var selected = [];
    var lastid;
    function selectedIDs() {
        var ids = [];
        var selected = $(".row_selected");
        for (var i = 0; i < selected.length; i++) {
            ids.push(selected[i].id.split("-")[1])
        }
        return ids;
    }
    function updateText() {
        var selected = selectedIDs(); //$(".row_selected");
        var text = [];
        for (var i = 0; i < selected.length; i++) {
            text.push($("#text" + selected[i])[0].innerText);
        }
        $("#text")[0].innerText = text.join("\n");
        if (text.length == 0) {
            $("#delete")[0].style.display = "none";
        } else {
            $("#delete")[0].style.display = "block";
        }
    }
    $(document).ready(function () {
        $('#maintable').dataTable();
        $("#time").timepicker();
        $("tbody").on("click", function (e) {
            console.log(e);
            var x = e.toElement.parentElement;
            var id = x.id.split("-")[1];
            console.log(id);
            var text = $("#text" + id)[0].innerText;
            var time = $("#time" + id)[0].innerText;
            time = time.split(" ");
            $(x).toggleClass("row_selected")
            //$("#text").val(text);
            $("#date").val(time[0]);
            $("#time").val(time[1]);
            updateText();
        });
        $("#delete").on("click", function () {
            selected = selectedIDs();
            if (window.confirm("Are you sure you want to delete " + selected.length + " Status updates ?")) {
                $.ajax({
                            type:'POST',
                            url:"index.php",
                            data:{
                                selected:JSON.stringify(selectedIDs()),
                                action:'delete'
                            }
                        }
                ).done(function (data) {
                            if (data == "success") {
                                var table = $('#maintable').dataTable();
                                $('.row_selected').remove();
                                selected = [];
                            }
                        });
            }
        });
    })
    ;
</script>
</body>
</html>