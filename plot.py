import numpy as np
import matplotlib.pyplot as plt
import math

D = float(input("Enter Demand (D, units per year): "))  # Annual demand
S = float(input("Enter Setup Cost (S): "))  # Cost per order
C = float(input("Enter Cost per Unit (C): "))  # Cost per unit
I = float(input("Enter Carrying Cost (I): "))  # Carrying cost per unit
LT = float(input("Enter Lead Time (LT, weeks): "))  # Lead time in weeks

def order(D, S, C, I, LT):
    try:
        # Calculate total cost and economic order quantity 
        numerator = 2 * D * S
        denominator = I * C
        Q_squared = numerator / denominator
        Q = math.sqrt(Q_squared)

        # Round up
        Q_up = math.ceil(Q)

        # Calculate total cost
        TC = (D / Q_up) * S + (I * C / 2) * Q_up

        # Calculate Reorder point quantity in units 
        R_square = (D / 52) * LT
        R_up = math.ceil(R_square)

        return Q_up, R_up
    except ZeroDivisionError:
        print("Error: Division by zero in calculations.")
        return None, None

def plot_inventory_wave(Q_star, R_star, D, LT):
    # Convert LT from weeks to days
    LT_days = LT * 7
    
    # Calculate time intervals
    time_to_R = (Q_star - R_star) / (D / 52) * 7  # Time to drop from Q* to R* in days
    time_to_0 = R_star / (D / 52) * 7              # Time to drop from R* to 0 in days

    # Create time points and inventory levels for multiple cycles
    time_points = []
    inventory_levels = []

    # Create inventory cycles (3 cycles)
    for cycle in range(3):  
        cycle_start = cycle * (time_to_R + time_to_0)

        # Drop from Q* to R*
        time_points.extend(np.linspace(cycle_start, cycle_start + time_to_R, int(time_to_R / 0.1)).tolist())
        inventory_levels.extend(np.linspace(Q_star, R_star, int(time_to_R / 0.1)).tolist())

        # Mark the first R* point (where the first downward line touches R*)
        time_points.append(cycle_start + time_to_R)
        inventory_levels.append(R_star)

        # Drop from R* to 0
        time_points.extend(np.linspace(cycle_start + time_to_R, cycle_start + time_to_R + time_to_0, int(time_to_0 / 0.1)).tolist())
        inventory_levels.extend(np.linspace(R_star, 0, int(time_to_0 / 0.1)).tolist())

        # Vertical rise from 0 to Q*
        time_points.append(cycle_start + time_to_R + time_to_0)  # time point at 0
        inventory_levels.append(0)  # at 0
        time_points.append(cycle_start + time_to_R + time_to_0 + 0.1)  # time point after rise
        inventory_levels.append(Q_star)  # back to Q*

    # Convert to numpy arrays
    time_points = np.array(time_points)
    inventory_levels = np.array(inventory_levels)

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(time_points, inventory_levels, label='Inventory Level', color='b', linewidth=2)

    # Add horizontal line for Q*
    plt.axhline(y=Q_star, color='purple', linestyle='--', label='Q*')
    plt.text(time_points[0], Q_star + 5, 'Q*', ha='left', fontsize=10, color='purple')
    plt.text(time_points[0], Q_star + 0.2, f'{Q_star}', ha='left', fontsize=10, color='purple')  # Label for Q*
    # Mark the first R* point
    first_R_position = time_points[np.argmax(inventory_levels == R_star)]
    plt.text(first_R_position, R_star + 5, 'R* (First)', ha='center', fontsize=10, color='orange')
    plt.text(first_R_position, R_star + 0.2, f'{R_star}', ha='center', fontsize=10, color='orange')  # Label for first R*
    # Drop from R* to 0
    # Mark the second R* position at the second downward line
    second_R_position = first_R_position + time_to_0 + time_to_R
    plt.text(second_R_position, R_star + 0.3, 'R* (Second)', ha='center', fontsize=10, color='orange')

    # Draw arrow for Lead Time (LT)
    plt.annotate('', xy=(first_R_position + LT_days, R_star), xytext=(first_R_position, R_star),
                 arrowprops=dict(arrowstyle='<->', color='green', lw=2),
                 fontsize=10)
    plt.text((first_R_position + (first_R_position + LT_days)) / 2, R_star + 0.1, 'LT', ha='center', fontsize=10, color='green')

    # Draw arrow for Cycle Time (T) in purple
    plt.annotate('', xy=(second_R_position, R_star - 1), xytext=(first_R_position, R_star - 1),
                 arrowprops=dict(arrowstyle='<->', color='purple', lw=2),
                 fontsize=10)
    plt.text((first_R_position + second_R_position) / 2, R_star - 1.5, 'T', ha='center', fontsize=10, color='purple')

    # Annotations for clarity
    plt.text(time_to_R - 0.5, 0 + 0.1, '0', ha='center', fontsize=10)

    # Add additional lines for clarity
    plt.axhline(y=0, color='red', linestyle='--', label='Zero Inventory')

    # Label T and LT
    plt.text(time_to_R + time_to_0 / 2, -5, f'T = {time_to_R + time_to_0:.1f} days (Cycle Time)', ha='center', fontsize=10, color='purple')
    plt.text(time_to_R + time_to_0 + 1, LT_days + 0.1, f'LT = {LT_days:.1f} days (Lead Time)', ha='center', fontsize=10, color='green')

    plt.title('Inventory Level Over Time')
    plt.xlabel('Time (days)')
    plt.ylabel('Inventory Level')
    plt.grid(True)
    plt.legend()
    plt.xlim(0, 3 * (time_to_R + time_to_0))
    plt.ylim(-10, Q_star + 10)
    plt.show()
    print(f"Hiii")
    return f"Hiii"

# Calculate Q* and R*
Q_star, R_star = order(D, S, C, I, LT)

if Q_star is not None and R_star is not None:
    # Call the function to plot the inventory wave
    plot_inventory_wave(Q_star, R_star, D, LT)
