# Do Newer LLMs Do Better?
### Evaluating GPT-4o, Claude, and Gemini on Normal and Obfuscated Code Analysis
 
**Institution:** Toronto Metropolitan University  
**Supervisor:** Prof. Manar Alalfi  
**Author:** Ali Navab Zadeh  

---

## Overview

This project extends the work of Fang et al. (USENIX Security 2024) by evaluating three newer LLMs on code analysis tasks using three prompting strategies.

**Models evaluated:**
- GPT-4o (OpenAI)
- Claude Sonnet 4.6 (Anthropic)
- Gemini 2.5 Flash (Google)

**Tasks:**
- Code explanation (99 Python files)
- Obfuscated JavaScript analysis (5 obfuscation schemes)

**Prompting strategies:**
- Zero-shot
- Few-shot
- Chain-of-thought (CoT)

---

## Key Findings

- All three newer models outperform the original models from Fang et al.
- GPT-4o achieves the highest scores on both tasks
- Chain-of-thought prompting does NOT improve performance on code analysis tasks

---

## Project Structure

llm-code-analysis/
├── prompts.py              # All 9 prompt functions
├── run_experiments.py      # API calls and experiment pipeline
├── evaluate.py             # BERTScore and cosine similarity evaluation
├── results_explanation.csv # Final explanation task results
├── results_obfuscated.csv  # Final obfuscated task results
├── show_figures_v2.py      # Generate result figures
└── llms-for-code-analysis/ # Dataset from Fang et al.

---

## Setup

1. Clone this repository
2. Install dependencies:

pip install -r requirements.txt

3. Create a `.env` file with your API keys:

OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here


4. Clone the dataset:
git clone https://github.com/aseec-lab/llms-for-code-analysis

---

## Running the Experiments

python3 run_experiments.py

## Evaluating Results

python3 evaluate.py

## Generating Figures

python3 show_figures_v2.py

---

## Dataset


Dataset from Fang et al.: https://github.com/aseec-lab/llms-for-code-analysis

---

## Reference

Fang et al. "Large Language Models for Code Analysis: Do LLMs Really Do Their Job?" USENIX Security 2024.