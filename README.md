# Precision vs Recall
This repo implements the assignment 7 of [MO805](http://www.ic.unicamp.br/~rtorres/mo805A_19s1/07-assignment.pdf) at UNICAMP.

![](precision_recall.png?raw=true)

# Implemented/Modified scripts

* `convert_mpeg_pgm.py` converts the `.gif` images of `mpeg7/`dataset to `.pgm` and stores them inside `MO445-descriptors/examples/mpeg7_pgm`

* `MO445-descriptors/examples/test.c` extracts Multiscale Fractal Dimension and Segment Saliences features and stores them inside `MO445-descriptors/examples/mpeg7_features`

* `MO445-descriptors/examples/file_name.py` is a small scripts that creates files with the paths and names of `MO445-descriptors/examples/mpeg7_pgm`.

* `precision_recall.py` computes the precision x recall curve and plots it in `precision_recall.png`

# Replicate Results

Clone the repository

```
git clone https://github.com/RQuispeC/mo805-assignment7.git
```

Then run all the scripts using the available Makefile

```
cd mo805-assignment7
make
```

# Prerequisites

The code was tested under a linux distribution with :

* GCC
* Python3
* Numpy
* MatplotLib
* PIL

# Notes

I used euclidean distance to compare feacture vectors for both Multiscale fractal and Segment salience descriptors. MO455 code offers a different distance function for Segment salience but euclidean may get better performance.
