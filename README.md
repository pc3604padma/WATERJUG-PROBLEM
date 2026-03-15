Water Jug Problem
📌 Project Description

The Water Jug Problem is a classic Artificial Intelligence problem that demonstrates how a goal can be achieved using a sequence of valid operations. In this project, two jugs with different capacities are used to measure a specific quantity of water without any additional measuring tools.

The program simulates the process of filling, emptying, and transferring water between the jugs until the required amount of water is obtained.

🎯 Objective

The objective of this project is to determine the steps required to obtain a target quantity of water using two jugs of different capacities.

Example:

Jug A capacity = 4 gallons

Jug B capacity = 3 gallons

Target = 2 gallons in the 4-gallon jug

Initially, both jugs are empty, and the solution is obtained through a sequence of operations.

⚙️ Features

Simulates the classic AI Water Jug Problem

Demonstrates state space search

Shows step-by-step solution to reach the goal state

Implements operations like filling, emptying, and pouring between jugs

Written using Python

🧠 Concepts Used

Artificial Intelligence

Problem Solving using Production Rules

State Space Representation

Search Algorithms

🔄 Allowed Operations

The following operations are used to solve the problem:

Fill the 4-gallon jug completely.

Fill the 3-gallon jug completely.

Empty the 4-gallon jug.

Empty the 3-gallon jug.

Pour water from the 4-gallon jug to the 3-gallon jug.

Pour water from the 3-gallon jug to the 4-gallon jug.

These operations help move from one state to another until the goal state is reached.

🧾 Example Solution Steps

Initial State: (0,0)

Fill the 3-gallon jug → (0,3)

Pour into 4-gallon jug → (3,0)

Fill 3-gallon jug again → (3,3)

Pour into 4-gallon jug → (4,2)

Empty 4-gallon jug → (0,2)

Pour remaining water → (2,0)

Goal state achieved successfully.

💻 Technologies Used

Python

GitHub

VS Code

📂 Project Structure
Water-Jug-Problem
│
├── code.py        # Python implementation of water jug problem
├── README.md      # Project documentation
▶️ How to Run

Clone the repository

git clone https://github.com/pc3604padma/WATERJUG-PROBLEM.git

Navigate to the project folder

cd WATERJUG-PROBLEM

Run the Python file

python code.py
📖 Conclusion

This project demonstrates how Artificial Intelligence techniques can solve logical problems using a sequence of rules and state transitions. The Water Jug Problem helps in understanding state space search and problem-solving strategies in AI.
