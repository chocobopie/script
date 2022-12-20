from datetime import datetime
import os
import re
import csv

filepath = input("Đường dẫn folder chứa các file backup của Nokia .txt: ")
filelist = []

filter = []

exit = '        exit'
shutdown = '                shutdown'
counter = 0

vprn = ['        vprn 20001', '        vprn 30001', '        vprn 30010', '        vprn 40001', '        vprn 40004']
filter_string = ['            interface ', '                address ', '                sap ']
filter_string_tail = [' create', '',' create']
     

def filter_log(s):
    lines = s.splitlines()
    device_name = None
    
    for i in range(len(lines)): 
      if lines[i].startswith('        name'):
          result = re.search('        name "(.*)"', lines[i])
          device_name = result.group(1)
          #for debug
          #if device_name is not None and len(device_name) > 0:
           #filter.append('=============================================================================================')
    
    device = device_name
    full_desc = ''
    
    if device_name is not None and len(device_name) > 0:  
     for i in range(len(lines)):
      for x in range(len(vprn)):
        if lines[i].startswith(vprn[x]):
            start_line = i
            for i in range(len(lines)):
                if lines[i].startswith(exit) and i > start_line:
                    end_line = i
                    for i in range(start_line, end_line):
                        if(end_line - start_line > 20):
                            if(lines[i].startswith(filter_string[0])):
                               af_start_line = i
                               for i in range(start_line, end_line):
                                  if(lines[i].startswith(filter_string[2]) and i > af_start_line):
                                    af_end_line = i + 1
                                    if(af_end_line - af_start_line == 7):
                                     for i in range(af_start_line, af_end_line):
                                        for z in range(len(filter_string)):
                                            if(lines[i].startswith(filter_string[z])):
                                                result = re.search(filter_string[z]+'(.*)'+filter_string_tail[z], lines[i])
                                                name = result.group(1)
                                                full_desc = full_desc+','+name
                                     device = device+''+full_desc
                                     print(device)
                                     filter.append(device)
                                     device = device_name
                                     full_desc = ''
                    break
                              
def save_file():
    
    #xuất file txt để debug
    #with open('C:\\Users\\kronk\\Desktop\\filter_log.txt', 'w') as f:
    #    for x in filter:
    #        f.write(f"{x}\n")
    
    today = datetime.today().strftime('%d-%m-%Y')
    
    #xuất file csv
    with open('C:\\Users\\kronk\\Desktop\\Nokia_filter_'+today+'.csv', 'w', encoding = 'UTF8', newline= '') as csvfile:
        header = ['Device', 'Interface', 'Address', 'Sap']
        writer = csv.writer(csvfile, delimiter = ',')
        writer.writerow(header)
        for line in filter:
            tmp = line.split(',')
            writer.writerow(tmp)
        csvfile.close()
    print('Filter completed selected files at date: ' + today)
                   
for root, dirs, files in os.walk(filepath):
	for file in files:
		filelist.append(os.path.join(root,file))

for file in filelist:
    f = open(file)
    s = f.read()
    filter_log(s)
    f.close()
    
save_file() 
    
