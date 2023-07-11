# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# .\.venv\Scripts\Activate
from flask import Flask, request, jsonify
from flask_cors import CORS
from finalChat import bot_conv
from connector import recommend

app = Flask(__name__)
CORS(app)

@app.route('/Chat', methods=['POST'])
def Chat():
    # Access user data here and process it
    data = request.get_json()
    processed_data = bot_conv(data["message"])

    # Return the processed data as a JSON object
    return jsonify(processed_data)

@app.route('/recommend', methods=['POST'])
def Rec():
    # Access user data here and process it
    data = request.get_json()
    processed_data = recommend(data["message"])

    # Return the processed data as a JSON object
    return jsonify(processed_data)

app.run(host='0.0.0.0', port=5000)