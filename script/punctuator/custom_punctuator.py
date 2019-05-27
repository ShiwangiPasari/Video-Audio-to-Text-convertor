import requests


def execute_punctuator(file_path):
    # print(f)
    audio_file = open(file_path).read()
    json_file = {"text": audio_file}
    r = requests.post(url="http://bark.phon.ioc.ee/punctuator", params=json_file)
    if r.status_code == 200:
        with open(file_path.replace('_audio_text.csv','_text.csv'),'w') as file:
            file.write(r.text)
    else:
        return "Punctuation of data could not be done."

#
# if __name__ == "__main__":
#     text = execute_punctuator("DigitalLending_v02_android_audio_text.csv")
#     print(text)
