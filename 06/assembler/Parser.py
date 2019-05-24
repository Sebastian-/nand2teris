class Parser:
  def __init__(self, file):
    self.commands = []
    with open(file) as asm:
      for line in asm:
        # ignore empty lines and comments
        if line.strip() and not line.strip().startswith('//'):
          line = line.split('//')[0].strip()
          self.commands.append(line)
    self.currentCommand = None
    self.commandIndex = -1


  def hasMoreCommands(self):
    return (self.commandIndex == -1 and len(self.commands) > 0) \
      or (self.commandIndex + 1 < len(self.commands))
  

  def advance(self):
    self.commandIndex += 1
    self.currentCommand = self.commands[self.commandIndex]
  

  def commandType(self):
    if self.currentCommand.startswith('@'):
      return 'A_COMMAND'
    elif self.currentCommand.startswith('('):
      return 'L_COMMAND'
    else:
      return 'C_COMMAND'
  

  def symbol(self):
    if '@' in self.currentCommand:
      return self.currentCommand.lstrip('@')
    else:
      return self.currentCommand[1:-1]


  def dest(self):
    if not '=' in self.currentCommand:
      return None
    else:
      end = self.currentCommand.find('=')
      return self.currentCommand[:end]


  def comp(self):
    start = 0
    end = len(self.currentCommand)
    if '=' in self.currentCommand:
      start = self.currentCommand.find('=') + 1
    if ';' in self.currentCommand:
      end = self.currentCommand.find(';')
    
    return self.currentCommand[start:end]
  

  def jump(self):
    if not ';' in self.currentCommand:
      return None
    else:
      start = self.currentCommand.find(';') + 1
      return self.currentCommand[start:]

# Tests
if __name__ == "__main__":
    import sys
    parser = Parser(sys.argv[1])
    while parser.hasMoreCommands():
      parser.advance()
      print(parser.currentCommand)
      print(parser.commandType())
      if parser.commandType() == 'A_COMMAND' or parser.commandType() == 'L_COMMAND':
        print(parser.symbol())
      else:
        print(parser.dest(), parser.comp(), parser.jump())