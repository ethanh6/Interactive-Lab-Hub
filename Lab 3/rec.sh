#!/bin/bash

echo "=== cleaning ==="
# rm my_recorded_mono.wav

echo "=== recording ==="
# arecord -D hw:2,0 -f cd -c1 -r 48000 -d 5 -t wav my_recorded_mono.wav

echo "=== decrypting ==="
# python3 main.py my_recorded_mono.wav


# to make it say a sentence
# espeak -ven+f2 -k5 -s150 --stdout "Hello motherfucker" | aplay


# to make it play an audio file
# aplay my_recorded_mono