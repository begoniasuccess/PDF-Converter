from flask import Flask, render_template

app = Flask(__name__, template_folder='convertPdf')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return "This is the About Page"

if __name__ == '__main__':
    app.run(debug=True)
