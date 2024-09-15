import math

def order(D, S, C, I, LT):
    try:
        # Calculate total cost and economic order quantity 
        numerator = 2 * D * S
        denominator = I * C
        Q_squared = numerator / denominator
        Q = math.sqrt(Q_squared)
        
        # Round up
        Q_up = math.ceil(Q)
        TC = (D / Q_up) * S + (I * C / 2) * Q_up

        # Calculate Reorder point quantity in units 
        R_square = (D / 52) * LT
        R_up = math.ceil(R_square)

        # Conclusion 
        print(f"When the inventory level drops to {R_up} units, place a replenishment order for {Q_up}.")
        return f"When the inventory level drops to {R_up}</br>units, place a replenishment order for {Q_up}."
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")


def noninstant(D, S, C, I, LT, P):
    try:
        # Calculate total cost and economic order quantity 
        numerator = 2 * D * S
        denominator = I * C
        Q_squared = numerator / denominator
        Q = math.sqrt(Q_squared)
        
        # Round up
        Q_up = math.ceil(Q)
        TC = (D / Q_up) * S + (I * C / 2) * Q_up

        # Calculate Reorder point quantity in units 
        R_square = (D / 52) * LT
        R_up = math.ceil(R_square)

        Q_square= Q_up * math.sqrt(P/(P-D/52))
        round_Q = math.ceil(Q_square)
        
        # Conclusion 
        print(f"When the inventory level drops to {R_up} units, place a replenishment order for {round_Q}.")
        return f"When the inventory level drops to {R_up}</br>units, place a replenishment order for {round_Q}."
        
    except ValueError:
        print("Invalid input. Please enter numeric values.")




