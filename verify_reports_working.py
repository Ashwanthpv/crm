#!/usr/bin/env python3
import requests
import sys

base_url = 'http://127.0.0.1:8000'

print('=' * 60)
print('TESTING REPORTS BUTTON AND PAGE')
print('=' * 60)

# Test 1: Check navbar has Reports button
print('\n[TEST 1] Checking navbar for Reports button...')
try:
    r = requests.get(f'{base_url}/clients/', timeout=10)
    if r.status_code == 200:
        if '/reports/' in r.text and 'Reports' in r.text:
            print('  ✓ Reports button found in navbar')
        else:
            print('  ✗ Reports button NOT found in navbar')
            sys.exit(1)
    else:
        print(f'  ✗ Failed to fetch /clients/ (status {r.status_code})')
        sys.exit(1)
except Exception as e:
    print(f'  ✗ Connection error: {e}')
    sys.exit(1)

# Test 2: Check Reports page loads
print('\n[TEST 2] Testing /reports/ endpoint...')
try:
    r = requests.get(f'{base_url}/reports/', timeout=10)
    if r.status_code != 200:
        print(f'  ✗ Page returned status {r.status_code}')
        sys.exit(1)
    print(f'  ✓ Reports page returned 200 OK')
except Exception as e:
    print(f'  ✗ Connection error: {e}')
    sys.exit(1)

# Test 3: Verify key elements in Reports page
print('\n[TEST 3] Verifying Reports page content...')
required_elements = {
    'Title': 'CRM Reports',
    'Metrics section': 'Total Clients',
    'Task chart': 'taskChart',
    'Customer chart': 'customerChart',
    'Deal chart': 'dealChart',
    'Chart.js library': 'chart.js',
    'Recent Clients table': 'Recent Clients',
    'Recent Tasks table': 'Recent Tasks',
    'Recent Deals table': 'Recent Deals',
    'Top Products table': 'Top Products',
}

missing = []
for name, text in required_elements.items():
    if text in r.text:
        print(f'  ✓ {name}')
    else:
        print(f'  ✗ {name} MISSING')
        missing.append(name)

if missing:
    print(f'\n✗ FAILED: {len(missing)} elements missing')
    sys.exit(1)

print('\n' + '=' * 60)
print('✓ ALL TESTS PASSED!')
print('=' * 60)
print('\nReports button and page are working correctly.')
print(f'Access it at: {base_url}/reports/')
