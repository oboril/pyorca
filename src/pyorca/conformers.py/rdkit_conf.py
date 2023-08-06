from rdkit.Chem import AllChem
from rdkit import Chem
from rdkit.Chem import Draw

# Generate molecule from SMILES
molecule = AllChem.MolFromSmiles("C1CCCCC1C(C)C")
molecule = Chem.AddHs(molecule)

# Generate 3D structure
AllChem.EmbedMolecule(molecule)
AllChem.UFFOptimizeMolecule(molecule)

# Create conformers, cids = conformer IDs
cids = AllChem.EmbedMultipleConfs(molecule, numConfs=100)

# aligning is not neccessary here
# rmslist = []
# AllChem.AlignMolConformers(molecule, RMSlist=rmslist)
# print(len(rmslist))
# print(rmslist)

# optimize all conformers, res = list of (not converged, energy)
res = AllChem.MMFFOptimizeMoleculeConfs(molecule, maxIters=10000)

# zip the results together, (not converged, energy, id)
data = list(zip(*zip(*res),cids))

# sort by convergence and energy (the sort is stable)
data = sorted(data, key=lambda d: d[1])
data = sorted(data)

# count converged
converged = sum([1 for d in data if d[0] == 0])
print(f"Converged {converged}/{len(data)}")

# save the best conformer
with open("saved.xyz", "w") as f:
    cid = data[0][2]
    xyz = Chem.rdmolfiles.MolToXYZBlock(molecule, cid)
    f.write(xyz)