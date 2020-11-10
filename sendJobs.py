from __future__ import division
import os
import subprocess
from decimal import *
getcontext().prec = 2
def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    defDS = '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM '
    parser.add_argument("--dataSet",default=defDS,help="Data set name.") 
    parser.add_argument("--nickName",default='MCpileup',help="Data set nick name.") 
    parser.add_argument("-m","--mode",default='anaXRD',help="Mode (script to run).")
    parser.add_argument("-y","--year",default=2017,type=str,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-c","--concatenate",default=5,type=int,help="How many files to run on each job")
    parser.add_argument("-t","--tag",default='ZH',type=str,help="Select a tag for your jobs")
    parser.add_argument("-s","--doSystematics",default='yes',type=str,help="do JME systematics")
    parser.add_argument("-l","--islocal",default='no',type=str,help="get list from /eos/ not DAS")
    return parser.parse_args()


def getFileName(line) :
    tmp = line.split()[0].strip(',')
    fileName = tmp.strip()
    return fileName


scriptName = "out.py"
f = open("../../Files/crab_template.py", "r")
text = f.read()
#print text


args = getArgs()
era = str(args.year)
doJME  = args.doSystematics.lower() == 'true' or args.doSystematics.lower() == 'yes' or args.doSystematics == '1'

period="B"
if 'Run2016' in args.dataSet or 'Run2017' in args.dataSet or 'Run2018' in args.dataSet: 
    poss = args.dataSet.find("Run")
    period = args.dataSet[int(poss)+7:int(poss)+8]
    print 'will set up', poss, period


query = '"file dataset={0:s}"'.format(args.dataSet)
if "USER" in str(args.dataSet) : query = '"file dataset={0:s}"'.format(args.dataSet+" instance=prod/phys03")
command = "dasgoclient --query={0:s} --limit=0  > fileList.txt".format(query)

print("Running in {0:s} mode.  Command={1:s}".format(args.mode,command))
os.system(command)






files = open('fileList.txt','r').readlines()
if len(files) < 1 :
    print("***In makeCondor.py: Empty fileList.txt")
    exit()

scriptList = [] 
file=[]
dataset=[]

era = str(args.year)
mjobs=args.concatenate

for nFiles, file in enumerate(files) :
     
    fileName=getFileName(file)
    if str(args.islocal.lower())=='yes' : fileName = fileName.replace('/eos/uscms','')
    if '#' not in fileName :  dataset.append(fileName)

    #query = '"file={0:s} | grep file.nevents"'.format(fileName)
    #command = "dasgoclient --query={0:s}  > nevents.txt".format(query)

    query = '"file dataset={0:s} | grep file.nevents"'.format(args.dataSet)
    command = "dasgoclient --query={0:s}  > nevents.txt".format(query)
    #out = subprocess.check_output( os.system(command), shell=True)
    os.system(command)

Nevents=[]
nev =open('nevents.txt','r').readlines()
for i, j in enumerate(nev) : Nevents.append(int(j))

    #print 'for ', args.dataSet, 'we have', output


nevents=sum(Nevents)
#nevents=10
#print '-------------------', Nevents, dataset, nevents
print nevents
#mjobs = 5
#this will set each job to about 50k on average

average = int(len(Nevents))
mjobs=int(nevents/50000)
if mjobs > 5 : mjobs = 5
#mjobs=5
print 'how many files', average, mjobs

ff = open("../../Files/runjme.sh", "r")
textf = ff.read()


outLines=['#!/usr/local/bin/python \n']
outLines.append(text)
for i in range(0, mjobs) :

    outFile = '{0:s}_{1:s}_{2:s}of{3:s}.root'.format(str(args.nickName), era, str(i+1), str(mjobs) )

    outLines.append("    config.General.workArea = '../../Crab_projects_{0:s}_newJECs' \n".format(era) )
    outLines.append("    config.General.requestName = '{0:s}_{1:s}_part{2:s}' \n".format(args.nickName, era, str(i)))
    outLines.append("    config.Data.outLFNDirBase = '/store/group/lpcsusyhiggs/ntuples/nAODv7/JEC_{0:s}' \n".format(era))
    outLines.append("    config.Data.inputDataset = '{0:s}' \n".format(str(args.dataSet)))
    outLines.append("    config.Data.outputDatasetTag = '{0:s}_{1:s}' \n".format(args.nickName, era))
    outLines.append("    config.JobType.outputFiles = ['{0:s}'] \n".format(outFile))
    outLines.append("    config.JobType.scriptExe = '/uscms_data/d3/alkaloge/ntuples/CMSSW_10_6_4/src/newCrab/{0:s}/{1:s}_{2:s}/part_{3:s}of{4:s}.sh' \n".format(args.tag, args.nickName, era, str(i+1),str(mjobs)))
    #outLines.append("    config.JobType.scriptExe = '/uscms_data/d3/alkaloge/ntuples/CMSSW_10_6_4/src/test/test/{1:s}_{2:s}/part_{3:s}.sh' \n".format(args.tag, args.nickName, era, str(i)))
    
    outLines.append("    config.JobType.maxJobRuntimeMin = 3000 \n") 
    outLines.append("    config.Data.splitting= 'FileBased' \n") 
    outLines.append("    config.Data.unitsPerJob= 1 \n") 
    outLines.append("    config.Data.totalUnits= {0:s} \n".format(str(nevents)))

    #if 'Run2016' in str(args.dataSet) : outLines.append("    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt'")
    #if 'Run2017' in str(args.dataSet) : outLines.append("    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'")
    #if 'Run2018' in str(args.dataSet) : outLines.append("    config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions16/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt")
    outLines.append("    submit(config) \n")

    runName = "part_{0:s}of{1:s}.sh".format(str(i+1),str(mjobs))
    #runLines=['#!/usr/local/bin/python \n']
    runLines=[]
    runLines.append(textf)
    start= '%.2f' %(i/mjobs)
    finish = '%.2f' %((i+1)/mjobs)
    print start, finish
    if i== mjobs-1 : finish = 1.05

    runLines.append("sed -i "'"s/STARTEVENT/{0:s}/g"'" make_jmev2.py \n" .format(str(start)) )
    runLines.append("sed -i "'"s/FINISHEVENT/{0:s}/g"'" make_jmev2.py \n" .format(str(finish)) )
    runLines.append("echo will skim between {0:s} and {1:s} \n".format(str(start), str(finish)))
    if 'Run'  in str(args.nickName) or 'data' in str(args.nickName): 
        
        runLines.append("python make_jmev2.py False {0:s} {1:s} \n" .format( era, period ))
        
    else  : runLines.append("python make_jmev2.py True {0:s} B \n" .format(era) )
    runLines.append("cp inFile_Skim.root ../../{0:s} \n".format(outFile))
    runLines.append("python -c \"import PSet; print \'\\n\'.join(list(PSet.process.source.fileNames))\" " )
    open(runName,'w').writelines(runLines)




open(scriptName,'w').writelines(outLines)



#python -c "import PSet; print '\n'.join(list(PSet.process.source.fileNames))"


