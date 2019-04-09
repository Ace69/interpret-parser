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
            return file, True
        elif first[:8] == "--input=":
            file = first[8:]
            cls.fileExist(file)
            return file, False
        else:
            Error.exitInrerpret(Error.invalidFile, "Invalid input file")

    @classmethod
    def checkTwoArg(cls, argv):
        first = argv[1]
        second = argv[2]
        file = first[:9]
        file2 = second[:9]
        if first[:9] == "--source=" and second[:9]== "--input=":
            cls.fileExist(file)
            cls.fileExist(file2)
            return file, file2
        elif first[:9] == "--input=" and second[:9]== "--source=":
            cls.fileExist(file)
            cls.fileExist(file2)
            return file2, file
        else:
            Error.exitInrerpret(Error.invalidFile, "Invalid input file")

    @classmethod
    def checkHelp(cls, argv):
        if argv[1] == "--help" and len(argv) == 2:
            print("naaapoveda")
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