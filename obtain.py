#!/usr/bin/python

import subprocess
result = subprocess.check_output("dmidecode -t memory", shell=True)

arr = result.split("\n\n")
dic = {'device': []}

for itm in arr:
    if 'Physical' in itm:
        for line in itm.split("\n"):
            if 'Error Correction' in line:
                dic['ecc'] = line.split(': ')[1]
            if 'Maximum Capacity' in line:
                if 'capacity' not in dic:
                     dic['capacity'] = 0
                dic['capacity'] += int(line.split(': ')[1].split(' ')[0])
    elif 'Memory Device' in itm:
        dev = {}
        for line in itm.split("\n"):
            if ": " in line:
                data = line.split(': ')[1]
                if 'Total Width' in line:
                    if not data.split(' ')[0].isdigit(): break
                    dev['totalwidth'] = int(data.split(' ')[0])
                elif 'Data Width' in line:
                    if not data.split(' ')[0].isdigit(): break
                    dev['datawidth'] = int(data.split(' ')[0])
                elif 'Size' in line:
                    if not data.split(' ')[0].isdigit(): break
                    dev['size'] = int(data.split(' ')[0])
                    if 'MB' in data:
                        dev['size'] = dev['size']/1024
                elif 'Type Detail' in line:
                    dev['type'] = data.strip()
                elif 'Part Number' in line:
                    dev['partno'] = data.strip()

        if 'totalwidth' in dev and 'datawidth' in dev:
            dev['ecc'] = dev['totalwidth'] != dev['datawidth']
        if len(dev) > 0:
            dic['device'].append(dev)

print(dic)

