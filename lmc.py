from opcodes import OpCodes
import time
from collections.abc import Callable
import argparse
from lmc_filereader import LMC_FileReader, LMC_FileType
from lmc_assembler import LMC_Assembler


class LMC:
    """An implementation of an LMC in python

    Args:
        debug: enable debug mode, this prints out information about how the program is parsed. 
        debug_timer: sets a float value representing the amount of seconds the program should wait between evaluations.
    """

    def __init__(self, debug = False, debug_timer: float = 0, verbose = False) -> None:
        self._acc: int = 0
        self._invalid_instructions = [900] + list(range(400, 500)) + list(range(903, 922)) + list(range(923, 1000)) 
        self._mem: list[int] = [0] * 100
        self._input: int = 0
        self._output: list[int] = list()
        self._program_counter: int = 0
        self._end: bool = False
        self._verbose: bool = verbose
        self._debug: bool = debug
        self._debug_timer: float = debug_timer
        self._op_registry: dict[int, Callable[[int], None]] = {
                OpCodes.ADD: self._add,
                OpCodes.SUB: self._sub,
                OpCodes.BRA: self._bra,
                OpCodes.BRZ: self._brz,
                OpCodes.BRP: self._brp,
                OpCodes.LDA: self._lda,
                OpCodes.STA: self._sta,
                OpCodes.INP: self._inp,
                OpCodes.OUT: self._out,
                OpCodes.HLT: self._halt,
                OpCodes.OTC: self._out_as_char
                }

    def run(self) -> None:
        """
        Starts running program loaded into memory.

        raises ValueError:
                if the programcounter points to an invalid memory location.
                if the program generates an invalid operation. 
        """
        while (not self._end):
            self._eval()

    def _clear(self) -> None:
        self._mem = [0] * 100
        self._acc = 0
        self._program_counter = 0
        self._end = False
        self._output = list()

    # Loads machinecode into internal memory of the lmc
    def load_machinecode(self, program: list[int]) -> None:
        """
        Resets lmc.
        Loads Machinecode into internal memory.
        Validates length and instructions. 

        - program: a list of integers representing lmc machine code. 
        """
        self._load(program)

    # Enumererer gjennom en fil linje for linje, og laster hver linje inn i memorybuffer som en int.  
    def load_machinecode_file(self, filereader: LMC_FileReader):
        """
        Loads a file representing machinecode. 
        parses each line to a whole number, then loads the finished list of integers as a program
        Validates length and instructions.

        Throws:
            If the filereader points to the wrong filetype.

        - filereader: An LMC_FileReader object that holds metadata about a lmc program file.
        """
        if not filereader.get_filetype() == LMC_FileType.MACHINE_CODE:
            raise ValueError(f"Wrong filetype provided to machinecode parser: {filereader.get_filetype()}")
        program = [self._parse_line(line, i) for i, line in enumerate(filereader.lines())]
        self._load(program)

    # Resetter lmc, laster inn program i internminne, validerer lengde og instrukser.
    def _load(self, program: list[int]) -> None:
        self._clear()
        if len(program) > 100:
            raise ValueError("The program sequence provided is longer than the program buffer.")
        for i in range(0, len(program)):
            if self._is_invalid_instruction(program[i]):
                raise ValueError(f"Invalid instruction provided at position {i}: {program[i]}")
            self._mem[i] = program[i]

    # Henter input fra en bruker.
    def _get_input(self) -> None:
        self._input = int(input("--->: "))

    # Returns output.
    def output(self) -> list[int]:
        """
        returns internal output.
        """
        return self._output

    def _is_invalid_instruction(self, instruction):
        return instruction < 0 or instruction in self._invalid_instructions or instruction >= 1000

    # Evaluerer programinstruksjonen,
    # henter operasjon fra registrar basert på opcode i programinstruksjon.
    def _eval(self) -> None:
        if self._program_counter >= 100:
            raise ValueError(f"Pointer moved passed alloted memory buffer: {self._program_counter}")
        instruction = self._mem[self._program_counter]
        if self._is_invalid_instruction(instruction):
            raise ValueError(f"Invalid instruction produced at pointer {self._program_counter}: {self._instruction}")
        self._program_counter += 1
        k = self._get_opcode_from_instruction(instruction)
        curr_op = self._op_registry[k]
        idx = instruction % 100
        if self._debug:
            time.sleep(self._debug_timer)
            print(f"Evaluerer {instruction}...")
            print(f"Kjører {OpCodes(k).name} på adresse {idx if idx >= 0 else 'I/O'}")
        curr_op(idx)

    # Definerer ADD instruksjonen, henter verdi i minne på idx, legger denne verdien til acc.
    def _add(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Adding {self._mem[idx]} from adress {idx} to current value in accumulator {self._acc}")
        self._acc += self._mem[idx]

    # Definerer SUB instruksjonen, henter verdi i mine på idx, trekker denne verdien fra acc.
    def _sub(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"subtracting {self._mem[idx]} from adress {idx} from value in accumulator {self._acc}")
        self._acc -= self._mem[idx]

    # Definerer STA instruksjonen, legger verdi i acc til minnet på idx. Overskriver hvis det allerede er noe der.
    def _sta(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Adding value from accumulator {self._acc} to adress {idx}")
        self._mem[idx] = self._acc

    # Definerer LDA instruksjonen, legger en verdi fra minnet på idx til acc, overskriver verdier allerede i acc.
    def _lda(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Loading value {self._mem[idx]} from adress {idx} to accumulator")
        self._acc = self._mem[idx]

    # Definerer BRA instruksjonen. Flytter programcounter til idx.
    def _bra(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Branching to {idx} from {self._program_counter}")
        self._program_counter = idx

    # Definerer BRZ instruksjonen. Flytter programcounter til idx hvis acc == 0.
    def _brz(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Trying to branch to {idx} from {self._program_counter} if accumulator is 0: {self._acc == 0}")
        if self._acc == 0:
            self._program_counter = idx

    # Definerer BRP instruksjonen. flytter programcounter til idx hvis acc >= 0 (positiv).
    def _brp(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Trying to branch to {idx} from {self._program_counter} if accumulator is a positive value: {self._acc >= 0}")
        if self._acc >= 0:
            self._program_counter = idx

    # Definerer INP instruksjonen. tar imot input fra terminal. setter verdi i acc. 
    def _inp(self, _idx) -> None:
        if self._verbose and self._debug:
            print(f"Loading data from input in accumulator.")
        self._get_input()
        self._acc = self._input

    # Definerer OUT instruksjonen. flytter verdi fra acc til output listen. 
    def _out(self, _idx) -> None:
        if self._verbose and self._debug:
            print(f"Storing value of accumulator: {self._acc} in output")
        self._output.append(self._acc)

    # Definerer OTC instruksjonen. flytter verdien i acc til output listen som en char verdi.
    def _out_as_char(self, _idx) -> None:
        if self._verbose and self._debug:
            print(f"Storing value in accumulator: {self._acc} in output as char")
        self._output.append(chr(self._acc))

    # Definerer HLT instruksjonen. setter _end til true, som avslutter løkken i run.
    def _halt(self, _idx) -> None:
        if self._verbose and self._debug:
            print("Halting program execution")
        self._end = True

    # Parser ut operasjonskoden fra instruksjonen, slik at det kan hentes en operasjon fra operasjonsregisteret. 
    def _get_opcode_from_instruction(self, instruction: int) -> OpCodes:
        if instruction in OpCodes:
            return OpCodes(instruction)
        return OpCodes(instruction // 100)


def main():
    parser = argparse.ArgumentParser(description="Simulates an LMC in python. Runs the lmc program in the provided textfile.")
    parser.add_argument("file", help="Textfile containing the lmc program")
    parser.add_argument("-d", "--debug", action="store_true", help="Enables debug mode.")
    parser.add_argument("-t", "--timer", type=float, default=0, help="Optional timer for debugmode printout.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Adds aditional information to debug mode.")
    args = parser.parse_args()
    lmc = LMC(args.debug, args.timer, args.verbose)
    reader = LMC_FileReader(args.file)
    assembler = LMC_Assembler()
    assembler.load(reader)
    lmc.load_machinecode(assembler.get_program())
    lmc.run()
    print(lmc.output())


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(error)

