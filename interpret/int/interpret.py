from xmlParse import *
from inputParse import *
from intLib import *


def main():

    labels = []
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
            if case('LABEL'): labels.append(Instruction.getLabel(instr))
            if case('CALL'): pass
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




    frame = Frame()

    # Interpretace

    for instr in stringg:
        instrName = Instruction.getInstrName(instr).upper()
        for case in switch(instrName):
            if case('CREATEFRAME'):
                IntInstruction.createframe(frame)
                break
            if case('PUSHFRAME'):
                IntInstruction.pushframe(frame)
                break
            if case('POPFRAME'):
                IntInstruction.popframe(frame)
                break
            if case('DEFVAR'):
                IntInstruction.defvar(frame, instr)
                break
            if case('MOVE'):
                IntInstruction.move(frame, instr)
                break
            if case('PUSHS'):
                IntInstruction.pushs(frame, instr)
                break
            if case('POPS'):
                IntInstruction.pops(frame, instr)
                break
            if case('ADD'):
                (firstNum,secondNum, varName) = IntInstruction.arithmeticOperation(frame, instr)
                val = frame.addTwoNumbers(firstNum,secondNum)
                IntInstruction.insertValue(frame, varName, int(val))
                break
            if case('SUB'):
                (firstNum, secondNum, varName) = IntInstruction.arithmeticOperation(frame, instr)
                val = frame.subTwoNumbers(firstNum, secondNum)
                IntInstruction.insertValue(frame, varName, int(val))
                break
            if case('MUL'):
                (firstNum, secondNum, varName) = IntInstruction.arithmeticOperation(frame, instr)
                val = frame.mulTwoNumbers(firstNum, secondNum)
                IntInstruction.insertValue(frame, varName, int(val))
                break
            if case('IDIV'):
                (firstNum, secondNum, varName) = IntInstruction.arithmeticOperation(frame, instr)
                val = frame.divTwoNumbers(firstNum, secondNum)
                IntInstruction.insertValue(frame, varName, int(val))
                break
            if case('WRITE'):
                IntInstruction.Write(frame, instr)
                break
            if case('LT'):
                (firstNum, secondNum, varName) = IntInstruction.relationOperation(frame, instr)
                val = frame.isLesser(firstNum, secondNum)
                IntInstruction.insertValue(frame, varName, val)
                break
            if case('GT'):
                (firstNum, secondNum, varName) = IntInstruction.relationOperation(frame, instr)
                val = frame.isGreater(firstNum, secondNum)
                IntInstruction.insertValue(frame, varName, val)
                break
            if case('EQ'):
                (firstNum, secondNum, varName) = IntInstruction.relationOperation(frame, instr)
                val = frame.isEq(firstNum, secondNum)
                IntInstruction.insertValue(frame, varName, val)
                break
            if case('AND'):
                (firstNum, secondNum, varName) = IntInstruction.logicalOperation(frame, instr)
                val = frame.logAnd(firstNum, secondNum)
                IntInstruction.insertValue(frame, varName, val)
                break
            if case('OR'):
                (firstNum, secondNum, varName) = IntInstruction.logicalOperation(frame, instr)
                val = frame.logOr(firstNum, secondNum)
                IntInstruction.insertValue(frame, varName, val)
                break
            if case('NOT'):
                (firstNum, secondNum, varName) = IntInstruction.logicalOperation(frame, instr)
                val = frame.logNot(firstNum)
                IntInstruction.insertValue(frame, varName, val)
                break
            if case('INT2CHAR'):
                IntInstruction.int2char(frame, instr)
                break
            if case('STRI2INT'):
                IntInstruction.stri2int(frame, instr)
                break
            if case('CONCAT'):
                IntInstruction.concat(frame, instr)
                break
            if case('STRLEN'):
                IntInstruction.strlen(frame, instr)
                break
            if case():
                Error.exitInrerpret(Error.invalidXmlStruct, "Unknown instruction")

    print("------------------------------------------")
    print("Global frame:           " + str(frame.GF))
    print("Temporary frame:        " + str(frame.TF))
    print("Local frame:            " + str(frame.LF))
    print("Frame stack:            " + str(frame.frameStack))
    print("Instruction counter:    " + str(frame.instructionCounter))
    print("Stack:                  " + str(frame.stack))



main()
