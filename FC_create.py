from array import array
import math
import json


class Coord:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return '[' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ']'


class Octi:
    def __init__(self, ldf, rdf, ltf, rtf, ldb, rdb, ltb, rtb):
        self.ldf = ldf
        self.rdf = rdf
        self.ltf = ltf
        self.rtf = rtf
        self.ldb = ldb
        self.rdb = rdb
        self.ltb = ltb
        self.rtb = rtb


def start2(file_name):
    def get_list():
        _ = 0
        params_name = None
        for i in file_name:
            if i == '_':
                params_name = file_name[_ + 1:] + 'x'
                break
            _ += 1
        params = []
        string = ''
        for i in params_name:
            if i != 'x':
                string += i
            else:
                params.append(int(string))
                string = ''

        input_file = open(file_name + '.raw', mode='r+b')
        start_array = array('b')
        start_array.frombytes(input_file.read())
        _ = 0
        for i in start_array:
            if i != 0:
                xxx.append(_)
            _ += 1
            start_list.append(i)
        params.append(xxx.__len__())
        return params

    def create_uz():
        uz_num = (x_l + 1) * (y_l + 1) * (z_l + 1)
        for i in range(uz_num):
            z = math.floor(i / ((x_l + 1) * (y_l + 1)))
            y = math.floor((i % ((x_l + 1) * (y_l + 1))) / (x_l + 1))
            x = (i % ((x_l + 1) * (y_l + 1))) % (x_l + 1)
            tmp = Coord(x, y, z)
            uz.append(tmp)

    def create_block():
        block_num = x_l * y_l * z_l
        for i in range(block_num):
            ldf = (math.floor(i / (x_l * y_l)) * (x_l + 1) * (y_l + 1)) + (
                    math.floor((i % (x_l * y_l)) / x_l) * (x_l + 1)) + (
                          (i % (x_l * y_l)) % x_l)
            rdf = ldf + 1
            ltf = ldf + (x_l + 1) * (y_l + 1)
            rtf = ltf + 1
            ldb = rdf + x_l
            rdb = ldb + 1
            ltb = rtf + x_l
            rtb = ltb + 1
            tmp = Octi(ldf, rdf, ltf, rtf, ldb, rdb, ltb, rtb)
            blocks.append(tmp)

    def create_elems():
        for i in range(block_qua):
            elems_list.append(
                [blocks[xxx[i]].ldf + 1, blocks[xxx[i]].rdf + 1, blocks[xxx[i]].rdb + 1, blocks[xxx[i]].ldb + 1,
                 blocks[xxx[i]].ltf + 1, blocks[xxx[i]].rtf + 1, blocks[xxx[i]].rtb + 1, blocks[xxx[i]].ltb + 1])

    def create_nids_arr0():
        for i in range(block_qua):
            for j in range(8):
                if not (elems_list[i][j] in nids_arr0):
                    nids_arr0.append(elems_list[i][j])
        return nids_arr0.__len__()

    def create_nodes_arr():
        for i in range(uz_num_2):
            nodes_arr.append([uz[nids_arr0[i] - 1].x, uz[nids_arr0[i] - 1].y, uz[nids_arr0[i] - 1].z])

    def create_json_nb():
        root = {
            "bcs": [
                {
                    "id": 0,
                    "load_factors": [
                        1
                    ],
                    "load_set_numbers": [
                        0
                    ],
                    "name": "General BC",
                    "restraint_set_number": 0
                }
            ],
            "header": {
                "binary": False,
                "description": "Fidesys Case Format",
                "types": {
                    "char": 1,
                    "double": 8,
                    "int": 4,
                    "short_int": 2
                },
                "version": 3
            },
            "materials": [
                {
                    "common": [
                        {
                            "const_dep": [
                                ""
                            ],
                            "const_dep_size": [
                                0
                            ],
                            "const_names": [
                                0
                            ],
                            "const_types": [
                                0
                            ],
                            "constants": [
                                [
                                    1.0
                                ]
                            ],
                            "type": 0
                        }
                    ],
                    "elasticity": [
                        {
                            "const_dep": [
                                "",
                                ""
                            ],
                            "const_dep_size": [
                                0,
                                0
                            ],
                            "const_names": [
                                0,
                                1
                            ],
                            "const_types": [
                                0,
                                0
                            ],
                            "constants": [
                                [
                                    1
                                ],
                                [
                                    0.25
                                ]
                            ],
                            "type": 0
                        }
                    ],
                    "id": 1,
                    "name": "steel"
                }
            ],
            "settings": {
                "compute_fields": [
                    "stress",
                    "strain",
                    "displacement"
                ],
                "contact": False,
                "dimensions": "3D",
                "elasticity": True,
                "finite_deformations": False,
                "heat_transfer": False,
                "incompressibility": False,
                "linear_solver": {
                    "iter_opts": {
                        "epsilon": 1.000000000000001e-09,
                        "max_iterations": 50000,
                        "preconditioner": "auto",
                        "stopping_criteria": 0
                    },
                    "method": "direct",
                    "on_fail": True,
                    "use_uzawa": "auto"
                },
                "nonlinear_solver": {
                    "arc_method": False,
                    "line_search": False,
                    "max_iterations": 50,
                    "max_load_steps": 10,
                    "min_load_steps": 1,
                    "target_iter": 5,
                    "tolerance": 0.001
                },
                "normal_force": False,
                "outputLog": True,
                "outputVtu": False,
                "output_cs": [
                    "cartesian"
                ],
                "output_intermediate_results": True,
                "periodic_bc": False,
                "permission_write": True,
                "plasticity": False,
                "record3d": True,
                "renum": False,
                "spectral_element": False,
                "type": "effectiveprops",
                "viscosity": False
            },
            "mesh": {
                "elem_blocks": [1] * block_qua,
                "elem_materials": [1] * block_qua,
                "elem_properties": [-1] * block_qua,
                "elem_types": [3] * block_qua,
                "elemids": list(range(1, block_qua + 1)),
                "elems": elems_list,
                "elems_count": block_qua,
                "nids": nids_arr0,
                "nodes": nodes_arr,
                "nodes_count": uz_num_2
            }

        }
        output_file = open(file_name+".fc", "w")
        output_file.write(json.dumps(root, indent=4, sort_keys=True))
        output_file.close()

    start_list = []
    uz = []
    blocks = []
    xxx = []
    elems_list = []
    nids_arr0 = []
    nodes_arr = []
    x_l, y_l, z_l, block_qua = get_list()
    create_uz()
    create_block()
    create_elems()
    uz_num_2 = create_nids_arr0()
    create_nodes_arr()
    create_json_nb()
