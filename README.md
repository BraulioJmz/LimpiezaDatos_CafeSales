# Cafe Sales Data Cleaning

Este repositorio contiene el código y los procesos utilizados para limpiar la base de datos de ventas de café. 

## Procedimiento

Para llevar a cabo este proyecto se utilizó **Pandas** como librería principal para la manipulación y análisis de datos, debido a su eficiencia manejando grandes volúmenes de información tabular. Adicionalmente, se utilizó **NumPy** específicamente para el manejo estandarizado de valores nulos (convirtiendo los strings inválidos a `np.nan`).

El flujo de trabajo siguió este orden:
1. **Inspección inicial**: Exploración cruda de los tipos de datos, cantidad de nulos reales y valores inválidos, además de la identificación de duplicados.
2. **Estandarización de valores inválidos**: Transformación de las cadenas de texto `'UNKNOWN'` y `'ERROR'` a valores nulos manejables por Pandas.
3. **Corrección de tipos de dato**: Forzar la conversión de texto a formatos numéricos y de fechas, según correspondiera.
4. **Imputación matemática**: Recuperación de valores faltantes en las columnas `Quantity`, `Price Per Unit` y `Total Spent` calculándolos algebraicamente usando las otras variables disponibles de la transacción.
5. **Tratamiento de categóricos**: Reemplazo de los valores nulos restantes en categorías por la etiqueta unificada `'Unknown'`.
6. **Limpieza crítica**: Eliminación definitiva de las filas que no contenían fecha de transacción.
7. **Verificación de duplicados**: Eliminación final de registros idénticos que pudieran introducirse en la lectura.
8. **Exportación**: Verificación final de integridad y guardado de los datos limpios en formato CSV.

### ¿Cómo correr este proyecto?
1. Instala las dependencias necesarias. Se recomienda usar un entorno virtual:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el script de limpieza principal:
   ```bash
   python clean_cafe_sales.py
   ```

## Resumen de Limpieza de Datos

Se aplicaron las siguientes técnicas de inspección, limpieza y transformación mediante el script `clean_cafe_sales.py`:

| Problema encontrado | Registros afectados | Acción realizada | Justificación |
| :--- | :--- | :--- | :--- |
| **Valores inválidos ('UNKNOWN', 'ERROR') en múltiples columnas** | 3,256 celdas | Se estandarizaron convirtiéndolos a valores nulos reales (`NaN`). | Permite manejar todos los datos faltantes o inválidos de manera uniforme a través de Pandas sin romper operaciones numéricas. |
| **Tipos de datos incorrectos** (todo almacenado como texto) | 10,000 filas | `Quantity`, `Price Per Unit` y `Total Spent` se convirtieron a numéricos. `Transaction Date` se convirtió a tipo fecha. | Requisito indispensable para poder realizar operaciones matemáticas, agregaciones y análisis de series de tiempo. |
| **Valores faltantes en columnas numéricas clave** | 1,398 celdas en total (Total Spent: 462, Qty: 441, Price: 495) | Imputación matemática. Si faltaba un valor pero se tenían los otros dos, se calculó usando: `Total = Quantity * Price`. | Permite recuperar una gran cantidad de datos precisos sin introducir sesgos que ocurrirían si se usara el promedio o mediana general. |
| **Valores faltantes en columnas categóricas** (`Item`, `Payment Method`, `Location`) | 8,108 celdas | Rellenados con la etiqueta estandarizada `'Unknown'`. | Evita perder otras métricas válidas de esa fila (como cuánto se gastó) y mantiene explícito que el dato de origen era desconocido. |
| **Transacciones sin Fecha (`Transaction Date`)** | 460 filas | Se eliminaron los registros (filas) de la base de datos. | En análisis de ventas minoristas, la dimensión temporal es crítica. Las transacciones sin fecha suelen no aportar valor a la mayoría de los análisis agregados. |
| **Filas duplicadas** | 0 filas | Verificación mediante `drop_duplicates()`. | Garantiza que no haya doble conteo en ingresos o volúmenes de ventas (aunque en este set no se encontraron casos). |

### Resultado Final
* **Filas iniciales**: 10,000
* **Filas finales**: 9,540
* **Archivo de salida**: `clean_cafe_sales.csv`

## Fuente de los Datos (Bibliografía)
El dataset original utilizado en este proyecto fue obtenido de Kaggle:
* Ahmed Mohamed. (2023). *Cafe Sales Dirty Data for Cleaning Training*. Kaggle. Disponible en: [https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training](https://www.kaggle.com/datasets/ahmedmohamed2003/cafe-sales-dirty-data-for-cleaning-training)
