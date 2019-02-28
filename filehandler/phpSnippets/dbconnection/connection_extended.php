<?php
/***
*@package Joomla.Site
*@subpackage mod_any_package
*@license GNU/GPL, see LICENSE.php
@copyright Copyright (C) 2005 - 2018, Open Source Matters, Inc. All rights reserved.
***/
// no direct access
defined('_JEXEC') or die;
// defining connection variables
define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'root');
define('DB_PASSWORD', '');
define(DB_NAME', 'JoomlaResearchTestSitedb');

$con = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD,DB_NAME);
if($con == false){
	die('Error, could not connect.' . mysqli_connect_error());
}
?>