from pprint import pprint
from string import Template
from decoderGenerator import getDecodeTree, getSwitch

opCodes = {
    # "0NNN": ("/* Do nothing */", "RCA ${nNN}", []),
    "00E0": ("for(int xx=0; xx<CHIP8_SCREEN_WIDTH; xx++) "
                "for(int yy=0; yy<CHIP8_SCREEN_HEIGHT; yy++) "
                    "pixels[xx + yy * CHIP8_SCREEN_HEIGHT] = 0xFF << 24; "
                    "updateScreen = 1;", "CLR", []),
    "00EE": ("pc = stack[sp--];", "RET", ["pc"]),
    "1NNN": ("pc = op.nNN;", "JP ${nNN}", ["pc"]),
    "2NNN": ("stack[++sp] = pc; pc = op.nNN;", "CALL ${nNN}", ["pc"]),
    "3XNN": ("if(*x == op.nN) "
                "pc += 2;", "SE V${vX}, ${nN}", ["vX", "pc"]),
    "4XNN": ("if(*x != op.nN) "
                "pc += 2;", "SNE V${vX}, ${nN}", ["vX", "pc"]),
    "5XY0": ("if(*x == *y) "
                "pc += 2;", "SE V${vX}, V${vY}", ["vX", "vY", "pc"]),
    "6XNN": ("*x = op.nN;", "MOV V${vX}, ${nN}", ["vX"]),
    "7XNN": ("*x += op.nN;", "ADD V${vX}, ${nN}", ["vX"]),
    "8XY0": ("*x = *y;", "MOV V${vX}, V${vY}", ["vX", "vY"]),
    "8XY1": ("*x |= *y;", "OR V${vX}, V${vY}", ["vX", "vY"]),
    "8XY2": ("*x &= *y;", "AND V${vX}, V${vY}", ["vX", "vY"]),
    "8XY3": ("*x ^= *y;", "XOR V${vX}, V${vY}", ["vX", "vY"]),
    "8XY4": ("{uint16 p = *x + *y; "
            "reg[0xF] = p >> 8;"
            "*x = p;}", "ADD V${vX}, V${vY}", ["vX", "vY", "vF"]),
    "8XY5": ("reg[0xF] = (*x >= *y) ? 1 : 0;"
            "*x -= *y;", "SUB V${vX}, V${vY}", ["vX", "vY", "vF"]),
    "8XY6": ("reg[0xF] = 0x1 & *x;"
            "*x >>= 1;", "RSH V${vX}", ["vX", "vY", "vF"]),
    "8XY7": ("reg[0xF] = (*x <= *y) ? 1 : 0; "
            "*x = *y - *x;", "RSUB V${vX}, V${vY}", ["vX", "vY", "vF"]),
    "8XYE": ("reg[0xF] = *x >> 7; *x <<= 1;", "LSH ${vX}", ["vX", "vY", "vF"]),
    "9XY0": ("if(*x != *y) pc += 2;", "SNE V${vX}, V${vY}", ["vX", "vY", "pc"]),
    "ANNN": ("I = op.nNN;", "MOV I, ${nNN}", ["I"]),
    "BNNN": ("pc = reg[0] + op.nNN;", "B V${vX}, ${nNN}", ["vX", "pc"]),
    "CXNN": ("*x = rand() & op.nN;", "RAND V${vX}, ${nN}", ["vX"]),
    "DXYN": ("opDraw(op);", "DRW V${vX}, V${vY}, ${n}", ["vX", "vY", "I"]),
    "EX9E": ("if(  (0x8000 >> *x) & keyboard.keys)  pc += 2;", "SKP V${vX}", ["vX", "keys"]),
    "EXA1": ("if(!((0x8000 >> *x) & keyboard.keys)) pc += 2;", "SKNP V${vX}", ["vX", "keys"]),
    "FX07": ("*x = dT;", "MOV V${vX}, DT", ["vX", "dT"]),
    "FX0A": ("waitingForInput = 1; waitingInputReg = op.vX;", "WAIT V${vX}", ["vX"]),
    "FX15": ("dT = *x;", "MOV DT, V${vX}", ["vX", "dT"]),
    "FX18": ("sT = *x;", "MOV ST, V${vX}", ["vX", "sT"]),
    "FX1E": ("I += *x;", "ADD I, V${vX}", ["vX", "I"]),
    "FX29": ("I = (*x)*FONT_HEIGHT + FONT_OFFSET;", "MOV F, V${vX}", ["vX", "I"]),
    "FX33": ("ram[I]   =  *x / 100; "
            "ram[I+1] = (*x % 100) / 10; " 
            "ram[I+2] =  *x % 10;", "BCD V${vX}", ["vX", "BCD"]),
    "FX55": ("for (int j=0; j<=op.vX; j++) "
                "ram[I++] = reg[j];", "PUSH V${vX}", ["vX", "regUpToVX", "ramUpToVX"]),
    "FX65": ("for (int j=0; j<=op.vX; j++) "
                "reg[j] = ram[I++];", "POP V${vX}", ["vX", "regUpToVX", "ramUpToVX"]),
}

branches = set("0123456789ABCDEF")
wildCard = "XYN"
ignore = ""

def genCode(tree):
    return opCodes[tree][0]

decodeTree = getDecodeTree(opCodes.keys(), wildCard, ignore)
print getSwitch(genCode, "/*Default*/", decodeTree, 0, base=16)
