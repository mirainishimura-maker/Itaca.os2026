"""
Ítaca OS 2.0 - Base de Datos SQLite
Todas las tablas, seed data, y operaciones CRUD
"""
import sqlite3, json, os
from datetime import datetime, timedelta, date
from contextlib import contextmanager

# Robust path that works in Streamlit Cloud, local, and any CWD
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_THIS_DIR, "data", "itaca.db")

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
            fecha_registro TEXT, ultimo_acceso TEXT,
            password TEXT DEFAULT 'Itaca2026!'
        );
        CREATE TABLE IF NOT EXISTS identidad (
            email TEXT PRIMARY KEY, nombre TEXT, foto_url TEXT, puesto TEXT,
            fecha_ingreso TEXT, rol TEXT, unidad TEXT, estado TEXT DEFAULT 'Activo',
            arquetipo_disc TEXT, arquetipo_secundario TEXT,
            disc_d INTEGER DEFAULT 0, disc_i INTEGER DEFAULT 0,
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
        CREATE TABLE IF NOT EXISTS focos (
            foco_id TEXT PRIMARY KEY, email_creador TEXT, unidad TEXT,
            nombre TEXT, descripcion TEXT, periodo TEXT,
            progreso INTEGER DEFAULT 0, estado TEXT DEFAULT 'En Progreso',
            fecha_creacion TEXT, fecha_limite TEXT, orden INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS krs (
            kr_id TEXT PRIMARY KEY, foco_id TEXT, nombre TEXT,
            meta_valor REAL, valor_actual REAL DEFAULT 0, unidad_medida TEXT,
            progreso INTEGER DEFAULT 0, estado TEXT DEFAULT 'En Progreso',
            periodicidad TEXT DEFAULT 'Mensual',
            fecha_creacion TEXT, fecha_limite TEXT,
            FOREIGN KEY (foco_id) REFERENCES focos(foco_id)
        );
        CREATE TABLE IF NOT EXISTS tareas (
            tarea_id TEXT PRIMARY KEY, kr_id TEXT, foco_id TEXT,
            titulo TEXT, descripcion TEXT,
            email_responsable TEXT, nombre_responsable TEXT,
            fecha_inicio TEXT, fecha_limite TEXT, fecha_completada TEXT,
            estado TEXT DEFAULT 'Pendiente', prioridad TEXT DEFAULT 'Media',
            progreso INTEGER DEFAULT 0, notas TEXT,
            fecha_creacion TEXT, ultimo_cambio TEXT, cambiado_por TEXT,
            FOREIGN KEY (kr_id) REFERENCES krs(kr_id),
            FOREIGN KEY (foco_id) REFERENCES focos(foco_id)
        );
        CREATE TABLE IF NOT EXISTS historial_cambios (
            cambio_id TEXT PRIMARY KEY, entidad TEXT, entidad_id TEXT,
            campo TEXT, valor_anterior TEXT, valor_nuevo TEXT,
            email_autor TEXT, nombre_autor TEXT, fecha TEXT
        );
        CREATE TABLE IF NOT EXISTS eval_360 (
            eval_id TEXT PRIMARY KEY, email_evaluado TEXT, email_evaluador TEXT,
            periodo TEXT, fecha TEXT, anonimo INTEGER DEFAULT 1,
            vision INTEGER, planificacion INTEGER, encaje INTEGER,
            entrenamiento INTEGER, evaluacion_mejora INTEGER, reconocimiento INTEGER,
            promedio REAL, comentario TEXT
        );
        CREATE TABLE IF NOT EXISTS eval_desempeno (
            eval_id TEXT PRIMARY KEY, email TEXT, periodo TEXT, fecha TEXT,
            evaluador_email TEXT, evaluador_nombre TEXT,
            cumplimiento_metas INTEGER, calidad_trabajo INTEGER,
            trabajo_equipo INTEGER, comunicacion INTEGER, iniciativa INTEGER,
            promedio REAL, fortalezas TEXT, areas_mejora TEXT,
            plan_desarrollo TEXT, comentario_general TEXT
        );
        CREATE TABLE IF NOT EXISTS capacitaciones (
            cap_id TEXT PRIMARY KEY, email TEXT, nombre_cap TEXT,
            tipo TEXT, horas INTEGER, fecha TEXT, certificado INTEGER DEFAULT 0,
            institucion TEXT, notas TEXT
        );

        -- ═══════════════════════════════════════════
        -- NUEVAS TABLAS v2.0 (HRIS + CRM + Finanzas)
        -- ═══════════════════════════════════════════

        -- Perfiles DISC ideales por puesto (semáforo de encaje)
        CREATE TABLE IF NOT EXISTS puestos_perfiles (
            puesto_id TEXT PRIMARY KEY,
            nombre_puesto TEXT,
            disc_ideal_principal TEXT,
            disc_ideal_secundario TEXT,
            unidad TEXT,
            descripcion TEXT
        );

        -- Flujo financiero (La Bóveda)
        CREATE TABLE IF NOT EXISTS finanzas_flujo (
            flujo_id TEXT PRIMARY KEY,
            unidad TEXT,
            tipo TEXT,
            categoria TEXT,
            monto REAL,
            fecha TEXT,
            campana TEXT,
            descripcion TEXT,
            registrado_por TEXT,
            fecha_registro TEXT
        );

        -- CRM Leads (El Puerto)
        CREATE TABLE IF NOT EXISTS crm_leads (
            lead_id TEXT PRIMARY KEY,
            telefono TEXT,
            nombre_apoderado TEXT,
            nombre_nino TEXT,
            edad INTEGER,
            ciudad TEXT,
            origen TEXT,
            precalificacion TEXT,
            estado TEXT DEFAULT 'Nuevo',
            unidad TEXT,
            notas TEXT,
            email_asesor TEXT,
            fecha_creacion TEXT,
            fecha_actualizacion TEXT
        );

        -- Cuotas de venta (auto-generadas al inscribir lead)
        CREATE TABLE IF NOT EXISTS ventas_cuotas (
            cuota_id TEXT PRIMARY KEY,
            lead_id TEXT,
            numero_cuota INTEGER,
            monto_esperado REAL,
            monto_pagado REAL DEFAULT 0,
            fecha_vencimiento TEXT,
            fecha_pago TEXT,
            estado TEXT DEFAULT 'Pendiente',
            FOREIGN KEY (lead_id) REFERENCES crm_leads(lead_id)
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
        # ═══════════════════════════════════════════════════════
        # 90 COLABORADORES REALES DE ÍTACA HUB
        # Fuente: BD MAESTRA (Excel), Febrero 2026
        # Formato: (email, nombre, rol, estado, unidad, email_lider, cargo, celular, ingreso)
        # ═══════════════════════════════════════════════════════
        users = [
            ("oscar.bereche@itaca.com","Oscar Sebastián García Bereche","Colaborador","Activo","321 SHOW","francisco.orellano@itaca.com","Videógrafo","974585296","2021-03-15"),
            ("francisco.orellano@itaca.com","Francisco Javier Muñoz Orellano","Líder","Activo","321 SHOW",None,"Socio","969680096","2021-09-10"),
            ("max.jimenez@itaca.com","Max Angel Chero Jiménez","Líder","Activo","ARTAMAX",None,"Socio / Gerente","973355562","2025-04-01"),
            ("esther.ortiz@itaca.com","Esther Abigail Ayala Ortiz","Colaborador","Activo","ARTAMAX","max.jimenez@itaca.com","Docente","917827155","2025-08-01"),
            ("anthonella.ojeda@itaca.com","Anthonella Abigail Ojeda Ojeda","Colaborador","Activo","ARTAMAX","max.jimenez@itaca.com","Asistente Gerencial","929596616","2025-10-13"),
            ("jorge.romero@itaca.com","Jorge Augusto Lazarte Romero","Líder","Activo","B&J ASESORES",None,"Socio / Director","959300115","2022-01-01"),
            ("keiko.cordova@itaca.com","Keiko Danitza Ramos Córdova","Colaborador","Activo","B&J ASESORES","jorge.romero@itaca.com","Asistente Contable","962807609","2023-01-01"),
            ("sara.miranda@itaca.com","Sara Belen Romero Miranda","Colaborador","Activo","B&J ASESORES","jorge.romero@itaca.com","Auxiliar Contable","933673617","2024-10-01"),
            ("nestor.hernandez@itaca.com","Néstor Javier Chanduvi Hernández","Colaborador","Activo","CLUB DE ARTE","luis.sosa@itaca.com","Docente","913069605","2020-01-06"),
            ("emma.mendoza@itaca.com","Emma Elizabeth Curipuma Mendoza","Colaborador","Activo","CLUB DE ARTE","luis.sosa@itaca.com","Docente","999138246","2023-01-01"),
            ("ana.sacchetti@itaca.com","Ana Luz López Sacchetti","Colaborador","Activo","CLUB DE ARTE","luis.sosa@itaca.com","Docente","940176075","2023-12-15"),
            ("melani.oscco@itaca.com","Melani Ramirez Oscco","Colaborador","Activo","CLUB DE ARTE","luis.sosa@itaca.com","Docente","969533354","2025-04-01"),
            ("pamela.silvera@itaca.com","Pamela Victoria Revilla Silvera","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","980715859","2023-08-31"),
            ("ayvi.huaman@itaca.com","Ayvi Yamillette Reyes Huamán","Coordinador","Activo","CONVER LIMA",None,"Coordinadora","960711603","2024-10-21"),
            ("katia.avila@itaca.com","Katia Gianelly Briones Avila","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","989018532","2025-03-15"),
            ("meriveth.garcia@itaca.com","Meriveth Ay-Ling Rojas García","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","978361147","2025-04-01"),
            ("arlette.mestanza@itaca.com","Arlette Solange Santibañez Mestanza","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","998732273","2025-04-01"),
            ("paolo.camacho@itaca.com","Paolo Fabio Ronceros Camacho","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","936809795","2025-05-05"),
            ("camila.gamarra@itaca.com","Camila Fiorella Alvarez Gamarra","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","961891335","2025-06-01"),
            ("cristel.motta@itaca.com","Cristel Fiorella Ríos Motta","Colaborador","Activo","CONVER LIMA","ayvi.huaman@itaca.com","Psicólogo","937091962","2025-06-01"),
            ("grecia.elera@itaca.com","Grecia Palacios Elera","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","962686617","2023-10-11"),
            ("alejandro.ortiz@itaca.com","Alejandro Chung Ortiz","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicólogo","968824862","2024-08-28"),
            ("joyce.mendoza@itaca.com","Joyce Calle Mendoza","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","995047598","2024-09-06"),
            ("yazmin.alvarado@itaca.com","Yazmin Fiorella Castillo Alvarado","Coordinador","Activo","CONVER PIURA",None,"Coordinadora","962840126","2025-01-02"),
            ("andrea.chirito@itaca.com","Andrea Elizabeth Cabellos Chirito","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","969214648","2025-01-30"),
            ("angi.vilela@itaca.com","Angi Lizeth Requena Vilela","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","958174225","2025-01-30"),
            ("maximo.espinoza@itaca.com","Maximo Jr. Aldana Espinoza","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicólogo","955667968","2025-06-16"),
            ("sofia.godinez@itaca.com","Sofía Isabel Ferreyra Godinez","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","991130790","2025-06-18"),
            ("inori.coronado@itaca.com","Inori Nishimura Coronado","Colaborador","Activo","CONVER PIURA","yazmin.alvarado@itaca.com","Psicóloga","970632478","2025-09-01"),
            ("maria.garcia@itaca.com","María Fernanda Vásquez García","Líder","Activo","ECO",None,"Directora y entrenadora","999642183","2025-04-02"),
            ("johana.sanchez@itaca.com","Johana Andrea Díaz Sanchez","Colaborador","Activo","ECO","maria.garcia@itaca.com","Docente","991403599","2025-08-01"),
            ("alvaro.gallo@itaca.com","Alvaro Alonso Gallo","Colaborador","Activo","ECO","maria.garcia@itaca.com","Docente","965788767","2025-08-01"),
            ("harold.arevalo@itaca.com","Harold Serhio Quinde Arévalo","Líder","Activo","ITACA EDUCACIÓN",None,"Entrenador / Director","901791803","2024-01-01"),
            ("maria.arechaga@itaca.com","María Carla Roxany Arrese Arechaga","Colaborador","Activo","ITACA EDUCACIÓN","harold.arevalo@itaca.com","Entrenadora","963777646","2024-01-01"),
            ("jadek.renteria@itaca.com","Jadek Renteria","Colaborador","Activo","ITACA EDUCACIÓN","harold.arevalo@itaca.com","Practicante","967384002","2025-07-14"),
            ("brandon.cordova@itaca.com","Brandon Skiev Soto Cordova","Líder","Activo","ITACA HUB",None,"Socio Ítaca Hub","951657082","2014-09-01"),
            ("brian.olaya@itaca.com","Brian Stefano Savitzky Olaya","Líder","Activo","ITACA HUB","brandon.cordova@itaca.com","Socio Ítaca Hub","944438905","2014-09-01"),
            ("mattias.savitzky@itaca.com","Mattias Mattos Savitzky","Coordinador","Activo","ITACA HUB","brandon.cordova@itaca.com","Coordinador administrativo","951201565","2022-01-06"),
            ("gabriel.savitzky@itaca.com","Gabriel Mattos Savitzky","Líder","Activo","ITACA HUB","brandon.cordova@itaca.com","Director comercial","922215252","2022-04-16"),
            ("astrid.vivas@itaca.com","Astrid Adanai Ramos Vivas","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Asistente Gerencial","957552519","2023-04-13"),
            ("jose.chuquicondor@itaca.com","José Piero Alexandro Zapata Chuquicondor","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Procesos administrativos","920129548","2023-12-11"),
            ("piero.garcia@itaca.com","Piero Huertas García","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Marketing","976216997","2024-03-01"),
            ("virginia.rabanal@itaca.com","Virginia Anaís Robledo Rabanal","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Asistente Gerencial","918406473","2024-09-01"),
            ("brando.juarez@itaca.com","Brando Augusto Franco Juárez","Colaborador","Activo","ITACA HUB","brandon.cordova@itaca.com","Marketing","947057325","2024-09-01"),
            ("mirai.coronado@itaca.com","Mirai Nishimura Coronado","Admin","Activo","ITACA HUB","brandon.cordova@itaca.com","Gestora de Talento Humano","977668497","2025-01-01"),
            ("monica.rolando@itaca.com","Mónica Alejandra Rodríguez Rolando","Colaborador","Activo","KIDS AREQUIPA","gabriel.savitzky@itaca.com","Entrenadora Kids Arequipa","953850222","2024-08-31"),
            ("axlen.barra@itaca.com","Axlen Nicole Fernández Barra","Colaborador","Activo","KIDS AREQUIPA","gabriel.savitzky@itaca.com","Entrenadora Kids Arequipa","983754707","2024-08-31"),
            ("gabriela.juarez@itaca.com","Gabriela Lucía Rentería Juárez","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Psicóloga","961350844","2019-01-02"),
            ("maria.ramirez@itaca.com","María de los Ángeles Espinoza Ramirez","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids","912550185","2024-01-01"),
            ("luana.camacho@itaca.com","Luana Marialé Gallesi Camacho","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Co-entrenadora Kids Lima","913718440","2024-01-12"),
            ("gianela.lopez@itaca.com","Gianela Esther Loardo Lopez","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids Lima","964240154","2024-04-12"),
            ("fernanda.cabrera@itaca.com","Fernanda Elizabeth Vizcarra Cabrera","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids Lima","980732705","2024-08-30"),
            ("giresse.castillo@itaca.com","Giresse Alexander Bernuy Castillo","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenador Kids Lima","947725759","2024-08-30"),
            ("adriana.alvarado@itaca.com","Adriana Ximena Harumy Díaz Alvarado","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Psicóloga","992837265","2024-08-30"),
            ("jesus.martinez@itaca.com","Jesús Israel Montellanos Martinez","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenador Kids Lima","906837369","2024-08-31"),
            ("diana.aliaga@itaca.com","Diana Susana Cornejo Aliaga","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids","963781075","2024-12-13"),
            ("lucia.huambachano@itaca.com","Lucía Alessandra Meza Huambachano","Colaborador","Activo","KIDS LIMA","brando.camacho@itaca.com","Entrenadora Kids Lima","",""),
            ("fransheska.atoche@itaca.com","Fransheska Teresa Saldarriaga Atoche","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids Piura","921988904","2020-07-01"),
            ("taiz.saucedo@itaca.com","Taiz Kasandra Ivonne Martinez Saucedo","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","994191006","2022-05-14"),
            ("candy.vera@itaca.com","Candy Alisson Huertas Vera","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","907851180","2023-09-01"),
            ("tatiana.cruz@itaca.com","Tatiana Milene Lachira Cruz","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids Piura","951933777","2024-04-11"),
            ("kristel.chunga@itaca.com","Kristel Rosa Saavedra Chunga","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","977195668","2024-04-27"),
            ("ana.iman@itaca.com","Ana Lucía Gallardo Imán","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","938310093","2024-09-01"),
            ("angie.morocho@itaca.com","Angie de los Milagros Salvador Morocho","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids Piura","953348766",""),
            ("victoria.valencia@itaca.com","Victoria María Rodríguez Valencia","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Psicóloga Kids","934637679",""),
            ("luisa.dolly@itaca.com","Luisa María Castillo Dolly","Colaborador","Activo","KIDS PIURA","mattias.savitzky@itaca.com","Entrenadora Kids","903003595",""),
            ("santiago.zambrano@itaca.com","Santiago Sánchez Zambrano","Líder","Activo","MARKETING",None,"Socio Ítaca Marketing","997754433","2020-01-11"),
            ("daniela.collantes@itaca.com","Daniela Fernanda Tocto Collantes","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Project Manager","944822543","2021-04-12"),
            ("edson.pena@itaca.com","Edson Martín Domínguez Peña","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Diseñador gráfico","978379477","2021-06-21"),
            ("jose.lecca@itaca.com","José Joaquín Murillo Lecca","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Entrenador Kids Lima","921168570","2024-01-08"),
            ("maickol.ayala@itaca.com","Maickol Yorvn Saavedra Ayala","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Creador de contenido","986982339","2024-01-12"),
            ("gabriel.querevalu@itaca.com","Gabriel Efraín Chavez Querevalu","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Analista de pauta","962082320","2024-11-04"),
            ("damaris.lupuche@itaca.com","Damaris Nicol Aguilar Lupuche","Colaborador","Activo","MARKETING","santiago.zambrano@itaca.com","Practicante CC","918135940","2024-11-04"),
            ("milagros.socola@itaca.com","Milagros Stephany Espinoza Socola","Colaborador","Activo","PRACTICANTES","mirai.coronado@itaca.com","Practicante Hub","959247793","2025-08-28"),
            ("rodrigo.hurtado@itaca.com","Rodrigo Joaquín Cruz Hurtado","Colaborador","Activo","PRACTICANTES","mirai.coronado@itaca.com","Practicante Marco Legal","961861390","2025-09-22"),
            ("jocelyn.vivas@itaca.com","Jocelyn Aradiel Ramos Vivas","Colaborador","Activo","PRACTICANTES","mirai.coronado@itaca.com","Practicante Editora","920862467","2025-10-01"),
            ("claudia.chuquicondor@itaca.com","Claudia Belén Zapata Chuquicondor","Colaborador","Activo","PRACTICANTES","mirai.coronado@itaca.com","Practicante RH","959143022","2025-12-15"),
            ("luis.sosa@itaca.com","Luis Alberto Chiroque Sosa","Líder","Activo","SOCIOS",None,"Socio Club de Arte y Cultura","943742516","2019-01-01"),
            ("nadia.olaya@itaca.com","Nadia Lissett Savitzky Olaya","Líder","Activo","SOCIOS",None,"Socia Ítaca Hub","978661349","2016-01-01"),
            ("eddie.cespedes@itaca.com","Eddie Raúl Valdiviezo Céspedes","Líder","Activo","SOCIOS",None,"Socio Ítaca Hub","958928102","2017-01-02"),
            ("keila.zegarra@itaca.com","Keila Cornejo Zegarra","Líder","Activo","SOCIOS",None,"Socia Club de Arte","929966010","2019-08-01"),
            ("luciana.calderon@itaca.com","Luciana Rubí Portilla Calderón","Líder","Activo","SOCIOS",None,"Socia Inversionista Kids Piura","991570706","2023-04-01"),
            ("brando.camacho@itaca.com","Brando Alonso Gallesi Camacho","Líder","Activo","SOCIOS",None,"Socio Ítaca Kids Lima","913066690","2023-12-31"),
            ("jesus.andrade@itaca.com","Jesús Andrade","Líder","Activo","SOCIOS",None,"Socio Ítaca Conversemos","954044292",""),
            ("nadia.echevarria@itaca.com","Nadia Susiré Herrera Echevarría","Líder","Activo","SOCIOS",None,"Socia Ítaca Kids Lima","964589249",""),
        ]
        for u in users:
            email, nombre, rol, estado, unidad, email_lider, cargo, cel, ingreso = u
            db.execute("INSERT OR IGNORE INTO usuarios VALUES (?,?,?,?,?,?,?,?,?)",
                (email, nombre, rol, estado, unidad, email_lider, now, now, 'Itaca2026!'))
            db.execute("""INSERT OR IGNORE INTO identidad
                (email,nombre,puesto,rol,unidad,estado,email_lider,telefono,fecha_ingreso,fecha_actualizacion)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (email, nombre, cargo, rol, unidad, estado, email_lider, cel, ingreso, now))
        # Algunos check-ins de ejemplo
        for i, email in enumerate(["astrid.vivas@itaca.com","grecia.elera@itaca.com","daniela.collantes@itaca.com"]):
            for w in range(4):
                d = datetime.now() - timedelta(weeks=w)
                estados = ["GENIAL","NORMAL","DIFICIL","NORMAL"]
                estres = [2, 3, 4, 2]
                cid = f"{email}_{d.strftime('%Y-%m-%d')}"
                sem = f"{d.year}-S{d.isocalendar()[1]:02d}"
                db.execute("INSERT OR IGNORE INTO checkins VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (cid, email, estados[w], estres[w], "Trabajo", "Concentrado,Determinado",
                     "", d.isoformat(), sem, 1 if estres[w]>=4 else 0))
        # Faros de ejemplo con colaboradores reales
        faros_data = [
            ("astrid.vivas@itaca.com","Astrid Adanai Ramos Vivas","mirai.coronado@itaca.com","Mirai Nishimura Coronado","Faro de Valor","ITACTIVIDAD","Ardilla","Gracias por resolver el tema de contratos sin que nadie te lo pidiera. Eso es ITACTIVIDAD pura."),
            ("grecia.elera@itaca.com","Grecia Palacios Elera","yazmin.alvarado@itaca.com","Yazmin Fiorella Castillo Alvarado","Faro de Aliento","Muro de Confianza","Ganso","Sé que esta semana fue intensa con las consultas. Quiero que sepas que cuentas con todo el equipo."),
            ("daniela.collantes@itaca.com","Daniela Fernanda Tocto Collantes","santiago.zambrano@itaca.com","Santiago Sánchez Zambrano","Faro de Guía","+1 Sí Importa","Castor","Gracias por enseñarme a usar las métricas de pauta. Siempre das la milla extra."),
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

        # Puestos con DISC ideal (para semáforo de encaje Torre de Control)
        puestos_seed = [
            ("PU001","Entrenador Kids","Amarillo","Verde","KIDS","Facilitador de talleres infantiles"),
            ("PU002","Psicólogo","Verde","Azul","CONVER","Atención psicológica"),
            ("PU003","Psicóloga","Verde","Azul","CONVER","Atención psicológica"),
            ("PU004","Socio / Gerente","Rojo","Amarillo","GENERAL","Líder de unidad de negocio"),
            ("PU005","Socio","Rojo","Amarillo","GENERAL","Socio fundador / líder"),
            ("PU006","Diseñador gráfico","Azul","Amarillo","MARKETING","Diseño de piezas gráficas"),
            ("PU007","Asistente Gerencial","Azul","Verde","GENERAL","Soporte administrativo"),
            ("PU008","Project Manager","Rojo","Azul","MARKETING","Gestión de proyectos"),
            ("PU009","Docente","Amarillo","Verde","EDUCACION","Facilitador educativo"),
            ("PU010","Asistente Contable","Azul","Rojo","B&J","Contabilidad"),
            ("PU011","Auxiliar Contable","Azul","Verde","B&J","Soporte contable"),
            ("PU012","Coordinadora","Rojo","Verde","GENERAL","Coordinación de equipo"),
            ("PU013","Creador de contenido","Amarillo","Azul","MARKETING","Contenido digital"),
            ("PU014","Analista de pauta","Azul","Rojo","MARKETING","Análisis de pauta digital"),
            ("PU015","Videógrafo","Amarillo","Azul","321 SHOW","Producción audiovisual"),
            ("PU016","Gestora de Talento Humano","Verde","Rojo","ITACA HUB","GTH / Admin"),
            ("PU017","Practicante","Verde","Amarillo","GENERAL","Prácticas pre-profesionales"),
            ("PU018","Marketing","Amarillo","Rojo","MARKETING","Estrategia de marketing"),
            ("PU019","Entrenadora Kids","Amarillo","Verde","KIDS","Facilitadora de talleres infantiles"),
            ("PU020","Entrenadora Kids Arequipa","Amarillo","Verde","KIDS","Facilitadora Kids Arequipa"),
            ("PU021","Entrenadora Kids Piura","Amarillo","Verde","KIDS","Facilitadora Kids Piura"),
            ("PU022","Entrenador Kids Lima","Amarillo","Verde","KIDS","Facilitador Kids Lima"),
            ("PU023","Entrenadora Kids Lima","Amarillo","Verde","KIDS","Facilitadora Kids Lima"),
            ("PU024","Co-entrenadora Kids Lima","Amarillo","Verde","KIDS","Co-facilitadora Kids Lima"),
            ("PU025","Psicóloga Kids","Verde","Amarillo","KIDS","Atención psicológica infantil"),
            ("PU026","Socio Ítaca Hub","Rojo","Amarillo","ITACA HUB","Socio principal"),
            ("PU027","Director comercial","Rojo","Amarillo","ITACA HUB","Dirección comercial"),
            ("PU028","Coordinador administrativo","Azul","Rojo","ITACA HUB","Coordinación admin"),
            ("PU029","Directora y entrenadora","Rojo","Amarillo","ECO","Dirección + facilitación"),
            ("PU030","Entrenador / Director","Rojo","Amarillo","EDUCACION","Director educativo"),
            ("PU031","Socio / Director","Rojo","Azul","B&J","Dirección B&J"),
            ("PU032","Practicante Hub","Verde","Amarillo","ITACA HUB","Prácticas Hub"),
            ("PU033","Practicante Marco Legal","Azul","Verde","ITACA HUB","Prácticas legales"),
            ("PU034","Practicante Editora","Amarillo","Azul","ITACA HUB","Prácticas edición"),
            ("PU035","Practicante RH","Verde","Azul","ITACA HUB","Prácticas RH"),
            ("PU036","Practicante CC","Amarillo","Verde","MARKETING","Prácticas CC"),
            ("PU037","Procesos administrativos","Azul","Verde","ITACA HUB","Gestión de procesos"),
        ]
        for p in puestos_seed:
            db.execute("INSERT OR IGNORE INTO puestos_perfiles VALUES (?,?,?,?,?,?)", p)

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

# ═══════════════════════════════════════════
# EVALUACIÓN 360 DE LIDERAZGO
# ═══════════════════════════════════════════

def save_eval_360(email_evaluado, email_evaluador, periodo, v1, v2, v3, v4, v5, v6, promedio, comentario):
    eid = f"E360_{int(datetime.now().timestamp()*1000)}"
    with get_db() as conn:
        conn.execute("INSERT INTO eval_360 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (eid, email_evaluado, email_evaluador, periodo, datetime.now().isoformat(),
             1, v1, v2, v3, v4, v5, v6, promedio, comentario))

def get_eval_360_results(email_evaluado, periodo=None):
    with get_db() as conn:
        if periodo:
            rows = conn.execute("SELECT * FROM eval_360 WHERE email_evaluado=? AND periodo=?",
                (email_evaluado, periodo)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM eval_360 WHERE email_evaluado=? ORDER BY fecha DESC",
                (email_evaluado,)).fetchall()
        return dict_rows(rows)

def get_360_avg(email_evaluado, periodo):
    with get_db() as conn:
        row = conn.execute("""SELECT AVG(vision) as vision, AVG(planificacion) as planificacion,
            AVG(encaje) as encaje, AVG(entrenamiento) as entrenamiento,
            AVG(evaluacion_mejora) as evaluacion_mejora, AVG(reconocimiento) as reconocimiento,
            AVG(promedio) as promedio, COUNT(*) as total
            FROM eval_360 WHERE email_evaluado=? AND periodo=?""",
            (email_evaluado, periodo)).fetchone()
        return dict_row(row)

def has_evaluated_360(email_evaluador, email_evaluado, periodo):
    with get_db() as conn:
        return conn.execute("SELECT 1 FROM eval_360 WHERE email_evaluador=? AND email_evaluado=? AND periodo=?",
            (email_evaluador, email_evaluado, periodo)).fetchone() is not None

# ═══════════════════════════════════════════
# EVALUACIÓN DE DESEMPEÑO
# ═══════════════════════════════════════════

def save_eval_desempeno(email, periodo, evaluador_email, evaluador_nombre,
    cumplimiento, calidad, equipo, comunicacion, iniciativa, promedio,
    fortalezas, areas_mejora, plan, comentario):
    eid = f"ED_{int(datetime.now().timestamp()*1000)}"
    with get_db() as conn:
        conn.execute("INSERT INTO eval_desempeno VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (eid, email, periodo, datetime.now().isoformat(), evaluador_email, evaluador_nombre,
             cumplimiento, calidad, equipo, comunicacion, iniciativa, promedio,
             fortalezas, areas_mejora, plan, comentario))

def get_eval_desempeno(email):
    with get_db() as conn:
        return dict_rows(conn.execute("SELECT * FROM eval_desempeno WHERE email=? ORDER BY fecha DESC",
            (email,)).fetchall())

# ═══════════════════════════════════════════
# CAPACITACIONES
# ═══════════════════════════════════════════

def add_capacitacion(email, nombre, tipo, horas, fecha, certificado, institucion, notas):
    cid = f"CAP_{int(datetime.now().timestamp()*1000)}"
    with get_db() as conn:
        conn.execute("INSERT INTO capacitaciones VALUES (?,?,?,?,?,?,?,?,?)",
            (cid, email, nombre, tipo, horas, fecha, 1 if certificado else 0, institucion, notas))

def get_capacitaciones(email):
    with get_db() as conn:
        return dict_rows(conn.execute("SELECT * FROM capacitaciones WHERE email=? ORDER BY fecha DESC",
            (email,)).fetchall())

# ═══════════════════════════════════════════
# GENERADOR DE REPORTES (DATA)
# ═══════════════════════════════════════════

def get_reporte_estrategico(unidad):
    with get_db() as conn:
        focos = dict_rows(conn.execute("SELECT * FROM focos WHERE unidad=? AND estado!='Eliminado'", (unidad,)).fetchall())
        for f in focos:
            f["krs"] = dict_rows(conn.execute("SELECT * FROM krs WHERE foco_id=? AND estado!='Eliminado'", (f["foco_id"],)).fetchall())
            f["tareas"] = dict_rows(conn.execute("SELECT * FROM tareas WHERE foco_id=? AND estado!='Eliminado'", (f["foco_id"],)).fetchall())
            total_t = len(f["tareas"])
            comp_t = len([t for t in f["tareas"] if t["estado"] == "Completado"])
            venc_t = len([t for t in f["tareas"] if t.get("fecha_limite") and t["fecha_limite"] < datetime.now().strftime("%Y-%m-%d") and t["estado"] != "Completado"])
            f["tareas_total"] = total_t
            f["tareas_completadas"] = comp_t
            f["tareas_vencidas"] = venc_t
        return focos

def get_reporte_clima(unidad=None, dias=30):
    with get_db() as conn:
        fecha_desde = (datetime.now() - timedelta(days=dias)).isoformat()
        if unidad:
            checkins = dict_rows(conn.execute("""
                SELECT c.*, i.nombre, i.unidad FROM checkins c
                JOIN identidad i ON c.email = i.email
                WHERE i.unidad=? AND c.fecha > ? ORDER BY c.fecha DESC""",
                (unidad, fecha_desde)).fetchall())
        else:
            checkins = dict_rows(conn.execute("""
                SELECT c.*, i.nombre, i.unidad FROM checkins c
                JOIN identidad i ON c.email = i.email
                WHERE c.fecha > ? ORDER BY c.fecha DESC""",
                (fecha_desde,)).fetchall())
        if not checkins:
            return {"total": 0, "avg_estres": 0, "alertas": 0, "por_estado": {}, "por_unidad": {}}
        avg_estres = sum(c["nivel_estres"] for c in checkins) / len(checkins)
        alertas = len([c for c in checkins if c["nivel_estres"] >= 4])
        por_estado = {}
        for c in checkins:
            e = c["estado_general"]
            por_estado[e] = por_estado.get(e, 0) + 1
        por_unidad = {}
        for c in checkins:
            u = c.get("unidad", "")
            if u not in por_unidad:
                por_unidad[u] = {"total": 0, "sum_estres": 0}
            por_unidad[u]["total"] += 1
            por_unidad[u]["sum_estres"] += c["nivel_estres"]
        for u in por_unidad:
            por_unidad[u]["avg_estres"] = round(por_unidad[u]["sum_estres"] / por_unidad[u]["total"], 1)
        return {
            "total": len(checkins), "avg_estres": round(avg_estres, 1),
            "alertas": alertas, "por_estado": por_estado, "por_unidad": por_unidad
        }

def get_reporte_cultura(dias=30):
    with get_db() as conn:
        fecha_desde = (datetime.now() - timedelta(days=dias)).isoformat()
        faros = dict_rows(conn.execute("SELECT * FROM faros WHERE fecha_envio > ?", (fecha_desde,)).fetchall())
        por_tipo = {}
        for f in faros:
            t = f["tipo_faro"]
            por_tipo[t] = por_tipo.get(t, 0) + 1
        top_emisores = {}
        for f in faros:
            n = f["nombre_emisor"]
            top_emisores[n] = top_emisores.get(n, 0) + 1
        top_receptores = {}
        for f in faros:
            n = f["nombre_receptor"]
            top_receptores[n] = top_receptores.get(n, 0) + 1
        return {
            "total_faros": len(faros), "por_tipo": por_tipo,
            "top_emisores": sorted(top_emisores.items(), key=lambda x: -x[1])[:5],
            "top_receptores": sorted(top_receptores.items(), key=lambda x: -x[1])[:5],
            "celebraciones": sum(f.get("celebraciones", 0) for f in faros)
        }

def get_reporte_ejecutivo():
    with get_db() as conn:
        total_users = conn.execute("SELECT COUNT(*) FROM usuarios WHERE estado='Activo'").fetchone()[0]
        por_unidad = dict_rows(conn.execute("""
            SELECT unidad, COUNT(*) as total FROM usuarios
            WHERE estado='Activo' AND unidad IS NOT NULL GROUP BY unidad ORDER BY unidad""").fetchall())
        por_rol = dict_rows(conn.execute("""
            SELECT rol, COUNT(*) as total FROM usuarios
            WHERE estado='Activo' GROUP BY rol""").fetchall())
    clima = get_reporte_clima()
    cultura = get_reporte_cultura()
    return {
        "total_users": total_users, "por_unidad": por_unidad, "por_rol": por_rol,
        "clima": clima, "cultura": cultura, "fecha": datetime.now().strftime("%d/%m/%Y")
    }

# ═══════════════════════════════════════════
# TABLERO ESTRATÉGICO: FOCOS + KR + TAREAS
# ═══════════════════════════════════════════

def _log_cambio(entidad, entidad_id, campo, anterior, nuevo, email_autor):
    """Registrar cambio en historial (audit trail)"""
    with get_db() as conn:
        cid = f"CHG_{int(datetime.now().timestamp()*1000)}"
        nombre = ""
        row = conn.execute("SELECT nombre FROM identidad WHERE email=?", (email_autor,)).fetchone()
        if row:
            nombre = row[0]
        conn.execute("INSERT INTO historial_cambios VALUES (?,?,?,?,?,?,?,?,?)",
            (cid, entidad, entidad_id, campo, str(anterior), str(nuevo), email_autor, nombre, datetime.now().isoformat()))

# ── FOCOS ──
def create_foco(email_creador, unidad, nombre, descripcion, periodo, fecha_limite):
    fid = f"FOCO_{int(datetime.now().timestamp()*1000)}"
    now = datetime.now().isoformat()
    with get_db() as conn:
        conn.execute("INSERT INTO focos VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (fid, email_creador, unidad, nombre, descripcion, periodo, 0, "En Progreso", now, fecha_limite, 0))
    return fid

def get_focos_by_unidad(unidad):
    with get_db() as conn:
        return dict_rows(conn.execute(
            "SELECT * FROM focos WHERE unidad=? AND estado!='Eliminado' ORDER BY orden, fecha_creacion DESC",
            (unidad,)).fetchall())

def get_focos_by_email(email):
    """Focos de la unidad del usuario"""
    with get_db() as conn:
        row = conn.execute("SELECT unidad FROM identidad WHERE email=?", (email,)).fetchone()
        if not row:
            return []
        return dict_rows(conn.execute(
            "SELECT * FROM focos WHERE unidad=? AND estado!='Eliminado' ORDER BY orden, fecha_creacion DESC",
            (row[0],)).fetchall())

def update_foco(foco_id, email_autor, **kwargs):
    with get_db() as conn:
        old = dict_row(conn.execute("SELECT * FROM focos WHERE foco_id=?", (foco_id,)).fetchone())
        if old:
            for k, v in kwargs.items():
                if str(old.get(k)) != str(v):
                    _log_cambio("foco", foco_id, k, old.get(k), v, email_autor)
        sets = ", ".join(f"{k}=?" for k in kwargs)
        conn.execute(f"UPDATE focos SET {sets} WHERE foco_id=?", (*kwargs.values(), foco_id))

def delete_foco(foco_id, email_autor):
    _log_cambio("foco", foco_id, "estado", "Activo", "Eliminado", email_autor)
    with get_db() as conn:
        conn.execute("UPDATE focos SET estado='Eliminado' WHERE foco_id=?", (foco_id,))

def recalc_foco_progreso(foco_id):
    """Recalcula progreso del foco basado en promedio de KRs"""
    with get_db() as conn:
        krs = conn.execute("SELECT progreso FROM krs WHERE foco_id=? AND estado!='Eliminado'", (foco_id,)).fetchall()
        if krs:
            avg = round(sum(r[0] for r in krs) / len(krs))
            conn.execute("UPDATE focos SET progreso=? WHERE foco_id=?", (avg, foco_id))
            return avg
    return 0

# ── KEY RESULTS ──
def create_kr(foco_id, nombre, meta_valor, unidad_medida, periodicidad, fecha_limite):
    kid = f"KR_{int(datetime.now().timestamp()*1000)}"
    now = datetime.now().isoformat()
    with get_db() as conn:
        conn.execute("INSERT INTO krs VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (kid, foco_id, nombre, meta_valor, 0, unidad_medida, 0, "En Progreso", periodicidad, now, fecha_limite))
    return kid

def get_krs_by_foco(foco_id):
    with get_db() as conn:
        return dict_rows(conn.execute(
            "SELECT * FROM krs WHERE foco_id=? AND estado!='Eliminado' ORDER BY fecha_creacion",
            (foco_id,)).fetchall())

def update_kr(kr_id, email_autor, **kwargs):
    foco_to_recalc = None
    with get_db() as conn:
        old = dict_row(conn.execute("SELECT * FROM krs WHERE kr_id=?", (kr_id,)).fetchone())
        if old:
            for k, v in kwargs.items():
                if str(old.get(k)) != str(v):
                    _log_cambio("kr", kr_id, k, old.get(k), v, email_autor)
            foco_to_recalc = old["foco_id"]
        sets = ", ".join(f"{k}=?" for k in kwargs)
        conn.execute(f"UPDATE krs SET {sets} WHERE kr_id=?", (*kwargs.values(), kr_id))
    if foco_to_recalc:
        recalc_foco_progreso(foco_to_recalc)

def delete_kr(kr_id, email_autor):
    _log_cambio("kr", kr_id, "estado", "Activo", "Eliminado", email_autor)
    foco_to_recalc = None
    with get_db() as conn:
        row = conn.execute("SELECT foco_id FROM krs WHERE kr_id=?", (kr_id,)).fetchone()
        conn.execute("UPDATE krs SET estado='Eliminado' WHERE kr_id=?", (kr_id,))
        if row:
            foco_to_recalc = row[0]
    if foco_to_recalc:
        recalc_foco_progreso(foco_to_recalc)

def recalc_kr_progreso(kr_id):
    """Recalcula progreso del KR basado en promedio de tareas"""
    with get_db() as conn:
        tareas = conn.execute("SELECT progreso FROM tareas WHERE kr_id=? AND estado!='Eliminado'", (kr_id,)).fetchall()
        if tareas:
            avg = round(sum(r[0] for r in tareas) / len(tareas))
            conn.execute("UPDATE krs SET progreso=? WHERE kr_id=?", (avg, kr_id))
            row = conn.execute("SELECT foco_id FROM krs WHERE kr_id=?", (kr_id,)).fetchone()
            if row:
                # Inline recalc foco to avoid nested connection
                foco_id = row[0]
                krs = conn.execute("SELECT progreso FROM krs WHERE foco_id=? AND estado!='Eliminado'", (foco_id,)).fetchall()
                if krs:
                    favg = round(sum(r[0] for r in krs) / len(krs))
                    conn.execute("UPDATE focos SET progreso=? WHERE foco_id=?", (favg, foco_id))
            return avg
    return 0

# ── TAREAS ──
def create_tarea(kr_id, foco_id, titulo, descripcion, email_responsable, fecha_inicio, fecha_limite, prioridad, email_creador):
    tid = f"TAR_{int(datetime.now().timestamp()*1000)}"
    now = datetime.now().isoformat()
    with get_db() as conn:
        nombre_resp = ""
        row = conn.execute("SELECT nombre FROM identidad WHERE email=?", (email_responsable,)).fetchone()
        if row:
            nombre_resp = row[0]
        conn.execute("INSERT INTO tareas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (tid, kr_id, foco_id, titulo, descripcion, email_responsable, nombre_resp,
             fecha_inicio, fecha_limite, None, "Pendiente", prioridad, 0, "",
             now, now, email_creador))
    return tid

def get_tareas_by_kr(kr_id):
    with get_db() as conn:
        return dict_rows(conn.execute(
            "SELECT * FROM tareas WHERE kr_id=? AND estado!='Eliminado' ORDER BY fecha_limite",
            (kr_id,)).fetchall())

def get_tareas_by_foco(foco_id):
    with get_db() as conn:
        return dict_rows(conn.execute(
            "SELECT * FROM tareas WHERE foco_id=? AND estado!='Eliminado' ORDER BY fecha_limite",
            (foco_id,)).fetchall())

def get_mis_tareas(email):
    with get_db() as conn:
        return dict_rows(conn.execute(
            "SELECT t.*, f.nombre as foco_nombre, k.nombre as kr_nombre FROM tareas t "
            "LEFT JOIN focos f ON t.foco_id = f.foco_id "
            "LEFT JOIN krs k ON t.kr_id = k.kr_id "
            "WHERE t.email_responsable=? AND t.estado NOT IN ('Eliminado','Completado') "
            "ORDER BY t.fecha_limite", (email,)).fetchall())

def update_tarea(tarea_id, email_autor, **kwargs):
    kr_to_recalc = None
    with get_db() as conn:
        old = dict_row(conn.execute("SELECT * FROM tareas WHERE tarea_id=?", (tarea_id,)).fetchone())
        if old:
            for k, v in kwargs.items():
                if str(old.get(k)) != str(v):
                    _log_cambio("tarea", tarea_id, k, old.get(k), v, email_autor)
            kr_to_recalc = old["kr_id"]
        kwargs["ultimo_cambio"] = datetime.now().isoformat()
        kwargs["cambiado_por"] = email_autor
        if kwargs.get("estado") == "Completado" and (not old or old.get("estado") != "Completado"):
            kwargs["fecha_completada"] = datetime.now().isoformat()
            kwargs["progreso"] = 100
        sets = ", ".join(f"{k}=?" for k in kwargs)
        conn.execute(f"UPDATE tareas SET {sets} WHERE tarea_id=?", (*kwargs.values(), tarea_id))
    if kr_to_recalc:
        recalc_kr_progreso(kr_to_recalc)

def delete_tarea(tarea_id, email_autor):
    _log_cambio("tarea", tarea_id, "estado", "Activo", "Eliminado", email_autor)
    kr_to_recalc = None
    with get_db() as conn:
        row = conn.execute("SELECT kr_id FROM tareas WHERE tarea_id=?", (tarea_id,)).fetchone()
        conn.execute("UPDATE tareas SET estado='Eliminado' WHERE tarea_id=?", (tarea_id,))
        if row:
            kr_to_recalc = row[0]
    if kr_to_recalc:
        recalc_kr_progreso(kr_to_recalc)

# ── HISTORIAL ──
def get_historial(entidad_id, limit=20):
    with get_db() as conn:
        return dict_rows(conn.execute(
            "SELECT * FROM historial_cambios WHERE entidad_id=? ORDER BY fecha DESC LIMIT ?",
            (entidad_id, limit)).fetchall())

# ── ANALYTICS ESTRATÉGICO ──
def get_strategic_stats(unidad):
    with get_db() as conn:
        focos = conn.execute("SELECT COUNT(*) FROM focos WHERE unidad=? AND estado!='Eliminado'", (unidad,)).fetchone()[0]
        avg_prog = conn.execute("SELECT AVG(progreso) FROM focos WHERE unidad=? AND estado!='Eliminado'", (unidad,)).fetchone()[0] or 0
        tareas_total = conn.execute(
            "SELECT COUNT(*) FROM tareas t JOIN focos f ON t.foco_id=f.foco_id WHERE f.unidad=? AND t.estado!='Eliminado'",
            (unidad,)).fetchone()[0]
        tareas_vencidas = conn.execute(
            "SELECT COUNT(*) FROM tareas t JOIN focos f ON t.foco_id=f.foco_id "
            "WHERE f.unidad=? AND t.estado NOT IN ('Completado','Eliminado') AND t.fecha_limite < ?",
            (unidad, datetime.now().strftime("%Y-%m-%d"))).fetchone()[0]
        return {"focos": focos, "avg_progreso": round(avg_prog), "tareas_total": tareas_total, "tareas_vencidas": tareas_vencidas}

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

# ═══════════════════════════════════════════
# ADMIN: GESTIÓN DE COLABORADORES
# ═══════════════════════════════════════════

def update_password(email, new_password):
    """Actualizar contraseña de un usuario"""
    with get_db() as db:
        db.execute("UPDATE usuarios SET password=? WHERE email=?", (new_password, email))

def add_colaborador(email, nombre, rol, unidad, email_lider, cargo, telefono, fecha_ingreso):
    """Agregar un nuevo colaborador (desde panel admin)"""
    now = datetime.now().isoformat()
    with get_db() as conn:
        existing = conn.execute("SELECT 1 FROM usuarios WHERE email=?", (email,)).fetchone()
        if existing:
            return False, "Ya existe un usuario con ese email."
        conn.execute("INSERT INTO usuarios VALUES (?,?,?,?,?,?,?,?,?)",
            (email, nombre, rol, "Activo", unidad, email_lider, now, now, "Itaca2026!"))
        conn.execute("""INSERT INTO identidad
            (email,nombre,puesto,rol,unidad,estado,email_lider,telefono,fecha_ingreso,fecha_actualizacion)
            VALUES (?,?,?,?,?,?,?,?,?,?)""",
            (email, nombre, cargo, rol, unidad, "Activo", email_lider, telefono, fecha_ingreso, now))
    return True, f"✅ {nombre} agregado exitosamente."

def deactivate_colaborador(email):
    """Desactivar un colaborador (no se borra, se marca inactivo)"""
    with get_db() as conn:
        conn.execute("UPDATE usuarios SET estado='Inactivo' WHERE email=?", (email,))
        conn.execute("UPDATE identidad SET estado='Inactivo' WHERE email=?", (email,))
    return True, "Colaborador desactivado."

def reactivate_colaborador(email):
    """Reactivar un colaborador"""
    with get_db() as conn:
        conn.execute("UPDATE usuarios SET estado='Activo' WHERE email=?", (email,))
        conn.execute("UPDATE identidad SET estado='Activo' WHERE email=?", (email,))
    return True, "Colaborador reactivado."

def update_colaborador(email, **kwargs):
    """Actualizar datos de un colaborador (nombre, rol, unidad, etc.)"""
    with get_db() as conn:
        # Update usuarios
        user_fields = {k: v for k, v in kwargs.items() if k in ("nombre","rol","unidad","email_lider")}
        if user_fields:
            sets = ", ".join(f"{k}=?" for k in user_fields)
            conn.execute(f"UPDATE usuarios SET {sets} WHERE email=?", (*user_fields.values(), email))
        # Update identidad
        ident_fields = {k: v for k, v in kwargs.items() if k in ("nombre","rol","unidad","email_lider","puesto","telefono")}
        if ident_fields:
            sets = ", ".join(f"{k}=?" for k in ident_fields)
            conn.execute(f"UPDATE identidad SET {sets}, fecha_actualizacion=? WHERE email=?",
                (*ident_fields.values(), datetime.now().isoformat(), email))

def reset_password(email):
    """Resetear contraseña a la default"""
    with get_db() as conn:
        conn.execute("UPDATE usuarios SET password='Itaca2026!' WHERE email=?", (email,))
    return True, "Contraseña reseteada a Itaca2026!"

def get_all_users_admin():
    """Obtener TODOS los usuarios (activos e inactivos) para el panel admin"""
    with get_db() as conn:
        return dict_rows(conn.execute("""
            SELECT u.*, i.puesto, i.telefono, i.fecha_ingreso
            FROM usuarios u
            LEFT JOIN identidad i ON u.email = i.email
            ORDER BY u.estado DESC, u.unidad, u.nombre""").fetchall())

def get_units():
    """Obtener lista de unidades únicas"""
    with get_db() as conn:
        rows = conn.execute("SELECT DISTINCT unidad FROM usuarios WHERE unidad IS NOT NULL AND unidad != '' ORDER BY unidad").fetchall()
        return [r[0] for r in rows]


# ═══════════════════════════════════════════════════════════════
# NUEVOS MÓDULOS v2.0: ESCUDO DE ESPARTA
# ═══════════════════════════════════════════════════════════════

def check_escudo_esparta(email_responsable):
    """
    🛡️ ESCUDO DE ESPARTA (Anti-Burnout):
    Si último estrés == 5 AND tareas vencidas > 3 → bloquear asignación
    Retorna: (bloqueado: bool, mensaje: str, nombre: str)
    """
    with get_db() as conn:
        ci = conn.execute(
            "SELECT nivel_estres FROM checkins WHERE email=? ORDER BY fecha DESC LIMIT 1",
            (email_responsable,)).fetchone()
        if not ci:
            return False, "", ""
        hoy = datetime.now().strftime("%Y-%m-%d")
        vencidas = conn.execute(
            "SELECT COUNT(*) FROM tareas WHERE email_responsable=? "
            "AND estado NOT IN ('Completado','Eliminado') AND fecha_limite < ?",
            (email_responsable, hoy)).fetchone()[0]
        nombre_row = conn.execute(
            "SELECT nombre FROM identidad WHERE email=?",
            (email_responsable,)).fetchone()
        nombre = nombre_row[0] if nombre_row else email_responsable
        if ci[0] == 5 and vencidas > 3:
            return True, (
                f"🛡️ Escudo de Esparta Activado: {nombre} superó su límite "
                f"(Estrés 5/5, {vencidas} tareas vencidas). "
                f"Reasigna a otro tripulante."
            ), nombre
    return False, "", ""


# ═══════════════════════════════════════════════════════════════
# PUESTOS / PERFILES DISC (Semáforo de Encaje)
# ═══════════════════════════════════════════════════════════════

def get_all_puestos():
    """Obtener todos los perfiles de puesto"""
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM puestos_perfiles ORDER BY nombre_puesto").fetchall())

def get_puesto_perfil(nombre_puesto):
    """Obtener perfil DISC ideal para un puesto"""
    with get_db() as db:
        return dict_row(db.execute(
            "SELECT * FROM puestos_perfiles WHERE nombre_puesto=?",
            (nombre_puesto,)).fetchone())

def add_puesto_perfil(nombre_puesto, disc_principal, disc_secundario, unidad, descripcion):
    """Agregar un perfil de puesto"""
    pid = f"PU_{int(datetime.now().timestamp()*1000)}"
    with get_db() as db:
        db.execute("INSERT INTO puestos_perfiles VALUES (?,?,?,?,?,?)",
            (pid, nombre_puesto, disc_principal, disc_secundario, unidad, descripcion))
    return pid

def get_encaje_disc(email):
    """
    Semáforo de Encaje DISC:
    Cruza el DISC del colaborador vs el DISC ideal del puesto
    Retorna: {"color": "Verde/Amarillo/Rojo", "emoji", "msg", "score"}
    """
    ident = get_identidad(email)
    if not ident or not ident.get("arquetipo_disc"):
        return None
    puesto_nombre = ident.get("puesto", "")
    perfil = get_puesto_perfil(puesto_nombre)
    if not perfil:
        return None
    disc_p = ident.get("arquetipo_disc", "")
    disc_s = ident.get("arquetipo_secundario", "")
    ideal_p = perfil.get("disc_ideal_principal", "")
    ideal_s = perfil.get("disc_ideal_secundario", "")
    score = 0
    if disc_p == ideal_p: score += 2
    elif disc_p == ideal_s: score += 1
    if disc_s == ideal_s: score += 1
    elif disc_s == ideal_p: score += 1
    if score >= 3:
        return {"color": "Verde", "emoji": "🟢", "msg": "Encaje ideal", "score": score}
    elif score >= 1:
        return {"color": "Amarillo", "emoji": "🟡", "msg": "Encaje parcial – explorar", "score": score}
    else:
        return {"color": "Rojo", "emoji": "🔴", "msg": "Desencaje – revisar reubicación", "score": score}


# ═══════════════════════════════════════════════════════════════
# TORRE DE CONTROL: ORÁCULO DE FUGAS + MATRIZ 9-BOX
# ═══════════════════════════════════════════════════════════════

def get_flight_risk():
    """
    🔮 ORÁCULO DE FUGAS (Flight Risk):
    Condición: estrés promedio >= 4 (últimas 2 semanas)
               AND 0 faros (enviados+recibidos) último mes
               AND > 2 tareas vencidas
    """
    hoy = datetime.now()
    hace_14d = (hoy - timedelta(days=14)).isoformat()
    hace_30d = (hoy - timedelta(days=30)).isoformat()
    hoy_str = hoy.strftime("%Y-%m-%d")
    with get_db() as conn:
        users = dict_rows(conn.execute(
            "SELECT email, nombre, unidad, puesto FROM identidad WHERE estado='Activo'"
        ).fetchall())
        risk_list = []
        for u in users:
            e = u["email"]
            avg_row = conn.execute(
                "SELECT AVG(nivel_estres) FROM checkins WHERE email=? AND fecha >= ?",
                (e, hace_14d)).fetchone()
            avg_estres = avg_row[0] if avg_row[0] else 0
            faros_env = conn.execute(
                "SELECT COUNT(*) FROM faros WHERE email_emisor=? AND fecha_envio >= ?",
                (e, hace_30d)).fetchone()[0]
            faros_rec = conn.execute(
                "SELECT COUNT(*) FROM faros WHERE email_receptor=? AND fecha_envio >= ?",
                (e, hace_30d)).fetchone()[0]
            vencidas = conn.execute(
                "SELECT COUNT(*) FROM tareas WHERE email_responsable=? "
                "AND estado NOT IN ('Completado','Eliminado') AND fecha_limite < ?",
                (e, hoy_str)).fetchone()[0]
            if avg_estres >= 4 and (faros_env + faros_rec) == 0 and vencidas > 2:
                risk_list.append({
                    **u, "avg_estres": round(avg_estres, 1),
                    "faros_total": faros_env + faros_rec,
                    "tareas_vencidas": vencidas, "riesgo": "ALTO"
                })
        return risk_list

def get_9box_data():
    """
    📊 MATRIZ 9-BOX:
    Eje X = Desempeño (promedio progreso tareas)
    Eje Y = Potencial (promedio eval 360 + faros recibidos)
    """
    with get_db() as conn:
        users = dict_rows(conn.execute(
            "SELECT email, nombre, unidad FROM identidad WHERE estado='Activo'"
        ).fetchall())
        data = []
        for u in users:
            e = u["email"]
            desemp = conn.execute(
                "SELECT AVG(progreso) FROM tareas "
                "WHERE email_responsable=? AND estado!='Eliminado'",
                (e,)).fetchone()[0] or 0
            avg_360 = conn.execute(
                "SELECT AVG(promedio) FROM eval_360 WHERE email_evaluado=?",
                (e,)).fetchone()[0] or 0
            faros_rec = conn.execute(
                "SELECT COUNT(*) FROM faros WHERE email_receptor=? AND fecha_envio > ?",
                (e, (datetime.now() - timedelta(days=90)).isoformat())).fetchone()[0]
            potencial = (avg_360 * 20) + min(faros_rec * 5, 20)
            if desemp > 0 or potencial > 0:
                d_level = "Alto" if desemp >= 70 else "Medio" if desemp >= 40 else "Bajo"
                p_level = "Alto" if potencial >= 70 else "Medio" if potencial >= 40 else "Bajo"
                data.append({
                    "email": e, "nombre": u["nombre"], "unidad": u["unidad"],
                    "desempeno": round(desemp, 1), "potencial": round(potencial, 1),
                    "d_level": d_level, "p_level": p_level,
                    "box": f"{p_level} Potencial / {d_level} Desempeño"
                })
        return data


# ═══════════════════════════════════════════════════════════════
# CRM — EL PUERTO
# ═══════════════════════════════════════════════════════════════

def create_lead(telefono, nombre_apoderado, nombre_nino, edad, ciudad,
                origen, precalificacion, unidad, email_asesor, notas=""):
    """Crear un nuevo lead en el pipeline"""
    lid = f"LEAD_{int(datetime.now().timestamp()*1000)}"
    now = datetime.now().isoformat()
    with get_db() as db:
        db.execute("INSERT INTO crm_leads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (lid, telefono, nombre_apoderado, nombre_nino, edad, ciudad,
             origen, precalificacion, "Nuevo", unidad, notas, email_asesor, now, now))
    return lid

def get_leads(unidad=None, estado=None):
    """Obtener leads filtrados por unidad y/o estado"""
    with get_db() as db:
        q = "SELECT * FROM crm_leads WHERE 1=1"
        params = []
        if unidad:
            q += " AND unidad=?"
            params.append(unidad)
        if estado:
            q += " AND estado=?"
            params.append(estado)
        return dict_rows(db.execute(q + " ORDER BY fecha_creacion DESC", params).fetchall())

def get_lead(lead_id):
    """Obtener un lead por ID"""
    with get_db() as db:
        return dict_row(db.execute(
            "SELECT * FROM crm_leads WHERE lead_id=?", (lead_id,)).fetchone())

def update_lead(lead_id, **kwargs):
    """Actualizar campos de un lead"""
    kwargs["fecha_actualizacion"] = datetime.now().isoformat()
    with get_db() as db:
        sets = ", ".join(f"{k}=?" for k in kwargs)
        db.execute(f"UPDATE crm_leads SET {sets} WHERE lead_id=?",
                   (*kwargs.values(), lead_id))

def inscribir_lead(lead_id, monto_total, num_cuotas):
    """
    Lead → Inscrito: genera cuotas automáticamente.
    Cuando una cuota se pague, ingresará a finanzas_flujo.
    """
    update_lead(lead_id, estado="Inscrito")
    lead = get_lead(lead_id)
    if not lead:
        return
    monto_cuota = round(monto_total / num_cuotas, 2)
    for i in range(1, num_cuotas + 1):
        cid = f"CUO_{int(datetime.now().timestamp()*1000)}_{i}"
        fecha_venc = (datetime.now() + timedelta(days=30 * i)).strftime("%Y-%m-%d")
        with get_db() as db:
            db.execute("INSERT INTO ventas_cuotas VALUES (?,?,?,?,?,?,?,?)",
                (cid, lead_id, i, monto_cuota, 0, fecha_venc, None, "Pendiente"))

def pagar_cuota(cuota_id, monto_pagado):
    """
    Pagar cuota → ingresa automáticamente a finanzas_flujo como Ingreso.
    """
    with get_db() as db:
        cuota = dict_row(db.execute(
            "SELECT * FROM ventas_cuotas WHERE cuota_id=?", (cuota_id,)).fetchone())
        if not cuota:
            return False
        db.execute(
            "UPDATE ventas_cuotas SET monto_pagado=?, fecha_pago=?, estado='Pagado' WHERE cuota_id=?",
            (monto_pagado, datetime.now().isoformat(), cuota_id))
        # Buscar unidad del lead
        lead = dict_row(db.execute(
            "SELECT * FROM crm_leads WHERE lead_id=?", (cuota["lead_id"],)).fetchone())
        unidad = lead["unidad"] if lead else ""
        # Auto-registro en finanzas
        fid = f"FIN_{int(datetime.now().timestamp()*1000)}"
        db.execute("INSERT INTO finanzas_flujo VALUES (?,?,?,?,?,?,?,?,?,?)",
            (fid, unidad, "Ingreso", "Cuota", monto_pagado,
             datetime.now().strftime("%Y-%m-%d"), "",
             f"Cuota {cuota['numero_cuota']} - Lead {cuota['lead_id']}",
             "", datetime.now().isoformat()))
    return True

def get_cuotas_by_lead(lead_id):
    """Obtener todas las cuotas de un lead"""
    with get_db() as db:
        return dict_rows(db.execute(
            "SELECT * FROM ventas_cuotas WHERE lead_id=? ORDER BY numero_cuota",
            (lead_id,)).fetchall())


# ═══════════════════════════════════════════════════════════════
# FINANZAS — LA BÓVEDA
# ═══════════════════════════════════════════════════════════════

def add_flujo_financiero(unidad, tipo, categoria, monto, fecha, campana,
                         descripcion, registrado_por):
    """Registrar un movimiento financiero"""
    fid = f"FIN_{int(datetime.now().timestamp()*1000)}"
    with get_db() as db:
        db.execute("INSERT INTO finanzas_flujo VALUES (?,?,?,?,?,?,?,?,?,?)",
            (fid, unidad, tipo, categoria, monto, fecha, campana,
             descripcion, registrado_por, datetime.now().isoformat()))
    return fid

def get_flujos(unidad=None, tipo=None, dias=30):
    """Obtener flujos financieros filtrados"""
    with get_db() as db:
        q = "SELECT * FROM finanzas_flujo WHERE fecha >= ?"
        params = [(datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")]
        if unidad:
            q += " AND unidad=?"
            params.append(unidad)
        if tipo:
            q += " AND tipo=?"
            params.append(tipo)
        return dict_rows(db.execute(q + " ORDER BY fecha DESC", params).fetchall())

def get_resumen_financiero(unidad=None, dias=30):
    """Resumen: ingresos, egresos, balance, movimientos"""
    flujos = get_flujos(unidad, dias=dias)
    ingresos = sum(f["monto"] for f in flujos if f["tipo"] == "Ingreso")
    egresos = sum(f["monto"] for f in flujos if f["tipo"] == "Egreso")
    return {
        "ingresos": ingresos, "egresos": egresos,
        "balance": ingresos - egresos, "movimientos": len(flujos)
    }


# Inicializar al importar
init_db()
