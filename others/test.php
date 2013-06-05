<?php
$fname = "/home/parth/data/cache.json";
$file = fopen($fname, "w+");
fwrite($file, "helo");
fclose($file);

echo file_get_contents($fname);


?>
