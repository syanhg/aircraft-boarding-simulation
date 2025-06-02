#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run the aircraft boarding simulation and generate visualizations
"""

from boarding_simulation import Aircraft, PassengerParameters, save_all_figures
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    
    print("Aircraft Boarding Simulation")
    print("--------------------------")
    
    # Initialize Boeing 737-800 configuration (21 rows, 6 seats per row)
    aircraft = Aircraft(rows=21, seats_per_row=6)
    params = PassengerParameters()
    
    print(f"Aircraft: Boeing 737-800")
    print(f"Total passengers: {aircraft.total_passengers}")
    print(f"Running simulations...")
    
    start_time = time.time()
    
    # Generate and save all figures
    figures = save_all_figures(aircraft, params)
    
    end_time = time.time()
    print(f"Simulation complete. Time elapsed: {end_time - start_time:.2f} seconds")
    print(f"Generated figures:")
    print("- boarding_heatmaps.png: Visual representation of boarding order for each strategy")
    print("- strategy_comparison.png: Comparison of different boarding strategies")
    print("- boarding_times.png: Comparison of boarding times")
    print("- sensitivity_analysis.png: Sensitivity analysis of key parameters")
    
    # Display one of the figures as example
    plt.figure()
    plt.imshow(plt.imread('boarding_times.png'))
    plt.axis('off')
    plt.show()