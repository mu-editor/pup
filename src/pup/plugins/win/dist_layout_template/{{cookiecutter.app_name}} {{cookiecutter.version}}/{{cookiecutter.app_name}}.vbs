Set objShell = CreateObject("WScript.Shell")

thisFilePath = Replace(WScript.ScriptFullName, WScript.ScriptName, "")
commandToRun = """" & thisFilePath & "Python\pythonw.exe"" {{cookiecutter.launch_pyflags}} -m {{cookiecutter.launch_module}}"

objShell.Run(commandToRun)
