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
if (count($parametros) > 0 && $metodo == 'get') {
    $funcionNombre = $funcionNombre . 'ConParametros';
}

if (function_exists($funcionNombre)) {
    call_user_func_array($funcionNombre, $parametros);
} else {
    outputError(400);
}

function outputJson($data, $codigo = 200)
{
    http_response_code($codigo);
    header('Content-Type: application/json');
    echo json_encode($data);
    error_log("outputJson: " . json_encode($data));
    exit;
}

function outputError($codigo = 500)
{
    http_response_code($codigo);
    die;
}

function inicializarBBDD()
{
    $servidor = 'localhost';
    $usuario = 'root';
    $contrasena = 'admin';
    $baseDatos = 'colegio_guevara';

    $conexion = new mysqli($servidor, $usuario, $contrasena, $baseDatos);

    if ($conexion->connect_error) {
        die('Error de conexión: ' . $conexion->connect_error);
    }

    return $conexion;
}

function postRestablecer()
{
    $bd = inicializarBBDD();
    $sql = file_get_contents(__DIR__ . '/../../adicional/dump.sql');
    $bd->query($sql);
    outputJson(['message' => 'Base de datos restablecida']);
}


function getVersion()
{
    return outputJson("v1.1");
}


function getMedia_Files()
{
    $bd = inicializarBBDD(); // Inicializa la conexión MySQL

    $query = "SELECT id,type,title,owner,src,uid_media, created_at FROM frontend_media_files order by id desc";
    $result = $bd->query($query);

    if ($result === false) {
        outputError(500); // Error en la consulta
    }

    // $nuevoComentario = [
    //     "user" => [
    //         "name" => "La china",
    //         "photo" => "https://imgs.search.brave.com/gcwOOYD00OXPSoDvIGk4yV64O2-MvnZyH8Wgf9QGvlw/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly93d3cu/aXN0b2NrcGhvdG8u/Y29tL3Jlc291cmNl/cy9pbWFnZXMvUGhv/dG9GVExQLzEwNTg4/MzQ2MTYuanBn"
    //     ],
    //     "text" => "Este video es fascinante.",select * from media_files mf;
    //     "date" => date('Y-m-d H:i:s') // Formatear la fecha en un formato legible
    // ];
    
    $media_files = [];
    while ($fila = $result->fetch_assoc()) {

        $queryComments = "SELECT user_name, user_photo, comment_text as text, created_at FROM frontend_media_files_comments where uid_media = '" . $fila['uid_media'] . "' order by created_at desc";
        $resultComments = $bd->query($queryComments);
    
        if ($result === false) {
            outputError(500); // Error en la consulta. Devuelve error code 500.
        }
       
        $media_files_comments = [];
        while ($filaComments = $resultComments->fetch_assoc()) {
            $user = [
                "name" => $filaComments['user_name'] ,
                "photo" => $filaComments['user_photo']
            ];
            $comment = [
                "user" => $user,
                "text" => $filaComments['text'],
                "date" => $filaComments['created_at']
            ];
            $media_files_comments[] = $comment;
        }
     
        $fila['id'] = (int) $fila['id']; // Convierte el ID a entero

        if (strpos($fila['src'], "http") !== 0) {
            $fila['src'] = 'http://localhost/frontend/public/api/' . $fila['src'];
        }
        $fila['comments'] = $media_files_comments; 
        $media_files[] = $fila;
    }

    $bd->close(); // Cierra la conexión
    outputJson($media_files);
}

function getMedia_files_OWNERConParametros($username)
{
    $conexion = inicializarBBDD(); // Asegurar que la conexión es válida

    // Recupara parametros de setting
    $query = "SELECT valor FROM core_setting WHERE codigo = 'dominio'";
    $result = $conexion->query($query);

    $dominio = 'localhost'; // Valor por defecto

    if ($result && $fila = $result->fetch_assoc()) {
        $dominio = $fila['valor'];
    }


    // Preparar la consulta
    $rol = 'alumno';
    $stmt = $conexion->prepare("
        select rol from core_usuario cu where cu.username = ?
    ");
    
    if (!$stmt) {
        die("Error en la preparación de la consulta: " . $conexion->error);
    }

    $stmt->bind_param("s", $username); // "s" porque username es string
    $stmt->execute(); // Ejecutar la consulta

    $result = $stmt->get_result(); // Obtener el resultado
    if ($fila = $result->fetch_assoc()) {
       $rol = $fila['rol']; 
    }
  
    // Preparar la consulta
    if ($rol == 'alumno') {
        $stmt = $conexion->prepare("SELECT * FROM frontend_media_files WHERE owner = ? ");
    } else {
        $stmt = $conexion->prepare("SELECT * FROM frontend_media_files ");
    }
      
    if (!$stmt) {
        die("Error en la preparación de la consulta: " . $conexion->error);
    }

    if ($rol == 'alumno') {
        $stmt->bind_param("s", $username); // "s" porque username es string
    } 
    
    $stmt->execute(); // Ejecutar la consulta

    $result = $stmt->get_result(); // Obtener el resultado
    
    $resultOutput = [];
    while ($fila = $result->fetch_assoc()) {
        $queryComments = "SELECT user_name, user_photo, comment_text as text, created_at FROM frontend_media_files_comments where uid_media = '" . $fila['uid_media'] . "' order by created_at desc";
        $resultComments = $conexion->query($queryComments);
    
        if ($result === false) {
            outputError(500); // Error en la consulta. Devuelve error code 500.
        }
       
        $media_files_comments = [];
        while ($filaComments = $resultComments->fetch_assoc()) {
            $user = [
                "name" => $filaComments['user_name'] ,
                "photo" => $filaComments['user_photo']
            ];
            $comment = [
                "user" => $user,
                "text" => $filaComments['text'],
                "date" => $filaComments['created_at']
            ];
            $media_files_comments[] = $comment;
        }


        if (strpos($fila['src'], "http") !== 0) { // Si no tiene un protocolo HTTP(S)
            if (strpos($fila['src'], "uploads") === 0) { 
                // Si la ruta empieza con "uploads", añade el dominio normal
                $fila['src'] = "http://$dominio/frontend/public/api/{$fila['src']}";
            } elseif (strpos($fila['src'], "generar-grafico") === 0) {
                // Si la ruta empieza con "generar-grafico", añade el puerto 8000
                $fila['src'] = "http://$dominio:8000/{$fila['src']}";
            }
        }
        
        $fila['comments'] = $media_files_comments; 

        $resultOutput[] = $fila;
    }

    outputJson($resultOutput); // Enviar la salida en formato JSON

    $stmt->close(); // Cerrar el statement
    $conexion->close(); // Cerrar la conexión
}


function postUploadFile() {
    $uploadDir = "uploads/";
    $maxSize = 5 * 1024 * 1024;
    $allowedTypes = ["jpg", "png", "gif", "pdf", "mp4", "jpeg"];
    //$inputName = array_key_first($_FILES) ?? "file";
    $inputName = 'file';
    // Verificar si se envió un archivo
    if (!isset($_FILES[$inputName]) || $_FILES[$inputName]['error'] !== UPLOAD_ERR_OK) {
        return outputJson(["error" => "No se ha subido ningún archivo o hubo un error en la carga."], 404);
    }

    $file = $_FILES[$inputName];
    $fileName = basename($file["name"]);
    $fileSize = $file["size"];
    $fileTmp = $file["tmp_name"];
    $fileExt = strtolower(pathinfo($fileName, PATHINFO_EXTENSION));

    // Validar tipo de archivo
    if (!in_array($fileExt, $allowedTypes)) {
        return ["error" => "Tipo de archivo no permitido. Solo se permiten: " . implode(", ", $allowedTypes)];
    }

    // Validar tamaño de archivo
    if ($fileSize > $maxSize) {
        return ["error" => "El archivo es demasiado grande. Máximo permitido: " . ($maxSize / 1024 / 1024) . "MB"];
    }

    // Crear directorio si no existe
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    // Generar un nombre único para evitar conflictos
    $newFileName = uniqid() . "." . $fileExt;
    //$uploadPath = $uploadDir . substr($newFileName,1);
    $uploadPath = $uploadDir . $newFileName;
    
    // Mover archivo al directorio de destino
    if (move_uploaded_file($fileTmp, $uploadPath)) {
        return outputJson(["uid_media" => uniqid(), "fileUrl" => $uploadPath]);
    } else {
        return outputJson(["error" => "Error al mover el archivo.".$uploadPath], 500);
    }
}



function postLogin_php()
{
    $bd = inicializarBBDD();
    $datos = json_decode(file_get_contents('php://input'), true);

    $username = $bd->real_escape_string($datos['username']);
    $password = $bd->real_escape_string($datos['password']);

    // Validar que los datos requeridos estén presentes
    if (!isset($datos['username']) || !isset($datos['password'])) {
        http_response_code(400);
        echo json_encode(["detail" => $datos]);
        return;
    }

    $query = "SELECT * FROM frontend_users WHERE username = '$username'";
    $resultado = $bd->query($query);

    if ($resultado && $fila = $resultado->fetch_assoc()) {
        // Verificar la contraseña.
        $hashedPassword = $fila['password']; // Contraseña almacenada (ya hasheada).
        $url = $fila['url'];
        if (password_verify($password, $hashedPassword)) {
            // Login exitoso.
            
            $arrayAsociativo['username'] = $datos['username'];
            $arrayAsociativo['url'] = $url;
            
            outputJson( $arrayAsociativo);
        } else {
            // Contraseña incorrecta.
            outputJson("credenciales incorrectas",401);
        }
    } else {
        // Usuario no encontrado.
        http_response_code(401);
        echo json_encode(["detail" => "Invalid credentials"]);
    }
   
}

function verify_django_password($password, $stored_hash) {
    list($algorithm, $iterations, $salt, $hash) = explode('$', $stored_hash);

    if ($algorithm !== 'pbkdf2_sha256') {
        return false; // No compatible con otros algoritmos
    }

    $iterations = (int) $iterations;
    $hash_length = strlen(base64_decode($hash, true));
    
    // Generar el hash con los mismos parámetros de Django
    $computed_hash = hash_pbkdf2("sha256", $password, $salt, $iterations, $hash_length, true);
    
    // Comparar el hash calculado con el almacenado en la base de datos
    return hash_equals(base64_decode($hash), $computed_hash);
}

function postLogin()
{
    $bd = inicializarBBDD();
    $datos = json_decode(file_get_contents('php://input'), true);

    $username = $bd->real_escape_string($datos['username']);
    $password = $bd->real_escape_string($datos['password']);

    // Validar que los datos requeridos estén presentes
    if (!isset($datos['username']) || !isset($datos['password'])) {
        http_response_code(400);
        echo json_encode(["detail" => "Missing username or password"]);
        return;
    }

    $query = "SELECT * FROM core_usuario WHERE username = '$username'";
    $resultado = $bd->query($query);

    if ($resultado && $fila = $resultado->fetch_assoc()) {
        // Verificar la contraseña con PBKDF2 usada por Django
        $hashedPassword = $fila['password']; // Contraseña almacenada en Django
        $url = $fila['url'];

        if (verify_django_password($password, $hashedPassword)) {
            // Login exitoso
            $arrayAsociativo['username'] = $datos['username'];
            $arrayAsociativo['url'] = $url;
            $arrayAsociativo['rol'] = $fila['rol'];
            outputJson($arrayAsociativo);
        } else {
            // Contraseña incorrecta
            outputJson("Login_new: credenciales incorrectas", 401);
        }
    } else {
        // Usuario no encontrado
        http_response_code(401);
        echo json_encode(["detail" => "Invalid credentials"]);
    }
}

function getUsers()
{
    $bd = inicializarBBDD(); // Inicializa la conexión MySQL
    $query = "SELECT * FROM users";
    $result = $bd->query($query);

    if ($result === false) {
        outputError(500); // Error en la consulta
    }

    $users = [];
    while ($fila = $result->fetch_assoc()) {
        $fila['id'] = (int) $fila['id']; // Convierte el ID a entero
        $users[] = $fila;
    }

    $bd->close(); // Cierra la conexión
    outputJson($users);
}


function postUsers()
{
    $bd = inicializarBBDD(); 
    $datos = json_decode(file_get_contents('php://input'), true);

    $username = $bd->real_escape_string($datos['username']);
    $password = $bd->real_escape_string($datos['password']);
    $email = $bd->real_escape_string($datos['email']);
    $hashedPassword = password_hash($password, PASSWORD_BCRYPT);

    $query = "INSERT INTO frontend_users (username, password, email) VALUES ( '$username', '$hashedPassword', '$email')";

    if ($bd->query($query)) {
        outputJson(['message' => 'Usuario creado exitosamente']);
    } else {
        outputError(500); 
    }
}



function getMedia_filesConParametros($id)
{
    $conexion = inicializarBBDD(); // Asegúrate de que inicializarBBDD retorne una conexión MySQL válida

    // Asegurarse de que el ID sea un entero
    $id = (int) $id;

    // Preparar la consulta para obtener el evento con sus servicios
    $stmt = $conexion->prepare("
        SELECT *
            
        FROM media_files
        WHERE id = ?
        ");
    
    $stmt->bind_param("i", $id); // Asignar el ID al parámetro
    $stmt->execute(); // Ejecutar la consulta

    $result = $stmt->get_result(); // Obtener el resultado de la consulta
    $result = $result->fetch_assoc(); // Obtener una fila del resultado
    outputJson($result);

    $stmt->close(); // Cerrar el statement
    $conexion->close(); // Cerrar la conexión
}




function postMedia_files()
{
    $bd = inicializarBBDD(); 
    $datos = json_decode(file_get_contents('php://input'), true);

    $title = $bd->real_escape_string($datos['title']);
    $owner = $bd->real_escape_string($datos['owner']);
    $src = $bd->real_escape_string($datos['src']);    
    $uid_media = $bd->real_escape_string($datos['uid_media']); 
    $type = $bd->real_escape_string($datos['type']);

    $query = "INSERT INTO frontend_media_files (title, owner , src, type, uid_media) VALUES ( '$title', '$owner', '$src', '$type', '$uid_media')";
  
    if ($bd->query($query)) {
        outputJson(['message' => 'frontend_media_files creado correctamente']);
    } else {
        outputError(500); 
    }
}

function postMedia_files_comments()
{
    $bd = inicializarBBDD(); 
    $datos = json_decode(file_get_contents('php://input'), true);

    $user_name = $bd->real_escape_string($datos['user']['name']);
    $user_photo = $bd->real_escape_string($datos['user']['photo']);
    $comment_text = $bd->real_escape_string($datos['text']);    
    $uid_media = $bd->real_escape_string($datos['uid_media']);

    $query = "INSERT INTO frontend_media_files_comments (uid_media, user_name, user_photo, comment_text) VALUES ( '$uid_media', '$user_name', '$user_photo', '$comment_text')";
  
    if ($bd->query($query)) {
        outputJson(['message' => 'frontend_media_files_comment creado correctamente']);
    } else {
        outputError(500); 
    }
}



function postEventos()
{
    $conexion = inicializarBBDD(); // Asegúrate de que inicializarBBDD retorne una conexión MySQL válida
    $datos = json_decode(file_get_contents('php://input'), true);

    // Validar y preparar datos
    $nombre = $conexion->real_escape_string($datos['nombre']);
    $fecha = $conexion->real_escape_string($datos['fecha']);
    $servicios = $datos['servicios'];

    if (!is_array($servicios) || empty($servicios)) {
        outputJson(['error' => 'Lista de servicios no válida'], 400);
        return;
    }

    // Iniciar una transacción para asegurar consistencia
    $conexion->begin_transaction();

    try {
        // Insertar el evento
        $stmtEvento = $conexion->prepare("INSERT INTO eventos (nombre, fecha) VALUES (?, ?)");
        $stmtEvento->bind_param("ss", $nombre, $fecha);
        $stmtEvento->execute();
        $idEvento = $stmtEvento->insert_id;
        $stmtEvento->close();

        // Insertar los servicios relacionados al evento
        $stmtServicios = $conexion->prepare("
            INSERT INTO eventos_servicios (id_evento, id_servicio)
            VALUES (?, ?)
        ");

        foreach ($servicios as $idServicio) {
            $idServicio = (int) $idServicio; // Asegurarse de que el ID sea un entero
            $stmtServicios->bind_param("ii", $idEvento, $idServicio);
            $stmtServicios->execute();
        }
        $stmtServicios->close();

        // Confirmar la transacción
        $conexion->commit();
        outputJson(['id' => $idEvento]);
    } catch (Exception $e) {
        // En caso de error, revertir los cambios
        $conexion->rollback();
        outputJson(['error' => 'Error al insertar el evento: ' . $e->getMessage()], 500);
    } finally {
        $conexion->close(); // Cerrar la conexión
    }
}


function deleteMedia_Files($id)
{
    $conexion = inicializarBBDD(); // Asegúrate de que inicializarBBDD retorne una conexión MySQL válida
    $id = (int) $id; // Convertir $id a entero por seguridad

    // Usar prepared statements para evitar inyecciones SQL
    $stmt1 = $conexion->prepare("DELETE FROM frontend_media_FILES WHERE id = ?");
    
    if ($stmt1) {
        // Enlazar y ejecutar la primera consulta
        $stmt1->bind_param("i", $id);
        $stmt1->execute();
        $stmt1->close();

        outputJson(['message' => 'frontend_Media_files eliminado']);
    } else {
        outputJson(['error' => 'Error al preparar la consulta'], 500);
    }

    $conexion->close(); // Cerrar la conexión a la base de datos
}

?>
