# SEO técnico para landings

**Cargar cuando:** se crea una ruta indexable, se cambian metadatos, dominio, idioma o despliegue.

## Contrato por página

- `<html lang>` correcto.
- `<title>` único, específico y alineado con intención/oferta.
- Descripción única y honesta.
- Canonical absoluto cuando corresponde, construido desde dominio/configuración confirmados.
- Directiva de indexación explícita cuando un entorno o página no debe indexarse.
- Open Graph mínimo: título, descripción, tipo, URL e imagen absoluta aprobada.
- Metadatos adicionales de la red objetivo solo si aportan una vista previa correcta.
- Favicon disponible y tipo/ruta válidos.

Centralizar la emisión en layout/componente SEO y pasar valores por página. No duplicar dos componentes que compitan por el mismo tag.

## Estructura y contenido

- Un encabezado principal claro y jerarquía que represente el documento.
- Landmarks, enlaces descriptivos y contenido importante en HTML inicial.
- Copy orientado a usuario; no esconder palabras clave ni crear secciones sin función.
- Pruebas, precios y datos estructurados deben coincidir con contenido visible y verificable.

## Sitemap y robots

- Añadir sitemap cuando el sitio indexable y sus rutas lo justifiquen; la integración oficial requiere `site` válido.
- `robots.txt` no protege contenido privado. Mantener entornos de preview/no producción fuera de indexación mediante controles adecuados del proveedor además de metadatos.
- Excluir del sitemap rutas no canónicas, privadas o de prueba según la configuración oficial vigente.

## Datos estructurados

- Elegir un tipo realmente aplicable, completar propiedades requeridas y serializar sin inyección.
- No inventar reviews, calificaciones, precios, disponibilidad, organización o FAQ.
- Validar contra la herramienta/esquema correspondiente; un JSON válido no garantiza elegibilidad.

## Migración y despliegue

- Preservar URLs valiosas o definir redirecciones en la capa del proveedor/servidor.
- Verificar `site`, `base`, trailing slash y canonical en el HTML construido.
- No publicar canonical de localhost, preview o dominio provisional.
- Revisar códigos HTTP, enlaces internos, 404, OG accesible y cabeceras de caché.

## Criterio de aceptación

Cada ruta tiene intención y metadata propia, canonical coherente, social preview verificable y contenido semántico; sitemap/robots reflejan el entorno final.

Fuentes oficiales: [configuración `site` y `base`](https://docs.astro.build/en/reference/configuration-reference/), [integración sitemap](https://docs.astro.build/en/guides/integrations-guide/sitemap/), [rutas](https://docs.astro.build/en/guides/routing/).

