Set oShell = CreateObject("Wscript.Shell")
Dim strArgs
Dim requirementsFile
Dim msg


msg = "Installing necessary modules.. It takes sometime to open the app. Make sure You've connected to Internet. "
MsgBox msg, 0, "Alert"

requirementsFile = "requirements.txt"

strArgs = "pip install -r " & requirementsFile
oShell.Run strArgs, 0, True


strArgs = "cmd /c pythonw window.py"
oShell.Run strArgs, 0, False