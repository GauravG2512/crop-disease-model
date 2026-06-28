"""
labels.py
---------
Maps raw class names (e.g. "Tomato___Late_blight") to human-friendly
display data: formatted name, short description, and treatment advice.

If a class name is not in DISEASE_INFO, the app falls back to the
auto-formatted version of the raw label.
"""

def parse_class_name(raw: str) -> tuple[str, str]:
    """
    Split 'Plant___Disease_Name' → ('Plant Name', 'Disease Name').
    Handles classes like 'Tomato___healthy' cleanly.
    """
    if "___" in raw:
        plant, disease = raw.split("___", 1)
    else:
        plant, disease = raw, ""

    plant = plant.replace("_", " ").strip().title()
    disease = disease.replace("_", " ").strip().title()
    return plant, disease


# ---------------------------------------------------------------------------
# Disease info dictionary
# Key   : exact raw class name from class_names.txt
# Value : dict with keys → description, treatment, severity
#         severity: "healthy" | "low" | "medium" | "high"
# ---------------------------------------------------------------------------
DISEASE_INFO: dict[str, dict] = {

    # ── Apple ──────────────────────────────────────────────────────────────
    "Apple___Apple_scab": {
        "description": "Fungal infection causing dark, scabby lesions on leaves and fruit surfaces.",
        "treatment": "Apply fungicides (captan or myclobutanil) at bud break. Remove fallen leaves. Prune for airflow.",
        "severity": "medium",
    },
    "Apple___Black_rot": {
        "description": "Fungal disease producing brown leaf spots and rotting fruit with concentric rings.",
        "treatment": "Remove mummified fruit and dead wood. Spray with thiophanate-methyl or captan fungicide.",
        "severity": "high",
    },
    "Apple___Cedar_apple_rust": {
        "description": "Rust fungus causing bright orange-yellow spots on leaves and distorted fruit.",
        "treatment": "Apply myclobutanil or mancozeb sprays during bloom. Remove nearby cedar/juniper hosts.",
        "severity": "medium",
    },
    "Apple___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Continue regular monitoring, balanced fertilisation, and good orchard hygiene.",
        "severity": "healthy",
    },

    # ── Blueberry ──────────────────────────────────────────────────────────
    "Blueberry___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Maintain acidic soil (pH 4.5–5.5), adequate irrigation, and annual pruning.",
        "severity": "healthy",
    },

    # ── Cherry ─────────────────────────────────────────────────────────────
    "Cherry_(including_sour)___Powdery_mildew": {
        "description": "White powdery fungal coating on young leaves, shoots, and fruit surfaces.",
        "treatment": "Spray with sulphur-based fungicide or potassium bicarbonate. Improve canopy airflow.",
        "severity": "medium",
    },
    "Cherry_(including_sour)___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Ensure good drainage, avoid overhead irrigation, and prune regularly.",
        "severity": "healthy",
    },

    # ── Corn (Maize) ───────────────────────────────────────────────────────
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "description": "Rectangular grey-to-tan lesions between leaf veins caused by Cercospora fungus.",
        "treatment": "Plant resistant hybrids. Apply strobilurin fungicides at early disease onset. Rotate crops.",
        "severity": "high",
    },
    "Corn_(maize)___Common_rust_": {
        "description": "Reddish-brown pustules scattered across both leaf surfaces.",
        "treatment": "Plant resistant varieties. Apply fungicide (propiconazole) if infection is heavy before tasselling.",
        "severity": "medium",
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "description": "Long cigar-shaped grey-green lesions that turn tan as the disease progresses.",
        "treatment": "Use resistant hybrids. Apply fungicide at early whorl stage. Practise crop rotation.",
        "severity": "high",
    },
    "Corn_(maize)___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Maintain balanced nutrition, proper plant spacing, and monitor regularly.",
        "severity": "healthy",
    },

    # ── Grape ──────────────────────────────────────────────────────────────
    "Grape___Black_rot": {
        "description": "Circular brown leaf lesions and shrivelled, mummified berries caused by Guignardia bidwellii.",
        "treatment": "Remove mummified berries. Apply mancozeb or myclobutanil fungicide from budbreak to veraison.",
        "severity": "high",
    },
    "Grape___Esca_(Black_Measles)": {
        "description": "Complex vascular disease causing tiger-stripe leaf patterns and sudden vine collapse.",
        "treatment": "No curative treatment. Prune during dry weather, seal wounds. Remove severely affected vines.",
        "severity": "high",
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "description": "Angular dark brown spots on leaves leading to defoliation in humid conditions.",
        "treatment": "Apply copper-based fungicides. Improve canopy ventilation. Avoid wetting foliage when irrigating.",
        "severity": "medium",
    },
    "Grape___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Maintain canopy management, balanced nutrition, and scout regularly for early signs.",
        "severity": "healthy",
    },

    # ── Orange ─────────────────────────────────────────────────────────────
    "Orange___Haunglongbing_(Citrus_greening)": {
        "description": "Bacterial disease spread by psyllid insects causing blotchy mottling and bitter, misshapen fruit.",
        "treatment": "No cure. Control Asian citrus psyllid with systemic insecticides. Remove infected trees promptly.",
        "severity": "high",
    },

    # ── Peach ──────────────────────────────────────────────────────────────
    "Peach___Bacterial_spot": {
        "description": "Water-soaked spots on leaves and fruit that turn dark and cause cracking.",
        "treatment": "Apply copper bactericide from green tip through petal fall. Plant resistant cultivars.",
        "severity": "medium",
    },
    "Peach___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Ensure proper thinning, pruning, and a balanced fertilisation programme.",
        "severity": "healthy",
    },

    # ── Pepper ─────────────────────────────────────────────────────────────
    "Pepper,_bell___Bacterial_spot": {
        "description": "Greasy water-soaked lesions on leaves and fruit that turn brown and scabby.",
        "treatment": "Use certified disease-free seed. Apply copper bactericide. Avoid overhead irrigation.",
        "severity": "medium",
    },
    "Pepper,_bell___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Maintain crop rotation, balanced watering, and inspect regularly.",
        "severity": "healthy",
    },

    # ── Potato ─────────────────────────────────────────────────────────────
    "Potato___Early_blight": {
        "description": "Concentric ring (target-board) lesions on older leaves caused by Alternaria solani.",
        "treatment": "Apply chlorothalonil or mancozeb fungicide. Remove infected debris. Rotate crops annually.",
        "severity": "medium",
    },
    "Potato___Late_blight": {
        "description": "Water-soaked, oily lesions that expand rapidly in cool humid weather — the disease behind the Irish Famine.",
        "treatment": "Apply metalaxyl or cymoxanil fungicide preventatively. Destroy volunteer plants and infected tubers.",
        "severity": "high",
    },
    "Potato___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Use certified seed potatoes, hill properly, and scout weekly during humid spells.",
        "severity": "healthy",
    },

    # ── Raspberry ──────────────────────────────────────────────────────────
    "Raspberry___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Prune out old canes after harvest, maintain good airflow, and mulch the root zone.",
        "severity": "healthy",
    },

    # ── Soybean ────────────────────────────────────────────────────────────
    "Soybean___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Rotate with non-legume crops, use resistant varieties, and apply balanced nutrition.",
        "severity": "healthy",
    },

    # ── Squash ─────────────────────────────────────────────────────────────
    "Squash___Powdery_mildew": {
        "description": "White powdery fungal patches on leaf surfaces that spread rapidly in warm, dry conditions.",
        "treatment": "Spray with neem oil, potassium bicarbonate, or sulphur fungicide. Avoid nitrogen excess.",
        "severity": "medium",
    },

    # ── Strawberry ─────────────────────────────────────────────────────────
    "Strawberry___Leaf_scorch": {
        "description": "Small purple-red spots that enlarge and coalesce, scorching leaf margins brown.",
        "treatment": "Remove infected foliage. Apply captan fungicide. Avoid overhead watering. Renovate beds annually.",
        "severity": "medium",
    },
    "Strawberry___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Renew planting every 3 years, keep beds weed-free, and ensure good drainage.",
        "severity": "healthy",
    },

    # ── Tomato ─────────────────────────────────────────────────────────────
    "Tomato___Bacterial_spot": {
        "description": "Small, water-soaked spots on leaves and fruit that turn dark with yellow halos.",
        "treatment": "Use copper bactericide + mancozeb mixture. Avoid wetting foliage. Rotate crops.",
        "severity": "medium",
    },
    "Tomato___Early_blight": {
        "description": "Dark concentric ring lesions on lower leaves that spread upward, causing defoliation.",
        "treatment": "Apply chlorothalonil or mancozeb. Stake plants for airflow. Remove infected lower leaves.",
        "severity": "medium",
    },
    "Tomato___Late_blight": {
        "description": "Greasy, grey-green lesions on leaves and stems that spread rapidly in cool, wet weather.",
        "treatment": "Apply copper fungicide or chlorothalonil preventatively. Remove and destroy infected plants immediately.",
        "severity": "high",
    },
    "Tomato___Leaf_Mold": {
        "description": "Pale green-yellow patches on upper leaf surface with olive-brown mould on underside.",
        "treatment": "Reduce humidity below 85%. Improve greenhouse ventilation. Apply mancozeb or chlorothalonil.",
        "severity": "medium",
    },
    "Tomato___Septoria_leaf_spot": {
        "description": "Circular spots with dark borders and lighter centres, starting on lowest leaves.",
        "treatment": "Remove infected leaves. Apply chlorothalonil or copper fungicide. Avoid overhead irrigation.",
        "severity": "medium",
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "description": "Tiny mites causing stippled, bronzed foliage and fine webbing on leaf undersides.",
        "treatment": "Spray with miticide (abamectin) or insecticidal soap. Increase humidity. Introduce predatory mites.",
        "severity": "medium",
    },
    "Tomato___Target_Spot": {
        "description": "Brown circular lesions with concentric rings and yellow halos on leaves and fruit.",
        "treatment": "Apply azoxystrobin or chlorothalonil. Improve airflow. Remove lower infected leaves promptly.",
        "severity": "medium",
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "description": "Viral disease spread by whiteflies causing severe leaf curling, yellowing, and stunted growth.",
        "treatment": "Control whitefly with reflective mulch and imidacloprid. Remove infected plants. Use resistant varieties.",
        "severity": "high",
    },
    "Tomato___Tomato_mosaic_virus": {
        "description": "Mosaic yellow-green mottling on leaves with distortion and reduced fruit yield.",
        "treatment": "No cure. Remove infected plants. Disinfect tools. Control aphid vectors. Use resistant cultivars.",
        "severity": "high",
    },
    "Tomato___healthy": {
        "description": "No signs of disease detected. The plant appears to be in good health.",
        "treatment": "Maintain consistent watering, crop rotation, and weekly scouting for early problem detection.",
        "severity": "healthy",
    },
}


def get_disease_info(raw_class: str) -> dict:
    """
    Return display info for a raw class name.
    Falls back to auto-parsed name with generic text if not in DISEASE_INFO.
    """
    plant, disease = parse_class_name(raw_class)

    if raw_class in DISEASE_INFO:
        info = DISEASE_INFO[raw_class].copy()
        info["plant"] = plant
        info["disease"] = disease if disease else "Healthy"
        return info

    # Fallback for unknown classes
    is_healthy = "healthy" in raw_class.lower()
    return {
        "plant": plant,
        "disease": disease if disease else ("Healthy" if is_healthy else "Unknown"),
        "description": "Healthy plant detected." if is_healthy else "No detailed information available for this class.",
        "treatment": "Continue standard care practices." if is_healthy else "Consult a local agricultural extension officer for advice.",
        "severity": "healthy" if is_healthy else "medium",
    }