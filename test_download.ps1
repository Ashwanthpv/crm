$url = 'http://127.0.0.1:8000/download-data/'
$output = 'D:\cuf\crm_download.zip'

Write-Host "Downloading from $url"
try {
    Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing -ErrorAction Stop
    $size = (Get-Item $output).Length
    Write-Host "SUCCESS: Downloaded $size bytes to $output"
    
    # Try to open as ZIP
    Add-Type -AssemblyName System.IO.Compression
    $zip = [System.IO.Compression.ZipFile]::OpenRead($output)
    Write-Host "ZIP contains $(($zip.Entries | Measure-Object).Count) files:"
    foreach ($entry in $zip.Entries) {
        Write-Host "  - $($entry.Name) ($($entry.Length) bytes)"
    }
    $zip.Dispose()
} catch {
    Write-Host "ERROR: $_"
}
