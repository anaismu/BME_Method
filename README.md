# BME_Method
Murat A. C., Koutsombogera M., Vogel C. (2023). Event Chronography in Multimodal Data: a Method for Quantitative Analyses [ABSTRACT]. Book of Abstracts of the 1st International Multimodal Communication Symposium (MMSYM 2023), 177-178.

It allows to align according to the BME method two input tiers given their timestamps.

## FILE PRESENTATIONS
### Git_BME_Main.py 
Main code in which the files info have to be entered

### Git_BME_Functions.py 
Function code that has to be downloaded as well

#### annotation1.csv and annotation2.csv
Example of input file for a demo

### Demo.csv
Example of output file created.


## NOTES

To use the code as is, your input files (one per tier) must be .csv files with at minimum 4 columns:
 1) annotation value
 2) Start time of the annotation
 3) End time of the annotation
 4) Time Duration of the annotation
#While registering these files, please indicate the name of these columns.

The output file results into a csv file ordered with the BME method.
It contains: 
 1) B lines for Beginnings of annotations
 2) E lines for Ends of annotations
 3) M lines for Middles, with the individual index of the M. (value, M, index_m , Start time, End time, Duration)
 4) Total counts of Middles per annotation can be found in front of the E annotation. (value, E, count_m, Start time, End time, Duration)

/!\ The code inside the functions is (quite) ugly. However, it works. If I happen to have time, I'll update it.

## Contact 

If the code returns any "ERROR" tag, or if you have any question regarding the method or code, please, contact me (Anaïs) at  <b> murata@tcd.ie </b> .
