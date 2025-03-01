import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# === PAGE DE CONNEXION ===
st.set_page_config(page_title="Plateforme de Questionnaires", layout="wide")

VALID_CREDENTIALS = {"user@example.com": "password123"}  # Replace with real credentials

def login():
    st.title("🔒 Authentification")
    email = st.text_input("Adresse e-mail")
    password = st.text_input("Mot de passe", type="password")
    
    if st.button("Se connecter"):
        if email in VALID_CREDENTIALS and VALID_CREDENTIALS[email] == password:
            st.session_state["authenticated"] = True
            st.session_state["email"] = email
            st.rerun()
        else:
            st.error("❌ Email ou mot de passe incorrect.")

if "authenticated" not in st.session_state:
    login()
    st.stop()

# === SÉLECTION DU QUESTIONNAIRE ===
st.sidebar.title("📋 Sélectionnez une enquête")
questionnaires = {
    "A": "Enquête sur la satisfaction des employés.",
    "B": "Enquête sur la performance organisationnelle.",
    "C": "Enquête sur la qualité des services.",
    "D": "Enquête sur l'impact environnemental.",
    "E": "Enquête sur la transformation digitale."
}
selected_survey = st.sidebar.selectbox("Choisissez une enquête :", list(questionnaires.keys()))

if selected_survey:
    st.sidebar.success(f"Vous avez sélectionné l'enquête {selected_survey}.")
    st.sidebar.write(f"📄 {questionnaires[selected_survey]}")

# === FORMULAIRE DE QUESTIONNAIRE ===
st.title("📝 Enquête")

with st.form("survey_form"):
    st.subheader("Informations de base")
    organisation = st.text_input("🏢 Organisation", "")
    nom_complet = st.text_input("👤 Nom complet", "")
    annee = st.selectbox("📅 Année", list(range(2022, 2027)))

    st.subheader("📊 Questions quantitatives (1-5)")
    responses_num = {f"Question {i}": st.number_input(f"Question {i}", min_value=0) for i in range(1, 6)}

    st.subheader("📝 Questions ouvertes (6-10)")
    responses_text = {f"Question {i}": st.text_area(f"Question {i}") for i in range(6, 11)}

    submitted = st.form_submit_button("✅ Soumettre")

if submitted:
    if not organisation or not nom_complet:
        st.error("❌ Veuillez remplir tous les champs obligatoires.")
    else:
        st.success("✅ Merci pour votre participation !")
        
        # Génération du fichier Excel
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Enquete_{now}.xlsx"
        
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            # Enregistrer les données dans des feuilles Excel
            pd.DataFrame({"Organisation": [organisation], "Nom": [nom_complet], "Année": [annee]}).to_excel(writer, sheet_name="Infos", index=False)
            pd.DataFrame.from_dict(responses_num, orient="index").to_excel(writer, sheet_name="Réponses Numériques", header=["Valeur"])
            pd.DataFrame.from_dict(responses_text, orient="index").to_excel(writer, sheet_name="Réponses Textuelles", header=["Réponse"])
        
        output.seek(0)  # ✅ Assurez-vous que le pointeur du fichier est bien au début

        # ✅ Ajout de 'wb' pour garantir la compatibilité avec streamlit
        st.download_button("📥 Télécharger les résultats", data=output, file_name=filename, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
