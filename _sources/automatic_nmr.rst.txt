NMR shifts of solvents
======================

In this example, we will create an automatic pipeline for predicting 1H NMR shifts of common solvents.
Although this is a simplistic example, it nicely demonstrates how PyORCA could be used to 
create automated workflows for ORCA calculations.

The individual steps are:
    1. Use PyORCA to guess initial geometry from SMILES
    2. Create ORCA input file
    3. Run the ORCA calculation
    4. Use PyORCA to parse the output file and extract NMR shielding constants
    5. Calibrate the shifts with reference to TMS
    6. Print the results and compare them with experimental data

ORCA input
----------

We will be using the following compound job for ORCA:

.. code-block:: text

    # Method for refining geometry and getting 1H NMR shielding constants
    # Implicit solvation with chloroform is used

    # Geometry refinement
    NEW_STEP
    ! B3LYP def2-TZVP def2/J D4 Opt TightOpt TightSCF Freq
    ! CPCM(chloroform)
    STEP_END

    # NMR calculation
    NEW_STEP
    ! B3LYP def2-TZVP NORI D4 NMR VeryTightSCF NoFrozenCore
    ! CPCM(chloroform)
    %EPRNMR
         NUCLEI = ALL H {SHIFT}
    END
    STEP_END

    END


The ORCA input files can reference this method, and their general structure will be:

.. code-block:: text

    %maxcore 8000

    * xyz 0 1
    [INITIAL GEOMETRY OF THE MOLECULE]
    *

    %compound "method.cmp"

So let's take a look on the Python script!


The Python script
-----------------

First, let's import relevant parts from PyORCA and define some paths.

.. code-block::

    from pyorca.conformers import conformer_from_smiles
    from pyorca.geometry import generate_xyz_block
    from pyorca import run_orca, OrcaOutput

    working_dir = "orca/"
    method = "method.cmp"

We also need to define the SMILES strings and create template for the ORCA input.

.. code-block::

    # names and SMILES of target molecules
    molecules = {
        'tetramethylsilane': 'C[Si](C)(C)C',
        'chloroform': 'ClC(Cl)Cl',
        'acetonitrile': 'CC#N',
        'acetone': 'CC(=O)C',
        'benzene': 'c1ccccc1',
    }

    # template for the ORCA input file
    # %VAR_NAME% will be replaced by actual values later
    input_template = """\
    %maxcore 8000

    * xyz 0 1
    %XYZ_BLOCK%
    *

    %compound "%METHOD%"

    """.replace("%METHOD%", method)

Now we run the individual ORCA calculations and extract the NMR data from the output files.

.. code-block::

    nmr_data = {} # NMR data will be stored here

    # run the ORCA calculation for all molecules
    for molecule, smiles in molecules.items():
        print('Starting ORCA calculation for:', molecule)

        # generate initial conformer
        # MMFF94 is defined well for all molecules in the dataset - should be better than UFF
        conformer = conformer_from_smiles(smiles, force_field='MMFF94')

        # create ORCA input file
        input_text = input_template.replace(
            "%XYZ_BLOCK%",
            generate_xyz_block(conformer.atoms, conformer.coordinates)
        )
        filename = path.join(working_dir, molecule+'.inp')
        with open(filename, 'w') as f:
            f.write(input_text)

        # run ORCA
        result = run_orca(filename)

        # check exit status
        if result.status_code != 0:
            print('ORCA terminated with status code', result.status_code)
            print(result.status_message)

        # parse the output file
        data = OrcaOutput.parse_file(result.output_file)

        # check imaginary frequencies from the second calculation
        n_imaginary_modes = data.calculations[0].final_single_point.normal_modes.imaginary
        if n_imaginary_modes > 0:
            print(f"The current structure has {n_imaginary_modes} imaginary nodes!!!")

        # get the NMR shifts
        nmr_data[molecule] = data.calculations[1].nmr

    print("All ORCA calculations finished!")
    print()

The last step is to calibrate shifts against TMS, and average shifts of equivalent hydrogens.

.. code-block::

    # Since all molecules in this dataset contain only equivalent hydrogens, we can average their shifts
    def average_shifts(shifts) -> float:
        return sum([s.shift for s in shifts])/len(shifts)

    # calibrate shifts according to TMS
    tms_shift = average_shifts(nmr_data['tetramethylsilane'].shifts)

    for molecule in nmr_data.keys():
        nmr_data[molecule].calibrate_shifts({'H': tms_shift})

The calculated shifts can be now neatly summarized and compared to experimental ones.

.. code-block::

    # for comparison, these are experimental shifts in CDCl3
    experimental_shifts = {
        'tetramethylsilane': 0.0,
        'chloroform': 7.26,
        'acetonitrile': 2.10,
        'acetone': 2.17,
        'benzene': 7.36,
    }

    # print summary table
    template = '{: <20} {: >12.2f} {: >12.2f}'
    print(template.replace('.2f','').format('Molecule', 'Calc. shift', 'Exp. shift'))

    for molecule in nmr_data.keys():
        print(template.format(
            molecule,
            average_shifts(nmr_data[molecule].shifts),
            experimental_shifts[molecule]
        ))

All the calculations take around an hour to run, and the script output is below:

.. code-block:: text

    Starting ORCA calculation for: tetramethylsilane
    Starting ORCA calculation for: chloroform
    Starting ORCA calculation for: acetonitrile
    Starting ORCA calculation for: acetone
    Starting ORCA calculation for: benzene
    All ORCA calculations finished!

    Molecule              Calc. shift   Exp. shift
    tetramethylsilane           -0.00         0.00
    chloroform                   7.82         7.26
    acetonitrile                 1.98         2.10
    acetone                      2.21         2.17
    benzene                      7.80         7.36

The accuracy of the calculated shifts reflect the accuracy of B3LYP/def2-TZVP, but overall they are not bad!

The great thing about this script is that we could calculate the shifts for tens or even hundreds of molecules, and fully automatically!

Directory Structure
-------------------

Let's also shortly talk about the directory structure.
I prefer to have separate folders for python scripts and tempates,
for ORCA input and output files, and for all other ORCA files.

I set up the directories like this:

.. code-block:: text

    ┳━ orca
    ┣━ process.py
    ┗━ method.cmp

The ORCA input files are saved into the ``orca`` folder, and the function `run_orca <pyorca.run_orca>`
then creates ``runtime`` subfolder, where all the other ORCA files will be saved.

After running ``process.py``, the directory structure looks like this:

.. code-block:: text

    ┳━ orca
    ┃  ┣━ runtime
    ┃  ┃   ┗━ many ORCA files, such as .xyz, .gbw, .hess, .opt, ...
    ┃  ┣━ acetone.inp
    ┃  ┣━ acetone.out
    ┃  ┣━ acetonitrile.inp
    ┃  ┣━ acetonitrile.out
    ┃  ┣━ benzene.inp
    ┃  ┣━ benzene.out
    ┃  ┗━ ...
    ┣━ process.py
    ┗━ method.cmp