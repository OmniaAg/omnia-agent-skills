# Componentes, layouts y contenido

**Cargar cuando:** se diseña arquitectura de componentes, se crea una página o se modela contenido repetible.

## Jerarquía recomendada

- **Página:** conoce ruta, datos de la ruta y layout elegido.
- **Layout:** emite documento, landmarks compartidos y contrato SEO; renderiza `<slot />`.
- **Sección:** representa una unidad narrativa/comercial (`Hero`, prueba, beneficios, CTA).
- **UI pequeña:** botón, enlace, badge o control solo cuando hay reutilización o un contrato útil.
- **Datos:** arrays/objetos tipados para contenido repetido; colección si escala/validación lo exige.

## Contratos obligatorios

```astro
---
interface Props {
  title: string;
  description?: string;
}

const { title, description } = Astro.props;
---
```

- Definir `Props` cerca del componente y evitar `any`.
- Usar nombres que expresen función comercial, no apariencia accidental.
- Mantener slots explícitos para composición; documentar slots nombrados si existen.
- Pasar contenido como props/datos, no inyectar HTML con JavaScript.
- Renderizar HTML semántico: landmarks, jerarquía de encabezados, listas, enlaces y botones según intención.

## Límites de componente

Dividir cuando una sección tiene contrato propio, se reutiliza, concentra una interacción o dificulta razonar/pruebas. No dividir cada `div`: una abstracción sin responsabilidad aumenta navegación y contexto.

Evitar componentes monolíticos mediante secciones coherentes, pero conservar juntos markup y CSS local que cambian por la misma razón.

## Layout y SEO

- El layout recibe metadatos por página y genera defaults solo donde están aprobados.
- Una página debe poder sobrescribir título, descripción, canonical, social e indexación.
- No crear varias fuentes de verdad para el mismo metadato.
- Para metadatos completos, cargar [SEO](12-seo.md).

## Contenido reutilizable

- Un array tipado es suficiente para beneficios, métricas, FAQs pequeñas o logos.
- Una colección aporta valor cuando hay muchas entradas, esquema, relaciones, consultas o autores no técnicos.
- No convertir copy único de una landing en CMS/colección por anticipación.
- No ocultar contenido importante detrás de JavaScript si puede estar en el HTML inicial.

## Revisión

- Una sola instancia de header/footer por documento.
- Un `main` y encabezado principal coherente por página.
- Props tipadas, imports locales válidos y ausencia de documentos anidados.
- Componentes interactivos revisados con [interactividad](08-native-interactivity.md) o [islas](09-islands-and-ui-frameworks.md).

Fuentes oficiales: [componentes Astro](https://docs.astro.build/en/basics/astro-components/), [layouts](https://docs.astro.build/en/basics/layouts/), [contenido en Astro](https://docs.astro.build/en/guides/content-collections/).

