Set objShell = CreateObject("WScript.Shell")

thisFilePath = Replace(WScript.ScriptFullName, WScript.ScriptName, "")
commandToRun = """" & thisFilePath & "Python\pythonw.exe"" -m {{cookiecutter.launch_module}}"

objShell.Run(commandToRun)
