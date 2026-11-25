#!/bin/bash
# Owner's REAL voice, light-touch preset (Nov 25, after heavy chains sounded worse):
# keeps the natural "s" (4-6 kHz untouched, so s never turns into sh), tames only harsh hiss above 6.5 kHz,
# catches p/b pops, warm bass, gentle compression, loud (~-12.5 LUFS). No AI cleanup, no gate, no pitch shift.
# usage: janob_natural.sh in.wav out.wav
IN="$1"; OUT="$2"; D="$(dirname "$0")"; T="${OUT%.wav}"
ffmpeg -y -loglevel error -i "$IN" -af "highpass=f=80,adynamicequalizer=dfrequency=100:dqfactor=0.8:tfrequency=100:tqfactor=0.8:threshold=0.12:ratio=6:mode=cut:attack=1:release=50,equalizer=f=110:t=q:w=1:g=4.5,equalizer=f=350:t=q:w=1.4:g=-2.5,equalizer=f=3000:t=q:w=1.2:g=1" -ar 48000 "${T}_a.wav"
python3 "$D/deess.py" "${T}_a.wav" "${T}_b.wav" -13 6500
ffmpeg -y -loglevel error -i "${T}_b.wav" -af "lowpass=f=13000,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=150:makeup=1.5,loudnorm=I=-13:TP=-2:LRA=6,volume=3dB,alimiter=limit=0.89:level=disabled" -ar 48000 "$OUT"
rm -f "${T}_a.wav" "${T}_b.wav"
