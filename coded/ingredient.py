from coded.globalvar import *

class Ingredient:
    """ This class contains full information about ingredient """
    
    def __init__(self, name_ = "", amount = 0, measurement = "", measuretype = ""):
        self.name = name_
        
        if measurement == "volume":
            self.measure = Volume(measuretype, amount)
        elif measurement == "weight":
            self.measure = Weight(measuretype, amount)
        else:
            self.measure = OtherMeasurement(amount)
    
    def to_str(self):
        """ Converts information about ingredient to string """
        
        return self.name + ": " + self.measure.to_str() 