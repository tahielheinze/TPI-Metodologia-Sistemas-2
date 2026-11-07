# Checklist de Code Review Inicial (Diagnóstico) — Metodología de Sistemas II

**Proyecto:** Sistema de Gestión de Solicitudes Académicas
**Versión de Evaluación:** `estado-inicial` (Código Base)

## Lista de Chequeo Técnica

### 1. Principios de Diseño y Arquitectura (SOLID)

| Criterio | Estado | Observación |
|---|---|---|
| SRP | Rechazado | La clase `SistemaGestorGeneral` actúa como *God Class*, acumulando lógica de negocio, validaciones, gestión de usuarios y escritura en disco |
| OCP | Rechazado | Para agregar un nuevo estado o canal de persistencia es obligatorio modificar el código fuente existente. |
| LSP | No Aplica | No existen jerarquías ni abstracciones en el diseño base. |
| ISP | No Aplica | Ausencia total de interfaces o contratos abstractos. |
| DIP | Rechazado | Acoplamiento rígido directo a archivos planos mediante la llamada directa a `open("solicitudes_db.txt")`. |

### 2. Calidad de Código y Code Smells Detectados

| Criterio | Estado | Observación |
|---|---|---|
| Tamaño de Funciones | Rechazado | Long Method: El método `procesar_solicitud_completa()` mezcla múltiples responsabilidades. |
| Manejo de Parámetros | Rechazado | Long Parameter List: La función `filtrar_solicitudes` requiere 6 parámetros sueltos en su firma. |
| Manejo de Cadenas | Rechazado | Magic Strings: Estados como `"Pendiente"` o `"En Proceso"` están hardcodeados como texto suelto. |
| Duplicación de Código | Rechazado | Código Duplicado: Verificación manual de permisos repetida en cada operación del gestor. |
| Delegación de Dominio | Rechazado | Feature Envy: La clase `Reporteador` manipula las estructuras internas de `Solicitud` en lugar de delegar la acción. |
| Manejo de Excepciones | Rechazado | Poor Error Handling: Uso de bloques `try-except` genéricos que ocultan y silencian excepciones de negocio (`pass`). |

### 3. Estándares y Seguridad

| Criterio | Estado | Observación |
|---|---|---|
| Privacidad de Datos | Aprobado | Se utilizan exclusivamente datos sintéticos anonimizados. |

## Resumen del Diagnóstico Inicial

El sistema cumple con la calidad externa básica (ejecuta las 4 operaciones requeridas), pero presenta una calidad interna crítica. La presencia de 8 code smells estructurales vulnera la mantenibilidad y eleva drásticamente el costo del cambio. Se requiere una refactorización segura y profunda.

## Estado de la Revisión: REQUIERE REFACTORIZACIÓN