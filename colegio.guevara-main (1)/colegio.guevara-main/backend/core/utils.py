import pandas as pd
from django.db import connection
from django.core.cache import cache

def obtener_datos(alumno_id=7, anio_calendario=2025):
    cache_key = f"datos_alumno_{alumno_id}_{anio_calendario}"
    df = cache.get(cache_key)

    if df is None:
        query = """
            SELECT 
                cc.anio_calendario, cc.curso, cc.anio, cc.asistencia, 
                cc.faltas_injustificadas, cc.faltas_justificadas,
                cu.first_name, cu.last_name,
                cm.nombre,
                cn.cuatrimestre_1_informe_1, cn.cuatrimestre_1_informe_2, cn.cuatrimestre_1_nota, 
                cn.cuatrimestre_2_informe_1, cn.cuatrimestre_2_informe_2, cn.cuatrimestre_2_nota,
                cn.nota_final 
            FROM core_nota cn
            INNER JOIN core_cursada cc ON cn.alumno_id = cc.alumno_id
            INNER JOIN core_usuario cu ON cn.alumno_id = cu.id 
            INNER JOIN core_materia cm ON cm.id = cn.materia_id AND cm.anio = cn.anio
            WHERE cc.alumno_id = %s AND cc.anio_calendario = %s;
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [alumno_id, anio_calendario])
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()

        df = pd.DataFrame(data, columns=columns)

        # Guardar en caché
        cache.set(cache_key, df, timeout=3600)

    return df






import matplotlib
matplotlib.use("Agg")  # Usa un backend sin GUI antes de importar pyplot
import matplotlib.pyplot as plt

import os
import math

def generar_grafico_evolucion(df):
    if df.empty:
        print("No hay datos disponibles para este alumno.")
        return None

    colegio = "Colegio Dr. Guevara"
    estudiante = f"Apellido y Nombres: {df.iloc[0]['last_name']} {df.iloc[0]['first_name']}"
    anio_escolar = f"Año: {df.iloc[0]['anio_calendario']}"
    grado = f"Grado: {df.iloc[0]['curso']}"
    faltas_justificadas = df.iloc[0]['faltas_justificadas']
    faltas_injustificadas = df.iloc[0]['faltas_injustificadas']
    
    num_materias = len(df)
    num_cols = 3
    num_rows = math.ceil(num_materias / num_cols)

    fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols, linewidth=2.5, figsize=(15, num_rows * 3), sharex=False, sharey=False)
    axes = axes.flatten()  # Convertir la matriz de ejes en una lista
    

    fig.suptitle(f"{colegio} - {estudiante} - {anio_escolar} - {grado}", fontsize=14, fontweight='bold', y=1.02)

    x_labels = ["C1 Inf1", "C1 Inf2", "C1 Nota", "C2 Inf1", "C2 Inf2", "C2 Nota", 'Nota']
   

    for index, row in df.iterrows():
        notas = [
            row["cuatrimestre_1_informe_1"], row["cuatrimestre_1_informe_2"], row["cuatrimestre_1_nota"],
            row["cuatrimestre_2_informe_1"], row["cuatrimestre_2_informe_2"], row["cuatrimestre_2_nota"],
            row["nota_final"]
        ]

        # Determinar color: rojo si alguna nota es menor a 4, verde si todas son 4 o más
        color = 'red' if any(nota < 4 for nota in notas if nota is not None) else 'green'

        ax = axes[index]
        ax.plot(x_labels, notas, marker='o', linestyle='-', color=color, label=row["nombre"])
        ax.set_title(row["nombre"],  color=color, fontsize=8, fontweight='bold')
        ax.set_ylabel("Nota")
        ax.set_ylim(0, 10)
        ax.set_yticks(range(1, 11))
        ax.legend(fontsize=8)
        ax.set_xticks(range(len(x_labels)))
        ax.set_xticklabels(x_labels, rotation=0, fontsize=8, fontweight='bold')

        ax.grid(True)

        

    for i in range(index + 1, len(axes)):
        fig.delaxes(axes[i])

    fig.text(0.5, -0.02, f"Faltas Justificadas: {faltas_justificadas} | Faltas Injustificadas: {faltas_injustificadas}", 
             ha='center', fontsize=12, fontweight='bold')

    plt.xlabel("Evaluaciones")
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    output_path = os.path.join("media", "grafico_evolucion_final.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    return output_path
