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
            instruction = Instruction(instr)
            instruction.getInstr()
            Switch.switch(instruction.getInstrName(instr))


            for arg in instr:
                instruction.getAttrib(arg)
            print("---------------------------\n")

    print("GF:", GF)
    print("TF:", TF)
    print("LF:", LF)

main()
