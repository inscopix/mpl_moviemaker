import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation, rc
from tqdm import tqdm
import numpy as np

class Movie(object):

    def __init__(self, start_frame, end_frame, fps, output_filename, fig_ax_func, frame_func, frame_interval=1, ffmpeg_path='/usr/bin/ffmpeg', matplotlib_style='dark_background', *args, **kwargs):
        '''
        init function for Movie class

        Args:
            start_frame (int): initial frame for output movie
            end_frame (int): final frame for output movie
            fps (float): desired playback speed of output movie in frames per second
            output_filename (str): output filename. type is specified by extension
            fig_ax_func (function): user defined function to generate figure and axes. must return fig, ax tuple
            frame_func (function): user defined function to plot frame. must take fig, ax, frame_number as inputs, plus additional *args, **kwargs
            frame_interval (int, optional): step between frames. Defaults to 1.
            ffmpeg_path (str, optional): path to ffmpeg install location on user's system. Defaults to '/usr/bin/ffmpeg'
            matplotlib_style (str, optional): desired matplotlib style. Defaults to 'dark_background'
        '''

        mpl.rcParams['animation.ffmpeg_path'] = ffmpeg_path
        plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

        self.matplotlib_style = matplotlib_style

        self.output_filename = output_filename

        self.fig_ax_func = fig_ax_func
        self.frame_func = frame_func

        self.start_frame = start_frame
        self.end_frame = end_frame
        self.frame_interval = frame_interval
        self.frames = np.arange(
            self.start_frame,
            self.end_frame,
            self.frame_interval
        )
        self.fps = fps

        self.args = args
        self.kwargs = kwargs
        self.writer = self.set_up_writer()


    def clear_axes(self, ax):
        '''
        clear axes
        checks types to clear either single axis or array/dict of axes

        Args:
            ax (matplotlib axis, array of axes, or dict with axes as values): axes to clear
        '''
        try:
            ax.cla()
        except AttributeError:
            if isinstance(ax, np.ndarray):
                for subaxis in ax.flatten():
                    subaxis.cla()
            elif isinstance(ax, dict):
                for key in ax.keys():
                    ax[key].cla()


    def update(self, frame_number):
        '''
        method to update figure
        animation class will call this on every frame

        Args:
            frame_number (int): current frame number
        '''
        self.clear_axes(self.ax)

        self.frame_func(
            self.fig, 
            self.ax, 
            frame_number,
            *self.args,
            **self.kwargs)

        self.pbar.update(1)


    def set_up_writer(self):
        '''
        instantiates the matplotlib writer object

        Returns:
            FFMpegWriter: the FFMpegWriter object
        '''

        writer = animation.FFMpegWriter(
            fps=self.fps,
            codec='mpeg4',
            bitrate=-1,
            extra_args=['-pix_fmt', 'yuv420p', '-q:v', '5']
        )
        return writer

    def make_movie(self):
        '''
        a wrapper on the matplotlib animation.FuncAnimation class
        user calls this without arguments after instantiating the Movie class
        '''
        with plt.style.context(self.matplotlib_style):
            self.fig, self.ax = self.fig_ax_func()
            a = animation.FuncAnimation(
                self.fig,
                self.update,
                frames=self.frames,
                interval=1/self.fps*1000,
                repeat=False,
                blit=False
            )

            with tqdm(total=len(self.frames)) as self.pbar:
                a.save(
                    self.output_filename,
                    writer=self.writer
                )