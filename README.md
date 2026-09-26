# UniGuard AI 



It specifically solves your two requirements:
1. **Easy to share**: You can ZIP this entire folder and send it to anyone. They just double-click `run.bat` and it works out-of-the-box on Windows.
2. **100% Custom AI Trained from Scratch**: This project does NOT use OpenAI, Gemini, or any pre-built AI API. It literally generates synthetic network traffic data, trains a `RandomForestClassifier` locally using Machine Learning math, saves the model weights to a file, and uses that model for threat detection.

## How to run (Windows)
Simply double click the `run.bat` file! It will install dependencies, train the AI, start the servers, open your browser, and wait for you to press a key to launch the attack.

## How to run (Mac/Linux)
You can run the files manually in this order from the terminal:
1. `pip install -r requirements.txt`
2. `python 1_train_model.py` (Generates synthetic data and trains the AI model)
3. `python 2_target_server.py &` (Starts the protected server in the background)
4. `python 3_ai_monitor.py &` (Starts the AI dashboard in the background)
5. Open `http://localhost:5001` in your web browser.
6. `python 4_attacker.py` (Runs the hacker script to trigger the AI alerts)
