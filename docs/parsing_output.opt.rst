Geometry Optimization
========================

Geometry optimizations are one of the most common calculations in quantum chemistry.
Let's take a look on the geometry optimization of ethylene once again!

The ORCA output is in :download:`ethylene_geometry.out  <_static/ethylene_geometry.out>`.

.. exec_code::

    # import PyORCA
    import pyorca as po

    # parse the ORCA output file
    data = po.OrcaOutput.parse_file('ethylene_geometry.out')

    # let's remind ourselves, what was the ORCA input
    print('The ORCA input was:')
    print(data.input_text)

    # geometry optimization is the only calculation in this output file
    geometry_optimization = data.calculations[0]

    # did the geometry optimization converge?
    print('Did geometry optimization converge:', geometry_optimization.converged)
    print()

    # how many geometry optimization cycles did it take?
    print('Number of optimization cycles:', len(geometry_optimization.cycles))
    print()

    # print the energies of the individual optimization cycles
    for idx, cycle in enumerate(geometry_optimization):
        print(f'Cycle {idx+1}: {cycle.energy:0.2f} kJ/mol')
    print()

    # it is common to check the frequencies of normal modes
    # any imaginary frequencies would signall that the structure is not at energetic minimum
    print('Number of imaginary modes:', geometry_optimization.final_single_point.normal_modes.imaginary)
    print()

    # let's also take a look what is the C-C bond order
    bond_orders = geometry_optimization.final_single_point.population_analysis.bond_orders
    # filter the bond orders based on atom indeces
    CC_bond_order = [bo for bo in bond_orders if bo.atom1==0 and bo.atom2==1][0]
    print(f'The C-C Mayer bond order is {CC_bond_order.order:0.2f}')

We can see that the optimization converged after 4 cycles, and that it is indeed a local minimum - there aren't any imaginary modes.

It is possible to read many different properties from both
:class:`OptimizationCycle <pyorca.orca_output.geometry_optimization.optimization_cycle.OptimizationCycle>`
and :class:`SinglePointCalculation <pyorca.orca_output.single_point.single_point.SinglePointCalculation>`.