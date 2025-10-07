"""
API de Usuarios - Endpoints para gestión de usuarios
"""

from typing import List
from uuid import UUID

from crud.reserva_crud import ReservaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from entities.habitacion import Habitacion
from entities.reserva import Reserva
from schemas import (
    RespuestaAPI,
    ReservaCreate,
    ReservaResponse,
    ReservaUpdate
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reservas", tags=["reservas"])

@router.get("/", response_model=List[ReservaResponse])
async def obtener_reservas(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
):
    try:
        reservas_crud = ReservaCRUD(db)
        reservas = reservas_crud.obtener_reservas(db, skip=skip, limit=limit)
        return reservas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener reservas: {str(e)}",
        )

@router.get("/{id_reserva}", response_model=ReservaResponse)
async def obtener_reserva(id_reserva: UUID, db: Session = Depends(get_db)):
    """Obtener una reserva por ID."""
    try:
        reservas_crud = ReservaCRUD(db)
        reservas = reservas_crud.obtener_reserva(db, id_reserva)
        if not reservas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada"
            )
        return reservas
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener reserva: {str(e)}",
        )

@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva_data: ReservaCreate, db: Session = Depends(get_db)):
    """Crear una nueva reserva."""
    try:
        
        nueva_reserva = Reserva(
            fecha_entrada=reserva_data.fecha_entrada,
            estado_reserva=reserva_data.estado_reserva,
            numero_de_personas=reserva_data.numero_de_personas,
            noches=reserva_data.noches,
            id_usuario=reserva_data.id_usuario,
            id_habitacion=reserva_data.id_habitacion
        )

        reservas_crud = ReservaCRUD(db)
        reserva = reservas_crud.crear_reserva(db, nueva_reserva)
        return reserva
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear reserva: {str(e)}",
        )
@router.put("/{id_reserva}", response_model=ReservaResponse)
async def actualizar_reserva(
    id_reserva: UUID, reserva_data: ReservaUpdate, db: Session = Depends(get_db)
):
    """Actualizar una reserva existente."""
    try:
        reservas_crud = ReservaCRUD(db)
        reserva_existente = reservas_crud.obtener_reserva(db, id_reserva)
        if not reserva_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada"
            )
        campos_actualizacion = {
            k: v for k, v in reserva_data.dict().items() if v is not None
        }
        if not campos_actualizacion:
            return reserva_existente
        reserva_actualizada = reservas_crud.actualizar_reserva(
            db, id_reserva, **campos_actualizacion
        )
        return reserva_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar reserva: {str(e)}",
        )

@router.delete("/{id_reserva}", response_model=RespuestaAPI)
async def eliminar_reserva(id_reserva: UUID, db: Session = Depends(get_db)):
    """Eliminar una reserva."""
    try:
        reservas_crud = ReservaCRUD(db)
        reserva_existente = reservas_crud.obtener_reserva(db, id_reserva)
        if not reserva_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada"
            )

        eliminado = reservas_crud.eliminar_reserva(id_reserva)
        if eliminado:
            return RespuestaAPI(mensaje="Reserva eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar reserva",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar reserva: {str(e)}",
        )

@router.patch("/{id_reserva}/estado", response_model=ReservaResponse)
async def actualizar_estado_reserva(
    id_reserva: UUID,
    estado_reserva: str,
    db: Session = Depends(get_db),
):
    """
    Cambiar el estado de una reserva (por ejemplo: 'Activa', 'Cancelada').
    """
    try:
        reserva_crud = ReservaCRUD(db)
        reserva_existente = reserva_crud.obtener_reserva(db, id_reserva)
        if not reserva_existente:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")

        reserva_actualizada = reserva_crud.actualizar_reserva(
            db, id_reserva, estado_reserva=estado_reserva
        )
        return reserva_actualizada
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al actualizar estado de reserva: {str(e)}",
        )
        
@router.get("/activas", response_model=List[ReservaResponse])
async def obtener_reservas_activas(db: Session = Depends(get_db)):
    """Obtener todas las reservas activas."""
    try:
        reserva_crud = ReservaCRUD(db)
        reservas_activas = reserva_crud.obtener_reservas_activas(db)
        return reservas_activas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener reservas activas: {str(e)}",
        )