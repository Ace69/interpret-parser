from inputParse import *
from xmlParse import  *
import sys

class Frame:

    def __init__(self):
        self.GF = dict()
        self.TF = None
        self.LF = None
        self.frameStack = []
        self.instructionCounter = 0
        self.stack = []
        self.labels = {}
        self.instructionStack = {}
        self.labelNames = []
        self.callStack = []

    def initLF(self):
        self.LF = dict()

    def initTF(self):
        self.TF = dict()

    def moveTFtoLF(self):
        if self.TF != None:
            self.LF = self.TF
            self.TF = None
        else:
            Error.exitInrerpret(Error.invalidFrame, "Frame not defined")

    def moveLFtoTF(self): #TODO Dodelat
        try:
            self.TF = self.LF
            self.LF = self.frameStack[0]
            self.frameStack.pop()
        except:
            Error.exitInrerpret(Error.invalidFrame, "No frame available")

    def insertIntoGlobal(self, var, value):
        self.GF[var[3:]] = value

    def insertIntoTemp(self, var):
        self.TF[var[3:]] = None

    def insertIntoLocal(self, var):
        self.LF[var[3:]] = None

    def insertVar(self, var):
        if var[:3] == "GF@":
            self.insertIntoGlobal(var, None)
        elif var[:3] == "TF@":
            try:
                self.insertIntoTemp(var)
            except:
                Error.exitInrerpret(Error.invalidFrame, "No temporary frame available")
        elif var[:3] == "LF@":
            try:
                self.insertIntoLocal(var)
            except:
                Error.exitInrerpret(Error.invalidFrame, "No local frame available")

    def checkInGlobal(self, varname):
        if not varname in self.GF:
            Error.exitInrerpret(Error.invalidVar, "Variable does not exists")

    def checkInTemp(self, varname):
        if self.TF != None:
            if varname in self.TF:
                pass
            else:
                Error.exitInrerpret(Error.invalidVar, "Variable does not exists")
        else:
            Error.exitInrerpret(Error.invalidFrame, "Frame does not exists")

    def checkInLocal(self, varname):
        if self.LF != None:
            if varname in self.LF:
                pass
            else:
                Error.exitInrerpret(Error.invalidVar, "Variable does not exists")
        else:
            Error.exitInrerpret(Error.invalidFrame, "Frame does not exists")

    def checkFrameExists(self, varname):
        if varname[:3] == "GF@":
            self.checkInGlobal(varname[3:])
        elif varname[:3] == "TF@":
            self.checkInTemp(varname[3:])
        elif varname[:3] == "LF@":
            self.checkInLocal(varname[3:])

    def insertValue(self, varName, value):
        if varName[:3] == "GF@":
            self.checkInGlobal(varName[3:])
            self.GF[varName[3:]] = value
        elif varName[:3] == "TF@":
            self.checkInTemp(varName[3:])
            self.TF[varName[3:]] = value
        elif varName[:3] == "LF@":
            self.checkInLocal(varName[3:])
            self.LF[varName[3:]] = value

    def insertValIntoStack(self, varname):
        self.stack.append(varname)

    def getValFromStack(self, varname):
        if varname[:3] == "GF@":
            if varname[3:] in self.GF:
                try:
                    self.GF[varname[3:]] = self.stack.pop()
                except:
                    Error.exitInrerpret(Error.noValue, "No value in stack")

        elif varname[:3] == "TF@":
            if varname[3:] in self.TF:
                try:
                    self.TF[varname[3:]] = self.stack.pop()
                except:
                    Error.exitInrerpret(Error.noValue, "No value in stack")

        elif varname[:3] == "LF@":
            if varname[3:] in self.LF:
                try:
                    self.LF[varname[3:]] = self.stack.pop()
                except:
                    Error.exitInrerpret(Error.noValue, "No value in stack")

    def getValFromVar(self, varname):
        self.checkFrameExists(varname)
        if varname[:3] == "GF@":
            return self.GF[varname[3:]]
        elif varname[:3] == "TF@":
            return self.TF[varname[3:]]
        elif varname[:3] == "LF@":
            return self.LF[varname[3:]]

    def isSameValue(self, one, two):
        if (one == "true" or one == "false") and (two == "true" or two == "false"):
            pass
        elif self.checkInt(one) and self.checkInt(two):
            pass
        else:
            Error.exitInrerpret(Error.invalidOperandValue, "Operands are not same")

    def isLesser(self, one, two):
        one = self.reversCorrBool(one)
        two = self.reversCorrBool(two)
        if one < two:
            return True
        else:
            return False

    def isEq(self, one, two):
        one = self.reversCorrBool(one)
        two = self.reversCorrBool(two)
        if one == two:
            return True
        else:
            return False

    def logAnd(self, one, two):
        one = self.reversCorrBool(one)
        two = self.reversCorrBool(two)
        return one and two

    def logOr(self, one, two):
        one = self.reversCorrBool(one)
        two = self.reversCorrBool(two)
        return one or two

    def logNot(self, one):
        one = self.reversCorrBool(one)
        return not one

    def checkLabelExist(self, label, instr):  # TODO ??
        for label in self.labels:
            print(Instruction.getAttribVal(instr, 0))

    def checkPositiveNumber(self, num):
        if (int(num) < 0):
            Error.exitInrerpret(Error.invalidString, "Invalid string")

    def modifyString(self, varname, index, string):
        if (len(string) > 1):
            string = string[0]
        if (string == ""):
            Error.exitInrerpret(Error.invalidString, "Invalid string")

        modifiedString = list(self.getValFromVar(varname))
        try:
            modifiedString[int(index)] = string
        except:
            Error.exitInrerpret(Error.invalidString, "Invalid string")
        modifiedString = ''.join(modifiedString)
        return modifiedString

    def printValue(self, val):
        if (val == True):
            print("true", end='')
        elif (val == False):
            print("false", end='')
        else:
            print(val, end='')

    def checkBool(self, one, two):
        if ((one != False and one != True) or (two != False and two != True)):
            Error.exitInrerpret(Error.invalidOperandType, "Invalid operators")

    def reversCorrBool(self, const):
        if (const == "true"):
            return True
        elif (const == "false"):
            return False
        else:
            return const

    def corrBool(self, const):
        if (const == True):
            return "true"
        elif (const == False):
            return "false"
        else:
            return const

    def getType(self, const):
        if (type(const) is int):
            return "int"
        elif (type(const) is str):
            return "string"
        elif (type(const) is bool):
            return "bool"
        elif (type(const) is None):
            return None

    def getEscapeSequence(self, instr):

        groups = re.findall(r"\\([0-9]{3})", instr)  # Find escape sequences
        groups = list(set(groups))  # Remove duplicates

        # -- Decode escape sqeuences --
        for group in groups:
            if group == "092":  # Special case for \ (I don't even know why)
                xmlValue = re.sub("\\\\092", "\\\\", instr)
                continue

        xmlValue = re.sub("\\\\{0}".format(group), chr(int(group)), instr)
        return xmlValue

    def isVariable(self, instr):
        if (Instruction.getAttrib(instr, 0) == "var"):
            return True

    def isGreater(self, one, two):
        if (str(one) > str(two)):
            return True
        else:
            return False

    def checkInt(self, integer):
        if not re.search(r"^[-+]?\d+$$",
                         str(integer)):  # pokud to nebyl object, tak regex hazel chybu, musel jsem castnout na string
            Error.exitInrerpret(Error.invalidOperandType, "Invalid operands")

    def divTwoNumbers(self, one, two):
        try:
            return (int(one) // int(two))
        except:
            Error.exitInrerpret(Error.invalidOperandValue, "Zero division!")

    def mulTwoNumbers(self, one, two):
        return (int(one) * int(two))

    def subTwoNumbers(self, one, two):
        return (int(one) - int(two))

    def addTwoNumbers(self, one, two):
        return (int(one) + int(two))

    def checkIfTypeInt(self, integer):
        if (integer != "int"):
            Error.exitInrerpret(Error.invalidOperandType, "Invalid operand type")

    def checkNone(self, instr):
        if instr is None:
            Error.exitInrerpret(Error.noValue, "No value in variable")


class IntInstruction(Frame):

    def createframe(self):
        """"" Vytvori novy TF a pripadne zahodi existujici"""""
        Frame.initTF(self)
        self.instructionCounter += 1
    def pushframe(self):
        """"" Presune TF do zasboniku ramcu LF, pote bude TF neinicializovany"""""
        Frame.initLF(self)
        Frame.moveTFtoLF(self)
        self.frameStack.append(self.LF)
        self.instructionCounter += 1

    def popframe(self):
        """"" Presune nejvyssi LF do TF, pokud neni tak chyba """""
        Frame.moveLFtoTF(self)
        self.instructionCounter += 1

    def defvar(self, instr):
        """"" Vytvoreni nove neinicializovane promenne <var> """""
        var = Instruction.getAttribVal(instr,0)
        Frame.insertVar(self,var)
        Frame.insertValue(self, var, None)
        self.instructionCounter += 1

    def move(self, instr):
        """"" Vlozeni hodnoty <symb> do promenne <var>"""""
        var = Instruction.getAttribVal(instr,0)
        value = Instruction.getAttribVal(instr,1)
        if Instruction.getAttrib(instr, 1) == "int":
            Frame.insertValue(self,var,int(value))
            self.instructionCounter += 1
        elif Instruction.getAttrib(instr, 1) == "bool":
            value = self.reversCorrBool( value)
            Frame.insertValue(self,var,value)
            self.instructionCounter += 1
        elif Instruction.getAttrib(instr, 1) == "string":
            if(value is None):
                Frame.insertValue(self,var,str(""))
            else:
                Frame.insertValue(self, var, str(value))
            self.instructionCounter += 1

    def pushs(self, instr):
        """"" Vlozeni <symb> do zasobniku zasobnikovych instrukci"""""
        varname = Instruction.getAttribVal(instr,0)
        self.checkFrameExists(varname)
        self.insertValIntoStack(varname)
        self.instructionCounter += 1

    def pops(self, instr):
        """"" Popnuti <symb> ze zasobniku zasobnikovych instrukci"""""
        varname = Instruction.getAttribVal(instr,0)
        self.checkFrameExists(varname)
        val = self.getValFromVar(varname)
        self.insertValue(varname, val)
        self.instructionCounter += 1

    def arithmeticOperation(self, instr):
        """"" Provedeni aritmetickych operaci ADD,SUB, MUL, IDIV"""""
        varname = Instruction.getAttribVal(instr,0)
        arg1 = Instruction.getAttribVal(instr,1)
        arg2 = Instruction.getAttribVal(instr,2)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)
        self.instructionCounter += 1

        firstNumT = self.getType(firstNum)
        secondNumT = self.getType(secondNum)


        if firstNum != None and secondNum != None: # pokud jsou opa operandy promenne
            self.checkIfTypeInt(firstNumT)
            self.checkIfTypeInt(secondNumT)
            return firstNum, secondNum, varname

        elif firstNum != None and secondNum == None: # pokud je prvni operand promenna a druhy konstanta
            self.checkIfTypeInt(firstNumT)
            self.checkIfTypeInt(Instruction.getAttrib(instr, 2))
            return firstNum, arg2, varname


        elif firstNum == None and secondNum != None: # pokud je prvni operand konstanta a druhy promenna
            self.checkIfTypeInt(Instruction.getAttrib(instr, 1))
            self.checkIfTypeInt(secondNumT)
            return arg1, secondNum, varname

        elif firstNum == None and secondNum == None: # pokud jsou oba operandy konstanty
            self.checkIfTypeInt(Instruction.getAttrib(instr, 1))
            self.checkIfTypeInt(Instruction.getAttrib(instr, 2))
            return arg1, arg2, varname


    def Write(self, instr):
        """"" Vypis hodnoty <symb> na standardni vystup """""
        varname = Instruction.getAttribVal(instr, 0)
        if self.isVariable(instr):
            self.checkFrameExists(varname)
            firstNum = self.getValFromVar(varname)
            self.checkNone(firstNum)
            self.printValue(firstNum)
        else:
            if Instruction.getAttrib(instr, 0) == "string":
                #varname = self.getEscapeSequence(varname)
                if varname == None:
                    print("",end='')
                else:
                    print(varname,end='')
            else:
                print(varname,end='')


    def relationOperation(self, instr):
        """"" Relacni operace GT/LT/EQ, - opet problem s booleanem, nutno dodelat"""""
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)

        arg1T = Instruction.getAttrib(instr,1)
        arg2T = Instruction.getAttrib(instr,2)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)

        firstNumT = self.getType(firstNum)
        secondNumT = self.getType(secondNum)

        self.instructionCounter += 1

        if firstNum != None and secondNum != None:  # pokud jsou opa operandy promenne
            if firstNumT == secondNumT:
                return firstNum, secondNum, varname
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif firstNum != None and secondNum == None:  # pokud je prvni operand promenna a druhy konstanta
            if firstNumT == arg2T:
                return firstNum, arg2, varname
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif firstNum == None and secondNum != None:  # pokud je prvni operand konstanta a druhy promenna
            if arg1T == secondNumT:
                return arg1, secondNum, varname
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif firstNum == None and secondNum == None:  # pokud jsou oba operandy konstanty
            if arg1T == arg2T:
                return arg1, arg2, varname
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")
            if firstNumT == secondNumT:
                return firstNum, secondNum, varname
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

    def logicalOperation(self, instr):
        """"" NOT nefunguje"""""
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)
        self.instructionCounter += 1

        if firstNum != None and secondNum != None:  # pokud jsou opa operandy promenne
            self.checkBool(firstNum, secondNum)
            return firstNum, secondNum, varname

        elif firstNum != None and secondNum == None:  # pokud je prvni operand promenna a druhy konstanta
            self.checkBool(firstNum, arg2)
            return firstNum, arg2, varname

        elif firstNum == None and secondNum != None:  # pokud je prvni operand konstanta a druhy promenna
            self.checkBool(arg1, secondNum)
            return arg1, secondNum, varname

        elif firstNum == None and secondNum == None:  # pokud jsou oba operandy konstanty
            self.checkBool(arg1, arg2)
            return arg1, arg2, varname


    def int2char(self, instr):
        """"" Prevede ciselnou hodnotu v <symb> na znak Unicode a vlozi do <var>"""""
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        self.instructionCounter += 1

        if firstNum != None: # promenna
            self.checkInt(firstNum)
            try:
                retVal = chr(int(firstNum))
                IntInstruction.insertValue(self, varname, retVal)
            except:
                Error.exitInrerpret(Error.invalidString, "String error")
        elif firstNum == None: # konstanta
            self.checkInt(arg1)
            try:
                retVal = chr(int(arg1))
                IntInstruction.insertValue(self, varname, retVal)
            except:
                Error.exitInrerpret(Error.invalidString, "String error")

    def stri2int(self, instr):
        """"" Do promenne <var>  se ulozi ordinalni(ciselna) hodnota znaku v <symb> """""
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        index = Instruction.getAttribVal(instr, 2)

        arg1T = Instruction.getAttrib(instr, 1)
        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(index)
        self.instructionCounter += 1
        firstNumT = self.getType(firstNum)
        if(firstNumT != "string" or arg1T != "string"):
            Error.exitInrerpret(Error.invalidOperandType, "Invalid value")

        if firstNum != None:
            try:
                reTval = ord(arg1[int(firstNum)]) #TODO: funguje nejak divne
                IntInstruction.insertValue(self, varname, reTval)
            except:
                Error.exitInrerpret(Error.invalidString, "invalid string")
        elif firstNum == None:
            try:
                reTval = ord(arg1[int(index)])
                IntInstruction.insertValue(self, varname, reTval)
            except:
                Error.exitInrerpret(Error.invalidString, "invalid string")

    def concat(self, instr):
        """"" Konkatenace dvou retezcu <symb1> a <symb1> a ulozeni do <var>"""""
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)

        arg1T = Instruction.getAttrib(instr, 1)
        arg2T = Instruction.getAttrib(instr, 2)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)

        firstNumT = self.getType(firstNum)
        secondNumT = self.getType(secondNum)

        self.checkNone(secondNumT)
        self.checkNone(firstNumT)
        self.checkNone(arg1T)
        self.checkNone(arg2T)

        self.instructionCounter += 1


        if firstNum != None and secondNum != None:
            if firstNumT == "string" and secondNumT == "string":
                retVal = firstNum + secondNum
                IntInstruction.insertValue(self, varname, retVal)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid value")

        elif firstNum == None and secondNum != None:
            if arg1T == "string" and secondNumT == "string":
                retVal = arg1 + secondNum
                IntInstruction.insertValue(self, varname, retVal)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid value")
        elif firstNum != None and secondNum == None:
            if firstNumT == "string" and arg2T == "string":
                retVal = firstNum + arg2
                IntInstruction.insertValue(self, varname, retVal)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid value")
        elif firstNum == None and secondNum == None:
            if arg1T == "string" and arg2T == "string":
                retVal = arg1 + arg2
                IntInstruction.insertValue(self, varname, retVal)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid value")

    def strlen(self, instr):
        """"" Zjisteni delky retezce <symb> a ulozeni do <var>"""""
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)

        arg1T = Instruction.getAttrib(instr, 1)

        self.instructionCounter += 1
        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)

        firstNumT = self.getType(firstNum)
        if firstNum != None:
            if firstNumT == "string":
                retVal = len(firstNum)
                IntInstruction.insertValue(self, varname, retVal)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid value")
        elif firstNum == None:
            if arg1T== "string":
                retVal = len(arg1)
                IntInstruction.insertValue(self, varname, retVal)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid value")
    def Exit(self, instr):
        """"" Ukonceni programu s kodem danym parametrem <symb> v intervalu 0-49, jinak chyba 57"""""
        arg1 = Instruction.getAttribVal(instr, 0)
        arg1T = Instruction.getAttrib(instr, 0)
        self.instructionCounter += 1
        firstNum = self.getValFromVar(arg1)
        firstNumT = self.getType(firstNum)
        if firstNum != None:
            if(firstNumT == "int"):
                if 0 <= int(firstNum) <= 49:
                    sys.exit(firstNum)
                else:
                    Error.exitInrerpret(Error.invalidOperandValue, "Invalid operand value")
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid operand value")

        elif firstNum == None:
            if(arg1T == "int"):
                if 0 <= int(arg1) <= 49:
                    sys.exit(arg1)
                else:
                    Error.exitInrerpret(Error.invalidOperandValue, "Invalid operand value")
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid operand value")

    def dPrint(self, instr):
        """"" Vypis <symb> na stderr """""
        arg1 = Instruction.getAttribVal(instr, 0)
        self.instructionCounter += 1

        firstNum = self.getValFromVar(arg1)
        if firstNum != None:
            sys.stderr.write(firstNum+"\n")
        elif firstNum == None:
            sys.stderr.write(arg1+"\n")
        else:
            Error.exitInrerpret(Error.invalidOperandType, "Dprint error")

    def Break(self):
        """"" Vypis potrebnych informaci na stdout """""
        self.instructionCounter += 1

        print("\n------------------------------------------")
        print("Global frame:           " + str(self.GF))
        print("Temporary frame:        " + str(self.TF))
        print("Local frame:            " + str(self.LF))
        print("Frame stack:            " + str(self.frameStack))
        print("Instruction counter:    " + str(self.instructionCounter))
        print("Stack:                  " + str(self.stack))
        print("Instruction stack:      " + str(self.instructionStack))
        print("Labels:                 " + str(self.labels))

    def label(self):
        """""Vse potrebne se jiz vykonalo v prvnim pruchodu """""
        self.instructionCounter += 1

    def jump(self, ac):
        """"" Nepodminene skoci na dane navesti"""""
        self.instructionCounter += 1
        for act_instr in self.labels:  # instrukci na pozici labelu, a take do i(ORDER) ulozime ORDER labelu -1, protoze se na konci cyklu automaticky
            if(Instruction.getAttribVal(self.labels[act_instr],0) == Instruction.getAttribVal(ac,0)):
                act_instr = self.labels[act_instr]
                return (int(Instruction.getOrder(act_instr))-1)

    def jumpIfEq(self, first, second, actual_instr, i):
        """""V pripade rovnosti skoci na dane navesti"""""
        self.instructionCounter += 1
        for actual_instr in self.labels:
            if int(first) == int(second):
                if (Instruction.getAttribVal(self.labels[act_instr], 0) == Instruction.getAttribVal(ac, 0)):
                    act_instr = self.labels[act_instr]
                    return (int(Instruction.getOrder(act_instr)) - 1)
                # act_instr = frame.instructionStack[str(i)]
            else:
                return  i
                #Nerovnaji se
        else:
            Error.exitInrerpret(Error.intSemantic, "Missing label")

    def jumpIfNeq(self, first, second, actual_instr, i):
        """""V pripade nerovnosti skoci na dane navesti"""""
        self.instructionCounter += 1
        for actual_instr in self.labels:
            if int(first) != int(second):
                actual_instr = (self.labels[actual_instr])
                i = int(Instruction.getOrder(actual_instr)) - 1
                return actual_instr, i
                # act_instr = frame.instructionStack[str(i)]
            else:
                return actual_instr, i
                #Nerovnaji se
        else:
            Error.exitInrerpret(Error.intSemantic, "Missing label")

    def equalOperator(self, instr):
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)

        arg1T = Instruction.getAttrib(instr, 1)
        arg2T = Instruction.getAttrib(instr, 2)


        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)

        firstNumT = getType(firstNum)
        secondNumT = getType(secondNum)

        self.instructionCounter += 1

        if firstNum != None and secondNum != None:  # pokud jsou opa operandy promenne
            Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif firstNum != None and secondNum == None:  # pokud je prvni operand promenna a druhy konstanta
            if firstNumT == arg2T:
                return firstNum, arg2
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif firstNum == None and secondNum != None:  # pokud je prvni operand konstanta a druhy promenna
            if arg1T == secondNumT:
                return arg1, secondNum
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif firstNum == None and secondNum == None:  # pokud jsou oba operandy konstanty
            if arg1T == arg2T:
                return arg1, arg2
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")
            if firstNumT == secondNumT:
                return firstNum, secondNum
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

    def getchar(self, instr):
        """""Vrati znak retezce v <symb1> na indexu <symb2>"""""
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)

        arg1T = Instruction.getAttrib(instr, 1)
        arg2T = Instruction.getAttrib(instr, 2)

        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)

        firstNumT = self.getType(firstNum)
        secondNumT = self.getType(secondNum)
        self.checkNone(secondNumT)
        self.checkNone(firstNumT)
        self.checkNone(arg1T)
        self.checkNone(arg2T)
        self.instructionCounter += 1
        if(firstNum is not None and secondNum is not None): # promenna a promenna

            if(firstNumT == "string" and secondNumT == "int"):
                self.checkPositiveNumber(secondNum)
                try:
                    IntInstruction.insertValue(self, varname, firstNum[int(secondNum)])
                except:
                    Error.exitInrerpret(Error.invalidString, "Invalid string")

        elif(firstNum is not None and secondNum is None): #promena a konstanta
            if(firstNumT == "string" and arg2T == "int" ):
                self.checkPositiveNumber(arg2)
                try:
                    IntInstruction.insertValue(self, varname, firstNum[int(arg2)])
                except:
                    Error.exitInrerpret(Error.invalidString, "Invalid string")

        elif (firstNum is None and secondNum is not None):  # promena a konstanta
            if (arg1T == "string" and secondNumT== "int"):
                self.checkPositiveNumber(secondNum)
                try:
                    IntInstruction.insertValue(self, varname, arg1[int(secondNum)])
                except:
                    Error.exitInrerpret(Error.invalidString, "Invalid string")

        elif (firstNum is None and secondNum is None):  # promena a konstanta
            if (arg1T == "string" and arg2T == "int"):
                self.checkPositiveNumber(arg2)
                try:
                    IntInstruction.insertValue(self, varname, arg1[int(arg2)])
                except:
                    Error.exitInrerpret(Error.invalidString, "Invalid string")

    def setchar(self, instr):
        """""Zmodifikuje znak v promenne <var> na indexu <symb1> na znak <symb2>"""""
        self.instructionCounter += 1
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)

        arg1T = Instruction.getAttrib(instr, 1)
        arg2T = Instruction.getAttrib(instr, 2)

        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)

        firstNumT = self.getType(firstNum)
        secondNumT = self.getType(secondNum)

        if(self.getType(self.getValFromVar(varname)) != "string"):
            Error.exitInrerpret(Error.invalidString, "Invalid string")

        if(firstNum is not None and secondNum is not None): # var a var
            if(firstNumT == "int" and secondNumT == "string"):
                reTval = self.modifyString(varname, firstNum, secondNum)
                self.insertValue(varname, reTval)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid operands")

        elif(firstNum is None and secondNum is not None): # const a var
            if(arg1T == "int" and secondNumT == "string"):
                reTval = self.modifyString(varname,arg1, secondNum)
                self.insertValue(varname, reTval)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid operands")
        elif (firstNum is not None and secondNum is None): # var a const
            if (firstNum == "int" and arg2T == "string"):
                reTval = self.modifyString(varname, firstNum, arg2)
                self.insertValue(varname, reTval)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid operands")
        elif (firstNum is None and secondNum is None): # var a const
            if (arg1T == "int" and arg2T == "string"):
                reTval = self.modifyString(varname, arg1, arg2)
                self.insertValue(varname, reTval)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "Invalid operands")
    def typeInstr(self, instr):
        """""Dynamicky vrati typ symbolu"""""
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        firstNum =  self.getValFromVar(arg1)

        if(firstNum is not None): # var
            self.insertValue(varname, self.getType(firstNum))
        else:
            self.insertValue(varname, Instruction.getAttrib(instr, 1))

    def callInstr(self, ac, i):
        """""Skoci na dane navesti s moznosti navraceni"""""
        self.callStack.append(i) # ulozeni hodnoty do zasobniku volani

        self.instructionCounter += 1
        for act_instr in self.labels:  # instrukci na pozici labelu, a take do i(ORDER) ulozime ORDER labelu -1, protoze se na konci cyklu automaticky
            if (Instruction.getAttribVal(self.labels[act_instr], 0) == Instruction.getAttribVal(ac, 0)):
                act_instr = self.labels[act_instr]
                return (int(Instruction.getOrder(act_instr)) - 1)

    def returnInstr(self):
        """""Navrat z daneho skoku, pokud je to mozne"""""
        i = 0
        try:
            i = self.callStack.pop()
        except:
            Error.exitInrerpret(Error.noValue, "No value to return")

        return i

    def readInstr(self, instr):
       pass
