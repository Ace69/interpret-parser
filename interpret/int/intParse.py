from xmlParse import *
from inputParse import *
import re


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

    def moveLFtoTF(self):
        try:
            self.TF = self.LF
            self.LF = self.frameStack[-1]
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
                self.GF[varname[3:]] = self.stack.pop()

        elif varname[:3] == "TF@":
            if varname[3:] in self.TF:
                self.TF[varname[3:]] = self.stack.pop()

        elif varname[:3] == "LF@":
            if varname[3:] in self.LF:
                self.LF[varname[3:]] = self.stack.pop()

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
