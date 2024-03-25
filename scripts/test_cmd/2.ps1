# 清空info.txt文件，如果文件不存在则创建它
"" | Out-File -FilePath .\info.txt -Force -Encoding UTF8

# 收集并写入操作系统信息
"操作系统信息:" | Out-File -FilePath .\info.txt -Append -Encoding UTF8
Get-WmiObject -class Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, LastBootUpTime | Out-File -FilePath .\info.txt -Append -Encoding UTF8

# 收集并写入CPU信息
"`nCPU信息:" | Out-File -FilePath .\info.txt -Append -Encoding UTF8
Get-WmiObject -class Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors | Out-File -FilePath .\info.txt -Append -Encoding UTF8

# 收集并写入内存信息
"`n内存信息:" | Out-File -FilePath .\info.txt -Append -Encoding UTF8
Get-WmiObject -class Win32_PhysicalMemory | Select-Object BankLabel, Capacity, Speed | Out-File -FilePath .\info.txt -Append -Encoding UTF8

# 收集并写入磁盘信息
"`n磁盘信息:" | Out-File -FilePath .\info.txt -Append -Encoding UTF8
Get-WmiObject -class Win32_LogicalDisk -filter "DriveType=3" | Select-Object DeviceID, VolumeName, Size, FreeSpace | Out-File -FilePath .\info.txt -Append -Encoding UTF8

# 收集并写入网络适配器信息
"`n网络适配器信息:" | Out-File -FilePath .\info.txt -Append -Encoding UTF8
Get-WmiObject -class Win32_NetworkAdapterConfiguration -filter "IPEnabled=True" | Select-Object Description, IPAddress, MACAddress | Out-File -FilePath .\info.txt -Append -Encoding UTF8

# 打开info.txt文件
Invoke-Item .\info.txt
