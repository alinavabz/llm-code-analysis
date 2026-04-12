import os
import pandas as pd
from bert_score import score
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer



def compute_scores(reference_text, hypothesis_text):
    # BERTScore
    P, R, F1 = score(
        [hypothesis_text], 
        [reference_text], 
        lang="en", 
        verbose=False
    )
    bert_f1 = F1.item()
    
    # Cosine similarity
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([reference_text, hypothesis_text])
    cosine_sim = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    return {
        "bertscore": round(bert_f1, 4),
        "cosine": round(float(cosine_sim), 4)
    }



def evaluate_explanation():
    results = []
    
    ground_truth_path = "llms-for-code-analysis/results/nonobfuscated/python-data/gpt-4"
    outputs_path = "outputs/explanation"
    
    models = ["gpt-4o", "claude", "gemini"]
    strategies = ["zero-shot", "few-shot", "cot"]
    
    for model in models:
        for strategy in strategies:
            output_dir = os.path.join(outputs_path, model, strategy)
            
            if not os.path.exists(output_dir):
                continue
                
            for filename in os.listdir(output_dir):
                if not filename.endswith('.txt'):
                    continue
                
                # Read your model's response
                output_file = os.path.join(output_dir, filename)
                with open(output_file, 'r', errors='ignore') as f:
                    hypothesis = f.read()
                
                # Read GPT-4 ground truth
                gt_file = os.path.join(ground_truth_path, filename)
                if not os.path.exists(gt_file):
                    continue
                with open(gt_file, 'r', errors='ignore') as f:
                    reference = f.read()
                
                # Compute scores
                scores = compute_scores(reference, hypothesis)
                
                results.append({
                    "model": model,
                    "strategy": strategy,
                    "filename": filename,
                    "bertscore": scores["bertscore"],
                    "cosine": scores["cosine"]
                })
                
                print(f"Evaluated {model} | {strategy} | {filename}")
    
    return results


def evaluate_obfuscated():
    results = []
    
    SCHEMES = ["default", "control-flow-flattening", "dead-code-injection", "split-string", "wobfuscator"]
    models = ["gpt-4o", "claude", "gemini"]
    strategies = ["zero-shot", "few-shot", "cot"]
    
    for scheme in SCHEMES:
        ground_truth_path = f"llms-for-code-analysis/results/obfuscated/javascript-data/{scheme}/gpt-4"
        outputs_path = f"outputs/obfuscated/{scheme}"
        
        for model in models:
            for strategy in strategies:
                output_dir = os.path.join(outputs_path, model, strategy)
                
                if not os.path.exists(output_dir):
                    continue
                
                for filename in os.listdir(output_dir):
                    if not filename.endswith('.txt'):
                        continue
                    
                    output_file = os.path.join(output_dir, filename)
                    with open(output_file, 'r', errors='ignore') as f:
                        hypothesis = f.read()
                    
                    gt_file = os.path.join(ground_truth_path, filename)
                    if not os.path.exists(gt_file):
                        continue
                    with open(gt_file, 'r', errors='ignore') as f:
                        reference = f.read()
                    
                    scores = compute_scores(reference, hypothesis)
                    
                    results.append({
                        "model": model,
                        "strategy": strategy,
                        "scheme": scheme,
                        "filename": filename,
                        "bertscore": scores["bertscore"],
                        "cosine": scores["cosine"]
                    })
                    
                    print(f"Evaluated {model} | {strategy} | {scheme} | {filename}")
    
    return results



def save_results(results, filename):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
    return df


if __name__ == "__main__":
    print("=== Evaluating explanation experiments ===")
    explanation_results = evaluate_explanation()
    explanation_df = save_results(explanation_results, "results_explanation.csv")
    
    print("\n=== Evaluating obfuscated experiments ===")
    obfuscated_results = evaluate_obfuscated()
    obfuscated_df = save_results(obfuscated_results, "results_obfuscated.csv")
    
    print("\n=== Summary ===")
    print("\nExplanation results by model and strategy:")
    print(explanation_df.groupby(["model", "strategy"])[["bertscore", "cosine"]].mean().round(4))
    
    print("\nObfuscated results by model and strategy:")
    print(obfuscated_df.groupby(["model", "strategy"])[["bertscore", "cosine"]].mean().round(4))
    
    print("\nObfuscated results by scheme:")
    print(obfuscated_df.groupby(["model", "strategy", "scheme"])[["bertscore", "cosine"]].mean().round(4))
    print("\nAll done!")

