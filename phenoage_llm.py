import streamlit as st
import numpy as np
import pandas as pd
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import math


def calculate_phenotypic_age(albumin, creatinine, glucose, c_reactive_protein, lymphocyte_percent, 
                             mean_cell_volume, red_blood_cell_distribution_width, alkaline_phosphatase, 
                             white_blood_cell_count, age):
    # Convert biomarker inputs
    albumin_g_L = albumin * 10
    creatinine_umol_L = creatinine * 88.4
    glucose_mmol_L = glucose * 0.0555
    if c_reactive_protein <= 0:
        raise ValueError("C Reactive Protein must be positive for logarithmic conversion.")
    crp_ln = math.log(c_reactive_protein * 0.1)

    b0 = -19.9067

    # Calculate weighted terms
    term_albumin = albumin_g_L * -0.0336
    term_creatinine = creatinine_umol_L * 0.0095
    term_glucose = glucose_mmol_L * 0.1953
    term_crp = crp_ln * 0.0954
    term_lymphocyte = lymphocyte_percent * -0.012
    term_mean_cell_volume = mean_cell_volume * 0.0268
    term_red_cell_dist_width = red_blood_cell_distribution_width * 0.3306
    term_alkaline_phosphatase = alkaline_phosphatase * 0.0019
    term_white_blood_cell_count = white_blood_cell_count * 0.0554
    term_age = age * 0.0804

    # Calculate the linear combination (LinComb)
    xb = (term_albumin + term_creatinine + term_glucose + term_crp + term_lymphocyte + 
          term_mean_cell_volume + term_red_cell_dist_width + term_alkaline_phosphatase + 
          term_white_blood_cell_count + term_age + b0)

    # Adjust Mortality Score calculation
    gamma = 0.0076927
    t_months = 120
    mort_score_part = 1 - math.exp(-math.exp(xb) * (math.exp(gamma * t_months) - 1) / gamma)

    if mort_score_part <= 0:
        raise ValueError("Mortality score calculation part must be positive for logarithmic conversion.")

    if 1 - mort_score_part <= 0:
        raise ValueError("1 - MortScore must be positive for logarithmic conversion.")

    # Calculate Phenotypic Age using Mortality Score
    ptypic_age = 141.50225 + math.log(-0.00553 * math.log(1 - mort_score_part)) / 0.09165

    dnam_phenoage = ptypic_age / (1 + 1.28047 * math.exp(0.0344329 * (-182.344 + ptypic_age)))

    return dnam_phenoage

def parse_lab_report(lab_report):
    chat = ChatOpenAI(model="gpt-4o", temperature=0)

    system_message = SystemMessage(content="""
    You are an AI assistant that helps parse unstructured lab reports and extract relevant information.
    The lab report will be provided in the next message. Your task is to extract the following values from the report:
    - albumin
    - creatinine
    - glucose
    - c_reactive_protein
    - lymphocyte_percent
    - mean_cell_volume
    - red_blood_cell_distribution_width
    - alkaline_phosphatase
    - white_blood_cell_count
    - age

    Note: The keys should be exactly as specified above, without units. The values should be the numeric values extracted from the report. 
    Make sure to look for common alternative names for these results, such as 'lymphocyte' for 'lymphocyte_percent', but only use the names above when listing them.

    Respond with a JSON object containing the extracted values, using the keys exactly as specified above in lowercase with underscores.

    Your response should start with "{" and end with "}".
    """)

    human_message = HumanMessage(content=lab_report)

    response = chat.invoke([system_message, human_message])
    assistant_message = response.content.strip()

    if not assistant_message:
        st.error("Received an empty response from the assistant.")
        return {}

    # Remove the "json" prefix if present
    if assistant_message.startswith("json"):
        assistant_message = assistant_message[assistant_message.index("{"):].strip()

    # Remove any extra formatting characters
    assistant_message = assistant_message.strip('```')

    assistant_message = assistant_message.replace('json', '')
    assistant_message = assistant_message.strip()

    # Attempt JSON parsing
    try:
        structured_data = json.loads(assistant_message)
    except json.JSONDecodeError as e:
        st.error(f"Error parsing the lab report: {e}")
        return {}

    # Provide default values for missing or null values
    for key in ["albumin", "creatinine", "glucose", "c_reactive_protein", "lymphocyte_percent",
                "mean_cell_volume", "red_blood_cell_distribution_width", "alkaline_phosphatase",
                "white_blood_cell_count", "age"]:
        if key not in structured_data or structured_data[key] is None:
            structured_data[key] = np.nan

    return structured_data

def main():
    st.title("Phenoage Calculator")
    st.write("Enter your labwork results to calculate your phenoage.")

    lab_report = st.text_area("Paste your lab report here:", height=200)

    if st.button("Calculate"):
        structured_data = parse_lab_report(lab_report)

        if structured_data:
            albumin = structured_data.get("albumin", np.nan)
            creatinine = structured_data.get("creatinine", np.nan)
            glucose = structured_data.get("glucose", np.nan)
            c_reactive_protein = structured_data.get("c_reactive_protein", np.nan)
            lymphocyte_percent = structured_data.get("lymphocyte_percent", np.nan)
            mean_cell_volume = structured_data.get("mean_cell_volume", np.nan)
            red_blood_cell_distribution_width = structured_data.get("red_blood_cell_distribution_width", np.nan)
            alkaline_phosphatase = structured_data.get("alkaline_phosphatase", np.nan)
            white_blood_cell_count = structured_data.get("white_blood_cell_count", np.nan)
            age = structured_data.get("age", np.nan)

            if np.isnan(age):
                age = st.number_input("Enter your age:", min_value=0, max_value=120, value=30)

            if all(pd.notna([albumin, creatinine, glucose, c_reactive_protein, lymphocyte_percent,
                             mean_cell_volume, red_blood_cell_distribution_width, alkaline_phosphatase,
                             white_blood_cell_count, age])):
                phenoage = calculate_phenotypic_age(albumin, creatinine, glucose, c_reactive_protein,
                                              lymphocyte_percent, mean_cell_volume,
                                              red_blood_cell_distribution_width, alkaline_phosphatase,
                                              white_blood_cell_count, age)
                st.write(f"Your phenoage is: {phenoage:.2f} years")
            else:
                st.error("Some values are missing or invalid. Please ensure all values are provided and try again.")
        else:
            st.error("Failed to parse the lab report. Please ensure the lab report format is correct and try again.")

if __name__ == "__main__":
    main()
