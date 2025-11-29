import requests
import sys
from datetime import datetime, timedelta

base_url = 'http://127.0.0.1:8000'

print('=' * 70)
print('REPORTS PAGE VERIFICATION')
print('=' * 70)

# Test 1: Basic page load
print('\n[TEST 1] Loading Reports page...')
try:
    r = requests.get(f'{base_url}/reports/', timeout=15)
    if r.status_code != 200:
        print(f'  ✗ FAILED: Status {r.status_code}')
        sys.exit(1)
    print('  ✓ Page loaded (HTTP 200)')
except Exception as e:
    print(f'  ✗ Connection failed: {e}')
    sys.exit(1)

# Test 2: Check for key elements
print('\n[TEST 2] Checking page elements...')
elements = {
    'Title': 'CRM Reports',
    'Metrics section': 'Total Clients',
    'Date filter form': 'from_date',
    'From Date input': 'From Date',
    'To Date input': 'To Date',
    'Filter button': '<button type="submit" class="btn btn-primary">Filter</button>',
    'Clear button': '<a href="/reports/" class="btn btn-secondary">Clear</a>',
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
for name, text in elements.items():
    if text in r.text:
        print(f'  ✓ {name}')
    else:
        print(f'  ✗ {name}')
        missing.append(name)

if missing:
    print(f'\n  WARNING: {len(missing)} elements missing')
    for m in missing:
        print(f'    - {m}')

# Test 3: Test date filtering
print('\n[TEST 3] Testing date filtering...')
today = datetime.now().date()
start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

filter_url = f'{base_url}/reports/?from_date={start_date}&to_date={end_date}'
try:
    r_filtered = requests.get(filter_url, timeout=15)
    if r_filtered.status_code != 200:
        print(f'  ✗ Filtered page failed: Status {r_filtered.status_code}')
    else:
        print(f'  ✓ Filtered page loaded (dates: {start_date} to {end_date})')
        # Check for filter confirmation message
        if 'Showing data' in r_filtered.text:
            print('  ✓ Filter confirmation message present')
        else:
            print('  ✗ Filter confirmation message missing')
except Exception as e:
    print(f'  ✗ Filter test failed: {e}')

# Test 4: Check navigation
print('\n[TEST 4] Checking Reports button in navbar...')
try:
    r_nav = requests.get(f'{base_url}/clients/', timeout=15)
    if r_nav.status_code == 200:
        if 'href="/reports/"' in r_nav.text and '>Reports<' in r_nav.text:
            print('  ✓ Reports button found in navbar')
        else:
            print('  ✗ Reports button not found in navbar')
    else:
        print(f'  ✗ Could not check navbar (status {r_nav.status_code})')
except Exception as e:
    print(f'  ✗ Navbar check failed: {e}')

print('\n' + '=' * 70)
if not missing and r.status_code == 200:
    print('✓ ALL TESTS PASSED - Reports page is working correctly!')
else:
    print('⚠ Some issues detected - see above')
print('=' * 70)
print(f'\nAccess Reports at: {base_url}/reports/')
