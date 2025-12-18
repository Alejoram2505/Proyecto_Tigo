# 📊 Proyecto Tigo – Sistema de Gestión de SR / OT

Sistema web desarrollado en **Django** para la **gestión, seguimiento y análisis de SR / OT**, con control de usuarios, carga de backlog, segmentación comercial y visualización de KPIs de rendimiento.

---

## 🧩 Funcionalidad General

La aplicación permite:

- 📥 Cargar backlog de SR / OT desde archivos Excel
- 👥 Administrar usuarios y roles
- 🧾 Consultar SR / OT con filtros y búsqueda
- ✏️ Editar información de las SR
- 💬 Agregar y gestionar comentarios por SR
- 📊 Visualizar gráficas de rendimiento (KPIs)
- 📤 Exportar KPIs a Excel
- 🧠 Calcular métricas automáticas como MTTI y días de cola

---

## 👤 Roles de Usuario

La app maneja **roles con permisos diferenciados**:

### 🔹 Administrador (`admin`)
- Acceso total a la aplicación
- Subir backlog
- Subir clientes y segmentos
- Crear y administrar usuarios
- Editar cualquier SR
- Ver y exportar KPIs

### 🔹 Ingeniero (`ing`)
- Ver SR
- Editar SR
- Ver gráficas de rendimiento
- Subir backlog
- Subir clientes

### 🔹 Cliente (`cliente`)
- Acceso de solo lectura
- Puede ver SR asignadas
- No puede editar ni acceder a gráficas

---

## 🏠 Home

Pantalla principal con accesos rápidos a:

- Subir backlog
- Ver SR
- Gráficas de rendimiento
- Agregar usuario (solo administrador)
- Subir clientes / segmentos
- Ver clientes

Diseño tipo **panel administrativo**, pensado para uso interno.

---

## 📥 Subir Backlog

Permite cargar un archivo Excel con SR / OT.

### Al cargar el archivo:
- Se crean o actualizan SR automáticamente
- Se normalizan nombres de clientes
- Se asignan familias
- Se calculan métricas iniciales

El proceso es **idempotente**, evitando duplicados.

---

## 🧑‍💼 Subir Clientes / Segmentos

Pantalla dedicada para cargar información de clientes:

- Nombre del cliente
- Segmento comercial  
  (`SMALL`, `LARGE`, `ENTERPRISE`, `GOVERNMENT`, `WHOLESALE`, `MNC`)

Esta información se utiliza para:
- Clasificar SR
- Alimentar las gráficas de rendimiento

---

## 📄 Ver SR

Vista en forma de tabla con:

- Buscador
- Filtros
- Paginación
- Estados visuales
- Acceso al detalle de cada SR

---

## 🔍 Detalle SR

Muestra toda la información de una SR:

- Cliente
- Segmento
- Familia
- Producto
- Estado
- Fechas
- Días de cola (con colores)
- SR relacionadas por SOL

### 💬 Comentarios
- Usuarios autorizados pueden comentar
- **Solo el autor del comentario puede eliminarlo**
- Comentarios ordenados por fecha

---

## ✏️ Editar SR

Pantalla basada visualmente en **Detalle SR**, con campos editables:

- Estado (`abierto`, `cerrado`, `pospuesto`, `cancelado`)
- Ingeniero encargado
- Segmento
- Familia
- Enlace
- Fechas (solo administrador)

Las métricas se recalculan automáticamente al guardar.

---

## 📊 Gráficas de Rendimiento

Pantalla dedicada con filtros de fecha.

### Incluye:
- OTs cerradas por familia
- MTTI promedio por familia
- OTs cerradas por segmento
- MTTI promedio por segmento
- Evolución de cierres en el tiempo
- Histogramas MTTI por familia
- Atención por segmento comercial (SR vs MTTI)

### Características:
- Filtro por rango de fechas
- Solo considera SR cerradas
- Colores corporativos
- Exportación a Excel con múltiples hojas

---

## 📤 Exportar KPIs

Genera un archivo Excel con:

- KPIs por familia
- KPIs por segmento
- Distribuciones MTTI
- Cierres temporales
- Resumen global

Diseñado para validar gráficas y realizar análisis externo.

---

## ⚙️ Cálculos Automáticos

La aplicación calcula automáticamente:

### 📌 MTTI
Promedio de días hábiles entre fecha de ingreso y fecha de cierre.  
No se cuentan fines de semana ni feriados de Guatemala.

### 📌 Días de cola
Calculados para SR abiertas al día actual.

Los cálculos se ejecutan mediante **signals de Django**.

---

## 🛠️ Tecnologías Usadas

- **Backend:** Django 5.x
- **Base de datos:** PostgreSQL
- **Frontend:** HTML + Bootstrap 5
- **Gráficas:** Chart.js y Plotly.js
- **Contenedores:** Docker y Docker Compose
- **Autenticación:** Custom User Model de Django


---

## 🚀 Estado del Proyecto

- ✔ Funcionalidad completa
- ✔ UI terminada (primera entrega)
- ✔ KPIs funcionando
- ✔ Exportación a Excel
- ✔ Listo para despliegue en servidor

---

## 🔮 Futuras Mejoras

- Dashboard resumido en Home
- Notificaciones
- Historial de cambios
- Permisos más granulares
- API REST pública
- Integración con autenticación corporativa

---

## 📌 Notas Finales

Este proyecto fue desarrollado como un **sistema interno de gestión y análisis**, priorizando:

- Claridad de información
- Trazabilidad
- Métricas confiables
- Escalabilidad futura

## Creado por: Diego Ramírez 

