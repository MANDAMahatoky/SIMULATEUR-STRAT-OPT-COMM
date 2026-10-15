import io
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Simulateur Commercial Madagascar", layout="wide"
)

st.title("🇲🇬 Simulateur Stratégique & Optimisation Commerciale - Madagascar")
st.markdown(
    "Pilotage multiniveaux, analyse croisée CS & MV avec codes couleurs,"
    " simulation financière par agence, et plan de réaffectation régional."
)

# ==========================================
# 1. DONNÉES DE BASE (VOLUMES, EFFECTIFS, ZONES BLANCHES PAR AGENCE)
# ==========================================


@st.cache_data
def load_base_data():
  data = {
      "Région": [
          "Centre",
          "Centre",
          "Est",
          "Est",
          "Nord",
          "Nord",
          "Nord",
          "Nord",
          "Nord",
          "Sud",
          "Sud",
          "Sud",
          "Sud",
          "Sud",
          "Sud",
      ],
      "Agence": [
          "11-Andranomahery",
          "12-Antsirabe",
          "01-Tanjombato",
          "09-Tamatave",
          "03-Usine-Diego",
          "07-Majunga",
          "18-Ambanja",
          "19-Sambava",
          "21-Nosy-Be",
          "04-Tulear",
          "05-Fianarantsoa",
          "06-Ihosy",
          "08-Manakara",
          "23-Morondava",
          "24-Fort-Dauphin",
      ],
      "MV": [5, 2, 5, 3, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1],  #[cite: 1]
      "CS_Actuels": [32, 13, 31, 18, 6, 10, 6, 5, 4, 7, 8, 3, 4, 4, 5],  #[cite: 1]
      "Ajustement_CS_DRV": [6, 3, 6, 3, 1, 3, 2, 2, 1, 2, 0, 1, 2, 2, 1],  #[cite: 3]
      "Vol_2026_Hls": [
          843256,
          306183,
          878064,
          511164,
          189959,
          338706,
          213219,
          150744,
          142658,
          202606,
          138452,
          86860,
          202880,
          85204,
          113113,
      ],  #[cite: 2]
      "Vol_2027_Hls": [
          902190,
          339742,
          976891,
          547209,
          187677,
          366320,
          238634,
          172094,
          161164,
          227276,
          155168,
          97400,
          235379,
          96757,
          119372,
      ],  #[cite: 2]
      "Nbre_PDV_Tradi": [
          5950,
          2450,
          5987,
          5307,
          1009,
          2830,
          2400,
          800,
          1300,
          1365,
          1500,
          700,
          1550,
          930,
          950,
      ],  #[cite: 3]
      "Temps_Dispo_Mois_Min": [
          601920,
          253440,
          586080,
          332640,
          110880,
          205920,
          126720,
          110880,
          79200,
          142560,
          126720,
          63360,
          95040,
          95040,
          95040,
      ],  #[cite: 3]
      "Vol_ZB_Inclut_Mois_Hls": [
          215,
          0,
          4005,
          0,
          70,
          2950,
          0,
          0,
          0,
          2473,
          0,
          0,
          0,
          0,
          0,
      ],  #[cite: 4]
      "PDV_Estimes_ZB": [50, 0, 850, 0, 30, 600, 0, 0, 0, 500, 0, 0, 0, 0, 0],
      "Lat": [
          -18.8792,
          -19.8658,
          -18.9667,
          -18.1492,
          -12.2786,
          -15.7167,
          -13.6773,
          -14.2667,
          -13.3167,
          -23.3500,
          -21.4333,
          -22.4000,
          -22.1333,
          -20.2833,
          -25.0200,
      ],
      "Lon": [
          47.5079,
          47.0333,
          47.5333,
          49.4023,
          49.2917,
          46.3167,
          48.4501,
          50.1667,
          48.2667,
          43.6667,
          47.0833,
          46.1333,
          48.0167,
          44.2833,
          46.9900,
      ],
  }
  return pd.DataFrame(data)


df_raw = load_base_data()

# ==========================================
# 2. PARAMÈTRES D'AJUSTEMENT (SIDEBAR)
# ==========================================
st.sidebar.header("⚙️ Paramètres & Seuils d'Évaluation")

obj_visites_jour = st.sidebar.number_input(
    "Objectif Visites max / Commercial / Jour", 1, 35, 22
)
jours_travailles_mois = st.sidebar.number_input(
    "Jours travaillés / mois", 15, 26, 20
)
temps_moyen_visite_min = st.sidebar.number_input(
    "Temps moyen par visite (min)", 10, 90, 30
)
cible_vol_cs = st.sidebar.number_input(
    "Volume Cible par CS (Hls/an)", 1000, 50000, 25000, 1000
)

st.sidebar.subheader("Seuils de Charge")
seuil_surcharge_cs = st.sidebar.number_input("Seuil Surcharge CS (> X PDV)", 200, 500, 250)
seuil_risque_cs = st.sidebar.number_input(
    "Seuil Risque CS (> X PDV)", 180, 400, 210
)
seuil_sous_charge_cs = st.sidebar.number_input(
    "Seuil Sous-charge CS (< X PDV)", 50, 200, 150
)
seuil_surcharge_mv = st.sidebar.number_input(
    "Seuil Surcharge MV (> X Hls vol)", 20000, 500000, 200000
)

st.sidebar.subheader("🎯 Simulation Zones Blanches par Agence")
selected_agence_zb = st.sidebar.selectbox(
    "Sélectionner une Agence", df_raw["Agence"].unique()
)
default_zb_vol = int(
    df_raw.loc[df_raw["Agence"] == selected_agence_zb, "Vol_ZB_Inclut_Mois_Hls"]
    .values[0]
)
default_zb_pdv = int(
    df_raw.loc[df_raw["Agence"] == selected_agence_zb, "PDV_Estimes_ZB"].values[0]
)

sim_zb_vol_mois = st.sidebar.number_input(
    f"Volume ZB Mensuel ({selected_agence_zb})", 0, 10000, default_zb_vol
)
sim_zb_pdv = st.sidebar.number_input(
    f"PDV ZB ({selected_agence_zb})", 0, 2000, default_zb_pdv
)

df = df_raw.copy()
df.loc[df["Agence"] == selected_agence_zb, "Vol_ZB_Inclut_Mois_Hls"] = (
    sim_zb_vol_mois
)
df.loc[df["Agence"] == selected_agence_zb, "PDV_Estimes_ZB"] = sim_zb_pdv

# ==========================================
# 3. CALCULS DYNAMIQUES & MOYENNES NATIONALES
# ==========================================
df["Total_CS_Propose"] = df["CS_Actuels"] + df["Ajustement_CS_DRV"]  #[cite: 3]
df["Evol_Vol_Abs"] = df["Vol_2027_Hls"] - df["Vol_2026_Hls"]
df["Evol_Vol_Pct"] = (df["Evol_Vol_Abs"] / df["Vol_2026_Hls"]) * 100
df["PDV_Total_Ajuste"] = df["Nbre_PDV_Tradi"] + df["PDV_Estimes_ZB"]

# Productivités
df["Vol_2027_Par_CS"] = df["Vol_2027_Hls"] / df["Total_CS_Propose"]
df["Vol_2027_Par_MV"] = df["Vol_2027_Hls"] / df["MV"]
df["PDV_Par_CS"] = df["PDV_Total_Ajuste"] / df["Total_CS_Propose"]
df["PDV_Par_MV"] = df["PDV_Total_Ajuste"] / df["MV"]
df["Ratio_CS_MV"] = df["Total_CS_Propose"] / df["MV"]

# Moyennes Nationales
nat_vol_2026 = df["Vol_2026_Hls"].sum()
nat_vol_2027 = df["Vol_2027_Hls"].sum()
nat_cs = df["Total_CS_Propose"].sum()
nat_mv = df["MV"].sum()
nat_pdv = df["PDV_Total_Ajuste"].sum()

nat_vol_cs = nat_vol_2027 / nat_cs
nat_vol_mv = nat_vol_2027 / nat_mv
nat_pdv_cs = nat_pdv / nat_cs
nat_pdv_mv = nat_pdv / nat_mv

# Affichage des Indicateurs Nationaux en haut de page
st.subheader("🇲🇬 Indicateurs Clés de Référence (Moyenne Nationale)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Volume Moyen / CS", f"{nat_vol_cs:,.0f} Hls", f"Cible: {cible_vol_cs:,.0f}")
kpi2.metric("Volume Moyen / MV", f"{nat_vol_mv:,.0f} Hls")
kpi3.metric("PDV Moyens / CS", f"{nat_pdv_cs:.1f} PDV")
kpi4.metric("PDV Moyens / MV", f"{nat_pdv_mv:.1f} PDV")
st.markdown("---")


def get_statut_cs(pdv_cs):
  if pdv_cs >= seuil_surcharge_cs:
    return "🔴 Surcharge CS"
  elif pdv_cs >= seuil_risque_cs:
    return "🟡 Risque Surcharge CS"
  elif pdv_cs <= seuil_sous_charge_cs:
    return "🔵 Sous-charge CS"
  else:
    return "🟢 Équilibré CS"


def get_statut_mv(vol_mv):
  if vol_mv >= seuil_surcharge_mv:
    return "🔴 Surcharge MV"
  else:
    return "🟢 Équilibré MV"


df["Statut_CS"] = df["PDV_Par_CS"].apply(get_statut_cs)
df["Statut_MV"] = df["Vol_2027_Par_MV"].apply(get_statut_mv)


def color_status_cells(val):
  if "🔴" in str(val):
    return "background-color: #ffcccc; color: #900000; font-weight: bold;"
  elif "🟡" in str(val):
    return "background-color: #fff3cd; color: #856404; font-weight: bold;"
  elif "🟢" in str(val):
    return "background-color: #d4edda; color: #155724; font-weight: bold;"
  elif "🔵" in str(val):
    return "background-color: #cce5ff; color: #004085; font-weight: bold;"
  return ""


# ==========================================
# 4. TABLEAU RÉCAPITULATIF (AVEC SURBRILLANCE DYNAMIQUE)
# ==========================================
st.subheader("📊 Tableau Récapitulatif : Volumes 2026 vs 2027 & Effectifs")
st.markdown(
    "*(Les cellules surlignées en fond jaune indiquent les variables dynamiques"
    " modifiées par vos paramètres ou la sélection des zones blanches)*"
)

df_recap = pd.DataFrame({
    "Agence": df["Agence"],
    "Région": df["Région"],
    "MV": df["MV"],
    "CS": df["Total_CS_Propose"],
    "Vol 2026 (Hls)": df["Vol_2026_Hls"],
    "Vol 2027 (Hls)": df["Vol_2027_Hls"],
    "Evol (+/- Hls)": df["Evol_Vol_Abs"],
    "Evol (%)": df["Evol_Vol_Pct"],
    "Vol / CS": df["Vol_2027_Par_CS"].round(0),
    "Vol / MV": df["Vol_2027_Par_MV"].round(0),
    "PDV / CS": df["PDV_Par_CS"].round(1),
    "Statut CS": df["Statut_CS"],
    "Statut MV": df["Statut_MV"],
})


def highlight_dynamic_cols(col):
  if col.name in [
      "Vol 2027 (Hls)",
      "Evol (+/- Hls)",
      "Evol (%)",
      "Vol / CS",
      "Vol / MV",
      "PDV / CS",
  ]:
    return ["background-color: #fffacd; font-weight: bold;"] * len(col)
  return [""] * len(col)


st.dataframe(
    df_recap.style.apply(highlight_dynamic_cols, axis=0)
    .map(color_status_cells, subset=["Statut CS", "Statut MV"])
    .format({
        "Vol 2026 (Hls)": "{:,.0f}",
        "Vol 2027 (Hls)": "{:,.0f}",
        "Evol (+/- Hls)": "{:+,.0f}",
        "Evol (%)": "{:+.2f}%",
        "Vol / CS": "{:,.0f}",
        "Vol / MV": "{:,.0f}",
        "PDV / CS": "{:.1f}",
    }),
    use_container_width=True,
)

# ==========================================
# 5. MODULE ISOLÉ : SIMULATEUR AVANT / APRÈS (RECRUTEMENT & TRANSFERT CS/MV)
# ==========================================
st.markdown("---")

# Style CSS spécifique pour isoler visuellement le bloc de simulation
st.markdown(
    """
    <style>
    .sim-container {
        background-color: #f0f4f8;
        border-left: 6px solid #1e3d59;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 25px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="sim-container">', unsafe_allow_html=True)
st.subheader(
    "🔄 Module de Simulation Avant / Après : Ajustement des Effectifs (CS & MV)"
)
st.markdown(
    "Simulez l'impact d'un **recrutement ou transfert d'effectifs** (+/- CS et"
    " MV) pour une agence et observez le recalcul automatique de la charge"
    " (Volume & PDV) et du **code couleur de situation** :"
)

sc1, sc2, sc3 = st.columns(3)
selected_sim_agence = sc1.selectbox(
    "Sélectionner l'Agence à simuler",
    df["Agence"].unique(),
    key="sim_agence_select",
)
delta_cs = sc2.number_input(
    "Ajustement CS (+/- Recrutement/Transfert)",
    -15,
    15,
    0,
    step=1,
    key="sim_delta_cs",
)
delta_mv = sc3.number_input(
    "Ajustement MV (+/- Recrutement/Transfert)",
    -5,
    5,
    0,
    step=1,
    key="sim_delta_mv",
)

# Extraction des données actuelles (Avant)
row_sim_orig = df.loc[df["Agence"] == selected_sim_agence].iloc[0]

mv_avant = row_sim_orig["MV"]
cs_avant = row_sim_orig["Total_CS_Propose"]
vol_2027_sim = row_sim_orig["Vol_2027_Hls"]
pdv_tot_sim = row_sim_orig["PDV_Total_Ajuste"]

vol_cs_avant = row_sim_orig["Vol_2027_Par_CS"]
vol_mv_avant = row_sim_orig["Vol_2027_Par_MV"]
pdv_cs_avant = row_sim_orig["PDV_Par_CS"]
statut_cs_avant = row_sim_orig["Statut_CS"]
statut_mv_avant = row_sim_orig["Statut_MV"]

# Calculs de la situation projetée (Après)
cs_apres = max(1, cs_avant + delta_cs)
mv_apres = max(1, mv_avant + delta_mv)

vol_cs_apres = vol_2027_sim / cs_apres
vol_mv_apres = vol_2027_sim / mv_apres
pdv_cs_apres = pdv_tot_sim / cs_apres

statut_cs_apres = get_statut_cs(pdv_cs_apres)
statut_mv_apres = get_statut_mv(vol_mv_apres)

# Assemblage du tableau comparatif Avant / Après
df_sim_comp = pd.DataFrame({
    "Dimension": [
        "Effectif MV",
        "Effectif CS",
        "Ratio CS / 1 MV",
        "Volume / CS (Hls/an)",
        "Volume / MV (Hls/an)",
        "Charge PDV / CS",
        "Statut Charge CS",
        "Statut Charge MV",
    ],
    "Situation AVANT": [
        f"{mv_avant}",
        f"{cs_avant}",
        f"{cs_avant / mv_avant:.1f}",
        f"{vol_cs_avant:,.0f}",
        f"{vol_mv_avant:,.0f}",
        f"{pdv_cs_avant:.1f}",
        statut_cs_avant,
        statut_mv_avant,
    ],
    "Situation APRÈS (Simulation)": [
        f"{mv_apres} ({delta_mv:+d})",
        f"{cs_apres} ({delta_cs:+d})",
        f"{cs_apres / mv_apres:.1f}",
        f"{vol_cs_apres:,.0f}",
        f"{vol_mv_apres:,.0f}",
        f"{pdv_cs_apres:.1f}",
        statut_cs_apres,
        statut_mv_apres,
    ],
})

st.dataframe(
    df_sim_comp.style.map(
        color_status_cells,
        subset=["Situation AVANT", "Situation APRÈS (Simulation)"],
    ),
    use_container_width=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. GRAPHIQUES DE VISUALISATION INTERACTIFS
# ==========================================
st.markdown("---")
st.subheader("📈 Visualisation Interactive : Agence vs Moyenne Nationale")

g_cols = st.columns(2)
with g_cols[0]:
  fig_vol = px.bar(
      df,
      x="Agence",
      y="Vol_2027_Par_CS",
      color="Région",
      title="Volume Moyen par CS par Agence vs Cible Nationale",
      labels={"Vol_2027_Par_CS": "Volume / CS (Hls)"},
  )
  fig_vol.add_hline(
      y=nat_vol_cs,
      line_dash="dash",
      line_color="red",
      annotation_text=f"Moyenne Nat ({nat_vol_cs:,.0f} Hls)",
  )
  fig_vol.add_hline(
      y=cible_vol_cs,
      line_dash="dot",
      line_color="green",
      annotation_text=f"Cible CS ({cible_vol_cs:,.0f} Hls)",
  )
  fig_vol.update_layout(xaxis_tickangle=-45)
  st.plotly_chart(fig_vol, use_container_width=True)

with g_cols[1]:
  fig_pdv = px.bar(
      df,
      x="Agence",
      y="PDV_Par_CS",
      color="Région",
      title="Charge PDV par CS par Agence vs Moyenne Nationale",
      labels={"PDV_Par_CS": "PDV / CS"},
  )
  fig_pdv.add_hline(
      y=nat_pdv_cs,
      line_dash="dash",
      line_color="red",
      annotation_text=f"Moyenne Nat ({nat_pdv_cs:.1f} PDV)",
  )
  fig_pdv.update_layout(xaxis_tickangle=-45)
  st.plotly_chart(fig_pdv, use_container_width=True)

# ==========================================
# 7. SIMULATION FINANCIÈRE LIÉE À L'AGENCE
# ==========================================
st.markdown("---")
st.subheader("💰 Simulation Financière & Point Mort (Break-even) par Agence")

fin_cols = st.columns(3)
selected_fin_agence = fin_cols[0].selectbox(
    "Choisir l'Agence pour la simulation financière", df["Agence"].unique()
)
cout_mensuel_cs = fin_cols[1].number_input(
    "Coût mensuel d'un CS (MGA)", 500000, 5000000, 1500000, 100000
)
marge_nette_hl = fin_cols[2].number_input(
    "Marge nette par Hectolitre (MGA/Hl)", 10000, 500000, 50000, 5000
)

row_fin = df.loc[df["Agence"] == selected_fin_agence].iloc[0]
vol_agence = row_fin["Vol_2027_Hls"]
cs_agence = row_fin["Total_CS_Propose"]
vol_par_cs_agence = row_fin["Vol_2027_Par_CS"]

cout_annuel_cs = cout_mensuel_cs * 12
seuil_rentabilite_hl = (
    cout_annuel_cs / marge_nette_hl if marge_nette_hl > 0 else 0
)
couverture_besoin = (
    (vol_par_cs_agence / seuil_rentabilite_hl) * 100
    if seuil_rentabilite_hl > 0
    else 0
)

st.markdown(f"### 📋 Mode de calcul & Résultats pour : **{selected_fin_agence}**")
st.latex(
    r"\text{Seuil de Rentabilité (Break-even)} = \frac{\text{Coût Annuel du CS}"
    r"}{\text{Marge Nette par Hl}}"
)
st.markdown(
    f"- **Coût Annuel par CS :** {cout_mensuel_cs:,.0f} MGA $\\times$ 12 mois ="
    f" **{cout_annuel_cs:,.0f} MGA**"
)
st.markdown(
    f"- **Volume nécessaire par CS pour rentabilité :**"
    f" $\\frac{{{cout_annuel_cs:,.0f}}}{{{marge_nette_hl:,.0f}}}=$ **{seuil_rentabilite_hl:,.1f}"
    " Hls/an**"
)
st.markdown(
    f"- **Performance actuelle de l'agence :** Un CS vend en moyenne"
    f" **{vol_par_cs_agence:,.1f} Hls/an** dans l'agence {selected_fin_agence}"
    f" (Volume total agence : {vol_agence:,.0f} Hls pour {cs_agence} CS)."
)

if vol_par_cs_agence >= seuil_rentabilite_hl:
  st.success(
      f"✅ L'agence {selected_fin_agence} est **rentable** par rapport au coût"
      f" d'un CS (Couverture du seuil : **{couverture_besoin:.1f}%**)."
  )
else:
  st.warning(
      f"⚠️ Attention, la productivité actuelle par CS dans cette agence est en"
      f" deçà du seuil de rentabilité (Couverture :"
      f" **{couverture_besoin:.1f}%**)."
  )

# ==========================================
# 8. CARTE DE MADAGASCAR INTERACTIVE
# ==========================================
st.markdown("---")
st.subheader("🗺️ Carte Interactive des Agences à Madagascar")
fig_map = px.scatter_map(
    df,
    lat="Lat",
    lon="Lon",
    size="Vol_2027_Hls",
    color="Région",
    hover_name="Agence",
    hover_data={
        "Vol_2027_Hls": ":,.0f",
        "Statut_CS": True,
        "Statut_MV": True,
        "Lat": False,
        "Lon": False,
    },
    zoom=4.8,
    center={"lat": -18.79, "lon": 46.85},
    map_style="open-street-map",
    height=500,
)
st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# 9. RECOMMANDATIONS & EXPORT CSV PROPRE
# ==========================================
st.markdown("---")
st.subheader("📋 Recommandations Détaillées par Agence & Export")

recos_list = []
for index, row in df.iterrows():
  region_actuelle = row["Région"]
  agences_meme_region = df[
      (df["Région"] == region_actuelle) & (df["Agence"] != row["Agence"])
  ]

  conseil_transfert = "Equilibre regional stable."
  if "Surcharge" in row["Statut_CS"]:
    sous_charges = agences_meme_region[
        agences_meme_region["Statut_CS"].str.contains("Sous-charge")
    ]
    if not sous_charges.empty:
      noms_sc = ", ".join(sous_charges["Agence"].tolist())
      conseil_transfert = (
          f"Surcharge CS : Envisager un transfert depuis [{noms_sc}] (meme"
          " region) ou recrutement local."
      )
    else:
      conseil_transfert = (
          "Surcharge CS : Pas de sous-charge regionale. Recrutement local"
          " imperatif."
      )
  elif "Sous-charge" in row["Statut_CS"]:
    surcharges = agences_meme_region[
        agences_meme_region["Statut_CS"].str.contains("Surcharge")
    ]
    if not surcharges.empty:
      noms_sur = ", ".join(surcharges["Agence"].tolist())
      conseil_transfert = (
          f"Sous-charge CS : Detachement possible vers [{noms_sur}] (meme"
          " region)."
      )

  recos_list.append({
      "Agence": row["Agence"].replace("-", " "),
      "Region": row["Région"],
      "MV Actuels": row["MV"],
      "CS Actuels": row["Total_CS_Propose"],
      "Vol 2027 Hls": row["Vol_2027_Hls"],
      "Vol / CS": round(row["Vol_2027_Par_CS"], 0),
      "Vol / MV": round(row["Vol_2027_Par_MV"], 0),
      "PDV / CS": round(row["PDV_Par_CS"], 1),
      "Statut CS": row["Statut_CS"],
      "Statut MV": row["Statut_MV"],
      "Reco Regionale": conseil_transfert,
  })

df_recos = pd.DataFrame(recos_list)

csv_buffer = io.StringIO()
df_recos.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
st.download_button(
    label="📥 Télécharger le rapport des recommandations (CSV)",
    data=csv_buffer.getvalue(),
    file_name="recommandations_commerciales_madagascar.csv",
    mime="text/csv",
)

for index, row in df.iterrows():
  with st.expander(
      f"🏢 Agence : {row['Agence']} ({row['Région']}) — [{row['Statut_CS']}]"
      f" | [{row['Statut_MV']}]"
  ):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Effectifs", f"{row['MV']} MV | {row['Total_CS_Propose']} CS")
    c2.metric("Ratio Agence", f"{row['Ratio_CS_MV']:.1f} CS / 1 MV")
    c3.metric(
        "Vol / MV",
        f"{row['Vol_2027_Par_MV']:,.0f} Hls",
        f"vs Nat: {row['Vol_2027_Par_MV'] - nat_vol_mv:+,.0f}",
    )
    c4.metric(
        "Vol / CS",
        f"{row['Vol_2027_Par_CS']:,.0f} Hls",
        f"vs Nat: {row['Vol_2027_Par_CS'] - nat_vol_cs:+,.0f}",
    )

    st.markdown(
        f"- **Volume 2027 :** {row['Vol_2027_Hls']:,.0f} Hls (Évolution:"
        f" {row['Evol_Vol_Pct']:+.2f}%)"
    )
    st.markdown(
        f"- **Charge PDV :** {row['PDV_Par_CS']:.1f} PDV/CS | **Zones Blanches"
        f" :** {row['PDV_Estimes_ZB']} PDV ({row['Vol_ZB_Inclut_Mois_Hls']}"
        " Hls/mois)"
    )

    region_act = row["Région"]
    agences_reg = df[
        (df["Région"] == region_act) & (df["Agence"] != row["Agence"])
    ]
    if "Surcharge" in row["Statut_CS"]:
      sc_list = agences_reg[
          agences_reg["Statut_CS"].str.contains("Sous-charge")
      ]["Agence"].tolist()
      if sc_list:
        st.warning(
            f"⚠️ **Suggestion Régionale :** Surcharge CS détectée. Possibilité"
            f" d'effectuer un transfert depuis l'agence sous-chargée de la même"
            f" région : **{', '.join(sc_list)}**, ou recrutement local."
        )
      else:
        st.warning(
            "⚠️ **Suggestion :** Surcharge CS sans sous-charge régionale."
            " **Recrutement local recommandé**."
        )
    elif "Sous-charge" in row["Statut_CS"]:
      sur_list = agences_reg[
          agences_reg["Statut_CS"].str.contains("Surcharge")
      ]["Agence"].tolist()
      if sur_list:
        st.info(
            f"ℹ️ **Suggestion Régionale :** Sous-charge CS identifiée. Possibilité"
            f" de détacher du personnel vers l'agence en surcharge de la même"
            f" région : **{', '.join(sur_list)}**."
        )
    else:
      st.success("✅ **Équilibre opérationnel validé.**")

# ==========================================
# 10. RÉCAPITULATIF FINAL : RECRUTEMENTS & TRANSFERTS INTER-AGENCES
# ==========================================
st.markdown("---")
st.subheader(
    "🎯 Récapitulatif Stratégique : Propositions de Recrutement & Transferts"
)

recap_lignes = []
for index, row in df.iterrows():
  region_actuelle = row["Région"]
  agences_meme_region = df[
      (df["Région"] == region_actuelle) & (df["Agence"] != row["Agence"])
  ]

  action = "Maintien de l'effectif"
  if "Surcharge CS" in row["Statut_CS"]:
    sous_charges = agences_meme_region[
        agences_meme_region["Statut_CS"].str.contains("Sous-charge")
    ]
    if not sous_charges.empty:
      noms_sc = ", ".join(sous_charges["Agence"].tolist())
      action = f"Transfert depuis [{noms_sc}] (même région) ou Recrutement Local"
    else:
      action = "Recrutement Local CS (Pas de source de transfert régional)"
  elif "Sous-charge CS" in row["Statut_CS"]:
    surcharges = agences_meme_region[
        agences_meme_region["Statut_CS"].str.contains("Surcharge")
    ]
    if not surcharges.empty:
      noms_sur = ", ".join(surcharges["Agence"].tolist())
      action = f"Détachement / Transfert vers [{noms_sur}] (même région)"
    else:
      action = "Sous-charge locale (Maintien ou redéploiement zones blanches)"
  elif "Surcharge MV" in row["Statut_MV"]:
    action = "Renfort d'Encadrement MV"

  recap_lignes.append({
      "Région": row["Région"],
      "Agence": row["Agence"],
      "Volume 2027 (Hls)": f"{row['Vol_2027_Hls']:,.0f}",
      "PDV Totaux": f"{row['PDV_Total_Ajuste']:,.0f}",
      "Charge CS (PDV/CS)": f"{row['PDV_Par_CS']:.1f}",
      "Statut CS": row["Statut_CS"],
      "Statut MV": row["Statut_MV"],
      "Action Proposée": action,
  })

df_recap_final = pd.DataFrame(recap_lignes)
st.table(df_recap_final)
