import streamlit as st

# --- CONSTANTS AND THRESHOLDS ---
CONSTANT_F = 12.03
CONSTANT_C = 8.42
THRESHOLD_AA = 51.82
THRESHOLD_A = 30.019

# --- SET PAGE CONFIG & STYLES ---
st.set_page_config(layout="wide", page_title="CHICK IT! Egg Freshness Index Calculator")

# Inline CSS to apply Montserrat font to headings (mimicking the original)
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <style>
        h1, h2, h3, h4 {
            font-family: 'Montserrat', sans-serif !important;
            font-weight: 700 !important;
        }
        .stButton>button {
            width: 100%;
            background-color: #4f46e5; /* indigo-600 */
            color: white;
            font-weight: 600;
        }
        .stButton>button:hover {
            background-color: #4338ca; /* indigo-700 */
        }
        /* Custom styling for the formula box */
        .formula-box {
            background-color: #eef2ff; /* indigo-50 */
            padding: 1rem;
            border-radius: 0.5rem;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        /* Custom styling for the guide cards */
        .guide-card {
            background-color: #ffffff;
            border-left: 4px solid #4f46e5;
            padding: 1.5rem;
            border-radius: 0.75rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .info-detail {
            background-color: #eff6ff; /* blue-50 */
            border-left: 3px solid #3b82f6; /* blue-500 */
            padding: 0.75rem;
            border-radius: 0.25rem;
            margin-top: 0.5rem;
            font-size: 0.875rem;
        }
    </style>
    """, unsafe_allow_html=True)

# --- CALCULATION FUNCTION ---
def calculate_freshness(weight, floating_score, candling_score):
    # Ensure scores are integers (0, 1, 2)
    if floating_score not in [0, 1, 2] or candling_score not in [0, 1, 2]:
        return "Invalid Score", "Floating and Candling Scores must be 0, 1, or 2.", "red"

    # Calculate Freshness Index (FI)
    freshness_index = weight - (CONSTANT_F * floating_score) - (CONSTANT_C * candling_score)
    fi_rounded = f"{freshness_index:.2f}"

    # Determine Classification
    if freshness_index >= THRESHOLD_AA:
        classification = "AA Grade"
        grade_name = "AA (Premium)"
        color = "green"
    elif freshness_index >= THRESHOLD_A:
        classification = "A Grade"
        grade_name = "A (Standard)"
        color = "blue"
    else:
        classification = "B Grade"
        grade_name = "B (Reduced)"
        color = "orange"

    return fi_rounded, classification, grade_name, color

# --- APP LAYOUT (Split into two columns) ---
col_calc, col_guides = st.columns([1, 1], gap="large")

# -----------------------------------------------------
# 1. LEFT COLUMN: CALCULATOR & ABOUT
# -----------------------------------------------------
with col_calc:
    st.image("https://media.discordapp.net/attachments/1439445774172815494/1439447528780206152/logo.png?ex=691a8d7a&is=69193bfa&hm=34b63f8114f9b4193057a2fc10e6bc00570f96af6b059e8421839ce598658625")
    st.title("CHICK IT! Egg Freshness Index (FI) Calculator")
    st.markdown("<p style='text-align: center; color: #6b7280;'>Calculates freshness based on Weight, Floating Score, and Candling Score.</p>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="formula-box">
            <p style='font-size: 1.25rem; font-weight: bold; color: #4f46e5;'>
                Formula: FI = W – {CONSTANT_F}F – {CONSTANT_C}C
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("Input Parameters")
    
    # 1. Weight Input
    with st.expander("1. Weight (W) in grams", expanded=True):
        st.markdown("""
        <div class='info-detail'>
        <strong>Weight (W):</strong> This refers to the total mass of the egg in grams. It is a critical factor because an egg loses weight as moisture evaporates through the shell over time. Freshness is inversely proportional to weight loss.
        </div>
        """, unsafe_allow_html=True)
        weight = st.number_input("Weight (W)", min_value=1.0, step=0.01, format="%.2f", value=55.0, label_visibility="collapsed")
    
    # 2. Floating Score Input (Integer 0, 1, 2)
    with st.expander("2. Floating Score (F)", expanded=True):
        st.markdown("""
        <div class='info-detail'>
        <strong>Floating Score (F):</strong> This score is derived from the **Float Test**. A score of **0** means the egg lies flat (freshest); **1** means it stands upright; and **2** means it floats (least fresh). Only whole integers (0, 1, 2) should be used.
        </div>
        """, unsafe_allow_html=True)
        floating_score = st.number_input("Floating Score (F)", min_value=0, max_value=2, step=1, value=0, label_visibility="collapsed")

    # 3. Candling Score Input (Integer 0, 1, 2)
    with st.expander("3. Candling Score (C)", expanded=True):
        st.markdown("""
        <div class='info-detail'>
        <strong>Candling Score (C):</strong> This score is derived from the **Candling Test**. It measures the visibility and movement of the yolk and the size of the air cell. A score of **0** indicates a small air cell and central yolk (freshest); **1** is medium; and **2** is a large air cell and mobile yolk (least fresh). Only whole integers (0, 1, 2) should be used.
        </div>
        """, unsafe_allow_html=True)
        candling_score = st.number_input("Candling Score (C)", min_value=0, max_value=2, step=1, value=0, label_visibility="collapsed")


    if st.button("Calculate Freshness Index"):
        fi_rounded, classification, grade_name, color = calculate_freshness(weight, floating_score, candling_score)
        
        if fi_rounded == "Invalid Score":
            st.error(grade_name)
        else:
            # Display results (using HTML for custom styling similar to the original)
            st.markdown("---")
            st.subheader("Calculation Result")

            color_map = {
                "green": "#10b981", #emerald-500
                "blue": "#3b82f6", #blue-500
                "orange": "#f59e0b" #amber-500
            }

            st.markdown(f"""
                <div style='border: 2px dashed {color_map[color]}; padding: 1.5rem; border-radius: 0.5rem; text-align: center;'>
                    <p style='font-size: 1.25rem; font-weight: bold; color: #1f2937;'>Freshness Index (FI): 
                        <span style='color: #4f46e5;'>{fi_rounded}</span>
                    </p>
                    <div style='background-color: {color_map[color]}30; color: {color_map[color]}; padding: 0.75rem; border-radius: 0.375rem; display: inline-block; margin-top: 0.5rem;'>
                        <p style='font-size: 1.5rem; font-weight: bold;'>{classification}</p>
                    </div>
                    <p style='font-size: 0.875rem; color: #4b5563; margin-top: 0.25rem;'>{grade_name}</p>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- ABOUT US SECTION (HTML copied from original) ---
    st.markdown("""
    <div style="padding: 1.5rem; background-color: white; border-radius: 0.75rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
        <h2 style="font-family: Montserrat, sans-serif; text-align: center; font-size: 1.5rem; color: #1f2937;">
            <span style="color: #4f46e5; margin-right: 0.5rem;">🔬</span> About This Project
        </h2>
        <p style="text-align: center; font-size: 0.875rem; color: #4b5563; margin-bottom: 1rem;">
            CHICK IT! is a research project developed by students of <strong>STEM-12 Bixby</strong> to provide a simple, scientific method for assessing egg quality using observable parameters (Weight, Float Test, and Candling).
        </p>
        <div style="border-top: 1px solid #e5e7eb; padding-top: 1rem; margin-top: 1rem;">
            <h3 style="font-family: Montserrat, sans-serif; text-align: center; color: #4f46e5; margin-bottom: 0.75rem; font-size: 1.125rem;">Researchers and Developers</h3>
            <ul style="list-style: none; padding: 0; text-align: center; font-size: 0.875rem; color: #374151;">
                <li><span style="color: #6b7280;">Lead Researcher & Web Developer:</span> <strong>Ian H. Escalderon</strong></li>
                <li><span style="color: #6b7280;">Researcher:</span> <strong>Louie Rafaell E. Trinchera</strong></li>
                <li><span style="color: #6b7280;">Researcher:</span> <strong>Prince Ezekiel G. Panlaque</strong></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------
# 2. RIGHT COLUMN: GUIDES
# -----------------------------------------------------
with col_guides:
    st.subheader("Guides and Interpretation")
    
    # --- Float Test Guide ---
    st.markdown("""
    <div class="guide-card">
        <h2 style="font-family: Montserrat, sans-serif; font-size: 1.5rem; color: #4f46e5;">
            <span style="font-size: 2rem; margin-right: 0.5rem;">💧</span> Float Test Guide (Floating Score, F)
        </h2>
        <p style='color: #4b5563; margin-bottom: 1rem;'>
            The float test is a simple, visual method to gauge an egg's freshness without cracking it open. It relies on the size of the air cell inside the egg, which expands as the egg ages.
        </p>
        <img src="https://media.discordapp.net/attachments/1439445774172815494/1439475350727032892/Gemini_Generated_Image_gkubbpgkubbpgkub.png?ex=691aa763&is=691955e3&hm=74987a2ff1700a54979d8f20da0ccd396a464675cb20bd182440f76b30021619" style="width: 100%; border-radius: 0.5rem; margin-bottom: 1rem;">
        
        <h3 style="font-family: Montserrat, sans-serif; font-size: 1.125rem; color: #1f2937; margin-bottom: 0.5rem;">Steps and Interpretation:</h3>
        <ul style="list-style-type: disc; padding-left: 20px; font-size: 0.875rem; color: #374151;">
            <li><strong style='color: #059669;'>Grade AA (Very Fresh) - F = 0:</strong> Sinks immediately and lies <strong>completely flat</strong> on its side. <br><span style='font-size: 0.75rem; color: #6b7280;'>Explanation: Tiny air cell; egg is dense and stable.</span></li>
            <li><strong style='color: #2563eb;'>Grade A (Still Fresh) - F = 1:</strong> Sinks but stands <strong>upright or tilted slightly</strong>, with its larger end pointing upwards. <br><span style='font-size: 0.75rem; color: #6b7280;'>Explanation: Small air cell (due to slight moisture loss) at the blunt end causes it to stand up.</span></li>
            <li><strong style='color: #ef4444;'>Grade B (Less Fresh / Older) - F = 2:</strong> The egg will <strong>float</strong> on the surface of the water. <br><span style='font-size: 0.75rem; color: #6b7280;'>Explanation: Significant moisture loss creates a large air cell, providing enough buoyancy to float. Best for baking.</span></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---") # Visual separator between guides

    # --- Candling Guide ---
    st.markdown("""
    <div class="guide-card">
        <h2 style="font-family: Montserrat, sans-serif; font-size: 1.5rem; color: #4f46e5;">
            <span style="font-size: 2rem; margin-right: 0.5rem;">🕯️</span> Candling Guide (Candling Score, C)
        </h2>
        <p style='color: #4b5563; margin-bottom: 1rem;'>
            Candling identifies freshness by observing the air cell size, yolk visibility/mobility, and albumen (white) thickness when the egg is held up to a strong light.
        </p>
        <img src="https://media.discordapp.net/attachments/1439445774172815494/1439475431974637618/eggcandle-day7_1.webp?ex=691aa777&is=691955f7&hm=b7ada3f1fc1da02ae7e7cbc45e620efdc8e3ced9d6e6720cfc205ea5b9054f5e" style="width: 100%; border-radius: 0.5rem; margin-bottom: 1rem;">
        
        <h3 style="font-family: Montserrat, sans-serif; font-size: 1.125rem; color: #1f2937; margin-bottom: 0.5rem;">Candling Interpretation by Age:</h3>
        <ul style="list-style-type: disc; padding-left: 20px; font-size: 0.875rem; color: #374151;">
            <li><strong style='color: #059669;'>🥚 Day 1-2: Very Fresh (Grade AA) - C = 0:</strong> <strong>Air Cell:</strong> Very small ($<1/8$ inch). <strong>Yolk:</strong> Barely visible, centered, and holds position well. <strong>Albumen:</strong> Thick and firm.</li>
            <li><strong style='color: #2563eb;'>🥚 Day 2-5: Slightly Fresh (Grade A) - C = 1:</strong> <strong>Air Cell:</strong> Slightly enlarged ($\text{up to } 3/16$ inch). <strong>Yolk:</strong> Clearer outline, moves slightly but returns to center. <strong>Albumen:</strong> Still reasonably thick.</li>
            <li><strong style='color: #ef4444;'>🥚 Day 6 and Beyond: Less Fresh (Grade B) - C = 2:</strong> <strong>Air Cell:</strong> Large ($>3/16$ inch). <strong>Yolk:</strong> Clearly visible, flatter, moves <strong>readily</strong> away from the center. <strong>Albumen:</strong> Weak and watery.</li>
        </ul>
        <p style='font-size: 0.75rem; font-style: italic; margin-top: 1rem; color: #6b7280;'>
            <strong>Key Reason:</strong> Loss of moisture enlarges the air cell. Loss of $\text{CO}_2$ thins the albumen, causing the yolk to move freely.
        </p>
    </div>
    """, unsafe_allow_html=True)