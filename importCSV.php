<?PHP

if($_FILES["file"]["type"] != "application/vnd.ms-excel"){
	die("error en tipo de archivo.");
}
elseif(is_uploaded_file($_FILES['file']['tmp_name'])){
	//conneccin a  la base
	$dbhost = 'localhost';
	$dbuser = 'root';
	$dbpass = 'password';
	$dbname = 'base';
	$link = mysql_connect($dbhost, $dbuser, $dbpass) or die('Error connecting to mysql server');
	mysql_select_db($dbname);
	
	$handle = fopen($_FILES['file']['tmp_name'], "r");
	$data = fgetcsv($handle, 1000, ";"); //quitar si el archivo no tiene cabecerasRemove
	while (($data = fgetcsv($handle, 1000, ";")) !== FALSE) {
		$att0 = mysql_real_escape_string($data[0]);
		$att1 = mysql_real_escape_string($data[1]);
		$att2 = mysql_real_escape_string($data[2]);
		$att3 = mysql_real_escape_string($data[3]);
		/*
		.
		.
		.
		$attN = mysql_real_escape_string($data[N]);

		*/
		
		$sql = "INSERT INTO `tbl_name` (
					`attribute0` ,
					`attribute1` ,
					`attribute2` ,
					`attribute3`
					)
					VALUES ('" . $att0 . "', '" . $att1 . "', '" . $att2 . "', '" . $att3 . "')";
		mysql_query($sql);
	}
	mysql_close($link);
	echo "CSV file successfully imported.";
}
else{
	die("error en la carga");
}
?>
