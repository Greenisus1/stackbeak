import unittest,tempfile
from pathlib import Path
from unittest.mock import patch
import stackbeak as a

class Tests(unittest.TestCase):
 def mk(self,seed=1):return a.Run(30,120,seed=seed)
 def test_initial(self):
  g=self.mk();self.assertEqual(g.stack,2);self.assertEqual(g.score,0);self.assertFalse(g.over);self.assertEqual(g.obstacles,[])
 def test_tap(self):
  g=self.mk();self.assertTrue(g.tap());self.assertEqual(g.stack,3)
 def test_tap_cap(self):
  g=self.mk();g.stack=8;self.assertFalse(g.tap());self.assertEqual(g.stack,8);self.assertIn('full',g.message)
 def test_spawn(self):
  g=self.mk();g.spawn();self.assertEqual(len(g.obstacles),1)
  o=g.obstacles[0];self.assertTrue(1<=o['h']<=5);self.assertEqual(o['x'],float(g.w)+4)
 def test_wall_heights(self):
  g=self.mk(7)
  for _ in range(20):g.spawn()
  self.assertTrue(all(1<=o['h']<=5 for o in g.obstacles))
 def test_shave(self):
  g=self.mk();g.nextobs=9999;g.stack=5
  g.obstacles=[{'x':float(g.bx),'h':3,'passed':False}]
  g.tick(.001)
  self.assertTrue(g.obstacles[0]['shaved']);self.assertEqual(g.stack,2);self.assertEqual(g.score,3);self.assertGreater(g.fever,0)
 def test_bonk(self):
  g=self.mk();g.nextobs=9999;g.stack=1
  g.obstacles=[{'x':float(g.bx),'h':2,'passed':False}]
  g.tick(.001)
  self.assertTrue(g.over);self.assertEqual(g.score,0);self.assertIn('R restarts',g.message)
 def test_pass_bonus(self):
  g=self.mk();g.nextobs=9999
  g.obstacles=[{'x':float(g.bx-4),'h':1,'passed':False,'shaved':True}]
  g.tick(.001);self.assertTrue(g.obstacles[0]['passed']);self.assertEqual(g.score,5)
 def test_fever_pass_bonus(self):
  g=self.mk();g.nextobs=9999;g.fever=2.
  g.obstacles=[{'x':float(g.bx-4),'h':1,'passed':False,'shaved':True}]
  g.tick(.001);self.assertEqual(g.score,10)
 def test_fever_decay(self):
  g=self.mk();g.nextobs=9999;g.fever=1.;g.tick(.1);self.assertAlmostEqual(g.fever,.9)
 def test_dt_clamp(self):
  g=self.mk();g.nextobs=9999;g.tick(10);self.assertAlmostEqual(g.world,1.)
 def test_offscreen_removed(self):
  g=self.mk();g.nextobs=9999;g.obstacles=[{'x':-5.,'h':2,'passed':True}];g.tick(.001);self.assertEqual(g.obstacles,[])
 def test_deterministic(self):
  a1=self.mk(42);a2=self.mk(42)
  a1.spawn();a2.spawn();self.assertEqual(a1.obstacles[0]['h'],a2.obstacles[0]['h'])
 def test_record(self):
  with tempfile.TemporaryDirectory() as d,patch.object(a,'RECORD',Path(d)/'best.json'):
   self.assertTrue(a.save(50));a.save(2);self.assertEqual(a.best(),50)
if __name__=='__main__':unittest.main()
