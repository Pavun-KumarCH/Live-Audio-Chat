import os
import asyncio
import pyaudio
from dotenv import load_dotenv
from google import genai
from google.genai.types import SpeechConfig, VoiceConfig, PrebuiltVoiceConfig

load_dotenv()

model_id = "gemini-2.0-flash-exp"
client = genai.Client(api_key = os.getenv("GOOGLE_API_KEY"), http_options = {"api_version": "v1alpha"}) # Http option to define api version

# config = {"response_modalities": ["TEXT"]}  # we can also pass AUDIO
config = {"responseModalities": ["AUDIO","TEXT"],
          "speechConfig": SpeechConfig(
              voiceConfig = VoiceConfig(
                  prebuiltVoiceConfig = PrebuiltVoiceConfig()))}

async def chat_with_gemini():
    # live client connection real time
    async with client.aio.live.connect(model = model_id, config = config) as session: 
        while True:

            message = input("Pavan: ")
            await session.send(message, end_of_turn = True) # end_of_turn we are teeling the model that we done speaking


            # listening to Gemini's response
            p = pyaudio.PyAudio()
            stream = p.open(format = pyaudio.paInt16,
                            channels = 1,
                            rate = 24000,  # sample rate 24000 Hz
                            output = True)
            
            async for response in session.receive():
                # print(f"Gemini 2.0: {response.text}")
                if response.server_content and response.server_content.model_turn:
                    for part in response.server_content.model_turn.parts:
                        stream.write(part.inline_data.data)

if __name__ == "__main__":
    asyncio.run(chat_with_gemini())