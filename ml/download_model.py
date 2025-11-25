from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def download_model():
    model_id = "vikhyatk/moondream2"
    revision = "2025-06-21"

    print(f"Downloading model: {model_id} (revision: {revision})")
    
    # Download model
    AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        trust_remote_code=True,
        dtype=torch.float16,
    )
    
    # Download tokenizer (good practice to have it available too)
    print(f"Downloading tokenizer: {model_id} (revision: {revision})")
    AutoTokenizer.from_pretrained(
        model_id,
        revision=revision,
    )

    print("Model and tokenizer downloaded successfully.")

if __name__ == "__main__":
    download_model()
