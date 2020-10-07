import os

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    defDS = '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM '
    parser.add_argument("--dataSet",default=defDS,help="Data set name.") 
    parser.add_argument("--nickName",default='MCpileup',help="Data set nick name.") 
    parser.add_argument("-m","--mode",default='anaXRD',help="Mode (script to run).")
    parser.add_argument("-y","--year",default=2017,type=str,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-c","--concatenate",default=1,type=int,help="On how many files to run on each job")
    parser.add_argument("-s","--selection",default='ZH',type=str,help="select ZH or AZH")
    parser.add_argument("-j","--doSystematics",default='yes',type=str,help="do JME systematics")
    parser.add_argument("-l","--islocal",default='no',type=str,help="get list from /eos/ not DAS")
    return parser.parse_args()


def getFileName(line) :
    tmp = line.split()[0].strip(',')
    fileName = tmp.strip()
    return fileName


scriptName = "out.py"
f = open("../../crab_template.py", "r")
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

events=1000

mjobs = 5


ff = open("../../runjme.sh", "r")
textf = ff.read()


outLines=['#!/usr/local/bin/python \n']
outLines.append(text)
for i in range(1, mjobs) :

    outFile = '{0:s}_{1:s}_{2:s}of{3:s}.root'.format(str(args.nickName), era, str(i), str(mjobs-1) )

    outLines.append("    config.General.requestName = '{0:s}_part{1:s}' \n".format(args.nickName, str(i)))
    outLines.append("    config.Data.outLFNDirBase = '/store/group/lpcsusyhiggs/ntuples/nAODv7/JEC_{0:s}' \n".format(era))
    outLines.append("    config.Data.inputDataset = '{0:s}' \n".format(str(args.dataSet)))
    outLines.append("    config.Data.outputDatasetTag = '{0:s}' \n".format(outFile))
    outLines.append("    config.Data.outputFiles = '{0:s}_{1:s}.root' \n".format(str(args.nickName), str(i)))
    outLines.append("    config.Data.scriptExe = '/uscms_data/d3/alkaloge/ntuples/CMSSW_10_6_4/src/test/{0:s}/{1:s}_{2:s}/part_{3:s}.sh' \n".format(args.selection, args.nickName, era, str(i)))
    outLines.append("    config.Data.maxJobRuntimeMin= 3000 \n") 
    outLines.append("    config.Data.splitting= 'FileBased' \n") 
    outLines.append("    config.Data.unitsPerJob= 1 \n") 
    outLines.append("    config.Data.totalUnits= {0:s} \n".format(str(events)))
    outLines.append("    submit(config) \n")

    runName = "part_{0:s}.sh".format(str(i))
    runLines=['#!/usr/local/bin/python \n']
    runLines.append(textf)
    start = i*0.2
    finish = (i+1) * 0.2
    if i== mjobs-1 : finish +=0.05
    runLines.append("sed -i "'"s/STARTEVENT/{0:s}/g"'" make_jmev2.py \n" .format(str(start)) )
    runLines.append("sed -i "'"s/FINISHEVENT/{0:s}/g"'" make_jmev2.py \n" .format(str(finish)) )
    runLines.append("python make_jmev2.py True 2016 B \n" .format(str(start)) )
    runLines.append("cp inFile_Skim.root ../../{0:s} \n".format(outFile))
    runLines.append("python -c \"import PSet; print \'\\n\'.join(list(PSet.process.source.fileNames))\" " )
    open(runName,'w').writelines(runLines)




open(scriptName,'w').writelines(outLines)



#python -c "import PSet; print '\n'.join(list(PSet.process.source.fileNames))"


