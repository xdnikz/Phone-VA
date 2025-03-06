from fastapi import FastAPI
import requests
import openai
import speech_recognition as sr

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"

# Phone Listener API URL (इसे फोन पर सेटअप करेंगे)
PHONE_API_URL = "http://your_phone_ip:5000/execute"

app = FastAPI()

# 🎤 Voice से Command लेना
def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="hi-IN")
            print(f"आपने कहा: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return None

# 🧠 AI से Response लेना (GPT-4)
def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        api_key=OPENAI_API_KEY
    )
    return response["choices"][0]["message"]["content"]

# 📲 Phone को Command भेजना
def send_command_to_phone(action, data=""):
    payload = {"action": action, "data": data}
    response = requests.post(PHONE_API_URL, json=payload)
    return response.json()

@app.get("/")
def home():
    return {"message": "Jarvis AI Server Running"}

@app.post("/process_command")
def process_command(command: str):
    if "whatsapp भेजो" in command:
        msg = command.replace("whatsapp भेजो", "").strip()
        send_command_to_phone("whatsapp", msg)
        return {"status": "sent", "message": msg}
    
    elif "कॉल करो" in command:
        number = command.replace("कॉल करो", "").strip()
        send_command_to_phone("call", number)
        return {"status": "calling", "number": number}
    
    elif "गूगल खोलो" in command:
        send_command_to_phone("open_browser", "https://www.google.com")
        return {"status": "browser opened"}

    else:
        ai_response = get_ai_response(command)
        return {"status": "ai_response", "response": ai_response}

# 🎙️ Voice से Command Process करना
@app.get("/listen")
def listen():
    command = listen_command()
    if command:
        return process_command(command)
    return {"status": "no_command"}

# Server Run करने के लिए
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
