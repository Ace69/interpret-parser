<?php

/**
 * Created by Jakub Dolejsi
 * Date: 11.2.19
 */

function lex_err(){
    fwrite(STDERR, "Lexical error!\n");
    exit(22);
}

function remove_eol($str){
    return trim(preg_replace('/\s\s+/', ' ', $str));
}

function var_or_const($in){
    if (strpos($in, "GF@") || strpos($in, "LF@") || strpos($in, "TF@")) # variable
        return 0;
    elseif(strpos($in, "int@") || strpos($in, "bool@") || strpos($in, "string@") || strpos($in, "nil@")) # const
        return 1;
    else
        return -1;
}

function check_2arg($in)
{
    if (strlen(strstr($in, "string@")) > 0 || strlen(strstr($in, "int@")) > 0 || strlen(strstr($in, "bool@")) > 0 || strlen(strstr($in, "nil@")) > 0) {
        return 0;
    }elseif(strlen(strstr($in, "GF@")) > 0 || strlen(strstr($in, "LF@")) > 0 || strlen(strstr($in, "TF@")) > 0){
        return 1;
    } else{
        return -1;
    }
}

function correct_const($in){
    $in = strstr($in, '@');
    $in = str_replace('@', '', $in);
    return $in;
}
/********************** Arguments parsing *************************** */
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
/********************** Check header *************************** */
$fh = fopen('test.txt', 'r');
$line = fgets($fh);
$line = strtoupper(trim($line));
if($line != ".IPPCODE19"){
    fwrite(STDERR, "Wrong header!\n");
    exit(21);
}

/*********************** Create XML header ************************* */
$domtree = new DOMDocument('1.0', 'UTF-8');
$domtree->formatOutput=true;
$domtree->preserveWhiteSpace=false;

$program = $domtree->createElement('program');
$program->setAttribute('language', 'IPPcode19');
$domtree->appendChild($program);


$data_types = array("int", "bool", "string", "nil", "label", "type", "var",);

/********************** Reading from unput / delete comments *************************** */
$instr_counter=1;
while($in=fgets($fh)){
    if(strpos($in, "#", 0) !== FALSE){
        $in = preg_replace('/\x23.*$/', "", $in); # find and delete "#" and characters after
        if($in === "\n"){
            $in = preg_replace('/^[ \t]*[\r\n]+/m', '', $in); # delete blank lines
        }
    }
    $instr_parse = strtok($in,' '); # split string by space
    $split_str = preg_split("/[\s]+/", $in); # string splitted by spaces into array
    $in = remove_eol($in);
    $instr_parse = remove_eol($instr_parse);
    $input_array=(explode(" ",$in));
    $type="string";
    if($instr_parse!="") { # sip comments
        switch ($instr_parse) {
            /********************** 0 operandu ******************************* */
            case "CREATEFRAME":
                if (strcmp($instr_parse, $in) != 0) {
                    lex_err();
                } else {
                    $createframe = $domtree->createElement("instruction");
                    $createframe->setAttribute("order","$instr_counter");
                    $createframe->setAttribute("opcode", "CREATEFRAME");
                    $program->appendChild($createframe);
                    $instr_counter++;
                }
                break;
            case "PUSHFRAME":
                if (strcmp($instr_parse, $in) != 0) {
                    lex_err();
                } else {
                    $pushframe = $domtree->createElement("instruction");
                    $pushframe->setAttribute("order","$instr_counter");
                    $pushframe->setAttribute("opcode", "PUSHFRAME");
                    $program->appendChild($pushframe);
                    $instr_counter++;
                }
                break;
            case "POPFRAME":
                if (strcmp($instr_parse, $in) != 0) {
                    lex_err();
                } else {
                    $popframe = $domtree->createElement("instruction");
                    $popframe->setAttribute("order","$instr_counter");
                    $popframe->setAttribute("opcode", "POPFRAME");
                    $program->appendChild($popframe);
                    $instr_counter++;
                }
                break;
            case "RETURN":
                if (strcmp($instr_parse, $in) != 0) {
                    lex_err();
                } else {
                    $return = $domtree->createElement("instruction");
                    $return->setAttribute("order","$instr_counter");
                    $return->setAttribute("opcode", "RETURN");
                    $program->appendChild($return);
                    $instr_counter++;
                }
                break;
            case "BREAK":
                if (strcmp($instr_parse, $in) != 0) {
                    lex_err();
                } else {
                    $break = $domtree->createElement("instruction");
                    $break->setAttribute("order","$instr_counter");
                    $break->setAttribute("opcode", "BREAK");
                    $program->appendChild($break);
                    $instr_counter++;
                }
                break;
            /***************v********** 1 operand **************************** */
            case "DEFVAR":
                if (str_word_count($in) != 3 || (strpos($in, 'GF@')==false && strpos($in, 'LF@')==false && strpos($in, 'TF@')==false)) {
                    lex_err();
                } else {
                    $defvar = $domtree->createElement("instruction");
                    $defvar->setAttribute("order","$instr_counter");
                    $defvar->setAttribute("opcode", "DEFVAR");
                    $program->appendChild($defvar);

                    $def_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $def_arg1->setAttribute("type","var");
                    $defvar->appendChild($def_arg1);
                    $instr_counter++;
                }
                break;
            case "CALL":
                if(str_word_count($in)!=2){
                    lex_err();
                } else {
                    $call = $domtree->createElement("instruction");
                    $call->setAttribute("order","$instr_counter");
                    $call->setAttribute("opcode", "CALL");
                    $program->appendChild($call);

                    $call_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $call_arg1->setAttribute("type", "label");
                    $call->appendChild($call_arg1);
                    $instr_counter++;
                }
                break;
            case "POPS":
                if(str_word_count($in)!=3 || (strpos($in, 'GF@')==false && strpos($in, 'LF@')==false && strpos($in, 'TF@')==false) ){
                    lex_err();
                } else {
                    $pops = $domtree->createElement("instruction");
                    $pops->setAttribute("order","$instr_counter");
                    $pops->setAttribute("opcode", "POPS");
                    $program->appendChild($pops);

                    $pops_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $pops_arg1->setAttribute("type", "label");
                    $pops->appendChild($pops_arg1);
                    $instr_counter++;
                }
                break;
            case "PUSHS":
                if(str_word_count($in)!=3){
                    lex_err();
                } else {
                    $pushs = $domtree->createElement("instruction");
                    $pushs->setAttribute("order","$instr_counter");
                    $pushs->setAttribute("opcode", "PUSHS");
                    $program->appendChild($pushs);

                    $pushs_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    if(var_or_const($in)==0){
                        $pushs_arg1->setAttribute("type", "var");
                    } elseif (var_or_const($in)==1){
                        $pushs_arg1->setAttribute("type", "const");
                    }else{
                        lex_err();
                    }
                    $pushs->appendChild($pushs_arg1);
                    $instr_counter++;
                }
                break;
            case "LABEL":
                if(str_word_count($in)!=2){
                    lex_err();
                } else {
                    $label = $domtree->createElement("instruction");
                    $label->setAttribute("order","$instr_counter");
                    $label->setAttribute("opcode", "LABEL");
                    $program->appendChild($label);

                    $label_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $label_arg1->setAttribute("type", "label");
                    $label->appendChild($label_arg1);
                    $instr_counter++;
                }
                break;
            case "JUMP":
                if(str_word_count($in)!=2){
                    lex_err();
                } else {
                    $jump = $domtree->createElement("instruction");
                    $jump->setAttribute("order","$instr_counter");
                    $jump->setAttribute("opcode", "JUMP");
                    $program->appendChild($jump);

                    $jump_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $jump_arg1->setAttribute("type", "label");
                    $jump->appendChild($jump_arg1);
                    $instr_counter++;
                }
                break;
            case "WRITE":
                if(str_word_count($in)!=3){
                    lex_err();
                } else{
                    $write = $domtree->createElement("instruction");
                    $write->setAttribute("order","$instr_counter");
                    $write->setAttribute("opcode", "WRITE");
                    $program->appendChild($write);

                    $write_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    if(var_or_const($in)==0){
                        $write_arg1->setAttribute("type", "var");
                    } elseif (var_or_const($in)==1){
                        $write_arg1->setAttribute("type", "const");
                    }else{
                        lex_err();
                    }
                    $write->appendChild($write_arg1);
                    $instr_counter++;
                }
                break;
            /***************v********** 2 operandy **************************** */
            #TODO: Dodelat overeni druheho parametru, protoze funkce var_or_const zkontroluje cely radek, a ja potrebuju pouze druhy argument
            # Ty dve operace s input_array[2] zajistuji odstraneni napr "GF@" prej vypisem konstanty
            case "MOVE":
                if(str_word_count($in)<4 || (strpos($in, 'GF@')==false && strpos($in, 'LF@')==false && strpos($in, 'TF@')==false) ){
                    lex_err();
                } else {
                    $move = $domtree->createElement("instruction");
                    $move->setAttribute("order","$instr_counter");
                    $move->setAttribute("opcode", "MOVE");
                    $program->appendChild($move);

                    $move_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $move_arg1->setAttribute("type", "var");
                    $move->appendChild($move_arg1);


                    if(var_or_const($in)==0){
                        if(check_2arg($input_array[2])==0) {
                            $input_array[2]= correct_const($input_array[2]);
                            $move_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                            $move_arg2->setAttribute("type", "const");
                        }
                        elseif(check_2arg($input_array[2])==1) {
                            $move_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                            $move_arg2->setAttribute("type", "var");
                        }
                        else
                            lex_err();
                    }else{
                        lex_err();
                    }
                    $move->appendChild($move_arg2);
                    $instr_counter++;

                }
                break;
            case "INT2CHAR":
                echo "lexOK";
                EXIT(0);
            case "READ":
                echo "lexOK";
                EXIT(0);
            case "STRLEN":
                echo "lexOK";
                EXIT(0);
            case "TYPE":
                echo "lexOK";
                EXIT(0);
            default:
                lex_err();
            /******* 3 operandy *******
             * nasrat */
        }
    }

}
echo $domtree->saveXML();