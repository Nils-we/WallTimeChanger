#!/usr/bin/env python3
# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# This file is part of WeatherDesk.
#
# WeatherDesk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WeatherDesk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WeatherDesk (in the LICENSE file).
# If not, see <http://www.gnu.org/licenses/>.

from urllib.request import urlopen
import urllib.error
import os
import time
import datetime
import json
import sys
import argparse
import Desktop
import traceback
import subprocess as sp
import random
from os import listdir
from os.path import isfile, join

NAMING_RULES = '''
This is how to name directories in the wallpaper (/.walls) directory:\n
	   for t -2: day, night
	   for t -3: day, evening, night
	   for t -4: morning, day, evening, night (this is the default setting)
Please be sure the directories are exactly spelled like above. Otherwise it will not work.

'''


# Arguments

arg_parser = argparse.ArgumentParser(
	description='''WallTimeChanger - Change the wallpaper based on the time''',
	formatter_class=argparse.RawTextHelpFormatter)

arg_parser.add_argument(
	'-d', '--dir', metavar='directory', type=str,
	help='Specify wallpaper directory. Default: %s' % '~/.walls',
	required=False)

arg_parser.add_argument(
	'-f', '--format', metavar='format', type=str,
	help='Specify image file format. Default: %s' % '.jpg',
	required=False)

arg_parser.add_argument(
	'-w', '--wait', metavar='seconds', type=int,
	help='Specify time (in seconds) to wait before updating. Default: 600',
	required=False)

arg_parser.add_argument(
	'-t', '--time', nargs='?',
	help='''Choose the amount of categories.\n
Variations:
  2 = day/night
  3 = day/evening/night
  4 = morning/day/evening/night [Default]
See --naming.''',
	type=int, choices=[2, 3, 4], const=3, default=4, required=False)

arg_parser.add_argument(
	'-n', '--naming', action='store_true',
	help='Show the image file-naming rules and exit.',
	required=False)

arg_parser.add_argument(
	'-o', '--one-time-run', action='store_true',
	help='Run once, then exit.',
	required=False)

args = arg_parser.parse_args()

use_time = bool(args.time)

if args.dir:

	# User provided a directory
	walls_dir = os.path.abspath(args.dir)

	if not os.path.isdir(walls_dir):

		sys.stderr.write('Invalid directory %s.' % walls_dir)
		sys.exit(1)
else:

	walls_dir = os.path.join(os.path.expanduser('~'), '.walls')

	if not os.path.isdir(walls_dir):

		os.mkdir(walls_dir)
		fmt = '''No directory specified.
Creating in {}... Put files there or specify directory with --dir'''
		sys.stderr.write(fmt.format(walls_dir))
		sys.exit(1)

if args.format:

	if not args.format.startswith('.'):

		args.format = '.' + args.format

	file_format = args.format

else:

	file_format = '.jpg'

wait_time = args.wait or 600  # ten minutes

if args.naming:

	print(NAMING_RULES.format(file_format))
	sys.exit(0)

# Functions

def get_time_of_day(level=4):

	'''
	For detail level 2:
	06 to 20: day
	20 to 06: night
	'''

	'''
	For detail level 3:
	06 to 17: day
	17 to 20: evening
	20 to 06: night
	'''

	'''
	For detail level 4:
	06 to 08: morning
	08 to 17: day
	17 to 20: evening
	20 to 06: night
	'''

	current_time = datetime.datetime.now().time()

	if level == 3:

		if current_time.hour in range(6, 17):

			return 'day'

		elif current_time.hour in range(17, 20):

			return 'evening'

		else:

			return 'night'

	elif level == 4:

		if current_time.hour in range(6, 8):

			return 'morning'

		elif current_time.hour in range(8, 17):

			return 'day'

		elif current_time.hour in range(17, 20):

			return 'evening'

		else:

			return 'night'

	else:

		if current_time.hour in range(6, 20):

			return 'day'

		else:
)
			return 'night'

def get_file_name():
	image_list = [f for f in listdir(walls_dir + '/' + get_time_of_day(args.time)) if isfile(join(walls_dir + '/' + get_time_of_day(args.time), f))]

	image = random.choice(image_list)


	return image


def check_if_all_files_exist(level=4):

	all_exist = True


	if level == 3:

		daytime = ['/day', '/evening', '/night']

	elif level == 4:

		daytime = ['/morning', '/day', '/evening', '/night']

	else:  # level 2

		daytime = ['/day', '/night']

	required_files = daytime

	for i in required_files:

		if not os.path.isdir(walls_dir + i):

			all_exist = False

			sys.stderr.write(walls_dir + '\n')

	return all_exist


if not check_if_all_files_exist(level=args.time):

	sys.stderr.write(
		'\nNot all required files were found.\n %s' % NAMING_RULES.format(
			file_format))

	sys.exit(1)

def restart_program():

	# Restarts the current program, with file objects and descriptors cleanup

	new_walltimechanger_cmd = ''

	for i in sys.argv:

		new_walltimechanger_cmd = ' ' + i

	sp.Popen([new_walltimechanger_cmd], shell=True)

	sys.exit(0)

def main():

	Desktop.set_wallpaper(
		os.path.join(walls_dir + '/' + get_time_of_day(args.time), get_file_name()))



# Main loop

if args.one_time_run:
	main()
	sys.exit(0)

while True:

	try:

		main()

	except urllib.error.URLError:

		# Don't shut off on temporary network problems

		trace_main_loop = '[Main loop] \n' + traceback.format_exc()


		if sys.platform.startswith('linux'):

			# HACK: glibc on Linux only loads /etc/resolv.conf once
			# This breaks our network communications after suspend/resume
			# So we force it to reload using the res_init() function

			# But sometimes res_init() mysteriously crashes the program
			# and it's too low-level for any try-except to catch.

			# So we restart the whole thing!

			restart_program()

	except ValueError:

		# Sometimes JSON returns a null value for no reason

		trace_main_loop = '[Main loop] \n' + traceback.format_exc()

	except:

		# All other errors (except KeyboardInterrupt ^C)
		# We'll still have a full stack trace

		trace_main_loop = '[Main loop] \n' + traceback.format_exc()

	else:

		trace_main_loop = '[Main loop] No error.'

	finally:

		print(trace_main_loop)

	time.sleep(wait_time)
