/*
	Mediastorage-proxy is a HTTP proxy for mediastorage based on elliptics
	Copyright (C) 2013-2015 Yandex

	This program is free software; you can redistribute it and/or
	modify it under the terms of the GNU General Public License
	as published by the Free Software Foundation; either version 2
	of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/

#ifndef SRC__HANDYSTATS_HPP
#define SRC__HANDYSTATS_HPP

#include <cstdio>
#include <string>

#include <handystats/measuring_points.hpp>
#include <handystats/module.h>

#ifndef _HAVE_HANDY_MODULE_MDS
	#define _HAVE_HANDY_MODULE_MDS 1
#endif

HANDY_MODULE(MDS)


// mds.REQUEST (counter)
//    - total number of requests
//    - request rate
// mds.REQUEST.time (timer)
//    - total time spent on processing of successful (2xx) request
//    - quantiles (25%, 50%, 75%, 90%, 95%)
// mds.REQUEST.reply.CODE (counter)
//    - total number of response codes (e.g., 404) and groups (e.g., 2xx) for request
//    - response code rate for request
// mds.REQUEST.reply.time (timer)
//    - time spent between request and successful (2xx) response code reply
//    - quantiles (25%, 50%, 75%, 90%, 95%)


namespace elliptics {

// REQUEST

inline void MDS_REQUEST_START(const std::string& method, const uint64_t& instance_id) {
	char metric_name[256];

	sprintf(metric_name, "mds.%s", method.c_str());
	MDS_COUNTER_INCREMENT(metric_name);

	sprintf(metric_name, "mds.%s.time", method.c_str());
	MDS_TIMER_START(metric_name, instance_id);

	sprintf(metric_name, "mds.%s.reply.time", method.c_str());
	MDS_TIMER_START(metric_name, instance_id);
}

inline void MDS_REQUEST_STOP(const std::string& method, const uint64_t& instance_id) {
	char metric_name[256];

	sprintf(metric_name, "mds.%s.time", method.c_str());
	MDS_TIMER_STOP(metric_name, instance_id);
}

inline void MDS_REQUEST_DISCARD(const std::string& method, const uint64_t& instance_id) {
	char metric_name[256];

	sprintf(metric_name, "mds.%s.time", method.c_str());
	MDS_TIMER_DISCARD(metric_name, instance_id);
}


// REPLY

inline void MDS_REQUEST_REPLY(const std::string& method, const int& code, const uint64_t& instance_id) {
	char metric_name[256];

	sprintf(metric_name, "mds.%s.reply.%d", method.c_str(), code);
	MDS_COUNTER_INCREMENT(metric_name);

	sprintf(metric_name, "mds.%s.reply.%dxx", method.c_str(), code / 100);
	MDS_COUNTER_INCREMENT(metric_name);

	if (code / 100 != 2) {
		sprintf(metric_name, "mds.%s.time", method.c_str());
		MDS_TIMER_DISCARD(metric_name, instance_id);

		sprintf(metric_name, "mds.%s.reply.time", method.c_str());
		MDS_TIMER_DISCARD(metric_name, instance_id);
	}
	else {
		sprintf(metric_name, "mds.%s.reply.time", method.c_str());
		MDS_TIMER_STOP(metric_name, instance_id);
	}
}

} // namespace elliptics

#endif // SRC__HANDYSTATS_HPP
