#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aircraft Seating Diagram Generator
----------------------------------
This script generates detailed seating diagrams for the Boeing 737-800 aircraft
and visualizes various boarding strategies.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
import matplotlib.colors as mcolors

def create_aircraft_seating_diagram(rows=21, prestige_rows=3):
    """Create a detailed seating diagram for Boeing 737-800"""
    # Define dimensions
    seat_width = 1.0
    seat_height = 0.8
    aisle_width = 0.6
    row_spacing = 1.0
    
    # Define colors
    prestige_color = '#A0C8E8'  # Light blue
    economy_color = '#D8E8C8'   # Light green
    aisle_color = '#F0F0F0'     # Light gray
    
    # Create figure
    fig_width = seat_width * 6 + aisle_width + 2
    fig_height = row_spacing * rows + 2
    
    fig, ax = plt.subplots(figsize=(10, 15))
    
    # Draw aircraft outline
    outline_width = seat_width * 6 + aisle_width + 1.0
    outline_height = row_spacing * rows + 1.5
    
    # Draw fuselage
    fuselage_points = np.array([
        [0.5, 0.5],                                     # Bottom left
        [0.5, 0.5 + outline_height],                    # Top left
        [0.5 + outline_width/2, 0.5 + outline_height + 1.0],  # Top middle
        [0.5 + outline_width, 0.5 + outline_height],    # Top right
        [0.5 + outline_width, 0.5],                     # Bottom right
        [0.5, 0.5]                                      # Back to start
    ])
    
    # Draw the outline
    ax.add_patch(Polygon(fuselage_points, facecolor='#E8E8E8', edgecolor='black', linewidth=1.5))
    
    # Draw the wings
    wing_width = outline_width * 1.5
    wing_start_y = 0.5 + outline_height * 0.6
    wing_height = outline_height * 0.1
    
    left_wing_points = np.array([
        [0.5, wing_start_y],  # Right side
        [0.5, wing_start_y + wing_height],  # Right top
        [0.5 - wing_width/2, wing_start_y + wing_height/2],  # Left tip
        [0.5, wing_start_y]  # Back to start
    ])
    
    right_wing_points = np.array([
        [0.5 + outline_width, wing_start_y],  # Left side
        [0.5 + outline_width, wing_start_y + wing_height],  # Left top
        [0.5 + outline_width + wing_width/2, wing_start_y + wing_height/2],  # Right tip
        [0.5 + outline_width, wing_start_y]  # Back to start
    ])
    
    ax.add_patch(Polygon(left_wing_points, facecolor='#D0D0D0', edgecolor='black', linewidth=1.0))
    ax.add_patch(Polygon(right_wing_points, facecolor='#D0D0D0', edgecolor='black', linewidth=1.0))
    
    # Draw seats
    seat_labels = ['A', 'B', 'C', 'D', 'E', 'F']
    
    for row in range(rows):
        row_num = rows - row  # Start numbering from the front
        
        # Determine if this is a prestige class row
        is_prestige = row_num <= prestige_rows
        seat_color = prestige_color if is_prestige else economy_color
        
        # Draw row number
        ax.text(0.7, 1.0 + row * row_spacing + seat_height/2, 
                str(row_num), fontsize=8, ha='center', va='center')
        
        # Draw seats on left side (A, B, C)
        for i, seat_label in enumerate(seat_labels[:3]):
            x = 1.0 + i * seat_width
            y = 1.0 + row * row_spacing
            
            ax.add_patch(Rectangle((x, y), seat_width, seat_height, 
                                  facecolor=seat_color, edgecolor='black', linewidth=1.0))
            
            # Add seat label
            ax.text(x + seat_width/2, y + seat_height/2, 
                    f"{row_num}{seat_label}", fontsize=7, ha='center', va='center')
        
        # Draw aisle
        x_aisle = 1.0 + 3 * seat_width
        ax.add_patch(Rectangle((x_aisle, 1.0 + row * row_spacing), 
                              aisle_width, seat_height, 
                              facecolor=aisle_color, edgecolor='none'))
        
        # Draw seats on right side (D, E, F)
        for i, seat_label in enumerate(seat_labels[3:]):
            x = 1.0 + 3 * seat_width + aisle_width + i * seat_width
            y = 1.0 + row * row_spacing
            
            ax.add_patch(Rectangle((x, y), seat_width, seat_height, 
                                  facecolor=seat_color, edgecolor='black', linewidth=1.0))
            
            # Add seat label
            ax.text(x + seat_width/2, y + seat_height/2, 
                    f"{row_num}{seat_label}", fontsize=7, ha='center', va='center')
    
    # Draw front and rear exits
    exit_width = 0.8
    
    # Front exit
    front_exit_y = 1.0 + rows * row_spacing
    ax.add_patch(Rectangle((0.5, front_exit_y - 0.2), 
                          exit_width, 0.4, 
                          facecolor='red', edgecolor='black', linewidth=1.5))
    ax.text(0.5 + exit_width/2, front_exit_y, 
            "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
    
    ax.add_patch(Rectangle((0.5 + outline_width - exit_width, front_exit_y - 0.2), 
                          exit_width, 0.4, 
                          facecolor='red', edgecolor='black', linewidth=1.5))
    ax.text(0.5 + outline_width - exit_width/2, front_exit_y, 
            "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
    
    # Rear exit
    rear_exit_y = 0.5 + 0.2
    ax.add_patch(Rectangle((0.5, rear_exit_y - 0.2), 
                          exit_width, 0.4, 
                          facecolor='red', edgecolor='black', linewidth=1.5))
    ax.text(0.5 + exit_width/2, rear_exit_y, 
            "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
    
    ax.add_patch(Rectangle((0.5 + outline_width - exit_width, rear_exit_y - 0.2), 
                          exit_width, 0.4, 
                          facecolor='red', edgecolor='black', linewidth=1.5))
    ax.text(0.5 + outline_width - exit_width/2, rear_exit_y, 
            "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
    
    # Add legend for seat classes
    ax.add_patch(Rectangle((1.0, 0.1), seat_width, seat_height, 
                          facecolor=prestige_color, edgecolor='black', linewidth=1.0))
    ax.text(1.0 + seat_width + 0.2, 0.1 + seat_height/2, 
            "Prestige Class", fontsize=8, ha='left', va='center')
    
    ax.add_patch(Rectangle((1.0 + 4 * seat_width, 0.1), seat_width, seat_height, 
                          facecolor=economy_color, edgecolor='black', linewidth=1.0))
    ax.text(1.0 + 5 * seat_width + 0.2, 0.1 + seat_height/2, 
            "Economy Class", fontsize=8, ha='left', va='center')
    
    # Add title
    ax.text(0.5 + outline_width/2, 0.5 + outline_height + 1.3, 
            "Boeing 737-800 Seating Configuration", 
            fontsize=14, ha='center', va='center', weight='bold')
    
    ax.text(0.5 + outline_width/2, 0.5 + outline_height + 0.8, 
            "3-3 Configuration (126 seats)", 
            fontsize=10, ha='center', va='center')
    
    # Set axis limits
    ax.set_xlim(0, outline_width + 1)
    ax.set_ylim(0, outline_height + 2)
    
    # Remove axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('equal')
    
    return fig

def create_boarding_strategy_visualization(rows=21, prestige_rows=3):
    """Create visualizations of different boarding strategies"""
    # Define dimensions
    seat_width = 1.0
    seat_height = 0.8
    aisle_width = 0.6
    row_spacing = 1.0
    
    # Define colors
    prestige_color = '#A0C8E8'  # Light blue
    economy_color = '#D8E8C8'   # Light green
    
    # Create figure with 4 subplots for different strategies
    fig, axes = plt.subplots(2, 2, figsize=(15, 18))
    axes = axes.flatten()
    
    strategy_names = [
        "Random Boarding",
        "Back-to-Front Boarding",
        "Outside-In (Window-Middle-Aisle) Boarding",
        "Hybrid Strategy"
    ]
    
    for ax_idx, ax in enumerate(axes):
        # Draw aircraft outline
        outline_width = seat_width * 6 + aisle_width + 1.0
        outline_height = row_spacing * rows + 1.5
        
        # Draw simplified fuselage
        ax.add_patch(Rectangle((0.5, 0.5), outline_width, outline_height, 
                             facecolor='#E8E8E8', edgecolor='black', linewidth=1.5))
        
        # Draw seats
        seat_labels = ['A', 'B', 'C', 'D', 'E', 'F']
        
        # Create different boarding order patterns
        if ax_idx == 0:  # Random
            # Random boarding
            boarding_order = np.random.permutation(rows * len(seat_labels))
            boarding_order = boarding_order.reshape(rows, len(seat_labels))
            # Normalize to 0-1 range
            boarding_order = boarding_order / (rows * len(seat_labels))
        
        elif ax_idx == 1:  # Back-to-Front
            # Back-to-Front boarding
            boarding_order = np.zeros((rows, len(seat_labels)))
            for i in range(rows):
                boarding_order[i, :] = i / rows
        
        elif ax_idx == 2:  # Outside-In
            # Outside-In boarding (Window-Middle-Aisle)
            boarding_order = np.zeros((rows, len(seat_labels)))
            # Window seats
            boarding_order[:, 0] = 0.0  # A
            boarding_order[:, 5] = 0.0  # F
            # Middle seats
            boarding_order[:, 1] = 0.33  # B
            boarding_order[:, 4] = 0.33  # E
            # Aisle seats
            boarding_order[:, 2] = 0.67  # C
            boarding_order[:, 3] = 0.67  # D
            
            # Add small random variation within each group
            boarding_order += np.random.uniform(0, 0.2, size=boarding_order.shape)
            # Rescale to 0-1
            boarding_order = (boarding_order - boarding_order.min()) / (boarding_order.max() - boarding_order.min())
        
        else:  # Hybrid
            # Hybrid strategy - combination of Back-to-Front and Outside-In
            boarding_order = np.zeros((rows, len(seat_labels)))
            
            # Divide into 3 zones (back, middle, front)
            zone_rows = rows // 3
            
            # Back zone window seats
            boarding_order[:zone_rows, 0] = 0.0  # A
            boarding_order[:zone_rows, 5] = 0.0  # F
            
            # Middle zone window seats
            boarding_order[zone_rows:2*zone_rows, 0] = 0.11  # A
            boarding_order[zone_rows:2*zone_rows, 5] = 0.11  # F
            
            # Front zone window seats
            boarding_order[2*zone_rows:, 0] = 0.22  # A
            boarding_order[2*zone_rows:, 5] = 0.22  # F
            
            # Back zone middle seats
            boarding_order[:zone_rows, 1] = 0.33  # B
            boarding_order[:zone_rows, 4] = 0.33  # E
            
            # Middle zone middle seats
            boarding_order[zone_rows:2*zone_rows, 1] = 0.44  # B
            boarding_order[zone_rows:2*zone_rows, 4] = 0.44  # E
            
            # Front zone middle seats
            boarding_order[2*zone_rows:, 1] = 0.55  # B
            boarding_order[2*zone_rows:, 4] = 0.55  # E
            
            # Back zone aisle seats
            boarding_order[:zone_rows, 2] = 0.67  # C
            boarding_order[:zone_rows, 3] = 0.67  # D
            
            # Middle zone aisle seats
            boarding_order[zone_rows:2*zone_rows, 2] = 0.78  # C
            boarding_order[zone_rows:2*zone_rows, 3] = 0.78  # D
            
            # Front zone aisle seats
            boarding_order[2*zone_rows:, 2] = 0.89  # C
            boarding_order[2*zone_rows:, 3] = 0.89  # D
            
            # Add small random variation within each group
            boarding_order += np.random.uniform(0, 0.1, size=boarding_order.shape)
            # Rescale to 0-1
            boarding_order = (boarding_order - boarding_order.min()) / (boarding_order.max() - boarding_order.min())
        
        # Create colormap from blue (early) to red (late)
        cmap = plt.cm.coolwarm
        
        for row in range(rows):
            row_num = rows - row  # Start numbering from the front
            
            # Determine if this is a prestige class row
            is_prestige = row_num <= prestige_rows
            base_color = prestige_color if is_prestige else economy_color
            
            # Draw seats on left side (A, B, C)
            for i, seat_label in enumerate(seat_labels[:3]):
                x = 1.0 + i * seat_width
                y = 1.0 + row * row_spacing
                
                # Get boarding order value for this seat
                order_value = boarding_order[row, i]
                
                # Mix base color with boarding order color
                order_color = cmap(order_value)
                mixed_color = mcolors.to_rgba(base_color, 0.5) + np.array(mcolors.to_rgba(order_color, 0.5)) * 0.8
                mixed_color = np.clip(mixed_color, 0, 1)
                
                ax.add_patch(Rectangle((x, y), seat_width, seat_height, 
                                     facecolor=mixed_color, edgecolor='black', linewidth=0.5))
                
                # Add seat label
                ax.text(x + seat_width/2, y + seat_height/2, 
                        f"{row_num}{seat_label}", fontsize=6, ha='center', va='center')
            
            # Draw aisle
            x_aisle = 1.0 + 3 * seat_width
            ax.add_patch(Rectangle((x_aisle, 1.0 + row * row_spacing), 
                                 aisle_width, seat_height, 
                                 facecolor='#F0F0F0', edgecolor='none'))
            
            # Draw seats on right side (D, E, F)
            for i, seat_label in enumerate(seat_labels[3:]):
                x = 1.0 + 3 * seat_width + aisle_width + i * seat_width
                y = 1.0 + row * row_spacing
                
                # Get boarding order value for this seat
                order_value = boarding_order[row, i+3]
                
                # Mix base color with boarding order color
                order_color = cmap(order_value)
                mixed_color = mcolors.to_rgba(base_color, 0.5) + np.array(mcolors.to_rgba(order_color, 0.5)) * 0.8
                mixed_color = np.clip(mixed_color, 0, 1)
                
                ax.add_patch(Rectangle((x, y), seat_width, seat_height, 
                                     facecolor=mixed_color, edgecolor='black', linewidth=0.5))
                
                # Add seat label
                ax.text(x + seat_width/2, y + seat_height/2, 
                        f"{row_num}{seat_label}", fontsize=6, ha='center', va='center')
        
        # Draw front and rear exits
        exit_width = 0.8
        
        # Front exit
        front_exit_y = 1.0 + rows * row_spacing
        ax.add_patch(Rectangle((0.5, front_exit_y - 0.2), 
                             exit_width, 0.4, 
                             facecolor='red', edgecolor='black', linewidth=1.5))
        ax.text(0.5 + exit_width/2, front_exit_y, 
                "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
        
        ax.add_patch(Rectangle((0.5 + outline_width - exit_width, front_exit_y - 0.2), 
                             exit_width, 0.4, 
                             facecolor='red', edgecolor='black', linewidth=1.5))
        ax.text(0.5 + outline_width - exit_width/2, front_exit_y, 
                "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
        
        # Rear exit
        rear_exit_y = 0.5 + 0.2
        ax.add_patch(Rectangle((0.5, rear_exit_y - 0.2), 
                             exit_width, 0.4, 
                             facecolor='red', edgecolor='black', linewidth=1.5))
        ax.text(0.5 + exit_width/2, rear_exit_y, 
                "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
        
        ax.add_patch(Rectangle((0.5 + outline_width - exit_width, rear_exit_y - 0.2), 
                             exit_width, 0.4, 
                             facecolor='red', edgecolor='black', linewidth=1.5))
        ax.text(0.5 + outline_width - exit_width/2, rear_exit_y, 
                "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
        
        # Add title
        ax.set_title(strategy_names[ax_idx], fontsize=12)
        
        # Add colorbar to show boarding sequence
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Boarding Sequence')
        
        # Set axis limits
        ax.set_xlim(0, outline_width + 1)
        ax.set_ylim(0, outline_height + 1)
        
        # Remove axis ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    fig.suptitle("Boeing 737-800 Boarding Strategy Visualizations", fontsize=16)
    
    return fig

def create_disembarkation_visualization(rows=21, prestige_rows=3):
    """Create visualizations of different disembarkation strategies"""
    # Define dimensions
    seat_width = 1.0
    seat_height = 0.8
    aisle_width = 0.6
    row_spacing = 1.0
    
    # Create figure with 3 subplots for different strategies
    fig, axes = plt.subplots(1, 3, figsize=(18, 12))
    axes = axes.flatten()
    
    strategy_names = [
        "Front-to-Back (Single Door)",
        "Dual-Door Disembarkation",
        "Priority-Based Disembarkation"
    ]
    
    for ax_idx, ax in enumerate(axes):
        # Draw aircraft outline
        outline_width = seat_width * 6 + aisle_width + 1.0
        outline_height = row_spacing * rows + 1.5
        
        # Draw simplified fuselage
        ax.add_patch(Rectangle((0.5, 0.5), outline_width, outline_height, 
                             facecolor='#E8E8E8', edgecolor='black', linewidth=1.5))
        
        # Draw seats
        seat_labels = ['A', 'B', 'C', 'D', 'E', 'F']
        
        # Create different disembarkation order patterns
        if ax_idx == 0:  # Front-to-Back (Single Door)
            # Front-to-Back disembarkation
            disembark_order = np.zeros((rows, len(seat_labels)))
            for i in range(rows):
                # Start from front
                disembark_order[i, :] = i / rows
        
        elif ax_idx == 1:  # Dual-Door
            # Dual-Door disembarkation
            disembark_order = np.zeros((rows, len(seat_labels)))
            half_rows = rows // 2
            
            # Front half exits through front door
            for i in range(half_rows):
                disembark_order[i, :] = i / half_rows
                
            # Rear half exits through rear door
            for i in range(half_rows, rows):
                disembark_order[i, :] = (rows - i - 1) / half_rows
        
        else:  # Priority-Based
            # Priority-Based disembarkation
            disembark_order = np.ones((rows, len(seat_labels)))
            
            # Priority 1: First class passengers (first few rows)
            disembark_order[:prestige_rows, :] = 0.0
            
            # Priority 2: Passengers with connecting flights (randomly distributed)
            connecting_flight_rows = np.random.choice(
                range(prestige_rows, rows), size=rows//5, replace=False
            )
            disembark_order[connecting_flight_rows, :] = 0.33
            
            # Priority 3: Everyone else (front to back)
            # Find rows that are not priority 1 or 2
            remaining_rows = np.array([
                i for i in range(rows) 
                if i >= prestige_rows and i not in connecting_flight_rows
            ])
            
            # Assign remaining rows with front-to-back priority
            for i, row in enumerate(remaining_rows):
                disembark_order[row, :] = 0.67 + 0.33 * (i / len(remaining_rows))
        
        # Create colormap from blue (early) to red (late)
        cmap = plt.cm.coolwarm
        
        for row in range(rows):
            row_num = rows - row  # Start numbering from the front
            
            # Draw seats on left side (A, B, C)
            for i, seat_label in enumerate(seat_labels[:3]):
                x = 1.0 + i * seat_width
                y = 1.0 + row * row_spacing
                
                # Get disembarkation order value for this seat
                order_value = disembark_order[row, i]
                
                # Get color from colormap
                color = cmap(order_value)
                
                ax.add_patch(Rectangle((x, y), seat_width, seat_height, 
                                     facecolor=color, edgecolor='black', linewidth=0.5))
                
                # Add seat label
                ax.text(x + seat_width/2, y + seat_height/2, 
                        f"{row_num}{seat_label}", fontsize=6, ha='center', va='center')
            
            # Draw aisle
            x_aisle = 1.0 + 3 * seat_width
            ax.add_patch(Rectangle((x_aisle, 1.0 + row * row_spacing), 
                                 aisle_width, seat_height, 
                                 facecolor='#F0F0F0', edgecolor='none'))
            
            # Draw seats on right side (D, E, F)
            for i, seat_label in enumerate(seat_labels[3:]):
                x = 1.0 + 3 * seat_width + aisle_width + i * seat_width
                y = 1.0 + row * row_spacing
                
                # Get disembarkation order value for this seat
                order_value = disembark_order[row, i+3]
                
                # Get color from colormap
                color = cmap(order_value)
                
                ax.add_patch(Rectangle((x, y), seat_width, seat_height, 
                                     facecolor=color, edgecolor='black', linewidth=0.5))
                
                # Add seat label
                ax.text(x + seat_width/2, y + seat_height/2, 
                        f"{row_num}{seat_label}", fontsize=6, ha='center', va='center')
        
        # Draw front and rear exits
        exit_width = 0.8
        
        # Front exit
        front_exit_y = 1.0 + rows * row_spacing
        ax.add_patch(Rectangle((0.5, front_exit_y - 0.2), 
                             exit_width, 0.4, 
                             facecolor='red', edgecolor='black', linewidth=1.5))
        ax.text(0.5 + exit_width/2, front_exit_y, 
                "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
        
        ax.add_patch(Rectangle((0.5 + outline_width - exit_width, front_exit_y - 0.2), 
                             exit_width, 0.4, 
                             facecolor='red', edgecolor='black', linewidth=1.5))
        ax.text(0.5 + outline_width - exit_width/2, front_exit_y, 
                "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
        
        # Rear exit
        rear_exit_y = 0.5 + 0.2
        ax.add_patch(Rectangle((0.5, rear_exit_y - 0.2), 
                             exit_width, 0.4, 
                             facecolor='red', edgecolor='black', linewidth=1.5))
        ax.text(0.5 + exit_width/2, rear_exit_y, 
                "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
        
        ax.add_patch(Rectangle((0.5 + outline_width - exit_width, rear_exit_y - 0.2), 
                             exit_width, 0.4, 
                             facecolor='red', edgecolor='black', linewidth=1.5))
        ax.text(0.5 + outline_width - exit_width/2, rear_exit_y, 
                "EXIT", fontsize=8, ha='center', va='center', color='white', weight='bold')
        
        # Add annotations for disembarkation strategy
        if ax_idx == 0:
            # Front-to-Back
            ax.arrow(outline_width/2 + 0.5, front_exit_y - 0.5, 0, -2, 
                   head_width=0.3, head_length=0.5, fc='black', ec='black', linewidth=1.5)
            ax.text(outline_width/2 + 1.2, front_exit_y - 1.5, 
                    "Disembarkation\nDirection", fontsize=10, ha='center', va='center')
            
        elif ax_idx == 1:
            # Dual-Door
            # Front half arrow
            ax.arrow(outline_width/2 + 0.5, front_exit_y - 0.5, 0, -2, 
                   head_width=0.3, head_length=0.5, fc='blue', ec='blue', linewidth=1.5)
            ax.text(outline_width/2 + 1.2, front_exit_y - 1.5, 
                    "Front Half\nExits", fontsize=10, ha='center', va='center', color='blue')
            
            # Rear half arrow
            ax.arrow(outline_width/2 + 0.5, rear_exit_y + 0.5, 0, 2, 
                   head_width=0.3, head_length=0.5, fc='green', ec='green', linewidth=1.5)
            ax.text(outline_width/2 + 1.2, rear_exit_y + 1.5, 
                    "Rear Half\nExits", fontsize=10, ha='center', va='center', color='green')
            
        else:
            # Priority-Based
            # First class
            ax.text(0.6, 1.0 + (rows - 1) * row_spacing, 
                    "Priority 1:\nFirst Class", fontsize=8, ha='left', va='center',
                    bbox=dict(facecolor='gold', alpha=0.5))
            
            # Connecting flights
            ax.text(0.6, 1.0 + rows * row_spacing / 2, 
                    "Priority 2:\nConnecting Flights", fontsize=8, ha='left', va='center',
                    bbox=dict(facecolor='silver', alpha=0.5))
            
            # Regular passengers
            ax.text(0.6, 1.0 + rows * row_spacing / 4, 
                    "Priority 3:\nOther Passengers", fontsize=8, ha='left', va='center',
                    bbox=dict(facecolor='#D0D0D0', alpha=0.5))
        
        # Add title
        ax.set_title(strategy_names[ax_idx], fontsize=12)
        
        # Add colorbar to show disembarkation sequence
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 1))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('Disembarkation Sequence')
        
        # Set axis limits
        ax.set_xlim(0, outline_width + 1)
        ax.set_ylim(0, outline_height + 1)
        
        # Remove axis ticks and labels
        ax.set_xticks([])
        ax.set_yticks([])
        
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    fig.suptitle("Boeing 737-800 Disembarkation Strategy Visualizations", fontsize=16)
    
    return fig

def create_passenger_flow_visualization():
    """Create visualization of passenger flow and congestion effects"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()
    
    # 1. Passenger Flow Rate vs. Time
    t = np.linspace(0, 25, 250)
    
    # Different boarding strategies
    flow_random = 12.6 * np.exp(-0.1 * t) * (1 - 0.5 * np.exp(-0.2 * t))
    flow_back_to_front = 27.7 * np.exp(-0.22 * t) * (1 - 0.3 * np.exp(-0.3 * t))
    flow_outside_in = 22.7 * np.exp(-0.18 * t) * (1 - 0.4 * np.exp(-0.25 * t))
    flow_hybrid = 18.9 * np.exp(-0.15 * t) * (1 - 0.35 * np.exp(-0.28 * t))
    
    axes[0].plot(t, flow_random, 'r-', label='Random')
    axes[0].plot(t, flow_back_to_front, 'g-', label='Back-to-Front')
    axes[0].plot(t, flow_outside_in, 'b-', label='Outside-In')
    axes[0].plot(t, flow_hybrid, 'y-', label='Hybrid')
    
    axes[0].set_title('Passenger Flow Rate vs. Time')
    axes[0].set_xlabel('Time (minutes)')
    axes[0].set_ylabel('Flow Rate (passengers/minute)')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    
    # 2. Congestion Factor vs. Time
    congestion_random = 1 - np.exp(-0.15 * t)
    congestion_back_to_front = (1 - np.exp(-0.4 * t)) * np.exp(-0.1 * t)
    congestion_outside_in = (1 - np.exp(-0.3 * t)) * np.exp(-0.15 * t)
    congestion_hybrid = (1 - np.exp(-0.25 * t)) * np.exp(-0.12 * t)
    
    axes[1].plot(t, congestion_random, 'r-', label='Random')
    axes[1].plot(t, congestion_back_to_front, 'g-', label='Back-to-Front')
    axes[1].plot(t, congestion_outside_in, 'b-', label='Outside-In')
    axes[1].plot(t, congestion_hybrid, 'y-', label='Hybrid')
    
    axes[1].set_title('Congestion Factor vs. Time')
    axes[1].set_xlabel('Time (minutes)')
    axes[1].set_ylabel('Congestion Factor (0-1)')
    axes[1].grid(True, alpha=0.3)
    axes[1].legend()
    
    # 3. Sensitivity to Passenger Parameters
    k_values = np.linspace(0.1, 0.3, 100)
    boarding_times_random = np.log(126) / k_values
    
    luggage_factors = np.linspace(0.8, 1.2, 100)
    boarding_times_luggage = np.log(126) / 0.15 * luggage_factors
    
    ax3 = axes[2]
    ax3.plot(k_values, boarding_times_random, 'b-', label='Efficiency Coefficient (k)')
    ax3_twin = ax3.twiny()
    ax3_twin.plot(luggage_factors, boarding_times_luggage, 'r-', label='Luggage Factor')
    
    ax3.set_title('Sensitivity to Passenger Parameters')
    ax3.set_xlabel('Efficiency Coefficient (k)')
    ax3.set_ylabel('Boarding Time (minutes)')
    ax3.grid(True, alpha=0.3)
    ax3_twin.set_xlabel('Luggage Factor', color='red')
    ax3_twin.tick_params(axis='x', colors='red')
    
    # Add both legends
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3_twin.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    # 4. Aisle Density Simulation
    # X-axis is position along the aircraft (rows)
    row_positions = np.arange(1, rows+1)
    
    # Create different density patterns at different time points
    t1_density = 0.8 * np.exp(-0.1 * (row_positions - 1))  # Early boarding
    t2_density = 0.6 * np.exp(-0.1 * (row_positions - 5))  # Mid boarding
    t3_density = 0.4 * np.exp(-0.1 * (row_positions - 10))  # Later boarding
    t4_density = 0.2 * np.exp(-0.1 * (row_positions - 15))  # End of boarding
    
    axes[3].plot(row_positions, t1_density, 'r-', label='T=2 min')
    axes[3].plot(row_positions, t2_density, 'g-', label='T=8 min')
    axes[3].plot(row_positions, t3_density, 'b-', label='T=15 min')
    axes[3].plot(row_positions, t4_density, 'y-', label='T=20 min')
    
    axes[3].set_title('Aisle Density During Boarding')
    axes[3].set_xlabel('Row Position (Front to Back)')
    axes[3].set_ylabel('Passenger Density in Aisle')
    axes[3].grid(True, alpha=0.3)
    axes[3].legend()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    fig.suptitle("Passenger Flow Dynamics Visualization", fontsize=16)
    
    return fig

def create_3d_boarding_time_surface():
    """Create 3D surface plot showing boarding time as a function of k and alpha"""
    # Create arrays for k and alpha values
    k_values = np.linspace(0.05, 0.30, 30)
    alpha_values = np.linspace(0.01, 0.05, 30)
    
    # Create meshgrid
    K, A = np.meshgrid(k_values, alpha_values)
    
    # Calculate boarding time using simplified model that accounts for congestion
    # T = ln(N)/k * (1 + alpha*k*N/2)
    N0 = 126  # Number of passengers
    T = np.log(N0) / K * (1 + A * K * N0 / 2)
    
    # Create figure
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Create surface plot
    surf = ax.plot_surface(K, A, T, cmap='viridis', alpha=0.8, 
                          rstride=1, cstride=1, linewidth=0, antialiased=True)
    
    # Add contour lines on the bottom
    cset = ax.contour(K, A, T, zdir='z', offset=0, cmap='viridis')
    
    # Mark specific boarding strategies
    strategies = {
        'Random': (0.10, 0.035, 25.3),
        'Back-to-Front': (0.22, 0.032, 12.1),
        'Outside-In': (0.18, 0.030, 15.3),
        'Hybrid': (0.15, 0.028, 18.2)
    }
    
    for name, (k, alpha, t) in strategies.items():
        ax.scatter([k], [alpha], [t], color='red', s=50, label=name)
        ax.text(k, alpha, t+1, name, fontsize=10)
    
    # Set labels and title
    ax.set_xlabel('Efficiency Coefficient (k)')
    ax.set_ylabel('Congestion Parameter (α)')
    ax.set_zlabel('Boarding Time (minutes)')
    ax.set_title('Boarding Time as a Function of Efficiency and Congestion Parameters')
    
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    return fig

if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    
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
    
    print("All visualizations created successfully!")