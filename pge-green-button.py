#!/usr/bin/python3
# Copyright 2021, Dave Hansen <dave@sr71.net>
#
# Released under the GNU General Public License version 2:
#
#	http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#
# usage: pge-green-button.py pgn_electric_interval...2020-12-31.csv
#
# On the PGE page after you log in, there is a
#
# 	Track your energy use
#
# and
#
# 	My Use
#
# section.  Look for a "Green Button" there.  Click on it.  It should
# open up a "Download my data" form.  In that form, click on "Export
# usage for a range of days", and select a range of days.  This tool
# will work most accurately if given whole months: 1/1/2020 to
# 12/31/2020 is better than 2/15/2020 to 4/15/2020.  Then, click
# "Export".  A file should download.  Pass that file as the first
# argument to this script.
#

import sys
import datetime

onpeak  = 0.12380
midpeak = 0.07051
offpeak = 0.04128

# Needed because "basic" rate goes up after 1000 kWh
this_month = -1
this_month_kwh = 0

def winter_weekday(hour):
	if (hour >= 6 and hour < 10):
		return onpeak;
	if (hour >= 10 and hour < 17):
		return midpeak;
	if (hour >= 17 and hour < 20):
		return onpeak;
	if (hour >= 20 and hour < 22):
		return onpeak;
	return offpeak;

def winter_saturday(hour):
	if (hour >= 6 and hour < 22):
		return midpeak;
	return offpeak;

def winter_sunday(hour):
	return offpeak;

def summer_weekday(hour):
	if (hour >=  6 and hour < 15):
		return midpeak;
	if (hour >= 15 and hour < 20):
		return onpeak;
	if (hour >= 20 and hour < 22):
		return midpeak;
	return offpeak;

def summer_saturday(hour):
	if (hour >= 6 and hour < 22):
		return midpeak;
	return offpeak;

def summer_sunday(hour):
	return offpeak;

def month_is_summer(month):
	if (month >= 5 and month <= 10):
		return True
	return False

def basic_price_kwh(date, kwh):
	global this_month_kwh
	global this_month
	if (date.month != this_month):
		#print("last month %d: %f" % (this_month, this_month_kwh))
		this_month_kwh = 0
		this_month = date.month

	this_month_kwh = this_month_kwh + kwh

	if (this_month_kwh < 1000):
		return 0.06329
	return 0.07051

def time_price_kwh(date, time, kwh):
	#print("date: '%s'" % (date))

	t = time.split(":")
	hour = int(t[0])

	weekday = date.weekday()
	#dp.dprint4("day: %d" % (date.weekday()))

	# TODO: add holidays
	if month_is_summer(date.month):
		if (weekday == 0):
			return summer_sunday(hour)
		if (weekday == 6):
			return summer_saturday(hour)
		return summer_weekday(hour)
	else:
		if (weekday == 0):
			return winter_sunday(hour)
		if (weekday == 6):
			return winter_saturday(hour)
		return winter_weekday(hour)

	print("bad 1234");
	sys.exit(1)

def cat_file(filename):
	filefd = open(filename)
	stuff = filefd.read()
	filefd.close()
	return stuff

sys.argv.pop()
csv_lines = []
for f in sys.argv:
	print ("reading '%s'" % (f))

	csv = cat_file(f)
	csv_lines = csv_lines + csv.split("\n")
	print ("now have %d lines" % (len(csv_lines)))

basic_total = 0
timed_total = 0

basic_months = {}
timed_months = {}
kwh_months   = {}

def inc(h, key, kwh):
	if h.get(key) == None:
		h[key] = 0
	h[key] = h[key] + kwh

for line in csv_lines:
	parts = line.split(",")

	if (parts[0] != "Electric usage"):
		#print("bad line: %s" % (line))
		continue

	#dp.dprint3("parsing line: %s" % (line))
	date = parts[1]
	time = parts[2]
	kwh  = float(parts[4])
	cost = parts[6]

	d = date.split("-")
	date = datetime.datetime(int(d[0]), int(d[1]), int(d[2]))

	timed_rate =  time_price_kwh(date, time, kwh)
	timed_cost = timed_rate * kwh
	timed_total = timed_total + timed_cost

	basic_rate = basic_price_kwh(date, kwh)
	basic_cost = basic_rate * kwh
	basic_total = basic_total + basic_cost

	# Gather up all the calulations per month
	key = "%4d-%02d" % (date.year, date.month)
	inc(timed_months, key, timed_cost)
	inc(basic_months, key, basic_cost)
	inc(kwh_months,   key, kwh)

for i in sorted(basic_months):
	print("month: %s basic: $%4.2f tiered: $%4.2f kwh: %4.0f" % (i,
		basic_months[i],
		timed_months[i],
		kwh_months[i]))

print("total: basic: $%4.2f tiered: $%4.2f" % (basic_total, timed_total))
