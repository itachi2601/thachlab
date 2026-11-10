# python3 scripts/video-thi-nghiem/render.py <ten clip trong clips/> [--preview]
import importlib, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine
mod = importlib.import_module("clips." + sys.argv[1])
engine.run(mod.CLIP, sys.argv[2:])
