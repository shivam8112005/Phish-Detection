from flask import Flask, render_template, request

#app
app = Flask(__name__)

#routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scam/', methods = ['GET', 'POST'])
def detect_scam():
    if "file" not in request.files:
        pass
         

#python main
if  __name__ == '__main__':
    app.run(debug=True)