from transformers import AutoModelForCausalLM

def init_models(app):
    model_id = "vikhyatk/moondream2"
    revision = "2025-06-21"

    app.model = AutoModelForCausalLM.from_pretrained(
        model_id,
        revision=revision,
        trust_remote_code=True,
        torch_dtype=torch.float16,
        device_map={"": "cuda"} if torch.cuda.is_available() else {"": "cpu"}
    )