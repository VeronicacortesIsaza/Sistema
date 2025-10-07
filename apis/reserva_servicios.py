"""
API de Usuarios - Endpoints para gestión de usuarios
"""

from typing import List
from uuid import UUID

from crud.reserva_servicios_crud import ReservaServiciosCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from entities.reserva_servicios import Reserva_Servicios
from schemas import (
    RespuestaAPI,
    ReservaServicioCreate,
    ReservaServicioResponse,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reserva_servicios", tags=["reserva_servicios"])


@router.get("/", response_model=List[ReservaServicioResponse])
async def obtener_reservas_servicios(db: Session = Depends(get_db)):
    """Obtener todos los registros de reservas con sus servicios adicionales."""
    try:
        reservas_servicios_crud = ReservaServiciosCRUD(db)
        registros = reservas_servicios_crud.obtener_reservas_servicios()
        return registros
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener reservas-servicios: {str(e)}",
        )


@router.get("/{id_reserva_servicio}", response_model=ReservaServicioResponse)
async def obtener_reserva_servicio(id_reserva: UUID, db: Session = Depends(get_db)):
    """Obtener un registro específico de reserva-servicio."""
    try:
        reservas_servicios_crud = ReservaServiciosCRUD(db)
        registro = reservas_servicios_crud.obtener_reserva_servicio(id_reserva)
        return registro
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener reserva-servicio: {str(e)}",
        )
        
@router.post("/", response_model=ReservaServicioResponse, status_code=status.HTTP_201_CREATED)
async def crear_reserva_servicio(
    reserva_servicio_data: ReservaServicioCreate, db: Session = Depends(get_db)
):
    """Asociar un servicio adicional a una reserva existente."""
    try:
        reservas_servicios_crud = ReservaServiciosCRUD(db)
        nuevo_registro = Reserva_Servicios(
            id_reserva=reserva_servicio_data.id_reserva,
            id_servicio=reserva_servicio_data.id_servicio,
        )
        registro = reservas_servicios_crud.crear_reserva_servicio(nuevo_registro)
        return registro
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear reserva-servicio: {str(e)}",
        )

@router.delete("/{id_reserva_servicio}", response_model=RespuestaAPI)
async def eliminar_reserva_servicio(id_reserva_servicio: UUID, db: Session = Depends(get_db)):
    """Eliminar un vínculo entre una reserva y un servicio adicional."""
    try:
        reservas_servicios_crud = ReservaServiciosCRUD(db)
        eliminado = reservas_servicios_crud.eliminar_reserva_servicio(id_reserva_servicio)
        if eliminado:
            return RespuestaAPI(
                mensaje="Reserva-servicio eliminada exitosamente",
                exito=True,
            )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar reserva-servicio: {str(e)}",
        )
        
@router.get("/reserva/{id_reserva}", response_model=RespuestaAPI)
async def obtener_servicios_por_reserva(id_reserva: UUID, db: Session = Depends(get_db)):
    """Obtener todos los servicios adicionales asociados a una reserva específica."""
    try:
        reservas_servicios_crud = ReservaServiciosCRUD(db)
        registros = reservas_servicios_crud.obtener_servicios_por_reserva(db, id_reserva)
        return registros
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener servicios por reserva: {str(e)}",
        )
        
@router.get("/servicio/{id_servicio}", response_model=RespuestaAPI)
async def obtener_reservas_por_servicio(id_servicio: UUID, db: Session = Depends(get_db)):
    """Obtener todas las reservas que tienen asociado un servicio adicional específico."""
    try:
        reservas_servicios_crud = ReservaServiciosCRUD(db)
        registros = reservas_servicios_crud.obtener_reservas_por_servicio(db, id_servicio)
        return registros
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener reservas por servicio: {str(e)}",
        )