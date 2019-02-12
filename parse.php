<?php

/**
 * Created by Jakub Dolejsi
 * Date: 11.2.19
 */
/* ********************* Arguments parsing *************************** */
$longopts = array("help");
$option = getopt("", $longopts);
if($argc == 2){
    if(array_key_exists("help", $option)){
        echo("--Skript typu filtr načte ze standartního vstupu zdrojový kód IPPcode19, zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standartní výstup XML reprezentaci programu.\n");
    }else{
        fwrite(STDERR, "Wrong input arguments!\n");
        exit(10);
    }
}
/* ********************* Check header *************************** */
$line = fgets(STDIN);
$line = strtoupper(trim($line));
if($line != ".IPPCODE19"){
    fwrite(STDERR, "Wrong header!\n");
    exit(21);
}
/* ********************* Reading from unput *************************** */
while($a=fgets(STDIN)){
    if(strpos($a, "#") != FALSE){
         $stringos = preg_replace('/./', '', $a);
        #print("komentar je: $a");
        echo($stringos);
    }
    echo $a;
}