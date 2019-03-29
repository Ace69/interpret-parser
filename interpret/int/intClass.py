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
    def noArgInstruction(cls, instr):
         if not(cls.getAttribCount(instr) == 0):
              Error.exitInrerpret(Error.invalidXmlStruct,"Invalid input code")

    @classmethod
    def oneArgVarInstruction(cls, instr):
        if(cls.getAttribCount(instr) == 1):
            variable = cls.getAttrib(instr,0)
            if(variable == "var"):
                varValue = cls.getAttribVal(instr, 0)
                cls.checkVariable(varValue)
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")


    @classmethod
    def oneArgLabelInstruction(cls,instr):
        if(cls.getAttribCount(instr) == 1):
            label = cls.getAttrib(instr,0)
            if(label[0] == "label"):
                labelVal = cls.getAttribVal(instr,0)
                cls.regexVarLabel(labelVal)
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

    @classmethod
    def oneArgSymbInstruction(cls, instr):
        if(cls.getAttribCount(instr) == 1):
            if(cls.getAttrib(instr,0) == "var"):
                varValue = cls.getAttribVal(instr,0)
                cls.checkVariable(varValue)
            else:
                cls.checkConst(instr,0)
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")

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

class Parser:

    @staticmethod
    def parser(instruction):
        instrName = Instruction.getInstrName(instruction).upper()
        if(instrName == "CREATEFRAME"):
            Instruction.noArgInstruction(instruction)
        elif (instrName == "PUSHFRAME"):
            Instruction.noArgInstruction(instruction)
        elif (instrName == "POPFRAME"):
            Instruction.noArgInstruction(instruction)
        elif (instrName == "RETURN"):
            Instruction.noArgInstruction(instruction)
        elif (instrName == "BREAK"):
            Instruction.noArgInstruction(instruction)
            # ---------------- 1 ARGUMENT -------------------------
        elif (instrName == "DEFVAR"):
            Instruction.oneArgVarInstruction(instruction)
        elif (instrName == "CALL"):
            Instruction.oneArgLabelInstruction(instruction)
        elif (instrName == "PUSHS"):
            Instruction.oneArgSymbInstruction(instruction)
        elif (instrName == "POPS"):
            Instruction.oneArgVarInstruction(instruction)
        elif (instrName == "WRITE"):
            Instruction.oneArgSymbInstruction(instruction)
        elif (instrName == "LABEL"):
            Instruction.oneArgLabelInstruction(instruction)
        elif (instrName == "JUMP"):
            Instruction.oneArgLabelInstruction(instruction)
        elif (instrName == "EXIT"):
            Instruction.oneArgSymbInstruction(instruction)
        elif (instrName == "DPRINT"):
            Instruction.oneArgSymbInstruction(instruction)
            # ---------------- 2 ARGUMENTY -------------------------
        elif (instrName == "MOVE"):
            Instruction.twoArgVarSymbInstruction(instruction)
        elif (instrName == "INT2CHAR"):
            Instruction.twoArgVarSymbInstruction(instruction)
        elif (instrName == "READ"):
            Instruction.twoArgVarTypeInstruction(instruction)
        elif (instrName == "STRLEN"):
            Instruction.twoArgVarSymbInstruction(instruction)
        elif (instrName == "TYPE"):
            Instruction.twoArgVarSymbInstruction(instruction)

        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Wrong instruction")



