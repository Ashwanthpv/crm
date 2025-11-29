import requests
import sys

url = 'http://127.0.0.1:8000/reports/'
print(f'Testing {url}...')
try:
    r = requests.get(url, timeout=10)
    print(f'Status: {r.status_code}')
    if r.status_code == 200:
        # Check for key elements
        checks = {
            'CRM Reports': 'CRM Reports' in r.text,
            'taskChart': 'taskChart' in r.text,
            'customerChart': 'customerChart' in r.text,
            'dealChart': 'dealChart' in r.text,
            'Total Clients': 'Total Clients' in r.text,
        }
        for key, present in checks.items():
            print(f'  {key}: {"✓" if present else "✗"}')
        if all(checks.values()):
            print('SUCCESS: Reports page loaded correctly!')
        else:
            print('WARNING: Some elements missing')
    else:
        print(f'Error: {r.status_code}')
        print(r.text[:300])
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
