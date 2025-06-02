# Aircraft Boarding Simulation

A comprehensive framework for simulating and analyzing aircraft boarding and disembarkation processes using mathematical modeling and computational techniques.

## Overview

This repository contains the implementation of mathematical models and simulation tools used to study passenger flow in aircraft boarding and disembarkation. The research aims to identify optimal strategies for minimizing aircraft turnaround time through scientific analysis.

## Key Features

- **Mathematical Models**: First-order differential equations with and without congestion effects
- **Computational Simulations**: Both continuous and discrete agent-based models
- **Visualization Tools**: Generate detailed diagrams of boarding strategies and passenger flow
- **Comparative Analysis**: Quantify and compare different boarding and disembarkation strategies

## Supported Boarding Strategies

1. **Random Boarding**: No specific order, passengers board as they arrive
2. **Back-to-Front**: Aircraft divided into zones from back to front
3. **Outside-In**: Window seats first, followed by middle, then aisle (regardless of row)
4. **Hybrid Strategy**: Combination of Back-to-Front and Outside-In approaches

## Disembarkation Strategies

1. **Front-to-Back**: Traditional approach with single door at the front
2. **Dual-Door**: Utilizing both front and rear doors
3. **Priority-Based**: Special consideration for connecting flights and premium passengers

## Getting Started

### Prerequisites

- Python 3.8+
- NumPy
- Matplotlib
- SciPy

### Installation

```bash
git clone https://github.com/syanhg/aircraft-boarding-simulation.git
cd aircraft-boarding-simulation
pip install -r requirements.txt
```

### Running Simulations

```python
# Basic simulation
python run_simulation.py --strategy back-to-front --passengers 126

# Generate visualizations
python generate_visualizations.py
```

## Research Findings

Our research demonstrates that:

- Back-to-Front boarding is approximately 2x more efficient than Random boarding
- Outside-In is about 1.6x more efficient than Random boarding
- Hybrid strategy offers about 1.4x improvement over Random boarding
- Dual-Door disembarkation reduces exit time by approximately 40%
- Combined optimal strategies can reduce total passenger processing time by 46%

## LaTeX Paper

The `updated_paper.tex` file contains the full academic paper detailing our methodology, mathematical models, and findings.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Based on research by Steffen (2008), Van den Briel et al. (2005), and others in the field of aircraft boarding optimization
- Inspired by real-world observations of aircraft boarding inefficiencies