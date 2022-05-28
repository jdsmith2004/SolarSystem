import tkinter as tk
from tkinter import simpledialog
import math
import arcade

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
        self.dx = 0
        self.dy = 0

class Ship:
    """
    This class describes all the characteristics and capabilities of the ship.
    """
    def __init__(self):
        """
        Basic stat initialization
        """
        self.img = "" # -> the path to the image
        self.ship_dist = EARTH_DIST # -> distance between Sun and ship
        self.center = Point() # -> coordinates of the center
        self.center.x = 350 # -> x-coordinate changed
        self.center.y = 250 # -> y-coordinate changed
        self.velocity = Velocity() # -> values for changing coordinates
    
    def advance(self):
        """
        Change of position. By this method an object will move through the update() method in the Game class. Next it will be redraw.
        By default, the object does not move.
        """
        self.center.x += self.velocity.dx # -> change the x-center position
        self.center.y += self.velocity.dy # -> change the y-center position

    def draw(self):
        """
        Draw an object.
        It should be an image.
        For test it will be a rectangle.
        """
        arcade.draw_rectangle_filled(self.center.x, self.center.y
                                    ,60, 20
                                    ,arcade.color.DARK_RED, 0)

class Planet:
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
        self.img = "" # -> the path to the image
        self.center = Point() # -> coordinates of the center
        self.center.x = distX # -> x-coordinate changed according to the planet distance
        self.center.y = 200 # -> y-coordinate changed to the default
        self.radius = radius # -> radius of the planet

    def draw(self):
        """
        Draw an object.
        It should be images.
        For test it will be circles.
        """
        arcade.draw_circle_filled(self.center.x, self.center.y
                                 ,self.radius, arcade.color.CARROT_ORANGE)

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
                                    ,arcade.color.BEIGE, 0)
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
        self.planets = [ # -> planets created
            Planet("Sun", 0, 0, 100),
            Planet("Mercury", MERCURY_DIST, 150, 8),
            Planet("Venus", VENUS_DIST, 250, 15),
            Planet("Earth", EARTH_DIST, 350, 20),
            Planet("Mars", MARS_DIST, 450, 10),
            Planet("Jupiter", JUPITER_DIST, 550, 40),
            Planet("Saturn", SATURN_DIST, 650, 35),
            Planet("Uranus", URANUS_DIST, 750, 30),
            Planet("Neptune", NEPTUNE_DIST, 850, 25),
            Planet("Pluto", PLUTO_DIST, 950, 8)
        ]
        self.info = Info(self.ship.ship_dist, self.planets) # -> info part created

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


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()