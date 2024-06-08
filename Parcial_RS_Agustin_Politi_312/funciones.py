import csv
import random
import json

def cargar_archivo(nombre_archivo):
    with open(nombre_archivo, mode='r') as archivo:
        lector_csv = csv.DictReader(archivo)
        datos = [linea for linea in lector_csv]
    print("Archivo cargado con éxito.")
    return datos

def imprimir_lista(datos):
    if len(datos) == 0:
        print("No hay datos para mostrar.")
        return

    for post in datos:
        print(post)

def asignar_estadisticas_post(post):
    post['likes'] = random.randint(500, 3000)
    post['dislikes'] = random.randint(300, 3500)
    post['followers'] = random.randint(10000, 20000)
    return post

def asignar_estadisticas(datos):
    datos = list(map(asignar_estadisticas_post, datos))
    return datos

def filtrar_mejores_posts(datos, nombre_archivo):
    mejores_posts = [post for post in datos if int(post['likes']) > 2000]
    if mejores_posts:
        with open(nombre_archivo, mode='w', newline='') as archivo:
            escritor_csv = csv.DictWriter(archivo, fieldnames=mejores_posts[0].keys())
            escritor_csv.writeheader()
            escritor_csv.writerows(mejores_posts)
        print(f"Archivo {nombre_archivo} generado con éxito.")
    else:
        print("No hay posts con más de 2000 likes.")

def filtrar_haters(datos, nombre_archivo):
    haters_posts = [post for post in datos if int(post['dislikes']) > int(post['likes'])]
    if haters_posts:
        with open(nombre_archivo, mode='w', newline='') as archivo:
            escritor_csv = csv.DictWriter(archivo, fieldnames=haters_posts[0].keys())
            escritor_csv.writeheader()
            escritor_csv.writerows(haters_posts)
        print(f"Archivo {nombre_archivo} generado con éxito.")
    else:
        print("No hay posts con más dislikes que likes.")

def informar_promedio_followers(datos):
    if len(datos) == 0:
        print("No hay datos disponibles para calcular el promedio de followers.")
        return
    
    total_followers = sum(int(post['followers']) for post in datos)
    promedio = total_followers / len(datos)
    print(f"Promedio de followers: {promedio}")

def ordenar_por_usuario(datos, nombre_archivo):
    if len(datos) == 0:
        print("No hay datos disponibles para ordenar.")
        return

    datos_ordenados = sorted(datos, key=lambda x: x['user'])
    with open(nombre_archivo, mode='w') as archivo:
        json.dump(datos_ordenados, archivo, indent=4)
    print(f"Archivo {nombre_archivo} generado con éxito.")

def mostrar_mas_popular(datos):
    if len(datos) == 0:
        print("No hay datos disponibles para mostrar el usuario más popular.")
        return

    max_likes = max(int(post['likes']) for post in datos)
    usuarios_populares = [post['user'] for post in datos if int(post['likes']) == max_likes]
    print(f"Usuario(s) con más likes ({max_likes}): {', '.join(usuarios_populares)}")
