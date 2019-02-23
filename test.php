<?php

function generate_header(){
    echo "<!DOCTYPE HTML><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=1920, initial-scale=1.0\"><title>IPP - Tests results</title></head><body>";
    echo "<font size=\"3\" color=\"#006400\"><br><h1><center>IPP project - test results</center></h1></br></font>";
    echo "<TABLE style='width: 100%;border:none;border-collapse: collapse;'>
    <tbody><tr style='background-color:#444444;color:white;border-collapse: collapse'>
    <th>number</th><th>Filename</th><th>Success</th><th>Error type</th></tr>";
}

function display_help()
{
    echo "  php7.3 test.php [--help] [--recursive] [--parse-script=] [--int-script=] [--directory=]\n";
    echo "     --help     		    - Zobrazi napovedu\n";
    echo "     --directory=path     - testy bude hledat v zadaném adresáři (chybí-li tento parametr, tak skriptprochází aktuální adresář)\n";
    echo "     --recursive          - testy bude hledat nejen v zadaném adresáři, ale i rekurzivněve všech jeho podadresářích\n";
    echo "     --parse-script=file  - soubor se skriptem v PHP 7.3 pro analýzu zdrojového kódu v IPP-code19 (chybí-li tento parametr, tak implicitní hodnotou je parse.php uložený v aktuálním adresáři)\n";
    echo "     --int-script=file    - soubor se skriptem v Python 3.6 pro interpret XML reprezentace kóduv IPPcode19 (chybí-li tento parametr, tak implicitní hodnotou je interpret.py uložený v aktuálním adresáři)\n";
    echo "     --parse-only         - bude testován pouze skript pro analýzu zdrojového kódu v IPPcode19 (tento parametr se nesmí kombinovat s parametrem--int-script)\n";
    echo "     --int-only           - bude testován pouze skript pro interpret XML reprezentace kódu v IPPcode19 (tento parametr se nesmí kombinovat s parametrem --parse-script)\n";
}

function parse_only(){

}
$longopts = array("help", "directory", "recursive", "parse-script", "int-script", "parse-only", "int-only");
$option = getopt("h", $longopts);

if($argc == 2) {
    if (array_key_exists("help", $option)) {
        display_help();
    } elseif (array_key_exists("directory", $option)) {
        echo "prohledame slozku";
    } elseif (array_key_exists("recursive", $option)) {
        echo "prohledame slozku rekursivne";
    } elseif (array_key_exists("recursive", $option)) {
        echo "prohledame slozku rekursivne";
    } elseif (array_key_exists("parse-script", $option)) {
        echo "prohledame slozku rekursivne";
    } elseif (array_key_exists("int-script", $option)) {
        echo "prohledame slozku rekursivne";
    } elseif (array_key_exists("parse-only", $option)) {
        echo "spustime parse test\n";
    } elseif (array_key_exists("int-only", $option)) {
        echo "prohledame slozku rekursivne";
    } else {
        fwrite(STDERR, "Wrong arguments!\n");
        exit(10);
    }
}
    generate_header();
