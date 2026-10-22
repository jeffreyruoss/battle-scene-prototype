#!/usr/bin/python


class Config:
	mute_music = False # True or False
	start_scene = '' # skip to scene. example: 'intro', 'battle', etc. Use False or '' to load as normal


"""
py2app requires absolute path for some reason. 
"""
class Path:
	root = '/Users/jeffreyruoss/Game Dev/PROJECTS/Battle Scene v2/'