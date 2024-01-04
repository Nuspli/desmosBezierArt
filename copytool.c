#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
#include<string.h>

int write_to_clipboard(char *output) {

    size_t len = strlen(output) + 1;
    HGLOBAL hMem =  GlobalAlloc(GMEM_MOVEABLE, len);
    memcpy(GlobalLock(hMem), output, len);
    GlobalUnlock(hMem);
    OpenClipboard(0);
    EmptyClipboard();
    SetClipboardData(CF_TEXT, hMem);
    CloseClipboard();
}

int main(int argc, char *argv[]) {

    FILE *file = NULL;
    char *line = NULL, *copy = NULL;
    size_t len = 0;

    if (argc < 4) {
        printf("usage: %s <filename> <start> <end>\n\n", argv[0]);
        printf("       both <start> and <end> are 0 based inclusive indices for the line segments\n");
        printf("       ex. 0 1 copies the first two segments, 2 4 the next three\n");
        exit(1);
    }

    if ((file = fopen(argv[1], "r")) == NULL) {
        printf("Error opening file: %s!\n", argv[1]);
        exit(1);
    }

    long start = strtol(argv[2], NULL, 10);
    long end = strtol(argv[3], NULL, 10);


    int read, total = 0, seg = 0, cpidx = 0, i = 0;

    printf("reading line from file...\n");

    read = getline(&line, &len, file);

    if ((copy = calloc(read+1, sizeof(char))) == NULL) {
        printf("failed to allocate %d bytes for copy!\ntry a smaller file, or split it into smaller chunks...\n", read+1 * sizeof(char));
        exit(1);
    }

    for (; i < read - 2; i++) {

        if (line[i] == ',' && line[i+1] == '(' && line[i+2] == '(') {

            total++;
            if (total >= start && total <= end) seg++;
        }

        if (total >= start && total <= end && !(line[i] == ',' && cpidx == 0)) {

            copy[cpidx++] = line[i];

            if (i == read - 3) {
                copy[cpidx++] = ')';
                copy[cpidx++] = ')';
            }
        }
    }

    copy[cpidx] = 0;

    printf("start index: %ld\nend index: %ld\n\n", start, start + seg);
    printf("copied characters (%d/%d)\n", cpidx, read);
    printf("copied segments (%d/%d)\n\n", seg+1, total+1);

    write_to_clipboard(copy);
    fclose(file);

    printf("success!");

    return 0;
}