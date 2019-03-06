<?php

/**
 * Created by Jakub Dolejsi
 * Date: 11.2.19
 */

function wrong_code(){
    fwrite(STDERR, "Wrong instruction!\n");
    exit(22);
}
function lex_err(){
    fwrite(STDERR, "Lexical/syntax error!\n");
    exit(23);
}
function arg_err(){
    fwrite(STDERR, "Wrong arguments!\n");
    exit(10);
}

function remove_eol($str){
    return trim(preg_replace('/\s\s+/', ' ', $str));
}

function check_arg($in){
    if (strncmp($in, "GF@", 3) === 0 || strncmp($in, "LF@", 3) === 0 || strncmp($in, "TF@", 3) === 0) { # variable
        check_var($in);
        return 0;
    }
    elseif(strncmp($in, "int@", 4) ===0 || strncmp($in, "bool@", 5) === 0|| strncmp($in, "string@", 7) === 0|| strncmp($in, "nil@", 4) === 0) # const
        return 1;
    else
        return -1;
}

function check_type($in){
    if (strncmp($in, "int@", 4) ===0 || strncmp($in, "bool@", 5) === 0|| strncmp($in, "string@", 7) === 0)
        return 0;
    else
        return -1;
}

function correct_const($in){
    $in = strstr($in, '@');
    $in = str_replace('@', '', $in);
    return $in;
}

function check_if_same($in, $in2){
    if((strncmp($in, "int@", 3)===0 && strncmp($in2, "int@", 3)===0) || (strncmp($in, "bool@", 5)===0 && strncmp($in2, "bool@", 5)===0) || (strncmp($in, "string@", 7)===0 && strncmp($in2, "string@", 7)===0))
        return 0;
    else
        return -1;
}

function generate_no_arg($ins, $instr_counter){
    global $createframe ;
    global $domtree;
    global $program;
    $createframe = $domtree->createElement("instruction");
    $createframe->setAttribute("order","$instr_counter");
    $createframe->setAttribute("opcode", "$ins");
    $program->appendChild($createframe);
}

function generate_one_arg_var($ins, $instr_counter, $input_array){
    global $pops;
    global $domtree;
    global $program;
    $pops = $domtree->createElement("instruction");
    $pops->setAttribute("order","$instr_counter");
    $pops->setAttribute("opcode", "$ins");
    $program->appendChild($pops);

    $input_array = corr_xml_string($input_array);
    $pops_arg1 = $domtree->createElement("arg1", "$input_array");
    $pops_arg1->setAttribute("type", "var");
    $pops->appendChild($pops_arg1);
}

function generate_one_arg_label($ins, $instr_counter, $input_array){
    global $call;
    global $domtree;
    global $program;
    $call = $domtree->createElement("instruction");
    $call->setAttribute("order","$instr_counter");
    $call->setAttribute("opcode", "$ins");
    $program->appendChild($call);

    $input_array = corr_xml_string($input_array);
    $call_arg1 = $domtree->createElement("arg1", "$input_array");
    $call_arg1->setAttribute("type", "label");
    $call->appendChild($call_arg1);
}

function generate_one_arg_symb($ins, $instr_counter, $input_array){
    global $pushs;
    global $domtree;
    global $program;
    $pushs = $domtree->createElement("instruction");
    $pushs->setAttribute("order","$instr_counter");
    $pushs->setAttribute("opcode", "$ins");
    $program->appendChild($pushs);

    if(check_arg($input_array)==0){

        $input_array = corr_xml_string($input_array);
        $pushs_arg1 = $domtree->createElement("arg1", "$input_array");
        $pushs_arg1->setAttribute("type", "var");
    } elseif (check_arg($input_array)==1){
        $type = get_type($input_array);
        check_string_escape($input_array,$type);
        check_bool($input_array,$type);
        check_nil($input_array,$type);
        $input_array = corr_xml_string(correct_const($input_array));
        $pushs_arg1 = $domtree->createElement("arg1", "$input_array");
        $pushs_arg1->setAttribute("type", $type);
    }else
        lex_err();
    $pushs->appendChild($pushs_arg1);
}

function generate_two_arg_symvar($ins, $instr_counter, $input_array, $input_array2){
    global $move;
    global $domtree;
    global $program;
    $move = $domtree->createElement("instruction");
    $move->setAttribute("order","$instr_counter");
    $move->setAttribute("opcode", "$ins");
    $program->appendChild($move);

    $input_array = corr_xml_string($input_array);
    $move_arg1 = $domtree->createElement("arg1", "$input_array");
    $move_arg1->setAttribute("type", "var");
    $move->appendChild($move_arg1);


    if(check_arg($input_array)==0){
        if(check_arg($input_array2)==0) {
            $input_array2 = corr_xml_string($input_array2);
            $move_arg2 = $domtree->createElement("arg2", "$input_array2");
            $move_arg2->setAttribute("type", "var");
        } elseif(check_arg($input_array2)==1) {
            $type = get_type($input_array2);
            check_string_escape($input_array2,$type);
            check_bool($input_array2,$type);
            check_nil($input_array2,$type);
            $input_array2 = corr_xml_string(correct_const($input_array2));
            $move_arg2 = $domtree->createElement("arg2", "$input_array2");
            $move_arg2->setAttribute("type", $type);
        } else
            lex_err();
    } else
        lex_err();
    $move->appendChild($move_arg2);
}

function two_arg_read($ins, $instr_counter, $input_array, $input_array2){
    global $read;
    global $domtree;
    global $program;
    $read = $domtree->createElement("instruction");
    $read->setAttribute("order","$instr_counter");
    $read->setAttribute("opcode", "$ins");
    $program->appendChild($read);

    $input_array = corr_xml_string($input_array);
    $read_arg1 = $domtree->createElement("arg1", "$input_array");
    $read_arg1->setAttribute("type", "var");

    $read_arg2 = $domtree->createElement("arg2", "$input_array2");
    $read_arg2->setAttribute("type", "type");

    $read->appendChild($read_arg1);
    $read->appendChild($read_arg2);
}


function generate_three_arg($ins, $instr_counter, $input_array, $input_array2,$input_array3){
    global $str2int;
    global $domtree;
    global $program;
    $str2int = $domtree->createElement("instruction");
    $str2int->setAttribute("order","$instr_counter");
    $str2int->setAttribute("opcode", "$ins");
    $program->appendChild($str2int);

    $input_array = corr_xml_string($input_array);
    $str2int_arg1 = $domtree->createElement("arg1", "$input_array");
    $str2int_arg1->setAttribute("type", "var");
    if(check_arg($input_array2)==0 && check_arg($input_array3)==0){
        $input_array2 = corr_xml_string($input_array2);
        $str2int_arg2 = $domtree->createElement("arg2", "$input_array2");
        $str2int_arg2->setAttribute("type", "var");

        $input_array3 = corr_xml_string($input_array3);
        $str2int_arg3 = $domtree->createElement("arg3", "$input_array3");
        $str2int_arg3->setAttribute("type", "var");

    } elseif (check_arg($input_array2)==0 && check_arg($input_array3)==1){
        $str2int_arg2 = $domtree->createElement("arg2", "$input_array2");
        $str2int_arg2->setAttribute("type", "var");

        $type = get_type($input_array3);
        check_string_escape($input_array3,$type);
        check_bool($input_array3,$type);
        check_nil($input_array3,$type);
        $input_array3 = corr_xml_string(correct_const($input_array3));
        $str2int_arg3 = $domtree->createElement("arg3", "$input_array3");
        $str2int_arg3->setAttribute("type", $type);
    } elseif (check_arg($input_array2)==1 && check_arg($input_array3)==0){

        $type=get_type($input_array2);
        check_string_escape($input_array2,$type);
        check_bool($input_array2,$type);
        check_nil($input_array2,$type);
        $input_array2 = corr_xml_string(correct_const($input_array2));
        $str2int_arg2 = $domtree->createElement("arg2", "$input_array2");
        $str2int_arg2->setAttribute("type", $type);


        $input_array3 = corr_xml_string($input_array3);
        $str2int_arg3 = $domtree->createElement("arg3", "$input_array3");
        $str2int_arg3->setAttribute("type", "var");
    }elseif(check_arg($input_array2)==1 && check_arg($input_array3)==1){
        $type = get_type($input_array2);
        check_string_escape($input_array2,$type);
        check_bool($input_array2,$type);
        check_nil($input_array2,$type);
        $input_array2 = corr_xml_string(correct_const($input_array2));
        $str2int_arg2 = $domtree->createElement("arg2", "$input_array2");
        $str2int_arg2->setAttribute("type", $type);

        $type2=get_type($input_array3);
        check_string_escape($input_array3,$type2);
        check_bool($input_array3,$type2);
        check_nil($input_array3,$type2);
        $input_array3 = corr_xml_string(correct_const($input_array3));
        $str2int_arg3 = $domtree->createElement("arg3", "$input_array3");
        $str2int_arg3->setAttribute("type", $type2);
    }else
        lex_err();

$str2int->appendChild($str2int_arg1);
$str2int->appendChild($str2int_arg2);
$str2int->appendChild($str2int_arg3);
}


function generate_three_arg_label($ins, $instr_counter, $input_array, $input_array2,$input_array3){
    global $setchar;
    global $domtree;
    global $program;
    $setchar = $domtree->createElement("instruction");
    $setchar->setAttribute("order","$instr_counter");
    $setchar->setAttribute("opcode", "$ins");
    $program->appendChild($setchar);

    $input_array = corr_xml_string($input_array);
    $setchar_arg1 = $domtree->createElement("arg1", "$input_array");
    $setchar_arg1->setAttribute("type", "label");
    if(check_arg($input_array2)==0 && check_arg($input_array3)==0){
        $input_array2 = corr_xml_string($input_array2);
        $setchar_arg2 = $domtree->createElement("arg2", "$input_array2");
        $setchar_arg2->setAttribute("type", "var");

        $input_array3 = corr_xml_string($input_array3);
        $setchar_arg3 = $domtree->createElement("arg3", "$input_array3");
        $setchar_arg3->setAttribute("type", "var");

    } elseif (check_arg($input_array2)==0 && check_arg($input_array3)==1){
        $input_array2 = corr_xml_string($input_array2);
        $setchar_arg2 = $domtree->createElement("arg2", "$input_array2");
        $setchar_arg2->setAttribute("type", "var");

        $type = get_type($input_array3);
        $input_array3 = corr_xml_string(correct_const($input_array3));
        $setchar_arg3 = $domtree->createElement("arg3", "$input_array3");
        $setchar_arg3->setAttribute("type", $type);
    } elseif (check_arg($input_array2)==1 && check_arg($input_array3)==0){
        $type = get_type($input_array2);
        $input_array2 = corr_xml_string(correct_const($input_array2));
        $setchar_arg2 = $domtree->createElement("arg2", "$input_array2");
        $setchar_arg2->setAttribute("type", $type);

        $input_array3 = corr_xml_string($input_array3);
        $setchar_arg3 = $domtree->createElement("arg3", "$input_array3");
        $setchar_arg3->setAttribute("type", "var");
    }elseif(check_arg($input_array2)==1 && check_arg($input_array3)==1){
        $type = get_type($input_array2);
        $input_array2 = corr_xml_string(correct_const($input_array2));
        $setchar_arg2 = $domtree->createElement("arg2", "$input_array2");
        $setchar_arg2->setAttribute("type", $type);

        $type2 = get_type($input_array3);
        $input_array3 = corr_xml_string(correct_const($input_array3));
        $setchar_arg3 = $domtree->createElement("arg3", "$input_array3");
        $setchar_arg3->setAttribute("type", $type2);
    }else
        lex_err();
$setchar->appendChild($setchar_arg1);
$setchar->appendChild($setchar_arg2);
$setchar->appendChild($setchar_arg3);
}

function check_params($instr_arr,$param1,$param2, $param3, $label_sign, $symb_sign){
    if($param1 == NULL && $param2 == NULL && $param3 == NULL) {
        if (count($instr_arr) != 1)
            lex_err();
    } elseif($param2 == NULL && $param3 == NULL && $label_sign == 0 && $symb_sign == 0){
        if(count($instr_arr)!=2  || check_arg($param1)!=0)
            lex_err();
    } elseif($param2 == NULL && $param3 == NULL && $label_sign == 1 && $symb_sign == 0) {
        if (count($instr_arr) != 2 || check_label($param1))
            lex_err();
    } elseif ($param2 == NULL && $param3 == NULL && $label_sign == 0 && $symb_sign == 1 ){
        if(count($instr_arr)!=2)
            lex_err();
    } elseif ($param3 == NULL && $label_sign == 0 && $symb_sign == 1){
        if(count($instr_arr)!=3  || check_arg($param1)!=0)
            lex_err();
    } elseif ($param3 == NULL && $label_sign ==0 && $symb_sign ==0 ){
        if(count($instr_arr) != 3 || check_arg($param1)!=0 || check_corr_type($param2)!=0)
            lex_err();
    }elseif($label_sign == 0 && $symb_sign == 1){
        if(count($instr_arr)!=4  || check_arg($param1)!=0)
            lex_err();
    }elseif($label_sign == 1 && $symb_sign ==0){
        if(count($instr_arr)!=4  || check_label($param1)){
            lex_err();
        }
    }

}

function check_corr_type($in){
    if(strcmp($in, "int") === 0 || strcmp($in, "string") === 0 || strcmp($in, "bool") === 0){
        return 0;
    } else
        return -1;
}

function corr_xml_string($in){
    return str_replace(array('&', '<', '>', '\'', '"'), array('&amp;', '&lt;', '&gt;', '&apos;', '&quot;'), $in);
}

function stats_gen($file,$file_output){
        if (file_put_contents($file, $file_output. PHP_EOL,FILE_APPEND) == FALSE) {
            fwrite(STDERR, "Something went wrong with opening file");
            exit(11);
        }
}

function open_file($file,$instr_count){
    if(file_exists($file)) {
        if (is_writable($file) == true) {
            if (file_put_contents($file, $instr_count)!=0) {
                fwrite(STDERR, "Something went wrong with opening file");
                exit(11);
            }
        } else {
            fwrite(STDERR, "Something went wrong with opening file");
            exit(11);
        }
    }else{
        if (file_put_contents($file, $instr_count)!=0) {
            fwrite(STDERR, "Something went wrong with opening file");
            exit(11);
        }
    }
}
/********************** Arguments parsing *************************** */
function check_arguments($option,$argc){
    global $extension;
    $extension = false;
    //var_dump($option);
    //exit(1);
    if($argc !=1) {
        if (array_key_exists("help", $option) == true) {
            if ($argc == 2) {
                echo("--Skript typu filtr načte ze standartního vstupu zdrojový kód IPPcode19, zkontroluje lexikální a syntaktickou správnost kódu a vypíše na standartní výstup XML reprezentaci programu.\n");
            } else
                arg_err();
        } elseif (array_key_exists("stats", $option) == true) {
            $extension = true;
        } else
            arg_err();
    }
}

function extension($option,$instr_counter,$comments_counter,$jump_counter,$label_counter,$argc,$argv){
    if (array_key_exists("stats", $option) == true) {
        $file = $option["stats"];
        open_file($file, "");
        for($i=2;$i<$argc;$i++){
            if($argv[$i]=="--loc"){
                stats_gen($file, $instr_counter-1);
            }elseif($argv[$i]=="--comments"){
                stats_gen($file,$comments_counter);
            }elseif($argv[$i]=="--jumps"){
                stats_gen($file,$jump_counter);
            } elseif($argv[$i]=="--labels"){
                stats_gen($file,$label_counter);
            }else {
                unlink($file);
                arg_err();
            }
        }
    } else
        arg_err();
}

function get_type($in){
    if(strncmp($in, "int@", 3)===0){
        return "int";
    }elseif (strncmp($in,"string@",7)===0){
        return "string";
    }elseif (strncmp($in,"bool@",5)===0){
        return "bool";
    }elseif (strncmp($in,"nil@",4)===0){
        return "nil";
    } else
        lex_err();
    return 0;
}

function check_arg_count($in,$count){
    if(count($in)!=$count){
        lex_err();
    }
}

function check_var($in){
    $temp=explode("@",$in);
    if($temp[1]!=""){
        if (preg_match('/^[A-Za-z$&%*!?_-][0-9A-Za-z$&%*!?_-]*$/', $temp[1]) != 1)
            lex_err();
    }
    return 0;
}

function check_label($in){
    if (preg_match('/^[A-Za-z$&%*!?_-][0-9A-Za-z$&%*!?_-]*$/', $in) != 1)
        lex_err();
    return 0;
}

function f_close($fh){
    if (is_resource($fh)) {
        fclose($fh);
    }
}

function check_string_escape($in,$type){
    if($type==="string") {
        $ret = strpos($in, "\\");
        if ($ret !== false) {
            $count = substr_count($in, "\\", 0);
            $ret = explode("\\", $in);

            for ($i = 1; $i < $count + 1; $i++) {
                $retval = substr($ret[$i], 0, 3);
                if (ctype_digit($retval) == false)
                    lex_err();
            }
        }
    }
}

function check_bool($in,$type){
    if($type==="bool") {
        $in = explode("@", $in);
        if ($in[1] !== "true" && $in[1] !== "false") {
            lex_err();
        }
    }
}

function check_nil($in,$type){
    if ($type === "nil") {
        $in = explode("@", $in);
        if ($in[1] !== "nil") {
            lex_err();
        }
    }
}

/********************** global variables *************************** */
global $file;
$instr_counter = 1;
$comments_counter=0;
$jump_counter=0;
$label_counter = 0;
global $labels,$loc,$comments,$jumps;
$labels = $loc = $comments = $jumps = FALSE;
global $extension;
$extension = false;


$longopts = array("help", "stats:","loc", "comments", "labels", "jumps");
$option = getopt("", $longopts);
check_arguments($option,$argc);
/********************** Check header *************************** */
$fh = fopen('read_test.src', 'r');
$line = fgets($fh);
if(strpos($line, "#", 0) !== FALSE){
    $comments_counter++;
    $line = preg_replace('/\x23.*$/', "", $line); # find and delete "#" and characters after
    if($line === "\n"){
        $line = preg_replace('/^[ \t]*[\r\n]+/m', '', $line); # delete blank lines
    }
}
$line = strtoupper(trim($line));
if($line != ".IPPCODE19"){
    //fwrite(STDERR, "Wrong header!\n");
    exit(21);
}

/*********************** Create XML header ************************* */
$domtree = new DOMDocument('1.0', 'UTF-8');
$domtree->formatOutput=true;
$domtree->preserveWhiteSpace=false;

$program = $domtree->createElement('program');
$program->setAttribute('language', 'IPPcode19');
$domtree->appendChild($program);

/********************** Reading from unput / delete comments *************************** */
while($in=fgets($fh)){
    if(strpos($in, "#", 0) !== FALSE){
        $comments_counter++;
        $in = preg_replace('/\x23.*$/', "", $in); # find and delete "#" and characters after
        if($in === "\n"){
            $in = preg_replace('/^[ \t]*[\r\n]+/m', '', $in); # delete blank lines
        }
    }
    $instr_parse = strtok($in,' '); # split string by space
    $in = remove_eol($in);
    $instr_parse = remove_eol($instr_parse);
    $input_array=(explode(" ",$in));
    if($instr_parse!="") { # sip comments
        $instr_parse = strtoupper($instr_parse);
        switch ($instr_parse) {
            /********************** 0 operandu ******************************* */
            case "CREATEFRAME":
                check_arg_count($input_array,1);
                check_params($input_array,NULL,NULL,NULL,0,0);
                generate_no_arg("CREATEFRAME",$instr_counter);
                $instr_counter++;
                break;
            case "PUSHFRAME":
                check_arg_count($input_array,1);
                check_params($input_array,NULL,NULL,NULL,0,0);
                generate_no_arg("PUSHFRAME",$instr_counter);
                $instr_counter++;
                break;
            case "POPFRAME":
                check_arg_count($input_array,1);
                check_params($input_array,NULL,NULL,NULL,0,0);
                generate_no_arg("POPFRAME",$instr_counter);
                $instr_counter++;
                break;
            case "RETURN":
                check_arg_count($input_array,1);
                check_params($input_array,NULL,NULL,NULL,0,0);
                generate_no_arg("RETURN",$instr_counter);
                $instr_counter++;
                $jump_counter++;
                break;
            case "BREAK":
                check_arg_count($input_array,1);
                check_params($input_array,NULL,NULL,NULL,0,0);
                generate_no_arg("BREAK",$instr_counter);
                $instr_counter++;
                break;
            /***************v********** 1 operand **************************** */
            case "DEFVAR":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 0,0);
                generate_one_arg_var("DEFVAR", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "CALL":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 1,0);
                generate_one_arg_label("CALL", $instr_counter, $input_array[1]);
                $instr_counter++;
                $jump_counter++;
                break;

            case "POPS":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 0,0);
                generate_one_arg_var("POPS", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "PUSHS":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 0,1);
                generate_one_arg_symb("PUSHS", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "LABEL":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 1,0);
                generate_one_arg_label("LABEL", $instr_counter, $input_array[1]);
                $instr_counter++;
                $label_counter++;
                break;

            case "JUMP":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 1,0);
                generate_one_arg_label("JUMP", $instr_counter, $input_array[1]);
                $instr_counter++;
                $jump_counter++;
                break;

            case "WRITE":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 0,1);
                generate_one_arg_symb("WRITE", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "EXIT":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 0,1);
                generate_one_arg_symb("EXIT", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "DPRINT":
                check_arg_count($input_array,2);
                check_params($input_array,$input_array[1], NULL, NULL, 0,1);
                generate_one_arg_symb("DPRINT", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            /***************v********** 2 operandy **************************** */
            case "MOVE":
                check_arg_count($input_array,3);
                check_params($input_array,$input_array[1], $input_array[2], NULL, 0,1);
                generate_two_arg_symvar("MOVE", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            case "STRLEN":
                check_arg_count($input_array,3);
                check_params($input_array,$input_array[1], $input_array[2], NULL, 0,1);
                generate_two_arg_symvar("STRLEN", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            case "TYPE":
                check_arg_count($input_array,3);
                check_params($input_array,$input_array[1], $input_array[2], NULL, 0,1);
                generate_two_arg_symvar("TYPE", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            case "INT2CHAR":
                check_arg_count($input_array,3);
                check_params($input_array,$input_array[1], $input_array[2], NULL, 0,1);
                generate_two_arg_symvar("INT2CHAR", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            case "READ":
                check_arg_count($input_array,3);
                check_params($input_array,$input_array[1], $input_array[2], NULL, 0,0);
                two_arg_read("READ", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            /***************v********** 3 operandy **************************** */
            case "ADD":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("ADD", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "SUB":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("SUB",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "MUL":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("MUL",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "IDIV":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("IDIV",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "LT":
                check_arg_count($input_array,4);
                #TODO: Neni osetren jeste NIL, zatim s nilem muzeme porovnavat jak pres LT, tak GT, ma ovsem fungovat pouze u EQ
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("LT",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "GT":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("GT",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "EQ":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("EQ",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "AND":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("AND",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "OR":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("OR",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "NOT":
                check_arg_count($input_array,3);
                check_params($input_array,$input_array[1], $input_array[2], NULL,0,1);
                generate_two_arg_symvar("NOT", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            case "STRI2INT":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("STRI2INT", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "CONCAT":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("CONCAT", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "GETCHAR":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("GETCHAR", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "SETCHAR":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 0,1);
                generate_three_arg("SETCHAR", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                break;

            case "JUMPIFEQ":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 1,0);
                generate_three_arg_label("JUMPIFEQ", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                $jump_counter++;
                break;

            case "JUMPIFNEQ":
                check_arg_count($input_array,4);
                check_params($input_array,$input_array[1], $input_array[2], $input_array[3], 1,0);
                generate_three_arg_label("JUMPIFNEQ", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                $instr_counter++;
                $jump_counter++;
                break;
            default:
                wrong_code();
        }
    }
}

f_close($fh);


/******************************* Extension ********************************/
if($extension)
    extension($option,$instr_counter,$comments_counter,$jump_counter,$label_counter,$argc,$argv);

echo $domtree->saveXML();