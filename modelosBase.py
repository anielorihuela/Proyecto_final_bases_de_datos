from sqlalchemy import create_engine, Column, Integer, String, Date, SmallInteger, ForeignKey, CheckConstraint, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
from conexion import DB_CONNECTION_STRING
from datetime import date

# Configuración de la base de datos
engine = create_engine(DB_CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

#Modelos
class Region(Base):
    __tablename__ = "region"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(20), nullable=False, unique=True)

class Estado(Base):
    __tablename__ = "estado"
    
    abbr = Column(String(2), primary_key=True)
    nombre = Column(String(40), nullable=False, unique=True)
    id_region = Column(Integer, ForeignKey("region.id", ondelete="restrict"), nullable=False)

class GrupoPooblacional(Base):
    __tablename__ = "grupo_poblacional"
    
    codigo = Column(String(4), primary_key=True)
    descripcion = Column(String(120), nullable=False)
    min_poblacion = Column(Integer)
    max_poblacion = Column(Integer)
    rank = Column(SmallInteger)
    
    __table_args__ = (
        CheckConstraint(
            "min_poblacion is null or max_poblacion is null or min_poblacion <= max_poblacion",
            name="rango_valido"
        ),
        CheckConstraint("rank between 1 and 10", name="rank_valido"),
    )

class Agencia(Base):
    __tablename__ = "agencia"
    
    ori = Column(String(9), primary_key=True)
    nombre = Column(String(120), nullable=False)
    tipo = Column(String(60), nullable=False)
    estado_abbr = Column(String(2), ForeignKey("estado.abbr", ondelete="restrict"), nullable=False)
    grupo_poblacional = Column(String(4), ForeignKey("grupo_poblacional.codigo", ondelete="restrict"), nullable=False)

class Ofensa(Base):
    __tablename__ = "ofensa"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(500), nullable=False, unique=True)

class Ubicacion(Base):
    __tablename__ = "ubicacion"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False, unique=True)

class Sesgo(Base):
    __tablename__ = "sesgo"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(500), nullable=False, unique=True)

class TipoVictima(Base):
    __tablename__ = "tipo_victima"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(200), nullable=False, unique=True)

class Incidente(Base):
    __tablename__ = "incidente"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agencia_ori = Column(String(9), ForeignKey("agencia.ori", ondelete="restrict"), nullable=False)
    
    # Fecha y año
    fecha_incidente = Column(Date, nullable=False)
    anio_reporte = Column(SmallInteger, nullable=False)
    
    # Ofensores
    raza_del_ofensor = Column(String(60))
    etnicidad_del_ofensor = Column(String(60))
    total_ofensores = Column(SmallInteger, nullable=False)
    numero_ofensores_adultos = Column(SmallInteger)
    numero_ofensores_menores_edad = Column(SmallInteger)
    
    # Víctimas
    numero_victimas_adultas = Column(SmallInteger)
    numero_victimas_menores = Column(SmallInteger)
    total_victimas_indiv_mas_entidades = Column(SmallInteger, nullable=False)
    numero_victimas_indiv = Column(SmallInteger)
    
    # Flags
    ofensa_multiple = Column(String(1), nullable=False)
    sesgo_multiple = Column(String(1), nullable=False)
    
    __table_args__ = (
        CheckConstraint("ofensa_multiple in ('S', 'M')", name="check_ofensa_multiple"),
        CheckConstraint("sesgo_multiple in ('S', 'M')", name="check_sesgo_multiple"),
        CheckConstraint("total_ofensores >= 0", name="check_ofensores"),
        CheckConstraint("total_victimas_indiv_mas_entidades >= 0", name="check_victimas"),
    )

class IncidenteOfensa(Base):
    __tablename__ = "incidente_ofensa"
    
    ofensa_id = Column(Integer, ForeignKey("ofensa.id", ondelete="restrict"), primary_key=True)
    incidente_id = Column(Integer, ForeignKey("incidente.id", ondelete="cascade"), primary_key=True)

class IncidenteUbicacion(Base):
    __tablename__ = "incidente_ubicacion"
    
    ubicacion_id = Column(Integer, ForeignKey("ubicacion.id", ondelete="restrict"), primary_key=True)
    incidente_id = Column(Integer, ForeignKey("incidente.id", ondelete="cascade"), primary_key=True)

class IncidenteSesgo(Base):
    __tablename__ = "incidente_sesgo"
    
    sesgo_id = Column(Integer, ForeignKey("sesgo.id", ondelete="restrict"), primary_key=True)
    incidente_id = Column(Integer, ForeignKey("incidente.id", ondelete="cascade"), primary_key=True)

class IncidenteTipoVictima(Base):
    __tablename__ = "incidente_tipo_victima"
    
    tipo_victima_id = Column(Integer, ForeignKey("tipo_victima.id", ondelete="restrict"), primary_key=True)
    incidente_id = Column(Integer, ForeignKey("incidente.id", ondelete="cascade"), primary_key=True)