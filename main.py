import streamlit as st
import pandas as pd
import datetime

import plotly.express as px
from os.path import exists

st.set_page_config(layout="wide", page_title="Data Reminder")

filename = "newData.csv"

if exists (filename):
    with open(filename) as f:
        st.sidebar.download_button('Download data', f)

st.title("Persone da contattare")
container = st.sidebar.container()
data = container.date_input("Data Appuntamento", datetime.datetime.now())
nome = container.text_input("Nome")
cognome = container.text_input("Cognome")
numeroTelefono = container.text_input("Telefono")
email = container.text_input("e-mail")
id = datetime.datetime.now()

if st.sidebar.button("Aggiungi"):
    #if "nuovaPersona" not in st.session_state:
    st.session_state["nuovaPersona"] =  {"id":[datetime.datetime.now()],"nome":[str(nome)],"cognome":[str(cognome)],"data":[data],"phone":[str(numeroTelefono)],"email":[str(email)]}




#try:
if "nuovaPersona" in st.session_state:
    a = pd.DataFrame.from_dict(st.session_state["nuovaPersona"])
    temp = st.sidebar.container()
    temp.caption("Recap")
    temp.caption("nome: " + str(a["nome"][0]))
    temp.caption("Cognome: " + str(a["cognome"][0]))
    temp.caption("Phone: " + str(a["phone"][0]))
    temp.caption("email: " + str(a["email"][0]))
    temp.caption("Data Iscrizione: " + str(a["data"][0]))
    #st.sidebar.dataframe(a)
    if st.sidebar.button("Salva"):
        if not exists(filename): 
            a.to_csv(filename,index=False)
        else:
            a.to_csv(filename, mode='a', index=False, header=False)
    
    if st.sidebar.button("reset Person data"):        
        del st.session_state["nuovaPersona"]
        st.experimental_rerun()

# Tempo trascorso
Accettabile=3
Medio=7
Inaccettabile=11



st.session_state.data = pd.read_csv(filename)
st.session_state.data.set_index(["id"])
differenzaDate = []
colori = []
NomeECognome = []
for i,x in enumerate(st.session_state.data["data"]):
    print(x)
    x = datetime.datetime. strptime(x, '%Y-%m-%d')
    print(x)
    duration =   datetime.datetime.now() - x
    duration = duration.days
    differenzaDate.append(duration)
    NomeECognome.append(str(st.session_state.data.loc[i,'nome']) + " " + str(st.session_state.data.loc[i,'cognome']))

    if duration <= Accettabile:
        colori.append("Accettabile")
    elif duration <= Medio:
        colori.append("Da risolvere")
    else :
        colori.append("Urgente")


st.session_state.data["tempoTrascorso"] = differenzaDate
st.session_state.data["warnings"] = colori

pf = px.bar(st.session_state.data, y=NomeECognome,x="tempoTrascorso",orientation='h',color = "warnings" ,hover_data=["phone","email"], color_discrete_map={"Accettabile": "green","Da risolvere": "orange","Urgente":"red"},opacity=0.6,text="tempoTrascorso")  
pf.update_layout(xaxis={'showticklabels': False})
st.plotly_chart(pf)


c1,c2,c4,cx1,c3 = st.columns([3,2,2,1,2])
if "index_to_delete" not in st.session_state:
    st.session_state.index_to_delete = []

for i,x in enumerate(st.session_state.data["nome"]):
    text_to_show = x + " " + st.session_state.data.loc[i,"cognome"]
    c2.text(st.session_state.data.loc[i,"phone"])
    if c1.button(text_to_show):
        c4.text("da rimuovere")
        st.session_state.index_to_delete.append(i)
    else:
        c4.text("In lavorazione")
    

if c3.button("Delete selected"):
    if st.session_state.index_to_delete is not []:
        newData = st.session_state.data.drop(st.session_state.index_to_delete)
        newData.to_csv(filename,index=False)
    st.session_state.index_to_delete = []
    st.experimental_rerun()


if st.button("Reset"):
    st.session_state.index_to_delete = []
               


