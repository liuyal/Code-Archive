@echo [0] SET STATIC
@echo [1] SET DHCP

@set /p id=Enter: 

@IF %id% == 0 (
	netsh interface ip set address "Wi-Fi" static 192.168.1.200 255.255.255.0 192.168.1.254
) ELSE (
	netsh interface ip set address "Wi-Fi" dhcp
)

@netsh interface ip show config "Wi-Fi"

@PAUSE