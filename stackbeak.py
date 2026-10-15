#!/usr/bin/env python3
"""Original offline stack-and-dash bird runner. Python standard library only."""
import curses,os,json,random,time,sys
from pathlib import Path
from ui import put,run
VERSION='1.0.0'
RECORD=Path.home()/'.local/share/stackbeak/best.json'
class Run:
 def __init__(self,h,w,seed=None):
  self.rng=random.Random(seed);self.h=h;self.w=w
  self.bx=max(6,w//5);self.stack=2;self.world=0.;self.speed=10.
  self.obstacles=[];self.nextobs=30.;self.score=0;self.fever=0.;self.over=False
  self.message='Space/W/Up stacks a block under your bird. Clear the walls!'
 def ground(self):return self.h-4
 def spawn(self):
  hgt=self.rng.randint(1,5)
  self.obstacles.append({'x':float(self.w)+4,'h':hgt,'passed':False})
 def tap(self):
  if self.over:return False
  if self.stack>=8:self.message='Stack is full!';return False
  self.stack+=1;return True
 def tick(self,dt):
  if self.over:return
  dt=min(.1,max(0,dt))
  self.world+=self.speed*dt;self.nextobs-=self.speed*dt
  if self.nextobs<=0:self.spawn();self.nextobs=self.rng.uniform(18,30)
  self.fever=max(0.,self.fever-dt)
  for o in list(self.obstacles):
   o['x']-=self.speed*dt
   if o['x']+2<0:self.obstacles.remove(o);continue
   if o['x']<=self.bx+2 and self.bx-1<=o['x']+2 and not o.get('shaved'):
    if self.stack>=o['h']:
     o['shaved']=True;self.stack-=o['h'];self.score+=o['h']
     self.fever=min(5.,self.fever+1.2)
     self.message='Shaved a wall! +'+str(o['h'])
    else:
     self.over=True;self.message='Bonked the wall. R restarts.';return
   if not o['passed'] and o['x']+2<self.bx-1:
    o['passed']=True;self.score+=5
    if self.fever>0:self.score+=5
def best():
 try:
  if RECORD.is_symlink():return 0
  return max(0,int(json.loads(RECORD.read_text()).get('best',0)))
 except (OSError,ValueError,TypeError,AttributeError):return 0
def save(score):
 try:
  if any(p.is_symlink() for p in [RECORD,*RECORD.parents]):return False
  RECORD.parent.mkdir(parents=True,exist_ok=True,mode=0o700);tmp=RECORD.with_suffix('.tmp');fd=os.open(tmp,os.O_WRONLY|os.O_CREAT|os.O_TRUNC|os.O_NOFOLLOW,0o600)
  with os.fdopen(fd,'w') as f:json.dump({'best':max(score,best())},f)
  tmp.replace(RECORD);return True
 except OSError:return False
def palette():
 if not curses.has_colors():return False
 curses.start_color();curses.use_default_colors()
 values=[(220,-1),(255,-1),(208,-1),(46,-1),(245,-1)] if curses.COLORS>=256 else [(3,-1),(7,-1),(1,-1),(2,-1),(7,-1)]
 for i,(fg,bg) in enumerate(values,1):curses.init_pair(i,fg,bg)
 return True
def play(s):
 h,w=s.getmaxyx();g=Run(h,w);last=time.monotonic();recorded=False;high=best();colors=palette();paused=False
 def color(i):return curses.color_pair(i) if colors else 0
 while True:
  s.timeout(40);key=s.getch();now=time.monotonic();dt=now-last;last=now;h,w=s.getmaxyx();s.erase()
  if key in (27,ord('q'),ord('Q')):return
  if key in (ord('p'),ord('P')):paused=not paused
  if key in (ord('r'),ord('R')):g=Run(h,w);recorded=False;paused=False
  if h<20 or w<60:put(s,1,1,'Resize to 60x20. Simulation paused. Q quits.');s.refresh();continue
  if not g.over and not paused:
   if key in (ord(' '),curses.KEY_UP,ord('w'),ord('W')):g.tap()
   g.tick(dt)
  if g.over and not recorded:g.message+=' Best saved.' if save(g.score) else ' Save unavailable.';recorded=True;high=max(high,best())
  ground=g.ground();top=ground-g.stack
  put(s,0,2,'STACKBEAK | SCORE '+str(g.score)+' | BEST '+str(high)+(' | FEVER' if g.fever>0 else '')+(' | PAUSED' if paused else ''),color(1)|curses.A_BOLD)
  put(s,1,2,g.message,color(2))
  for x in range(w):put(s,ground+1,x,'=',color(5))
  for o in g.obstacles:
   ox=round(o['x'])
   for yy in range(o['h']):
    put(s,ground-yy,ox,'##',color(3))
  for yy in range(g.stack-1):put(s,ground-yy,g.bx,'[]',color(4))
  put(s,top-1,g.bx,'<o',color(1)|curses.A_BOLD)
  put(s,h-2,2,'Space/W/Up stack | P pause | R restart | Q quit',color(2))
  put(s,h-1,2,'Stack high enough to shave each wall: blocks equal to the wall height are spent. Fever doubles pass bonuses.',color(5));s.refresh()
if __name__=='__main__':
 if '--version' in sys.argv:print(VERSION)
 else:raise SystemExit(run(play))
