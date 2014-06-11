## commands: list all commands
commands:
	@grep -E '^##' makefile | sed -e 's/##//g'

## debug: use crtl+e to open the inspector
debug:
	python combineFiles.py combine
	sudo python main.py -m inspector
	python combineFiles.py clean

## normal: for PCs
normal:
	python combineFiles.py combine
	sudo python main.py
	python combineFiles.py clean

## play: same as normal
play:
	python combineFiles.py combine
	sudo python main.py
	python combineFiles.py clean

## android: to run on connected android phone
android: 
	python combineFiles.py combine
	sudo buildozer android debug deploy run
	python combineFiles.py clean

## sandroid: simulate android phone
sandroid:
	echo Simulate Motorola Droid 2 screen
	python combineFiles.py combine
	sudo python main.py -m screen:droid2
	python combineFiles.py clean

## sipad: simulate ipad
sipad:
	echo Simulate ipad2 screen
	python combineFiles.py combine
	sudo python main.py -m screen:ipad
	python combineFiles.py clean

## sipad3: simulate ipad3 (retina)
sipad3:
	echo Simulate ipad3 retina screen
	python combineFiles.py combine
	sudo python main.py -m screen:ipad3,scale:0.33
	python combineFiles.py clean

## clean: clean up
clean:
	python combineFiles.py clean
