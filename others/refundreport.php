<?php
$page = "refundreport.php";

include("auth.php");
include ("config.php");

$by = isset($_GET['by']) ? strtolower($_GET['by']) : 'service_id';
$days = isset($_GET['days']) ? $_GET['days'] : '7';

$byf = "&by=$by";
$daysf = "&days=$days";

$sql = <<< endo
select
c.$by,
count(cr.id) as request,
sum(cr.amount) as `amount`
from call_refund cr join calls c on cr.call_id=c.id
and c.date > date_sub(now(), interval $days day)
group by c.$by
endo;

$sql = <<< neo
select
cl.$by,
count(cr.id) as request,
sum(cr.amount) as `amount`
from calls_log cl
join calls c on c.date=cl.datetime_stop
join call_refund cr on cr.call_id=c.id
where c.service_id=cl.service_id
and c.ani=cl.ani
and c.did=cl.did
and c.dst=cl.dst
and c.date > date_sub(now(), interval $days day)
group by cl.$by
neo;


#die($sql);
$columns = array(ucfirst(str_replace("_", " ", $by)), 'Requests', 'Amount');


$result = $conn->prepare($sql);
$result->execute();
$result = $result->fetchAll(PDO::FETCH_NUM);
function arrayToTable($array, $wrap = "td")
{
    $x = array();
    foreach ($array as $data) {
        $x[] = "<$wrap>" . implode("</$wrap> <$wrap>", $data) . "</$wrap>";
    }
    return "<tr>" . implode("</tr> \n<tr>", $x) . "</tr>";
}

?>

<html>
<head>
    <style>
        body {

            padding: 30px;
        }

        .sidebar-nav {
            padding: 9px 0;
        }
    </style>
    <link href="design/bootstrap/css/bootstrap.css" rel="stylesheet">
    <link href="css/demo_table.css" rel="stylesheet">
    <link href="css/jquery.dataTables.css" rel="stylesheet">
    <script src="js/jquery-1.8.3.min.js"></script>
    <script src="js/jquery-ui-1.9.2.custom.min.js"></script>
    <script src="js/jquery.dataTables.min.js"></script>
</head>
<body>
<h1>Call Refund Report</h1>

<div class=row-fluid>
    <div class="span3">
        <div class="well sidebar-nav">
            <ul class="nav nav-list">
                <li class="nav-header">Period</li>
                <li <?php if($days==1) echo "class=active" ?>><a href="?days=1<?=$byf?>">Last 24 Hours</a></li>
                <li <?php if($days==7) echo "class=active" ?>><a href="?days=7<?=$byf?>">Last 7 Days</a></li>
                <li <?php if($days==15) echo "class=active" ?>><a href="?days=15<?=$byf?>">Last 15 Days</a></li>
                <li <?php if($days==30) echo "class=active" ?>><a href="?days=30<?=$byf?>">Last 30 days</a></li>
                <li <?php if($days==60) echo "class=active" ?>><a href="?days=60<?=$byf?>">Last 2 Months</a></li>
                <li <?php if($days==150) echo "class=active" ?>><a href="?days=150<?=$byf?>">Last 5 Months</a></li>
                <li <?php if($days==365) echo "class=active" ?>><a href="?days=365<?=$byf?>">Last 12 Months</a></li>

                <li class="nav-header">Data For</li>
                <li <?php if($by=='service_id') echo "class=active" ?>><a href="?by=service_id<?=$daysf?>">Service ID</a></li>
                <li <?php if($by=='dst') echo "class=active" ?>><a href="?by=dst<?=$daysf?>">Destination</a></li>
                <li <?php if($by=='did') echo "class=active" ?>><a href="?by=did<?=$daysf?>">DID</a></li>
                <li <?php if($by=='ast_hangup_cause') echo "class=active" ?>><a href="?by=ast_hangup_cause<?=$daysf?>">Hangup Cause</a></li>
                <li <?php if($by=='rate_slot') echo "class=active" ?>><a href="?by=rate_slot<?=$daysf?>">Route</a></li>
            </ul>
        </div>
        <!--/.well -->
    </div>
    <div class="span9 well">
        <table id=maintable>
            <thead>
            <? echo arrayToTable(array($columns), "th") ?>
            </thead>
            <tbody>
            <? echo arrayToTable($result) ?>
            </tbody>
        </table>
    </div>
    <script>
        $(document).ready(function () {
            $('#maintable').dataTable();
        });
    </script>
    <!--/span-->
</div>
</body>
</html>