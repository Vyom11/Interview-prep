# Module 11 — Hyperparameter Tuning and Training Stability

> **Focus pillars:** Optimization stability · Convergence · Regularization · Initialization · Debugging training failures

---

## Table of Contents

1. [Why This Module Matters](#why-this-module-matters)
2. [ELI5](#eli5)
3. [Core Concepts](#core-concepts)
4. [Math Intuition](#math-intuition)
5. [Key Formulas and Equations](#key-formulas-and-equations)
6. [Algorithms Breakdown](#algorithms-breakdown)
7. [Visual Mental Models](#visual-mental-models)
8. [Real-World Applications](#real-world-applications)
9. [Engineering Insights](#engineering-insights)
10. [Production Notes](#production-notes)
11. [Common Mistakes](#common-mistakes)
12. [Best Practices](#best-practices)
13. [Minimal Practical Workflow](#minimal-practical-workflow)
14. [Python Ecosystem](#python-ecosystem)
15. [Interview Questions](#interview-questions)
16. [How to Explain in an Interview](#how-to-explain-in-an-interview)
17. [Summary Cheatsheet](#summary-cheatsheet)

---

## Why This Module Matters

Training a neural network is not a single-step operation — it is an ongoing negotiation between your model, your data, and the optimization landscape. Most practitioners who call deep learning "unpredictable" simply haven't learned to read its signals yet.

This module bridges theory and the engineering reality of getting models to **actually converge**:

| Pain Point | Module Answer |
|---|---|
| Loss explodes to `NaN` on step 1 | Gradient clipping + He/Xavier init |
| Loss plateaus early | LR scheduling + momentum optimizers |
| Model memorizes training set | Dropout, weight decay, early stopping |
| Results change across runs | Seed control + stability experiments |
| Tuning feels like guessing | Random search + principled grid search |

> **Core thesis:** Every training failure has a root cause. This module gives you the diagnostic vocabulary to find and fix it.

---

## ELI5

Imagine you're learning to ride a bike on a hilly road. The **hill** is your loss landscape.

- **Vanishing gradients** = your pedals barely move the bike (no learning signal reaches early layers)
- **Exploding gradients** = your pedals spin so fast you crash (unstable updates)
- **Weight initialization** = where on the hill you start — bad start → trapped in a pothole
- **Learning rate** = how big each pedal stroke is — too big → zigzag off-road; too small → never reach the bottom
- **Momentum** = your bike's speed carries you through small bumps (local minima)
- **Batch normalization** = re-leveling the road at every checkpoint so the terrain stays consistent
- **Dropout** = randomly removing spokes from your wheel so you learn to ride without relying on any one spoke
- **Weight decay** = a slight headwind that keeps you from going too fast in any direction (prevents overfit)
- **Learning rate schedule** = starting with big pedal strokes and gradually taking smaller, precise ones
- **Early stopping** = getting off the bike before you ride back up the hill (overfit)

---

## Core Concepts

### 1. Vanishing and Exploding Gradients

During backpropagation, gradients are computed by chaining derivatives across layers. In deep networks this multiplicative chain causes two failure modes:

**Vanishing gradients:**  
When activation derivatives are small (< 1), repeated multiplication shrinks the gradient exponentially toward 0. Early layers receive essentially zero gradient → they don't learn.

*Symptoms:*
- Loss stops decreasing after first few epochs
- Weights in early layers barely change
- Activations saturate near 0 or 1 (sigmoid/tanh networks)

**Exploding gradients:**  
When weight matrices have large singular values or gradients amplify across layers, gradients grow exponentially → weight updates become enormous → loss diverges.

*Symptoms:*
- Loss becomes `NaN` or `inf` rapidly
- Weight norm grows unboundedly
- Training loss oscillates wildly

**Mitigation toolkit:**

| Problem | Solution |
|---|---|
| Vanishing | ReLU activations, residual connections, careful init |
| Exploding | Gradient clipping, smaller LR, weight initialization |
| Both | Batch normalization, LSTM/GRU cells (for RNNs) |

---

### 2. Weight Initialization

The starting point of your parameters matters enormously. Poor initialization causes:
- Symmetry breaking failure (all neurons learn the same thing)
- Immediate vanishing/exploding activations

**Zero initialization — always wrong for hidden layers:**  
All neurons produce identical gradients → the network can never diversify.

**Random small values — better but fragile:**  
Works for shallow networks. Scale matters a lot.

#### Xavier (Glorot) Initialization

Designed for **sigmoid and tanh** activations. Balances variance of activations and gradients through the network.

```
W ~ Uniform(-√(6/(n_in + n_out)), +√(6/(n_in + n_out)))
```

Or equivalently from a normal distribution:

```
W ~ Normal(0, √(2 / (n_in + n_out)))
```

*Intuition:* Keeps the variance of activations approximately equal across layers, so neither signals nor gradients vanish/explode.

#### He Initialization

Designed for **ReLU activations**. ReLU zeroes out half the neurons, so variance needs to be doubled to compensate.

```
W ~ Normal(0, √(2 / n_in))
```

*Intuition:* Accounts for the ~50% activation kill of ReLU. Maintains signal strength through very deep networks.

| Activation | Recommended Init | Variance Factor |
|---|---|---|
| sigmoid / tanh | Xavier | `2 / (n_in + n_out)` |
| ReLU | He | `2 / n_in` |
| Leaky ReLU | He (adjusted) | `2 / ((1+α²) * n_in)` |
| SELU | LeCun | `1 / n_in` |

---

### 3. Regularization Techniques

Regularization fights overfitting by constraining the model's capacity or adding noise.

#### Dropout

During training, randomly zero out neurons with probability `p` at each forward pass. Forces the network to learn **redundant representations** — no single neuron can be relied upon.

- At inference: all neurons are active, weights scaled by `(1 - p)` (or use inverted dropout which scales during training)
- Typical values: `p = 0.5` for fully-connected layers, `p = 0.1–0.2` for convolutional layers
- **Does not work well with Batch Normalization** — they conflict (BN reduces internal covariate shift while dropout reintroduces noise into BN statistics)

#### Weight Decay (L2 Regularization)

Adds a penalty term to the loss proportional to the squared magnitude of weights:

```
L_total = L_task + (λ/2) * Σ w²
```

Gradient contribution: `∂L/∂w += λw`

Effect on update: `w ← w - η(∂L/∂w + λw) = w(1 - ηλ) - η∂L/∂w`

The factor `(1 - ηλ)` is the *weight decay* — weights shrink toward zero every step unless the gradient pushes back. Encourages sparse, low-magnitude weight solutions.

> ⚠️ **AdamW vs Adam:** Standard Adam with L2 regularization does not apply true weight decay because adaptive learning rates scale the regularization term unevenly. **AdamW** decouples weight decay from the gradient update, making it the preferred choice for transformers and modern architectures.

#### Early Stopping

Monitor validation loss during training. Stop when validation loss stops improving for `patience` epochs.

```
best_val_loss = ∞
patience_counter = 0

for epoch in training:
    val_loss = evaluate()
    if val_loss < best_val_loss - min_delta:
        best_val_loss = val_loss
        save_checkpoint()
        patience_counter = 0
    else:
        patience_counter += 1
        if patience_counter >= patience:
            restore_best_checkpoint()
            break
```

*Important: always restore the best checkpoint, not the last.*

#### Data Augmentation

Artificially expand training data by applying label-preserving transforms:

| Domain | Augmentations |
|---|---|
| Vision | Random crop, flip, rotation, color jitter, cutout, mixup, RandAugment |
| NLP | Synonym replacement, back-translation, random deletion |
| Audio | Time stretch, pitch shift, noise injection, SpecAugment |
| Tabular | SMOTE (for class imbalance), Gaussian noise injection |

---

### 4. Batch Normalization

Normalizes the pre-activation (or post-activation, debated) of each layer across the mini-batch:

```
μ_B = (1/m) Σ x_i                     # batch mean
σ²_B = (1/m) Σ (x_i - μ_B)²           # batch variance
x̂_i = (x_i - μ_B) / √(σ²_B + ε)      # normalize
y_i = γ * x̂_i + β                    # scale and shift (learnable)
```

**Why it helps:**
1. Reduces **internal covariate shift** — the distribution of layer inputs no longer shifts every update
2. Provides implicit regularization (batch statistics add noise)
3. Allows **higher learning rates** — less sensitivity to initialization
4. Smooths the loss landscape

**Inference behavior:** Uses running mean/variance computed during training (not batch stats). This is why `model.train()` vs `model.eval()` matters in PyTorch.

**Failure modes:**
- Very small batch sizes (< 8) → noisy batch statistics → use Group Norm or Layer Norm instead
- Variable-length sequences → use Layer Norm
- Placed after dropout → ordering matters for stability

---

### 5. Optimizers

#### SGD (Stochastic Gradient Descent)

Pure gradient descent on mini-batches:

```
w ← w - η * ∇L(w)
```

- Simple, well-understood
- Can escape sharp minima through noise
- Requires careful LR tuning
- Slow on ill-conditioned loss surfaces (narrow valleys)

#### SGD with Momentum

Accumulates a velocity vector in directions of consistent gradient:

```
v ← β * v - η * ∇L(w)
w ← w + v
```

Typical `β = 0.9`. Effect: damps oscillations in high-curvature dimensions, accelerates in consistent gradient direction. Nesterov momentum (lookahead gradient) often converges faster.

#### Adam (Adaptive Moment Estimation)

Combines momentum (first moment) with per-parameter adaptive learning rates (second moment):

```
m_t = β₁ * m_{t-1} + (1 - β₁) * g_t          # 1st moment (momentum)
v_t = β₂ * v_{t-1} + (1 - β₂) * g_t²         # 2nd moment (adaptive scale)

m̂_t = m_t / (1 - β₁ᵗ)                         # bias correction
v̂_t = v_t / (1 - β₂ᵗ)                         # bias correction

w ← w - η * m̂_t / (√v̂_t + ε)
```

Default hyperparameters: `β₁ = 0.9`, `β₂ = 0.999`, `ε = 1e-8`

**Why Adam converges faster:**
- Each parameter gets its own effective learning rate
- `√v̂_t` in the denominator normalizes by recent gradient magnitude → large gradients → small effective LR; small gradients → large effective LR
- Bias correction prevents artificially small updates at the start

**Adam vs SGD — the generalization gap:**  
Adam often converges faster but to sharper minima with worse generalization than SGD+momentum in some vision tasks. AdamW + LR warmup + cosine decay is the modern standard for transformers.

| Optimizer | Convergence Speed | Generalization | Sensitivity to LR |
|---|---|---|---|
| SGD | Slow | Often best (CV) | High |
| SGD + Momentum | Medium | Good | Medium |
| Adam | Fast | Good (NLP) | Low |
| AdamW | Fast | Best (transformers) | Low |

---

### 6. Learning Rate Scheduling

The learning rate is the most impactful hyperparameter. A fixed LR is almost always suboptimal.

**Step Decay:**  
`η_t = η_0 * γ^(floor(t / step_size))`  
Reduces LR by factor `γ` every fixed number of epochs.

**Cosine Annealing:**  
`η_t = η_min + (1/2)(η_max - η_min)(1 + cos(πt/T))`  
Smooth decay; often used with warm restarts (SGDR).

**Warmup + Cosine Decay (Transformer standard):**  
LR linearly increases for `warmup_steps`, then cosine-decays. Critical for transformer stability — without warmup, early large updates corrupt embeddings.

**Cyclical LR (CLR):**  
Oscillates between `lr_min` and `lr_max`. Lets the optimizer escape saddle points and sharp minima periodically.

**One-Cycle Policy:**  
One cosine cycle from `lr_min → lr_max → very_low_lr`. Combined with momentum cycling — state of the art for fast training.

---

### 7. Mini-batch Training and Batch Size Tradeoffs

**Why not use full-batch gradient descent?**
- Memory prohibitive for large datasets
- No noise → more likely to converge to sharp minima (worse generalization)

**Why not use batch size = 1 (pure SGD)?**
- Maximum noise → training is unstable
- No GPU parallelism utilization

**The batch size-learning rate relationship:**  
Linear scaling rule: if batch size increases by `k×`, increase LR by `k×` (with warmup). This preserves the effective learning rate per sample.

| Batch Size | Training Speed | Gradient Noise | Generalization | Memory |
|---|---|---|---|---|
| Small (8–32) | Slow (less parallelism) | High | Often better | Low |
| Medium (64–256) | Balanced | Medium | Good | Medium |
| Large (512+) | Fast | Low | Can degrade without LR scaling | High |

> **The sharp minima hypothesis (Keskar et al., 2016):** Large batch training converges to sharp minima (narrow, high-curvature) while small batch training finds flat minima. Flat minima generalize better because small perturbations to weights don't change the loss much.

---

### 8. Hyperparameter Search

#### Grid Search

Exhaustively evaluates all combinations of a predefined grid.

```python
# 3 LR values × 3 dropout values × 2 batch sizes = 18 trials
param_grid = {
    'lr':      [1e-4, 1e-3, 1e-2],
    'dropout': [0.2, 0.4, 0.6],
    'batch':   [32, 128]
}
```

- ✅ Reproducible, exhaustive in grid
- ❌ Exponential scaling — 5 params × 5 values = 3125 trials
- ❌ Wastes compute on unimportant hyperparameters

#### Random Search

Samples hyperparameters randomly from defined distributions.

```python
param_dist = {
    'lr':      loguniform(1e-5, 1e-1),   # log scale for LR!
    'dropout': uniform(0.1, 0.6),
    'batch':   choice([16, 32, 64, 128])
}
```

- ✅ More efficient than grid — each trial explores a unique slice of each param
- ✅ Easily parallelizable
- ✅ Better coverage of important hyperparameters
- ❌ No exploitation of promising regions (Bayesian search does this)

**Key insight (Bergstra & Bengio, 2012):** In any search space, only a few hyperparameters actually matter. Random search is more likely to find good values for those important ones because it doesn't waste trials on the unimportant dimensions.

> For most practical tuning: **random search with 20–50 trials** outperforms grid search and is far cheaper than Bayesian optimization at small scale.

---

## Math Intuition

### Why vanishing gradients happen — a concrete chain

For a 5-layer sigmoid network, the gradient of the loss w.r.t. layer 1 weights involves:

```
∂L/∂W₁ = ∂L/∂a₅ · σ'(z₅)·W₅ · σ'(z₄)·W₄ · σ'(z₃)·W₃ · σ'(z₂)·W₂ · σ'(z₁)
```

The sigmoid derivative `σ'(z) = σ(z)(1-σ(z))` has a **maximum of 0.25**.

With 5 layers: `0.25⁵ ≈ 0.001` — gradient is 1000× smaller at layer 1. With 20 layers: `0.25²⁰ ≈ 10⁻¹²`. Layer 1 receives effectively zero learning signal.

ReLU derivative is either 0 or 1 — no exponential shrinkage (though dead ReLU neurons can still cause vanishing).

### Xavier init derivation intuition

We want `Var(output) = Var(input)` through a linear layer `y = Wx`.

```
Var(y_i) = n_in * Var(w) * Var(x)    # assuming independence
```

For `Var(y) = Var(x)` we need `Var(w) = 1/n_in`.

Going backward (for gradient flow): `Var(w) = 1/n_out`.

Xavier splits the difference: `Var(w) = 2/(n_in + n_out)`.

He init: ReLU zeroes out ~half the neurons, effectively halving the variance. Compensation: `Var(w) = 2/n_in`.

### Adam's bias correction

At step 1 with zero-initialized moments:

```
m_1 = (1 - β₁) * g₁ = 0.1 * g₁    (β₁ = 0.9)
```

Without correction: the effective learning rate is 10× smaller than intended. Bias correction `m̂_1 = m_1 / (1 - 0.9¹) = m_1 / 0.1 = g₁` restores the correct scale. This matters most in the first ~100 steps.

---

## Key Formulas and Equations

### Gradient Flow

```
∂L/∂W^(l) = δ^(l) · (a^(l-1))ᵀ

δ^(l) = ((W^(l+1))ᵀ δ^(l+1)) ⊙ f'(z^(l))     # backprop signal
```

### Gradient Clipping

```
# Norm clipping (preferred)
g_clipped = g * min(1, clip_value / ||g||₂)

# Value clipping (simpler, cruder)
g_clipped = clip(g, -clip_value, clip_value)
```

### Dropout (inverted)

```
# Training
mask ~ Bernoulli(1 - p)
h_out = (h * mask) / (1 - p)    # scale up during training

# Inference
h_out = h                         # no scaling needed
```

### Weight Decay Update Rule

```
w_t = w_{t-1} * (1 - η * λ) - η * ∇L(w_{t-1})
```

### Batch Normalization (full)

```
# Forward
μ = mean(x_batch)
σ² = var(x_batch) + ε
x_norm = (x - μ) / √σ²
y = γ * x_norm + β

# Backward: gradients flow through γ, β, and the normalization
# Running stats for inference:
μ_run = (1 - momentum) * μ_run + momentum * μ_batch
```

### Cosine Annealing

```
η_t = η_min + (η_max - η_min)/2 * (1 + cos(π * t / T_max))
```

### Adam Update

```
g_t = ∇L(w_t)
m_t = β₁ m_{t-1} + (1 - β₁) g_t
v_t = β₂ v_{t-1} + (1 - β₂) g_t²
m̂_t = m_t / (1 - β₁ᵗ)
v̂_t = v_t / (1 - β₂ᵗ)
w_{t+1} = w_t - η * m̂_t / (√v̂_t + ε)
```

### Random Search — Log-Uniform Sampling for LR

```python
lr = 10 ** np.random.uniform(-5, -1)   # samples from [1e-5, 1e-1] on log scale
```

---

## Algorithms Breakdown

### Backpropagation + Gradient Clipping (Pseudo-code)

```
for batch in dataloader:
    # Forward pass
    loss = model(batch)
    
    # Backward pass
    optimizer.zero_grad()
    loss.backward()
    
    # Gradient clipping (BEFORE optimizer step)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
    
    # Parameter update
    optimizer.step()
    scheduler.step()
```

> ⚠️ **Order matters:** clip gradients AFTER `.backward()` and BEFORE `.step()`.

### Early Stopping (Pseudo-code)

```
best_val_loss = float('inf')
patience = 10
counter = 0

for epoch in range(max_epochs):
    train_one_epoch(model, train_loader, optimizer)
    val_loss = evaluate(model, val_loader)
    
    if val_loss < best_val_loss - delta:
        best_val_loss = val_loss
        save_checkpoint(model, 'best_model.pt')
        counter = 0
    else:
        counter += 1
    
    if counter >= patience:
        print(f"Early stopping at epoch {epoch}")
        load_checkpoint(model, 'best_model.pt')
        break
```

### Hyperparameter Search (Random Search Skeleton)

```python
import optuna  # or manual loop

def objective(trial):
    lr = trial.suggest_float('lr', 1e-5, 1e-1, log=True)
    dropout = trial.suggest_float('dropout', 0.1, 0.6)
    wd = trial.suggest_float('weight_decay', 1e-6, 1e-2, log=True)
    
    model = build_model(dropout=dropout)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    
    return train_and_evaluate(model, optimizer)

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=50)
```

---

## Visual Mental Models

### Loss Landscape Navigation

```
         Sharp Minima              Flat Minima
         (large batch)             (small batch)

         /\                        /‾‾‾‾‾\
        /  \                      /        \
  _____/    \_____          _____/          \_____

  • High curvature              • Low curvature
  • Hurts generalization        • Better generalization
  • LR sensitivity high         • More robust to perturbation
```

### Gradient Flow Through Network

```
  Input → [L1] → [L2] → [L3] → [L4] → [L5] → Loss
  
  Vanishing:   ←←← 0.001 ←← 0.01 ←← 0.1 ←← 1.0  (no signal reaches L1)
  Exploding:   ←←← 10000 ←← 1000 ←← 100 ←← 10   (L1 updates explode)
  Healthy:     ←←←   0.7 ←←  0.8 ←←  0.9 ←← 1.0  (consistent signal)
```

### Adam Adaptive Learning Rates

```
Parameter A: sparse gradients (rarely updated)
  v_t → small → η_effective = η/√small → LARGE effective LR ✓

Parameter B: dense gradients (frequently updated)  
  v_t → large → η_effective = η/√large → SMALL effective LR ✓
```

### Batch Normalization Effect

```
Without BN:
  Layer output distribution shifts each batch
  → Next layer must constantly re-adapt
  → Need lower LR, careful init

With BN:
  Each layer's input is re-centered to N(0,1) before scaling
  → Stable training signal every batch
  → Higher LR tolerated
  → Initialization less critical
```

### Dropout as Ensemble

```
Dropout creates 2^N possible sub-networks (N = neurons)

Training:                    Inference:
[●]─[●]─[○]─[●]            [●]─[●]─[●]─[●]
[●]─[○]─[●]─[●]   →→→     [●]─[●]─[●]─[●]
[●]─[●]─[●]─[○]            [●]─[●]─[●]─[●]

Each forward pass = different sub-network
Final model = implicit average of all sub-networks
```

### Learning Rate Schedule Comparison

```
LR
│  ┌──── One-Cycle Policy ────┐
│  │                           \
│  │                            \____
│  │  ╱╲ ╱╲ ╱╲ Cyclical LR     
│  │ ╱  ╲╱  ╲╱  ╲
│  │╱                           Cosine Annealing
│  ╲___________________________╲___
│
└─────────────────────────────────── Steps
```

---

## Real-World Applications

### Computer Vision (ResNet / EfficientNet)

- **Init:** He initialization (ReLU activations)
- **Optimizer:** SGD + momentum (0.9) with cosine decay
- **Regularization:** Weight decay (1e-4), random crop, horizontal flip, mixup
- **BN:** After every conv, before activation
- **Batch size:** 256–1024 with linear LR scaling

### NLP / Transformers (BERT / GPT)

- **Init:** Xavier for attention, He for FFN layers
- **Optimizer:** AdamW (`β₁=0.9, β₂=0.999, ε=1e-8`)
- **LR schedule:** Linear warmup (10% of steps) + linear/cosine decay
- **Regularization:** Dropout (0.1), weight decay (0.01), gradient clipping (1.0)
- **BN → Layer Norm** (BN doesn't work with variable-length sequences)

### Reinforcement Learning

- **Init:** Orthogonal initialization (preserves gradient norms in policy networks)
- **Optimizer:** Adam with very small LR (3e-4)
- **Stability:** Gradient clipping critical; reward normalization

### Time Series (LSTMs)

- **Init:** Orthogonal (recurrent weights), Glorot (input weights)
- **Exploding gradients:** Clip at norm 5.0 (standard for RNNs)
- **Regularization:** Variational dropout (same mask every timestep)

---

## Engineering Insights

### Diagnosing Training Failures — Decision Tree

```
Loss is NaN or inf immediately?
  → Check init (zeros?) → Check LR (too high?) → Check data (NaN in inputs?)
  
Loss decreases then flatlines early?
  → LR too low? → Try 10× LR
  → Gradient vanishing? → Check activation saturation, use BN
  → Dead ReLUs? → Check weight init, use leaky ReLU

Train loss low, val loss high (overfit)?
  → Increase dropout
  → Add weight decay
  → Get more data / stronger augmentation
  → Reduce model size

Val loss better than train loss?
  → Dropout is ON during evaluation — check model.eval()
  → BN using batch stats at test time — check model.eval()

Training unstable / oscillating?
  → Reduce LR
  → Add gradient clipping
  → Increase batch size
  → Add/adjust BN
```

### Gradient Monitoring in Practice

```python
# Log gradient norms per layer — catches vanishing/exploding early
for name, param in model.named_parameters():
    if param.grad is not None:
        writer.add_scalar(f'grad_norm/{name}', 
                          param.grad.norm(), global_step)
```

A healthy model shows relatively uniform gradient norms across layers. If early layers are consistently 100× smaller → vanishing. If any layer is 100× larger → exploding.

### The Learning Rate Range Test (Smith, 2017)

```python
# Increase LR exponentially, plot loss vs LR
# LR just before loss explodes = good starting LR for one-cycle

lrs = np.logspace(-7, 0, 100)
for lr in lrs:
    set_lr(optimizer, lr)
    loss = train_one_step(batch)
    record(lr, loss)

# Plot: loss starts decreasing around lr* → use lr* / 10 as max LR
```

### Batch Norm vs Layer Norm vs Group Norm

| Norm Type | Normalizes Over | Best For |
|---|---|---|
| Batch Norm | Batch dimension | CNNs, large batches |
| Layer Norm | Feature dimension | Transformers, RNNs |
| Group Norm | Groups of channels | Small batch CNNs |
| Instance Norm | Each sample individually | Style transfer |

---

## Production Notes

### Reproducibility

```python
import torch, numpy as np, random

def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False  # trades speed for determinism
```

### Checkpoint Strategy

```python
# Save: model state, optimizer state, scheduler state, epoch, val_loss
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'scheduler_state_dict': scheduler.state_dict(),
    'val_loss': val_loss,
}, 'checkpoint.pt')
```

> Always save optimizer and scheduler state — resuming without them restarts momentum/LR schedule history.

### Mixed Precision Training (AMP)

```python
scaler = torch.cuda.amp.GradScaler()

with torch.cuda.amp.autocast():
    loss = model(batch)

scaler.scale(loss).backward()
scaler.unscale_(optimizer)
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
scaler.step(optimizer)
scaler.update()
```

GradScaler handles FP16 gradient underflow — critical when using mixed precision.

### Monitoring Tools

| Tool | Use Case |
|---|---|
| TensorBoard | Loss curves, gradient histograms, weight distributions |
| Weights & Biases | Experiment tracking, hyperparameter sweeps |
| Optuna | Bayesian / random / grid search with pruning |
| PyTorch Profiler | GPU utilization, bottleneck identification |

---

## Common Mistakes

### ❌ Mistake 1: Forgetting `model.eval()` during validation

```python
# WRONG — dropout and BN use train behavior
val_loss = evaluate(model, val_loader)  

# RIGHT
model.eval()
with torch.no_grad():
    val_loss = evaluate(model, val_loader)
model.train()
```

### ❌ Mistake 2: Clipping gradients after `optimizer.step()`

The entire point is to clip before the update modifies weights. Post-step clipping does nothing.

### ❌ Mistake 3: Using weight decay with Adam instead of AdamW

```python
# WRONG — L2 regularization inside Adam is NOT true weight decay
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)

# RIGHT — decoupled weight decay
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
```

### ❌ Mistake 4: Grid search on LR in linear scale

```python
# WRONG — most values are clustered near 0.1
lr_grid = [0.01, 0.02, 0.03, ..., 0.1]

# RIGHT — log scale covers orders of magnitude
lr_grid = [1e-4, 1e-3, 1e-2, 1e-1]
```

### ❌ Mistake 5: Applying dropout to BN layers

Dropout before BN corrupts the batch statistics. Apply dropout only after BN, or avoid using both on the same feature maps.

### ❌ Mistake 6: Not restoring best checkpoint in early stopping

```python
# WRONG — model state at patience expiry might be worse than best
model.load_state_dict(last_state)

# RIGHT — restore explicitly
model.load_state_dict(torch.load('best_model.pt')['model_state_dict'])
```

### ❌ Mistake 7: Using the same LR for fine-tuning as pre-training

Fine-tuning pre-trained models requires LR 10×–100× smaller. Large LR destroys learned representations. Use **discriminative learning rates** (lower LR for early layers, higher for final layers).

---

## Best Practices

### Initialization

- ✅ Use **He init** for ReLU/LeakyReLU architectures
- ✅ Use **Xavier init** for sigmoid/tanh architectures
- ✅ Use **orthogonal init** for RNNs and RL policy networks
- ✅ For transformers: follow the source paper's exact init (e.g., GPT-2 scales init by `1/√(2*num_layers)` for residual branches)

### Optimization

- ✅ Default to **AdamW** for NLP/transformers
- ✅ Default to **SGD + momentum** for vision when final accuracy matters
- ✅ Always use **LR scheduling** — cosine annealing + warmup is the safest default
- ✅ Apply **gradient clipping** (norm=1.0) whenever loss is unstable
- ✅ Tune LR first — it's the most impactful hyperparameter

### Regularization

- ✅ Apply weight decay before other regularization
- ✅ Use **dropout after fully-connected layers**, not after BN layers
- ✅ **Early stopping** with `patience=10–20` is almost always worth it
- ✅ **Data augmentation** is the highest ROI regularization for small datasets

### Batch Normalization

- ✅ Use BN by default in CNNs
- ✅ Switch to Layer Norm for transformers and variable-length inputs
- ✅ Always call `model.train()` / `model.eval()` correctly
- ✅ Monitor running statistics divergence in production (distribution shift)

### Hyperparameter Search

- ✅ Use **log scale for LR and weight decay**
- ✅ **Random search over 20–50 trials** before attempting Bayesian optimization
- ✅ Fix random seed across trials for fair comparison
- ✅ Log everything — you will need to reproduce that one great run

---

## Minimal Practical Workflow

```python
import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR

# 1. Model with proper initialization
def build_model():
    model = MyNetwork()
    for m in model.modules():
        if isinstance(m, nn.Linear):
            nn.init.kaiming_normal_(m.weight, nonlinearity='relu')
            nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Conv2d):
            nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.ones_(m.weight)
            nn.init.zeros_(m.bias)
    return model

# 2. Optimizer + scheduler
model = build_model()
optimizer = AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
scheduler = CosineAnnealingLR(optimizer, T_max=num_epochs)

# 3. Training loop with best practices
best_val_loss = float('inf')
patience_counter = 0
PATIENCE = 10

for epoch in range(max_epochs):
    # --- Train ---
    model.train()
    for batch in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(batch['x']), batch['y'])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # clip
        optimizer.step()
    
    scheduler.step()
    
    # --- Validate ---
    model.eval()
    with torch.no_grad():
        val_loss = sum(criterion(model(b['x']), b['y']) for b in val_loader)
    
    # --- Early stopping ---
    if val_loss < best_val_loss - 1e-4:
        best_val_loss = val_loss
        torch.save(model.state_dict(), 'best.pt')
        patience_counter = 0
    else:
        patience_counter += 1
        if patience_counter >= PATIENCE:
            print(f"Early stop at epoch {epoch}")
            break

model.load_state_dict(torch.load('best.pt'))
```

---

## Python Ecosystem

| Library / Tool | Purpose | Key APIs |
|---|---|---|
| **PyTorch** | Core framework | `nn.init`, `optim.AdamW`, `clip_grad_norm_`, `GradScaler` |
| **PyTorch Lightning** | Training loop abstraction | `Trainer`, `ModelCheckpoint`, `EarlyStopping` |
| **Optuna** | Hyperparameter optimization | `study.optimize`, `trial.suggest_float`, pruning |
| **Weights & Biases** | Experiment tracking | `wandb.init`, `wandb.log`, sweeps |
| **TensorBoard** | Loss/gradient visualization | `SummaryWriter`, `add_scalar`, `add_histogram` |
| **scikit-learn** | Grid/random search (sklearn models) | `GridSearchCV`, `RandomizedSearchCV` |
| **Ray Tune** | Distributed hyperparameter search | `tune.run`, `ASHAScheduler` |
| **Hydra** | Config management for experiments | `@hydra.main`, `cfg` composition |

### Quick Reference — PyTorch Scheduler Cheatsheet

```python
from torch.optim.lr_scheduler import (
    StepLR,                    # step decay
    CosineAnnealingLR,         # cosine annealing
    CosineAnnealingWarmRestarts,  # SGDR
    OneCycleLR,                # one-cycle policy (best default for CV)
    ReduceLROnPlateau,         # reduce when val metric plateaus
    LinearLR,                  # linear warmup
    SequentialLR,              # chain schedulers (warmup → cosine)
)

# Modern transformer training: warmup + cosine
warmup = LinearLR(optimizer, start_factor=0.1, total_iters=warmup_steps)
cosine = CosineAnnealingLR(optimizer, T_max=total_steps - warmup_steps)
scheduler = SequentialLR(optimizer, [warmup, cosine], milestones=[warmup_steps])
```

---

## Interview Questions

### Conceptual

**Q1. Why do vanishing gradients occur with sigmoid activations in deep networks?**  
Sigmoid derivative ≤ 0.25. In a 10-layer network, the chain rule multiplies 10 such terms: `0.25^10 ≈ 10^-6`. Gradient reaching layer 1 is 1 million times smaller than at layer 10 → effectively no learning signal.

**Q2. What is the difference between Xavier and He initialization? When would you use each?**  
Xavier: `Var(w) = 2/(n_in + n_out)` — preserves variance for symmetric activations (sigmoid, tanh). He: `Var(w) = 2/n_in` — compensates for ~50% kill rate of ReLU. Use He for ReLU networks, Xavier for sigmoid/tanh.

**Q3. Why is AdamW preferred over Adam with L2 regularization?**  
In Adam, the adaptive denominator `√v̂_t` scales the gradient and the L2 regularization term together. This means parameters with large gradients receive less effective regularization. AdamW decouples weight decay from the adaptive scaling, applying `w ← w*(1 - η*λ)` independently of gradient magnitude.

**Q4. How does batch normalization help training stability?**  
BN normalizes activations to zero mean and unit variance per batch, then applies learnable scale/shift. This (1) reduces internal covariate shift so each layer sees a stable input distribution, (2) smooths the loss landscape enabling higher LR, (3) provides implicit regularization through batch statistics noise.

**Q5. Why is random search often better than grid search?**  
In a hyperparameter space with unimportant dimensions, grid search wastes most evaluations exploring those dimensions. Random search covers the important dimensions more efficiently — each trial is unique in every dimension. Bergstra & Bengio showed random search is almost always better for the same number of trials.

### Debugging Scenarios

**Q6. Your model's loss is `NaN` after 2 steps. What do you check first?**  
1. Input data — contains NaN/inf? 2. Loss function — log of zero? division by zero? 3. Learning rate — is it absurdly large? 4. Weight initialization — zeros/identical values? 5. Add gradient clipping immediately.

**Q7. Your training loss is 0.01 but validation loss is 0.8. What's happening and how do you fix it?**  
Classic overfitting. Fixes: increase dropout, add/increase weight decay, enable early stopping, add data augmentation, reduce model capacity, get more training data.

**Q8. After 5 epochs your loss stops improving completely. What do you investigate?**  
1. LR too low — try 10× increase 2. LR too high and it's oscillating — try 10× decrease 3. Dead ReLUs — check activation statistics 4. Gradient vanishing — check gradient norms 5. Data pipeline issue — verify batches are correct.

---

## How to Explain in an Interview

### "Walk me through how you would debug a training run that won't converge."

> *"My debugging follows a systematic checklist. First, I look at the loss curve — is it NaN immediately (initialization or LR problem), decreasing then plateauing (vanishing gradients or too-low LR), or oscillating wildly (too-high LR or exploding gradients)?*
>
> *Next I check gradient norms across layers. If early layers show near-zero gradients while later layers are healthy, that's vanishing — I'd switch to He init, add batch norm, or use residual connections. If any layer shows very large gradient norms, I add gradient clipping.*
>
> *For the optimizer, I verify weight initialization matches the activation function, learning rate is on the right order of magnitude (I use the LR range test), and I'm using a scheduler. If training is stable but generalization is poor, I add regularization — dropout and weight decay first, then stronger augmentation.*
>
> *Throughout all of this, I'm logging gradient norms, weight norms, and activation statistics to TensorBoard so I can see exactly where in the network the problem lives."*

### "Explain Adam to a non-ML engineer."

> *"Imagine you're adjusting dozens of dials on a mixing board. Some dials get touched constantly, others rarely. SGD would move every dial by the same amount per feedback. Adam is smarter — for dials that get adjusted constantly, it takes small careful steps because it's already well-tuned there. For dials rarely touched, it takes bigger steps to catch up. This adaptive behavior is why Adam converges faster on most problems, especially when different parameters have very different gradient frequencies — like word embeddings in NLP."*

---

## Summary Cheatsheet

```
┌─────────────────────────────────────────────────────────────────────────┐
│              MODULE 11 — TRAINING STABILITY CHEATSHEET                  │
├────────────────────────┬────────────────────────────────────────────────┤
│ PROBLEM                │ SOLUTION                                        │
├────────────────────────┼────────────────────────────────────────────────┤
│ Vanishing gradients    │ He/Xavier init, ReLU, BN, residual connections  │
│ Exploding gradients    │ Gradient clipping (norm=1.0), reduce LR         │
│ Overfitting            │ Dropout, weight decay, early stopping, augment  │
│ Slow convergence       │ Adam/AdamW, LR scheduling, momentum             │
│ Training instability   │ Clip grads, BN, reduce LR, warmup               │
│ NaN loss               │ Check data, init, LR; add clipping              │
│ LR plateaus            │ LR range test, cosine annealing, one-cycle      │
├────────────────────────┼────────────────────────────────────────────────┤
│ INITIALIZATION         │ USE WHEN                                        │
├────────────────────────┼────────────────────────────────────────────────┤
│ He (kaiming_normal_)   │ ReLU, Leaky ReLU (default for modern CNNs)      │
│ Xavier (glorot_)       │ Sigmoid, Tanh                                   │
│ Orthogonal             │ RNNs, RL policy networks                        │
│ LeCun                  │ SELU activations                                │
├────────────────────────┼────────────────────────────────────────────────┤
│ OPTIMIZER              │ BEST FOR                                        │
├────────────────────────┼────────────────────────────────────────────────┤
│ AdamW                  │ Transformers, NLP (default choice)              │
│ SGD + Momentum         │ Vision (ImageNet, best final accuracy)          │
│ Adam                   │ Quick experiments, small models                 │
│ RMSProp                │ RL, non-stationary objectives                   │
├────────────────────────┼────────────────────────────────────────────────┤
│ LR SCHEDULE            │ BEST FOR                                        │
├────────────────────────┼────────────────────────────────────────────────┤
│ Warmup + Cosine Decay  │ Transformers (standard)                         │
│ One-Cycle Policy       │ Fast training, vision                           │
│ ReduceLROnPlateau      │ When unsure about total steps                   │
│ Step Decay             │ Simple baselines                                │
├────────────────────────┼────────────────────────────────────────────────┤
│ NORMALIZATION          │ BEST FOR                                        │
├────────────────────────┼────────────────────────────────────────────────┤
│ Batch Norm             │ CNNs, large batch (≥16)                         │
│ Layer Norm             │ Transformers, RNNs, variable-length             │
│ Group Norm             │ Small batch CNNs, object detection              │
│ Instance Norm          │ Style transfer                                  │
├────────────────────────┼────────────────────────────────────────────────┤
│ HYPERPARAMETER SEARCH  │ WHEN TO USE                                     │
├────────────────────────┼────────────────────────────────────────────────┤
│ Random Search          │ < 100 trials, most practical cases              │
│ Bayesian (Optuna)      │ Expensive evaluations, 20+ trials               │
│ Grid Search            │ ≤ 2 params, small grid only                     │
├────────────────────────┼────────────────────────────────────────────────┤
│ BATCH SIZE RULES       │                                                  │
├────────────────────────┼────────────────────────────────────────────────┤
│ Increase batch 2×      │ Increase LR by 2× (linear scaling rule)        │
│ Small batch (8-32)     │ Better generalization, less memory              │
│ Large batch (512+)     │ Scale LR, use warmup, watch for sharp minima   │
└────────────────────────┴────────────────────────────────────────────────┘

GOLDEN CHECKLIST FOR EVERY NEW TRAINING RUN:
  □ Correct init for activation function
  □ Gradient clipping enabled (norm=1.0)
  □ LR schedule configured with warmup
  □ model.eval() + torch.no_grad() during validation
  □ Early stopping with checkpoint restore
  □ Logging: loss, grad norms, LR, weight norms
  □ Seed fixed for reproducibility
  □ Data pipeline verified (no NaNs, correct normalization)
```

---

*Module 11 of the Deep Learning Engineering Series*  
*Topics: Gradient Flow · Initialization · Regularization · Optimization · Scheduling · Hyperparameter Search*
