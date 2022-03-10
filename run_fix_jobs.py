## Execute the fix job in OpenGuard by calling the API

import time
import urllib.request

openguard_job_api_url = 'http://192.168.56.1:8000/jobs/run'
check_for_jobs = True
## interval in seconds
check_interval = 10

while check_for_jobs:
  try:
    with urllib.request.urlopen(openguard_job_api_url) as f:
      print(f.read().decode('utf-8'))
    #print('hello')
    time.sleep(check_interval)
  except Exception as url_access_message:
    print(url_access_message)
  