# -*- coding: utf-8 -*-
import os
import torch
from transformers import pipeline, BitsAndBytesConfig, GenerationConfig, AutoTokenizer
from peft import AutoPeftModelForCausalLM

os.environ['HF_TOKEN'] = ""
model_name = "models/llama-1B-finetuned-8e"

model = AutoPeftModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16).to('cuda')
tokenizer = AutoTokenizer.from_pretrained(model_name)
quant_config = BitsAndBytesConfig(load_in_8bit=True)
chatbot = pipeline(task='text-generation',
                   model=model,
                   tokenizer=tokenizer,
                   device_map='auto',
                   model_kwargs={'quantization_config':quant_config})

gen_strategy  = GenerationConfig(
    do_sample=False,
    num_beams=1,
    max_new_tokens = 3000,
    repetition_penalty=1.2,
)

conversation_dicts = [
    {'role': 'user', 'content': f'''Given the following system description, tell me in full detail and without ambiguities or vagueness everything that someone implementing the system should know. If necessary, make assumptions as you see fit, providing concrete examples for any potential doubts that may arise-for instance, when there are references to time without specific durations, when conditions are mentioned but not explicitly defined, or when dealing with device connections, etc. Present the information in the form of functional and non-functional requirements.
     
The Space Fractions project is a learning tool created to help improve fraction-solving skills for sixth-grade students. The product will be a web-based, interactive game. At the end of the game, students will be given feedback based on their game scores. We are also providing an umbrella for the past games created. The umbrella will be a web-based menu system allowing the user to choose between the games.'''}
]

outputs = chatbot(conversation_dicts, generation_config=gen_strategy)

output_file = "../outputs/llama-1B/1_space_fractions_8e_2p.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(outputs[0]['generated_text'][-1]['content'])
