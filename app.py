import streamlit as st
import pandas as pd
import os
import csv

# ---------------------------
# Page Configuration
# ---------------------------
st.set_page_config(
    page_title="💡 The Light Archive",
    layout="wide"
)

#---------------------------
# ADD TITLE
#---------------------------

st.markdown("""
    <div style='text-align: center; padding: 1rem 1rem;'>
        <h1 style='font-size: 2.8rem;'>💡 The Light Archive</h1>
        <p style='font-size: 1.3rem; max-width: 700px; margin: auto; line-height: 1.6;'>
            A digital storytelling platform transforming racialized isolation 
            into collective visibility.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------
# CSS for Colors & Tabs
# ---------------------------
st.markdown("""
<style>
/* App background */
body, .stApp {
    background-color: #000000;
    color: white;
}

/* Streamlit tabs styling */
div[role="tab"] {
    background-color: #007A33;  /* Green tabs */
    color: white;
    font-weight: bold;
    border-radius: 5px 5px 0 0;
    padding: 10px 15px;
    margin-right: 2px;
}

/* Hover effect for tabs */
div[role="tab"]:hover {
    background-color: #E10600;  /* Red hover */
    color: white;
}

/* Selected tab */
div[role="tab"][aria-selected="true"] {
    background-color: #007A33;  /* Green selected */
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# CSV File Setup
# ---------------------------
DATA_FILE = "archive.csv"

# Ensure CSV exists
if not os.path.exists(DATA_FILE):
    pd.DataFrame(
        columns=["title", "city", "theme", "dimmed", "reclaimed"]
    ).to_csv(DATA_FILE, index=False, quoting=csv.QUOTE_ALL)

# Read CSV safely
try:
    df = pd.read_csv(DATA_FILE, quoting=csv.QUOTE_ALL)
except pd.errors.EmptyDataError:
    df = pd.DataFrame(columns=["title", "city", "theme", "dimmed", "reclaimed"])

# ---------------------------
# Tabs Navigation
# ---------------------------
tab_home, tab_explore, tab_submit, tab_about = st.tabs([
    "Home", "Explore the Archive", "Submit Your Story", "About"
])

# ===================================
# HOME TAB
# ===================================
with tab_home:

    st.markdown("---")

    # ====== Landing Section ======
    st.write("")  # Top padding
    st.write("")
    # Subtitle / tagline
    st.markdown("<h3 style='text-align: center; color: #ffffff;'>A space where Black youth stories are seen, shared, and celebrated</h3>", unsafe_allow_html=True)
    st.write("")
    st.write("")

    # Main paragraph - centered using markdown trick
    st.markdown(
        """
    <p style='text-align: center; font-size: 1.2rem; line-height: 1.8; max-width: 800px; margin: auto;'>
    💡The Light Archive is a space where the experiences of Black youth are seen, shared, and celebrated. Here, stories of moments when one’s potential was overlooked, underestimated, or challenged are collected. By shining a light on these experiences, we turn isolation into visibility, personal struggles into shared understanding, and private victories into collective inspiration. Every story submitted helps reveal patterns, builds community awareness, and reminds everyone that even when light is dimmed, it can always be reclaimed.
    </p>
    """,
        unsafe_allow_html=True
    )

    st.write("")  # bottom padding
    st.write("")
    st.write("---")  # horizontal line to separate from next section
    st.write("")
    st.write("Explore the archive or contribute your story using the tabs above!")

# ===================================
# EXPLORE TAB
# ===================================
with tab_explore:
    st.header("Explore Stories")
    if df.empty:
        st.info("No stories have been submitted yet.")
    else:
        theme_options = ["All"] + sorted(df["theme"].dropna().unique())
        theme_filter = st.selectbox("Filter by Theme", theme_options)

        filtered_df = df if theme_filter == "All" else df[df["theme"] == theme_filter]

        for _, row in filtered_df.iterrows():
            title_display = row["title"] if pd.notna(row["title"]) and row["title"] != "" else "Untitled Story"
            city_display = f" ({row['city']})" if pd.notna(row["city"]) and row["city"] != "" else ""

            with st.expander(f"{title_display}{city_display}"):
                st.subheader("When My Light Felt Dimmed")
                st.write(row["dimmed"])
                st.subheader("How I Reclaimed or Am Rebuilding It")
                st.write(row["reclaimed"])

# ===================================
# SUBMIT TAB
# ===================================
with tab_submit:
    st.header("Submit Your Story")
    st.markdown("""
This prototype demonstrates submission functionality.  
In a full implementation, submissions would be stored in a secure database with moderation safeguards.
""")

    with st.form("submission_form", clear_on_submit=True):
        title = st.text_input("Story Title (Optional)")
        city = st.text_input("City (Optional)")
        theme = st.selectbox(
            "Theme",
            [
                "Academic Streaming",
                "Stereotype Threat",
                "Underrepresentation",
                "Discipline Disparities",
                "Code-Switching Fatigue",
                "Other"
            ]
        )
        dimmed = st.text_area("When My Light Felt Dimmed")
        reclaimed = st.text_area("How I Reclaimed or Am Rebuilding It")
        submitted = st.form_submit_button("Submit Story")

        if submitted:
            if dimmed.strip() == "" or reclaimed.strip() == "":
                st.error("Please complete both story sections before submitting.")
            else:
                new_entry = pd.DataFrame(
                    [[title, city, theme, dimmed, reclaimed]],
                    columns=["title", "city", "theme", "dimmed", "reclaimed"]
                )
               new_entry.to_csv(DATA_FILE, mode="a", header=False, index=False, quoting=csv.QUOTE_ALL, lineterminator="\n")
                st.success("Your story has been added to the archive.")

# ===================================
# ABOUT TAB
# ===================================
with tab_about:
    st.header("About The Light Archive 💡")
    st.markdown("""
**Purpose:**  
The Light Archive is a platform designed to collect and showcase stories of Black youth 
whose potential has been questioned, overlooked, or misunderstood. Each story highlights 
how individuals have reclaimed their light, offering inspiration and insight into shared experiences.

**How It Works:**  
- Explore stories across different themes of systemic barriers and personal triumphs.  
- Submit your own experiences to help others see patterns, resilience, and community solutions.  

**Why It Matters:**  
By giving space to these narratives, we turn isolation into visibility, making structural 
challenges apparent and fostering collective empowerment.

""")
