#!/bin/bash
# Studio voice chain for the owner's cloned voice (Janob): warmer bass, slightly slower, broadcast polish.
# usage: studio_voice.sh in.wav out.wav [tempo=0.92]
IN="$1"; OUT="$2"; T="${3:-0.92}"
ffmpeg -y -loglevel error -i "$IN" -af "\
highpass=f=60,\
afftdn=nf=-32,\
atempo=$T,\
equalizer=f=110:t=q:w=1.0:g=4,\
equalizer=f=250:t=q:w=1.2:g=1.5,\
equalizer=f=450:t=q:w=1.5:g=-2,\
equalizer=f=3200:t=q:w=1.4:g=2,\
deesser=i=0.4:m=0.5:f=0.5,\
acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,\
aecho=0.8:0.6:28:0.06,\
loudnorm=I=-16:TP=-1.5:LRA=7" -ar 48000 -ac 1 "$OUT"
