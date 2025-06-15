# Sistema Predictor de Grupos Relacionados por el Diagnóstico (GRD)

Este proyecto tiene como objetivo desarrollar un modelo de predicción de Grupos Relacionados por el Diagnóstico (GRD) en el momento del **triaje** de pacientes en urgencias. El sistema se enfoca en predecir el GRD **al ingreso**, considerando que ciertas variables clínicas no están disponibles aún.

## Objetivo

Diseñar un predictor de GRD utilizando información disponible en triaje y aplicar técnicas de ciencia de datos desde el análisis exploratorio hasta la validación de modelos.

## Variables Predictoras

- `GRD-Código`
- `GRD-Descripción`
- `Tipo GRD`

**Nota:** se consideraron restricciones sobre la disponibilidad de variables en el momento de triaje.

## Tecnologías y Herramientas

- Python (pandas, scikit-learn, xgboost, matplotlib, seaborn)
- Jupyter Notebooks

## Algoritmos Utilizados

- Decision Tree
- Random Forest
- XGBoost

## Flujo de Trabajo

1. **Análisis Exploratorio de Datos** 
2. **Preprocesamiento:**
    - Imputación de valores faltantes.
    - Codificación de variables categóricas.
    - Normalización / Estandarización si aplica.
3. **División de datos:** entrenamiento (train), validación y prueba (test).
4. **Entrenamiento de modelos:** ajuste de hiperparámetros con validación cruzada.
5. **Evaluación:** comparación de métricas:
    - Accuracy
    - F1-score
    - Recall
    - Matriz de confusión
6. **Selección del mejor modelo.**

## Ejecución

```bash
git clone https://github.com/Santiago-Rivera-Estrada/Practica2InfoMedica.git
```

## Autores

- Luisa Fernanda Enciso Franco – Bioingeniería – Universidad de Antioquia
- Maria Julieth Ostos Plazas – Bioingeniería – Universidad de Antioquia
- Santiago Rivera Estrada – Bioingeniería – Universidad de Antioquia
