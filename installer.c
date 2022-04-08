#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>


int main() {
    //
    system("git clone https://github.com/DiscoveryFox/Charlie-s-Fourth-Angel.git");
    system("cd Charlie-s-Fourth-Angel/");
    //open the app.cfg file and read the content
    FILE *file = fopen("app.cfg", "r");
    char line[1024];
    // get the current directory and save it in a variable
    char *current_dir = getcwd(NULL, 0);
    // append /Charlie-s-Fourth-Angel to the current directory
    char *install_dir = malloc(strlen(current_dir) + strlen("/Charlie-s-Fourth-Angel") + 1);
    // search in the content of the file for the word "ServicesPath"
    while (fgets(line, sizeof(line), file)) {
        if (strstr(line, "ServicesPath")) {
            // if found, replace the word with the install dir 
            strcpy(line, "ServicesPath=");
            strcat(line, install_dir);
            strcat(line, "\n");
            // write the new line to the file
            fputs(line, file);
        }
    }

    const int SIZE = 5;
    int apps_to_install[SIZE];
    apps_to_install[0] = "app.py";
    apps_to_install[1] = "get_ip.sh";
    apps_to_install[2] = "startcam.sh";
    apps_to_install[3] = "start.py";
    apps_to_install[4] = "tool_installer.py";
    // make executables from apps_to_install
    // loop through apps_to_install and make them executable
    for (int i = 0; i < SIZE; i++) {
        system("chmod +x " + apps_to_install[i]);
    }
    // install all requirements through pip
    system("apt-get install -y python3-pip");
    system("pip3 install -r requirements.txt");
}
