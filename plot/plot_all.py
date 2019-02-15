#! /usr/bin/python
# coding:utf8
#

from myclass import PlotMain, processFolder

dates = [('2018-07-30', '2018-08-12'), ('2018-08-13', '2018-08-26'), ('2018-08-27', '2018-09-09'), ('2018-09-10', '2018-09-23'), ('2018-09-24', '2018-10-07')]
pathes = ['/ifs/cisinas03/projects/PioneerLite', '/ifs/cisinas03/projects2/Cambricon_Thunder', '/ifs/data/Isilon_Support', '/ifs/.ifsvar/upgrade', '/ifs/cisinas03/homeproj/ccase/ClearCase_View_Templates']
keys = ['blocked', 'contended', 'getattr', 'lock', 'lookup', 'read', 'setattr', 'write', 'rename', 'unlink', 'link']

for path in pathes:
    for date in dates:
	date1 = date[0]
	date2 = date[1]
        folder_jpg = processFolder(path, date1, date2)

	try:
	    for key in keys:
		myplot = PlotMain(path, key, date1, date2, folder_jpg)
		myplot.sql_x()
		myplot.sql_y()
		myplot.savepic()
		# raw_input("P: ")
	except Exception as e:
	    print "画图错误: " + str(e)

	
