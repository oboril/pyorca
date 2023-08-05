Parsing ORCA output files
=========================

The ORCA output can be parsed using the :class:`OrcaOutput <pyorca.OrcaOutput>` class.

Example
~~~~~~~

DFT calculation was used to optimize ethylene geometry. Let's see some basic information about the calculation!

The ORCA output is in :download:`ethylene_geometry.out  <_static/ethylene_geometry.out>` file.

.. exec_code::

    # import PyOrca
    import pyorca as po

    # parse the ORCA output file
    data = po.OrcaOutput.parse_file('ethylene_geometry.out')

    # see what was the ORCA input file name
    print('The input file name:', data.input_filename)

    # see what was the calculation input
    print('The ORCA input was:')
    print(data.input_text)

    # check that the calculation terminated normally
    print('Did calculation terminate normally:', data.terminated_normally)

    # see how long the ORCA calculation took
    print('The calculation took', data.duration)
    
We can see what was the calculation input, and that the calculation took just under 15 seconds!

The results of the calculation can be accessed in :attr:`OrcaOutput.calculations <pyorca.OrcaOutput.calculations>`.