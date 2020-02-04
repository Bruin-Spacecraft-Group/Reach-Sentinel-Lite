default: build run

build:
	clear; docker build -t reach-lite .

run:
	#clear; docker run -it --rm -p 8000:8000 reach-lite #bash
	#clear; docker run -it --rm -p 127.0.0.1:8000:8000 reach-lite
	#clear; docker run -p 8000:8000 -it reach-lite python3 -m http.server --bind 0.0.0.0
	clear; docker run -p 8000:8000 -it reach-lite #python3 --bind 0.0.0.0
