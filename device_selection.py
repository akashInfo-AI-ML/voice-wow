import pyaudio



p = pyaudio.PyAudio()
def device_index_tts():
    for i in range(p.get_device_count()):
        info = p.get_device_info_by_index(i)
        if f"{i} {info['name']} - Inputs: {info['maxInputChannels']} | Outputs: {info['maxOutputChannels']}" == "4 CABLE Input (VB-Audio Virtual C - Inputs: 0 | Outputs: 16":
            return i

def DEVICE_INDEX_STT():
    for j in range(p.get_device_count()):
        info = p.get_device_info_by_index(j)        
        if f"{j} {info['name']} - Inputs: {info['maxInputChannels']} | Outputs: {info['maxOutputChannels']}" == "1 CABLE Output (VB-Audio Virtual  - Inputs: 16 | Outputs: 0":
            return j

