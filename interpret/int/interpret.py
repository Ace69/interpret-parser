from intClass import *

GF = dict()
TF = {}
LF = []


def main():

    sourceFile = IOperation('input.src')
    fh =sourceFile.openFile()


    xmlInput = XmlOperation(fh) # instance
    string = xmlInput.readXml() # naparsovany xml string


     #loop na vsechny instrukce
    for instr in string:
            Parser.parser(instr)



    print("GF:", GF)
    print("TF:", TF)
    print("LF:", LF)
    print("Lex/syntax OK")

main()
