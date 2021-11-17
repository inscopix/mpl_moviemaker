# mpl_moviemaker
Wrapper for the Matplotlib Animation class that facilitates movie generation

# Setup Instructions
Clone the repository
```
git clone https://github.com/inscopix/mpl_moviemaker.git
```

Install with pip
```
cd mpl_moviemaker
pip install .
```

# Use
## overview
The functions in this library are built on top of the Matplotlib Animation class and are designed to make movie generation easier.  

The basic concept is that the user defines two functions:
* A function to lay out the figure canvas and axis (or axes) on that canvas
* A function to define what is displayed on those axes for a given frame.
The user then instantiates the `Movie` class, passing it those two functions along with some other parameters (start_frame, end_frame, frame_step, fps, filename). After calling the `make_movie` method on the `Movie` class, each frame will be generated and stacked into a movie with the desired filename.

## a simple example

![Alt Text](https://github.com/inscopix/mpl_moviemaker/sample_movie_1.gif)