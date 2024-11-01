#!/usr/bin/env python3

# Programa para convertir un número entero en su descripcion con letra
# Con su valor en $ pesos, como un cheque.  

def unidades(n):
    """
       Funcion que convierte las unidades del 0 (cero) al 9 (nueve)
       a letras.
    """
    unidades = ["cero", "uno", "dos", "tres", "cuatro", "cinco",
               "seis", "siete", "ocho", "nueve"]
    return unidades[n]

def especiales(n):
    """
       Funcion que convierte los números del 10 (diez) al 19(diecinueve)
       a letras.
    """
    especiales = ["diez", "once", "doce", "trece", "catorce",
                  "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve"]
    return especiales[n - 10]

def decenas(n):
    """
       Funcion que convierte las decenas del 20(veinte) al 90(noventa)
       a letras y para los numeros del 21(veintiuno) al 29(veintinueve).
    """
    decenas = ["", "", "veinte", "treinta", "cuarenta", "cincuenta",
               "sesenta", "setenta", "ochenta", "noventa"]
    if n < 10:
        return unidades(n)
    elif 10 <= n < 20:
        return especiales(n)
    elif n == 20:
        return "veinte"
    else:
        dec = decenas[n // 10]
        uni = n % 10
        if uni != 0:
            # Para los números del 21(veintiuno) al 29 (veintinueve).
            if dec == "veinte":
                return f"veinti{unidades(uni)}"
            else:
                return f"{dec} y {unidades(uni)}"
        else:
            return decenas[n // 10]

def centenas_func(n):
    """
       Funcion que convierte las centenas del 100(cien) al 900(novecientos)
       a letras.
    """
    centenas_list = ["", "ciento", "doscientos", "trescientos", "cuatrocientos",
                   "quinientos", "seiscientos", "setecientos", "ochocientos",
                   "novecientos"]
    if n == 0:
        return ""
    elif n == 100:
        return "cien"
    elif n < 100:
        return decenas(n)
    else:
        cent = centenas_list[n // 100]
        resto = n % 100
        if resto != 0:
            return f"{cent} {decenas(resto)}"
        else:
            return cent

def millares_func(n):
    """
       Funcion que regresa n < 1000 a letras.
    """
    if n == 0:
        return ""
    elif n == 100:
        return "cien"
    else:
        return centenas_func(n)

def numero_a_letras(n):
    """Convierte un número entero a letras."""
    if n == 0:
        return "cero pesos"
    else:
        partes = []
        
        # se muestran las cantidades de mil a billones
        secciones = [
            (10**12, "billón", "billones"),
            (10**9, "mil millones", "mil millones"),
            (10**6, "millón", "millones"),
            (10**3, "mil", "mil")
        ]
        
        for divisor, singular, plural in secciones:
            cantidad = n // divisor
            if cantidad > 0:
                if divisor == 10**3:
                    # 'mil' no usa 'un', solo 'mil'
                    if cantidad == 1:
                        partes.append("mil")
                    else:
                        partes.append(f"{millares_func(cantidad)} mil")
                elif divisor >= 10**6:
                    if cantidad == 1:
                        partes.append(f"un {singular}")
                    else:
                        partes.append(f"{millares_func(cantidad)} {plural}")
                n %= divisor
        
        if n > 0:
            partes.append(millares_func(n))
        
        letras = ' '.join(partes)
        return f"{letras} pesos"

def main():
    """Función principal del programa."""
    try:
        numero_input = input("Ingrese la cantidad en numero: ")
        # Eliminar comas y puntos que puedan estar como separadores de miles
        numero = int(numero_input.replace(",", "").replace(".", ""))
        letras = numero_a_letras(numero)
        print(f"El importe en letra es: {letras}")
    except ValueError:
        print("Por favor, ingrese la cantidad correcta.")

if __name__ == "__main__":
    main()
