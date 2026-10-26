import io
import os
import re
import base64
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Simulateur Commercial Madagascar", layout="wide"
)

# ==========================================
# LECTURE DU LOGO STAR (Fichier local)
# ==========================================
try:
    with open("star.png", "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Logo STAR">'
except Exception:
    logo_html = '<p style="color:#E3000F; font-weight:bold; font-size:1.5rem;">STAR ★</p>'

# ==========================================
# THÈME GLOBAL - CHARTE GRAPHIQUE STAR
# ==========================================
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;900&display=swap');
    [data-testid="stAppViewContainer"] > .main {{ padding-top: 1rem !important; }}
    .block-container {{ padding-top: 1rem !important; }}
    [data-testid="stSidebarUserContent"] {{ padding-top: 0rem !important; }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:first-child {{ margin-top: -20px !important; }}
    html, body, [class*="css"] {{ font-family: 'Montserrat', sans-serif; }}

    .header-star {{
        background: #ffffff; border-radius: 10px; box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        margin-bottom: 20px; margin-top: 0px; position: relative; overflow: hidden;
        border-left: 8px solid transparent; border-image: linear-gradient(to bottom, #E3000F 50%, #009639 50%) 1;
        display: flex; align-items: center; justify-content: center; height: 100px; 
    }}
    .header-star::before {{
        content: ''; position: absolute; top: -80px; right: -80px; width: 300px; height: 300px;
        background: radial-gradient(circle, rgba(227,0,15,0.05) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%; pointer-events: none;
    }}
    .header-star::after {{
        content: ''; position: absolute; bottom: -80px; left: 20%; width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(0,150,57,0.05) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%; pointer-events: none;
    }}
    .header-title-star {{
        font-size: 2.2rem; font-weight: 900; color: #1a1a1a; margin: 0; padding: 0; line-height: 1;
        text-transform: uppercase; letter-spacing: -0.5px; position: relative; z-index: 1; text-align: center;
    }}
    .text-red {{ color: #E3000F; }}
    .star-icon {{
        position: absolute; right: 30px; top: 50%; transform: translateY(-50%); color: #E3000F;
        font-size: 2.2rem; animation: spin-star 4s linear infinite; text-shadow: 2px 2px 4px rgba(227,0,15,0.2); z-index: 1;
    }}
    @keyframes spin-star {{
        0% {{ transform: translateY(-50%) rotate(0deg) scale(1); }}
        50% {{ transform: translateY(-50%) rotate(180deg) scale(1.1); }}
        100% {{ transform: translateY(-50%) rotate(360deg) scale(1); }}
    }}
    h2, h3 {{
        color: #E3000F !important; font-family: 'Montserrat', sans-serif; font-weight: 700 !important;
        background-color: #f0f4f8; border-left: 6px solid #E3000F; padding: 6px 15px !important;
        margin-top: 15px !important; margin-bottom: 15px !important; border-radius: 6px; box-shadow: none;
        border-top: none; border-right: none; border-bottom: none; display: flex; justify-content: center; align-items: center;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }}
    h2 {{ font-size: 1.5rem !important; }}
    h3 {{ font-size: 1.3rem !important; }}
    hr {{ margin-top: 10px !important; margin-bottom: 10px !important; }}
    [data-testid="stSidebar"] {{ background-color: #f8f9fa; border-right: 4px solid #009639; }}
    .sidebar-logo-container {{ text-align: center; padding: 0 0 10px 0; margin-bottom: 10px; border-bottom: 1px solid #e0e0e0; }}
    .sidebar-logo-container img {{ max-width: 160px; height: auto; }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: #009639 !important; background-color: transparent; border: none; box-shadow: none;
        padding: 0; margin-top: 10px; margin-bottom: 10px; display: block; white-space: nowrap; font-size: 1.2rem !important; line-height: 1.3;
    }}
    .stButton>button, .stDownloadButton>button {{
        background-color: #E3000F !important; color: white !important; border-radius: 5px; border: none;
        font-weight: 600; padding: 0.5rem 1rem; transition: 0.3s;
    }}
    .stButton>button:hover, .stDownloadButton>button:hover {{ background-color: #b3000b !important; }}
    .streamlit-expanderHeader {{ background-color: #f0f4f8 !important; color: #E3000F !important; font-weight: 700; border-left: 4px solid #009639; }}
    .stTabs [data-baseweb="tab-list"] button {{ background-color: transparent; color: #333; font-weight: 600; }}
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{ color: #E3000F !important; border-bottom-color: #E3000F !important; }}
    [data-testid="stMetricValue"] {{ color: #E3000F; font-size: 1.6rem !important; font-weight: 700; }}
    [data-testid="stMetricLabel"] {{ color: #009639; font-size: 0.9rem !important; font-weight: 600; }}
    .stDataFrame {{ border: 1px solid #e0e0e0; border-radius: 5px; }}
    [data-testid="stPlotlyChart"] {{ margin-top: 0px !important; margin-bottom: 0px !important; padding-top: 0px !important; padding-bottom: 0px !important; }}
    .js-plotly-plot .plotly .main-svg {{ border-radius: 8px; }}
    .kpi-container {{ display: flex; gap: 15px; margin-bottom: 20px; }}
    .kpi-card {{
        flex: 1; background-color: #ffffff; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        border: 1px solid #eaeaea; overflow: hidden; text-align: center; padding-bottom: 15px; position: relative;
    }}
    .kpi-header {{ color: white; font-weight: 700; font-size: 0.85rem; padding: 6px 5px; text-transform: uppercase; letter-spacing: 0.5px; }}
    .bg-star-green {{ background-color: #009639; }}
    .bg-star-red {{ background-color: #E3000F; }}
    .kpi-value {{ font-size: 1.8rem; font-weight: 800; color: #333333; margin: 15px 0 5px 0; line-height: 1; }}
    .kpi-sub {{ font-size: 0.8rem; color: #666666; font-weight: 500; display: flex; justify-content: center; align-items: center; gap: 5px; }}
    .kpi-arrow-up {{ color: #70ad47; font-weight: bold; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="header-star">
        <div class="header-title-star">
            <span class="text-red">Simulateur Stratégique & Optimisation Commerciale</span>
        </div>
        <span class="star-icon">★</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# COMPATIBILITÉ PLOTLY 5 / 6
# ==========================================
_HAS_SCATTER_MAPBOX = hasattr(px, "scatter_mapbox")

def scatter_map_auto(df, **kwargs):
    if _HAS_SCATTER_MAPBOX:
        return px.scatter_mapbox(df, **kwargs)
    if "mapbox_style" in kwargs:
        kwargs["map_style"] = kwargs.pop("mapbox_style")
    return px.scatter_map(df, **kwargs)

def apply_marker_style(fig, size=6, opacity=0.75):
    for trace in fig.data:
        try:
            trace.marker.size = size
            trace.marker.opacity = opacity
        except Exception:
            pass

# ==========================================
# 1. DONNÉES DE BASE (Modèle par défaut)
# ==========================================
@st.cache_data
def load_base_data():
    data = {
        "Région": [
            "Centre", "Centre", "Est", "Est", "Nord", "Nord", "Nord",
            "Nord", "Nord", "Sud", "Sud", "Sud", "Sud", "Sud", "Sud",
        ],
        "Agence": [
            "11-Andranomahery", "12-Antsirabe", "01-Tanjombato", "09-Tamatave",
            "03-Usine-Diego", "07-Majunga", "18-Ambanja", "19-Sambava",
            "21-Nosy-Be", "04-Tulear", "05-Fianarantsoa", "06-Ihosy",
            "08-Manakara", "23-Morondava", "24-Fort-Dauphin",
        ],
        "MV": [5, 2, 5, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1],
        "CS_Actuels": [32, 13, 31, 18, 6, 10, 6, 5, 4, 7, 8, 3, 4, 4, 5],
        "Ajustement_CS_DRV": [6, 3, 6, 3, 1, 3, 2, 2, 1, 2, 0, 1, 2, 2, 1],
        "Vol_2026_Hls": [
            843256, 306183, 878064, 511164, 189959, 338706, 213219,
            150744, 142658, 202606, 138452, 86860, 202880, 85204, 113113,
        ],
        "Vol_2027_Hls": [
            902190, 339742, 976891, 547209, 187677, 366320, 238634,
            172094, 161164, 227276, 155168, 97400, 235379, 96757, 119372,
        ],
        "Nbre_PDV_Tradi": [
            5950, 2450, 5987, 5307, 1009, 2830, 2400, 800, 1300,
            1365, 1500, 700, 1550, 930, 950,
        ],
        "Temps_Dispo_Mois_Min": [
            601920, 253440, 586080, 332640, 110880, 205920, 126720,
            110880, 79200, 142560, 126720, 63360, 95040, 95040, 95040,
        ],
        "Vol_ZB_Inclut_Mois_Hls": [
            215, 0, 4005, 0, 70, 2950, 0, 0, 0, 2473, 0, 0, 0, 0, 0,
        ],
        "PDV_Estimes_ZB": [50, 0, 850, 0, 30, 600, 0, 0, 0, 500, 0, 0, 0, 0, 0],
        "Lat": [
            -18.8792, -19.8658, -18.9667, -18.1492, -12.2786, -15.7167,
            -13.6773, -14.2667, -13.3167, -23.3500, -21.4333, -22.4000,
            -22.1333, -20.2833, -25.0200,
        ],
        "Lon": [
            47.5079, 47.0333, 47.5333, 49.4023, 49.2917, 46.3167,
            48.4501, 50.1667, 48.2667, 43.6667, 47.0833, 46.1333,
            48.0167, 44.2833, 46.9900,
        ],
    }
    return pd.DataFrame(data)

# ==========================================
# NOUVEAU : UPLOAD ET CHOIX OUI/NON AVEC CALLBACK ET TRADUCTION ROBUSTE
# ==========================================
if "radio_defaults" not in st.session_state:
    st.session_state.radio_defaults = "NON"

def handle_upload_change():
    st.session_state.radio_defaults = "NON"

col_upload1, col_upload2 = st.columns(2)

with col_upload1:
    _uploaded_data = st.file_uploader(
        "1. Charger le fichier Excel des données Agences",
        type=["xlsx", "xls"],
        key="upload_data",
        on_change=handle_upload_change
    )
    
    use_defaults_choice = st.radio(
        "Voulez-vous utiliser les données par défaut ?",
        options=["NON", "OUI"],
        horizontal=True,
        key="radio_defaults",
        help="Choisissez 'OUI' pour afficher le tableau de bord avec les données par défaut."
    )

with col_upload2:
    _uploaded_gps = st.file_uploader(
        "2. Charger le fichier Excel des coordonnées GPS (Coord_GPS.xlsx)",
        type=["xlsx", "xls"],
        key="upload_gps"
    )

# ==========================================
# LOGIQUE DE CHARGEMENT DES DONNÉES AVEC TRADUCTION DE COLONNES
# ==========================================
if _uploaded_data:
    try:
        df_raw = pd.read_excel(_uploaded_data)
        
        # 1. NETTOYAGE STRICT DES COLONNES (Anti-doublons et espaces)
        df_raw.columns = df_raw.columns.astype(str).str.replace('\n', ' ').str.strip()
        df_raw = df_raw.loc[:, ~df_raw.columns.str.startswith('Unnamed')]
        df_raw = df_raw.loc[:, ~df_raw.columns.duplicated(keep='first')]

        # 2. NETTOYAGE DES LIGNES DE TOTAL
        agence_cols = [c for c in df_raw.columns if c.lower() == 'agence']
        if agence_cols:
            agence_col = agence_cols[0]
            df_raw = df_raw[df_raw[agence_col].notna() & (~df_raw[agence_col].astype(str).str.upper().str.startswith('TOTAL'))]

        # 3. TRADUCTION FLEXIBLE DES COLONNES
        rename_dict = {}
        for col in df_raw.columns:
            col_upper = str(col).upper()
            if col_upper == 'AGENCE':
                rename_dict[col] = 'Agence'
            elif 'TOTAL CS' in col_upper or 'CS_ACTUELS' in col_upper:
                rename_dict[col] = 'CS_Actuels'
            elif 'VOLUME 2026' in col_upper or 'VOL_2026_HLS' in col_upper:
                rename_dict[col] = 'Vol_2026_Hls'
            elif 'VOLUME 2027' in col_upper or 'VOL_2027_HLS' in col_upper:
                rename_dict[col] = 'Vol_2027_Hls'
            elif 'UNIVERS TRADI' in col_upper or 'NBRE_PDV_TRADI' in col_upper:
                rename_dict[col] = 'Nbre_PDV_Tradi'
            elif col_upper == 'MV':
                rename_dict[col] = 'MV'
            elif 'RÉGION' in col_upper or 'REGION' in col_upper:
                rename_dict[col] = 'Région'
        
        df_raw = df_raw.rename(columns=rename_dict)
        df_raw = df_raw.loc[:, ~df_raw.columns.duplicated(keep='first')]

        # 4. REMPLIR LA COLONNE RÉGION (Correction pour les cellules fusionnées Excel)
        if "Région" in df_raw.columns:
            df_raw["Région"] = df_raw["Région"].ffill()
        else:
            df_raw["Région"] = "Inconnue"

        # 5. SUPPRESSION DES COLONNES CALCULÉES (si présentes dans le fichier)
        cols_to_drop = ["Total_CS_Propose", "Evol_Vol_Abs", "Evol_Vol_Pct", "PDV_Total_Ajuste", 
                        "Vol_2027_Par_CS", "Vol_2027_Par_MV", "PDV_Par_CS", "PDV_Par_MV", "Ratio_CS_MV"]
        df_raw = df_raw.drop(columns=[c for c in cols_to_drop if c in df_raw.columns])

        # 6. AJOUT DES COLONNES MANQUANTES AVEC VALEURS PAR DÉFAUT
        if "Ajustement_CS_DRV" not in df_raw.columns:
            df_raw["Ajustement_CS_DRV"] = 0
        if "Temps_Dispo_Mois_Min" not in df_raw.columns:
            df_raw["Temps_Dispo_Mois_Min"] = 600000
        if "Vol_ZB_Inclut_Mois_Hls" not in df_raw.columns:
            df_raw["Vol_ZB_Inclut_Mois_Hls"] = 0
        if "PDV_Estimes_ZB" not in df_raw.columns:
            df_raw["PDV_Estimes_ZB"] = 0

        # 7. FORCER LES COLONNES NUMÉRIQUES
        numeric_cols = ["MV", "CS_Actuels", "Ajustement_CS_DRV", "Vol_2026_Hls", "Vol_2027_Hls", 
                        "Nbre_PDV_Tradi", "Temps_Dispo_Mois_Min", "Vol_ZB_Inclut_Mois_Hls", "PDV_Estimes_ZB"]
        for col in numeric_cols:
            if col in df_raw.columns:
                if isinstance(df_raw[col], pd.DataFrame):
                    df_raw[col] = df_raw[col].iloc[:, 0]
                df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce').fillna(0)

        # 8. RÉCUPÉRATION AUTOMATIQUE DES COORDONNÉES GPS (Lat/Lon)
        base_df = load_base_data()
        if "Lat" not in df_raw.columns or "Lon" not in df_raw.columns:
            df_raw = df_raw.drop(columns=[c for c in ["Lat", "Lon"] if c in df_raw.columns])
            df_raw = df_raw.merge(base_df[["Agence", "Lat", "Lon"]], on="Agence", how="left")
            df_raw["Lat"] = df_raw["Lat"].fillna(-18.79)
            df_raw["Lon"] = df_raw["Lon"].fillna(46.85)

        # 9. VÉRIFICATION FINALE
        required_cols = [
            "Région", "Agence", "MV", "CS_Actuels", "Ajustement_CS_DRV",
            "Vol_2026_Hls", "Vol_2027_Hls", "Nbre_PDV_Tradi",
            "Temps_Dispo_Mois_Min", "Vol_ZB_Inclut_Mois_Hls",
            "PDV_Estimes_ZB", "Lat", "Lon"
        ]
        missing = [c for c in required_cols if c not in df_raw.columns]
        if missing:
            st.error(f"❌ Colonnes manquantes dans le fichier Excel : {missing}. Le modèle par défaut est utilisé.")
            df_raw = load_base_data()
        else:
            st.success("✅ Données Agences chargées et traduites avec succès !")

    except Exception as e:
        st.error(f"❌ Erreur de lecture du fichier : {e}")
        df_raw = load_base_data().iloc[0:0]

elif use_defaults_choice == "OUI":
    df_raw = load_base_data()
    st.info("ℹ️ **Mode par défaut activé :** Affichage des données par défaut de l'application.")

else:
    df_raw = load_base_data().iloc[0:0]
    st.warning("⚠️ **En attente de données :** Uploadez un fichier Excel ou sélectionnez 'OUI' pour utiliser les valeurs par défaut.")

# ==========================================
# 2. PARSING DMS (GPS)
# ==========================================
def _dms_to_dec_single(txt):
    if not isinstance(txt, str):
        return None, None
    s = (txt.replace("?", "°")
            .replace("’", "'").replace("′", "'")
            .replace("″", '"').replace("”", '"')
            .replace(",", " "))
    pattern = r"(\d+)\s*°\s*(\d+)\s*'\s*([\d.]+)\s*\"?\s*([NSEW])"
    matches = re.findall(pattern, s)
    if len(matches) < 2:
        return None, None
    lat = lon = None
    for d, m, sec, dir_ in matches:
        val = float(d) + float(m) / 60 + float(sec) / 3600
        if dir_ in ("S", "W"):
            val = -val
        if dir_ in ("N", "S"):
            lat = val
        else:
            lon = val
    return lat, lon

# ==========================================
# 3. CHARGEMENT GPS
# ==========================================
def _find_gps_column(columns):
    alias = (
        "gps", "coordonnees", "coordonnées", "coordonnee", "coordonnée",
        "position", "localisation", "coordonnees_gps", "point_gps",
        "gps_coord", "coord",
    )
    for col in columns:
        if str(col).strip().lower() in alias:
            return col
    return None

@st.cache_data
def load_gps_data(_uploaded_file=None):
    if _uploaded_file is None:
        return pd.DataFrame()

    source = _uploaded_file
    try:
        xls = pd.ExcelFile(source)
        sheet_names = xls.sheet_names
    except Exception as e:
        st.error(f"❌ Impossible d'ouvrir le classeur GPS : {e}")
        return pd.DataFrame()

    sheet_to_use = None
    for sh in sheet_names:
        try:
            tmp = pd.read_excel(source, sheet_name=sh, nrows=5)
            tmp.columns = [str(c).strip() for c in tmp.columns]
            if _find_gps_column(tmp.columns) is not None:
                sheet_to_use = sh
                break
        except Exception:
            continue

    if sheet_to_use is None:
        for c in ["Feuil1", "Feuille1", "Sheet1", "GPS", "Coordonnees",
                  "Coordonnées", "Data", "Clients"]:
            if c in sheet_names:
                sheet_to_use = c
                break

    if sheet_to_use is None:
        sheet_to_use = sheet_names[0]

    try:
        df_gps = pd.read_excel(source, sheet_name=sheet_to_use)
    except Exception as e:
        st.error(f"❌ Erreur de lecture de la feuille GPS `{sheet_to_use}` : {e}")
        return pd.DataFrame()

    df_gps.columns = [str(c).strip() for c in df_gps.columns]

    if not df_gps.empty and str(df_gps.iloc[0].get("Ag", "")).strip() == "Ag":
        df_gps = df_gps.iloc[1:].reset_index(drop=True)

    gps_col = _find_gps_column(df_gps.columns)
    if gps_col is None:
        st.error(
            f"❌ Aucune colonne GPS trouvée. Colonnes disponibles : "
            f"{list(df_gps.columns)}"
        )
        return pd.DataFrame()

    coords = df_gps[gps_col].apply(_dms_to_dec_single)
    df_gps["Lat"] = [c[0] for c in coords]
    df_gps["Lon"] = [c[1] for c in coords]

    df_gps = df_gps.dropna(subset=["Lat", "Lon"])
    df_gps = df_gps[
        df_gps["Lat"].between(-26, -11) & df_gps["Lon"].between(42, 51)
    ]

    st.success(
        f"✅ Fichier GPS chargé — feuille `{sheet_to_use}` — "
        f"{len(df_gps):,} points valides."
    )
    return df_gps.reset_index(drop=True)

df_clients_gps = load_gps_data(_uploaded_gps) if _uploaded_gps else pd.DataFrame()

# ==========================================
# AJOUT DU LIEN DE REDIRECTION VERS LA CARTE
# ==========================================
if not df_clients_gps.empty:
    st.markdown(
        """
        <style>
        .link-carte {
            display: inline-flex; align-items: center; gap: 6px; background-color: #E3000F;
            color: white !important; text-decoration: none; padding: 5px 12px; border-radius: 5px;
            font-weight: 600; font-size: 0.8rem; margin-bottom: 10px; transition: 0.2s;
            box-shadow: 0 2px 5px rgba(227,0,15,0.2);
        }
        .link-carte:hover {
            background-color: #b3000b; color: white !important; box-shadow: 0 4px 10px rgba(227,0,15,0.3);
        }
        </style>
        <a href="#section-carte" class="link-carte">🗺️ Accéder à la carte</a>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# 4. SIDEBAR — LOGO ET PARAMÈTRES
# ==========================================
st.sidebar.markdown(
    f"""
    <div class="sidebar-logo-container">
        {logo_html}
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("⚙️ Paramètres & Seuils d'Évaluation")

obj_visites_jour = st.sidebar.number_input("Objectif Visites max / Commercial / Jour", 1, 35, 22)
jours_travailles_mois = st.sidebar.number_input("Jours travaillés / mois", 15, 26, 20)
temps_moyen_visite_min = st.sidebar.number_input("Temps moyen par visite (min)", 10, 90, 30)
cible_vol_cs = st.sidebar.number_input("Volume Cible par CS (Hls/an)", 1000, 50000, 25000, 1000)

st.sidebar.subheader("Seuils de Charge")
seuil_surcharge_cs = st.sidebar.number_input("Seuil Surcharge CS (> X PDV)", 200, 500, 250)
seuil_risque_cs = st.sidebar.number_input("Seuil Risque CS (> X PDV)", 180, 400, 210)
seuil_sous_charge_cs = st.sidebar.number_input("Seuil Sous-charge CS (< X PDV)", 50, 200, 150)
seuil_surcharge_mv = st.sidebar.number_input("Seuil Surcharge MV (> X Hls vol)", 20000, 500000, 200000)

st.sidebar.subheader("🎯 Simulation Zones Blanches par Agence")

if not df_raw.empty:
    selected_agence_zb = st.sidebar.selectbox("Sélectionner une Agence", df_raw["Agence"].unique())
    default_zb_vol = int(df_raw.loc[df_raw["Agence"] == selected_agence_zb, "Vol_ZB_Inclut_Mois_Hls"].values[0])
    default_zb_pdv = int(df_raw.loc[df_raw["Agence"] == selected_agence_zb, "PDV_Estimes_ZB"].values[0])
    
    sim_zb_vol_mois = st.sidebar.number_input(f"Volume ZB Mensuel ({selected_agence_zb})", 0, 10000, default_zb_vol)
    sim_zb_pdv = st.sidebar.number_input(f"PDV ZB ({selected_agence_zb})", 0, 2000, default_zb_pdv)
    
    df = df_raw.copy()
    df.loc[df["Agence"] == selected_agence_zb, "Vol_ZB_Inclut_Mois_Hls"] = sim_zb_vol_mois
    df.loc[df["Agence"] == selected_agence_zb, "PDV_Estimes_ZB"] = sim_zb_pdv
else:
    st.sidebar.info("Sélectionnez des données pour voir les options.")
    df = df_raw.copy()

# ==========================================
# 5. CALCULS DYNAMIQUES
# ==========================================
df["Total_CS_Propose"] = df["CS_Actuels"] + df["Ajustement_CS_DRV"]
df["Evol_Vol_Abs"] = df["Vol_2027_Hls"] - df["Vol_2026_Hls"]
df["Evol_Vol_Pct"] = (df["Evol_Vol_Abs"] / df["Vol_2026_Hls"].replace(0, np.nan)) * 100
df["Evol_Vol_Pct"] = df["Evol_Vol_Pct"].fillna(0)
df["PDV_Total_Ajuste"] = df["Nbre_PDV_Tradi"] + df["PDV_Estimes_ZB"]

df["Vol_2027_Par_CS"] = df["Vol_2027_Hls"] / df["Total_CS_Propose"].replace(0, np.nan)
df["Vol_2027_Par_CS"] = df["Vol_2027_Par_CS"].fillna(0)
df["Vol_2027_Par_MV"] = df["Vol_2027_Hls"] / df["MV"].replace(0, np.nan)
df["Vol_2027_Par_MV"] = df["Vol_2027_Par_MV"].fillna(0)
df["PDV_Par_CS"] = df["PDV_Total_Ajuste"] / df["Total_CS_Propose"].replace(0, np.nan)
df["PDV_Par_CS"] = df["PDV_Par_CS"].fillna(0)
df["PDV_Par_MV"] = df["PDV_Total_Ajuste"] / df["MV"].replace(0, np.nan)
df["PDV_Par_MV"] = df["PDV_Par_MV"].fillna(0)
df["Ratio_CS_MV"] = df["Total_CS_Propose"] / df["MV"].replace(0, np.nan)
df["Ratio_CS_MV"] = df["Ratio_CS_MV"].fillna(0)

sum_vol = df["Vol_2027_Hls"].sum()
sum_cs = df["Total_CS_Propose"].sum()
sum_mv = df["MV"].sum()
sum_pdv = df["PDV_Total_Ajuste"].sum()

nat_vol_cs = sum_vol / sum_cs if sum_cs > 0 else 0
nat_vol_mv = sum_vol / sum_mv if sum_mv > 0 else 0
nat_pdv_cs = sum_pdv / sum_cs if sum_cs > 0 else 0
nat_pdv_mv = sum_pdv / sum_mv if sum_mv > 0 else 0

st.subheader("🇲🇬 Indicateurs Clés de Référence (Moyenne Nationale)")

st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-header bg-star-green">Volume Moyen / CS</div>
            <div class="kpi-value">{nat_vol_cs:,.0f}</div>
            <div class="kpi-sub"><span class="kpi-arrow-up">↑</span> Cible : {cible_vol_cs:,.0f} Hecto</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header bg-star-green">Volume Moyen / MV</div>
            <div class="kpi-value">{nat_vol_mv:,.0f}</div>
            <div class="kpi-sub">Hecto</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header bg-star-red">PDV Moyens / CS</div>
            <div class="kpi-value">{nat_pdv_cs:.1f}</div>
            <div class="kpi-sub">Points de Vente</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-header bg-star-red">PDV Moyens / MV</div>
            <div class="kpi-value">{nat_pdv_mv:.1f}</div>
            <div class="kpi-sub">Points de Vente</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

def get_statut_cs(pdv_cs):
    if pdv_cs >= seuil_surcharge_cs: return "🔴 Surcharge CS"
    elif pdv_cs >= seuil_risque_cs: return "🟡 Risque Surcharge CS"
    elif pdv_cs <= seuil_sous_charge_cs: return "🔵 Sous-charge CS"
    else: return "🟢 Équilibré CS"

def get_statut_mv(vol_mv):
    if vol_mv >= seuil_surcharge_mv: return "🔴 Surcharge MV"
    return "🟢 Équilibré MV"

df["Statut_CS"] = df["PDV_Par_CS"].apply(get_statut_cs)
df["Statut_MV"] = df["Vol_2027_Par_MV"].apply(get_statut_mv)

def color_status_cells(val):
    if "🔴" in str(val): return "background-color: #ffcccc; color: #900000; font-weight: bold;"
    elif "🟡" in str(val): return "background-color: #fff3cd; color: #856404; font-weight: bold;"
    elif "🟢" in str(val): return "background-color: #d4edda; color: #155724; font-weight: bold;"
    elif "🔵" in str(val): return "background-color: #cce5ff; color: #004085; font-weight: bold;"
    return ""

# ==========================================
# 6. TABLEAU RÉCAPITULATIF
# ==========================================
st.subheader("📊 Tableau Récapitulatif : Volumes 2026 vs 2027 & Effectifs")
st.markdown("*(Les cellules surlignées en fond jaune indiquent les variables dynamiques modifiées)*")

df_recap = pd.DataFrame({
    "Agence": df["Agence"], "Région": df["Région"], "MV": df["MV"], "CS": df["Total_CS_Propose"],
    "Vol 2026 (Hls)": df["Vol_2026_Hls"], "Vol 2027 (Hls)": df["Vol_2027_Hls"],
    "Evol (+/- Hls)": df["Evol_Vol_Abs"], "Evol (%)": df["Evol_Vol_Pct"],
    "Vol / CS": df["Vol_2027_Par_CS"].round(0), "Vol / MV": df["Vol_2027_Par_MV"].round(0),
    "PDV / CS": df["PDV_Par_CS"].round(1), "Statut CS": df["Statut_CS"], "Statut MV": df["Statut_MV"],
})

def highlight_dynamic_cols(col):
    if col.name in ["Vol 2027 (Hls)", "Evol (+/- Hls)", "Evol (%)", "Vol / CS", "Vol / MV", "PDV / CS"]:
        return ["background-color: #fffacd; font-weight: bold;"] * len(col)
    return [""] * len(col)

st.dataframe(
    df_recap.style.apply(highlight_dynamic_cols, axis=0).map(color_status_cells, subset=["Statut CS", "Statut MV"])
    .format({
        "Vol 2026 (Hls)": "{:,.0f}", "Vol 2027 (Hls)": "{:,.0f}", "Evol (+/- Hls)": "{:+,.0f}",
        "Evol (%)": "{:+.2f}%", "Vol / CS": "{:,.0f}", "Vol / MV": "{:,.0f}", "PDV / CS": "{:.1f}",
    }), use_container_width=True,
)

# ==========================================
# 7. SIMULATEUR AVANT / APRÈS
# ==========================================
st.markdown("---")
st.subheader("🔄 Module de Simulation Avant / Après : Ajustement des Effectifs (CS & MV)")
st.markdown("Simulez l'impact d'un **recrutement ou transfert d'effectifs** (+/- CS et MV) :")

if "simulations_sauvegardees" not in st.session_state:
    st.session_state.simulations_sauvegardees = {}

if not df.empty:
    sc1, sc2, sc3 = st.columns(3)
    selected_sim_agence = sc1.selectbox("Sélectionner l'Agence à simuler", df["Agence"].unique(), key="sim_agence_select")

    default_cs = st.session_state.simulations_sauvegardees.get(selected_sim_agence, {}).get("delta_cs", 0)
    default_mv = st.session_state.simulations_sauvegardees.get(selected_sim_agence, {}).get("delta_mv", 0)

    delta_cs = sc2.number_input("Ajustement CS (+/- Recrutement/Transfert)", -15, 15, default_cs, step=1, key=f"sim_delta_cs_{selected_sim_agence}")
    delta_mv = sc3.number_input("Ajustement MV (+/- Recrutement/Transfert)", -5, 5, default_mv, step=1, key=f"sim_delta_mv_{selected_sim_agence}")

    row_sim_orig = df.loc[df["Agence"] == selected_sim_agence].iloc[0]
    mv_avant, cs_avant = row_sim_orig["MV"], row_sim_orig["Total_CS_Propose"]
    vol_2027_sim, pdv_tot_sim = row_sim_orig["Vol_2027_Hls"], row_sim_orig["PDV_Total_Ajuste"]
    vol_cs_avant, vol_mv_avant, pdv_cs_avant = row_sim_orig["Vol_2027_Par_CS"], row_sim_orig["Vol_2027_Par_MV"], row_sim_orig["PDV_Par_CS"]
    statut_cs_avant, statut_mv_avant = row_sim_orig["Statut_CS"], row_sim_orig["Statut_MV"]

    cs_apres = max(1, cs_avant + delta_cs)
    mv_apres = max(1, mv_avant + delta_mv)
    vol_cs_apres = vol_2027_sim / cs_apres
    vol_mv_apres = vol_2027_sim / mv_apres
    pdv_cs_apres = pdv_tot_sim / cs_apres
    statut_cs_apres, statut_mv_apres = get_statut_cs(pdv_cs_apres), get_statut_mv(vol_mv_apres)

    df_sim_comp = pd.DataFrame({
        "Dimension": ["Effectif MV", "Effectif CS", "Ratio CS / 1 MV", "Volume / CS (Hls/an)", "Volume / MV (Hls/an)", "Charge PDV / CS", "Statut Charge CS", "Statut Charge MV"],
        "Situation AVANT": [f"{mv_avant}", f"{cs_avant}", f"{cs_avant / mv_avant:.1f}", f"{vol_cs_avant:,.0f}", f"{vol_mv_avant:,.0f}", f"{pdv_cs_avant:.1f}", statut_cs_avant, statut_mv_avant],
        "Situation APRÈS (Simulation)": [f"{mv_apres} ({delta_mv:+d})", f"{cs_apres} ({delta_cs:+d})", f"{cs_apres / mv_apres:.1f}", f"{vol_cs_apres:,.0f}", f"{vol_mv_apres:,.0f}", f"{pdv_cs_apres:.1f}", statut_cs_apres, statut_mv_apres],
    })

    st.dataframe(df_sim_comp.style.map(color_status_cells, subset=["Situation AVANT", "Situation APRÈS (Simulation)"]), use_container_width=True)

    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("💾 Enregistrer cette simulation", key="save_sim"):
            st.session_state.simulations_sauvegardees[selected_sim_agence] = {"delta_cs": delta_cs, "delta_mv": delta_mv}
            st.success(f"Modifications sauvegardées pour {selected_sim_agence} !")
            st.rerun()

    if st.session_state.simulations_sauvegardees:
        st.info("📌 **Simulations actives en mémoire :**")
        for ag, mods in st.session_state.simulations_sauvegardees.items():
            if mods['delta_cs'] != 0 or mods['delta_mv'] != 0:
                st.write(f"- **{ag}** : CS {mods['delta_cs']:+d} | MV {mods['delta_mv']:+d}")
else:
    st.info("Aucune donnée disponible pour le module de simulation.")


# ==========================================
# 8. GRAPHIQUES
# ==========================================
st.markdown("---")
st.subheader("📈 Visualisation Interactive : Agence vs Moyenne Nationale")

VIBRANT_COLORS = ["#007bff", "#6f42c1", "#fd7e14", "#17a2b8", "#e83e8c"]

sims_actives = {ag: m for ag, m in st.session_state.simulations_sauvegardees.items() if m["delta_cs"] != 0 or m["delta_mv"] != 0}

comparer = st.toggle("🔄 Comparer Avant / Après simulation", value=False, disabled=not sims_actives or df.empty, key="toggle_compare_graphs", help="Affiche sur les graphiques l'impact des simulations enregistrées.")
if not sims_actives:
    st.caption("ℹ️ Enregistrez au moins une simulation pour activer la comparaison.")

df_apres = df.copy()
if not df_apres.empty:
    df_apres["Total_CS_Propose"] = [max(1, r["Total_CS_Propose"] + sims_actives.get(r["Agence"], {}).get("delta_cs", 0)) for _, r in df.iterrows()]
    df_apres["MV"] = [max(1, r["MV"] + sims_actives.get(r["Agence"], {}).get("delta_mv", 0)) for _, r in df.iterrows()]
    df_apres["Vol_2027_Par_CS"] = df_apres["Vol_2027_Hls"] / df_apres["Total_CS_Propose"]
    df_apres["PDV_Par_CS"] = df_apres["PDV_Total_Ajuste"] / df_apres["Total_CS_Propose"]

    nat_vol_cs_apres = df_apres["Vol_2027_Hls"].sum() / df_apres["Total_CS_Propose"].sum() if df_apres["Total_CS_Propose"].sum() > 0 else 0
    nat_pdv_cs_apres = df_apres["PDV_Total_Ajuste"].sum() / df_apres["Total_CS_Propose"].sum() if df_apres["Total_CS_Propose"].sum() > 0 else 0
else:
    nat_vol_cs_apres, nat_pdv_cs_apres = 0, 0

g_cols = st.columns(2)

if not comparer:
    with g_cols[0]:
        fig_vol = px.bar(df, x="Agence", y="Vol_2027_Par_CS", color="Région", title="Volume Moyen par CS par Agence vs Cible Nationale", labels={"Vol_2027_Par_CS": "Volume / CS (Hls)"}, color_discrete_sequence=VIBRANT_COLORS)
        fig_vol.add_hline(y=nat_vol_cs, line_dash="dash", line_color="#343a40", annotation_text=f"Moyenne Nat ({nat_vol_cs:,.0f} Hls)", annotation_position="top left")
        fig_vol.add_hline(y=cible_vol_cs, line_dash="dot", line_color="#fd7e14", annotation_text=f"Cible CS ({cible_vol_cs:,.0f} Hls)", annotation_position="bottom right")
        fig_vol.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_vol, use_container_width=True)

    with g_cols[1]:
        fig_pdv = px.bar(df, x="Agence", y="PDV_Par_CS", color="Région", title="Charge PDV par CS par Agence vs Moyenne Nationale", labels={"PDV_Par_CS": "PDV / CS"}, color_discrete_sequence=VIBRANT_COLORS)
        fig_pdv.add_hline(y=nat_pdv_cs, line_dash="dash", line_color="#343a40", annotation_text=f"Moyenne Nat ({nat_pdv_cs:.1f} PDV)", annotation_position="top left")
        fig_pdv.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_pdv, use_container_width=True)
else:
    d_avant = df[["Agence", "Région", "Vol_2027_Par_CS", "PDV_Par_CS"]].copy()
    d_avant["Scénario"] = "Avant"
    d_apres = df_apres[["Agence", "Région", "Vol_2027_Par_CS", "PDV_Par_CS"]].copy()
    d_apres["Scénario"] = "Après (simulation)"
    df_cmp = pd.concat([d_avant, d_apres], ignore_index=True)

    COLOR_SCEN = {"Avant": "#9aa5b1", "Après (simulation)": "#E3000F"}

    with g_cols[0]:
        fig_vol_c = px.bar(df_cmp, x="Agence", y="Vol_2027_Par_CS", color="Scénario", barmode="group", color_discrete_map=COLOR_SCEN, title="Volume par CS : Avant vs Après simulation", labels={"Vol_2027_Par_CS": "Volume / CS (Hls)"}, hover_data={"Région": True})
        fig_vol_c.add_hline(y=nat_vol_cs, line_dash="dash", line_color="#6c757d", annotation_text=f"Moy. Nat Avant ({nat_vol_cs:,.0f})", annotation_position="top left")
        fig_vol_c.add_hline(y=nat_vol_cs_apres, line_dash="dash", line_color="#E3000F", annotation_text=f"Moy. Nat Après ({nat_vol_cs_apres:,.0f})", annotation_position="top right")
        fig_vol_c.add_hline(y=cible_vol_cs, line_dash="dot", line_color="#fd7e14", annotation_text=f"Cible CS ({cible_vol_cs:,.0f})", annotation_position="bottom right")
        fig_vol_c.update_layout(xaxis_tickangle=-45, legend_title_text="")
        st.plotly_chart(fig_vol_c, use_container_width=True)

    with g_cols[1]:
        fig_pdv_c = px.bar(df_cmp, x="Agence", y="PDV_Par_CS", color="Scénario", barmode="group", color_discrete_map=COLOR_SCEN, title="Charge PDV par CS : Avant vs Après simulation", labels={"PDV_Par_CS": "PDV / CS"}, hover_data={"Région": True})
        fig_pdv_c.add_hline(y=nat_pdv_cs, line_dash="dash", line_color="#6c757d", annotation_text=f"Moy. Nat Avant ({nat_pdv_cs:.1f})", annotation_position="top left")
        fig_pdv_c.add_hline(y=nat_pdv_cs_apres, line_dash="dash", line_color="#E3000F", annotation_text=f"Moy. Nat Après ({nat_pdv_cs_apres:.1f})", annotation_position="top right")
        fig_pdv_c.add_hline(y=seuil_surcharge_cs, line_dash="dot", line_color="#b3000b", annotation_text=f"Seuil surcharge ({seuil_surcharge_cs})", annotation_position="bottom right")
        fig_pdv_c.update_layout(xaxis_tickangle=-45, legend_title_text="")
        st.plotly_chart(fig_pdv_c, use_container_width=True)

    lignes = []
    for ag, m in sims_actives.items():
        a = df.loc[df["Agence"] == ag].iloc[0]
        b = df_apres.loc[df_apres["Agence"] == ag].iloc[0]
        lignes.append({
            "Agence": ag, "Δ CS": f"{m['delta_cs']:+d}", "Δ MV": f"{m['delta_mv']:+d}", "Vol/CS Avant": f"{a['Vol_2027_Par_CS']:,.0f}", "Vol/CS Après": f"{b['Vol_2027_Par_CS']:,.0f}",
            "PDV/CS Avant": f"{a['PDV_Par_CS']:.1f}", "PDV/CS Après": f"{b['PDV_Par_CS']:.1f}", "Statut CS Avant": a["Statut_CS"], "Statut CS Après": get_statut_cs(b["PDV_Par_CS"]),
        })
    st.markdown("**Agences modifiées par les simulations enregistrées :**")
    st.dataframe(pd.DataFrame(lignes).style.map(color_status_cells, subset=["Statut CS Avant", "Statut CS Après"]), use_container_width=True, hide_index=True)

# ==========================================
# 9. SIMULATION FINANCIÈRE
# ==========================================
st.markdown("---")
st.subheader("💰 Simulation Financière & Point Mort (Break-even) par Agence")

if not df.empty:
    fin_cols = st.columns(3)
    selected_fin_agence = fin_cols[0].selectbox("Choisir l'Agence pour la simulation financière", df["Agence"].unique())
    cout_mensuel_cs = fin_cols[1].number_input("Coût mensuel d'un CS (MGA)", 500000, 5000000, 1500000, 100000)
    marge_nette_hl = fin_cols[2].number_input("Marge nette par Hectolitre (MGA/Hl)", 10000, 500000, 50000, 5000)

    row_fin = df.loc[df["Agence"] == selected_fin_agence].iloc[0]
    vol_agence, cs_agence, vol_par_cs_agence = row_fin["Vol_2027_Hls"], row_fin["Total_CS_Propose"], row_fin["Vol_2027_Par_CS"]

    cout_annuel_cs = cout_mensuel_cs * 12
    seuil_rentabilite_hl = cout_annuel_cs / marge_nette_hl if marge_nette_hl > 0 else 0
    couverture_besoin = (vol_par_cs_agence / seuil_rentabilite_hl) * 100 if seuil_rentabilite_hl > 0 else 0

    st.info(f"**Mode de calcul & Résultats pour : {selected_fin_agence}**")
    st.latex(r"\text{Seuil de Rentabilité (Break-even)} = \frac{\text{Coût Annuel du CS}}{\text{Marge Nette par Hl}}")
    st.markdown(f"- **Coût Annuel par CS :** {cout_mensuel_cs:,.0f} MGA $\\times$ 12 mois = **{cout_annuel_cs:,.0f} MGA**")
    st.markdown(f"- **Volume nécessaire par CS :** $\\frac{{{cout_annuel_cs:,.0f}}}{{{marge_nette_hl:,.0f}}}=$ **{seuil_rentabilite_hl:,.1f} Hls/an**")
    st.markdown(f"- **Performance actuelle :** {vol_par_cs_agence:,.1f} Hls/an/CS ({vol_agence:,.0f} Hls / {cs_agence} CS)")

    if vol_par_cs_agence >= seuil_rentabilite_hl:
        st.success(f"✅ L'agence {selected_fin_agence} est **rentable** (Couverture : **{couverture_besoin:.1f}%**).")
    else:
        st.warning(f"⚠️ Productivité en deçà du seuil de rentabilité (Couverture : **{couverture_besoin:.1f}%**).")
else:
    st.info("Aucune donnée disponible pour la simulation financière.")

# ==========================================
# 10. CARTE INTERACTIVE
# ==========================================
st.markdown("---")
st.markdown('<div id="section-carte"></div>', unsafe_allow_html=True)
st.subheader("🗺️ Carte Interactive : Agences & Points de Vente Détaillés")

df_map_agences = df.copy() if not df.empty else load_base_data()

ag_col = None
if not df_clients_gps.empty:
    for c in df_clients_gps.columns:
        if str(c).strip().lower() in ("ag", "agence", "code_agence", "code agence", "id_agence"):
            ag_col = c
            break

if ag_col is not None and not df_map_agences.empty:
    selected_agence_map = st.selectbox("Filtrer par Agence :", ["Toutes les agences"] + df_map_agences["Agence"].tolist())
    df_map_filtered = df_clients_gps.copy()
    if selected_agence_map != "Toutes les agences":
        ag_id = str(int(selected_agence_map.split("-")[0])).zfill(2)
        df_map_filtered = df_map_filtered[df_map_filtered[ag_col].astype(str).str.zfill(2) == ag_id]
else:
    selected_agence_map = "Toutes les agences"
    df_map_filtered = df_clients_gps.copy()

hover_cols = {c: True for c in ["Nom CS2", "Nom client", "Description activité", "Activite", "CS"] if c in df_map_filtered.columns}
hover_cols["Lat"], hover_cols["Lon"] = False, False

color_col = None
for c in ["Description activité", "Activite", "Description activite"]:
    if c in df_map_filtered.columns:
        color_col = c
        break

color_discrete_map, symbol_map = None, None
if color_col is not None:
    unique_vals = df_map_filtered[color_col].astype(str).unique()
    default_palette = px.colors.qualitative.Plotly
    color_discrete_map, symbol_map = {}, {}
    idx = 0
    for val in unique_vals:
        val_upper = str(val).strip().upper()
        if val_upper in ["DISTRIBUTEUR STAR", "DISTRIBUTEURS STAR", "DS", "DISTRIBUTION STAR"]:
            color_discrete_map[val], symbol_map[val] = "#E3000F", "star"
        elif val_upper == "ZONE BLANCHE":
            color_discrete_map[val], symbol_map[val] = "#000000", "circle"
        else:
            color_discrete_map[val], symbol_map[val] = default_palette[idx % len(default_palette)], "circle"
            idx += 1

kwargs = dict(lat="Lat", lon="Lon", hover_name="Nom client" if "Nom client" in df_map_filtered.columns else None, hover_data=hover_cols, zoom=5.5, center={"lat": -18.79, "lon": 46.85}, mapbox_style="open-street-map", height=650, title="Cartographie des Points de Vente & Agences")
if color_col is not None:
    kwargs["color"] = color_col
    if color_discrete_map is not None:
        kwargs["color_discrete_map"] = color_discrete_map

if not df_map_filtered.empty:
    fig_map = scatter_map_auto(df_map_filtered, **kwargs)
    if color_col is not None and symbol_map is not None:
        for trace in fig_map.data:
            trace_name = trace.name
            if trace_name in symbol_map:
                trace.marker.symbol = symbol_map[trace_name]
            if trace_name and str(trace_name).strip().upper() in ["DISTRIBUTEUR STAR", "DISTRIBUTEURS STAR", "DS", "DISTRIBUTION STAR"]:
                trace.marker.size = 14
    apply_marker_style(fig_map, size=6, opacity=0.75)
else:
    fig_map = scatter_map_auto(pd.DataFrame({"Lat": [-18.79], "Lon": [46.85]}), lat="Lat", lon="Lon", zoom=5.5, center={"lat": -18.79, "lon": 46.85}, mapbox_style="open-street-map", height=650, title="Cartographie des Points de Vente & Agences")
    fig_map.data = []

if not df_map_agences.empty:
    if selected_agence_map != "Toutes les agences":
        df_map_agences = df_map_agences[df_map_agences["Agence"] == selected_agence_map]
    if not df_map_agences.empty:
        cols_to_hover = {"Vol_2027_Hls": ":,.0f", "Lat": False, "Lon": False}
        if "Statut_CS" in df_map_agences.columns: cols_to_hover["Statut_CS"] = True
        if "Statut_MV" in df_map_agences.columns: cols_to_hover["Statut_MV"] = True

        fig_agences = scatter_map_auto(df_map_agences, lat="Lat", lon="Lon", hover_name="Agence", hover_data=cols_to_hover, mapbox_style="open-street-map")
        for trace in fig_agences.data:
            trace.marker.symbol, trace.marker.color, trace.marker.size, trace.name = "square", "#FF0000", 14, "Agences (Entrepôt)"
        for trace_ag in fig_agences.data:
            fig_map.add_trace(trace_ag)

st.caption(f"📍 {len(df_clients_gps):,} points de vente chargés.")
st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# 11. RECOMMANDATIONS & EXPORT
# ==========================================
st.markdown("---")
st.subheader("📋 Recommandations Détaillées par Agence & Export")

recos_list = []
for _, row in df.iterrows():
    region_actuelle = row["Région"]
    agences_meme_region = df[(df["Région"] == region_actuelle) & (df["Agence"] != row["Agence"])]

    conseil_transfert = "Equilibre regional stable."
    if "Surcharge" in row["Statut_CS"]:
        sous_charges = agences_meme_region[agences_meme_region["Statut_CS"].str.contains("Sous-charge")]
        conseil_transfert = f"Surcharge CS : Envisager un transfert depuis [{', '.join(sous_charges['Agence'].tolist())}] (meme region) ou recrutement local." if not sous_charges.empty else "Surcharge CS : Pas de sous-charge regionale. Recrutement local imperatif."
    elif "Sous-charge" in row["Statut_CS"]:
        surcharges = agences_meme_region[agences_meme_region["Statut_CS"].str.contains("Surcharge")]
        if not surcharges.empty:
            conseil_transfert = f"Sous-charge CS : Detachement possible vers [{', '.join(surcharges['Agence'].tolist())}] (meme region)."

    recos_list.append({
        "Agence": row["Agence"].replace("-", " "), "Region": row["Région"], "MV Actuels": row["MV"], "CS Actuels": row["Total_CS_Propose"],
        "Vol 2027 Hls": row["Vol_2027_Hls"], "Vol / CS": round(row["Vol_2027_Par_CS"], 0), "Vol / MV": round(row["Vol_2027_Par_MV"], 0),
        "PDV / CS": round(row["PDV_Par_CS"], 1), "Statut CS": row["Statut_CS"], "Statut MV": row["Statut_MV"], "Reco Regionale": conseil_transfert,
    })

df_recos = pd.DataFrame(recos_list, columns=["Agence", "Region", "MV Actuels", "CS Actuels", "Vol 2027 Hls", "Vol / CS", "Vol / MV", "PDV / CS", "Statut CS", "Statut MV", "Reco Regionale"])
csv_buffer = io.StringIO()
df_recos.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
st.download_button(label="📥 Télécharger le rapport des recommandations (CSV)", data=csv_buffer.getvalue(), file_name="recommandations_commerciales_madagascar.csv", mime="text/csv")

if df.empty:
    st.info("Aucune donnée disponible pour les recommandations.")

for _, row in df.iterrows():
    with st.expander(f"🏢 Agence : {row['Agence']} ({row['Région']}) — [{row['Statut_CS']}] | [{row['Statut_MV']}]"):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Effectifs", f"{row['MV']} MV | {row['Total_CS_Propose']} CS")
        c2.metric("Ratio Agence", f"{row['Ratio_CS_MV']:.1f} CS / 1 MV")
        c3.metric("Vol / MV", f"{row['Vol_2027_Par_MV']:,.0f}", f"vs Nat: {row['Vol_2027_Par_MV'] - nat_vol_mv:+,.0f}")
        c4.metric("Vol / CS", f"{row['Vol_2027_Par_CS']:,.0f}", f"vs Nat: {row['Vol_2027_Par_CS'] - nat_vol_cs:+,.0f}")

        st.markdown(f"- **Volume 2027 :** {row['Vol_2027_Hls']:,.0f} Hls (Évolution: {row['Evol_Vol_Pct']:+.2f}%)")
        st.markdown(f"- **Charge PDV :** {row['PDV_Par_CS']:.1f} PDV/CS | **Zones Blanches :** {row['PDV_Estimes_ZB']} PDV ({row['Vol_ZB_Inclut_Mois_Hls']} Hls/mois)")

        region_act = row["Région"]
        agences_reg = df[(df["Région"] == region_act) & (df["Agence"] != row["Agence"])]
        if "Surcharge" in row["Statut_CS"]:
            sc_list = agences_reg[agences_reg["Statut_CS"].str.contains("Sous-charge")]["Agence"].tolist()
            if sc_list:
                st.warning(f"⚠️ **Suggestion Régionale :** Surcharge CS détectée. Possibilité d'effectuer un transfert depuis l'agence sous-chargée de la même région : **{', '.join(sc_list)}**, ou recrutement local.")
            else:
                st.warning("⚠️ **Suggestion :** Surcharge CS sans sous-charge régionale. **Recrutement local recommandé**.")
        elif "Sous-charge" in row["Statut_CS"]:
            sur_list = agences_reg[agences_reg["Statut_CS"].str.contains("Surcharge")]["Agence"].tolist()
            if sur_list:
                st.info(f"ℹ️ **Suggestion Régionale :** Sous-charge CS identifiée. Possibilité de détacher du personnel vers l'agence en surcharge de la même région : **{', '.join(sur_list)}**.")
        else:
            st.success("✅ **Équilibre opérationnel validé.**")

# ==========================================
# 12. RÉCAPITULATIF FINAL
# ==========================================
st.markdown("---")
st.subheader("🎯 Récapitulatif Stratégique : Propositions de Recrutement & Transferts")

recap_lignes = []
for _, row in df.iterrows():
    region_actuelle = row["Région"]
    agences_meme_region = df[(df["Région"] == region_actuelle) & (df["Agence"] != row["Agence"])]

    action = "Maintien de l'effectif"
    if "Surcharge CS" in row["Statut_CS"]:
        sous_charges = agences_meme_region[agences_meme_region["Statut_CS"].str.contains("Sous-charge")]
        action = f"Transfert depuis [{', '.join(sous_charges['Agence'].tolist())}] (même région) ou Recrutement Local" if not sous_charges.empty else "Recrutement Local CS (Pas de source de transfert régional)"
    elif "Sous-charge CS" in row["Statut_CS"]:
        surcharges = agences_meme_region[agences_meme_region["Statut_CS"].str.contains("Surcharge")]
        action = f"Détachement / Transfert vers [{', '.join(surcharges['Agence'].tolist())}] (même région)" if not surcharges.empty else "Sous-charge locale (Maintien ou redéploiement zones blanches)"
    elif "Surcharge MV" in row["Statut_MV"]:
        action = "Renfort d'Encadrement MV"

    saved_mods = st.session_state.simulations_sauvegardees.get(row["Agence"])
    if saved_mods:
        sim_mv = f"{saved_mods['delta_mv']:+d}" if saved_mods['delta_mv'] != 0 else "0"
        sim_cs = f"{saved_mods['delta_cs']:+d}" if saved_mods['delta_cs'] != 0 else "0"
        new_cs, new_mv = max(1, row['Total_CS_Propose'] + saved_mods['delta_cs']), max(1, row['MV'] + saved_mods['delta_mv'])
        statut_cs_apres, statut_mv_apres = get_statut_cs(row['PDV_Total_Ajuste'] / new_cs), get_statut_mv(row['Vol_2027_Hls'] / new_mv)
    else:
        sim_mv, sim_cs, statut_cs_apres, statut_mv_apres = ".", ".", row["Statut_CS"], row["Statut_MV"]

    recap_lignes.append({
        "Région": row["Région"], "Agence": row["Agence"], "Volume 2027 (Hls)": f"{row['Vol_2027_Hls']:,.0f}", "PDV Totaux": f"{row['PDV_Total_Ajuste']:,.0f}",
        "Charge CS (PDV/CS)": f"{row['PDV_Par_CS']:.1f}", "Statut CS": statut_cs_apres, "Statut MV": statut_mv_apres, "Action Proposée": action,
        "Simulation (+/- MV)": sim_mv, "Simulation (+/- CS)": sim_cs,
    })

df_recap_final = pd.DataFrame(recap_lignes, columns=["Région", "Agence", "Volume 2027 (Hls)", "PDV Totaux", "Charge CS (PDV/CS)", "Statut CS", "Statut MV", "Action Proposée", "Simulation (+/- MV)", "Simulation (+/- CS)"])
st.table(df_recap_final)

dl_col1, dl_col2, _ = st.columns([1, 1, 3])
xlsx_buffer = io.BytesIO()
with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
    df_recap_final.to_excel(writer, index=False, sheet_name="Récapitulatif")
    ws = writer.sheets["Récapitulatif"]
    for col_cells in ws.columns:
        max_len = max(len(str(c.value)) if c.value is not None else 0 for c in col_cells)
        ws.column_dimensions[col_cells[0].column_letter].width = min(max_len + 2, 60)
dl_col2.download_button(label="📥 Télécharger (Excel)", data=xlsx_buffer.getvalue(), file_name="recapitulatif_strategique_recrutement_transferts.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="dl_recap_xlsx")
