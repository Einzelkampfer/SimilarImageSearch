# -*- coding:utf-8 -*- 
import smtplib
import sys
import os
import math
import shutil
import time
import commands

shellcommand = "$(cat ../features.txt| wc -l)"
lineNum = commands.getstatusoutput(shellcommand)
lineNum = lineNum[1].split(" ")[2][:-1]
lineNum = int(lineNum)
fileObj = open("trainImgList.txt", "r")
i = 1
start = time.time()
line = fileObj.readline()
while True:
	if not line:
		break
	if i > lineNum:
		# print i
		s = time.time()
		line = line.strip()
		cmd = """./build/tools/googlenet_extract_feature.bin \
			models/bvlc_googlenet/deploy.prototxt \
			models/bvlc_googlenet/bvlc_googlenet.caffemodel \
			data/ilsvrc12/imagenet_mean.binaryproto \
			/media/zsz/新加卷/features.txt \
			pool5/7x7_s1 %s"""  % line
		os.system(cmd)
		# time.sleep(5.0)
		e = time.time()
		print "time used:%f seconds" % (e - s)
		print "total time used:%f seconds" % (e - start)
	i += 1
	line = fileObj.readline()
end = time.time()
print "total time used:%f seconds" % (end - start)
fileObj.close()



# cat trainImgList.txt  | while read myline
# do
# 	let "i++"
# 	if [ "$i" -gt "$linenum" ];then
# 		# echo "$i"
# 		s=$(date "+%s")
		
# 		e=$(date "+%s")
# 		time=$((e-s))
# 		echo "time used:$time seconds"
# 		time=$((e-start))
# 		echo "total time used:$time seconds"
# 	fi
# done
# end=$(date "+%s")
# time=$((end-start))
# echo "total time used:$time seconds"