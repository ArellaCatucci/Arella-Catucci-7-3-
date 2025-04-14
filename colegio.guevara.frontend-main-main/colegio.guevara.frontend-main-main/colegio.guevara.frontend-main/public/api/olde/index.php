<?php
header('Access-Control-Allow-Origin: *');
header("Access-Control-Allow-Headers: X-API-KEY, Origin, X-Requested-With, Content-Type, Accept, Access-Control-Request-Method");
header('Access-Control-Allow-Methods: POST, GET, PATCH, DELETE');
header("Allow: GET, POST, PATCH, DELETE");

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {    
   return 0;    
}  

$metodo = strtolower($_SERVER['REQUEST_METHOD']);
$accion = explode('/', strtolower($_GET['accion']));
$funcionNombre = $metodo . ucfirst($accion[0]);
$parametros = array_slice($accion, 1);
if (count($parametros) >0 && $metodo == 'get') {
    $funcionNombre = $funcionNombre.'ConParametros';
}
if (function_exists($funcionNombre)) {
    call_user_func_array ($funcionNombre, $parametros);
} else {
    outputError(400);
}

function outputJson($data, $codigo = 200)
{
    header('', true, $codigo);
    header('Content-type: application/json');
    print json_encode($data);
}

function outputError($codigo = 500)
{
    switch ($codigo) {
        case 400:
            header($_SERVER["SERVER_PROTOCOL"] . " 400 Bad request", true, 400);
            die;
        case 404:
            header($_SERVER["SERVER_PROTOCOL"] . " 404 Not Found", true, 404);
            die;
        default:
            header($_SERVER["SERVER_PROTOCOL"] . " 500 Internal Server Error", true, 500);
            die;
            break;
    }
}

function inicializarBBDD()
{
    return $bd = new SQLite3(__DIR__ . '/../../adicional/baseDatos.db');
}

function postRestablecer()
{
    $bd = inicializarBBDD();
    $sql = file_get_contents(__DIR__ . '/../../adicional/dump.sql');
    $result = $bd->exec($sql);
    outputJson([]);
}

function getServicios()
{
    $bd = inicializarBBDD();
    $result = $bd->query('SELECT * FROM servicios');
    $ret = [];
    while ($fila = $result->fetchArray(SQLITE3_ASSOC)) {
        settype($fila['id'], 'integer');
        $ret[] = $fila;
    }
    outputJson($ret);
}

function getEventos()
{
    $bd = inicializarBBDD();
    $result = $bd->query('SELECT eventos.id AS id, eventos.nombre AS nombre, eventos.fecha AS fecha, GROUP_CONCAT(servicios.descripcion) AS servicios FROM eventos LEFT JOIN eventos_servicios ON eventos.id=eventos_servicios.id_evento LEFT JOIN servicios ON servicios.id=eventos_servicios.id_servicio GROUP BY eventos.id');
    $ret = [];
    while ($fila = $result->fetchArray(SQLITE3_ASSOC)) {
        settype($fila['id'], 'integer');
        $fila['servicios'] = $fila['servicios']=='' ? [] : explode(',', $fila['servicios']);
        $ret[] = $fila;
    }
    outputJson($ret);
}

function getEventosConParametros($id)
{
    $bd = inicializarBBDD();
    settype($id, 'integer');
    $result = $bd->query("SELECT eventos.id AS id, eventos.nombre AS nombre, eventos.fecha AS fecha, GROUP_CONCAT(eventos_servicios.id_servicio) AS servicios FROM eventos LEFT JOIN eventos_servicios ON eventos.id=eventos_servicios.id_evento WHERE id=$id GROUP BY eventos.id");
    $ret = [];
    $fila = $result->fetchArray(SQLITE3_ASSOC);
    settype($fila['id'], 'integer');
    $fila['servicios'] = $fila['servicios']=='' ? [] : array_map(function ($v) { return $v+0;},  explode(',', $fila['servicios']));
    outputJson($fila);
}

function postEventos()
{
    $bd = inicializarBBDD();
    $datos = json_decode(file_get_contents('php://input'), true);
    
    $nombre = $bd->escapeString($datos['nombre']);
    $fecha = $datos['fecha'];
    $servicios = implode(',', $datos['servicios']);

    $result = @$bd->exec("INSERT INTO eventos (nombre, fecha) VALUES ('$nombre', '$fecha')");
    $id = $bd->lastInsertRowID();
    $result = @$bd->exec("INSERT INTO eventos_servicios (id_evento, id_servicio) SELECT $id as id_evento, servicios.id AS id_servicio FROM servicios WHERE servicios.id in ($servicios)");
    outputJson(['id' => $id]);
}

function patchEventos($id)
{
    settype($id, 'integer');
    $bd = inicializarBBDD();
    $datos = json_decode(file_get_contents('php://input'), true);
    
    $nombre = $bd->escapeString($datos['nombre']);
    $fecha = $datos['fecha'];
    $servicios = implode(',', $datos['servicios']);

    $result = @$bd->exec("UPDATE eventos SET nombre='$nombre', fecha='$fecha' WHERE id=$id");
    $result = $bd->query("DELETE FROM eventos_servicios WHERE id_evento=$id");
    $result = @$bd->exec("INSERT INTO eventos_servicios (id_evento, id_servicio) SELECT $id as id_evento, servicios.id AS id_servicio FROM servicios WHERE servicios.id in ($servicios)");
    outputJson(['id' => $id]);
}

function deleteEventos($id)
{
    settype($id, 'integer');
    $bd = inicializarBBDD();
    $result2 = $bd->query("DELETE FROM eventos_servicios WHERE id_evento=$id");
    $result1 = $bd->query("DELETE FROM eventos WHERE id=$id");
    
    outputJson([]);
}
