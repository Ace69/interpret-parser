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

function check_arg($in){
    if (strncmp($in, "GF@", 3) === 0 || strncmp($in, "LF@", 3) === 0 || strncmp($in, "TF@", 3) === 0) # variable
        return 0;
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

function no_arg($ins, $instr_counter){
    global $createframe ;
    global $domtree;
    global $program;
    $createframe = $domtree->createElement("instruction");
    $createframe->setAttribute("order","$instr_counter");
    $createframe->setAttribute("opcode", "$ins");
    $program->appendChild($createframe);
}

function one_arg_var($ins, $instr_counter, $input_array){
    global $pops;
    global $domtree;
    global $program;
    $pops = $domtree->createElement("instruction");
    $pops->setAttribute("order","$instr_counter");
    $pops->setAttribute("opcode", "$ins");
    $program->appendChild($pops);

    $pops_arg1 = $domtree->createElement("arg1", "$input_array");
    $pops_arg1->setAttribute("type", "var");
    $pops->appendChild($pops_arg1);
}

function one_arg_label($ins, $instr_counter, $input_array){
    global $call;
    global $domtree;
    global $program;
    $call = $domtree->createElement("instruction");
    $call->setAttribute("order","$instr_counter");
    $call->setAttribute("opcode", "$ins");
    $program->appendChild($call);

    $call_arg1 = $domtree->createElement("arg1", "$input_array");
    $call_arg1->setAttribute("type", "label");
    $call->appendChild($call_arg1);
}

function one_arg_symb($ins, $instr_counter, $input_array){
    global $pushs;
    global $domtree;
    global $program;
    $pushs = $domtree->createElement("instruction");
    $pushs->setAttribute("order","$instr_counter");
    $pushs->setAttribute("opcode", "$ins");
    $program->appendChild($pushs);

    if(check_arg($input_array)==0){
        $pushs_arg1 = $domtree->createElement("arg1", "$input_array");
        $pushs_arg1->setAttribute("type", "var");
    } elseif (check_arg($input_array)==1){
        $input_array = correct_const($input_array);
        $pushs_arg1 = $domtree->createElement("arg1", "$input_array");
        $pushs_arg1->setAttribute("type", "const");
    }else
        lex_err();
    $pushs->appendChild($pushs_arg1);
}

function two_arg_symvar($ins, $instr_counter, $input_array, $input_array2){
    global $move;
    global $domtree;
    global $program;
    $move = $domtree->createElement("instruction");
    $move->setAttribute("order","$instr_counter");
    $move->setAttribute("opcode", "$ins");
    $program->appendChild($move);

    $move_arg1 = $domtree->createElement("arg1", "$input_array");
    $move_arg1->setAttribute("type", "var");
    $move->appendChild($move_arg1);


    if(check_arg($input_array)==0){
        if(check_arg($input_array2)==0) {
            $move_arg2 = $domtree->createElement("arg2", "$input_array2");
            $move_arg2->setAttribute("type", "var");
        } elseif(check_arg($input_array2)==1) {
            $input_array2 = correct_const($input_array2);
            $move_arg2 = $domtree->createElement("arg2", "$input_array2");
            $move_arg2->setAttribute("type", "const");
        } else
            lex_err();
    } else
        lex_err();
    $move->appendChild($move_arg2);
}
function three_arg_semantic($ins, $instr_counter, $input_array, $input_array2,$input_array3){
    global $add;
    global $domtree;
    global $program;
    $add = $domtree->createElement("instruction");
    $add->setAttribute("order","$instr_counter");
    $add->setAttribute("opcode", "$ins");
    $program->appendChild($add);

    $add_arg1 = $domtree->createElement("arg1", "$input_array");
    $add_arg1->setAttribute("type", "var");

    if (check_arg($input_array2) === 0) {
        $add_arg2 = $domtree->createElement("arg2", "$input_array2");
        $add_arg2->setAttribute("type", "var");
    } elseif (check_arg($input_array2) == 1 && strncmp($input_array2, "int@", 4) ===0) {
        $input_array2 = correct_const($input_array2);
        $add_arg2 = $domtree->createElement("arg2", "$input_array2");
        $add_arg2->setAttribute("type", "const");
    } else
        lex_err();
    if (check_arg($input_array3) == 0) {
        $add_arg3 = $domtree->createElement("arg3", "$input_array3");
        $add_arg3->setAttribute("type", "var");
    } elseif (check_arg($input_array3) == 1 && strncmp($input_array3, "int@", 4) ===0) {
        $input_array3 = correct_const($input_array3);
        $add_arg3 = $domtree->createElement("arg3", "$input_array3");
        $add_arg3->setAttribute("type", "const");
    } else
        lex_err();
    $add->appendChild($add_arg1);
    $add->appendChild($add_arg2);
    $add->appendChild($add_arg3);
}
function three_arg_bool($ins, $instr_counter, $input_array, $input_array2,$input_array3){
    global $add;
    global $domtree;
    global $program;
    $add = $domtree->createElement("instruction");
    $add->setAttribute("order","$instr_counter");
    $add->setAttribute("opcode", "$ins");
    $program->appendChild($add);

    $add_arg1 = $domtree->createElement("arg1", "$input_array");
    $add_arg1->setAttribute("type", "var");
    if(check_if_same($input_array2, $input_array3)==0) {
        $input_array2 = correct_const($input_array2);
        $add_arg2 = $domtree->createElement("arg2", "$input_array2");
        $add_arg2->setAttribute("type", "const");

        $input_array3 = correct_const($input_array3);
        $add_arg3 = $domtree->createElement("arg3", "$input_array3");
        $add_arg3->setAttribute("type", "const");
    } elseif (check_arg($input_array2)==0 && check_arg($input_array[3])==1) {
        $add_arg2 = $domtree->createElement("arg2", "$input_array2");
        $add_arg2->setAttribute("type", "var");

        $input_array3 = correct_const($input_array3);
        $add_arg3 = $domtree->createElement("arg3", "$input_array3");
        $add_arg3->setAttribute("type", "const");
    } elseif(check_arg($input_array2)==1 && check_arg($input_array3)==0){
        $input_array2 = correct_const($input_array2);
        $add_arg2 = $domtree->createElement("arg2", "$input_array2");
        $add_arg2->setAttribute("type", "const");

        $add_arg3 = $domtree->createElement("arg3", "$input_array3");
        $add_arg3->setAttribute("type", "var");
    } elseif(check_arg($input_array2)==0 && check_arg($input_array3)==0){
        $add_arg2 = $domtree->createElement("arg2", "$input_array2");
        $add_arg2->setAttribute("type", "var");

        $add_arg3 = $domtree->createElement("arg3", "$input_array3");
        $add_arg3->setAttribute("type", "var");
    }
    else
        lex_err();
    $add->appendChild($add_arg1);
    $add->appendChild($add_arg2);
    $add->appendChild($add_arg3);
}
function three_arg_nosemantic($ins, $instr_counter, $input_array, $input_array2,$input_array3){
    global $str2int;
    global $domtree;
    global $program;
    $str2int = $domtree->createElement("instruction");
    $str2int->setAttribute("order","$instr_counter");
    $str2int->setAttribute("opcode", "$ins");
    $program->appendChild($str2int);

    $str2int_arg1 = $domtree->createElement("arg1", "$input_array");
    $str2int_arg1->setAttribute("type", "var");
    if(check_arg($input_array2)==0 && check_arg($input_array3)==0){
        $str2int_arg2 = $domtree->createElement("arg2", "$input_array2");
        $str2int_arg2->setAttribute("type", "var");

        $str2int_arg3 = $domtree->createElement("arg3", "$input_array3");
        $str2int_arg3->setAttribute("type", "var");

    } elseif (check_arg($input_array2)==0 && check_arg($input_array3)==1){
        $str2int_arg2 = $domtree->createElement("arg2", "$input_array2");
        $str2int_arg2->setAttribute("type", "var");

        $input_array3 = correct_const($input_array3);
        $str2int_arg3 = $domtree->createElement("arg3", "$input_array3");
        $str2int_arg3->setAttribute("type", "const");
    } elseif (check_arg($input_array2)==1 && check_arg($input_array3)==0){
        $input_array2 = correct_const($input_array2);
        $str2int_arg2 = $domtree->createElement("arg2", "$input_array2");
        $str2int_arg2->setAttribute("type", "const");

        $str2int_arg3 = $domtree->createElement("arg3", "$input_array3");
        $str2int_arg3->setAttribute("type", "var");
    }elseif(check_arg($input_array2)==1 && check_arg($input_array3)==1){
        $input_array2 = correct_const($input_array2);
        $str2int_arg2 = $domtree->createElement("arg2", "$input_array2");
        $str2int_arg2->setAttribute("type", "const");

        $input_array3 = correct_const($input_array3);
        $str2int_arg3 = $domtree->createElement("arg3", "$input_array3");
        $str2int_arg3->setAttribute("type", "const");
    }else
        lex_err();

$str2int->appendChild($str2int_arg1);
$str2int->appendChild($str2int_arg2);
$str2int->appendChild($str2int_arg3);
}

function three_arg_label($ins, $instr_counter, $input_array, $input_array2,$input_array3){
    global $setchar;
    global $domtree;
    global $program;
    $setchar = $domtree->createElement("instruction");
    $setchar->setAttribute("order","$instr_counter");
    $setchar->setAttribute("opcode", "$ins");
    $program->appendChild($setchar);

    $setchar_arg1 = $domtree->createElement("arg1", "$input_array");
    $setchar_arg1->setAttribute("type", "label");
    if(check_arg($input_array2)==0 && check_arg($input_array3)==0){
        $setchar_arg2 = $domtree->createElement("arg2", "$input_array2");
        $setchar_arg2->setAttribute("type", "var");

        $setchar_arg3 = $domtree->createElement("arg3", "$input_array3");
        $setchar_arg3->setAttribute("type", "var");

    } elseif (check_arg($input_array2)==0 && check_arg($input_array3)==1){
        $setchar_arg2 = $domtree->createElement("arg2", "$input_array2");
        $setchar_arg2->setAttribute("type", "var");

        $input_array3 = correct_const($input_array3);
        $setchar_arg3 = $domtree->createElement("arg3", "$input_array3");
        $setchar_arg3->setAttribute("type", "const");
    } elseif (check_arg($input_array2)==1 && check_arg($input_array3)==0){
        $input_array2 = correct_const($input_array2);
        $setchar_arg2 = $domtree->createElement("arg2", "$input_array2");
        $setchar_arg2->setAttribute("type", "const");

        $setchar_arg3 = $domtree->createElement("arg3", "$input_array[3]");
        $setchar_arg3->setAttribute("type", "var");
    }elseif(check_arg($input_array2)==1 && check_arg($input_array3)==1){
        $input_array2 = correct_const($input_array2);
        $setchar_arg2 = $domtree->createElement("arg2", "$input_array2");
        $setchar_arg2->setAttribute("type", "const");

        $input_array3 = correct_const($input_array3);
        $setchar_arg3 = $domtree->createElement("arg3", "$input_array3");
        $setchar_arg3->setAttribute("type", "const");
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
        if (count($instr_arr) != 2 || ctype_alnum($param1) == false)
            lex_err();
    } elseif ($param2 == NULL && $param3 == NULL && $label_sign == 0 && $symb_sign == 1 ){
        if(count($instr_arr)!=2)
                lex_err();
    } elseif ($param3 == NULL && $label_sign == 0 && $symb_sign == 1){
        if(count($instr_arr)!=3  || check_arg($param1)!=0)
            lex_err();
        }

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

/********************** Reading from unput / delete comments *************************** */
global $instr_counter;
$instr_counter=1;
while($in=fgets($fh)){
    if(strpos($in, "#", 0) !== FALSE){
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
        switch ($instr_parse) {
            /********************** 0 operandu ******************************* */
            case "CREATEFRAME":
                check_params($input_array,NULL,NULL,NULL,0,0);
                no_arg("CREATEFRAME",$instr_counter);
                $instr_counter++;
                break;
            case "PUSHFRAME":
                check_params($input_array,NULL,NULL,NULL,0,0);
                no_arg("PUSHFRAME",$instr_counter);
                $instr_counter++;
                break;
            case "POPFRAME":
                check_params($input_array,NULL,NULL,NULL,0,0);
                no_arg("POPFRAME",$instr_counter);
                $instr_counter++;
                break;
            case "RETURN":
                check_params($input_array,NULL,NULL,NULL,0,0);
                no_arg("RETURN",$instr_counter);
                $instr_counter++;
                break;
            case "BREAK":
                check_params($input_array,NULL,NULL,NULL,0,0);
                no_arg("BREAK",$instr_counter);
                $instr_counter++;
                break;
            /***************v********** 1 operand **************************** */
            case "DEFVAR":
                check_params($input_array,$input_array[1], NULL, NULL, 0,0);
                one_arg_var("DEFVAR", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "CALL":
                check_params($input_array,$input_array[1], NULL, NULL, 1,0);
                one_arg_label("CALL", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "POPS":
                check_params($input_array,$input_array[1], NULL, NULL, 0,0);
                one_arg_var("POPS", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "PUSHS":
                check_params($input_array,$input_array[1], NULL, NULL, 0,1);
                one_arg_symb("PUSHS", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "LABEL":
                check_params($input_array,$input_array[1], NULL, NULL, 1,0);
                one_arg_label("LABEL", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "JUMP":
                check_params($input_array,$input_array[1], NULL, NULL, 1,0);
                one_arg_label("JUMP", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "WRITE":
                check_params($input_array,$input_array[1], NULL, NULL, 0,1);
                one_arg_symb("WRITE", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "EXIT":
                check_params($input_array,$input_array[1], NULL, NULL, 0,1);
                one_arg_symb("EXIT", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            case "DPRINT":
                check_params($input_array,$input_array[1], NULL, NULL, 0,1);
                one_arg_symb("DPRINT", $instr_counter, $input_array[1]);
                $instr_counter++;
                break;

            /***************v********** 2 operandy **************************** */
            case "MOVE":
                check_params($input_array,$input_array[1], $input_array[2], NULL, 0,1);
                two_arg_symvar("MOVE", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            case "STRLEN":
                check_params($input_array,$input_array[1], $input_array[2], NULL, 0,1);
                two_arg_symvar("STRLEN", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            case "TYPE":
                check_params($input_array,$input_array[1], $input_array[2], NULL, 0,1);
                two_arg_symvar("TYPE", $instr_counter, $input_array[1], $input_array[2]);
                $instr_counter++;
                break;

            case "INT2CHAR":
                if(count($input_array)!=3  || check_arg($input_array[1])!=0)
                    lex_err();
                 else {
                     two_arg_symvar("INT2CHAR", $instr_counter, $input_array[1], $input_array[2]);
                     $instr_counter++;
                 }break;

            case "READ":
                #TODO: opravit druhy parametr a predelat do funkce
                if(str_word_count($in)<4 || str_word_count($in)>5 || check_type($input_array[2])!=0 || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    $read = $domtree->createElement("instruction");
                    $read->setAttribute("order","$instr_counter");
                    $read->setAttribute("opcode", "READ");
                    $program->appendChild($read);

                    $read_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $read_arg1->setAttribute("type", "var");
                    $input_array[2] = correct_const($input_array[2]);
                    $read_arg2 = $domtree->createElement("arg1", "$input_array[2]");
                    $read_arg2->setAttribute("type", "type");
                    $read->appendChild($read_arg1);
                    $read->appendChild($read_arg2);
                    $instr_counter++;
                }
                break;
            case "ADD":
                if(count($input_array)!=4  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_semantic("ADD", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }break;

            case "SUB":
                if(count($input_array)!=4  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_semantic("SUB",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }
                break;
            case "MUL":
                if(count($input_array)!=4  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_semantic("MUL",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }
                break;
            case "IDIV":
                if(count($input_array)!=4  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_semantic("IDIV",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }
                break;
            case "LT":
                #TODO: Neni osetren jeste NIL, zatim s nilem muzeme porovnavat jak pres LT, tak GT, ma ovsem fungovat pouze u EQ
                if(count($input_array)!=4  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_bool("LT",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }
                break;
            case "GT":
                if(count($input_array)!=4  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_bool("GT",$instr_counter,$input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }
                break;
            case "EQ":
                if(((check_arg($input_array[1])!=0) || count($input_array)!=4 ))
                    lex_err();
                else {
                    $add = $domtree->createElement("instruction");
                    $add->setAttribute("order","$instr_counter");
                    $add->setAttribute("opcode", "EQ");
                    $program->appendChild($add);

                    $add_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $add_arg1->setAttribute("type", "var");
                    if(check_if_same($input_array[2], $input_array[3])==0) {
                        $input_array[2] = correct_const($input_array[2]);
                        $add_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $add_arg2->setAttribute("type", "const");

                        $input_array[3] = correct_const($input_array[3]);
                        $add_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $add_arg3->setAttribute("type", "const");
                    } elseif (check_arg($input_array[2])==0 && check_arg($input_array[3])==1) {
                        $add_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $add_arg2->setAttribute("type", "var");

                        $input_array[3] = correct_const($input_array[3]);
                        $add_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $add_arg3->setAttribute("type", "const");
                    } elseif(check_arg($input_array[2])==1 && check_arg($input_array[3])==0){
                        $input_array[2] = correct_const($input_array[2]);
                        $add_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $add_arg2->setAttribute("type", "const");

                        $add_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $add_arg3->setAttribute("type", "var");
                    } elseif(check_arg($input_array[2])==0 && check_arg($input_array[3])==0){
                        $add_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $add_arg2->setAttribute("type", "var");

                        $add_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $add_arg3->setAttribute("type", "var");
                    }
                    else
                        lex_err();
                    $add->appendChild($add_arg1);
                    $add->appendChild($add_arg2);
                    $add->appendChild($add_arg3);
                    $instr_counter++;
                }
                break;
            case "AND":
                if(count($input_array)!=4  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    $and = $domtree->createElement("instruction");
                    $and->setAttribute("order","$instr_counter");
                    $and->setAttribute("opcode", "AND");
                    $program->appendChild($and);

                    $and_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $and_arg1->setAttribute("type", "var");
                    $and->appendChild($and_arg1);

                    if(check_arg($input_array[2])==0 && check_arg($input_array[3])===0){
                        $and_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $and_arg2->setAttribute("type", "var");
                        $and->appendChild($and_arg2);
                        $and_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $and_arg3->setAttribute("type", "var");

                    } elseif(strncmp($input_array[2], "bool@", 5)===0 && check_arg($input_array[3])==0) {
                        $input_array[2] = correct_const($input_array[2]);
                        $and_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $and_arg2->setAttribute("type", "const");
                        $and->appendChild($and_arg2);
                        $and_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $and_arg3->setAttribute("type", "var");

                    } elseif (strncmp($input_array[3], "bool@", 5)===0 && check_arg($input_array[2])==0) {
                        $and_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $and_arg2->setAttribute("type", "var");
                        $and->appendChild($and_arg2);
                        $input_array[3] = correct_const($input_array[3]);
                        $and_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $and_arg3->setAttribute("type", "const");

                    } elseif (strncmp($input_array[2], "bool@", 5)===0 && strncmp($input_array[3], "bool@", 5)===0){
                        $input_array[2] = correct_const($input_array[2]);
                        $and_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $and_arg2->setAttribute("type", "const");


                        $input_array[3] = correct_const($input_array[3]);
                        $and_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $and_arg3->setAttribute("type", "const");

                    }
                    else
                        lex_err();
                    $and->appendChild($and_arg1);
                    $and->appendChild($and_arg2);
                    $and->appendChild($and_arg3);
                    $instr_counter++;
                }
                break;
            case "OR":
                if(count($input_array)!=4  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    $and = $domtree->createElement("instruction");
                    $and->setAttribute("order","$instr_counter");
                    $and->setAttribute("opcode", "OR");
                    $program->appendChild($and);

                    $and_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $and_arg1->setAttribute("type", "var");


                    if(check_arg($input_array[2])==0 && check_arg($input_array[3])===0){
                        $and_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $and_arg2->setAttribute("type", "var");

                        $and_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $and_arg3->setAttribute("type", "var");

                    } elseif(strncmp($input_array[2], "bool@", 5)===0 && check_arg($input_array[3])==0) {
                        $input_array[2] = correct_const($input_array[2]);
                        $and_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $and_arg2->setAttribute("type", "const");

                        $and_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $and_arg3->setAttribute("type", "var");

                    } elseif (strncmp($input_array[3], "bool@", 5)===0 && check_arg($input_array[2])==0) {
                        $and_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $and_arg2->setAttribute("type", "var");

                        $input_array[3] = correct_const($input_array[3]);
                        $and_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $and_arg3->setAttribute("type", "const");

                    } elseif (strncmp($input_array[2], "bool@", 5)===0 && strncmp($input_array[3], "bool@", 5)===0){
                        $input_array[2] = correct_const($input_array[2]);
                        $and_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $and_arg2->setAttribute("type", "const");


                        $input_array[3] = correct_const($input_array[3]);
                        $and_arg3 = $domtree->createElement("arg3", "$input_array[3]");
                        $and_arg3->setAttribute("type", "const");

                    }
                    else
                        lex_err();
                    $and->appendChild($and_arg1);
                    $and->appendChild($and_arg2);
                    $and->appendChild($and_arg3);
                    $instr_counter++;
                }
                break;

            case "NOT":
                if(count($input_array)!=3  || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    $not = $domtree->createElement("instruction");
                    $not->setAttribute("order","$instr_counter");
                    $not->setAttribute("opcode", "NOT");
                    $program->appendChild($not);

                    $not_arg1 = $domtree->createElement("arg1", "$input_array[1]");
                    $not_arg1->setAttribute("type", "var");

                    if(check_arg($input_array[2])==0 ){
                        $not_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $not_arg2->setAttribute("type", "var");
                    } elseif(strncmp($input_array[2], "bool@", 5)===0){
                        $input_array[2]= correct_const($input_array[2]);
                        $not_arg2 = $domtree->createElement("arg2", "$input_array[2]");
                        $not_arg2->setAttribute("type", "const");
                    }
                }
                $not->appendChild($not_arg1);
                $not->appendChild($not_arg2);
                $instr_counter++;
                break;

                #TODO: Odtud az dolu neresim semantiku
            case "STR2INT":
                if(count($input_array)!=4 || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_nosemantic("STR2INT", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }break;

            case "CONCAT":

                if(count($input_array)!=4 || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_nosemantic("CONCAT", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }break;

            case "GETCHAR":
                if(count($input_array)!=4 || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_nosemantic("GETCHAR", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }break;

            case "SETCHAR":
                if(count($input_array)!=4 || check_arg($input_array[1])!=0)
                    lex_err();
                else {
                    three_arg_nosemantic("SETCHAR", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }break;

            case "JUMPIFEQ":
                if(count($input_array)!=4  || ctype_alnum($input_array[1])==false)
                    lex_err();
                else {
                    three_arg_label("SETCHAR", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }break;

            case "JUMPIFNEQ":
                if(count($input_array)!=4  || ctype_alnum($input_array[1])==false)
                    lex_err();
                else {
                    three_arg_label("SETCHAR", $instr_counter, $input_array[1], $input_array[2], $input_array[3]);
                    $instr_counter++;
                }break;
            default:
                lex_err();
        }
    }
}
echo $domtree->saveXML();