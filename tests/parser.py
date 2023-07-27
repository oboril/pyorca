from orcapython.parsers.outputdata import OutputData

data = OutputData.parse_file("tests/testdata/H2O_opt_freq.out")
print(data.terminated_normally)
print(data.final_energy)
print(data.single_point_energies)
print(data.vib_freqs)