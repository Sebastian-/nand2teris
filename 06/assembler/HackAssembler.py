from Parser import Parser
from CInstrTranslator import CInstrTranslator
import sys
import os

if __name__ == "__main__":
  asmFilename = sys.argv[1]
  hackFilename = asmFilename[:-4] + '.hack'
  parser = Parser(asmFilename)
  with open(hackFilename, 'w') as hackBinary:
    while parser.hasMoreCommands():
      parser.advance()
      
      binaryCommand = ''
      if parser.commandType() == 'A_COMMAND':
        binaryCommand += '0'
        binaryCommand += format(int(parser.symbol()), '0>15b')
      if parser.commandType() == 'C_COMMAND':
        binaryCommand += '111'
        binaryCommand += CInstrTranslator.translateComp(parser.comp())
        binaryCommand += CInstrTranslator.translateDest(parser.dest())
        binaryCommand += CInstrTranslator.translateJump(parser.jump())
      
      hackBinary.write(binaryCommand + '\n')
