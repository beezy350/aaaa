#!/bin/bash
# Owner's REAL recorded voice (Uzbek or English) for Instagram @janobuzbek_2020 — Nov 25 preset.
# Run DeepFilterNet first (clean-audio workflow), then this: extra bass, louder (-10 LUFS),
# strong de-ess on s/sh/ch, plosive (p/b) control, slight pitch down, slightly slower.
# usage: janob_real.sh in.wav out.wav [tempo=0.96]
IN="$1"; OUT="$2"; T="${3:-0.96}"
ffmpeg -y -loglevel error -i "$IN" -af "\
highpass=f=85,\
afftdn=nf=-40:nr=14:tn=1,\
adynamicequalizer=dfrequency=110:dqfactor=0.8:tfrequency=110:tqfactor=0.8:threshold=0.10:ratio=8:mode=cut:attack=1:release=50,\
agate=threshold=0.03:ratio=6:attack=3:release=80:range=0.06,\
rubberband=pitch=0.972:tempo=$T:formant=preserved,\
equalizer=f=100:t=q:w=0.9:g=8,\
equalizer=f=170:t=q:w=1.1:g=4,\
equalizer=f=330:t=q:w=1.4:g=-4,\
equalizer=f=700:t=q:w=1.6:g=-2,\
equalizer=f=3500:t=q:w=1.3:g=1,\
adynamicequalizer=dfrequency=5500:dqfactor=1.4:tfrequency=5500:tqfactor=1.2:threshold=0.02:ratio=10:mode=cut:attack=1:release=30,\
adynamicequalizer=dfrequency=8000:dqfactor=1.2:tfrequency=8000:tqfactor=1.0:threshold=0.015:ratio=10:mode=cut:attack=1:release=30,\
deesser=i=1:m=0.8:f=0.5,\
lowpass=f=10500,\
acompressor=threshold=-26dB:ratio=4:attack=6:release=90:makeup=3,\
loudnorm=I=-13:TP=-2:LRA=4,volume=3.6dB,alimiter=limit=0.89:attack=1:release=30:level=disabled" -ar 48000 -ac 1 "$OUT"
