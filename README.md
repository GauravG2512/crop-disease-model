# 🌿 Crop Disease Detection

> An AI-powered plant pathology tool — upload a leaf photograph and get an instant diagnosis, confidence score, Grad-CAM attention map, and actionable treatment advice.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

</div>

---

## Overview

Crop Disease Detection uses **transfer learning on MobileNetV2** trained on the PlantVillage dataset to classify **38 plant disease categories** across 14 crop species. The project goes beyond a simple classifier — it explains _why_ the model made a prediction using **Grad-CAM visualisation**, and pairs every diagnosis with a human-readable description and treatment recommendation.

---


## Architecture

```
┌─────────────────────────────────────────────┐
│                  app.py                     │
│        Streamlit UI  •  Plotly charts       │
│        Grad-CAM tab  •  Low-conf warning    │
└────────────┬──────────────┬─────────────────┘
             │              │
     ┌───────▼──────┐  ┌────▼──────────┐
     │  predict.py  │  │   labels.py   │
     │  Model load  │  │  Disease info │
     │  Preprocess  │  │  Treatments   │
     │  Inference   │  │  Severity     │
     └───────┬──────┘  └───────────────┘
             │
     ┌───────▼──────────────────────┐
     │      MobileNetV2 backbone    │
     │  + GlobalAveragePooling2D    │
     │  + Dense(38, softmax)        │
     │  + Rescaling(1/255) layer    │
     └──────────────────────────────┘
```

---

## Model

| Property            | Value                          |
| ------------------- | ------------------------------ |
| Base architecture   | MobileNetV2 (ImageNet weights) |
| Input size          | 224 × 224 × 3                  |
| Output classes      | 38                             |
| Normalisation       | `Rescaling(1./255)` (internal) |
| Validation accuracy | **93.36%**                     |
| Dataset             | PlantVillage                   |
| Framework           | TensorFlow / Keras             |

The model has a `Rescaling(1./255)` layer baked in as the first layer, so the inference pipeline feeds **raw [0–255] pixel values** with no external normalisation.

---

## Dataset

[PlantVillage](https://github.com/spMohanty/PlantVillage-Dataset) — 54,306 images of healthy and diseased crop leaves across 38 classes:

| Crop       | Conditions                                                |
| ---------- | --------------------------------------------------------- |
| Apple      | Scab, Black rot, Cedar rust, Healthy                      |
| Cherry     | Powdery mildew, Healthy                                   |
| Corn       | Gray leaf spot, Common rust, N. leaf blight, Healthy      |
| Grape      | Black rot, Esca, Leaf blight, Healthy                     |
| Orange     | Citrus greening                                           |
| Peach      | Bacterial spot, Healthy                                   |
| Pepper     | Bacterial spot, Healthy                                   |
| Potato     | Early blight, Late blight, Healthy                        |
| Strawberry | Leaf scorch, Healthy                                      |
| Tomato     | 9 conditions including mosaic virus, late blight, healthy |
| _(+ more)_ |                                                           |

---

## Features

- **Instant diagnosis** — classification across 38 plant disease classes
- **Confidence score** — circular gauge chart; low-confidence warning below 60%
- **Grad-CAM visualisation** — attention heatmap showing which leaf regions drove the prediction
- **Top-3 predictions** — horizontal bar chart comparing the model's top candidates
- **Treatment advice** — human-written descriptions and recommended actions for every class
- **Severity rating** — Healthy / Low / Medium / High with colour-coded badges
- **Premium UI** — dark botanical theme, Lora serif typography, Plotly charts, mobile-friendly

---

## Project Structure

```
crop-disease-detection/
│
├── app.py              # Streamlit UI — layout, charts, Grad-CAM tab
├── predict.py          # Model loading, preprocessing, inference
├── labels.py           # Disease metadata, treatment text, severity
│
├── crop_disease_model.keras   # Trained Keras model (not in repo — see below)
├── class_names.txt            # One class label per line (38 lines)
│
├── requirements.txt
└── README.md
```

---

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/GauravG2512/crop-disease-detection.git
cd crop-disease-detection

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add model files
# Place crop_disease_model.keras and class_names.txt in the project root

# 5. Run
streamlit run app.py
```

### requirements.txt

```
streamlit>=1.32
tensorflow>=2.13
Pillow>=10.0
numpy>=1.24
plotly>=5.18
opencv-python-headless>=4.8
```

---

## Usage

1. Open the app at `http://localhost:8501`
2. Upload a clear, well-lit photograph of a single leaf (JPG or PNG)
3. The model classifies the image and displays:
   - Plant name and disease name
   - Confidence score (donut chart)
   - Severity badge
   - Description and treatment recommendation
   - Top-3 predictions (bar chart)
   - Grad-CAM attention map (Diagnosis → Grad-CAM tab)

**Tips for best accuracy:**

- Use a single leaf against a plain background
- Ensure good, even lighting
- Avoid blurry or very small images
- If confidence is below 60%, the app will warn you

---

## How Grad-CAM Works

Gradient-weighted Class Activation Mapping (Grad-CAM) computes the gradient of the predicted class score with respect to the feature maps of the last convolutional layer. Regions with high positive gradients correspond to areas that most influenced the prediction — visualised as a heatmap overlaid on the original image.

For MobileNetV2 specifically, the relevant layer is `Conv_1` inside the `mobilenetv2_1.00_224` sub-model (the penultimate convolutional block before global average pooling).

---

## Results

| Metric               | Value               |
| -------------------- | ------------------- |
| Training accuracy    | ~96%                |
| Validation accuracy  | **93.36%**          |
| Test set (20 random) | 17/20 correct (85%) |

The 85% on a small random test sample is consistent with 93.36% validation accuracy given the sample size.

---

## Deployment

### Streamlit Community Cloud

1. Push the repo to GitHub (ensure `crop_disease_model.keras` is accessible — use Git LFS or download from a public URL at startup)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo and set `app.py` as the entry point
4. Add `requirements.txt` — Streamlit Cloud installs dependencies automatically

### Hugging Face Spaces

1. Create a new Space with the **Streamlit** SDK
2. Upload all files including the model
3. Add a `packages.txt` for system dependencies if needed

---

## Future Work

- [ ] Fine-tune on real-world phone photographs (not just PlantVillage lab images)
- [ ] Multi-leaf detection with YOLOv8 before classification
- [ ] REST API endpoint (`FastAPI`) for mobile app integration
- [ ] Offline mode — TensorFlow Lite model for on-device inference
- [ ] Farmer-facing report PDF export with diagnosis summary
- [ ] Regional language support (Hindi, Marathi)

---

## Author

**Gaurav Ghude**
B.Tech Information Technology — Vidyalankar Institute of Technology, Mumbai

[![GitHub](https://img.shields.io/badge/GitHub-GauravG2512-181717?style=flat&logo=github)](https://github.com/GauravG2512)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/)

---

## Acknowledgements

- [PlantVillage Dataset](https://github.com/spMohanty/PlantVillage-Dataset) — Hughes & Salathé, 2015
- [MobileNetV2](https://arxiv.org/abs/1801.04381) — Sandler et al., Google, 2018
- [Grad-CAM](https://arxiv.org/abs/1610.02391) — Selvaraju et al., 2017
- [Streamlit](https://streamlit.io) — open-source app framework

---

## License

MIT License — see [LICENSE](LICENSE) for details.
