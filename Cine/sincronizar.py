from time import sleep
from update import main
import schedule

def sincronizar(hora_sincronizar):

    print('Actualizando Base de Datos...')
    main()
    print('Base de Datos Actualizada')
    print(f'La Base de Datos sera Actualizada a las {hora_sincronizar}')
    

if __name__ == "__main__":
    
    hora_sincronizar = "05:00"    
    schedule.every().day.at(hora_sincronizar).do(sincronizar,hora_sincronizar)
    print(f'La Base de Datos sera Actualizada a las {hora_sincronizar}')
    while True:   
        schedule.run_pending()     
        sleep(30)


