import os,sys,time
print (sys.version)

from flask import ( Flask, render_template)

# https://wiki.jenkins.io/display/JENKINS/Step+by+step+guide+to+set+up+master+and+agent+machines+on+Windows

# Create the application instance
app = Flask(__name__, template_folder="templates")

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/

    :return:        the rendered template 'home.html'
    """
    return render_template('home.php')

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(debug=True)