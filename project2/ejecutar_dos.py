import threading
import requests
import time

URL = "http://localhost:8000/api/proyectos/"


TOKEN_AUTH0 = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBoWEhWaFFwd1BKUm5UWnBSdlQwRCJ9.eyJpc3MiOiJodHRwczovL2Rldi1sM3RuNnUxdTJ1ZmNpMDNsLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJHR04ySDQ5REV4QzR1RnNyMVh1d0RrZkxlaHNFMnFtckBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9hcGkuYml0ZWNvLmNvbSIsImlhdCI6MTc4MDAyMTAxNSwiZXhwIjoxNzgwMTA3NDE1LCJzY29wZSI6InJlYWQ6cmVwb3J0ZXMgd3JpdGU6cmVwb3J0ZXMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMiLCJhenAiOiJHR04ySDQ5REV4QzR1RnNyMVh1d0RrZkxlaHNFMnFtciIsInBlcm1pc3Npb25zIjpbInJlYWQ6cmVwb3J0ZXMiLCJ3cml0ZTpyZXBvcnRlcyJdfQ.KP-A72DdYCJ5MItDsAi8XfVhwFQuDXjJq-5bpJ_evs_9zosnv43KO7H_CUwuY24X-T3jkihE01yab8wH27NK0wwq10pAE5lcvF68QPofkwHo-qo4G9_9cW9P0BQzZ1ERn5qbA2UUtotscdLDwhjHH8_gkEgyHgG10LrGVsWgPoxVf7cQ2IAlAkjE49aPR6LPWKfNqnstKZbN76YWSc192sW1GnpIt0XBvdLttQSm5ELxOsttTfAYX-_woc-Zgt8ZGMv-C5hJq1X-UUyhmTAlrZbKRTR35haKcSgwxYxsMF4HaX_88wfBGgF7UWg_PGyDuusZa1YuX39S1H8Ccs1JZA"

def atacar():
    print("⚔️ Atacante DoS iniciado...")
    count_401 = 0
    count_429 = 0
    
    # El atacante inunda el servidor sin mandar ningún token
    for _ in range(100):
        try:
            r = requests.get(URL)
            if r.status_code == 429:
                count_429 += 1
            elif r.status_code == 401:
                count_401 += 1
        except:
            pass
            
    print(f"\n--- RESUMEN DEL ATAQUE ---")
    print(f"❌ Peticiones que llegaron a Django sin token (401): {count_401}")
    print(f"🛡️ Peticiones bloqueadas por Kong (429): {count_429}")

def usuario_legitimo():
    # Esperamos 1 segundo para asegurarnos de que el ataque ya empezó
    time.sleep(1) 
    print("\n😇 Usuario legítimo intentando acceder...")
    
    # -------------------------------------------------------------
    # AQUÍ PONEMOS LOS ENCABEZADOS (HEADERS)
    # 1. Authorization: Manda el token de Auth0
    # 2. X-Forwarded-For: Finge ser otra IP para que Kong no lo asocie al ataque
    # -------------------------------------------------------------
    headers_bueno = {
        "Authorization": f"Bearer {TOKEN_AUTH0}",
        "X-Forwarded-For": "192.168.1.50" 
    }
    
    try:
        r = requests.get(URL, headers=headers_bueno)
        print(f"💎 Código HTTP del usuario legítimo: {r.status_code}")
        
        if r.status_code == 200:
            print("✅ ¡ÉXITO TOTAL! El usuario entró y Kong detuvo al atacante en paralelo.")
        elif r.status_code == 401:
            print("⚠️ Kong lo dejó pasar, pero Django lo rechazó porque el TOKEN_AUTH0 no es válido.")
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    # Creamos dos caminos paralelos para que ocurran a la vez
    hilo_ataque = threading.Thread(target=atacar)
    hilo_usuario = threading.Thread(target=usuario_legitimo)
    
    # Los iniciamos al mismo tiempo
    hilo_ataque.start()
    hilo_usuario.start()
    
    # Esperamos a que terminen para salir
    hilo_ataque.join()
    hilo_usuario.join()