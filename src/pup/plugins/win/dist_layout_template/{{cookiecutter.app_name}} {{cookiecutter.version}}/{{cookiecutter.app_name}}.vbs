Set objShell = CreateObject("WScript.Shell")
objShell.Run("Python\pythonw.exe -m {{cookiecutter.launch_module}}")
Set objShell = Nothing