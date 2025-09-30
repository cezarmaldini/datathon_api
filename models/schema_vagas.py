from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID, uuid4


class SchemaVagas(BaseModel):
    data_requisicao: date = Field(..., description="Data em que a vaga foi requisitada")
    titulo_vaga: str = Field(..., min_length=1, max_length=200, description="Título da vaga")
    tipo_contratacao: str = Field(..., description="Modelo de contratação (CLT, PJ, Freelancer)")
    vaga_pcd: bool = Field(default=False, description="Se a vaga é específica para PCD")
    cidade: str = Field(..., description="Cidade da vaga")
    estado: str = Field(..., max_length=2, description="Estado da vaga (sigla)")
    pais: str = Field(default="Brasil", description="País da vaga")
    nivel_profissional: str = Field(..., description="Nível de senioridade (Júnior, Pleno, Sênior)")
    nivel_academico: str = Field(..., description="Nível acadêmico exigido")
    areas_atuacao: List[str] = Field(..., description="Áreas de atuação da vaga")
    principais_atividades: str = Field(..., description="Descrição das principais atividades")
    competencias_tecnicas: List[str] = Field(..., description="Competências técnicas e tecnologias")
    habilidades_comportamentais: List[str] = Field(..., description="Habilidades comportamentais")
    modalidade: str = Field(..., description="Modalidade (Remoto, Híbrido, Presencial)")
    ativa: bool = Field(default=True, description="Status da vaga (ativa/inativa)")


class VagaCreate(SchemaVagas):
    pass


class VagaUpdate(BaseModel):
    data_requisicao: Optional[date] = Field(None)
    titulo_vaga: Optional[str] = Field(None, min_length=1, max_length=200)
    tipo_contratacao: Optional[str] = Field(None)
    vaga_pcd: Optional[bool] = Field(None)
    cidade: Optional[str] = Field(None)
    estado: Optional[str] = Field(None, max_length=2)
    pais: Optional[str] = Field(None)
    nivel_profissional: Optional[str] = Field(None)
    nivel_academico: Optional[str] = Field(None)
    areas_atuacao: Optional[List[str]] = Field(None)
    principais_atividades: Optional[str] = Field(None)
    competencias_tecnicas: Optional[List[str]] = Field(None)
    habilidades_comportamentais: Optional[List[str]] = Field(None)
    modalidade: Optional[str] = Field(None)
    ativa: Optional[bool] = Field(None)


class VagaInDB(SchemaVagas):
    id: UUID = Field(default_factory=uuid4)
    criada_em: datetime = Field(default_factory=datetime.utcnow)
    atualizada_em: datetime = Field(default_factory=datetime.utcnow)


class VagaResponse(VagaInDB):
    class Config:
        from_attributes = True


class VagasListResponse(BaseModel):
    vagas: List[VagaResponse]
    total: int
    pagina: int
    por_pagina: int