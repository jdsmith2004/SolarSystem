import math
import arcade
import os

relpath = lambda p: os.path.normpath(os.path.join(os.path.dirname(__file__), p))

# Global constants to use throughout the game
# Screen parameters
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 650
# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200
# How fast the camera pans to the player. 1.0 is instant.
CAMERA_SPEED = 0.1

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

SOLAR_SYSTEM = 178619362920.544
SCALE_PLANET = 0.003
SCALE_SYSTEM = 0.00000001


#Sun to Mercury size(Sun radius) to distance(kil) ratio
SUN_MERCURY_RATIO = SUN_RADIUS / 67368000

# Distance Ratios to Earth

# Size Ratios to Sun(Kilometers)
SUN_SIZE = 600
MERCURY_SIZE = 1 / 277 * SUN_SIZE
VENUS_SIZE = 1 / 113 * SUN_SIZE
EARTH_SIZE = 1 / 108 * SUN_SIZE
MARS_SIZE = 1 / 208 * SUN_SIZE
JUPITER_SIZE = 1 / 9.7 * SUN_SIZE
SATURN_SIZE = 1 / 11.4 * SUN_SIZE
URANUS_SIZE = 1 / 26.8 * SUN_SIZE
NEPTUNE_SIZE = 1 / 27.7 * SUN_SIZE
PLUTO_SIZE = 1 / 585 * SUN_SIZE

MERCURY_D = SUN_SIZE / SUN_MERCURY_RATIO




SCREEN_TITLE = "Solar System 1.2"
SHIP_TURN_AMOUNT = 3
SHIP_SPEED = 3

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
        self.img = relpath("images/ship_1.png")
        self.texture = arcade.load_texture(self.img) # -> the path to the image
        self.width = self.texture.width*0.10
        self.height = self.texture.height*0.10
        self.ship_dist = EARTH_DIST # -> distance between Sun and ship
        self.center = Point() # -> coordinates of the center
        self.center.x = 250 # -> x-coordinate changed
        self.center.y = 250 # -> y-coordinate changed
        self.velocity = Velocity() # -> values for changing coordinates
        self.angle = 0
    
    def advance(self):
        """ a base method for movement"""
        # self.bounds() this would help to limit the movement of the ship
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def draw(self): 
        arcade.draw_texture_rectangle(self.center.x,self.center.y, 
                                    self.width, self.height, 
                                    self.texture, self.angle, 255)
    
    def rotate(self, key):
        if key == 'l':
            self.angle += SHIP_TURN_AMOUNT
        if key == 'r':
            self.angle -= SHIP_TURN_AMOUNT
    def move(self, key):
        if key == 'u':
            self.velocity.dx = (-SHIP_SPEED)*math.sin(math.radians(self.angle))# * SHIP_SPEED
            self.velocity.dy = (SHIP_SPEED)*math.cos(math.radians(self.angle))# * SHIP_SPEED
        if key == 'd':
            self.velocity.dx = 0
            self.velocity.dy = 0


# This could be a planet base class
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
        self.radius = radius # -> radius of the planet to help with scaling
        self.img = f"images/{self.name}.png" # -> the path to the image
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width*SCALE_PLANET*radius
        self.height = self.texture.height*SCALE_PLANET*radius
        self.center = Point() # -> coordinates of the center
        self.center.x = distX # -> x-coordinate changed according to the planet distance
        self.center.y = 200 # -> y-coordinate changed to the default

    def draw(self):
        arcade.draw_texture_rectangle(self.center.x,self.center.y, self.width, self.height, self.texture, 0, 255)

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
    def __init__(self, width, height, title):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        
        #self.background = arcade.load_texture(r"C:\Users\Joseph Raymant\Documents\School\2022 Spring\Applied Programming(CSE 310)\Team\SolarSystem\SimpleSpace.jpg")
        
        self.held_keys = set()
        # Create each object
        self.ship = Ship()
        
        self.planets = [ # -> planets created
            Planet("Sun", 0, -500, SUN_SIZE),
            Planet("Mercury", MERCURY_DIST, 150, MERCURY_SIZE),
            Planet("Venus", VENUS_DIST, 250, VENUS_SIZE),
            Planet("Earth", EARTH_DIST, 350, EARTH_SIZE),
            Planet("Mars", MARS_DIST, 450, MARS_SIZE),
            Planet("Jupiter", JUPITER_DIST, 620, JUPITER_SIZE),
            Planet("Saturn", SATURN_DIST, 800, SATURN_SIZE),
            Planet("Uranus", URANUS_DIST, 925, URANUS_SIZE),
            Planet("Neptune", NEPTUNE_DIST, 1050, NEPTUNE_SIZE),
            #Planet("Pluto", PLUTO_DIST, 1150, PLUTO_SIZE)
        ]

        # Used in scrolling
        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_bottom = 0
        self.view_left = 0

        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.info = Info(EARTH_DIST, self.planets) # -> info part created

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # Clear the screen to begin drawing
        arcade.start_render()
        
#         arcade.draw_texture_rectangle(590, 350,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
        
        # Select the camera we'll use to draw all our sprites
        self.camera_sprites.use()

        # Draw each object
        for planet in self.planets:
            planet.draw() # -> each planet is drawn
        
        # self.player_list.draw() # -> the ship is drawn
        self.ship.draw()
        # Display speed
        # ----------------------------HERE we need relative values for position
        arcade.draw_text(f"X position: {self.ship.center.x:6.3f}", 10, 20, arcade.color.WHITE)
        arcade.draw_text(f"Y position: {self.ship.center.y:6.3f}", 10, 40, arcade.color.WHITE)
        arcade.draw_text(f"X vel: {self.ship.velocity.dx:6.3f}", 10, 60, arcade.color.WHITE)
        arcade.draw_text(f"Y vel: {self.ship.velocity.dy:6.3f}", 10, 80, arcade.color.WHITE)

        self.info.draw() # -> draw the list with distances

        # Select the (unscrolled) camera for our GUI
        self.camera_gui.use()
        
        # Draw the GUI
        arcade.draw_rectangle_filled(self.width // 2, 20, self.width, 40, arcade.color.ALMOND)
        text = f"Scroll value: ({self.camera_sprites.position[0]:5.1f}, {self.camera_sprites.position[1]:5.1f})"
        arcade.draw_text(text, 10, 10, arcade.color.BLACK_BEAN, 20)

        # Draw the box that we work to make sure the user stays inside of.
        # This is just for illustration purposes. We'd want to remove this
        # in our game.
        left_boundary = VIEWPORT_MARGIN
        right_boundary = self.width - VIEWPORT_MARGIN
        top_boundary = self.height - VIEWPORT_MARGIN
        bottom_boundary = VIEWPORT_MARGIN
        arcade.draw_lrtb_rectangle_outline(left_boundary, right_boundary, top_boundary, bottom_boundary,
                                           arcade.color.RED, 2)
    
    def check_collision(self):
        # this would help to check if we get in to a planet
        pass

    def check_keys(self):
        """This function checks for keys that are being held down."""
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate('l')

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate('r')

        if arcade.key.UP in self.held_keys:
            self.ship.move('u')

        if arcade.key.DOWN in self.held_keys:
            self.ship.move('d')

        if arcade.key.SPACE in self.held_keys:
            # this key would help to display a planet info
            # or something like that
            pass

    def on_key_press(self, key: int, modifiers: int):
        self.held_keys.add(key)
      
    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
    
    def on_update (self, delta):
        """Logic for movement and other future features"""
        self.check_keys()
        self.ship.advance()
        self.check_collision()
        self.scroll_to_player()
    
    def scroll_to_player(self):
        """
        Scroll the window to the player.
        This method will attempt to keep the player at least VIEWPORT_MARGIN
        pixels away from the edge.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.ship.center.x < left_boundary:
            self.view_left -= left_boundary - self.ship.center.x

        # Scroll right
        right_boundary = self.view_left + self.width - VIEWPORT_MARGIN
        if self.ship.center.x > right_boundary:
            self.view_left += self.ship.center.x - right_boundary

        # Scroll up
        top_boundary = self.view_bottom + self.height - VIEWPORT_MARGIN
        if self.ship.center.y > top_boundary:
            self.view_bottom += self.ship.center.y - top_boundary

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.ship.center.y < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.ship.center.y

        # Scroll to the proper location
        position = self.view_left, self.view_bottom
        self.camera_sprites.move_to(position, CAMERA_SPEED)
    
    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))

window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
arcade.run()