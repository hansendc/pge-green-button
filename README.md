# pge-green-button
A quick and dirty cost calculator of "Green Button" data

There seem to be a bunch of libraries out there for parsing this
data, but none of them were obviously what I wanted, so I hacked
something together.

My goal here was to see if PGE's "basic" pricing (which is pretty
much flat) or their "time of use" pricing would be better for me.
I just hard-coded the per-kWh prices and schedule (day of week,
seasons, and hours of day).  I ignore holidays for now.

My python is embarrasing, but here it is anyway.

usage: pge-green-button.py pgn_electric_interval...2020-12-31.csv

On the PGE page after you log in, there is a

	Track your energy use

and

	My Use

section.  Look for a "Green Button" there.  Click on it.  It should
open up a "Download my data" form.  In that form, click on "Export
usage for a range of days", and select a range of days.  This tool
will work most accurately if given whole months: 1/1/2020 to
12/31/2020 is better than 2/15/2020 to 4/15/2020.  Then, click
"Export".  A file should download.  Pass that file as the first
argument to this script.

You should see output like this:

	month: 2019-01 basic: $58.22 tiered: $71.38 kwh:  920
	month: 2019-02 basic: $54.46 tiered: $65.41 kwh:  860
	month: 2019-03 basic: $60.15 tiered: $71.95 kwh:  950
	month: 2019-04 basic: $53.03 tiered: $62.37 kwh:  838
	month: 2019-05 basic: $57.37 tiered: $61.21 kwh:  906
	total: basic: $1234.56 tiered: $6789.01

