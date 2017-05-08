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

import sys

try:
	from jinja2 import Environment, FileSystemLoader
except ImportError:
	print('[-] Could not import a required library.  Please run "pip install -r requirements.txt"')
	sys.exit(1)

class Delivery(object):
	"""Class for accessing launcher delivery mechanisms"""

	def chunks(self, l, n): # shamelessly ganked from Empire
	    """Generator to split a string l into chunks of size n."""
	    for i in range(0, len(l), n):
	        yield l[i:i+n]

	def generate_hta(self, obfuscated_launcher, pattern):
		"""This function generates an hta file to deliver the obfuscated launcher"""
		env = Environment(loader=FileSystemLoader('templates'))
		hta_template = env.get_template('hta_template.txt')
		hta_file = hta_template.render(obfuscated_launcher=obfuscated_launcher, pattern=pattern)
		return hta_file

	def generate_vba(self, obfuscated_launcher, pattern):
		"""This function generates a vba file to deliver the obfuscated launcher"""
		# Break obfuscated_launcher into 50 char chunks
		launcher_chunks = list(self.chunks(obfuscated_launcher, 50))
		chunked_launcher = "Dim Str As String\n"
		chunked_launcher += "\tstr = \"" + str(launcher_chunks[0]) + "\"\n"
		for chunk in launcher_chunks[1:]:
			chunked_launcher += "\tstr = str + \"" + str(chunk) + "\"\n"

		# Create vba_file from template
		env = Environment(loader=FileSystemLoader('templates'))
		hta_template = env.get_template('vba_template.txt')
		vba_file = hta_template.render(obfuscated_launcher=chunked_launcher, pattern=pattern)
		return vba_file