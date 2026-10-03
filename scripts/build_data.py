"""Genera data/datos.js para el sitio Juventud de Upala a partir de los CSV del vault ADC.

Uso: python scripts/build_data.py   (desde la carpeta del sitio)
Fuentes: 05_MARCOS/datos/upala_juventud/ (matriz y capas) y 05_MARCOS/datos/upala_decomisos_distrito_2018_2022.csv
"""
import json, os
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
SITIO = os.path.dirname(AQUI)
VAULT = os.path.normpath(os.path.join(SITIO, '..', '..', '..', '05_MARCOS', 'datos'))
UJ = os.path.join(VAULT, 'upala_juventud')

DIST = {'21301': 'Upala', '21302': 'Aguas Claras', '21303': 'San José (Pizote)', '21304': 'Bijagua',
        '21305': 'Delicias', '21306': 'Dos Ríos', '21307': 'Yolillal', '21308': 'Canalete'}
COL = {'Upala': '21301', 'Aguas Claras': '21302', 'San Jose (Pizote)': '21303', 'Bijagua': '21304',
       'Delicias': '21305', 'Dos Rios': '21306', 'Yolillal': '21307', 'Canalete': '21308'}

# Metadatos de cada indicador de la matriz: (fila en matriz, id, nombre visible, unidad, peor, decimales, fuente corta, nota)
# peor = 'alto' si un valor alto es una situacion mas desfavorable para la juventud, 'bajo' si al reves, None si es contexto.
META = [
    ('Poblacion total 2022 (estimacion Censo)', 'pob', 'Población total 2022', 'personas', None, 0, 'INEC, estimaciones Censo 2022', 'Censo con 61% de cobertura: INEC publica estimaciones. Otra serie del INEC (proyecciones 2025) difiere hasta 24% en algunos distritos.'),
    ('% poblacion 12-35 anios (proyeccion 2022)', 'joven', 'Población de 12 a 35 años', '%', None, 1, 'INEC, proyecciones distritales 2025 (cálculo propio por edad simple)', ''),
    ('% nacida en el extranjero 2022', 'extranj', 'Población nacida en el extranjero', '%', None, 1, 'INEC, estimaciones Censo 2022', 'Contexto: no es un problema en sí, pero se asocia a menor aseguramiento y mayor movilidad.'),
    ('% hogares con al menos una carencia (NBI) 2022', 'nbi', 'Hogares con al menos una carencia (NBI)', '%', 'alto', 1, 'INEC, estimaciones Censo 2022', ''),
    ('% poblacion asegurada CCSS 2022', 'aseg', 'Población asegurada en la CCSS', '%', 'bajo', 1, 'INEC, estimaciones Censo 2022', ''),
    ('% viviendas con internet 2022', 'internet', 'Viviendas con internet', '%', 'bajo', 1, 'INEC, estimaciones Censo 2022', ''),
    ('% 5-24 que asiste a educacion 2022', 'asiste', 'Asistencia a la educación (5 a 24 años)', '%', 'bajo', 1, 'INEC, estimaciones Censo 2022', ''),
    ('% 7-17 con 2+ anios de rezago 2022', 'rezago', 'Rezago escolar de 2 años o más (7 a 17)', '%', 'alto', 1, 'INEC, estimaciones Censo 2022', ''),
    ('% 15+ con secundaria o mas 2022', 'secund', 'Personas de 15+ con secundaria o más', '%', 'bajo', 1, 'INEC, estimaciones Censo 2022', ''),
    ('IDS 2023 total (0-100)', 'ids', 'Índice de Desarrollo Social 2023', 'puntos (0-100)', 'bajo', 1, 'MIDEPLAN, IDS 2023 (Tabla 20) y Plan Estratégico Municipal 2024-2028', 'Dos fuentes coinciden.'),
    ('IDS 2023 dimension economica', 'ids_eco', 'IDS: dimensión económica', 'puntos (0-100)', 'bajo', 1, 'MIDEPLAN, IDS 2023', ''),
    ('IDS 2023 dimension participacion', 'ids_par', 'IDS: dimensión participación', 'puntos (0-100)', 'bajo', 1, 'MIDEPLAN, IDS 2023', ''),
    ('% exclusion secundaria 2018-2022', 'excl', 'Exclusión (deserción) en secundaria 2018-2022', '%', 'alto', 2, 'MEP, bases por centro (cálculo propio por periodo)', 'Distrito donde está el colegio, no donde vive el estudiante.'),
    ('% repitencia secundaria 2018-2022', 'repit', 'Repitencia en secundaria 2018-2022', '%', 'alto', 2, 'MEP, bases por centro (cálculo propio)', 'Base 2018 con ceros dudosos; 2017 sin dato.'),
    ('% reprobacion definitiva secundaria 2018-2021', 'reprob', 'Reprobación definitiva en secundaria 2018-2021', '%', 'alto', 2, 'MEP, bases por centro (cálculo propio)', ''),
    ('% aplazados secundaria 2022', 'aplaz', 'Estudiantes aplazados en secundaria 2022', '%', 'alto', 1, 'MEP, bases por centro', 'Yolillal (3,7%) es atípico frente al resto: posible error de la base.'),
    ('% mujeres adolescentes con hijos 2022', 'madres', 'Mujeres adolescentes con hijos', '%', 'alto', 1, 'INEC, estimaciones Censo 2022', ''),
    ('Tasa fecundidad general 2021 (x1000 MEF)', 'fecund', 'Fecundidad general 2021', 'por 1.000 mujeres de 15-49', None, 1, 'Ministerio de Salud, ASIS Área Rectora Upala 2023', 'No es específica de adolescentes.'),
    ('Denuncias OIJ 2019-2025 (6 delitos)', 'denun', 'Denuncias al OIJ 2019-2025', 'denuncias', 'alto', 0, 'OIJ, Estadísticas Policiales', 'Asalto, hurto, robo, tacha y robo de vehículo, homicidio. Mide denuncias, no incidencia real.'),
    ('Asaltos OIJ 2019-2025', 'asaltos', 'Asaltos denunciados 2019-2025', 'denuncias', 'alto', 0, 'OIJ, Estadísticas Policiales', ''),
    ('Homicidios OIJ 2019-2025', 'homic', 'Homicidios 2019-2025', 'casos', 'alto', 0, 'OIJ, Estadísticas Policiales', 'Números pequeños.'),
    ('Tasa ofendidos violencia domestica I-sem 2026 (x100mil)', 'vd', 'Personas ofendidas por violencia doméstica (I sem. 2026)', 'por 100.000 hab.', 'alto', 2, 'Observatorio de la Violencia, Atlas MSP I semestre 2026', 'Un semestre; números pequeños.'),
    ('Tasa aprehendidos Ley Psicotropicos I-sem 2026 (x100mil)', 'psico', 'Aprehensiones por Ley de Psicotrópicos (I sem. 2026)', 'por 100.000 hab.', 'alto', 2, 'Observatorio de la Violencia, Atlas MSP I semestre 2026', 'Mide acción policial, no consumo.'),
    ('Eventos de decomiso 2018-2022 (coca+crack+mari)', 'decom', 'Eventos de decomiso de drogas 2018-2022', 'eventos', 'alto', 0, 'ICD, Decomisos por cantón y distrito', 'Cocaína, crack y marihuana. Mide acción policial, no consumo.'),
]

CAPA = {'pob': 'Población', 'joven': 'Población', 'extranj': 'Población', 'nbi': 'Condiciones de vida', 'aseg': 'Condiciones de vida',
        'internet': 'Condiciones de vida', 'ids': 'Desarrollo social', 'ids_eco': 'Desarrollo social', 'ids_par': 'Desarrollo social',
        'asiste': 'Educación', 'rezago': 'Educación', 'secund': 'Educación', 'excl': 'Educación', 'repit': 'Educación', 'reprob': 'Educación',
        'aplaz': 'Educación', 'superv': 'Educación', 'madres': 'Salud', 'fecund': 'Salud', 'denun': 'Seguridad', 'asaltos': 'Seguridad', 'homic': 'Seguridad',
        'vd': 'Seguridad', 'psico': 'Drogas', 'decom': 'Drogas'}


# Como se lee cada indicador: (nombre explicito, sufijo que acompana al valor, lectura en una frase)
LECTURA = {
    'pob': ('Población total 2022', 'habitantes', 'Personas que viven en el distrito según la estimación del INEC para 2022. Es contexto, no un problema.'),
    'joven': ('Peso de la población de 12 a 35 años', '% tiene de 12 a 35 años', 'Porcentaje de la población que tiene entre 12 y 35 años. Es contexto, no un problema.'),
    'extranj': ('Población nacida en el extranjero', '% nació fuera del país', 'Porcentaje de la población que nació fuera de Costa Rica. Es contexto, no un problema.'),
    'nbi': ('Hogares con al menos una carencia (NBI)', '% de hogares con carencias', 'Porcentaje de hogares con al menos una necesidad básica insatisfecha. Más alto es peor: arriba queda el distrito con más hogares en carencia.'),
    'aseg': ('Población que tiene seguro de la CCSS', '% tiene seguro', 'Porcentaje de la población que sí tiene seguro de la CCSS. Más bajo es peor: arriba queda el distrito con menos personas aseguradas.'),
    'internet': ('Viviendas que tienen internet', '% de viviendas con internet', 'Porcentaje de viviendas que sí tienen conexión a internet. Más bajo es peor: arriba queda el distrito con menos acceso.'),
    'asiste': ('Personas de 5 a 24 años que asisten a estudiar', '% asiste', 'Porcentaje de personas de 5 a 24 años que sí asisten a la educación regular. Más bajo es peor: arriba queda el distrito donde menos asisten.'),
    'rezago': ('Estudiantes de 7 a 17 años con 2 o más años de atraso', '% con 2+ años de atraso', 'Porcentaje de niñas, niños y adolescentes de 7 a 17 años que van atrasados 2 años o más respecto al nivel que les corresponde. Más alto es peor.'),
    'secund': ('Personas de 15 años o más que alcanzaron secundaria', '% llegó a secundaria', 'Porcentaje de personas de 15 años o más que sí alcanzaron la secundaria o un nivel mayor. Más bajo es peor: arriba queda el distrito con menos escolaridad.'),
    'ids': ('Índice de Desarrollo Social 2023', 'puntos de 100', 'Índice de MIDEPLAN de 0 a 100: más puntos, más desarrollo. Más bajo es peor: arriba queda el distrito menos desarrollado.'),
    'ids_eco': ('Índice de Desarrollo Social: dimensión económica', 'puntos de 100', 'Parte económica del índice de MIDEPLAN, de 0 a 100. Más bajo es peor.'),
    'ids_par': ('Índice de Desarrollo Social: dimensión participación', 'puntos de 100', 'Parte de participación ciudadana del índice de MIDEPLAN, de 0 a 100. Más bajo es peor.'),
    'excl': ('Estudiantes que abandonaron el colegio (2018-2022)', '% abandonó', 'Porcentaje de estudiantes de secundaria que abandonaron el colegio durante el año, acumulado 2018-2022. Más alto es peor.'),
    'repit': ('Estudiantes que repitieron el año (2018-2022)', '% repitió', 'Porcentaje de estudiantes de secundaria que repiten el año, acumulado 2018-2022. Más alto es peor.'),
    'reprob': ('Estudiantes que reprobaron el año (2018-2021)', '% reprobó', 'Porcentaje de estudiantes de secundaria que reprobaron de forma definitiva, acumulado 2018-2021. Más alto es peor.'),
    'aplaz': ('Estudiantes que quedaron aplazados (2022)', '% quedó aplazado', 'Porcentaje de estudiantes de secundaria que quedaron aplazados en al menos una materia en 2022. Más alto es peor.'),
    'madres': ('Adolescentes que ya son madres', '% ya es madre', 'Porcentaje de mujeres adolescentes que ya tienen al menos un hijo o hija. Más alto es peor.'),
    'fecund': ('Fecundidad general 2021', 'nacimientos por 1.000 mujeres', 'Nacimientos por cada 1.000 mujeres de 15 a 49 años. Es contexto: no separa a las adolescentes.'),
    'denun': ('Denuncias al OIJ 2019-2025', 'denuncias', 'Cantidad de denuncias por asalto, hurto, robo, robo y tacha de vehículo y homicidio entre 2019 y 2025. Más es peor, pero depende del tamaño de la población.'),
    'denun_tasa': ('Denuncias al OIJ por cada 1.000 habitantes (2019-2025)', 'denuncias por 1.000 hab.', 'Denuncias de 2019 a 2025 divididas entre la población de 2022. Permite comparar distritos de distinto tamaño. Más alto es peor.'),
    'asaltos': ('Asaltos denunciados 2019-2025', 'asaltos', 'Cantidad de asaltos denunciados al OIJ entre 2019 y 2025. Más es peor.'),
    'homic': ('Homicidios 2019-2025', 'homicidios', 'Cantidad de homicidios registrados por el OIJ entre 2019 y 2025. Más es peor. Son números pequeños.'),
    'vd': ('Víctimas de violencia doméstica (I semestre 2026)', 'por 100.000 hab.', 'Personas ofendidas por violencia doméstica por cada 100.000 habitantes en el primer semestre de 2026. Más alto es peor.'),
    'psico': ('Aprehensiones por drogas (I semestre 2026)', 'por 100.000 hab.', 'Personas aprehendidas por la Ley de Psicotrópicos por cada 100.000 habitantes en el primer semestre de 2026. Más alto es peor. Mide acción policial, no consumo.'),
    'decom': ('Decomisos de drogas 2018-2022', 'decomisos', 'Cantidad de eventos de decomiso de cocaína, crack y marihuana entre 2018 y 2022. Más es peor. Mide acción policial, no consumo.'),
}


def limpio(v):
    try:
        f = float(v)
        return None if pd.isna(f) else f
    except (TypeError, ValueError):
        return None


def indicadores():
    m = pd.read_csv(os.path.join(UJ, 'matriz_upala_juventud.csv'))
    out = []
    for fila, iid, nombre, unidad, peor, dec, fuente, nota in META:
        r = m[m.indicador == fila]
        if r.empty:
            raise SystemExit(f'Falta en la matriz: {fila}')
        r = r.iloc[0]
        out.append({'id': iid, 'capa': CAPA[iid], 'nombre': nombre, 'unidad': unidad, 'peor': peor, 'dec': dec,
                    'fuente': fuente, 'nota': nota,
                    'valores': {COL[k]: limpio(r[k]) for k in COL},
                    'canton': limpio(r['Canton']), 'pais': limpio(r['Pais'])})
    # Tasa de denuncias por 1.000 habitantes (calculo propio con la estimacion 2022)
    pob = next(i for i in out if i['id'] == 'pob')
    den = next(i for i in out if i['id'] == 'denun')
    out.insert(out.index(den) + 1, {
        'id': 'denun_tasa', 'capa': 'Seguridad', 'nombre': 'Denuncias al OIJ por 1.000 habitantes (2019-2025)',
        'unidad': 'por 1.000 hab. (7 años)', 'peor': 'alto', 'dec': 1, 'fuente': 'OIJ y estimación de población INEC 2022 (cálculo propio)',
        'nota': 'Comparativo entre distritos. La población 2022 tiene una tensión entre dos series del INEC.',
        'valores': {d: round(den['valores'][d] / pob['valores'][d] * 1000, 1) for d in DIST},
        'canton': round(den['canton'] / pob['canton'] * 1000, 1), 'pais': None})
    # Supervivencia escolar 7o a 11o (cohortes sinteticas, metodo replicado de Nosara)
    r = pd.read_csv(os.path.join(UJ, 'cohortes', 'cohortes_upala_resumen.csv'))
    r = r[r.tramo == '7o a 11o (secundaria)'].set_index('ambito').superv_pct
    pos_excl = next(k for k, i in enumerate(out) if i['id'] == 'excl')
    out.insert(pos_excl, {
        'id': 'superv', 'capa': 'Educación', 'peor': 'bajo', 'dec': 1,
        'unidad': 'de cada 100', 'fuente': 'MEP, matrícula inicial por grado 2014-2022 (cohortes sintéticas, cálculo propio)',
        'nota': 'Distrito del colegio, no de residencia. 7.º incluye repitentes, por eso subestima la retención en todos lados. Canalete sin dato: su colegio no aparece en 2018.',
        'valores': {COL[k]: (float(r[k]) if k in r.index and not pd.isna(r[k]) else None) for k in COL},
        'canton': float(r['Canton Upala']), 'pais': float(r['Costa Rica'])})
    LECTURA['superv'] = ('Estudiantes que llegan de 7.º a 11.º (cohortes 2014-2018)', 'de cada 100 llegan a 11.º',
                         'De cada 100 estudiantes que entran a sétimo, cuántos llegan a undécimo cuatro años después. Más bajo es peor: arriba queda el distrito donde más se pierden.')
    out += extras()
    for i in out:
        i['nombre'], i['sufijo'], i['lectura'] = LECTURA[i['id']]
    # orden por capa para que el selector y la ficha agrupen bien
    orden = ['Población', 'Condiciones de vida', 'Desarrollo social', 'Participación', 'Educación', 'Salud', 'Seguridad', 'Drogas']
    out.sort(key=lambda i: orden.index(i['capa']))
    return out


def ind_simple(iid, capa, peor, dec, unidad, fuente, nota, valores, canton, pais, nombre, sufijo, lectura):
    LECTURA[iid] = (nombre, sufijo, lectura)
    return {'id': iid, 'capa': capa, 'peor': peor, 'dec': dec, 'unidad': unidad, 'fuente': fuente, 'nota': nota,
            'valores': valores, 'canton': canton, 'pais': pais}


def extras():
    capas = os.path.join(UJ, 'capas')
    res = []
    # Nacimientos por edad de la madre y distrito de residencia (INEC, REDATAM VITNAC)
    n = pd.read_csv(os.path.join(capas, 'nacimientos_edad_madre_zona_periodo.csv'), dtype={'zona': str})
    n = n[n.periodo == '2020-2025'].set_index('zona')
    def pct(z, cols):
        return round(float(n.loc[z, cols].sum() / n.loc[z, 'total'] * 100), 1)
    m20, m18 = ['<15', '15-17', '18-19'], ['<15', '15-17']
    fte = 'INEC, estadísticas vitales (REDATAM, nacimientos por residencia de la madre), 2020-2025'
    alaj20, alaj18 = pct('20000', m20), pct('20000', m18)
    res.append(ind_simple('nac20', 'Salud', 'alto', 1, '%', fte, f'Provincia de Alajuela: {fmt_es(alaj20)}%. 2025 puede ser preliminar.',
        {d: pct(d, m20) for d in DIST}, pct('21300', m20), None,
        'Nacimientos de madres menores de 20 años (2020-2025)', '% de los nacimientos',
        'De todos los nacimientos de 2020 a 2025, qué porcentaje fue de madres menores de 20 años. Más alto es peor.'))
    res.append(ind_simple('nac18', 'Salud', 'alto', 1, '%', fte, f'Provincia de Alajuela: {fmt_es(alaj18)}%.',
        {d: pct(d, m18) for d in DIST}, pct('21300', m18), None,
        'Nacimientos de madres menores de 18 años (2020-2025)', '% de los nacimientos',
        'De todos los nacimientos de 2020 a 2025, qué porcentaje fue de madres menores de 18 años. Más alto es peor.'))
    res.append(ind_simple('nac15', 'Salud', 'alto', 0, 'nacimientos', fte, 'Cada caso de una madre menor de 15 años es, por ley, un delito sexual. Números pequeños.',
        {d: int(n.loc[d, '<15']) for d in DIST}, int(n.loc['21300', '<15']), None,
        'Nacimientos de madres menores de 15 años (2020-2025)', 'nacimientos', 'Cantidad de nacimientos de niñas menores de 15 años entre 2020 y 2025. Más es peor.'))
    # Abstencionismo, segunda ronda presidencial 2022 (TSE)
    e = pd.read_csv(os.path.join(capas, 'extra_datos.csv'), dtype=str)
    a = e[(e.indicador == 'Abstencionismo') & (e.sexo == 'todos') & (e.anio == '2022') & (e.grupo_edad == 'todos (18 y mas)')].set_index('distrito_codigo').valor.astype(float)
    res.append(ind_simple('abst', 'Participación', 'alto', 1, '%', 'TSE, cómputo de votos, segunda ronda presidencial 2022 (Cuadro 1.4)',
        'San José (Pizote) tuvo el 2.º abstencionismo más alto entre todos los distritos del país; Dos Ríos, el 6.º. Incluye a todo el padrón. Por edad solo hay dato del cantón: entre 20 y 24 años no votó el 69,0%.',
        {d: float(a[d]) for d in DIST}, float(a['213']), None,
        'Abstencionismo en la elección presidencial 2022', '% no votó', 'Porcentaje del padrón que no votó en la segunda ronda presidencial de 2022. Más alto es peor.'))
    # Censo educativo MEP (Power BI), corte inicial o final 2024, III ciclo
    p = pd.read_csv(os.path.join(capas, 'educ_pbi_datos.csv'), dtype=str)
    def pbi(ind, sexo='Total'):
        x = p[(p.indicador == ind) & (p.anio == '2024') & (p.sexo == sexo) & (p.grupo_edad == 'III ciclo (7o-9o)')].set_index('distrito_codigo').valor.astype(float)
        return {d: round(float(x[d]), 1) for d in DIST}, round(float(x['213']), 1), round(float(x['0']), 1)
    f_pbi = 'MEP, Censo Educativo (tablero público SABER), 2024'
    v, c, pa = pbi('estudiantes_sin_internet_inicial_pct')
    res.append(ind_simple('sin_net', 'Educación', 'alto', 1, '%', f_pbi, 'Lo reporta el propio estudiante. Distrito del centro educativo.', v, c, pa,
        'Estudiantes de 7.º a 9.º sin internet en la casa (2024)', '% sin internet', 'Porcentaje de estudiantes de sétimo a noveno que no tienen internet. Más alto es peor.'))
    v, c, pa = pbi('sobreedad_2mas_inicial_pct')
    res.append(ind_simple('sobreedad', 'Educación', 'alto', 1, '%', f_pbi + ' (cálculo propio)', 'Definición de trabajo: 2 o más años por encima de la edad esperada para el grado. Por confirmar con el MEP.', v, c, pa,
        'Estudiantes de 7.º a 9.º con 2 o más años de atraso (2024)', '% con sobreedad', 'Porcentaje de estudiantes de sétimo a noveno que tienen 2 años o más por encima de la edad que corresponde a su grado. Más alto es peor.'))
    v, c, pa = pbi('aplazados_censo_final_pct')
    res.append(ind_simple('aplaz24', 'Educación', 'alto', 1, '%', f_pbi, 'Condición al cierre del censo educativo.', v, c, pa,
        'Estudiantes de 7.º a 9.º aplazados (2024)', '% quedó aplazado', 'Porcentaje de estudiantes de sétimo a noveno que quedaron aplazados al cierre de 2024. Más alto es peor.'))
    return res


def fmt_es(x):
    return f'{x:.1f}'.replace('.', ',')


def series():
    s = {}
    dc = pd.read_csv(os.path.join(VAULT, 'upala_decomisos_distrito_2018_2022.csv'))
    a = dc.groupby('anio')[['coca_ev', 'crack_ev', 'mari_ev']].sum()
    s['decomisos'] = {'anios': [int(x) for x in a.index], 'Cocaína': a.coca_ev.astype(int).tolist(),
                      'Crack': a.crack_ev.astype(int).tolist(), 'Marihuana': a.mari_ev.astype(int).tolist(),
                      'fuente': 'ICD, Decomisos por cantón y distrito 2018-2022 (eventos)'}
    g = pd.read_csv(os.path.join(UJ, 'capas', 'segur_datos.csv'), dtype=str)
    x = g[g.indicador.str.startswith('Denuncias OIJ') & (g.grupo_edad == 'todos') & (g.distrito_codigo == '213')].copy()
    x['v'] = x.valor.astype(float)
    t = x[x.anio.isin([str(y) for y in range(2019, 2026)])].groupby('anio').v.sum()
    s['denuncias'] = {'anios': [int(y) for y in t.index], 'Cantón Upala': [int(v) for v in t.values],
                      'fuente': 'OIJ, Estadísticas Policiales (6 delitos)'}
    e = pd.read_csv(os.path.join(UJ, 'capas', 'educ_datos.csv'), dtype=str)
    y = e[(e.indicador == 'exclusion_intra_anual_pct') & (e.grupo_edad == 'Total secundaria (7o-12o)')]
    pv = y.pivot_table(index='anio', columns='distrito', values='valor', aggfunc='first')
    anios = [a for a in pv.index if a <= '2022']
    s['exclusion'] = {'anios': [int(a) for a in anios],
                      'Cantón Upala': [round(float(pv.loc[a, 'Upala (canton)']), 2) for a in anios],
                      'Costa Rica': [round(float(pv.loc[a, 'Costa Rica (referencia)']), 2) for a in anios],
                      'fuente': 'MEP, bases por centro (exclusión intra-anual neta, secundaria)'}
    # Nacimientos en madres de 15-19, canton (tablero UNFPA con base INEC; 2024 preliminar)
    h = pd.read_csv(os.path.join(UJ, 'capas', 'salud_datos.csv'), dtype=str)
    z = h[(h.indicador == 'nacimientos_madres_adolescentes') & (h.distrito_codigo == '213') & (h.grupo_edad.str.contains('15', na=False))]
    z = z[z.anio.str.fullmatch(r'\d{4}')].copy()
    z['a'] = z.anio.astype(int)
    z = z[z.a >= 2010].drop_duplicates('a').sort_values('a')
    s['madres_adol'] = {'anios': z.a.tolist(), 'Madres de 15 a 19 años': [int(float(v)) for v in z.valor],
                        'fuente': 'UNFPA, tablero de nacimientos con base INEC (2024 preliminar)'}
    return s


def main():
    geo = json.load(open(os.path.join(SITIO, 'data', 'distritos_upala.geojson'), encoding='utf-8'))
    hall = json.load(open(os.path.join(SITIO, 'data', 'contenido.json'), encoding='utf-8'))
    datos = {'distritos': DIST, 'indicadores': indicadores(), 'series': series(), 'geo': geo, **hall,
             'generado': pd.Timestamp.now().strftime('%Y-%m-%d')}
    with open(os.path.join(SITIO, 'data', 'datos.js'), 'w', encoding='utf-8') as f:
        f.write('window.DATOS = ' + json.dumps(datos, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print('ok', len(datos['indicadores']), 'indicadores', {k: len(v.get('anios', [])) for k, v in datos['series'].items()})


if __name__ == '__main__':
    main()
