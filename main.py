import streamlit as st
import pandas as pd
import datetime

#import plotly.express as px
from os.path import exists

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
    st.sidebar.dataframe(a)
if st.sidebar.button("salva"):
    if not exists(filename): 
        a.to_csv(filename,index=False)
    else:
        a.to_csv(filename, mode='a', index=False, header=False)


# Tempo trascorso
Accettabile=5
Medio=8
Inaccettabile=11



st.session_state.data = pd.read_csv(filename)
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
        colori.append("ok")
    elif duration <Medio:
        colori.append("care")
    else :
        colori.append("NOTOK")


st.session_state.data["tempoTrascorso"] = differenzaDate
st.session_state.data["warnings"] = colori

#pf = px.bar(st.session_state.data, y=NomeECognome,x="tempoTrascorso",orientation='h',color="warnings",hover_data=["phone"])    
st.dataframe(st.session_state.data)
#st.plotly_chart(pf)


c1,c2 = st.columns([4,1])
if "index_to_delete" not in st.session_state:
    st.session_state.index_to_delete = []

for i,x in enumerate(st.session_state.data["nome"]):
    text_to_show = x + " " + st.session_state.data.loc[i,"cognome"]
    if c1.button(text_to_show):
        c2.text("RIMOSSO")
        st.session_state.index_to_delete.append(i)
    

if st.button("Delete selected"):
    if st.session_state.index_to_delete is not []:
        newData = st.session_state.data.drop(st.session_state.index_to_delete)
        newData.to_csv(filename,index=False)
    st.session_state.index_to_delete = []
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))


if st.button("Reset"):
    st.session_state.index_to_delete = []
                


