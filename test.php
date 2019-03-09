<?php
/**
 * Author: jakub Dolejsi
 * Date: 3.3.19
 * Time: 0:30
 */
include_once 'test-lib.php';

function parse_script(){
    return 0;
}
function int_script(){
    return 0;
}
function recursive(){
    return 0;
}
function int_only(){
    return 0;
}

global $output, $parseExitCode,$diff_out,$ec,$success;
$recurs_flag = false;
$dir_flag = false;
$parse_script_flag = false;
$int_script_flag = false;
$parse_only_flag = false;
$int_only_flag = false;

$test_counter = 1;
$success = false;



generate_meta();
generate_header();
check_arg($option,$argc);
#TODO: Rekurze funguje, ale doresit, pokud je zadana jenom rekurse, bez dir
generate_output($dir_flag, $recurs_flag,$parse_script_flag, $int_script_flag,$parse_only_flag,$int_only_flag);
//recursiveScan($direc_path);


//print "\n".$folder."\n";   // Realpath

echo "</table>";

