<?php
    // $db = JFactory::getDbo();
    // $query = $db->getQuery(true);
    // --these variables must be included as the user inputs
    define('DB_SERVER','localhost');
    define('DB_USERNAME','root');
    define('DB_PASSWORD','');
    define('DB_NAME','JoomlaResearchTestSitedb');
    // --

    $db=mysqli_connect(DB_SERVER,DB_USERNAME,DB_PASSWORD,DB_NAME);
    if($db===false){
        die("Error, could not connect " . mysqli_connect_error());
    }
?>
