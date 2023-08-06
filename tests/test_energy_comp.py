import pyorca as po

path = 'data/fluoromethane/'

# load the experimentally determined geometry as a reference
# the order of atoms if [C, F, H, H, H]
with open(path+'fluoromethane.xyz', 'r') as f:
    atoms, exp_geometry, _ = po.geometry.read_xyz(f.read())

# this is the list of different levels of theory and the respective output files
calculated = [
    ("PM3", "fluoromethane_PM3.out"),
    ("BLYP/def2-SVP", "fluoromethane_BLYP_SVP.out"),
    ("B3LYP/def2-SVP", "fluoromethane_B3LYP_SVP.out"),
    ("B3LYP/def2-TZVP", "fluoromethane_B3LYP_TZVP.out"),
    ("B2PLYP/def2-TZVP", "fluoromethane_B2PLYP_TZVP.out"),
    ("B2PLYP/def2-QZVPP", "fluoromethane_B2PLYP_QZVPP.out"),
]

# this function extracts information about the geometry
# and also calculates RMSD (root mean squared distance) from the experimental structure
def calc_descriptors(exp_geometry, other_geometry):
    # align the structures and calculate RMSD
    rmds = po.geometry.aligned_rmsd(exp_geometry, other_geometry)

    # calculate bond distances and angles
    CF_dist = po.geometry.distance(other_geometry[0], other_geometry[1])
    CH_dist = po.geometry.distance(other_geometry[0], other_geometry[2])
    HCH_angl = po.geometry.angle_degree(other_geometry[2], other_geometry[0], other_geometry[3])

    # return all values for printing
    return rmds, CF_dist, CH_dist, HCH_angl

# Define template for printing nice table
template = '{: <18} {: <10.3f} {: <10.3f} {: <10.3f} {: <10.3f} {: ^15}'

# print table header
print(template.replace('.3f','').format('Method', 'RMSD', 'C-F dist.', 'C-H dist.', 'H-C-H angl.', 'duration'))

# print the experimental geometry for reference
print(template.format('Experimental', *calc_descriptors(exp_geometry, exp_geometry), '-'))

# process all ORCA output files
for method, filename in calculated:
    # parse the file
    data = po.OrcaOutput.parse_file(path+filename)

    # load final geometry and calculation duration
    final_geometry = data.calculations[0].final_coordinates
    duration = data.duration

    # print the data
    print(template.format(method, *calc_descriptors(exp_geometry, final_geometry), duration))