linenum=$(cat ../features.txt| wc -l)
# echo "$linenum"
start=$(date "+%s")
i=0
cat trainImgList.txt  | while read myline
do
	let "i++"
	if [ "$i" -gt "$linenum" ];then
		# echo "$i"
		s=$(date "+%s")
		./build/tools/googlenet_extract_feature.bin \
		models/bvlc_googlenet/deploy.prototxt \
		models/bvlc_googlenet/bvlc_googlenet.caffemodel \
		data/ilsvrc12/imagenet_mean.binaryproto \
		/media/zsz/新加卷/features.txt \
		pool5/7x7_s1 $myline
		e=$(date "+%s")
		time=$((e-s))
		echo "time used:$time seconds"
		time=$((e-start))
		echo "total time used:$time seconds"
	fi
done
end=$(date "+%s")
time=$((end-start))
echo "total time used:$time seconds"
