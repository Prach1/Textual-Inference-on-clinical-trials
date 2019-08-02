
for i in $(seq 1 4); do
	FPATH=out/out_ec_$i python3.5 predict.py < input/input_ec_$i.txt;
done
