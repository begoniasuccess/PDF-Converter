from flask import Flask, render_template
from api.files import files_bp  # 引入 API

app = Flask(__name__, template_folder='convertPdf')
app.register_blueprint(files_bp) # 註冊 Blueprint

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/about')
# def about():
#     return "This is the About Page"

if __name__ == '__main__':
    app.run(debug=True)
