import requests
import sys

base = 'http://127.0.0.1:8000'
print('Testing API create -> get -> delete against', base)
payload = {
    'name': 'API Test Client',
    'email': 'apitest@example.com',
    'phone': '123-456',
    'company': 'TestCo',
    'product': 'TestProd',
    'status': 'prospect',
    'description': 'Created by automated test',
    'assignee': 'QA',
    'next_step': 'Call next week'
}
try:
    r = requests.post(f"{base}/api/customers/", json=payload, timeout=10)
except Exception as e:
    print('ERROR: could not connect to server at', base, '->', e)
    sys.exit(2)
print('POST status', r.status_code)
if r.ok:
    try:
        c = r.json()
    except Exception:
        print('POST returned non-JSON:', r.text)
        sys.exit(3)
    cid = c.get('id')
    print('Created id', cid)
    r2 = requests.get(f"{base}/api/customers/", timeout=10)
    print('GET list status', r2.status_code, 'items', len(r2.json()) if r2.ok else 'N/A')
    # cleanup
    r3 = requests.delete(f"{base}/api/customers/{cid}/", timeout=10)
    print('DELETE status', r3.status_code)
    if r3.status_code in (200, 204):
        print('Cleanup successful')
    else:
        print('Cleanup may have failed, response:', r3.status_code, r3.text)
else:
    print('Create failed, response:', r.status_code, r.text)
    sys.exit(4)
