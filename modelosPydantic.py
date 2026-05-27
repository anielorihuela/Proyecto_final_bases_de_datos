from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field

#-------------------CREAR-----------------------------------
#Región
class RegionCrear(BaseModel):
    nombre: str
    
#Estado
class EstadoCrear(BaseModel):
    abbr: str = Field(max_length=2)
    nombre : str
    id_region: int
    
#Grupo poblacional
class GrupoPoblacionalCrear(BaseModel):
    codigo: str = Field(max_length=4)
    descripcion: str
    min_poblacion: int
    max_poblacion: int
    rank: int

# Agencia
class AgenciaCrear(BaseModel):
    ori: str = Field(max_length=9)
    nombre: str
    tipo : str
    estado_abbr: str = Field(max_length=2)
    grupo_poblacional: str = Field(max_length=4)
    
    
#Ofensa
class OfensaCrear(BaseModel):
    nombre: str

#ubicación
class UbicacionCrear(BaseModel):
    nombre: str

#sesgo
class SesgoCrear(BaseModel):
    descripcion: str

#tipo de víctima
class TipoVictimaCrear(BaseModel):
    tipo: str

#incidente
class IncidenteCrear(BaseModel):
    fecha: str
    agencia_ori: str = Field(max_length=9)
    fecha_incidente: date
    anio_reporte: int
    raza_del_ofensor: str
    etnicidad_del_ofensor: str
    total_ofensores: int
    numero_ofensores_adultos: int
    numero_ofensores_menores_edad: int
    numero_victimas_adultas: int
    numero_victimas_menores: int
    total_victimas_indiv_mas_entidades: int
    numero_victimas_indiv: int
    ofensa_multiple: str = Field(max_length=1)
    sesgo_multiple: str = Field(max_length=1)

#Incidente ofensa
class IncidenteOfensaCrear(BaseModel):
    ofensa_id: int
    incidente_id: int

#incidente ubicacion
class IncidenteUbicacionCrear(BaseModel):
    ubicacion_id: int
    incidente_id: int

#incidente sesgo
class IncidenteSesgoCrear(BaseModel):
    sesgo_id: int
    incidente_id: int  

#incidente tipo victima
class IncidenteTipoVictimaCrear(BaseModel):
    tipo_victima_id: int
    incidente_id: int

#--------------------------Response Crear-------------------------------
# ===== CONFIG COMÚN =====
class Config(BaseModel):
    class Config:
        from_attributes = True

# ===== REGIÓN =====
class RegionResponse(BaseModel):
    id: int
    nombre: str
    
    class Config:
        from_attributes = True

# ===== ESTADO =====
class EstadoResponse(BaseModel):
    abbr: str
    nombre: str
    id_region: int
    
    class Config:
        from_attributes = True

# ===== GRUPO POBLACIONAL =====
class GrupoPoblacionalResponse(BaseModel):
    codigo: str
    descripcion: str
    min_poblacion: Optional[int]
    max_poblacion: Optional[int]
    tipo_agencia: Optional[str]
    rank: Optional[int]
    
    class Config:
        from_attributes = True

# ===== AGENCIA =====
class AgenciaResponse(BaseModel):
    ori: str
    nombre: str
    tipo: str
    estado_abbr: str
    grupo_poblacional: str
    
    class Config:
        from_attributes = True

# ===== RAZA OFENSOR =====
class RazaOfensorResponse(BaseModel):
    codigo: str
    descripcion: str
    
    class Config:
        from_attributes = True

# ===== ETNICIDAD OFENSOR =====
class EtnicidadOfensorResponse(BaseModel):
    codigo: str
    descripcion: str
    
    class Config:
        from_attributes = True

# ===== OFENSA =====
class OfensaResponse(BaseModel):
    id: int
    nombre: str
    
    class Config:
        from_attributes = True

# ===== UBICACIÓN =====
class UbicacionResponse(BaseModel):
    id: int
    nombre: str
    
    class Config:
        from_attributes = True

# ===== SESGO =====
class SesgoResponse(BaseModel):
    id: int
    descripcion: str
    
    class Config:
        from_attributes = True

# ===== TIPO VÍCTIMA =====
class TipoVictimaResponse(BaseModel):
    id: int
    tipo: str
    
    class Config:
        from_attributes = True

# ===== INCIDENTE =====
class IncidenteResponse(BaseModel):
    id: int
    agencia_ori: str
    fecha_incidente: date
    anio_reporte: int
    raza_del_ofensor: str
    etnicidad_del_ofensor: str
    total_ofensores: int
    numero_ofensores_adultos: Optional[int]
    numero_ofensores_menores_edad: Optional[int]
    numero_victimas_adultas: Optional[int]
    numero_victimas_menores: Optional[int]
    total_victimas_indiv_mas_entidades: int
    numero_victimas_indiv: Optional[int]
    ofensa_multiple: str
    sesgo_multiple: str
    
    class Config:
        from_attributes = True

# ===== INCIDENTE OFENSA =====
class IncidenteOfensaResponse(BaseModel):
    ofensa_id: int
    incidente_id: int
    
    class Config:
        from_attributes = True

# ===== INCIDENTE UBICACIÓN =====
class IncidenteUbicacionResponse(BaseModel):
    ubicacion_id: int
    incidente_id: int
    
    class Config:
        from_attributes = True

# ===== INCIDENTE SESGO =====
class IncidenteSesgoResponse(BaseModel):
    sesgo_id: int
    incidente_id: int
    
    class Config:
        from_attributes = True

# ===== INCIDENTE TIPO VÍCTIMA =====
class IncidenteTipoVictimaResponse(BaseModel):
    tipo_victima_id: int
    incidente_id: int
    
    class Config:
        from_attributes = True
        
#--------------------------------------Consultas avanzadas-------------------------------
class SesgoAnalisisResponse(BaseModel):
    total_victimas: int
    sesgo_desc: str
    
class PorcentajeCambioReportesResponse(BaseModel):
    año: int
    incidentes_año_actual: int
    incidentes_año_anterior: int
    porcentaje_cambio: float
    
class CombinacionesOfensaSesgoResponse(BaseModel):
    ofensa: str
    sesgo: str
    frecuencia: int
    ranking: int
    
class ReportesPorAgenciaPorRegionResponse(BaseModel):
    agencia: str
    estado: str
    region: str
    total_incidentes: int
    ranking_en_region: int
    
class RatioSesgoMenoresAdultosResponse(BaseModel):
    sesgo: str
    total_victimas_menores: int
    total_victimas_adultas: int
    ratio_menores_adultos: float
    porcentaje_menores: float
    
class EstadisticasPorEstadoResponse(BaseModel):
    estado: str
    total_incidentes: int
    promedio_por_anio: float
    anio_pico: int
    poblacion_estimada: int | None
    incidentes_por_100k: float | None
    
#--------------------------Update-------------------------------
#Agencia
class AgenciaUpdate(BaseModel):
    nombre: Optional[str]
    
#Incidente
#En caso de que se revelen nuevos detalles sobre el evento
class IncidenteUpdate(BaseModel):
    raza_del_ofensor: Optional[str]
    etnicidad_del_ofensor: Optional[str]
    total_ofensores: Optional[int]
    numero_ofensores_adultos: Optional[int]
    numero_ofensores_menores_edad: Optional[int]
    numero_victimas_adultas: Optional[int]
    numero_victimas_menores: Optional[int]
    total_victimas_indiv_mas_entidades: Optional[int]
    numero_victimas_indiv: Optional[int]
    ofensa_multiple: Optional[str] = Field(max_length=1)
    sesgo_multiple: Optional[str] = Field(max_length=1)
