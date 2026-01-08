Va, **muy resumido y claro**, tipo guía que puedes pegar como comentario o README 👌

---

## Arquitectura: Model – Controller – Repository

### **Model**

**Qué es:**
Estructura de datos pura. **No piensa, no decide, no toca archivos**.

**Debe hacer:**

* Guardar estado:

  * `text`
  * `last_nota`
  * `path`
* Ser simple (atributos, opcional `__init__`)

**NO debe:**

* Leer/escribir archivos
* Validar nombres
* Formatear texto
* Llamar al repository

---

### 🎮 **Controller**

**Qué es:**
El orquestador. **Decide qué hacer y cuándo**.

**Debe hacer:**

* Coordinar Model ↔ Repository
* Aplicar lógica de negocio:

  * qué nota cargar
  * cuándo guardar
  * qué pasa al borrar
* Preparar datos antes de guardarlos
* Decidir **qué contenido** se guarda

**NO debe:**

* Acceder directamente al filesystem
* Guardar config manualmente
* Saber cómo se escriben archivos

---

### **Repository**

**Qué es:**
Capa de persistencia. **Solo sabe leer y escribir**.

**Debe hacer:**

* Leer / escribir notas
* Listar archivos
* Borrar archivos
* Leer / escribir configuración
* Normalizar nombres de archivo

**NO debe:**

* Decidir qué nota usar
* Formatear contenido
* Tener lógica de negocio
* Depender de la UI
