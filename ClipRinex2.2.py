import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

    

## from an list argument of strings readed in main, 
## return a specific sequence that represents the starting date
def find_sdate(date_list):

    index = date_list.index('FIRST') - 9

    date_list = date_list[index:index + 6]
    
    year = re.findall('..', date_list[0])
        
    sec = re.findall('..', date_list[5])
    
    sec = re.findall('.', sec[0])
    
    if sec[1] == '.':
        sec = sec[0]
    else:
        sec = re.findall('..', date_list[5])
    
    date_list[0] = year[1]
       
    date_list[-1] = sec[0]
    
    sdate = [int(x) for x in date_list]
                
    if int(date_list[1]) < 10:
        mode = re.findall('.', date_list[1])[0]
    elif int(date_list[3]) < 10:
        mode = re.findall('.', date_list[2])[0]
    else:
        mode = re.findall('.', date_list[3])[0]
        
    if mode != '0':
        mode = ' '

    return sdate, mode




## from an list argument of strings readed in main, 
## return a specific sequence that represents the ending date
def find_edate(date_list):

    index = date_list.index('LAST') - 9

    date_list = date_list[index:index + 6]
        
    year = re.findall('..', date_list[0])
        
    sec = re.findall('..', date_list[5])
    
    sec = re.findall('.', sec[0])
    
    if sec[1] == '.':
        sec = sec[0]
    else:
        sec = re.findall('..', date_list[5])
    
    date_list[0] = year[1]
       
    date_list[-1] = sec[0]
    
    edate = [int(x) for x in date_list]
    
    edate[-1] = edate[-1] + 1

    return edate



def advance_date(date_list, step):    
    if date_list[4] + step < 60:        
        date_list[4] = date_list[4] + step

    else:        
        date_list[4] = date_list[4] + step - 60

        if date_list[3] + 1 < 60:            
            date_list[3] = date_list[3] + 1

        else:            
            date_list[3] = date_list[3] + 1 - 60

            date_list[2] = date_list[2] + 1

    return date_list



def retreat_date(date_list, step):    
    if date_list[4] - step > 0:        
        date_list[4] = date_list[4] - step

    else:        
        date_list[4] = date_list[4] - step + 60

        if date_list[3] - 1 > 0:            
            date_list[3] = date_list[3] - 1

        else:            
            date_list[3] = date_list[3] - 1 + 60

            date_list[2] = date_list[2] - 1

    return date_list



def clip_rinex(rinex_list, adate, rdate):
    substring = 'HEADER'
    
    sclip = [string for string in rinex_list if substring in string]

    sindex = rinex_list.index(sclip[0])
            
    mclip = [string for string in rinex_list if adate in string]

    mindex = rinex_list.index(mclip[0])
        
    eclip = [string for string in rinex_list if rdate in string]

    eindex = rinex_list.index(eclip[0])
        
    cliped = []
    
    cliped.append(rinex_list[:sindex + 1] + rinex_list[mindex:eindex])
        
    return cliped[0]



def main():
    Tk().withdraw()
    
    path = askopenfilename()
    
    text = open(path, 'r')

    lines = text.readlines()

    beginning, ending = lines[:100], lines[-100:]

    sdate_list = ' '.join(beginning).split()

    find = find_sdate(sdate_list)

    sdate = find[0]
    
    mode = find[1]

    adate = advance_date(sdate, 5)

    adate = [str(x) for x in adate]
    
    for i in range(0, len(adate)):        
        if int(adate[i]) < 10:            
            adate[i] = mode + adate[i]

    adate[5] = adate[5] + '.0000000'

    adate = ' '.join(adate)
        
    edate_list = ' '.join(beginning).split()
    
    edate = find_edate(edate_list)

    rdate = retreat_date(edate, 5)

    rdate = [str(x) for x in rdate]
    
    for i in range(0, len(rdate)):        
        if int(rdate[i]) < 10:            
            rdate[i] = mode + rdate[i]
    
    rdate[5] = rdate[5] + '.0000000'

    rdate = ' '.join(rdate)    
    
    cliped = clip_rinex(lines, adate, rdate)

    if '.21O' in path:
        fileindex = path.index('.21O')
    else:
        fileindex = path.index('.21o')
        
    filename = path[:fileindex] + '_cliped' + path[fileindex:]
        
    rinex_cliped = open(filename, 'w')
    
    for i in cliped:
        rinex_cliped.write(i)
        
    rinex_cliped.close()



if __name__ == '__main__':
    
    main()


