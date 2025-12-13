import numpy as np
from scipy.io.wavfile import write

# Parâmetros do som
samplerate = 44100  # Hz
frequency = 440.0   # Hz
duration = 1.0      # segundos

# Gerar o tom
t = np.linspace(0., duration, int(samplerate * duration))
amplitude = np.iinfo(np.int16).max * 0.5
data = amplitude * np.sin(2. * np.pi * frequency * t)

# Escrever o arquivo .wav
write("assets/test_sound.wav", samplerate, data.astype(np.int16))

print("Arquivo 'assets/test_sound.wav' gerado com sucesso!")
