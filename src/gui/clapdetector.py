import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CLAP_THRESHOLD = 7000  # आवाजाच्या संवेदनशीलतेनुसार हा नंबर 5000 ते 10000 दरम्यान बदलू शकता

def wait_for_clap():
    p = pyaudio.PyAudio()
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            peak = np.max(np.abs(audio_data))
            
            if peak > CLAP_THRESHOLD:
                stream.stop_stream()
                stream.close()
                p.terminate()
                return True
    except Exception as e:
        print(f"Clap Detector Error: {e}")
        return False
    
