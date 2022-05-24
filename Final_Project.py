import tkinter as tk
from tkinter import simpledialog
import math
import arcade

# Measurements are in km
# conversion km to miles (1/1.60934)
# conversion AU(astronomical units) to Km 1AU=150,000,000km

SOLAR_SYSTEM = 178619362920.544
# Distance form Sun
MERCURY_DIST = 57900000
VENUS_DIST = 108200000
#EARTH_DIST =  149600000
MARS_DIST = 227900000
JUPITER_DIST = 778600000
SATURN_DIST = 1433500000
URANUS_DIST = 2872500000
NEPTUNE_DIST = 4495100000

# PLANET_LIST = {'MERCURY':57900000,
# 'VENUS':108200000,
# 'EARTH':149600000,
# 'MARS':227900000,
# 'JUPITER':778600000,
# 'SATURN':1433500000,
# 'URANUS':2872500000,
# 'NEPTUNE':4495100000,
# }
# radius of planets
SUN_RADIUS = 432690
MERCURY_RADIUS = 2439.5
VENUS_RADIUS = 6054
EARTH_RADIUS = 6378
MARS_RADIUS = 3396
JUPITER_RADIUS = 71492
SATURN_RADIUS = 60268
URANUS_RADIUS = 25559
NEPTUNE_RADIUS = 24764


class Conv_Units():
    def __init__(self):
        self.decision = ''

    def km(self):
        dist = {'MERCURY': 57900000,
                'VENUS': 108200000,
                'EARTH': 149600000,
                'MARS': 227900000,
                'JUPITER': 778600000,
                'SATURN': 1433500000,
                'URANUS': 2872500000,
                'NEPTUNE': 4495100000,
                }

        return dist

    def miles(self, c):
        miles = c * 1.60934
        return miles

    def AU(self, c):
        AU = c * 150000000
        return AU


class Ship(Conv_Units):
    def __init__(self):
        super().__init__()
        self.u = Conv_Units()
        dict = self.km()
        self.ship_initial = dict['EARTH']

    def move(self):
        # if self.fuel <= 0:
        #     print("Insufficient fuel to perform action")

        while True:
            command = input(
                'Would you like to move in or out of the solar system?: ')

            if command.lower() == 'in' or command.lower() == 'out':
                break
            else:
                print('Invalid input. Please try again.')

        while True:
            move_amount = input("How far would you like to move: ")

            if not move_amount.isdigit():
                print('Invalid input. Please try again.')
            else:
                break

        if command == 'in':
            self.ship_initial -= int(move_amount)
        elif command == "out":
            self.ship_initial += int(move_amount)

    def current_position(self):
        print(f"Distance from Sun: {self.ship_initial}km ")

    def get_distance(self):
        list = []
        PLANET_LIST = self.u.km()
        for planet in PLANET_LIST.items():
            key = planet[0]
            planet = planet[1]
            if self.ship_initial >= planet:
                dist_from_planet = self.ship_initial - planet
            elif self.ship_initial <= planet:
                dist_from_planet = planet - self.ship_initial
            list.append(f"{key} : {dist_from_planet} km")
        # print(list)
        return list

# class Planet_Dist(Ship):
#     def __init__(self):
#         super().__init__()
#         self.planet_distance = 0
#         self.ship_location = self.ship_initial

#     def get_distance(self):
#         PLANET_LIST = self.u.km('list')
#         for planet in PLANET_LIST.items():
#             key = planet[0]
#             planet = planet[1]
#             if self.ship_location >= planet:
#                 dist_from_planet = self.ship_location - planet
#             elif self.ship_location <= planet:
#                 dist_from_planet = planet - self.ship_location
#             print(f"{key} : {dist_from_planet} km")


def main():
    # p = Planet_Dist()
    p = Ship()

    print('*All measurments are shown as approximates*')
    print('*Original planets distances are from Nasa*')
    print()
    p.move()
    p.current_position()
    print()
    dist = p.get_distance()
    for i in dist:
        print(i)


if __name__ == "__main__":
    main()
