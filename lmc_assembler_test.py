from lmc_assembler import LMC_Assembler


def validate_assembly_output(assembly: str, expected: list[int]) -> None:
    assembler = LMC_Assembler()
    assembler.load_assembly_string(assembly)
    assert assembler.get_program() == expected


# Test 1 ADD converteres til korrekt maskinkode
program_1 = "ADD 01"
expected_1 = [101] + ([0] * 99)
validate_assembly_output(program_1, expected_1)

# Test 2 SUB konverteres til korrekt maskinkode
program_2 = "SUB 01"
expected_2 = [201] + ([0] * 99)
validate_assembly_output(program_2, expected_2)

# Test 3 LDA konterteres til korrekt maskinkode
program_3 = "LDA 01"
expected_3 = [501] + ([0] * 99)
validate_assembly_output(program_3, expected_3)

# Test 4 STA konverteres til korrekt maskinkode
program_4 = "STA 01"
expected_4 = [301] + ([0] * 99)
validate_assembly_output(program_4, expected_4)

# Test 5 BRA konverteres til korrekt maskinkode
program_5 = "BRA 01"
expected_5 = [601] + ([0] * 99)
validate_assembly_output(program_5, expected_5)

# Test 6 BRZ konverteres til korrekt maskinkode
program_6 = "BRZ 01"
expected_6 = [701] + ([0] * 99)
validate_assembly_output(program_6, expected_6)

# Test 7 BRP konverteres til korrekt maskinkode
program_7 = "BRP 01"
expected_7 = [801] + ([0] * 99)
validate_assembly_output(program_7, expected_7)

# Test 8 INP konverteres til korrekt maskinkode
program_8 = "INP"
expected_8 = [901] + ([0] * 99)
validate_assembly_output(program_8, expected_8)

# Test 9 OUT Konverteres til korrekt maskinkode
program_9 = "OUT"
expected_9 = [902] + ([0] * 99)
validate_assembly_output(program_9, expected_9)

# Test 10 OTC Konverteres til korrekt maskinkode
program_10 = "OTC"
expected_10 = [922] + ([0] * 99)
validate_assembly_output(program_10, expected_10)

# Test I/O with operand til
program_11 = "OUT 01"
expected_11 = [901] + ([0] * 99)
try:
    validate_assembly_output(program_11, expected_11)
    assert False
except ValueError:
    assert True

# Test labels convert to correct operand
program_12 = """ LDA x
x DAT 01"""
expected_12 = [501, 1] + ([0] * 98)
validate_assembly_output(program_12, expected_12)


# Test label on DAT without operand defaults value at index to 0
program_13 = """LDA x
x DAT"""
expected_13 = [501] + ([0] * 99)
validate_assembly_output(program_13, expected_13)
