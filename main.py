from shuffler.image import ImageShuffler
from shuffler.video import VideoShuffler
import shuffler.shuffling_algorithms as sa
from datetime import datetime


def test_random_shuffle(img_path="prezentare/lenna.png", repeats=1):
    shuffler = ImageShuffler(img_path)
    shuffler.random_shuffle(repeats)
    shuffler.save_scrambled("prezentare/random_shuffle.jpg")

def test_fisher_yates(img_path="prezentare/lenna.png", repeats=1):
    shuffler = ImageShuffler(img_path)
    shuffler.fisher_yates_shuffle(repeats)
    shuffler.save_scrambled("prezentare/fisher_yates.jpg")

def test_poisson(img_path="prezentare/lenna.png", repeats=1):
    shuffler = ImageShuffler(img_path)
    shuffler.poisson_charlier_shuffle(repeats, 0.5, 10)
    shuffler.save_scrambled("prezentare/poisson_charlier.jpg")

def test_boriga_dascalescu(img_path="prezentare/lenna.png", repeats=1):
    shuffler = ImageShuffler(img_path)
    shuffler.boriga_dascalescu_shuffle(repeats)
    shuffler.save_scrambled("prezentare/boriga_dascalescu.jpg")

def test_boriga_dascalescu_heap(img_path="prezentare/lenna.png", repeats=1):
    shuffler = ImageShuffler(img_path)
    shuffler.boriga_dascalescu_shuffle_heap(repeats)
    shuffler.save_scrambled("prezentare/boriga_dascalescu_heap.jpg")


def test_boriga_dascalescu_heap2(img_path="prezentare/lenna.png", repeats=1):
    shuffler = ImageShuffler(img_path)
    shuffler.boriga_dascalescu_shuffle_heap2(repeats)
    shuffler.save_scrambled("prezentare/boriga_dascalescu_heap2.jpg")

def test_boriga_dascalescu_set(img_path="prezentare/boriga_dascalescu_set.jpg"):
    shuffler = ImageShuffler(img_path)
    shuffler.boriga_dascalescu_shuffle_set(repeats)
    shuffler.save_scrambled("prezentare/boriga_dascalescu_set.jpg")

def test_all_shufflers():
    test_random_shuffle()
    test_fisher_yates()
    test_poisson(repeats=20)
    test_boriga_dascalescu(repeats=10)
    test_boriga_dascalescu_heap()
    test_boriga_dascalescu_heap2()

def test_is_same_image():
    shuffler = ImageShuffler("prezentare/lenna.png")
    shuffler2 = ImageShuffler("prezentare/boriga_dascalescu.jpg")
    shuffler3 = ImageShuffler("prezentare/lenna.png")
    print("Test original image with scrambled image, should equal False")
    print(ImageShuffler.is_same_image(shuffler, shuffler2))
    print("Test original image with itself, should equal True")
    print(ImageShuffler.is_same_image(shuffler, shuffler3))

def test_same_pixels_for_all():
    shuffler = ImageShuffler("prezentare/lenna.png")
    shuffler.random_shuffle(1)
    print(f"Random Shuffle {shuffler.has_the_same_pixels()}")
    shuffler.fisher_yates_shuffle(1)
    print(f"Fisher-Yates {shuffler.has_the_same_pixels()}")
    shuffler.poisson_charlier_shuffle(1, 0.5, 10)
    print(f"Poisson-Charlier {shuffler.has_the_same_pixels()}")
    shuffler.boriga_dascalescu_shuffle(1)
    print(f"Boriga Dascalescu {shuffler.has_the_same_pixels()}")

def test_video_shuffleing(video_path="prezentare/earth.mp4"):
    video_shuffler = VideoShuffler(video_path)
    video_shuffler.poisson_charlier_shuffle(1)
    video_shuffler.write_scrambled("prezentare/test_cut_scrambled.mp4")

def main():
    # test_all_shufflers()
    # test_is_same_image()
    # test_same_pixels_for_all()
    # test_video_shuffleing("data/test_cut.mp4")
    test_poisson(repeats=1)

if __name__ == "__main__":
    main()
