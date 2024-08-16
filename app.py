import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
from textblob import TextBlob

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
stakeholders = ["Students", "Employers", "University"]

# Palette de couleurs personnalisée
colors = px.colors.qualitative.Set2

# Section 1: Vue d'ensemble avec filtres dynamiques
st.header("Overview of Placement Rates")

# Ajouter un filtre pour sélectionner un secteur spécifique (appartient au pie chart)
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

# Générer des données fictives pour les noms de métiers
job_titles = ["Data Scientist", "Software Engineer", "Financial Analyst", "Healthcare Manager", 
              "Teacher", "Consultant", "Civil Engineer", "Mechanical Engineer", 
              "Project Manager", "Data Analyst", "Marketing Specialist", "Researcher"]
job_titles *= 10  # Augmenter la fréquence des métiers

# Créer un nuage de mots
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(" ".join(job_titles))

# Afficher côte à côte le pie chart et le word cloud
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Titre distinct pour le word cloud
    st.subheader("Word Cloud of Job Titles")
    # Afficher le nuage de mots dans Streamlit
    st.image(wordcloud.to_array(), use_column_width=True)

# Statistiques clés avec mise à jour dynamique
st.subheader("Key Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Overall Placement Rate", f"{np.mean(df_filtered['Placement Rate (%)']):.1f}%")
col2.metric("Highest Placement Sector", f"{df_filtered['Sector'].iloc[np.argmax(df_filtered['Placement Rate (%)'])]} ({np.max(df_filtered['Placement Rate (%)'])}%)")
col3.metric("Lowest Placement Sector", f"{df_filtered['Sector'].iloc[np.argmin(df_filtered['Placement Rate (%)'])]} ({np.min(df_filtered['Placement Rate (%)'])}%)")

# section 6
# Exemples de données géographiques fictives (Remplacer par vos données réelles)
geo_data = {
    "Country": ["Morocco", "France", "USA", "Germany", "Canada"],
    "Recruits": [150, 80, 200, 50, 70],
    "Lat": [31.7917, 46.6034, 37.0902, 51.1657, 56.1304],
    "Lon": [-7.0926, 1.8883, -95.7129, 10.4515, -106.3468]
}

df_geo = pd.DataFrame(geo_data)

# Créer une carte interactive avec Plotly
fig = px.scatter_geo(df_geo, 
                     lat='Lat', 
                     lon='Lon', 
                     size='Recruits', 
                     hover_name='Country',
                     title="Global Recruitment Heatmap",
                     color='Recruits',
                     size_max=80)

fig.update_layout(geo=dict(
    scope='world',
    projection_type='natural earth'
))

# Afficher la carte dans Streamlit
st.header("Global Recruitment Heatmap")
st.plotly_chart(fig, use_container_width=True)

# Section 2: Analyse détaillée avec prévisions
st.header("Detailed Placement Analysis")

# Générer des données fictives pour les cohortes et les années
df_cohorts = pd.DataFrame({
    "Year": np.repeat(years, len(cohorts)),
    "Cohort": cohorts * len(years),
    "Placement Rate (%)": np.random.randint(50, 90, size=len(years) * len(cohorts))
})

# Graphique de ligne pour les tendances des taux de placement par cohorte
fig2 = px.line(df_cohorts, x="Year", y="Placement Rate (%)", color="Cohort", markers=True,
               title="Placement Rate Trends by Cohort",
               color_discrete_sequence=colors)
fig2.update_layout(xaxis_title="Year", yaxis_title="Placement Rate (%)",
                   plot_bgcolor='#F7F7F7')

# Générer des données pour les taux de placement par niveau d'études
df_degree = pd.DataFrame({
    "Degree Level": ["Bachelor", "Master", "PhD"],
    "Placement Rate (%)": [75, 85, 70]
})

# Graphique en barres pour les taux de placement par niveau d'études
fig_degree = px.bar(df_degree, x="Degree Level", y="Placement Rate (%)",
                    title="Placement Rate by Degree Level",
                    color="Degree Level",
                    color_discrete_sequence=colors)
fig_degree.update_layout(xaxis_title="Degree Level", yaxis_title="Placement Rate (%)",
                         plot_bgcolor='#F7F7F7')

# Afficher côte à côte les graphiques de la section 2
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.plotly_chart(fig_degree, use_container_width=True)


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

# Paramètres généraux
years = np.arange(2015, 2025)
stakeholders = ["Students", "Employers", "University"]
colors = ["#636EFA", "#EF553B", "#00CC96"]

# Section 1: Suivi du Score de Satisfaction des Parties Prenantes
st.header("Stakeholder Satisfaction and Sentiment Analysis")

# Diviser l'espace en deux colonnes
col1, col2 = st.columns(2)

# Colonne 1 : Suivi du Score de Satisfaction des Parties Prenantes
with col1:
    st.subheader("Satisfaction Score Over Time")

    # Données fictives pour les scores de satisfaction au fil du temps
    df_satisfaction_time = pd.DataFrame({
        "Year": years,
        "Students": np.random.randint(70, 95, size=len(years)),
        "Employers": np.random.randint(60, 90, size=len(years)),
        "University": np.random.randint(65, 85, size=len(years)),
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
    avg_satisfaction_faculty = df_satisfaction_time["University"].mean()

    # Calculer la moyenne globale en prenant en compte chaque stakeholder
    avg_satisfaction = (avg_satisfaction_students + avg_satisfaction_employers + avg_satisfaction_faculty) / 3

    # Afficher le score global de satisfaction
    st.subheader(f"Overall Stakeholder Satisfaction Score: {avg_satisfaction:.1f}%")

# Colonne 2 : Analyse du Sentiment des Commentaires des Parties Prenantes
with col2:
    st.subheader("Sentiment Analysis of Stakeholder Feedback")

    # Exemples de commentaires fictifs
    comments = [
        "The career services are amazing!",
        "I wish the job placement was better.",
        "Great support from the University.",
        "The recruitment process could be improved.",
        "I'm very satisfied with the opportunities provided."
    ]

    # Analyse du sentiment
    sentiments = [TextBlob(comment).sentiment.polarity for comment in comments]
    df_sentiment = pd.DataFrame({"Comment": comments, "Sentiment Score": sentiments})

    # Graphique des scores de sentiment
    fig_sentiment = px.bar(df_sentiment, x="Comment", y="Sentiment Score",
                           title="Sentiment Analysis of Stakeholder Comments",
                           color="Sentiment Score",
                           color_continuous_scale="RdYlGn")
    fig_sentiment.update_layout(xaxis_title="Comment", yaxis_title="Sentiment Score",
                                plot_bgcolor='#F7F7F7', xaxis_tickangle=-45)
    st.plotly_chart(fig_sentiment, use_container_width=True)