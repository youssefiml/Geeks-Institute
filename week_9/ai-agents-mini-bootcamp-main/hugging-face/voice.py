import torch
from transformers import AutoTokenizer, AutoProcessor, CsmForConditionalGeneration
from tokenizers.processors import TemplateProcessing
import soundfile as sf
import torch

model_id = "Marvis-AI/marvis-tts-250m-v0.1-transformers"
device = "mps" if torch.backends.mps.is_available() else "cpu"

# load the model and the processor
processor = AutoProcessor.from_pretrained(model_id)
model = CsmForConditionalGeneration.from_pretrained(model_id).to(device)

# prepare the inputs
text = "[0]Marvis TTS is a new text-to-speech model that provides fast streaming on edge devices." # `[0]` for speaker id 0
inputs = processor(text, add_special_tokens=True, return_tensors="pt").to(device).pop("token_type_ids")
# infer the model
audio = model.generate(**inputs, output_audio=True)
sf.write("example_without_context.wav", audio[0].cpu(), samplerate=24_000, subtype="PCM_16")
