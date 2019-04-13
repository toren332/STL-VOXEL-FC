from stl import mesh
import math
import copy
import numpy as np
from box_triangle import intersects_box
from mpl_toolkits import mplot3d
from matplotlib import pyplot
import matplotlib.pyplot as plt
from array import array
import re
import sys

sys.setrecursionlimit(100000)

def round_custom(number):
    if number < 0:
        return math.floor(number)
    else:
        return math.ceil(number)


def start(file_name, detalization_level, layers):
    def mm():
        maximum_x = -float('inf')
        maximum_y = -float('inf')
        maximum_z = -float('inf')
        minimum_x = float('inf')
        minimum_y = float('inf')
        minimum_z = float('inf')
        for triangle in mesh0:
            _ = [[triangle[0], triangle[1], triangle[2]],
                 [triangle[3], triangle[4], triangle[5]],
                 [triangle[6], triangle[7], triangle[8]]]
            for dot in _:
                if dot[0] > maximum_x:
                    maximum_x = dot[0]
                elif dot[0] < minimum_x:
                    minimum_x = dot[0]
                if dot[1] > maximum_y:
                    maximum_y = dot[1]
                elif dot[1] < minimum_y:
                    minimum_y = dot[1]
                if dot[2] > maximum_z:
                    maximum_z = dot[2]
                elif dot[2] < minimum_z:
                    minimum_z = dot[2]
            mesh1.append(_)
        maximum_x = round_custom(maximum_x)
        maximum_y = round_custom(maximum_y)
        maximum_z = round_custom(maximum_z)
        minimum_x = round_custom(minimum_x)
        minimum_y = round_custom(minimum_y)
        minimum_z = round_custom(minimum_z)
        return [maximum_x, maximum_y, maximum_z, minimum_x, minimum_y, minimum_z]

    def real_cube_mesh():
        x_centers = []
        y_centers = []
        z_centers = []
        for i in range(round(min_x / voxel_size), round(max_x / voxel_size)):
            x_centers.append(i * voxel_size + voxel_size / 2)

        for i in range(round(min_y / voxel_size), round(max_y / voxel_size)):
            y_centers.append(i * voxel_size + voxel_size / 2)

        for i in range(round(min_z / voxel_size), round(max_z / voxel_size)):
            z_centers.append(i * voxel_size + voxel_size / 2)

        for x_center in x_centers:
            for y_center in y_centers:
                for z_center in z_centers:
                    all_centers.append([x_center, y_center, z_center])

    def voxel_mesh():
        x_centers = []
        y_centers = []
        z_centers = []
        for i in range(round(min_x / voxel_size), round(max_x / voxel_size)):
            x_centers.append(round(i - min_x / voxel_size))

        for i in range(round(min_y / voxel_size), round(max_y / voxel_size)):
            y_centers.append(round(i - min_y / voxel_size))

        for i in range(round(min_z / voxel_size), round(max_z / voxel_size)):
            z_centers.append(round(i - min_z / voxel_size))
        for x_center in x_centers:
            for y_center in y_centers:
                for z_center in z_centers:
                    all_voxel_centers.append([x_center, y_center, z_center])

    def insertions():
        block_number = 0
        for center in all_centers:
            good = 0
            for triangle in mesh1:
                if intersects_box(np.array(triangle), np.array(center), voxel_size):
                    good = 1
                    break
            if good == 0:
                bad_voxels.append(all_voxel_centers[block_number])
            block_number += 1
            # print(str(block_number) + '/' + str(all_centers.__len__()))

    def find_fill_coord():
        for zz in range(y_l):
            for xx in range(x_l):
                for yy in range(z_l):
                    if n_voxels[xx][yy][zz] == 1:
                        beam1 = ''
                        beam2 = ''
                        for zz_1 in range(zz, y_l):
                            # верхний луч
                            beam1 += str(int(n_voxels[xx][yy][zz_1]))
                        for zz_2 in range(0, zz + 1):
                            # нижний луч
                            beam2 += str(int(n_voxels[xx][yy][zz_2]))

                        nbeam1 = beam1[::-1]
                        nbeam2 = beam2[::-1]
                        match1 = re.search(r'0*1+0+[0-1]*1+0*', nbeam1)
                        match2 = re.search(r'0*1+0+[0-1]*1+0*', nbeam2)

                        if match1:
                            first_1 = 0
                            for nchar in range(nbeam1.__len__()):
                                char = nbeam1[nchar]
                                if char == '1' and first_1 == 0:
                                    first_1 = 1
                                if char == '0' and first_1 == 1:
                                    zzz = zz + nbeam1.__len__() - nchar - 1
                                    fill_coords = [xx, yy, zzz]
                                    return fill_coords

                        elif match2:
                            first_1 = 0
                            for nchar in range(nbeam2.__len__()):
                                char = nbeam2[nchar]
                                if char == '1' and first_1 == 0:
                                    first_1 = 1
                                if char == '0' and first_1 == 1:
                                    zzz = nbeam2.__len__() - 1 - nchar
                                    fill_coords = [xx, yy, zzz]
                                    return fill_coords
                        else:
                            pass

    def fill(coord):
        if coord[0]<x_l and coord[1]<z_l and coord[2]<y_l:
            if n_voxels[coord[0]][coord[1]][coord[2]] == 0:
                n_voxels[coord[0]][coord[1]][coord[2]] = 1

                ncoord1 = copy.deepcopy(coord)
                ncoord1[0] = ncoord1[0] - 1
                if n_voxels[ncoord1[0]][ncoord1[1]][ncoord1[2]] == 0:
                    fill(ncoord1)

                ncoord2 = copy.deepcopy(coord)
                ncoord2[0] = ncoord2[0] + 1
                if n_voxels[ncoord2[0]][ncoord2[1]][ncoord2[2]] == 0:
                    fill(ncoord2)

                ncoord3 = copy.deepcopy(coord)
                ncoord3[1] = ncoord3[1] - 1
                if n_voxels[ncoord3[0]][ncoord3[1]][ncoord3[2]] == 0:
                    fill(ncoord3)

                ncoord4 = copy.deepcopy(coord)
                ncoord4[1] = ncoord4[1] + 1
                if n_voxels[ncoord4[0]][ncoord4[1]][ncoord4[2]] == 0:
                    fill(ncoord4)

                ncoord5 = copy.deepcopy(coord)
                ncoord5[2] = ncoord5[2] - 1
                if n_voxels[ncoord5[0]][ncoord5[1]][ncoord5[2]] == 0:
                    fill(ncoord5)

                ncoord6 = copy.deepcopy(coord)
                ncoord6[2] = ncoord6[2] + 1
                if n_voxels[ncoord6[0]][ncoord6[1]][ncoord6[2]] == 0:
                    fill(ncoord6)
                # 6

        pass

    mesh0 = mesh.Mesh.from_file('models/' + file_name + '.stl')
    mesh1 = []
    max_x, max_y, max_z, min_x, min_y, min_z = mm()
    voxel_size = 0.5 ** detalization_level

    x_l = round((max_x - min_x) / voxel_size)
    y_l = round((max_y - min_y) / voxel_size)
    z_l = round((max_z - min_z) / voxel_size)
    all_centers = []
    all_voxel_centers = []
    voxel_mesh()
    real_cube_mesh()
    bad_voxels = []
    insertions()
    n_voxels = np.ones((x_l, z_l, y_l))

    for vox in bad_voxels:
        x_, y_, z_ = vox
        n_voxels[x_][z_][y_] = 0

    fill(find_fill_coord())
    raw_list = []
    for yy in range(y_l):
        for xx in range(x_l):
            for zz in range(z_l):
                if layers != -1:
                    if yy > layers - 1:
                        n_voxels[xx][zz][yy] = 0
                if n_voxels[xx][zz][yy] == 1:
                    raw_list.append(1)
                else:
                    raw_list.append(0)
    output_file = open(file_name + '_' + str(z_l) + 'x' + str(x_l) + 'x' + str(y_l) + ".raw", "wb")
    new_array = array('b', raw_list)
    new_array.tofile(output_file)
    output_file.close()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.voxels(n_voxels, edgecolor='k')

    plt.show()
    return file_name + '_' + str(z_l) + 'x' + str(x_l) + 'x' + str(y_l)
