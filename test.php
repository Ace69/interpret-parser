<?php

function generate_meta(){
    echo "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8;\"><title> IPP - Test Results </title> <style> td,th { border-collapse:collapse;text-align:center}</style></head><body><h1 style='color:#4e2aff;text-align: center'>IPP test results</h1><br>\n";
}

function generate_header(){
    echo "<table style=\"width:100%;\"><tr style='background-color:#aeaeae;'><th>Filename</th><th>Success</th><th>Exit code</th></tr>\n";
}

function generate_test($name, $success, $exit_code){
    echo "<tr style=\"text-align: center;\"><td>$name</td><td>$success</td><td>$exit_code</td></tr></table>";
}

function generate_perc($percentage){
    if($percentage == "100")
        echo "><tr><th>Percentage</th></tr><tr><td style='color: #086418'>$percentage</td>></tr></table>";
    else
        echo "<table style=\"width:80%\"><tr><th>Percentage</th></tr><tr><td style='color: #ae1923'>$percentage</td>></tr></table>";
}

function display_help(){
    echo "  php7.3 test.php [--help] [--recursive] [--parse-script=] [--int-script=] [--directory=]\n";
    echo "     --help     		    - Zobrazi napovedu\n";
    echo "     --directory=path     - testy bude hledat v zadaném adresáři (chybí-li tento parametr, tak skriptprochází aktuální adresář)\n";
    echo "     --recursive          - testy bude hledat nejen v zadaném adresáři, ale i rekurzivněve všech jeho podadresářích\n";
    echo "     --parse-script=file  - soubor se skriptem v PHP 7.3 pro analýzu zdrojového kódu v IPP-code19 (chybí-li tento parametr, tak implicitní hodnotou je parse.php uložený v aktuálním adresáři)\n";
    echo "     --int-script=file    - soubor se skriptem v Python 3.6 pro interpret XML reprezentace kóduv IPPcode19 (chybí-li tento parametr, tak implicitní hodnotou je interpret.py uložený v aktuálním adresáři)\n";
    echo "     --parse-only         - bude testován pouze skript pro analýzu zdrojového kódu v IPPcode19 (tento parametr se nesmí kombinovat s parametrem--int-script)\n";
    echo "     --int-only           - bude testován pouze skript pro interpret XML reprezentace kódu v IPPcode19 (tento parametr se nesmí kombinovat s parametrem --parse-script)\n";
}

function directory(){
    echo "prohledame slozku";
}

function parse_only(){

    exec('php7.3 parse.php < test.src', $output, $exitCode);
    if ($exitCode != 0) {
        echo "Error\n";
        exit($exitCode);
    } else
        file_put_contents('test.out', $output);

}

global $output, $exitCode;
$test_counter = 1;
$success = false;
$longopts = array("help", "directory", "recursive", "parse-script", "int-script", "parse-only", "int-only");
$option = getopt("h", $longopts);

if ($argc == 2) {
    if (array_key_exists("help", $option)) {
        display_help();
    } elseif (array_key_exists("directory", $option)) {
        directory();
    } elseif (array_key_exists("recursive", $option)) {
        echo "prohledame slozku rekursivne";
    } elseif (array_key_exists("parse-script", $option)) {
        echo "nastavime parser pro  IPPcode19";
    } elseif (array_key_exists("int-script", $option)) {
        echo "nastavime interpret pro IPPcode19 ";
    } elseif (array_key_exists("parse-only", $option)) {
        parse_only();
    } elseif (array_key_exists("int-only", $option)) {
        echo "bude testovan pouze interpret XML reprezentace kodu IPPcode19";
    } else {
        fwrite(STDERR, "Wrong arguments!\n");
        exit(10);
    }
}
generate_meta();
generate_test("test.src", "true", "0");
generate_perc("100");
parse_only();

