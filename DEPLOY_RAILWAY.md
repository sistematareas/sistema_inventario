# 🚀 Guía Completa de Despliegue en Railway

Esta guía te llevará paso a paso para desplegar tu Sistema de Inventario en Railway.

## 📋 Prerequisitos

- Cuenta en [Railway](https://railway.app/) (gratis)
- Base de datos en TiDB Cloud (ya configurada)
- Código del proyecto

---

## 🎯 Arquitectura de Despliegue

Railway desplegará 2 servicios:
1. **Backend** (Flask API) → Servicio Python
2. **Frontend** (React + Vite) → Servicio Node.js

```
┌─────────────────────────────────────────────┐
│           Railway Project                    │
│                                              │
│  ┌──────────────┐      ┌──────────────┐    │
│  │   Backend    │      │   Frontend   │    │
│  │   (Flask)    │◄─────│   (React)    │    │
│  │   Puerto: *  │      │   Puerto: *  │    │
│  └──────┬───────┘      └──────────────┘    │
│         │                                    │
└─────────┼────────────────────────────────────┘
          │
          ▼
   ┌──────────────┐
   │  TiDB Cloud  │ (Base de datos externa)
   └──────────────┘
```

---

## 🔧 PARTE 1: Preparar el Repositorio

### 1.1 Verificar archivos creados ✅

Los siguientes archivos ya fueron creados automáticamente:

**Backend:**
- ✅ `backend/Procfile` - Comando para ejecutar Flask
- ✅ `backend/runtime.txt` - Versión de Python
- ✅ `backend/requirements.txt` - Incluye gunicorn
- ✅ `backend/.env.example` - Ejemplo de variables de entorno

**Frontend:**
- ✅ `frontend/.env.example` - Ejemplo de variables de entorno
- ✅ `frontend/src/services/api.js` - Actualizado para usar variables de entorno

### 1.2 Subir código a GitHub

```bash
# Si no tienes Git inicializado
git init
git add .
git commit -m "Preparar proyecto para Railway"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANTE:** Asegúrate de que `.env` esté en `.gitignore` para no subir credenciales.

---

## 🚂 PARTE 2: Configurar Railway

### 2.1 Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app/) e inicia sesión
2. Click en **"New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Autoriza Railway a acceder a tu cuenta de GitHub
5. Selecciona tu repositorio

### 2.2 Configurar Backend (Flask)

#### A. Crear servicio Backend

1. En tu proyecto de Railway, click **"+ New"**
2. Selecciona **"GitHub Repo"**
3. Selecciona tu repositorio
4. Railway detectará automáticamente que es Python

#### B. Configurar Root Directory

1. En el servicio del Backend, ve a **Settings**
2. En **"Root Directory"**, escribe: `backend`
3. Guarda los cambios

#### C. Agregar Variables de Entorno

1. Ve a la pestaña **"Variables"**
2. Agrega las siguientes variables:

```bash
SECRET_KEY=tu-clave-secreta-super-segura-para-produccion-cambiala
DATABASE_URL=mysql+pymysql://3rfSSP22cK5pJkQ.root:e1lCHXUyPjbUQdZA@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/tienda_inventario
FLASK_ENV=production
```

**💡 TIP:** Genera una SECRET_KEY segura:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### D. Exponer el servicio

1. En **Settings** del servicio Backend
2. En **"Networking"**, click **"Generate Domain"**
3. Copia la URL generada (algo como `https://tu-backend.up.railway.app`)

### 2.3 Configurar Frontend (React)

#### A. Crear servicio Frontend

1. En tu proyecto Railway, click **"+ New"** nuevamente
2. Selecciona **"GitHub Repo"**
3. Selecciona el mismo repositorio
4. Railway detectará Node.js

#### B. Configurar Root Directory

1. En el servicio Frontend, ve a **Settings**
2. En **"Root Directory"**, escribe: `frontend`
3. Guarda los cambios

#### C. Configurar Build y Start Commands

1. Ve a **Settings** → **"Build"**
2. Configura:
   - **Build Command:** `npm run build`
   - **Start Command:** `npm run preview -- --host 0.0.0.0 --port $PORT`

#### D. Agregar Variables de Entorno

1. Ve a la pestaña **"Variables"**
2. Agrega:

```bash
VITE_API_URL=https://tu-backend.up.railway.app
```

**⚠️ IMPORTANTE:** Reemplaza `https://tu-backend.up.railway.app` con la URL real de tu backend que copiaste en el paso 2.2.D

#### E. Exponer el servicio

1. En **Settings** del servicio Frontend
2. En **"Networking"**, click **"Generate Domain"**
3. Copia la URL generada (algo como `https://tu-frontend.up.railway.app`)

---

## 🔐 PARTE 3: Configurar CORS en Backend

Necesitas permitir que el frontend se comunique con el backend:

1. Edita `backend/run.py` en tu repositorio local
2. Actualiza la configuración de CORS:

```python
# Habilitar CORS para permitir peticiones desde React
CORS(app, origins=[
    "http://localhost:5173",  # Desarrollo local
    "https://tu-frontend.up.railway.app",  # Producción Railway
    "https://*.railway.app"  # Cualquier subdominio de Railway
])
```

3. Commit y push:
```bash
git add backend/run.py
git commit -m "Configurar CORS para Railway"
git push
```

Railway redesplegará automáticamente.

---

## ✅ PARTE 4: Verificar Despliegue

### 4.1 Verificar Backend

Abre tu URL del backend y deberías ver:

```json
{
  "message": "Tienda Inventario API",
  "version": "1.0.0",
  "frontend": "http://localhost:5173"
}
```

Prueba los endpoints:
- `https://tu-backend.up.railway.app/api/productos/`
- `https://tu-backend.up.railway.app/api/categorias/`
- `https://tu-backend.up.railway.app/api/proveedores/`

### 4.2 Verificar Frontend

Abre tu URL del frontend y deberías ver la aplicación funcionando.

### 4.3 Verificar Conexión a TiDB

El backend debería conectarse automáticamente a TiDB Cloud. Revisa los logs en Railway:

1. Ve al servicio Backend
2. Pestaña **"Deployments"**
3. Click en el último deployment
4. Revisa los **logs** para ver si hay errores de conexión

---

## 🐛 Solución de Problemas

### Error: "Cannot connect to database"

**Solución:**
- Verifica que la `DATABASE_URL` sea correcta
- Asegúrate de que TiDB Cloud permita conexiones desde Railway
- En TiDB Cloud, ve a **"Security Settings"** y agrega `0.0.0.0/0` a los IPs permitidos

### Error: "CORS policy blocked"

**Solución:**
- Verifica que agregaste la URL del frontend en CORS (Parte 3)
- El backend debe estar corriendo antes de probar el frontend

### Error: "Failed to fetch API"

**Solución:**
- Verifica que la variable `VITE_API_URL` en el frontend tenga la URL correcta del backend
- Asegúrate de que el backend esté funcionando y accesible

### El frontend no se actualiza

**Solución:**
- Las variables de entorno de Vite se incluyen en el **build time**, no en runtime
- Después de cambiar `VITE_API_URL`, debes redesplegar el frontend
- En Railway: Ve al servicio → **Deployments** → **"Redeploy"**

---

## 📊 Monitoreo

### Ver Logs en Tiempo Real

1. En Railway, selecciona un servicio (Backend o Frontend)
2. Ve a la pestaña **"Deployments"**
3. Click en el deployment activo
4. Los logs aparecerán en tiempo real

### Métricas

Railway te muestra:
- CPU usage
- Memory usage
- Network traffic
- Request count

---

## 💰 Costos

Railway ofrece:
- **Tier Gratuito:** $5 USD de crédito mensual (suficiente para proyectos pequeños)
- **Tier Hobby:** $5 USD/mes por servicio después del crédito gratuito

**Estimación para este proyecto:**
- Backend (Flask): ~$5-10 USD/mes
- Frontend (Static): ~$0-5 USD/mes
- **Total:** $5-15 USD/mes

---

## 🎉 ¡Listo!

Tu sistema de inventario ahora está desplegado en Railway con:

✅ Backend Flask corriendo con Gunicorn
✅ Frontend React optimizado con Vite
✅ Base de datos TiDB Cloud conectada
✅ Variables de entorno configuradas
✅ CORS habilitado
✅ SSL automático (HTTPS)

**URLs finales:**
- Frontend: `https://tu-frontend.up.railway.app`
- Backend: `https://tu-backend.up.railway.app`

---

## 📝 Notas Adicionales

### Actualizar la Aplicación

Cada vez que hagas `git push`, Railway redesplegará automáticamente (CI/CD).

### Dominios Personalizados

Puedes agregar tu propio dominio:
1. Ve a **Settings** → **Networking**
2. Click en **"Custom Domain"**
3. Sigue las instrucciones para configurar tu DNS

### Base de Datos

TiDB Cloud está fuera de Railway, lo cual es **IDEAL** porque:
- Los datos persisten independientemente del despliegue
- Puedes escalar la BD independientemente
- Backups y seguridad gestionados por TiDB

---

## 🆘 Soporte

Si tienes problemas:
1. Revisa los logs en Railway
2. Verifica las variables de entorno
3. Asegúrate de que TiDB Cloud permite conexiones externas
4. Consulta la [documentación de Railway](https://docs.railway.app/)

---

**¡Éxito con tu despliegue! 🚀**
