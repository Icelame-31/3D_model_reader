import numpy as np

colorMapIndex = {"Jet": 0, "HSV": 1, "Hot": 2, "Cool": 3, "Spring": 4, "Summer": 5, "Autum": 6, "Winter": 7, "Gray": 8,
                 "Bone": 9, "Copper": 10, "Pink": 11, "Lines": 12}

colorMap = np.zeros((13, 4, 3))
# Jet
colorMap[0][0][0] = 0
colorMap[0][0][1] = 0
colorMap[0][0][2] = 1
colorMap[0][1][0] = 0
colorMap[0][1][1] = 1
colorMap[0][1][2] = 1
colorMap[0][2][0] = 1
colorMap[0][2][1] = 1
colorMap[0][2][2] = 0
colorMap[0][3][0] = 1
colorMap[0][3][1] = 0
colorMap[0][3][2] = 0

# HSV
colorMap[1][0][0] = 1
colorMap[1][0][1] = 0
colorMap[1][0][2] = 0
colorMap[1][1][0] = 0.5
colorMap[1][1][1] = 1
colorMap[1][1][2] = 0
colorMap[1][2][0] = 0
colorMap[1][2][1] = 1
colorMap[1][2][2] = 1
colorMap[1][3][0] = 0.5
colorMap[1][3][1] = 0
colorMap[1][3][2] = 1


# Hot
colorMap[2][0][0] = 1
colorMap[2][0][1] = 0
colorMap[2][0][2] = 0
colorMap[2][1][0] = 1
colorMap[2][1][1] = 1
colorMap[2][1][2] = 0
colorMap[2][2][0] = 1
colorMap[2][2][1] = 1
colorMap[2][2][2] = 0.5
colorMap[2][3][0] = 1
colorMap[2][3][1] = 1
colorMap[2][3][2] = 1

# Cool
colorMap[3][0][0] = 0
colorMap[3][0][1] = 1
colorMap[3][0][2] = 1
colorMap[3][1][0] = 0.3333
colorMap[3][1][1] = 0.667
colorMap[3][1][2] = 1
colorMap[3][2][0] = 0.667
colorMap[3][2][1] = 0.3333
colorMap[3][2][2] = 1
colorMap[3][3][0] = 1
colorMap[3][3][1] = 0
colorMap[3][3][2] = 1

# Spring
colorMap[4][0][0] = 1
colorMap[4][0][1] = 0
colorMap[4][0][2] = 1
colorMap[4][1][0] = 1
colorMap[4][1][1] = 0.33
colorMap[4][1][2] = 0.67
colorMap[4][2][0] = 1
colorMap[4][2][1] = 0.67
colorMap[4][2][2] = 0.33
colorMap[4][3][0] = 1
colorMap[4][3][1] = 1
colorMap[4][3][2] = 0

# Summer
colorMap[5][0][0] = 0
colorMap[5][0][1] = 0.5
colorMap[5][0][2] = 0.4
colorMap[5][1][0] = 0.33
colorMap[5][1][1] = 0.67
colorMap[5][1][2] = 0.4
colorMap[5][2][0] = 0.67
colorMap[5][2][1] = 0.83
colorMap[5][2][2] = 0.4
colorMap[5][3][0] = 1
colorMap[5][3][1] = 1
colorMap[5][3][2] = 0.4

# Autumn
colorMap[6][0][0] = 1
colorMap[6][0][1] = 0
colorMap[6][0][2] = 0
colorMap[6][1][0] = 1
colorMap[6][1][1] = 0.33
colorMap[6][1][2] = 0
colorMap[6][2][0] = 1
colorMap[6][2][1] = 0.67
colorMap[6][2][2] = 0
colorMap[6][3][0] = 1
colorMap[6][3][1] = 1
colorMap[6][3][2] = 0

# Winter
colorMap[7][0][0] = 0
colorMap[7][0][1] = 0
colorMap[7][0][2] = 1
colorMap[7][1][0] = 0
colorMap[7][1][1] = 0.33
colorMap[7][1][2] = 0.83
colorMap[7][2][0] = 0
colorMap[7][2][1] = 0.67
colorMap[7][2][2] = 0.67
colorMap[7][3][0] = 0
colorMap[7][3][1] = 1
colorMap[7][3][2] = 0.5

# Gray
colorMap[8][0][0] = 0
colorMap[8][0][1] = 0
colorMap[8][0][2] = 0
colorMap[8][1][0] = 0.28
colorMap[8][1][1] = 0.28
colorMap[8][1][2] = 0.28
colorMap[8][2][0] = 0.56
colorMap[8][2][1] = 0.56
colorMap[8][2][2] = 0.56
colorMap[8][3][0] = 0.84
colorMap[8][3][1] = 0.84
colorMap[8][3][2] = 0.84

# Bone
colorMap[9][0][0] = 0
colorMap[9][0][1] = 0
colorMap[9][0][2] = 0.125
colorMap[9][1][0] = 0.2917
colorMap[9][1][1] = 0.4167
colorMap[9][1][2] = 0.4167
colorMap[9][2][0] = 0.6458
colorMap[9][2][1] = 0.7083
colorMap[9][2][2] = 0.7083
colorMap[9][3][0] = 1
colorMap[9][3][1] = 1
colorMap[9][3][2] = 1.0

# Copper
colorMap[10][0][0] = 0
colorMap[10][0][1] = 0
colorMap[10][0][2] = 0.
colorMap[10][1][0] = 0.4167
colorMap[10][1][1] = 0.2604
colorMap[10][1][2] = 0.1658
colorMap[10][2][0] = 0.8333
colorMap[10][2][1] = 0.5208
colorMap[10][2][2] = 0.3317
colorMap[10][3][0] = 1
colorMap[10][3][1] = 0.7812
colorMap[10][3][2] = 0.4975

# Pink
colorMap[11][0][0] = 0.5744
colorMap[11][0][1] = 0
colorMap[11][0][2] = 0.
colorMap[11][1][0] = 0.7454
colorMap[11][1][1] = 0.7454
colorMap[11][1][2] = 0.4714
colorMap[11][2][0] = 0.8819
colorMap[11][2][1] = 0.8819
colorMap[11][2][2] = 0.7817
colorMap[11][3][0] = 1
colorMap[11][3][1] = 1
colorMap[11][3][2] = 1

# Lines
colorMap[12][0][0] = 0
colorMap[12][0][1] = 0
colorMap[12][0][2] = 1.
colorMap[12][1][0] = 0
colorMap[12][1][1] = 0.5
colorMap[12][1][2] = 0
colorMap[12][2][0] = 1.0
colorMap[12][2][1] = 0
colorMap[12][2][2] = 0
colorMap[12][3][0] = 0
colorMap[12][3][1] = 0.75
colorMap[12][3][2] = 0.75
