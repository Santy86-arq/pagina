import streamlit as st

# Constantes de proporción de materiales por m³ de concreto según resistencia
PROPORCIONES_CONCRETO = {
    "150 kg/cm²": {"cemento": 210, "arena": 0.56, "grava": 0.84, "agua": 180},
    "200 kg/cm²": {"cemento": 280, "arena": 0.48, "grava": 0.96, "agua": 180},
    "250 kg/cm²": {"cemento": 350, "arena": 0.56, "grava": 0.84, "agua": 180},
    "300 kg/cm²": {"cemento": 420, "arena": 0.48, "grava": 0.96, "agua": 180},
}

# Peso de varillas por metro lineal (kg/m) según calibre
PESO_VARILLA = {
    3: 0.56,  # Calibre 3/8"
    4: 0.99,  # Calibre 1/2"
    5: 1.55,  # Calibre 5/8"
    6: 2.24,  # Calibre 3/4"
    8: 3.98,  # Calibre 1"
}

# Dimensiones de un block estándar (en metros)
LARGO_BLOCK = 0.40
ALTO_BLOCK = 0.20
ANCHO_JUNTA = 0.015  # 1.5 cm de junta

# Rendimiento de pintura (litros por m²)
RENDIMIENTO_PINTURA = 10  # 1 litro por cada 10 m²

# Función para calcular los materiales de concreto
def calcular_materiales(volumen, resistencia):
    proporciones = PROPORCIONES_CONCRETO.get(resistencia, PROPORCIONES_CONCRETO["250 kg/cm²"])
    cemento = volumen * proporciones["cemento"]
    arena = volumen * proporciones["arena"]
    grava = volumen * proporciones["grava"]
    agua = volumen * proporciones["agua"]
    return cemento, arena, grava, agua

# Función para calcular el acero
def calcular_acero(tipo_elemento, medidas, calibre_varilla, cantidad_varillas, separacion_estribos):
    if tipo_elemento in ["Trabe", "Columna", "Castillo"]:
        largo = medidas["largo"]
        ancho = medidas["ancho"]
        alto = medidas["alto"]
        perimetro = 2 * (ancho + alto)
        longitud_estribo = perimetro + 0.20  # Añadir solape
        cantidad_estribos = (largo * 100) / separacion_estribos  # Convertir a cm
        metros_lineales = (cantidad_varillas * largo) + (cantidad_estribos * longitud_estribo)
    elif tipo_elemento == "Losa":
        largo = medidas["largo"]
        ancho = medidas["ancho"]
        espesor = medidas["espesor"]
        metros_lineales = cantidad_varillas * (largo + ancho)  # Simplificación para ejemplo
    elif tipo_elemento == "Zapata":
        lado1 = medidas["lado1"]
        lado2 = medidas["lado2"]
        altura = medidas["altura"]
        metros_lineales = cantidad_varillas * (lado1 + lado2 + altura)  # Simplificación para ejemplo

    peso_total = metros_lineales * PESO_VARILLA.get(calibre_varilla, 0)
    return metros_lineales, peso_total

# Función para calcular volumen de excavación o demolición
def calcular_volumen(largo, ancho, altura):
    return largo * ancho * altura

# Función para calcular cantidad de block y mortero
def calcular_block(largo_muro, alto_muro):
    area_muro = largo_muro * alto_muro
    cantidad_block = area_muro / (LARGO_BLOCK * ALTO_BLOCK)
    metros_junta = (largo_muro / LARGO_BLOCK) * (alto_muro / ALTO_BLOCK) * ANCHO_JUNTA * 2  # Junta horizontal y vertical
    return area_muro, cantidad_block, metros_junta

# Función para calcular pintura
def calcular_pintura(largo, ancho):
    area = largo * ancho
    litros_pintura = area / RENDIMIENTO_PINTURA
    return area, litros_pintura

# Interfaz de la página web
st.title("Calculadora de Materiales de Construcción")

# Crear pestañas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Cálculo de Concreto", "Cálculo de Acero", "Excavación/Demolición", "Cálculo de Block", "Cálculo de Pintura"])

# Pestaña 1: Cálculo de Concreto
with tab1:
    st.subheader("Cálculo de Concreto")

    # Selección del tipo de elemento
    tipo_elemento = st.selectbox(
        "Selecciona el tipo de elemento:",
        ("Trabe", "Columna", "Castillo", "Losa", "Zapata"),
        key="concreto_elemento"
    )

    # Selección de resistencia del concreto
    resistencia = st.selectbox(
        "Selecciona la resistencia del concreto:",
        options=list(PROPORCIONES_CONCRETO.keys()),
        key="resistencia_concreto"
    )

    # Ingreso de medidas
    st.subheader("Ingresa las medidas (en metros):")
    if tipo_elemento in ["Trabe", "Columna", "Castillo"]:
        largo = st.number_input("Largo:", min_value=0.1, key="concreto_largo")
        ancho = st.number_input("Ancho:", min_value=0.1, key="concreto_ancho")
        alto = st.number_input("Alto:", min_value=0.1, key="concreto_alto")
        volumen = largo * ancho * alto
    elif tipo_elemento == "Losa":
        largo = st.number_input("Largo:", min_value=0.1, key="concreto_largo")
        ancho = st.number_input("Ancho:", min_value=0.1, key="concreto_ancho")
        espesor = st.number_input("Espesor:", min_value=0.1, key="concreto_espesor")
        volumen = largo * ancho * espesor
    elif tipo_elemento == "Zapata":
        lado1 = st.number_input("Lado 1:", min_value=0.1, key="concreto_lado1")
        lado2 = st.number_input("Lado 2:", min_value=0.1, key="concreto_lado2")
        altura = st.number_input("Altura:", min_value=0.1, key="concreto_altura")
        volumen = lado1 * lado2 * altura

    # Calcular y mostrar resultados
    if st.button("Calcular Materiales de Concreto"):
        cemento, arena, grava, agua = calcular_materiales(volumen, resistencia)
        st.subheader("Resultados:")
        st.write(f"**Volumen total de concreto:** {volumen:.2f} m³")
        st.write(f"**Cemento:** {cemento:.2f} kg")
        st.write(f"**Arena:** {arena:.2f} m³")
        st.write(f"**Grava:** {grava:.2f} m³")
        st.write(f"**Agua:** {agua:.2f} litros")

# Pestaña 2: Cálculo de Acero
with tab2:
    st.subheader("Cálculo de Acero")

    # Selección del tipo de elemento
    tipo_elemento = st.selectbox(
        "Selecciona el tipo de elemento:",
        ("Trabe", "Columna", "Castillo", "Losa", "Zapata"),
        key="acero_elemento"
    )

    # Ingreso de medidas
    st.subheader("Ingresa las medidas (en metros):")
    medidas = {}
    if tipo_elemento in ["Trabe", "Columna", "Castillo"]:
        medidas["largo"] = st.number_input("Largo:", min_value=0.1, key="acero_largo")
        medidas["ancho"] = st.number_input("Ancho:", min_value=0.1, key="acero_ancho")
        medidas["alto"] = st.number_input("Alto:", min_value=0.1, key="acero_alto")
    elif tipo_elemento == "Losa":
        medidas["largo"] = st.number_input("Largo:", min_value=0.1, key="acero_largo")
        medidas["ancho"] = st.number_input("Ancho:", min_value=0.1, key="acero_ancho")
        medidas["espesor"] = st.number_input("Espesor:", min_value=0.1, key="acero_espesor")
    elif tipo_elemento == "Zapata":
        medidas["lado1"] = st.number_input("Lado 1:", min_value=0.1, key="acero_lado1")
        medidas["lado2"] = st.number_input("Lado 2:", min_value=0.1, key="acero_lado2")
        medidas["altura"] = st.number_input("Altura:", min_value=0.1, key="acero_altura")

    # Ingreso de datos de acero
    calibre_varilla = st.selectbox("Calibre de varilla:", options=[3, 4, 5, 6, 8], key="calibre_varilla")
    cantidad_varillas = st.number_input("Cantidad de varillas:", min_value=1, key="cantidad_varillas")
    separacion_estribos = st.number_input("Separación de estribos (cm):", min_value=5, key="separacion_estribos")

    # Calcular y mostrar resultados
    if st.button("Calcular Acero"):
        metros_lineales, peso_total = calcular_acero(tipo_elemento, medidas, calibre_varilla, cantidad_varillas, separacion_estribos)
        st.subheader("Resultados:")
        st.write(f"**Metros lineales de acero:** {metros_lineales:.2f} m")
        st.write(f"**Peso total de acero:** {peso_total:.2f} kg")

# Pestaña 3: Excavación/Demolición
with tab3:
    st.subheader("Cálculo de Volumen de Excavación/Demolición")

    # Selección de tipo de trabajo
    tipo_trabajo = st.selectbox(
        "Selecciona el tipo de trabajo:",
        ("Excavación", "Demolición de piso", "Demolición de losa"),
        key="tipo_trabajo"
    )

    # Ingreso de medidas
    st.subheader("Ingresa las medidas (en metros):")
    largo = st.number_input("Largo:", min_value=0.1, key="excavacion_largo")
    ancho = st.number_input("Ancho:", min_value=0.1, key="excavacion_ancho")
    altura = st.number_input("Altura:", min_value=0.1, key="excavacion_altura")

    # Calcular y mostrar resultados
    if st.button("Calcular Volumen"):
        volumen = calcular_volumen(largo, ancho, altura)
        st.subheader("Resultados:")
        st.write(f"**Volumen de {tipo_trabajo.lower()}:** {volumen:.2f} m³")

# Pestaña 4: Cálculo de Block
with tab4:
    st.subheader("Cálculo de Cantidad de Block")

    # Ingreso de medidas
    st.subheader("Ingresa las medidas del muro (en metros):")
    largo_muro = st.number_input("Largo del muro:", min_value=0.1, key="block_largo")
    alto_muro = st.number_input("Alto del muro:", min_value=0.1, key="block_alto")

    # Calcular y mostrar resultados
    if st.button("Calcular Block"):
        area_muro, cantidad_block, metros_junta = calcular_block(largo_muro, alto_muro)
        st.subheader("Resultados:")
        st.write(f"**Área del muro:** {area_muro:.2f} m²")
        st.write(f"**Cantidad de block:** {cantidad_block:.0f} piezas")
        st.write(f"**Metros lineales de junta de mortero:** {metros_junta:.2f} m")

# Pestaña 5: Cálculo de Pintura
with tab5:
    st.subheader("Cálculo de Pintura")

    # Ingreso de medidas
    st.subheader("Ingresa las medidas de la superficie a pintar (en metros):")
    largo = st.number_input("Largo:", min_value=0.1, key="pintura_largo")
    ancho = st.number_input("Ancho:", min_value=0.1, key="pintura_ancho")

    # Calcular y mostrar resultados
    if st.button("Calcular Pintura"):
        area, litros_pintura = calcular_pintura(largo, ancho)
        st.subheader("Resultados:")
        st.write(f"**Área a pintar:** {area:.2f} m²")
        st.write(f"**Litros de pintura necesarios:** {litros_pintura:.2f} litros")