class Material():
    '''define materials'''
    def __init__(self, youngModulus, density):
        self.youngModulus = youngModulus * pow(10,9)
        self.density = density

plumbum = Material(18, 11340)
aluminum  = Material(70, 2712)
silver = Material(80, 10500)
cuprum = Material(110, 8900)
steel = Material(200, 7856)