import pandas as pd
import matplotlib.pyplot as plt


def calculate_ema(data, alpha):
  # Initialize a list for EMA values
  ema_values = []

  # Calculate EMA
  for i in range(len(data)):
    if i == 0:
      # For t=1, EMA is equal to the first Yt value (this will be used for t=2)
      ema_values.append(data['Yt'].iloc[i])  # This will be plotted at t=2
    else:
      # For t=2 and onwards, apply the EMA formula
      current_value = data['Yt'].iloc[i]
      previous_ema = ema_values[i - 1]  # Use the previous EMA value
      ema = alpha * current_value + (1 - alpha) * previous_ema
      ema_values.append(ema)

  # Shift EMA values for plotting
  # None for the first entry, shift EMA values
  data['EMA'] = [None] + ema_values[:-1]

  return data


def plot_data_ema(data, alpha):
  plt.figure(figsize=(12, 6))

  # Plot actual values
  plt.plot(
      data['T'],
      data['Yt'],
      label='Actual Yt',
      color='blue',
      marker='o',
      linestyle='-')

  # Plot EMA
  plt.plot(
      data['T'],
      data['EMA'],
      label=f'EMA (alpha={alpha})',
      color='orange',
      marker='o',
      linestyle='-')

  # Set x and y axis limits
  plt.xlim(left=0)
  plt.ylim(bottom=0)

  # Label the actual values
  for i, value in enumerate(data['Yt']):
    plt.text(
        data['T'].iloc[i],
        value,
        f'{value:.2f}',
        fontsize=9,
        ha='right',
        va='bottom')

  # Label the EMA values
  for i, value in enumerate(data['EMA']):
    if value is not None:  # Only label EMA values that exist
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
  # Input file path and alpha value
  file_path = input("Enter the path to your CSV file: ")
  alpha = float(input("Enter the smoothing factor (alpha) between 0 and 1: "))

  # Validate alpha
  if not (0 < alpha < 1):
    print("Error: Alpha must be between 0 and 1.")
    return

  # Calculate EMA
  try:
    data = pd.read_csv(file_path)
    result = calculate_ema(data, alpha)
    print(result)

    # Plot data
    plt = plot_data_ema(result, alpha)
    plt.show()

  except Exception as e:
    print("Error:", e)
