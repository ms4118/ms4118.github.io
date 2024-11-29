import pandas as pd
import matplotlib.pyplot as plt


def calculate_sma(data, r):
  # Calculate the Simple Moving Average
  data['SMA'] = data['Yt'].rolling(window=r).mean()

  return data


def sma_predict_next_value(data):
  predictions = []
  for i in range(len(data) - 3):
    # Use the last three values to predict the next one
    next_value = (data['Yt'].iloc[i] +
                  data['Yt'].iloc[i + 1] + data['Yt'].iloc[i + 2]) / 3
    predictions.append(next_value)

  # Create a new DataFrame for predictions
  prediction_index = range(len(data) - 3, len(data) + len(predictions) - 3)
  predicted_df = pd.DataFrame({
      'T': prediction_index,
      'Predicted_Yt': predictions
  })

  return predicted_df


def plot_sma_data(data, r, predicted_df):
  plt.figure(figsize=(12, 6))

  # Plot actual values
  plt.plot(data['T'], data['Yt'], label='Actual Yt', color='blue')

  # Plot SMA
  plt.plot(data['T'], data['SMA'], label=f'SMA (window={r})', color='orange')

  # Plot predictions
  plt.plot(
      predicted_df['T'],
      predicted_df['Predicted_Yt'],
      label='Predicted Yt',
      color='green',
      linestyle='--')

  # Set x and y axis limits
  plt.xlim(left=0)
  plt.ylim(bottom=0)

  plt.title('Simple Moving Average and Predictions')
  plt.xlabel('Time (T)')
  plt.ylabel('Values (Yt)')
  plt.legend()
  plt.grid()

  return plt


def main():
  # Input file path and number of periods
  file_path = input("Enter the path to your CSV file: ")
  r = int(input("Enter the number of periods for SMA: "))

  # Calculate SMA
  try:
    # Load the CSV file
    data = pd.read_csv(file_path)
    result = calculate_sma(data, r)
    print(result)

    # Predict next values
    predicted_df = sma_predict_next_value(result)

    # Plot data
    plt = plot_sma_data(result, r, predicted_df)
    plt.show()

  except Exception as e:
    print("Error:", e)


