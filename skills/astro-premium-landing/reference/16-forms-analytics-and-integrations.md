# Formularios, analítica e integraciones

**Cargar cuando:** la conversión envía datos, se añade analítica, CRM, agenda, pagos, chat o un servicio externo.

## Decisión de formulario

1. Definir campos, finalidad, responsable, retención, consentimiento, estados y destino.
2. Elegir servicio gestionado, endpoint existente o ruta de servidor según requisitos; no activar renderizado bajo demanda para toda la landing si un servicio aislado basta.
3. Validar en cliente para usabilidad y siempre en el receptor como autoridad.
4. Diseñar éxito, error, reintento, duplicados, spam y pérdida de conexión.
5. No poner claves privadas en el navegador ni en variables públicas.

## Accesibilidad y UX obligatorias

- Labels persistentes, tipos/autocomplete adecuados e instrucciones antes del error.
- Errores específicos asociados al campo; resumen/manejo de foco según complejidad.
- Botón con estado de envío sin impedir recuperar/reintentar.
- Conservar valores ante errores no sensibles.
- Mensaje de privacidad y consentimiento cuando corresponda; no marcar opt-ins opcionales por defecto.
- CTA funcional sin depender solo de un handler JavaScript opaco.

## Analítica

- Crear un mapa de eventos: nombre, disparador, propiedades permitidas, finalidad y propietario.
- Medir la conversión real, no cada interacción posible.
- No enviar PII, copy de campos, URLs con datos ni secretos.
- Cargar según consentimiento y política aplicable; documentar comportamiento sin consentimiento.
- Evitar listeners duplicados y eventos dobles después de navegación/reintento.
- Verificar en entorno de prueba sin contaminar producción si el proveedor lo permite.

## Integraciones

- Confirmar contrato, timeout, rate limit, privacidad, licencia, CSP/domains y fallback.
- Aislar la integración en un componente/módulo con interfaz pequeña.
- Diferir widgets pesados hasta interacción cuando no sean críticos.
- Tratar HTML o scripts remotos como no confiables; evitar inyección directa.
- Registrar variables por nombre y entorno, nunca valores.

## Renderizado

Si se requiere secreto o lógica por petición, cargar [Node/on-demand](21-deploy-node-on-demand.md) y documentación oficial del adaptador. Mantener estáticas las rutas que puedan prerenderizarse.

## Criterio de aceptación

Flujo de éxito y error probado, datos minimizados, accesibilidad completa, eventos sin duplicación, secretos solo del lado apropiado y contrato de operación documentado.

