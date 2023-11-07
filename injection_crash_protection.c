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
* "gcc -std=c11 -Wall -Wextra -Werror -pedantic -Wshadow -Wformat=2 -Wfloat-equal -Wconversion -Wlong-long -Wshift-overflow -Wnull-dereference -O3 -g -o injection injection_crash_protection.c"
******************************************************************************/

// IMPORTS
#include "stdlib.h"
#include "stdio.h"

// ERROR CODES
#define kErr_file_error -1

int main(void){

    FILE *written_file = fopen("injection_data.csv", "w");

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
        read_file = fopen("injection_data.csv", "r");

        // ERROR Management File
        if (read_file == NULL){
            fprintf(stderr,"ERROR: cannot read file. Exiting...");
            exit(kErr_file_error);
        }

        fscanf(read_file, "%d", &firstValue); // fetching data of the csv

        if (firstValue == -1) {
            system("rm injection_data.csv"); // remove the csv - useless memory
            fclose(read_file); // closing the open file
            return 0;
        }

        fclose(read_file); // closing the open file
        system("python3 injection.py");
    }
}
