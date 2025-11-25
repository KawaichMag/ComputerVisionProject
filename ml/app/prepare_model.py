import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

print("Torch version:", torch.__version__)
print("CUDA:", torch.version.cuda)
print("Is CUDA available?", torch.cuda.is_available())
print("Device count:", torch.cuda.device_count())
# print("Device name:", torch.cuda.get_device_name(0))

print("Starting model loading process..")
start_load = time.time()
# Define the model
model_id = "vikhyatk/moondream2"
revision = "2025-06-21"
save_directory = "./ml_model"

# Load the model
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    revision=revision,
    trust_remote_code=True,
    dtype=torch.float16,
    device_map={"": "cuda"} if torch.cuda.is_available() else {"": "cpu"},
)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

print(f"Done with model preparing in {time.time() - start_load}")

# Save Model and Tokenizer
print(f"Saving model and tokenizer to {save_directory}...")
os.makedirs(save_directory, exist_ok=True)
model.save_pretrained(save_directory)
tokenizer.save_pretrained(save_directory)
print("Model and tokenizer saved successfully.")
