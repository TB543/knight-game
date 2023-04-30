from os import listdir
from graphics.Animation import Animation


class Character:
    """
    class representing a game character and all of its animations based on the characters current action
    """

    def __init__(self, path: str, resize_ratio: float, position: tuple, health: float, damage: dict, stamina: dict):
        """
        creates the character object
        :param path: the path to the character files
        :param resize_ratio: the ratio to use when resizing the characters image
        :param position: the position of the player on the map
        :param health: the health of the character
        :param damage: the damage the character does for each attack in the form {'attack type': damage}
            example: {'light': 5, 'heavy': 10, 'special': 15}
        :param stamina: the stamina for the player and each attach in the form {'total': total, 'attack type': drain}
            example: {'total': 100, 'light': 5, 'heavy': 10, 'special': 15}
        """

        # sets fields for graphics
        self.resize_ratio = resize_ratio
        self.attack_level = 0
        self.mirror = False
        self.frames_since_animation = 0

        # sets fields for movement and stats
        self.position = list(position)
        self.velocity = [False, False, 0, 0, False, False]  # l, r, x, y, up, down
        self.prev_health = self.health = health  # todo with damage and stam
        self.damage = damage
        self.stamina = stamina

        # loads animations
        self.animations = {}
        for animation in listdir(path):
            self.animations[animation] = Animation(f'{path}/{animation}')
        self.current_animation = self.animations['idle']
        self.blocking_animation = False

    def resize(self, height: int):
        """
        resizes the character based on the given height
        :param height: the new height of the scene
        """

        for animation in self.animations.values():
            animation.resize(height * self.resize_ratio)

    def move(self):
        """
        updates the position velocity and mirror of the character
        """

        # handles mirror
        self.mirror = True if self.velocity[2] < 0 else self.mirror
        self.mirror = False if self.velocity[2] > 0 else self.mirror

        # handles position
        self.position[0] += self.velocity[2]  # left right movement
        self.position[1] += self.velocity[3]  # up down movement
        self.position[1] = 0 if self.position[1] < 0 else self.position[1]  # hit ground

        # handles velocity when on ground
        if self.position[1] == 0:

            # x velocity
            self.velocity[2] = 0 if self.velocity[0] and self.velocity[1] else self.velocity[2]  # l and r
            self.velocity[2] = 0 if not self.velocity[0] and not self.velocity[1] else self.velocity[2]  # still
            self.velocity[2] = -1.25 if self.velocity[0] and not self.velocity[1] else self.velocity[2]  # l
            self.velocity[2] = 1.25 if not self.velocity[0] and self.velocity[1] else self.velocity[2]  # r

            # y velocity
            self.velocity[3] += 50 if self.velocity[4] else 0  # jumping
            self.velocity[3] = 0 if self.velocity[3] < 0 else self.velocity[3]  # hit ground

        # handles y velocity when in air
        elif self.position[1] > 0:
            self.velocity[3] -= 10 if self.velocity[4] and self.velocity[5] else 0  # normal fall
            self.velocity[3] -= 10 if not self.velocity[4] and not self.velocity[5] else 0
            self.velocity[3] -= 5 if self.velocity[4] and not self.velocity[5] else 0  # slow fall
            self.velocity[3] -= 15 if not self.velocity[4] and self.velocity[5] else 0  # fast fall

    def key_binds(self, x: str = 'ignore', y: str = 'ignore', attack_level: int = 0):
        """
        function for updating player velocity with key-binds

        how to bind keys:

        self.canvas.master.bind("<KeyRelease-space>", lambda event: self.key_binds(y='up off'))
        self.canvas.master.bind("<KeyPress-space>", lambda event: self.key_binds(y='up on'))
        self.canvas.master.bind("<KeyRelease-w>", lambda event: self.key_binds(y='up off'))
        self.canvas.master.bind("<KeyPress-w>", lambda event: self.key_binds(y='up on'))
        self.canvas.master.bind("<KeyPress-s>", lambda event: self.key_binds(y='down on'))
        self.canvas.master.bind("<KeyRelease-s>", lambda event: self.key_binds(y='down off'))
        self.canvas.master.bind("<KeyPress-a>", lambda event: self.key_binds(x='left on'))
        self.canvas.master.bind("<KeyRelease-a>", lambda event: self.key_binds(x='left off'))
        self.canvas.master.bind("<KeyPress-d>", lambda event: self.key_binds(x='right on'))
        self.canvas.master.bind("<KeyRelease-d>", lambda event: self.key_binds(x='right off'))
        self.canvas.master.bind("<Button-1>", lambda event: self.key_binds(attack_level=1))
        self.canvas.master.bind("<Button-3>", lambda event: self.key_binds(attack_level=2))
        self.canvas.master.bind("<Button-2>", lambda event: self.key_binds(attack_level=3))

        :param x: how to change x velocity, options are, ignore, left, right, reset
        :param y: how to change y velocity, options are ignore, up on, up off, down on, down off
        :param attack_level: the attack to use, 1 for light, 2 for heavy, 3 for special, and 0 to ignore
        """

        # handles x movement
        if x == 'right on':
            self.velocity[1] = True
        elif x == 'right off':
            self.velocity[1] = False
        elif x == 'left on':
            self.velocity[0] = True
        elif x == 'left off':
            self.velocity[0] = False

        # handles y movement
        if y == 'up on':
            self.velocity[4] = True
        elif y == 'up off':
            self.velocity[4] = False
        elif y == 'down on':
            self.velocity[5] = True
        elif y == 'down off':
            self.velocity[5] = False

        # handles attack
        self.attack_level = attack_level if self.attack_level == 0 else self.attack_level

    def draw(self):
        """
        draws the players correct animation to the screen todo handle animations other characters do/dont have and hit/attack functions
        """

        # handles when animation is not blocking
        animation = self.current_animation
        if not self.blocking_animation:

            # handles run and idle animations
            animation = self.animations['idle'] if self.velocity[2] == 0 else self.animations['run']

            # handles mid air animations
            if self.position[1] > 0:
                animation = self.animations['jump'] if self.velocity[3] >= 0 else self.animations['fall']

            # handles attack animations
            if self.attack_level > 0:
                animation = self.animations['light'] if self.attack_level == 1 else animation
                animation = self.animations['heavy'] if self.attack_level == 2 else animation
                animation = self.animations['heavy'] if self.attack_level == 3 else animation
                self.attack_level = 0
                self.blocking_animation = True

            # handles hit animation
            if self.health < self.prev_health:
                animation = self.animations['hit']
                self.prev_health = self.health
                self.blocking_animation = True

            # handles death animation
            if self.health == 0:
                animation = self.animations['death']
                raise NotImplementedError()  # todo death menu

            # resets previous animation if needed
            if animation != self.current_animation:
                self.current_animation.reset()
                self.current_animation = animation

        # runs animation
        result = animation.draw(self.position[0], self.position[1], self.mirror, self.frames_since_animation != 3)
        self.blocking_animation = not result if self.blocking_animation else self.blocking_animation

        # advances frame counter
        self.frames_since_animation += 1
        if self.frames_since_animation == 4:
            self.frames_since_animation = 0
