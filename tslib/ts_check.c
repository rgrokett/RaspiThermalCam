/*
 *  ts_check.c
 *
 *  Derived from tslib/src/ts_test.c by Douglas Lowder
 *  Just prints touchscreen events -- does not paint them on framebuffer
 *
 * This file is placed under the GPL.  Please see the file
 * COPYING for more details.
 *
 * SPDX-License-Identifier: GPL-2.0+
 *
 *
 * Basic touch program for touchscreen library.
 * Returns X/Y or blank
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "tslib.h"


int main(void)
{
	struct tsdev *ts;

	ts = ts_setup(NULL, 1);
	if (!ts) {
		perror("ts_setup");
		exit(1);
	}

	int loop = 1;
	while (loop) {
		struct ts_sample samp;
		int ret;
		int cnt;

		if (cnt > 10) { loop = 0; }	

		ret = ts_read(ts, &samp, 1);

                //printf("ts_print: read returns %d\n", ret);


		if (ret < 0) {
			perror("ts_read");
			ts_close(ts);
			exit(1);
		}

		if (ret != 1){
			cnt++;
			usleep(1000);
			continue;
		}

		//printf("%ld.%06ld: %6d %6d %6d\n", samp.tv.tv_sec, samp.tv.tv_usec, samp.x, samp.y, samp.pressure);
		printf("%6d %6d\n", samp.x, samp.y);
		loop = 0;

	}

	ts_close(ts);
	return(0);
}
