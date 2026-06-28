"""
app.py  —  Crop Disease Detection
Run with:  streamlit run app.py
"""

import streamlit as st
from PIL import Image
import plotly.graph_objects as go

from predict import load_model, load_class_names, predict
from labels import get_disease_info

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Crop Disease Detection",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CONFIDENCE_THRESHOLD = 0.60   # below this → low-confidence warning

# ── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Sans:wght@300;400;500&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {
    background: #0d1a10 !important;
    font-family: 'IBM Plex Sans', sans-serif;
    color: #c8dfc4;
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse 80% 50% at 10% 5%,  rgba(34,80,34,0.25) 0%, transparent 55%),
        radial-gradient(ellipse 60% 40% at 90% 90%, rgba(15,55,20,0.30) 0%, transparent 55%) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"],
#MainMenu, footer { display: none !important; }

.block-container {
    max-width: 700px !important;
    padding: 1.5rem 1.25rem 5rem !important;
    margin: 0 auto !important;
}

/* ── Uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(16,34,14,0.8) !important;
    border: 1.5px dashed rgba(80,160,60,0.45) !important;
    border-radius: 14px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] p,
[data-testid="stFileUploaderDropzoneInstructions"] small {
    color: #5a8a54 !important;
}

/* ── Image preview: constrained height ── */
[data-testid="stImage"] img {
    border-radius: 14px !important;
    max-height: 280px !important;
    width: 100% !important;
    object-fit: cover !important;
    border: 1px solid rgba(80,140,60,0.3) !important;
    box-shadow: 0 8px 36px rgba(0,0,0,0.5) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: rgba(16,36,14,0.75);
    border: 1px solid rgba(60,120,40,0.25);
    border-radius: 12px;
    padding: 0.9rem 1rem !important;
}
[data-testid="stMetricLabel"]  { color: #5a8a50 !important; font-size: 0.72rem !important; letter-spacing: 0.1em; text-transform: uppercase; }
[data-testid="stMetricValue"]  { color: #d4edd0 !important; font-family: 'Lora', serif !important; font-size: 1.25rem !important; }

/* ── Plotly chart background ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(12,28,10,0.65) !important;
    border: 1px solid rgba(50,110,35,0.22) !important;
    border-radius: 12px !important;
}
summary { color: #7ecb5a !important; font-size: 0.85rem !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: 10px !important; }

/* ── Progress bar ── */
[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #3d9428, #7ecb5a) !important;
}

/* ── Section divider ── */
hr { border-color: rgba(80,140,60,0.18) !important; margin: 1.4rem 0 !important; }

/* ── Tabs ── */
[data-testid="stTabs"] button {
    color: #7a9e74 !important;
    font-size: 0.82rem !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #7ecb5a !important;
    border-bottom-color: #7ecb5a !important;
}

/* ── Severity badge ── */
.sev-badge {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 14px; border-radius: 100px;
    font-size: 0.72rem; font-weight: 500; font-family: 'IBM Plex Sans', sans-serif;
}
.sev-healthy { background: rgba(60,160,60,0.15);  border: 1px solid rgba(60,160,60,0.4);  color: #7ecb5a; }
.sev-medium  { background: rgba(200,160,30,0.15); border: 1px solid rgba(200,160,30,0.4); color: #c8a84a; }
.sev-high    { background: rgba(200,70,40,0.15);  border: 1px solid rgba(200,70,40,0.4);  color: #e07850; }
.sev-low     { background: rgba(80,170,220,0.15); border: 1px solid rgba(80,170,220,0.4); color: #7ac0e0; }

/* ── Grad-CAM note ── */
.gradcam-note {
    font-size: 0.72rem; color: #5a8250; text-align: center;
    margin-top: 0.4rem; font-style: italic;
}
</style>
""", unsafe_allow_html=True)


# ── Load model (cached) ────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading model…")
def _load():
    m, me = load_model()
    n, ne = load_class_names()
    return m, me, n, ne

model, model_err, class_names, cls_err = _load()


# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2rem 0 1.4rem;">
  <div style="display:inline-block; font-size:0.62rem; font-weight:500;
              letter-spacing:0.22em; text-transform:uppercase; color:#6ab356;
              background:rgba(106,179,86,0.1); border:1px solid rgba(106,179,86,0.28);
              border-radius:20px; padding:0.28rem 0.9rem; margin-bottom:0.9rem;">
    AI Plant Pathology
  </div>
  <div style="font-family:'Lora',Georgia,serif; font-size:clamp(1.8rem,4vw,2.75rem);
              font-weight:600; color:#daefd4; line-height:1.17; letter-spacing:-0.02em;
              margin-bottom:0.65rem;">
    Crop Disease<br><em style="color:#7ecb5a;">Detection</em>
  </div>
  <div style="font-size:0.86rem; font-weight:300; color:#7a9e74;
              line-height:1.6; max-width:360px; margin:0 auto;">
    Upload a clear leaf photograph — get an instant AI diagnosis,
    confidence score, and treatment advice.
  </div>
</div>
""", unsafe_allow_html=True)

if model_err:
    st.error(f"⚠ Model unavailable — {model_err}")
if cls_err:
    st.error(f"⚠ Class names missing — {cls_err}")

st.divider()


# ── Upload ─────────────────────────────────────────────────────────────────
uploaded = st.file_uploader(
    "Drop a leaf image here, or click to browse",
    type=["jpg", "jpeg", "png"],
    label_visibility="visible",
)


# ── Grad-CAM helper ────────────────────────────────────────────────────────
def make_gradcam(model, img_array, pred_index):
    """
    Grad-CAM for a MobileNetV2-based model.

    MobileNetV2 is a *nested* Functional model — its Conv2D layers live
    inside the 'mobilenetv2_1.00_224' sub-model, not at the top level.
    We therefore:
      1. Try the named backbone + 'Conv_1' (the penultimate conv block).
      2. Fall back to recursively searching all sub-models for any Conv2D.
      3. Build the grad-model using the top-level model's input and output
         so gradients flow end-to-end.

    Returns a PIL Image (heatmap overlay) or None on failure.
    All exceptions are surfaced via st.error so the real cause is visible.
    """
    import traceback as _tb

    try:
        import tensorflow as tf
        import numpy as np
        import cv2

        # ── Step 1: locate the last conv layer ──────────────────────────────
        conv_layer = None
        backbone   = None

        # Primary strategy: known MobileNetV2 backbone name + layer name
        BACKBONE_NAMES   = ["mobilenetv2_1.00_224", "mobilenetv2_1.00_192",
                            "mobilenetv2_1.00_160", "mobilenetv2_1.00_128",
                            "mobilenetv2"]
        CONV_LAYER_NAMES = ["Conv_1", "out_relu", "Conv_1_bn"]

        for bname in BACKBONE_NAMES:
            try:
                backbone = model.get_layer(bname)
                for lname in CONV_LAYER_NAMES:
                    try:
                        conv_layer = backbone.get_layer(lname)
                        break
                    except Exception:
                        pass
                if conv_layer:
                    break
            except Exception:
                backbone = None

        # Fallback: recursively walk every sub-model for the last Conv2D
        if conv_layer is None:
            def _find_last_conv(m):
                found = None
                for layer in m.layers:
                    if isinstance(layer, tf.keras.layers.Conv2D):
                        found = layer
                    elif hasattr(layer, "layers"):
                        inner = _find_last_conv(layer)
                        if inner is not None:
                            found = inner
                return found
            conv_layer = _find_last_conv(model)

        # Debug: always show which layer was selected
        if conv_layer is not None:
            st.caption(f"🔬 Grad-CAM layer: `{conv_layer.name}` ({type(conv_layer).__name__})")
        else:
            st.error("Grad-CAM: could not find any Conv2D layer in the model graph.")
            return None

        # ── Step 2: build grad model ─────────────────────────────────────────
        # If conv_layer lives inside a nested sub-model (e.g. MobileNetV2),
        # TF may raise "Graph disconnected" when we try to wire
        # conv_layer.output → outer model.output.
        # Strategy A: use the backbone model's input/output directly.
        # Strategy B: fall back to the outer model's full graph.
        try:
            if backbone is not None:
                # Build grad model scoped to the backbone to avoid graph issues
                grad_model = tf.keras.models.Model(
                    inputs=backbone.input,
                    outputs=[conv_layer.output, backbone.output],
                )
                use_backbone = True
            else:
                grad_model = tf.keras.models.Model(
                    inputs=model.input,
                    outputs=[conv_layer.output, model.output],
                )
                use_backbone = False
        except Exception as e:
            st.error(f"Grad-CAM: failed to build grad model.\n{e}")
            st.code(_tb.format_exc())
            return None

        # ── Step 3: compute gradients ────────────────────────────────────────
        # If we scoped to the backbone, we need to feed backbone's input.
        # The backbone's input == the outer model's input after Rescaling,
        # so we pre-apply Rescaling manually for this forward pass.
        img_tensor = tf.cast(img_array, tf.float32)

        if use_backbone:
            # Apply every layer before the backbone to transform the input
            x = img_tensor
            for layer in model.layers:
                if layer is backbone:
                    break
                x = layer(x, training=False)
            feed = x
        else:
            feed = img_tensor

        with tf.GradientTape() as tape:
            tape.watch(feed)
            conv_out, preds = grad_model(feed, training=False)
            # When scoped to backbone, preds = backbone output (not softmax).
            # We still use argmax of the outer model, so just take the max channel.
            if use_backbone:
                loss = tf.reduce_max(preds)   # proxy: strongest backbone feature
            else:
                loss = preds[:, pred_index]

        grads    = tape.gradient(loss, conv_out)
        if grads is None:
            st.error("Grad-CAM: gradient is None — the conv layer may not be on the tape path.")
            return None

        grads    = grads[0]        # (H, W, C)
        conv_out = conv_out[0]     # (H, W, C)

        # ── Step 4: weighted combination → heatmap ───────────────────────────
        weights = tf.reduce_mean(grads, axis=(0, 1))
        cam = tf.reduce_sum(tf.multiply(weights, conv_out), axis=-1).numpy()
        cam = np.maximum(cam, 0)
        cam = cam / (cam.max() + 1e-8)

        cam_resized = cv2.resize(cam, (224, 224))
        heatmap = cv2.applyColorMap(np.uint8(255 * cam_resized), cv2.COLORMAP_JET)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

        # ── Step 5: overlay on original ──────────────────────────────────────
        orig    = np.array(img_array[0], dtype=np.uint8)
        overlay = (0.55 * orig + 0.45 * heatmap).astype(np.uint8)
        return Image.fromarray(overlay)

    except Exception as e:
        st.error(f"Grad-CAM error: {e}")
        st.code(_tb.format_exc())
        return None


# ── Confidence donut chart ─────────────────────────────────────────────────
def confidence_donut(confidence: float, color: str) -> go.Figure:
    fig = go.Figure(go.Pie(
        values=[confidence, 100 - confidence],
        hole=0.72,
        marker_colors=[color, "rgba(255,255,255,0.05)"],
        textinfo="none",
        hoverinfo="skip",
        sort=False,
    ))
    fig.add_annotation(
        text=f"<b>{confidence:.1f}%</b>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=20, color=color, family="IBM Plex Sans"),
    )
    fig.update_layout(
        showlegend=False, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=160, width=160,
    )
    return fig


# ── Top-K bar chart ────────────────────────────────────────────────────────
def topk_bar_chart(top_k: list) -> go.Figure:
    labels = []
    for item in reversed(top_k):
        raw = item["class"]
        p, d = raw.split("___", 1) if "___" in raw else (raw, "")
        label = f"{p.replace('_',' ')}<br>{d.replace('_',' ')}" if d else p.replace("_", " ")
        labels.append(label)
    values = [item["confidence"] for item in reversed(top_k)]
    colors = ["#7ecb5a" if v == max(values) else "rgba(106,179,86,0.38)" for v in values]

    fig = go.Figure(go.Bar(
        x=values, y=labels,
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        textfont=dict(color="#9bbf94", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(range=[0, 105], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, tickfont=dict(color="#9bbf94", size=11)),
        margin=dict(l=10, r=60, t=10, b=10),
        height=160,
    )
    return fig


# ── Main inference block ────────────────────────────────────────────────────
if uploaded is not None:

    try:
        image = Image.open(uploaded).convert("RGB")
    except Exception as exc:
        st.error(f"Could not open image: {exc}")
        st.stop()

    # Preview
    st.image(image, use_container_width=True)
    st.markdown("")

    if model is None or class_names is None:
        st.error("Cannot run prediction — fix the model/class-name errors above.")
        st.stop()

    with st.spinner("Analysing leaf…"):
        try:
            import numpy as np
            from predict import preprocess
            arr = preprocess(image)          # raw [0-255] float32, shape (1,224,224,3)
            result = predict(model, image, class_names)
        except Exception as exc:
            st.error(f"Prediction error: {exc}")
            st.stop()

    raw_class  = result["predicted_class"]
    confidence = result["confidence"]        # 0–100 float
    top_k      = result["top_k"]
    info       = get_disease_info(raw_class)

    plant   = info["plant"]
    disease = info["disease"]
    desc    = info["description"]
    treat   = info["treatment"]
    sev     = info["severity"]   # "healthy" | "low" | "medium" | "high"

    # ── Low-confidence warning ──────────────────────────────────────────────
    if confidence < CONFIDENCE_THRESHOLD * 100:
        st.warning(
            "⚠ **Low confidence prediction.** "
            "Try using a clearer, well-lit image of a single leaf against a plain background."
        )

    # ── Severity colours ────────────────────────────────────────────────────
    SEV_MAP = {
        "healthy": ("#7ecb5a", "sev-healthy", "✦ Healthy",          "high"),
        "low":     ("#7ac0e0", "sev-low",     "◇ Low Severity",     "high"),
        "medium":  ("#c8a84a", "sev-medium",  "◆ Medium Severity",  "medium"),
        "high":    ("#e07850", "sev-high",    "⚑ High Severity",    "low-c"),
    }
    accent, badge_cls, badge_label, _bar = SEV_MAP.get(sev, SEV_MAP["medium"])

    # ── Result header ───────────────────────────────────────────────────────
    st.markdown(f"""
<div style="margin-bottom:0.2rem; font-size:0.66rem; font-weight:500;
            letter-spacing:0.16em; text-transform:uppercase; color:#5a8250;">
  {plant}
</div>
<div style="font-family:'Lora',Georgia,serif; font-size:1.9rem; font-weight:600;
            color:#daefd4; line-height:1.18; margin-bottom:0.6rem;">
  {disease}
</div>
<span class="sev-badge {badge_cls}">{badge_label}</span>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Confidence donut + metrics row ──────────────────────────────────────
    col_donut, col_metrics = st.columns([1, 1.8], gap="medium")
    with col_donut:
        fig_donut = confidence_donut(confidence, accent)
        st.plotly_chart(fig_donut, use_container_width=False, config={"displayModeBar": False})
        st.markdown('<p class="gradcam-note">Confidence Score</p>', unsafe_allow_html=True)

    with col_metrics:
        st.metric("Plant", plant)
        st.metric("Severity", sev.title())
        st.metric("Top prediction", f"{confidence:.1f}%")

    st.divider()

    # ── Tabs: Info / Chart / Grad-CAM ───────────────────────────────────────
    tab_info, tab_chart, tab_cam = st.tabs(["📋 Diagnosis", "📊 Top Predictions", "🌡️ Grad-CAM"])

    with tab_info:
        st.markdown(f"""
<div style="margin-bottom:1.1rem;">
  <div style="font-size:0.64rem; font-weight:500; letter-spacing:0.14em;
              text-transform:uppercase; color:#4e7248; margin-bottom:0.35rem;">About</div>
  <div style="font-size:0.88rem; color:#9bbf94; line-height:1.7;">{desc}</div>
</div>
<div>
  <div style="font-size:0.64rem; font-weight:500; letter-spacing:0.14em;
              text-transform:uppercase; color:#4e7248; margin-bottom:0.35rem;">Recommended Treatment</div>
  <div style="font-size:0.88rem; color:#9bbf94; line-height:1.7;">{treat}</div>
</div>
""", unsafe_allow_html=True)

    with tab_chart:
        st.markdown(
            "<div style='font-size:0.75rem; color:#5a8250; margin-bottom:0.5rem;'>"
            "Top-3 model predictions by confidence</div>",
            unsafe_allow_html=True
        )
        st.plotly_chart(
            topk_bar_chart(top_k),
            use_container_width=True,
            config={"displayModeBar": False}
        )

    with tab_cam:
        with st.spinner("Generating Grad-CAM…"):
            pred_index = class_names.index(raw_class) if raw_class in class_names else 0
            cam_img = make_gradcam(model, arr, pred_index)

        if cam_img:
            col_orig, col_cam = st.columns(2, gap="small")
            with col_orig:
                st.markdown(
                    "<div style='font-size:0.72rem;color:#5a8250;text-align:center;"
                    "margin-bottom:0.3rem;'>Original</div>",
                    unsafe_allow_html=True
                )
                st.image(image, use_container_width=True)
            with col_cam:
                st.markdown(
                    "<div style='font-size:0.72rem;color:#5a8250;text-align:center;"
                    "margin-bottom:0.3rem;'>Attention Map</div>",
                    unsafe_allow_html=True
                )
                st.image(cam_img, use_container_width=True)
            st.markdown(
                '<p class="gradcam-note">Warmer colours = regions most influential to the prediction</p>',
                unsafe_allow_html=True
            )
        else:
            st.info(
                "Grad-CAM requires OpenCV (`pip install opencv-python-headless`) "
                "and a model with Conv2D layers."
            )


# ── Model info panel ───────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()

st.markdown("""
<div style="font-size:0.62rem; font-weight:500; letter-spacing:0.2em;
            text-transform:uppercase; color:#4e7248; margin-bottom:1rem;">
  Model Information
</div>
""", unsafe_allow_html=True)

info_cols = st.columns(4, gap="small")
model_stats = [
    ("Model",        "MobileNetV2"),
    ("Val Accuracy", "93.36%"),
    ("Dataset",      "PlantVillage"),
    ("Classes",      "38"),
]
for col, (label, value) in zip(info_cols, model_stats):
    with col:
        st.metric(label, value)


# ── Footer ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 2.5rem 0 1rem; margin-top:1rem;">
  <div style="font-family:'Lora',Georgia,serif; font-size:1rem;
              color:#5a8250; margin-bottom:0.35rem; font-style:italic;">
    Crop Disease Detection
  </div>
  <div style="font-size:0.72rem; color:#3d5e39; letter-spacing:0.04em;">
    Developed by <span style="color:#6ab356;">GG</span>
    &nbsp;·&nbsp;
    Built with TensorFlow &nbsp;•&nbsp; MobileNetV2 &nbsp;•&nbsp; Streamlit
  </div>
</div>
""", unsafe_allow_html=True)