from flask import Flask, render_template, request, redirect, url_for, abort
from Line import Line

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('different_page', name = request.form.get("some stuff")))
    
    return render_template('index.html')

@app.route('/test/')
@app.route('/test/<string:name>')
def different_page(name = None):
    return render_template('test_name.html', name=name)

@app.route('/line_status/<string:line_name>')
def line_status(line_name: str):
    line = Line(line_name)
    try:
        statuses = line.get_status()
    except Exception:
        return render_template('line_status/line_not_found.html', line_name = line_name), 404
    
    return render_template('line_status/line_status.html', line_name = line_name, line_status = statuses)

if __name__ == '__main__':
    app.run(port=8000, debug=True)