#include <libgen.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>

#include <mach-o/dyld.h>


#define PATH_BUFFER_SIZE 4096


int main() {

    char * nice_name = "{{cookiecutter.nice_name}}";

    char launcher_path[PATH_BUFFER_SIZE];
    char launcher_dir[PATH_BUFFER_SIZE];
    char python_path[PATH_BUFFER_SIZE];
    char tcl_lib_path[PATH_BUFFER_SIZE];
    char tcl_lib_env[PATH_BUFFER_SIZE];
    uint32_t size = PATH_BUFFER_SIZE;

    if ( _NSGetExecutablePath(launcher_path, &size) != 0 ) {
        fprintf(stderr, "_NSGetExecutablePath failed: need %u bytes buffer.\n", size);
    }
    strncpy(launcher_dir, dirname(launcher_path), PATH_BUFFER_SIZE);
    int i = strlen(launcher_dir)-1;
    if ( launcher_dir[i] == '/' ) {
        launcher_dir[i] = 0;
    }

    snprintf(tcl_lib_path, PATH_BUFFER_SIZE, "%s/../Resources/Python/lib/tcl8.6", launcher_dir);
    snprintf(tcl_lib_env, PATH_BUFFER_SIZE, "TCL_LIBRARY=%s", tcl_lib_path);
    putenv(tcl_lib_env);

    snprintf(python_path, PATH_BUFFER_SIZE, "%s/../Resources/Python/bin/%s", launcher_dir, nice_name);
    char * args[] = {nice_name, "-m" , "{{cookiecutter.launch_module}}"};
    if ( execv(python_path, args) ) {
        fprintf(stderr, "execv(\"%s\") failed: %s.\n", python_path, strerror(errno));
    }

    return 0;
}
