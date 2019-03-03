<?php
/**
 * Author: jakub Dolejsi
 * Date: 3.3.19
 * Time: 1:18
 */

/** Generovani testu do HTML */
function generate_test($name, $success, $exit_code){
    if($success!="true")
        echo "<tr style=\"text-align: center;\"><td>$name</td><td style='background-color: #c8110c'>$success</td><td>$exit_code</td></tr>";
    else
        echo "<tr style=\"text-align: center;\"><td>$name</td><td style='background-color: #3fc82c'>$success</td><td>$exit_code</td></tr>";}

/** Print --help */
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
/** Vygenerovani podkladu HTML */
function generate_meta(){
    echo "<!DOCTYPE HTML>";
    echo "<html>";
    echo "<head>";
    echo "<meta charset=\"utf-8\">";
    echo "<meta name=\"viewport\" content=\"width=1920, initial-scale=1.0\">";
    echo "<title>IPP - test results</title>";
    echo "</head>";
    echo "<body style='background-color: #4f9fff'>";
}
/** Funkce na vygenerovani hlavicky HTML */
function generate_header(){
    echo "<h1 style='text-align: center; color: #eaf8f5;'>IPP - Test results</h1>";
    echo "<table style=\"width:100%;\"><tr style='background-color:#aeaeae;'><th>Filename</th><th>Success</th><th>Exit code</th></tr>\n";
}

/** Jeste uplne nefunguje, doladit kde tabulka bude */
function generate_perc($percentage){

}
