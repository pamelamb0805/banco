def es_vacio(texto):
    return texto.strip() == ""

def valida_run(run):
    run = run.upper().replace(".","").replace("-","")
    if len(run) != 9 or not run[:-1].isdigit():
        return False
    
    cuerpo, dv = run[:-1], run[-1]
    suma = sum(int(d)*((i%6)+2) for i,d in enumerate(cuerpo[::-1]))
    digito = 11 - (suma % 11)
    dv_valido = {10: "K", 11: "0"}.get(digito, str(digito))
    return dv == dv_valido

def limpiar_run(run):
    return run.replace(".","").split("-")[0]

def es_numero(num):
    return num.isdigit() and int(num) > 0

def formatear_monto(monto):
    return f"${monto:,.0f}".replace(",",".")