from libraries_import import *

##  TODO: FIX !VERY IMPORTANT! The voice data are buffered in memory (OOM Exception), find workaround.
class MicrophoneRecorder(QThread):
    voice_data = pyqtSignal(object)
    def __init__(self, rate=4000, chunksize=1024):
        super(MicrophoneRecorder, self).__init__()
        self.rate = rate
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.new_frame)
        self.lock = threading.Lock()
        self.stop = False
        self.frames = []
        print("MicrophoneRecorder initialized")
        #atexit.register(self.stop_recording)

    def new_frame(self, data, frame_count, time_info, status):
        data = np.frombuffer(data, 'int16')
        
        with self.lock:
            self.frames.append(data)
            
            self.voice_data.emit(data)
            
            if self.stop:
                return None, pyaudio.paComplete
        return None, pyaudio.paContinue
    
    def get_frames(self):
        with self.lock:
            frames = self.frames
            
            self.frames = []
            return frames
    
    def start_recording(self):
        self.stop = False
        print("Starting Recording")
        self.stream.start_stream()

    def stop_recording(self):
        #with self.lock:
        self.stop = True
        self.stream.stop_stream()

        
    def save_file(self,filename="test"):
        frames = self.get_frames()
        wf = wave.open("./data/" +filename+ "/Audio/"+ filename+".wav", 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        print("saved")