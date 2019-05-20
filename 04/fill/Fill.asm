// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.


@isScreenFilled
M=0

(INFLOOP)
  // reset screen address offset
  @i
  M=0

  // check if key is pressed
  @KBD
  D=M
  @KEYPRESSED
  D;JGT
  @KEYNOTPRESSED
  0;JMP

  // fill screen if it's not already filled
  (KEYPRESSED)
    @isScreenFilled
    D=M
    @INFLOOP
    D;JGT
    @FILLSCREEN
    0;JMP
  
  // clear screen if it's not already cleared
  (KEYNOTPRESSED)
    @isScreenFilled
    D=M
    @CLEARSCREEN
    D;JGT
    @INFLOOP
    0;JMP

  (CLEARSCREEN)
    // bounds check for screen memory - total of 32 * 256 registers
    @8192
    D=A
    @i
    D=D-M
    @CLEARSCREENEND
    D;JLE

    // clear register
    @SCREEN
    D=A
    @i
    D=D+M
    A=D
    M=0

    // i++
    @i
    M=M+1
    @CLEARSCREEN
    0;JMP

  (CLEARSCREENEND)
    @isScreenFilled
    M=0
    @INFLOOP
    0;JMP
  
  (FILLSCREEN)
    // bounds check for screen memory - total of 32 * 256 registers
    @8192
    D=A
    @i
    D=D-M
    @FILLSCREENEND
    D;JLE

    // fill register
    @SCREEN
    D=A
    @i
    D=D+M
    A=D
    M=-1

    // i++
    @i
    M=M+1
    @FILLSCREEN
    0;JMP

  (FILLSCREENEND)
    @isScreenFilled
    M=1
    @INFLOOP
    0;JMP