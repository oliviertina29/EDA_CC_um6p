import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configurer la page du tableau de bord avec un thème personnalisé
st.set_page_config(page_title="Students Employability Dashboard", layout="wide")

# Titre principal
st.title("UM6P Career Center Dashboard: Student Employability Tracking")

# Générer des données fictives pour le tableau de bord
np.random.seed(42)
sectors = ["Tech", "Finance", "Healthcare", "Education", "Consulting", "Engineering"]
placement_rates = np.random.randint(50, 90, size=len(sectors))
years = [2020, 2021, 2022, 2023]
cohorts = ["Cohort A", "Cohort B", "Cohort C", "Cohort D"]
stakeholders = ["Students", "Employers", "Faculty"]

# Palette de couleurs personnalisée
colors = px.colors.qualitative.Set2

# Section 1: Vue d'ensemble avec filtres dynamiques
st.header("Overview of Placement Rates")

# Ajouter un filtre pour sélectionner un secteur spécifique
selected_sector = st.multiselect("Select Sector(s)", sectors, default=sectors)

# Filtrer les données en fonction des secteurs sélectionnés
df_overview = pd.DataFrame({
    "Sector": sectors,
    "Placement Rate (%)": placement_rates
})
df_filtered = df_overview[df_overview["Sector"].isin(selected_sector)]

# Graphique en anneau pour les taux de placement par secteur
fig1 = px.pie(df_filtered, values='Placement Rate (%)', names='Sector', hole=0.4, 
              title="Placement Rate by Sector",
              color_discrete_sequence=colors)
fig1.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=2)))
st.plotly_chart(fig1, use_container_width=True)

# Statistiques clés avec mise à jour dynamique
st.subheader("Key Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Overall Placement Rate", f"{np.mean(df_filtered['Placement Rate (%)']):.1f}%")
col2.metric("Highest Placement Sector", f"{df_filtered['Sector'].iloc[np.argmax(df_filtered['Placement Rate (%)'])]} ({np.max(df_filtered['Placement Rate (%)'])}%)")
col3.metric("Lowest Placement Sector", f"{df_filtered['Sector'].iloc[np.argmin(df_filtered['Placement Rate (%)'])]} ({np.min(df_filtered['Placement Rate (%)'])}%)")

# Section 2: Analyse détaillée avec prévisions
st.header("Detailed Placement Analysis")

# Générer des données fictives pour les cohortes et les années
df_cohorts = pd.DataFrame({
    "Year": np.repeat(years, len(cohorts)),
    "Cohort": cohorts * len(years),
    "Placement Rate (%)": np.random.randint(50, 90, size=len(years) * len(cohorts))
})

# Graphique de ligne pour les tendances des taux de placement
fig2 = px.line(df_cohorts, x="Year", y="Placement Rate (%)", color="Cohort", markers=True,
               title="Placement Rate Trends by Cohort",
               color_discrete_sequence=colors)
fig2.update_layout(xaxis_title="Year", yaxis_title="Placement Rate (%)",
                   plot_bgcolor='#F7F7F7')
st.plotly_chart(fig2, use_container_width=True)

# Ajouter une section de prévisions basées sur une tendance linéaire
st.subheader("Forecast for Next Year")
next_year = max(years) + 1
forecast = df_cohorts.groupby("Year")["Placement Rate (%)"].mean().iloc[-1] * 1.05  # Simple trend estimation
st.write(f"Estimated Placement Rate for {next_year}: {forecast:.1f}%")

# Section 3: Performance du Career Center avec rapports téléchargeables
st.header("Career Center Performance")

# Générer des données fictives pour la satisfaction des parties prenantes et le budget utilisé
satisfaction_scores = np.random.randint(70, 100, size=len(stakeholders))
budget_used = np.random.uniform(50, 100)

df_performance = pd.DataFrame({
    "Stakeholder": stakeholders,
    "Satisfaction Score (%)": satisfaction_scores
})

# Graphique en barres pour la satisfaction des parties prenantes
fig3 = px.bar(df_performance, x='Stakeholder', y='Satisfaction Score (%)', text_auto=True, 
              title="Stakeholder Satisfaction",
              color='Stakeholder',
              color_discrete_sequence=colors)
fig3.update_layout(xaxis_title="Stakeholder", yaxis_title="Satisfaction Score (%)",
                   plot_bgcolor='#F7F7F7')
st.plotly_chart(fig3, use_container_width=True)

# Affichage du budget utilisé
st.subheader(f"Budget Utilized: {budget_used:.1f}% of Total")

# Bouton pour télécharger les données sous forme de CSV
st.download_button(label="Download Performance Data", 
                   data=df_performance.to_csv(index=False), 
                   file_name='career_center_performance.csv',
                   mime='text/csv')

# Section 4: Analyse des tendances du marché avec comparaison intersectorielle
st.header("Market Trends Analysis")

# Générer des données fictives pour les entreprises qui recrutent
companies = ["Company A", "Company B", "Company C", "Company D", "Company E"]
recruitment_numbers = np.random.randint(10, 50, size=len(companies))

df_market_trends = pd.DataFrame({
    "Company": companies,
    "Number of Recruits": recruitment_numbers
})

# Générer des données fictives pour la comparaison intersectorielle
df_comparison = pd.DataFrame({
    "Year": years,
    "Tech": np.random.randint(50, 90, size=len(years)),
    "Finance": np.random.randint(50, 85, size=len(years)),
    "Healthcare": np.random.randint(45, 80, size=len(years)),
    "Education": np.random.randint(40, 75, size=(len(years))),
    "Consulting": np.random.randint(50, 88, size=(len(years))),
    "Engineering": np.random.randint(55, 92, size=(len(years)))
})

# Création des graphiques avec Plotly
fig4 = px.bar(
    df_market_trends, 
    x='Company', 
    y='Number of Recruits', 
    text_auto=True, 
    title="Top Recruiting Companies",
    color='Company',
    color_discrete_sequence=colors
)
fig4.update_layout(
    xaxis_title="Company", 
    yaxis_title="Number of Recruits",
    plot_bgcolor='#F7F7F7',
    showlegend=False  # Cacher la légende pour ce graphique
)

fig5 = go.Figure()
for i, sector in enumerate(sectors):
    fig5.add_trace(go.Scatter(
        x=df_comparison["Year"], 
        y=df_comparison[sector], 
        mode='lines+markers', 
        name=sector, 
        line=dict(color=colors[i % len(colors)])
    ))

fig5.update_layout(
    title="Employment Trends by Sector", 
    xaxis_title="Year", 
    yaxis_title="Placement Rate (%)",
    plot_bgcolor='#F7F7F7'
)

# Affichage côte à côte des deux graphiques
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.plotly_chart(fig5, use_container_width=True)

# Section 5: Suivi du Score de Satisfaction des Parties Prenantes
st.header("Stakeholder Satisfaction Score")

# Données fictives pour les scores de satisfaction au fil du temps
df_satisfaction_time = pd.DataFrame({
    "Year": years,
    "Students": np.random.randint(70, 95, size=len(years)),
    "Employers": np.random.randint(60, 90, size=len(years)),
    "Faculty": np.random.randint(65, 85, size=(len(years))),
})

# Graphique de ligne pour suivre l'évolution des scores de satisfaction
fig6 = go.Figure()
for i, stakeholder in enumerate(stakeholders):
    fig6.add_trace(go.Scatter(x=df_satisfaction_time["Year"], y=df_satisfaction_time[stakeholder],
                              mode='lines+markers', name=stakeholder,
                              line=dict(color=colors[i % len(colors)])))

fig6.update_layout(title="Stakeholder Satisfaction Over Time", xaxis_title="Year", yaxis_title="Satisfaction Score (%)",
                   plot_bgcolor='#F7F7F7')
st.plotly_chart(fig6, use_container_width=True)

# Calculer la moyenne de satisfaction pour chaque stakeholder
avg_satisfaction_students = df_satisfaction_time["Students"].mean()
avg_satisfaction_employers = df_satisfaction_time["Employers"].mean()
avg_satisfaction_faculty = df_satisfaction_time["Faculty"].mean()

# Calculer la moyenne globale en prenant en compte chaque stakeholder
avg_satisfaction = (avg_satisfaction_students + avg_satisfaction_employers + avg_satisfaction_faculty) / 3

# Afficher le score global de satisfaction
st.subheader(f"Overall Stakeholder Satisfaction Score: {avg_satisfaction:.1f}%")

