#IMPORT#

from copy import * #to deep copy in new cells

#FUNCTIONS#

def write_line(time, BorE, N, section, new_line): #creates a new line in the table
    line = deepcopy(new_line)
    line[0] = deepcopy(time)
    line[1] = deepcopy(BorE)
    line[N] = deepcopy(section)
    line[N][1] = deepcopy(BorE)
    return (line)

def place_new_event(section, N, table, new_line): #Places the annotation into the table according to its time stamps
    # deals with B event:
    section[1] = 'B'
    i = 0
    for line in table:

        time = deepcopy(float(line[0]))
        STT = float(section[3])
        BorE = line[1]  # B or E line
        isnt_last_line = False

        if line != table[-1]:  # if isn't the last line
            isnt_last_line = True
            time1 = float(table[i + 1][0])
            typeline1 = table[i + 1][1]  # B or E

        if isnt_last_line == True:
            if STT == time:
                if BorE == 'B':
                    line[N] = deepcopy(section)
                    break
                elif BorE == 'E':
                    if time1 != time:  # i.e if this time stamp is different from the next one. Otherwise, might want to skip to next one that could already be the B
                        firstline = write_line(STT, 'B', N, section, new_line)
                        table.insert(i + 1, firstline)
                        print("anno:", "line:", line)
                        break

            if time < STT < time1:
                firstline = write_line(STT, 'B', N, section, new_line)
                table.insert(i + 1, firstline)
                break

        elif isnt_last_line == False:
            if STT == time:
                if BorE == 'B':
                    line[N] = deepcopy(section)
                    break
                elif BorE == 'E':
                    j = 4.52
                    firstline = write_line(STT, 'B', N, section, new_line)
                    table.extend([firstline])

            elif time < STT:
                firstline = write_line(STT, 'B', N, section, new_line)
                table.extend([firstline])
                break
            else:
                print("couldn't put this line. quit")
                print("time:", time)
                print("STT:", STT)
                print("STT==Time?", STT == time)
                quit()
        i += 1

    # deals with E event:
    section[1] = 'E'
    i = 0

    for line in table:
        isnt_last_line = False
        time = deepcopy(float(line[0]))
        ETT = float(section[4])
        BorE = line[1]  # B or E line

        if line != table[-1]:  # if is the last line
            isnt_last_line = True
            time1 = float(table[i + 1][0])
            typeline1 = table[i + 1][1]  # B or E

        if isnt_last_line == True:
            if ETT == time:
                if BorE == 'E':

                    if table[i + 1][N][3] != "" and table[i + 1][N][4] != "" and table[i + 1][N][4] == table[i + 1][N][
                        3] and time == time1:
                        continue
                    else:
                        line[N] = deepcopy(section)
                        break

                elif BorE == "B":
                    if line[N][3] != "" and line[N][4] != '' and float(line[N][4]) == time == float(line[N][
                                                                                                        3]):  # i.e if it is the same event <1ms:
                        firstline = write_line(ETT, 'E', N, section, new_line)
                        table.insert(i + 1, firstline)
                        break

                    elif table[i + 1][N][3] != '' and line[N][3] != '' and float(table[i + 1][N][3]) == float(
                            line[N][3]) \
                            and typeline1 == 'E':
                        firstline = write_line(ETT, 'E', N, section, new_line)
                        table.insert(i, firstline)

                    else:
                        firstline = write_line(ETT, 'E', N, section, new_line)
                        table.insert(i, firstline)
                    break

            if time < ETT < time1:
                firstline = write_line(ETT, 'E', N, section, new_line)
                table.insert(i + 1, firstline)
                break

        else:  # if last line
            if time < ETT:
                firstline = write_line(ETT, 'E', N, section, new_line)
                table.extend([firstline])
                break

            elif time == ETT and BorE == 'E':
                line[N] = deepcopy(section)

            else:
                print("couldn't put this line. quit")
                print("Section:", section)
                print("time:", time)
                print("ETT:", ETT)
                print("line:", line)
                print("i:", i)
                quit()

        i += 1

    return(table)

def put_m(table):
    i = 0 #line index

    for section in table[-1][2:]:
            if section[1] == 'B' or section[1] == 'E':
                section[2] = '0'
            else:
                section[2] = ''

    for line in table[1:-1]:
        previousline = table[i]
        N = 0

        for section in line[2:]:
            if section[1]=='M':
                print("section==M", section)
                quit()


            if previousline[N+2][1] == 'B':
                #if the line now has nothing:
                if section[1] == '':
                    #duplicate section from the line before and replace B by M
                    line[N+2] = deepcopy(table[i][N+2])
                    line[N+2][1] = 'M'
                    line[N+2][2] = 1 #change start count to 1

                #elif the line has E and is about the same annotation (content and maybe start time):
                elif (section[1] == 'E') and (section[0] == table[i][N+2][0]) and (section[3] == table[i][N+2][3]):
                    if table[i+2][N + 2][0] == section[0] and table[i+2][N + 2][3:] == section[3:]: #if the line after is a E for the same thing.
                        line[N + 2] = deepcopy(table[i][N + 2])
                        line[N + 2][1] = 'M'
                        line[N + 2][2] = 1
                    else:
                        line[N + 2][2] = '0'

                elif (section[1] == 'B'):
                    if (section[0] == table[i][N+2][0]) and (section[3] == table[i][N+2][3]):
                        line[N+2][1] = 'M'
                        line[N+2][2] = 1

                    else:
                        line[N + 2][2] = '0'



                else:
                    line[N+2][2] = 'ERROR'

            #elif the same section on line before had a M
            elif table[i][N+2][1] == 'M':
                #if the line now has nothing:
                if section[1] == '':
                    line[N+2] = deepcopy(table[i][N+2]) #duplicate the line.
                    #count incremented by 1
                    try:
                        j = int(table[i][N + 2][2])
                        j +=1
                        line[N+2][2] = j
                    except:
                        line[N + 2][2] = "ERROR"

                # elif the line has E or B and is about the same annotation (content and maybe start time):
                elif ((section[1] == 'E') and (section[0] == table[i][N+2][0]) and (section[3] == table[i][N+2][3])):
                    if table[i + 2][N + 2][0] == section[0] and table[i + 2][N + 2][3:] == section[3:]:  # if the line after is a E for the same thing,
                        # then m+1
                        line[N + 2] = deepcopy(table[i][N + 2])
                        line[N + 2][1] = 'M'
                        j = int(table[i][N + 2][2])
                        j += 1
                        line[N + 2][2] = j
                    else:
                        line[N + 2][2] = '0'

                elif (section[1] == 'B') :
                    if (section[0] == table[i][N+2][0]) and (section[3] == table[i][N+2][3]):
                        line[N+2][1] = 'M'
                        try:
                            j = int(table[i][N+2][2])
                            j +=1
                            line[N+2][2] = j
                        except:
                            line[N + 2][2] = "ERROR"

                    else:
                        line[N + 2][2] = ''

                else:
                    line[N+2][2] = 'ERROR'

            else: #if previous == 'E' or '':
                if section[1] == 'E':
                    if (section[0] == table[i][N + 2][0]) and (section[3] == table[i][N + 2][3]):
                        line[N + 2][2] = '0'

                elif section[1] == 'B' :
                    line[N + 2][2] = '0'

                else:
                    line[N + 2][2] = ''

            N += 1
        i += 1

    #Counts the number of Ms and displays it in E lines.
    i = 0
    for line in table:
        n = 2

        for section in line[2:]:
            if section[1] not in ['M', 'B', 'E'] :
                section[1] = '0'

            if section[1] == 'B' :
                section[2] = 0
            elif section[1] == 'E':
                section[2] = table[i-1][n][2] #displays the final number of Ms on the E line
                print('table i-1, N, 2:', table[i-1][n][2])

            n += 1
        i += 1

    print('Putting M done')

    return(table)

def verifier(table):
    numberline = 0
    listofB_throughout = []
    listofE_throughout = []
    i=0
    for line in table:
        linehasBorE = 0
        listofEandBs = []
        listofSTimes =[]
        listofETimes = []
        N=0
        for column in line[2:]:
            if column[1]== 'B' or column[1] == 'E':
                linehasBorE = 1
                listofEandBs.append(column[1])
                listofSTimes.append(column[3])
                listofETimes.append(column[4])
                if column[1]== 'B':
                    for Bs in listofB_throughout:
                        if Bs[1] == column[3] and Bs[0] != numberline and table[i-2][N+2][4] != table[i-2][N+2][3]:
                            line[-3][1] = "ERROR : Same B ="+ str(column[3])+"exists on line"+ str(Bs[0]+1)+"."
                    listofB_throughout.append([numberline, column[3]])

                if column[1] =='E':
                    for Es in listofE_throughout:
                        if Es[1] == column[4] and Es[0] != numberline and table[i-1][N+2][4] != table[i-1][N+2][3]:
                            line[-3][1] = "ERROR : Same E ="+ str(column[4])+"exists on line"+ str(Es[0]+1)+"."
                    listofE_throughout.append([numberline, column[4]])
            N+=1
        i+=1

        if linehasBorE != 1:
            line[1] = 'ERROR : no B nor E'
            if numberline == 0:
                table.remove(line) #removes the first line since it was simply the first bootstrap line that eventually wasn't used.
        else:
            if len(set(listofEandBs)) > 1:
                line[1] = 'ERROR : B and E on the same line'
            else : #there are only Bs or only Es on the line
                if listofEandBs[0] == 'B':
                    if len(set(listofSTimes)) != 1:
                        line[1] = 'ERROR: Bs do not have same Starting Times'
                else : #if there are several 'E's:
                    if len(set(listofETimes)) != 1:
                        line[1] = 'ERROR: Es do not have same End Times'

        numberline += 1

    return(table)

def verifier_integritycolumns(table):
    i=1
    for line in table[1:]:
        N=2

        for section in line[2:]:
            if section[1] == 'E' and table[i-1][N][0] != section[0]:
                line[N][-1] = "ERROR: E shouldn't be here"

            if section[1] == 'B' and table[i-1][N][0] == section[0] and table[i-1][N][3] == section[3]:
                line[N][-1] = "ERROR: B shouldn't be here"
            if section[1] == 'M' and table[i-1][N][0] != section[0]:
                line[N][-1] = "ERROR: M shouldn't be here"
            N += 1
        i += 1

    i=1
    for line in table[:-1]:
        if float(line[0])>float(table[i][0]):
            line[1] = "ERROR: time isn't chronological"
        i+=1

    lastanno = ["","","","","","","","","","",""]
    for line in table[:-1]:
        section_N = 0

        for section in line[2:]:
            if section[1] == 'B':
                if lastanno[section_N] not in ['E', ""]:
                    section[5] = "ERROR: B should not be here"
                    lastanno[section_N] = 'B'
                else:
                    lastanno[section_N] = 'B'
            if section[1] == 'E' :
                if lastanno[section_N] not in ['B', 'M']:
                    section[5] = "ERROR: E should not be here"
                    lastanno[section_N] = 'E'
                else:
                    lastanno[section_N] = 'E'
            if section[1] == 'M':
                if lastanno[section_N] not in ['B', 'M']:
                    print("ERROR: M should not be here")
                    lastanno[section_N] = 'M'
                else:
                    lastanno[section_N] = 'M'

            section_N += 1
    return(table)



def writefile(name, table): #creates a csv file from the table.
    with open(name, "w") as annotatedfile:
        for line in table:
            for item in line:
                if type(item) == list:
                    for unit in item:
                        annotatedfile.write("{}\t".format(unit))
                else:
                    annotatedfile.write("{}\t".format(item))
            annotatedfile.write("\n")
    annotatedfile.close()
    return(print("Your BME annotated dataframe", name, " has been created"))

