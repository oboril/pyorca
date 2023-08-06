PyORCA.conformers reference
===========================

RD Kit conformers
-----------------

RD Kit can generate random conformers and optimize them using force fields, such as UFF and MMFF94.
This cannot replace proper conformer search and the conformers are not guaranteed to be global minima.
For small or rigid molecules, however, the generated conformers are generally good initial structures for
quantum calculations.

.. autofunction:: pyorca.conformers.conformer_from_smiles