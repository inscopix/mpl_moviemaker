import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation, rc
from tqdm import tqdm
import numpy as np

class Movie(object):

    def __init__(self, start_frame, end_frame, fps, output_filename, fig_ax_func, frame_func, frame_interval=1, *args, **kwargs):

        mpl.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'
        plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg'

        plt.style.use('dark_background')

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
        animation class will call this
        the print statement is there to help track progress
        '''
        self.clear_axes(self.ax)

        self.frame_func(
            fig=self.fig, 
            ax=self.ax, 
            frame_number=frame_number,
            *self.args,
            **self.kwargs)

        # print('done plotting at {} seconds'.format(time.time() - t0))

        self.pbar.update(1)

    def set_up_writer(self):

        writer = animation.FFMpegWriter(
            fps=self.fps,
            codec='mpeg4',
            bitrate=-1,
            extra_args=['-pix_fmt', 'yuv420p', '-q:v', '5']
        )
        return writer

    def make_movie(self):
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