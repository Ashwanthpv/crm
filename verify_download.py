import requests
import zipfile
import sys

print('Testing /download-data/ endpoint...')
url = 'http://127.0.0.1:8000/download-data/'
try:
    r = requests.get(url, timeout=10)
    print(f'Status: {r.status_code}')
    print(f'Content-Type: {r.headers.get("content-type")}')
    
    if r.status_code == 200:
        with open('test_download.zip', 'wb') as f:
            f.write(r.content)
        print(f'Downloaded {len(r.content)} bytes')
        
        # Inspect ZIP
        try:
            z = zipfile.ZipFile('test_download.zip')
            files = z.namelist()
            print(f'ZIP contains: {files}')
            
            # Show first few lines of each CSV
            for fname in files:
                data = z.read(fname).decode('utf-8', errors='replace')
                lines = data.splitlines()
                print(f'\n--- {fname} ({len(lines)} lines) ---')
                for i, line in enumerate(lines[:3]):
                    print(f'  {line}')
        except Exception as e:
            print(f'Error inspecting ZIP: {e}')
    else:
        print(f'Error: {r.text[:200]}')
except Exception as e:
    print(f'Connection error: {e}')
    sys.exit(1)
