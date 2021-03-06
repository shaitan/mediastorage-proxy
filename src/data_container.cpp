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

#include "data_container.hpp"

namespace elliptics {
ioremap::elliptics::data_pointer data_container_t::pack(const data_container_t &ds) {
	ioremap::elliptics::data_buffer data;

	if (!ds.embeds.empty()) {
		for (auto it = ds.embeds.begin(); it != ds.embeds.end(); ++it) {
			data.write(bswap(it->second.header));
			data.write((const char *)it->second.data_pointer.data(), it->second.data_pointer.size());
		}
		embed_t::header_t h;
		h.size = ds.data.size();
		h.type = DNET_FCGI_EMBED_DATA;
		h.flags = 0;
		data.write(bswap(h));
	}

	data.write((const char *)ds.data.data(), ds.data.size());
	return std::move(data);
}

data_container_t data_container_t::unpack(ioremap::elliptics::data_pointer data_pointer, bool embeded) {
	elliptics::data_container_t ds;

	if (embeded) {
		embed_t::header_t h;

		h = bswap(*data_pointer.data<embed_t::header_t>());
		data_pointer = data_pointer.skip<embed_t::header_t>();

		while (h.type != DNET_FCGI_EMBED_DATA) {
			embed_t e;
			e.header = h;
			e.data_pointer = data_pointer.slice(0, e.header.size);
			data_pointer = data_pointer.skip(e.header.size);
			ds.embeds.insert(std::make_pair(e.header.type, e));

			h = bswap(*data_pointer.data<embed_t::header_t>());
			data_pointer = data_pointer.skip<embed_t::header_t>();
		}
	}

	ds.data = data_pointer;
	return ds;
}

data_container_t::embed_t::header_t data_container_t::bswap(const data_container_t::embed_t::header_t &header) {
	embed_t::header_t res;
	res.size = dnet_bswap64(header.size);
	res.flags = dnet_bswap32(header.flags);
	res.type = dnet_bswap32(header.type);
	return res;
}

} // namespace elliptics
