#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aircraft Boarding Simulation Model
==================================

This module implements various algorithms for simulating aircraft boarding processes
using mathematical modeling and agent-based simulation techniques.
"""

import numpy as np
import matplotlib.pyplot as plt
from enum import Enum
import argparse
import time
from typing import List, Dict, Tuple, Optional

# Define boarding strategies
class BoardingStrategy(Enum):
    RANDOM = "random"
    BACK_TO_FRONT = "back-to-front"
    OUTSIDE_IN = "outside-in"
    HYBRID = "hybrid"

# Define seat types
class SeatType(Enum):
    WINDOW = 0
    MIDDLE = 1
    AISLE = 2

class Aircraft:
    """Model of an aircraft with configurable seating layout"""
    
    def __init__(self, rows: int = 32, seats_per_row: int = 6):
        """
        Initialize aircraft configuration
        
        Args:
            rows: Number of rows in the aircraft
            seats_per_row: Number of seats per row (typically 6 for single-aisle aircraft)
        """
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.total_seats = rows * seats_per_row
        
        # Initialize empty aircraft
        self.seating = np.zeros((rows, seats_per_row), dtype=int)
        
        # Map seat positions to seat types
        self.seat_types = {}
        for row in range(rows):
            for seat in range(seats_per_row):
                if seat == 0 or seat == seats_per_row - 1:
                    self.seat_types[(row, seat)] = SeatType.WINDOW
                elif seat == 1 or seat == seats_per_row - 2:
                    self.seat_types[(row, seat)] = SeatType.MIDDLE
                else:
                    self.seat_types[(row, seat)] = SeatType.AISLE

class Passenger:
    """Model of a passenger with assigned seat and boarding behavior"""
    
    def __init__(self, passenger_id: int, row: int, seat: int, 
                 walking_speed: float = 1.0, 
                 stowing_time: float = 5.0):
        """
        Initialize passenger attributes
        
        Args:
            passenger_id: Unique passenger identifier
            row: Assigned row number
            seat: Assigned seat position within row
            walking_speed: Walking speed in rows per second
            stowing_time: Time needed to stow luggage in seconds
        """
        self.id = passenger_id
        self.row = row
        self.seat = seat
        self.walking_speed = walking_speed
        self.stowing_time = stowing_time
        self.boarded = False
        self.position = -1  # Position in the aisle, -1 means not boarded yet
        
    def __repr__(self):
        return f"Passenger({self.id}, row={self.row}, seat={self.seat})"
        
class Simulation:
    """Main simulation class for aircraft boarding process"""
    
    def __init__(self, aircraft: Aircraft, strategy: BoardingStrategy = BoardingStrategy.RANDOM):
        """
        Initialize simulation parameters
        
        Args:
            aircraft: Aircraft model with seating configuration
            strategy: Boarding strategy to use
        """
        self.aircraft = aircraft
        self.strategy = strategy
        self.passengers = []
        self.time = 0
        self.generate_passengers()
        
    def generate_passengers(self):
        """Generate passengers with assigned seats based on the strategy"""
        passenger_id = 0
        
        # Create a passenger for each seat
        seats = []
        for row in range(self.aircraft.rows):
            for seat in range(self.aircraft.seats_per_row):
                seats.append((row, seat))
        
        # Order passengers based on strategy
        if self.strategy == BoardingStrategy.RANDOM:
            np.random.shuffle(seats)
        elif self.strategy == BoardingStrategy.BACK_TO_FRONT:
            # Sort by row (back to front)
            seats.sort(key=lambda x: (-x[0], x[1]))
        elif self.strategy == BoardingStrategy.OUTSIDE_IN:
            # Sort by seat type (window, middle, aisle)
            seats.sort(key=lambda x: (self.aircraft.seat_types[(x[0], x[1])].value, x[0]))
        elif self.strategy == BoardingStrategy.HYBRID:
            # Combination: Back-to-front with window-middle-aisle in each zone
            zones = 4  # Divide aircraft into zones
            rows_per_zone = self.aircraft.rows // zones
            
            # Create zones
            zoned_seats = []
            for zone in range(zones):
                zone_seats = []
                start_row = self.aircraft.rows - (zone + 1) * rows_per_zone
                end_row = self.aircraft.rows - zone * rows_per_zone
                
                for row in range(start_row, end_row):
                    for seat in range(self.aircraft.seats_per_row):
                        zone_seats.append((row, seat))
                
                # Sort zone seats by seat type
                zone_seats.sort(key=lambda x: self.aircraft.seat_types[(x[0], x[1])].value)
                zoned_seats.extend(zone_seats)
            
            seats = zoned_seats
        
        # Create passengers from ordered seat list
        for row, seat in seats:
            self.passengers.append(Passenger(passenger_id, row, seat))
            passenger_id += 1
    
    def run(self, max_time: float = 1000.0, display_progress: bool = True) -> float:
        """
        Run the simulation until all passengers are seated
        
        Args:
            max_time: Maximum simulation time
            display_progress: Whether to display progress updates
            
        Returns:
            Total boarding time
        """
        # Queue of passengers waiting to board
        queue = self.passengers.copy()
        
        # Passengers in the aisle
        aisle = []
        
        # Simulation time
        self.time = 0
        
        # Run simulation until all passengers are seated or max time reached
        while queue or aisle:
            # Update passenger positions
            self.update_passengers(queue, aisle)
            
            # Increment time
            self.time += 1
            
            # Display progress periodically
            if display_progress and self.time % 10 == 0:
                seated = len(self.passengers) - len(queue) - len(aisle)
                print(f"Time: {self.time:.1f}s, Seated: {seated}/{len(self.passengers)}")
            
            # Check for timeout
            if self.time >= max_time:
                print(f"Simulation timed out after {max_time} seconds")
                break
        
        return self.time
    
    def update_passengers(self, queue: List[Passenger], aisle: List[Passenger]):
        """
        Update passenger positions in one time step
        
        Args:
            queue: List of passengers waiting to board
            aisle: List of passengers in the aisle
        """
        # Try to add a new passenger to the aisle if possible
        if queue and (not aisle or aisle[-1].position > 2):
            passenger = queue.pop(0)
            passenger.position = 0
            aisle.append(passenger)
        
        # Process passengers in the aisle (from front to back)
        for i in range(len(aisle) - 1, -1, -1):
            passenger = aisle[i]
            
            # Check if passenger has reached their row
            if passenger.position == passenger.row:
                # Simulate stowing luggage and sitting
                if hasattr(passenger, 'stowing_remaining'):
                    passenger.stowing_remaining -= 1
                    if passenger.stowing_remaining <= 0:
                        # Passenger is now seated
                        passenger.boarded = True
                        aisle.pop(i)
                else:
                    # Start stowing process
                    passenger.stowing_remaining = passenger.stowing_time
            else:
                # Check if passenger can move forward
                can_move = True
                for other in aisle:
                    # Check if there's another passenger blocking the way
                    if (other != passenger and 
                        other.position > passenger.position and
                        other.position - passenger.position <= passenger.walking_speed):
                        can_move = False
                        break
                
                if can_move:
                    # Move towards assigned row
                    steps = min(passenger.walking_speed, 
                                passenger.row - passenger.position)
                    passenger.position += steps

def run_comparison(aircraft: Aircraft, display_results: bool = True) -> Dict[str, float]:
    """
    Run simulations with different boarding strategies and compare results
    
    Args:
        aircraft: Aircraft model to use for simulations
        display_results: Whether to display results
        
    Returns:
        Dictionary with boarding times for each strategy
    """
    results = {}
    
    # Run simulation for each strategy
    for strategy in BoardingStrategy:
        print(f"\nRunning simulation with {strategy.value} strategy...")
        sim = Simulation(aircraft, strategy)
        boarding_time = sim.run(display_progress=False)
        results[strategy.value] = boarding_time
        print(f"{strategy.value}: {boarding_time:.1f} seconds")
    
    # Display comparative results
    if display_results:
        # Calculate efficiency compared to random boarding
        random_time = results[BoardingStrategy.RANDOM.value]
        print("\nRelative Efficiency (compared to random boarding):")
        for strategy, time in results.items():
            if strategy != BoardingStrategy.RANDOM.value:
                efficiency = random_time / time
                print(f"{strategy}: {efficiency:.2f}x faster")
        
        # Plot results
        plt.figure(figsize=(10, 6))
        strategies = list(results.keys())
        times = list(results.values())
        plt.bar(strategies, times)
        plt.xlabel('Boarding Strategy')
        plt.ylabel('Boarding Time (seconds)')
        plt.title('Comparison of Aircraft Boarding Strategies')
        plt.savefig('boarding_comparison.png')
        if display_results:
            plt.show()
    
    return results

def main():
    """Main function to run simulations based on command line arguments"""
    parser = argparse.ArgumentParser(description='Aircraft Boarding Simulation')
    parser.add_argument('--rows', type=int, default=32, help='Number of rows in aircraft')
    parser.add_argument('--seats', type=int, default=6, help='Number of seats per row')
    parser.add_argument('--strategy', type=str, choices=[s.value for s in BoardingStrategy], 
                       default='random', help='Boarding strategy to use')
    parser.add_argument('--compare', action='store_true', help='Run comparison of all strategies')
    
    args = parser.parse_args()
    
    # Create aircraft model
    aircraft = Aircraft(rows=args.rows, seats_per_row=args.seats)
    
    if args.compare:
        run_comparison(aircraft)
    else:
        # Run single simulation with specified strategy
        strategy = BoardingStrategy(args.strategy)
        sim = Simulation(aircraft, strategy)
        boarding_time = sim.run()
        print(f"\nTotal boarding time: {boarding_time:.1f} seconds")

if __name__ == "__main__":
    main()