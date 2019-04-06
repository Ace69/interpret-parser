from inputParse import *
from xmlParse import  *
import re


class Frame(Instruction):

    def __init__(self):
        self.GF = dict()
        self.TF = None
        self.LF = None
        self.frameStack = []
        self.instructionCounter = 0
        self.stack = []

    def initLF(self):
        self.LF = dict()


    def initTF(self):
        self.TF = dict()


    def moveTFtoLF(self):
        if(self.TF != None):
            self.LF = self.TF
            self.TF = None
        else:
            Error.exitInrerpret(Error.invalidFrame,"Frame not defined")

    def moveLFtoTF(self):
        try:
            self.TF = self.LF
            self.LF = self.frameStack[-1]
            self.frameStack.pop()
        except:
            Error.exitInrerpret(Error.invalidFrame, "No frame available")

    def insertIntoGlobal(self, var, value):
        self.GF[var[3:]] = value

    def insertIntoTemp(self,var):
        self.TF[var[3:]] = None

    def insertIntoLocal(self, var):
        self.LF[var[3:]] = None


    def insertVar(self, var):
        if (var[:3] == "GF@"):
            self.insertIntoGlobal(var, None)
        elif(var[:3] == "TF@"):
            try:
                self.insertIntoTemp(var)
            except:
                Error.exitInrerpret(Error.invalidFrame,"No temporary frame available")
        elif(var[:3] == "LF@"):
            try:
                self.insertIntoLocal(var)
            except:
                Error.exitInrerpret(Error.invalidFrame,"No local frame available")

    def checkInGlobal(self, varname):
        if not varname in  self.GF:
            Error.exitInrerpret(Error.invalidVar, "Variable does not exists")


    def checkInTemp(self, varname):
        if(self.TF != None):
            if varname in self.TF:
                pass
            else:
                Error.exitInrerpret(Error.invalidVar, "Variable does not exists")
        else:
            Error.exitInrerpret(Error.invalidFrame, "Frame does not exists")

    def checkInLocal(self, varname):
        if(self.LF != None):
            if varname in self.LF:
                pass
            else:
                Error.exitInrerpret(Error.invalidVar, "Variable does not exists")
        else:
            Error.exitInrerpret(Error.invalidFrame, "Frame does not exists")

    def checkFrameExists(self, varname):
        if(varname[:3] == "GF@"):
            self.checkInGlobal(varname[3:])
        elif (varname[:3] == "TF@"):
            self.checkInTemp(varname[3:])
        elif (varname[:3] == "LF@"):
            self.checkInLocal(varname[3:])


    def insertValue(self, varName,value):
        if(varName[:3] == "GF@"):
            self.checkInGlobal(varName[3:])
            self.GF[varName[3:]] = value
        elif(varName[:3] == "TF@"):
            self.checkInTemp(varName[3:])
            self.TF[varName[3:]] = value
        elif(varName[:3] == "LF@"):
            self.checkInLocal(varName[3:])
            self.LF[varName[3:]] = value

    def insertValIntoStack(self, varname):
        if(varname[:3] == "GF@"):
            if varname[3:] in self.GF:
                self.stack.append(self.GF.get(varname[3:]))

        elif(varname[:3] == "TF@"):
            if(varname[3:] in self.TF):
                self.stack.append(self.TF.get(varname[3:]))

        elif(varname[:3] == "LF@"):
            if(varname[3:] in self.LF):
                self.stack.append(self.LF.get(varname[3:]))

    def getValFromStack(self, varname):
        if (varname[:3] == "GF@"):
            if varname[3:] in self.GF:
                self.GF[varname[3:]] = self.stack.pop()

        elif (varname[:3] == "TF@"):
            if varname[3:] in self.TF:
                self.TF[varname[3:]] = self.stack.pop()

        elif (varname[:3] == "LF@"):
            if varname[3:] in self.LF:
                self.LF[varname[3:]] = self.stack.pop()

    def checkIfTypeInt(self, integer):
        if(integer != "int"):
            Error.exitInrerpret(Error.invalidOperandType, "Invalid operand type")



    def getValFromVar(self, varname):
        self.checkFrameExists(varname)
        if(varname[:3] == "GF@"):
            return (self.GF[varname[3:]])
        elif (varname[:3] == "TF@"):
            return (self.TF[varname[3:]])
        elif (varname[:3] == "LF@"):
            return (self.LF[varname[3:]])

    def addTwoNumbers(self, one, two):
        return (int(one) + int(two))

    def subTwoNumbers(self, one, two):
        return (int(one) - int(two))

    def mulTwoNumbers(self, one, two):
        return (int(one) * int(two))

    def divTwoNumbers(self, one, two):
        try:
            return (int(one) / int(two))
        except:
            Error.exitInrerpret(Error.invalidOperandValue, "Zero division!")

    def checkInt(self, integer):
        if not re.search(r"^[-+]?\d+$$", str(integer)): # pokud to nebyl object, tak regex hazel chybu, musel jsem castnout na string
            Error.exitInrerpret(Error.invalidOperandType, "Invalid operands")


    def isSameValue(self, one,two):
        if((one == "true" or one == "false") and ( two == "true" or two == "false")):
            print("booole")
        elif(self.checkInt(one) and self.checkInt(two)):
            print("intttt")
            pass
        else:
            print("neuspelo")

    def isGreater(self, one, two):
        if(str(one) > str(two)):
            return True
        else:
            return False

    def isLesser(self, one, two):
        if(str(one) < str(two)):
            return True
        else:
            return False

    def isEq(self, one, two):
        if(str(one) == str(two)):
            return True
        else:
            return False

    def logAnd(self, one, two):
        one = self.reversCorrBool(one)
        two = self.reversCorrBool(two)
        return(one and two)

    def logOr(self, one, two):
        one = self.reversCorrBool(one)
        two = self.reversCorrBool(two)
        return (one or two)

    def logNot(self, one):
        one = self.reversCorrBool(one)
        return (not(one))

    def isVariable(self, instr):
        if(Instruction.getAttrib(instr,0) == "var"):
            return True

    def getEscapeSequence(cls, instr):

        groups = re.findall(r"\\([0-9]{3})", instr)  # Find escape sequences
        groups = list(set(groups))  # Remove duplicates

        # -- Decode escape sqeuences --
        for group in groups:
            if group == "092":  # Special case for \ (I don't even know why)
                xmlValue = re.sub("\\\\092", "\\\\", instr)
                continue

        xmlValue = re.sub("\\\\{0}".format(group), chr(int(group)), instr)
        return xmlValue

    def getType(self, const):
        if(type(const) is int):
            return "int"
        elif(type(const) is str):
            return "string"
        elif(type(const) is bool):
            return "bool"
        elif(type(const) is None):
            return "None"

    def corrBool(self, const):
        if(const == True):
            return "true"
        elif(const == False):
            return "false"

    def reversCorrBool(self, const):
        if(const == "true"):
            return True
        elif(const == "false"):
            return False

    def checkBool(self, one, two):
        if((one != "false" and one != "true") or (two != "false" and two != "true")):
            Error.exitInrerpret(Error.invalidOperandType, "Invalid operators")

class IntInstruction(Frame):

    def createframe(self):
        Frame.initTF(self)
        self.instructionCounter += 1
    def pushframe(self):
        Frame.initLF(self)
        Frame.moveTFtoLF(self)
        self.frameStack.append(self.LF)
        self.instructionCounter += 1


    def popframe(self):
        Frame.moveLFtoTF(self)
        self.instructionCounter += 1

    def defvar(self, instr):
        var = Instruction.getAttribVal(instr,0)
        Frame.insertVar(self,var)
        self.instructionCounter += 1

    def move(self, instr):
        var = Instruction.getAttribVal(instr,0)
        value = Instruction.getAttribVal(instr,1)
        if( Instruction.getAttrib(instr,1) == "int"):
            Frame.insertValue(self,var,int(value))
            self.instructionCounter += 1
        elif(Instruction.getAttrib(instr,1) == "bool"):
            Frame.insertValue(self,var,value)
            self.instructionCounter += 1
        elif(Instruction.getAttrib(instr,1) == "string"):
            Frame.insertValue(self,var,str(value))
            self.instructionCounter += 1

    def pushs(self, instr):
        varname = Instruction.getAttribVal(instr,0)
        self.checkFrameExists(varname)
        self.insertValIntoStack(varname)
        self.instructionCounter += 1

    def pops(self, instr):
        varname = Instruction.getAttribVal(instr,0)
        self.checkFrameExists(varname)
        self.getValFromStack(varname)
        self.instructionCounter += 1

    def arithmeticOperation(self, instr):
        varname = Instruction.getAttribVal(instr,0)
        arg1 = Instruction.getAttribVal(instr,1)
        arg2 = Instruction.getAttribVal(instr,2)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)
        self.instructionCounter += 1

        if(firstNum != None and secondNum != None): # pokud jsou opa operandy promenne
            self.checkInt(firstNum)
            self.checkInt(secondNum)
            return (firstNum, secondNum, varname)

        elif(firstNum != None and secondNum == None): # pokud je prvni operand promenna a druhy konstanta
            self.checkInt(firstNum)
            self.checkIfTypeInt(Instruction.getAttrib(instr, 2))
            return (firstNum, arg2, varname)


        elif(firstNum == None and secondNum != None): # pokud je prvni operand konstanta a druhy promenna
            self.checkIfTypeInt(Instruction.getAttrib(instr, 1))
            print(secondNum)
            self.checkInt(secondNum)
            return (arg1, secondNum, varname)

        elif(firstNum == None and secondNum == None): # pokud jsou oba operandy konstanty
            self.checkIfTypeInt(Instruction.getAttrib(instr, 1))
            self.checkIfTypeInt(Instruction.getAttrib(instr, 2))
            return (arg1, arg2, varname)


    def Write(self, instr):
        varname = Instruction.getAttribVal(instr, 0)
        if(self.isVariable(instr)):
            self.checkFrameExists(varname)
            firstNum = self.getValFromVar(varname)
            print(firstNum)
        else:
            if(Instruction.getAttrib(instr,0) == "string"):
                #varname = self.getEscapeSequence(varname)
                if(varname == None):
                    print("")
                else:
                    print(varname)
            else:
                print(varname)


    def relationOperation(self, instr):
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

        if (firstNum != None and secondNum != None):  # pokud jsou opa operandy promenne
            if(firstNumT == secondNumT):
                return (firstNum, secondNum, varname)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif (firstNum != None and secondNum == None):  # pokud je prvni operand promenna a druhy konstanta
            if(firstNumT == arg2T):
                return (firstNum, arg2, varname)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif (firstNum == None and secondNum != None):  # pokud je prvni operand konstanta a druhy promenna
            if(arg1T == secondNumT):
                return (arg1, secondNum, varname)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

        elif (firstNum == None and secondNum == None):  # pokud jsou oba operandy konstanty
            if(arg1T == arg2T):
                return (arg1, arg2, varname)
            else:
                Error.exitInrerpret(Error.invalidOperandType, "invalid logical operand")

    def logicalOperation(self, instr):
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)
        self.instructionCounter += 1

        if (firstNum != None and secondNum != None):  # pokud jsou opa operandy promenne
            self.checkBool(firstNum, secondNum)
            return (firstNum, secondNum, varname)

        elif (firstNum != None and secondNum == None):  # pokud je prvni operand promenna a druhy konstanta
            self.checkBool(firstNum, arg2)
            return (firstNum, arg2, varname)

        elif (firstNum == None and secondNum != None):  # pokud je prvni operand konstanta a druhy promenna
            self.checkBool(arg1, secondNum)
            return (arg1, secondNum, varname)

        elif (firstNum == None and secondNum == None):  # pokud jsou oba operandy konstanty
            self.checkBool(arg1, arg2)
            return (arg1, arg2, varname)


    def int2char(self, instr):
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        self.instructionCounter += 1

        if(firstNum != None): # promenna
            self.checkInt(firstNum)
            try:
                retVal = chr(int(firstNum))
                IntInstruction.insertValue(self, varname, retVal)
            except:
                Error.exitInrerpret(Error.invalidString, "String error")
        elif(firstNum == None): # konstanta
            self.checkInt(arg1)
            try:
                retVal = chr(int(arg1))
                IntInstruction.insertValue(self, varname, retVal)
            except:
                Error.exitInrerpret(Error.invalidString, "String error")

    def stri2int(self, instr):
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        index = Instruction.getAttribVal(instr, 2)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(index)
        self.instructionCounter += 1

        if(firstNum != None):
            try:
                reTval = ord(arg1[int(firstNum)])
                IntInstruction.insertValue(self, varname, reTval)
            except:
                Error.exitInrerpret(Error.invalidString, "invalid string")
        elif(firstNum == None):
            try:
                reTval = ord(arg1[int(index)])
                IntInstruction.insertValue(self, varname, reTval)
            except:
                Error.exitInrerpret(Error.invalidString, "invalid string")

    def concat(self, instr):
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
        self.instructionCounter += 1


        if(firstNum != None and secondNum != None):
            if(firstNumT == "string" and secondNumT == "strng"):
                retVal = firstNum + secondNum

        elif(firstNum == None and secondNum != None):
            if(arg1T == "string" and secondNumT == "string"):
                retVal = arg1 + secondNum
                IntInstruction.insertValue(self, varname, retVal)
        elif(firstNum != None and secondNum == None):
            if(firstNumT == "string" and arg2T == "string"):
                retVal = firstNum + arg2
                IntInstruction.insertValue(self, varname, retVal)
        elif(firstNum == None and secondNum == None):
            if(arg1T == "string" and arg2T == "string"):
                retVal = arg1 + arg2
                IntInstruction.insertValue(self, varname, retVal)

    def strlen(self, instr):
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)

        arg1T = Instruction.getAttrib(instr, 1)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)

        firstNumT = self.getType(firstNum)
        if(firstNum != None):
            if(firstNumT == "string"):
                retVal = len(firstNum)
                IntInstruction.insertValue(self, varname, retVal)
        elif(firstNum == None):
            if(arg1T== "string"):
                retVal = len(arg1)
                IntInstruction.insertValue(self, varname, retVal)
