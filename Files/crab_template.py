import CRABClient
from CRABClient.UserUtilities import config
from WMCore.Configuration import Configuration


config = config()
config.General.workArea = 'Crab_projects_JECs'
config.General.transferOutputs = True
config.General.transferLogs = True
config.JobType.psetName = 'pset.py'
config.JobType.inputFiles =[ '/uscms_data/d3/alkaloge/ntuples/CMSSW_10_6_4/src/test/Files/make_jmev2.py', '/uscms_data/d3/alkaloge/ntuples/CMSSW_10_6_4/src/test/Files/branchselection.py', '/uscms_data/d3/alkaloge/ntuples/CMSSW_10_6_4/src/test/Files/keep_and_drop.txt',  '/uscms_data/d3/alkaloge/ntuples/CMSSW_10_6_4/src/test/Files/pset.py', '/uscms_data/d3/alkaloge/ntuples/CMSSW_10_6_4/src/test/Files/FrameworkJobReport.xml']
#config.JobType.outputFiles = ['all_HWminus_002_4of10.root']
config.JobType.allowUndistributedCMSSW = True
config.Data.inputDBS = 'global'
config.Data.publication = False
config.Data.outLFNDirBase = '/store/group/lpcsusyhiggs/ntuples/nAODv7/'
config.section_('Site')
config.Site.storageSite = 'T3_US_FNALLPC'

#HWminus,Other,0.114,299799.0,159582.2,,/HWminusJ_HToWW_M125_13TeV_powheg_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM
# 26 HWplus,Other,0.180,299997.0,255007.3,,/HWplusJ_HToWW_M125_13TeV_powheg_pythia8/RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8-v1/NANOAODSIM


if __name__ == '__main__':

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException
    #from WMCore.Configuration import Configuration
    #from CRABClient.UserUtilities import config

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
    config.General.workArea = 'crab_projects_multiPub'

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

