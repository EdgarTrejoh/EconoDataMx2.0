import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st 
import yfinance as yf
from streamlit_gsheets import GSheetsConnection

class graficar():
    def __init__(self):
        self.graficar_linea
        self.graficar_lineas
        self.cargar_datos_gsheets_economics
        self.cargar_datos_yfinance
        self.filtrar_por_fecha
        self.seleccionar_columna_captacion
        self.seleccionar_columna_cartera

    def graficar_linea(df: pd.DataFrame, x_col, y_col, title, x_title = None, y_title = None, line_color= None, title_color=None, title_size=18, width=None, height=None):
        fig = px.line(df, x=x_col, y=y_col)
        
        if x_title:
            fig.update_xaxes(title_text = x_title)
        if y_title:
            fig.update_yaxes(title_text = y_title)
        
        fig.update_layout(
            title_text = title,
            title_font = dict(
                color = title_color,
                size = title_size
            )
        )

        fig.update_traces(line=dict(color = line_color))

        if width and height:
            fig.update_layout(width=width, height=height)

        return fig
    
    def graficar_lineas(df, x_col, y_cols, titles, width=None, height=None):
        fig = go.Figure()
    
        for y_col, title in zip(y_cols, titles):
            fig.add_trace(go.Scatter(x=df[x_col], y=df[y_col], mode='lines', name=title))
            fig.update_layout(xaxis_title=x_col, yaxis_title="Tasa de interés (%)", width=width, height=height)
                
        return fig
    
    @st.cache_resource(ttl=6000)  # Almacena en caché los resultados durante 1 hora (3600 segundos)
    def cargar_datos_gsheets_economics(worksheet_name: str, columns: list= None):
        conn = st.connection("gsheets", type=GSheetsConnection)
        try:
            df = conn.read(worksheet=worksheet_name, usecols=columns, ttl=2).dropna()
            return df
        except Exception as e:
            st.error(f"Error al cargar los datos de la hoja de cálculo '{worksheet_name}': {str(e)}")
            #st.rerun()
            return None

    @st.cache_resource(ttl=6000)
    def cargar_datos_yfinance(symbol: str, period: str):
        try:
            df = yf.download(symbol, period=period)
            return df
        except Exception as e:
            st.error(f"Error al cargar los datos de Yahoo Finance para el símbolo '{symbol}': {str(e)}")
            return None

    def filtrar_por_fecha(df: pd.DataFrame, fecha_minima: str):
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df['Fecha'] = df["Fecha"].dt.strftime('%Y-%m-%d')
        df = df[df['Fecha'] >= fecha_minima]
        return df
    
    def seleccionar_columna_indicadoeres(tipo_info):
        columnas = {
                        'Activo Total': 'Activo',
                        'Capital Contable': 'Capital',
                        'Resultado Neto': 'Resultado',
                    }
        return columnas.get(tipo_info, [])
    
    def seleccionar_columna_captacion(tipo_info):
        columnas = {
                        'Captación Total': 'Captacion',
                        'Depósitos de exigencia inmediata': 'DepExigInm',
                        'Depósitos a plazo': 'DepPlazo',
                        'Cuenta global de captación sin movimientos': 'CtaGlobal',
                    }
        return columnas.get(tipo_info, [])

    def seleccionar_columna_cartera(tipo_info):
        columnas = {
                        'Cartera de Crédito Total': 'CCT',
                        'Cartera Créditos de Consumo': 'CCCT',
                        'Cartera Créditos Empresariales': 'CCE',
                        'Cartera de Tarjeta de Crédito': 'CCCTC',
                        'Cartera Créditos de Nomina' : 'CCCN',
                        'Cartera Créditos Personales': 'CCCP',
                        'Cartera Créditos de Vivienda': 'CCV',
                        'Cartera Crédito Automotriz': 'CCCA',
                    }
        return columnas.get(tipo_info, [])