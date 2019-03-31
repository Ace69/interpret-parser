from xmlParse import *
from inputParse import *

GF = dict()
TF = {}
LF = []


def main():

    sourceFile = IOperation('input.src')
    fh =sourceFile.openFile()


    xmlInput = XmlOperation(fh)
    stringg = xmlInput.readXml() # naparsovany xml string


    # Prvni pruchod kvuli lex/syn analyze
    for instr in stringg:
        instrName = Instruction.getInstrName(instr).upper()
        for case in switch(instrName):
            if case('CREATEFRAME'): pass
            if case('PUSHFRAME'): pass
            if case('POPFRAME'): pass
            if case('BREAK'): pass
            if case('RETURN'):
                Instruction.argCountCheck(instr, 0)
                Instruction.noArgInstruction(instr)
                break
            # ------------------ 1 Argument ---------------------
            if case('DEFVAR'): pass
            if case('POPS'):
                Instruction.argCountCheck(instr, 1)
                Instruction.argVarInstruction(instr, 0)
                break
            if case('CALL'): pass
            if case('LABEL'): pass
            if case('JUMP'):
                Instruction.argCountCheck(instr, 1)
                Instruction.argLabelInstruction(instr, 0)
                break
            if case('PUSHS'): pass
            if case('WRITE'): pass
            if case('EXIT'): pass
            if case('DPRINT'):
                Instruction.argCountCheck(instr, 1)
                Instruction.argSymbInstruction(instr, 0)
                break
            # ------------------ 2 Argumenty ---------------------
            if case('MOVE'): pass
            if case('INT2CHAR'): pass
            if case('STRLEN'): pass
            if case('TYPE'):
                Instruction.argCountCheck(instr, 2)
                Instruction.argVarInstruction(instr, 0)
                Instruction.argSymbInstruction(instr, 1)
                break
            if case('READ'):
                Instruction.argCountCheck(instr, 2)
                Instruction.argVarInstruction(instr, 0)
                Instruction.argTypeInstruction(instr, 1)
                break
            # ------------------ 3 Argumenty ---------------------
            if case('ADD'): pass
            if case('SUB'): pass
            if case('MUL'): pass
            if case('IDIV'): pass
            if case('LT'): pass
            if case('GT'): pass
            if case('EQ'): pass
            if case('AND'): pass
            if case('OR'): pass
            if case('NOT'): pass
            if case('STRI2INT'): pass
            if case('CONCAT'): pass
            if case('GETCHAR'): pass
            if case('SETCHAR'):
                Instruction.argCountCheck(instr, 3)
                Instruction.argVarInstruction(instr, 0)
                Instruction.argSymbInstruction(instr, 1)
                Instruction.argSymbInstruction(instr, 2)
                break
            if case('JUMPIFEQ'): pass
            if case('JUMPIFNEQ'):
                Instruction.argCountCheck(instr, 3)
                Instruction.argLabelInstruction(instr, 0)
                Instruction.argSymbInstruction(instr, 1)
                Instruction.argSymbInstruction(instr, 2)
                break
            if case():
                Error.exitInrerpret(Error.invalidXmlStruct, "Unknown instruction")
    print("Parse OK")

    for instr in stringg:
        instrName = Instruction.getInstrName(instr).upper()
        for case in switch(instrName):
            if case('CREATEFRAME'): pass
main()
