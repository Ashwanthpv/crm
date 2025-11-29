import requests
url='http://127.0.0.1:8000/download-data/'
print('Requesting', url)
r=requests.get(url, timeout=10)
print('status', r.status_code)
print('content-type', r.headers.get('content-type'))
with open('downloaded_crm_data.zip','wb') as f:
    f.write(r.content)
print('Wrote downloaded_crm_data.zip, bytes=', len(r.content))
