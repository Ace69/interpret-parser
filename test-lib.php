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

function fileError(){
    fwrite(STDERR,"Invalid input file/directory\n");
    exit(11);
}

$longopts = array("help", "directory:", "recursive", "parse-script:", "int-script:", "parse-only", "int-only");
$option = getopt("", $longopts);
function argError(){
    fwrite(STDERR,"Wrong arguemtns\n");
    exit(10);
}

function parsePath($option)
{
    $file = $option["parse-script"];
    $parse_path = realpath($file);
    if ($parse_path)
        return $parse_path;
     else
        fileError();
}

function intPath($option){
    $file = $option["int-script"];
    $int_path = realpath($file);
    if($int_path)
        return $int_path;
    else
        fileError();
}

function argCheck($option, $argc)
{
    global $dir_flag, $recurs_flag, $int_script_flag, $parse_only_flag, $int_only_flag, $direc_path,$parse_script_flag;

    if ($argc != 1) {
        if (array_key_exists("help", $option)) {
            if ($argc == 2)
                displayHelp();
            else
                argError();
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
            argError();
}


/** Generovani testu do HTML */
function generateTest($name, $exit_code, $exp_code, $success){
    if($success!="true")
        echo "<td style='width: 25%'>$name</td><td style='width: 25%'>$exit_code</td><td style='width: 25%;'>$exp_code</td><td style='background-color: #c8110c; width: 25%'>$success</td></tr>";
    else
        echo "<td>$name</td><td>$exit_code</td><td>$exp_code</td><td style='background-color: #3fc82c'>$success</td></tr>";}

/** Print --help */
function displayHelp(){
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
function generateMeta(){
    echo "<!DOCTYPE html>";
    echo "<html>";
    echo "<head>";
    echo "<meta charset=\"utf-8\">";
    echo "<meta name=\"viewport\" content=\"width=1920, initial-scale=1.0\">";
    echo "<title>IPP - test results</title>";
    echo "</head>";
    echo "<body style='background-color: #4f9fff; text-align: center'>";
}
/** Funkce na vygenerovani hlavicky HTML */
function generateHeader(){
    echo "<h1 style='text-align: center; color: #eaf8f5;'>IPP - Test results</h1>";
    echo "<table border='1'; style=\"width:100%;\"><tr style='background-color:#aeaeae; text-align: justify-all'><th>Filename</th><th>Exit code</th><th>Expected exit code</th><th>Success</th></tr>\n";
}

/** Jeste uplne nefunguje, doladit kde tabulka bude */
function generatePerc($percentage){

}

function parseDirectory($filename, $parser = "parse.php")
{
    $ref_file =  explode(".",$filename); // rozdelime si nazev souboru na nazev a priponu
    $ref_file = $ref_file[0];                   // ulozime si cast nazvu testu pred priponou, napr. read_test
    //global $output,$ec,$diff_out;
    $temp_file = tmpfile(); // vytvoreni temp souboru
    $path = stream_get_meta_data($temp_file)['uri']; // cesta k temp souboru

    exec("cat $filename | php7.3 $parser", $output, $parseExitCode);
    $output = implode("\n", $output);
    fwrite($temp_file,$output);
    rewind($temp_file); // zapsani vystupu parseru do temp souboru

    if(is_file("$ref_file.rc"))
        exec("cat $ref_file.rc",$rc); // vypsani .rc souboru do promenne rc
    else {
        file_put_contents("$ref_file.rc", "0");
        $rc = array("0");
    }
    $rc = $rc[0];
    if(!is_file("$ref_file.out"))
        touch("$ref_file.out");
    exec("java -jar /home/jakub/Plocha/IPP/xml/jexamxml.jar $ref_file.out $path diffs.xml options",$diff_out,$ec);
    if($ec == "0" && $rc == $parseExitCode){ // Pokud JExamXML vrati 0(shoda) a exit kod parseru a refercni exit kod se shoduji
        generateTest($filename,$parseExitCode,$rc,"true");
    } else
        generateTest($filename,$parseExitCode,$rc,"false");
    if(is_file("$ref_file.out.log"))
        unlink("$ref_file.out.log");
    unlink($path);
}

function intDirectory($filename, $interpret = "interpret.py"){
    $ref_file =  explode(".",$filename); // rozdelime si nazev souboru na nazev a priponu
    $ref_file = $ref_file[0];                   // ulozime si cast nazvu testu pred priponou, napr. read_test
   // global $output,$ec,$diff_out;
    $temp_file = tmpfile(); // vytvoreni temp souboru
    $path = stream_get_meta_data($temp_file)['uri']; // cesta k temp souboru

    exec("cat $filename | python3.6 $interpret", $output, $intExitCode);
    $output = implode("\n", $output);
    fwrite($temp_file,$output);
    rewind($temp_file); // zapsani vystupu interpretu do temp souboru

    if(is_file("$ref_file.rc"))
        exec("cat $ref_file.rc",$rc); // vypsani .rc souboru do promenne rc
    else {
        file_put_contents("$ref_file.rc", "0");
        $rc = array("0");
    }
    $rc = $rc[0];
    if(!is_file("$ref_file.out"))
        touch("$ref_file.out");
    exec("diff $ref_file.out $path ",$diff_out,$ec);
    if($ec == "0" && $rc == $intExitCode){ // Pokud Diff vrati 0(shoda) a exit kod parseru a refercni exit kod se shoduji
        generateTest($filename,$intExitCode,$rc,"true");
    } else
        generateTest($filename,$intExitCode,$rc,"false");
    unlink($path);
}

function bothDirectory($filename,$parser,$int)
{
    $intExitCode = 0;
    if ($parser == null)
        $parser = "parse.php";
    if ($int == null)
        $int = "interpret.py";


    $ref_file = explode(".", $filename); // rozdelime si nazev souboru na nazev a priponu
    $ref_file = $ref_file[0];                   // ulozime si cast nazvu testu pred priponou, napr. read_test
    $temp_file = tmpfile(); // vytvoreni temp souboru
    $path = stream_get_meta_data($temp_file)['uri']; // cesta k temp souboru
    checkIfExists($ref_file); // pripadne dogenerovani chybejicich souboru

    exec("cat $filename | php7.3 $parser", $parseOut, $parseExitCode);
    exec("cat $ref_file.rc", $rc); // vypsani .rc souboru do promenne rc

    $parseOut = implode("\n", $parseOut);
    fwrite($temp_file, $parseOut);
    rewind($temp_file); // zapsani vystupu interpretu do temp souboru
    if ($rc[0] == $parseExitCode) {
        // budeme pokracovat v interpretaci
        exec("python3.6 $int --source=$path", $intOut, $intExitCode);
        exec("cat $ref_file.rc", $rc);
        exec("cat $ref_file.out", $out);
        if ($rc[1] == $intExitCode && $intOut == $out)
            generateTest("$ref_file", $intExitCode, $rc[1], "true");
        else
            generateTest("$filename", $intExitCode, $rc[1], "false");
    } else
        generateTest("$filename", $intExitCode, $rc[1], "false");
    unlink($path);
}

function checkIfExists($in){
    if(!is_file("$in.in"))
        touch("$in.in");
    if(!is_file("$in.out"))
        touch("$in.out");
    if(!is_file("in.rc"))
        file_put_contents("$in.rc","0");
}

function bothSearchDir($direc_path,$parser,$int){
    $test_files = glob("$direc_path/*.src");
    foreach ($test_files as $filename){
        bothDirectory($filename,$parser,$int);
    }
}
function parseSearchDir($direc_path, $parser = "parse.php"){
    $test_files = glob("$direc_path/*.src");
    foreach ($test_files as $filename){
        parseDirectory($filename,$parser);
    }
}

function intSearchDir($direc_path, $int = "interpret.py"){
    $test_files = glob("$direc_path/*.src");
    foreach ($test_files as $filename){
        intDirectory($filename,$int);
    }
}

function bothRecursive($dir, $parse, $int){
    if (!is_dir($dir))
        fileError();
    $it = new RecursiveDirectoryIterator($dir);
    $allowed = array("src");
    foreach (new RecursiveIteratorIterator($it) as $file) {
        if (in_array(substr($file, strrpos($file, '.') + 1), $allowed)) {
            bothDirectory($file,$parse,$int);
        }
    }
}

function intRecursive($dir, $int = "interpret.py") {
    if (!is_dir($dir))
        fileError();
    $it = new RecursiveDirectoryIterator($dir);
    $allowed = array("src");
    foreach (new RecursiveIteratorIterator($it) as $file) {
        if (in_array(substr($file, strrpos($file, '.') + 1), $allowed)) {
            parseDirectory($file, $int);
        }
    }
}

function parseRecursive($dir, $parser = "parse.php"){
    if (!is_dir($dir))
        fileError();
    $it = new RecursiveDirectoryIterator($dir);
        $allowed = array("src");
        foreach (new RecursiveIteratorIterator($it) as $file) {
            if (in_array(substr($file, strrpos($file, '.') + 1), $allowed)) {
                parseDirectory($file,$parser);
            }
        }
}

function isValidParser($in){
    $in = explode(".",$in);
    if($in[1]!=="php")
        fileError();
}

function isValidInt($in){
    $in = explode(".",$in);
    if($in[1]!=="py")
        fileError();
}

function generateOutput($dir_flag, $recurse_flag, $parse_script_flag, $int_script_flag, $parse_only_flag, $int_only_flag){
    global $option, $direc_path,$folder;

    if ($parse_script_flag && $int_script_flag && !$parse_only_flag && !$int_only_flag) {
        $parser_path=parsePath($option);
        if(!is_file($parser_path))
            fileError();
        isValidParser($parser_path);

        $int_path = intPath($option);
        if(!is_file($int_path))
            fileError();
        isValidInt($int_path);
        if ($dir_flag && $recurse_flag) {
            bothRecursive($direc_path,$parser_path,$int_path);
        } elseif ($dir_flag && !$recurse_flag) {
            bothSearchDir($direc_path,$parser_path,$int_path);
        } elseif (!$dir_flag && $recurse_flag) {
            bothRecursive($folder,$parser_path,$int_path);

        }
    } elseif ($parse_script_flag && $parse_only_flag && !$int_script_flag && !$int_only_flag) {
        $parser_path=parsePath($option); // do promenne parser_path ulozi cestu k validnimu parseru, tj ktery existuje
        if(!is_file($parser_path))
            fileError();
        isValidParser($parser_path);
        if ($dir_flag && $recurse_flag) {
            parseRecursive($direc_path,$parser_path);
        } elseif ($dir_flag && !$recurse_flag) {
            parseSearchDir($direc_path,$parser_path);
        } elseif (!$dir_flag && $recurse_flag) {
            parseRecursive($folder,$parser_path);
        }
    } elseif ($int_script_flag && $int_only_flag && !$parse_script_flag && !$parse_only_flag) {
        $int_path = intPath($option);
        if(!is_file($int_path))
            fileError();
        isValidInt($int_path);
        if ($dir_flag && $recurse_flag) {
            intSearchDir($direc_path);
            intRecursive($direc_path,$int_path);
        } elseif ($dir_flag && !$recurse_flag) {
            intSearchDir($direc_path,$int_path);
        } elseif (!$dir_flag && $recurse_flag) {
            intRecursive($folder,$int_path);
        }
    } elseif ($parse_script_flag && !$parse_only_flag && !$int_script_flag && !$int_only_flag) {
        $parser_path=parsePath($option); // do promenne parser_path ulozi cestu k validnimu parseru, tj ktery existuje
        if(!is_file($parser_path))
            fileError();
        isValidParser($parser_path);
        if ($dir_flag && $recurse_flag) {
            bothRecursive($direc_path,$parser_path,null);
        } elseif ($dir_flag && !$recurse_flag) {
            bothSearchDir($direc_path,$parser_path,null);
        } elseif (!$dir_flag && $recurse_flag) {
            bothRecursive($folder,$parser_path,null);
        }
    }elseif (!$parse_script_flag && !$parse_only_flag && $int_script_flag && !$int_only_flag) {
        $int_path = intPath($option);
        if(!is_file($int_path))
            fileError();
        isValidInt($int_path);
        if ($dir_flag && $recurse_flag) {
            bothRecursive($direc_path,null,$int_path);
        } elseif ($dir_flag && !$recurse_flag) {
            bothSearchDir($direc_path,null,$int_path);
        } elseif (!$dir_flag && $recurse_flag) {
            bothRecursive($folder,null,$int_path);
        }
    }elseif (!$parse_script_flag && $parse_only_flag && !$int_script_flag && !$int_only_flag) {
        if ($dir_flag && $recurse_flag) {
            parseSearchDir($direc_path);
            parseRecursive($direc_path);
        } elseif ($dir_flag && !$recurse_flag) {
            parseSearchDir($direc_path);
        } elseif (!$dir_flag && $recurse_flag) {
            parseRecursive($folder);
        }
    }elseif (!$parse_script_flag && !$parse_only_flag && !$int_script_flag && $int_only_flag) {
        if ($dir_flag && $recurse_flag) {
            intRecursive($direc_path,null);
        } elseif ($dir_flag && !$recurse_flag) {
            intSearchDir($direc_path,null);
        } elseif (!$dir_flag && $recurse_flag) {
            intRecursive($folder,null);
        }
    }elseif ($dir_flag && $recurse_flag && !$parse_script_flag && !$parse_only_flag && !$int_script_flag && !$int_only_flag) {
        // zdan dir a recurse
        bothRecursive($direc_path,null,null);

    }elseif($dir_flag && !$recurse_flag && !$parse_script_flag && !$parse_only_flag && !$int_script_flag && !$int_only_flag) {
        //zdan pouze dir
        bothSearchDir($direc_path,null,null);
    }elseif (!$dir_flag && $recurse_flag && !$parse_script_flag && !$parse_only_flag && !$int_script_flag && !$int_only_flag) {
        // zadan pouze recurse
        bothRecursive($folder,null,null);

    }else
        argError();
}