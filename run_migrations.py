import subprocess
import sys
import os

os.chdir('D:\\cuf')

print('=' * 60)
print('RUNNING MIGRATIONS')
print('=' * 60)

# Step 1: makemigrations
print('\n[STEP 1] Running makemigrations...')
result = subprocess.run(
    ['.venv\\Scripts\\python.exe', 'manage.py', 'makemigrations'],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr)
if result.returncode != 0:
    print(f'ERROR: makemigrations failed with code {result.returncode}')
    sys.exit(1)

# Step 2: migrate
print('\n[STEP 2] Running migrate...')
result = subprocess.run(
    ['.venv\\Scripts\\python.exe', 'manage.py', 'migrate'],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.stderr:
    print('STDERR:', result.stderr)
if result.returncode != 0:
    print(f'ERROR: migrate failed with code {result.returncode}')
    sys.exit(1)

print('\n' + '=' * 60)
print('✓ MIGRATIONS COMPLETED SUCCESSFULLY')
print('=' * 60)
