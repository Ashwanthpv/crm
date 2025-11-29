import zipfile, sys
p='downloaded_crm_data.zip'
try:
    z=zipfile.ZipFile(p)
except Exception as e:
    print('ERROR opening zip', e)
    sys.exit(2)
names=z.namelist()
print('files:', names)
for name in names:
    print('\n---', name)
    try:
        data=z.read(name).decode('utf-8', errors='replace')
    except Exception as e:
        print('  (could not decode file)', e)
        continue
    lines=data.splitlines()
    for i,l in enumerate(lines[:10]):
        print(f'{i+1:2d}:', l)
    if len(lines) > 10:
        print('   ...', len(lines), 'lines total')
