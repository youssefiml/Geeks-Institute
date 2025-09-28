from transformers import pipeline
import torch

model = pipeline("summarization", model="facebook/bart-large-cnn")

response = model("Artificial Intelligence (AI) is transforming industries worldwide. From healthcare to finance, AI systems help analyze large amounts of data, improve decision-making, and automate repetitive tasks. For example, in medicine, AI assists doctors by detecting diseases in early stages through image analysis. In business, AI chatbots provide customer support 24/7, reducing costs and improving efficiency. However, the rise of AI also brings challenges, including job displacement and ethical concerns about privacy and bias. Balancing innovation with responsibility is now a key priority.")

print(response)