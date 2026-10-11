0-99 adresser. 
1-9 opcodes.

1. ADD -> 1xx -> Adds value in adresse xx til accumulator.
2. SUB -> 2xx(4xx) -> Subtracts value in adress xx from accumulator. 
3. STA -> 3xx(2xx) -> Stores value in accumulator in adress xx. 
4. LDA -> 5xx -> Loads value from adress xx into accumulator. 
5. BRA -> 6xx(9xx) -> Unconditionaly jumps to instruction adress xx
6. BRZ -> 7xx -> Jumps to adress xx if accumulator is 0
7. BRP -> 8xx -> Jumps to adress xx if accumulator is 0 or positive.
8. INP -> 901 -> Takes a value from input tray, and places it in the accumulator. 
9. OUT -> 902 -> Copies the value from the accumulator to output tray. 

