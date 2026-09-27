# LiveKit Voice AI Agent (Ashley)

Reusable LiveKit voice agent: Deepgram STT + Gemma LLM + Inworld TTS.
Yeh package aap dobara kisi bhi naye project mein copy karke seedha chala sakte hain.

## Folder contents / Folder mein kya hai

```
livekit-voice-agent/
├── agent.py          # main agent code
├── requirements.txt  # python dependencies
├── .env.example       # env template (rename to .env and fill your keys)
└── README.md          # yeh file
```

## Setup (English)

1. **Extract the zip** and open a terminal inside the folder.

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your `.env` file**:
   - Rename `.env.example` to `.env`
   - Fill in your LiveKit Cloud credentials (get these from https://cloud.livekit.io → your project → Settings → Keys):
     ```
     LIVEKIT_URL=wss://your-project.livekit.cloud
     LIVEKIT_API_KEY=your_api_key
     LIVEKIT_API_SECRET=your_api_secret
     ```
   - `inference.STT`, `inference.LLM`, and `inference.TTS` use LiveKit's hosted inference — no separate Deepgram/Google/Inworld keys are needed as long as your LiveKit Cloud project has inference enabled.

5. **Run the agent in dev mode** (opens a local test console):
   ```bash
   python agent.py dev
   ```
   This starts the worker and gives you a link/console to test the voice conversation in your browser.

   Other useful modes:
   - `python agent.py console` — talk to the agent directly in your terminal (mic/speaker), no browser needed.
   - `python agent.py start` — production mode, connects to LiveKit Cloud and waits for real rooms/calls.

6. To actually talk to it from a browser app, you need a LiveKit frontend (e.g. the LiveKit Agents Playground at https://agents-playground.livekit.io, or your own app) connected to the same LiveKit project.

## Setup (Urdu/Roman Urdu)

1. Zip ko extract karein aur us folder ke andar terminal kholein.

2. Virtual environment banayein (behtar hai):
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Dependencies install karein:
   ```bash
   pip install -r requirements.txt
   ```

4. `.env` file set karein:
   - `.env.example` ko `.env` naam de dein
   - LiveKit Cloud (https://cloud.livekit.io) se apni project ki keys lekar bharein:
     ```
     LIVEKIT_URL=wss://your-project.livekit.cloud
     LIVEKIT_API_KEY=your_api_key
     LIVEKIT_API_SECRET=your_api_secret
     ```

5. Agent chalayein:
   ```bash
   python agent.py dev
   ```
   Ya seedha terminal mein baat karne ke liye:
   ```bash
   python agent.py console
   ```

6. Browser se baat karne ke liye LiveKit Agents Playground (https://agents-playground.livekit.io) use karein, apni LiveKit project se connect karke.

## Reusing this for a new project

- Copy the whole folder, keep `agent.py` and `requirements.txt` as-is.
- Only change: the `instructions` text in the `Assistant` class (personality/behavior), the `voice=` name in `inference.TTS`, and the `.env` keys for your new LiveKit project.
- Naya project shuru karte waqt sirf `.env` aur `Assistant` ke instructions change karein, baqi sab same rakh sakte hain.
