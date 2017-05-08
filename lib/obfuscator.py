# Copyright (c) 2017, Jeff McCutchan [jamcut]
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import random
import string

class Obfuscator(object):
	"""Class for accessing launcher obfuscation functions"""

	def pattern_obfuscate(self, launcher, pattern):
		"""This function will obfuscate launcher but injecting one
		instance of pattern before every character"""
		x = []
		launcher_chars = list(launcher)
		for char in launcher_chars:
			c = pattern + char
			x.append(c)
		return ''.join(x)

	def generate_pattern(self):
		"""This function generates an ascii_lowercase pattern of at least 4 characters"""
		pattern_length = int(random.choice(range(4,11)))
		chars = string.ascii_lowercase
		return ''.join(random.SystemRandom().choice(chars) for _ in range(pattern_length + 1))