from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('furniture.html')

@app.route('/run-try', methods=['POST'])
def run_try():
    # Run the Python script
    result = subprocess.run(['python', 'helloworld.py'], capture_output=True, text=True)
    return f"Output: {result.stdout}"  # Display the output of the script

if __name__ == '__main__':
    app.run(debug=True)
