import numpy as np
CAMERA_HEIGHT = 1.65 #m

#matrix_coefficients - Intrinsic matrix of the calibrated camera
MATRIX_COEFFICIENTS = np.array([[
            1447.9804004365824,
            0.0,
            617.3063266183908
        ],
        [
            0.0,
            1448.4116664252433,
            289.02239681156016
        ],
        [
            0.0,
            0.0,
            1.0
        ]])

#distortion_coefficients - Distortion coefficients associated with our camera
DISTORTION_COEFFICIENTS = np.array([
            0.0397515407032859,
            1.259291585298002,
            -0.010631456171277863,
            -0.00784841820297665,
            -5.925444820936321
        ])
    