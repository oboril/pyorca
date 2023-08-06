import pyorca as po

conformer = po.conformers.conformer_from_smiles("C[Si](C)(C)C", force_field="MMFF94")

print(conformer.converged, conformer.energy)

with open("results.xyz", "w") as f:
    f.write(po.geometry.write_xyz(conformer.atoms, conformer.coordinates))