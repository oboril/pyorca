"""Test the .out file parsing with some simple example files"""


from orcapython import OutputData

print("### H2O opt freq")
data = OutputData.parse_file("tests/testdata/H2O_opt_freq.out")
print(data.summary())

print("\n\n### CH4 uvvis")
data = OutputData.parse_file("tests/testdata/CH4_UVVIS.out")
print(data.summary())


print("\n\n### CH4 nmr")
data = OutputData.parse_file("tests/testdata/CH4_NMR.out")
print(data.summary())