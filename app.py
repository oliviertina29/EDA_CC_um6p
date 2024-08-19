import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
from textblob import TextBlob


# Configurer la page du tableau de bord avec un thème personnalisé
st.set_page_config(page_title="Students Employability Dashboard", layout="wide")

# Style CSS pour les titres
st.markdown("""
    <style>
        /* Style pour le titre principal */
        .main-title {
            font-size: 3em;
            font-weight: bold;
            color: #1F4E79;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Style pour les titres de section */
        .section-title {
            font-size: 2em;
            color: #1F4E79;
            text-align: left;
            margin-top: 40px;
            margin-bottom: 10px;
            border-bottom: 3px solid #1F4E79;
            padding-bottom: 10px;
        }

        /* Style global pour améliorer la typographie */
        body {
            font-family: 'Arial', sans-serif;
            color: #333;
        }

        /* Style pour les sous-titres */
        .sub-title {
            font-size: 1.5em;
            font-weight: bold;
            color: #4B8BBE;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("<h1 class='main-title'>Student Employability Monitoring</h1>", unsafe_allow_html=True)

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
st.markdown("<h2 class='section-title'>Overview of Placement Rates</h2>", unsafe_allow_html=True)

# Ajouter un filtre pour sélectionner un secteur spécifique (appartient au pie chart)
selected_sector = st.multiselect("Select Sector(s)", sectors, default=sectors)

# Filtrer les données en fonction des secteurs sélectionnés
df_overview = pd.DataFrame({
    "Sector": sectors,
    "Placement Rate (%)": placement_rates
})
df_filtered = df_overview[df_overview["Sector"].isin(selected_sector)] if selected_sector else df_overview.copy()

# Graphique en anneau pour les taux de placement par secteur
fig1 = px.pie(df_filtered, values='Placement Rate (%)', names='Sector', hole=0.4, 
              title="Placement Rate by Sector",
              color_discrete_sequence=colors)
fig1.update_traces(textinfo='percent+label', textposition='inside',
                   marker=dict(line=dict(color='#000000', width=2)))
fig1.update_layout(showlegend=True, margin=dict(t=50, b=0, l=0, r=0))

# Générer des données fictives pour les noms de métiers (exemple pour la démonstration)
job_titles = ["Data Scientist", "Software Engineer", "Financial Analyst", "Healthcare Manager", 
              "Teacher", "Consultant", "Civil Engineer", "Mechanical Engineer", 
              "Project Manager", "Data Analyst", "Marketing Specialist", "Researcher"]
job_titles *= 10  # Augmenter la fréquence des métiers

# Créer un nuage de mots avec un design harmonisé
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='plasma').generate(" ".join(job_titles))

# Afficher côte à côte le pie chart et le word cloud
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Titre distinct pour le word cloud
    st.subheader("Word Cloud of Job Titles")
    # Afficher le nuage de mots dans Streamlit
    st.image(wordcloud.to_array(), use_column_width=True)

# Statistiques clés avec mise en valeur
st.subheader("Key Statistics")

# Créer une palette de couleurs harmonisée pour les statistiques
background_colors = ["#6C63FF", "#FF6347", "#FFD700"]
text_color = "white"

# Liste des statistiques clés
metrics = [
    {
        "title": "Overall Placement Rate",
        "value": f"{np.mean(df_filtered['Placement Rate (%)']):.1f}%",
        "background_color": background_colors[0],
        "icon": "fa-line-chart"
    },
    {
        "title": "Highest Placement Sector",
        "value": f"{df_filtered['Sector'].iloc[np.argmax(df_filtered['Placement Rate (%)'])]} ({np.max(df_filtered['Placement Rate (%)'])}%)",
        "background_color": background_colors[1],
        "icon": "fa-arrow-up"
    },
    {
        "title": "Lowest Placement Sector",
        "value": f"{df_filtered['Sector'].iloc[np.argmin(df_filtered['Placement Rate (%)'])]} ({np.min(df_filtered['Placement Rate (%)'])}%)",
        "background_color": background_colors[2],
        "icon": "fa-arrow-down"
    }
]

# Afficher les statistiques en utilisant les colonnes de Streamlit avec un style réactif
cols = st.columns(len(metrics))

for col, metric in zip(cols, metrics):
    col.markdown(
        f"""
        <div style='background-color: {metric['background_color']}; padding: 20px; border-radius: 10px; text-align: center;'>
            <h3 style='color: {text_color}; margin-bottom: 10px;'>{metric['title']}</h3>
            <i style='color: {text_color}; font-size: 30px; margin-bottom: 10px;' class="fa {metric['icon']}"></i>
            <p style='font-size: 35px; color: {text_color}; font-weight: bold; margin: 0;'>{metric['value']}</p>
        </div>
        """, unsafe_allow_html=True
    )

# section 2
# Exemples de données géographiques fictives (Remplacer par vos données réelles)
geo_data = {
    "Country": ["Morocco", "France", "USA", "Germany", "Canada",
                "Senegal", "Ivory Coast", "Nigeria", "Kenya", "Ghana", "Mali", "South Africa", "Cameroon"],
    "Recruits": [150, 80, 35, 50, 70, 
                 90, 55, 120, 75, 65, 40, 85, 40],
    "Lat": [31.7917, 46.6034, 37.0902, 51.1657, 56.1304, 
            14.4974, 7.539989, 9.0820, -1.2921, 7.9465, 12.6392, -30.5595, 3.8480],
    "Lon": [-7.0926, 1.8883, -95.7129, 10.4515, -106.3468, 
            -14.4524, -5.5471, 8.6753, 36.8219, -1.0232, -8.0029, 22.9375, 11.5021]
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
                     size_max=50)

# Mettre à jour la disposition pour agrandir la carte
fig.update_layout(
    geo=dict(
        scope='world',
        projection_type='natural earth'
    ),
    width=1300,  # Largeur de la carte
    height=800   # Hauteur de la carte
)

# Afficher la carte dans Streamlit
st.markdown("<h2 class='section-title'>Global Recruitment Heatmap</h2>", unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)


# Section 3: Analyse détaillée avec prévisions
st.markdown("<h2 class='section-title'>Detailed Placement Analysis</h2>", unsafe_allow_html=True)

# Palette de couleurs améliorée
colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]

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
                   plot_bgcolor='#FAFAFA',
                   paper_bgcolor='#FAFAFA',
                   font=dict(family="Arial, sans-serif", size=12, color="#2a2a2a"),
                   title_font=dict(size=16, color="#2a2a2a", family="Arial, sans-serif"),
                   legend_title=dict(font=dict(size=14, color="#2a2a2a")),
                   xaxis=dict(showline=True, linewidth=2, linecolor='black'),
                   yaxis=dict(showline=True, linewidth=2, linecolor='black'),
                   hovermode="x unified")

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
                         plot_bgcolor='#FAFAFA',
                         paper_bgcolor='#FAFAFA',
                         font=dict(family="Arial, sans-serif", size=12, color="#2a2a2a"),
                         title_font=dict(size=16, color="#2a2a2a", family="Arial, sans-serif"),
                         legend_title=dict(font=dict(size=14, color="#2a2a2a")),
                         xaxis=dict(showline=True, linewidth=2, linecolor='black'),
                         yaxis=dict(showline=True, linewidth=2, linecolor='black'),
                         hovermode="x unified")

# Afficher côte à côte les graphiques de la section 2
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.plotly_chart(fig_degree, use_container_width=True)

# Section 4: Performance du Career Center avec rapports téléchargeables
st.markdown("<h2 class='section-title'>Career Center Performance</h2>", unsafe_allow_html=True)

# Générer des données fictives pour la satisfaction des parties prenantes
satisfaction_scores = np.random.randint(70, 100, size=len(stakeholders))
budget_used = np.random.uniform(50, 100)

df_performance = pd.DataFrame({
    "Stakeholder": stakeholders,
    "Satisfaction Score (%)": satisfaction_scores
})

# Graphique en radar pour la satisfaction des parties prenantes
fig3 = go.Figure()

fig3.add_trace(go.Scatterpolar(
    r=df_performance['Satisfaction Score (%)'],
    theta=df_performance['Stakeholder'],
    fill='toself',
    name='Satisfaction Score',
    marker=dict(color='#FF6347')
))

fig3.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100]),
    ),
    showlegend=False,
    title="Stakeholder Satisfaction",
    margin=dict(l=40, r=40, t=40, b=40),
)

# Ajout d'un graphique Scatterpolar pour la satisfaction moyenne par catégorie
categories = ["Communication", "Support", "Resources", "Events"]
category_scores = np.random.randint(70, 100, size=len(categories))

fig4 = go.Figure()

fig4.add_trace(go.Scatterpolar(
    r=category_scores,
    theta=categories,
    fill='toself',
    name='Category Satisfaction',
    marker=dict(color='#6C63FF')
))

fig4.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100]),
    ),
    showlegend=False,
    title="Category Satisfaction",
    margin=dict(l=40, r=40, t=40, b=40),
)

# Afficher les deux graphiques côte à côte
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.plotly_chart(fig4, use_container_width=True)

# Affichage du budget utilisé avec amélioration esthétique
st.markdown(
    f"""
    <div style='background-color: #FFD700; padding: 10px; border-radius: 5px; text-align: center;'>
        <h2 style='color: #000;'>Budget Utilized: {budget_used:.1f}% of Total</h2>
    </div>
    """, unsafe_allow_html=True
)

# Bouton pour télécharger les données sous forme de CSV avec style
st.markdown(
    """
    <style>
    .stDownloadButton button {
        background-color: #6C63FF;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.download_button(label="Download Performance Data", 
                   data=df_performance.to_csv(index=False), 
                   file_name='career_center_performance.csv',
                   mime='text/csv')


# Section 5: Analyse des tendances du marché avec comparaison intersectorielle
st.markdown("<h2 class='section-title'>Market Trends Analysis</h2>", unsafe_allow_html=True)

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

# Section 6: Suivi du Score de Satisfaction des Parties Prenantes
st.markdown("<h2 class='section-title'>Stakeholder Satisfaction and Sentiment Analysis</h2>", unsafe_allow_html=True)

# Diviser l'espace en deux colonnes
col1, col2 = st.columns(2)

# Colonne 1 : Suivi du Score de Satisfaction des Parties Prenantes
with col1:
    st.subheader("Satisfaction Score Over Time")

    # Données fictives pour les scores de satisfaction au fil du temps
    df_satisfaction_time = pd.DataFrame({
        "Year": years,
        "Students": np.random.randint(75, 95, size=len(years)),
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

st.markdown(
        f"""
        <div style='background-color: #6C63FF; padding: 10px; border-radius: 5px; text-align: center;'>
            <h2 style='color: #000;'>Overall Stakeholder Satisfaction Score: {avg_satisfaction:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True
    )