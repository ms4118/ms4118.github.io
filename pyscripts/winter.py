import pandas as pd
import matplotlib.pyplot as plt


def calculate_initials(data, M):
  n = len(data)
  group_size = n // M
  Y1 = data[:group_size]
  Y2 = data[group_size:2 * group_size]
  mean_Y1 = Y1.mean()
  mean_Y2 = Y2.mean()
  A0 = round((mean_Y1 + mean_Y2) / M, 2)
  B0 = round((mean_Y2 - mean_Y1) / (n - group_size), 2)
  S1 = round((Y1.iloc[0] / mean_Y1 + Y2.iloc[0] / mean_Y2) / M, 2)

  return A0, B0, S1, mean_Y1, mean_Y2, group_size


def calculate_ABC(data, alpha, beta, gamma, M):
  n = len(data)
  A = [0] * n
  B = [0] * n
  S = [0] * n

  A0, B0, S1, mean_Y1, mean_Y2, group_size = calculate_initials(data, M)
  A[0] = A0
  B[0] = B0
  S[0] = S1
  mean_Y1 = round(data[:group_size].mean(), 2)
  mean_Y2 = round(data[group_size:2 * group_size].mean(), 2)

  # S for group 1
  for t in range(1, group_size + 1):  # t = 1 to 9
    S[t - 1] = round(((data[t - 1] / mean_Y1) +
                     (data[t + group_size - 1] / mean_Y2)) / M, 2)

  # A for group 1
  for t in range(1, group_size + 1):
    if t == 1:
      A[t - 1] = round(alpha * (data[t - 1] / S[t - 1]) +
                       (1 - alpha) * (A0 + B0), 2)
    else:
      A[t - 1] = round(alpha * (data[t - 1] / S[t - 1]) +
                       (1 - alpha) * (A[t - 2] + B[t - 2]), 2)
    print(f"A({t}) = {A[t - 1]}")

  # cal B group 1
  for t in range(1, group_size + 1):
    if t == 1:
      B[t - 1] = round(beta * (A[t - 1] - A0) + (1 - beta) * B0, 2)
    else:
      B[t - 1] = round(beta * (A[t - 1] - A[t - 2]) + (1 - beta) * B[t - 2], 2)
    print(f"B({t}) = {B[t - 1]}")

  #  S second group 
  for t in range(group_size + 1, n + 1):  # t = 10 to 18
    S[t - 1] = round(gamma * (data[t - 1] / A[t - 2]) +
                     (1 - gamma) * S[t - group_size - 1], 2)
    A[t - 1] = round(alpha * (data[t - 1] / S[t - 1]) +
                     (1 - alpha) * (A[t - 2] + B[t - 2]), 2)

    # B group 2
    B[t - 1] = round(beta * (A[t - 1] - A[t - 2]) + (1 - beta) * B[t - 2], 2)
    print(f"B({t}) = {B[t - 1]}") 

  return A, B, S


def forecast_seasons(A, B, S, n_forecasts, group_size):
  forecasts = []
  for i in range(n_forecasts * group_size):
    season_index = i % group_size
    forecast = A[-1] + (i + 1) * B[-1] * S[season_index]
    forecasts.append(forecast)
  return forecasts


def main():
  # input
  file_path = input("Enter the path to the CSV file: ")
  data = pd.read_csv(file_path)
  Yt = data['Yt']
  alpha = float(input("Enter alpha (0 < alpha < 1): "))
  beta = float(input("Enter beta (0 < beta < 1): "))
  gamma = float(input("Enter gamma (0 < gamma < 1): "))
  M = int(input("Enter the number of seasons (M): "))
  n_forecasts = int(input("Enter the number of seasons to forecast: "))

  # Calculate A, B, S
  A, B, S = calculate_ABC(Yt, alpha, beta, gamma, M)
  group_size = len(Yt) // M
  forecasts = forecast_seasons(A, B, S, n_forecasts, group_size)

  # Graph part
  forecast_df = pd.DataFrame({
      'Time Period': range(len(Yt) + 1, len(Yt) + len(forecasts) + 1),
      'Forecast': forecasts
  })

  plt.figure(figsize=(12, 6))
  plt.plot(range(1, len(Yt) + 1), Yt, label='Original Data')
  plt.plot(
      forecast_df['Time Period'],
      forecast_df['Forecast'],
      label='Forecasted Data',
      linestyle='--')
  plt.xlabel('Time Period')
  plt.ylabel('Values')
  plt.title('Seasonal Forecasting')
  plt.legend()
  plt.show()
