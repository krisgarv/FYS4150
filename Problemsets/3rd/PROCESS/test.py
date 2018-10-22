import numpy as np
import re

i = 0

objects = ['Earth']

if 'Sun' not in objects:
    objects.append('Sun')
input_matrix = np.empty((len(objects), 7))
data = open('CODES/planets_distancespeed.txt', 'r')
for lines in data.read().splitlines():
    name = re.findall(r"(^\D+):", lines)
    if len(set(name) & set(objects)) >= 1:
        index = lines.index(':')
        numbers = lines[index+1:]
        array = np.asarray([float(value) for value in numbers.split(',')])
        input_matrix[i, :] = array
        i += 1
print (input_matrix)
input_matrix[:, 4:7] = input_matrix[:, 4:7]*365
print(input_matrix)

def CM(matrix):
    #new_position = np.zeros(3)
    x, y, z = sum(matrix[:, 0].reshape(len(objects), 1)*matrix[:, 1:4])/sum(matrix[:, 0])
    print(x, y, z)
    matrix[:, 1] = matrix[:, 1]-x
    matrix[:, 2] = matrix[:, 2]-y
    matrix[:, 3] = matrix[:, 3]-z
    numerator = np.empty(3)
    for i in range(1, len(objects)):
        numerator += matrix[i, 0]*matrix[i, 1:4]*matrix[i, 4:7]
        #(matrix[i, 0]*matrix[i, 1:4]*matrix[i, 4:7])/(matrix[0, 0]*matrix[0, 1:4])
    matrix[0, 4:7] = numerator/(matrix[0, 0]*matrix[0, 1:4])
    #sum(matrix[1:, 0]*matrix[1:, 1:4]*matrix[1:, 4:7])/(matrix[0, 0]*matrix[0, 1:4])
    return matrix



matrix = CM(input_matrix)
print (matrix)


"""
def center_of_mass(self, matrix):
    # Changing the positions of all objects relative to center of mass, in origo.
    x = sum(matrix[:, 0]*matrix[:, 1])/sum(matrix[:, 0])
    y = sum(matrix[:, 0]*matrix[:, 2])/sum(matrix[:, 0])
    z = sum(matrix[:, 0]*matrix[:, 3])/sum(matrix[:, 0])
    # x-direction
    matrix[:, 1]-x
    # y-direction
    matrix[:, 2]-y
    # z-direction
    matrix[:, 3]-z
    # empty array for the initial velocity of the Sun
    numerator = np.empty(3)
    # The Suns initial velocity which makes the total momentum of the system zero
    # velcity_sun = (sum(mass_planet_i*veocity_planet_i*position_planets_i)/(mass_sun*position_sun))
    for i in range(1, len(self.objects)):
        # Calculating the numerator first to avoid repetative calculation
        numerator += matrix[i, 0]*matrix[i, 1:4]*matrix[i, 4:7]
    # Divinding by the mass and position of the Sun
    matrix[0, 4:7] = numerator/(matrix[0, 0]*matrix[0, 1:4])
    # Returning the modified matrix
    return matrix
"""
