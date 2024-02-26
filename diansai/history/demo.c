#include "fdc2214.h"
#include "stdio.h"
#include "unistd.h"

int main()
{
	FDC2214_init();
	while(1)
	{
		uint32_t value = FDC2214_readCh0();
		printf("%d", value);
		usleep(200000);
	}

}
