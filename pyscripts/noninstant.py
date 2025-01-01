import numpy as np
import matplotlib.pyplot as plt
import math

# User inputs
D = float(input("Enter Demand (D, units per year): "))  
S = float(input("Enter Setup Cost (S): "))  
C = float(input("Enter Cost per Unit (C): "))  
I = float(input("Enter Carrying Cost (I): "))  
LT = float(input("Enter Lead Time (LT, weeks): ")) 
P = float(input("Enter Price (P): ")) 

def noninstant(D, S, C, I, LT, P):
    try:
        numerator = 2 * D * S
        denominator = I * C
        Q_squared = numerator / denominator
        Q = math.sqrt(Q_squared)
        
        Q_up = math.ceil(Q)
        
        R_square = (D / 52) * LT
        R_up = math.ceil(R_square)

        Q_square = Q_up * math.sqrt(P / (P - D / 52))
        round_Q = math.ceil(Q_square)
        max_inventory = (round_Q / P) * (P - D / 52)

        print(f"When the inventory level drops to {R_up} units, place a replenishment order for {round_Q}.")
        return round_Q, max_inventory, R_up
        
    except ValueError:
        print("Invalid input. Please enter positive values.")
        return None, None, None

round_Q, max_inventory, R_up = noninstant(D, S, C, I, LT, P)

if round_Q is not None:
    # repeat 3 times
    repetitions = 3
    time_period = 10  # Total time for one cycle
    t = np.linspace(0, time_period * repetitions, 1000)
    inventory_levels = np.zeros_like(t)

    # Generate the sawtooth wave
    for i in range(len(t)):
        cycle_position = t[i] % time_period  # Position within the current cycle
        if cycle_position < time_period / 2:
            inventory_levels[i] = (max_inventory / (time_period / 2)) * cycle_position  # Linear up
        else:
            inventory_levels[i] = max_inventory - ((max_inventory / (time_period / 2)) * (cycle_position - time_period / 2))  # Linear down

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(t, inventory_levels, label='Inventory Level', color='blue')
    
    # Draw Q*, max inventory, and R* lines
    plt.axhline(y=round_Q, color='green', linestyle='--', label=f'Q*: {round_Q}')
    plt.axhline(y=max_inventory, color='red', linestyle='--', label=f'Max Inventory: {max_inventory:.2f}')
    plt.axhline(y=R_up, color='orange', linestyle='--', label=f'Reordering Quantity: {R_up}')

    # Adjust y-axis to accommodate Q*
    plt.ylim(0, max(round_Q, max_inventory) * 1.1)  # Enlarged to the value of Q*
    
    plt.title('Sawtooth Wave of Inventory Levels (3 Cycles)')
    plt.xlabel('Time')
    plt.ylabel('Inventory Level')
    plt.xlim(0, time_period * repetitions)
    plt.grid()
    plt.legend()
    
    # Label for Q*
    plt.text(0, round_Q + 0.05 * max(round_Q, max_inventory), f'Q*: {round_Q}', color='green')
    # Label for Max Inventory
    plt.text(0, max_inventory + 0.05 * max(round_Q, max_inventory), f'Max Inventory: {max_inventory:.2f}', color='red')
    # Label for Reordering Quantity
    plt.text(0, R_up + 0.05 * max(round_Q, max_inventory), f'Reordering Quantity: {R_up}', color='orange')

    plt.show()
