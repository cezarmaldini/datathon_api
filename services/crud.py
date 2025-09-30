from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status
import logging
from models.schema_vagas import VagaCreate, VagaUpdate, VagaInDB

logger = logging.getLogger(__name__)


class VagaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def criar_vaga(self, vaga: VagaCreate) -> VagaInDB:
        """Cria uma nova vaga no banco de dados"""
        try:
            vaga_dict = vaga.model_dump()
            
            query = text("""
                INSERT INTO vagas (
                    data_requisicao, titulo_vaga, tipo_contratacao, vaga_pcd,
                    cidade, estado, pais, nivel_profissional, nivel_academico,
                    areas_atuacao, principais_atividades, competencias_tecnicas,
                    habilidades_comportamentais, modalidade, ativa
                ) VALUES (
                    :data_requisicao, :titulo_vaga, :tipo_contratacao, :vaga_pcd,
                    :cidade, :estado, :pais, :nivel_profissional, :nivel_academico,
                    :areas_atuacao, :principais_atividades, :competencias_tecnicas,
                    :habilidades_comportamentais, :modalidade, :ativa
                )
                RETURNING *
            """)
            
            result = self.db.execute(query, vaga_dict)
            self.db.commit()
            
            vaga_criada = result.fetchone()
            return VagaInDB(**dict(vaga_criada._mapping))
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao criar vaga: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao criar vaga"
            )

    def obter_vaga(self, vaga_id: UUID) -> Optional[VagaInDB]:
        """Obtém uma vaga específica pelo ID"""
        try:
            query = text("SELECT * FROM vagas WHERE id = :vaga_id")
            result = self.db.execute(query, {"vaga_id": str(vaga_id)})
            vaga = result.fetchone()
            
            if not vaga:
                return None
                
            return VagaInDB(**dict(vaga._mapping))
            
        except Exception as e:
            logger.error(f"Erro ao obter vaga {vaga_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao buscar vaga"
            )

    def listar_vagas(self, skip: int = 0, limit: int = 100) -> List[VagaInDB]:
        """Lista todas as vagas com paginação"""
        try:
            query = text("""
                SELECT * FROM vagas 
                ORDER BY criada_em DESC 
                LIMIT :limit OFFSET :skip
            """)
            
            count_query = text("SELECT COUNT(*) FROM vagas")
            
            # Executar query de contagem
            count_result = self.db.execute(count_query)
            total = count_result.scalar()
            
            # Executar query principal
            result = self.db.execute(query, {"limit": limit, "skip": skip})
            vagas = result.fetchall()
            
            return [VagaInDB(**dict(vaga._mapping)) for vaga in vagas], total
            
        except Exception as e:
            logger.error(f"Erro ao listar vagas: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao listar vagas"
            )

    def atualizar_vaga(self, vaga_id: UUID, vaga_update: VagaUpdate) -> Optional[VagaInDB]:
        """Atualiza uma vaga existente"""
        try:
            vaga_existente = self.obter_vaga(vaga_id)
            if not vaga_existente:
                return None
            
            update_data = vaga_update.model_dump(exclude_unset=True)
            if not update_data:
                return vaga_existente
            
            update_data['vaga_id'] = str(vaga_id)
            
            set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys() if key != 'vaga_id'])
            
            query = text(f"""
                UPDATE vagas 
                SET {set_clause}
                WHERE id = :vaga_id
                RETURNING *
            """)
            
            result = self.db.execute(query, update_data)
            self.db.commit()
            
            vaga_atualizada = result.fetchone()
            return VagaInDB(**dict(vaga_atualizada._mapping))
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao atualizar vaga {vaga_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao atualizar vaga"
            )

    def excluir_vaga(self, vaga_id: UUID) -> bool:
        """Exclui uma vaga do banco de dados"""
        try:
            query = text("DELETE FROM vagas WHERE id = :vaga_id")
            result = self.db.execute(query, {"vaga_id": str(vaga_id)})
            self.db.commit()
            
            return result.rowcount > 0
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao excluir vaga {vaga_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao excluir vaga"
            )