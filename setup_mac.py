from setuptools import setup
import development

"""
py2app build script for MyApplication

Usage:
    python setup_mac.py py2app
"""

icon_path = development.Path.root + 'icon.icns'

OPTIONS = {
	'iconfile': icon_path
}
setup(
	name="BATTLE SCENE Prototype",
	app=["game.py"],
	options={'py2app': OPTIONS},
	setup_requires=["py2app"]
)