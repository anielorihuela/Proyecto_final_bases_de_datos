from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from modelosPydantic import *
from modelosBase import *
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from conexion import DB_CONNECTION_STRING


app = FastAPI()

if not DB_CONNECTION_STRING:
    raise ValueError("La variable de entorno DB_CONNECTION_STRING no está definida")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Create 
@app.post("/regiones/", response_model=RegionResponse)
def crear_region(region: RegionCrear, db: Session = Depends(get_db)):
    nueva_region = Region(nombre=region.nombre)
    db.add(nueva_region)
    db.commit()
    db.refresh(nueva_region)
    return nueva_region

@app.post("/estados/", response_model=EstadoResponse)
def crear_estado(estado: EstadoCrear, db: Session = Depends(get_db)):
    nueva_estado = Estado(abbr=estado.abbr, nombre=estado.nombre, id_region=estado.id_region)
    db.add(nueva_estado)
    db.commit()
    db.refresh(nueva_estado)
    return nueva_estado

@app.post("/grupos_poblacionales/", response_model=GrupoPoblacionalResponse)
def crear_grupo_poblacional(grupo: GrupoPoblacionalCrear, db: Session = Depends(get_db)):
    nuevo_grupo = GrupoPooblacional(
        codigo=grupo.codigo,
        descripcion=grupo.descripcion,
        min_poblacion=grupo.min_poblacion,
        max_poblacion=grupo.max_poblacion,
        rank=grupo.rank
    )
    db.add(nuevo_grupo)
    db.commit()
    db.refresh(nuevo_grupo)
    return nuevo_grupo

@app.post("/agencias/", response_model=AgenciaResponse)
def crear_agencia(agencia: AgenciaCrear, db: Session = Depends(get_db)):
    nueva_agencia = Agencia(
        ori=agencia.ori,
        nombre=agencia.nombre,
        tipo=agencia.tipo,
        estado_abbr=agencia.estado_abbr,
        grupo_poblacional=agencia.grupo_poblacional
    )
    db.add(nueva_agencia)
    db.commit()
    db.refresh(nueva_agencia)
    return nueva_agencia


@app.post("/ofensas/", response_model=OfensaResponse)
def crear_ofensa(ofensa: OfensaCrear, db: Session = Depends(get_db)):
    nueva_ofensa = Ofensa(nombre=ofensa.nombre)
    db.add(nueva_ofensa)
    db.commit()
    db.refresh(nueva_ofensa)
    return nueva_ofensa

@app.post("/ubicaciones/", response_model=UbicacionResponse)
def crear_ubicacion(ubicacion: UbicacionCrear, db: Session = Depends(get_db)):
    nueva_ubicacion = Ubicacion(nombre=ubicacion.nombre)
    db.add(nueva_ubicacion)
    db.commit()
    db.refresh(nueva_ubicacion)
    return nueva_ubicacion

@app.post("/sesgos/", response_model=SesgoResponse)
def crear_sesgo(sesgo: SesgoCrear, db: Session = Depends(get_db)):
    nuevo_sesgo = Sesgo(descripcion=sesgo.descripcion)
    db.add(nuevo_sesgo)
    db.commit()
    db.refresh(nuevo_sesgo)
    return nuevo_sesgo

@app.post("/tipos_victima/", response_model=TipoVictimaResponse)
def crear_tipo_victima(tipo_victima: TipoVictimaCrear, db: Session = Depends(get_db)):
    nuevo_tipo_victima = TipoVictima(tipo=tipo_victima.tipo)
    db.add(nuevo_tipo_victima)
    db.commit()
    db.refresh(nuevo_tipo_victima)
    return nuevo_tipo_victima

@app.post("/incidentes/", response_model=IncidenteResponse)
def crear_incidente(incidente: IncidenteCrear, db: Session = Depends(get_db)):
    nuevo_incidente = Incidente(
        agencia_ori=incidente.agencia_ori,
        fecha_incidente=incidente.fecha_incidente,
        anio_reporte=incidente.anio_reporte,
        raza_del_ofensor=incidente.raza_del_ofensor,
        etnicidad_del_ofensor=incidente.etnicidad_del_ofensor,
        total_ofensores=incidente.total_ofensores,
        numero_ofensores_adultos=incidente.numero_ofensores_adultos,
        numero_ofensores_menores_edad=incidente.numero_ofensores_menores_edad,
        numero_victimas_adultas=incidente.numero_victimas_adultas,
        numero_victimas_menores=incidente.numero_victimas_menores,
        total_victimas_indiv_mas_entidades=incidente.total_victimas_indiv_mas_entidades,
        numero_victimas_indiv=incidente.numero_victimas_indiv,
        ofensa_multiple=incidente.ofensa_multiple,
        sesgo_multiple=incidente.sesgo_multiple
    )
    db.add(nuevo_incidente)
    db.commit()
    db.refresh(nuevo_incidente)
    return nuevo_incidente

@app.post("/incidentes_ofensas/", response_model=IncidenteOfensaResponse)
def crear_incidente_ofensa(incidente_ofensa: IncidenteOfensaCrear, db: Session = Depends(get_db)):
    nuevo_incidente_ofensa = IncidenteOfensa(
        ofensa_id=incidente_ofensa.ofensa_id,
        incidente_id=incidente_ofensa.incidente_id
    )
    db.add(nuevo_incidente_ofensa)
    db.commit()
    db.refresh(nuevo_incidente_ofensa)
    return nuevo_incidente_ofensa

@app.post("/incidentes_ubicaciones/", response_model=IncidenteUbicacionResponse)
def crear_incidente_ubicacion(incidente_ubicacion: IncidenteUbicacionCrear, db: Session = Depends(get_db)):
    nuevo_incidente_ubicacion = IncidenteUbicacion(
        ubicacion_id=incidente_ubicacion.ubicacion_id,
        incidente_id=incidente_ubicacion.incidente_id
    )
    db.add(nuevo_incidente_ubicacion)
    db.commit()
    db.refresh(nuevo_incidente_ubicacion)
    return nuevo_incidente_ubicacion

@app.post("/incidentes_sesgos/", response_model=IncidenteSesgoResponse)
def crear_incidente_sesgo(incidente_sesgo: IncidenteSesgoCrear, db: Session = Depends(get_db)):
    nuevo_incidente_sesgo = IncidenteSesgo(
        sesgo_id=incidente_sesgo.sesgo_id,
        incidente_id=incidente_sesgo.incidente_id
    )
    db.add(nuevo_incidente_sesgo)
    db.commit()
    db.refresh(nuevo_incidente_sesgo)
    return nuevo_incidente_sesgo

# Read 
@app.get("/consultas-avanzadas/ranking-sesgos/{ranking}", response_model=SesgoAnalisisResponse)
def ranking_sesgos(ranking: int, db: Session = Depends(get_db)):
    query = text("""with ranks as(
	select sum(total_victimas_indiv_mas_entidades) as total_victimas, 
	sesgo.descripcion as sesgo_desc,
	ROW_NUMBER() OVER (ORDER BY sum(total_victimas_indiv_mas_entidades) DESC) as ranking
	from sesgo 
	inner join incidente_sesgo on incidente_sesgo.sesgo_id = sesgo.id
	inner join incidente on incidente_sesgo.incidente_id = incidente.id
	group by sesgo.descripcion
    )
    select total_victimas, sesgo_desc, ranking
    from ranks
    where ranking = :ranking_param""")
    result = db.execute(query, {"ranking_param": ranking}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Ranking no encontrado")
    return SesgoAnalisisResponse(total_victimas=result[0], sesgo_desc=result[1])

@app.get("/consultas-avanzadas/porcentaje-cambio-reportes/{anio}", response_model=list[PorcentajeCambioReportesResponse])
def porcentaje_cambio_reportes(anio: int, db: Session = Depends(get_db)):
    query = text("""select
    incidente.anio_reporte as año,
    count(*) as incidentes_año,
    lag(count(*)) over (order by anio_reporte) as incidentes_año_anterior,
    ((count(*) - lag(count(*)) over (order by anio_reporte))::decimal
     / lag(count(*)) over (order by anio_reporte) * 100)
    as porcentaje_cambio
    from incidente
    where incidente.anio_reporte >= :anio_param
    group by anio_reporte
    order by anio_reporte""")
    results = db.execute(query, {"anio_param": anio}).fetchall()
    response = []
    for row in results:
        response.append(PorcentajeCambioReportesResponse(
            año=row[0],
            incidentes_año_actual=row[1],
            incidentes_año_anterior=row[2] if row[2] is not None else 0,
            porcentaje_cambio=row[3] if row[3] is not None else 0.0
        ))
    return response

@app.get("/consultas-avanzadas/combinaciones-ofensa-sesgo/{limite}", response_model=list[CombinacionesOfensaSesgoResponse])
def combinaciones_ofensa_sesgo(limite: int, db: Session = Depends(get_db)):
    query = text("""with combinaciones as (
    select 
        ofensa.nombre as ofensa,
        sesgo.descripcion as sesgo,
        count(*) as frecuencia
    from incidente_ofensa
    inner join ofensa on incidente_ofensa.ofensa_id = ofensa.id
    inner join incidente on incidente_ofensa.incidente_id = incidente.id
    inner join incidente_sesgo on incidente.id = incidente_sesgo.incidente_id
    inner join sesgo on incidente_sesgo.sesgo_id = sesgo.id
    group by ofensa.nombre, sesgo.descripcion
    )
    select 
        ofensa,
        sesgo,
        frecuencia,
        row_number() over (order by frecuencia desc) as ranking
    from combinaciones
    order by frecuencia desc
    limit :limite_param;""")
    result = db.execute(query, {"limite_param": limite}).fetchall()
    response = []
    for row in result:
        response.append(CombinacionesOfensaSesgoResponse(
            ofensa=row[0],
            sesgo=row[1],
            frecuencia=row[2],
            ranking=row[3]
        ))
    return response

@app.get("/consultas-avanzadas/reportes-por-agencia-region/{nombre_region}", response_model=list[ReportesPorAgenciaPorRegionResponse])
def reportes_por_agencia_region(nombre_region: str, db: Session = Depends(get_db)):
    query = text("""with agencia_reportes as (
    select 
        agencia.nombre as agencia,
        estado.nombre as estado,
        region.nombre as region,
        count(*) as total_incidentes
    from incidente
    inner join agencia on incidente.agencia_ori = agencia.ori
    inner join estado on agencia.estado_abbr = estado.abbr
    inner join region on estado.id_region = region.id
    where region.nombre = :nombre_region_param
    group by agencia.nombre, estado.nombre, region.nombre
    )
    select 
        agencia,
        estado,
        region,
        total_incidentes,
        rank() over (partition by region order by total_incidentes desc) as ranking_en_region
    from agencia_reportes
    order by region, ranking_en_region;""")
    results = db.execute(query, {"nombre_region_param": nombre_region}).fetchall()
    response = []
    for row in results:
        response.append(ReportesPorAgenciaPorRegionResponse(
            agencia=row[0],
            estado=row[1],
            region=row[2],
            total_incidentes=row[3],
            ranking_en_region=row[4]
        ))
    return response

@app.get("/consultas-avanzadas/ratio-sesgo-menores-adultos/{sesgo}", response_model=RatioSesgoMenoresAdultosResponse)
def ratio_sesgo_menores_adultos(sesgo: str, db: Session = Depends(get_db)):
    query = text("""select
    sesgo.descripcion as sesgo,
    sum(incidente.numero_victimas_menores) as total_victimas_menores,
    sum(incidente.numero_victimas_adultas) as total_victimas_adultas,
    sum(incidente.numero_victimas_menores)::decimal /
    nullif(sum(incidente.numero_victimas_adultas), 0)
    as ratio_menores_adultos,
    (sum(incidente.numero_victimas_menores)::decimal / 
    nullif(sum(incidente.numero_victimas_menores) + sum(incidente.numero_victimas_adultas), 0) * 100)
    as porcentaje_menores
    from incidente
    inner join incidente_sesgo on incidente.id = incidente_sesgo.incidente_id
    inner join sesgo on incidente_sesgo.sesgo_id = sesgo.id
    where sesgo.descripcion = :sesgo_param
    group by sesgo.descripcion;""")
    result = db.execute(query, {"sesgo_param": sesgo}).fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Sesgo no encontrado")
    return RatioSesgoMenoresAdultosResponse(
        sesgo=result[0],
        total_victimas_menores=result[1],
        total_victimas_adultas=result[2],
        ratio_menores_adultos=result[3],
        porcentaje_menores=result[4]
    )

@app.get("/consultas-avanzadas/estadisticas-por-estado/", response_model=list[EstadisticasPorEstadoResponse])
def estadisticas_por_estado(db: Session = Depends(get_db)):
    query = text("""with poblacion_estado as (
    select
        estado.nombre as estado,
        sum(
            coalesce(
                (gp.min_poblacion + gp.max_poblacion) / 2.0,
                gp.max_poblacion,
                gp.min_poblacion
            )
        ) as poblacion_estimada
        from agencia
        join estado on agencia.estado_abbr = estado.abbr
        join grupo_poblacional gp on agencia.grupo_poblacional = gp.codigo
        where gp.min_poblacion is not null or gp.max_poblacion is not null
        group by estado.nombre
        ),
        incidentes_por_anio as (
            select
                estado.nombre as estado,
                incidente.anio_reporte as anio,
                count(*) as incidentes_anio
            from incidente
            inner join agencia on incidente.agencia_ori = agencia.ori
            inner join estado on agencia.estado_abbr = estado.abbr
            group by estado.nombre, incidente.anio_reporte
        ),
        estado_stats as (
            select
                estado,
                sum(incidentes_anio) as total_incidentes,
                cast(sum(incidentes_anio) as decimal) / count(distinct anio)
                as promedio_por_anio
            from incidentes_por_anio
            group by estado
        ),
        anio_pico as (
            select
                estado,
                anio as anio_pico,
                row_number() over (
                    partition by estado
                    order by incidentes_anio desc
                ) as rn
            from incidentes_por_anio
        )
        select
            estado_stats.estado,
            estado_stats.total_incidentes,
            estado_stats.promedio_por_anio,
            anio_pico.anio_pico,
            round(pe.poblacion_estimada) as poblacion_estimada,
            round(
                (estado_stats.total_incidentes::decimal / nullif(pe.poblacion_estimada, 0)) * 100000,
                2
            ) as incidentes_por_100k
            from estado_stats
            inner join anio_pico
                on estado_stats.estado = anio_pico.estado
                and anio_pico.rn = 1
            left join poblacion_estado pe on pe.estado = estado_stats.estado
            order by incidentes_por_100k desc
            limit 10;""")
    results = db.execute(query).fetchall()
    response = []
    for row in results:
        response.append(EstadisticasPorEstadoResponse(
            estado=row[0],
            total_incidentes=row[1],
            promedio_por_anio=float(row[2]),
            anio_pico=row[3],
            poblacion_estimada=row[4],
            incidentes_por_100k=float(row[5]) if row[5] is not None else None
        ))
    return response

# Update 
@app.put("/agencias/{ori}", response_model=AgenciaResponse)
def actualizar_agencia(ori: str, agencia: AgenciaUpdate, db: Session = Depends(get_db)):
    query = text("""update agencia
                 set nombre = :nombre_param
                 where ori = :ori_param
    """)
    db.execute(query, {"nombre_param": agencia.nombre, "ori_param": ori})
    db.commit()
    return db.query(Agencia).filter(Agencia.ori == ori).first()

@app.put("/incidentes/{incidente_id}", response_model=IncidenteResponse)
def actualizar_incidente(incidente_id: int, incidente: IncidenteUpdate, db: Session = Depends(get_db)):
    query = text("""update incidente
                    set raza_del_ofensor = :raza_param,
                     etnicidad_del_ofensor = :etnicidad_param,
                     total_ofensores = :total_ofensores_param,
                     numero_ofensores_adultos = :numero_ofensores_adultos_param,
                     numero_ofensores_menores_edad = :numero_ofensores_menores_edad_param,
                     numero_victimas_adultas = :numero_victimas_adultas_param,
                     numero_victimas_menores = :numero_victimas_menores_param,
                     total_victimas_indiv_mas_entidades = :total_victimas_indiv_mas_entidades_param,
                     numero_victimas_indiv = :numero_victimas_indiv_param,
                     ofensa_multiple = :ofensa_multiple_param,
                     sesgo_multiple = :sesgo_multiple_param
                     where id = :incidente_id_param
    """)
    db.execute(query, {
        "raza_param": incidente.raza_del_ofensor,
        "etnicidad_param": incidente.etnicidad_del_ofensor,
        "total_ofensores_param": incidente.total_ofensores,
        "numero_ofensores_adultos_param": incidente.numero_ofensores_adultos,
        "numero_ofensores_menores_edad_param": incidente.numero_ofensores_menores_edad,
        "numero_victimas_adultas_param": incidente.numero_victimas_adultas,
        "numero_victimas_menores_param": incidente.numero_victimas_menores,
        "total_victimas_indiv_mas_entidades_param": incidente.total_victimas_indiv_mas_entidades,
        "numero_victimas_indiv_param": incidente.numero_victimas_indiv,
        "ofensa_multiple_param": incidente.ofensa_multiple,
        "sesgo_multiple_param": incidente.sesgo_multiple,
        "incidente_id_param": incidente_id
    })
    db.commit()
    return db.query(Incidente).filter(Incidente.id == incidente_id).first()

# Delete 
@app.delete("/agencias/{ori}")
def eliminar_agencia(ori: str, db: Session = Depends(get_db)):
    query = text("""delete from agencia where ori = :ori_param""")
    db.execute(query, {"ori_param": ori})
    db.commit()
    return {"Respuesta": f"Agencia con ORI {ori} eliminada"}

@app.delete("/incidentes/{incidente_id}")
def eliminar_incidente(incidente_id: int, db: Session = Depends(get_db)):
    query = text("""delete from incidente where id = :incidente_id_param""")
    db.execute(query, {"incidente_id_param": incidente_id})
    db.commit()
    return {"Respuesta": f"Incidente con ID {incidente_id} eliminado"}