from transformers import AutoTokenizer
import argparse
import transformers
import torch


def load_model(model):
    tokenizer = AutoTokenizer.from_pretrained(model)
    pipeline = transformers.pipeline("text-generation", model=model, torch_dtype=torch.float16, device_map="auto")

def generate_result(dataset, outdir):
    fout = open(outdir, "w")
    with open(dataset, "r") as f:
        lines = f.readlines()
        for i in range(0, len(lines), 3):
            text = lines[i].strip()
            aspect = lines[i+1].strip()
            polarity = lines[i+2].strip()
            
            prompt = f"Classify the aspect of the text into neutral, negative or positive.\nText: {text}\nAspect: {aspect}\nSentiment:"

            sequences = pipeline(prompt, do_sample=True, top_k=10, num_return_sequences=1, eos_token_id=tokenizer.eos_token_id, max_length=10,)
            print(sequences)
            #fout.write(sequences)
            #print(f"Result: {seq['generated_text']}")




def main():
    parser = argparse.ArgumentParser()
    
    # Define command line arguments
    parser.add_argument("--model_dir", type=str, required=True)
    parser.add_argument("--dataset_dir", type=str, required=True)
    parser.add_argument("--method", type=str, choices=["zeroshot", "cot"], required=True)
    parser.add_argument("--outdir", type=str, required=True)
    parser.add_argument("--senticnet_api", type=str)
    
    args = parser.parse_args()
    args_dict = vars(args)
    for key, value in args_dict.items():
        print(f"{key}: {value}") 
    load_model(args.model_dir)
    generate_result(args.dataset_dir, args.outdir)

if __name__ == "__main__":
    main()

