from tkinter import Canvas, Tk
from time import time


class Scene(Canvas):
    """
    a class for a scene that controls the following objects
        --> the background
        --> the player
        --> the other characters
    """

    def __init__(self, background, player, characters: list = None):
        """
        creates scene object
        :param background: the background to use
        :param player: the characters object representing the player
        :param characters: other character objects
        """

        # calls and configures super class
        super().__init__()
        self.master.geometry(f'{int(background.images[0].size[0] * 1.5)}x{int(background.images[0].size[1] * .75)}')
        self.draw_after = self.resize_after = self.after(0, lambda: None)

        # sets fields
        self.background = background
        self.player = player
        self.characters = characters if characters else []
        self.bounds = [player.position[0] - 10, player.position[0] + 90]

        # configures fields
        self.background.canvas = self
        self.player.canvas = self
        for character in [self.player] + self.characters:
            for animation in character.animations.values():
                animation.canvas = self

    def start(self):
        """
        shows the scene and starts the update loop
        """

        self.bind("<Configure>", lambda event: self.resize(event))
        self.pack(fill='both', expand=True)
        self.draw_after = self.after(0, self.draw)

    def stop(self):
        """
        stops the update loop and hides the scene
        """

        self.after_cancel(self.draw_after)
        self.unbind("<Configure>")
        self.pack_forget()

    def resize(self, event, ignore: bool = True):
        """
        resizes the every element in the scene
        :param event: the resize event
        :param ignore: determines if the resize event should be ignored, default is true
            helps to prevent lag when using is resizing and method is called repeatedly todo center
        """

        # prevents lag by ensuring 300 ms have passed since last resize
        self.after_cancel(self.resize_after)
        self.resize_after = self.after(300, lambda: self.resize(event, False))

        # resizes the images when the user has stopped resizing
        if not ignore:
            self.after_cancel(self.resize_after)
            self.delete('all')

            # gets the height to resize to
            height = event.height
            if event.width / event.height < self.background.aspect_ratio * 2:
                height = event.width / (self.background.aspect_ratio * 2)

            # resizes every element
            self.background.resize(height)
            for character in [self.player] + self.characters:
                character.resize(height)

            # draws bounding rectangles
            rect_one_coordinates = (0, 0, self.bbox(self.background.still_layers[0])[0], height)
            rect_two_coordinates = (self.bbox(self.background.still_layers[0])[2], 0, self.winfo_width(), height)
            self.create_rectangle(*rect_one_coordinates, fill='black')
            self.create_rectangle(*rect_two_coordinates, fill='black')

    def convert_coordinates(self, x: float, y: float):
        """
        converts in game coordinates to canvas coordinates for drawing items to the screen
        :param x: the x coordinate of the object in the game
        :param y: the y coordinate of the object in the game
        :return: the converted x, y coordinate as a tuple in the form (x, y) todo improve
        """

        bbox = self.bbox(self.background.still_layers[0])
        width_ratio = (bbox[2] - bbox[0]) // 100
        height_ratio = (bbox[3] - bbox[1]) // 1000
        return bbox[2] - ((self.bounds[1] - x) * width_ratio), bbox[3] - ((y - 25) * height_ratio)

    def draw(self):
        """
        updates the game
        """

        # prevents crash if game has not finished loading
        last_updated_animation = list(([self.player] + self.characters)[-1].animations.values())[-1]
        if not last_updated_animation.mirrored_layers:
            self.after(100, self.draw)
            return

        # updates the player position and scene bounds
        self.player.move()
        initial_bound_l = self.bounds[0]
        if self.player.position[0] > self.bounds[1] - 10:
            self.bounds = [self.player.position[0] - 90, self.player.position[0] + 10]
        elif self.player.position[0] < self.bounds[0] + 10:
            self.bounds = [self.player.position[0] - 10, self.player.position[0] + 90]

        # updates characters and background
        bbox = self.bbox(self.background.still_layers[0])
        self.background.draw((initial_bound_l - self.bounds[0]) * (bbox[2] - bbox[0]) // 100)
        [character.draw() for character in [self.player] + self.characters]
        self.draw_after = self.after(17, self.draw)
