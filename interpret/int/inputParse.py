import sys
import xml.etree.ElementTree as ET
import os




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

class ArgumentParse:

    @classmethod
    def fileExist(cls, file):
        if not (os.path.isfile(file)):
            Error.exitInrerpret(Error.invalidFile, "Invalid input file")

    @classmethod
    def checkOneArg(cls, argv):
        first = argv[1]
        if first[:9] == "--source=":
            file = first[9:]
            cls.fileExist(file)
            return True, file, None
        elif first[:8] == "--input=":
            file = first[8:]
            cls.fileExist(file)
            return False, file, None
        else:
            Error.exitInrerpret(Error.invalidFile, "Invalid input file")

    @classmethod
    def checkTwoArg(cls, argv):
        first = argv[1]
        second = argv[2]
        file = first[9:]
        file2 = second[8:]
        if first[:9] == "--source=" and second[:8]== "--input=":
            cls.fileExist(file)
            cls.fileExist(file2)
            return True,file, file2
        elif first[:8] == "--input=" and second[:9]== "--source=":
            cls.fileExist(file)
            cls.fileExist(file2)
            return False, file2, file
        else:
            Error.exitInrerpret(Error.invalidFile, "pico\n") #TODO !!!

    @classmethod
    def checkHelp(cls, argv):
        if argv[1] == "--help" and len(argv) == 2:
            print("Program načte XML reprezentaci programu ze zadaného souboru a tento program s využitím standardního vstupu a výstupu interpretuje")
            sys.exit(0)

    @classmethod
    def readArg(cls, argv):
        if 1 < len(argv) <= 3:
            cls.checkHelp(argv)
            if len(argv) == 2:
                return cls.checkOneArg(argv)
            elif len(argv) == 3:
                return cls.checkTwoArg(argv)
            else:
                Error.exitInrerpret(Error.invalidFile, "Invalid input file")
        else:
            Error.exitInrerpret(Error.invalidFile, "Invalid input file")

    @classmethod
    def chooseInput(cls, file):
        inputRead = ""
        if (file[2] == None):  # Byl zadan pouze jeden argument
            if (file[0] == True):  # Byl zadan --source=file
                sourceRead = open(file[1])
                inputRead = sys.stdin
            else:  # Byl zadan parametr --input=file
                sourceRead = sys.stdin
                inputRead = open(file[1])
        else:
            if (file[0] == True):  # prvni je parametr --source
                sourceRead = open(file[1])
                inputRead = open(file[2])
            else:                   # druhy parametr --input
                sourceRead = open(file[2])
                inputRead = open(file[1])

        return sourceRead, inputRead
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


    @staticmethod
    def closeFile(op):
        op.close()



class XmlOperation:

    def __init__(self,xmlFile):
        self.xmlFile = xmlFile

    def sortChildrenBy(parent, attr):
        parent[:] = sorted(parent, key=lambda child: child.get(attr))


    def readXml(self):
        retVal = ""
        for line in self.xmlFile:
            retVal += line
        try:
            retVal= ET.fromstring(retVal)
        except:
            Error.exitInrerpret(Error.noWellFormedXml, "Xml is no well formed")
        if not(retVal.tag =="program"):
            Error.exitInrerpret(Error.noWellFormedXml, "Xml is no well formed")
        return retVal

    def getTag(self):
        return self.xmlFile.getroot()