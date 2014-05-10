android: 
	python combineFiles combine
	buildozer android debug deploy run
	python combineFiles clean

play:
	sudo python main.py

sipad:
	echo Simulate ipad2 screen
	python combineFiles combine	
	sudo python main.py -m screen:ipad
	python combineFiles clean

sandroid:
	echo Simulate Motorola Droid 2 screen
	python combineFiles combine	
	sudo python main.py -m screen:droid2
	python combineFiles clean

clean:
	python combineFiles clean

