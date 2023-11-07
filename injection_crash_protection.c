// IMPORTS
#include "stdlib.h"
#include "stdio.h"


int main(void){
    // INFINITE LOOP
    FILE *first_file = fopen("injection_data.csv", "w");
    fprintf(first_file, "0");
    fclose(first_file);
    int firstValue;
    while(1>0){
        // The "system" function surpasses anything and offers optimal resilience
        FILE *second_file = fopen("injection_data.csv", "r");
        fscanf(second_file, "%d", &firstValue);
        if (firstValue == -1) {
            printf("Injection complete. Exiting...\n");
            system("rm injection_data.csv");
            fclose(second_file);
            return 0;
        }
        fclose(second_file);
        system("python3 injection.py");
    }
}