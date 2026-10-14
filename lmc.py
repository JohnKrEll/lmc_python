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
        self._invalid_instructions = [900] + list(range(400, 450)) + list(range(451, 500)) + list(range(903, 922)) + list(range(923, 950)) + list(range(950, 1000)) 
        self._mem: list[int] = [0] * 100
        self._input: int = 0
        self._output: list[int] = list()
        self._program_counter: int = 0
        self._end: bool = False
        self._verbose: bool = verbose
        self._debug: bool = debug
        self._debug_timer: float = debug_timer
        self._op_registry: dict[int, Callable[[int], None]] = {
                OpCodes.ADD.value: self._add,
                OpCodes.SUB.value: self._sub,
                OpCodes.BRA.value: self._bra,
                OpCodes.BRZ.value: self._brz,
                OpCodes.BRP.value: self._brp,
                OpCodes.LDA.value: self._lda,
                OpCodes.STA.value: self._sta,
                OpCodes.INP.value: self._inp,
                OpCodes.OUT.value: self._out,
                OpCodes.HLT.value: self._halt,
                OpCodes.COUT.value: self._out_as_char
                }

    def run(self) -> None:
        while (not self._end):
            self._eval()

    def _clear(self) -> None:
        self._mem = [0] * 100
        self._acc = 0
        self._program_counter = 0
        self._end = False
        self._output = list()

    # Laster inn et program representert av en kommaseparert string.
    def load_csv_string(self, program_string: str) -> None:
        program = [self._parse_line(n,i) for i, n in enumerate(program_string.split(","))]
        self._load(program)

    def _parse_line(self, line: str, linenr: int) -> int:
        try:
            return int(line)
        except ValueError:
            raise ValueError(f"Invalid instruction in program at line {linenr + 1}: {line.strip()!r}") from None

    def load_machinecode(self, program):
        self._load(program)

    # Enumererer gjennom en fil linje for linje, og laster hver linje inn i memorybuffer som en int.  
    def load_machinecode_file(self, filereader: LMC_FileReader):
        program = [self._parse_line(line, i) for i, line in enumerate(filereader.lines())]
        self._load(program)

    def _load(self, program):
        self._clear()
        if len(program) > 100:
            raise ValueError("The program sequence provided is longer than the program buffer.")
        for i in range(0, len(program)):
            if self._is_invalid_instruction(program[i]):
                raise ValueError(f"Invalid instruction provided at position {i}: {program[i]}")
            self._mem[i] = program[i]

    # Fetches input from a user
    def _get_input(self) -> None:
        self._input = int(input("--->: "))
    
    # Returns output.
    def output(self) -> list[int]:
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

    # returns result of adding value of index in memory to accumulator.
    def _add(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Adding {self._mem[idx]} from adress {idx} to current value in accumulator {self._acc}")
        self._acc += self._mem[idx]

    # returns result of subtracting value of index in memory from accumulator.
    def _sub(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"subtracting {self._mem[idx]} from adress {idx} from value in accumulator {self._acc}")
        self._acc -= self._mem[idx]

    # stores accumulator in index of memory.
    def _sta(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Adding value from accumulator {self._acc} to adress {idx}")
        self._mem[idx] = self._acc

    # returns value in index of memory, should be used as a way to load some memory into acc.
    def _lda(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Loading value {self._mem[idx]} from adress {idx} to accumulator")
        self._acc = self._mem[idx]

    # returns value in index of memory, should be used as a way to branch to this as instruction. 
    def _bra(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Branching to {idx} from {self._program_counter}")
        self._program_counter = idx

    # returns the value in index of memory if accumulator is zero, else false.
    def _brz(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Trying to branch to {idx} from {self._program_counter} if accumulator is 0: {self._acc == 0}")
        if self._acc == 0:
            self._program_counter = idx

    # returns the value in index of memory if accumulator is 0 or positive, else false.
    def _brp(self, idx: int) -> None:
        if self._verbose and self._debug:
            print(f"Trying to branch to {idx} from {self._program_counter} if accumulator is a positive value: {self._acc >= 0}")
        if self._acc >= 0:
            self._program_counter = idx

    # Tar imot en input verdi, og gjør om acc til input. 
    def _inp(self, _idx) -> None:
        if self._verbose and self._debug:
            print(f"Loading data from input in accumulator.")
        self._get_input()
        self._acc = self._input

    # Flytter verdi fra acc til output. 
    def _out(self, _idx) -> None:
        if self._verbose and self._debug:
            print(f"Storing value of accumulator: {self._acc} in output")
        self._output.append(self._acc)

    def _out_as_char(self, _idx) -> None:
        if self._verbose and self._debug:
            print(f"Storing value in accumulator: {self._acc} in output as char")
        self._output.append(chr(self._acc))

    # setter end til true.
    def _halt(self, _idx) -> None:
        if self._verbose and self._debug:
            print("Halting program execution")
        self._end = True

    # Leser en programinstruksjon, og parser opcode. 
    def _get_opcode_from_instruction(self, instruction: int) -> int:
        if instruction in OpCodes:
            return instruction
        return instruction // 100


def main():
    parser = argparse.ArgumentParser(description="Simulates an LMC in python. Runs the lmc program in the provided textfile.")
    parser.add_argument("file", help="Textfile containing the lmc program")
    parser.add_argument("-d", "--debug", action="store_true", help="Enables debug mode.")
    parser.add_argument("-t", "--timer", type=float, default=0, help="Optional timer for debugmode printout.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Adds aditional information to debug mode.")
    args = parser.parse_args()
    lmc = LMC(args.debug, args.timer, args.verbose)
    reader = LMC_FileReader(args.file)
    match reader.get_filetype():
        case LMC_FileType.ASSEMBLY:
            assembler = LMC_Assembler()
            assembler.load(reader)
            lmc.load_machinecode(assembler.get_program())
        case LMC_FileType.MACHINE_CODE:
            lmc.load_machinecode_file(reader)
        case _:
            raise ValueError(f"Invalid filetype: {reader.get_filetype()}")
    lmc.run()
    print(lmc.output())


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(error)

