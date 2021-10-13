#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import sys
import os
import wave
import json
from util import *


if not os.path.exists("model"):
    print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
    exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print ("Audio file must be WAV format mono PCM.")
    exit (1)

model = Model("model")

# You can also specify the possible word list
rec = KaldiRecognizer(model, wf.getframerate(), "bitcoin facebook google zero one two three four five six seven eight nine hello good morning [unk]")
rec = KaldiRecognizer(model, wf.getframerate(),
            "zero one two three four five six seven eight nine ten \
            google facebook tesla microsoft amazon apple [unk]")



try:
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
except:
    print("gocha bitch")


# stock price
TODAY = "2021-10-13"
stock_dict = get_today(TODAY).to_dict()
for k, v in stock_dict.items():
    print(k, v)

# cryptocurrencies
coins = ["bitcoin", "ethereum"]
coin_price = get_crypto_price(coins)
btc_price, eth_price = coin_price['bitcoin']['usd'], coin_price['ethereum']['usd']
print("bitcoin: {}\nethereum: {}".format(btc_price, eth_price))
