import os
import time
from dotenv import load_dotenv
import openai
import anthropic
from google import genai as genai_client
from prompts import (
    zero_shot_explanation, few_shot_explanation, chain_of_thought_explanation,
    zero_shot_obfuscated, few_shot_obfuscated, chain_of_thought_obfuscated
)

# Load API keys from .env file
load_dotenv()

# Connect to each model
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
google_client = genai_client.Client(api_key=os.getenv("GOOGLE_API_KEY"))



def call_model(model_name, prompt):
    if model_name == "gpt-4o":
        response = openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096
        )
        return response.choices[0].message.content

    elif model_name == "claude":
        response = anthropic_client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    elif model_name == "gemini":
        response = google_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text


def save_response(response, model_name, strategy, filename, task):
    output_dir = f"outputs/{task}/{model_name}/{strategy}"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename.replace('.py', '.txt').replace('.js', '.txt'))
    with open(output_path, 'w') as f:
        f.write(response)


# Define models and strategies
MODELS = ["gpt-4o", "claude", "gemini"]

STRATEGIES = {
    "zero-shot": zero_shot_explanation,
    "few-shot": few_shot_explanation,
    "cot": chain_of_thought_explanation
}



def run_explanation_experiments():
    dataset_path = "llms-for-code-analysis/dataset/nonobfuscated/python-data"
    
    files = [f for f in os.listdir(dataset_path) if f.endswith('.py')]
    print(f"Found {len(files)} Python files")
    
    for filename in files:
        file_path = os.path.join(dataset_path, filename)
        
        with open(file_path, 'r', errors='ignore') as f:
            code = f.read()
        
        for model_name in MODELS:
            for strategy_name, prompt_function in STRATEGIES.items():
                
                # Skip if already done
                output_path = f"outputs/explanation/{model_name}/{strategy_name}/{filename.replace('.py', '.txt')}"
                if os.path.exists(output_path):
                    print(f"Skipping {model_name} | {strategy_name} | {filename} — already done")
                    continue
                
                print(f"Running {model_name} | {strategy_name} | {filename}")
                
                try:
                    prompt = prompt_function(code)
                    response = call_model(model_name, prompt)
                    save_response(response, model_name, strategy_name, filename, "explanation")
                except Exception as e:
                    print(f"Error on {model_name} | {strategy_name} | {filename}: {e}")
                
                time.sleep(1)


def run_obfuscated_experiments():
    SCHEMES = ["default", "control-flow-flattening", "dead-code-injection", "split-string", "wobfuscator"]
    
    OBFUSCATED_STRATEGIES = {
        "zero-shot": zero_shot_obfuscated,
        "few-shot": few_shot_obfuscated,
        "cot": chain_of_thought_obfuscated
    }
    
    for scheme in SCHEMES:
        dataset_path = f"llms-for-code-analysis/dataset/obfuscated/javascript-data/{scheme}"
        
        files = [f for f in os.listdir(dataset_path) if f.endswith('.js')]
        print(f"\nScheme: {scheme} — Found {len(files)} JavaScript files")
        
        for filename in files:
            file_path = os.path.join(dataset_path, filename)
            
            with open(file_path, 'r', errors='ignore') as f:
                code = f.read()
            
            for model_name in MODELS:
                for strategy_name, prompt_function in OBFUSCATED_STRATEGIES.items():
                    
                    # Skip if already done
                    output_path = f"outputs/obfuscated/{scheme}/{model_name}/{strategy_name}/{filename.replace('.js', '.txt')}"
                    if os.path.exists(output_path):
                        print(f"Skipping {model_name} | {strategy_name} | {filename} — already done")
                        continue
                    
                    print(f"Running {model_name} | {strategy_name} | {scheme} | {filename}")
                    
                    try:
                        prompt = prompt_function(code)
                        response = call_model(model_name, prompt)
                        save_response(response, model_name, strategy_name, filename, f"obfuscated/{scheme}")
                    except Exception as e:
                        print(f"Error on {model_name} | {strategy_name} | {filename}: {e}")
                    
                    time.sleep(1)



if __name__ == "__main__":
    print("=== Running explanation experiments ===")
    run_explanation_experiments()
    
    print("\n=== Running obfuscated experiments ===")
    run_obfuscated_experiments()
    
    print("\nAll experiments complete!")