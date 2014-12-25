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

class TestClass:
	@pytest.fixture(autouse=True)
	def init(self):
		self.proxy = proxy.Proxy(config.NAMESPACE + '_unknown_namespace', config.PROXY_HOST)

	def test_simple_upload(self):
		r = self.proxy.simple_upload('uniqkey_test_simple_upload', 'data')
		assert r.status_code == 404

	def test_simple_get(self):
		r = self.proxy.simple_get(123, 'test_simple_get')
		assert r.status_code == 404

	def test_delete(self):
		r = self.proxy.delete(123, 'test_delete')
		assert r.status_code == 404

	def test_statistics(self):
		r = self.proxy.statistics()
		assert r.status_code == 404

