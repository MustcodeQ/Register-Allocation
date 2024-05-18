Register Allocation Example
This repository contains a simple example of register allocation using graph coloring in C++. The example demonstrates how to allocate a limited number of CPU registers to variables in a program while ensuring that no two variables that interfere with each other share the same register.

Table of Contents
Overview
Requirements
Usage
Example Output
Code Structure
Detailed Explanation
Contributing
License
Overview
The code performs the following steps:

Liveness Analysis: Determines when variables are live within a basic block.
Interference Graph Construction: Builds an interference graph where nodes represent variables and edges represent conflicts between variables.
Register Allocation: Uses a simplified graph coloring algorithm to allocate registers to variables.
Requirements
A C++ compiler (e.g., g++)
Usage
Compile the Code
sh
Copy code
g++ main.cpp -o register_allocation
Run the Executable
sh
Copy code
./register_allocation
Example Output
The program prints the register allocation result, showing which variable is assigned to which register. For example:

rust
Copy code
Register Allocation:
a -> R1
b -> R2
c -> R3
d -> R2
e -> R1
Code Structure
main.cpp: Contains the main logic for constructing the interference graph and performing register allocation.
Detailed Explanation
Data Structures
BasicBlock: Represents a basic block in the control flow graph with an ID, instructions, and sets for live-in and live-out variables.
InterferenceGraph: Represents the interference graph where edges indicate that two variables interfere and cannot share the same register.
Functions
createInterferenceGraph: Builds the interference graph from the basic blocks.
allocateRegisters: Allocates registers using a graph coloring algorithm, ensuring no two interfering variables share the same register.
Steps in the Code
Liveness Analysis: The createInterferenceGraph function constructs the interference graph by analyzing the lifetimes of variables.
Graph Coloring: The allocateRegisters function uses a stack-based approach to simplify the interference graph and assign registers.
Contributing
Contributions are welcome! If you have any improvements or bug fixes, please submit an issue or a pull request.
