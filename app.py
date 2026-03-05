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

# ---------------------------
# TITLE
# ---------------------------
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
body, .stApp {
    background-color: #000000;
    color: white;
}
div[role="tab"] {
    background-color: #007A33;
    color: white;
    font-weight: bold;
    border-radius: 5px 5px 0 0;
    padding: 10px 15px;
    margin-right: 2px;
}
div[role="tab"]:hover {
    background-color: #E10600;
    color: white;
}
div[role="tab"][aria-selected="true"] {
    background-color: #007A33;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# CSV File Setup
# ---------------------------
DATA_FILE = "archive.csv"
COLUMNS = ["title", "city", "theme", "dimmed", "reclaimed"]

# Ensure CSV exists
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(
        DATA_FILE, index=False, quoting=csv.QUOTE_ALL, line_terminator="\n"
    )

# Safe CSV read
try:
    df = pd.read_csv(DATA_FILE, quoting=csv.QUOTE_ALL)
except (pd.errors.EmptyDataError, pd.errors.ParserError):
    df = pd.DataFrame(columns=COLUMNS)

# ---------------------------
# Tabs
# ---------------------------
tab_home, tab_explore, tab_submit, tab_about = st.tabs([
    "Home", "Explore the Archive", "Submit Your Story", "About"
])

# ---------------------------
# HOME TAB
# ---------------------------
with tab_home:
    st.markdown("---")
    st.markdown(
        "<h3 style='text-align: center; color: #ffffff;'>A space where Black youth stories are seen, shared, and celebrated</h3>",
        unsafe_allow_html=True
    )
    st.markdown(
        """
<p style='text-align: center; font-size: 1.2rem; line-height: 1.8; max-width: 800px; margin: auto;'>
💡The Light Archive collects the stories of Black youth whose potential was questioned, underestimated, or challenged. By sharing these experiences, isolation becomes visibility and personal triumphs become collective inspiration. Every story helps reveal patterns, build awareness, and remind everyone that even when light is dimmed, it can be reclaimed.
</p>
""",
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.write("Explore the archive or contribute your story using the tabs above!")

# ---------------------------
# EXPLORE TAB
# ---------------------------
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

# ---------------------------
# SUBMIT TAB
# ---------------------------
with tab_submit:
    st.header("Submit Your Story")
    st.markdown("This is a prototype. Submissions are appended safely to the CSV.")

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
                    columns=COLUMNS
                )
                new_entry.to_csv(
                    DATA_FILE,
                    mode="a",
                    header=False,
                    index=False,
                    quoting=csv.QUOTE_ALL,
                    lineterminator="\n"
                )
                st.success("Your story has been added to the archive.")

# ---------------------------
# ABOUT TAB
# ---------------------------
with tab_about:
    st.header("About The Light Archive 💡")
    st.markdown("""
**Purpose:**  
The Light Archive collects and showcases stories of Black youth whose potential has been questioned or underestimated.

**How It Works:**  
- Explore stories across different themes.  
- Submit your own experiences safely.  

**Why It Matters:**  
By sharing these narratives, isolation becomes visibility, and collective understanding grows.
""")

