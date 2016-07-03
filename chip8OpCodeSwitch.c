switch (op.digit0_0) {
case 0x0: switch (op.digit1_3) {
	case 0xE0: for(int xx=0; xx<CHIP8_SCREEN_WIDTH; xx++) for(int yy=0; yy<CHIP8_SCREEN_HEIGHT; yy++) pixels[xx + yy * CHIP8_SCREEN_HEIGHT] = 0xFF << 24; updateScreen = 1; break;
	case 0xEE: pc = stack[sp--]; break;
	default: /*Default*/ break;
	} break;
case 0x1: pc = op.nNN; break;
case 0x2: stack[++sp] = pc; pc = op.nNN; break;
case 0x3: if(*x == op.nN) pc += 2; break;
case 0x4: if(*x != op.nN) pc += 2; break;
case 0x5: if(*x == *y) pc += 2; break;
case 0x6: *x = op.nN; break;
case 0x7: *x += op.nN; break;
case 0x8: switch (op.digit3_3) {
	case 0x0: *x = *y; break;
	case 0x1: *x |= *y; break;
	case 0x2: *x &= *y; break;
	case 0x3: *x ^= *y; break;
	case 0x4: {uint16 p = *x + *y; reg[0xF] = p >> 8;*x = p;} break;
	case 0x5: reg[0xF] = (*x >= *y) ? 1 : 0;*x -= *y; break;
	case 0x6: reg[0xF] = 0x1 & *x;*x >>= 1; break;
	case 0x7: reg[0xF] = (*x <= *y) ? 1 : 0; *x = *y - *x; break;
	case 0xE: reg[0xF] = *x >> 7; *x <<= 1; break;
	default: /*Default*/ break;
	} break;
case 0x9: if(*x != *y) pc += 2; break;
case 0xA: I = op.nNN; break;
case 0xB: pc = reg[0] + op.nNN; break;
case 0xC: *x = rand() & op.nN; break;
case 0xD: opDraw(op); break;
case 0xE: switch (op.digit2_3) {
	case 0x9E: if(  (0x8000 >> *x) & keyboard.keys)  pc += 2; break;
	case 0xA1: if(!((0x8000 >> *x) & keyboard.keys)) pc += 2; break;
	default: /*Default*/ break;
	} break;
case 0xF: switch (op.digit2_3) {
	case 0x7: *x = dT; break;
	case 0xA: waitingForInput = 1; waitingInputReg = op.vX; break;
	case 0x15: dT = *x; break;
	case 0x18: sT = *x; break;
	case 0x1E: I += *x; break;
	case 0x29: I = (*x)*FONT_HEIGHT + FONT_OFFSET; break;
	case 0x33: ram[I]   =  *x / 100; ram[I+1] = (*x % 100) / 10; ram[I+2] =  *x % 10; break;
	case 0x55: for (int j=0; j<=op.vX; j++) ram[I++] = reg[j]; break;
	case 0x65: for (int j=0; j<=op.vX; j++) reg[j] = ram[I++]; break;
	default: /*Default*/ break;
	} break;
default: /*Default*/ break;
}
