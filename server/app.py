from flask import Flask, request
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    logging.info(f"Received callback data: {data}")
    return 'Callback received', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
