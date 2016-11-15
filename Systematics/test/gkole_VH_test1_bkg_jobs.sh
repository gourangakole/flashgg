#!/bin/bash
# NB this command is specific to the configuration at IC and is not gaurenteed elsewhere
# outdir="/vols/cms04/szenz"
queue="8nh"
#useAAA=1
version="10"
fggRunJobs.py --load gkole_VH_test1_bkg_jobs.json -d VH_bkg_jobs_v$version -x cmsRun workspaceStd_10_10_2016_MET45.py maxEvents=-1 -n 500 -q $queue -D -P --no-copy-proxy --no-use-tarball targetLumi=12.9e+3 puTarget=5.05e+03,2.41e+05,7.83e+05,1.74e+06,2.37e+06,3.41e+06,6.12e+06,2.43e+07,6.78e+07,1.45e+08,2.57e+08,4.06e+08,5.63e+08,7.06e+08,8.41e+08,9.54e+08,1.03e+09,1.06e+09,1.06e+09,1.02e+09,9.47e+08,8.51e+08,7.41e+08,6.19e+08,4.93e+08,3.72e+08,2.67e+08,1.82e+08,1.18e+08,7.18e+07,4.13e+07,2.24e+07,1.15e+07,5.57e+06,2.56e+06,1.12e+06,4.7e+05,1.92e+05,7.78e+04,3.3e+04,1.61e+04,9.87e+03,7.67e+03,6.92e+03,6.66e+03,6.56e+03,6.49e+03,6.4e+03,6.28e+03,6.12e+03
