#!/usr/bin/env python3
"""
Script de verificación pre-despliegue para Railway
Ejecuta este script antes de desplegar para verificar que todo está configurado correctamente
"""

import os
import sys
from pathlib import Path

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def check(condition, message, error_msg=""):
    """Verifica una condición y muestra el resultado"""
    if condition:
        print(f"{GREEN}✓{RESET} {message}")
        return True
    else:
        print(f"{RED}✗{RESET} {message}")
        if error_msg:
            print(f"  {YELLOW}→{RESET} {error_msg}")
        return False

def main():
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}🔍 Verificación Pre-Despliegue para Railway{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    all_good = True
    
    # Verificar estructura del proyecto
    print(f"{YELLOW}📁 Estructura del Proyecto{RESET}")
    all_good &= check(
        Path("backend").exists(),
        "Carpeta backend existe"
    )
    all_good &= check(
        Path("frontend").exists(),
        "Carpeta frontend existe"
    )
    
    # Verificar archivos del backend
    print(f"\n{YELLOW}🐍 Backend (Flask){RESET}")
    all_good &= check(
        Path("backend/requirements.txt").exists(),
        "requirements.txt existe",
        "Necesario para instalar dependencias"
    )
    all_good &= check(
        Path("backend/Procfile").exists(),
        "Procfile existe",
        "Necesario para Railway sepa cómo ejecutar el servidor"
    )
    all_good &= check(
        Path("backend/runtime.txt").exists(),
        "runtime.txt existe",
        "Especifica la versión de Python"
    )
    all_good &= check(
        Path("backend/run.py").exists(),
        "run.py existe",
        "Punto de entrada de la aplicación"
    )
    
    # Verificar contenido de requirements.txt
    if Path("backend/requirements.txt").exists():
        with open("backend/requirements.txt", "r", encoding="utf-8") as f:
            requirements = f.read()
            all_good &= check(
                "gunicorn" in requirements,
                "gunicorn está en requirements.txt",
                "Necesario para servidor de producción"
            )
    
    # Verificar archivos del frontend
    print(f"\n{YELLOW}⚛️ Frontend (React){RESET}")
    all_good &= check(
        Path("frontend/package.json").exists(),
        "package.json existe",
        "Necesario para instalar dependencias de Node"
    )
    all_good &= check(
        Path("frontend/vite.config.js").exists(),
        "vite.config.js existe",
        "Configuración de Vite"
    )
    all_good &= check(
        Path("frontend/src/services/api.js").exists(),
        "api.js existe",
        "Servicio de API del frontend"
    )
    
    # Verificar que api.js usa variables de entorno
    if Path("frontend/src/services/api.js").exists():
        with open("frontend/src/services/api.js", "r", encoding="utf-8") as f:
            api_content = f.read()
            all_good &= check(
                "import.meta.env.VITE_API_URL" in api_content,
                "api.js usa variables de entorno",
                "Necesario para configurar URL del backend en Railway"
            )
    
    # Verificar .gitignore
    print(f"\n{YELLOW}🔒 Seguridad{RESET}")
    if Path(".gitignore").exists():
        with open(".gitignore", "r", encoding="utf-8") as f:
            gitignore = f.read()
            all_good &= check(
                ".env" in gitignore,
                ".env está en .gitignore",
                "Evita subir credenciales a Git"
            )
    else:
        all_good &= check(
            False,
            ".gitignore existe",
            "Necesario para no subir archivos sensibles"
        )
    
    # Verificar ejemplos de variables de entorno
    print(f"\n{YELLOW}⚙️ Variables de Entorno{RESET}")
    all_good &= check(
        Path("backend/.env.example").exists(),
        "backend/.env.example existe",
        "Template de variables para Railway"
    )
    all_good &= check(
        Path("frontend/.env.example").exists(),
        "frontend/.env.example existe",
        "Template de variables para Railway"
    )
    
    # Verificar documentación
    print(f"\n{YELLOW}📚 Documentación{RESET}")
    all_good &= check(
        Path("DEPLOY_RAILWAY.md").exists(),
        "DEPLOY_RAILWAY.md existe",
        "Guía completa de despliegue"
    )
    all_good &= check(
        Path("RAILWAY_CHECKLIST.md").exists(),
        "RAILWAY_CHECKLIST.md existe",
        "Checklist rápido"
    )
    
    # Resultado final
    print(f"\n{BLUE}{'='*60}{RESET}")
    if all_good:
        print(f"{GREEN}✅ ¡Todo listo para desplegar en Railway!{RESET}")
        print(f"\n{YELLOW}Próximos pasos:{RESET}")
        print(f"  1. Lee {BLUE}RAILWAY_CHECKLIST.md{RESET} para pasos rápidos")
        print(f"  2. Lee {BLUE}DEPLOY_RAILWAY.md{RESET} para guía detallada")
        print(f"  3. Asegúrate de hacer commit y push a GitHub")
        print(f"  4. Ve a railway.app y despliega\n")
        return 0
    else:
        print(f"{RED}❌ Hay problemas que resolver antes de desplegar{RESET}")
        print(f"\n{YELLOW}Revisa los errores arriba y corrígelos{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
