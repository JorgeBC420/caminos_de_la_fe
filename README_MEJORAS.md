# README: Mejoras y Expansiones Pendientes para Caminos de la Fe

## Localización
- Integrar el sistema de claves de texto en toda la UI.
- Añadir más textos y traducciones en `en.json` y `es.json`.
- Detección automática de idioma en `lang_manager.py` (ya implementado, expandir a toda la UI).

## Servidor y Multiplayer
- Crear servidor FastAPI con endpoints para guerras santas, duelos y progreso de jugador.
- Implementar simulación de batallas en el backend.
- Añadir Redis para cache y MongoDB para persistencia de datos.

## Items Legendarios y Facciones
- Añadir 3 items legendarios por facción avanzada (Vikingos, Egipcios, Romanos).
- Implementar mecánica de robo/protección y sistema de purificación.
- Crear habilidades únicas por facción avanzada.
- Diseñar equipo temático y modelos 3D para cada facción.

## Optimización
- Implementar pooling de enemigos y objetos.
- Añadir LOD (Level of Detail) para modelos 3D complejos.
- Mejorar gestión de memoria en escenas grandes.

## Guardado y Progreso
- Añadir sistema de guardado automático y recuperación.
- Guardar progreso de invitado localmente.
- Persistencia de mundo y selección de servidores.

## Facciones Avanzadas (Endgame)
- Sistema de desbloqueo por nivel y misiones de iniciación.
- Integrar NPC de facciones avanzadas con diálogos grabados.
- Crear zonas especiales y mapas únicos para cada facción avanzada.
- Implementar efectos visuales y habilidades especiales.
- Diseñar interfaces específicas para cada facción.

## Misiones y Reputación
- Añadir misiones secundarias temáticas.
- Sistema de reputación por facción y recompensas.

## Interfaces y Experiencia
- Diseñar interfaces específicas para facciones avanzadas y zonas especiales.
- Integrar GridMenu y ParticleEffect prefabs en inventario y habilidades.
- Grabar y añadir diálogos interactivos para NPCs faccionarios.

---

**Prioridad:**
1. Servidor FastAPI y endpoints clave
2. Integración total de localización
3. Facciones avanzadas y contenido endgame
4. Optimización y guardado automático
5. Interfaces y diálogos temáticos

**Notas:**
- Requiere modelos 3D y assets visuales para equipo y enemigos avanzados.
- Grabar diálogos para NPCs y facciones.
- Diseñar interfaces y menús temáticos para cada facción avanzada.
