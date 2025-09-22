from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('different_page', name=request.form.get("some stuff")))
    
    return render_template('index.html')

@app.route('/test/')
@app.route('/test/<string:name>')
def different_page(name = None):
    return render_template('test_name.html', name=name)

if __name__ == '__main__':
    app.run(port=8000, debug=True)