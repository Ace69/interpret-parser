import sys
import xml.etree.ElementTree as ET
import re

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


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
            Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")

    @classmethod
    def regexVarLabel(cls, input):
        if not re.search("[\w_\-$&%*][\w\d_\-$&%*]*$",input):   # REgex funguje dost divne, jakoze je napsany spravne, ale python si dela co chce
            Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")


    @classmethod
    def checkVariable(cls, var):
        var = var.split("@")
        if(var[0] != "GF" and var[0] != "TF" and var[0] != "LF"):
            Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")

        cls.regexVarLabel(var[1])

    @classmethod
    def checkConst(cls, const, number):
        inputConst = cls.getAttrib(const,number)
        ConstValue = cls.getAttribVal(const,number)
        if(inputConst == "string"):
            pass
        elif(inputConst == "int"):
            if not(ConstValue.isnumeric()):
                Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")
        elif(inputConst == "bool"):
            if not (ConstValue == "true" or ConstValue == "false"):
                Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")
        elif(inputConst == "nil"):
            if not(ConstValue == "nil"):
                Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")
        else:
            Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")

    @classmethod
    def argCountCheck(cls, instr,  count):
        if(cls.getAttribCount(instr) != count):
            Error.exitInrerpret(Error.invalidXmlStruct, "invalid inout code")

    @classmethod
    def noArgInstruction(cls, instr):
         if not(cls.getAttribCount(instr) == 0):
              Error.exitInrerpret(Error.invalidXmlStruct,"Lexical or syntax error")

    @classmethod
    def argVarInstruction(cls, instr, count):
            variable = cls.getAttrib(instr,count)
            if(variable == "var"):
                varValue = cls.getAttribVal(instr, count)
                cls.checkVariable(varValue)
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")

    @classmethod
    def argLabelInstruction(cls, instr, count):
            label = cls.getAttrib(instr,count)
            if(label == "label"):
                labelVal = cls.getAttribVal(instr,count)
                cls.regexVarLabel(labelVal)
            else:
                Error.exitInrerpret(Error.invalidXmlStruct, "Lexical or syntax error")
    @classmethod
    def argSymbInstruction(cls, instr, count):
            if(cls.getAttrib(instr,count) == "var"):
                varValue = cls.getAttribVal(instr,count)
                cls.checkVariable(varValue)
            else:
                cls.checkConst(instr,count)

    @classmethod
    def argTypeInstruction(cls, instr, count):
        if(cls.getAttrib(instr,count) == "type"):
            typeValue = cls.getAttrib(instr,count)
            cls.checkIfType(typeValue)
        else:
            Error.exitInrerpret(Error.invalidXmlStruct,"Lexical or syntax error")


