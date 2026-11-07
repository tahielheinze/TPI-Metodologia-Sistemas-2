# Sistema de Gestión de Solicitudes Académicas — Trabajo Práctico Integrador (Metodología de Sistemas II)

Este proyecto constituye el Trabajo Práctico Integrador de la materia Metodología de Sistemas II de la Tecnicatura Universitaria en Programación (TUPaD UTN).
Consiste en la evolución y refactorización de un sistema de software enfocado en la gestión de solicitudes académicas. Logrando la reducción de deuda técnica, la aplicación de principios SOLID y la preservación del comportamiento externo mediante refactoring seguro.

## Enlace Video de Presentación
[Demostración y Defensa Técnica del Proyecto](https://youtu.be/9Mqp4jKQ6e0)

## Arquitectura del Sistema y Evolución Técnica

El proyecto expone la evolución técnica en dos estados claramente diferenciados a través de Git:

1. **Estado Inicial (`estado-inicial`)**: Versión monolítica acoplada a persistencia estática en archivos planos. Presenta 8 code smells diagnosticados (Long Method, God Class, Long Parameter List, Feature Envy, Magic Strings, Duplicate Code, Tight Coupling y Poor Error Handling).

2. **Estado Refactorizado (`estado-refactorizado`)**: Arquitectura limpia orientada a dominio, aplicando principios SOLID (SRP, OCP, LSP, ISP, DIP), desacoplamiento de persistencia por interfaz de repositorio y simplificación de parámetros mediante objetos de transferencia (DTO).

## Módulo 1: Sistema Base (Estado Inicial)

Prototipo monolítico diseñado para evidenciar problemas de calidad interna sin alterar la calidad externa visible para el usuario.
Características Principales:
- **Gestión Monolítica**: La clase `SistemaGestorGeneral` concentra todas las operaciones del sistema.
- **Persistencia Directa**: Escritura y lectura acoplada sobre archivos planos de texto.
- **Validación Rígida**: Duplicación de lógica de permisos y bloques de manejo de errores genéricos.
- **Definición de Estados**: Uso de cadenas mágicas (Magic Strings) dispersas en el flujo de ejecución.

## Módulo 2: Sistema Refactorizado (Estado Final)

Arquitectura optimizada orientada a la mantenibilidad, extensibilidad y legibilidad del código fuente.
Características Principales:
- **Inversión de Dependencias (DIP)**: Uso de interfaces explícitas (`ISolicitudRepository`) para abstraer la persistencia de datos.
- **Descomposición de Métodos (Extract Method)**: Reducción de métodos extensos a funciones atómicas con responsabilidad única.
- **Transferencia de Parámetros (Introduce Parameter Object)**: Agrupación de filtros de búsqueda mediante la estructura `FiltroSolicitudDTO`.
- **Encapsulamiento del Dominio**: Eliminación de Feature Envy trasladando la responsabilidad de actualización a las entidades correspondientes.

## Tecnologías:
- Python | Git / GitHub | Paradigma Orientado a Objetos (POO) | Estándar PEP8

## Estructura del Repositorio y Git Tags:
- `estado-inicial`: Tag inmutable con la versión base con deudas técnicas.
- `estado-refactorizado`: Tag inmutable con la versión refactorizada y optimizada.
- `etapa-diagnostico`, `etapa-refactoring`, `etapa-pruebas`, `etapa-docs`: Tags de seguimiento por hitos.

## Instalación y Ejecución

### Requisitos Previos
- Python 3.10 o superior instalado en el sistema.

### Ejecución del Sistema Base (Estado Inicial)
```bash
python sistema_academico_base.py
```

### Ejecución del Sistema Refactorizado (Estado Final)
```bash
python sistema_academico_refactorizado.py
```

## Documentación y Evidencias
- La carpeta `/docs` contiene el checklist técnico de Code Review profesional (`checklist_code_review.md`).
- La carpeta `/docs/evidencias/` almacena las capturas comparativas de "Antes y Después" de las refactorizaciones aplicadas.

## Consideraciones Importantes
- **Datos Sintéticos**: Todos los datos de pruebas son 100% sintéticos y anonimizados.
