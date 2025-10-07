from flask import Flask, render_template, request, jsonify, Response, abort
from src.Line import Line, get_lines_list
from src.Weather import City_Weather
from typing import Tuple

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def dashboard() -> str:
    return render_template('index.html')

@app.route('/placeholder')
def placeholder() -> str:
    return render_template('placeholder.html')

@app.route('/line_status/<string:line_name>')
def line_status_display(line_name: str) -> Tuple[str, int]:
    display_name = request.args.get('display_name', line_name)

    line: Line = Line(line_name, display_name)
    try:
        line.cache_status()
    except Exception:
        return render_template('line_status/line_not_found.html', line_name = line_name), 404
    
    return render_template('line_status/line_status.html', line = line), 200

@app.route('/lines')
def get_lines() -> Response:
    return jsonify(get_lines_list())

@app.route('/line_statuses')
def line_statuses() -> str:
    lines = get_lines_list()
    return(render_template('line_status/line_statuses.html', lines = lines))

@app.route('/weather/<string:city>')
def get_weather_for_city(city: str) -> Tuple[str, int]:
    display_name = request.args.get('display_name', city)
    
    weather = City_Weather(city, display_name)
    try:
        return render_template("weather/city_weather.html", weather = weather), 200
    except Exception:
        abort(404)

if __name__ == '__main__':
    app.run(port = 8000, debug = True, host = "0.0.0.0")