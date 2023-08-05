from pyorca import OrcaOutput

data = OrcaOutput.parse_file('data/scan.out')

# print(f"{data.input_filename=}")
# print(f"{data.input_text=}")
# print(f"{data.terminated_normally=}")
# print(f"{data.duration=}")


print(f"{data.calculations=}")

energies = [step.final_energy for step in data.calculations[0].steps]
print(energies)

# print("GEOMETRY OPTIMIZATION CYCLES")

# energies = [cycle.energy for cycle in data.calculations[0].cycles]
# print(energies)
# print(data.calculations[0].final_energy)
