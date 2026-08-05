# Flujo y guardrails universales

**Cargar cuando:** se inicia un encargo, cambia el alcance o se prepara la entrega. Estas reglas son independientes del framework.

## Obligatorio

1. Convertir el intake en una lista de requisitos confirmados, pendientes, restricciones y criterios de aceptación.
2. Inspeccionar antes de editar: estructura, scripts, configuración, convenciones y cambios ajenos.
3. Limitar cada cambio al objetivo actual. No ampliar stack, proveedor o superficie de datos por conveniencia.
4. Preservar contenido y trabajo existente; una refactorización visual no autoriza reescribir negocio o infraestructura.
5. Registrar comandos ejecutados, salidas relevantes y pruebas no ejecutadas.
6. Tratar credenciales, formularios, analítica, licencias de assets y despliegue como superficies sensibles.
7. Terminar con build verificable, revisión de la salida y un reporte de riesgos; no con una impresión visual aislada.

## Bucle operativo

1. **Descubrir:** intake, entorno, estado inicial y bloqueos.
2. **Decidir:** arquitectura mínima, dirección visual, contenido, métricas y presupuesto.
3. **Implementar:** cortes verticales pequeños y reversibles.
4. **Verificar:** primero comprobaciones rápidas; después tipos, build, navegador y checklist.
5. **Optimizar:** solo a partir de evidencia o un presupuesto incumplido.
6. **Entregar:** cambios, decisiones, documentación, comandos, resultados y pendientes.

## Condiciones de bloqueo

- Falta el destino de un formulario o la base legal para procesar datos.
- No está claro qué contenido, licencia o dominio puede publicarse.
- Elegir renderizado dinámico, framework o proveedor cambiaría materialmente coste y arquitectura.
- El archivo objetivo contiene cambios ajenos incompatibles que no pueden preservarse.
- La operación requiere credenciales, instalación, despliegue o modificación fuera del alcance.

Un dato cosmético ausente no bloquea el análisis: se marca como pendiente. No sustituirlo silenciosamente por contenido de demostración.

## Recuperación

- Mantener una lista de archivos tocados y pruebas asociadas.
- Ante regresión, aislar el último cambio propio y corregirlo; no usar resets destructivos.
- Si una validación externa no está disponible, ejecutar las verificaciones estáticas posibles y declarar la limitación.
- Si cambia una decisión de arquitectura, actualizar intake, módulo afectado y criterios antes de continuar.

## Recomendado

- Priorizar un corte completo y accesible de la página antes de efectos decorativos.
- Mantener evidencia compacta: resumen y rutas, no volcados enteros de herramientas.
- Revisar este módulo junto con [validación y release](17-validation-and-release.md) al cerrar.

