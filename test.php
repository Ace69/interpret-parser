<?php
/**
 * Author: jakub Dolejsi
 * Date: 3.3.19
 * Time: 0:30
 */

require_once 'test-lib.php';

//global $output, $parseExitCode,$diff_out,$ec,$success;
$recurs_flag = false;
$dir_flag = false;
$parse_script_flag = false;
$int_script_flag = false;
$parse_only_flag = false;
$int_only_flag = false;

$test_counter = 1;
$success = false;



generateMeta();
generateHeader();
argCheck($option,$argc);
#TODO: Rekurze funguje, ale doresit, pokud je zadana jenom rekurse bez dir
# Vyresit rekurzi pro arguemnt "both"
//bothDirectory($folder,"parsik.php","intik.py");


generateOutput($dir_flag, $recurs_flag,$parse_script_flag, $int_script_flag,$parse_only_flag,$int_only_flag);
//recursiveScan($direc_path);


//print "\n".$folder."\n";   // Realpath

echo "</table>";

