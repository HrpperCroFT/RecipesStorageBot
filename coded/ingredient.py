from coded.globalvar import *

class Ingredient:
    def __init__(self, name_ = "", amount = 0, measurement = "", measuretype = "", fromlist = False, lst = []):
        if fromlist:
            self.name = lst[0]
            self.measure = list_to_measure(lst[1])
            return
        self.name = name_
        if measurement == "volume":
            self.measure = Volume(measuretype, amount)
        elif measurement == "weight":
            self.measure = Weight(measuretype, amount)
        else:
            self.measure = OtherMeasurement(amount)
    
    def to_str(self):
        return self.name + ": " + self.measure.to_str() 
    
    def to_list(self):
        return [self.name, measure_to_list(self.measure)]
        
        
def measure_to_list(measure):
    if isinstance(measure, OtherMeasurement):
        return [2, measure.amount]
    elif isinstance(measure, Volume):
        return [0, measure.measure.value, measure.amount]
    else:
        return [1, measure.measure.value, measure.amount]
    
def list_to_measure(lst):
    match lst[0]:
        case 0:
            return Volume(VolumeMeasure(lst[1]), lst[2])
        case 1:
            return Weight(WeightMeasure(lst[1]), lst[2])
        case 2:
            return OtherMeasurement(lst[1])