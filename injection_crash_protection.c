/******************************************************************************
* File:         injection_crash_protection.c
* Author:       Martin Lemaire
* Date created: November 7, 2023
* Description:  Manages the good completion of capital injection.
*               Interacts with a csv file to keep track of the injection stages.
* 
* Modifications:
*   [v1.0.0 - 07.11.23 - INITIAL]
******************************************************************************/

/******************************************************************************
* COMPILING COMMAND :
* "gcc -std=c11 -Wall -Wextra -Werror -pedantic -Wshadow -Wformat=2 -Wfloat-equ
*  al -Wconversion -Wlong-long -Wshift-overflow -Wnull-dereference -O3 -g -o in
*  jection injection_crash_protection.c"
******************************************************************************/

// IMPORTS
#include "stdlib.h"
#include "stdio.h"
#include "unistd.h"
#include "string.h"

// ERROR CODES
#define kErr_file_error -1

int main(void){

    // Get path
    char injection_data_path[1024];
    getcwd(injection_data_path, sizeof(injection_data_path));
    strcat(injection_data_path, "/injection_data.csv");

    FILE *written_file = fopen(injection_data_path, "w");

    // ERROR Management File
    if (written_file == NULL){
        fprintf(stderr,"ERROR: cannot write file. Exiting...");
        exit(kErr_file_error);
    }

    fprintf(written_file, "0");
    fclose(written_file); // closing the open file

    int firstValue;
    FILE *read_file;

    // Infinite loop
    while(1){
        // The "system" function surpasses anything and offers optimal resilience
        read_file = fopen(injection_data_path, "r");

        // ERROR Management File
        if (read_file == NULL){
            fprintf(stderr,"ERROR: cannot read file. Exiting...");
            exit(kErr_file_error);
        }

        fscanf(read_file, "%d", &firstValue); // fetching data of the csv

        if (firstValue == -1) {
            // Composing the command
            char remove_command[1024];
            strcpy(remove_command,"rm ");
            strcat(remove_command,injection_data_path);
            system(remove_command); // remove the csv - useless memory
            fclose(read_file); // closing the open file
            return 0;
        }

        fclose(read_file); // closing the open file

        // Get path
        char injection_script_path[1024];
        getcwd(injection_script_path, sizeof(injection_script_path));
        strcat(injection_script_path, "/injection.py");

        // Composing the command
        char injection_command[1024];
        strcpy(injection_command,"python3 ");
        strcat(injection_command,injection_script_path);
        system(injection_command); // remove the csv - useless memory
    }
}
