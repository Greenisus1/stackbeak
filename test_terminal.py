"""Real PTY controls/resize/restore test; no third-party dependencies."""
import os,pty,subprocess,fcntl,termios,struct,time,select

def main():
 m,s=pty.openpty();fcntl.ioctl(s,termios.TIOCSWINSZ,struct.pack('HHHH',34,100,0,0));before=termios.tcgetattr(s)
 p=subprocess.Popen(['python3','stackbeak.py'],stdin=s,stdout=s,stderr=s,env=dict(os.environ,TERM='xterm-256color',LANG='C.UTF-8'));out=b''
 def collect(sec):
  nonlocal out
  end=time.monotonic()+sec
  while time.monotonic()<end:
   if select.select([m],[],[],.02)[0]:out+=os.read(m,65536)
 collect(.3)
 for key in [b' ',b' ',b' ',b'w',b'P',b'p',b'R']:os.write(m,key);collect(.2)
 fcntl.ioctl(s,termios.TIOCSWINSZ,struct.pack('HHHH',16,50,0,0));os.kill(p.pid,28);collect(.15)
 assert b'Resize to 60x20' in out
 fcntl.ioctl(s,termios.TIOCSWINSZ,struct.pack('HHHH',34,100,0,0));os.kill(p.pid,28);collect(.1);os.write(m,b'R');collect(.1)
 with open('/tmp/stackbeak-terminal.ansi','wb') as f:f.write(out)
 os.write(m,b'Q');collect(.15);p.wait(timeout=3)
 assert p.returncode==0 and termios.tcgetattr(s)==before
 assert b'STACKBEAK' in out and b'SCORE' in out
 os.close(m);os.close(s);print('PTY stack/pause/restart/resize/uppercase quit/terminal restoration PASS')
if __name__=='__main__':main()
