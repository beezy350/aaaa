#!/bin/bash
# Owner's Instagram voice (Janob) — FINAL preset, Nov 25: podcast style, loud (-11 LUFS), more bass,
# no hiss (stronger noise reduction, no exciter, softer air), no puffs (plosive control + breath gate), strong de-ess.
# usage: janob_voice.sh in.wav out.wav [tempo=0.92]
IN="$1"; OUT="$2"; T="${3:-0.92}"
ffmpeg -y -loglevel error -i "$IN" -af "\
highpass=f=75,\
afftdn=nf=-42:nr=18:tn=1,\
anlmdn=s=0.0008:p=0.004:r=0.006,\
adynamicequalizer=dfrequency=90:dqfactor=0.9:tfrequency=90:tqfactor=0.9:threshold=0.15:ratio=6:mode=cut:attack=1:release=60,\
agate=threshold=0.03:ratio=6:attack=3:release=80:range=0.06,\
rubberband=pitch=0.972:tempo=$T:formant=preserved,\
equalizer=f=105:t=q:w=0.9:g=6,\
equalizer=f=180:t=q:w=1.2:g=3,\
equalizer=f=330:t=q:w=1.4:g=-4,\
equalizer=f=700:t=q:w=1.6:g=-2,\
equalizer=f=3800:t=q:w=1.2:g=1.5,\
adynamicequalizer=dfrequency=6500:dqfactor=1.5:tfrequency=6500:tqfactor=1.2:threshold=0.04:ratio=8:mode=cut:attack=1:release=40,\
deesser=i=0.8:m=0.7:f=0.6,\
lowpass=f=11500,\
acompressor=threshold=-26dB:ratio=4:attack=6:release=90:makeup=3,\
alimiter=limit=0.9:attack=3:release=40,\
loudnorm=I=-11:TP=-1.0:LRA=4" -ar 48000 -ac 1 "$OUT"
