<?php
$mode = "none";
ini_set('display_errors', 'On');
error_reporting(E_ALL);
/**
 * Created by Parth Mudgal.
 * Date: 8/10/12
 * Time: 10:03 PM
 */
set_error_handler("myErrorHandler");
include ("config.php");

$action = $_REQUEST['action'];

if ($action == "savePivotNote") {
    global $reportDb;
    $pivot = $_REQUEST['pivot'];
    $note = $_REQUEST['note'];
    $array = array(
        'note' => $note
    );
    $reportDb->update("pivot",
        $array,
        "id='$pivot'"
    );
    die("success");

}

if ($action == "getPivotNote") {
    global $reportDb;
    $pivot = $_REQUEST['pivot'];
    $res = $reportDb->select()->from("pivot", array("note"))->where("id=?", $pivot);
    $res = $res->query()->fetch();
    $note = $res['note'];
    die(json_encode(
        array(
            'success' => 1,
            'text' => $note
        )
    ));
}

if ($action == "customQuery") {
    $data = json_decode($_REQUEST['data'], 1);
    $sql = $_REQUEST['query'];
    global $dbName;

    $_SESSION['reportData'] = json_encode(array(
        'result' => 'success',
        'columnsData' => $data,
        'sql' => $sql,
    ));

    echo json_encode(array(
        'result' => 'success',
        'columnsData' => $data,
        'sql' => $sql,
    ));
}

if ($action == "getPivot") {
    global $reportDb;
    $id = @$_REQUEST['id'];
    if ($id == "") die("error");
    $res = $reportDb->select()->from("pivot", array("data"))->where("id=?", $id);
    $res = $res->query()->fetch();
    die(json_encode($res));
}


if ($action == "getPivots") {
    global $reportDb;
    $sql = $_REQUEST['sql'];
    $sql = explode("limit", $sql);
    $sql = trim($sql[0]);
    $sql = str_replace("\n", " ", $sql);
    $sql = str_replace("\\n", " ", $sql);
    $res = $reportDb->select()->from("pivot", array("id", "name"))->where("`data` like ?", "%$sql%");
    $res = $res->query()->fetchAll();
    die(json_encode(array("queries" => $res)));
}

if ($action == "savepivot") {
    if (!isset($_REQUEST['name']) || $_REQUEST['name'] == "") {
        die(json_encode(array(
            'result' => 'error',
            'error' => 'no name given'
        )));
    }
    $name = $_POST['name'];
    $data = $_REQUEST['data'];
    global $reportDb;
    global $dbName;

    $reportDb->insert("pivot", array(
        "name" => $name,
        "database" => $dbName,
        'data' => $data
    ));
    die("success");
}

if ($action == "getLastRequest") {
    $mode = @$_REQUEST['mode'];
    if (!isset($_SESSION['reportData'])) {
        die(json_encode(array(
            'result' => 'error',
            'error' => "no data found"
        )));
    }

    //die(print_r($_SESSION['reportData']));
    $Rdata = json_decode($_SESSION['reportData'], 1);
    $query = str_replace("\n", " ", $Rdata['sql']);


    $limit = isset($_SESSION['limit']) && $_SESSION['limit'] != "" ? $_SESSION['limit'] : 20000;
    $query = rtrim($query, "; ");
    $query = $query . " limit $limit";

    if ($mode != "OnlyMeta") {
        try {
            $res = $defaultDb->query($query);
            $data = $res->fetchAll();
        } catch (Exception $e) {
            throw new Exception($query);
        }
    } else {
        $data = "";
    }


    die(json_encode(array(
        'result' => 'success',
        'columnsData' => $Rdata['columnsData'],
        'sql' => $query,
        'data' => $data
    ), JSON_NUMERIC_CHECK));
}

if ($action == "setSavedParams") {
    $data = json_decode($_REQUEST['data'], 1);

    $Rdata = isset($_SESSION['reportData']) ? json_decode($_SESSION['reportData'], 1) : array();
    $query = $_SESSION['last_query'];

    for ($i = 0; $i < count($data); $i++) {
        $name = $data[$i]['name'];
        $value = $data[$i]['value'];
        $query = str_replace("?$name?", $value, $query);
    }
    $Rdata['sql'] = $query;
    $_SESSION['reportData'] = json_encode($Rdata);
    die(json_encode(array(
        'result' => "success",
        'sql' => $query
    )));
}

if ($action == "getSavedQuery") {

    global $reportDb;
    $name = $_GET['name'];
    $limit = isset($_GET['limit']) ? $_GET['limit'] : 20000;
    $res = $reportDb->select()->from("reports", array("sql", "database", "data"))->where("name =?", $name)->query();
    if ($res->rowCount() == 0) {
        die("error");
    }
    $res = $res->fetch();

    $data = json_decode($res['data'], 1);
    preg_match_all('/\?([A-Za-z0-9_]+)\?/', $data['sql'], $matches);
    $matches = $matches[1];


    $_SESSION['last_query'] = $data['sql'];
    $_SESSION['executeDB'] = $res['database'];
    $_SESSION['limit'] = $limit;
    $_SESSION['name'] = $name;
    $_SESSION['reportData'] = $res['data'];
    if (count($matches) > 0) {
        die(json_encode(array('variables' => $matches, 'result' => 'getvariables')));
    }
    die("success");
}

if ($action == "getSaved") {
    global $reportDb;
    if (isset($_SESSION['limit'])) {
        $res = $reportDb->select()->from("reports", "name")->limit($_SESSION['limit'])->query()->fetchAll();
        unset($_SESSION['limit']);
    } else {
        $res = $reportDb->select()->from("reports", "name")->query()->fetchAll();
    }
    die(json_encode(array("queries" => $res)));
}

if ($action == "saveQuery") {
    global $reportDb;
    $name = $_GET['name'];
    $Rdata = json_decode(@$_SESSION['reportData'], 1);
    $query = str_replace("\n", " ", $Rdata['sql']);
    $data = @$_SESSION['reportData'];
    if (strlen($query) < 10) {
        die("No Query");
    }
    global $dbName;
    $select = $reportDb->select();
    $res = $select->from("reports")->where("name=?", $name)->query();
    if ($res->rowCount() > 0) {
        $reportDb->update("reports",
            array("database" => $dbName,
                "sql" => $query,
                'columnData' => $data
            ),
            "name='$name'"
        );
    } else {
        $reportDb->insert("reports", array(
            "name" => $name,
            "database" => $dbName,
            "sql" => $query,
            'data' => $data
        ));
    }
    die("success");
}

if ($action == "csvgo") {
    $Rdata = json_decode($_SESSION['reportData'], 1);
    $query = $Rdata['sql'];
    $limit = isset($_SESSION['limit']) ? $_SESSION['limit'] : 20000;
    $name = isset($_SESSION['name']) ? $_SESSION['name'] . ".csv" : "data.csv";
    $_SESSION['name'] = "data";
    $_SESSION['limit'] = 20000;
    header("Cache-Control: public");
    header("Content-Description: File Transfer");
    header("Content-Disposition: attachment; filename='$name'");
    header("Content-Type: application/text");
    header("Content-Transfer-Encoding: ascii");

    $query = rtrim($query, "; ");
    $query = $query . " limit $limit";
    $res = $defaultDb->query($query);
    if ($res->rowCount() > 0) {
        $r = $res->fetch();
        $cols = array_keys($r);
        $cols = implode(",", $cols);
        echo $cols . "\n";
        $fp = fopen('php://output', 'w');
        fputcsv($fp, $r);
        while (($r = $res->fetch()) && ($limit > 0)) {
            fputcsv($fp, $r, ",", '"');
            $limit--;
        }
    }
    die();
}

if ($action == "doRetrieve") {
    header("Content-type: text/json");
    $json = json_decode($_POST['q'], 1);


    $tables = $json['e'];
    if (!is_array($tables)) {
        $tables = array($tables);
    }

    $queries = $json['c'];
    $relations = @$json['r'];

    if (!isset($queries[0]) && isset($queries['fn'])) {
        $queries = array(0 => $queries);
    }

    if (!isset($relations[0]) && isset($relations['es'])) {
        $relations = array(0 => $relations);
    }

    $tableAlias = array();
    $tableDone = array();
    foreach ($tables as $table) {
        $tableDone[$table] = 0;
        $table1 = explode("_", $table);
        $str = "";
        foreach ($table1 as $t) {
            $str .= $t[0];
        }
        $tableAlias[$table] = $str;
    }


    $columnsOfTable = array();
    $allColumns = array();
    $displayColumn = array();
    $ColNames = array();
    $coldata = array();
    for ($i = 0; $i < count($queries); $i++) {
        //die(var_dump($queries[$i]));
        $queries[$i]['fn'] = str_replace(
            $queries[$i]['colName'],
            $tableAlias[$queries[$i]['tn']] . "." . $queries[$i]['colName'],
            $queries[$i]['fn']
        );

        $query = $queries[$i];
        if ($query['d']) {
            $coldata[] = getColumn($query['colName'], $query['tn']);
        }
        $queries[$i]['tfn'] = $queries[$i]['fn'];
        if (!is_array($query['ag']) && $query['ag'] != null) {
            $queries[$i]['fn'] = $query['ag'] . "(" . $query['fn'] . ") as sum_{$queries[$i]['tn']}_{$query['colName']}";
            $query = $queries[$i];
            if ($query['d']) {
                $columnsOfTable[$query['tn']][] = $query['fn'];
                $ColNames[] = "sum_{$queries[$i]['tn']}_{$query['colName']}";
            }
            $allColumns[] = $query['fn'];
        } else {
            if ($query['d']) {
                $columnsOfTable[$query['tn']][] = $query['fn'] . " as {$queries[$i]['tn']}_{$query['colName']}";
                $ColNames[] = "{$queries[$i]['tn']}_{$query['colName']}";
            }
            $allColumns[] = "{$queries[$i]['tn']}_{$query['colName']}";
        }

        $displayColumn[$query['fn']] = $query['d'];
    }

    $select = $defaultDb->select();

    if (is_array($relations)) {
        for ($i = 0; $i < count($relations); $i++) {
            $relation = $relations[$i];
            /*if (!isset($tableDone[$relation['et']]) || !$tableDone[$relation['et']]) {
                array_push($relations, $relation);
                continue;
            }*/

            if (!isset($tableDone[$relation['es']]) || !$tableDone[$relation['es']]) {
                $select->join(
                    array($tableAlias[$relation['es']] => $relation['es'])
                    , "{$tableAlias[$relation['es']]}.{$relation['fs']}={$tableAlias[$relation['et']]}.{$relation['ft']}"
                    , isset($columnsOfTable[$relation['es']]) ? $columnsOfTable[$relation['es']] : array());
                $tableDone[$relation['es']] = 1;
            } else {
                $select->join(
                    array($tableAlias[$relation['es']] => $relation['es'])
                    , "{$tableAlias[$relation['es']]}.{$relation['fs']}={$tableAlias[$relation['et']]}.{$relation['ft']}"
                    , isset($columnsOfTable[$relation['es']]) ? $columnsOfTable[$relation['es']] : array());
            }
        }
    }

    foreach ($columnsOfTable as $table => $columns) {
        if (!$tableDone[$table]) {
            $select->from(array($tableAlias[$table] => $table), $columns);
            $tableDone[$table] = 1;
        }
    }

    foreach ($queries as $query) {
        for ($i = 1; $i < 4; $i++) {
            if (!is_array($query["o$i"]) && strlen($query["o$i"]) > 1) {
                $select->where("{$tableAlias[$query['tn']]}.{$query['colName']} {$query["o$i"]}");
            }
        }
        if ($query['s']) {
            $order = $query['s'] == 1 ? "ASC" : "DESC";
            $tempCol = explode(" as ", "{$query['fn']}");
            $tempCol = $tempCol[0];
            $select->order("$tempCol $order");
        }

        if ($query['gb'] == "true") {
            $select->group("{$query['fn']}");
        }
    }


    $_SESSION['last_query'] = $select->__toString();

    $columnsAll = $allColumns;


    $finalColData = array();
    for ($i = 0; $i < count($columnsAll); $i++) {
        $finalColData[] = array("name" => $ColNames[$i], "type" => $coldata[$i]['type']);
    }

    $_SESSION['reportData'] = json_encode(array(
        'result' => 'success',
        'columnsData' => $finalColData,
        'sql' => $select->__toString(),
    ));

    die(json_encode(array(
        'result' => 'success',
        'columnsData' => $finalColData,
        'sql' => $select->__toString(),
    )));

}

if ($action == "getTables") {
    header("Content-type: application/json");
    $tablesres = $defaultDb->query("show tables");
    $tables = $tablesres->fetchAll();
    $tdata = array();
    foreach ($tables as $name) {
        $colname = array_keys($name);
        $colname = $colname[0];
        $tdata[] = array("TableName" => $name[$colname]);
    }

    echo json_encode(array("tables" => $tdata));
    die();
}

header("Content-type: application/json");

function getTableColumns($table)
{
    global $defaultDb;
    $sql = "show columns in $table";
    $res = $defaultDb->query($sql);
    $columns = array();
    while ($r = $res->fetch()) {
        $columns[] = array(
            "ColumnName" => $r['Field'],
            "TableName" => $table,
            "Type" => getColumnType($r['Type']),
            //"Type" => $r['Type'],
            'Selected' => false
        );
    }
    return $columns;
}

if ($action == "getColumns") {
    $table = $_GET['table'];
    $columns = getTableColumns($table);
    die(json_encode(array('Columns' => $columns)));
}

if ($action == "getSchemas") {
    $data = array();
    foreach (array_keys($dbData) as $schemaName) {
        $data[] = array('SchemaName' => $schemaName);
    }

    $data = json_encode(array("schemas" => $data));
    die($data);
    /*echo '<?xml version="1.0"?>' . "\n";
    echo '<schemas>';
    foreach (array_keys($dbData) as $schema) {
        echo '<schema><name>' . $schema . '</name></schema>';
    }
    echo '</schemas>';*/
    die();
}

function getColumnType($type)
{
    $type = substr($type, 0, 3);
    switch ($type) {
        case 'dat':
        case 'tim':
            $type = "datetime";
            break;
        case 'int':
        case 'big':
        case 'tin':
            $type = "int";
            break;
        case 'flo':
            $type = "float";
            break;
        case 'var':
        case 'cha':
            $type = "string";
            break;
        default:
            $type = 'string';
    }
    return $type;
}

function getColumn($col, $table)
{
    global $defaultDb;
    $res = $defaultDb->query("show columns in $table where field='$col';")->fetchAll();
    $res = $res[0];
    $type = substr($res['Type'], 0, 3);
    $type = getColumnType($type);
    return array('name' => $col, 'type' => $type, 'table' => $table);
}

function myErrorHandler($errno, $errstr, $errfile, $errline)
{


    if (!(error_reporting() & $errno)) {
        // This error code is not included in error_reporting
        return;
    }

    //echo "window.result='error';";
    //echo "window.error=" . json_encode(array("error" => $errstr, "line" => $errline, "file" => $errfile));
    die(json_encode(array(
        'result' => 'error',
        'error' => $errstr,
        'line' => $errline,
        'file' => $errfile
    )));
    //die();

    /* Don't execute PHP internal error handler */
    return true;
}

?>