# CC
the depository created during the Modeling with Open Source Software course, Fall 2025.

The model describes liquid steel and air flows in the continuous casting mould using compressibleVof OpenFOAM v13 solver.

The computational mesh "mould_CC.msh" is generated in a third-party software and is supplied in the model repository.

fluent3DMeshToFoam -scale 0.001 mould_CC.msh command is used to convert the mesh.

To run the case the user must (1) make the file executable through chmod +x Allrun command (2) ./Allrun

To post-process the residual data the user needs to use ./Post command making it executable in the first place. 

To clean up the computed data the user needs to use ./Allclean.

To view the saved state, one can load state.pvsm to Paraview.

PS
Stefan_git contains Stefan test case setup. The meshes can be changed in Allrun.

PS, PS
There were multiple Stefan case try with different meshes and BCs. Also, the reference setup was tested and may not be included to Stefan_git folder.




