import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
matplotlib.rcParams['font.size'] = 11

# ── Load your results ─────────────────────────────────────────────────────────
# Run this from your CP8320 Project folder
df1 = pd.read_csv('results_explanation.csv')
df2 = pd.read_csv('results_obfuscated.csv')

MODEL_COLORS  = {'gpt-4o': '#2196F3', 'gemini': '#FF9800', 'claude': '#4CAF50'}
MODEL_LABELS  = {'gpt-4o': 'GPT-4o', 'gemini': 'Gemini 2.5 Flash', 'claude': 'Claude Sonnet 4.6'}
STRATEGY_ORDER  = ['zero-shot', 'few-shot', 'cot']
STRATEGY_LABELS = {'zero-shot': 'Zero-Shot', 'few-shot': 'Few-Shot', 'cot': 'CoT'}
MODELS        = ['gpt-4o', 'gemini', 'claude']
SCHEME_ORDER  = ['default', 'dead-code-injection', 'control-flow-flattening', 'split-string', 'wobfuscator']
SCHEME_LABELS = {
    'default':                 'Default',
    'dead-code-injection':     'Dead Code',
    'control-flow-flattening': 'Control Flow',
    'split-string':            'Split String',
    'wobfuscator':             'Wobfuscator',
}

bar_w     = 0.22
group_gap = 0.08
n_models  = len(MODELS)

# ── Figure 1: Explanation BERTScore ──────────────────────────────────────────
exp = df1.groupby(['model', 'strategy'])['bertscore'].mean().round(4).reset_index()
x = [i * (n_models * bar_w + group_gap) for i in range(len(STRATEGY_ORDER))]

fig, ax = plt.subplots(figsize=(8, 4.5))
for mi, model in enumerate(MODELS):
    vals = [exp[(exp['model']==model) & (exp['strategy']==s)]['bertscore'].values[0]
            if len(exp[(exp['model']==model) & (exp['strategy']==s)]) else 0
            for s in STRATEGY_ORDER]
    positions = [xi + mi * bar_w for xi in x]
    bars = ax.bar(positions, vals, width=bar_w, label=MODEL_LABELS[model],
                  color=MODEL_COLORS[model], edgecolor='white', linewidth=0.5)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{v:.3f}', ha='center', va='bottom', fontsize=7.5)

ax.set_xticks([xi + (n_models-1)*bar_w/2 for xi in x])
ax.set_xticklabels([STRATEGY_LABELS[s] for s in STRATEGY_ORDER])
ax.set_ylabel('BERTScore (F1)')
ax.set_ylim(0.76, 0.85)
ax.legend(loc='lower right', fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figure1_explanation.pdf', bbox_inches='tight')
plt.savefig('figure1_explanation.png', dpi=180, bbox_inches='tight')
plt.show()
print("Figure 1 saved.")

# ── Figure 2: Obfuscated BERTScore by strategy ───────────────────────────────
obs = df2.groupby(['model', 'strategy'])['bertscore'].mean().round(4).reset_index()
x = [i * (n_models * bar_w + group_gap) for i in range(len(STRATEGY_ORDER))]

fig, ax = plt.subplots(figsize=(8, 4.5))
for mi, model in enumerate(MODELS):
    vals = [obs[(obs['model']==model) & (obs['strategy']==s)]['bertscore'].values[0]
            if len(obs[(obs['model']==model) & (obs['strategy']==s)]) else 0
            for s in STRATEGY_ORDER]
    positions = [xi + mi * bar_w for xi in x]
    bars = ax.bar(positions, vals, width=bar_w, label=MODEL_LABELS[model],
                  color=MODEL_COLORS[model], edgecolor='white', linewidth=0.5)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{v:.3f}', ha='center', va='bottom', fontsize=7.5)

ax.set_xticks([xi + (n_models-1)*bar_w/2 for xi in x])
ax.set_xticklabels([STRATEGY_LABELS[s] for s in STRATEGY_ORDER])
ax.set_ylabel('BERTScore (F1)')
ax.set_ylim(0.79, 0.87)
ax.legend(loc='lower right', fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figure2_obfuscated.pdf', bbox_inches='tight')
plt.savefig('figure2_obfuscated.png', dpi=180, bbox_inches='tight')
plt.show()
print("Figure 2 saved.")

# ── Figure 3: Obfuscated BERTScore by scheme ─────────────────────────────────
sch   = df2.groupby(['model', 'scheme'])['bertscore'].mean().round(4).reset_index()
bar_w2 = 0.22
gap2   = 0.10
x3 = [i * (n_models * bar_w2 + gap2) for i in range(len(SCHEME_ORDER))]

fig, ax = plt.subplots(figsize=(10, 4.8))
for mi, model in enumerate(MODELS):
    vals = [sch[(sch['model']==model) & (sch['scheme']==s)]['bertscore'].values[0]
            if len(sch[(sch['model']==model) & (sch['scheme']==s)]) else 0
            for s in SCHEME_ORDER]
    positions = [xi + mi * bar_w2 for xi in x3]
    bars = ax.bar(positions, vals, width=bar_w2, label=MODEL_LABELS[model],
                  color=MODEL_COLORS[model], edgecolor='white', linewidth=0.5)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
                f'{v:.3f}', ha='center', va='bottom', fontsize=7)

ax.set_xticks([xi + (n_models-1)*bar_w2/2 for xi in x3])
ax.set_xticklabels([SCHEME_LABELS[s] for s in SCHEME_ORDER])
ax.set_ylabel('BERTScore (F1)')
ax.set_ylim(0.79, 0.87)
ax.legend(loc='lower right', fontsize=9)
ax.grid(axis='y', linestyle='--', alpha=0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figure3_schemes.pdf', bbox_inches='tight')
plt.savefig('figure3_schemes.png', dpi=180, bbox_inches='tight')
plt.show()
print("Figure 3 saved.")
print("All done!")