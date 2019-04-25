#include "MO445.h"
#include <stdio.h>
#include <string.h>

const int LIMIT = 1400;

char* paths[1400];
char* names[1400];
int max_len = 50;
void chomp(char *s){
	s[strcspn(s, "\n")] = '\0';
}

void read_dataset_data(){
	FILE *fp;
	char *line = NULL;
	size_t len = 255;
	line = malloc(sizeof(char) * max_len);

	fp = fopen("paths.txt", "r");

	int ind = 0;
	while ((fgets(line, len, fp)) != NULL)
	{
		paths[ind] = malloc(sizeof(char) * max_len);
		chomp(line);
		strcpy(paths[ind], line);
		//printf("%s\n", paths[ind]);
		ind += 1;
	}

	fp = fopen("names.txt", "r");

	ind = 0;
	while ((fgets(line, len, fp)) != NULL)
	{
		names[ind] = malloc(sizeof(char) * max_len);
		chomp(line);
		strcpy(names[ind], line);
		//printf("%s\n", names[ind]);
		ind += 1;
	}
	free(line);
}

int main(int argc,char **argv){

	read_dataset_data();
	printf("Loaded data for files\n");

	for (int i = 0; i < LIMIT; i++){
		printf("%s --- >  %s\n", names[i], paths[i]);

		Image *img = NULL;
		FeatureVector1D *fvMS = NULL, *fvSS = NULL;
		char *outfile_name = NULL;
		outfile_name = malloc(sizeof(char) * 3 * max_len);

		img = ReadImage(paths[i]);
		fvMS = MS_ExtractionAlgorithm(img);
		strcpy(outfile_name,"mpeg7_features/");
		strcat(outfile_name, names[i]);
		strcat(outfile_name, "_MS.txt");
		WriteFeatureVector1D(fvMS, outfile_name);
		printf("termino feature 1 %s\n", outfile_name);

		fvSS = SS_ExtractionAlgorithm(img);
		strcpy(outfile_name, "mpeg7_features/");
		strcat(outfile_name, names[i]);
		strcat(outfile_name, "_SS.txt");
		WriteFeatureVector1D(fvSS, outfile_name);
		printf("termino feature 2 %s\n", outfile_name);

		DestroyFeatureVector1D(&fvSS);
		DestroyFeatureVector1D(&fvMS);
		DestroyImage(&img);
	}
	fprintf(stderr,"\n");

	return 0;
}
