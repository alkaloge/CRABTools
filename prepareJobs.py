
# generate a runMC.csh script that creates the .csh and .jdl files
# to process MC data 

import os

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--inFile",default='MCsamples_2016.csv',help="Input file name.") 
    parser.add_argument("-y","--year",default=2017,type=int,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-t","--tag",default='ZH',type=str,help="Select a tag")
    parser.add_argument("-s","--doSystematics",default='yes',type=str,help="do JME systematics")
    parser.add_argument("-l","--islocal",default='no',type=str,help="local /eos files or DBS")
    #parser.add_argument("-i","--isMC",default='yes',type=str,help="flag if this is MC")
    return parser.parse_args()

args = getArgs() 
era=str(args.year)
outLines = []
cwd = os.getcwd()
conc=5
if str(args.islocal.lower())=='yes' or str(args.islocal.lower())=='1' or str(args.islocal.lower())=='true': conc = 1

for line in open(args.inFile,'r').readlines() :
    if 'Run' in line or 'data' in line :
    #if str(args.isMC.lower())=='yes' or str(args.isMC.lower())=='true' or str(args.isMC.lower())=='1': 
        print 'this is a MC?'
	nickname = line.split(',')[0]

	#print("\n\n\n line.split(',')={0:s}".format(str(line.split(','))))
	dataset = line.split(',')[6].replace(' ','_').strip()

    else :

        print 'this is likely MC '
        dataset = line.strip()
        if len(dataset) < 2 : continue
        nickname = dataset.split('/')[1] + '_' + dataset.split('/')[2].split('-')[0]
        if 'ver2' in dataset : nickname +="ver2"
        if 'ver1' in dataset : nickname +="ver1"


    if 'NANO' in dataset : conc=5
    if len(dataset) < 2 : continue
    #print("\n***line.split()={0:s}".format(str(line.split(','))))
    print("nickname={0:s} \n dataset={1:s}".format(nickname,dataset))

    mode = 'anaXRD'
    if '#' in nickname : continue
    
    outLines.append("mkdir -p {0:s}/{1:s}_{2:s}\ncd {0:s}/{1:s}_{2:s}\n".format(args.tag,nickname,era))
    #if 'Run' not in nickname : 
    outLines.append("python ../../sendJobs.py --dataSet {0:s} --nickName {1:s} --mode {2:s} --year {3:s} -t {4:s} -c {5:s} -s {6:s} -l {7:s}\n".format(dataset,nickname, mode,era, args.tag, str(conc), args.doSystematics, str(args.islocal)))
    #else :
        #outLines.append("python ../../sendJobs.py --dataSet {0:s} --nickName {1:s} --mode {2:s} --year {3:s} -c {5:s} -s {4:s} -j {6:s} -l {7:s} -d data\n".format(dataset,nickname, mode,era, args.tag, str(conc), args.doSystematics, str(args.islocal)))
    outLines.append("cd {0:s}\n".format(cwd))

fOut='jobs_{0:s}_{1:s}.csh'.format(str(args.year),args.tag)
open(fOut,'w').writelines(outLines)



    
    
