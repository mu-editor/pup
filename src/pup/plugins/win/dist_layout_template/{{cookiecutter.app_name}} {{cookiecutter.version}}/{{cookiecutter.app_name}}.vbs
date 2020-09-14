Set objShell = CreateObject("WScript.Shell")
objShell.Run("python\pythonw.exe -m {{cookiecutter.launch_module}}")
Set objShell = Nothing