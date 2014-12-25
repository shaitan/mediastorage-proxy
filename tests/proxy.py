# ===============================================================================
# Mediastorage-proxy is a HTTP proxy for mediastorage based on elliptics
# Copyright (C) 2013-2014 Yandex
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ===============================================================================

import requests

class Proxy:
	def __init__(self, namespace, host):
		self.namespace = namespace
		self.host = host

	def url(self, handler, filename = None, couple_id = None):
		res = self.host + '/' + handler
		if filename:
			res += '-' + self.namespace + '/'
			if couple_id:
				res += str(couple_id) + '/'
			res += filename
		return res

	def ping(self):
		return requests.get(self.url('ping'))

	def statistics(self):
		return requests.get(self.url('statistics-' + self.namespace))

	def cache_update(self):
		return requests.get(self.url('cache-update'))

	def simple_upload(self, filename, data):
		return requests.post(self.url('upload', filename), data=data)

	def simple_get(self, couple_id, filename):
		return requests.get(self.url('get', filename, couple_id))

	def delete(self, couple_id, filename):
		return requests.get(self.url('delete', filename, couple_id))

