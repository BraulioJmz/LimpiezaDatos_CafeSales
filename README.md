# Cafe Sales Data Cleaning

Este repositorio contiene el código y los procesos utilizados para limpiar la base de datos de ventas de café. 

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
