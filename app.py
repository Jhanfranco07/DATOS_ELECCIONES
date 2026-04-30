import streamlit as st
import pandas as pd

st.title("Resultados Electorales ONPE 2021")
st.header("Parte 2: Uso de datos electorales públicos CSV")

# Cargar archivo CSV
df = pd.read_csv("presidencial.csv", sep=",", encoding="utf-8")

# Mostrar vista previa
st.subheader("Vista previa del dataset")
st.dataframe(df.head())

# Información general
st.subheader("Información general del dataset")
st.write("Cantidad de registros:", df.shape[0])
st.write("Cantidad de columnas:", df.shape[1])

# Identificación de campos importantes
st.subheader("Campos electorales identificados")

st.write("Ubigeo:", "ubigeo")
st.write("Departamento:", "departamento")
st.write("Provincia:", "provincia")
st.write("Distrito:", "distrito")
st.write("Electores habilitados:", "ELECTORES_HABIL")
st.write("Ciudadanos que votaron:", "TOT_CIUDADANOS_VOTARON")
st.write("Porcentaje de participación:", "POR_CIUDADANOS_VOTARON")
st.write("Actas procesadas:", "ACTAS_PROCESADAS")

# Número aproximado de mesas/actas procesadas
st.subheader("Número de mesas o actas procesadas")
total_actas = df["ACTAS_PROCESADAS"].sum()
st.write("Total de actas procesadas:", total_actas)

# Ubigeos únicos
st.subheader("Ubigeos registrados")
total_ubigeos = df["ubigeo"].nunique()
st.write("Cantidad de ubigeos únicos:", total_ubigeos)

# Valores nulos
st.subheader("Revisión de valores nulos")
st.write(df.isnull().sum())

# Limpieza básica
df_limpio = df.dropna()

st.subheader("Dataset limpio")
st.write("Registros antes de limpieza:", df.shape[0])
st.write("Registros después de limpieza:", df_limpio.shape[0])

st.dataframe(df_limpio.head())
