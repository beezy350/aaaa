#!/bin/bash
# Studio "condenser mic" chain for the owner's cloned voice (Janob, Instagram only).
# Dry (no reverb), boxy/bathroom mids cut, warm proximity bass, condenser presence + air, tight gate on room tails.
# usage: studio_voice.sh in.wav out.wav [tempo=0.92]
IN="$1"; OUT="$2"; T="${3:-0.92}"
ffmpeg -y -loglevel error -i "$IN" -af "\
highpass=f=70,\
afftdn=nf=-35,\
agate=threshold=0.02:ratio=4:attack=5:release=60:range=0.15,\
atempo=$T,\
equalizer=f=110:t=q:w=1.0:g=3.5,\
equalizer=f=320:t=q:w=1.4:g=-3.5,\
equalizer=f=650:t=q:w=1.6:g=-2,\
equalizer=f=4500:t=q:w=1.2:g=2.5,\
treble=g=3:f=10000:t=s:w=0.7,\
deesser=i=0.45:m=0.5:f=0.5,\
acompressor=threshold=-22dB:ratio=3.5:attack=6:release=90:makeup=2,\
loudnorm=I=-16:TP=-1.5:LRA=6" -ar 48000 -ac 1 "$OUT"
