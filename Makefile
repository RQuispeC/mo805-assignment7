all:
	mkdir MO445-descriptors/examples/mpeg7_pgm
	mkdir MO445-descriptors/examples/mpeg7_features
	python3 convert_mpeg_pgm.py
	mkdir MO445-descriptors/lib
	mkdir MO445-descriptors/obj
	cd MO445-descriptors/examples && \
	python3 file_name.py && \
	make && \
	./test
	python3 precision_recall.py