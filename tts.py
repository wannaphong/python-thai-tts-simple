# -*- coding: utf-8 -*-
import pyaudio
import wave
import codecs
from glob import glob
from pythainlp.tokenize import dict_word_tokenize,create_custom_dict_trie
from marisa_trie import Trie
from pydub import AudioSegment
class tts:
    def __init__(self,file="temp.wav"):
        self.chunk = 1024
        self.data_file={}
        with codecs.open('data.txt','r',encoding='utf-8-sig') as self.f:
            self.t= self.f.read()
        for self.line in self.t.split("\n"):
            self.data_file[self.line.split(',')[0]]=self.line.split(',')[1].replace('\r\n', '').replace('\r', '')
        self.word_list=self.data_file.keys()
        self.file=file
    def run(self,text):
        self.sound=None
        self.text_cut=dict_word_tokenize(text,Trie(self.word_list))
        self.i=0 # ประกาศตัวแปร i เพื่อใช้ในการลูป
        self.num_sound=0 # ประกาศตัวแปร num_sound สำหรับเก็บจำนวนเสียงที่ถูกรวม
        while self.i<len(self.text_cut):
            if self.text_cut[self.i] in self.word_list and self.num_sound==0: # ถ้ามีคำนี้ในระบบและเป็นคำแรกที่รวม
                self.sound=AudioSegment.from_wav("data/"+self.data_file[self.text_cut[self.i]]+".wav") # ให้ self.sound แทนไฟล์เสียงที่ถูกตัดไฟล์แรก
                self.num_sound+=1
            elif self.text_cut[self.i] in self.word_list:
                self.sound+=AudioSegment.from_wav("data/"+self.data_file[self.text_cut[self.i]]+".wav") # ทำการรวมไฟล์เสียงเข้าไป
                self.num_sound+=1
            self.i+=1
        self.sound.export(self.file, format="wav")
    def play(self):
        self.f = wave.open(self.file,"rb")
        self.p = pyaudio.PyAudio()  
        #open stream  
        self.stream = self.p.open(format = self.p.get_format_from_width(self.f.getsampwidth()),  
                channels = self.f.getnchannels(),  
                rate = self.f.getframerate(),  
                output = True)
        #read data  
        self.data = self.f.readframes(self.chunk)  
        #play stream  
        while self.data:  
            self.stream.write(self.data)  
            self.data = self.f.readframes(self.chunk)  
        #stop stream  
        self.stream.stop_stream()  
        self.stream.close()  
        #close PyAudio  
        self.p.terminate()  
if __name__ == '__main__':
    t=tts()
    print("TTS พัฒนาโดย นาย วรรณพงษ์ ภัททิยไพบูลย์")
    while True:
        text=input("Text : ")
        if text=="exit" :
            break
        else:
            t.run(text)
            t.play()