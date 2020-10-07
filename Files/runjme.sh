#!/bin/sh
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc820
workdir=`pwd`
cmsrel CMSSW_10_6_4
cd CMSSW_10_6_4/src
eval `scramv1 runtime -sh`
cmsenv
cp ${workdir}/* .
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
cp branchselection.py PhysicsTools/NanoAODTools/python/postprocessing/framework/.
cp keep_and_drop.txt PhysicsTools/NanoAODTools/python/postprocessing/framework/.
cd PhysicsTools/NanoAODTools
scram b -j 4
cd ${workdir}/CMSSW_10_6_4/src/
echo this is the working dir ${workdir}
#xrdcp root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAODv7/HWminusJ_HToWW_M125_13TeV_powheg_pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/70000/524598A2-DBA7-144A-B1F2-C9631FB13C74.root inFile.root
echo FILE FROM INPUTTTTTTTTTTTTTTTTTT

echo LOCAL LISTTTT
ls -ltrh

tar -xzvf input_files.tar.gz


file=`cat job_input_file_list_${CRAB_Id}.txt  | awk -F "[" '{print $2}' | awk -F "]" '{print $1}' | cut -d '"' -f2`

echo WORKDIR  LISTTTT

ls ../../ -ltrh


echo THE WINNER IS $file 
xrdcp root://cms-xrd-global.cern.ch/$file inFile.root


