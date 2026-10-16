from lmc import LMC

# Denne må omskrives!

# Dette programmet skal hente to tall fra brukeren, summe de sammen og legge svaret i output. 
lmc = LMC()
# Dette programmet skal legge tallet 1 i adresse 99, så adde 1 på seg selv to ganger.
# INP
# STA 99
# ADD 99
# ADD 99
# OUT
lmc.load_machinecode(program)
lmc.run()
assert lmc.output() == [3]


# Dette programmet skal skrive ut Hello i output
program = [450, 72, 922, 450, 101, 922, 450, 108, 922, 450, 108, 922, 450, 111, 922]
lmc.load_csv_string(program)
lmc.run()
assert lmc.output() == ['H', 'e', 'l', 'l', 'o']

# Dette programmet skal telle ned fra 2 -> 0.
# DAT
# 002
# STA 98
# DAT
# 001
# STA 99
# ADD 98
# SUB 99
# OUT
# BRZ 11
# BRA 07
# HALT
program = "450, 2, 398, 450, 1, 399, 198, 299, 902, 711, 607, 000"
lmc.load_csv_string(program)
lmc.run()
assert lmc.output() == [2, 1, 0]
