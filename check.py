import os
import os.path
import sys
import subprocess
year=sys.argv[1]
inFile='eos_{0:s}'.format(str(sys.argv[1]))
inFilelocal ='local_{0:s}'.format(str(sys.argv[1]))


fileseos=[]
#first put in a list the files existing on eos

for line in open(inFile,'r').readlines() :
    dataset=line.strip()

    nickname = dataset.split('/')[13]
    
    nickname = nickname.replace('_JECs_1.root', '_JECs')
    nickname = nickname.replace('_JECs_2.root', '_JECs')
    nickname = nickname.replace('_JECs_3.root', '_JECs')
    nickname = nickname.replace('.py', '')

    fileseos.append(nickname)
    #if 'Single' in line : print '------------', line, 'nickname', nickname

#print fileseos

for line in open(inFilelocal,'r').readlines() :

    dataset=line.strip()

    nickname = dataset.split('/')[2]

    nickname = nickname.replace('_JECs_1.root', '_JECs')
    nickname = nickname.replace('_JECs_2.root', '_JECs')
    nickname = nickname.replace('_JECs_3.root', '_JECs')
    nickname = nickname.replace('.py', '')
    nickname = nickname.replace('crab_', '')

    #print nickname

    #cf=os.path.isfile('Crab_projects_{0:s}_JECs/crab_ntuples_{1:s}/crab.log'.format(str(year), str(nickname)))

    res = [i for i in fileseos if nickname in i] 
    #if str(nickname) not in fileseos : print  nickname, 'does not exist on eos'
    if len(res) == 0 and nickname != 'pset' : 

        base = nickname.strip()
        localfile = ("find ZH_JECs/*{1:s}* -type f -name '"'*{0:s}*submitted'"' ".format(str(nickname),str(year) ))
        output = subprocess.check_output(localfile, shell=True)
        if '2016B' in nickname : continue
        print  nickname, 'does not exist on eos for ', year,  output
        command=("rm {0:s}".format(output))
        print command
        #os.system(command)
        #command=("crab status -d Crab_projects_{0:s}_JECs/crab_ntuples_{1:s}".format(str(year), str(nickname)))
        command=("rm -fr  Crab_projects_{0:s}_JECs/crab_ntuples_{1:s}".format(str(year), str(nickname)))
        #os.system(command)


