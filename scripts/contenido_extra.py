"""Agrega al contenido del sitio: hallazgos actualizados, contexto regional, diversidad y seleccion de prensa.
Se corre una sola vez sobre data/contenido.json (es idempotente: reemplaza las secciones que crea).
"""
import json, os
import pandas as pd

SITIO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(SITIO, 'data', 'contenido.json')
PRENSA = os.path.normpath(os.path.join(SITIO, '..', '..', '..', '05_MARCOS', 'datos', 'upala_juventud', 'capas', 'prensa_notas.csv'))

c = json.load(open(P, encoding='utf-8'))
H = {h['id']: h for h in c['hallazgos']}

punto_abst = ('También es donde menos se vota: en la segunda ronda presidencial de 2022 no votó el 68,0% en San José (Pizote) '
              'y el 63,9% en Dos Ríos, el 2.º y el 6.º abstencionismo más alto entre todos los distritos del país.')
if punto_abst not in H['H1']['puntos']:
    H['H1']['puntos'].append(punto_abst)
if 'TSE, segunda ronda 2022' not in H['H1']['fuentes']:
    H['H1']['fuentes'].append('TSE, segunda ronda 2022')

H['H2'].update({
    'titulo': 'La maternidad adolescente se concentra en Delicias y San José (Pizote)',
    'verdad': 'hecho operativo',
    'fuentes': ['INEC, estadísticas vitales 2020-2025', 'INEC, estimaciones Censo 2022',
                'Ministerio de Salud, ASIS Upala 2023 (fecundidad general, indicio indirecto)'],
    'distritos': ['21305', '21303'],
    'puntos': [
        'Entre 2020 y 2025, el 17,0% de los nacimientos en Delicias fue de madres menores de 20 años y el 7,6% de madres menores de 18. En el cantón son 11,7% y 5,2%.',
        'San José (Pizote) es el segundo distrito: 12,4% de los nacimientos de madres menores de 20 años y 5,9% de menores de 18.',
        'El Censo 2022 coincide: 6,1% de las adolescentes de San José (Pizote) y 5,6% de las de Delicias ya son madres, frente a 3,2% en el país.',
        'En el cantón nacieron 26 bebés de niñas menores de 15 años entre 2020 y 2025: 6 en Delicias, 6 en San José (Pizote) y 6 en el distrito Upala. Por ley, cada caso es un delito sexual.',
        'La tendencia baja en todos los distritos: en el cantón, los nacimientos de madres menores de 20 años pasaron de 24,5% (2010-2014) a 11,7% (2020-2025).',
    ]})

c['contexto'] = [
    {'titulo': 'Violencia en los centros educativos de la región', 'ambito': 'Dirección Regional de Educación Zona Norte-Norte, 2023', 'verdad': 'señal',
     'puntos': ['Ciberacoso: 2,52 casos por cada 1.000 estudiantes, frente a 1,37 en el país (4.º lugar entre 27 regiones).',
                'Violencia de docentes y de otro personal hacia estudiantes: 6.º lugar entre 27 regiones.',
                'Los casos registrados de lesiones autoinfligidas o riesgo suicida están por debajo del país (23.º lugar). Puede ser subregistro: en 2020, una funcionaria de salud alertó que los intentos de suicidio de 10 a 17 años en Upala pasaron de 3 en 2017 a 25 en 2019.'],
     'fuente': 'MEP, Situaciones de violencia en centros educativos 2018-2023 (tasas: cálculo propio); UNA Comunica, 3 de marzo de 2020'},
    {'titulo': 'Embarazo y maternidad en estudiantes', 'ambito': 'Dirección Regional de Educación Zona Norte-Norte, 2016-2019', 'verdad': 'señal',
     'puntos': ['Alumnas menores de edad embarazadas: 21, 28, 32 y 31 por año.', 'Alumnas menores de edad que ya son madres: 34, 40, 32 y 42 por año.'],
     'fuente': 'MEP, Estudiantes embarazadas, madres y padres menores de edad 2016-2019 (Cuadros 3 y 4)'},
    {'titulo': 'Población migrante', 'ambito': 'Área de Salud de Upala, 2023', 'verdad': 'señal',
     'puntos': ['12.523 personas extranjeras adscritas al Área de Salud; 12.031 nacidas en Nicaragua.',
                'Estudiantes extranjeros en 2021: 4,7% en primaria y 3,6% en secundaria.'],
     'fuente': 'Municipalidad de Upala, Política Municipal de Movilidad Humana 2024-2034 (datos de la CCSS y el MEP)'},
    {'titulo': 'Participación electoral joven', 'ambito': 'Cantón de Upala, segunda ronda presidencial 2022', 'verdad': 'señal',
     'puntos': ['No votó el 65,8% de 18 a 19 años, el 69,0% de 20 a 24 años, el 65,1% de 25 a 29 años y el 57,1% de 30 a 34 años.',
                'En todo el padrón del cantón, el abstencionismo fue de 55,0%.'],
     'fuente': 'TSE, Estadísticas del Sufragio, segunda ronda 2022 (Cuadros 1.4 y 5.3)'},
    {'titulo': 'Prevención en escuelas y colegios', 'ambito': 'Dirección Regional de Educación Zona Norte-Norte, 2019', 'verdad': 'señal',
     'puntos': ['El programa Convivir llegó al 73,0% de la matrícula de primaria de la región, frente a 39,4% en el país.',
                'En secundaria, el programa de prevención PDEIT llegó solo al 4,8%, frente a 10,4% en el país.'],
     'fuente': 'MEP, Departamento de Análisis Estadístico, programas de prevención del uso indebido de drogas 2014-2019'},
]

c['diversidad'] = {
    'titulo': 'Juventud LGBTIQ+: lo que no se mide',
    'texto': 'En Costa Rica no existe ninguna estadística oficial sobre población LGBTIQ+ por cantón o distrito. Estos son los datos más cercanos a Upala; ninguno permite estimar cuántas personas jóvenes LGBTIQ+ viven en el cantón.',
    'puntos': [
        'En la encuesta cantonal de juventud de Upala de 2010 (855 personas de 15 a 35 años), el 35,8% dijo que en el cantón hay discriminación por preferencia sexual. Es la única medición local y tiene 16 años.',
        'Región Huetar Norte, 2026: el 1,1% de las personas jóvenes reporta discriminación por orientación sexual o identidad de género en su centro educativo (país: 2,4%).',
        'Provincia de Alajuela: 565 matrimonios entre personas del mismo sexo entre 2020 y 2024. El dato por cantón existe en el INEC, pero solo por solicitud.',
        'El MEP registró 83 casos de discriminación por orientación sexual y 35 por identidad de género en todo el país en 2023.'],
    'fuente': 'CPJ, Encuesta cantonal de juventud de Upala 2010 (Gráfico 23); CPJ, IV Encuesta Nacional de Juventudes 2026 (Cuadro 6); INEC, matrimonios 2020-2024; MEP, Situaciones de violencia 2018-2023',
    'propuesta': 'Incluir en una consulta propia preguntas anónimas sobre discriminación, comparables con las de 2010, y reportar solo resultados agregados.'}

n = pd.read_csv(PRENSA, dtype=str)
SEL = [(0, 'Estudiantes del liceo de Cuatro Bocas denuncian agresión policial durante una protesta', 'Aguas Claras'),
       (4, 'Estudiantes de Upala reclaman por las deficiencias de la infraestructura de sus colegios', 'Delicias y Upala'),
       (6, 'Inauguran el Colegio Científico de Upala, con la UNED', 'Upala'),
       (14, 'Alerta por el aumento de intentos de suicidio en adolescentes de Upala', 'Cantón'),
       (16, 'Detienen a seis personas por vender drogas a domicilio', 'Cantón'),
       (18, 'Detienen a dos sospechosos de venta de drogas en el sector de Brasilia', 'Dos Ríos'),
       (27, 'Detienen a un sospechoso de violar a una niña de 12 años', 'Upala'),
       (29, 'El PANI atiende a colegiales involucrados en un video sexual en el CTP de Upala', 'Upala'),
       (31, 'Entregan materiales para educar a la niñez sobre la trata de personas', 'Delicias'),
       (34, 'ACNUR abre una oficina en Upala por el aumento de solicitudes de refugio', 'Cantón'),
       (36, 'Tras el huracán Otto faltaban cuadernos y uniformes para volver a clases', 'Upala'),
       (41, 'Bijagua se recupera del huracán Otto con el turismo', 'Bijagua'),
       (42, 'Estudiantes en peligro por el desvío de un río', 'Aguas Claras'),
       (43, 'Evacuan a menores de un centro educativo afectado por lluvias', 'Cantón'),
       (48, 'En la zona norte baja el subempleo, pero miles dejan de buscar trabajo', 'Región')]
c['prensa'] = [{'texto': t, 'lugar': l, 'medio': n.loc[i, 'medio'].split(' (')[0], 'fecha': n.loc[i, 'fecha'], 'url': n.loc[i, 'url'],
                'institucional': 'institucional' in n.loc[i, 'medio']} for i, t, l in SEL]

nota = 'Las notas de prensa sirven para detectar temas, no como fuente de cifras. Los comunicados institucionales se marcan como tales.'
if nota not in c['tensiones']:
    c['tensiones'].append(nota)
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ok', len(c['prensa']), 'notas')

# --- IV Encuesta Nacional de Juventudes 2026: Huetar Norte frente al pais (CPJ) ---
c = json.load(open(P, encoding='utf-8'))
c['enj'] = {
    'titulo': 'Huetar Norte frente al país',
    'ambito': 'IV Encuesta Nacional de Juventudes 2026, región Huetar Norte (incluye Upala), personas de 15 a 35 años',
    'filas': [
        {'txt': 'Estudia actualmente', 'hn': 40.5, 'pais': 45.3, 'peor': 'bajo', 'ref': 'Gráfico 2, p. 20'},
        {'txt': 'Sin trabajo remunerado y sin buscar trabajo en el último mes', 'hn': 82.2, 'pais': 62.9, 'peor': 'alto', 'ref': 'Cuadro 8, p. 27'},
        {'txt': 'Tiene internet en la casa', 'hn': 78.7, 'pais': 89.1, 'peor': 'bajo', 'ref': 'Cuadro 22, p. 52'},
        {'txt': 'Está embarazada o su pareja lo está', 'hn': 6.4, 'pais': 3.0, 'peor': 'alto', 'ref': 'Cuadro 18, p. 46'},
        {'txt': 'Tiene hijos o hijas', 'hn': 46.3, 'pais': 38.5, 'peor': None, 'ref': 'Cuadro 18, p. 46'},
        {'txt': 'Tiene acceso a instalaciones deportivas cerradas en su comunidad', 'hn': 31.6, 'pais': 53.3, 'peor': 'bajo', 'ref': 'Cuadro 24, p. 55'},
        {'txt': 'Ha tenido deseos de quitarse la vida', 'hn': 8.0, 'pais': 15.0, 'peor': 'alto', 'ref': 'Gráfico 6, p. 39'},
        {'txt': 'Ha intentado quitarse la vida', 'hn': 5.0, 'pais': 9.1, 'peor': 'alto', 'ref': 'Gráfico 6, p. 39'},
        {'txt': 'Tomó alcohol en el último mes', 'hn': 21.3, 'pais': 35.2, 'peor': 'alto', 'ref': 'Gráfico 7, p. 41'},
        {'txt': 'Vivió al menos una situación de acoso en su centro educativo', 'hn': 44.7, 'pais': 53.6, 'peor': 'alto', 'ref': 'Gráfico 3, p. 23'},
    ],
    'cambios': [
        'Entre 2018 y 2026, la proporción de jóvenes de Huetar Norte que estudia subió de 32,1% a 40,5%.',
        'El embarazo joven bajó a la mitad en el país (de 6,6% a 3,0%), pero no en Huetar Norte (de 6,5% a 6,4%).',
    ],
    'cautela': 'Huetar Norte reporta menos deseos de quitarse la vida, consumo de alcohol y acoso que el país. Puede ser una diferencia real o que se declare menos; el informe no publica márgenes de error por región. La muestra de Huetar Norte fue de 1.244 personas.',
    'fuente': 'Consejo de la Persona Joven, IV Encuesta Nacional de Juventudes 2026 (informe de agosto de 2026) y III Encuesta Nacional de Juventudes 2018 (Cuadro 45 y anexo regional)'}
c['upala2010'] = {
    'titulo': 'Lo que dijeron las personas jóvenes de Upala en 2010',
    'ambito': 'Encuesta cantonal de juventud de Upala, 855 personas de 15 a 35 años, julio de 2010',
    'puntos': [
        'Los problemas del cantón que más señalaron: falta de empleo (76,5%), pobreza (58,2%) y drogadicción (53,3%).',
        'El 48,3% estudiaba y el 20,9% de quienes tenían de 15 a 17 años no estudiaba.',
        'El 42,0% de quienes trabajaban no tenía ninguna garantía laboral.',
        'El 70,8% percibía al menos una forma de discriminación hacia jóvenes en el cantón; la más mencionada, por ser migrante (49,2%).'],
    'nota': 'Es la única encuesta de juventud hecha en el cantón. Tiene 16 años: sirve como línea de base para repetirla.',
    'fuente': 'Consejo de la Persona Joven, Encuesta cantonal de juventud de Upala 2010 (Gráficos 1, 11, 22 y 23)'}
json.dump(c, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('enj ok')
