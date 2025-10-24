# Instalación de RockMongo en Debian 13

## 🧠 ¿Qué es RockMongo?
RockMongo es una herramienta web escrita en PHP para administrar bases de datos MongoDB (similar a phpMyAdmin, pero para MongoDB).  
Permite ver colecciones, documentos, ejecutar consultas y gestionar usuarios desde el navegador.

---

## ⚙️ Requisitos previos

Antes de instalar RockMongo, necesitas tener tres cosas:

1. **Un servidor web con PHP**  
   Puede ser Apache o Nginx, junto con PHP (versión 5.x o superior, aunque en Debian 13 tendrás PHP 8.x).  

   ```bash
   sudo apt update
   sudo apt install apache2 php php-cli php-mongodb unzip -y
   ```

2. **El driver de PHP para MongoDB**  
   El paquete `php-mongodb` que instalamos arriba ya incluye el driver necesario.

3. **MongoDB instalado y funcionando**  
   Si aún no lo tienes:
   ```bash
   sudo apt install -y mongodb
   sudo systemctl enable --now mongodb
   ```

   Comprueba que funciona:
   ```bash
   mongo --eval 'db.runCommand({ connectionStatus: 1 })'
   ```

---

## 🧩 Instalación de RockMongo

1. **Descargar el paquete desde GitHub**

   ```bash
   cd /var/www/html
   sudo git clone https://github.com/iwind/rockmongo.git
   sudo mv rockmongo /var/www/html/rockmongo
   ```

   *(Si no tienes `git`, instala con `sudo apt install git -y`)*

   Alternativamente, puedes descargar el ZIP:
   ```bash
   wget https://github.com/iwind/rockmongo/archive/refs/heads/master.zip
   unzip master.zip
   mv rockmongo-master /var/www/html/rockmongo
   ```

2. **Configurar permisos**
   ```bash
   sudo chown -R www-data:www-data /var/www/html/rockmongo
   sudo chmod -R 755 /var/www/html/rockmongo
   ```

3. **Configurar RockMongo**
   Abre el archivo de configuración:
   ```bash
   sudo nano /var/www/html/rockmongo/config.php
   ```

   Dentro verás algo como:
   ```php
   $MONGO["servers"][$i]["host"] = "localhost";
   $MONGO["servers"][$i]["port"] = "27017";
   $MONGO["servers"][$i]["mongo_auth"] = false;
   $MONGO["servers"][$i]["control_users"]["admin"] = "admin";
   ```

   Puedes cambiar los valores según tu entorno:
   - **host**: IP o nombre del servidor MongoDB  
   - **port**: puerto (por defecto 27017)  
   - **control_users**: usuario y contraseña para entrar en RockMongo  

   Por defecto, usuario y contraseña son `admin` / `admin`.

4. **Probar la instalación**

   Abre en tu navegador:
   ```
   http://localhost/rockmongo/index.php
   ```

   Verás la página de inicio de sesión de RockMongo.

   🔑 Ingresa con:
   ```
   Usuario: admin
   Contraseña: admin
   ```

5. **¡Listo!**
   Ya puedes gestionar tus bases de datos MongoDB desde la interfaz web.

---

## 🔄 Actualización desde una versión anterior

Si ya tenías RockMongo instalado:
1. Copia todos los archivos nuevos **excepto `config.php`** a tu carpeta vieja.
   ```bash
   cp -r rockmongo/* /var/www/html/rockmongo/
   ```
2. ¡Listo! No necesitas más pasos.

---

## 🧩 Notas adicionales

- El proyecto ya no se actualiza frecuentemente, así que puede tener compatibilidad limitada con versiones recientes de PHP o MongoDB.
- Si tienes problemas con PHP 8, puedes probar `php7.4-fpm` en lugar de PHP 8.x.
- También existen alternativas modernas, como **Mongo Express** (Node.js) o **NoSQLBooster** (desktop).

---

¿Quieres que te escriba un script automático de instalación (un `.sh` que haga todo por ti en Debian 13)?  
Puedo generarlo listo para ejecutar.
