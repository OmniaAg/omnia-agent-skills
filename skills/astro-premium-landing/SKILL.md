---
name: astro-premium-landing
description: Diseña, implementa, audita y prepara para producción landing pages comerciales premium con Astro, TypeScript, HTML semántico, CSS moderno, JavaScript mínimo, SEO, accesibilidad y alto rendimiento. Úsala para landings nuevas o existentes, migraciones desde HTML estático, arquitectura de componentes, assets, formularios, animaciones y despliegue multiplataforma.
---

# Astro Premium Landing

## Propósito

Crear landing pages comerciales con Astro que conviertan, sean mantenibles y lleguen a producción con evidencia verificable. Esta skill orquesta el trabajo; carga de `reference/` solo los módulos que correspondan a la tarea.

## Alcance

- Analizar, inicializar, implementar, migrar, optimizar y auditar landings con Astro.
- Definir arquitectura, componentes, estilos, contenido, SEO, accesibilidad, rendimiento, interacción, assets, formularios y despliegue.
- Favorecer salida estática, componentes `.astro`, TypeScript y HTML semántico.
- Conservar dirección comercial y visual sin imponer un proveedor, framework de interfaz o sistema CSS.

## Cuándo usarla

- La entrega principal es una landing o micrositio comercial construido con Astro.
- Se necesita adaptar HTML/CSS/JavaScript tradicional a una arquitectura Astro.
- Se requiere una auditoría integral o una preparación previa a producción.
- Hay que justificar islas, integraciones, adaptadores o decisiones de despliegue.

## Cuándo no usarla

- La tarea no involucra Astro ni una landing comercial.
- El producto es principalmente una aplicación autenticada o un panel con estado complejo; usa una arquitectura de aplicación adecuada.
- Solo se pide una API, un backend o una operación de infraestructura sin interfaz.
- El usuario exige otro stack y no autoriza migrarlo.

## Requisitos previos

1. Lee el brief o `intake-template.md`; registra lo que falte sin inventarlo.
2. Inspecciona archivos, scripts, gestor de paquetes y cambios existentes antes de escribir.
3. Detecta versión de Astro, modo de salida, integraciones, estrategia CSS y destino de despliegue.
4. Localiza la skill oficial `astro`. En este workspace está en `.agents/skills/astro/SKILL.md`.
5. Si la tarea altera APIs, directivas, configuración, rutas, assets, integraciones o adaptadores, consulta primero la documentación oficial vigente.

## Reglas críticas siempre activas

### Seguridad y alcance

- Modifica únicamente archivos autorizados. Conserva cambios ajenos y nunca sobrescribas sin inspección.
- No instales dependencias, frameworks, adaptadores ni integraciones sin necesidad demostrada y autorización dentro del alcance.
- No ejecutes despliegues ni operaciones destructivas por inferencia.
- No expongas secretos. Solo las variables públicas explícitas pueden llegar al cliente; valida la convención vigente de Astro antes de usarlas.
- Usa comandos no interactivos, argumentos separados y rutas absolutas o correctamente delimitadas; en Windows no construyas comandos con concatenación insegura.

### Arquitectura Astro

- Usa generación estática por defecto. El renderizado bajo demanda exige una necesidad dinámica concreta y un destino compatible.
- `src/pages/` define rutas; `src/layouts/` layouts; `src/components/` componentes; `src/styles/` estilos compartidos; `src/assets/` recursos procesables; `public/` archivos servidos sin procesamiento.
- Los componentes `.astro` son la primera opción. Tipa `Props`, modela contenido repetido con datos o componentes y evita duplicar header, footer, SEO o documentos HTML completos.
- Usa layouts para estructura y metadatos consistentes, pero permite metadatos por página.
- Usa colecciones de contenido solo si validación, consulta o escala del contenido compensan la complejidad.
- Instala un adaptador solo cuando el modo de renderizado o el proveedor lo requiera.
- El proyecto debe completar sus comprobaciones y build antes de declararse terminado.

### Interfaz y JavaScript

- Resuelve primero con HTML semántico y CSS; después con JavaScript nativo para interacciones pequeñas.
- No instales React, Vue, Svelte, Preact, Solid u otro runtime por defecto.
- Cada isla hidratada debe registrar motivo, componente, alternativas, impacto, directiva `client:*` y coste de mantenimiento/rendimiento.
- No uses `client:load` por comodidad. Elige la directiva más restrictiva que mantenga la experiencia necesaria.
- Mantén scripts locales, acotados, idempotentes y compatibles con navegación o reinicialización cuando aplique.

### Calidad visual y comercial

- Alinea jerarquía, prueba, oferta y CTA con el objetivo de conversión.
- Diseña responsive desde el contenido; preserva lectura, foco, contraste, objetivos táctiles y movimiento reducido.
- Selecciona una dirección visual y una firma distintiva. Evita plantillas genéricas, efectos sin función y dependencias visuales innecesarias.
- Tailwind es opcional: solo úsalo si el proyecto ya lo usa o el usuario lo solicita.

## Documentación oficial de Astro

- Usa exclusivamente `https://docs.astro.build/` como autoridad para Astro cuando exista documentación aplicable.
- Sigue primero las instrucciones de la skill oficial `astro`; no copies su contenido dentro de esta skill.
- Carga solo la página oficial necesaria para la decisión actual.
- Revalida cualquier detalle sensible a versión: configuración, CLI, directivas, integraciones, adaptadores, variables de entorno y despliegue.
- Registra en el reporte final título o tema, URL y decisión respaldada. Distingue documentación, inferencia y restricción del proyecto.

## Flujo de trabajo

### 1. Intake y entorno

Objetivo: convertir el encargo en requisitos verificables.

- Carga `reference/01-workflow-and-guardrails.md` y `reference/02-environment-and-project-audit.md`.
- Completa el intake; marca decisiones pendientes y bloqueos reales.
- Inspecciona proyecto, versión, estructura, scripts, lockfile, configuración y cambios existentes.
- Fin: alcance, conversión, stack, riesgos y criterios de aceptación están explícitos.

### 2. Consulta oficial y arquitectura

Objetivo: decidir la solución mínima correcta.

- Carga los módulos obligatorios del Registry.
- Consulta documentación oficial solo para las superficies Astro que se modificarán.
- Define rutas, layout, componentes, modelo de contenido, estilos, assets e interactividad.
- Fin: cada dependencia, integración o isla tiene justificación; no quedan supuestos críticos ocultos.

### 3. Implementación

Objetivo: producir una landing semántica, modular y fiel al brief.

- Implementa verticalmente: shell/layout, secciones, contenido, responsive, estados, assets y metadatos.
- Reutiliza patrones, tokens y componentes sin abstraer prematuramente.
- Mantén JavaScript y CSS global bajo control.
- Fin: rutas y estados acordados funcionan con contenido final o pendientes identificados.

### 4. Verificación y optimización

Objetivo: obtener evidencia, no impresiones.

- Ejecuta el verificador rápido durante el trabajo y `--strict` al cerrar.
- Ejecuta comprobación de tipos y build con los scripts locales del proyecto; no instales automáticamente.
- Revisa salida construida, accesibilidad, teclado, responsive, SEO, assets, reduced motion y presupuesto de cliente.
- Fin: no hay errores; las advertencias aceptadas tienen justificación.

### 5. Preparación de despliegue y reporte

Objetivo: producir un artefacto desplegable sin acoplamiento accidental.

- Carga el módulo de despliegue general y solo el módulo del destino elegido.
- Verifica `site`, `base`, rutas, variables, formularios, redirecciones, caché y directorio de salida.
- No despliegues salvo petición y autorización explícitas.
- Fin: build reproducible, checklist completo, documentación consultada, cambios y riesgos reportados.

## Skills Registry

Los módulos obligatorios se cargan antes de decidir; los opcionales solo si se activa su condición.

| Tipo de tarea | Módulos obligatorios | Módulos opcionales | Scripts |
|---|---|---|---|
| Analizar proyecto | `02-environment-and-project-audit`, `03-astro-architecture`, `10-critical-astro-gotchas` | `22-windows-troubleshooting` si el entorno es Windows | `verify_project.py` |
| Inicializar landing | `01-workflow-and-guardrails`, `03-astro-architecture`, `04-components-layouts-and-content` | `05-styling-and-design-tokens` al definir estilos | `verify_project.py` |
| Crear página | `03-astro-architecture`, `04-components-layouts-and-content`, `12-seo` | `07-effects-and-animation` si hay movimiento | `verify_project.py` |
| Crear componente | `04-components-layouts-and-content`, `05-styling-and-design-tokens` | `13-accessibility` si es interactivo o estructural | `verify_project.py` |
| Diseñar arquitectura | `03-astro-architecture`, `04-components-layouts-and-content` | `06-landing-archetypes`, `23-legacy-html-migration` | `verify_project.py` |
| Añadir animación | `07-effects-and-animation`, `14-performance` | `15-visual-diversity-guardrails` para dirección visual | `verify_project.py` |
| Añadir JavaScript | `08-native-interactivity`, `14-performance` | `09-islands-and-ui-frameworks` si JS nativo no basta | `verify_project.py` |
| Añadir framework | `09-islands-and-ui-frameworks`, `14-performance` | documentación oficial de la integración concreta | `verify_project.py` |
| Configurar Tailwind | `05-styling-and-design-tokens` | `23-legacy-html-migration` si se migra CSS | `verify_project.py` |
| Optimizar imágenes | `11-images-and-assets` | Openverse si faltan recursos con licencia | `normalize_assets.py`, `openverse_fetch.py` |
| Obtener imágenes externas | `11-images-and-assets` | `13-accessibility` para texto alternativo | `openverse_fetch.py` |
| Añadir SEO | `12-seo` | `04-components-layouts-and-content` para metadatos reutilizables | `verify_project.py` |
| Añadir accesibilidad | `13-accessibility` | `16-forms-analytics-and-integrations` si hay formularios | `verify_project.py` |
| Revisar rendimiento | `14-performance`, `17-validation-and-release` | `07-effects-and-animation`, `09-islands-and-ui-frameworks` | `verify_project.py` |
| Configurar formularios | `16-forms-analytics-and-integrations`, `13-accessibility` | `21-deploy-node-on-demand` si requiere servidor | `verify_project.py` |
| Preparar despliegue | `17-validation-and-release`, `18-deployment-overview` | módulo del proveedor o `20-deploy-static-apache-hostinger` | `verify_project.py` |
| Desplegar plataforma gestionada | `18-deployment-overview`, `19-deploy-platforms` | `21-deploy-node-on-demand` si hay renderizado bajo demanda | `verify_project.py` |
| Hosting tradicional o Apache | `18-deployment-overview`, `20-deploy-static-apache-hostinger` | `22-windows-troubleshooting` si se prepara desde Windows | `verify_project.py` |
| Corregir Windows | `22-windows-troubleshooting`, `02-environment-and-project-audit` | documentación del script afectado | `verify_project.py` |
| Auditar proyecto | `17-validation-and-release`, `10-critical-astro-gotchas` | `18-deployment-overview` si está próximo a publicar | `verify_project.py` |
| Migrar HTML tradicional | `23-legacy-html-migration`, `03-astro-architecture` | `08-native-interactivity`, `20-deploy-static-apache-hostinger` | `verify_project.py` |

Prefija cada nombre del Registry con `reference/` y sufija `.md`. Todos los nombres corresponden a archivos reales.

## Uso de scripts

Desde la raíz de esta skill:

```text
python scripts/verify_project.py RUTA
python scripts/verify_project.py RUTA --strict
python scripts/verify_project.py RUTA --json
python scripts/verify_project.py RUTA --build
python scripts/openverse_fetch.py --help
python scripts/normalize_assets.py --help
```

- `verify_project.py` es de solo lectura salvo que `--build` permita al CLI local generar sus artefactos habituales. Nunca instala.
- `openverse_fetch.py` requiere red, licencia aceptada y destino dentro del proyecto; no sobrescribe sin `--overwrite`.
- `normalize_assets.py` requiere Pillow disponible en el entorno; conserva originales y no instala dependencias.
- Lee `scripts/README.md`, la ayuda del script y su módulo relacionado antes de ejecutarlo.

## Manejo de errores

- Detén la mutación si falta un requisito que cambia arquitectura, tratamiento legal, datos de formulario o destino.
- Si falta una dependencia, informa el comando sugerido pero no la instales sin autorización.
- Si una API de Astro es incierta, pausa esa decisión, consulta la documentación oficial y registra el resultado.
- Si falla una verificación, conserva la salida relevante, corrige la causa mínima y repite la misma prueba.
- Si hay cambios ajenos solapados, preserva el archivo y solicita dirección cuando no exista una edición segura.

## Estrategia de recuperación

1. Registra estado inicial y archivos que se modificarán.
2. Trabaja en cambios pequeños y reversibles; no uses resets destructivos.
3. Ante fallo, revierte solo el cambio propio identificado o aplica una corrección localizada.
4. Repite comprobaciones rápidas antes de continuar.
5. Si el build previo funcionaba y el nuevo no, compara configuración, imports, rutas y dependencias antes de ampliar el alcance.

## Reglas de verificación

- No declares una prueba aprobada si no se ejecutó.
- Como mínimo: sintaxis/configuración, tipos, build, rutas/assets, SEO, accesibilidad básica y pendientes de contenido.
- Revisa la landing construida en sus breakpoints y estados relevantes; los chequeos heurísticos no reemplazan auditoría en navegador o tecnología asistiva.
- Usa `--json` para automatización y salida humana para diagnóstico.
- En modo estricto, resuelve o justifica cada advertencia.

## Criterios de finalización

- Se cumplen objetivo de conversión, sitemap, contenido y criterios del intake.
- La arquitectura es Astro-first, estática por defecto, semántica, tipada y sin duplicación estructural evidente.
- No hay frameworks, Tailwind, hidratación, adaptadores o librerías sin justificación.
- Metadatos, assets, teclado, foco, contraste, reduced motion, responsive y rendimiento fueron revisados.
- Las comprobaciones acordadas y el build pasan; la salida final fue inspeccionada.
- El reporte enumera archivos, documentación oficial, comandos, resultados, advertencias aceptadas, riesgos y próximos pasos.

## Límites de modificación

- No cambies hosting, analítica, formularios, dominio, DNS, dependencias o modo de renderizado fuera del alcance autorizado.
- No sustituyas el sistema de estilos existente por preferencia personal.
- No conviertas datos únicos en una colección ni contenido repetible en HTML duplicado.
- No copies documentación extensa de Astro: enlázala y conserva aquí solo decisiones operativas.
