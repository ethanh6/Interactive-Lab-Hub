#!/bin/bash

arecord -D hw:2,0 -f cd -c1 -r 48000 -d 10 -t wav my_recorded_mono.wav
python3 test_words.py my_recorded_mono.wav