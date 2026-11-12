# Narrated slideshow: python3 make_video.py <slides_dir> <out.mp4> <music.mp3> <lines.txt>
import sys,subprocess,os,soundfile as sf,numpy as np,tempfile
from kokoro_onnx import Kokoro
sd,out,music,lf=sys.argv[1:5]
lines=[l.strip() for l in open(lf) if l.strip()]
k=Kokoro('/home/claude/kokoro/kokoro-v1.0.onnx','/home/claude/kokoro/voices-v1.0.bin')
t=tempfile.mkdtemp(); segs=[]
for i,line in enumerate(lines,1):
    a,sr=k.create(line,voice='am_michael',speed=0.92,lang='en-us')
    a=np.concatenate([np.zeros(int(sr*0.35)),a,np.zeros(int(sr*0.6))]); w=f'{t}/v{i}.wav'; sf.write(w,a,sr)
    d=len(a)/sr; fr=int(d*30)+1; s=f'{t}/s{i}.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-i',f'{sd}/slide_{i:02d}.jpg','-i',w,'-filter_complex',
      f"[0:v]scale=2160:3840,zoompan=z='min(1+0.0006*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1920:fps=30,format=yuv420p[v]",
      '-map','[v]','-map','1:a','-t',str(d),'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','aac','-ar','44100','-ac','2',s],check=True)
    segs.append(s)
open(f'{t}/l.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',f'{t}/l.txt','-c','copy',f'{t}/vo.mp4'],check=True)
D=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{t}/vo.mp4']))
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',f'{t}/vo.mp4','-i',music,'-filter_complex',
  f"[1:a]volume=0.14,afade=t=in:d=1.5,afade=t=out:st={D-2}:d=2[m];[0:a][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]",
  '-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','160k','-t',str(D),out],check=True)
print(out,round(D,1))
