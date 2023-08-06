Single Point Calculation
========================

The results of single point calculations are in ``SinglePointCalculation`` class.

Example
-------

The optimizied geometry of ethylene was used to calculate the electronic transitions, these can be useful for predicting UV-VIS spectrum.

The ORCA output is in the :download:`ethylene_uvvis.out <_static/ethylene_uvvis.out>` file, let's see how we can parse it!

.. exec_code::

    # import PyORCA
    import pyorca as po

    # parse the ORCA output file
    data = po.OrcaOutput.parse_file('ethylene_uvvis.out')

    # check that the calculation terminated normally
    assert(data.terminated_normally)

    # this output file contains only single calculations, the TD-DFT calculation
    print('Number of calculations:', len(data.calculations))
    print()

    # get the information about electronic spectrum
    electronic_spectrum = data.calculations[0].electronic_spectrum

    # print the wavelengths and intensities of electronic transitions
    print('Electronic transitions:')
    for wavelength, intensity in zip(electronic_spectrum.wavelengths, electronic_spectrum.intensities):
        print(f'{wavelength:0.1f} nm (relative intensity {intensity:0.4f})')

The experimental UV-VIS spectrum of ethylene has absorption maximum around 261 nm, so even simple B3LYP/def2-TZVP can give us a good estimate!