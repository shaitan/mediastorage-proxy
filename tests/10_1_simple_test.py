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

import pytest

import config
import mastermind
import proxy

ns_settings = {
		'groups-count' : 2,
		'success-copies' : 'any',
		}

class TestClass:
	@pytest.fixture(autouse=True)
	def init(self):
		self.mastermind = mastermind.Mastermind(config.NAMESPACE, config.MASTERMIND_HOST)
		self.proxy = proxy.Proxy(config.NAMESPACE, config.PROXY_HOST)

		self.mastermind.ns_setup(ns_settings)
		self.proxy.cache_update()

	def test_ping(self):
		r = self.proxy.ping()
		assert r.status_code == 200
		assert not r.text

	def simple_upload_small_file_impl(self, filename, data):
		r = self.proxy.simple_upload(filename, data)
		assert r.status_code == 200
		# TODO: check body
		return r

	def test_simple_upload_small_file(self):
		self.simple_upload_small_file_impl('test_simple_upload_small_file', 'data')

