#!/bin/bash
# Radio / podcast voice for the owner's cloned voice (Janob, Instagram only).
# usage: radio_voice.sh in.wav out.wav [style=janob|radio|podcast] [tempo=0.92]   (janob = owner's chosen default)
IN="$1"; OUT="$2"; S="${3:-janob}"; T="${4:-0.92}"; LUFS=-16; MID=1.5
if [ "$S" = radio ]; then PITCH=0.944; LOW=6; COMP="threshold=-26dB:ratio=5:attack=4:release=70:makeup=3"; EXC=3; elif [ "$S" = janob ]; then PITCH=0.972; LOW=7; MID=3; LUFS=-13; COMP="threshold=-26dB:ratio=4:attack=6:release=90:makeup=3"; EXC=1.5   # owner pick Nov 25: podcast + louder + more bass
else PITCH=0.972; LOW=4; COMP="threshold=-24dB:ratio=3.5:attack=6:release=90:makeup=2"; EXC=1.5; fi
# pitch down (~1 semitone radio, ~0.5 podcast) keeping tempo: rubberband
ffmpeg -y -loglevel error -i "$IN" -af "\
highpass=f=60,afftdn=nf=-35,\
agate=threshold=0.02:ratio=4:attack=5:release=60:range=0.15,\
rubberband=pitch=$PITCH:tempo=$T:formant=preserved,\
equalizer=f=95:t=q:w=0.9:g=$LOW,\
equalizer=f=180:t=q:w=1.2:g=$MID,\
equalizer=f=330:t=q:w=1.4:g=-4,\
equalizer=f=700:t=q:w=1.6:g=-2,\
equalizer=f=4000:t=q:w=1.2:g=2.5,\
treble=g=2.5:f=10000:t=s:w=0.7,\
aexciter=amount=$EXC:drive=4:blend=0:freq=2500:ceil=12000,\
deesser=i=0.5:m=0.5:f=0.5,\
acompressor=$COMP,\
alimiter=limit=0.9:attack=3:release=40,\
loudnorm=I=$LUFS:TP=-1.0:LRA=4" -ar 48000 -ac 1 "$OUT"
