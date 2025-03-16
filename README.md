The Collatz Conjecture, also known as the "3n+1 problem," proposes that starting with any positive integer and repeatedly applying a simple rule (if even, divide by 2; if odd, multiply by 3 and add 1), you will always eventually reach the number 1.
# Collatz Conjecture Visualizer

A Python GUI application to visualize the Collatz conjecture sequences as fractal-like trees with interactive controls.



![image](https://github.com/user-attachments/assets/b26585c3-c088-4511-9b9c-d74aabdfc8e2)




## Features

- **Interactive GUI Controls**:
  - Adjust branch angles (even/odd numbers)
  - Set number of sequences (even/odd split)
  - Control branch length and depth
  - Modify starting number range
- **Visual Elements**:
  - Dark theme interface
  - Rainbow-colored paths (gist_rainbow colormap)
  - White root node (1) with yellow end markers
  - Rotated text labels for starting numbers
- **Technical Implementation**:
  - Tkinter-based GUI
  - Matplotlib integration for plotting
  - Optimized path generation
  - Responsive design

## Installation

1. **Requirements**:
   - Python 3.6+
   - Required packages:
     ```bash
     pip install matplotlib numpy
     ```
  Left Panel: Control parameters

Right Panel: Visualization canvas

Click "Generate" after parameter changes

Recommended Workflow:

Start with default values

Gradually increase complexity:

Start with 20 sequences, max_start=500

Progress to 100+ sequences, max_start=10,000

![image](https://github.com/user-attachments/assets/70f63748-bb3a-4421-8376-a875f95b1ac4)

Technical Details
Algorithm:

Randomly select even/odd starting numbers

Generate Collatz sequences:

Even: n → n/2

Odd: n → 3n + 1

Performance:

Optimized for 50-100 sequences

Depth 25-30 recommended for clarity

Larger values may reduce responsiveness
