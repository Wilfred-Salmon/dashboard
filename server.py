from flask import Flask, render_template, request, redirect, url_for
from src.Line import Line

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
    line: Line = Line(line_name)
    try:
        line.cache_status()
    except Exception:
        return render_template('line_status/line_not_found.html', line_name = line_name), 404
    
    return render_template('line_status/line_status.html', line = line)

@app.route('/line_statuses')
def line_statuses():
    line_names = ["victoria", "district", "circle", "hammersmith-city" ,"metropolitan"]

    lines = [Line(name) for name in line_names]

    return(render_template('line_status/line_statuses.html', lines = lines))

if __name__ == '__main__':
    app.run(port=8000, debug=True)