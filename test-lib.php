<?php
/**
 * Author: jakub Dolejsi
 * Date: 3.3.19
 * Time: 1:18
 */
/* argument check*/

$direc_path="";
$parser_path="";
$folder = getcwd();

function file_err(){
    fwrite(STDERR,"Invalid input file/directory");
    exit(11);
}

$longopts = array("help", "directory:", "recursive", "parse-script:", "int-script", "parse-only", "int-only");
$option = getopt("", $longopts);
function arg_err(){
    fwrite(STDERR,"Wrong arguemtns\n");
    exit(10);
}

function parse_path($option)
{
    $file = $option["parse-script"];
    $parse_path = realpath($file);
    if ($parse_path) {
        //c
        return $parse_path;
    } else
        file_err();
}

function check_arg($option,$argc)
{
    global $dir_flag, $recurs_flag, $int_script_flag, $parse_only_flag, $int_only_flag, $direc_path,$parse_script_flag;

    if ($argc != 1) {
        if (array_key_exists("help", $option)) {
            if ($argc == 2)
                display_help();
            else
                arg_err();
        }
        if (array_key_exists("directory", $option)) {
            $direc_path = $option["directory"];
            $dir_flag = true;
        }
            if (array_key_exists("recursive", $option))
                $recurs_flag = true;
            if (array_key_exists("parse-script", $option)) {
                $parse_script_flag = true;
            }
            if (array_key_exists("int-script", $option))
                $int_script_flag = true;
            if (array_key_exists("parse-only", $option))
                $parse_only_flag = true;
            if (array_key_exists("int-only", $option)) {
                $int_only_flag = true;
            }
        } else
            arg_err();
}


/** Generovani testu do HTML */
function generate_test($name,$exit_code,$exp_code,$success){
    if($success!="true")
        echo "<td>$name</td><td>$exit_code</td><td>$exp_code</td><td style='background-color: #c8110c'>$success</td></tr>";
    else
        echo "<td>$name</td><td>$exit_code</td><td>$exp_code</td><td style='background-color: #3fc82c'>$success</td></tr>";}

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
    echo "<body style='background-color: #4f9fff; text-align: center'>";
}
/** Funkce na vygenerovani hlavicky HTML */
function generate_header(){
    echo "<h1 style='text-align: center; color: #eaf8f5;'>IPP - Test results</h1>";
    echo "<table style=\"width:100%;\"><tr style='background-color:#aeaeae;'><th>Filename</th><th>Exit code</th><th>Expected exit code</th><th>Success</th></tr>\n";
}

/** Jeste uplne nefunguje, doladit kde tabulka bude */
function generate_perc($percentage){

}
function parse_only($filename)
{
    $ref_file =  explode(".",$filename); // rozdelime si nazev souboru na nazev a priponu
    $ref_file = $ref_file[0];                   // ulozime si cast nazvu testu pred priponou, napr. read_test
    global $output,$ec,$diff_out;
    $temp_file = tmpfile(); // vytvoreni temp souboru
    $path = stream_get_meta_data($temp_file)['uri']; // cesta k temp souboru

    exec("cat $filename | php7.3 parse.php", $output, $parseExitCode);
    $output = implode("\n", $output);
    fwrite($temp_file,$output);
    rewind($temp_file); // zapsani vystupu parseru do temp souboru

    exec("cat $ref_file.rc",$rc); // vypsani .rc souboru do promenne rc
    $rc = $rc[0];
    exec("java -jar /home/jakub/Plocha/IPP/xml/jexamxml.jar $ref_file.out $path diffs.xml options",$diff_out,$ec);
    if($ec == "0" && $rc == $parseExitCode){ // Pokud JExamXML vrati 0(shoda) a exit kod parseru a refercni exit kod se shoduji
        generate_test($filename,$parseExitCode,$rc,"true");
    } else
        generate_test($filename,$parseExitCode,$rc,"false");
    fclose($temp_file);
}

function directory($filename,$parser = "parse.php")
{
    $ref_file =  explode(".",$filename); // rozdelime si nazev souboru na nazev a priponu
    $ref_file = $ref_file[0];                   // ulozime si cast nazvu testu pred priponou, napr. read_test
    global $output,$ec,$diff_out;
    $temp_file = tmpfile(); // vytvoreni temp souboru
    $path = stream_get_meta_data($temp_file)['uri']; // cesta k temp souboru

    exec("cat $filename | php7.3 $parser", $output, $parseExitCode);
    $output = implode("\n", $output);
    fwrite($temp_file,$output);
    rewind($temp_file); // zapsani vystupu parseru do temp souboru

    exec("cat $ref_file.rc",$rc); // vypsani .rc souboru do promenne rc
    $rc = $rc[0];
    exec("java -jar /home/jakub/Plocha/IPP/xml/jexamxml.jar $ref_file.out $path diffs.xml options",$diff_out,$ec);
    if($ec == "0" && $rc == $parseExitCode){ // Pokud JExamXML vrati 0(shoda) a exit kod parseru a refercni exit kod se shoduji
        generate_test($filename,$parseExitCode,$rc,"true");
    } else
        generate_test($filename,$parseExitCode,$rc,"false");
    fclose($temp_file);
}

function search_dir($direc_path,$parser = "parse.php"){
    $test_files = glob("$direc_path/*.src");
    foreach ($test_files as $filename){
        directory($filename,$parser);
    }
}

function recursiveScan($dir){
    if (!is_dir($dir))
        file_err();
    $it = new RecursiveDirectoryIterator($dir);
        $allowed = array("src");
        foreach (new RecursiveIteratorIterator($it) as $file) {
            if (in_array(substr($file, strrpos($file, '.') + 1), $allowed)) {
                directory($file);
            }
        }
}

function is_valid_parser($in){
    $in = explode(".",$in);
    if($in[1]!=="php")
        file_err();
}

function generate_output($dir_flag, $recurse_flag,$parse_script_flag, $int_script_flag,$parse_only_flag,$int_only_flag){
    global $option, $direc_path,$folder;

    if ($parse_script_flag && $int_script_flag && !$parse_only_flag && !$int_only_flag) {
        //prvni case
        // nastavime jak interpret,tak parser
        if ($dir_flag && $recurse_flag) {
            // budeme prohledavat zadany adresar rekuzrivne
        } elseif ($dir_flag && !$recurse_flag) {
            // budeme prohledavat zadany adresar normalne
        } elseif (!$dir_flag && $recurse_flag) {
            //budeme prohledavat aktualni adresar rekurzivne
        }
    } elseif ($parse_script_flag && $parse_only_flag && !$int_script_flag && !$int_only_flag) {
        // druhy case
        $parser_path=parse_path($option); // do promenne parser_path ulozi cestu k validnimu parseru, tj ktery existuje
        if(!is_file($parser_path))
            file_err();
        is_valid_parser($parser_path);
        if ($dir_flag && $recurse_flag) {
            // budeme prohledavat zadany adresar rekuzrivne
            search_dir($direc_path);
            recursiveScan($direc_path);
        } elseif ($dir_flag && !$recurse_flag) {
            search_dir($direc_path);
            // budeme prohledavat zadany adresar normalne
        } elseif (!$dir_flag && $recurse_flag) {
            search_dir($folder);
            recursiveScan($folder);
            //budeme prohledavat aktualni adresar rekurzivne
        }
    } elseif ($int_script_flag && $int_only_flag && !$parse_script_flag && !$parse_only_flag) {
        //treti case
        // nastavime interpret a budeme testovat pouze interpret
        if ($dir_flag && $recurse_flag) {
            // budeme prohledavat zadany adresar rekuzrivne
        } elseif ($dir_flag && !$recurse_flag) {
            // budeme prohledavat zadany adresar normalne
        } elseif (!$dir_flag && $recurse_flag) {
            //budeme prohledavat aktualni adresar rekurzivne
        }
    } elseif ($parse_script_flag && !$parse_only_flag && !$int_script_flag && !$int_only_flag) {
        // 4 cast
        // nastavime pouze parser
        if ($dir_flag && $recurse_flag) {
            // budeme prohledavat zadany adresar rekuzrivne
        } elseif ($dir_flag && !$recurse_flag) {
            // budeme prohledavat zadany adresar normalne
        } elseif (!$dir_flag && $recurse_flag) {
            //budeme prohledavat aktualni adresar rekurzivne
        }
    }elseif (!$parse_script_flag && !$parse_only_flag && $int_script_flag && !$int_only_flag) {
        // 4 cast
        // nastavime pouze interpret
        if ($dir_flag && $recurse_flag) {
            // budeme prohledavat zadany adresar rekuzrivne
        } elseif ($dir_flag && !$recurse_flag) {
            // budeme prohledavat zadany adresar normalne
        } elseif (!$dir_flag && $recurse_flag) {
            //budeme prohledavat aktualni adresar rekurzivne
        }
    }elseif (!$parse_script_flag && $parse_only_flag && !$int_script_flag && !$int_only_flag) {
        // 5 cast
        // budeme testovat pouze parser
        if ($dir_flag && $recurse_flag) {
            // budeme prohledavat zadany adresar rekuzrivne
        } elseif ($dir_flag && !$recurse_flag) {
            // budeme prohledavat zadany adresar normalne
        } elseif (!$dir_flag && $recurse_flag) {
            //budeme prohledavat aktualni adresar rekurzivne
        }
    }elseif (!$parse_script_flag && !$parse_only_flag && !$int_script_flag && $int_only_flag) {
        // 6 cast
        // budeme testovat pouze interpret
        if ($dir_flag && $recurse_flag) {
            // budeme prohledavat zadany adresar rekuzrivne
        } elseif ($dir_flag && !$recurse_flag) {
            // budeme prohledavat zadany adresar normalne
        } elseif (!$dir_flag && $recurse_flag) {
            //budeme prohledavat aktualni adresar rekurzivne
        }
    }elseif ($dir_flag && $recurse_flag && !$parse_script_flag && !$parse_only_flag && !$int_script_flag && !$int_only_flag) {
        // zdan dir a recurse
        //search_dir($direc_path);
        recursiveScan($direc_path);
    }elseif($dir_flag && !$recurse_flag && !$parse_script_flag && !$parse_only_flag && !$int_script_flag && !$int_only_flag) {
        search_dir($direc_path);
        //zdan pouze dir
    }elseif (!$dir_flag && $recurse_flag && !$parse_script_flag && !$parse_only_flag && !$int_script_flag && !$int_only_flag) {
        // zadan pouze recurse
        //search_dir($folder);
        recursiveScan($folder);

    }else
        arg_err();
}