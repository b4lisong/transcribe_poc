# server.py
import asyncio
import ssl
import websockets
import json
from vosk import Model, KaldiRecognizer

# Load the Vosk model
model = Model("models/en-us")

# SSL context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

async def transcribe(websocket):
    """
    Handles incoming WebSocket connections and transcribes audio data.
    """
    print("Client connected")
    recognizer = KaldiRecognizer(model, 16000)

    try:
        while True:
            # Receive audio data from the client
            data = await websocket.recv()
            # Process audio data
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get('text', '')
                print(f"Transcription: {text}")
                # Send the transcription back to the client
                await websocket.send(text)
            else:
                # Handle partial results if needed
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result).get('partial', '')
                # Optionally, send partial results to the client
                # await websocket.send(partial_text)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    """
    Starts the WebSocket server and runs it indefinitely.
    """
    async with websockets.serve(transcribe, "0.0.0.0", 8765, ssl=ssl_context):
        print("Secure WebSocket server started on port 8765")
        await asyncio.Future()  # Keep the server running indefinitely

if __name__ == "__main__":
    # Entry point of the script
    asyncio.run(main())

