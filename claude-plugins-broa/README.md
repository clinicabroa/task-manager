# Kit de instalación: Corporate Law Expert MX para Clínica Broa

Este directorio contiene lo necesario para distribuir el plugin
[`Corporate-Law-Expert-MX`](https://github.com/abogadodigital/Corporate-Law-Expert-MX)
a toda la organización `clinicabroa` desde claude.ai, sin que cada persona
tenga que instalarlo a mano.

## Qué es el plugin

| Dato | Valor |
|---|---|
| Nombre del plugin | `corporate-law-expert-mx` |
| Autor | Joel A. Gómez Treviño |
| Licencia | CC BY-NC-SA 4.0 (uso **no comercial**) |
| Contenido | 13 skills + 6 corpus JSON (LGSM, 260 artículos; 55 tesis SCJN) |
| Hooks / MCP / ejecutables | **Ninguno** — solo Markdown y JSON |
| Directorio `bin/` de nivel superior | No tiene (requisito para distribución org-wide) |

No ejecuta código: las skills son instrucciones en Markdown y los corpus son
datos JSON. Por eso el riesgo técnico de distribuirlo es bajo.

**Costo de contexto medido** (con `claude plugin details`, Claude Code 2.1.278):
~4,545 tokens *always-on*, es decir añadidos a cada sesión de quien lo tenga
activo. Cada skill cuesta además entre ~1.4k y ~3.5k tokens al dispararse. Es un
costo notable: si el equipo incluye a personas que no hacen trabajo societario,
conviene dejar el plugin **opcional** en lugar de requerido (paso 5).

**Verificación realizada**: `claude plugin validate` pasa tanto sobre el repo
del autor como sobre el marketplace-espejo de este directorio, y la cadena
completa (añadir el espejo → instalar desde la fuente pública) se probó con
éxito: se cargan las 13 skills, 0 agentes, 0 hooks, 0 servidores MCP y 0 LSP.

## Por qué hace falta este marketplace-espejo

La distribución org-wide (**Configuración de la organización > Plugins** en
claude.ai) exige que **el repositorio del marketplace sea privado o interno**
en github.com y que se lea a través de la conexión GitHub de tu organización.
El repositorio del autor es público y no pertenece a `clinicabroa`, así que no
puede usarse directamente.

La regla complementaria sí permite lo que hacemos aquí: *"Any other plugin
source must be a public repository on github.com, gitlab.com, or bitbucket.org,
which organization sync fetches without credentials."* Es decir, un marketplace
**privado de Clínica Broa** puede apuntar como *fuente de plugin* al repo
**público** del autor. Eso es exactamente lo que hace
`.claude-plugin/marketplace.json` de este directorio.

Ventaja adicional: no copiamos el material del autor, solo lo referenciamos, y
el equipo recibe las actualizaciones que él publique.

## Pasos (los ejecuta un Owner de la organización en claude.ai)

1-2. **Crear el repositorio espejo y subir el manifiesto.** Desde una máquina
   con `gh` autenticado como `clinicabroa`, parado en la raíz de este repo:

   ```bash
   gh repo create clinicabroa/claude-plugins --private \
     --description "Biblioteca de plugins de Claude distribuida a Clínica Broa"

   git clone https://github.com/clinicabroa/claude-plugins /tmp/claude-plugins
   mkdir -p /tmp/claude-plugins/.claude-plugin
   cp claude-plugins-broa/.claude-plugin/marketplace.json \
      /tmp/claude-plugins/.claude-plugin/marketplace.json

   cd /tmp/claude-plugins
   git add .claude-plugin/marketplace.json
   git commit -m "Add Broa plugin marketplace manifest"
   git push
   ```

   La ruta del archivo importa: el manifiesto debe quedar exactamente en
   `.claude-plugin/marketplace.json`, en la **raíz** del repo nuevo.

   > Este paso no puede hacerlo Claude Code desde una sesión remota: el token
   > de la Claude GitHub App está limitado a los repositorios donde está
   > instalada y no tiene permiso para crear repositorios nuevos (GitHub
   > responde `403 Resource not accessible by integration`).

3. **Verificar la conexión de GitHub.** La sincronización de organización lee
   el repo mediante la Claude GitHub App. Si aún no está instalada sobre
   `clinicabroa/claude-plugins`, instálala en
   <https://github.com/apps/claude/installations/select_target>.

4. **Dar de alta el marketplace.** Entra a
   <https://claude.ai/admin-settings/plugins> (requiere plan Team o Enterprise
   y rol **Owner**), añade el marketplace apuntando a
   `clinicabroa/claude-plugins` y activa **Sync automatically** si quieres que
   cada push a la rama por defecto dispare una sincronización.

5. **Habilitar el plugin para el equipo.** Una vez sincronizado, habilita
   `corporate-law-expert-mx` para la organización desde esa misma página. Si lo
   marcas como **requerido**, nadie del equipo podrá desactivarlo:
   `claude plugin disable` responderá
   `Plugin "corporate-law-expert-mx@synced" is required by your organization and
   can't be disabled here.` Si lo dejas opcional, cada quien puede apagarlo con
   `claude plugin disable corporate-law-expert-mx@synced`.

6. **Cómo lo recibe el equipo.** Los plugins habilitados en claude.ai llegan
   solos: en Claude Code se descargan a `~/.claude/plugins/synced/` y se cargan
   como `corporate-law-expert-mx@synced`. En sesiones de terminal requiere
   Claude Code v2.1.273 o posterior. Para verlos: `claude plugin list` (bajo el
   encabezado *Synced from claude.ai*). Si una sesión ya estaba abierta,
   `/reload-plugins`.

Las skills se activan solas según el tema de la consulta; también pueden
invocarse por nombre, p. ej. `/corporate-law-expert-mx:identificacion-tipo-social-aplicable`.

## Alternativa: carga directa

La misma página **Configuración de la organización > Plugins** admite subir un
plugin directamente, sin marketplace. Esa ruta copia el material a la
biblioteca de la organización (queda congelado en la versión subida, sin
actualizaciones del autor) y el detalle del formato de archivo aceptado está en
el artículo de soporte *Manage plugins for your organization*
(<https://support.claude.com/en/articles/13837433>), que no pude consultar desde
este entorno. Si prefieres esa ruta, confirma el formato en la propia interfaz.

## Fijar una versión concreta (opcional)

Para auditoría jurídica puede convenir congelar el corpus en un commit
verificado, en lugar de seguir la rama. Añade `ref` y/o `sha` a la fuente:

```json
"source": {
  "source": "github",
  "repo": "abogadodigital/Corporate-Law-Expert-MX",
  "sha": "49660c161d261a74b902239a3e069720bff0c504"
}
```

Ese SHA corresponde al único commit publicado al 22 de septiembre de 2026.

## Instalación individual (sin pasar por la organización)

Si alguien necesita el plugin antes de que se complete lo anterior, en su
propio Claude Code:

```shell
/plugin marketplace add abogadodigital/Corporate-Law-Expert-MX
/plugin install corporate-law-expert-mx@corporate-law-expert-mx
```

El nombre del marketplace y el del plugin coinciden porque el repo del autor es
su propio marketplace.

## Advertencias para el equipo

- **Licencia no comercial.** CC BY-NC-SA 4.0 permite el uso interno,
  profesional, académico y de investigación, pero prohíbe —sin autorización
  escrita del autor— usar el material dentro de una oferta comercial de
  servicios legales, cursos o consultoría de pago. Si el uso en la clínica
  dejara de ser interno, hay que pedir autorización a joelgomez@abogado.digital.
- **Atribución obligatoria** al compartir o adaptar el material: Joel Gómez
  Treviño, *Corporate Law Expert MX*, https://github.com/abogadodigital/Corporate-Law-Expert-MX,
  CC BY-NC-SA 4.0.
- **No es asesoría jurídica.** Todo dictamen, escrito o borrador que produzca
  requiere revisión de un abogado antes de usarse.
- **Fechas de corte.** El texto de la LGSM refleja la última reforma publicada
  en el DOF el 20-10-2023 (cantidades actualizadas por acuerdo DOF 26-12-2025) y
  el corpus jurisprudencial, una investigación al 18 de agosto de 2026. Verifica
  vigencia en https://www.dof.gob.mx, https://www.diputados.gob.mx/LeyesBiblio/
  y https://sjf2.scjn.gob.mx antes de invocar una disposición o criterio.
