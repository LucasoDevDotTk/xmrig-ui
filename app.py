from flask import Flask, render_template
from flaskwebgui import FlaskUI

__version__ = "0.1.0"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/configuration')
def serve_configuration():
    return render_template('configuration.html')

@app.route('/settings')
def configuration():
    return render_template('settings.html')

if __name__ == "__main__":
    # app.run(debug=True)
    FlaskUI(app=app, server="flask").run()
