from os import listdir
from PIL.ImageTk import PhotoImage
from PIL.Image import open as open_image


class Background:
    """
    a class for the map background with layers
    """

    def __init__(self, path: str, layer_speeds: list):
        """
        creates the scene object
        :param path: the path to the directory with background images
        :param layer_speeds: an ordered list of the speed multiplier of each layer where index 0 is furthest back layer
            and index -1 is closest layer, all layer speeds must be positive
        """

        # configures layer speeds
        layer_speeds.sort()
        self.num_still_layers = layer_speeds.count(0)
        self.layer_speeds = layer_speeds[self.num_still_layers:] * 2
        self.layer_speeds.sort()

        # gets and loads images all images from directory
        self.canvas = self.photo_images = self.still_layers = self.layers = None
        images = listdir(path)
        images.sort(reverse=True, key=lambda name: int(name[6:-4]))
        self.images = [open_image(f'{path}/{image}') for image in images]
        self.aspect_ratio = self.images[0].size[0] / self.images[0].size[1]

    def resize(self, height: int):
        """
        resizes the background images when the window is resized
        :param height: the height of the resize event todo maintain scroll amount after resize
        """

        # resizes images and deletes old ones
        new_dimensions = (int(self.aspect_ratio * height * 2), int(height * 2))
        self.images = [self.images[i].resize(new_dimensions) for i in range(len(self.images))]
        self.photo_images = [PhotoImage(image) for image in self.images]

        # places still images
        self.still_layers = []
        for i in range(self.num_still_layers):
            layer = self.canvas.create_image(self.canvas.winfo_width() // 2, 0, image=self.photo_images[i])
            self.still_layers.append(layer)

        # places moving images
        self.layers = []
        for i in range(self.num_still_layers, len(self.photo_images) - 0):
            left_coordinates = (self.canvas.winfo_width() // 2, 0)
            right_coordinates = (self.canvas.bbox(self.still_layers[0])[0], 0)
            left = self.canvas.create_image(*left_coordinates, image=self.photo_images[i])
            right = self.canvas.create_image(*right_coordinates, image=self.photo_images[i], anchor='e')
            self.layers.append(left)
            self.layers.append(right)

    def draw(self, x: float):
        """
        draws the layers to the screen based on the displacement given
        :param x: the displacement of the player
        """

        # ensures program doesn't crash when window hasn't loaded yet
        if self.layers is None:
            self.canvas.after(100, lambda: self.draw(x))
            return

        # loops over every layer to move
        for i in range(len(self.layers)):
            width = (self.canvas.bbox(self.layers[i])[2] - self.canvas.bbox(self.layers[i])[0])
            self.canvas.move(self.layers[i], x * self.layer_speeds[i], 0)

            # shifts the layer left if needed
            while self.canvas.bbox(self.layers[i])[0] > self.canvas.bbox(self.still_layers[0])[2]:
                self.canvas.move(self.layers[i], -2 * width, 0)

            # shifts the layer right if needed
            while self.canvas.bbox(self.still_layers[0])[0] > self.canvas.bbox(self.layers[i])[2]:
                self.canvas.move(self.layers[i], 2 * width, 0)
