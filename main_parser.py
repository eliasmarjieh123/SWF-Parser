from shutil import copyfile, copy
import os
from datetime import datetime, date
from RowClass import RowClass
import matplotlib.pyplot as plt 
import numpy as np
# datetime, order, submit_time, runtime, number_of_nodes, user_id, group_id,
# application_id, number_of_queues, wait_time=0, average_cpu_time=-1, average_memory_per_node=-1,
# requested_processors=-1, requested_runtime=-1, requested_memory=-1, status=-1, number_of_partitions=-1,
# preceding_job_number=-1, think_time=-1

original_log_path = "log_files/NASA-iPSC-1993-0.txt"
SWF_log = "log_files/SWF_log.txt"

if os.path.isfile(SWF_log):  # delete SWF file if already exists
    os.remove(SWF_log)

# copyfile(original_log_path, SWF_log)

log_file = open(original_log_path, "r")

row_counter = 1

first_row = log_file.readline()
log_file.seek(0)

started_time = datetime.strptime(first_row.split()[4] + " " + first_row.split()[5], "%m/%d/%y %H:%M:%S")

Interarrivals=dict()
Interarrivals2=list()
Interarrivals1=list()




with open(SWF_log, "w") as swf_file:
    for row in log_file.readlines():

        row_split_list = row.split()

        date_and_time = datetime.strptime(row_split_list[4] + " " + row_split_list[5], "%m/%d/%y %H:%M:%S")

        submit_time = datetime.combine(date.today(), date_and_time.time()) - datetime.combine(date.today(),
                                                                                              started_time.time())  # subtract current time from start time to get time from beginning
        runtime = row_split_list[3]

        number_of_nodes = row_split_list[2]

        user_id = row_split_list[0]

        if (str.__contains__(user_id, "user")):
            group_id = 1
        else:  # sysadmin
            group_id = 2

        application_id = row_split_list[1]

        number_of_queues = 1

        current_row = RowClass(date_and_time, row_counter, submit_time.seconds, runtime, number_of_nodes, user_id, group_id,
                               application_id, number_of_queues)

        swf_file.write(current_row.convert_to_string())

        row_counter += 1
        




'''
Interarrivals=dict()
Interarrivals2=list()
Interarrivals1=list()
def CreateInterarrivalsDict():
    SWF=open(SWF_log,"r")
    for row in SWF:
        row=row.split()
        secs=datetime.strptime(row[18]+' '+row[19], '%Y-%m-%d %H:%M:%S')
        Interarrivals1.append(secs)
    i=1;
    while i<len(Interarrivals1):
        Interarrivals1[i-1]=(Interarrivals1[i]-Interarrivals1[i-1]).total_seconds()
        i+=1
    Interarrivals1.remove(Interarrivals1[i-1])  
    for secs in Interarrivals1:
        if secs in Interarrivals.keys():
            Interarrivals[secs]+=1
        else:
            Interarrivals2.append(secs)
            Interarrivals.setdefault(secs,1)
    SWF.close()
    
    
CreateInterarrivalsDict()
Probabilities=list()
Interarrivals2.sort()
vals=list()
for v in Interarrivals2:
    vals.append(Interarrivals[v])
    
for v in vals:
    Probabilities.append(v/len(Interarrivals1))
#here we show the probabilities graph
plt.title("Probability(y) of Interarrivals times in seconds(x)")
plt.xscale('log',basex=2)
plt.plot(Interarrivals2, Probabilities)
plt.xlim(0, 1000)
plt.ylim(0, 0.017)
plt.xlabel('Interarrival (seconds)')
plt.ylabel('PDF')
plt.show()


#here we show the CDF grph
Probabilities2=list()
Interarrivals3=list()
i=0
while i<52000:
    p=0
    j=0
    Interarrivals3.append(i)
    while Interarrivals2[j]<i:
        p+=Probabilities[j]
        j+=1
    i+=1    
    Probabilities2.append(p)
plt.title("Cumulative Probability(y) of Interarrivals times in seconds(x)")    
plt.xscale('log',basex=2)    
plt.plot(Interarrivals3, Probabilities2)
plt.xlim(0, 2000)
plt.ylim(0, 1)
plt.xlabel('Interarrival (seconds)')
plt.ylabel('Comulative probability')
plt.show()
    
RunTimes=list()
RunTimes2=list()
RunTimesDict=dict()
RunTimesProbabilities=list()
RunTimesProbabilities2=list()

RunTimesS=list()
RunTimes2S=list()
RunTimesDictS=dict()
RunTimesProbabilitiesS=list()
RunTimesProbabilities2S=list()



def  CreateRunTimes():
    SWF=open(SWF_log,"r")
    for row in SWF:
        row=row.split()
        runTime=int(row[3])
        RunTimes.append(runTime)
        if row[11] == "special":
            RunTimesS.append(int(row[3]))
    for runTime in RunTimes:
        if runTime in RunTimesDict.keys():
            RunTimesDict[runTime]+=1
        else:
            RunTimes2.append(runTime)
            RunTimesDict.setdefault(runTime,1)
            
    for runTime in RunTimesS:
        if runTime in RunTimesDictS.keys():
            RunTimesDictS[runTime]+=1
        else:
            RunTimes2S.append(runTime)
            RunTimesDictS.setdefault(runTime,1)    
            
    SWF.close()
    
CreateRunTimes()

RunTimes2=sorted(RunTimes2)
RunTimes2S=sorted(RunTimes2S)
vals=list()

for r in RunTimes2:
    vals.append(RunTimesDict[r])

for v in vals:
    RunTimesProbabilities.append(v/len(RunTimes))
vals=list()    

for r in RunTimes2S:
    vals.append(RunTimesDictS[r])

for v in vals:
    RunTimesProbabilitiesS.append(v/len(RunTimesS))
plt.title("Probability(y) of Run Times in seconds(x)")    
plt.xscale('log',basex=2)
plt.plot(RunTimes2, RunTimesProbabilities,label="All Jobs")
plt.plot(RunTimes2S, RunTimesProbabilitiesS,label="Jobs by user special")
plt.xlim(0, 52000)
plt.ylim(0, 0.1)
plt.xlabel('Run Time (seconds)')
plt.ylabel('probability')
plt.legend()
plt.show()
i=0
RunTimes3=list()
RunTimes3O=list()
RunTimes3S=list()
while i<52000:
    p=0
    j=0
    RunTimes3.append(i)
    while RunTimes2[j]<i:
        p+=RunTimesProbabilities[j]
        j+=1
    i+=1    
    RunTimesProbabilities2.append(p)

i=0
while i<52000:
    p=0
    j=0
    RunTimes3S.append(i)
    while RunTimes2S[j]<i:
        p+=RunTimesProbabilitiesS[j]
        j+=1
    i+=1    
    RunTimesProbabilities2S.append(p)
plt.title("Cumulative probability(y) of Run Times in seconds(x)")     
plt.xscale('log',basex=2)
#plt.plot(RunTimes3O, RunTimesProbabilities2O,label="Other Jobs")
plt.plot(RunTimes3, RunTimesProbabilities2,label="All Jobs")
plt.plot(RunTimes3S, RunTimesProbabilities2S,label="user special Jobs")
plt.xlim(1, 51000)
plt.ylim(0, 1)
plt.xlabel('Run Time (seconds)')
plt.ylabel('Cumulative probability')
plt.legend()
plt.show()

print(sum(Probabilities))
print(sum(RunTimesProbabilities))
print(sum(RunTimesProbabilitiesS))'''''''''''