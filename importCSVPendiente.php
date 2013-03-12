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
		 $att1 = mysql_real_escape_string($data[1]); 
 		 $att2 = mysql_real_escape_string($data[2]); 
 		 $att3 = mysql_real_escape_string($data[3]); 
 		 $att4 = mysql_real_escape_string($data[4]); 
 		 $att5 = mysql_real_escape_string($data[5]); 
 		 $att6 = mysql_real_escape_string($data[6]); 
 		 $att7 = mysql_real_escape_string($data[7]); 
 		 $att8 = mysql_real_escape_string($data[8]); 
 		 $att9 = mysql_real_escape_string($data[9]); 
 		 $att10 = mysql_real_escape_string($data[10]); 
 		 $att11 = mysql_real_escape_string($data[11]); 
 		 $att12 = mysql_real_escape_string($data[12]); 
 		 $att13 = mysql_real_escape_string($data[13]); 
 		 $att14 = mysql_real_escape_string($data[14]); 
 		 $att15 = mysql_real_escape_string($data[15]); 
 		 $att16 = mysql_real_escape_string($data[16]); 
 		 $att17 = mysql_real_escape_string($data[17]); 
 		 $att18 = mysql_real_escape_string($data[18]); 
 		 $att19 = mysql_real_escape_string($data[19]); 
 		 $att20 = mysql_real_escape_string($data[20]); 
 		 $att21 = mysql_real_escape_string($data[21]); 
 		 $att22 = mysql_real_escape_string($data[22]); 
 		 $att23 = mysql_real_escape_string($data[23]); 
 		 $att24 = mysql_real_escape_string($data[24]); 
 		 $att25 = mysql_real_escape_string($data[25]); 
 		 $att26 = mysql_real_escape_string($data[26]); 
		/*
		.
		.
		.
		$attN = mysql_real_escape_string($data[N]);

		*/
		
		$sql = "INSERT INTO `tbl_name` (
					 ` Item Number ` ,
					 ` Description  ` , 
					 ` Branch Plant ` ,
					 ` S/T 700 ` ,
					 ` S/T 799 ` , 
					 ` Discotinued by OAI? ` ,
					 ` Replacement Item # (JDE) ` , 
					 ` It Mg ` , 
					 ` Print Message ` , 
					 ` G/L Code ` , 
					 ` Segment ` , 
					 ` Sls Cd1 Description 1 ` ,
					 ` Line ` ,
					 ` Sls Cd2 Description 1 ` ,
					 ` Group ` ,
					 ` Sls Cd3 Description 1 ` ,
					 ` Class ` ,
					 ` Sls Cd4 Description 1 ` ,
					 ` Supplier Number ` ,
					 ` Supplier Name ` ,
					 ` Exception ` ,
					 ` Vendor ` ,
					 ` Standard Cost ` ,
					 ` Transfer Price (OAI) ` ,
					 ` Transfer Price (Exceptions) ` ,
					 ` Found in OLA Price List ` ,
					 `OLA List Price ` ,
					 ` Net Price (GI 27%) ` ,
					 ` % Discount (GI) ` ,
					 ` Net Price (SP 27%) ` ,
					 ` % Discount (SP) ` ,
					 ` Discrepancies found ` ,
					 ` List 146P V2 OLYMPUS ` ,
					 ` Net 146P V3 OLYMPUS ` ,
					 ` Descontinuados ` ,
					 ` DISTRIBUTOR DISCOUNT ` ,
					 ` GM $ OLA OLYMPUS ` ,
					 ` GM% OLA OLYMPUS ` ,
					 ` 146 Gyrus Acmi List ` ,
					 ` 147 Gyrus Acmi Net ` ,
					 ` DISTRIBUTOR DISCOUNT ` ,
					 ` GM $ OLA Gyrus ` ,
					 ` GM% OLA Gyrus `

					)
					VALUES ('" . $att1 . "', '" . $att2 . "', '" . $att3 . "', '" . $att4 . "', '" . $att5 . "', '" . $att6 . "', '" . $att7 . "', '" . $att8 . "', '" . $att9 . "', '" . $att10 . "', '" . $att11 . "', '" . $att12 . "', '" . $att13 . "', '" . $att14 . "', '" . $att15 . "', '" . $att16 . "', '" . $att17 . "', '" . $att18 . "', '" . $att19 . "', '" . $att20 . "', '" . $att21 . "', '" . $att22 . "', '" . $att23 . "', '" . $att24 . "', '" . $att25 . "', '" . $att26 . "')";
		mysql_query($sql);
	}
	mysql_close($link);
	echo "CSV file successfully imported.";
}
else{
	die("error en la carga");
}
?>
