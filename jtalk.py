# import library
import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from random import randrange
import altair as alt
import matplotlib.pyplot as plt
import xlrd

# import data
img_logo = Image.open('logo.png')
white_img = Image.open('white.PNG')
df_text = pd.read_excel('performance_campagne.xlsx')


######################### STREAMLIT #########################
header = st.beta_container()
category = st.beta_container()
storico = st.beta_container()
copy = st.beta_container()

st.markdown("""
<style>
.JTALK_1 {font-size:40px !important; font-family: arial black;color: #B41E3C}
.JTALK_2 {font-size:40px !important; font-family: arial black;color: #002060}
.big-font {font-size:30px !important; font-family: arial black;color: #002060}
</style>
""", unsafe_allow_html=True)

# side bar
st.sidebar.image(img_logo, width = 180)
st.sidebar.button("Connettore Dati Clienti")
st.sidebar.button("Import CSV")

######################### INTRO #########################
with header:
    st.markdown('<div style="text-align:center"><span class="JTALK_1">J</span><span class="JTALK_2">TALK - AI Subject Generation</span></div>', unsafe_allow_html=True)
    st.image(white_img, width = 25)
    
    # BUTTONS
    col1, dem, sms, pn, col5 = st.beta_columns(5)
    col1.button("DEM") 
    sms.button("SMS") 
    col5.button("PN") 
    st.image(white_img, width = 10)
    

######################### STORICO #########################
with storico:
    st.markdown('<div style="text-align:center"><p class="big-font">Storico Campagne</p></div>', unsafe_allow_html=True)  
    campaign = st.selectbox("Select a campaign", ['01/08/2019 - CAMPAIGN 1', '01/10/2019 - CAMPAIGN 2', '01/12/2019 - CAMPAIGN 3', '01/01/2020 - CAMPAIGN 4', '01/03/2020 - CAMPAIGN 5', '01/05/2020 - CAMPAIGN 6'])
    
    # subject line storico
    if campaign == "01/08/2019 - CAMPAIGN 1":
        df_campaign = df_text.query('CASE == "STORICO" & CAMPAGNA == 1').reset_index(drop = True)
        bars = ['darkred', 'indianred']
        colors = ["#CD5C5C", "#8B0000"]
    elif campaign == "01/10/2019 - CAMPAIGN 2":
        df_campaign = df_text.query('CASE == "STORICO" & CAMPAGNA == 2').reset_index(drop = True)
        bars = ['darkred', 'indianred']
        colors = ["#CD5C5C", "#8B0000"]
    elif campaign == "01/12/2019 - CAMPAIGN 3":
        df_campaign = df_text.query('CASE == "STORICO" & CAMPAGNA == 3').reset_index(drop = True)
        bars = ['darkred', 'indianred']
        colors = ["#CD5C5C", "#8B0000"]
    elif campaign == "01/01/2020 - CAMPAIGN 4":
        df_campaign = df_text.query('CASE == "STORICO" & CAMPAGNA == 4').reset_index(drop = True)
        bars = ['navy', 'royalblue']
        colors = ["#4169e1", "#000080"]
    elif campaign == "01/03/2020 - CAMPAIGN 5":
        df_campaign = df_text.query('CASE == "STORICO" & CAMPAGNA == 5').reset_index(drop = True)
        bars = ['navy', 'royalblue']
        colors = ["#4169e1", "#000080"]
    elif campaign == "01/05/2020 - CAMPAIGN 6":
        df_campaign = df_text.query('CASE == "STORICO" & CAMPAGNA == 6').reset_index(drop = True)
        bars = ['navy', 'royalblue']
        colors = ["#4169e1", "#000080"]
    
    df_subject = df_campaign.set_index('ID')
    df_subject = df_subject[['SUBJECT']]

    st.table(df_subject)

    # colonne per i grafici
    or_chart, spider = st.beta_columns(2)

    # grafico OR con OR maggiore colorato e linea media
    df_or = df_campaign[['ID','OR']]
    max_or =  df_or.iloc[df_or["OR"].idxmax()]
    min_or =  df_or.iloc[df_or["OR"].idxmin()]
    chart = alt.Chart(df_or).mark_bar().encode(
        alt.X('OR', axis=alt.Axis(format='%')),
        y = 'ID', 
        color=alt.condition(alt.datum.ID == str(max_or['ID']), alt.value(bars[0]), alt.value(bars[1]))
        ).interactive().properties(height=300, width = 300)
    mean_or = alt.Chart(df_or).mark_rule(color='red').encode(x='mean(OR)')
    or_chart.altair_chart(chart + mean_or)
    st.image(white_img, width = 10)

    # grafico spider
    df_mean_values = df_campaign.drop(df_campaign['OR'].idxmax())
    df_mean_values.loc['MEAN'] = df_mean_values.mean()
    df_mean_values['ID']['MEAN'] = "MEAN"
    df_mean_values = df_mean_values.query('ID == "MEAN"')
    df_max_values =  df_campaign[df_campaign.OR == df_campaign.OR.max()]
    df_spider = df_mean_values.append(df_max_values).reset_index(drop = True)
    df_spider = df_spider[['CURIOSITA', 'SCARSITA', 'CONVENIENZA', 'PERSONALIZZAZIONE', 'CONFRONTO', 'LUNGHEZZA', 'BOOSTER', 'COLORI']]

    markers = [0, 1, 2, 3, 4, 5]
    str_markers = ["0", "1", "2", "3", "4", "5"]
    labels = np.array(['CURIOSITA', 'SCARSITA', 'CONVENIENZA', 'PERSONALIZZAZIONE', 'CONFRONTO', 'LUNGHEZZA', 'BOOSTER', 'COLORI'])
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    angles = np.concatenate((angles,[angles[0]]))
    fig= plt.figure()

    for i in range(0, 2):
        stats = np.concatenate((df_spider.loc[i],[df_spider.loc[i][0]]))
        ax = fig.add_subplot(111, polar=True)
        ax.plot(angles, stats, 'o-', linewidth=2, color = colors[i])
        ax.fill(angles, stats, alpha=0.25, color = colors[i])
        ax.set_thetagrids(angles * 180/np.pi, labels)
        plt.yticks(markers)
        ax.grid(True)

    spider.pyplot(plt)


######################### JTALK #########################
with copy:
    st.markdown('<div style="text-align:center"><p class="big-font">Creazione Copy</p></div>', unsafe_allow_html=True)

    but_1, but_2, but_3, but_4 = st.beta_columns(4)
    but_1.selectbox("Split", [1 ,2, 3, 4, 5, 6, 7])
    but_1.selectbox("Commit", ["None"])
    but_2.selectbox("Target", ["General", "Women", "Man", "Traditionalist", "Baby Boomers", "Generation X", "Millennials", "Gen Z"])
    but_2.selectbox("Length", ["None", "Short", "Medium", "Long"])
    but_3.selectbox("Size", ["< 100k", "100k - 500k", "500k - 1M", "> 1M"])
    but_3.selectbox("Boost", ["None", "Allowed", "Not Allowed"])
    but_4.selectbox("Delta Min", ["0,1%", "0,2%", "0,3%"])
    but_4.selectbox("Industry", ["None", "Energy and Service", "Insurance", "Telco and Media", "Fashion", "Retail"])
    
    st.image(white_img, width = 10)
    col1, col2, col3, col4, col5 = st.beta_columns(5)

    if (col3.button("JTALK CREATE")):

        # subject line jtalk
        num_test = randrange(3) 
        
        df_jtalk = df_text.query('CASE == "JTALK" & CAMPAGNA == @num_test').reset_index(drop = True)     
        df_copy = df_jtalk.set_index('ID')
        df_copy = df_copy[['SUBJECT']]
        st.table(df_copy)
        
        # colonne per i grafici
        or_chart_pred, spider_pred = st.beta_columns(2)

        # grafico OR predicted
        df_or_pred = df_jtalk[['ID','OR']]
        max_or_pred =  df_or_pred.iloc[df_or_pred["OR"].idxmax()]
        chart = alt.Chart(df_or_pred).mark_bar().encode(
            alt.X('OR', axis=alt.Axis(format='%')),
            y = 'ID', 
            color=alt.condition(alt.datum.ID == str(max_or_pred['ID']), alt.value('navy'),alt.value('royalblue'))
            ).interactive().properties(height=300, width = 300)
        mean_or_pred = alt.Chart(df_or_pred).mark_rule(color='red').encode(x='mean(OR)')
        or_chart_pred.altair_chart(chart + mean_or_pred)
        st.image(white_img, width = 10)

        # grafico spider
        df_mean_values = df_jtalk.drop(df_jtalk['OR'].idxmax())
        df_mean_values.loc['MEAN'] = df_mean_values.mean()
        df_mean_values['ID']['MEAN'] = "MEAN"
        df_mean_values = df_mean_values.query('ID == "MEAN"')
        df_max_values =  df_campaign[df_campaign.OR == df_campaign.OR.max()]
        df_spider = df_mean_values.append(df_max_values).reset_index(drop = True)
        df_spider = df_spider[['CURIOSITA', 'SCARSITA', 'CONVENIENZA', 'PERSONALIZZAZIONE', 'CONFRONTO', 'LUNGHEZZA', 'BOOSTER', 'COLORI']]

        markers = [0, 1, 2, 3, 4, 5]
        str_markers = ["0", "1", "2", "3", "4", "5"]
        labels = np.array(['CURIOSITA', 'SCARSITA', 'CONVENIENZA', 'PERSONALIZZAZIONE', 'CONFRONTO', 'LUNGHEZZA', 'BOOSTER', 'COLORI'])
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
        angles = np.concatenate((angles,[angles[0]]))
        fig= plt.figure()
        colors = ["#4169e1", "#000080"]

        for i in range(0, 2):
            stats = np.concatenate((df_spider.loc[i],[df_spider.loc[i][0]]))
            ax = fig.add_subplot(111, polar=True)
            ax.plot(angles, stats, 'o-', linewidth=2, color = colors[i])
            ax.fill(angles, stats, alpha=0.25, color = colors[i])
            ax.set_thetagrids(angles * 180/np.pi, labels)
            plt.yticks(markers)
            ax.grid(True)

        spider_pred.pyplot(plt)
    
