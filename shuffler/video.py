from PIL import Image
from .image import ImageShuffler
import numpy as np
import cv2

class FrameShuffler:
    def __init__(self, frame):
        self.original_frame = Image.fromarray(frame)
        self.shuffler = ImageShuffler(self.original_frame)

    @property
    def scrambled_pixels(self):
        if self.shuffler.scrambled_pixels is None:
            return None
        return np.array(self.shuffler.scrambled_pixels)

class VideoShuffler:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video = cv2.VideoCapture(self.video_path)
        self.frame_count = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_rate = self.video.get(cv2.CAP_PROP_FPS)
        self.frames = []
        success, frame = self.video.read()
        while success:
            self.frames.append(FrameShuffler(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            success, frame = self.video.read()

    def __getattr__(self, attr):
        def wrapper(*args, **kwargs):
            for frame_shuffler in self.frames:
                method = getattr(frame_shuffler.shuffler, attr, None)
                if method is not None and callable(method):
                    method(*args, **kwargs)
                else:
                    raise AttributeError(f"'{type(self).__name__}' and '{type(frame_shuffler.shuffler).__name__}' object has no attribute '{attr}'")
        return wrapper

    def write_scrambled(self, output_path=None):
        if output_path is None:
            split_path = self.video_path.split('.')
            f"{split_path[0]}_scrambled.{split_path[1]}"

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_video = cv2.VideoWriter(output_path, fourcc, self.frame_rate, (self.frame_width, self.frame_height))
        for frame_shuffler in self.frames:
            frame_bgr = cv2.cvtColor(frame_shuffler.scrambled_pixels, cv2.COLOR_RGB2BGR)
            output_video.write(frame_bgr)

        self.video.release()
        output_video.release()
