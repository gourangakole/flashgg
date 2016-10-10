# NB this command is specific to the configuration at IC and is not gaurenteed elsewhere
# outdir="/vols/cms04/szenz"
queue="8nh"
process="wh"
#useAAA=1
version="3"
fggRunJobs.py --load gkole3_wh_sig_test_jobs.json -d wh_sig_test_jobs_v$version -x cmsRun workspaceStd_test3_gkole.py maxEvents=-1 -n 500 -q $queue -D -P --no-copy-proxy --no-use-tarball processId=$process
