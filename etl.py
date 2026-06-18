#Maria Maricela Gomez Ortiz
#10/06/2026
#Analisis de calificaciones de Fin de ciclo

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("calificaciones.csv", encoding='cp1252')

materias = [
    "Matemáticas",
    "Español",
    "Historia",
    "Ciencias",
    "Inglés"
]


df["Promedio_Materias"] = df[materias].mean(axis=1)


df["pon_mat"] = df["Promedio_Materias"].apply(
    lambda p: p * 0.60
)
df["pon_tar"] = df["Promedio Tareas"].apply(
    lambda p: p * 0.30
)
df["pon_pun"] = df["Promedio Puntualidad"].apply(
    lambda p: p * 0.05
)
df["pon_asi"] = df["Promedio Asistencia"].apply(
    lambda p: p * 0.05
)

df["Promedio_Materias"] = df["Promedio_Materias"].round(1)
df["pon_mat"] = df["pon_mat"].round(1)
df["pon_tar"] = df["pon_tar"].round(1)
df["pon_pun"] = df["pon_pun"].round(1)
df["pon_asi"] = df["pon_asi"].round(1)


df["cal_final"] = df["pon_mat"] + df["pon_tar"] + df["pon_pun"] + df["pon_asi"]
df["cal_final"] =df["cal_final"].round(1)

df["Estatus"] = df["cal_final"].apply(
    lambda x: "Aprobado" if x >= 6 else "Reprobado"
)


#Archivo de salida

df.to_csv(
    "calificaciones_salida.csv",
    index=False
)


#Analisis

print (f"Promedio Grupal {df["cal_final"].mean()}")
print(f"Promedio Materias ")
print(df[materias].mean())

print(f"{df.loc[df["cal_final"].idxmax()]}")


#Los tres mejores alumnos
top3 = df.groupby("Nombre_Alumno")["cal_final"].sum().sort_values(ascending=False).head(3)

#Alumnos en riesgo de permanenacia o reprobados
riesgo = df[ (df["cal_final"] < 7) | (df["Promedio Asistencia"] < 5)].groupby("Nombre_Alumno")["cal_final"].sum().sort_values(ascending=True).head(3)

print(f"Riesgo {riesgo}")

promedios = df[materias].mean()

#Grafico promedio por materia

plt.figure(figsize=(8,5))
plt.bar(materias, df[materias].mean(),color="deepskyblue")


plt.title("Promedio por Materia")
plt.xlabel("Materias")
plt.ylabel("Calificación Promedio")
plt.ylim(0,10)

plt.savefig("promediomaterias.png", dpi=300, bbox_inches="tight")
plt.show()
#Top 3 mejores alumnos

conte = top3.reset_index()
conte.columns = ["cal_final","Nombre_Alumno"]

plt.figure(figsize=(8,5))
sns.barplot(data = conte, x="cal_final",y="Nombre_Alumno",color="green")
plt.title("Mejores Alumnos")
plt.xlabel("Alumnos")
plt.ylabel("Promedios")
plt.savefig("top3.png", dpi=300, bbox_inches="tight")
plt.show()

#Alumnos en riesgo

conte2 = riesgo.reset_index()
conte2.columns = ["cal_final","Nombre_Alumno"]

plt.figure(figsize=(8,5))
sns.barplot(data = conte2, x="cal_final",y="Nombre_Alumno",color="orange")
plt.title("Alumnos en Riesgo")
plt.xlabel("Alumnos")
plt.ylabel("Promedios")
plt.savefig("riesgo.png", dpi=300, bbox_inches="tight")
plt.show()







