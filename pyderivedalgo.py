#!/bin/env python
from __future__ import division

class DerivedAlgorithmRunner:
 def __init__(self, slope_slope, slope_offset, offset_slope, offset_offset):
  self.slope_slope = slope_slope
  self.slope_offset = slope_offset
  self.offset_slope =  offset_slope
  self.offset_offset =  offset_offset
     
 def __slopefunc(self, raw_temp):
  return self.slope_slope * raw_temp + self.offset_slope
 def __offsetfunc(self, raw_temp):
  return self.slope_offset  * raw_temp + self.offset_offset
       
 def GetGlucoseFromRaw(self, raw_glucose, raw_temp):
  return self.__slopefunc(raw_temp) * raw_glucose + self.__offsetfunc(raw_temp)
       
def mgdl_to_mmol(glucose, molecular_weight=180):
 return (glucose)/molecular_weight*1000/100

#these params will differ for every new sensor you put on
# for these exact parameters, I took the packet from
# https://github.com/tzachi-dar/LibreOOPAlgorithm/blob/6c70d7cd48326d42381a0b40a1c30c37739b5e40/app/src/main/java/com/hg4/oopalgorithm/oopalgorithm/MainActivity.java#L252
# and calibrated it using http://libreoopweb.azurewebsites.net/Home/CalibrateSensor
#calibration result was:
# [18:54:22] {"status":"complete","slope_slope":0.000015166666666666661,"slope_offset":-0.00016666666666664771,"offset_offset":-19.500000000000114,"offset_slope":0.004500000000000032,"uuid":"calibrationmetadata-fef0eba2-b270-4d3e-8ba4-f39b1ac05c06","isValidForFooterWithReverseCRCs":49778}
runner = DerivedAlgorithmRunner(0.000015166666666666661, -0.00016666666666664771, 0.004500000000000032, -19.500000000000114)


#
# Raw glucose and raw temperature will normally be extracted from FRAM body, so these are just examples
#
glucose = runner.GetGlucoseFromRaw(raw_glucose=1900, raw_temp=4500)

print("calculated glucose is: {} mgdl or {} mmol or {} (last two should be equal)".format(glucose, glucose/18, mgdl_to_mmol(glucose) ) )

with open("file.txt", "w") as f:
 f.write("rawglucose|rawtemp|derivedalgoresult\n")
 for glucose in range(1000, 3000, 8):
   for temp in range(6000, 9000, 8):
     f.write("{}|{}|{}\n".format(glucose, temp, runner.GetGlucoseFromRaw(glucose, temp)))
     
  
   
 
 
