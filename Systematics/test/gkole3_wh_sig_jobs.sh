# NB this command is specific to the configuration at IC and is not gaurenteed elsewhere
# outdir="/vols/cms04/szenz"
queue="8nh"
#useAAA=1
version="5"
fggRunJobs.py --load gkole2_wh_sig_jobs.json -d wh_sig_jobs_v$version -x cmsRun workspaceStd_test2_gkole.py maxEvents=-1 -n 500 -q $queue -D -P --no-copy-proxy --no-use-tarball 
