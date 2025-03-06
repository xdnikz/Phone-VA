from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def execute_command():
    data = request.json
    action = data.get("action")
    param = data.get("data")

    if action == "whatsapp":
        os.system(f'am start -a android.intent.action.SEND -t "text/plain" --es android.intent.extra.TEXT "{param}"')
    
    elif action == "call":
        os.system(f'am start -a android.intent.action.CALL -d tel:{param}')

    elif action == "open_browser":
        os.system(f'am start -a android.intent.action.VIEW -d "{param}"')

    return {"status": "executed", "action": action}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
