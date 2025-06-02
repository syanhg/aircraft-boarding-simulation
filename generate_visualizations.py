#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate all visualizations for the paper
"""

from aircraft_seating_diagram import (create_aircraft_seating_diagram, 
                                    create_boarding_strategy_visualization,
                                    create_disembarkation_visualization,
                                    create_passenger_flow_visualization,
                                    create_3d_boarding_time_surface)
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    
    print("Generating visualizations for aircraft boarding paper...")
    start_time = time.time()
    
    # Create and save seating diagram
    print("Creating seating diagram...")
    seating_fig = create_aircraft_seating_diagram(rows=21, prestige_rows=3)
    seating_fig.savefig('boeing_737_800_seating.png', dpi=300, bbox_inches='tight')
    
    # Create and save boarding strategy visualization
    print("Creating boarding strategy visualization...")
    boarding_fig = create_boarding_strategy_visualization(rows=21, prestige_rows=3)
    boarding_fig.savefig('boarding_strategy_visualization.png', dpi=300, bbox_inches='tight')
    
    # Create and save disembarkation visualization
    print("Creating disembarkation visualization...")
    disembark_fig = create_disembarkation_visualization(rows=21, prestige_rows=3)
    disembark_fig.savefig('disembarkation_visualization.png', dpi=300, bbox_inches='tight')
    
    # Create and save passenger flow visualization
    print("Creating passenger flow visualization...")
    flow_fig = create_passenger_flow_visualization()
    flow_fig.savefig('passenger_flow_visualization.png', dpi=300, bbox_inches='tight')
    
    # Create and save 3D boarding time surface
    print("Creating 3D boarding time surface...")
    surface_fig = create_3d_boarding_time_surface()
    surface_fig.savefig('boarding_time_surface_3d.png', dpi=300, bbox_inches='tight')
    
    end_time = time.time()
    print(f"All visualizations created successfully! Time elapsed: {end_time - start_time:.2f} seconds")
    print("Files saved:")
    print("- boeing_737_800_seating.png")
    print("- boarding_strategy_visualization.png")
    print("- disembarkation_visualization.png")
    print("- passenger_flow_visualization.png")
    print("- boarding_time_surface_3d.png")
    
    # Display the diagrams
    plt.figure(figsize=(8, 8))
    plt.imshow(plt.imread('boeing_737_800_seating.png'))
    plt.axis('off')
    plt.title('Boeing 737-800 Seating Diagram')
    plt.show()