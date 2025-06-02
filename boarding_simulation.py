#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aircraft Boarding Simulation Model
----------------------------------
This script implements various boarding strategies and simulates their efficiency
using both differential equation models and discrete passenger simulations.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import time

# Define the aircraft parameters
class Aircraft:
    def __init__(self, rows=21, seats_per_row=6, aisle_width=1):
        """Initialize aircraft configuration"""
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.aisle_width = aisle_width
        self.total_passengers = rows * seats_per_row
        
        # For a Boeing 737-800, we have 3-3 configuration
        self.seat_layout = ['A', 'B', 'C', 'D', 'E', 'F']  # Window-Middle-Aisle-Aisle-Middle-Window
        
        # Categorize seats
        self.window_seats = ['A', 'F']
        self.middle_seats = ['B', 'E']
        self.aisle_seats = ['C', 'D']
        
        # Generate all seat positions
        self.all_seats = [(row, seat) for row in range(1, rows+1) 
                          for seat in self.seat_layout]

# Define passenger behavior parameters
class PassengerParameters:
    def __init__(self):
        """Initialize passenger behavior parameters"""
        # Time to store luggage (seconds) - normal distribution parameters
        self.luggage_time_mean = 12
        self.luggage_time_std = 4
        
        # Walking speed in aisle (rows per second)
        self.walking_speed_mean = 0.7
        self.walking_speed_std = 0.15
        
        # Interference delays (seconds)
        self.aisle_interference_time = 3.5  # When passengers block each other in aisle
        self.seat_interference_time = {
            'A': 5,  # Window seats take longer to access
            'B': 3,  # Middle seats
            'C': 0,  # Aisle seats
            'D': 0,  # Aisle seats
            'E': 3,  # Middle seats
            'F': 5   # Window seats
        }
        
        # Efficiency coefficient for various boarding strategies (min^-1)
        self.k_random = 0.10
        self.k_back_to_front = 0.22
        self.k_outside_in = 0.18
        self.k_hybrid = 0.15
        
        # Congestion parameter (min/passenger)
        self.alpha = 0.033

# First-order ODE models
class BoardingModels:
    def __init__(self, aircraft, params):
        """Initialize boarding models"""
        self.aircraft = aircraft
        self.params = params
    
    def basic_model(self, t, N, k):
        """Basic exponential decay model: dN/dt = -k*N"""
        return -k * N
    
    def congestion_model(self, t, N, k, alpha):
        """Model with congestion effects: dN/dt = -k*N*(1-C)
        where C = min(1, alpha*dN/dt)
        """
        # Calculate congestion factor
        C = min(1, alpha * k * N)
        return -k * N * (1 - C)
    
    def solve_basic_model(self, k, N0, t_span, t_eval=None):
        """Solve the basic model using solve_ivp"""
        solution = solve_ivp(
            lambda t, N: self.basic_model(t, N, k),
            t_span, [N0], t_eval=t_eval, method='RK45'
        )
        return solution.t, solution.y[0]
    
    def solve_congestion_model(self, k, alpha, N0, t_span, t_eval=None):
        """Solve the congestion model using solve_ivp"""
        solution = solve_ivp(
            lambda t, N: self.congestion_model(t, N, k, alpha),
            t_span, [N0], t_eval=t_eval, method='RK45'
        )
        return solution.t, solution.y[0]

# Boarding strategy implementations
class BoardingStrategies:
    def __init__(self, aircraft):
        """Initialize boarding strategies"""
        self.aircraft = aircraft
        
    def random_order(self):
        """Random boarding strategy: passengers board in random order"""
        boarding_order = self.aircraft.all_seats.copy()
        np.random.shuffle(boarding_order)
        return boarding_order
    
    def back_to_front(self, num_zones=3):
        """Back-to-front boarding: divide aircraft into zones from back to front"""
        # Create zones from back to front
        rows_per_zone = self.aircraft.rows // num_zones
        zones = {}
        
        for i in range(num_zones):
            if i < num_zones - 1:
                zone_rows = range(self.aircraft.rows - (i+1)*rows_per_zone + 1, 
                                  self.aircraft.rows - i*rows_per_zone + 1)
            else:
                # Last zone might have more rows
                zone_rows = range(1, self.aircraft.rows - i*rows_per_zone + 1)
            
            zones[i] = [(row, seat) for row in zone_rows 
                        for seat in self.aircraft.seat_layout]
        
        # Create boarding order by zones
        boarding_order = []
        for i in range(num_zones):
            zone_passengers = zones[i].copy()
            np.random.shuffle(zone_passengers)
            boarding_order.extend(zone_passengers)
            
        return boarding_order
    
    def outside_in(self):
        """Outside-in boarding: window seats first, then middle, then aisle"""
        # Group seats by type
        window_seats = [(row, seat) for row in range(1, self.aircraft.rows+1) 
                        for seat in self.aircraft.window_seats]
        middle_seats = [(row, seat) for row in range(1, self.aircraft.rows+1) 
                        for seat in self.aircraft.middle_seats]
        aisle_seats = [(row, seat) for row in range(1, self.aircraft.rows+1) 
                       for seat in self.aircraft.aisle_seats]
        
        # Shuffle each group internally
        np.random.shuffle(window_seats)
        np.random.shuffle(middle_seats)
        np.random.shuffle(aisle_seats)
        
        # Combine in the desired order
        boarding_order = window_seats + middle_seats + aisle_seats
        return boarding_order
    
    def hybrid_strategy(self, num_zones=3):
        """Hybrid strategy: combines back-to-front with outside-in"""
        # Create zones from back to front
        rows_per_zone = self.aircraft.rows // num_zones
        zones = {}
        
        for i in range(num_zones):
            if i < num_zones - 1:
                zone_rows = range(self.aircraft.rows - (i+1)*rows_per_zone + 1, 
                                  self.aircraft.rows - i*rows_per_zone + 1)
            else:
                # Last zone might have more rows
                zone_rows = range(1, self.aircraft.rows - i*rows_per_zone + 1)
            
            # Group by seat type within each zone
            window = [(row, seat) for row in zone_rows for seat in self.aircraft.window_seats]
            middle = [(row, seat) for row in zone_rows for seat in self.aircraft.middle_seats]
            aisle = [(row, seat) for row in zone_rows for seat in self.aircraft.aisle_seats]
            
            zones[i] = {
                'window': window,
                'middle': middle,
                'aisle': aisle
            }
        
        # Create boarding order
        boarding_order = []
        
        # First all window seats from back to front
        for i in range(num_zones):
            window_passengers = zones[i]['window'].copy()
            np.random.shuffle(window_passengers)
            boarding_order.extend(window_passengers)
        
        # Then all middle seats from back to front
        for i in range(num_zones):
            middle_passengers = zones[i]['middle'].copy()
            np.random.shuffle(middle_passengers)
            boarding_order.extend(middle_passengers)
        
        # Finally all aisle seats from back to front
        for i in range(num_zones):
            aisle_passengers = zones[i]['aisle'].copy()
            np.random.shuffle(aisle_passengers)
            boarding_order.extend(aisle_passengers)
            
        return boarding_order

# Discrete event simulation
class DiscreteSimulation:
    def __init__(self, aircraft, params):
        """Initialize the discrete event simulation"""
        self.aircraft = aircraft
        self.params = params
        
        # Initialize the aircraft seating grid
        self.grid = np.zeros((aircraft.rows, aircraft.seats_per_row))
        
        # Track passenger positions in the aisle (indexed by row)
        self.aisle = [None] * (aircraft.rows + 1)  # +1 for entry position
        
        # Track simulation metrics
        self.time_elapsed = 0
        self.seated_passengers = 0
        self.passengers_history = []  # Track remaining passengers over time
        
    def reset(self):
        """Reset the simulation state"""
        self.grid = np.zeros((self.aircraft.rows, self.aircraft.seats_per_row))
        self.aisle = [None] * (self.aircraft.rows + 1)
        self.time_elapsed = 0
        self.seated_passengers = 0
        self.passengers_history = []
        
    def seat_to_grid_position(self, seat):
        """Convert seat letter to grid position"""
        return self.aircraft.seat_layout.index(seat)
    
    def calculate_interference_delay(self, row, seat):
        """Calculate interference delay when accessing a seat"""
        seat_index = self.seat_to_grid_position(seat)
        delay = 0
        
        # For seats on the left side (A, B, C)
        if seat_index <= 2:
            for j in range(seat_index):
                if self.grid[row-1, j] == 1:  # If there's someone seated
                    delay += self.params.seat_interference_time[self.aircraft.seat_layout[j]]
        
        # For seats on the right side (D, E, F)
        else:
            for j in range(seat_index+1, self.aircraft.seats_per_row):
                if self.grid[row-1, j] == 1:  # If there's someone seated
                    delay += self.params.seat_interference_time[self.aircraft.seat_layout[j]]
        
        return delay
    
    def run_simulation(self, boarding_order, time_limit=120, time_step=1):
        """Run the discrete event simulation with the given boarding order"""
        self.reset()
        
        # Assign walking speeds and luggage times to passengers
        passenger_data = []
        for i, (row, seat) in enumerate(boarding_order):
            walking_speed = max(0.1, np.random.normal(
                self.params.walking_speed_mean, 
                self.params.walking_speed_std
            ))
            luggage_time = max(1, np.random.normal(
                self.params.luggage_time_mean, 
                self.params.luggage_time_std
            ))
            passenger_data.append({
                'id': i,
                'row': row,
                'seat': seat,
                'walking_speed': walking_speed,
                'luggage_time': luggage_time,
                'status': 'queue',  # queue, aisle, seated
                'current_position': 0,  # Row position in aisle (0 is entry)
                'time_to_next_action': 0  # Time until passenger can move again
            })
        
        # Main simulation loop
        while self.seated_passengers < len(passenger_data) and self.time_elapsed < time_limit:
            # Update passenger states
            for passenger in passenger_data:
                if passenger['status'] == 'queue' and self.aisle[0] is None:
                    # Passenger enters the aisle
                    passenger['status'] = 'aisle'
                    passenger['current_position'] = 0
                    self.aisle[0] = passenger['id']
                    passenger['time_to_next_action'] = 1 / passenger['walking_speed']
                
                elif passenger['status'] == 'aisle':
                    if passenger['time_to_next_action'] <= 0:
                        current_pos = passenger['current_position']
                        target_row = passenger['row']
                        
                        if current_pos == target_row:
                            # Passenger has reached their row
                            interference_delay = self.calculate_interference_delay(
                                target_row, passenger['seat']
                            )
                            
                            total_time = passenger['luggage_time'] + interference_delay
                            passenger['time_to_next_action'] = total_time
                            passenger['status'] = 'seating'
                        
                        elif current_pos < target_row and self.aisle[current_pos + 1] is None:
                            # Move forward in the aisle
                            self.aisle[current_pos] = None
                            passenger['current_position'] += 1
                            self.aisle[passenger['current_position']] = passenger['id']
                            passenger['time_to_next_action'] = 1 / passenger['walking_speed']
                    
                    else:
                        passenger['time_to_next_action'] -= time_step
                
                elif passenger['status'] == 'seating':
                    if passenger['time_to_next_action'] <= 0:
                        # Passenger takes their seat
                        row_idx = passenger['row'] - 1
                        seat_idx = self.seat_to_grid_position(passenger['seat'])
                        self.grid[row_idx, seat_idx] = 1
                        self.aisle[passenger['current_position']] = None
                        passenger['status'] = 'seated'
                        self.seated_passengers += 1
                    else:
                        passenger['time_to_next_action'] -= time_step
            
            # Record current state
            remaining = len(passenger_data) - self.seated_passengers
            self.passengers_history.append((self.time_elapsed, remaining))
            
            # Advance time
            self.time_elapsed += time_step
        
        # Convert history to numpy arrays
        times, remaining = zip(*self.passengers_history)
        return np.array(times), np.array(remaining)

# Simulation and analysis
def run_all_strategies_comparison(aircraft, params, n_simulations=10):
    """Run simulations for all strategies and compare results"""
    strategies = BoardingStrategies(aircraft)
    simulation = DiscreteSimulation(aircraft, params)
    models = BoardingModels(aircraft, params)
    
    # Define strategies to compare
    all_strategies = {
        'Random': (strategies.random_order, params.k_random),
        'Back-to-Front': (strategies.back_to_front, params.k_back_to_front),
        'Outside-In': (strategies.outside_in, params.k_outside_in),
        'Hybrid': (strategies.hybrid_strategy, params.k_hybrid)
    }
    
    results = {}
    
    for name, (strategy_func, k) in all_strategies.items():
        # Continuous model solution
        t_span = (0, 30)  # 0 to 30 minutes
        t_eval = np.linspace(0, 30, 300)  # 300 evaluation points
        
        # Basic model without congestion
        t_basic, n_basic = models.solve_basic_model(
            k, aircraft.total_passengers, t_span, t_eval
        )
        
        # Model with congestion
        t_congestion, n_congestion = models.solve_congestion_model(
            k, params.alpha, aircraft.total_passengers, t_span, t_eval
        )
        
        # Run discrete simulations
        discrete_times = []
        discrete_remaining = []
        boarding_times = []
        
        for _ in range(n_simulations):
            # Generate boarding order
            boarding_order = strategy_func()
            
            # Run simulation
            times, remaining = simulation.run_simulation(boarding_order)
            
            # Convert to minutes for consistency with continuous models
            times_min = times / 60
            
            discrete_times.append(times_min)
            discrete_remaining.append(remaining)
            
            # Calculate when boarding is complete (less than 5 passengers remaining)
            if np.any(remaining <= 5):
                complete_time = times_min[np.argmax(remaining <= 5)]
                boarding_times.append(complete_time)
        
        # Store results
        results[name] = {
            'continuous_basic': (t_basic, n_basic),
            'continuous_congestion': (t_congestion, n_congestion),
            'discrete_times': discrete_times,
            'discrete_remaining': discrete_remaining,
            'boarding_times': boarding_times,
            'mean_boarding_time': np.mean(boarding_times),
            'std_boarding_time': np.std(boarding_times)
        }
    
    return results

def generate_heatmap_data(aircraft, strategy_name):
    """Generate seating heatmap data showing the order of boarding"""
    strategies = BoardingStrategies(aircraft)
    
    if strategy_name == 'Random':
        boarding_order = strategies.random_order()
    elif strategy_name == 'Back-to-Front':
        boarding_order = strategies.back_to_front()
    elif strategy_name == 'Outside-In':
        boarding_order = strategies.outside_in()
    elif strategy_name == 'Hybrid':
        boarding_order = strategies.hybrid_strategy()
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    
    # Create heatmap data
    heatmap_data = np.zeros((aircraft.rows, len(aircraft.seat_layout)))
    
    for i, (row, seat) in enumerate(boarding_order):
        seat_idx = aircraft.seat_layout.index(seat)
        # Normalize boarding order to 0-1 range
        heatmap_data[row-1, seat_idx] = i / len(boarding_order)
    
    return heatmap_data

def plot_boarding_heatmaps(aircraft):
    """Plot heatmaps showing boarding order for different strategies"""
    strategies = ['Random', 'Back-to-Front', 'Outside-In', 'Hybrid']
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for i, strategy in enumerate(strategies):
        heatmap_data = generate_heatmap_data(aircraft, strategy)
        
        # Custom colormap from blue (early) to red (late)
        cmap = LinearSegmentedColormap.from_list('boarding_cmap', 
                                               ['#0000FF', '#00FFFF', '#FFFF00', '#FF0000'])
        
        im = axes[i].imshow(heatmap_data, cmap=cmap, aspect='auto')
        axes[i].set_title(f"{strategy} Strategy")
        axes[i].set_xlabel("Seat")
        axes[i].set_ylabel("Row")
        
        # Set y-ticks (rows)
        axes[i].set_yticks(np.arange(aircraft.rows))
        axes[i].set_yticklabels(np.arange(1, aircraft.rows+1))
        
        # Set x-ticks (seats)
        axes[i].set_xticks(np.arange(len(aircraft.seat_layout)))
        axes[i].set_xticklabels(aircraft.seat_layout)
        
        # Add colorbar
        plt.colorbar(im, ax=axes[i], label="Boarding Order (normalized)")
    
    plt.tight_layout()
    return fig

def plot_comparison_results(results):
    """Plot comparison of different boarding strategies"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.flatten()
    
    for i, (name, data) in enumerate(results.items()):
        # Plot continuous models
        t_basic, n_basic = data['continuous_basic']
        t_congestion, n_congestion = data['continuous_congestion']
        
        axes[i].plot(t_basic, n_basic, 'b-', linewidth=2, label='Basic Model')
        axes[i].plot(t_congestion, n_congestion, 'g-', linewidth=2, label='Congestion Model')
        
        # Plot discrete simulation results
        for j in range(len(data['discrete_times'])):
            if j == 0:  # Only add label for the first one
                axes[i].plot(data['discrete_times'][j], data['discrete_remaining'][j], 
                         'r-', alpha=0.3, label='Discrete Simulations')
            else:
                axes[i].plot(data['discrete_times'][j], data['discrete_remaining'][j], 
                         'r-', alpha=0.3)
        
        # Add annotations
        mean_time = data['mean_boarding_time']
        std_time = data['std_boarding_time']
        
        axes[i].axvline(x=mean_time, color='k', linestyle='--', alpha=0.7)
        axes[i].text(mean_time + 0.2, aircraft.total_passengers * 0.8, 
                 f'Mean: {mean_time:.2f} min\nStd: {std_time:.2f} min',
                 bbox=dict(facecolor='white', alpha=0.7))
        
        axes[i].set_title(f"{name} Strategy")
        axes[i].set_xlabel("Time (minutes)")
        axes[i].set_ylabel("Remaining Passengers")
        axes[i].set_xlim(0, 20)
        axes[i].set_ylim(0, aircraft.total_passengers * 1.05)
        axes[i].grid(True, alpha=0.3)
        axes[i].legend()
    
    plt.tight_layout()
    return fig

def plot_boarding_time_comparison(results):
    """Create a bar chart comparing boarding times"""
    strategies = list(results.keys())
    mean_times = [results[s]['mean_boarding_time'] for s in strategies]
    std_times = [results[s]['std_boarding_time'] for s in strategies]
    
    # Calculate relative efficiency compared to random
    random_time = results['Random']['mean_boarding_time']
    relative_efficiency = [random_time / time for time in mean_times]
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Bar chart for boarding times
    bars = ax1.bar(np.arange(len(strategies)), mean_times, yerr=std_times, 
                  capsize=5, color='skyblue', alpha=0.7)
    
    ax1.set_ylabel('Boarding Time (minutes)', color='blue')
    ax1.set_xlabel('Strategy')
    ax1.set_title('Comparison of Boarding Times Across Strategies')
    ax1.set_xticks(np.arange(len(strategies)))
    ax1.set_xticklabels(strategies)
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # Twin axis for relative efficiency
    ax2 = ax1.twinx()
    ax2.plot(np.arange(len(strategies)), relative_efficiency, 'ro-', linewidth=2)
    ax2.set_ylabel('Relative Efficiency (vs Random)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Add text annotations for the values
    for i, v in enumerate(mean_times):
        ax1.text(i, v + 0.2, f"{v:.2f}", ha='center', va='bottom', color='blue')
    
    for i, v in enumerate(relative_efficiency):
        ax2.text(i, v + 0.05, f"{v:.2f}x", ha='center', va='bottom', color='red')
    
    plt.tight_layout()
    return fig

def plot_sensitivity_analysis(aircraft, params):
    """Perform sensitivity analysis on key parameters"""
    models = BoardingModels(aircraft, params)
    t_span = (0, 30)
    t_eval = np.linspace(0, 30, 300)
    
    # Vary efficiency coefficient
    k_values = np.linspace(0.05, 0.3, 6)
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Effect of k on boarding time
    for k in k_values:
        t, n = models.solve_basic_model(k, aircraft.total_passengers, t_span, t_eval)
        axes[0].plot(t, n, label=f'k = {k:.2f}')
    
    axes[0].set_title('Effect of Efficiency Coefficient (k)')
    axes[0].set_xlabel('Time (minutes)')
    axes[0].set_ylabel('Remaining Passengers')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Vary congestion parameter
    alpha_values = np.linspace(0.01, 0.05, 5)
    k = 0.15  # Fixed k
    
    for alpha in alpha_values:
        t, n = models.solve_congestion_model(k, alpha, aircraft.total_passengers, t_span, t_eval)
        axes[1].plot(t, n, label=f'α = {alpha:.3f}')
    
    axes[1].set_title('Effect of Congestion Parameter (α)')
    axes[1].set_xlabel('Time (minutes)')
    axes[1].set_ylabel('Remaining Passengers')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def save_all_figures(aircraft, params):
    """Generate and save all figures for the paper"""
    # Run all simulations
    results = run_all_strategies_comparison(aircraft, params, n_simulations=5)
    
    # Create and save boarding heatmaps
    fig_heatmaps = plot_boarding_heatmaps(aircraft)
    fig_heatmaps.savefig('boarding_heatmaps.png', dpi=300, bbox_inches='tight')
    
    # Create and save comparison plots
    fig_comparison = plot_comparison_results(results)
    fig_comparison.savefig('strategy_comparison.png', dpi=300, bbox_inches='tight')
    
    # Create and save boarding time comparison
    fig_times = plot_boarding_time_comparison(results)
    fig_times.savefig('boarding_times.png', dpi=300, bbox_inches='tight')
    
    # Create and save sensitivity analysis
    fig_sensitivity = plot_sensitivity_analysis(aircraft, params)
    fig_sensitivity.savefig('sensitivity_analysis.png', dpi=300, bbox_inches='tight')
    
    return {
        'heatmaps': fig_heatmaps,
        'comparison': fig_comparison,
        'times': fig_times,
        'sensitivity': fig_sensitivity
    }

# Main execution
if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Initialize aircraft and parameters
    aircraft = Aircraft(rows=21, seats_per_row=6)  # Boeing 737-800 configuration
    params = PassengerParameters()
    
    # Generate and save all figures
    print("Generating figures...")
    figures = save_all_figures(aircraft, params)
    print("Figures saved successfully!")