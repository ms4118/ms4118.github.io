def calculate_csi(V_b, N_d, N_r, R_r):
    """
    Calculate the Cardboard Savings Index (CSI).

    Parameters:
        V_b (float): Average volume of cardboard used per package (in cubic meters).
        N_d (int): Total number of deliveries in a given time period.
        N_r (int): Number of reuses per package (for reusable systems). If single-use, N_r = 1.
        R_r (float): Reduction ratio in packaging volume achieved by dynamic optimization (e.g., 0.3 for 30%).

    Returns:
        float: Cardboard Savings Index (CSI) in cubic meters.
    """
    # Traditional System: Total cardboard used
    traditional_cardboard = (V_b * N_d) / N_r

    # Innovative System: Total cardboard used after reduction
    innovative_cardboard = V_b * N_d * (1 - R_r)

    # Cardboard Savings Index (CSI)
    csi = traditional_cardboard - innovative_cardboard

    return csi


def calculate_cwcs(csi, C_c):
    """
    Calculate the Carbon-Weighted Cardboard Savings (CWCS).

    Parameters:
        csi (float): Cardboard Savings Index (CSI) in cubic meters.
        C_c (float): Carbon footprint of producing 1 cubic meter of cardboard (e.g., 200 kg CO₂/m³).

    Returns:
        float: Carbon-Weighted Cardboard Savings (CWCS) in kg CO₂.
    """
    # Calculate CWCS
    cwcs = csi * C_c

    return cwcs


# Example Inputs
#V_b = 0.01  # Average volume of cardboard per package (m³)
#N_d = 10000  # Number of deliveries in a month
#N_r = 5  # Number of reuses per package
#R_r = 0.4  # Reduction ratio in packaging volume (40%)
#C_c = 200  # Carbon footprint of producing 1 m³ of cardboard (kg CO₂/m³)

# Calculate CSI
csi = calculate_csi(V_b, N_d, N_r, R_r)

# Calculate CWCS
cwcs = calculate_cwcs(csi, C_c)

# Output Results
print(f"Traditional System Cardboard Used: {(V_b * N_d) / N_r:.2f} m³")
print(f"Innovative System Cardboard Used: {V_b * N_d * (1 - R_r):.2f} m³")
print(f"Cardboard Savings Index (CSI): {csi:.2f} m³")
print(f"Carbon-Weighted Cardboard Savings (CWCS): {cwcs:.2f} kg CO₂")
