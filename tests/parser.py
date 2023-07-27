"""Test the .out file parsing with some simple example files"""


from orcapython.parsers.outputdata import OutputData

print("H2O opt freq")
data = OutputData.parse_file("tests/testdata/H2O_opt_freq.out")
print(data.terminated_normally)
print(data.final_energy)
print(data.single_point_energies)
print(data.vib_freqs)
print(data.thermochemistry[0])

print("\n\nCH4 uvvis")
data = OutputData.parse_file("tests/testdata/CH4_UVVIS.out")
print(data.terminated_normally)
print(data.final_energy)
print(data.single_point_energies)
print(data.electronic_trans)


print("\n\nCH4 nmr")
data = OutputData.parse_file("tests/testdata/CH4_UVVIS.out")
print(data.terminated_normally)
print(data.final_energy)