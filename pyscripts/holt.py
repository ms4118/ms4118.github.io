import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def holt_linear_exponential_smoothing(data, alpha, beta):
  n = len(data)
  a = np.zeros(n)  # Level
  b = np.zeros(n)  # Trend
  P = np.zeros(n)  # Forecast

  # Initialize
  a[0] = data[0]  # First level is the first data point
  b[0] = 0        # Initial trend is zero

  # Calculate level, trend, and forecast
  for t in range(1, n):
    a[t] = alpha * data[t] + (1 - alpha) * (a[t - 1] + b[t - 1])
    b[t] = beta * (a[t] - a[t - 1]) + (1 - beta) * b[t - 1]
    P[t] = a[t] + b[t]

  return a, b, P


def forecast_future_values_holt(a_last, b_last, num_forecasts):
  forecasts = []
  for j in range(1, num_forecasts + 1):
    forecast = a_last + b_last * j
    forecasts.append(forecast)
  return forecasts


def plot_results_holt(data, a, P, future_forecasts, num_forecasts):
  plt.figure(figsize=(10, 6))

  # Plot actual data
  plt.scatter(
      range(
          1,
          len(data) + 1),
      data,
      color='blue',
      label='Actual Data (Yt)')
  plt.plot(range(1, len(data) + 1), a, color='orange', label='Level (at)')
  plt.plot(range(2,
                 len(data) + 1),
           P[1:],
           color='red',
           linestyle='dotted',
           label='Forecasts (Pt)')
  for j in range(num_forecasts):
    plt.scatter(len(data) + j + 1, future_forecasts[j], color='green')
    plt.text(
        len(data) + j + 1,
        future_forecasts[j],
        f'P({len(data) + j + 1})={future_forecasts[j]:.2f}',
        fontsize=9,
        ha='center')

  # Labels
  plt.xlabel('Time (t)')
  plt.ylabel('Values (Yt, at, Pt)')
  plt.title("Holt's Linear Exponential Smoothing")
  plt.axhline(0, color='black', linewidth=0.5, ls='--')
  plt.axvline(0, color='black', linewidth=0.5, ls='--')
  plt.legend()
  plt.grid()
  return plt
  
def main():
  file_path = input("Enter the path to the CSV file: ")
  alpha = float(input("Enter the smoothing factor alpha (0 < alpha < 1): "))
  beta = float(input("Enter the smoothing factor beta (0 < beta < 1): "))
  num_forecasts = int(
      input("How many future values do you want to forecast? "))

  # Validate 
  if not (0 < alpha < 1):
    raise ValueError("Alpha must be between 0 and 1.")
  if not (0 < beta < 1):
    raise ValueError("Beta must be between 0 and 1.")

  try:
    data = pd.read_csv(file_path)

    if 'Yt' not in data.columns:
      raise ValueError("The CSV file must contain a column named 'Yt'.")

    Y = data['Yt'].values
    a, b, P = holt_linear_exponential_smoothing(Y, alpha, beta)

    # Get last level and trend
    last_a = a[-1]
    last_b = b[-1]

    future_forecasts = forecast_future_values_holt(
        last_a, last_b, num_forecasts)
    for j in range(num_forecasts):
      print(f"Forecast for P({len(Y) + j + 1}) = {future_forecasts[j]:.2f}")

    # Plot
    plt = plot_results_holt(Y, a, P, future_forecasts, num_forecasts)
    plt.show()

  except Exception as e:
    print(f"Error: {e}")


