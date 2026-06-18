import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import webbrowser, subprocess, os, sys, shutil, math, random, json, threading
import urllib.request, urllib.parse, uuid, platform

# ─── PALETA NUEVA — DARK GLASSMORPHISM ───────────────────────────────
# Fondos: carbón y negro profundo con capas
BG_DEEP    = "#0A0A0F"          # negro profundo — fondo base
BG_PANEL   = "#0F0F18"          # carbón oscuro — sidebar
BG_CARD    = "#16161F"          # cristal oscuro — tarjetas base
BG_CARD2   = "#1C1C28"          # cristal medio — tarjetas hover / inputs

# Glassmorphism — capas translúcidas con brillo de borde
GLASS_BG   = "#12121C"          # fondo cristal principal
GLASS_BG2  = "#1A1A26"          # fondo cristal secundario
GLASS_EDGE = "#2A2A3E"          # borde iluminado del cristal
GLASS_GLOW = "#1E1E30"          # brillo interior del panel

# Acento naranja — se mantiene del original (señal de marca)
ACCENT     = "#FF7A29"          # naranja vivo — marca Crust Engine
ACCENT2    = "#FF9D50"          # naranja cálido — hover / subtítulos
ACCENT_DIM = "#1F140A"          # naranja atenuado — fondo activo nav
ACCENT_GLOW= "#FF7A2918"        # destello naranja muy sutil

# Texto — escala desde blanco hasta invisible
TEXT_MAIN  = "#E8E8F0"          # blanco azulado — texto principal
TEXT_MUTED = "#7A7A9A"          # gris azulado — texto secundario
TEXT_HINT  = "#3A3A52"          # gris oscuro — texto fantasma

# Bordes y separadores
BORDER     = "#22223A"          # borde sutil entre paneles
BORDER_LIT = "#32325A"          # borde iluminado (hover / activo)

# Colores de acento adicionales
GOLD       = "#F0C050"          # ámbar / dorado
GOLD_DIM   = "#1A160A"
RED        = "#F06060"
BLUE       = "#5B9BF5"
TEAL       = "#50D0C8"          # nuevo acento frío para variedad

# ─── TIPOGRAFÍA GEOMÉTRICA MODERNA ───────────────────────────────────
# Segoe UI Variable / Segoe UI como fallback sans-serif geométrico
# para los títulos; Consolas para datos monoespaciados
FONT_LOGO   = ("Segoe UI", 13, "bold")       # logo sidebar
FONT_HEAD   = ("Segoe UI", 13, "bold")       # encabezados de sección
FONT_BODY   = ("Segoe UI", 10)               # texto de cuerpo
FONT_SMALL  = ("Segoe UI", 9)                # etiquetas pequeñas
FONT_MONO   = ("Consolas", 10)               # datos / código
FONT_MONO_S = ("Consolas", 9)                # metadatos / pie
FONT_STAT   = ("Segoe UI", 22, "bold")       # números grandes en stats

MODPACK = {
    "name": "Crust Engine", "ver": "1.0.0",
    "mc": "1.21.8", "loader": "Fabric",
    "author": "Torrijaslover", "mods": 42,
    "desc": "El modpack de rendimiento definitivo para Minecraft 1.21.8.\nDiseñado con Fabric para exprimir cada FPS posible.",
}

MODS = [
    ("Sodium","Render","Motor gráfico moderno — hasta 3× más FPS"),
    ("Lithium","Optimización","Lógica del servidor acelerada al máximo"),
    ("Starlight","Iluminación","Motor de luz completamente reescrito"),
    ("FerriteCore","Memoria","Reduce el uso de RAM significativamente"),
    ("EntityCulling","Render","Omite entidades fuera del campo visual"),
    ("ImmediatelyFast","GUI/HUD","Renderizado de interfaz ultrarrápido"),
    ("ModernFix","Carga","Reduce tiempos de carga brutalmente"),
    ("Krypton","Red","Optimiza el protocolo de red"),
    ("Noisium","Mundo","Generación de chunks más rápida"),
    ("Concurrent Chunk Migration","Chunks","Carga de chunks en paralelo"),
    ("Indium","Compat.","API de render para mods de terceros"),
    ("Iris Shaders","Shaders","Soporte de shaders compatible con Sodium"),
    ("Dynamic FPS","FPS","Limita FPS en segundo plano y menús"),
    ("LazyDFU","Carga","Retrasa la inicialización innecesaria de DFU"),
    ("Smooth Boot","Carga","Distribuye la carga inicial uniformemente"),
    ("Memory Leak Fix","Memoria","Parchea fugas de memoria del juego base"),
    ("Exordium","GUI","Reduce carga del renderizado de GUIs"),
    ("Clumps","Entidades","Agrupa orbes de XP para mejor rendimiento"),
    ("FastAnim","Animaciones","Acelera cálculos de animaciones"),
    ("No Chat Reports","Privacidad","Elimina el sistema de reportes de chat"),
    ("Reese's Sodium Options","Config","Menú de opciones ampliado para Sodium"),
    ("Sodium Extra","Render","Opciones adicionales para Sodium"),
]

SERVERS = [
    ("DiosesMC","mc.diosesmc.net","El survival roleado de Vegetta y Willyrex · Java 1.13-1.21",ACCENT),
    ("LemonCloud","one.lemoncloud.net","Skyblock, Factions, Prison, Cobblemon · activo",ACCENT2),
    ("Cubeland","cubeland.es","Survival y Box PvP · comunidad española desde 2014",GOLD),
    ("VanillaLand","mc.vanillaland.es","Survival vanilla puro · comunidad activa",TEXT_MUTED),
    ("CraftMania","play.craftmania.es","Skyblock, Prison, Facciones y Survival",BLUE),
]

LINKS = [
    ("Modrinth","https://modrinth.com","Descarga el modpack",ACCENT),
    ("CurseForge","https://curseforge.com","Alternativa de descarga",ACCENT2),
    ("Discord","https://discord.gg","Únete a la comunidad","#7289DA"),
    ("GitHub","https://github.com","Código fuente y bugs",TEXT_MUTED),
    ("Java 21","https://adoptium.net","Descargar Java 21",GOLD),
]

PRIVACY_TEXT = """POLÍTICA DE PRIVACIDAD Y PROTECCIÓN DE DATOS
Crust Engine Launcher — Versión 1.0.0
Autor: Torrijaslover | Fecha: Junio 2026

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. RESPONSABLE DEL TRATAMIENTO
   Torrijaslover, creador del modpack Crust Engine,
   actúa como responsable del tratamiento de los datos
   personales que puedas proporcionar voluntariamente
   a través de este launcher.

2. DATOS QUE SE RECOGEN
   • Nick de Minecraft: introducido voluntariamente por
     el usuario para mostrar la cabeza del personaje.
     Este dato se guarda localmente en un archivo
     config.json dentro de la carpeta de datos de tu
     usuario (no en el propio launcher), solo en tu PC,
     y nunca se envía a servidores externos.
   • Componentes del sistema: el launcher puede leer
     información de hardware local (CPU, RAM, GPU)
     únicamente para ofrecer recomendaciones de
     rendimiento. Estos datos NO se envían a ningún
     servidor externo.
   • Centro de ayuda: las preguntas que escribes en la
     sección de Ayuda se procesan ÍNTEGRAMENTE en tu
     propio ordenador (respuestas predefinidas). No se
     envían a Anthropic ni a ningún otro servidor, y no
     requieren conexión a internet.

3. FINALIDAD DEL TRATAMIENTO
   Los datos se usan exclusivamente para:
   • Mostrar la skin/cabeza de tu personaje (nick)
   • Verificar compatibilidad de tu PC (hardware)
   • Responder preguntas frecuentes sobre el modpack
     (Centro de Ayuda, totalmente local)
   Ningún dato se usa con fines comerciales ni
   se comparte con terceros salvo lo indicado en §2.

4. BASE LEGAL (RGPD Art. 6.1.a)
   El tratamiento se basa en el consentimiento
   expreso del usuario al introducir sus datos
   voluntariamente en el launcher.

5. DERECHOS DEL USUARIO
   Conforme al RGPD y la LOPDGDD puedes ejercer:
   • Acceso, rectificación y supresión de tus datos
   • Oposición y limitación del tratamiento
   • Portabilidad de los datos
   Para suprimir tu nick guardado, usa el botón
   "Borrar nick guardado" dentro del launcher
   (recomendado), o borra manualmente el archivo
   config.json de la carpeta de datos de la aplicación.

6. TRANSFERENCIAS INTERNACIONALES
   Este launcher no envía datos a servidores externos
   para el Centro de Ayuda: las respuestas son
   predefinidas y se generan localmente en tu equipo,
   sin conexión a internet ni a terceros.

7. CONSERVACIÓN
   El nick se guarda localmente hasta que el usuario
   lo borre. El resto de datos son temporales en RAM.

8. SEGURIDAD
   Este launcher es software de código abierto.
   No recopila contraseñas, tokens ni credenciales
   de Minecraft en ningún momento.

9. CONTACTO
   Para cualquier consulta sobre privacidad,
   puedes abrir un issue en el repositorio GitHub
   del proyecto.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Al usar este launcher aceptas esta política.
Última actualización: Junio 2026
"""

HELP_FAQ = [
    {
        "label": "¿Cómo instalo el pack?",
        "keywords": ["instal", "descarg", "como empiezo", "primeros pasos", "setup", "configurar el pack"],
        "answer": (
            "Para instalar Crust Engine sigue estos pasos:\n\n"
            "1. Instala Java 21 desde adoptium.net (sección Enlaces).\n"
            "2. Descarga el modpack desde Modrinth o CurseForge (sección Enlaces).\n"
            "3. Abre tu launcher de mods (Prism Launcher es el recomendado) y crea\n"
            "   un perfil con Minecraft 1.21.8 y loader Fabric.\n"
            "4. Coloca los 42 mods del pack en la carpeta 'mods' de ese perfil.\n"
            "5. Vuelve aquí y pulsa ▶ JUGAR — se abrirá tu launcher para que\n"
            "   selecciones ese perfil.\n\n"
            "Nota: este launcher no instala los mods por ti, solo abre tu\n"
            "launcher de Minecraft. El perfil con Fabric y los mods debe\n"
            "estar preparado de antemano."
        ),
    },
    {
        "label": "¿Qué hace Sodium?",
        "keywords": ["sodium"],
        "answer": (
            "Sodium es el mod de renderizado principal del pack: reescribe el\n"
            "motor gráfico de Minecraft (sin cambiar el aspecto del juego) y\n"
            "puede multiplicar tus FPS hasta 3×.\n\n"
            "Trabaja junto a:\n"
            "• Iris Shaders — soporte de shaders compatible con Sodium\n"
            "• Indium — API de render para mods de terceros\n"
            "• Sodium Extra / Reese's Sodium Options — opciones extra\n\n"
            "Puedes ver los 42 mods completos en la sección Mods."
        ),
    },
    {
        "label": "Flags JVM recomendadas",
        "keywords": ["jvm", "flag", "argumento", "ram", "memoria asign"],
        "answer": (
            "Argumentos de JVM recomendados (pégalos en tu launcher, en\n"
            "Configuración → Java/JVM Arguments):\n\n"
            "-Xms4G -Xmx8G -XX:+UseG1GC -XX:+ParallelRefProcEnabled\n"
            "-XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions\n"
            "-XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40\n"
            "-XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20\n"
            "-XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4\n"
            "-XX:InitiatingHeapOccupancyPercent=15\n\n"
            "Ajusta -Xmx8G según tu RAM (recomendado: hasta la mitad de tu\n"
            "RAM total). Necesitas Java 21 instalado."
        ),
    },
    {
        "label": "Requisitos mínimos",
        "keywords": ["requisito", "minimo", "especificacion", "spec", "necesito para jugar"],
        "answer": (
            "Requisitos para Crust Engine (MC 1.21.8 · Fabric):\n\n"
            "MÍNIMOS:\n"
            "• 4 GB de RAM asignada\n"
            "• Java 21\n"
            "• CPU de 4 núcleos\n\n"
            "RECOMENDADOS:\n"
            "• 8 GB de RAM asignada\n"
            "• Java 21 (GraalVM recomendado)\n"
            "• GPU GTX 1060 o superior\n\n"
            "Más detalles en la sección Requisitos."
        ),
    },
    {
        "label": None,
        "keywords": ["shader", "iris"],
        "answer": (
            "Iris Shaders viene incluido en el pack y añade soporte de\n"
            "shaders compatible con Sodium. Para activarlos: Opciones de\n"
            "vídeo → Shaderpacks, coloca el .zip del shader en esa carpeta y\n"
            "selecciónalo. Ten en cuenta que los shaders bajan bastante el\n"
            "rendimiento, así que prueba primero sin ellos."
        ),
    },
    {
        "label": None,
        "keywords": ["lag", "fps", "rendimiento", "rinde", "va lento", "tiron", "va mal"],
        "answer": (
            "Si el rendimiento no es bueno, prueba en este orden:\n\n"
            "1. Revisa las flags JVM recomendadas (pregunta 'Flags JVM').\n"
            "2. Baja la distancia de renderizado en Opciones de vídeo.\n"
            "3. Comprueba que tienes Java 21 (no una versión más antigua).\n"
            "4. Asegúrate de no tener mods duplicados o conflictivos.\n"
            "5. Cierra los shaders si los tienes activados — bajan mucho los FPS."
        ),
    },
    {
        "label": None,
        "keywords": ["crash", "error", "se cierra", "se ha cerrado", "falla", "no abre", "no arranca"],
        "answer": (
            "Si el juego crashea o no arranca:\n\n"
            "1. Comprueba que el perfil usa Java 21 y loader Fabric.\n"
            "2. Revisa que no falte ningún mod de los 42 del pack.\n"
            "3. Mira el log de crash de tu launcher (carpeta 'crash-reports').\n"
            "4. Si sigue sin funcionar, pide ayuda en el Discord de la\n"
            "   comunidad (sección Enlaces) y adjunta el log."
        ),
    },
    {
        "label": None,
        "keywords": ["servidor", "conectar a un server", " ip "],
        "answer": (
            "Tienes varios servidores recomendados y compatibles con el pack\n"
            "en la sección Servidores: DiosesMC, LemonCloud, Cubeland,\n"
            "VanillaLand y CraftMania. Échales un vistazo allí."
        ),
    },
    {
        "label": None,
        "keywords": ["discord", "comunidad", "contacto", "soporte"],
        "answer": (
            "Puedes unirte a la comunidad y pedir ayuda en el Discord —\n"
            "lo encuentras en la sección Enlaces."
        ),
    },
]

HELP_DEFAULT_ANSWER = (
    "No tengo una respuesta predefinida para eso todavía.\n\n"
    "Prueba con una de las preguntas rápidas de abajo, o consulta las\n"
    "secciones Mods, Requisitos o Servidores. También puedes preguntar\n"
    "en el Discord de la comunidad (sección Enlaces)."
)

QUICK_HELP_QUESTIONS = [item["label"] for item in HELP_FAQ if item["label"]]
_QUICK_HELP_ANSWERS  = {item["label"]: item["answer"] for item in HELP_FAQ if item["label"]}

def get_help_answer(text):
    """Devuelve una respuesta predefinida según palabras clave — no hay
    llamada a ninguna IA ni API, todo es local e instantáneo."""
    if text in _QUICK_HELP_ANSWERS:
        return _QUICK_HELP_ANSWERS[text]
    t = text.lower()
    for item in HELP_FAQ:
        for kw in item["keywords"]:
            if kw in t:
                return item["answer"]
    return HELP_DEFAULT_ANSWER

# ─── RUTAS DE CONFIG ─────────────────────────────────────────────────
# IMPORTANTE: antes config.json se guardaba "junto al script". Eso falla
# en silencio en dos casos muy comunes:
#   1) El launcher está compilado con PyInstaller -> __file__ apunta a una
#      carpeta temporal (_MEIxxxxx) que Windows BORRA al cerrar el programa,
#      así que el nick "se guardaba" pero desaparecía siempre al reabrir.
#   2) El .exe vive en "Archivos de programa" -> esa carpeta no es escribible
#      sin permisos de administrador, así que el guardado fallaba sin avisar.
# Solución: usar siempre una carpeta de datos de usuario garantizada-escribible
# (igual que hacen Discord, Spotify, etc.), independientemente de dónde esté
# el ejecutable o de si se ejecuta empaquetado o como script .py.
def _app_data_dir():
    if os.name == "nt":
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    folder = os.path.join(base, "CrustEngineLauncher")
    try:
        os.makedirs(folder, exist_ok=True)
    except Exception:
        # Si por lo que sea esa carpeta no es escribible, usamos la carpeta
        # del propio ejecutable/script como último recurso.
        folder = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
    return folder

CONFIG_FILE = os.path.join(_app_data_dir(), "config.json")

def _migrate_legacy_config():
    """Si existe un config.json antiguo junto al .exe/.py (versiones previas),
    lo importa una vez a la nueva ubicación para que el usuario no pierda su nick."""
    try:
        legacy_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
        legacy_path = os.path.join(legacy_dir, "config.json")
        if os.path.exists(legacy_path) and not os.path.exists(CONFIG_FILE):
            with open(legacy_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

_migrate_legacy_config()

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_config(data):
    """Guarda la config de forma atómica (escribe a .tmp y luego renombra,
    para no corromper el archivo si se cierra la app a mitad de escritura).
    Devuelve True/False — antes los fallos se tragaban en silencio, lo que
    hacía parecer que el nick simplemente "no se guardaba"."""
    try:
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        tmp_path = CONFIG_FILE + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, CONFIG_FILE)
        return True
    except Exception as e:
        print(f"[CrustEngine] No se pudo guardar config.json: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════
#  NÚCLEO DE LANZAMIENTO PROPIO — minecraft-launcher-lib
# ═══════════════════════════════════════════════════════════════════

def _check_mll_installed():
    """Comprueba si minecraft-launcher-lib está instalado."""
    try:
        import minecraft_launcher_lib  # noqa: F401
        return True
    except ImportError:
        return False

def _install_mll():
    """Instala minecraft-launcher-lib via pip. Devuelve (ok, msg).

    IMPORTANTE: esto SOLO puede funcionar cuando el launcher se ejecuta
    como script .py con un Python normal instalado (p. ej. via el .bat).
    Dentro de un .exe compilado con PyInstaller, sys.executable apunta al
    propio .exe (no hay ningún "pip" real ahí dentro), así que intentar
    "sys.executable -m pip install ..." en ese caso NO instala nada: en
    el mejor de los casos no hace nada y en el peor relanza una segunda
    copia del propio launcher y se queda colgado hasta el timeout.
    Por eso, si detectamos que estamos congelados (frozen), ni lo
    intentamos: directamente avisamos de que hay que volver a compilar
    el .exe con la librería ya instalada en el entorno de PyInstaller."""
    if getattr(sys, "frozen", False):
        return False, (
            "Esta versión compilada (.exe) no incluye 'minecraft-launcher-lib'.\n\n"
            "No se puede instalar en caliente dentro de un .exe: hay que volver "
            "a generar el ejecutable después de instalar la librería en el "
            "Python que usas para compilar, por ejemplo:\n\n"
            "  pip install minecraft-launcher-lib\n"
            "  pyinstaller --onefile --noconsole crust_engine_launcher.py\n\n"
            "Una vez recompilado, el .exe funcionará igual que el .bat."
        )
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "minecraft-launcher-lib"],
            capture_output=True, text=True, timeout=180
        )
        if result.returncode == 0:
            return True, "OK"
        return False, result.stderr.strip()
    except Exception as e:
        return False, str(e)

def _get_minecraft_dir():
    """Carpeta de datos de Crust Engine (independiente de .minecraft oficial)."""
    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~")
    folder = os.path.join(base, "CrustEngine")
    os.makedirs(folder, exist_ok=True)
    return folder

def _find_java():
    """Busca java 17+ instalado en el sistema."""
    java = shutil.which("java") or shutil.which("java.exe")
    if java:
        return java
    if os.name == "nt":
        localappdata = os.environ.get("LOCALAPPDATA", "")
        progfiles    = os.environ.get("PROGRAMFILES", "")
        progfiles86  = os.environ.get("PROGRAMFILES(X86)", "")
        for base in [localappdata, progfiles, progfiles86]:
            for vendor in ["Eclipse Adoptium", "Microsoft", "Java",
                           "OpenJDK", "BellSoft", "Amazon Corretto"]:
                folder = os.path.join(base, vendor)
                if not os.path.isdir(folder):
                    continue
                for name in sorted(os.listdir(folder), reverse=True):
                    exe = os.path.join(folder, name, "bin", "java.exe")
                    if os.path.exists(exe):
                        return exe
    return None

def _get_fabric_version_id(mc_version, mc_dir):
    """Devuelve el ID de la versión de Fabric instalada para mc_version, o None."""
    try:
        import minecraft_launcher_lib
        installed = minecraft_launcher_lib.utils.get_installed_versions(mc_dir)
        for v in installed:
            vid = v.get("id", "")
            if mc_version in vid and vid.startswith("fabric-loader-"):
                return vid
    except Exception:
        pass
    return None

# ═══════════════════════════════════════════════════════════════════
#  CUENTA MICROSOFT (premium) — login real, para que tu skin de
#  verdad aparezca en el juego (en vez del Steve/Alex por defecto del
#  modo offline).
# ═══════════════════════════════════════════════════════════════════
# Esto requiere registrar una app GRATUITA propia en Azure (Microsoft
# no deja usar el client_id del launcher oficial de Mojang). Pasos:
#   1. Entra en https://portal.azure.com -> "Microsoft Entra ID"
#      -> "Registros de aplicaciones" -> "Nuevo registro".
#   2. Nombre: el que quieras (p. ej. "Crust Engine Launcher").
#   3. Tipos de cuenta admitidos: "Cuentas en cualquier organización
#      y cuentas personales de Microsoft".
#   4. Plataforma -> "Agregar una plataforma" -> "Aplicaciones
#      móviles y de escritorio" -> en "URI de redirección
#      personalizadas" añade EXACTAMENTE:   http://localhost
#      (sin puerto: Microsoft permite cualquier puerto en esa URI
#      especial para apps de escritorio).
#   5. Copia el "Id. de aplicación (cliente)" de la página de
#      Información general y pégalo aquí abajo. No hace falta
#      client secret (es una app "pública").
MS_CLIENT_ID = "4568ab5d-6908-473f-89a2-969f52f63cd5"


def _ms_configured():
    return bool(MS_CLIENT_ID) and MS_CLIENT_ID != "PON_AQUI_TU_CLIENT_ID_DE_AZURE"


def _free_local_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _ms_oauth_login(timeout=180):
    """Abre el navegador para iniciar sesión con Microsoft y captura la
    redirección con un mini-servidor local (el usuario no tiene que
    copiar/pegar ninguna URL). Devuelve (account_info, error_msg)."""
    if not _ms_configured():
        return None, ("No se ha configurado MS_CLIENT_ID en el código del "
                       "launcher. Hay que registrar una app en "
                       "portal.azure.com y pegar el Client ID en la "
                       "constante MS_CLIENT_ID.")
    try:
        import minecraft_launcher_lib as mll
        import http.server
    except Exception as e:
        return None, f"Falta una dependencia: {e}"

    port = _free_local_port()
    redirect_uri = f"http://localhost:{port}"

    try:
        login_url, state, code_verifier = mll.microsoft_account.get_secure_login_data(
            MS_CLIENT_ID, redirect_uri)
    except Exception as e:
        return None, f"No se pudo generar la URL de login: {e}"

    captured = {}

    class _Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            captured["url"] = f"{redirect_uri}{self.path}"
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write((
                "<html><body style='font-family:sans-serif;text-align:"
                "center;padding-top:80px;background:#0A0A0F;color:#E8E8F0'>"
                "<h2>Sesion iniciada ✔</h2>"
                "<p>Ya puedes cerrar esta pestana y volver al launcher.</p>"
                "</body></html>").encode("utf-8"))

        def log_message(self, *a, **k):
            pass

    try:
        server = http.server.HTTPServer(("127.0.0.1", port), _Handler)
    except OSError as e:
        return None, f"No se pudo abrir el servidor local de login: {e}"
    server.timeout = timeout

    webbrowser.open(login_url)
    server.handle_request()  # bloquea hasta la primera petición o el timeout
    try:
        server.server_close()
    except Exception:
        pass

    if "url" not in captured:
        return None, "No se completó el login a tiempo (¿se cerró el navegador antes de terminar?)."

    try:
        auth_code = mll.microsoft_account.get_auth_code_from_url(captured["url"])
        account = mll.microsoft_account.complete_login(
            MS_CLIENT_ID, None, redirect_uri, auth_code, code_verifier)
        return account, None
    except Exception as e:
        return None, str(e)


def _ms_refresh(refresh_token):
    """Refresca una sesión de Microsoft ya existente, sin abrir el
    navegador. Devuelve (account_info, error_msg)."""
    if not _ms_configured():
        return None, "MS_CLIENT_ID no configurado."
    try:
        import minecraft_launcher_lib as mll
        account = mll.microsoft_account.complete_refresh(
            MS_CLIENT_ID, None, None, refresh_token)
        return account, None
    except Exception as e:
        return None, str(e)


def animate_hover(widget, bg_normal, bg_hover, fg_normal=None, fg_hover=None):
    """Aplica animación de hover suave a un widget Button o Label clickeable."""
    def on_enter(e):
        widget.config(bg=bg_hover)
        if fg_hover and fg_normal:
            widget.config(fg=fg_hover)
    def on_leave(e):
        widget.config(bg=bg_normal)
        if fg_normal:
            widget.config(fg=fg_normal)
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)

def animate_click(widget, bg_normal, bg_hover, bg_click):
    """Aplica efecto visual de click (flash) a un botón."""
    def on_press(e):
        widget.config(bg=bg_click)
    def on_release(e):
        widget.config(bg=bg_hover)
        widget.after(120, lambda: widget.config(bg=bg_normal))
    widget.bind("<ButtonPress-1>", on_press)
    widget.bind("<ButtonRelease-1>", on_release)

def animate_card(card, bg_normal, bg_hover, children=None):
    """Aplica hover a una tarjeta completa y sus hijos."""
    def on_enter(e):
        card.config(bg=bg_hover)
        if children:
            for ch in children:
                try: ch.config(bg=bg_hover)
                except Exception: pass
    def on_leave(e):
        card.config(bg=bg_normal)
        if children:
            for ch in children:
                try: ch.config(bg=bg_normal)
                except Exception: pass
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    if children:
        for ch in children:
            ch.bind("<Enter>", on_enter)
            ch.bind("<Leave>", on_leave)

def make_animated_button(parent, text, command, fg=BG_DEEP, bg=ACCENT,
                          hover_bg=None, click_bg=None,
                          font=FONT_BODY, padx=8, pady=4, cursor="hand2", **kw):
    """Crea un botón con animaciones hover y click integradas."""
    if hover_bg is None:
        # Ligeramente más brillante que bg
        hover_bg = ACCENT2 if bg == ACCENT else bg
    if click_bg is None:
        click_bg = BG_CARD2 if bg in (BG_CARD, BG_PANEL) else ACCENT_DIM

    btn = tk.Button(parent, text=text, font=font, fg=fg, bg=bg,
                    activeforeground=fg, activebackground=hover_bg,
                    relief="flat", bd=0, padx=padx, pady=pady,
                    cursor=cursor, command=command, **kw)
    animate_hover(btn, bg, hover_bg)
    animate_click(btn, bg, hover_bg, click_bg)
    return btn


# ═══════════════════════════════════════════════════════════════════
#  PARTÍCULAS
# ═══════════════════════════════════════════════════════════════════
class Particles(tk.Canvas):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BG_DEEP, highlightthickness=0, **kw)
        self._running = True; self._p = []
        self.after(120, self._init)

    def _init(self):
        w = self.winfo_width() or 700
        h = self.winfo_height() or 600
        cols = ["#16162A","#1A1A30","#12122A","#1E1E35","#141425"]
        for _ in range(22):
            sz  = random.choice([4,6,8])
            clr = random.choice(cols)
            x   = random.uniform(0, w)
            y   = random.uniform(0, h)
            vy  = random.uniform(-0.25, -0.07)
            iid = self.create_rectangle(x, y, x+sz, y+sz, fill=clr, outline="")
            self._p.append({"id":iid,"x":x,"y":y,"sz":sz,"vy":vy,"w":w,"h":h})
        self._tick()

    def _tick(self):
        if not self._running: return
        for p in self._p:
            p["y"] += p["vy"]
            if p["y"]+p["sz"] < 0:
                p["y"] = p["h"]+p["sz"]
                p["x"] = random.uniform(0, p["w"])
            self.coords(p["id"], p["x"], p["y"], p["x"]+p["sz"], p["y"]+p["sz"])
        self.after(40, self._tick)

    def stop(self): self._running = False


# ═══════════════════════════════════════════════════════════════════
#  LAUNCHER PRINCIPAL
# ═══════════════════════════════════════════════════════════════════
class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crust Engine Launcher")
        self.geometry("1020x680")
        self.configure(bg=BG_DEEP)
        # OBLIGATORIO: la ventana SOLO puede abrirse en modo ventana, nunca
        # a pantalla completa ni maximizada. resizable(False, False) anula
        # el botón de maximizar y el doble clic en la barra de título en
        # Windows/macOS/Linux. Además, por si algún gestor de ventanas
        # forzara el estado "zoomed" (p. ej. al arrastrar a una esquina o
        # con el atajo del sistema), lo detectamos y lo revertimos al
        # instante a tamaño normal.
        self.resizable(False, False)
        self.bind("<Configure>", self._block_fullscreen)
        try: self.iconbitmap("icon.ico")
        except: pass

        # Cargar config guardada
        cfg = load_config()
        self._player_nick = tk.StringVar(value=cfg.get("nick", ""))
        self._config      = cfg
        self._build()

    def _block_fullscreen(self, event=None):
        """Si el sistema operativo intenta maximizar/pantalla-completa la
        ventana, la devolvemos de inmediato a su tamaño de ventana normal."""
        try:
            if self.state() == "zoomed":
                self.state("normal")
                self.geometry("1020x680")
        except tk.TclError:
            pass

    def _save_nick(self, nick):
        """Guarda el nick en config.json y en memoria. Si falla, avisa (antes
        fallaba en silencio y parecía que el nick simplemente no se guardaba)."""
        self._config["nick"] = nick
        ok = save_config(self._config)
        if not ok:
            messagebox.showwarning(
                "No se pudo guardar",
                "No se pudo guardar tu nick en el disco.\n"
                "Comprueba que el launcher tiene permisos de escritura en:\n"
                f"{CONFIG_FILE}")
        self._refresh_sidebar_session()
        return ok

    def _build(self):
        root = tk.Frame(self, bg=BG_DEEP)
        root.pack(fill="both", expand=True)
        self._build_sidebar(root)
        right = tk.Frame(root, bg=BG_DEEP)
        right.pack(side="left", fill="both", expand=True)
        self._particles = Particles(right)
        self._particles.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._content = tk.Frame(right, bg=BG_DEEP)
        self._content.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._goto("home")

    def _build_sidebar(self, parent):
        # Sidebar principal con fondo de cristal oscuro
        sb = tk.Frame(parent, bg=BG_PANEL, width=220)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        # ── Logo / marca ─────────────────────────────────────────────
        lf = tk.Frame(sb, bg=BG_PANEL)
        lf.pack(fill="x", padx=18, pady=(26, 8))

        # Icono cuadrado — cuatro cuadros en naranja / amber
        bc = tk.Canvas(lf, width=36, height=36, bg=BG_PANEL, highlightthickness=0)
        bc.pack(side="left", padx=(0, 12))
        # Fondo con borde iluminado
        bc.create_rectangle(0, 0, 36, 36, fill=GLASS_BG, outline=ACCENT, width=1)
        # Cuatro bloques geométricos — identidad visual Crust Engine
        bc.create_rectangle(4,  4, 15, 15, fill=ACCENT,  outline="")
        bc.create_rectangle(21, 4, 32, 15, fill=ACCENT,  outline="")
        bc.create_rectangle(4, 21, 15, 32, fill=ACCENT2, outline="")
        bc.create_rectangle(21,21, 32, 32, fill=ACCENT2, outline="")

        nf = tk.Frame(lf, bg=BG_PANEL)
        nf.pack(side="left")
        tk.Label(nf, text="CRUST",  font=("Segoe UI", 14, "bold"), fg=ACCENT,  bg=BG_PANEL).pack(anchor="w")
        tk.Label(nf, text="ENGINE", font=("Segoe UI", 14, "bold"), fg=ACCENT2, bg=BG_PANEL).pack(anchor="w")

        # Metadatos de versión
        tk.Label(sb, text=f"v{MODPACK['ver']}  ·  MC {MODPACK['mc']}",
                 font=FONT_MONO_S, fg=TEXT_MUTED, bg=BG_PANEL).pack(pady=(0, 2))
        tk.Label(sb, text=f"by {MODPACK['author']}",
                 font=("Segoe UI", 9, "italic"), fg=TEXT_HINT, bg=BG_PANEL).pack(pady=(0, 16))

        # Separador iluminado
        tk.Frame(sb, bg=BORDER_LIT, height=1).pack(fill="x", padx=16, pady=4)

        # ── Navegación ───────────────────────────────────────────────
        nav = [
            ("home",    "  Inicio"),
            ("player",  "  Mi Perfil"),
            ("mods",    "  Mods"),
            ("servers", "  Servidores"),
            ("specs",   "  Requisitos"),
            ("ai",      "  Ayuda"),
            ("links",   "  Enlaces"),
            ("privacy", "  Privacidad"),
        ]
        self._nav_btns = {}
        for key, label in nav:
            b = tk.Button(sb, text=label, font=("Segoe UI", 10), anchor="w",
                          fg=TEXT_MUTED, bg=BG_PANEL,
                          activeforeground=ACCENT, activebackground=ACCENT_DIM,
                          relief="flat", bd=0, padx=20, pady=9, cursor="hand2",
                          command=lambda k=key: self._goto(k))
            b.pack(fill="x")
            self._nav_btns[key] = b

            def _nav_enter(e, btn=b):
                if btn.cget("bg") != ACCENT_DIM:
                    btn.config(bg=GLASS_BG2, fg=TEXT_MAIN)
            def _nav_leave(e, btn=b):
                if btn.cget("bg") != ACCENT_DIM:
                    btn.config(bg=BG_PANEL, fg=TEXT_MUTED)
            def _nav_press(e, btn=b):
                btn.config(bg=GLASS_EDGE)
            b.bind("<Enter>", _nav_enter)
            b.bind("<Leave>", _nav_leave)
            b.bind("<ButtonPress-1>", _nav_press)

        tk.Frame(sb, bg=BG_PANEL).pack(fill="both", expand=True)
        tk.Frame(sb, bg=BORDER_LIT, height=1).pack(fill="x", padx=16, pady=(0, 8))

        # ── Widget de sesión (nick + cabeza), justo encima de "● Listo" ──
        self._session_frame = tk.Frame(sb, bg=BG_PANEL)
        self._session_frame.pack(fill="x", padx=14, pady=(0, 8))
        self._build_session_widget()

        self._status_lbl = tk.Label(sb, text="● Listo", font=FONT_MONO_S,
                                    fg=ACCENT2, bg=BG_PANEL)
        self._status_lbl.pack(padx=20, anchor="w")

        # Botón JUGAR — estilo moderno con acento naranja
        play_btn = tk.Button(sb, text="▶  JUGAR", font=("Segoe UI", 12, "bold"),
                  fg="#0A0A0F", bg=ACCENT, activeforeground="#0A0A0F",
                  activebackground=ACCENT2, relief="flat", bd=0, pady=14,
                  cursor="hand2", command=self._launch)
        play_btn.pack(fill="x", padx=16, pady=(8, 22))
        animate_hover(play_btn, ACCENT, ACCENT2)
        animate_click(play_btn, ACCENT, ACCENT2, "#E85A10")

    # ── WIDGET DE SESIÓN (nick + cabeza, estilo "login") ────────────
    def _build_session_widget(self):
        """Dibuja, justo encima de '● Listo', un mini bloque tipo 'sesión
        iniciada como <nick>' con la cabeza del personaje al lado — igual
        que muestra cualquier launcher oficial tras iniciar sesión.
        Si hay una cuenta Microsoft vinculada, esa tiene prioridad sobre
        el nick offline (porque con ella se ve la skin real en el juego)."""
        for w in self._session_frame.winfo_children():
            w.destroy()

        ms = self._config.get("ms_account") or {}
        ms_name = ms.get("name", "")
        offline_nick = self._config.get("nick", "")
        display_name = ms_name or offline_nick

        row = tk.Frame(self._session_frame, bg=BG_CARD, cursor="hand2")
        row.pack(fill="x")

        avatar_holder = tk.Frame(row, bg=BG_CARD2, width=32, height=32)
        avatar_holder.pack(side="left", padx=(8, 10), pady=8)
        avatar_holder.pack_propagate(False)
        self._session_avatar_holder = avatar_holder
        self._draw_avatar_placeholder(avatar_holder, ok=bool(display_name))

        text_col = tk.Frame(row, bg=BG_CARD)
        text_col.pack(side="left", fill="both", expand=True, pady=8)
        if ms_name:
            tk.Label(text_col, text=ms_name, font=("Segoe UI", 10, "bold"),
                     fg=TEXT_MAIN, bg=BG_CARD, anchor="w").pack(anchor="w")
            tk.Label(text_col, text="✔ Premium · skin real", font=("Segoe UI", 8),
                     fg=GOLD, bg=BG_CARD, anchor="w").pack(anchor="w")
        elif offline_nick:
            tk.Label(text_col, text=offline_nick, font=("Segoe UI", 10, "bold"),
                     fg=TEXT_MAIN, bg=BG_CARD, anchor="w").pack(anchor="w")
            tk.Label(text_col, text="✔ Sesión iniciada (offline)", font=("Segoe UI", 8),
                     fg=ACCENT2, bg=BG_CARD, anchor="w").pack(anchor="w")
        else:
            tk.Label(text_col, text="Sin sesión", font=("Segoe UI", 9),
                     fg=TEXT_MUTED, bg=BG_CARD, anchor="w").pack(anchor="w")
            tk.Label(text_col, text="Pulsa para iniciar →", font=("Segoe UI", 8),
                     fg=TEXT_HINT, bg=BG_CARD, anchor="w").pack(anchor="w")

        clickable = [row, avatar_holder, text_col] + text_col.winfo_children()
        for w in clickable:
            w.bind("<Button-1>", lambda e: self._goto("player"))
        animate_card(row, BG_CARD, GLASS_BG2, [avatar_holder, text_col] + text_col.winfo_children())

        if display_name:
            self._load_sidebar_avatar(display_name)

    def _refresh_sidebar_session(self):
        """Vuelve a dibujar el widget de sesión (se llama al guardar o
        borrar el nick para que se actualice al instante)."""
        try:
            if self._session_frame.winfo_exists():
                self._build_session_widget()
        except (AttributeError, tk.TclError):
            pass

    def _draw_avatar_placeholder(self, holder, ok=False):
        for w in holder.winfo_children():
            w.destroy()
        c = tk.Canvas(holder, width=32, height=32, bg=GLASS_BG if ok else BG_CARD2,
                      highlightthickness=0)
        c.pack(fill="both", expand=True)
        c.create_text(16, 16, text=("✓" if ok else "?"),
                       fill=(ACCENT2 if ok else TEXT_MUTED), font=("Segoe UI", 12, "bold"))

    def _load_sidebar_avatar(self, nick):
        """Descarga en segundo plano una miniatura de la cabeza del jugador
        para el widget de sesión (no bloquea la interfaz)."""
        def fetch():
            photo = None
            try:
                from PIL import Image, ImageTk
                import io
                req = urllib.request.Request(
                    f"https://mc-heads.net/avatar/{urllib.parse.quote(nick)}/30",
                    headers={"User-Agent": "CrustEngineLauncher/1.0"})
                with urllib.request.urlopen(req, timeout=6) as r:
                    data = r.read()
                img = Image.open(io.BytesIO(data)).convert("RGBA").resize((30,30), Image.NEAREST)
                photo = ImageTk.PhotoImage(img)
            except Exception:
                photo = None
            self.after(0, lambda: self._apply_sidebar_avatar(photo))
        threading.Thread(target=fetch, daemon=True).start()

    def _apply_sidebar_avatar(self, photo):
        try:
            holder = self._session_avatar_holder
            if not holder.winfo_exists():
                return
        except (AttributeError, tk.TclError):
            return
        for w in holder.winfo_children():
            w.destroy()
        if photo:
            lbl = tk.Label(holder, image=photo, bg=BG_CARD2, bd=0)
            lbl.image = photo  # evita que el GC borre la imagen
            lbl.pack(fill="both", expand=True)
            lbl.bind("<Button-1>", lambda e: self._goto("player"))
        else:
            self._draw_avatar_placeholder(holder, ok=True)


    def _goto(self, key):
        for k, b in self._nav_btns.items():
            b.config(fg=ACCENT if k == key else TEXT_MUTED,
                     bg=ACCENT_DIM if k == key else BG_PANEL)
        for w in self._content.winfo_children(): w.destroy()
        {
            "home":    self._s_home,
            "player":  self._s_player,
            "mods":    self._s_mods,
            "servers": self._s_servers,
            "specs":   self._s_specs,
            "ai":      self._s_ai,
            "links":   self._s_links,
            "privacy": self._s_privacy,
        }[key]()

    def _scrollable(self, parent):
        c  = tk.Canvas(parent, bg=BG_DEEP, highlightthickness=0)
        sb = tk.Scrollbar(parent, orient="vertical", command=c.yview)
        inner = tk.Frame(c, bg=BG_DEEP)
        inner.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
        c.create_window((0,0), window=inner, anchor="nw")
        c.configure(yscrollcommand=sb.set)
        c.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        c.bind_all("<MouseWheel>", lambda e: c.yview_scroll(int(-1*(e.delta/120)),"units"))
        return inner

    # ══════════════════════════════════════════════════════════════
    #  SECCIÓN: INICIO
    # ══════════════════════════════════════════════════════════════
    def _s_home(self):
        f = tk.Frame(self._content, bg=BG_DEEP)
        f.pack(fill="both", expand=True, padx=30, pady=24)

        # ── Hero card — cristal oscuro con borde iluminado ────────────
        hero = tk.Frame(f, bg=GLASS_BG, padx=28, pady=22)
        hero.pack(fill="x", pady=(0, 16))
        # Borde superior naranja — línea de acento de marca
        tk.Frame(hero, bg=ACCENT, height=2).pack(fill="x", pady=(0, 14))

        tk.Label(hero, text="CRUST ENGINE", font=("Segoe UI", 28, "bold"),
                 fg=ACCENT, bg=GLASS_BG).pack(anchor="w")
        tk.Label(hero, text=MODPACK["desc"], font=("Segoe UI", 10),
                 fg=TEXT_MAIN, bg=GLASS_BG, justify="left", wraplength=540).pack(anchor="w", pady=(8, 0))
        tk.Label(hero,
                 text=f"MC {MODPACK['mc']}  ·  {MODPACK['loader']}  ·  {MODPACK['mods']} mods  ·  by {MODPACK['author']}",
                 font=FONT_MONO_S, fg=TEXT_MUTED, bg=GLASS_BG).pack(anchor="w", pady=(12, 0))

        # ── Stat cards ─────────────────────────────────────────────────
        sf = tk.Frame(f, bg=BG_DEEP)
        sf.pack(fill="x", pady=(0, 16))
        for val, lbl, clr in [(str(MODPACK["mods"]), "Mods", ACCENT),
                               (MODPACK["mc"], "Versión MC", ACCENT2),
                               (MODPACK["loader"], "Loader", GOLD),
                               ("8 GB", "RAM Rec.", TEAL)]:
            c = tk.Frame(sf, bg=GLASS_BG, padx=18, pady=14)
            c.pack(side="left", fill="x", expand=True, padx=(0, 8))
            # Pequeña línea de color en la parte superior de cada stat
            tk.Frame(c, bg=clr, height=2).pack(fill="x", pady=(0, 8))
            tk.Label(c, text=val, font=FONT_STAT, fg=clr, bg=GLASS_BG).pack()
            tk.Label(c, text=lbl, font=FONT_SMALL, fg=TEXT_MUTED, bg=GLASS_BG).pack()
            # Hover suave
            animate_card(c, GLASS_BG, GLASS_BG2, [])

        bottom = tk.Frame(f, bg=BG_DEEP)
        bottom.pack(fill="x", expand=True)

        # ── Novedades ─────────────────────────────────────────────────
        news = tk.Frame(bottom, bg=GLASS_BG)
        news.pack(side="left", fill="both", expand=True, padx=(0, 8))
        ni = tk.Frame(news, bg=GLASS_BG)
        ni.pack(fill="both", padx=18, pady=16)
        tk.Label(ni, text="NOVEDADES", font=("Segoe UI", 9, "bold"), fg=TEXT_MUTED, bg=GLASS_BG).pack(anchor="w")
        tk.Frame(ni, bg=BORDER_LIT, height=1).pack(fill="x", pady=8)
        for clr, tag, txt in [
            (ACCENT,  "v1.0.0",  f"Pack publicado — {MODPACK['mods']} mods optimizados"),
            (ACCENT2, "PRÓXIMO", "Soporte shaders Iris — en pruebas"),
            (GOLD,    "PRÓXIMO", "Pack de texturas 16x complementario"),
            (TEAL,    "IDEA",    "Preset JVM para máx. FPS incluido"),
        ]:
            row = tk.Frame(ni, bg=GLASS_BG); row.pack(fill="x", pady=3)
            tag_lbl = tk.Label(row, text=tag, font=FONT_MONO_S, fg=clr, bg=GLASS_BG, width=9, anchor="w")
            tag_lbl.pack(side="left")
            txt_lbl = tk.Label(row, text=txt, font=FONT_BODY, fg=TEXT_MAIN, bg=GLASS_BG, anchor="w")
            txt_lbl.pack(side="left")
            animate_card(row, GLASS_BG, GLASS_BG2, [tag_lbl, txt_lbl])

        # ── Inicio rápido ─────────────────────────────────────────────
        tip = tk.Frame(bottom, bg=GLASS_BG2)
        tip.pack(side="left", fill="both", expand=True)
        ti = tk.Frame(tip, bg=GLASS_BG2); ti.pack(fill="both", padx=18, pady=16)
        tk.Label(ti, text="INICIO RÁPIDO", font=("Segoe UI", 9, "bold"), fg=ACCENT, bg=GLASS_BG2).pack(anchor="w")
        tk.Frame(ti, bg=ACCENT, height=1).pack(fill="x", pady=8)
        for num, txt in [("1.", "Instala Java 21 desde adoptium.net"),
                          ("2.", "Descarga el pack en Modrinth o CurseForge"),
                          ("3.", "Ábrelo con Fabric Launcher"),
                          ("4.", "Pulsa ▶ JUGAR"),]:
            r = tk.Frame(ti, bg=GLASS_BG2); r.pack(fill="x", pady=3)
            n = tk.Label(r, text=num, font=FONT_MONO_S, fg=ACCENT, bg=GLASS_BG2, width=3)
            n.pack(side="left")
            t = tk.Label(r, text=txt, font=FONT_BODY, fg=TEXT_MAIN, bg=GLASS_BG2)
            t.pack(side="left")
            animate_card(r, GLASS_BG2, GLASS_EDGE, [n, t])

    # ══════════════════════════════════════════════════════════════
    #  SECCIÓN: PERFIL DE JUGADOR
    # ══════════════════════════════════════════════════════════════
    def _s_player(self):
        f = tk.Frame(self._content, bg=BG_DEEP)
        f.pack(fill="both", expand=True, padx=30, pady=24)

        tk.Label(f, text="MI PERFIL DE JUGADOR",
                 font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG_DEEP).pack(anchor="w")

        saved_nick = self._config.get("nick", "")
        if saved_nick:
            saved_lbl = tk.Label(f, text=f"✔ Nick guardado: {saved_nick}",
                                 font=FONT_MONO_S, fg=ACCENT2, bg=BG_DEEP)
            saved_lbl.pack(anchor="w", pady=(2, 4))
        else:
            tk.Label(f, text="Introduce tu nick de Minecraft para ver tu cabeza de jugador",
                     font=FONT_BODY, fg=TEXT_MUTED, bg=BG_DEEP).pack(anchor="w", pady=(2, 4))

        card = tk.Frame(f, bg=GLASS_BG)
        card.pack(fill="x", pady=(0, 12))
        ci = tk.Frame(card, bg=GLASS_BG); ci.pack(fill="both", padx=26, pady=22)

        input_row = tk.Frame(ci, bg=GLASS_BG); input_row.pack(fill="x", pady=(0, 16))
        tk.Label(input_row, text="Nick de Minecraft:", font=FONT_BODY,
                 fg=TEXT_MUTED, bg=GLASS_BG).pack(side="left", padx=(0, 10))
        nick_entry = tk.Entry(input_row, textvariable=self._player_nick,
                              font=("Segoe UI", 11), fg=TEXT_MAIN, bg=BG_CARD2,
                              insertbackground=ACCENT, relief="flat",
                              width=24, bd=4)
        nick_entry.pack(side="left")

        def do_search():
            nick = self._player_nick.get().strip()
            if nick:
                self._save_nick(nick)
            self._load_player_head(ci, nick)

        search_btn = make_animated_button(
            input_row, " Buscar ", do_search,
            fg="#0A0A0F", bg=ACCENT, hover_bg=ACCENT2, click_bg="#E85A10",
            font=("Segoe UI", 10), padx=10, pady=4)
        search_btn.pack(side="left", padx=(10, 0))

        def clear_nick():
            self._player_nick.set("")
            self._config.pop("nick", None)
            save_config(self._config)
            self._refresh_sidebar_session()
            self._goto("player")

        if saved_nick:
            clear_btn = make_animated_button(
                input_row, " Borrar guardado ", clear_nick,
                fg=RED, bg=BG_CARD2, hover_bg="#1E1010", click_bg="#2A0808",
                font=FONT_SMALL, padx=6, pady=4)
            clear_btn.pack(side="left", padx=(8, 0))

        # Zona de resultado
        self._player_result = tk.Frame(ci, bg=GLASS_BG)
        self._player_result.pack(fill="x")

        if self._player_nick.get():
            self._load_player_head(ci, self._player_nick.get().strip())

        # ── Cuenta Microsoft (premium) — para skin real en el juego ───
        ms_card = tk.Frame(f, bg=GLASS_BG)
        ms_card.pack(fill="x", pady=(0, 12))
        ms_inner = tk.Frame(ms_card, bg=GLASS_BG)
        ms_inner.pack(fill="both", padx=26, pady=22)
        self._build_ms_account_section(ms_inner)

        # Info — panel secundario de cristal
        info = tk.Frame(f, bg=GLASS_BG2); info.pack(fill="x")
        ii = tk.Frame(info, bg=GLASS_BG2); ii.pack(fill="x", padx=20, pady=14)
        tk.Label(ii, text="¿Por qué pedir tu nick?", font=FONT_HEAD, fg=ACCENT, bg=GLASS_BG2).pack(anchor="w")
        tk.Label(ii,
                 text="Tu nick se guarda localmente en config.json (solo en tu PC) para que no\n"
                      "tengas que introducirlo cada vez. Nunca se envía a servidores externos.\n"
                      "La cabeza se carga desde la API pública de Mojang (crafatar.com).",
                 font=FONT_BODY, fg=TEXT_MUTED, bg=GLASS_BG2, justify="left").pack(anchor="w", pady=(6, 0))

    # ── CUENTA MICROSOFT — login real para skin real en el juego ──────
    def _build_ms_account_section(self, parent):
        """Dibuja la tarjeta de cuenta Microsoft dentro de Mi Perfil.
        Se puede volver a llamar para refrescar tras iniciar/cerrar sesión."""
        for w in parent.winfo_children():
            w.destroy()

        tk.Label(parent, text="Cuenta Microsoft (premium)", font=FONT_HEAD,
                 fg=ACCENT, bg=GLASS_BG).pack(anchor="w")

        ms = self._config.get("ms_account") or {}
        if ms.get("name"):
            tk.Label(parent, text=f"✔ Sesión iniciada como {ms['name']}",
                     font=FONT_BODY, fg=GOLD, bg=GLASS_BG).pack(anchor="w", pady=(6, 2))
            tk.Label(parent,
                     text="Al pulsar JUGAR se usará tu skin real, no el Steve/Alex\n"
                          "por defecto del modo offline.",
                     font=FONT_SMALL, fg=TEXT_MUTED, bg=GLASS_BG, justify="left").pack(anchor="w")
            logout_btn = make_animated_button(
                parent, " Cerrar sesión Microsoft ", self._ms_logout_clicked,
                fg=RED, bg=BG_CARD2, hover_bg="#1E1010", click_bg="#2A0808",
                font=FONT_SMALL, padx=10, pady=6)
            logout_btn.pack(anchor="w", pady=(10, 0))
        else:
            tk.Label(parent,
                     text="Sin sesión Microsoft: se jugará en modo offline (skin\n"
                          "Steve/Alex por defecto). Inicia sesión con tu cuenta\n"
                          "Microsoft para que se use tu skin real.",
                     font=FONT_BODY, fg=TEXT_MUTED, bg=GLASS_BG, justify="left").pack(anchor="w", pady=(6, 10))
            login_btn = make_animated_button(
                parent, " Iniciar sesión con Microsoft ", self._ms_login_clicked,
                fg="#0A0A0F", bg=ACCENT, hover_bg=ACCENT2, click_bg="#E85A10",
                font=("Segoe UI", 10), padx=12, pady=7)
            login_btn.pack(anchor="w")
            if not _ms_configured():
                tk.Label(parent,
                         text="(El launcher todavía no tiene un Client ID de Azure "
                              "configurado — ver MS_CLIENT_ID en el código)",
                         font=FONT_MONO_S, fg=TEXT_HINT, bg=GLASS_BG, wraplength=560,
                         justify="left").pack(anchor="w", pady=(8, 0))

        self._ms_status_lbl = tk.Label(parent, text="", font=FONT_SMALL,
                                        fg=GOLD, bg=GLASS_BG)
        self._ms_status_lbl.pack(anchor="w", pady=(8, 0))

    def _ms_login_clicked(self):
        if not _ms_configured():
            messagebox.showwarning(
                "Falta configurar",
                "Todavía no se ha configurado MS_CLIENT_ID en el código del "
                "launcher.\n\nRegistra una app gratuita en portal.azure.com "
                "y pega el Client ID en la constante MS_CLIENT_ID, justo "
                "encima de la sección de cuenta Microsoft.")
            return
        try:
            self._ms_status_lbl.config(text="● Abriendo el navegador para iniciar sesión...", fg=GOLD)
        except (AttributeError, tk.TclError):
            pass

        def worker():
            account, err = _ms_oauth_login()
            self.after(0, lambda: self._ms_login_done(account, err))
        threading.Thread(target=worker, daemon=True).start()

    def _ms_login_done(self, account, err):
        try:
            self._ms_status_lbl.config(text="", fg=GOLD)
        except (AttributeError, tk.TclError):
            pass
        if err or not account:
            messagebox.showerror("No se pudo iniciar sesión",
                f"No se pudo iniciar sesión con Microsoft:\n\n{err}")
            return
        self._config["ms_account"] = {
            "name":          account.get("name"),
            "id":            account.get("id"),
            "refresh_token": account.get("refresh_token"),
        }
        ok = save_config(self._config)
        self._refresh_sidebar_session()
        self._goto("player")
        if ok:
            messagebox.showinfo("Sesión iniciada",
                f"Sesión iniciada como {account.get('name')}.\n"
                "Tu skin real se usará la próxima vez que pulses JUGAR.")

    def _ms_logout_clicked(self):
        self._config.pop("ms_account", None)
        save_config(self._config)
        self._refresh_sidebar_session()
        self._goto("player")


    def _load_player_head(self, container, nick):
        if not nick:
            messagebox.showwarning("Nick vacío", "Introduce tu nick de Minecraft primero.")
            return
        for w in self._player_result.winfo_children(): w.destroy()
        tk.Label(self._player_result, text="Buscando jugador...", font=FONT_MONO_S,
                 fg=TEXT_MUTED, bg=GLASS_BG).pack(anchor="w")
        self.update()

        def fetch():
            try:
                import json as _json, ssl, urllib.error, base64

                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                hdrs = {"User-Agent": "CrustEngineLauncher/1.0"}

                def get(url, timeout=8):
                    req = urllib.request.Request(url, headers=hdrs)
                    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
                        return r.read()

                try:
                    data = _json.loads(get(
                        f"https://api.mojang.com/users/profiles/minecraft/{urllib.parse.quote(nick)}"))
                    uuid      = data.get("id", "")
                    real_nick = data.get("name", nick)
                except urllib.error.HTTPError as e:
                    if e.code == 404:
                        self.after(0, lambda: self._show_head_error(
                            f"El jugador '{nick}' no existe.\nComprueba el nick."))
                        return
                    raise
                if not uuid:
                    self.after(0, lambda: self._show_head_error("No se encontro el UUID."))
                    return

                img_data = None
                errs = []

                try:
                    img_data = get(f"https://minotar.net/helm/{uuid}/96.png", timeout=7)
                except Exception as e:
                    errs.append(f"minotar:{e}")

                if not img_data:
                    try:
                        img_data = get(f"https://mc-heads.net/avatar/{uuid}/96", timeout=7)
                    except Exception as e:
                        errs.append(f"mc-heads:{e}")

                if not img_data:
                    try:
                        img_data = get(f"https://visage.surgeplay.com/face/96/{uuid}.png", timeout=7)
                    except Exception as e:
                        errs.append(f"visage:{e}")

                if not img_data:
                    try:
                        prof = _json.loads(get(
                            f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}", timeout=8))
                        props = prof.get("properties", [])
                        tp = next((p for p in props if p["name"] == "textures"), None)
                        if tp:
                            tj = _json.loads(base64.b64decode(tp["value"]))
                            skin_url = tj["textures"]["SKIN"]["url"]
                            img_data = b"SKIN:" + get(skin_url, timeout=8)
                    except Exception as e:
                        errs.append(f"mojang-tex:{e}")

                if img_data:
                    self.after(0, lambda: self._show_head(real_nick, uuid, img_data))
                else:
                    self.after(0, lambda: self._show_head_error(
                        "Sin conexion a las APIs de skin.\nComprueba tu internet.\n"
                        + "; ".join(errs[:2])))

            except Exception as e:
                err = str(e)
                self.after(0, lambda: self._show_head_error(err))

        threading.Thread(target=fetch, daemon=True).start()

    def _show_head(self, nick, uuid, img_data):
        for w in self._player_result.winfo_children(): w.destroy()

        shown_image = False
        try:
            from PIL import Image, ImageTk
            import io

            if img_data[:5] == b"SKIN:":
                raw = img_data[5:]
                skin = Image.open(io.BytesIO(raw)).convert("RGBA")
                skin = skin.resize((64, 64), Image.NEAREST)
                face = skin.crop((8, 8, 16, 16))
                hat  = skin.crop((40, 8, 48, 16))
                face.paste(hat, (0, 0), hat)
                img = face.resize((96, 96), Image.NEAREST)
            else:
                img = Image.open(io.BytesIO(img_data)).convert("RGBA").resize((96, 96), Image.NEAREST)

            photo = ImageTk.PhotoImage(img)
            lbl = tk.Label(self._player_result, image=photo, bg=BG_CARD,
                           highlightthickness=2, highlightbackground=ACCENT)
            lbl.image = photo
            lbl.pack(side="left", padx=(0, 20), pady=10)
            shown_image = True
        except ImportError:
            pass
        except Exception:
            pass

        if not shown_image:
            size = 96
            c = tk.Canvas(self._player_result, width=size, height=size,
                          bg=GLASS_BG, highlightthickness=2, highlightbackground=ACCENT)
            c.pack(side="left", padx=(0, 20), pady=10)
            P = size // 8
            c.create_rectangle(0, 0, size, size, fill="#C68642", outline="")
            for ex in [2, 5]:
                c.create_rectangle(ex*P, 3*P, (ex+1)*P, 4*P, fill="#1A1A1A", outline="")
            c.create_rectangle(3*P, 4*P, 5*P, 5*P, fill="#A0522D", outline="")
            c.create_rectangle(2*P, 6*P, 6*P, 7*P, fill="#8B0000", outline="")
            c.create_text(size//2, size-8, text="sin Pillow", font=("Consolas", 7),
                          fill=TEXT_MUTED)

        info_col = tk.Frame(self._player_result, bg=GLASS_BG)
        info_col.pack(side="left", fill="y", pady=10)
        tk.Label(info_col, text=nick, font=("Segoe UI", 18, "bold"),
                 fg=ACCENT, bg=GLASS_BG).pack(anchor="w")
        tk.Label(info_col, text="Jugador de Minecraft", font=FONT_SMALL,
                 fg=TEXT_MUTED, bg=GLASS_BG).pack(anchor="w")
        uuid_fmt = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}" if len(uuid)==32 else uuid
        tk.Label(info_col, text=uuid_fmt, font=("Consolas", 8),
                 fg=TEXT_HINT, bg=GLASS_BG).pack(anchor="w", pady=(2, 0))
        tk.Label(info_col, text=f"Modpack activo:  Crust Engine {MODPACK['ver']}",
                 font=FONT_MONO_S, fg=ACCENT2, bg=GLASS_BG).pack(anchor="w", pady=(8, 0))
        tk.Label(info_col, text=f"MC {MODPACK['mc']}  ·  {MODPACK['loader']}  ·  {MODPACK['mods']} mods",
                 font=FONT_MONO_S, fg=TEXT_MUTED, bg=GLASS_BG).pack(anchor="w")

        namemc_btn = make_animated_button(
            info_col, "Ver en NameMC →",
            lambda: webbrowser.open(f"https://namemc.com/profile/{nick}"),
            fg=ACCENT, bg=GLASS_BG, hover_bg=GLASS_BG2, click_bg=BG_CARD2,
            font=FONT_SMALL, padx=0, pady=4)
        namemc_btn.pack(anchor="w", pady=(10, 0))

        self._save_nick(nick)
        tk.Label(info_col, text="✔ Nick guardado", font=("Consolas", 8),
                 fg=ACCENT2, bg=GLASS_BG).pack(anchor="w", pady=(4, 0))

    def _show_head_error(self, err):
        for w in self._player_result.winfo_children(): w.destroy()
        tk.Label(self._player_result,
                 text=f"No se pudo cargar la skin.\nComprueba el nick o tu conexión.\n({err[:60]})",
                 font=FONT_SMALL, fg=RED, bg=GLASS_BG, justify="left").pack(anchor="w", pady=10)

    # ══════════════════════════════════════════════════════════════
    #  SECCIÓN: MODS
    # ══════════════════════════════════════════════════════════════
    def _s_mods(self):
        f = tk.Frame(self._content, bg=BG_DEEP)
        f.pack(fill="both", expand=True)
        h = tk.Frame(f, bg=BG_DEEP); h.pack(fill="x", padx=30, pady=(24, 10))
        tk.Label(h, text="MODS INCLUIDOS", font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG_DEEP).pack(anchor="w")
        tk.Label(h, text=f"{len(MODS)} mods · Fabric {MODPACK['mc']} · todos compatibles",
                 font=FONT_BODY, fg=TEXT_MUTED, bg=BG_DEEP).pack(anchor="w")

        c = tk.Frame(f, bg=BG_DEEP); c.pack(fill="both", expand=True, padx=30, pady=(0, 10))
        inner = self._scrollable(c)

        hr = tk.Frame(inner, bg=BG_DEEP); hr.pack(fill="x", pady=(0, 4))
        for txt, w in [("  MOD", 200), ("CATEGORÍA", 110), ("DESCRIPCIÓN", 1)]:
            tk.Label(hr, text=txt, font=FONT_MONO_S, fg=TEXT_MUTED,
                     bg=BG_DEEP, width=w//8 if w>1 else 1, anchor="w").pack(side="left")

        cat_c = {"Render": ACCENT, "Optimización": ACCENT2, "Memoria": GOLD, "Red": BLUE,
                 "Carga": "#F0A030", "GUI/HUD": ACCENT2, "Mundo": TEAL, "Chunks": ACCENT,
                 "Compat.": TEXT_MUTED, "Shaders": GOLD, "FPS": ACCENT, "Entidades": ACCENT2,
                 "Animaciones": "#F080A0", "Privacidad": RED, "Config": TEXT_MUTED, "GUI": ACCENT2}
        for i, (name, cat, desc) in enumerate(MODS):
            bg = GLASS_BG if i % 2 == 0 else GLASS_BG2
            bg_hover = GLASS_BG2 if i % 2 == 0 else GLASS_EDGE
            row = tk.Frame(inner, bg=bg); row.pack(fill="x")
            name_lbl = tk.Label(row, text=f"  {name}", font=("Segoe UI", 10, "bold"),
                     fg=TEXT_MAIN, bg=bg, width=24, anchor="w", pady=9)
            name_lbl.pack(side="left")
            cat_lbl = tk.Label(row, text=cat, font=FONT_MONO_S,
                     fg=cat_c.get(cat, ACCENT2), bg=bg, width=13, anchor="w")
            cat_lbl.pack(side="left")
            desc_lbl = tk.Label(row, text=desc, font=FONT_BODY, fg=TEXT_MUTED, bg=bg, anchor="w")
            desc_lbl.pack(side="left", fill="x", expand=True, padx=(0, 12))
            animate_card(row, bg, bg_hover, [name_lbl, cat_lbl, desc_lbl])

    # ══════════════════════════════════════════════════════════════
    #  SECCIÓN: SERVIDORES
    # ══════════════════════════════════════════════════════════════
    def _s_servers(self):
        f = tk.Frame(self._content, bg=BG_DEEP)
        f.pack(fill="both", expand=True, padx=30, pady=24)

        tk.Label(f, text="SERVIDORES ESPAÑOLES",
                 font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG_DEEP).pack(anchor="w")
        tk.Label(f, text="IPs verificadas junio 2026 · copia o entra directamente",
                 font=FONT_BODY, fg=TEXT_MUTED, bg=BG_DEEP).pack(anchor="w", pady=(2, 10))

        box = tk.Frame(f, bg=GLASS_BG2)
        box.pack(fill="x", pady=(0, 12))
        tk.Frame(box, bg=ACCENT, height=1).pack(fill="x")
        tk.Label(box, text="● Crust Engine — launcher propio activo",
                 font=FONT_MONO_S, fg=ACCENT, bg=GLASS_BG2, padx=16, pady=10).pack(anchor="w")

        for name, ip, desc, clr in SERVERS:
            card = tk.Frame(f, bg=GLASS_BG); card.pack(fill="x", pady=5)
            # Borde izquierdo de color
            accent_bar = tk.Frame(card, bg=clr, width=3)
            accent_bar.pack(side="left", fill="y")
            inner = tk.Frame(card, bg=GLASS_BG)
            inner.pack(side="left", fill="x", expand=True, padx=18, pady=14)

            name_lbl = tk.Label(inner, text=name, font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=GLASS_BG, anchor="w")
            name_lbl.pack(anchor="w")
            desc_lbl = tk.Label(inner, text=desc, font=FONT_SMALL, fg=TEXT_MUTED, bg=GLASS_BG, anchor="w")
            desc_lbl.pack(anchor="w")
            row = tk.Frame(inner, bg=GLASS_BG); row.pack(anchor="w", pady=(8, 0))
            ip_lbl = tk.Label(row, text=ip, font=FONT_MONO, fg=clr, bg=GLASS_BG)
            ip_lbl.pack(side="left")

            copy_btn = make_animated_button(
                row, " Copiar ", lambda i=ip: self._copy(i),
                fg=TEXT_MAIN, bg=GLASS_EDGE, hover_bg=BORDER_LIT, click_bg=BG_CARD2,
                font=FONT_SMALL, padx=6, pady=2)
            copy_btn.pack(side="left", padx=(10, 4))

            play_btn = make_animated_button(
                row, " ▶ Jugar ", lambda i=ip: self._launch_server_indie(i),
                fg="#0A0A0F", bg=clr, hover_bg=ACCENT2, click_bg=ACCENT_DIM,
                font=("Segoe UI", 9, "bold"), padx=6, pady=2)
            play_btn.pack(side="left", padx=4)

            animate_card(card, GLASS_BG, GLASS_BG2, [inner, name_lbl, desc_lbl, row, ip_lbl])

    def _copy(self, ip):
        self.clipboard_clear(); self.clipboard_append(ip)
        messagebox.showinfo("Copiado ✓", f"IP copiada:\n{ip}")

    def _detect_pack(self):
        bases = [
            os.path.join(os.environ.get("APPDATA",""), ".minecraft","mods"),
            os.path.join(os.path.expanduser("~"),"curseforge","minecraft","Instances"),
            os.path.join(os.environ.get("APPDATA",""),"PrismLauncher","instances"),
        ]
        for base in bases:
            if not os.path.isdir(base): continue
            for root, dirs, files in os.walk(base):
                dirs[:] = [d for d in dirs if d not in ("__pycache__",)]
                for fn in files:
                    if fn.lower().endswith(".jar") and "sodium" in fn.lower():
                        short = root[-38:] if len(root)>38 else root
                        return True, f"Sodium en ...{short}"
        return False, "Instala el pack en CurseForge/Modrinth primero"

    def _launch_server_indie(self, ip):
        """Copia la IP y lanza el juego via el núcleo propio."""
        self.clipboard_clear(); self.clipboard_append(ip)
        messagebox.showinfo("IP copiada ✓",
            f"IP copiada al portapapeles:\n\n    {ip}\n\n"
            "Se abrirá el juego. Una vez dentro:\n"
            "  Multijugador → Añadir servidor → pega la IP.")
        self._launch()

    # ══════════════════════════════════════════════════════════════
    #  SECCIÓN: REQUISITOS
    # ══════════════════════════════════════════════════════════════
    def _s_specs(self):
        f = tk.Frame(self._content, bg=BG_DEEP)
        f.pack(fill="both", expand=True, padx=30, pady=24)
        tk.Label(f, text="REQUISITOS DEL SISTEMA",
                 font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG_DEEP).pack(anchor="w")
        tk.Label(f, text="Analizando tu PC en tiempo real...",
                 font=FONT_BODY, fg=TEXT_MUTED, bg=BG_DEEP).pack(anchor="w", pady=(2, 14))

        cols = tk.Frame(f, bg=BG_DEEP); cols.pack(fill="x", pady=(0, 12))
        for tier, clr, items in [
            ("MÍNIMO",      ACCENT2, [("RAM","4 GB"),       ("Java","Java 21"),         ("CPU","4 núcleos 2.5 GHz"), ("GPU","OpenGL 4.5+"),       ("Disco","2 GB")]),
            ("RECOMENDADO", ACCENT,  [("RAM","8 GB"),       ("Java","Java 21 GraalVM"), ("CPU","6 núcleos 3.5 GHz"), ("GPU","GTX 1060 / RX 580+"),("Disco","4 GB SSD")]),
            ("ULTRA",       GOLD,    [("RAM","12 GB"),      ("Java","Java 21 GraalVM"), ("CPU","8 núcleos 4.5 GHz"), ("GPU","RTX 3060 / RX 6600+"),("Disco","NVMe SSD")]),
        ]:
            col = tk.Frame(cols, bg=GLASS_BG)
            col.pack(side="left", fill="both", expand=True, padx=(0, 8))
            # Cabecera de color sólido con texto oscuro
            tk.Frame(col, bg=clr, height=3).pack(fill="x")
            tk.Label(col, text=tier, font=("Segoe UI", 10, "bold"), fg=BG_DEEP, bg=clr, pady=8).pack(fill="x")
            for lbl, val in items:
                r = tk.Frame(col, bg=GLASS_BG); r.pack(fill="x", padx=14, pady=5)
                lbl_w = tk.Label(r, text=lbl, font=FONT_SMALL, fg=TEXT_MUTED, bg=GLASS_BG, width=7, anchor="w")
                lbl_w.pack(side="left")
                val_w = tk.Label(r, text=val, font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=GLASS_BG, anchor="w")
                val_w.pack(side="left")
                animate_card(r, GLASS_BG, GLASS_BG2, [lbl_w, val_w])

        hw_card = tk.Frame(f, bg=GLASS_BG); hw_card.pack(fill="x", pady=(0, 10))
        hc = tk.Frame(hw_card, bg=GLASS_BG); hc.pack(fill="x", padx=20, pady=16)
        tk.Label(hc, text="TU PC — ANÁLISIS EN TIEMPO REAL",
                 font=("Segoe UI", 10, "bold"), fg=ACCENT, bg=GLASS_BG).pack(anchor="w")
        tk.Frame(hc, bg=BORDER_LIT, height=1).pack(fill="x", pady=8)
        self._hw_frame = tk.Frame(hc, bg=GLASS_BG)
        self._hw_frame.pack(fill="x")
        tk.Label(self._hw_frame, text="Analizando hardware...", font=FONT_SMALL,
                 fg=TEXT_MUTED, bg=GLASS_BG).pack(anchor="w")
        threading.Thread(target=self._scan_hardware, daemon=True).start()

        # Panel JVM — vidrio secundario en lugar de naranja marrón
        tip = tk.Frame(f, bg=GLASS_BG2); tip.pack(fill="x")
        ti = tk.Frame(tip, bg=GLASS_BG2); ti.pack(fill="x", padx=20, pady=14)
        tk.Label(ti, text="FLAGS JVM RECOMENDADAS (Aikar)",
                 font=("Segoe UI", 10, "bold"), fg=ACCENT, bg=GLASS_BG2).pack(anchor="w")
        tk.Frame(ti, bg=ACCENT, height=1).pack(fill="x", pady=6)
        flags = "-Xmx8G -Xms4G -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC\n-XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50"
        tk.Label(ti, text=flags, font=FONT_MONO_S, fg=TEXT_MAIN, bg=GLASS_BG2, justify="left").pack(anchor="w", pady=(4, 0))

    def _scan_hardware(self):
        info = {}
        try:
            import ctypes
            class MEMSTATUS(ctypes.Structure):
                _fields_ = [("dwLength",ctypes.c_ulong),("dwMemoryLoad",ctypes.c_ulong),
                             ("ullTotalPhys",ctypes.c_ulonglong),("ullAvailPhys",ctypes.c_ulonglong),
                             ("ullTotalPageFile",ctypes.c_ulonglong),("ullAvailPageFile",ctypes.c_ulonglong),
                             ("ullTotalVirtual",ctypes.c_ulonglong),("ullAvailVirtual",ctypes.c_ulonglong),
                             ("sullAvailExtendedVirtual",ctypes.c_ulonglong)]
            ms = MEMSTATUS(); ms.dwLength = ctypes.sizeof(ms)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            total_gb = round(ms.ullTotalPhys / (1024**3), 1)
            info["RAM"] = f"{total_gb} GB"
            if total_gb < 4:   info["RAM_ok"] = RED
            elif total_gb < 8: info["RAM_ok"] = GOLD
            else:               info["RAM_ok"] = ACCENT
        except: info["RAM"] = "No detectada"; info["RAM_ok"] = TEXT_MUTED

        try:
            import os as _os
            cores = _os.cpu_count() or 0
            info["CPU"] = f"{cores} núcleos lógicos"
            info["CPU_ok"] = ACCENT if cores>=6 else (GOLD if cores>=4 else RED)
        except: info["CPU"] = "No detectada"; info["CPU_ok"] = TEXT_MUTED

        try:
            r = subprocess.run(["java","-version"], capture_output=True, text=True, timeout=4)
            ver_line = (r.stderr or r.stdout).split("\n")[0]
            info["Java"] = ver_line[:48] if ver_line else "No encontrado"
            info["Java_ok"] = ACCENT if "21" in ver_line or "22" in ver_line or "23" in ver_line or "24" in ver_line else GOLD
        except: info["Java"] = "No encontrado en PATH"; info["Java_ok"] = RED

        try:
            # Get-CimInstance funciona tanto en Windows PowerShell como en
            # PowerShell 7+ (Get-WmiObject está obsoleto y puede no existir).
            # Pedimos TODOS los adaptadores, no solo el primero: WMI puede
            # listar primero un monitor virtual (p. ej. "Meta Virtual Monitor"
            # de Meta Quest Link/Air Link, o software de escritorio remoto)
            # en vez de tu GPU física real.
            r = subprocess.run(
                ["powershell", "-NoProfile", "-Command",
                 "Get-CimInstance Win32_VideoController | Select-Object Name | ConvertTo-Json -Compress"],
                capture_output=True, text=True, timeout=6)
            import json as _json
            raw = (r.stdout or "").strip()
            data = _json.loads(raw) if raw else []
            if isinstance(data, dict):
                data = [data]
            names = [d.get("Name", "").strip() for d in data if d.get("Name")]

            # Adaptadores virtuales/no físicos conocidos — NO son tu GPU real,
            # los descartamos aunque WMI los liste primero.
            VIRTUAL_BLACKLIST = [
                "meta virtual", "virtual monitor", "oculus virtual",
                "remote display", "remote desktop", " idd", "indirect display",
                "microsoft basic render", "microsoft basic display",
                "teamviewer", "parsec", "citrix", "vmware", "virtualbox",
                "duet display", "spacedesk", "ndi virtual", "splashtop",
            ]
            real_gpus = [n for n in names
                         if not any(b in n.lower() for b in VIRTUAL_BLACKLIST)]

            candidates = real_gpus or names
            if candidates:
                # Si hay varias (p. ej. integrada + dedicada), prioriza la
                # GPU dedicada NVIDIA/AMD sobre una integrada Intel.
                candidates = sorted(candidates, key=lambda n: 0 if any(
                    k in n.lower() for k in
                    ("nvidia", "geforce", "rtx", "gtx", "radeon", "amd ")
                ) else 1)
                gpu = candidates[0][:50]
                info["GPU"] = gpu
                low = gpu.lower()
                if any(k in low for k in ("rtx", "radeon rx", "geforce")):
                    info["GPU_ok"] = ACCENT
                elif any(k in low for k in ("gtx", "amd")):
                    info["GPU_ok"] = GOLD
                else:
                    info["GPU_ok"] = TEXT_MUTED
            else:
                info["GPU"] = "No detectada"
                info["GPU_ok"] = TEXT_MUTED
        except Exception:
            info["GPU"] = "No detectada"; info["GPU_ok"] = TEXT_MUTED

        self.after(0, lambda: self._show_hardware(info))

    def _show_hardware(self, info):
        for w in self._hw_frame.winfo_children(): w.destroy()

        score = sum(1 for k in ["RAM_ok","CPU_ok","Java_ok"] if info.get(k)==ACCENT)
        if score == 3:   verdict, vc = "ULTRA — Tu PC va a volar con este pack", ACCENT
        elif score >= 2: verdict, vc = "COMPATIBLE — Rendimiento recomendado alcanzable", ACCENT2
        elif score >= 1: verdict, vc = "BÁSICO — Jugable, considera mejorar la RAM o Java", GOLD
        else:            verdict, vc = "INSUFICIENTE — Actualiza tu PC antes de jugar", RED

        vf = tk.Frame(self._hw_frame, bg=GLASS_BG2); vf.pack(fill="x", pady=(0, 10))
        tk.Label(vf, text=verdict, font=("Segoe UI", 11, "bold"),
                 fg=vc, bg=GLASS_BG2, padx=14, pady=10).pack(anchor="w")

        for label, key, ok_key in [
            ("RAM Total", "RAM",  "RAM_ok"),
            ("CPU",       "CPU",  "CPU_ok"),
            ("Java",      "Java", "Java_ok"),
            ("GPU",       "GPU",  "GPU_ok"),
        ]:
            row = tk.Frame(self._hw_frame, bg=GLASS_BG); row.pack(fill="x", pady=3)
            clr = info.get(ok_key, TEXT_MUTED)
            dot  = tk.Label(row, text="●", font=FONT_MONO_S, fg=clr, bg=GLASS_BG, width=3)
            dot.pack(side="left")
            lbl_w = tk.Label(row, text=label, font=FONT_SMALL, fg=TEXT_MUTED, bg=GLASS_BG, width=12, anchor="w")
            lbl_w.pack(side="left")
            val_w = tk.Label(row, text=info.get(key, "—"), font=("Segoe UI", 10, "bold"),
                     fg=TEXT_MAIN, bg=GLASS_BG, anchor="w")
            val_w.pack(side="left")
            animate_card(row, GLASS_BG, GLASS_BG2, [dot, lbl_w, val_w])

    # ══════════════════════════════════════════════════════════════
    #  SECCIÓN: ASISTENTE IA
    # ══════════════════════════════════════════════════════════════
    def _s_ai(self):
        f = tk.Frame(self._content, bg=BG_DEEP)
        f.pack(fill="both", expand=True, padx=30, pady=24)

        tk.Label(f, text="CENTRO DE AYUDA — CRUST ENGINE",
                 font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG_DEEP).pack(anchor="w")
        tk.Label(f, text="Elige una pregunta rápida o escribe la tuya · Respuestas predefinidas, sin IA ni conexión a internet",
                 font=FONT_BODY, fg=TEXT_MUTED, bg=BG_DEEP).pack(anchor="w", pady=(2, 10))

        chat_frame = tk.Frame(f, bg=GLASS_BG); chat_frame.pack(fill="both", expand=True, pady=(0, 8))

        self._chat_canvas = tk.Canvas(chat_frame, bg=GLASS_BG, highlightthickness=0)
        chat_sb = tk.Scrollbar(chat_frame, orient="vertical", command=self._chat_canvas.yview)
        self._chat_inner = tk.Frame(self._chat_canvas, bg=GLASS_BG)
        self._chat_inner.bind("<Configure>",
            lambda e: self._chat_canvas.configure(scrollregion=self._chat_canvas.bbox("all")))
        self._chat_canvas.create_window((0, 0), window=self._chat_inner, anchor="nw")
        self._chat_canvas.configure(yscrollcommand=chat_sb.set)
        self._chat_canvas.pack(side="left", fill="both", expand=True)
        chat_sb.pack(side="right", fill="y")

        self._add_chat_msg("ayuda",
            "¡Hola! Este es el centro de ayuda de Crust Engine. Pulsa una de\n"
            "las preguntas rápidas de abajo, o escribe la tuya — tengo\n"
            "respuestas guardadas sobre:\n"
            "• Instalación y configuración del modpack\n"
            "• Mods incluidos\n"
            "• Optimización de rendimiento y JVM\n"
            "• Requisitos, shaders, servidores y soporte\n"
            "¿En qué te puedo ayudar?")

        sug_frame = tk.Frame(f, bg=BG_DEEP); sug_frame.pack(fill="x", pady=(0, 8))
        for sug in QUICK_HELP_QUESTIONS:
            btn = make_animated_button(
                sug_frame, sug, lambda s=sug: self._send_help(s),
                fg=ACCENT, bg=GLASS_BG, hover_bg=GLASS_BG2, click_bg=GLASS_EDGE,
                font=FONT_SMALL, padx=10, pady=4)
            btn.pack(side="left", padx=(0, 6))

        input_frame = tk.Frame(f, bg=GLASS_BG); input_frame.pack(fill="x")
        self._help_input = tk.Text(input_frame, font=FONT_BODY, fg=TEXT_MAIN,
                                  bg=BG_CARD2, insertbackground=ACCENT,
                                  relief="flat", height=2, bd=6, wrap="word")
        self._help_input.pack(side="left", fill="x", expand=True, padx=4, pady=6)
        self._help_input.bind("<Return>", lambda e: self._help_enter(e))
        self._help_input.bind("<Shift-Return>", lambda e: None)

        send_btn = make_animated_button(
            input_frame, "Enviar\n↵",
            lambda: self._send_help(self._help_input.get("1.0", "end").strip()),
            fg="#0A0A0F", bg=ACCENT, hover_bg=ACCENT2, click_bg="#E85A10",
            font=("Segoe UI", 9, "bold"), padx=12, pady=0)
        send_btn.pack(side="right", padx=(0, 4), pady=6, fill="y")

        tk.Label(f, text="Enter = enviar  ·  Shift+Enter = nueva línea  ·  Respuestas automáticas predefinidas (sin conexión)",
                 font=FONT_MONO_S, fg=TEXT_HINT, bg=BG_DEEP).pack(anchor="w", pady=(4, 0))

    def _help_enter(self, event):
        txt = self._help_input.get("1.0", "end").strip()
        if txt: self._send_help(txt)
        return "break"

    def _add_chat_msg(self, role, text):
        is_user = role == "usuario"
        bg = GLASS_BG2 if is_user else GLASS_EDGE
        clr = TEXT_MAIN if is_user else ACCENT
        prefix = "Tú    " if is_user else "Ayuda "
        prefix_clr = TEXT_MUTED if is_user else ACCENT2

        row = tk.Frame(self._chat_inner, bg=GLASS_BG); row.pack(fill="x", padx=8, pady=4)
        tk.Label(row, text=prefix, font=FONT_MONO_S, fg=prefix_clr, bg=GLASS_BG, width=6, anchor="e"
                 ).pack(side="left", anchor="n", pady=8)
        bubble = tk.Frame(row, bg=bg); bubble.pack(side="left", fill="x", expand=True)
        tk.Label(bubble, text=text, font=FONT_BODY, fg=clr, bg=bg,
                 justify="left", wraplength=580, padx=12, pady=8, anchor="w"
                 ).pack(fill="x")

        self._chat_canvas.update_idletasks()
        self._chat_canvas.yview_moveto(1.0)

    def _send_help(self, text):
        """Muestra el mensaje del usuario y responde al instante con una
        respuesta predefinida local — no hay IA ni llamadas a ninguna API."""
        if not text: return
        self._help_input.delete("1.0","end")
        self._add_chat_msg("usuario", text)
        respuesta = get_help_answer(text)
        self._add_chat_msg("ayuda", respuesta)

    # ══════════════════════════════════════════════════════════════
    #  SECCIÓN: ENLACES
    # ══════════════════════════════════════════════════════════════
    def _s_links(self):
        f = tk.Frame(self._content, bg=BG_DEEP)
        f.pack(fill="both", expand=True, padx=30, pady=24)
        tk.Label(f, text="ENLACES Y RECURSOS", font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG_DEEP).pack(anchor="w")
        tk.Label(f, text="Todo lo que necesitas para empezar",
                 font=FONT_BODY, fg=TEXT_MUTED, bg=BG_DEEP).pack(anchor="w", pady=(2, 14))
        for name, url, desc, clr in LINKS:
            card = tk.Frame(f, bg=GLASS_BG, cursor="hand2"); card.pack(fill="x", pady=5)
            # Borde izquierdo de color
            accent_bar = tk.Frame(card, bg=clr, width=3)
            accent_bar.pack(side="left", fill="y")
            inner = tk.Frame(card, bg=GLASS_BG)
            inner.pack(side="left", fill="x", expand=True, padx=18, pady=16)
            name_lbl = tk.Label(inner, text=name, font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=GLASS_BG, anchor="w")
            name_lbl.pack(anchor="w")
            desc_lbl = tk.Label(inner, text=desc, font=FONT_SMALL, fg=TEXT_MUTED, bg=GLASS_BG, anchor="w")
            desc_lbl.pack(anchor="w")
            url_lbl = tk.Label(inner, text=url, font=FONT_MONO_S, fg=clr, bg=GLASS_BG, anchor="w")
            url_lbl.pack(anchor="w")
            arr = tk.Label(card, text="→ ", font=("Segoe UI", 14), fg=TEXT_MUTED, bg=GLASS_BG)
            arr.pack(side="right", padx=14)

            def open_url(e, u=url): webbrowser.open(u)
            for w in [card, inner, name_lbl, desc_lbl, url_lbl]:
                w.bind("<Button-1>", open_url)

            animate_card(card, GLASS_BG, GLASS_BG2, [inner, name_lbl, desc_lbl, url_lbl, arr])

        tk.Label(f, text=f"\nCrust Engine Launcher  ·  by {MODPACK['author']}  ·  MC {MODPACK['mc']}",
                 font=FONT_MONO_S, fg=TEXT_HINT, bg=BG_DEEP).pack(pady=(16, 0))

    def _s_privacy(self):
        f = tk.Frame(self._content, bg=BG_DEEP)
        f.pack(fill="both", expand=True, padx=30, pady=24)

        tk.Label(f, text="POLÍTICA DE PRIVACIDAD",
                 font=("Segoe UI", 16, "bold"), fg=ACCENT, bg=BG_DEEP).pack(anchor="w")
        tk.Label(f, text="Protección de datos · RGPD · LOPDGDD",
                 font=FONT_BODY, fg=TEXT_MUTED, bg=BG_DEEP).pack(anchor="w", pady=(2, 10))

        c = tk.Frame(f, bg=BG_DEEP); c.pack(fill="both", expand=True)
        canvas = tk.Canvas(c, bg=GLASS_BG, highlightthickness=0)
        sb = tk.Scrollbar(c, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=GLASS_BG)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        tk.Label(inner, text=PRIVACY_TEXT, font=FONT_MONO_S,
                 fg=TEXT_MAIN, bg=GLASS_BG, justify="left",
                 padx=26, pady=20, wraplength=720).pack(anchor="w")

        copy_btn = make_animated_button(
            f, "Copiar texto completo",
            lambda: [self.clipboard_clear(), self.clipboard_append(PRIVACY_TEXT),
                     messagebox.showinfo("Copiado", "Texto de privacidad copiado.")],
            fg="#0A0A0F", bg=ACCENT, hover_bg=ACCENT2, click_bg="#E85A10",
            font=FONT_SMALL, padx=12, pady=7)
        copy_btn.pack(anchor="w", pady=(10, 0))

    # ══════════════════════════════════════════════════════════════
    #  LANZAR — núcleo propio con minecraft-launcher-lib
    # ══════════════════════════════════════════════════════════════
    def _launch(self):
        """Botón JUGAR — instala Fabric si hace falta y lanza el juego sin
        depender de ningún launcher externo."""
        # 1) Comprobar / instalar minecraft-launcher-lib
        if not _check_mll_installed():
            self._status_lbl.config(text="● Instalando dependencias...", fg=GOLD)
            self.update()
            ok, msg = _install_mll()
            if not ok:
                self._status_lbl.config(text="● Error", fg=RED)
                messagebox.showerror("Error de instalación",
                    f"No se pudo instalar minecraft-launcher-lib:\n{msg}\n\n"
                    "Prueba manualmente:\n  pip install minecraft-launcher-lib")
                return

        # 2) Comprobar Java
        java = _find_java()
        if not java:
            self._status_lbl.config(text="● Java no encontrado", fg=RED)
            messagebox.showerror("Java no encontrado",
                "No se encontró Java 21 en tu sistema.\n\n"
                "Descárgalo gratis desde:\n  https://adoptium.net\n\n"
                "Instálalo y vuelve a pulsar JUGAR.")
            return

        # Lanzar en hilo para no bloquear la UI
        self._status_lbl.config(text="● Preparando...", fg=GOLD)
        self.update()
        threading.Thread(target=self._launch_thread, args=(java,), daemon=True).start()

    def _launch_thread(self, java):
        """Hilo de lanzamiento: instala Fabric si no está, construye el
        comando y ejecuta el juego."""
        import minecraft_launcher_lib as mll

        mc_dir     = _get_minecraft_dir()
        mc_version = MODPACK["mc"]
        nick       = self._config.get("nick", "Player")
        player_uuid = str(uuid.uuid3(uuid.NAMESPACE_DNS, nick))

        # Crear carpetas que Fabric necesita antes de arrancar
        # (evita el error NoSuchFileException en .fabric/remappedJars)
        for folder in [
            os.path.join(mc_dir, ".fabric"),
            os.path.join(mc_dir, ".fabric", "remappedJars"),
            os.path.join(mc_dir, ".fabric", "remappedJars",
                         f"minecraft-{mc_version}-0.19.3"),
            os.path.join(mc_dir, "mods"),
            os.path.join(mc_dir, "saves"),
            os.path.join(mc_dir, "resourcepacks"),
            os.path.join(mc_dir, "shaderpacks"),
        ]:
            os.makedirs(folder, exist_ok=True)

        try:
            # 3) Instalar Minecraft vanilla si no está descargado
            self.after(0, lambda: self._status_lbl.config(
                text="● Descargando Minecraft...", fg=GOLD))

            def _progress(current, total, status):
                if total:
                    pct = int(current / total * 100)
                    self.after(0, lambda p=pct, s=status:
                        self._status_lbl.config(
                            text=f"● {s[:30]}... {p}%", fg=GOLD))

            callback = {
                "setStatus":   lambda s: _progress(0, 0, s),
                "setProgress": lambda v: None,
                "setMax":      lambda v: None,
            }

            # Instalar vanilla (descarga JARs, assets, librerías)
            mll.install.install_minecraft_version(mc_version, mc_dir, callback)

            # 4) Instalar Fabric Loader
            self.after(0, lambda: self._status_lbl.config(
                text="● Instalando Fabric...", fg=GOLD))
            mll.fabric.install_fabric(mc_version, mc_dir)

            # 5) Obtener ID de la versión Fabric instalada
            fabric_id = _get_fabric_version_id(mc_version, mc_dir)
            if not fabric_id:
                raise RuntimeError("No se encontró la versión Fabric instalada.")

            # 6) Identidad: cuenta Microsoft real (si hay sesión) o modo
            #    offline. Se intenta refrescar el token de Microsoft en
            #    cada lanzamiento para asegurarnos de que sigue siendo
            #    válido (los access_token duran poco).
            ms_account  = self._config.get("ms_account") or {}
            use_premium = False
            username, token, player_uuid = nick, "0", player_uuid

            if ms_account.get("refresh_token"):
                self.after(0, lambda: self._status_lbl.config(
                    text="● Verificando sesión Microsoft...", fg=GOLD))
                fresh, ms_err = _ms_refresh(ms_account["refresh_token"])
                if fresh and fresh.get("access_token"):
                    use_premium = True
                    username = fresh.get("name", nick)
                    token    = fresh.get("access_token")
                    raw_id   = fresh.get("id", "")
                    try:
                        player_uuid = str(uuid.UUID(raw_id))
                    except Exception:
                        player_uuid = raw_id or player_uuid
                    # Microsoft suele rotar el refresh_token en cada uso;
                    # si no se guarda el nuevo, el siguiente refresco falla.
                    self._config["ms_account"] = {
                        "name": username,
                        "id": fresh.get("id"),
                        "refresh_token": fresh.get("refresh_token", ms_account["refresh_token"]),
                    }
                    save_config(self._config)
                else:
                    self.after(0, lambda err=ms_err: messagebox.showwarning(
                        "Sesión Microsoft caducada",
                        "No se pudo renovar tu sesión de Microsoft "
                        f"({err}).\n\nSe jugará en modo offline esta vez. "
                        "Vuelve a iniciar sesión desde 'Mi Perfil' cuando quieras."))

            # 7) Construir comando de lanzamiento
            options = {
                "username":    username,
                "uuid":        player_uuid,
                "token":       token,
                "jvmArguments": [
                    f"-Xms4G", "-Xmx8G",
                    "-XX:+UnlockExperimentalVMOptions",
                    "-XX:+UseG1GC",
                    "-XX:G1NewSizePercent=20",
                    "-XX:G1ReservePercent=20",
                    "-XX:MaxGCPauseMillis=50",
                    "-XX:G1HeapRegionSize=32M",
                ],
                "executablePath": java,
            }

            cmd = mll.command.get_minecraft_command(fabric_id, mc_dir, options)

            # 8) ¡Lanzar!
            self.after(0, lambda: self._status_lbl.config(
                text="● Lanzando...", fg=ACCENT))
            subprocess.Popen(cmd, cwd=mc_dir)

            self.after(500, lambda: self._status_lbl.config(
                text="● Jugando ▶", fg=ACCENT))

        except Exception as e:
            err = str(e)
            self.after(0, lambda: self._status_lbl.config(text="● Error", fg=RED))
            self.after(0, lambda: messagebox.showerror("Error al lanzar",
                f"No se pudo lanzar Minecraft:\n\n{err}\n\n"
                "Comprueba tu conexión a internet y que Java 21 esté instalado."))

    def on_close(self):
        try: self._particles.stop()
        except: pass
        self.destroy()


if __name__ == "__main__":
    app = Launcher()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
