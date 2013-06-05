<?php
set_error_handler("myErrorHandler");
/**
 * Created by Parth Mudgal.
 * Date: 9/29/12
 * Time: 4:25 PM
 */

include ("config.php");
include ("lib/php-sql-parser.php");
$sql = $_POST['sql'];

$start = microtime(true);
$parser = new PHPSQLParser($sql, true);

$parsed = $parser->parsed;
$select = $parsed['SELECT'];


$columns = array();
$aliasToColumn = array();
$columnsWithoutAlias = array();
$colsWithTable = 0;
$allColumns = array();
$n = 1;
$namesTaken = array();
foreach ($select as $sel) {
    if ($sel['expr_type'] == "expression" && !$sel['alias']) {
        die(json_encode(
            array(
                'result' => 'error',
                'error' => 'Expression ' . $sel['base_expr'] . " has no alias. Please add an Alias for this column in the SQL"
            )
        ));
    } else {
        if ($sel['alias']) {
            $colname = $sel['alias']['name'];
        } else {
            $sel['base_expr'] = str_replace("`", "", $sel['base_expr']);
            $colname = explode(".", $sel['base_expr']);
            if (count($colname) > 1) {
                $colname = $colname[1];
            } else {
                $colname = $colname[0];
            }
        }

    }
    $colname = getName($colname);
    $columns[] = array('base' => $sel['base_expr'], 'alias' => $colname); //$array[0] . "_" . $array[1];

    /*    if (is_array($sel['alias']) && isset($sel['alias']['name'])) {
        $columns[$colname]['as'] = $colname;
    }*/
}

header("Content-type: text/json");
die(json_encode($columns));


function getName($name)
{
    global $namesTaken;
    if (isset($namesTaken[$name])) {
        $n = $namesTaken[$name];
        $namesTaken[$name]++;
        $name = getName($name . $n);
    } else {
        $namesTaken[$name] = 1;
    }
    return $name;
}

$from = $parsed['FROM'];
$tables = array();
$aliasToTable = array();
foreach ($from as $t) {
    $tableName = $t['table'];
    $tables[$tableName]['tablaName'] = $tableName;

    if (is_array($t['alias']) && isset($t['alias']['name'])) {
        $tables[$tableName]['alias'] = $t['alias']['name'];
        $tables[$tableName]['columns']
            = array_merge(
            isset($aliasToColumn[$tables[$tableName]['alias']]) ? $aliasToColumn[$tables[$tableName]['alias']] : array(),
            isset($aliasToColumn[$tables[$tableName]['tablaName']]) ? $aliasToColumn[$tables[$tableName]['tablaName']] : array()
        );
    } else {
        $tables[$tableName]['columns'] = $aliasToColumn[$tables[$tableName]['tablaName']];
    }

    $tables[$tableName]['allColumns'] = getTableColumns($tableName);

}


function getTableColumns($table)
{
    global $defaultDb;
    $sql = "show columns in $table";
    $res = $defaultDb->query($sql);
    $columns = array();
    while ($r = $res->fetch()) {
        $columns[$r['Field']] = array(
            "ColumnName" => $r['Field'],
            "TableName" => $table,
            "Type" => getColumnType($r['Type']),
            //"Type" => $r['Type'],
            'Selected' => false
        );
    }
    return $columns;
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
