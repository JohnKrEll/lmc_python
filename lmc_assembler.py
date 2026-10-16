from opcodes import OpCodes
from lmc_filereader import LMC_FileReader, LMC_FileType


class LMC_Assembler:
    def __init__(self):
        self._label_registry = dict()
        self._assembly = [0] * 100
        self._program = [0] * 100

    def _parse_assembly_line(self, line, idx):
        if line.startswith("//"):
            return
        line_values = line.split()
        match len(line_values):
            case 0:
                return
            case 1:
                self._parse_single_value_line(line_values[0], idx)
            case 2:
                op, addr = line_values
                if addr == "DAT":
                    self._label_registry[op] = idx
                else:
                    self._parse_line_no_label_def(op, addr, idx)
            case 3:
                label, op, addr = line_values
                self._parse_line_with_label_definition(label, op, addr, idx)
            case _:
                raise ValueError(f"More than three instructions provided on line {idx + 1}: {line}")

    def _parse_single_value_line(self, value, idx):
        if value.isnumeric():
            self._assembly[idx] = int(value)
        elif OpCodes.eval_opcode(value) == 9 or OpCodes.eval_opcode(value) == 0:
            self._assembly[idx] = OpCodes[value].value
        else:
            raise ValueError(f"Unknown command and value at line {idx + 1}: {value}")

    def _parse_line_no_label_def(self, op, addr, idx):
        if op == "DAT": 
            if addr.isnumeric():
                self._assembly[idx] = int(addr)
            else:
                self._assembly[idx] = (None, addr)
            return
        if op not in [code.name for code in OpCodes]:
            raise ValueError(f"Error on line {idx + 1}: Operation {op} not supported")
        if OpCodes.eval_opcode(op) == 0 or OpCodes.eval_opcode(op) == 9:
            raise ValueError(f"Error on line {idx + 1}: Invalid operand assignmed to non-supported operation. Operation: {op}, Value: {addr}")
            return
        if addr.isnumeric():
            self._assembly[idx] = OpCodes[op].value * 100 + int(addr)
            return
        self._assembly[idx] = (OpCodes[op].value, addr)

    def _parse_line_with_label_definition(self, label, op, addr, idx):
        if label in self._label_registry.keys():
            raise ValueError(f"Error on line {idx + 1}: Allready defined {label} at line {self._label_registry[label]}")
        self._label_registry[label] = idx
        self._parse_line_no_label_def(op, addr, idx)

    def _assemble(self):
        for i, line in enumerate(self._assembly):
            if isinstance(line, tuple):
                if line[0] is None:
                    self._program[i] = self._label_registry[line[1]]
                else:
                    self._program[i] = line[0] * 100 + self._label_registry[line[1]]
            else:
                self._program[i] = self._assembly[i]

    def _read_machine_code_filetype(self, filereader: LMC_FileReader):
        self._program = [self._parse_machine_code_line(line, idx) for idx, line in enumerate(filereader.lines())]

    def _parse_machine_code_line(self, line, idx):
        try:
            return int(line.strip())
        except ValueError:
            raise ValueError(f"Unsupported machinecode at line {idx+1}: {line}")

    def load(self, filereader: LMC_FileReader) -> None:
        match filereader.get_filetype():
            case LMC_FileType.ASSEMBLY:
                for i, line in enumerate(filereader.lines()):
                    self._parse_assembly_line(line, i)
                self._assemble()
            case LMC_FileType.MACHINE_CODE:
                self._read_machine_code_filetype(filereader)
            case _:
                raise ValueError(f"Unsupported filetype {filereader.get_filetype()}")

    def load_assembly_string(self, assembly: str) -> None:
        for i, line in enumerate(assembly.split("\n")):
            self._parse_assembly_line(line, i)
        self._assemble()

    def get_program(self):
        return self._program
