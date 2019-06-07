import sys

from Parser import Parser
from CInstrTranslator import CInstrTranslator
from SymbolTable import SymbolTable


class HackAssember:
  def __init__(self):
    self.symbolTable = SymbolTable()
    self.symbolTable.addEntry('SP', 0)
    self.symbolTable.addEntry('LCL', 1)
    self.symbolTable.addEntry('ARG', 2)
    self.symbolTable.addEntry('THIS', 3)
    self.symbolTable.addEntry('THAT', 4)
    self.symbolTable.addEntry('SCREEN', 16384)
    self.symbolTable.addEntry('KBD', 24576)
    for i in range(16):
      self.symbolTable.addEntry('R' + str(i), i)


  def firstPass(self, asmFile):
    '''Populates symbol table with label addresses'''
    parser = Parser(asmFile)
    instructionAddress = 0
    
    while parser.hasMoreCommands():
      parser.advance()
      if parser.commandType() == 'L_COMMAND':
        self.symbolTable.addEntry(parser.symbol(), instructionAddress)
      else:
        instructionAddress += 1
  

  def assembleACommand(self, symbol, freeMemoryAddress):
    '''Assembles A commands (eg. @1234, @R0, or @index) into hack binary
       Returns the binary command and a boolean indicating whether a new
       symbol was added to the symbol table'''
    aCommandFormat = '0>16b'

    if symbol[0].isnumeric():
      # eg. @1234
      return format(int(symbol), aCommandFormat), False
    elif self.symbolTable.contains(symbol):
      # eg. @R0
      return format(int(self.symbolTable.getAddress(symbol)), aCommandFormat), False
    else:
      # add new symbol to table
      self.symbolTable.addEntry(symbol, freeMemoryAddress)
      return format(freeMemoryAddress, aCommandFormat), True


  def assembleCCommand(self, comp, dest, jump):
    binaryCommand = '111'
    binaryCommand += CInstrTranslator.translateComp(comp)
    binaryCommand += CInstrTranslator.translateDest(dest)
    binaryCommand += CInstrTranslator.translateJump(jump)
    return binaryCommand



  def assemble(self, asmFile):
    self.firstPass(asmFile)
    hackFilename = asmFile[:-4] + '.hack'
    parser = Parser(asmFile)
    freeMemoryAddress = 16

    with open(hackFilename, 'w') as hackBinary:
      while parser.hasMoreCommands():
        parser.advance()

        if parser.commandType() == 'A_COMMAND':
          binaryACommand, allocatedMemory = self.assembleACommand(parser.symbol(), freeMemoryAddress)
          hackBinary.write(binaryACommand + '\n')
          if allocatedMemory:
            freeMemoryAddress += 1
          
        if parser.commandType() == 'C_COMMAND':
          binaryCCommand = self.assembleCCommand(parser.comp(), parser.dest(), parser.jump())
          hackBinary.write(binaryCCommand + '\n')


if __name__ == "__main__":
  asmFile = sys.argv[1]
  assembler = HackAssember()
  assembler.assemble(asmFile)

