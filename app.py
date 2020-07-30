from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')

@app.errorhandler(404)
def error404(e):
    #note that we set the 404 status explicity
    return render_template('404.html'), 404
    if __name__ == '__main__':
  app.run(debug=True)    