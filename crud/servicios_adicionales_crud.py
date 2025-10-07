from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.servicios_adicionales import Servicios_Adicionales
from entities.usuario import Usuario
from datetime import date, datetime

class ServiciosAdicionalesCRUD:
    """
    Módulo CRUD para la entidad Servicios_Adicionales.

    Gestiona los servicios extra que ofrece el hotel, como lavandería,
    transporte, restaurante, entre otros.

    Funciones principales:
        - crear_servicio(db: Session, servicio: Servicios_Adicionales) -> Servicios_Adicionales
        - obtener_servicio(db: Session, id_servicio: UUID) -> Servicios_Adicionales
        - obtener_servicios(db: Session) -> List[Servicios_Adicionales]
        - actualizar_servicio(db: Session, servicio: Servicios_Adicionales, id_usuario_edita: int, fecha_edita: date) -> Servicios_Adicionales
        - eliminar_servicio(db: Session, id_servicio: UUID) -> bool

    Notas:
        - Se valida nombre no vacío, precio mayor a 0 y unicidad del servicio.
    """
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_servicio(db: Session, servicio: Servicios_Adicionales):
        if servicio.nombre_servicio is None:
            raise ValueError("El nombre del servicio es obligatorio")
        if not servicio.nombre_servicio.strip():
            raise ValueError("El nombre del servicio no puede estar vacío")
        existente = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.nombre_servicio == servicio.nombre_servicio).first()
        if existente:
            raise ValueError("El servicio adicional ya existe")
        if servicio.precio is None:
            raise ValueError("El precio del servicio es obligatorio")
        if servicio.precio <= 0:
            raise ValueError("El precio del servicio debe ser mayor a 0")
        if servicio.descripcion is None:
            raise ValueError("La descripción del servicio es obligatoria")
        if not servicio.descripcion.strip():
            raise ValueError("La descripción del servicio no puede estar vacía")
        if servicio.id_usuario_crea is None:
            raise ValueError("El ID del usuario que crea el servicio es obligatorio")
        usuario_existe = db.query(Usuario).filter(Usuario.id_usuario == servicio.id_usuario_crea).first()
        if not usuario_existe:
            raise ValueError("El usuario que crea el servicio no existe")
        servicio.fecha_creacion = datetime.now()
        db.add(servicio)
        db.commit()
        db.refresh(servicio)
        return servicio

    @staticmethod
    def obtener_servicio(db: Session, id_servicio: UUID):
        servicio = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio == id_servicio).first()
        if not servicio:
            raise ValueError("Servicio no encontrado")
        return servicio

    @staticmethod
    def obtener_servicios(db: Session, skip: int = 0, limit: int = 100):
        servicios = db.query(Servicios_Adicionales).offset(skip).limit(limit).all()
        if not servicios:
            raise ValueError("No hay servicios adicionales registrados")
        return servicios

    @staticmethod
    def actualizar_servicio(db, servicio: Servicios_Adicionales, **kwargs):
        existente = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.nombre_servicio == servicio.nombre_servicio).first()
        if existente:
            raise ValueError("El servicio adicional ya existe")
        servicio.id_usuario_edita = kwargs.get("id_usuario_edita", servicio.id_usuario_edita)
        servicio.fecha_edicion = datetime.now()
        for key, value in kwargs.items():
            setattr(servicio, key, value)
        db.commit()
        db.refresh(servicio)
        return servicio

    @staticmethod
    def eliminar_servicio(db: Session, id_servicio: UUID) -> bool:
        servicio = db.query(Servicios_Adicionales).filter(Servicios_Adicionales.id_servicio == id_servicio).first()
        if not servicio:
            raise ValueError("Servicio no encontrado")
        db.delete(servicio)
        db.commit()
        return True
