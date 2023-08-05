from orcapython import OrcaOutput

data = OrcaOutput.parse_file('data/CH4_UVVIS.out')

print(f"{data.input_filename=}")
print(f"{data.input_text=}")
print(f"{data.terminated_normally=}")
print(f"{data.duration=}")


print(f"{data.calculations=}")
