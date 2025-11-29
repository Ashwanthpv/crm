import requests
import sys

url = 'http://127.0.0.1:8000/reports/'
print(f'Testing Reports page: {url}')
try:
    r = requests.get(url, timeout=15)
    print(f'HTTP Status: {r.status_code}')
    
    if r.status_code == 200:
        # Verify key elements
        checks = {
            'Page title': 'CRM Reports' in r.text,
            'Task chart': 'taskChart' in r.text,
            'Customer chart': 'customerChart' in r.text,
            'Deal chart': 'dealChart' in r.text,
            'Chart.js library': 'chart.js' in r.text,
            'Metrics cards': 'Total Clients' in r.text,
            'Recent tables': 'Recent Clients' in r.text,
        }
        
        print('\nElement checks:')
        for name, present in checks.items():
            status = '✓' if present else '✗'
            print(f'  {status} {name}')
        
        if all(checks.values()):
            print('\n✓ SUCCESS: Reports page is working correctly!')
        else:
            print('\n⚠ Some elements missing')
    else:
        print(f'ERROR: Status {r.status_code}')
        if r.status_code == 404:
            print('Page not found - route may not be registered')
        print(f'Response: {r.text[:300]}')
        sys.exit(1)
        
except ConnectionRefusedError:
    print('ERROR: Server not running on port 8000')
    sys.exit(2)
except Exception as e:
    print(f'ERROR: {e}')
    sys.exit(1)
