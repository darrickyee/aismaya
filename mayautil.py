def fixRotations(vec):
    return [rot if rot <= 180 else rot - 360 for rot in vec]
