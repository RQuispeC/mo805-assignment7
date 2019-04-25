all:
	mkdir MO445-descriptors/examples/mpeg7_pgm
	mkdir MO445-descriptors/examples/mpeg7_features
	python3 convert_mpeg_pgm.py
	cd MO445-descriptors/examples && \
	python3 file_name.py && \
	make && \
	./test
	python3 precision_recall.py
