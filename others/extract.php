<?php
/**
 * Created by Parth Mudgal.
 * Date: 10/31/12
 * Time: 10:53 PM
 */
$page = "extract.php";
include("auth.php");

function getDataFileName()
{
    if ($_SERVER['SERVER_NAME'] == "localhost") {
        return "data/cache.json";
    }
    return "/home/parth/data/cache.json";
}

$date = date("Y-m-d", time() - 3600 * 24);
$date = isset($_GET['date']) ? $_GET['date'] : $date;
$cache = isset($_GET['nocache']) ? $_GET['nocache'] : false;

$date = date("Y-m-d", strtotime($date));
$date .= "T00:00:00Z";
$finaldata = array();
error_reporting(1);
require('class.curl.php');

$max_redirect = 3; // Skipable: default => 3

$row = getauthorize($date);
$finaldata = array_merge($finaldata, $row);

$row = getnobel888($date);
$finaldata = array_merge($finaldata, $row);

$row = getrnkdata($date);
$finaldata = array_merge($finaldata, $row);

$row = getnet2phone($date);
$finaldata = array_merge($finaldata, $row);


$html = "<h3>$date</h3><br>";
foreach ($finaldata as $key => $val) {
    $val = str_replace(",", "", $val);
    if ($val[0] == "$") {
        $val = "$" . round(substr($val, 1), 2);
    } else {
        $val = round($val, 2);
    }
    $html .= $key . " = " . $val . "<br>\n";
    //$html .= $key . " = " . round($val, 2) . "<br>\n";
}

function getauthorize($date)
{
    return array();
    $originalDate = $date;
    $date = date("d-M-Y", strtotime($date) + 30000);


    $finaldata = array(
        'Charges',
        'Revenues'
    );
    $cached = getcache($originalDate, $finaldata);
    if ($cached) {
        return $cached;
    }
    global $max_redirect;
    $curl = new Curl_Client(array(

        CURLOPT_FRESH_CONNECT => 1,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_USERAGENT => 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_SSL_VERIFYPEER => false

    ), $max_redirect);
    $curl->get("https://account.authorize.net/ui/themes/anet/logon.aspx");
    $html = $curl->currentResponse();
    $html = $html['body'];
    $viewstate = explode('<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE"', $html);
    $viewstate = explode('value="', $viewstate[1]);
    $viewstate = explode('" />', $viewstate[1]);
    $viewstate = $viewstate[0];

    $pagekey = explode('"__LOGIN_PAGE_KEY" value="', $html);
    $pagekey = explode('" />', $pagekey[1]);
    $pagekey = $pagekey[0];
    $data = array(
        '__VIEWSTATE' => $viewstate,
        '__PAGE_KEY' => '',
        'MerchantLogin' => 'Indian0rchard',
        'Password' => 'Purple%p@nther2',
        '__LOGIN_PAGE_KEY' => $pagekey
    );


    $curl->post("https://account.authorize.net/UI/themes/anet/logon.aspx", $data);

    $curl->get("https://account.authorize.net/UI/themes/anet/merch.aspx?page=history&sub=stat");
    $html = $curl->currentResponse();
    $html = $html['body'];
    preg_match('/[0-9]+!' . $date . '[^\"]+/', $html, $match);
    $dates = $match[0];

    $pagekey = explode('__PAGE_KEY" value="', $html);
    $pagekey = explode('"', $pagekey[1]);
    $pagekey = $pagekey[0];
    $data = array(
        'StartRecord' => '1',
        'RecordCount' => '20',
        'WithSummary' => '1',
        'TransType' => 'Settled',
        'StartBatchID' => $dates,
        'EndBatchID' => $dates,
        'RunStatReport' => 'Run Report',
        '__PAGE_KEY' => $pagekey
    );
    $curl->post("https://account.authorize.net/UI/themes/anet/merch.aspx?page=history&sub=batchstats", $data);
    $html = $curl->currentResponse();
    $html = $html['body'];
    $temp = explode('Net Amount', $html);
    $totalcount = explode('Total Count', $temp[0]);
    $totalcount = explode('<td align="right" class=', $totalcount[1]);

    $totalcount = $totalcount[count($totalcount) - 1];
    $totalcount = explode(">", $totalcount);
    $totalcount = explode("<", $totalcount[1]);
    $totalcount = $totalcount[0];
    $netamount = explode('<td colspan="11" class="HorizontalLine">', $temp[1]);
    $netamount = explode('<td align="right" class="', $netamount[0]);
    $netamount = $netamount[count($netamount) - 1];
    $netamount = explode('>', $netamount);
    $netamount = explode('<', $netamount[1]);
    $netamount = $netamount[0];
    $netamount = trim($netamount);
    $finaldata = array(
        'Charges' => $totalcount,
        'Revenues' => $netamount
    );
    save2cache($originalDate, $finaldata);
    return $finaldata;
}

function getnobel888($date)
{
    $originalDate = $date;
    $finaldata = array(
        'Nobel-Cost',
        'Nobel-Minutes'
    );
    $cached = getcache($originalDate, $finaldata);

    if ($cached) {
        return $cached;
    }
    $date = date("m/d/y", strtotime($date) + 30000);

    global $max_redirect;
    $curl = new Curl_Client(array(

        CURLOPT_FRESH_CONNECT => 1,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_USERAGENT => 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_SSL_VERIFYPEER => false

    ), $max_redirect);
    $data = array(
        'uri' => '/carrier/index.htm',
        'username' => 'Zenofon',
        'password' => 'r0ck53',
        'rememberme' => 'on',
        'submit' => 'Login'
    );
    $curl->post("https://www.nobeldiamond888.com/dn/carrier/login.htm", $data);

    $data = array(
        'fromDate' => $date,
        'toDate' => $date,
        'groupBy' => 'date',
        //'groupByDestination' => 'true',
        //'showAsr' => 'true',
        //'showAcd' => 'true',
        'showTotalMinutes' => 'true',
        //'showTotalCalls' => 'true',
        'showAnsweredCost' => 'true',
        //'showAverageAnsweredCost' => 'true',
        'submit' => 'SUBMIT'
    );
    $curl->post("https://www.nobeldiamond888.com/dn/carrier/custReports.htm", $data);
    $html = $curl->currentResponse();
    $html = $html['body'];
    $html = explode("<b>", $html);
    $minutes = explode("</b>", $html[2]);
    $minutes = $minutes[0];
    $cost = explode("</b>", $html[3]);
    $cost = $cost[0];
    $finaldata = array(
        'Nobel-Cost' => $cost,
        'Nobel-Minutes' => $minutes
    );
    save2cache($originalDate, $finaldata);
    return $finaldata;
}

function getrnkdata($date)
{
    $originalDate = $date;
    $finaldata = array(
        'RNK-Minutes',
        'RNK-Total'
    );
    $cached = getcache($originalDate, $finaldata);
    if ($cached) {
        return $cached;
    }
    global $max_redirect;
    $curl = new Curl_Client(array(

        CURLOPT_FRESH_CONNECT => 1,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_USERAGENT => 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_SSL_VERIFYPEER => false

    ), $max_redirect);

    $data = array(
        'data[system][page]' => 'sign_in',
        'data[input][email_address]' => 'veena@zenofon.com',
        'data[input][password]' => '0282',
        'action' => 'Sign In'
    );
    $curl->post("http://rnkportal.rnkcom.com/index.php", $data);


    $date = explode("T", $date);
    $date = $date[0];
    $data = array(
        'data[system][page]' => 'view',
        'data[system][order]' => 'start_date',
        'data[system][sort]' => 'asc',
        'data[date][from]' => $date,
        'data[date][to]' => $date,
        'data[input][mask]' => '',
        'data[input][dialed_number]' => '',
        'data[input][ani]' => '',
        'action' => 'view',
        'data[group]' => 'day'
    );
    $curl->post("http://rnkportal.rnkcom.com/module2.php", $data);
    $response = $curl->currentResponse();
    $html = $response['body'];
    $html = explode('value="Arpm"></td>', $html);
    $html = $html[1];
    $html = explode('</table', $html);
    $html = $html[0];
    $html = explode("<td>", $html);
    $min = explode('</td>', $html[4]);
    $min = $min[0];
    $total = explode("</td>", $html[10]);
    $total = $total[0];
    $finaldata = array(
        'RNK-Minutes' => $min,
        'RNK-Total' => $total
    );
    save2cache($originalDate, $finaldata);
    return $finaldata;
}

function getnet2phone($date)
{
    $originalDate = $date;
    $finaldata = array(
        'IDT-minutes',
        'IDT-spend'
    );
    $cached = getcache($originalDate, $finaldata);
    if ($cached) {
        return $cached;
    }
    global $max_redirect;
    $curl = new Curl_Client(array(

        CURLOPT_FRESH_CONNECT => 1,
        CURLOPT_TIMEOUT => 30,
        CURLOPT_USERAGENT => 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ja; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_SSL_VERIFYPEER => false

    ), $max_redirect);


    $curl->get("https://secure.net2phonewholesale.com/");
    $html = $curl->currentResponse();
    $html = $html['body'];
    $x = explode('<input name="authenticity_token" type="hidden" value="', $html);

    $x = explode('" /></div>', $x[1]);
    $x = $x[0];
    $data = array(
        'authenticity_token' => $x,
        'user[login]' => 'baruchherzfeld',
        'user[password]' => 'Redp@nd@',
        'commit' => 'Sign in'
    );

    $curl->post("https://secure.net2phonewholesale.com/users/sign_in", $data);

    $curl->setHeadersFromString("Accept:application/json, text/javascript, */*; q=0.01;;;Accept-Encoding:gzip, deflate;;;Accept-Language:en-us,en;;;q=0.5;Referer:https://secure.net2phonewholesale.com/dashboard;;;X-CSRF-Token:$x;;;X-Requested-With:XMLHttpRequest"
    );

    $curl->get("https://secure.net2phonewholesale.com/minute_spend_graph");

    $html = $curl->currentResponse();
    $body = $html['body'];
    $body = json_decode($body, 1);
    $row = array();
    foreach ($body as $r) {
        if ($r['call_date'] == $date) {
            $row = $r;
            break;
        }
    }
    $finaldata = array(
        'IDT-minutes' => $row['minutes'],
        'IDT-spend' => $row['spend']
    );
    save2cache($originalDate, $finaldata);
    return $finaldata;
}


function save2cache($date, $values)
{
    $cacheFile = getDataFileName();
    $data = @file_get_contents($cacheFile);
    $data = json_decode($data, 1);
    if (!is_array($data)) {
        $data = array();
    }
    if (!isset($data[$date])) {
        $data[$date] = $values;
    } else {
        $data[$date] = array_merge($data[$date], $values);
    }
    @unlink($cacheFile);
    $file = fopen($cacheFile, "a+");
    fwrite($file, json_encode($data));
    fclose($file);
}

function getcache($date, $values)
{
    global $cache;
    if ($cache) {
        echo "<!-- Ignore Cache -->";
        return false;
    }
    $cacheFile = getDataFileName();
    $data = @file_get_contents($cacheFile);
    $data = json_decode($data, 1);
    if (isset($data[$date])) {
        $final = array();
        foreach ($values as $name) {
            if (isset($data[$date][$name]) && strlen($data[$date][$name]) > 1) {
                $final[$name] = $data[$date][$name];
            } else {
                return false;
            }
        }
        return $final;
    }
    return false;
}

?>

<!doctype html>

<html lang="en">
<head>
    <meta charset="utf-8"/>
    <title>Quick Summary</title>
    <link rel="stylesheet" href="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.1/themes/base/jquery-ui.css"/>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.1/jquery-ui.min.js"></script>

    <script>
        $(function () {
            $("#datepicker").datepicker({
                format:'Y-m-d'
            });
        });
    </script>
</head>
<body>
<form>
    <p>Date: <input type="text" id="datepicker" name="date" value='<?=@$_GET['date']?>'/></p>
    <input type=hidden name=pass value='<?=$_GET['pass']?>'><br>
    <input type=checkbox name=nocache value=1>Get Data from Site<br>
    <input type=submit value="Get Data">
</form>
<br>
<?php echo $html ?>

</body>
</html>