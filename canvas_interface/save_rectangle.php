<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = file_get_contents('php://input');
    file_put_contents('request_body.json', $data);
    echo 'Request body written to file.';
}
?>
