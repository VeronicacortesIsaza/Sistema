from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.reserva_servicios import Reserva_Servicios
from entities.reserva import Reserva
from entities.servicios_adicionales import Servicios_Adicionales

class ReservaServiciosCRUD:
    """
    Módulo CRUD para la entidad Reserva_Servicios.

    Administra la relación entre las reservas y los servicios adicionales contratados.

    Funciones principales:
        - crear_reserva_servicio(db: Session, reserva_servicio: Reserva_Servicios) -> Reserva_Servicios
        - obtener_reserva_servicio(db: Session, id_reserva_servicio: UUID) -> Reserva_Servicios
        - obtener_reservas_servicios(db: Session, skip: int = 0, limit: int = 100) -> List[Reserva_Servicios]
        - eliminar_reserva_servicio(db: Session, id_reserva_servicio: UUID) -> bool
    """
    def __init__(self, db):
        self.db = db
    @staticmethod
    def crear_reserva_servicio(db: Session, reserva_servicio: Reserva_Servicios):
        if not reserva_servicio.id_reserva: 
            raise ValueError("El registro debe estar asociado a una reserva")
        if not reserva_servicio.id_servicio:
            raise ValueError("El registro debe estar asociado a un servicio adicional")

        reserva = db.query(Reserva.id_reserva).filter(Reserva.id_reserva == reserva_servicio.id_reserva).first()
        if not reserva:
            raise ValueError("La reserva asociada no existe")
        servicio = db.query(Servicios_Adicionales.id_servicio).filter(Servicios_Adicionales.id_servicio == reserva_servicio.id_servicio).first()
        if not servicio:
            raise ValueError("El servicio asociado no existe")

        db.add(reserva_servicio)
        db.commit()
        db.refresh(reserva_servicio)
        return reserva_servicio

    @staticmethod
    def obtener_reserva_servicio(db: Session, id_reserva_servicio: UUID):
        rs = db.query(Reserva_Servicios).filter(Reserva_Servicios.id_reserva_servicio == id_reserva_servicio).first()
        if not rs:
            raise ValueError("Reserva-Servicio no encontrado")
        return rs

    @staticmethod
    def obtener_reservas_servicios(db: Session, skip: int = 0, limit: int = 100):
        reservas_servicios = db.query(Reserva_Servicios).offset(skip).limit(limit).all()
        if not reservas_servicios:
            raise ValueError("No hay registros de reservas con servicios adicionales")
        return reservas_servicios
    
    @staticmethod
    def obtener_servicios_por_reserva(db: Session, id_reserva: UUID):
        servicios = db.query(Reserva_Servicios).filter(Reserva_Servicios.id_reserva == id_reserva).all()
        if not servicios:
            raise ValueError("No hay servicios adicionales asociados a esta reserva")
        return servicios
    
    @staticmethod
    def actualizar_reserva_servicio(db: Session, id_reserva: UUID, id_servicio: UUID, **kwargs):
        rs = db.query(Reserva_Servicios).filter(
            Reserva_Servicios.id_reserva == id_reserva,
            Reserva_Servicios.id_servicio == id_servicio
        ).first()
        if not rs:
            raise ValueError("Reserva-Servicio no encontrado")

        for key, value in kwargs.items():
            if hasattr(rs, key):
                setattr(rs, key, value)

        db.commit()
        db.refresh(rs)
        return rs

    @staticmethod
    def obtener_reservas_por_servicio(db: Session, id_servicio: UUID):
        reservas = db.query(Reserva_Servicios).filter(Reserva_Servicios.id_servicio == id_servicio).all()
        if not reservas:
            raise ValueError("No hay reservas asociadas a este servicio adicional")
        return reservas

    @staticmethod
    def eliminar_reserva_servicio(db: Session, id_reserva_servicio: UUID) -> bool:
        rs = db.query(Reserva_Servicios).filter(Reserva_Servicios.id_reserva_servicio == id_reserva_servicio).first()
        if not rs:
            raise ValueError("Reserva-Servicio no encontrado")
        db.delete(rs)
        db.commit()
        return True
