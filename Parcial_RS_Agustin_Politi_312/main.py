import funciones as sna

def mostrar_menu():
    print("1) Cargar archivo CSV")
    print("2) Imprimir lista")
    print("3) Asignar estadísticas")
    print("4) Filtrar por mejores posts")
    print("5) Filtrar por haters")
    print("6) Informar promedio de followers")
    print("7) Ordenar los datos por nombre de user ascendente")
    print("8) Mostrar más popular")
    print("9) Salir")

def main():
    datos = []
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nombre_archivo = input("Ingrese el nombre del archivo CSV: ")
            try:
                datos = sna.cargar_archivo(nombre_archivo)
            except FileNotFoundError:
                print(f"Archivo {nombre_archivo} no encontrado.")
        elif opcion == "2":
            sna.imprimir_lista(datos)
        elif opcion == "3":
            datos = sna.asignar_estadisticas(datos)
        elif opcion == "4":
            nombre_archivo = input("Ingrese el nombre del archivo para guardar los mejores posts: ")
            sna.filtrar_mejores_posts(datos, nombre_archivo)
        elif opcion == "5":
            nombre_archivo = input("Ingrese el nombre del archivo para guardar los posts con más dislikes que likes: ")
            sna.filtrar_haters(datos, nombre_archivo)
        elif opcion == "6":
            sna.informar_promedio_followers(datos)
        elif opcion == "7":
            nombre_archivo = input("Ingrese el nombre del archivo JSON para guardar los datos ordenados: ")
            sna.ordenar_por_usuario(datos, nombre_archivo)
        elif opcion == "8":
            sna.mostrar_mas_popular(datos)
        elif opcion == "9":
            print("Salir")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")

if __name__ == "__main__":
    main()
