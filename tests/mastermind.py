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

import subprocess
from ast import literal_eval as make_tuple

ns_settings_example = {
		'groups-count' : 2,
		'success-copies' : 'all',
		'auth-key-write' : '',
		'auth-key-read' : '',
		'sign-token' : '123',
		'sign-path-prefix' : '/srv/storage/',
		'redirect-content-length-threshold' : 2,
		'redirect-expire-time' : 60,
		'multipart-content-length-threshold' : -1,
		'select-couple-to-upload' : 'true'
		}

class Mastermind:
	def __init__(self, namespace, host):
		self.namespace = namespace
		self.host = host

	def run_command(self, command):
		command.append('--host=' + self.host)
		p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		output, _ = p.communicate()
		return output

	def ns_setup(self, ns_settings):
		command = ['mastermind', 'ns', 'setup', '--overwrite', self.namespace]

		for k in ns_settings.keys():
			command.append('--' + k + '=' + str(ns_settings[k]))

		self.run_command(command)

	def couple_build(self, couples_info):
		command = ['mastermind', 'couple', 'build', '--state=coupled'
			, '--namespace=' + self.namespace
			, '--couples=' + str(couples_info['count'])
			, str(couples_info['size'])
			, '--dry-run']

		output = self.run_command(command)

		couples = []
		for c in  output.split('\n')[1:-1]:
			couples.append(sorted(make_tuple(c)))
		return couples

	def couple_list(self, state = 'all'):
		command = ['mastermind', 'couple', 'list', '--namespace=' + self.namespace
				, '--short']

		if state != 'all':
			command.append('--state=' + state)

		output = self.run_command(command)

		return make_tuple(output)

