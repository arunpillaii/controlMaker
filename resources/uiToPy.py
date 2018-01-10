""" convert ui file to py
"""

from pyside2uic import compileUi
import os as _os

rootDirectory = _os.path.dirname(
	_os.path.abspath(
		_os.path.join(__file__ ,"../")
	)
)
inputPath = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)),"controlMakerWidget.ui")

pyFilePath = _os.path.join(
		rootDirectory,
		"src",
		"ui",
		_os.path.basename(inputPath).replace(".ui", ".py")
	)

with open(pyFilePath, 'w') as pyFile:
	compileUi(inputPath, pyFile, False, 4, False)

