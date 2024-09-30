import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openai  # Nuevo import para OpenAI

# Configura tu clave de API de OpenAI
openai.api_key = 'clave'  # Reemplaza con tu clave de API

# Carga el archivo CSV desde GitHub
url = "https://raw.githubusercontent.com/jeanarteaga/Proyecto_final_F/refs/heads/main/Datos_proyecto_final_limpio.csv"
data = pd.read_csv(url)

# Título del Dashboard
st.title("Dashboard Interactivo de 100 Empresas")
st.subheader("Primero selecciona la opción que deseas analizar del menú desplegable lateral izquierdo.")

# Barra lateral para selección del análisis
st.sidebar.title("Opciones de Análisis")

# Opciones de análisis
opciones_analisis = ["Todas las empresas", "Por Industria", "Por País", "Por Tamaño de Empresa"]
seleccion = st.sidebar.selectbox("Seleccione qué desea analizar:", opciones_analisis)

# Mostrar la opción seleccionada
st.write(f"Ha seleccionado analizar:   {seleccion}")
st.write("Para ver un resumen en tabla de las empresas y algunos gráficos preestablecidos, haz clic en el botón de abajo.")

# Mapear la selección a la columna correspondiente en el DataFrame
if seleccion == "Por Industria":
    filtro_comparacion = 'Industria'
elif seleccion == "Por País":
    filtro_comparacion = 'País'
elif seleccion == "Por Tamaño de Empresa":
    filtro_comparacion = 'Tamaño_empresa'  
else:
    filtro_comparacion = None

if filtro_comparacion:
    subcategorias_seleccionadas = st.multiselect(
        f"Selecciona una o más categorías de {seleccion} para comparar:",
        data[filtro_comparacion].unique()
    )

    if subcategorias_seleccionadas:
        # Filtrar los datos según la selección
        data_filtrada = data[data[filtro_comparacion].isin(subcategorias_seleccionadas)]

        st.subheader(f"Análisis de empresas por {seleccion}")
        st.write(data_filtrada.head(10))

        # Distribución de empresas en las subcategorías seleccionadas
        st.subheader(f"Distribución de empresas por {seleccion}")
        fig, ax = plt.subplots()
        data_filtrada[filtro_comparacion].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
        ax.set_ylabel('')
        st.pyplot(fig)

        
else:
    # === Opción "Todas las empresas" ===
    if st.button("Mostrar Tabla y Gráficos"):
        st.subheader("Primeras 10 líneas de la tabla")
        st.write(data.head(10))

        # Crear gráficos de pie por Industria, País y Tamaño de Empresa
        st.subheader("Distribución de las empresas por Industria")
        fig1, ax1 = plt.subplots()
        data['Industria'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax1)
        ax1.set_ylabel('')
        st.pyplot(fig1)

        st.subheader("Distribución de las empresas por País")
        fig2, ax2 = plt.subplots()
        data['País'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax2)
        ax2.set_ylabel('')
        st.pyplot(fig2)

        st.subheader("Distribución de las empresas por Tamaño de Empresa")
        fig3, ax3 = plt.subplots()
        data['Tamaño_empresa'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax3)
        ax3.set_ylabel('')
        st.pyplot(fig3)

       

    # Inicializar data_seleccionada en session_state si no existe
    if 'data_seleccionada' not in st.session_state:
        st.session_state['data_seleccionada'] = pd.DataFrame()

    # Botón para calcular y comparar ratios financieros
    st.subheader("Calcular ratios financieros para empresas seleccionadas")
    empresas_seleccionadas = st.multiselect(
        "Seleccione hasta 10 empresas para calcular ratios:",
        data['ID_empresa'].unique(),
        max_selections=10
    )

    if st.button("Calcular y Comparar Ratios"):
        if empresas_seleccionadas:
            # Filtrar las empresas seleccionadas
            data_seleccionada = data[data['ID_empresa'].isin(empresas_seleccionadas)].copy()

            # Calcular los ratios
            data_seleccionada['Ratio_Liquidez_Corriente'] = data_seleccionada['Activo_ciculante_MM'] / data_seleccionada['Pasivo_circulante_MM']
            data_seleccionada['Ratio_Deuda_a_Patrimonio'] = (
                data_seleccionada['Deuda_Corto_Plazo_MM'] + data_seleccionada['Deuda_Largo_Plazo_MM']
            ) / data_seleccionada['Capital_MM']
            data_seleccionada['Cobertura_Gastos_Financieros'] = data_seleccionada['Ingresos_totales_MM'] / data_seleccionada['Gastos_financieros_MM']

            # Guardar los datos calculados en session_state
            st.session_state['data_seleccionada'] = data_seleccionada

            # Mostrar los resultados en una tabla
            st.subheader("Ratios Financieros Calculados")
            st.write(data_seleccionada[['ID_empresa', 'Ratio_Liquidez_Corriente', 'Ratio_Deuda_a_Patrimonio', 'Cobertura_Gastos_Financieros']])

    # Comprobar si hay datos calculados para mostrar
    if not st.session_state['data_seleccionada'].empty:
        data_seleccionada = st.session_state['data_seleccionada']

        # Comparar visualmente los ratios seleccionados
        ratio_a_comparar = st.selectbox(
            "Seleccione un ratio para comparar:",
            ['Ratio_Liquidez_Corriente', 'Ratio_Deuda_a_Patrimonio', 'Cobertura_Gastos_Financieros']
        )

        fig5, ax5 = plt.subplots()
        data_seleccionada.plot(x='ID_empresa', y=ratio_a_comparar, kind='bar', ax=ax5)
        ax5.set_title(f"Comparación de {ratio_a_comparar} entre empresas")
        st.pyplot(fig5)

       

# Filtro adicional para comparar Industria, País, o Tamaño de Empresa
st.subheader("Comparar por categoría")

# Opciones de filtro
opcion_filtro = st.selectbox("Selecciona una categoría para comparar:", ["Industria", "País", "Tamaño de Empresa", ""])

# Mapear la opción seleccionada a la columna correspondiente en el DataFrame
if opcion_filtro == "Industria":
    filtro_comparacion = 'Industria'
elif opcion_filtro == "País":
    filtro_comparacion = 'País'
elif opcion_filtro == "Tamaño de Empresa":
    filtro_comparacion = 'Tamaño_empresa'  
else:
    filtro_comparacion = None

if filtro_comparacion:
    subcategorias_seleccionadas = st.multiselect(
        f"Selecciona una o más {opcion_filtro} para comparar:",
        data[filtro_comparacion].unique()
    )

    if subcategorias_seleccionadas:
        # Incluir las razones financieras en la selección de variables numéricas
        variable_numerica = st.selectbox(
            f"Selecciona una variable numérica para comparar en {opcion_filtro}:",
            ['Ingresos_totales_MM', 'Deuda_Corto_Plazo_MM', 'Deuda_Largo_Plazo_MM',
             'Activo_ciculante_MM', 'Pasivo_circulante_MM', 'Capital_MM',
             'Gastos_financieros_MM', 'R_liquidez', 'R_apalancamiento', 'R_cobertura_intereses']
        )

        if st.button("Mostrar gráfico de comparación"):
            data_filtrada = data[data[filtro_comparacion].isin(subcategorias_seleccionadas)]
            fig, ax = plt.subplots()
            data_filtrada.groupby(filtro_comparacion)[variable_numerica].sum().plot.pie(autopct='%1.1f%%', ax=ax)
            ax.set_ylabel('')
            st.subheader(f"Gráfico de comparación para {variable_numerica} en {', '.join(subcategorias_seleccionadas)}")
            st.pyplot(fig)

            

columna_categoria = None
data_filtrada = None

if seleccion == "Por Industria":
    columna_categoria = 'Industria'
elif seleccion == "Por País":
    columna_categoria = 'País'
elif seleccion == "Por Tamaño de Empresa":
    columna_categoria = 'Tamaño_empresa'  

# Mostrar tabla con promedios de las variables numéricas por categoría seleccionada
if columna_categoria:
    if st.button(f"Mostrar tabla para {seleccion}"):
        st.subheader(f"Tabla de promedios por {columna_categoria}")
        tabla_promedios = data.groupby(columna_categoria)[
            ['Ingresos_totales_MM', 'Deuda_Corto_Plazo_MM', 'Deuda_Largo_Plazo_MM',
             'Activo_ciculante_MM', 'Pasivo_circulante_MM', 'Capital_MM',
             'Gastos_financieros_MM']
        ].mean()
        st.write(tabla_promedios)

    categoria_seleccionada = st.selectbox(
        f"Selecciona una categoría de {seleccion}",
        data[columna_categoria].unique()
    )
    data_filtrada = data[data[columna_categoria] == categoria_seleccionada]
    tipo_grafico = st.radio("Seleccione el tipo de gráfico:", ('Barras', 'Líneas'))

    if st.button(f"Mostrar gráficos para {categoria_seleccionada}"):
        promedios = data_filtrada[
            ['Ingresos_totales_MM', 'Deuda_Corto_Plazo_MM', 'Deuda_Largo_Plazo_MM',
             'Activo_ciculante_MM', 'Pasivo_circulante_MM', 'Capital_MM',
             'Gastos_financieros_MM']
        ].mean()

        st.write(f"Promedios para {categoria_seleccionada}:")
        st.write(promedios)

        st.subheader(f"Gráfico de promedios para {categoria_seleccionada}")
        fig, ax = plt.subplots()
        if tipo_grafico == 'Barras':
            promedios.plot(kind='bar', ax=ax)
        else:
            promedios.plot(kind='line', marker='o', ax=ax)
        ax.set_ylabel('Valor promedio')
        ax.set_title(f"Promedios de variables numéricas para {categoria_seleccionada}")
        st.pyplot(fig)

      

    # Botón para mostrar razones financieras por separado
    if st.button(f"Mostrar razones financieras para {categoria_seleccionada}"):
        if data_filtrada is not None:
            promedios_razones = data_filtrada[
                ['R_liquidez', 'R_apalancamiento', 'R_cobertura_intereses']
            ].mean()

            st.write(f"Promedios de razones financieras para {categoria_seleccionada}:")
            st.write(promedios_razones)

            # Mostrar gráficos separados para cada razón financiera
            razones = ['R_liquidez', 'R_apalancamiento', 'R_cobertura_intereses']
            for razon in razones:
                st.subheader(f"{razon} para {categoria_seleccionada}")
                fig, ax = plt.subplots()
                ax.bar([razon], [promedios_razones[razon]])
                ax.set_ylabel('Valor promedio')
                st.pyplot(fig)

           

    # Botón para mostrar gráfico de barra apilada para las razones financieras
    if st.button(f"Mostrar barra apilada de razones financieras para {categoria_seleccionada}"):
        if data_filtrada is not None:
            promedios_razones = data_filtrada[
                ['R_liquidez', 'R_apalancamiento', 'R_cobertura_intereses']
            ].mean()

            st.write(f"Gráfico de barra apilada de razones financieras para {categoria_seleccionada}:")
            fig, ax = plt.subplots()
            ax.barh(['Razones Financieras'], [promedios_razones['R_liquidez']], color='blue', label='R_liquidez')
            ax.barh(['Razones Financieras'], [promedios_razones['R_apalancamiento']], left=[promedios_razones['R_liquidez']], color='orange', label='R_apalancamiento')
            ax.barh(['Razones Financieras'], [promedios_razones['R_cobertura_intereses']], left=[promedios_razones['R_liquidez'] + promedios_razones['R_apalancamiento']], color='green', label='R_cobertura_intereses')
            ax.set_xlabel('Valor promedio')
            ax.set_title(f"Razones financieras apiladas para {categoria_seleccionada}")
            ax.legend()
            st.pyplot(fig)

            # Interpretación del gráfico apilado utilizando ChatGPT
     


client = openai.Client(api_key=openai_api_key)

def obtener_respuesta(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
        messages=[
            {"role": "system", "content": """
            Eres un financiero que trabaja para la aseguradora patito, eres experto en el área de solvencia,
            entonces vas a responder todo desde la perspectiva de la aseguradora. Contesta siempre en español
            en un máximo de 50 palabras.
            """}, #Solo podemos personalizar la parte de content
            {"role": "user", "content": prompt}
        ]
    )
    output = response.choices[0].message.content
    return output

prompt_user = st.text_area("Ingresa tu consulta:")
output_modelo=obtener_respuesta(prompt_user)