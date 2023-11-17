from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/success', methods=['POST'])
def success():
    request_data = request.json
    response_data = {
        "status": "ok",
        "details": request_data
    }
    return jsonify(response_data), 200


@app.route('/fail', methods=['POST'])
def fail():
    response_data = {
        "status": "error",
        "details": ""
    }
    return jsonify(response_data), 503


@app.route('/fail-miserably', methods=['POST'])
def fail_miserably():
    response_data = {
        "status": "error",
        "details": ""
    }
    return jsonify(response_data), 404


if __name__ == '__main__':
    app.run(debug=True)