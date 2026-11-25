#!/bin/bash
# Owner's REAL voice preset (Nov 25, owner feedback): NO de-essing — cutting the high "s" band made
# "s" sound like a child's "th" (boks, taslim). Keep every consonant natural; only catch p/b pops,
# warm bass, cut boxy mids, gentle compression, loud (~-12.5 LUFS). No AI cleanup, gate or pitch shift.
# usage: janob_natural.sh in.wav out.wav
IN="$1"; OUT="$2"
ffmpeg -y -loglevel error -i "$IN" -af "highpass=f=70,adynamicequalizer=dfrequency=100:dqfactor=0.8:tfrequency=100:tqfactor=0.8:threshold=0.12:ratio=6:mode=cut:attack=1:release=50,equalizer=f=110:t=q:w=1:g=4.5,equalizer=f=350:t=q:w=1.4:g=-2.5,acompressor=threshold=-20dB:ratio=2:attack=15:release=150:makeup=1.5,loudnorm=I=-13:TP=-2:LRA=7,volume=3dB,alimiter=limit=0.89:attack=5:release=50:level=disabled" -ar 48000 "$OUT"
