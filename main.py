import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import functions as fc
from streamlit_option_menu import option_menu
from st_paywall import add_auth

#Main page configuration
st.set_page_config(
     page_title="Inicio", 
     page_icon=":rocket:",
     #layout="wide",
     )

def main():
    col_1, col_2 = st.columns(2)

    with col_1:
        st.image('EconoData.jpg', width=110)
    
    with col_2:
        st.title(':grey[ECONODATA-MX]')
        st.markdown("""
                    [![Twitter](https://img.shields.io/badge/Twitter-@EconoDataMx-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white&labelColor=101010)](https://x.com/EconoDataMx)
                    """)

    # Código del Menú
    menu_options = option_menu(
        menu_title='Menú Principal',
        options=["Inicio", "Indicadores", "Banca", "Vivienda", "Comparativas"],
        icons=["rocket-takeoff-fill", "bar-chart-fill", "bank2", "house-fill", "bookmark-fill"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#DDE4EA"},
            "icon": {"color": "#0E7EEE", "font-size": "15px"},
            "nav-link": {
                "font-size": "15px",
                "text-align": "center",
                "margin": "1px",
                "--hover-color": "#eee"
            },
            "nav-link-selected": {"background-color": "blue"},
        }
    )

    if menu_options == "Inicio":
        st.title(f"Sección actual: {menu_options}")
        st.markdown("""
                    > *El objetivo del presente sitio es proporcionar 
                    información que refleje la evolución de diferentes 
                    indicadores económicos, así como  la condición financiera 
                    de la Banca Múltiple en México.*
                    """
                    )
        periodo = "1mo"

        #Obtener información para resumen de tipo de cambio y-finance
        df_tipo_cambio = fc.graficar.cargar_datos_yfinance('USDMXN=X', periodo)
        df_tipo_cambio_ultimo = df_tipo_cambio['Close'].iloc[-1]
        df_tc_fecha = df_tipo_cambio.index[-1]
        df_tc_fecha_str = df_tc_fecha.strftime('%Y-%m-%d')
        resumen_tipo_cambio = df_tipo_cambio.describe()

        #Obtener información para resumen de inflación
        df_inflacion = fc.graficar.cargar_datos_gsheets_economics('IE_004', [0,2])
        df_inflacion_ultimo = df_inflacion['Inflación Anual'].iloc[-1]
        df_inflacion_fecha = df_inflacion['Fecha'].iloc[-1] 
        resumen_df_inflacion = df_inflacion['Inflación Anual'].describe()

        #Obtener información para resumen de tasa de referencia Banxico
        df_tasa_referencia = fc.graficar.cargar_datos_gsheets_economics('IE_001', [0, 1])
        df_tasa_referencia_fecha = df_tasa_referencia['Fecha'].iloc[-1]
        df_resumen_tasa_referencia = df_tasa_referencia['TasaReferencia'].describe()
        df_tasa_referencia_ultimo = df_tasa_referencia['TasaReferencia'].iloc[-1]

        #Obtener información para resumen del PIB
        df_pib = fc.graficar.cargar_datos_gsheets_economics('IE_006', [2,3,4])
        df_pib_fecha = df_pib['Periodo'].iloc[-1]
        df_resumen_pib = df_pib['Producto interno bruto'].describe()
        df_pib_ultimo = df_pib ['PIB (%)'].iloc[-1] 
        st.subheader("Principales índices")
        
        indicador1, indicador2, indicador3, indicador4 =st.columns(4, gap='medium')
        
        with indicador1:
            st.info(':blue[Tipo de Cambio]', icon= "📌")
            st.metric(label="USD/MXP", value=f"${df_tipo_cambio_ultimo:,.2f}")
            st.text(f"Corte: {df_tc_fecha_str}")
            st.text(resumen_tipo_cambio)

        with indicador2:
            st.info(':blue[Tasa Referencia]', icon="📌")
            st.metric(label="Banxico", value=f"{df_tasa_referencia_ultimo:,.2f} %")
            st.text(f'Corte: {df_tasa_referencia_fecha}')
            st.text(df_resumen_tasa_referencia)

        with indicador3:
            st.info(':blue[Inflación Anual]',icon="📌")
            st.metric(label="INEGI", value=f"{df_inflacion_ultimo:,.2f} %")
            st.text(f"Corte: {df_inflacion_fecha}")
            st.text(resumen_df_inflacion)

        with indicador4:
            st.info(':blue[Variacion Anual PIB]',icon= "📌")
            st.metric(label="INEGI", value=f"{df_pib_ultimo:,.2f} %")
            st.text(f'Trimestre: {df_pib_fecha}')
            st.text(df_resumen_pib)
            
    add_auth(required=True)
    #        login_button_text="Login with Google",
    #        login_button_color="#FD504D",
    #        login_sidebar=True)

    st.write("Congrats, you are subscribed!")
    st.write("the email of the user is " + str(st.session_state.email))

    if menu_options == "Indicadores":
        st.title(f"Sección actual: {menu_options}")

        # Cargar datos 
        df_IE004 = fc.graficar.cargar_datos_gsheets_economics('IE_004', [0, 1, 2])
        if df_IE004 is not None:
            df_IE004 = pd.DataFrame(df_IE004)
            df_IE004 = fc.graficar.filtrar_por_fecha(df_IE004, '2000-01-01')
        
            # Crear las pestañas y la división de la página
            tabs = st.tabs([":chart_with_upwards_trend: Inflacion", ":heavy_dollar_sign: Tipo de Cambio", ":classical_building: Tasa de Referencia", ":building_construction: PIB"])
            
            with tabs[0]:  # Pestaña de Inflacion

                # Dividir la página en dos columnas
                col1, col2 = st.columns([1,1], gap='medium')

                # Mostrar una gráfica en la primera columna
                with col1:
                    st.plotly_chart(fc.graficar.graficar_linea(df_IE004, 'Fecha', 'SP1', 'Evolución Histórica del INPC','Fecha', 'INPC', width=380, height=480))

                # Mostrar la gráfica en la segunda columna
                with col2:
                    st.plotly_chart(fc.graficar.graficar_linea(df_IE004, 'Fecha','Inflación Anual', 'Inflación Anual Histórica','Inflación Anual (%)', width=380, height=480))

                st.markdown("""
                            Fuente: INEGI. 
                            
                            Índices de precios.
                            
                            """)

            with tabs[1]:
                    st.title("Evolución del Tipo de Cambio (USD/MXN)")
                    # Cargar datos de Yahoo Finance
                    
                    with st.form("form_exchange"):
                        period = st.selectbox("Periodo de información", ("5Y", "1Y", "YTD", "7mo", "5mo", "1mo"))
                        df_IE007 = fc.graficar.cargar_datos_yfinance('USDMXN=X', period)
                        df_IE007['Variacion'] = (df_IE007['Close']/df_IE007['Close'].shift()-1)*100
                        submitted = st.form_submit_button("Consultar")
                
                        if submitted:
                    
                            if df_IE007 is not None:
                            # Dividir la página en dos columnas
                                col1, col2 = st.columns([1, 1])

                            # Mostrar el DataFrame en la primera columna
                            with col1:
                                fig_ie007 = px.line(df_IE007,
                                                    x=df_IE007.index,
                                                    y = ['Close'],
                                                    title = "Evolución histórica del tipo de cambio"
                                                    )
                                
                                fig_ie007.update_layout(
                                        height = 380,
                                        width=280,
                                        showlegend = False,
                                        title_font=dict(
                                            color="#027034",
                                            size=14
                                            )
                                        )
                                
                                fig_ie007.update_yaxes(title_text="MXP / USD")
                                fig_ie007.update_xaxes(title="Fecha")
                                
                                st.plotly_chart(fig_ie007)
                                
                            # Mostrar la gráfica en la segunda columna
                            with col2:
                                fig_ie007_bis = px.line(df_IE007,
                                                        x=df_IE007.index,
                                                        y = ["Variacion"],
                                                        title = "Variación del tipo de cambio (%)"
                                                        )
                                fig_ie007_bis.update_layout(
                                        height = 380,
                                        width=280,
                                        showlegend = False,
                                        title_font=dict(
                                            color="#027034",
                                            size=14
                                            )
                                        )
                                
                                fig_ie007_bis.update_yaxes(title_text="Variación (%)")
                                fig_ie007_bis.update_xaxes(title="Fecha")

                                st.plotly_chart(fig_ie007_bis)

                            st.markdown ("[Fuente: Yahoo Finance](https://finance.yahoo.com/)")
            
            with tabs[2]:
                    st.title("Tasa Referencia: Banco de México")
                    # Cargar datos de tasa objetivo de Banxico
                    df_IE001 = fc.graficar.cargar_datos_gsheets_economics('IE_001', [0, 1])
                    if df_IE001 is not None:
                        df_IE001 = pd.DataFrame(df_IE001)
                        st.plotly_chart(fc.graficar.graficar_linea(df_IE001, 'Fecha', 'TasaReferencia', 'Tasa de Referencia BANXICO', 'Tasa de Referencia BANXICO (%)', width=680, height=480))  
                        st.markdown("""
                            Fuente: Banco de México.                            
                            """)

            with tabs[3]:
                st.title("Producto Interno Bruto")
                df_IE006 = fc.graficar.cargar_datos_gsheets_economics('IE_006', [2,4])
                if df_IE006 is not None:
                    df_IE006 = pd.DataFrame(df_IE006)
                    fig_df_IE006 = px.bar(df_IE006, x="Periodo", y = "PIB (%)")
                    st.plotly_chart(fig_df_IE006)
                    st.markdown("""
                            Fuente: INEGI.                            
                            """)

    elif menu_options == "Banca":
        st.title(f"Sección actual: {menu_options}")
        tabs001 = st.tabs([":books: Indicadores Financieros", ":clipboard: Captación(Saldo de Cuentas de Ahorro)", ":credit_card: Colocación (Saldo de Cartera de Créditos)"])        
        
        with tabs001[0]:
            #Indicadores Financieros
            df_C001 = fc.graficar.cargar_datos_gsheets_economics('IE_002')
            df_C001 = pd.DataFrame(df_C001)
            
            with st.form("form_banca"):
                lista_banca = st.selectbox('Tipo de información', ("Activo Total", "Capital Contable", "Resultado Neto"))
                entidades = st.multiselect('Selecciona las entidades:', ['BBVA México', 'Banamex', 'Santander', 'Banorte','HSBC', 'Inbursa', 'Scotiabank', 'Banco Azteca'])                
                
                col_seleccionada = fc.graficar.seleccionar_columna_indicadoeres(lista_banca)                
                columnas_indicadores = [col for col in df_C001.columns if f'{col_seleccionada}-' in col]

                for col in columnas_indicadores:
                    df_C001[f'Var_anual_{col}'] = (df_C001[col] / df_C001[col].shift(12) - 1) * 100

                def graficas_entidad_financiera_indicadores_var_anual(df, entidades):
                    fig_var_indicadores = go.Figure()

                    for entidad in entidades:
                        fig_var_indicadores.add_trace(go.Scatter(x=df['Fecha'],  y=df[f'Var_anual_{col_seleccionada}-{entidad}'], mode = 'lines', name=entidad))
                        
                        fig_var_indicadores.update_layout(title=f'Variación Anual: {lista_banca}', xaxis_title='Fecha', yaxis_title='Variación anual (%)', height = 380, width=580)

                    st.plotly_chart(fig_var_indicadores)
                    
                def graficas_entidad_financiera_indicadores_historica(df, entidades):
                    fig_hist_indicadores = go.Figure()

                    for entidad in entidades:
                        fig_hist_indicadores.add_trace(go.Scatter(x=df['Fecha'],  y=df[f'{col_seleccionada}-{entidad}'], mode = 'lines', name=entidad))
                        
                        fig_hist_indicadores.update_layout(title=f'Evolución Histórica: {lista_banca}', xaxis_title='Fecha', yaxis_title='Saldo (mdp)', height = 380, width=580)

                    st.plotly_chart(fig_hist_indicadores)

                fig_indicadores_sistema = fc.graficar.graficar_linea(df_C001, 'Fecha', f'{col_seleccionada}-SIS',  f'Evolución Histórica: <br>{lista_banca}', "Saldo (mdp)", width=310, height=380)
                fig_indicadores_sistema_var = fc.graficar.graficar_linea(df_C001, 'Fecha', f'Var_anual_{col_seleccionada}-SIS',  f'Variación anual: <br>{lista_banca}', "Variación Anual (%)", width=310, height=380)

                submitted = st.form_submit_button("Consultar")
                
                if submitted:
                        
                    col1, col2 = st.columns([1,1], gap='medium')
                            
                    with col1:
                        st.plotly_chart(fig_indicadores_sistema)
                            
                    with col2:
                        st.plotly_chart(fig_indicadores_sistema_var)
                    
                    st.subheader(':paperclip: Información por Entidades Seleccionadas', divider='gray')
                    with st.expander(":green[Entidades]"):
                        graficas_entidad_financiera_indicadores_historica(df_C001, entidades)
                        graficas_entidad_financiera_indicadores_var_anual(df_C001, entidades)

                    st.markdown("""
                            Fuente: Comisión Nacional Bancaria y de Valores.                            
                            """)

        with tabs001[1]:
            #Captacion
            with st.form("form_captacion"):
                lista_captacion = st.selectbox('Tipo de información', ('Captación Total','Depósitos de exigencia inmediata',  'Depósitos a plazo', 'Cuenta global de captación sin movimientos'))
                entidades = st.multiselect('Selecciona las entidades:', ['BBVA México', 'Banamex', 'Santander', 'Banorte','HSBC', 'Inbursa', 'Scotiabank', 'Banco Azteca'])                
                
                columna_seleccionada = fc.graficar.seleccionar_columna_captacion(lista_captacion)                
                columnas_captacion = [col for col in df_C001.columns if f'{columna_seleccionada}-' in col]

                for col in columnas_captacion:
                    df_C001[f'Var_anual_{col}'] = (df_C001[col] / df_C001[col].shift(12) - 1) * 100
                
                def graficas_entidad_financiera_captacion_var_anual(df, entidades):
                    fig_var_capt = go.Figure()

                    for entidad in entidades:
                        fig_var_capt.add_trace(go.Scatter(x=df['Fecha'],  y=df[f'Var_anual_{columna_seleccionada}-{entidad}'], mode = 'lines', name=entidad))
                        
                        fig_var_capt.update_layout(title=f'Variación Anual: {lista_captacion}', xaxis_title='Fecha', yaxis_title='Variación anual (%)', height = 380, width=580)

                    st.plotly_chart(fig_var_capt)
                    
                def graficas_entidad_financiera_captacion_historica(df, entidades):
                    fig_hist_capt = go.Figure()

                    for entidad in entidades:
                        fig_hist_capt.add_trace(go.Scatter(x=df['Fecha'],  y=df[f'{columna_seleccionada}-{entidad}'], mode = 'lines', name=entidad))
                        
                        fig_hist_capt.update_layout(title=f'Evolución Histórica: {lista_captacion}', xaxis_title='Fecha', yaxis_title='Saldo (mdp)', height = 380, width=580)

                    st.plotly_chart(fig_hist_capt)

                fig_capt_sistema = fc.graficar.graficar_linea(df_C001, 'Fecha', f'{columna_seleccionada}-SIS',  f'Evolución Histórica: <br>{lista_captacion}', "Saldo (mdp)", width=310, height=380)
                fig_capt_sistema_var = fc.graficar.graficar_linea(df_C001, 'Fecha', f'Var_anual_{columna_seleccionada}-SIS',  f'Variación anual: <br>{lista_captacion}', "Variación Anual (%)", width=310, height=380)
               
                submit_2 = st.form_submit_button("Consultar")
                
                if submit_2:
                    
                    col1, col2 = st.columns([1,1], gap='medium')
                            
                    with col1:
                        st.plotly_chart(fig_capt_sistema)
                            
                    with col2:
                        st.plotly_chart(fig_capt_sistema_var)
                    
                    st.subheader(':paperclip: Información por Entidades Seleccionadas', divider='gray')
                    with st.expander(":green[Entidades]"):
                        graficas_entidad_financiera_captacion_historica(df_C001, entidades)
                        graficas_entidad_financiera_captacion_var_anual(df_C001, entidades)

                    st.markdown("""
                            Fuente: Comisión Nacional Bancaria y de Valores.                            
                            """)

        with tabs001[2]:
            #Colocación
            with st.form("form_cartera"):
                #Cargar informacion
                df_C001_Cartera = fc.graficar.cargar_datos_gsheets_economics('IE_002')
                df_C001_Cartera = pd.DataFrame(df_C001_Cartera)
                
                #Filtrar informacion 
                lista_cartera = st.selectbox('Tipo de información', ('Cartera de Crédito Total','Cartera Créditos de Consumo',  'Cartera Créditos Empresariales', 'Cartera de Tarjeta de Crédito', 'Cartera Créditos de Nomina', 'Cartera Créditos Personales',  'Cartera Créditos de Vivienda','Cartera Crédito Automotriz')) 
                entidades = st.multiselect('Selecciona las entidades:', ['BBVA México', 'Banamex', 'Santander', 'Banorte','HSBC', 'Inbursa', 'Scotiabank', 'Banco Azteca'])                

                columna_seleccionada = fc.graficar.seleccionar_columna_cartera(lista_cartera)
                columnas_saldo = [col for col in df_C001_Cartera.columns if f'{columna_seleccionada}_Saldo-' in col]

                #Calcular la variacion anual 
                for col in columnas_saldo:
                    df_C001_Cartera[f'Var_anual_{col}'] = (df_C001_Cartera[col] / df_C001_Cartera[col].shift(12) - 1) * 100        

                #Graficas por entidad financiera
                def graficas_entidad_financiera(df, entidades):
                    fig_saldo = go.Figure()
                    fig_imor = go.Figure()
                    fig_pe = go.Figure()
                    fig_var = go.Figure()

                    for entidad in entidades:
                        fig_saldo.add_trace(go.Scatter(x=df['Fecha'], y=df[f'{columna_seleccionada}_Saldo-{entidad}'], mode='lines', name=entidad))
                        fig_imor.add_trace(go.Scatter(x=df['Fecha'], y=df[f'{columna_seleccionada}_IMOR-{entidad}'], mode='lines', name=entidad))
                        fig_pe.add_trace(go.Scatter(x=df['Fecha'], y=df[f'{columna_seleccionada}_PE-{entidad}'], mode='lines', name=entidad))
                        fig_var.add_trace(go.Scatter(x=df['Fecha'],  y=df[f'Var_anual_{columna_seleccionada}_Saldo-{entidad}'], mode = 'lines', name=entidad))
                        
                        fig_saldo.update_layout(title=f'Comparativo de Saldo: {lista_cartera}', xaxis_title='Fecha', yaxis_title='Saldo (mdp)', height = 380, width=580)
                        fig_imor.update_layout(title=f'Comparativo de IMOR: {lista_cartera}', xaxis_title='Fecha', yaxis_title='IMOR (%)', height = 380, width=580)
                        fig_pe.update_layout(title=f'Comparativo de Pérdida Esperada: {lista_cartera}', xaxis_title='Fecha', yaxis_title='PE (%)', height = 380, width=580)
                        fig_var.update_layout(title=f'Variación Anual: {lista_cartera}', xaxis_title='Fecha', yaxis_title='Variación anual (%)', height = 380, width=580)

                    st.plotly_chart(fig_saldo)
                    st.plotly_chart(fig_var)
                    st.plotly_chart(fig_imor)
                    st.plotly_chart(fig_pe)

                #Graficas Sistema

                fig_saldo_cartera_sistema = fc.graficar.graficar_linea(df_C001_Cartera, 'Fecha', f'{columna_seleccionada}_Saldo-SIS',  f'Evolución Histórica: <br>{lista_captacion}', "Saldo (mdp)", width=310, height=310)
                fig_saldo_cartra_sistema_imor = fc.graficar.graficar_linea(df_C001_Cartera, 'Fecha', f'{columna_seleccionada}_IMOR-SIS',  f'Evolución Histórica IMOR: <br>{lista_captacion}', "IMOR (%)", width=310, height=310)
                fig_saldo_cartra_sistema_pe = fc.graficar.graficar_linea(df_C001_Cartera, 'Fecha', f'{columna_seleccionada}_PE-SIS',  f'Evolución Histórica PE: <br>{lista_captacion}', "PE (%)", width=310, height=310)
                fig_saldo_cartera_sistema_var = fc.graficar.graficar_linea(df_C001_Cartera, 'Fecha', f'Var_anual_{columna_seleccionada}_Saldo-SIS',  f'Variación anual: <br>{lista_captacion}', "Variación Anual (%)", width=310, height=310)

                submit = st.form_submit_button("Consultar")

                if submit:
                    
                    col1, col2 = st.columns(2)

                    with col1:
                        st.plotly_chart(fig_saldo_cartera_sistema)
                        st.plotly_chart(fig_saldo_cartra_sistema_imor)
                    
                    with col2:
                        fig_saldo_cartera_sistema_var
                        fig_saldo_cartra_sistema_pe

                    st.subheader(':paperclip: Información por Entidades Seleccionadas', divider='gray')
                    with st.expander(":green[Entidades]"):
                        graficas_entidad_financiera(df_C001_Cartera, entidades)

                    st.markdown("""
                        Fuente: Comisión Nacional Bancaria y de Valores.                            
                        """)

    elif menu_options == "Vivienda":
        st.title(f"Sección actual: {menu_options}")
        
        tabs002 = st.tabs([':house_buildings:Índice precios a la vivienda (SHF)', ':chart: Índice SHF - Estados', ':chart: Tasa de interés Créditos a la Vivienda']) 
        
        with tabs002[0]:
            st.write("Índice de precios a la vivienda (SHF)")
         
            with st.form("form_SHF"):
                df_IE005 = fc.graficar.cargar_datos_gsheets_economics('IE_005', [1, 6, 7])
                lista = df_IE005['Global'].dropna().unique()
                value= st.selectbox('Tipo de información', lista) 
                df_IE005_bis = df_IE005[df_IE005['Global']==value]  
                df_IE005_bis['Diferencia'] = (df_IE005_bis['Indice']/df_IE005_bis['Indice'].shift(4)-1)*100
                st.write("Información del Índice de Precios a la vivienda SHF")
                
                fig_df_ie005 = fc.graficar.graficar_linea(df_IE005_bis, 'Trimestre', 'Indice',  f'Evolución del Índice SHF <br>{value}', width=310, height=380)
        
                fig_df_ie005_bis = fc.graficar.graficar_linea(df_IE005_bis, 'Trimestre', 'Diferencia',  f'Variación Anual: <br>{value}', "Variación Anual (%)", width=310, height=380)
                
                submitted = st.form_submit_button("Consultar")
                
                if submitted:
        
                    col1, col2 = st.columns([1,1], gap='medium')

                    with col1:
                        st.plotly_chart(fig_df_ie005_bis)

                # Mostrar la gráfica en la segunda columna
                    with col2:
                        st.plotly_chart(fig_df_ie005)
                    
                    st.text("Fuete: SHF, Índice SHF de Precios a la Vivienda en México")

        with tabs002[1]:
            with st.form("form_SHF_Estados"):
                #Indice SHF por Estados
                df_IE007 = fc.graficar.cargar_datos_gsheets_economics('IE_007', [0,3,4,5])
                #Indice SHF por Estados - Municipios   
                df_IE008 = fc.graficar.cargar_datos_gsheets_economics('IE_008', [0,1,4,5,6])
                #Información para mapa
                df_IE009 = fc.graficar.cargar_datos_gsheets_economics('IE_009', [0,1,2,3])
                #Informacion economica por estados
                df_IE011 = fc.graficar.cargar_datos_gsheets_economics('IE_011', [0,1,2,3,4,5,6,7])
                df_IE011 = pd.DataFrame(df_IE011)

                estados = df_IE007['Estado'].unique()
                estado_seleccionado = st.selectbox('Selecciona el Estado:', estados)
                #Dataframe por Estado
                df_IE007_Estado = df_IE007[df_IE007['Estado']==estado_seleccionado]
                #Dataframe Estado - Municipio
                df_IE008_Municipio = df_IE008[df_IE008['Estado']==estado_seleccionado]
                #Dataframe Nacional
                df_nacional = df_IE005[df_IE005['Global']=="Nacional"]
                df_nacional['VarAnual'] = (df_nacional['Indice']/df_nacional['Indice'].shift(4)-1)*100
                
                #Economics
                info_estado = df_IE011[df_IE011['Estado']==estado_seleccionado]
                pob_fem = info_estado['Pob_Femenina'].values[0]
                pob_masc = info_estado['Pob_Masculina'].values[0]
                pob_viviendas = info_estado['Viviendas_Habitadas'].values[0]
                pob_sucursales = info_estado['Sucursales'].values[0]
                pob_cajeros = info_estado['Cajeros_Autom'].values[0]
                pob_tpv = info_estado['TPV'].values[0]
                formatted_pob_fem = "{:,.0f}".format(pob_fem)
                formatted_pob_masc = "{:,.0f}".format(pob_masc)
                formatted_pob_viviendas = "{:,.0f}".format(pob_viviendas)
                formatted_pob_sucursales = "{:,.0f}".format(pob_sucursales)
                formatted_pob_cajeros = "{:,.0f}".format(pob_cajeros)
                formatted_pob_tpv = "{:,.0f}".format(pob_tpv)

                #Gráfico con el histórico del índice
                fig_df_IE007 = go.Figure()

                for municipio in df_IE008_Municipio['Municipio'].unique():
                    df_municipio = df_IE008_Municipio[df_IE008_Municipio['Municipio']== municipio]
                    fig_df_IE007.add_trace(go.Scatter(
                        x = df_municipio['Trimestre'],
                        y = df_municipio['Indice'],
                        mode = 'lines',
                        name = municipio)
                    )

                fig_df_IE007.add_trace(go.Scatter(
                        x=df_IE007_Estado['Trimestre'], 
                        y=df_IE007_Estado['Indice'], 
                        mode='lines', 
                        name= estado_seleccionado))    
                
                fig_df_IE007.add_trace(go.Scatter(
                        x=df_nacional['Trimestre'], 
                        y=df_nacional['Indice'], 
                        mode='lines', 
                        name= 'Nacional'))

                fig_df_IE007.update_layout(
                    title=f"Índice SHF en {estado_seleccionado} por Municipio",
                    xaxis_title="Trimestre",
                    yaxis_title="Índice",
                    legend_title="Municipio",
                    template="plotly_white",
                    width=650, 
                    height=480
                )    
                
                #Gráfico de variación vs trimestre anterior
                fig_df_IE007_Variacion = go.Figure()

                for municipio in df_IE008_Municipio['Municipio'].unique():
                    df_municipio = df_IE008_Municipio[df_IE008_Municipio['Municipio']== municipio]
                    fig_df_IE007_Variacion.add_trace(go.Scatter(
                        x = df_municipio['Trimestre'],
                        y = df_municipio['VarAnual'],
                        mode = 'lines',
                        name = municipio)
                    )

                fig_df_IE007_Variacion.add_trace(go.Scatter(
                        x=df_IE007_Estado['Trimestre'], 
                        y=df_IE007_Estado['VarAnual'], 
                        mode='lines', 
                        name= estado_seleccionado))    
                
                fig_df_IE007_Variacion.add_trace(go.Scatter(
                        x=df_nacional['Trimestre'], 
                        y=df_nacional['VarAnual'], 
                        mode='lines', 
                        name= 'Nacional'))

                fig_df_IE007_Variacion.update_layout(
                    title=f"Variación anual Índice SHF en {estado_seleccionado} por Municipio",
                    xaxis_title="Trimestre",
                    yaxis_title="Índice",
                    legend_title="Municipio",
                    template="plotly_white",
                    width=650, 
                    height=480
                )

                submitted = st.form_submit_button("Consultar")
                
                if submitted:
                    
                    st.title(estado_seleccionado)

                    columna1, columna2, columna3 = st.columns(3)

                    columna1.metric("Población Fenemina*", formatted_pob_fem,)
                    columna2.metric("Población Masculina*", formatted_pob_masc)
                    columna3.metric("Viviendas habitadas*", formatted_pob_viviendas)

                    columna4, columna5, columna6 = st.columns(3)

                    columna4.metric("Cajeros Automáticos**", formatted_pob_cajeros,)
                    columna5.metric("Total de sucursales**", formatted_pob_sucursales)
                    columna6.metric("Terminales Punto de Venta**", formatted_pob_tpv)

                    st.markdown("""
                                *Censo de POblación 2020 INEGI

                                ** Cifras operativas marzo 2024 CNBV       
                                
                                """)

                    st.map(df_IE009[df_IE009['Estado']== estado_seleccionado],
                           latitude='Latitud', 
                           longitude='Longitud', 
                           color="#EE340F", 
                           size=50)
                    
                    st.plotly_chart(fig_df_IE007)

                    st.plotly_chart(fig_df_IE007_Variacion)
                
        with tabs002[2]:
            
            st.write('Tasa de interés créditos a la vivienda')

            df_IEO03 = fc.graficar.cargar_datos_gsheets_economics('IE_003',[0, 4, 5, 6] )

            y_cols = []
            titles = []

            if st.checkbox("Tasa de interés mínima de créditos en pesos a tasa fija"):
                # Si el checkbox está seleccionado, agrega 'Variable1' a la lista de variables seleccionadas
                y_cols.append('SF43424')
                titles.append('Tasa de interés mínima')  # Cambia 'Variable1' por el título adecuado
    
            if st.checkbox("Tasa de interés máxima de créditos en pesos a tasa fija"):
                # Si el checkbox está seleccionado, agrega 'Variable2' a la lista de variables seleccionadas
                y_cols.append('SF43425')
                titles.append('Tasa de interés máxima')  # Cambia 'Variable2' por el título adecuado
    
            if st.checkbox("Tasa de interés promedio de créditos en pesos a tasa fija"):
                # Si el checkbox está seleccionado, agrega 'Variable3' a la lista de variables seleccionadas
                y_cols.append('SF43426')
                titles.append('Tasa de interés promedio')  # Cambia 'Variable3' por el título adecuado

            if y_cols:  # Verifica si se seleccionaron variables para mostrar
                fig = fc.graficar.graficar_lineas(df_IEO03, 'Fecha', y_cols, titles)
                st.plotly_chart(fig)
                st.markdown("""
                Fuente: Banco de México con información proporcionada por los intermediarios e INFOSEL.                            
                """)

            else:
                st.warning("Por favor, selecciona al menos una variable para mostrar.")

    elif menu_options == "Comparativas":
        st.title(f"Sección actual: {menu_options}")

        with st.expander(":green[INEGI]"):
            #st.text("Inflación INEGI")
            st.markdown("### Notas")
            st.markdown("""
                        
                        Portal Web del Instituto Nacional de Estadística y Geografía [INEGI](https://www.inegi.org.mx/) 
                        
                        ---
                        """)
            
        with st.expander(":green[Banxico]"):
            st.markdown("### Notas")
            st.markdown("""
                        
                        Portal Web de Banco de México [BANXICO](https://www.banxico.org.mx/) 
                        
                        ---
                        """
                        )
        
        with st.expander(":green[CNBV]"):
            st.markdown("### Notas")
            st.markdown("""
                        
                        Portal Web de la Comisión Nacional Bancaria y de Valores [CNBV](https://www.gob.mx/cnbv) 
                        
                        ---
                        <p> 1/ Para la cartera total se considera la información de cartera de los
                        bancos junto con la cartera de sus respectivas Sociedades Financieras de 
                        Objeto Múltiple Reguladas a las que consolidan.</p>
                        
                        - **Hasta diciembre 2021**: **_Cartera total_** = Cartera vigente + cartera vencida. </p>
                        - **A partir de enero 2022**: **_Cartera total_** = Cartera de crédito con riesgo de crédito en etapa 1 + 2 + 3 + cartera de crédito valuada a valor razonable. </p>
                        ---

                        2/ Respecto al ***resultado neto*** se muestran saldos acumulados al cierre de mes.
                        
                        ---
                        
                        3/ Hasta diciembre 2021:  **_IMOR = Índice de Morosidad_** = cartera vencida / (Cartera vigente + cartera vencida).

                        - **A partir de enero 2022**: **_IMOR = Índice de Morosidad_** = cartera de crédito con riesgo de crédito en etapa 3 / (Cartera de crédito con riesgo de crédito en etapa 1 + 2 + 3).


                        """, unsafe_allow_html=True)

        with st.expander(":green[SHF]"):
            st.markdown("### Notas")
            st.markdown("""                    
                        Portal Web de Sociedad Hipotecaria Federal [SHF](https://www.gob.mx/shf) 
                        ---
                        """)

if __name__ == "__main__":
    main()