Register Allocation Example
This repository contains a simple example of register allocation using graph coloring in C++. The example demonstrates how to allocate a limited number of CPU registers to variables in a program while ensuring that no two variables that interfere with each other share the same register.

Overview
The code performs the following steps:

Liveness Analysis: Determines when variables are live within a basic block.
Interference Graph Construction: Builds an interference graph where nodes represent variables and edges represent conflicts between variables.
Register Allocation: Uses a simplified graph coloring algorithm to allocate registers to variables.
Code Structure
main.cpp: Contains the main logic for constructing the interference graph and performing register allocation.
How to Compile and Run
Compile the Code:

sh
Copy code
g++ main.cpp -o register_allocation
Run the Executable:

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
Detailed Explanation
Data Structures
BasicBlock: Represents a basic block in the control flow graph with an ID, instructions, and sets for live-in and live-out variables.
InterferenceGraph: Represents the interference graph where edges indicate that two variables interfere and cannot share the same register.
Functions
createInterferenceGraph: Builds the interference graph from the basic blocks.
allocateRegisters: Allocates registers using a graph coloring algorithm, ensuring no two interfering variables share the same register.
Contributing
Feel free to submit issues or pull requests if you have any improvements or bug fixes.
