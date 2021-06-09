# Sudoku-Solver

A sudoku solver built as part of the Artificial Intelligence unit of my degree.
I used constraint satisfaction for solver. It is able to solve most problems, but can struggle on the hardest ones. 
Tweaks could be made to improve performance, such as using deepcopy less frequently, or using a different algorithm.
The code was originally contained within a Jupyter notebook, but I have not posted the notebook I did not produce it.

The sudoku boards are entered as Numpy arrays with zeroes representing the empty spaces.
The "sudoku_solver" method is called with the board entered as an argument. The completed board is returned.
If the sudoku is not valid (e.g. two of the same number in a row), the board is returned with all spaces filled with "-1".
