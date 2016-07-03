from pprint import pprint
from string import Template
from decoderGenerator import getDecodeTree, getSwitch

opCodes = {
    "00 000000": ("", "NOP", []),
    "00 001000": ("", "LD ${N}, SP", []),
    "00 RR 0001": ("", "LD ${R}, ${N}", []),
    "00 RR 1001": ("", "ADD HL, ${R}", []),
    "00 0r 0 010": ("", "LD ${R}, A", []),
    "00 0r 1 010": ("", "LD A, ${R}", []),
    "00 RR 0 011": ("", "INC ${R}", []),
    "00 RR 1 011": ("", "DEC ${R}", []),
    "00 DDD 10 0": ("", "INC ${D}", []),
    "00 DDD 10 1": ("", "DEC ${D}", []),
    "00 DDD 110": ("", "LD ${D}, ${N}", []),
    "00 00 d 111": ("", "RdCA", []),
    "00 01 d 111": ("", "RdA", []),
    "00 010000": ("", "STOP", []),
    "00 011 000": ("", "JR ${N}", []),
    "00 1FF 000": ("", "JR ${F}, ${N}", []),
    "00 100 010": ("", "LDI HL, A", []),
    "00 101 010": ("", "LDI A, HL", []),
    "00 100 010": ("", "LDD HL, A", []),
    "00 111 010": ("", "LDD A, HL", []),

    "00 100111": ("", "DAA", []),
    "00 101111": ("", "CPL", []),
    "00 110111": ("", "SCF", []),
    "00 111111": ("", "CCF", []),

    "01 DDD DDD": ("", "LD ${D}, ${D2}", []),
    "01 110 110": ("", "HALT", []),

    "10 AAA DDD": ("", "${ALU} A, ${D2}", []),
    "11 AAA 110": ("", "${ALU} A, ${N}", []),

    "11 RR0 0 01": ("", "POP ${R}", []),
    "11 RR0 1 01": ("", "PUSH ${R}", []),

    "11 NNN 111": ("", "RST ${RST}", []),

    "110 FF 000": ("", "RET ${F}", []),
    "110 01001": ("", "RET", []),
    "110 11001": ("", "RETI", []),
    "110 FF 010": ("", "JP ${F}, ${N}", []),
    "110 00011": ("", "JP ${N}", []),
    "110 FF 100": ("", "CALL ${F}, ${N}", []),
    "110 01101": ("", "CALL ${N}", []),

    "111 01000": ("", "ADD SP, ${N}", []),
    "111 11000": ("", "LD HL, SP+${N}", []),

    "111 00000": ("", "LD FF00 + ${N}, A", []),
    "111 10000": ("", "LD A, FF00 + ${N}", []),

    "111 0 0010": ("", "LD C, A", []),
    "111 1 0010": ("", "LD A, C", []),
    "111 0 1010": ("", "LD ${N}, A", []),
    "111 1 1010": ("", "LD A, ${N}", []),

    "111 01001": ("", "JP HL", []), # Also known as "LD PC, HL"
    "111 11001": ("", "LD SP, HL", []),

    "111 10011": ("", "DI", []),
    "111 11011": ("", "EI", []),

    "1100 1011": ("", "MB", []), # Multiple byte command
}

branches = set("01")
wildcard = "XDFRArNd"
ignore = " ,"

def genDisassemble(tree):
    d = {
        "ALU": "ALU",
        "R": "R",
        "r": "r",
        "D": "D",
        "D2": "D",
        "F": "F",
        "N": "N",
        "RST": "RST",
    }
    return "std::cout << \"%s\" << std::endl;" % Template(opCodes[tree][1]).substitute(d)

decodeTree = getDecodeTree(opCodes, wildcard, ignore)
print getSwitch(genDisassemble, "/*Default*/", decodeTree, 0)
