import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calculate_linear_regression(data):
  t = data['T'].values
  Y = data['Yt'].values
  mean_t = np.mean(t)
  mean_Y = np.mean(Y)
  numerator = np.sum((t - mean_t) * (Y - mean_Y))
  denominator = np.sum((t - mean_t) ** 2)
  b_t = numerator / denominator
  b_t = round(b_t, 1)
  a_t = mean_Y - b_t * mean_t
  a_t = round(a_t, 1)
  return a_t, b_t, t, Y

def predict_linear(a_t, b_t, start_t, num_predictions):
  predictions = {}
  for i in range(num_predictions):
    t_val = start_t + i + 1  # Predict next number
    predictions[t_val] = round(a_t + b_t * t_val, 1)
  return predictions


def plot_regression_linear(t, Y, a_t, b_t, predictions):
  plt.figure(figsize=(10, 6))
  plt.scatter(t, Y, color='blue', label='Data Points')
  regression_line = a_t + b_t * t
  plt.plot(t, regression_line, color='red', label='Regression Line')

  future_t = list(predictions.keys())
  prediction_line = [a_t + b_t * t_val for t_val in future_t]
  plt.plot(
      future_t,
      prediction_line,
      color='green',
      linestyle='dotted',
      label='Prediction Line')
  for t_val, pred in predictions.items():
    plt.scatter(
        t_val,
        pred,
        color='green',
        label=f'Predicted P({t_val}) = {pred}')

  # Label
  plt.xlabel('t (Time)')
  plt.ylabel('Y (Value)')
  plt.title('Linear Regression with Predictions')
  plt.axhline(0, color='black', linewidth=0.5, ls='--')
  plt.axvline(0, color='black', linewidth=0.5, ls='--')

  plt.legend()
  plt.grid()
  return plt


def main():
  file_path = input("Enter the path to the CSV file: ")
  data = pd.read_csv(file_path)
  try:
    a_t, b_t, t, Y = calculate_linear_regression(data)
    print(f"The linear regression equation is: Y_t = {a_t} + {b_t}t")

    # Ask how many
    num_predictions = int(
        input("How many future values do you want to predict? "))
    start_t = int(t[-1])  # last t
    predictions = predict_linear(a_t, b_t, start_t, num_predictions)

    for t_val in predictions:
      print(f"P({t_val}) = {predictions[t_val]} (Predicted Value)")
    plt = plot_regression_linear(t, Y, a_t, b_t, predictions)
    plt.show()

  except Exception as e:
    print(f"Error: {e}")
