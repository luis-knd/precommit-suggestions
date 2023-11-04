<?php
function getComboArray($name, $array, $opciones=NULL) {

	$ret = "<option value=''>Seleccionar...</option>\n";
	if($array) {
		foreach($array as $r){
			$r = array_values($r);
			$ret .= "<option value='{$r[0]}'>{$r[1]}</option>\n";
		}
	}
	$ret = "<select name='{$name}' id='{$name}' {$opciones}>\n" . $ret . "</select>\n";
	return $ret;
}