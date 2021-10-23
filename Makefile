clean:
	rm -r batches

run:
	PASSWORD=pass DEBUG=false python3 main.py

reverse:
	PASSWORD=pass python3 reader.py

benchmark:
	PASSWORD=pass python3 test.py