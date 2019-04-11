from xmlParse import *
from inputParse import *
from intLib import *
import sys


def main():
    fh = ""
    inputRead = ""
    sys.stderr.write("---------------------------------------------------")
    file = ArgumentParse.readArg(sys.argv)
    (fh, inputRead) = ArgumentParse.chooseInput(file)



    xmlInput = XmlOperation(fh)
    stringg = xmlInput.readXml() # naparsovany xml string
    #stringg = xmlInput.readXmlFromIn()

    frame = Frame()

    # Prvni pruchod kvuli lex/syn analyze
    for instr in stringg:
        instrName = Instruction.getInstrName(instr).upper()
        for case in switch(instrName):
            if case('CREATEFRAME'):pass
            if case('PUSHFRAME'): pass
            if case('POPFRAME'): pass
            if case('BREAK'): pass
            if case('RETURN'):
                frame.instructionStack[Instruction.getOrder(instr)] = instr
                Instruction.argCountCheck(instr, 0)
                Instruction.noArgInstruction(instr)
                break
            # ------------------ 1 Argument ---------------------
            if case('DEFVAR'): pass
            if case('POPS'):
                Instruction.argCountCheck(instr, 1)
                Instruction.argVarInstruction(instr, 0)
                frame.instructionStack[Instruction.getOrder(instr)] = instr
                break
            if case('LABEL'):
                frame.labels[Instruction.getOrder(instr)] = instr
                Instruction.checkLabel(instr, frame.labelNames)
                frame.labelNames.append(Instruction.getLabel(instr))
            if case('CALL'): pass
            if case('JUMP'):
                Instruction.argCountCheck(instr, 1)
                Instruction.argLabelInstruction(instr, 0)
                frame.instructionStack[Instruction.getOrder(instr)] = instr
                break
            if case('PUSHS'): pass
            if case('WRITE'): pass
            if case('EXIT'): pass
            if case('DPRINT'):
                Instruction.argCountCheck(instr, 1)
                Instruction.argSymbInstruction(instr, 0)
                frame.instructionStack[Instruction.getOrder(instr)] = instr
                break
            # ------------------ 2 Argumenty ---------------------
            if case('MOVE'): pass
            if case('NOT'): pass
            if case('INT2CHAR'): pass
            if case('STRLEN'): pass
            if case('TYPE'):
                Instruction.argCountCheck(instr, 2)
                Instruction.argVarInstruction(instr, 0)
                Instruction.argSymbInstruction(instr, 1)
                frame.instructionStack[Instruction.getOrder(instr)] =  instr
                break
            if case('READ'):
                Instruction.argCountCheck(instr, 2)
                Instruction.argVarInstruction(instr, 0)
                Instruction.argTypeInstruction(instr, 1)
                frame.instructionStack[Instruction.getOrder(instr)] =  instr
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
            if case('STRI2INT'): pass
            if case('CONCAT'): pass
            if case('GETCHAR'): pass
            if case('SETCHAR'):
                frame.instructionStack[Instruction.getOrder(instr)] =  instr
                Instruction.argCountCheck(instr, 3)
                Instruction.argVarInstruction(instr, 0)
                Instruction.argSymbInstruction(instr, 1)
                Instruction.argSymbInstruction(instr, 2)
                frame.instructionStack[Instruction.getOrder(instr)] =  instr
                break
            if case('JUMPIFEQ'): pass
            if case('JUMPIFNEQ'):
                Instruction.checkIfLabelExist(instr, frame.labelNames)
                Instruction.argCountCheck(instr, 3)
                Instruction.argLabelInstruction(instr, 0)
                Instruction.argSymbInstruction(instr, 1)
                Instruction.argSymbInstruction(instr, 2)
                frame.instructionStack[Instruction.getOrder(instr)] =  instr
                break
            if case():
                Error.exitInrerpret(Error.invalidXmlStruct, "Unknown instruction")


    # interpretace
    try:
        act_instr = frame.instructionStack['1']
    except:
        sys.exit(0)
    i = int(Instruction.getOrder(act_instr))
    count = len(frame.instructionStack)
    while i <= count:

        instrName = Instruction.getInstrName(act_instr).upper() #nazev instrukce


        if instrName == 'CREATEFRAME':
            IntInstruction.createframe(frame)
        elif instrName == 'PUSHFRAME':
            IntInstruction.pushframe(frame)

        elif instrName == 'POPFRAME':
            IntInstruction.popframe(frame)

        elif instrName == 'DEFVAR':
            IntInstruction.defvar(frame, act_instr)

        elif instrName == 'MOVE':
            IntInstruction.move(frame, act_instr)

        elif instrName == 'PUSHS':
            IntInstruction.pushs(frame, act_instr)

        elif instrName == 'POPS':
            IntInstruction.pops(frame, act_instr)

        elif instrName == 'ADD':
            (firstNum, secondNum, varName) = IntInstruction.arithmeticOperation(frame, act_instr)
            val = frame.addTwoNumbers(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, int(val))
        elif instrName == 'SUB':
            (firstNum, secondNum, varName) = IntInstruction.arithmeticOperation(frame, act_instr)
            val = frame.subTwoNumbers(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, int(val))
        elif instrName == 'MUL':
            (firstNum, secondNum, varName) = IntInstruction.arithmeticOperation(frame, act_instr)
            val = frame.mulTwoNumbers(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, int(val))
        elif instrName == 'IDIV':
            (firstNum, secondNum, varName) = IntInstruction.arithmeticOperation(frame, act_instr)
            val = frame.divTwoNumbers(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, int(val))

        elif instrName == 'WRITE':
            IntInstruction.Write(frame, act_instr)

        elif instrName == 'LT':
            (firstNum, secondNum, varName) = IntInstruction.relationOperation(frame, act_instr)
            val = frame.isLesser(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, val)
        elif instrName == 'GT':
            (firstNum, secondNum, varName) = IntInstruction.relationOperation(frame, act_instr)
            val = frame.isGreater(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, val)
        elif instrName == 'EQ':
            (firstNum, secondNum, varName) = IntInstruction.relationOperation(frame, act_instr)
            val = frame.isEq(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, val)
        elif instrName == 'AND':
            (firstNum, secondNum, varName) = IntInstruction.logicalOperation(frame, act_instr)
            val = frame.logAnd(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, val)
        elif instrName == 'OR':
            (firstNum, secondNum, varName) = IntInstruction.logicalOperation(frame, act_instr)
            val = frame.logOr(firstNum, secondNum)
            IntInstruction.insertValue(frame, varName, val)
        elif instrName == 'NOT':
            (firstNum, secondNum, varName) = IntInstruction.logicalOperation(frame, act_instr)
            val = frame.logNot(firstNum)
            IntInstruction.insertValue(frame, varName, val)
        elif instrName == 'INT2CHAR':
            IntInstruction.int2char(frame, act_instr)
        elif instrName == 'STRI2INT':
            IntInstruction.stri2int(frame, act_instr)
        elif instrName == 'CONCAT':
            IntInstruction.concat(frame, act_instr)
        elif instrName == 'STRLEN':
            IntInstruction.strlen(frame, act_instr)
        elif instrName == 'EXIT':
            IntInstruction.Exit(frame, act_instr)
        elif instrName == 'DPRINT':
            IntInstruction.dPrint(frame, act_instr)
        elif instrName == 'BREAK':
            IntInstruction.Break(frame)
        elif instrName == 'LABEL':
            IntInstruction.label(frame)
        elif instrName == 'JUMP':          # podivame se, jestli label existuje, a pokud ano, tak do nasledujici instrukce ulozime
            Instruction.checkIfLabelExist(act_instr, frame.labelNames)
            i = IntInstruction.jump(frame, act_instr)
        elif instrName == 'JUMPIFEQ':
            (firstNum, secondNum) = IntInstruction.equalOperator(frame, act_instr)
            i= IntInstruction.jumpIfEq(frame, firstNum, secondNum, act_instr, i)
        elif instrName == 'JUMPIFNEQ':
            (firstNum, secondNum) = IntInstruction.equalOperator(frame, act_instr)
            (act_instr, i) = IntInstruction.jumpIfNeq(frame, firstNum, secondNum, act_instr, i)
        elif instrName == 'BREAK':
            IntInstruction.Break(frame)
        elif instrName == 'GETCHAR':
            IntInstruction.getchar(frame, act_instr)
        elif instrName == 'SETCHAR':
            IntInstruction.setchar(frame, act_instr)
        elif instrName == 'TYPE':
            IntInstruction.typeInstr(frame, act_instr)
        elif instrName == 'CALL':
            Instruction.checkIfLabelExist(act_instr, frame.labelNames)
            i = IntInstruction.callInstr(frame, act_instr, i)
        elif instrName == 'RETURN':
             i = IntInstruction.returnInstr(frame)
        elif instrName == 'READ':
            IntInstruction.readInstr(frame, act_instr)
        else:
            print(instrName)
            print("jina instrukce")
            exit(420)


        i += 1
        if i <= count:
            #print("pico konec")
            try:
                act_instr = frame.instructionStack[str(i)]
            except:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid XML")

main()
