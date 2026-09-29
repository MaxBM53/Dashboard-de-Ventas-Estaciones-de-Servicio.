
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE LA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Dashboard Estaciones de Servicio",
    page_icon="⛽",
    layout="wide"
)

st.title("⛽ Análisis de Ventas y Estimación de Ganancias - EESS Argentina")
st.markdown("Dashboard interactivo desarrollado con **Streamlit** y **Plotly** para el portafolio de análisis de datos.")

# ---------------------------------------------------------
# 2. CARGA DE DATOS (Con Cache para optimizar rendimiento)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    banderas = ['YPF', 'Shell', 'Axion', 'Puma', 'Gulf']
    provincias = ['Mendoza', 'Buenos Aires', 'Córdoba', 'Santa Fe']
    productos = ['Nafta Super', 'Infinia / Premium', 'Diesel 500', 'Infinia Diesel', 'GNC']
    
    data = []
    for _ in range(500):
        prov = np.random.choice(provincias, p=[0.4, 0.3, 0.15, 0.15])
        bandera = np.random.choice(banderas, p=[0.55, 0.20, 0.15, 0.06, 0.04])
        prod = np.random.choice(productos)
        
        # Precios aproximados por litro/m3 en ARS
        precio_base = {'Nafta Super': 1100, 'Infinia / Premium': 1350, 'Diesel 500': 1150, 'Infinia Diesel': 1400, 'GNC': 600}
        precio = precio_base[prod] * np.random.uniform(0.95, 1.05)
        litros_vendidos = np.random.randint(5000, 45000)
        
        # Estimación de Facturación y Comisión/Ganancia Bruta (ejemplo: 8% promedio de comisión)
        facturacion = litros_vendidos * precio
        comision_pct = 0.08
        ganancia_estimada = facturacion * comision_pct
        
        data.append({
            'Provincia': prov,
            'Bandera': bandera,
            'Producto': prod,
            'Precio_Unitario': round(precio, 2),
            'Litros_Vendidos': litros_vendidos,
            'Facturacion_ARS': round(facturacion, 2),
            'Ganancia_Estimada_ARS': round(ganancia_estimada, 2)
        })
    return pd.DataFrame(data)

df = load_data()

# ---------------------------------------------------------
# 3. FILTROS EN LA BARRA LATERAL (SIDEBAR)
# ---------------------------------------------------------
st.sidebar.header("🔍 Filtros de Selección")

provincia_sel = st.sidebar.multiselect(
    "Seleccionar Provincia:",
    options=df['Provincia'].unique(),
    default=df['Provincia'].unique()
)

bandera_sel = st.sidebar.multiselect(
    "Seleccionar Bandera:",
    options=df['Bandera'].unique(),
    default=df['Bandera'].unique()
)

# Filtrar DataFrame según selección
df_filtrado = df[(df['Provincia'].isin(provincia_sel)) & (df['Bandera'].isin(bandera_sel))]

# ---------------------------------------------------------
# 4. MÉTRICAS CLAVE (KPIs)
# ---------------------------------------------------------
st.subheader("📊 Indicadores Principales (KPIs)")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

total_litros = df_filtrado['Litros_Vendidos'].sum()
total_facturacion = df_filtrado['Facturacion_ARS'].sum()
total_ganancia = df_filtrado['Ganancia_Estimada_ARS'].sum()
ticket_promedio = df_filtrado['Facturacion_ARS'].mean() if len(df_filtrado) > 0 else 0

kpi1.metric("Volumen Vendido", f"{total_litros:,.0f} Lts")
kpi2.metric("Facturación Total", f"${total_facturacion:,.2f}")
kpi3.metric("Ganancia Est. (8%)", f"${total_ganancia:,.2f}")
kpi4.metric("Venta Prom. / Operación", f"${ticket_promedio:,.2f}")

st.divider()

# ---------------------------------------------------------
# 5. GRÁFICOS INTERACTIVOS (Plotly)
# ---------------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("⛽ Ventas por Bandera")
    fig_bandera = px.bar(
        df_filtrado.groupby('Bandera')['Litros_Vendidos'].sum().reset_index(),
        x='Bandera',
        y='Litros_Vendidos',
        color='Bandera',
        title="Volumen Total Vendido por Operador (Litros)",
        text_auto='.2s'
    )
    st.plotly_chart(fig_bandera, use_container_width=True)

with col_right:
    st.subheader("📊 Distribución por Producto")
    fig_producto = px.pie(
        df_filtrado,
        names='Producto',
        values='Facturacion_ARS',
        title="Participación en Facturación por Producto",
        hole=0.4
    )
    st.plotly_chart(fig_producto, use_container_width=True)

# ---------------------------------------------------------
# 6. TABLA DE DATOS DETALLADA
# ---------------------------------------------------------
with st.expander("📄 Ver Tabla de Datos Filtrada"):
    st.dataframe(df_filtrado, use_container_width=True)



