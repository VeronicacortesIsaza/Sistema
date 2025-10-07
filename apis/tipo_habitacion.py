"""
API de Usuarios - Endpoints para gestión de usuarios
"""

from typing import List
from uuid import UUID

from crud.tipo_habitacion_crud import TipoHabitacionCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    RespuestaAPI,
    TipoHabitacionResponse,
    TipoHabitacionUpdate,
    TipoHabitacionCreate
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/TipoDeHabitacion", tags=["TipoDeHabitacion"])


@router.get("/", response_model=List[TipoHabitacionResponse])
async def obtener_tipos_habitacion(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los tipos de habitacion con paginación."""
    try:
        tipo_habitacion_crud = TipoHabitacionCRUD(db)
        tipos_habitacion = tipo_habitacion_crud.obtener_tipos_habitacion(db)
        return tipos_habitacion
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los tipos de habitacion: {str(e)}",
        )


@router.get("/{id_tipo}", response_model=TipoHabitacionResponse)
async def obtener_tipo_habitacion(id_tipo: UUID, db: Session = Depends(get_db)):
    """Obtener los tipos de habitacion por ID."""
    try:
        tipo_habitacion_crud = TipoHabitacionCRUD(db)
        tipo_habitacion = tipo_habitacion_crud.obtener_tipo_habitacion(db, id_tipo)
        return tipo_habitacion
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el tipo de habitacion: {str(e)}",
        )

@router.post("/", response_model=TipoHabitacionResponse, status_code=status.HTTP_201_CREATED)
async def crear_tipo_habitacion(tipo: TipoHabitacionCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de habitación."""
    try:
        tipo_habitacion_crud = TipoHabitacionCRUD(db)
        tipo_habitacion= tipo_habitacion_crud.crear_tipo_habitacion(db, tipo)
        return tipo_habitacion
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear un tipo de habitación: {str(e)}",
        )


@router.put("/{id_tipo}", response_model=TipoHabitacionResponse)
async def actualizar_tipo_habitacion(
    id_tipo: UUID, tipo_data: TipoHabitacionUpdate, db: Session = Depends(get_db)
):
    """Actualizar un tipo de habitación existente."""
    try:
        tipo_habitacion_crud = TipoHabitacionCRUD(db)

        tipo_existente = tipo_habitacion_crud.obtener_tipo_habitacion(db, id_tipo)
        if not tipo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Tipo de habitación no encontrado"
            )

        campos_actualizacion = {
            k: v for k, v in tipo_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return tipo_existente

        usuario_actualizado = tipo_habitacion_crud.actualizar_tipo_habitacion(
            id_tipo, **campos_actualizacion
        )
        return usuario_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}",
        )


@router.delete("/{id_tipo}", response_model=RespuestaAPI)
async def eliminar_tipo_habitacion(id_tipo: UUID, db: Session = Depends(get_db)):
    """Eliminar un usuario."""
    try:
        tipo_habitacion_crud = TipoHabitacionCRUD(db)

        # Verificar que el usuario existe
        tipo_existente = tipo_habitacion_crud.obtener_tipo_habitacion(db, id_tipo)
        if not tipo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        eliminado = tipo_habitacion_crud.eliminar_tipo_habitacion(db, id_tipo)
        if eliminado:
            return RespuestaAPI(mensaje="Usuario eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar usuario",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar usuario: {str(e)}",
        )