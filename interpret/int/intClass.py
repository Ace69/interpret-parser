import sys
import xml.etree.ElementTree as ET


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
        sys.stderr(msg)
        sys.exit(code)


class Switch:
    @staticmethod
    def switch(instrName):
        if(instrName == "CREATEFRAME"):
            print("CREATEFRAME")
        if(instrName == "PUSHFRAME"):
            print("PUSHFRAME")
        if (instrName == "POPFRAME"):
            print("POPFRAME")
        if (instrName == "RETURN"):
            print("RETURN")
        if (instrName == "BREAK"):
            print("BREAK")

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
    def __init__(self, instr):
        self.instr = instr
        self.opcode = instr.attrib

    def getInstr(self):
        print(self.opcode)

    def getAttrib(self, arg):
        print(arg.attrib)

    def getInstrName(self,instr):
        return (instr.attrib["opcode"])

class Parser:
    def createframe(self):
        pass