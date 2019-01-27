from flask import Flask, render_template

# The name of this application is app
app = Flask(__name__)


@app.route("/")
def index():
    """
    @author EM
    The homepage of the application.
    """
    return render_template("index.html")
