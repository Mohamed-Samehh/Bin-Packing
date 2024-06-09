Bin Packing Problem Solver

Overview
- This project provides a graphical user interface (GUI) for solving the Bin Packing Problem using two different algorithms: backtracking and a genetic algorithm.
- The goal of the bin packing problem is to pack a set of items with given sizes into bins with a fixed capacity in such a way that the number of bins used is minimized.

Features
- Graphical User Interface (GUI): The application features a user-friendly GUI for inputting item sizes, bin capacity, and algorithm parameters.
- Backtracking Algorithm: Provides a solution by exhaustively searching for the optimal way to pack items into bins.
- Genetic Algorithm: Provides a solution using a population-based approach, which evolves over generations to find an optimal or near-optimal solution.
- Visualization: Displays the results in a bar chart, showing the distribution of item sizes across bins, along with the solution quality and computation time.

Prerequisites
- Python 3.x
- Required Python packages: matplotlib, tkinter

Installation
1- Install the required packages:
(Command)
pip install matplotlib

2- Run the application:
(Command)
python bin_packing_solver.py

How to Use
- Enter Item Sizes: Input the sizes of the items separated by spaces.
- Enter Bin Capacity: Specify the maximum capacity of each bin.
- Choose Algorithm: Select '1' for the backtracking algorithm or '2' for the genetic algorithm.
- Genetic Algorithm Parameters (optional):
  - Population Size: Default is 50.
  - Number of Generations: Default is 100.
  - Mutation Rate: Default is 0.01.

Visualization Options:
- Title: Enter a title for the visualization.
- Display Grid: Check the box to display a grid on the chart.
- Submit: Click the "Submit" button to run the selected algorithm and visualize the result.

Algorithm Details
- Backtracking Algorithm
- Function: bin_packing_backtracking(items, max_capacity)
- Description: Sorts items in descending order and attempts to place each item in the current bins. If an item cannot be placed, a new bin is created. The algorithm uses recursive backtracking to explore all possible ways to place items in bins.

Genetic Algorithm
- Function: genetic_algorithm(items, max_capacity, population_size, generations, mutation_rate)
- Description: Initializes a population of random solutions and evolves them over a number of generations using selection, crossover, and mutation to find an optimal or near-optimal solution.

Visualization
- The solution is visualized using a bar chart where each bar represents a bin, and the height of the bar corresponds to the total size of items in that bin. The chart also displays the solution quality and computation time.

Notes
- Ensure that item sizes do not exceed the bin capacity, as such items will be ignored.
- The application adjusts the recursion limit to handle larger sets of items for the backtracking algorithm.

Example
- Item Sizes: 4 5 6 7 8 9
- Bin Capacity: 15
- Algorithm Choice: 2 (Genetic Algorithm)
- Population Size: 50
- Generations: 100
- Mutation Rate: 0.01
- Title: Bin Packing Visualization
- Display Grid: Checked

Output
- Bar chart showing the distribution of items across bins.
- Solution quality (number of bins used).
- Computation time.
