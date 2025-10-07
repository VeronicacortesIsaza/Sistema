from datetime import datetime, timedelta
from http.client import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID
from entities.habitacion import Habitacion
from entities.reserva import Reserva
from entities.reserva_servicios import Reserva_Servicios
from entities.usuario import Usuario

class ReservaCRUD:
    """
    Módulo CRUD para la entidad Reserva.

    Gestiona las reservas realizadas por los clientes, validando fechas
    y asociando correctamente a cliente y habitación.

    Funciones principales:
        - crear_reserva(db: Session, reserva: Reserva) -> Reserva
        - obtener_reserva(db: Session, id_reserva: UUID) -> Reserva
        - obtener_reservas(db: Session) -> List[Reserva]
        - actualizar_reserva(db: Session, id_reserva: UUID, **kwargs) -> Reserva
        - eliminar_reserva(db: Session, id_reserva: UUID) -> bool
        - obtener_reservas_activas(db: Session) -> List[Reserva]
        - actualizar_costo_total(db: Session, id_reserva: UUID, monto_extra: float) -> Reserva

    Notas:
        - Se valida que la fecha de entrada sea menor a la de salida.
        - Al cancelar una reserva se recomienda actualizar el estado de la habitación.
    """
    def __init__(self, db):
        self.db = db
        
    @staticmethod
    def crear_reserva(db: Session, reserva: Reserva):
        if not reserva.fecha_entrada:
            raise ValueError("La fecha de entrada es obligatoria")
        if reserva.fecha_entrada < datetime.now().date():
            raise ValueError("La fecha de entrada debe ser posterior a la fecha actual")
        if not reserva.numero_de_personas:
            raise ValueError("El número de personas es obligatorio")
        if reserva.numero_de_personas <= 0:
            raise ValueError("El número de personas debe ser mayor a 0")
        if not reserva.noches:
            raise ValueError("El número de noches es obligatorio")
        if reserva.noches <= 0:
            raise ValueError("El número de noches debe ser mayor a 0")
        if not reserva.estado_reserva:
            raise ValueError("El estado de la reserva es obligatorio")
        estados = ["Activa", "Cancelada"]
        if reserva.estado_reserva not in estados:
            raise ValueError(f"Estado de reserva inválido. Debe ser uno de: {', '.join(estados)}")
        if not reserva.id_usuario:
            raise ValueError("El ID del usuario asociado a la reserva es obligatorio")
        usuario_existe = db.query(Usuario).filter(Usuario.id_usuario == reserva.id_usuario).first()
        if not usuario_existe:
            raise ValueError("El usuario asociado no existe")
        if not reserva.id_habitacion:
            raise ValueError("El ID de la habitación es obligatorio")
        habitacion = db.query(Habitacion).filter(Habitacion.id_habitacion == reserva.id_habitacion).first()
        if not habitacion:
            raise ValueError("La habitación asociada no existe")
        if not habitacion.disponible:
            raise ValueError("La habitación no está disponible")
        reserva.estado_reserva = "Activa"
        reserva.fecha_creacion = datetime.now()
        reserva.costo_total = habitacion.precio * reserva.noches
        reserva.fecha_salida = reserva.fecha_entrada + timedelta(days=reserva.noches)
        habitacion.disponible = False
        reserva.fecha_creacion = datetime.now()
        reserva.id_usuario_crea = usuario_existe.id_usuario
        
        db.add(reserva)
        db.commit()
        db.refresh(reserva)
        return reserva

    @staticmethod
    def obtener_reserva(db: Session, id_reserva: UUID):
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            raise ValueError("Reserva no encontrada")
        return reserva

    @staticmethod
    def obtener_reservas(db: Session, skip: int = 0, limit: int = 100):
        reservas = db.query(Reserva).offset(skip).limit(limit).all()
        if not reservas:
            raise ValueError("No hay reservas registradas")
        return reservas

    @staticmethod
    def actualizar_reserva(db: Session, id_reserva: UUID, **kwargs):
        estados = ["Activa", "Cancelada"]
        if kwargs.get("estado_reserva") not in estados:
            raise ValueError(f"Estado de reserva inválido. Debe ser uno de: {', '.join(estados)}")
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            raise ValueError("Reserva no encontrada")

        for key, value in kwargs.items():
            if hasattr(reserva, key):
                setattr(reserva, key, value)

        if reserva.fecha_entrada and reserva.fecha_salida and reserva.fecha_entrada >= reserva.fecha_salida:
            raise ValueError("La fecha de entrada debe ser anterior a la fecha de salida")
        reserva.fecha_edicion = datetime.now()
        db.commit()
        db.refresh(reserva)
        return reserva

    @staticmethod
    def eliminar_reserva(db: Session, id_reserva: UUID):
        reserva = db.query(Reserva).filter(Reserva.id_reserva == id_reserva).first()
        if not reserva:
            raise ValueError("La reserva no existe.")

        db.query(Reserva_Servicios).filter(Reserva_Servicios.id_reserva == id_reserva).delete()

        db.delete(reserva)
        db.commit()
    
    @staticmethod
    def actualizar_costo_total(db: Session, id_reserva, monto_extra: float):
        reserva = db.query(Reserva).filter_by(id_reserva=id_reserva).first()
        if not reserva:
            raise ValueError("Reserva no encontrada")

        reserva.costo_total += monto_extra
        db.add(reserva)
        return reserva
    
    @staticmethod
    def obtener_reservas_por_usuario(db: Session, id_usuario: UUID):
        reservas = db.query(Reserva).filter(Reserva.id_usuario == id_usuario).all()
        if not reservas:
            raise ValueError("No se encontraron reservas para el usuario especificado")
        return reservas
    
    @staticmethod
    def obtener_reservas_activas(db: Session):
        activas = db.query(Reserva).filter(Reserva.estado_reserva == "Activa").all()
        if not activas:
            raise ValueError("No hay reservas activas en este momento")
        return activas