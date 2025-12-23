<<<<<<< HEAD
=======
# CC

>>>>>>> b046d9a (Add mould_6_solidification_BOF OpenFOAM case)
the depository created during the Modeling with Open Source Software course, Fall 2025.

The model describes liquid steel and air flows in the continuous casting mould using compressibleVof OpenFOAM v13 solver.

<<<<<<< HEAD
The computational mesh "mould_CC.msh" is generated in a third-party software and is supplied in the model repository.

fluent3DMeshToFoam -scale 0.001 mould_CC.msh command is used to convert the mesh.
=======
The computational mesh "mould\_CC.msh" is generated in a third-party software and is supplied in the model repository.

fluent3DMeshToFoam -scale 0.001 mould\_CC.msh command is used to convert the mesh.
>>>>>>> b046d9a (Add mould_6_solidification_BOF OpenFOAM case)

To run the case the user must (1) make the file executable through chmod +x Allrun command (2) ./Allrun

To post-process the residual data the user needs to use ./Post command making it executable in the first place.

To clean up the computed data the user needs to use ./Allclean
<<<<<<< HEAD
=======

To see the state view one can load state.pvsm to Paraview.

>>>>>>> b046d9a (Add mould_6_solidification_BOF OpenFOAM case)
