import torch
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer

def main():
    # Present model choices to the user
    print("Choose a model:")
    print("a: gpt2")
    print("b: EleutherAI/gpt-neo-2.7B")
    
    model_choice = input("Enter your choice (a or b): ").strip().lower()
    if model_choice == 'a':
        model_name = "gpt2"
    elif model_choice == 'b':
        model_name = "EleutherAI/gpt-neo-2.7B"
    else:
        print("Invalid choice. Please run the script again and enter either 'a' or 'b'.")
        return
    prompt = input("Enter the text prompt: ").strip()
    max_new_tokens = int(input("Enter the maximum number of new tokens to generate: ").strip())
    do_sample = input("Do you want to use sampling? (yes/no): ").strip().lower() == 'yes'
    use_cache = input("Do you want to use cache? (yes/no): ").strip().lower() == 'yes'
    
    # Load the model and tokenizer
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Set the device to CUDA if available
    device = 0 if torch.cuda.is_available() else -1

    # Create the text generation pipeline
    pipe = pipeline('text-generation', model=model, tokenizer=tokenizer, device=device)

    # Generate text with mixed precision if CUDA is available
    if torch.cuda.is_available():
        with torch.autocast('cuda', dtype=torch.bfloat16):
            generated_text = pipe(
                prompt,
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                use_cache=use_cache
            )
    else:
        generated_text = pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            use_cache=use_cache
        )

    # Print the generated text
    print("Generated Text:")
    print(generated_text[0]['generated_text'])

if __name__ == "__main__":
    main()
