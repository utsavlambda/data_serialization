#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Processing GPS tracking log files"""

__author__ = "talatiuh"

import math
import csv


def distance(p1, p2):
    """
    Calculate the distance in miles on a sphere from longitudes and latitudes.

    Based on the haversine formula:
    https://en.wikipedia.org/wiki/Haversine_formula

    Arguments:
        p1, p2: (latitude, longitude) tuples of the two points

    Latitude and longitude coordinates are represented as decimal numbers.
    The latitude is preceded by a minus sign (–) if it is south of the equator
    (a positive number implies north), and the longitude is preceded by a
    minus sign if it is west of the prime meridian (a positive number implies
    east).

    E.g. from p1 = (36.144698, -86.803177) and p2 = (36.144871, -86.793150)
    the calculated distance should be approximately 0.56 miles.
    """
    radians = math.pi/180.0

    c1 = (90.0 - p1[0])*radians
    long1 = p1[1] * radians
    c2 = (90.0 - p2[0])*radians
    long2 = p2[1] * radians

    differance = long1 - long2

    cos_orig1 = math.cos(c1)
    cos_orig2 = math.cos(c2)
    sin_orig1 = math.sin(c1)
    sin_orig2 = math.sin(c2)

    cos = (sin_orig1 * sin_orig2 * math.cos(differance) +
           cos_orig1 * cos_orig2)

    arCos = math.acos(cos)

    return arCos * 3960


def main(filename):
    """
    Calculate key metrics of a route from a GPS teacking log.

    Print the overall distance (in miles), the average and the maximum
    speeds (in mph)
    """
    with open(filename, 'r') as file:
        parser = csv.reader(file)
        next(parser)
        data = list(parser)

    miles = 0

    data = [[float(item) for item in lst] for lst in data]

    for i in range(len(data)-1):
        miles = miles + distance(data[i][1:], data[i+1][1:])

    average_speed = miles / (data[-1][0] - data[0][0]) * 3600

    maximum = 0
    for i in range(len(data)-1):
        numerator = distance(data[i][1:], data[i+1][1:])
        denominator = (data[i+1][0] - data[i][0])
        speed = numerator / denominator * 3600
        if speed > maximum:
            maximum = speed

    print_info(miles, average_speed, maximum)


def print_info(miles, average_speed, maximum):
    print("Distance: {:.1f} miles".format(miles))
    print("Average speed: {} mph".format(round(average_speed)))
    print("Maximum speed: {} mph".format(round(maximum)))


if __name__ == '__main__':
    main("gps_log.csv")
