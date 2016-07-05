# opcode-decoder-generator
A tool for generating C code for decoding machine instructions. The input is a list of op codes and a function. The output is C code for decoding an instruction "op" and the output of the passed function with the op code definition as input. "op" is a union of structs which index substrings of bits.

The output is undefined for ambiguous op code definitions and invalid inputs to the generated code.

## Example
The inputs are list of a subset of the Z80 instruction set, and a function which returns a string which prints out the assembly instruction for a given op code pattern.

## Input
```python
opCodes = {
    "00000000": "NOP",
    "00001000": "LD N, SP",
    "00**0001": "LD (R), N",
    "00**1001": "ADD HL, (R)",
    "000*0010": "LD (R), A",
    "000*1010": "LD A, (R)",
    "00**0011": "INC (R)",
    "00**1011": "DEC (R)",
    "00***100": "INC (D)",
    "00***101": "DEC (D)",
    "00***110": "LD (D), N",
    "0000*111": "RdCA",
    "0001*111": "RdA",
    "00010000": "STOP",
    "00011000": "JR N",
    "001**000": "JR F, N",
    "00100010": "LDI HL, A",
    "00101010": "LDI A, HL",
    "00100010": "LDD HL, A",
    "00111010": "LDD A, HL",
    # ...
}

def getInstruction(key):
    return '''std::cout << "%s" << std::endl;''' % opCodes[key]

wildcard = "*"
ignore = ""

decodeTree = getDecodeTree(opCodes.keys(), wildcard, ignore)
print getSwitch(getInstruction, "/*Default*/", decodeTree, 0)
```

### Output
```C++
switch (op.digit5_7) {
case 0x0: switch (op.digit0_2) {
	case 0x0: switch (op.digit3_4) {
		case 0x0: std::cout << "NOP" << std::endl; break;
		case 0x1: std::cout << "LD N, SP" << std::endl; break;
		case 0x2: std::cout << "STOP" << std::endl; break;
		case 0x3: std::cout << "JR N" << std::endl; break;
		default: /*Default*/ break;
		} break;
	case 0x1: std::cout << "JR F, N" << std::endl; break;
	default: /*Default*/ break;
	} break;
case 0x1: switch (op.digit0_1) {
	case 0x0: switch (op.digit4_4) {
		case 0x0: std::cout << "LD (R), N" << std::endl; break;
		case 0x1: std::cout << "ADD HL, (R)" << std::endl; break;
		default: /*Default*/ break;
		} break;
	default: /*Default*/ break;
	} break;
case 0x2: switch (op.digit0_2) {
	case 0x0: switch (op.digit4_4) {
		case 0x0: std::cout << "LD (R), A" << std::endl; break;
		case 0x1: std::cout << "LD A, (R)" << std::endl; break;
		default: /*Default*/ break;
		} break;
	case 0x1: switch (op.digit3_4) {
		case 0x0: std::cout << "LDD HL, A" << std::endl; break;
		case 0x1: std::cout << "LDI A, HL" << std::endl; break;
		case 0x3: std::cout << "LDD A, HL" << std::endl; break;
		default: /*Default*/ break;
		} break;
	default: /*Default*/ break;
	} break;
case 0x3: switch (op.digit0_1) {
	case 0x0: switch (op.digit4_4) {
		case 0x0: std::cout << "INC (R)" << std::endl; break;
		case 0x1: std::cout << "DEC (R)" << std::endl; break;
		default: /*Default*/ break;
		} break;
	default: /*Default*/ break;
	} break;
case 0x4: std::cout << "INC (D)" << std::endl; break;
case 0x5: std::cout << "DEC (D)" << std::endl; break;
case 0x6: std::cout << "LD (D), N" << std::endl; break;
case 0x7: switch (op.digit0_3) {
	case 0x0: std::cout << "RdCA" << std::endl; break;
	case 0x1: std::cout << "RdA" << std::endl; break;
	default: /*Default*/ break;
	} break;
default: /*Default*/ break;
}
```

## How It Works
The list of op codes is recursively partitioned based on the longest substring of non-wildcard characters. The example above has the following intermediate form:
```python
decodeTree = \
{'*****000': {'000*****': {'***00***': '00000000',
                           '***01***': '00001000',
                           '***10***': '00010000',
                           '***11***': '00011000'},
              '001*****': '001**000'},
 '*****001': {'00******': {'****0***': '00**0001', '****1***': '00**1001'}},
 '*****010': {'000*****': {'****0***': '000*0010', '****1***': '000*1010'},
              '001*****': {'***00***': '00100010',
                           '***01***': '00101010',
                           '***11***': '00111010'}},
 '*****011': {'00******': {'****0***': '00**0011', '****1***': '00**1011'}},
 '*****100': '00***100',
 '*****101': '00***101',
 '*****110': '00***110',
 '*****111': {'0000****': '0000*111', '0001****': '0001*111'}}
```

Each key of the nested dictionaries represents portions of the patterns found in the value of its leaves.

As an example:
```python
decodeTree['*****001']\
          ['00******']\
          ['****1***'] =
            00**1001
```

## Issues:
The following list of op codes cannot currently be handled, but is not ambiguous:

```python
opCodes = [
    "*1111", #00111, 10111
    "1*011", #10011, 11011
    "11*01", #11001, 11101
    "111*0", #11100, 11110
    "1010*", #10100, 10101
]
```

This issue results from the algorithm requiring that for each subset of the list there exists an index such that the union of the characters at the index of each element has a size greater than 1, and does not have a wildcard character.
