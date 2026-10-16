#!/usr/bin/env python3
"""Dựng bài từ data/bai.json — logic ở skill soan-bai-avcn (scripts/build_avcn.py). Chạy: python3 build.py"""
import pathlib, runpy, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.argv = [sys.argv[0], str(HERE)]
runpy.run_path(str(HERE.parents[2] / ".claude/skills/soan-bai-avcn/scripts/build_avcn.py"), run_name="__main__")
