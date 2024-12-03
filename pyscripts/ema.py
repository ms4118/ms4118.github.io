import pandas as pd
import matplotlib.pyplot as plt


def calculate_ema(data, alpha):
  ema_values = []

  # Calculate
  for i in range(len(data)):
    if i == 0:
      ema_values.append(data['Yt'].iloc[i]) 
    else:
      current_value = data['Yt'].iloc[i]
      previous_ema = ema_values[i - 1] 
      ema = alpha * current_value + (1 - alpha) * previous_ema
      ema_values.append(ema)
  data['EMA'] = [None] + ema_values[:-1]

  return data


def plot_data_ema(data, alpha):
  plt.figure(figsize=(12, 6))

  # Plot
  plt.plot(
      data['T'],
      data['Yt'],
      label='Actual Yt',
      color='blue',
      marker='o',
      linestyle='-')
  plt.plot(
      data['T'],
      data['EMA'],
      label=f'EMA (alpha={alpha})',
      color='orange',
      marker='o',
      linestyle='-')

  # xy
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

  # Label
  for i, value in enumerate(data['EMA']):
    if value is not None: 
      plt.text(
          data['T'].iloc[i],
          value,
          f'{value:.2f}',
          fontsize=9,
          ha='right',
          va='bottom')
  plt.title('Exponential Moving Average (EMA)')
  plt.xlabel('Time (T)')
  plt.ylabel('Values (Yt)')
  plt.legend()
  plt.grid()
  return plt


def main():
  file_path = input("Enter the path to your CSV file: ")
  alpha = float(input("Enter the smoothing factor (alpha) between 0 and 1: "))
  if not (0 < alpha < 1):
    print("Error: Alpha must be between 0 and 1.")
    return
  try:
    data = pd.read_csv(file_path)
    result = calculate_ema(data, alpha)
    print(result)

    # Plot data
    plt = plot_data_ema(result, alpha)
    plt.show()

  except Exception as e:
    print("Error:", e)
