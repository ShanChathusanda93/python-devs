<?php 
 require_once '/home/shan/Developments/Projects/research-devs/python-devs/fileHandler/phpSnippets/dbconnection/connection.php'; $sql = "SELECT username,post_name, post_image FROM  post_image "; mysqli_query($link, $sql); $result = mysqli_query($link, "SELECT * FROM  post_image  ");  
?>