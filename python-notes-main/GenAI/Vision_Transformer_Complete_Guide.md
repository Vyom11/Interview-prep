# Vision Transformers (ViT) — Complete Beginner to Engineer Guide

## 1. Introduction & The Backstory

### What is a Vision Transformer (ViT)?

**Interview Definition:**

> A Vision Transformer (ViT) is a deep learning architecture that treats an image as a sequence of patches and processes those patches using transformer-based self-attention mechanisms. Unlike CNNs, which learn through convolutions and local receptive fields, ViTs learn relationships between all image patches globally through attention, making them highly effective for large-scale computer vision tasks such as image classification, object detection, and segmentation.

---

## Before ViTs: The Era of CNNs

For many years, **Convolutional Neural Networks (CNNs)** dominated computer vision.

CNNs process images using small filters called **kernels**.

### CNN Processing Pipeline

```text
+---------+
|  Image  |
+---------+
     |
     v
+-------------+
| 3x3 Filter  |
+-------------+
     |
     v
+-------------+
| Feature Map |
+-------------+
     |
     v
+-------------+
| More Filters|
+-------------+
     |
     v
+-------------+
| Prediction  |
+-------------+
```

---

## What CNNs Are Good At

CNNs are excellent at learning:

### 1. Edges

```text
| Vertical Edge
---------
Horizontal Edge
```

### 2. Textures

```text
Brick Wall
Grass
Sand
Water
```

### 3. Shapes

```text
Circle
Square
Triangle
Face
Car
Dog
```

---

## Limitation #1: Local View

CNNs only see a small region at a time.

Imagine a cat image:

```text
CNN sees:

Ear
 ↓
Eye
 ↓
Nose
 ↓
Mouth
```

CNN gradually combines these features through many layers.

### Analogy

Imagine reading a large poster through a tiny hole.

You only see one small part at a time and slowly understand the entire picture.

---

## Limitation #2: Long-Range Relationships

Consider:

```text
Person ---------------- Bicycle
```

A CNN initially sees:

```text
Layer 1:
Person

Layer 1:
Bicycle
```

These objects are far apart.

CNN requires many layers before it understands:

```text
"This person is riding this bicycle."
```

---

## The Transformer Idea

Transformers were originally invented for NLP.

Example sentence:

```text
"The cat sat on the mat."
```

Self-attention learns:

```text
cat ↔ sat
sat ↔ mat
cat ↔ mat
```

Every word can communicate with every other word.

Researchers asked:

> If words can be tokens, why not image patches?

This idea gave birth to Vision Transformers.

---

# 2. What Does a Vision Transformer Do?

Vision Transformers can perform:

## Applications

### Image Classification

```text
Cat
Dog
Horse
Bird
```

### Object Detection

```text
Locate objects in image
```

### Image Segmentation

```text
Assign class to every pixel
```

### Face Recognition

```text
Identify person
```

### Medical Image Analysis

```text
Tumor Detection
X-Ray Analysis
MRI Analysis
```

### Satellite Image Analysis

```text
Road Detection
Forest Monitoring
Building Detection
```

---

## Example

### Input

```text
Dog Image
```

### Output

```text
Dog   → 98%
Cat   → 1%
Horse → 1%
```

---

## Core Idea of ViT

Instead of processing pixels directly:

```text
Image
 ↓
Split into small patches
 ↓
Treat patches as tokens
 ↓
Feed into Transformer
```

---

### Example

Input image:

```text
224 × 224
```

Patch size:

```text
16 × 16
```

Number of patches:

```text
(224/16) × (224/16)

14 × 14

196 patches
```

---

### Visual Representation

```text
+----+----+----+----+
| P1 | P2 | P3 | P4 |
+----+----+----+----+
| P5 | P6 | P7 | P8 |
+----+----+----+----+
| ...              |
+------------------+
```

Each patch becomes a token.

Just like:

```text
Sentence → Words → Tokens

Image → Patches → Tokens
```

---

# 3. Deconstructing the ViT Architecture Pipeline

## Full Pipeline

```text
+-------+
| Image |
+-------+
    |
    v
+---------------+
| Patch Creation|
+---------------+
    |
    v
+----------------+
|Patch Embedding |
+----------------+
    |
    v
+----------------+
|Position Encode |
+----------------+
    |
    v
+----------------+
|Transformer Enc |
+----------------+
    |
    v
+----------------+
|Classification  |
|     Head       |
+----------------+
    |
    v
+-------------+
| Prediction  |
+-------------+
```

---

# Step 1: Image Patches

Input image:

```text
224 × 224 × 3
```

Where:

```text
224 = height
224 = width
3 = RGB channels
```

Split into:

```text
16 × 16 patches
```

Result:

```text
14 × 14 = 196 patches
```

---

### NLP Comparison

```text
Sentence:
[I] [love] [AI]

Image:
[P1] [P2] [P3] ... [P196]
```

---

# Step 2: Patch Embedding

Transformers cannot understand raw pixels.

### Raw Patch

```text
16 × 16 × 3

= 768 values
```

Example:

```text
[255,120,34,...]
```

---

### Linear Projection

Convert:

```text
768 dimensions
```

into

```text
512 dimensions
```

Example:

```text
Patch
 ↓
Dense Layer
 ↓
[0.12,0.45,0.89,...]
```

This becomes the patch embedding.

---

## Why?

Transformers only understand vectors.

Patch embeddings convert image information into a format transformers can process.

---

# Step 3: Position Encoding

Transformers do not know spatial location.

Without positional information:

```text
Dog Face Patch
Dog Tail Patch
```

could be swapped.

Transformer would not know.

---

## Solution

Add position information.

Example:

```text
Patch 1  → Top Left
Patch 50 → Center
Patch 196 → Bottom Right
```

---

### Final Token

```text
Final Token

=
Patch Embedding
+
Position Encoding
```

---

# Step 4: CLS Token

A special token:

```text
[CLS]
```

is added at the beginning.

---

Before:

```text
P1 P2 P3 ... P196
```

After:

```text
CLS P1 P2 P3 ... P196
```

---

## Purpose

During attention:

```text
CLS token
collects information
from all patches
```

At the end:

```text
CLS token
↓
Classification Head
↓
Prediction
```

---

# Step 5: Self-Attention (QKV)

This is the heart of ViT.

Each patch asks:

> Which other patches are important to me?

---

## Example

Dog eye patch:

```text
Eye Patch
```

attends to:

```text
Nose Patch = 0.90
Ear Patch  = 0.85
Grass      = 0.05
```

---

## QKV Mechanism

Each token generates:

### Query (Q)

```text
What am I looking for?
```

---

### Key (K)

```text
What information do I contain?
```

---

### Value (V)

```text
Actual information stored.
```

---

## Attention Formula

```text
Attention(Q,K,V)
=
softmax(QKᵀ / √dₖ)V
```

---

### Simplified Understanding

```text
Query
   ↓
Compare with Keys
   ↓
Generate Scores
   ↓
Apply Softmax
   ↓
Weighted Sum of Values
```

---

# Step 6: Multi-Head Attention

Instead of one attention mechanism:

Use many.

---

Example:

```text
Head 1 → Edges

Head 2 → Texture

Head 3 → Shapes

Head 4 → Object Parts
```

---

Visual:

```text
          Token
             |
  -------------------------
  |     |      |         |
Head1 Head2  Head3    Head4
  |     |      |         |
  -------------------------
             |
          Output
```

---

## Benefit

Different heads learn different relationships simultaneously.

---

# Step 7: Feed Forward Network (FFN)

After attention:

```text
Attention Output
      |
      v
Linear
      |
      v
GELU
      |
      v
Linear
```

---

## Purpose

Learns more complex feature representations.

Think of it as:

```text
Attention = Gather Information

FFN = Process Information
```

---

# Step 8: Layer Normalization & Residual Connections

Training very deep models is difficult.

Problems:

```text
Vanishing Gradients
Exploding Gradients
Slow Learning
```

---

## Layer Normalization

Normalizes activations.

Benefits:

```text
Stable Training
Faster Convergence
Better Gradient Flow
```

---

## Residual Connection

```text
Output
=
Layer(Input)
+
Input
```

Visual:

```text
Input
  |
  +------------+
  |            |
  v            |
 Layer         |
  |            |
  +-----+------+
        |
        v
     Output
```

---

## Benefit

Helps information flow through deep networks.

---

# Step 9: Complete Transformer Encoder Block

One encoder block:

```text
Input
  |
  v
LayerNorm
  |
  v
Multi-Head Attention
  |
  v
Residual Add
  |
  v
LayerNorm
  |
  v
Feed Forward Network
  |
  v
Residual Add
  |
  v
Output
```

---

## Multiple Encoder Layers

Example:

```text
Encoder Block 1
      ↓
Encoder Block 2
      ↓
Encoder Block 3
      ↓
...
      ↓
Encoder Block 12
```

Common configurations:

```text
ViT-Base   → 12 Layers
ViT-Large  → 24 Layers
ViT-Huge   → 32+ Layers
```

---

# 4. Global View vs Local View

## CNN

```text
Patch A
 ↓
 ↓
 ↓
 ↓
Patch Z
```

Requires many layers.

---

## ViT

```text
Patch A <----------------> Patch Z
```

Direct communication.

---

### Why ViTs Work

CNN:

```text
Local Understanding First
Global Understanding Later
```

ViT:

```text
Global Understanding Immediately
```

---

# 5. Requirements for Vision Transformers

## Requirement 1: Large Datasets

Examples:

* ImageNet
* JFT-300M

---

## Why?

CNNs contain built-in assumptions:

```text
Nearby pixels are related.
Patterns repeat.
```

This is called:

### Inductive Bias

---

ViTs have much weaker inductive bias.

Therefore:

```text
Need more examples
Need more data
```

to learn visual relationships.

---

# Requirement 2: High Compute

Self-attention complexity:

```text
O(N²)
```

Where:

```text
N = Number of Patches
```

---

Example:

```text
196 patches

Need
196 × 196

pairwise interactions
```

---

## Hardware Needed

```text
GPU
TPU
Multi-GPU Clusters
```

for large models.

---

# Requirement 3: Memory

Attention stores:

```text
Patch ↔ Patch
relationships
```

---

More patches:

```text
More Attention Scores
More RAM
More VRAM
```

required.

---

# 6. Summary, Glossary & Decision Matrix

# Glossary

| Term                 | Meaning                           |
| -------------------- | --------------------------------- |
| Patch                | Small image chunk                 |
| Token                | Embedded patch                    |
| Patch Embedding      | Vector representation of patch    |
| Position Encoding    | Location information              |
| CLS Token            | Special classification token      |
| Query (Q)            | What information is needed        |
| Key (K)              | What information exists           |
| Value (V)            | Actual information                |
| Self-Attention       | Token-to-token communication      |
| Multi-Head Attention | Multiple attention mechanisms     |
| FFN                  | Feed Forward Network              |
| LayerNorm            | Stabilizes training               |
| Residual Connection  | Skip connection for gradient flow |
| Encoder Block        | Core transformer processing unit  |

---

# ViT vs CNN Comparison

| Feature                       | CNN         | Vision Transformer |
| ----------------------------- | ----------- | ------------------ |
| Main Operation                | Convolution | Self-Attention     |
| Learning Local Patterns       | Excellent   | Good               |
| Learning Global Relationships | Hard        | Excellent          |
| Data Requirement              | Lower       | Higher             |
| Compute Requirement           | Lower       | Higher             |
| Parallelization               | Moderate    | Excellent          |
| Large Dataset Performance     | Good        | Often Better       |

---

# Popular Vision Transformer Variants

### ViT

Original Vision Transformer.

---

### DeiT

Data-Efficient Image Transformer.

---

### Swin Transformer

Uses local windows for better scalability.

---

### BEiT

BERT-style pretraining for images.

---

### DINO

Self-supervised Vision Transformer.

---

### CLIP

Joint image-text understanding model.

---

# Practical Engineering Guide

## Use Vision Transformers When

✅ Large dataset available

✅ Strong GPUs available

✅ Need state-of-the-art accuracy

✅ Long-range relationships matter

Examples:

```text
Medical Imaging
Satellite Imaging
Autonomous Driving
Large Scale Recognition
Object Detection
```

---

## Use CNNs When

✅ Small dataset

✅ Limited hardware

✅ Fast inference required

✅ Mobile or edge deployment

Examples:

```text
Mobile Apps
Embedded Devices
Real-time Video Systems
IoT Cameras
```

---

# Final Takeaway

A CNN learns an image **piece by piece**, gradually building a global understanding through many convolution layers.

A Vision Transformer treats an image as a **sequence of patches**, allowing every patch to communicate with every other patch through **self-attention**, giving it a powerful global view of the image from the very beginning. This ability to model long-range relationships is the primary reason Vision Transformers have become one of the most important architectures in modern computer vision.
