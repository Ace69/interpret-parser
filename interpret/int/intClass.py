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
    def checkSymbol(cls, symb):
        if(symb[:3] == "GF@" or symb[:3] == "TF@" or symb[:3] == "LF@"):
            print("variable")
        else:
            print("konstanta")

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
    def getAttrib(cls, instr):
        retVal = ""
        for arg in instr:
            retVal += arg.attrib["type"]
        return retVal


    @classmethod
    def getInstrName(cls,instr):
        return (instr.attrib["opcode"])

    @classmethod
    def noArgInstruction(cls, instr):
         if not(cls.getAttribCount(instr) == 0):
              Error.exitInrerpret(Error.invalidXmlStruct,"Invalid input code")

    @classmethod
    def oneArgVarInstruction(cls, instr):
        if(cls.getAttribCount(instr) == 1):
            if((cls.getAttrib(instr)) == "var"):
                varValue = cls.getAttribVal(instr, 0)
                cls.checkVariable(varValue)
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Invalid input code")


    @classmethod
    def oneArgLabelInstruction(cls,instr):
        if(cls.getAttribCount(instr) == 1):
            if(cls.getAttrib(instr) == "label"):
                labelVal = cls.getAttribVal(instr,0)
                cls.regexVarLabel(labelVal)
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
        elif (instrName == "DEFVAR"):
            Instruction.oneArgVarInstruction(instruction)
        elif (instrName == "CALL"):
            Instruction.oneArgLabelInstruction(instruction)
        elif (instrName == "PUSHS"):
            Instruction.oneArgVarInstruction(instruction)
        elif (instrName == "POPS"):
            Instruction.oneArgVarInstruction(instruction)
        elif (instrName == "WRITE"):
            Instruction.oneArgVarInstruction(instruction)
        elif (instrName == "LABEL"):
            Instruction.oneArgLabelInstruction(instruction)
        elif (instrName == "JUMP"):
            Instruction.oneArgVarInstruction(instruction)
        elif (instrName == "EXIT"):
            Instruction.oneArgVarInstruction(instruction)
        elif (instrName == "DPRINT"):
            Instruction.oneArgVarInstruction(instruction)
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Wrong instruction")



