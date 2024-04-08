import numpy as np
from PIL import Image
from . import shuffling_algorithms as sa
from skimage.metrics import peak_signal_noise_ratio, structural_similarity


class ImageShuffler:
    def __init__(self, image):
        if isinstance(image, str):
            self.image = Image.open(image)
        else:
            self.image = image
        self.pixels = np.array(self.image)
        self.pixels_flat = self.pixels.reshape(-1, 3)
        self.width, self.height = self.image.size
        self.flat_index_array = np.arange(self.width * self.height)
        self.image_path = image if isinstance(image, str) else None
        self.scrambled = None
        self.scrambled_pixels = None

    def shuffle_func_method(self, func, repeats, *args, **kwargs):
        for _ in range(repeats):
            self.flat_index_array = func(self.flat_index_array, *args, **kwargs)
        self.apply_indexes()

    def __getattr__(self, name):
        try:
            algorithm_func = getattr(sa, name)
            return lambda repeats, *args, **kwargs: self.shuffle_func_method(algorithm_func, repeats, *args, **kwargs)
        except AttributeError:
            raise AttributeError(f"{self.__class__.__name__} object has no attribute {name}")

    def display_image(self):
        if self.scrambled is None:
            self.image.show()
        else:
            self.scrambled.show()

    def save_scrambled(self, file_path):
        assert self.scrambled is not None, "Image not scrambled yet"
        self.scrambled.save(file_path)

    def apply_indexes(self):
        self.scrambled_pixels = self.pixels_flat[self.flat_index_array].reshape(self.height, self.width, 3)
        self.scrambled = Image.fromarray(self.scrambled_pixels)

    def scrambling_score(self):
        assert self.scrambled is not None, "Image not scrambled yet"
        assert self.scrambled_pixels.shape == self.pixels.shape, "Scrambled image must have the same shape as the original image"
        return np.mean(np.abs(self.pixels - self.scrambled_pixels)) / 255

    def has_the_same_pixels(self):
        sorted_original_pixels = np.sort(self.pixels.flatten())
        sorted_scrambled_pixels = np.sort(self.scrambled_pixels.flatten())

        return np.array_equal(sorted_original_pixels, sorted_scrambled_pixels)

    def is_scrambled(self):
        return not np.array_equal(self.pixels.flatten(), self.scrambled_pixels.flatten)

    @staticmethod
    def is_same_image(img1, img2):
        return np.array_equal(img1.pixels.flatten(), img2.pixels.flatten())

    def calculate_scrambling_performance(self):
        original_array = np.array(self.pixels)
        scrambled_array = np.array(self.scrambled)
        # Ensure that the arrays have the same shape
        if original_array.shape != scrambled_array.shape:
            raise ValueError("The original and scrambled arrays must have the same shape.")

        #Handle grayscale
        if len(original_array.shape) == 2:
            original_array = original_array[:, :, np.newaxis]
            scrambled_array = scrambled_array[:, :, np.newaxis]

        psnr = peak_signal_noise_ratio(original_array, scrambled_array)
        ssim = structural_similarity(original_array, scrambled_array, multichannel=True, channel_axis=2)
        mse = np.mean((original_array - scrambled_array) ** 2)

        return {
            "PSNR":psnr,
            "SSIM":ssim,
            "MSE":mse,
            "RMSE":np.sqrt(mse),
            }

