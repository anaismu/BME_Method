#IMPORT#

from copy import * #to deep copy in new cells
import pandas as pd
from Git_BME_Functions import *

#YOUR DATA#
#Note: Your input files (one per tier) must be .csv files with at minimum 4 columns:
## 1) annotation value
## 2) Start time of the annotation
## 3) End time of the annotation
## 4) Time Duration of the annotation
#While registering these files, please indicate the names of these columns.

input_files = {
    "file1" : {"pathway":"", "name":"annotation1.csv", "column_annotation_value":"value", "column_Start_Time":"ST", "column_End_Time":"ET", "column_duration":"duration"},
    "file2" : {"pathway":"", "name":"annotation2.csv", "column_annotation_value":"value", "column_Start_Time":"ST", "column_End_Time":"ET", "column_duration": "duration"}
}

output_file = {
    "pathway" : "",
    "name" : "Demo.csv"
}

#INITIATES THE TABLE#

number_of_columns = len(input_files) #number of columns == number of files i.e number of tiers

table = [] #initiates the output table
header_output = ['Time', 'BE_line'] #will be appended with column names
new_line = [0,"B"] #First line, hence timestamp 0.

for x in range(number_of_columns): #adds up space for columns of annotations.
    new_line.append(["", "", "", "", "", ""])

table.append(deepcopy(new_line))

#ORDERS TAGS#

number_column = 2 #because 0 and 1 are respectively Time and BE_line columns.

for file in input_files :
    print("Dealing with", file)
    dataframe = pd.read_csv(str(input_files[file]["pathway"]) + str(input_files[file]["name"])) #opens input file
    names_column = ["Tag_"+input_files[file]["name"],"BME_"+input_files[file]["name"],"N_"+input_files[file]["name"],"ST_"+input_files[file]["name"],"ET_"+input_files[file]["name"]] #creates the output header automatically
    for name in names_column :
        header_output.append(name)

    for i, anno in enumerate(dataframe[input_files[file]["column_annotation_value"]]): #for each annotation of the file
        #gets all the information
        tag = anno
        Start_Time = float(dataframe[input_files[file]["column_Start_Time"]][i])
        End_Time = float(dataframe[input_files[file]["column_End_Time"]][i])
        duration = float(dataframe[input_files[file]["column_duration"]][i])
        section =   [tag, '', '', Start_Time, End_Time, duration]
        #inserts info into the table
        table = place_new_event(section, int(number_column), table, deepcopy(new_line))
    number_column += 1   #is incremented as we are moving to the next column (i.e next tier)

print("Starts adding Ms...")
table = put_m(table) #counts the number of Ms between B and Es
print("Starts checking the entire table...")
table = verifier(table) #checks that the linear alignment is coherent; error tagged by "ERROR"
table = verifier_integritycolumns(table) #checks that all annotations in columns follow "B+x*M+E" order; error tagged by "ERROR".
print("Verification done; if any, errors tagged with keyword 'ERROR'")

table.insert(0, header_output) #inserts the header

writefile(output_file["pathway"] + output_file["name"], table) #creates the csv file

