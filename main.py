from RAW_create import start
from FC_create import start2

# filename = "CubeWithoutCube"
filename = "CubeWithoutCube"
detalization_level = 1
raw_filename = start(filename, detalization_level, -1)
start2(raw_filename)
