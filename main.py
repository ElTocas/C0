from matplotlib.axis import YAxis
from matplotlib.pyplot import ticklabel_format
import streamlit as st
import pandas as pd
import datetime

import plotly.express as px
from os.path import exists


st.set_page_config(layout="wide", page_title="Timer from Rachel call")

filename = "this_data.csv"

st.title("Persone da contattare")
container = st.sidebar.container()
data = container.date_input("Data Appuntamento Rachel", datetime.datetime.now())
nome = container.text_input("Nome")
cognome = container.text_input("Cognome")
numeroTelefono = container.text_input("Telefono")
id = datetime.datetime.now()

if st.sidebar.button("aggiungi"):
    #if "nuovaPersona" not in st.session_state:
    st.session_state["nuovaPersona"] =  {"id":[datetime.datetime.now()],"nome":[nome],"cognome":[cognome],"data":[data],"phone":[numeroTelefono]}




#try:
if "nuovaPersona" in st.session_state:
    a = pd.DataFrame.from_dict(st.session_state["nuovaPersona"])
    temp = st.sidebar.container()
    temp.caption("Recap")
    temp.caption("nome: " + str(a["nome"][0]))
    temp.caption("Cognome: " + str(a["cognome"][0]))
    temp.caption("Phone: " + str(a["phone"][0]))
    temp.caption("Data Iscrizione: " + str(a["data"][0]))
    #st.sidebar.dataframe(a)
    if st.sidebar.button("salva"):
        if not exists(filename): 
            a.to_csv(filename,index=False)
        else:
            a.to_csv(filename, mode='a', index=False, header=False)
    
    if st.sidebar.button("reset Person data"):        
        del st.session_state["nuovaPersona"]
        st.experimental_rerun()

# Tempo trascorso
Accettabile=3
Medio=8
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
    NomeECognome.append(st.session_state.data.loc[i,'nome'] + " " + st.session_state.data.loc[i,'cognome'])

    if duration < Accettabile:
        colori.append("Accettabile")
    elif duration <Medio:
        colori.append("Da risolvere")
    else :
        colori.append("Urgente")


st.session_state.data["tempoTrascorso"] = differenzaDate
st.session_state.data["warnings"] = colori

pf = px.bar(st.session_state.data, y=NomeECognome,x="tempoTrascorso",orientation='h',color = "warnings" ,hover_data=["phone"], color_discrete_map={"Accettabile": "green","Da risolvere": "blue","Urgente":"red"},opacity=0.6,text="tempoTrascorso")  
st.plotly_chart(pf)


c1,c2,cx,cx1,c3 = st.columns([3,2,2,1,2])
if "index_to_delete" not in st.session_state:
    st.session_state.index_to_delete = []

for i,x in enumerate(st.session_state.data["nome"]):
    text_to_show = x + " " + st.session_state.data.loc[i,"cognome"]
    if c1.button(text_to_show):
        c2.text("da rimuovere")
        st.session_state.index_to_delete.append(i)
    else:
        c2.text("In lavorazione")
    

if c3.button("Delete selected"):
    if st.session_state.index_to_delete is not []:
        newData = st.session_state.data.drop(st.session_state.index_to_delete)
        newData.to_csv(filename,index=False)
    st.session_state.index_to_delete = []
    st.experimental_rerun()


if st.button("Reset"):
    st.session_state.index_to_delete = []
                


