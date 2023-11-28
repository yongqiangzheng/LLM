export SENTICNET_API="1"

model="llama"
dataset="lap14"
outdir="result/$model/$dataset/"

if [ ! -d "$outdir" ]; then
    mkdir -p "$outdir"
fi

python inference.py \
	--model /data/algo/HFAssets/Models/HF-LLaMA/7B/ \
	--dataset SemEval2014/Laptops_Test.txt \
	--method zeroshot \
	--outdir $outdir \
	--senticnet_api $SENTICNET_API \
