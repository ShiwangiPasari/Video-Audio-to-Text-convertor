import speech_recognition as sr
import sys
import shutil
from googletrans import Translator
from pathlib import Path
from script.punctuator import custom_punctuator
from script.summarizer import testing_summary
import os
import wave


class Audio:

    def createDirectory(self,path):
        print("creating directory : " + path)
        directoryPath = Path(path)
        if not (directoryPath.exists() and directoryPath.is_dir()):
            directoryPath.mkdir(parents=True, exist_ok=True)

    def audio_to_text(self,video_lst,audio_path):
        try:
            txt_lst=[]
            for video_file in video_lst:

                video_path_part=video_file.split('\\')
                video_name=video_path_part[-1]
                video_cat=video_path_part[-2]

                file_part = video_name.split('.')
                audio_path_mod = os.path.join(audio_path,video_cat)+'\\'+ '.'.join(file_part[:-1])
                self.createDirectory(audio_path_mod)
                audio_file='.'.join(file_part[:-1])+'.wav'
                command = 'ffmpeg -i ' + video_file + ' ' + audio_path_mod + '\\' + audio_file
                os.system(command)
                r=sr.Recognizer()
                translator = Translator()
                dura=30
                lang='en'

                wav_filename=audio_path_mod+'\\'+audio_file

                f = wave.open(wav_filename, 'r')
                frames = f.getnframes()
                rate = f.getframerate()
                audio_duration = frames / float(rate)
                final_text_lst=[]
                counter=0

                with sr.AudioFile(wav_filename) as source:
                    # r.adjust_for_ambient_noise(source)
                    while counter<audio_duration:
                        audio=r.record(source,duration=dura)
                        counter+=dura
                        try:
                            str=r.recognize_google(audio,language=lang)
                            final_text_lst.append(str)
                            # print(str)
                            # final_text_lst.append(translator.translate(str, dest='en').text)
                        except Exception as e:
                            print(e)

                print('Text data generated..')

                text_path=audio_path_mod+'\\'+audio_file.replace('.wav','_audio_text.csv')
                with open(text_path, 'w') as f:
                    f.write(' '.join(final_text_lst))

                custom_punctuator.execute_punctuator(text_path)
                print('Punctuated audio text..')
                # shutil.move(text_path+'.punct.punct.proc.txt',text_path.replace('_audio_text.csv','_text.csv'))
                txt_lst.append(text_path.replace('_audio_text.csv','_text.csv'))

            testing_summary.get_summary(txt_lst,SENTENCES_COUNT=3)
            print('Sumamrization done for punctuated audio text..')

        except Exception as e:
            print(e)
