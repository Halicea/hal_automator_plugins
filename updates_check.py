'''
Created on Dec 5, 2013

@author: Costa Halicea
'''
import os
import subprocess

orig_dir = os.getcwd()
def update_pending():
  global orig_dir
  orig_dir = os.getcwd()
  orig_dir = os.getcwd()
  should_update = False
  try:
    os.chdir(os.path.dirname(__file__))
    should_update = subprocess.check_output('git diff origin/master'.split(' '))
  except:
    pass
  finally:
    os.chdir(orig_dir)
  return should_update

def update_if_needed():
  if update_pending():
    try:
      os.chdir(os.path.dirname(__file__))
      should_update = subprocess.check_output('git diff origin/master'.split(' '))  # @UnusedVariable
    except:
      pass
    finally:
      os.chdir(orig_dir)
