# Create Code Signing Certificate
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=AtoZ Scrapy Publisher, O=AtoZ Scrapy, C=US" -CertStoreLocation "Cert:\CurrentUser\My"

# Export and import to Trusted Root Certification Authorities so Windows trusts it locally
$store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", "CurrentUser")
$store.Open("ReadWrite")
$store.Add($cert)
$store.Close()

# Sign the EXE file
Set-AuthenticodeSignature -FilePath "C:\Users\saghi\Downloads\AtoZ-Scrapy-Windows-11-ED.exe" -Certificate $cert
Set-AuthenticodeSignature -FilePath "C:\Users\saghi\Downloads\Scrapy\dist\AtoZ-Scrapy-Windows-11-ED.exe" -Certificate $cert

# Unblock file attribute
Unblock-File -Path "C:\Users\saghi\Downloads\AtoZ-Scrapy-Windows-11-ED.exe"
Unblock-File -Path "C:\Users\saghi\Downloads\Scrapy\dist\AtoZ-Scrapy-Windows-11-ED.exe"

Write-Host "✅ Successfully signed and unblocked AtoZ-Scrapy-Windows-11-ED.exe!"
