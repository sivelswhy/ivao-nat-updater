from itertools import count
from lib2to3.pgen2.token import RPAR
import requests
from pathlib import Path
import os
import sys
import re
n = 0
g = False
fixes = []
a_fixes = []
TMI = []
string = ""
string2 = ""
if getattr(sys, 'frozen', False):absolute_path = os.path.dirname(sys.executable)
elif __file__:absolute_path = os.path.dirname(__file__)
path_path = absolute_path+"\path.txt"
if os.path.isfile(path_path):
    f = open(path_path,"r")
    aurora_path = f.read()
else:
    aurora_path = input('Paste "Aurora" folder path: ').rstrip("\\")
    os.system('cls')
    aurora_path = aurora_path+"\\SectorFiles\\Include\\XA\\czqx\\"
    f = open(path_path,"w")
    f.write(aurora_path)
    f.close()
    print("Created file with Aurora path in this directory: "+path_path+"\n")
with open(os.path.join(aurora_path + "fixes.fix"),'r') as file:
    data = file.read().split("\n")
    if data[-1] == "":g = True
for b in data:
    if "//" not in b:
        b = b.split(";")
        a_fixes.append(b[0])
a_fixes = list(filter(None, a_fixes))
try:
    response = requests.get("https://www.notams.faa.gov/common/nat.html")
    response = response.content.decode("UTF-8").split("\n")
except requests.exceptions.ConnectionError as errc:
    print("Script couldn't download necessary data. Please check your internet connection!")
    input("Press ENTER to exit")
    raise SystemExit()
for d in response:
    if ("TMI" in d) and ("IS" in d) and (("1." in d) or ("1 ." in d)):
        d = re.findall(r'\d+',d)
        TMI.append(d[1])
TMI = list(dict.fromkeys(TMI))
if len(TMI)>1:
    for e in TMI:
        string = string + " " +e
    print("NATs that were generated with TMIs:"+string)
else:print("NATs that were generated with TMI: "+TMI[0])
string = ""
while n < len(response):
    flightlevels = ""
    if "EAST LVLS" in response[n]:   
        t = 0  
        NAT = response[n-1].split(" ")
        print("\tNAT"+NAT[0])


        if "EAST LVLS NIL" in response[n]:
            i = response[n+1].split(" ")
            for h in i[2:]:
                flightlevels = flightlevels + str(h) + " "
            flightlevels = flightlevels[:-1]
        else:
            i = response[n].split(" ")
            for h in i[2:]:
                flightlevels = flightlevels + str(h) + " "
            flightlevels = flightlevels[:-1]

        for a in NAT[1:]:
            if "/" in a:
                k = NAT[NAT.index(a)+1].split("/")
                a = a.split("/")
                if len(a[0])>2:
                    split_a = [a[0][idx:idx+2] for idx in range(0,len(a[0]),2)]
                    string = string + "T;NAT"+NAT[0]+";H"+str(split_a[0])+str(a[1])+";H"+str(split_a[0])+str(a[1])+";\n"
                    newFix = str("H"+str(split_a[0])+str(a[1])+";N0"+str(split_a[0])+"."+str(split_a[1])+".00.000;W0"+str(a[1])+".00.00.000;")
                    fixes.append(newFix)
                    if t == 0: 
                        if len(k[0])>2:
                            split_k = [k[0][idx:idx+2] for idx in range(0,len(k[0]),2)]
                        string = string + "L;NAT"+NAT[0]+";H"+str(split_a[0])+str(a[1])+";H"+str(split_a[0])+str(a[1])+";\n"
                        string2 = string2 + NAT[0] + " " + str(flightlevels) + ";;N0" + str(split_k[0]) + ".30.00.000;W0" + str(k[1])+".00.00.000;\n"
                        t+=1
                else:
                    string = string + "T;NAT"+NAT[0]+";"+str(a[0])+str(a[1])+"N;"+str(a[0])+str(a[1])+"N;\n"
                    newFix = str(str(a[0])+str(a[1])+"N;N0"+str(a[0])+".00.00.000;W0"+str(a[1])+".00.00.000;")
                    fixes.append(newFix)
                    if t == 0: 
                        string = string + "L;NAT"+NAT[0]+";"+str(a[0])+str(a[1])+"N;"+str(a[0])+str(a[1])+"N;\n"
                        string2 = string2 + NAT[0] + " " + str(flightlevels) + ";;N0" + str(k[0]) + ".00.00.000;W0" + str(k[1])+".00.00.000;\n"
                        t+=1
            else:
                string = string + "T;NAT"+NAT[0]+";"+str(a)+";"+str(a)+";\n"
                fixes.append(a)
    n+=1
fixes = list(dict.fromkeys(fixes))
f = open(os.path.join(aurora_path + "fixes.fix"),"a")
c=0
for a in fixes:
    a_split = str(a).split(";")
    if a_split[0] not in a_fixes:
        c += 1
        if len(a_split)>1:
            if c == 1:
                print("\nFixes that were added:")
                if g == False:f.write("\n")
            f.write(a+"\n")
        else:
            if c == 1: print("Fixes that have to be added manualy:")
        print("\t"+a_split[0])
if c == 0:print("\nNo additional fixes were added.")
f.close()
f = open(os.path.join(aurora_path + "highairway.awh"),'w')
f.write(string)
f.close()
f = open(os.path.join(aurora_path + "cyqx.vfi"),'w')
f.write(string2)
f.close()
input("Press ENTER to exit")