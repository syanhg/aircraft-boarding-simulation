#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aircraft Boarding Simulation - Interactive Visualization Component
=================================================================

This module provides an interactive web-based visualization for the 
aircraft boarding simulation, allowing users to:
1. Select and compare different boarding strategies
2. Visualize the boarding process in real-time
3. Analyze the results of the simulations
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
import json
from typing import Dict, List, Tuple, Any, Optional
import os
import flask
from flask import Flask, render_template, request, jsonify
import threading
import webbrowser

from simulation import Aircraft, Simulation, BoardingStrategy, Passenger

class SimulationVisualizer:
    """Class for creating and managing visualizations of boarding simulations"""
    
    def __init__(self, simulation: Simulation):
        """
        Initialize the visualizer with a simulation instance
        
        Args:
            simulation: The simulation to visualize
        """
        self.simulation = simulation
        self.aircraft = simulation.aircraft
        self.fig = None
        self.ax = None
        self.grid = None
        self.aisle_positions = []
        
    def setup_visualization(self):
        """Set up the visualization components"""
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.ax.set_xlim(-1, self.aircraft.seats_per_row)
        self.ax.set_ylim(-1, self.aircraft.rows)
        
        # Create grid for aircraft layout
        self.grid = np.zeros((self.aircraft.rows, self.aircraft.seats_per_row))
        
        # Plot aircraft outline
        self.ax.set_xticks(np.arange(0, self.aircraft.seats_per_row, 1))
        self.ax.set_yticks(np.arange(0, self.aircraft.rows, 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.grid(True, color='black', linewidth=0.5)
        
        # Create color map
        colors = [(0.9, 0.9, 0.9), (0.1, 0.5, 0.8)]
        cmap = LinearSegmentedColormap.from_list('custom_cmap', colors, N=100)
        
        # Initial plot
        self.im = self.ax.imshow(self.grid, cmap=cmap, vmin=0, vmax=2)
        self.aisle_positions = []
        
        # Add title
        self.ax.set_title(f"Aircraft Boarding Simulation: {self.simulation.strategy.value} strategy")
        
    def update_visualization(self, queue: List[Passenger], aisle: List[Passenger], frame: int):
        """
        Update the visualization for the current simulation state
        
        Args:
            queue: Passengers waiting to board
            aisle: Passengers in the aisle
            frame: Current animation frame number
        """
        # Reset grid
        self.grid = np.zeros((self.aircraft.rows, self.aircraft.seats_per_row))
        
        # Update seated passengers
        for passenger in self.simulation.passengers:
            if passenger.boarded:
                self.grid[passenger.row, passenger.seat] = 2
                
        # Clear previous aisle positions
        for row, col in self.aisle_positions:
            if 0 <= row < self.aircraft.rows and col == -1:
                # Draw aisle as white
                self.ax.plot(col + 0.5, row + 0.5, 'w.', markersize=10)
                
        # Update passengers in aisle
        self.aisle_positions = []
        for passenger in aisle:
            if 0 <= passenger.position < self.aircraft.rows:
                self.aisle_positions.append((passenger.position, -1))
                # Draw passenger in aisle as a red dot
                self.ax.plot(-0.5, passenger.position + 0.5, 'ro', markersize=10)
                
        # Update grid visualization
        self.im.set_array(self.grid)
        
        # Add status text
        seated = len(self.simulation.passengers) - len(queue) - len(aisle)
        self.ax.set_xlabel(f"Time: {frame}s | Seated: {seated}/{len(self.simulation.passengers)}")
        
        return [self.im]
        
    def create_animation(self, save_path: Optional[str] = None):
        """
        Create an animation of the boarding process
        
        Args:
            save_path: Optional path to save the animation
            
        Returns:
            Matplotlib animation object
        """
        self.setup_visualization()
        
        # Queue of passengers waiting to board
        queue = self.simulation.passengers.copy()
        
        # Passengers in the aisle
        aisle = []
        
        def animate(frame):
            """Animation function called for each frame"""
            # Skip frames to speed up animation
            for _ in range(3):  # Adjust this value to control animation speed
                if queue or aisle:
                    self.simulation.update_passengers(queue, aisle)
                    
            return self.update_visualization(queue, aisle, frame)
            
        # Create animation
        anim = animation.FuncAnimation(
            self.fig, animate, frames=1000, 
            interval=50, blit=True, repeat=False)
            
        if save_path:
            anim.save(save_path, writer='pillow', fps=20)
            
        plt.tight_layout()
        return anim
        
    def show(self):
        """Display the visualization"""
        plt.show()
        
class InteractiveVisualizer:
    """Flask-based interactive visualization server"""
    
    def __init__(self, port: int = 5000):
        """
        Initialize the interactive visualization server
        
        Args:
            port: Port number for the web server
        """
        self.app = Flask(__name__)
        self.port = port
        self.setup_routes()
        
    def setup_routes(self):
        """Set up Flask routes for the application"""
        
        @self.app.route('/')
        def index():
            """Render the main application page"""
            return render_template('index.html')
        
        @self.app.route('/api/run_simulation', methods=['POST'])
        def run_simulation():
            """API endpoint to run a simulation with the specified parameters"""
            params = request.json
            
            # Create aircraft
            rows = int(params.get('rows', 32))
            seats_per_row = int(params.get('seats_per_row', 6))
            aircraft = Aircraft(rows=rows, seats_per_row=seats_per_row)
            
            # Create simulation with the requested strategy
            strategy_name = params.get('strategy', 'random')
            strategy = BoardingStrategy(strategy_name)
            simulation = Simulation(aircraft, strategy)
            
            # Run simulation and collect data
            queue = simulation.passengers.copy()
            aisle = []
            time_steps = []
            seated_counts = []
            aisle_counts = []
            
            max_steps = 1000
            for step in range(max_steps):
                simulation.update_passengers(queue, aisle)
                
                # Record data
                time_steps.append(step)
                seated_counts.append(len(simulation.passengers) - len(queue) - len(aisle))
                aisle_counts.append(len(aisle))
                
                # Check if simulation is complete
                if not queue and not aisle:
                    break
            
            # Prepare results
            results = {
                'time_steps': time_steps,
                'seated_counts': seated_counts,
                'aisle_counts': aisle_counts,
                'total_time': len(time_steps),
                'total_passengers': len(simulation.passengers)
            }
            
            return jsonify(results)
            
        @self.app.route('/api/compare_strategies', methods=['POST'])
        def compare_strategies():
            """API endpoint to compare multiple boarding strategies"""
            params = request.json
            
            # Create aircraft
            rows = int(params.get('rows', 32))
            seats_per_row = int(params.get('seats_per_row', 6))
            aircraft = Aircraft(rows=rows, seats_per_row=seats_per_row)
            
            # Run simulation for each strategy
            results = {}
            for strategy in BoardingStrategy:
                simulation = Simulation(aircraft, strategy)
                queue = simulation.passengers.copy()
                aisle = []
                
                step = 0
                max_steps = 1000
                while (queue or aisle) and step < max_steps:
                    simulation.update_passengers(queue, aisle)
                    step += 1
                
                results[strategy.value] = step
            
            return jsonify(results)
            
    def create_template_directory(self):
        """Create the template directory and HTML file for the Flask app"""
        # Create templates directory if it doesn't exist
        if not os.path.exists('templates'):
            os.makedirs('templates')
            
        # Create index.html template
        with open('templates/index.html', 'w') as f:
            f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aircraft Boarding Simulation</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
        }
        .controls {
            flex: 1;
            min-width: 300px;
            padding: 15px;
            background: #f5f5f5;
            border-radius: 5px;
        }
        .results {
            flex: 2;
            min-width: 400px;
        }
        .chart-container {
            margin-top: 20px;
            position: relative;
            height: 400px;
        }
        button {
            padding: 10px;
            margin-top: 10px;
            background: #0066cc;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background: #0055aa;
        }
        select, input {
            padding: 8px;
            margin: 5px 0;
            width: 100%;
        }
        h1, h2 {
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 20px;
        }
        .comparison-results {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Aircraft Boarding Simulation</h1>
    
    <div class="container">
        <div class="controls">
            <h2>Simulation Controls</h2>
            <div class="form-group">
                <label for="strategy">Boarding Strategy:</label>
                <select id="strategy">
                    <option value="random">Random</option>
                    <option value="back-to-front">Back-to-Front</option>
                    <option value="outside-in">Outside-In</option>
                    <option value="hybrid">Hybrid</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="rows">Number of Rows:</label>
                <input type="number" id="rows" value="32" min="10" max="60">
            </div>
            
            <div class="form-group">
                <label for="seats_per_row">Seats per Row:</label>
                <input type="number" id="seats_per_row" value="6" min="3" max="10">
            </div>
            
            <button id="run_simulation">Run Simulation</button>
            <button id="compare_strategies">Compare All Strategies</button>
            
            <div class="loading" id="loading">
                <p>Running simulation...</p>
            </div>
        </div>
        
        <div class="results">
            <h2>Simulation Results</h2>
            <div class="chart-container">
                <canvas id="boarding_chart"></canvas>
            </div>
            
            <div class="comparison-results" id="comparison_results" style="display: none;">
                <h3>Strategy Comparison</h3>
                <div class="chart-container">
                    <canvas id="comparison_chart"></canvas>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        // Initialize charts
        let boardingChart = null;
        let comparisonChart = null;
        
        // Run single simulation
        document.getElementById('run_simulation').addEventListener('click', async () => {
            const strategy = document.getElementById('strategy').value;
            const rows = document.getElementById('rows').value;
            const seats_per_row = document.getElementById('seats_per_row').value;
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('comparison_results').style.display = 'none';
            
            try {
                const response = await fetch('/api/run_simulation', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ strategy, rows, seats_per_row })
                });
                
                const data = await response.json();
                displayResults(data, strategy);
            } catch (error) {
                console.error('Error running simulation:', error);
                alert('Error running simulation. Check console for details.');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        // Compare all strategies
        document.getElementById('compare_strategies').addEventListener('click', async () => {
            const rows = document.getElementById('rows').value;
            const seats_per_row = document.getElementById('seats_per_row').value;
            
            document.getElementById('loading').style.display = 'block';
            
            try {
                const response = await fetch('/api/compare_strategies', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ rows, seats_per_row })
                });
                
                const data = await response.json();
                displayComparison(data);
            } catch (error) {
                console.error('Error comparing strategies:', error);
                alert('Error comparing strategies. Check console for details.');
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        function displayResults(data, strategy) {
            const ctx = document.getElementById('boarding_chart').getContext('2d');
            
            if (boardingChart) {
                boardingChart.destroy();
            }
            
            boardingChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.time_steps,
                    datasets: [
                        {
                            label: 'Passengers Seated',
                            data: data.seated_counts,
                            borderColor: 'rgb(75, 192, 192)',
                            tension: 0.1,
                            fill: false
                        },
                        {
                            label: 'Passengers in Aisle',
                            data: data.aisle_counts,
                            borderColor: 'rgb(255, 99, 132)',
                            tension: 0.1,
                            fill: false
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: `${strategy} Boarding Strategy (Total time: ${data.total_time}s)`
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: data.total_passengers
                        }
                    }
                }
            });
        }
        
        function displayComparison(data) {
            document.getElementById('comparison_results').style.display = 'block';
            
            const ctx = document.getElementById('comparison_chart').getContext('2d');
            const strategies = Object.keys(data);
            const times = Object.values(data);
            
            if (comparisonChart) {
                comparisonChart.destroy();
            }
            
            // Calculate relative efficiency compared to random
            const randomTime = data['random'] || 1;
            const efficiency = {};
            
            for (const strategy of strategies) {
                if (strategy !== 'random') {
                    efficiency[strategy] = (randomTime / data[strategy]).toFixed(2) + 'x';
                }
            }
            
            comparisonChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: strategies,
                    datasets: [
                        {
                            label: 'Boarding Time (seconds)',
                            data: times,
                            backgroundColor: [
                                'rgba(255, 99, 132, 0.5)',
                                'rgba(54, 162, 235, 0.5)',
                                'rgba(255, 206, 86, 0.5)',
                                'rgba(75, 192, 192, 0.5)'
                            ],
                            borderColor: [
                                'rgb(255, 99, 132)',
                                'rgb(54, 162, 235)',
                                'rgb(255, 206, 86)',
                                'rgb(75, 192, 192)'
                            ],
                            borderWidth: 1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Comparison of Boarding Strategies'
                        },
                        tooltip: {
                            callbacks: {
                                afterLabel: function(context) {
                                    const strategy = context.label;
                                    if (strategy !== 'random') {
                                        return `Efficiency: ${efficiency[strategy]} faster than random`;
                                    }
                                    return '';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Boarding Time (seconds)'
                            }
                        }
                    }
                }
            });
        }
    </script>
</body>
</html>''')
                
    def run(self):
        """Start the visualization server"""
        self.create_template_directory()
        
        # Open browser in a separate thread
        def open_browser():
            webbrowser.open(f'http://localhost:{self.port}/')
            
        threading.Timer(1.0, open_browser).start()
        
        # Start Flask app
        self.app.run(port=self.port, debug=False)

def main():
    """Main function to start the interactive visualization"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Interactive Aircraft Boarding Simulation')
    parser.add_argument('--port', type=int, default=5000, help='Port number for the web server')
    
    args = parser.parse_args()
    
    visualizer = InteractiveVisualizer(port=args.port)
    visualizer.run()

if __name__ == "__main__":
    main()