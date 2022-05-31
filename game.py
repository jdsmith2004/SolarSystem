import tkinter as tk
from tkinter import Scale, simpledialog
import math
import arcade
from abc import ABC, abstractmethod
import os

relpath = lambda p: os.path.normpath(os.path.join(os.path.dirname(__file__), p))

# Global constants to use throughout the game
# Screen parameters
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

SOLAR_SYSTEM = 178619362920.544
# Distance form Sun (km)
MERCURY_DIST = 57900000
VENUS_DIST = 108200000
EARTH_DIST =  149600000
MARS_DIST = 227900000
JUPITER_DIST = 778600000
SATURN_DIST = 1433500000
URANUS_DIST = 2872500000
NEPTUNE_DIST = 4495100000
PLUTO_DIST = 5884500000

# Radius of planets (km)
SUN_RADIUS = 432690
MERCURY_RADIUS = 2439.5
VENUS_RADIUS = 6054
EARTH_RADIUS = 6378
MARS_RADIUS = 3396
JUPITER_RADIUS = 71492
SATURN_RADIUS = 60268
URANUS_RADIUS = 25559
NEPTUNE_RADIUS = 24764

SCALE = 0.003
SHIP_THRUST = 3

class Point:
    """
    This class is a coordinates of a central point of objects
    """
    def __init__(self):
        """
        Basic stat initialization.
        By default, the object is located at a point with coordinates 0,0
        """
        self.x = 0
        self.y = 0

class Velocity:
    """
    This class tells how the coordinates will change while moving.
    (It is necessary for moving elements. For example: a ship)
    """
    def __init__(self):
        """
        Basic stat initialization.
        By default, the coordinates do not change, so the coefficients are specified as 0.
        """
        self.dx = 1
        self.dy = 0

class FlyingObjects(ABC):
    def __init__(self, obj, scale):
        """ Abstract class with attributes for flying objects
            Here we use an abstractmethod to say that
            every child object need the method or set of methods
            that we created here
        """
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.path = relpath(obj)
        self.texture = arcade.load_texture(self.path)
        self.width = self.texture.width*SCALE*scale
        self.height = self.texture.height*SCALE*scale
        self.angle = 0
        self.radius = 0
        # self.direction = 0
        # self.speed = 0

    def advance(self):
        """ a base method for movement"""
        # self.wrap()
        self.bounds()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

# THIS IS A TEST METHOD, NOT sure how would work for the rest of objects
    def bounds(self):
        """Method to limit the movement of the ship"""
        # This part needs some adjustments
        if  self.center.x > SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH           
        elif self.center.y > SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT
        elif self.center.x < 0:
            self.center.x += SCREEN_WIDTH
        elif self.center.y < 0:
            self.center.y += SCREEN_HEIGHT

    # def wrap(self):
    #     """ a base method for deleting flying objects when they leave the screen"""
    #     if  self.center.x > SCREEN_WIDTH:
    #         self.center.x -= SCREEN_WIDTH           
    #     elif self.center.y > SCREEN_HEIGHT:
    #         self.center.y -= SCREEN_HEIGHT
    #     elif self.center.x < 0:
    #         self.center.x += SCREEN_WIDTH
    #     elif self.center.y < 0:
    #         self.center.y += SCREEN_HEIGHT

    """This abstract method will help to create every
     texture or image needed in the project"""
    @abstractmethod
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x,self.center.y, self.width, self.height, self.texture, self.angle, 255)


class Ship(FlyingObjects):
    """
    This class describes all the characteristics and capabilities of the ship.
    """
    def __init__(self):
        """
        Basic stat initialization
        """
        super().__init__("images/ship_1.png",25)
        # self.img = "" # -> the path to the image
        self.ship_dist = EARTH_DIST # -> distance between Sun and ship
        self.center = Point() # -> coordinates of the center
        self.center.x = 350 # -> x-coordinate changed
        self.center.y = 350 # -> y-coordinate changed
        self.velocity = Velocity() # -> values for changing coordinates
        self.velocity.dx = SHIP_THRUST/2
    
    def move_left(self):
        if (self.velocity.dx >0):
            self.velocity.dx *=-1
        super().advance()
        # self.angle += self.velocity.dx
        # self.center.x -= self.velocity.dx
    
    def move_right(self):
        if (self.velocity.dx<0):
            self.velocity.dx *=-1 
        super().advance()
        # self.angle -= self.velocity.dx
        # self.center.x += self.velocity.dx

    def draw(self): 
        """ Call the abstract method"""
        # arcade.draw_texture_rectangle(self.center.x,self.center.y, self.width, self.height, self.texture, self.angle, 255)
        super().draw()

# This could be a planet base class
class Planet(FlyingObjects):
    """
    The class describes the main characteristics of the planet and draws it.
    """
    def __init__(self, name, p_dist, distX, radius):
        """
        Basic stat initialization.
        It uses:
        name - can be used for img path and for info part on the screen
        p_dist - planet distance from the Sun. Will be used fof info part
        distX - position on the screen. Can be related to the actual distance from the Sun. Now it is form the head.
        radius - planet radius. Can be related to the real numbers. Now it is form the head.
        """
        self.name = name # -> planet name (can be used for img name)
        self.p_dist = p_dist # -> planet distance from the Sun
        self.radius = radius # -> radius of the planet to help with scaling
        self.img = f"images/{self.name}.png" # -> the path to the image
        super().__init__(self.img,self.radius)
        self.center = Point() # -> coordinates of the center
        self.center.x = distX # -> x-coordinate changed according to the planet distance
        self.center.y = 200 # -> y-coordinate changed to the default


    def draw(self):
        """
        Draw an object.
        It should be images.
        For test it will be circles.
        """
        super().draw()
        # arcade.draw_circle_filled(self.center.x, self.center.y
        #                          ,self.radius, arcade.color.CARROT_ORANGE)

class Info():
    """
    Class for the list of distances between planets and ship
    """
    def __init__(self, ship_dist, planets):
        """
        Create a dictionary with text and y-position on the screen for each line (planet)
        """
        self.dist_text = {
            'line': [],
            'start_y': []
        }
        start_y = SCREEN_HEIGHT - 20 # -> start value for y-position for first line
        for planet in planets:
            self.dist_text['line'].append(planet.name+": "+str(abs(ship_dist - planet.p_dist))) # -> text for a line (Ex.: Mars: 78300000)
            self.dist_text['start_y'].append(start_y) # -> y-position for line
            start_y -= 20 # -> change y-position for next line
        self.start_x = 10 # -> x-position the same for all lines

    def draw(self):
        """
        Puts the current distances on the screen.
        Draw line by line on the light background.
        """
        # Backgroud for info part
        arcade.draw_rectangle_filled(100, SCREEN_HEIGHT-110
                                    ,200, 220
                                    ,arcade.color.BEIGE, 0,)
        # Text
        for i in range(len(self.dist_text['line'])):
            arcade.draw_text(self.dist_text['line'][i], 
                            start_x=self.start_x, start_y=self.dist_text['start_y'][i], 
                            font_size=12, color=arcade.color.NAVY_BLUE)
            


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    """
    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        # Create each object
        self.ship = Ship() # -> ship created
        # Remember: Planet(name, p_dist, distX, radius)
        # p_dist - planet distance from the Sun. Will be used fof info part
        # distX - position on the screen. Can be related to the actual distance from the Sun.
        # radius - planet radius. Can be related to the real numbers.
        self.planets = [ # -> planets created
            Planet("Sun", 0, 25, 100),
            Planet("Mercury", MERCURY_DIST, 150, 15),
            Planet("Venus", VENUS_DIST, 200, 12),
            Planet("Earth", EARTH_DIST, 300, 20),
            Planet("Mars", MARS_DIST, 400, 14),
            Planet("Jupiter", JUPITER_DIST, 540, 40),
            Planet("Saturn", SATURN_DIST, 710, 35),
            Planet("Uranus", URANUS_DIST, 850, 25),
            Planet("Neptune", NEPTUNE_DIST, 950, 20),
            # Planet("Pluto", PLUTO_DIST, 950, 8)
        ]
        self.info = Info(self.ship.ship_dist, self.planets) # -> info part created

        # Variable for movement of the ship
        self.held_keys = set()

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # Clear the screen to begin drawing
        arcade.start_render()

        # Draw each object
        self.ship.draw() # -> the ship is drawn
        for planet in self.planets:
            planet.draw() # -> each planet is drawn

        self.info.draw() # -> draw the list with distances

    def update (self, delta):
        """Logic for movement and other future features"""
        self.check_keys()

        self.ship.advance()

    def check_keys(self):
        """This function checks for keys that are being held down."""
        if arcade.key.LEFT in self.held_keys:
            self.ship.move_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.move_right()
    def on_key_press(self, key: int, modifiers: int):
        self.held_keys.add(key)
    
    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()