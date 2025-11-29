import requests
import time

time.sleep(2)  # Give server time to start

base = 'http://127.0.0.1:8000'
print('Testing CRM application endpoints...\n')

tests = [
    ('Landing page', '/'),
    ('Clients page', '/clients/'),
    ('Tasks page', '/tasks/'),
    ('Deals page', '/deals/'),
    ('Products page', '/products/'),
    ('Reports page', '/reports/'),
    ('API: Customers', '/api/customers/'),
    ('API: Tasks', '/api/tasks/'),
    ('API: Deals', '/api/deals/'),
    ('API: Products', '/api/products/'),
    ('Download data', '/download-data/'),
]

passed = 0
failed = 0

for name, url in tests:
    try:
        r = requests.get(base + url, timeout=10)
        if r.status_code == 200:
            print(f'✓ {name:20} {r.status_code}')
            passed += 1
        else:
            print(f'✗ {name:20} {r.status_code}')
            failed += 1
    except Exception as e:
        print(f'✗ {name:20} ERROR: {str(e)[:40]}')
        failed += 1

print(f'\n{"="*50}')
print(f'Results: {passed} passed, {failed} failed')
print(f'{"="*50}')

if failed == 0:
    print('\n✓ ALL ENDPOINTS WORKING!')
else:
    print(f'\n⚠ {failed} endpoint(s) failed')
