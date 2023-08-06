Welcome to PyORCA!
==================================

.. note::
   PyORCA is currently in development, many features are missing or incomplete. The first stable version should be coming soon!

This Python packages aims to help with creating automated pipelines for quantum chemistry calculations!

PyORCA allows you to easily build input files, parse output files and build automated pipelines for ORCA.
`ORCA <https://orcaforum.kofo.mpg.de/index.php>`_ is free quantum chemistry package - I'm not affiliated to ORCA, but I love using it!

Look into the examples below to explore how to use PyORCA.

.. toctree::
   :maxdepth: 1
   :hidden:

   self
   installation

.. toctree::
   :maxdepth: 1
   :caption: Parsing Output

   parsing_output
   parsing_output.sp
   parsing_output.opt
   parsing_output.ref

.. toctree::
   :maxdepth: 1
   :caption: 3D structures

   geometry.example
   geometry.ref
   conformers.ref

.. toctree::
   :maxdepth: 1
   :caption: Automated Workflows

   automatic_nmr
   orca_interface.ref