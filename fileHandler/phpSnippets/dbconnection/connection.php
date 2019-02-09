<?php
$link = mysqli_connect("myserver","myuname","mypass","mydb");
if($link == false){
die('Error, could not connect.' . mysqli_connect_error());
}
?>