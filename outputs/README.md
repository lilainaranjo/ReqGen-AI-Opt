# Conguración de los modelos de lenguaje

Este documento agrupa las configuraciones empleadas por cada modelo ajustado y sus respectivas salidas generadas en el directorio `outputs/`.

Cada subdirectorio dentro de `outputs/` (por ejemplo, `llama-1B/`, `llama-3B/`, `llama-8B/`, `mistral/`, `deepseek/`, `chatgpt/`) representa un **modelo base** diferente:

| Directorio         | Modelo base                         |
|--------------------|-------------------------------------|
| `llama-1B/` | `meta-llama/Llama-3.2-1B-Instruct` (Hugging Face) |
| `llama-3B/` | `meta-llama/Llama-3.2-3B-Instruct` (Hugging Face) |
| `llama-8B/` | `meta-llama/Llama-3.1-8B-Instruct` (Hugging Face) |
| `mistral/` | `mistralai/Mistral-7B-Instruct-v0.3` (Hugging Face) |
| `deepseek/` | DeepSeek (no fine-tuning) |
| `chatgpt/` | OpenAI ChatGPT (no fine-tuning) |

Los ficheros dentro de cada directorio de llama y mistral representan salidas generadas por ese modelo con distintas configuraciones de entrenamiento o inferencia. **El prefijo numérico en el nombre del archivo (ID)** indica una variante de configuración concreta.

---

## Convención de IDs

- Todos los ficheros con **ID 1** representan la salida del **modelo base sin ajustar** (zero-shot).
- El resto de IDs corresponden a variantes del modelo ajustado (fine-tuned) con diferentes configuraciones.

---

## Parámetros usados por configuración

| ID | Épocas | LoRA | Cuantización | Repetition Penalty | Sistema | Prompt |
|----|--------|------|--------------|--------------------|---------|--------|
| 2 | 1 | Sí | No | 1.0 | 2001 - space fractions | default |
| 3 | 2 | Sí | No | 1.0 | 2001 - space fractions | default |
| 4 | 2 | Sí | No | 1.0 | 2001 - space fractions | default |
| 5 | 8 | Sí | No | 1.0 | 2001 - space fractions | default |
| 6 | 16 | Sí | No | 1.0 | 2001 - space fractions | default |
| 7 | 32 | Sí | No | 1.0 | 2001 - space fractions | default |
| 8 | 1 | Sí | No | 1.0 | 2001 - space fractions | simple |
| 9 | 2 | Sí | No | 1.0 | 2001 - space fractions | simple |
| 10 | 4 | Sí | No | 1.0 | 2001 - space fractions | simple |
| 11 | 8 | Sí | No | 1.0 | 2001 - space fractions | simple |
| 12 | 16 | Sí | No | 1.0 | 2001 - space fractions | simple |
| 13 | 4 | Sí | No | 1.0 | 2007 - e-store.pdf | default |
| 14 | 8 | Sí | No | 1.0 | 2007 - e-store.pdf | default |
| 15 | 16 | Sí | No | 1.0 | 2007 - e-store.pdf | default |
| 16 | 4 | Sí | No | 1.1 | 2001 - space fractions | default |
| 17 | 4 | Sí | No | 1.2 | 2001 - space fractions | default |
| 18 | 4 | Sí | No | 1.3 | 2001 - space fractions | default |
| 19 | 4 | Sí | No | 1.4 | 2001 - space fractions | default |
| 20 | 4 | Sí | No | 1.5 | 2001 - space fractions | default |
| 21 | 8 | Sí | No | 1.1 | 2001 - space fractions | default |
| 22 | 8 | Sí | No | 1.2 | 2001 - space fractions | default |

## Notas

- **LoRA** siempre emplea: `r = 8`, `lora_alpha = 16`, `dropout = 0.05`.
- `Repetition Penalty` es el parámetro variado en algunos experimentos de inferencia.
- Los modelos ajustados se almacenan en `models/` bajo nombres como `llama-1B-finetuned-8e/`.
- El **prompt por defecto (default)** utilizado es:
```text
Given the following system description, tell me in full detail and without ambiguities or vagueness everything that someone implementing the system should know. If necessary, make assumptions as you see fit, providing concrete examples for any potential doubts that may arise-for instance, when there are references to time without specific durations, when conditions are mentioned but not explicitly defined, or when dealing with device connections, etc. Present the information in the form of functional and non-functional requirements.

[System description here]
```
- El **prompt simple** utilizado es:
```text
Given the following system description, extract its functional and non-functional requirements.

[System description here]
```
