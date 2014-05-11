android: 
	python combineFiles.py combine
	sudo buildozer android debug deploy run
	python combineFiles.py clean

play:
	sudo python main.py

sipad:
	echo Simulate ipad2 screen
	python combineFiles.py combine
	sudo python main.py -m screen:ipad
	python combineFiles.py clean

sandroid:
	echo Simulate Motorola Droid 2 screen
	python combineFiles.py combine
	sudo python main.py -m screen:droid2
	python combineFiles.py clean

sipad3:
	echo Simulate ipad3 retina screen
	python combineFiles.py combine
	sudo python main.py -m screen:ipad3,scale:0.5
	python combineFiles.py clean

clean:
	python combineFiles clean

