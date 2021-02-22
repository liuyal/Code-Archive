
@echo "Turnning Wi-Fi Off"
netsh interface set interface "Wi-Fi" disabled

@timeout 5

@echo "Turnning Wi-Fi On"
netsh interface set interface "Wi-Fi" enabled

@timeout 10

@netsh interface show interface
@netsh interface ip show config "Wi-Fi"

@PAUSE