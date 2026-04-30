import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Resultados Electorales ONPE 2021",
)

st.title("Resultados Electorales ONPE 2021")
st.write("Sistema básico de carga, análisis y visualización de datos electorales.")

# CARGA DEL DATASET


df = pd.read_csv("presidencial.csv", sep=",", encoding="utf-8")

# PARTE 2: USO DE DATOS CSV


st.header("Parte 2: Uso de datos electorales públicos CSV")

st.subheader("Vista previa del dataset")
st.dataframe(df.head())

st.subheader("Información general del dataset")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Registros", df.shape[0])

with col2:
    st.metric("Columnas", df.shape[1])

with col3:
    st.metric("Ubigeos únicos", df["ubigeo"].nunique())

st.subheader("Campos electorales identificados")

st.write("""
El dataset contiene información electoral agregada por ubicación geográfica.
Entre sus principales campos se identifican:
- Ubigeo
- Departamento
- Provincia
- Distrito
- Electores habilitados
- Ciudadanos que votaron
- Porcentaje de participación
- Actas procesadas
""")

st.subheader("Número aproximado de mesas o actas procesadas")

total_actas = df["ACTAS_PROCESADAS"].sum()
st.metric("Total de actas procesadas", int(total_actas))

st.info(
    "El dataset no contiene el número individual de cada mesa electoral, "
    "pero sí contiene la columna ACTAS_PROCESADAS, que permite analizar "
    "la cantidad de actas o mesas procesadas por distrito."
)

st.subheader("Revisión de valores nulos")

valores_nulos = df.isnull().sum()
st.dataframe(valores_nulos)

df_limpio = df.dropna()

st.subheader("Dataset luego de limpieza básica")

col4, col5 = st.columns(2)

with col4:
    st.metric("Registros antes de limpieza", df.shape[0])

with col5:
    st.metric("Registros después de limpieza", df_limpio.shape[0])

st.dataframe(df_limpio.head())

# PARTE 3: VISUALIZACIONES

st.header("Parte 3: Visualización de resultados electorales")

# Ver qué departamentos tienen más participación

st.subheader("1. Ciudadanos que votaron por departamento")

df_dep = (
    df.groupby("departamento")["TOT_CIUDADANOS_VOTARON"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(df_dep)

# Comparación de cuántos podían votar vs cuántos votaron

st.subheader("2. Electores habilitados vs ciudadanos que votaron")

df_comparacion = (
    df.groupby("departamento")[["ELECTORES_HABIL", "TOT_CIUDADANOS_VOTARON"]]
    .sum()
    .sort_values(by="ELECTORES_HABIL", ascending=False)
)

st.bar_chart(df_comparacion)

# Ver el top de qué Regiones votaron más proporcionalmente

st.subheader("3. Porcentaje promedio de participación por departamento")

df_participacion = (
    df.groupby("departamento")["POR_CIUDADANOS_VOTARON"]
    .mean()
    .sort_values(ascending=False)
)

st.bar_chart(df_participacion)

# Análisis de comportamiento por zonas

st.subheader("4. Participación por macroregión")

df_macro = (
    df.groupby("macroregion_inei")["TOT_CIUDADANOS_VOTARON"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(df_macro)

#  Distritos con mayor votación

st.subheader("5. Top 10 distritos con mayor cantidad de ciudadanos que votaron")

top_distritos = df.sort_values(
    by="TOT_CIUDADANOS_VOTARON",
    ascending=False
).head(10)

st.dataframe(
    top_distritos[
        [
            "departamento",
            "provincia",
            "distrito",
            "ELECTORES_HABIL",
            "TOT_CIUDADANOS_VOTARON",
            "POR_CIUDADANOS_VOTARON"
        ]
    ]
)

# PARTE 4: MACHINE LEARNING

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.header("Parte 4: Análisis con Machine Learning (Clustering)")

# Selección de variables
X = df[[
    "ELECTORES_HABIL",
    "TOT_CIUDADANOS_VOTARON",
    "POR_CIUDADANOS_VOTARON"
]]

# Normalizar datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Aplicar KMeans
kmeans = KMeans(n_clusters=3, random_state=42)
df["cluster"] = kmeans.fit_predict(X_scaled)

st.subheader("Asignación de clusters")
st.dataframe(df[[
    "departamento",
    "provincia",
    "distrito",
    "cluster"
]].head(20))
