<?php
/**
 * Created by Parth Mudgal.
 * Date: 8/10/12
 * Time: 10:03 PM
 */

include ("config.php");

$action = $_GET['action'];

if ($action == "login") {
    header("Location: index.html");
    die();
}

if ($action == "getSavedQuery") {

    global $reportDb;
    $name = $_GET['name'];
    $limit = isset($_GET['limit']) ? $_GET['limit'] : 1000;
    $res = $reportDb->select()->from("reports", array("sql", "database"))->where("name =?", $name)->query();
    if ($res->rowCount() == 0) {
        die("error");
    }
    $res = $res->fetch();
    $_SESSION['last_query'] = $res['sql'];
    $_SESSION['executeDB'] = $res['database'];
    $_SESSION['limit'] = $limit;

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
    die(json_encode($res));
}

if ($action == "saveQuery") {
    global $reportDb;
    $name = $_GET['name'];
    $query = @$_SESSION['last_query'];
    if (strlen($query) < 10) {
        die("No Query");
    }
    global $dbName;
    $select = $reportDb->select();
    $res = $select->from("reports")->where("name=?", $name)->query();
    if ($res->rowCount() > 0) {
        $reportDb->update("reports",
            array("database" => $dbName,
                "sql" => $query),
            "name='$name'"
        );
    } else {
        $reportDb->insert("reports", array(
            "name" => $name,
            "database" => $dbName,
            "sql" => $query
        ));
    }
    die("success");
}

if ($action == "csvgo") {
    $query = $_SESSION['last_query'];
    $limit = isset($_SESSION['limit']) ? $_SESSION['limit'] : 1000;
    header("Cache-Control: public");
    header("Content-Description: File Transfer");
    header("Content-Disposition: attachment; filename=data.csv");
    header("Content-Type: application/text");
    header("Content-Transfer-Encoding: ascii");

    $query = rtrim($query . "; ");
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
    $request_body = file_get_contents('php://input');
    $json = xml2array(urldecode($request_body));

    $json = $json['q'];


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
    for ($i = 0; $i < count($queries); $i++) {
        //die(var_dump($queries[$i]));
        $queries[$i]['fn'] = str_replace(
            $queries[$i]['colName'],
            '`' . $tableAlias[$queries[$i]['tn']] . "`.`" . $queries[$i]['colName'] . '`',
            //$tableAlias[$queries[$i]['tn']] . "." . $queries[$i]['colName'],
            $queries[$i]['fn']
        );

        $query = $queries[$i];
        if (!is_array($query['ag'])) {
            $queries[$i]['fn'] = $query['ag'] . "(" . $query['fn'] . ") as sum_{$query['colName']}";
            $query = $queries[$i];
        }

        $displayColumn[$query['fn']] = $query['d'];
        $columnsOfTable[$query['tn']][] = $query['fn'];
        $allColumns[] = $query['fn'];
    }

    $select = $defaultDb->select();


    if (is_array($relations)) {
        foreach ($relations as $relation) {
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
            if (!is_array($query["o$i"])) {
                $select->where("{$query['fn']} {$query["o$i"]}");
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
    $select->limit(1000);
    #die(print_r($select->__toString()));


    try {
        $res = $select->query();
    } catch (Exception $e) {
        echo "window.result='error';";
        echo "window.error=" . json_encode(array("error" => $e->getMessage(), "sql" => $select->__toString()));
        die();
    }


    $data = $res->fetchAll();
    if ($res->rowCount() > 0) {
        $r = $data[0];
        $columnsAll = array_keys($r);
    } else {
        $columnsAll = $allColumns;
    }

    echo "window.result='success';";
    echo "window.columns=" . json_encode($columnsAll) . ";\n";
    echo "window.sql=" . json_encode(array("sql"=>$select->__toString())) . ";console.log(window.sql);\n";
    echo "window.data=" . json_encode($data, 1) . ";\n";
    die();
}

if ($action == "getTables") {
    header("Content-type: text/json");
    $tablesres = $defaultDb->query("show tables");
    $tables = $tablesres->fetchAll();
    $tdata = array();
    foreach ($tables as $name) {
        $colname = array_keys($name);
        $colname = $colname[0];
        $tdata[] = array("table" => $name[$colname]);
    }

    echo "var tables=" . json_encode($tdata) . ";\n";
    die();
}

header("Content-type: text/xml");

function getTableColumns($table)
{
    global $defaultDb;
    $sql = "show create table $table";
    $res = $defaultDb->query($sql);
    $r = $res->fetch();
    $data = $r['Create Table'];
    $data = explode("\n", $data);

    $tables = array();
    foreach ($data as $row) {
        $row = trim($row);
        if ($row[0] != '`') {
            continue;
        }
        $x = explode(" ", $row);
        $x = str_replace("`", "", $x[0]);
        $tables[] = $x;
    }
    return $tables;
}

if ($action == "getColumns") {
    $table = $_GET['table'];
    $columns = getTableColumns($table);
    echo '<?xml version="1.0"?>' . "\n";
    echo '<columns>';
    foreach ($columns as $column) {
        echo '<column><name>' . $column . '</name></column>';
    }
    echo '</columns>';
}

if ($action == "getSchemas") {
    echo '<?xml version="1.0"?>' . "\n";
    echo '<schemas>';
    foreach (array_keys($dbData) as $schema) {
        echo '<schema><name>' . $schema . '</name></schema>';
    }
    echo '</schemas>';
    die();
}


function myErrorHandler($errno, $errstr, $errfile, $errline)
{


    if (!(error_reporting() & $errno)) {
        // This error code is not included in error_reporting
        return;
    }

    echo "window.result='error';";
    echo "window.error=" . json_encode(array("error" => $errstr, "line" => $errline, "file" => $errfile));
    die();

    /* Don't execute PHP internal error handler */
    return true;
}

set_error_handler("myErrorHandler");
?>