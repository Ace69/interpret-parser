<?php

/**
 * Created by Jakub Dolejsi
 * Date: 11.2.19
 */

/*************** STDERR function ******************* */
function lex_err(){
    fwrite(STDERR, "Lexical error!\n");
    exit(22);
}

/*********** remove eol from string *************************/
function remove_eol($str){
    return trim(preg_replace('/\s\s+/', ' ', $str));
}

/* ********************* Arguments parsing *************************** */
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
/********************** Used instruction *************************** */
$instructions = array("", "", "", "", "", "", "",
    "", "", "ADD", "SUB", "IDIV", "MUL", "LT", "GT", "EQ", "AND", "OR",
    "NOT", "", "STRI2INT", "", "", "CONCAT", "", "GETCHAR",
    "", "", "", "JUMPIFEQ", "JUMPIFNEQ", "EXIT", "DPRINT", "");

/********************** Reading from unput / delete comments *************************** */
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
    #echo $instr_parse;
    switch ($instr_parse){
        /********************** 0 operandu ******************************* */
        case "CREATEFRAME":
            if(strcmp($instr_parse, $in)!=0){
                lex_err();
            }else{
                echo"generujeme\n";
                break;
            }
        case "PUSHFRAME":
            if(strcmp($instr_parse, $in)!=0){
                lex_err();
            }else{
                echo "opet generujeme\n";
                break;
            }
        case "POPFRAME":
            if(strcmp($instr_parse, $in)!=0){
                lex_err();
            }else{
                echo "opet generujeme\n";
                break;
            }
        case "RETURN":
            if(strcmp($instr_parse, $in)!=0){
                lex_err();
            }else{
                echo "opet generujeme\n";
                break;
            }
        case "BREAK":
            if(strcmp($instr_parse, $in)!=0){
                lex_err();
            }else{
                echo "opet generujeme\n";
                break;
            }
        /***************v********** 1 operand **************************** */
        case "DEFVAR":
            echo"lexOK";
            EXIT(0);
        case "CALL":
            echo"lexOK";
            EXIT(0);
        case "POPS":
            echo"lexOK";
            EXIT(0);
        case "PUSHS":
            echo"lexOK";
            EXIT(0);
        case "LABEL":
            echo"lexOK";
            EXIT(0);
        case "JUMP":
            echo"lexOK";
            EXIT(0);
        case "WRITE":
            echo"lexOK";
            EXIT(0);
        /***************v********** 2 operandy **************************** */
        case "MOVE":
            echo"lexOK";
            EXIT(0);
        case "INT2CHAR":
            echo"lexOK";
            EXIT(0);
        case "READ":
            echo"lexOK";
            EXIT(0);
        case "STRLEN":
            echo"lexOK";
            EXIT(0);
        case "TYPE":
            echo"lexOK";
            EXIT(0);
        /******* 3 operandy *******
         nasrat */
    }

}

$domtree = new DOMDocument('1.0', 'UTF-8');
$program = $domtree->createElement('program');
$program->setAttribute('language', 'IPPcode19');
