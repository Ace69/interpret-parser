import sys
import xml.etree.ElementTree as ET
import re




class Error:
    invalidArgument = 10
    invalidFile = 11

    noWellFormedXml = 31
    invalidXmlStruct = 32

    intSemantic = 52
    invalidOperandType = 53
    invalidVar = 54
    invalidFrame = 55
    noValue = 56
    invalidOperandValue = 57
    invalidString = 58

    @staticmethod
    def exitInrerpret(code,msg):
        sys.stderr.write(msg)
        sys.exit(code)


class IOperation:

    def __init__(self,file):
        self.file = file

    def openFile(self):
        global op
        try:
            op = open(self.file, "r")
        except:
            Error.exitInrerpret(Error.invalidFile,"Wrong input file")
        return  op


    def closeFile(self,op):
        op.close()

class XmlOperation:

    def __init__(self,xmlFile):
        self.xmlFile = xmlFile

    def readXml(self):
        retVal = ""
        for line in self.xmlFile:
            retVal += line
        try:
            retVal= ET.fromstring(retVal)
        except:
            sys.exit("XML is not well formed")
        if not(retVal.tag =="program"):
            sys.exit("Invalid XML file")
        return retVal

    def getAttrib(self, string,pos):
        return (string[pos].attrib)


class Instruction:

    @classmethod
    def getAttribCount(cls, instr):
        count = 0
        for line in instr:
            count += 1
        return count

    @classmethod
    def getAttribVal(cls, instr, argNumber):
        return (instr[argNumber].text)

    @classmethod
    def getAttrib(cls, instr, number):
        retVal = []
        for arg in instr:
            retVal.append(arg.attrib["type"])
        return retVal[number]

    @classmethod
    def removeEoL(cls, instr):
        reTval = instr.split("\n")
        return reTval[0]

    @classmethod
    def getInstrName(cls,instr):
        return (instr.attrib["opcode"])

    @classmethod
    def checkIfType(cls, type):
        if not(type == "int" or type == "string" or type == "bool"):
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

    @classmethod
    def regexVarLabel(cls, input):
        if not re.search("[\w_\-$&%*][\w\d_\-$&%*]*$",input):   # REgex funguje dost divne, jakoze je napsany spravne, ale python si dela co chce
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")


    @classmethod
    def checkVariable(cls, var):
        var = var.split("@")
        if(var[0] != "GF" and var[0] != "TF" and var[0] != "LF"):
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

        cls.regexVarLabel(var[1])

    @classmethod
    def checkConst(cls, const, number):
        inputConst = cls.getAttrib(const,number)
        ConstValue = cls.getAttribVal(const,number)
        if(inputConst == "string"):
            pass
        elif(inputConst == "int"):
            if not(ConstValue.isnumeric()):
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
        elif(inputConst == "bool"):
            if not (ConstValue == "true" or ConstValue == "false"):
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
        elif(inputConst == "nil"):
            if not(ConstValue == "nil"):
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

    @classmethod
    def argCountCheck(cls, instr,  count):
        if(cls.getAttribCount(instr) != count):
            Error.exitInrerpret(Error.invalidXmlStruct, "invalid inout code")

    @classmethod
    def noArgInstruction(cls, instr):
         if not(cls.getAttribCount(instr) == 0):
              Error.exitInrerpret(Error.invalidXmlStruct,"Invalid input code")

    @classmethod
    def oneArgVarInstruction(cls, instr, count):
            variable = cls.getAttrib(instr,count)
            if(variable == "var"):
                varValue = cls.getAttribVal(instr, count)
                cls.checkVariable(varValue)
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

    @classmethod
    def oneArgLabelInstruction(cls,instr, count):
            label = cls.getAttrib(instr,count)
            if(label == "label"):
                labelVal = cls.getAttribVal(instr,count)
                cls.regexVarLabel(labelVal)
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
    @classmethod
    def oneArgSymbInstruction(cls, instr, count):
            if(cls.getAttrib(instr,count) == "var"):
                varValue = cls.getAttribVal(instr,count)
                cls.checkVariable(varValue)
            else:
                cls.checkConst(instr,count)

    @classmethod
    def oneArgTypeInstruction(cls, instr, count):
        if(cls.getAttrib(instr,count) == "type"):
            typeValue = cls.getAttrib(instr,count)
            cls.checkIfType(typeValue)
        else:
            Error.exitInrerpret(Error.invalidXmlStruct,"invalid input code")

    @classmethod
    def twoArgVarSymbInstruction(cls, instr):
        if(cls.getAttribCount(instr) == 2):
            firstArg = cls.getAttrib(instr,0)
            secondArg =cls.getAttrib(instr,1)
            if(firstArg == "var"):
                firstArgVal = cls.getAttribVal(instr,0)
                cls.checkVariable(firstArgVal)
                if(secondArg == "var"):
                    secondArgVal = cls.getAttribVal(instr,1)
                    cls.checkVariable(secondArgVal)
                else:
                    cls.checkConst(instr,1)
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

    @classmethod
    def twoArgVarTypeInstruction(cls, instr):
        if(cls.getAttribCount(instr) == 2):
            firstArg = cls.getAttrib(instr,0)
            secondArg = cls.getAttrib(instr,1)
            if(firstArg == "var"):
                firstArg = cls.getAttribVal(instr,0)
                cls.checkVariable(firstArg)
                if(secondArg == "type"):
                    secondArg = cls.getAttribVal(instr,1)
                    cls.checkIfType(secondArg)
                else:
                    Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

    @classmethod
    def threeArgInstruction(cls, instr):
        if(cls.getAttribCount(instr) == 3):
            firstArg = cls.getAttrib(instr,0)
            secondArg = cls.getAttrib(instr,1)
            thirdArg = cls.getAttrib(instr,2)
            if(firstArg == "var"):
                firstArg = cls.getAttribVal(instr,0)
                cls.checkVariable(instr)

            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")


class Parser:

    @staticmethod
    def parser(instruction):
        instrName = Instruction.getInstrName(instruction).upper()
        if(instrName == "CREATEFRAME"):
            Instruction.argCountCheck(instruction,0)
            Instruction.noArgInstruction(instruction)
        elif (instrName == "PUSHFRAME"):
            Instruction.argCountCheck(instruction, 0)
            Instruction.noArgInstruction(instruction)
        elif (instrName == "POPFRAME"):
            Instruction.argCountCheck(instruction, 0)
            Instruction.noArgInstruction(instruction)
        elif (instrName == "RETURN"):
            Instruction.argCountCheck(instruction, 0)
            Instruction.noArgInstruction(instruction)
        elif (instrName == "BREAK"):
            Instruction.argCountCheck(instruction, 0)
            Instruction.noArgInstruction(instruction)
            # ---------------- 1 ARGUMENT -------------------------
        elif (instrName == "DEFVAR"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgVarInstruction(instruction,0)
        elif (instrName == "CALL"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgLabelInstruction(instruction,0)
        elif (instrName == "PUSHS"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgSymbInstruction(instruction,0)
        elif (instrName == "POPS"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgVarInstruction(instruction,0)
        elif (instrName == "WRITE"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgSymbInstruction(instruction,0)
        elif (instrName == "LABEL"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgLabelInstruction(instruction,0)
        elif (instrName == "JUMP"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgLabelInstruction(instruction,0)
        elif (instrName == "EXIT"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgSymbInstruction(instruction,0)
        elif (instrName == "DPRINT"):
            Instruction.argCountCheck(instruction, 1)
            Instruction.oneArgSymbInstruction(instruction,0)
            # ---------------- 2 ARGUMENTY -------------------------
        elif (instrName == "MOVE"):
            Instruction.argCountCheck(instruction, 2)
            Instruction.oneArgVarInstruction(instruction,0)
            Instruction.oneArgSymbInstruction(instruction,1)
        elif (instrName == "INT2CHAR"):
            Instruction.argCountCheck(instruction, 2)
            Instruction.oneArgVarInstruction(instruction, 0)
            Instruction.oneArgSymbInstruction(instruction, 1)
        elif (instrName == "READ"):
            Instruction.argCountCheck(instruction,2)
            Instruction.oneArgVarInstruction(instruction,0)
            Instruction.oneArgTypeInstruction(instruction,1)
        elif (instrName == "STRLEN"):
            Instruction.argCountCheck(instruction, 2)
            Instruction.oneArgVarInstruction(instruction, 0)
            Instruction.oneArgSymbInstruction(instruction, 1)
        elif (instrName == "TYPE"):
            Instruction.argCountCheck(instruction, 2)
            Instruction.oneArgVarInstruction(instruction, 0)
            Instruction.oneArgSymbInstruction(instruction, 1)
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Wrong instruction")



