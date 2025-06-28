from datos import cliente,contactos
from validaciones import es_numero,formatear_monto

def registrar_cliente():
    while True:
        cliente["nombre"] = input("Ingrese su Nombre: ")
        if cliente["nombre"].isalpha():
            break
        print("Nombre inválido. Solo letras.")

    while True:
        cliente["apellido"] = input("Ingrese su Apellido: ")
        if cliente["apellido"].isalpha():
            break
        print("Apellido inválido. Solo letras.")

    while True:
        run = input("Ingrese RUN (XX.XXX.XXX-X): ")
        if len(run) == 12 and run.count('.') == 2 and run.count('-') == 1:
            cliente["run"] = run
            cliente["cuenta"] = run.replace('.','').replace('-','')[:-1]
            break
        print("RUN inválido. Formato: XX.XXX.XXX-X")

def calcular_beneficios():
    while True:
        try:
            deposito = int(input("Monto depósito inicial: $"))
            if deposito <= 100000:
                cliente.update({
                    "saldo": deposito,
                    "linea": 50000,
                    "tarjeta": 80000
                })
            elif deposito <= 500000:
                cliente.update({
                    "saldo": deposito,
                    "linea": 250000,
                    "tarjeta": 300000
                })
            else:
                cliente.update({
                    "saldo": deposito,
                    "linea": 500000,
                    "tarjeta": 700000
                })
            break
        except:
            print("Monto inválido. Solo números.")

# FUNCIONES DE TRANSFERENCIA
def transferencia_contactos():
    print("\n--------------------------------")
    print("       Banco Inacapino       ")
    print("--------------------------------")
    print(f"Nro cuenta: {cliente['cuenta']}")
    print(f"Saldo: ${cliente['saldo']}   Línea: ${cliente['linea']}")
    print("--------------------------------")
    print("Transferir a:")
    print(f"1. {contactos[1]['Nombre']} - Cuenta: {contactos[1]['Cuenta']}")
    print(f"2. {contactos[2]['Nombre']} - Cuenta: {contactos[2]['Cuenta']}")

def transferencia_monto():
    while True:
        try:
            opcion = int(input("Seleccione contacto (1-2): "))
            if opcion in [1, 2]:
                contacto = contactos[opcion]
                max_trans = cliente['saldo'] + cliente['linea']
                
                print(f"\nCuenta destino: {contacto['Cuenta']}")
                print(f"Monto máximo: ${max_trans}")
                
                monto = int(input("Monto a transferir: $"))
                if 0 < monto <= max_trans:
                    cliente['monto_transferir'] = monto
                    cliente['contacto_selec'] = opcion
                    return
                print("Monto inválido.")
        except:
            print("Opción inválida.")

def transferencia_aprobar():
    print("\n--------------------------------")
    print("   Confirmar Transferencia    ")
    print("--------------------------------")
    contacto = contactos[cliente['contacto_selec']]
    print(f"Destino: {contacto['Nombre']}")
    print(f"Cuenta: {contacto['Cuenta']}")
    print(f"Monto: ${cliente['monto_transferir']}")
    
    if input("Confirmar? (S/N): ").upper() == 'S':
        if cliente['saldo'] >= cliente['monto_transferir']:
            cliente['saldo'] -= cliente['monto_transferir']
        else:
            diferencia = cliente['monto_transferir'] - cliente['saldo']
            cliente['linea'] -= diferencia
            cliente['saldo'] = 0
        print("Transferencia exitosa!")
    else:
        print("Transferencia cancelada.")

def avance():
    print("\n--------------------------------")
    print("    AVANCE CON TARJETA DE CRÉDITO    ")
    print("--------------------------------")
    print(f"Límite disponible: {formatear_monto(cliente['tarjeta'])}")
    
    while True:
        try:
            monto = int(input("Ingrese monto a avanzar: $"))
            if monto <= 0:
                print("El monto debe ser mayor a cero")
            elif monto > cliente['tarjeta']:
                print("No puede exceder el límite de su tarjeta")
            else:
                cliente['avance'] = monto
                break
        except ValueError:
            print("Error: Ingrese un monto válido")
    
    while True:
        try:
            cuotas = int(input("Ingrese número de cuotas (12, 24, 36, 48): "))
            if cuotas in [12, 24, 36, 48]:
                cliente['cuotas'] = cuotas
                cliente['cuota_actual'] = 1  # Inicializar contador
                
                # Asignar tasa de interés según cuotas
                if cuotas == 12:
                    cliente['interes'] = 0.015
                elif cuotas == 24:
                    cliente['interes'] = 0.03
                elif cuotas == 36:
                    cliente['interes'] = 0.04
                else:
                    cliente['interes'] = 0.05
                
                cliente['saldo'] += monto
                print("\n¡Avance aprobado!")
                print(f"Interés aplicado: {cliente['interes']*100}% mensual")
                break
            else:
                print("Error: Debe seleccionar 12, 24, 36 ó 48 cuotas")
        except ValueError:
            print("Error: Ingrese un número válido")

def avance_pago():
    # Verificar si hay avances activos
    if cliente['cuotas'] == 0 or cliente['avance'] == 0:
        print("\n--- NO TIENE AVANCES PENDIENTES ---")
        return
    
    # Calcular valor de la cuota
    interes_mensual = cliente['interes']
    cuotas_totales = cliente['cuotas']
    cuota_actual = cliente['cuota_actual']
    
    valor_cuota = (cliente['avance'] * interes_mensual * (1 + interes_mensual)**cuotas_totales) / ((1 + interes_mensual)**cuotas_totales - 1)
    
    print("\n--------------------------------")
    print("      PAGO DE CUOTA AVANCE      ")
    print("--------------------------------")
    print(f"Cuota {cuota_actual}/{cuotas_totales}")
    print(f"Monto original: {formatear_monto(cliente['avance'])}")
    print(f"Interés mensual: {interes_mensual*100}%")
    print(f"Valor cuota: {formatear_monto(valor_cuota)}")
    print(f"Saldo disponible: {formatear_monto(cliente['saldo'])}")
    print("--------------------------------")
    
    if input("¿Desea pagar esta cuota? (S/N): ").upper() == 'S':
        if cliente['saldo'] >= valor_cuota:
            cliente['saldo'] -= valor_cuota
            cliente['cuota_actual'] += 1
            cliente['abonado'] += valor_cuota
            print("\n¡Pago realizado con éxito!")
            
            # Verificar si completó todas las cuotas
            if cliente['cuota_actual'] > cliente['cuotas']:
                print("\n¡FELICITACIONES! Ha completado todos los pagos.")
                cliente['avance'] = 0
                cliente['cuotas'] = 0
        else:
            print("\nError: Saldo insuficiente para realizar el pago")
    else:
        print("\nPago cancelado")

def deposito():
    print("\n--------------------------------")
    print("       DEPÓSITO       ")
    print("--------------------------------")
    print(f"Saldo actual: {formatear_monto(cliente['saldo'])}")
    print(f"Deuda en línea: {formatear_monto(cliente['deuda'])}")
    print(f"Línea disponible: {formatear_monto(cliente['linea'])}")
    print("--------------------------------")
    
    while True:
        try:
            monto = int(input("Ingrese monto a depositar: $"))
            if monto <= 0:
                print("El monto debe ser mayor a cero")
                continue
                
            # Primero pagar deuda si existe
            if cliente['deuda'] > 0:
                if monto >= cliente['deuda']:
                    print(f"Pagando deuda de {formatear_monto(cliente['deuda'])}...")
                    monto -= cliente['deuda']
                    cliente['linea'] += cliente['deuda']
                    cliente['deuda'] = 0
                else:
                    print(f"Abonando {formatear_monto(monto)} a deuda...")
                    cliente['deuda'] -= monto
                    cliente['linea'] += monto
                    monto = 0
            
            # Acreditar saldo restante
            if monto > 0:
                cliente['saldo'] += monto
            
            print("\nOperación realizada con éxito")
            print(f"Nuevo saldo: {formatear_monto(cliente['saldo'])}")
            print(f"Línea disponible: {formatear_monto(cliente['linea'])}")
            break
            
        except ValueError:
            print("Error: Ingrese un monto válido (solo números)")