from inputParse import *
from xmlParse import  *


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
        self.TF = self.LF
        self.LF = self.frameStack[-1]

        try:
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

    def checkIfInt(self, integer):
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

    def isSame(self, varname, varname2):
        pass


    def isGreater(self, one, two):
        if(int(one) > int(two)):
            return True
        else:
            return False


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
        Frame.insertValue(self,var,value)
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

    def Add(self, instr):
        varname = Instruction.getAttribVal(instr,0)
        arg1 = Instruction.getAttribVal(instr,1)
        arg2 = Instruction.getAttribVal(instr,2)
        firstNum = 0
        secondNum = 0

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)


        if(firstNum != None and secondNum != None): # pokud jsou opa operandy promenne
            value = self.addTwoNumbers(firstNum, secondNum)
            Frame.insertValue(self, varname, value)
            return (firstNum, secondNum)

        elif(firstNum != None and secondNum == None): # pokud je prvni operand promenna a druhy konstanta
            self.checkIfInt(Instruction.getAttrib(instr, 2))
            value = self.addTwoNumbers(firstNum, arg2)
            Frame.insertValue(self, varname, value)

        elif(firstNum == None and secondNum != None): # pokud je prvni operand konstanta a druhy promenna
            self.checkIfInt(Instruction.getAttrib(instr,1))
            value = self.addTwoNumbers(arg1, secondNum)
            Frame.insertValue(self, varname, value)

        elif(firstNum == None and secondNum == None): # pokud jsou oba operandy konstanty
            self.checkIfInt(Instruction.getAttrib(instr, 1))
            self.checkIfInt(Instruction.getAttrib(instr, 2))
            value = self.addTwoNumbers(arg1, arg2)
            Frame.insertValue(self, varname, value)
        self.instructionCounter += 1

    def sub(self, instr):
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)
        firstNum = 0
        secondNum = 0

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)

        if (firstNum != None and secondNum != None):  # pokud jsou opa operandy promenne
            value = self.subTwoNumbers(firstNum, secondNum)
            Frame.insertValue(self, varname, value)

        elif (firstNum != None and secondNum == None):  # pokud je prvni operand promenna a druhy konstanta
            self.checkIfInt(Instruction.getAttrib(instr, 2))
            value = self.subTwoNumbers(firstNum, arg2)
            Frame.insertValue(self, varname, value)

        elif (firstNum == None and secondNum != None):  # pokud je prvni operand konstanta a druhy promenna
            self.checkIfInt(Instruction.getAttrib(instr, 1))
            value = self.subTwoNumbers(arg1, secondNum)
            Frame.insertValue(self, varname, value)

        elif (firstNum == None and secondNum == None):  # pokud jsou oba operandy konstanty
            self.checkIfInt(Instruction.getAttrib(instr, 1))
            self.checkIfInt(Instruction.getAttrib(instr, 2))
            value = self.subTwoNumbers(arg1, arg2)
            Frame.insertValue(self, varname, value)
        self.instructionCounter += 1

    def Mul(self, instr):
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)
        firstNum = 0
        secondNum = 0

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)

        if (firstNum != None and secondNum != None):  # pokud jsou opa operandy promenne
            value = self.mulTwoNumbers(firstNum, secondNum)
            Frame.insertValue(self, varname, value)

        elif (firstNum != None and secondNum == None):  # pokud je prvni operand promenna a druhy konstanta
            self.checkIfInt(Instruction.getAttrib(instr, 2))
            value = self.mulTwoNumbers(firstNum, arg2)
            Frame.insertValue(self, varname, value)

        elif (firstNum == None and secondNum != None):  # pokud je prvni operand konstanta a druhy promenna
            self.checkIfInt(Instruction.getAttrib(instr, 1))
            value = self.mulTwoNumbers(arg1, secondNum)
            Frame.insertValue(self, varname, value)

        elif (firstNum == None and secondNum == None):  # pokud jsou oba operandy konstanty
            self.checkIfInt(Instruction.getAttrib(instr, 1))
            self.checkIfInt(Instruction.getAttrib(instr, 2))
            value = self.mulTwoNumbers(arg1, arg2)
            Frame.insertValue(self, varname, value)
        self.instructionCounter += 1


    def Idiv(self, instr):
        varname = Instruction.getAttribVal(instr, 0)
        arg1 = Instruction.getAttribVal(instr, 1)
        arg2 = Instruction.getAttribVal(instr, 2)
        firstNum = 0
        secondNum = 0

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(arg1)
        secondNum = self.getValFromVar(arg2)

        if (firstNum != None and secondNum != None):  # pokud jsou opa operandy promenne
            value = self.divTwoNumbers(firstNum, secondNum)
            Frame.insertValue(self, varname, value)

        elif (firstNum != None and secondNum == None):  # pokud je prvni operand promenna a druhy konstanta
            self.checkIfInt(Instruction.getAttrib(instr, 2))
            value = self.divTwoNumbers(firstNum, arg2)
            Frame.insertValue(self, varname, value)

        elif (firstNum == None and secondNum != None):  # pokud je prvni operand konstanta a druhy promenna
            self.checkIfInt(Instruction.getAttrib(instr, 1))
            value = self.divTwoNumbers(arg1, secondNum)
            Frame.insertValue(self, varname, value)

        elif (firstNum == None and secondNum == None):  # pokud jsou oba operandy konstanty
            self.checkIfInt(Instruction.getAttrib(instr, 1))
            self.checkIfInt(Instruction.getAttrib(instr, 2))
            value = self.divTwoNumbers(arg1, arg2)
            Frame.insertValue(self, varname, value)
        self.instructionCounter += 1

    def Write(self, instr):
        varname = Instruction.getAttribVal(instr, 0)

        self.checkFrameExists(varname)
        firstNum = self.getValFromVar(varname)
        print(firstNum, end='')