#!/usr/bin/env python
import os
import sys
from pocketsphinx import Pocketsphinx, AudioFile, get_model_path, get_data_path

print(sys.argv)
if len(sys.argv)>1 :
    fin_path=sys.argv[1]
else:
    fin_path='lindySpeechTest.raw'

if len(sys.argv)>2 :
    fout_path=sys.argv[2]
else:
    fout_path='pocketsphinx.log'

fout=open(fout_path,'w')

model_path = get_model_path()
data_path = get_data_path()

config = {
    'verbose': False,
    'audio_file': os.path.join(fin_path),
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
}

audio = AudioFile(**config)
for phrase in audio:
    print(str(phrase))
    fout.write(str(phrase))

fout.close()
