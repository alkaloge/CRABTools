Some CRAB tools to run the JME nAODTools to get systeamatics

python prepapereJobs.py -y year -t tag -s dosystematics -l islocal -t tag -j JobsPerFile

once the .csh is created, you can  execute it and it will submit crab jobs.

Edit Files/keep_and_drop.txt to add/remove branches that you don't need

Edit Files/crab_template.py to change the output path and the relative path for the jobs/templates

