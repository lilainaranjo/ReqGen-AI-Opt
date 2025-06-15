# -*- coding: utf-8 -*-
import os
import torch
from datasets import load_dataset
from transformers import BitsAndBytesConfig, Trainer, AutoModelForCausalLM, AutoTokenizer, TrainingArguments, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model

# General configuration
os.environ['HF_TOKEN'] = ""
model_name = "meta-llama/Llama-3.2-1B-Instruct"
context_length = 2048
total_epochs = 8
batch_size = 1
learning_rate = 1e-4

# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def tokenize_with_chat_template(rows):
    conversation_dicts = [{'role':'system', 'content': 'Your are an expert software engineer.'}]
    for prompt, sol in zip(rows['prompt'], rows['requirements']):
        prompt = prompt or ""
        sol = sol or ""
        conversation_dicts.append({'role':'user', 'content':prompt})
        conversation_dicts.append({'role':'assistant', 'content':sol})

    outputs = tokenizer.apply_chat_template(
        conversation_dicts,
        truncation=False,
    )
    batch_ids = [outputs[i:i + context_length] for i in range(0, len(outputs), context_length)]
    batch_ids = batch_ids[:-1]
    return {"input_ids": batch_ids}

# Dataset
data = load_dataset('csv', data_files='data/dataset.csv', split='all', delimiter=';')
data_train = data.map(tokenize_with_chat_template, batched=True, remove_columns=data.column_names)

# Model configuration
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

lora_config = LoraConfig(
    r=8,  
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
model = get_peft_model(model, lora_config)

# Training
training_args = TrainingArguments(
    output_dir = "./models/llama-1B-finetuned-8e",
    overwrite_output_dir = True,
    num_train_epochs = total_epochs,
    eval_strategy = "no",
    save_strategy = "no",
    save_total_limit = 2,
    load_best_model_at_end = False,
    logging_strategy = 'epoch',
    per_device_train_batch_size = batch_size,
    per_device_eval_batch_size = 2*batch_size,
    learning_rate = learning_rate,
    weight_decay = 0.01,
    warmup_steps = 0,
    report_to="none",
)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

trainer = Trainer(
    model = model,
    args = training_args,
    train_dataset = data_train,
    data_collator = data_collator,
    processing_class = tokenizer,
)

trainer.train()

# Save model
trainer.save_model("./models/llama-1B-finetuned-8e")
tokenizer.save_pretrained("./models/llama-1B-finetuned-8e")
