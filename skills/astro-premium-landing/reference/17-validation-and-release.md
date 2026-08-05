# Checklist previo a producción

**Cargar cuando:** se audita, se prepara release o se declara terminada una landing.

## 1. Alcance y contenido

- [ ] Intake y criterios de aceptación actualizados.
- [ ] No quedan `TODO`, `FIXME`, `PENDIENTE`, lorem, placeholders, URLs o assets de ejemplo.
- [ ] Oferta, precios, métricas, testimonios, logos y claims tienen aprobación/fuente.
- [ ] CTA y destinos funcionan; legales y privacidad están disponibles.

## 2. Arquitectura y código

- [ ] Rutas, layouts, componentes, estilos, assets y `public/` cumplen su responsabilidad.
- [ ] Props/datos TypeScript no usan `any` injustificado.
- [ ] No hay documentos HTML anidados, duplicación estructural o componentes monolíticos sin motivo.
- [ ] No existen imports rotos, rutas frágiles o referencias `/src/assets/`.
- [ ] Frameworks, Tailwind, integraciones, adaptador e islas están justificados.
- [ ] `document`/`window` no se ejecutan durante render del servidor.

## 3. Interfaz

- [ ] Responsive revisado en anchos estrechos, medios y amplios con contenido real.
- [ ] Sin overflow, solapes, texto cortado ni targets difíciles.
- [ ] Estados hover/focus/active/disabled/error/success están definidos cuando aplican.
- [ ] Interacciones funcionan sin inicialización duplicada y degradan razonablemente.
- [ ] Reduced motion preserva contenido y función.

## 4. Accesibilidad

- [ ] Landmarks, headings, nombres, labels, alt y orden de lectura revisados.
- [ ] Recorrido de teclado completo, foco visible y retorno de foco correcto.
- [ ] Contraste, zoom/reflow, errores y anuncios dinámicos revisados.
- [ ] Automatización ejecutada y limitaciones humanas declaradas.

## 5. SEO y assets

- [ ] `lang`, title, description, canonical, OG, favicon e indexación por ruta.
- [ ] `site`, `base`, robots y sitemap coinciden con producción.
- [ ] Imágenes tienen licencia, alt, dimensiones, peso y carga apropiados.
- [ ] Imagen social absoluta accesible; enlaces internos y 404 revisados.

## 6. Rendimiento y seguridad

- [ ] Presupuesto de JS, fuentes, CSS, imágenes y terceros revisado.
- [ ] LCP, CLS e interacción evaluados en build final cuando hay herramientas.
- [ ] No hay secretos en cliente, repositorio, logs o salida construida.
- [ ] Formularios, consentimiento, spam, analítica y fallbacks probados.
- [ ] Cabeceras, caché, CSP y redirecciones corresponden a la capa de despliegue.

## 7. Comandos y salida

1. `python scripts/verify_project.py RUTA --strict`
2. Comprobación Astro/TypeScript definida por el proyecto.
3. Build del proyecto con su gestor y lockfile, sin instalar implícitamente.
4. Inspección de `dist/` o salida del adaptador.
5. Prueba local de rutas, assets, formularios y 404 en un servidor equivalente.

No inventar comandos: leer `package.json` y consultar la CLI oficial vigente.

## Evidencia final

Registrar fecha, entorno, commit/estado si existe, comandos exactos, exit codes, resultados, pruebas omitidas, documentación oficial consultada, advertencias aceptadas y rollback. Un checklist marcado sin evidencia no cuenta como validación.

