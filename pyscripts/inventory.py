import math


def eoq(D, S, C, I):
    try:
        # Q = sqrt(2DS / (IC))
        numerator = 2 * D * S
        denominator = I * C

        if denominator == 0:
            print("The denominator is zero. Please check your inputs for C and I.")
            return

        Q_squared = numerator / denominator

        if Q_squared < 0:
            print("There is no real solution for Q. The value is negative. please check your inputs again")
            return

        Q = math.sqrt(Q_squared)

        # Round up
        Q_up = math.ceil(Q)
        # Calculate Total Cost (TC)
        TC = (D / Q_up) * S + (I * C / 2) * Q_up

        # Conclusions
        print(f"Your economic order quantity will be: {Q_up}")
        print(f"Your total inventory cost will be: {TC:.2f}")
        return f"Your economic order quantity will be: {Q_up}</br>Your total inventory cost will be: {TC:.2f}"

    except ValueError:
        print("Invalid input. Please enter numeric values.")
        


