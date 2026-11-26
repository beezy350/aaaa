#!/bin/bash
# Be Bold DEFAULT voice polish (owner: "This is Best", Nov 25 2026). Input = joined Chatterbox clips (ex 0.75, cfg 0.4, ref_deep_warm.wav).
# Trims low rumble, adds warmth + light saturation + very light studio room, loud (~-12 LUFS).
# bebold_voice.sh in.wav out.wav [tempo=0.96]
IN="$1"; OUT="$2"; T="${3:-0.96}"
ffmpeg -y -loglevel error -i "$IN" -af "atempo=$T,highpass=f=95,equalizer=f=140:t=q:w=1:g=-2.5,equalizer=f=230:t=q:w=1.2:g=1.5,equalizer=f=380:t=q:w=1.4:g=-1.5,equalizer=f=3000:t=q:w=1.4:g=2,highshelf=f=9000:g=1,asoftclip=type=tanh:threshold=0.7,deesser=i=0.3,aecho=0.85:0.9:23|41:0.10|0.06,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=2,loudnorm=I=-14:TP=-2,volume=6.5dB,alimiter=limit=0.89:attack=3:release=40:level=disabled" -ar 48000 "$OUT"
