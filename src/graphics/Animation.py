from os import listdir
from PIL.ImageTk import PhotoImage
from PIL.Image import open as open_image
from PIL.ImageOps import mirror


class Animation:
    """
    a class to represent a frame that will display an animation from a list of images
    """

    def __init__(self, animation_path: str):
        """
        creates the animation frame
        :param animation_path: a file path to the folder containing the animation images
        """

        # gets all images from directory
        images = listdir(animation_path)
        images.sort(key=lambda name: int(name[:-4]))
        self.images = [open_image(f'{animation_path}/{image}') for image in images]

        # sets fields
        self.mirrored_images = self.photo_images = self.mirrored_photo_images = None
        self.mirrored_layers = self.canvas = self.layers = self.half_width = None
        self.aspect_ratio = self.images[0].size[0] / self.images[0].size[1]
        self.frame_index = self.previous_frame = -1
        self.previous_frame_coordinates = (0, 0)

    def resize(self, height: int):
        """
        resizes the background images when the window is resized
        ** note: all images will be places outside of view after resizing **
        :param height: the height of the resize event
        """

        # resizes images
        new_dimensions = (int(self.aspect_ratio * height * 2), int(height * 2))
        self.images = [self.images[i].resize(new_dimensions) for i in range(len(self.images))]
        self.mirrored_images = [mirror(image) for image in self.images]
        self.photo_images = [PhotoImage(image) for image in self.images]
        self.mirrored_photo_images = [PhotoImage(image) for image in self.mirrored_images]

        # places images to canvas
        self.layers = []
        self.mirrored_layers = []
        for i in range(len(self.photo_images)):
            self.layers.append(self.canvas.create_image(0, 0, image=self.photo_images[i], anchor='se'))
            mirrored_layer = self.canvas.create_image(0, 0, image=self.mirrored_photo_images[i], anchor='se')
            self.mirrored_layers.append(mirrored_layer)
        self.half_width = (self.canvas.bbox(self.layers[0])[2] - self.canvas.bbox(self.layers[0])[0]) // 2.5

    def draw(self, x: int, y: int, mirrored: bool = False, skip: bool = False):
        """
        places the next animation frame to the given location and hides previous frame
        :param x: the x coordinate to place the image to
        :param y: the y coordinate to place the image to
        :param mirrored: determines if the image should be mirrored
        :param skip: if true, animation will move but will not be advanced a frame
        :return true if the animation has reached last frame, false if it has not,
            note: the animation will loop if called again after last frame has been reached
        """

        # converts coordinates
        x, y = self.canvas.convert_coordinates(x, y)
        x += self.half_width

        # hides previous frame
        self.canvas.move(self.previous_frame, *self.previous_frame_coordinates)
        self.previous_frame_coordinates = (-x, -y)
        if not skip:
            self.frame_index += 1 if self.frame_index < len(self.layers) - 1 else 1 - len(self.layers)

        # shows next frame
        frame = self.mirrored_layers[self.frame_index] if mirrored else self.layers[self.frame_index]
        self.canvas.move(frame, x, y)
        self.previous_frame = frame
        return self.frame_index == len(self.layers) - 1

    def reset(self):
        """
        resets the animation to its starting frame and hides the animation until draw is called
        """

        self.canvas.move(self.previous_frame, *self.previous_frame_coordinates)
        self.frame_index = self.previous_frame = -1
        self.previous_frame_coordinates = (0, 0)
