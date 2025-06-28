from datos import cliente
from validaciones import formatear_monto
from controlador import (
    registrar_cliente,
    calcular_beneficios,
    transferencia_contactos,
    transferencia_monto,
    transferencia_aprobar,
    deposito,
    avance,
    avance_pago
)

def mostrar_menu():
    registrar_cliente()
    calcular_beneficios()
    while True:
        print("\n--------------------------------")
        print("       Banco Inacapino       ")
        print("--------------------------------")
        print(f"Nro de cuenta: {cliente['cuenta']}")
        print(f"Saldo: {formatear_monto(cliente['saldo'])}   Linea de credito: {formatear_monto(cliente['linea'])}")
        print(f"Tarjeta de credito: {formatear_monto(cliente['tarjeta'])}")
        print("1.- Transferencia")
        print("2.- Deposito")
        print("3.- Avance con tarjeta de credito")
        print("4.- Pago cuota avance")
        print("5.- Salir")
        print("--------------------------------")
        
        opcion = input("Ingrese opcion (1-5): ")
        
        if opcion == '1':
            transferencia_contactos()
            transferencia_monto()
            transferencia_aprobar()
        elif opcion == '2':
            deposito()
        elif opcion == '3':
            avance()
        elif opcion == '4':
            avance_pago()
        elif opcion == '5':
            print("Gracias por usar Banco Inacapino")
            break
        else:
            print("Opcion no valida")


mostrar_menu()