import pandas as pd
import numpy as np

def clean_cafe_data(input_path, output_path):
    print("--- INICIANDO LIMPIEZA DE DATOS ---")
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    
    # 1. Estandarizar valores nulos o inválidos ('UNKNOWN', 'ERROR') a NaN
    # Contamos cuántos valores 'UNKNOWN' o 'ERROR' hay en toda la base antes de reemplazar
    invalid_mask = df.isin(['UNKNOWN', 'ERROR'])
    invalid_count = invalid_mask.sum().sum()
    df.replace(['UNKNOWN', 'ERROR'], np.nan, inplace=True)
    print(f"[1] Valores 'UNKNOWN'/'ERROR' convertidos a nulos: {invalid_count} celdas afectadas.")
    
    # 2. Corregir tipos de datos
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    df['Price Per Unit'] = pd.to_numeric(df['Price Per Unit'], errors='coerce')
    df['Total Spent'] = pd.to_numeric(df['Total Spent'], errors='coerce')
    df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')
    print("[2] Tipos de datos corregidos (Numéricos y Fechas).")

    # 3. Imputar valores faltantes usando la lógica matemática (Total = Cantidad * Precio)
    # Recuperar Total Spent
    mask_total = df['Total Spent'].isna() & df['Quantity'].notna() & df['Price Per Unit'].notna()
    df.loc[mask_total, 'Total Spent'] = df.loc[mask_total, 'Quantity'] * df.loc[mask_total, 'Price Per Unit']
    reco_total = mask_total.sum()
    
    # Recuperar Quantity
    mask_qty = df['Quantity'].isna() & df['Total Spent'].notna() & df['Price Per Unit'].notna()
    df.loc[mask_qty, 'Quantity'] = df.loc[mask_qty, 'Total Spent'] / df.loc[mask_qty, 'Price Per Unit']
    reco_qty = mask_qty.sum()
    
    # Recuperar Price Per Unit
    mask_price = df['Price Per Unit'].isna() & df['Total Spent'].notna() & df['Quantity'].notna()
    df.loc[mask_price, 'Price Per Unit'] = df.loc[mask_price, 'Total Spent'] / df.loc[mask_price, 'Quantity']
    reco_price = mask_price.sum()
    
    print(f"[3] Registros recuperados matemáticamente: Total Spent ({reco_total}), Quantity ({reco_qty}), Price ({reco_price}).")

    # 4. Rellenar valores categóricos nulos con 'Unknown' (o 'Desconocido')
    cat_cols = ['Item', 'Payment Method', 'Location']
    missing_cat_before = df[cat_cols].isna().sum().sum()
    for col in cat_cols:
        df[col] = df[col].fillna('Unknown')
    print(f"[4] Valores categóricos faltantes rellenados con 'Unknown': {missing_cat_before} celdas afectadas.")

    # 5. Eliminar filas donde no hay fecha de transacción, ya que es crítica
    missing_date = df['Transaction Date'].isna().sum()
    df.dropna(subset=['Transaction Date'], inplace=True)
    print(f"[5] Filas eliminadas por falta de fecha de transacción (No recuperables): {missing_date} filas afectadas.")
    
    # 6. Eliminar duplicados
    duplicates = df.duplicated().sum()
    df.drop_duplicates(inplace=True)
    print(f"[6] Filas duplicadas eliminadas: {duplicates} filas afectadas.")

    # Exportar los datos
    df.to_csv(output_path, index=False)
    final_rows = len(df)
    print(f"\n--- RESUMEN ---")
    print(f"Filas iniciales: {initial_rows}")
    print(f"Filas finales: {final_rows}")
    print(f"Datos limpios exportados exitosamente a: {output_path}")

if __name__ == '__main__':
    clean_cafe_data('dirty_cafe_sales.csv', 'clean_cafe_sales.csv')
