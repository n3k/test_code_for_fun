// FunRLE.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

/*
XXXXXXXXXXXX       XXXXXXXXXXXX    XXX    XXXX
XXX      XXXXX     XX       XXX    XXX   XXXX
XXX        XXXX    XX       XXX    XXX  XXXX
XXX         XXX    XX     XXXXX    XXX XXXX
XXX         XXX    XX   XXXXXXX    XXXXXX
XXX         XXX    XXXXXXXXXXXX    XXXXXXX
XXX         XXX    XXX             XXX  XXXX
XXX         XXX    XXX             XXX   XXXX
XXX         XXX    XXX             XXX    XXXX
XXX         XXX    XXX       XX    XXX     XXXX
XXX         XXX    XXXXXXXXXXXX    XXX      XXXX
*/

int main() {
	int a, b, c;
	c = 10;
	for (b = 5;
		a = "D0 u kn0w how 1t Works?????!!\
LGLDCDDCCFEEBGCDCCDDCHDDBGCDCBDE\
CICDBEEDCADFCICDBCGDFHCICDLDGG\
CICDCMCBDECICDCMCCDDCICDCMCDDC\
CICDCGBDCEDBCICDLDCFDA"[b++ + 24]; )
		for (; a-- > 64; )
			putchar(++c == 59 ? c = c - 49 : b & 1 ? 32 : 88);
	
	getchar();	
	return 0;
}
