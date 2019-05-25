import sys

from Parser import Parser
from CInstrTranslator import CInstrTranslator
from SymbolTable import SymbolTable


def initSymbolTable():
  '''Initializes a symbol table with predefined values'''
  table = SymbolTable()
  table.addEntry('SP', 0)
  table.addEntry('LCL', 1)
  table.addEntry('ARG', 2)
  table.addEntry('THIS', 3)
  table.addEntry('THAT', 4)
  table.addEntry('SCREEN', 16384)
  table.addEntry('KBD', 24576)
  for i in range(16):
    table.addEntry('R' + str(i), i)
  
  return table


def firstPass(file):
  '''Populates symbol table with label addresses'''
  parser = Parser(file)
  table = initSymbolTable()
  instructionAddress = 0
  
  while parser.hasMoreCommands():
    parser.advance()
    if parser.commandType() == 'L_COMMAND':
      table.addEntry(parser.symbol(), instructionAddress)
    else:
      instructionAddress += 1
  
  return table



if __name__ == "__main__":
  asmFilename = sys.argv[1]
  hackFilename = asmFilename[:-4] + '.hack'
  symbolTable = firstPass(asmFilename)
  parser = Parser(asmFilename)
  freeMemoryAddress = 16

  with open(hackFilename, 'w') as hackBinary:
    while parser.hasMoreCommands():
      parser.advance()

      if parser.commandType() == 'A_COMMAND':
        aCommandFormat = '0>16b'
        symbol = parser.symbol()
        if symbol[0].isnumeric():
          # @number
          hackBinary.write(format(int(symbol), aCommandFormat) + '\n')
        elif symbolTable.contains(symbol):
          # @label
          hackBinary.write(format(symbolTable.getAddress(symbol), aCommandFormat) + '\n')
        else:
          # @variable
          symbolTable.addEntry(symbol, freeMemoryAddress)
          hackBinary.write(format(freeMemoryAddress, aCommandFormat) + '\n')
          freeMemoryAddress += 1

      if parser.commandType() == 'C_COMMAND':
        binaryCommand = '111'
        binaryCommand += CInstrTranslator.translateComp(parser.comp())
        binaryCommand += CInstrTranslator.translateDest(parser.dest())
        binaryCommand += CInstrTranslator.translateJump(parser.jump())
        hackBinary.write(binaryCommand + '\n')

