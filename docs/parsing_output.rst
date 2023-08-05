Parsing ORCA output files
=========================

The ORCA output can be parsed using the ``OrcaOutput`` class.

Example
~~~~~~~

DFT calculation was used to optimize water geometry. Let's see some basic information about the calculation!

The ORCA output is in :download:`water_geometry.out  <_static/water_geometry.out>` file.

.. exec_code::

    import pyorca as po

    data = po.OrcaOutput.parse_file('water_geometry.out')

    print('The input file name:', data.input_filename)

    print('The ORCA input was:')
    print(data.input_text)

    print('Did calculation terminate normally:', data.terminated_normally)
    print('The calculation took', data.duration)
    
We can see what was the calculation input, and that the calculation took just under 15 seconds!

The results of the calculation can be accessed in ``OrcaOutput.calculations``.

OrcaOutput class
~~~~~~~~~~~~~~~~

.. autoclass:: pyorca.OrcaOutput
    :members: