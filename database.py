"""
Ítaca OS 2.0 - Base de Datos SQLite
Todas las tablas, seed data, y operaciones CRUD
"""
import sqlite3, json, os
from datetime import datetime, timedelta, date
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "itaca.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def dict_row(row):
    return dict(row) if row else None

def dict_rows(rows):
    return [dict(r) for r in rows]

# ═══════════════════════════════════════════
# CREAR TABLAS
# ═══════════════════════════════════════════
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            email TEXT PRIMARY KEY, nombre TEXT, rol TEXT DEFAULT 'Colaborador',
            estado TEXT DEFAULT 'Activo', unidad TEXT, email_lider TEXT,
            fecha_registro TEXT, ultimo_acceso TEXT
        );
        CREATE TABLE IF NOT EXISTS identidad (
            email TEXT PRIMARY KEY, nombre TEXT, foto_url TEXT, puesto TEXT,
            fecha_ingreso TEXT, rol TEXT, unidad TEXT, estado TEXT DEFAULT 'Activo',
            arquetipo_disc TEXT, disc_d INTEGER DEFAULT 0, disc_i INTEGER DEFAULT 0,
            disc_s INTEGER DEFAULT 0, disc_c INTEGER DEFAULT 0,
            meta_trascendente TEXT, frase_personal TEXT, limitantes TEXT,
            fortalezas TEXT, progreso_meta INTEGER DEFAULT 0, telefono TEXT,
            email_lider TEXT, fecha_actualizacion TEXT
        );
        CREATE TABLE IF NOT EXISTS metas (
            meta_id TEXT PRIMARY KEY, email TEXT, tipo TEXT, periodo TEXT,
            objetivo TEXT, kr1 TEXT, kr2 TEXT, kr3 TEXT,
            progreso INTEGER DEFAULT 0, estado TEXT DEFAULT 'Pendiente',
            fecha_creacion TEXT, fecha_limite TEXT
        );
        CREATE TABLE IF NOT EXISTS checkins (
            checkin_id TEXT PRIMARY KEY, email TEXT, estado_general TEXT,
            nivel_estres INTEGER, area_preocupacion TEXT, etiquetas TEXT,
            comentario TEXT, fecha TEXT, semana TEXT, alerta_enviada INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS faros (
            faro_id TEXT PRIMARY KEY, email_emisor TEXT, nombre_emisor TEXT,
            email_receptor TEXT, nombre_receptor TEXT, tipo_faro TEXT,
            pilar TEXT, animal TEXT, mensaje TEXT, foto_url TEXT,
            fecha_envio TEXT, estado TEXT DEFAULT 'Pendiente',
            email_aprobador TEXT, fecha_aprobacion TEXT,
            celebraciones INTEGER DEFAULT 0, visible INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS notificaciones (
            notif_id TEXT PRIMARY KEY, email_dest TEXT, tipo TEXT,
            titulo TEXT, mensaje TEXT, fecha TEXT,
            leida INTEGER DEFAULT 0, prioridad TEXT DEFAULT 'Media'
        );
        CREATE TABLE IF NOT EXISTS logros (
            logro_id TEXT PRIMARY KEY, email TEXT, badge_id TEXT,
            nombre_badge TEXT, descripcion TEXT, puntos INTEGER,
            categoria TEXT, fecha TEXT, icono TEXT
        );
        CREATE TABLE IF NOT EXISTS hexagono (
            eval_id TEXT PRIMARY KEY, email TEXT, periodo TEXT, fecha TEXT,
            vision INTEGER, planificacion INTEGER, encaje INTEGER,
            entrenamiento INTEGER, evaluacion_mejora INTEGER, reconocimiento INTEGER,
            promedio REAL, reflexion TEXT, dim_baja TEXT, dim_alta TEXT
        );
        CREATE TABLE IF NOT EXISTS journal (
            journal_id TEXT PRIMARY KEY, email TEXT, fecha TEXT,
            emociones TEXT, intensidad INTEGER, trigger_text TEXT,
            pensamiento TEXT, reflexion TEXT, estrategia TEXT,
            efectividad INTEGER, contexto TEXT, dia_semana TEXT, hora_dia TEXT
        );
        CREATE TABLE IF NOT EXISTS brujula_eval (
            brujula_id TEXT PRIMARY KEY, email TEXT, periodo TEXT, fecha TEXT,
            autoconocimiento INTEGER, autorregulacion INTEGER, motivacion INTEGER,
            empatia INTEGER, habilidades_sociales INTEGER,
            promedio REAL, comp_baja TEXT, comp_alta TEXT, reflexion TEXT,
            ejercicios_mes INTEGER DEFAULT 0, journal_mes INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS ejercicios_log (
            log_id TEXT PRIMARY KEY, email TEXT, ejercicio_id TEXT,
            fecha TEXT, duracion_real INTEGER, efectividad INTEGER,
            estado_antes TEXT, estado_despues TEXT, notas TEXT, competencia TEXT
        );
        CREATE TABLE IF NOT EXISTS planes_accion (
            plan_id TEXT PRIMARY KEY, email TEXT, periodo TEXT, dimension TEXT,
            puntaje_actual INTEGER, puntaje_meta INTEGER,
            accion1 TEXT, accion2 TEXT, accion3 TEXT,
            fecha_creacion TEXT, fecha_limite TEXT, estado TEXT DEFAULT 'Pendiente'
        );
        CREATE TABLE IF NOT EXISTS activity_log (
            log_id TEXT PRIMARY KEY, email TEXT, accion TEXT,
            detalle TEXT, fecha TEXT, modulo TEXT
        );
        """)
    seed_data()

# ═══════════════════════════════════════════
# SEED DATA
# ═══════════════════════════════════════════
def seed_data():
    with get_db() as db:
        c = db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
        if c > 0:
            return
        now = datetime.now().isoformat()
        # Usuarios de prueba
        users = [
            ("mirai@itaca.com", "Mirai Gonzales", "Admin", "Activo", "RH", None),
            ("carlos@itaca.com", "Carlos Mendoza", "Líder", "Activo", "Ventas", "mirai@itaca.com"),
            ("ana@itaca.com", "Ana Torres", "Líder", "Activo", "Operaciones", "mirai@itaca.com"),
            ("pedro@itaca.com", "Pedro Ramírez", "Colaborador", "Activo", "Ventas", "carlos@itaca.com"),
            ("lucia@itaca.com", "Lucía Fernández", "Colaborador", "Activo", "Ventas", "carlos@itaca.com"),
            ("diego@itaca.com", "Diego Silva", "Colaborador", "Activo", "Operaciones", "ana@itaca.com"),
            ("maria@itaca.com", "María López", "Colaborador", "Activo", "Operaciones", "ana@itaca.com"),
            ("jorge@itaca.com", "Jorge Castillo", "Coordinador", "Activo", "Marketing", "mirai@itaca.com"),
        ]
        for u in users:
            db.execute("INSERT OR IGNORE INTO usuarios VALUES (?,?,?,?,?,?,?,?)", (*u, now, now))
            db.execute("""INSERT OR IGNORE INTO identidad 
                (email,nombre,puesto,rol,unidad,estado,email_lider,fecha_actualizacion)
                VALUES (?,?,?,?,?,?,?,?)""",
                (u[0], u[1], f"{u[2]} de {u[4]}", u[2], u[4], u[3], u[5], now))
        # Algunos check-ins de ejemplo
        for i, email in enumerate(["pedro@itaca.com","lucia@itaca.com","diego@itaca.com"]):
            for w in range(4):
                d = datetime.now() - timedelta(weeks=w)
                estados = ["GENIAL","NORMAL","DIFICIL","NORMAL"]
                estres = [2, 3, 4, 2]
                cid = f"{email}_{d.strftime('%Y-%m-%d')}"
                sem = f"{d.year}-S{d.isocalendar()[1]:02d}"
                db.execute("INSERT OR IGNORE INTO checkins VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (cid, email, estados[w], estres[w], "Trabajo", "Concentrado,Determinado",
                     "", d.isoformat(), sem, 1 if estres[w]>=4 else 0))
        # Algunos faros de ejemplo
        faros_data = [
            ("pedro@itaca.com","Pedro Ramírez","lucia@itaca.com","Lucía Fernández","Faro de Valor","ITACTIVIDAD","Ardilla","Gracias por resolver el problema del cliente sin que nadie te lo pidiera. Eso es ITACTIVIDAD pura."),
            ("diego@itaca.com","Diego Silva","maria@itaca.com","María López","Faro de Aliento","Muro de Confianza","Ganso","Sé que esta semana fue difícil. Quiero que sepas que cuentas conmigo."),
            ("lucia@itaca.com","Lucía Fernández","carlos@itaca.com","Carlos Mendoza","Faro de Guía","+1 Sí Importa","Castor","Gracias por tomarte el tiempo de enseñarme el proceso de ventas."),
        ]
        for i, f in enumerate(faros_data):
            fid = f"FARO_{int(datetime.now().timestamp())}{i}"
            d = datetime.now() - timedelta(days=i*3)
            db.execute("INSERT OR IGNORE INTO faros VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (fid, f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], "",
                 d.isoformat(), "Aprobado", "mirai@itaca.com", d.isoformat(), 0, 1))
        # Badge de ejemplo
        db.execute("INSERT OR IGNORE INTO logros VALUES (?,?,?,?,?,?,?,?,?)",
            ("LOGRO_pedro_firstfaro", "pedro@itaca.com", "FIRST_FARO", "🔦 Primer Faro",
             "Encendiste tu primer faro", 10, "Cultura", now, "🔦"))

# ═══════════════════════════════════════════
# CRUD OPERATIONS
# ═══════════════════════════════════════════

# ── USUARIOS ──
def get_user(email):
    with get_db() as db:
        return dict_row(db.execute("SELECT * FROM usuarios WHERE email=?", (email,)).fetchone())

def get_all_users():
    with get_db() as db:
        return dict_rows(db.execute("SELECT * FROM usuarios WHERE estado='Activo' ORDER BY nombre").fetchall())

def get_identidad(email):
    with get_db() as db:
        return dict_row(db.execute("SELECT * FROM identidad WHERE email=?", (email,)).fetchone())

def update_identidad(email, **kwargs):
    with get_db() as db:
        sets = ", ".join(f"{k}=?" for k in kwargs)
        vals = list(kwargs.values()) + [email]
        db.execute(f"UPDATE identidad SET {sets}, fecha_actualizacion=? WHERE email=?",
                   (*kwargs.values(), datetime.now().isoformat(), email))

def get_team_members(email_lider):
    with get_db() as db:
        user = dict_row(db.execute("SELECT unidad FROM identidad WHERE email=?", (email_lider,)).fetchone())
        if not user: return []
        return dict_rows(db.execute(
            "SELECT * FROM identidad WHERE unidad=? AND email!=? AND estado='Activo'",
            (user["unidad"], email_lider)).fetchall())

# ── CHECK-INS ──
def save_checkin(email, estado, estres, area, etiquetas, comentario):
    now = datetime.now()
    cid = f"{email}_{now.strftime('%Y-%m-%d')}"
    sem = f"{now.year}-S{now.isocalendar()[1]:02d}"
    with get_db() as db:
        existing = db.execute("SELECT 1 FROM checkins WHERE email=? AND semana=?", (email, sem)).fetchone()
        if existing:
            return False, "Ya hiciste tu check-in esta semana."
        db.execute("INSERT INTO checkins VALUES (?,?,?,?,?,?,?,?,?,?)",
            (cid, email, estado, estres, area, ",".join(etiquetas) if etiquetas else "",
             comentario, now.isoformat(), sem, 1 if estres >= 4 else 0))
    return True, "Check-in registrado. ¡Gracias por compartir!"

def get_my_checkins(email, limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM checkins WHERE email=? ORDER BY fecha DESC LIMIT ?",
            (email, limit)).fetchall())

def get_team_checkins(email_lider):
    members = get_team_members(email_lider)
    if not members: return []
    emails = [m["email"] for m in members]
    ph = ",".join("?" * len(emails))
    with get_db() as db:
        return dict_rows(db.execute(f"""
            SELECT c.*, i.nombre FROM checkins c
            JOIN identidad i ON c.email = i.email
            WHERE c.email IN ({ph})
            ORDER BY c.fecha DESC LIMIT 50""", emails).fetchall())

def checkin_done_this_week(email):
    now = datetime.now()
    sem = f"{now.year}-S{now.isocalendar()[1]:02d}"
    with get_db() as db:
        return db.execute("SELECT 1 FROM checkins WHERE email=? AND semana=?", (email, sem)).fetchone() is not None

# ── FAROS ──
def save_faro(email_emisor, email_receptor, tipo_faro, mensaje):
    from config import TIPOS_FARO
    info = TIPOS_FARO[tipo_faro]
    now = datetime.now()
    fid = f"FARO_{int(now.timestamp())}"
    with get_db() as db:
        em = db.execute("SELECT nombre FROM identidad WHERE email=?", (email_emisor,)).fetchone()
        rc = db.execute("SELECT nombre FROM identidad WHERE email=?", (email_receptor,)).fetchone()
        nombre_e = em["nombre"] if em else email_emisor
        nombre_r = rc["nombre"] if rc else email_receptor
        db.execute("INSERT INTO faros VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (fid, email_emisor, nombre_e, email_receptor, nombre_r, tipo_faro,
             info["pilar"], info["animal"], mensaje, "", now.isoformat(),
             "Aprobado", "", now.isoformat(), 0, 1))
    return True, f"¡Faro enviado a {nombre_r}!"

def get_faros_recibidos(email, limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM faros WHERE email_receptor=? AND visible=1 ORDER BY fecha_envio DESC LIMIT ?",
            (email, limit)).fetchall())

def get_faros_enviados(email, limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM faros WHERE email_emisor=? ORDER BY fecha_envio DESC LIMIT ?",
            (email, limit)).fetchall())

def get_faros_publicos(limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM faros WHERE visible=1 ORDER BY fecha_envio DESC LIMIT ?",
            (limit,)).fetchall())

def celebrar_faro(faro_id):
    with get_db() as db:
        db.execute("UPDATE faros SET celebraciones = celebraciones + 1 WHERE faro_id=?", (faro_id,))

# ── HEXÁGONO ──
def save_hexagono(email, puntajes, reflexion):
    now = datetime.now()
    periodo = now.strftime("%Y-%m")
    eid = f"{email}_{periodo}"
    vals = list(puntajes.values())
    prom = round(sum(vals) / 6, 2)
    nombres = ["Visión Corporativa","Planificación","Encaje de Talento","Entrenamiento","Evaluación y Mejora","Reconocimiento"]
    dim_baja = nombres[vals.index(min(vals))]
    dim_alta = nombres[vals.index(max(vals))]
    with get_db() as db:
        existing = db.execute("SELECT 1 FROM hexagono WHERE eval_id=?", (eid,)).fetchone()
        if existing:
            return False, "Ya evaluaste este mes."
        db.execute("INSERT INTO hexagono VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (eid, email, periodo, now.isoformat(), *vals, prom, reflexion, dim_baja, dim_alta))
    return True, f"Evaluación guardada. Promedio: {prom}"

def get_my_hexagono(email, limit=12):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM hexagono WHERE email=? ORDER BY periodo DESC LIMIT ?",
            (email, limit)).fetchall())

# ── JOURNAL ──
def save_journal(email, emociones, intensidad, trigger, pensamiento, reflexion, estrategia, efectividad, contexto):
    now = datetime.now()
    jid = f"{email}_{now.strftime('%Y-%m-%d_%H%M')}"
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    dia = dias[now.weekday()]
    hora = "Mañana" if now.hour < 12 else "Tarde" if now.hour < 18 else "Noche"
    with get_db() as db:
        db.execute("INSERT INTO journal VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (jid, email, now.isoformat(), ",".join(emociones), intensidad,
             trigger, pensamiento, reflexion, estrategia or "", efectividad or 0,
             contexto, dia, hora))
    return True, "Entrada de journal guardada."

def get_my_journal(email, limit=30):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM journal WHERE email=? ORDER BY fecha DESC LIMIT ?",
            (email, limit)).fetchall())

# ── BRÚJULA IE ──
def save_brujula(email, puntajes, reflexion):
    now = datetime.now()
    periodo = now.strftime("%Y-%m")
    bid = f"{email}_{periodo}"
    vals = list(puntajes.values())
    prom = round(sum(vals) / 5, 2)
    nombres = ["Autoconocimiento","Autorregulación","Motivación","Empatía","Habilidades Sociales"]
    comp_baja = nombres[vals.index(min(vals))]
    comp_alta = nombres[vals.index(max(vals))]
    with get_db() as db:
        existing = db.execute("SELECT 1 FROM brujula_eval WHERE brujula_id=?", (bid,)).fetchone()
        if existing:
            return False, "Ya evaluaste este mes."
        ej_count = db.execute("SELECT COUNT(*) FROM ejercicios_log WHERE email=? AND fecha LIKE ?",
            (email, f"{periodo}%")).fetchone()[0]
        j_count = db.execute("SELECT COUNT(*) FROM journal WHERE email=? AND fecha LIKE ?",
            (email, f"{periodo}%")).fetchone()[0]
        db.execute("INSERT INTO brujula_eval VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (bid, email, periodo, now.isoformat(), *vals, prom, comp_baja, comp_alta,
             reflexion, ej_count, j_count))
    return True, f"Evaluación IE guardada. Promedio: {prom}"

def get_my_brujula(email, limit=12):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM brujula_eval WHERE email=? ORDER BY periodo DESC LIMIT ?",
            (email, limit)).fetchall())

# ── LOGROS ──
def get_my_logros(email):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM logros WHERE email=? ORDER BY fecha DESC", (email,)).fetchall())

def get_total_puntos(email):
    with get_db() as db:
        r = db.execute("SELECT COALESCE(SUM(puntos),0) FROM logros WHERE email=?", (email,)).fetchone()
        return r[0]

def otorgar_badge(email, badge_id, nombre, desc, puntos, categoria, icono):
    lid = f"LOGRO_{email.split('@')[0]}_{badge_id}"
    with get_db() as db:
        existing = db.execute("SELECT 1 FROM logros WHERE logro_id=?", (lid,)).fetchone()
        if existing: return False
        db.execute("INSERT INTO logros VALUES (?,?,?,?,?,?,?,?,?)",
            (lid, email, badge_id, nombre, desc, puntos, categoria, datetime.now().isoformat(), icono))
    return True

# ── NOTIFICACIONES ──
def get_notificaciones(email, limit=20):
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM notificaciones WHERE email_dest=? ORDER BY fecha DESC LIMIT ?",
            (email, limit)).fetchall())

def count_unread(email):
    with get_db() as db:
        return db.execute("SELECT COUNT(*) FROM notificaciones WHERE email_dest=? AND leida=0",
            (email,)).fetchone()[0]

# ── ANALYTICS (Admin) ──
def get_analytics():
    with get_db() as db:
        total_users = db.execute("SELECT COUNT(*) FROM usuarios WHERE estado='Activo'").fetchone()[0]
        checkins_week = db.execute("SELECT COUNT(*) FROM checkins WHERE semana=?",
            (f"{datetime.now().year}-S{datetime.now().isocalendar()[1]:02d}",)).fetchone()[0]
        avg_estres = db.execute("SELECT AVG(nivel_estres) FROM checkins WHERE fecha > ?",
            ((datetime.now() - timedelta(days=7)).isoformat(),)).fetchone()[0] or 0
        alertas = db.execute("SELECT COUNT(*) FROM checkins WHERE alerta_enviada=1 AND fecha > ?",
            ((datetime.now() - timedelta(days=7)).isoformat(),)).fetchone()[0]
        faros_mes = db.execute("SELECT COUNT(*) FROM faros WHERE fecha_envio > ?",
            ((datetime.now() - timedelta(days=30)).isoformat(),)).fetchone()[0]
        total_faros = db.execute("SELECT COUNT(*) FROM faros").fetchone()[0]
        return {
            "total_users": total_users, "checkins_week": checkins_week,
            "avg_estres": round(avg_estres, 1), "alertas": alertas,
            "faros_mes": faros_mes, "total_faros": total_faros,
            "tasa_checkin": round((checkins_week / max(total_users, 1)) * 100),
        }

# Inicializar al importar
init_db()
