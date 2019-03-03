<?php
/**
 * Author: jakub Dolejsi
 * Date: 3.3.19
 * Time: 0:30
 */
include_once 'test-lib.php';



global $output, $exitCode,$diff_out,$ec;
$parse_flag = false;
$parse_script_flag = false;
$test_counter = 1;
$success = false;
$longopts = array("help", "directory", "recursive", "parse-script:", "int-script", "parse-only", "int-only");
$option = getopt("", $longopts);


function directory(){
    echo "prohledame slozku";
}

function parse_only(){
    exec('php7.3 parse.php < test.src > test.out', $tmp_parse, $exitCode);
    $diff_out = shell_exec("diff test.out ref.out"); # Zde bude namisto diffu JeXML porovnani
    //echo "$exitCode";
    file_put_contents("test.rc", "$exitCode");
    return $exitCode;
}
function parse_script($parser){
    exec("php7.3 $parser < test.src > test.out", $tmp_parse, $exitCode);
    $diff_out = shell_exec("diff test.out ref.out"); # Zde bude namisto diffu JeXML porovnani
    file_put_contents("test.rc", "$exitCode");
    return $exitCode;
}

if ($argc == 2) {
    if (array_key_exists("help", $option)) {
        display_help();
    } elseif (array_key_exists("directory", $option)) {
        directory();
    } elseif (array_key_exists("recursive", $option)) {
        echo "prohledame slozku rekursivne";
    } elseif (array_key_exists("parse-script", $option)) {
        $file = $option["parse-script"];
        $parse_path = realpath($file);
        if($file){
            parse_script($parse_path);
            $parse_script_flag=true;
        }
    } elseif (array_key_exists("int-script", $option)) {
        echo "nastavime interpret pro IPPcode19 ";
    } elseif (array_key_exists("parse-only", $option)) {
        $ec = parse_only();
        if($ec==0){
         $parse_flag = true;
        }
    } elseif (array_key_exists("int-only", $option)) {
        echo "bude testovan pouze interpret XML reprezentace kodu IPPcode19";
    } else {
        fwrite(STDERR, "Wrong arguments!\n");
        exit(10);
    }
}
generate_meta();
generate_header();
if($parse_flag==true)
    generate_test("test.src", "true", $ec);
if($parse_script_flag==true)
    generate_test("test.src", "true", $ec);
generate_perc("50");
parse_only();
echo "</table>";

