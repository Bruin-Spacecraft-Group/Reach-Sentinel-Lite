default:
	build
	run

build:
	clear; docker build -t reach-lite .

run:
	clear; docker run -it --rm reach-lite
