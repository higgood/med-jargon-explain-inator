executable = run_pipeline.sh
getenv = True
error = condor_logs/pipeline.error
log = condor_logs/pipeline.log
notification = always
transfer_executable = false
request_memory = 8*1024
request_GPUs = 1
+Research = True
Queue