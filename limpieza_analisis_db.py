import pandas as pd
import numpy as np
import unicodedata

# Cargar la base de datos
archivo = 'DataBase.xlsx'
df = pd.read_excel(archivo)

# Función para quitar tildes y convertir a mayúsculas
def limpiar_texto(texto):
    if isinstance(texto, str):
        texto = texto.upper()
        texto = unicodedata.normalize('NFKD', texto)
        texto = ''.join([c for c in texto if not unicodedata.combining(c)])
        return texto
    return texto

# Aplicar limpieza a todo el DataFrame
df = df.applymap(limpiar_texto)
# Limpiar tildes y poner en mayúsculas los nombres de las columnas
df.columns = [limpiar_texto(col) for col in df.columns]

# Información de NaN por columna
print('--- Valores NaN por columna ---')
print(df.isna().sum())

# Información de valores únicos por columna
descripcion_columnas = []
for col in df.columns:
    valores_unicos = df[col].nunique(dropna=True)
    muestra_valores = df[col].unique()[:5]
    descripcion_columnas.append({
        'columna': col,
        'valores_unicos': valores_unicos,
        'muestra_valores': muestra_valores
    })

print('\n--- Resumen de columnas ---')
for desc in descripcion_columnas:
    print(f"Columna: {desc['columna']}")
    print(f"  Valores únicos: {desc['valores_unicos']}")
    print(f"  Ejemplo de valores: {desc['muestra_valores']}")
    if desc['valores_unicos'] == 1:
        print('  -> ¡OJO! Solo hay un valor único, probablemente no es significativa para el modelo.')
    print()

# Sugerencia de columnas poco útiles para predecir en triage (basado en valores únicos)
print('--- Sugerencia de columnas poco útiles para predecir en triage ---')
for desc in descripcion_columnas:
    if desc['valores_unicos'] == 1:
        print(f"{desc['columna']} (solo un valor)")

# Diccionarios de normalización para columnas relevantes
normalizaciones = {
    'Tipo de ingreso': {
        'URGENCIAS': 'URGENCIA',
        'URGENCIA': 'URGENCIA',
        'URGENCIA ADULTOS': 'URGENCIA',
        'U.ADULTOS': 'URGENCIA',
        'U. ADULTOS': 'URGENCIA',
        'URGENCIA PEDIATRICA': 'URGENCIA',
        'URGENCIAS PEDIATRICAS': 'URGENCIA',
        'URGENCIA GINECOLOGICA': 'URGENCIA',
        'URGENCIAS GINECOLOGICAS': 'URGENCIA',
        'URGENCIA OBSTETRICA': 'URGENCIA',
        'URGENCIAS OBSTETRICAS': 'URGENCIA',
    },
    'Situacion al alta': {
        'MUERTO': 'FALLECIDO',
        'FALLECIDO': 'FALLECIDO',
        'DEFUNCION': 'FALLECIDO',
    },
    'ServicioAlta': {
        'URGENCIAS': 'URGENCIA',
        'URGENCIA': 'URGENCIA',
        'U.ADULTOS': 'URGENCIA',
        'U. ADULTOS': 'URGENCIA',
        'URGENCIA ADULTOS': 'URGENCIA',
    }
}

# Normalizar valores equivalentes
for columna, reemplazos in normalizaciones.items():
    if columna in df.columns:
        df[columna] = df[columna].replace(reemplazos)

# Eliminar columnas con más del 70% de NaN
umbral_nan = 0.7
porcentaje_nan = df.isna().mean()
columnas_a_eliminar = porcentaje_nan[porcentaje_nan > umbral_nan].index.tolist()

# Imprimir desglose de columnas eliminadas por exceso de NaN
for col in columnas_a_eliminar:
    cantidad_nan = df[col].isna().sum()
    print(f"Columna '{col}' eliminada por exceso de NaN: {cantidad_nan} valores NaN")

df = df.drop(columns=columnas_a_eliminar)
print(f"Columnas eliminadas por exceso de NaN (>70%): {columnas_a_eliminar}")

# Reemplazar NaN: 0 en numéricos, 'DESCONOCIDO' en el resto
for col in df.columns:
    if pd.api.types.is_numeric_dtype(df[col]):
        df[col] = df[col].fillna(0)
    else:
        df[col] = df[col].fillna('DESCONOCIDO')

# Guardar CSV con datos organizados y NaN reemplazados
csv_organizado = 'DataBaseOrganizado.csv'
df.to_csv(csv_organizado, index=False, sep=';')
print(f"CSV con datos organizados y NaN reemplazados guardado como: {csv_organizado}")

# Eliminar columnas poco importantes para el modelo (también en el DataFrame final)
columnas_poco_importantes = [
    'NUM CASO', 'ASEGURADORA -CODIGO-', 'ASEGURADORA -DESCRIPCION-', 'CODIGO DE CIUDAD',
    'FECHA DE INGRESO', 'FECHA DE EGRESO', 'CODIGO CAUSA EXTERNA', 'CAUSA EXTERNA'
]
columnas_poco_importantes = [col for col in columnas_poco_importantes if col in df.columns]
df_final = df.drop(columns=columnas_poco_importantes)
if columnas_poco_importantes:
    print(f"(Final) Columnas poco importantes eliminadas: {columnas_poco_importantes}")

# Eliminar columnas con solo 1 dato único y reportar cuántos datos se eliminaron
columnas_un_valor = [col for col in df_final.columns if df_final[col].nunique(dropna=True) == 1]
datos_borrados = {}
for col in columnas_un_valor:
    datos_borrados[col] = df_final.shape[0]
df_final = df_final.drop(columns=columnas_un_valor)

for col, cantidad in datos_borrados.items():
    print(f"Columna '{col}' eliminada por tener solo 1 dato único. Se eliminaron {cantidad} datos.")

# Guardar CSV con las columnas finales
csv_final = 'DataBaseFinal.csv'
df_final.to_csv(csv_final, index=False, sep=';')
print(f"CSV con columnas finales guardado como: {csv_final}") 