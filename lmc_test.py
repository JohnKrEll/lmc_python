from lmc import LMC

# Dette programmet skal hente to tall fra brukeren, summe de sammen og legge svaret i output. 

# Dette programmet skal multiplisere to tall,
# ved å hente inn en incrementorverdi,
# hente inn en multiplikator verdi,
# så hente inn en verdi som skal multipliseres med multiplikator.
program = "901,395,901,396,596,398,901,397,599,197,399,598,295,716,398,608,599,902"
lmc = LMC()
lmc.load_csv_string(program)
lmc.run()
print(lmc.output())
