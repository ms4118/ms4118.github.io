import pandas as pd
import matplotlib.pyplot as plt

def calculate_wma(data, r):
  wma_values = []

  for i in range(r - 1, len(data)):
    weights = list(range(1, r + 1))  
    weighted_sum = sum(data['Yt'].iloc[i - j] * weights[j] for j in range(r))
    wma = weighted_sum / sum(weights)
    wma_values.append(wma)
  data['WMA'] = [None] * (r - 1) + wma_values  # First r-1 entries are None
  return data

def predict_future_values_wma(data, r, forecast_periods):
  last_values = data['Yt'].iloc[-r:].values
  weights = list(range(1, r + 1))  
  future_values = []

  for _ in range(forecast_periods):
    weighted_sum = sum(last_values[j] * weights[j] for j in range(r))
    next_value = weighted_sum / sum(weights)
    future_values.append(next_value)
    last_values = list(last_values[1:]) + [next_value]

  return future_values


def plot_data_wma(data, r, future_values):
  plt.figure(figsize=(12, 6))

  plt.plot(data['T'], data['Yt'], label='Actual Yt', color='blue', marker='o')

  # Plot WMA
  plt.plot(
      data['T'],
      data['WMA'],
      label=f'WMA (window={r})',
      color='orange',
      marker='o')

  # Plot future predictions
  future_t = range(data['T'].iloc[-1] + 1,
                   data['T'].iloc[-1] + len(future_values) + 1)
  plt.plot(
      future_t,
      future_values,
      label='Future Predictions',
      color='green',
      linestyle='--',
      marker='o')


  plt.xlim(left=0)
  plt.ylim(bottom=0)
  for i, value in enumerate(data['Yt']):
    plt.text(
        data['T'].iloc[i],
        value,
        f'{value:.2f}',
        fontsize=9,
        ha='right',
        va='bottom')
  for i, value in enumerate(data['WMA'].dropna()):
    plt.text(data['T'].iloc[i + r - 1], value,
             f'{value:.2f}', fontsize=9, ha='right', va='bottom')
  for i, value in enumerate(future_values):
    plt.text(
        future_t[i],
        value,
        f'{value:.2f}',
        fontsize=9,
        ha='right',
        va='bottom')

  plt.title('Weighted Moving Average and Future Predictions')
  plt.xlabel('Time (T)')
  plt.ylabel('Values (Yt)')
  plt.legend()
  plt.grid()

  return plt


def main():
  # Input 
  file_path = input("Enter the path to your CSV file: ")
  r = int(input("Enter the number of periods for WMA: "))
  forecast_periods = int(
      input("Enter the number of future periods to forecast: "))

  # Calculate WMA
  try:
    data = pd.read_csv(file_path)
    result = calculate_wma(data, r)
    print(result)

    future_values = predict_future_values_wma(result, r, forecast_periods)
    print(f"Future Predictions: {future_values}")

    # Plot data
    plt = plot_data_wma(result, r, future_values)
    plt.show()

  except Exception as e:
    print("Error:", e)
