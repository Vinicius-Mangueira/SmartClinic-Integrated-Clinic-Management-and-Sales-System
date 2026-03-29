from dataclasses import dataclass
from typing import List, Optional
from mysql.connector import Error
from db import get_conn


@dataclass(frozen=True)
class Produto:
    id_produto: int
    nome: str
    descricao: Optional[str]
    preco: float
    quantidade: int
    categoria: str
    fabricado_em_mari: bool


class ProdutoDAO:

    @staticmethod
    def inserir(nome, descricao, preco, quantidade, categoria, fabricado_em_mari=False) -> int:
        sql = """INSERT INTO produto (nome, descricao, preco, quantidade, categoria, fabricado_em_mari)
                 VALUES (%s,%s,%s,%s,%s,%s)"""
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (nome, descricao, preco, quantidade, categoria, int(fabricado_em_mari)))
                conn.commit(); return int(cur.lastrowid)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao inserir produto: {e}")
            finally:
                cur.close()

    @staticmethod
    def alterar(id_produto, nome, descricao, preco, quantidade, categoria, fabricado_em_mari) -> int:
        sql = """UPDATE produto SET nome=%s,descricao=%s,preco=%s,quantidade=%s,
                 categoria=%s,fabricado_em_mari=%s WHERE id_produto=%s"""
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (nome, descricao, preco, quantidade, categoria,
                                  int(fabricado_em_mari), id_produto))
                conn.commit(); return int(cur.rowcount)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao alterar produto: {e}")
            finally:
                cur.close()

    @staticmethod
    def remover(id_produto) -> int:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM produto WHERE id_produto=%s", (id_produto,))
                conn.commit(); return int(cur.rowcount)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao remover produto: {e}")
            finally:
                cur.close()

    @staticmethod
    def _rows_to_list(cur) -> List[Produto]:
        return [Produto(r[0], r[1], r[2], float(r[3]), r[4], r[5], bool(r[6]))
                for r in cur.fetchall()]

    @staticmethod
    def listar_todos() -> List[Produto]:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id_produto,nome,descricao,preco,quantidade,categoria,fabricado_em_mari FROM produto ORDER BY nome")
                return ProdutoDAO._rows_to_list(cur)
            except Error as e:
                raise RuntimeError(f"Erro ao listar produtos: {e}")
            finally:
                cur.close()

    @staticmethod
    def buscar_por_id(id_produto) -> Optional[Produto]:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id_produto,nome,descricao,preco,quantidade,categoria,fabricado_em_mari FROM produto WHERE id_produto=%s",
                            (id_produto,))
                r = cur.fetchone()
                if r:
                    return Produto(r[0], r[1], r[2], float(r[3]), r[4], r[5], bool(r[6]))
                return None
            except Error as e:
                raise RuntimeError(f"Erro ao buscar produto: {e}")
            finally:
                cur.close()

    @staticmethod
    def pesquisar(nome=None, preco_min=None, preco_max=None,
                  categoria=None, fabricado_em_mari=None,
                  estoque_baixo=False) -> List[Produto]:
        """
        Filtros combinados:
        - nome: busca parcial
        - preco_min / preco_max: faixa de preço
        - categoria: categoria exata
        - fabricado_em_mari: True/False
        - estoque_baixo: mostra apenas produtos com quantidade < 5 (uso do funcionário)
        """
        sql = """SELECT id_produto,nome,descricao,preco,quantidade,categoria,fabricado_em_mari
                 FROM produto WHERE 1=1"""
        params = []
        if nome:
            sql += " AND nome LIKE %s"; params.append(f"%{nome}%")
        if preco_min is not None:
            sql += " AND preco >= %s"; params.append(preco_min)
        if preco_max is not None:
            sql += " AND preco <= %s"; params.append(preco_max)
        if categoria:
            sql += " AND categoria = %s"; params.append(categoria)
        if fabricado_em_mari is not None:
            sql += " AND fabricado_em_mari = %s"; params.append(int(fabricado_em_mari))
        if estoque_baixo:
            sql += " AND quantidade < 5"
        sql += " ORDER BY nome"

        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, params)
                return ProdutoDAO._rows_to_list(cur)
            except Error as e:
                raise RuntimeError(f"Erro ao pesquisar produto: {e}")
            finally:
                cur.close()

    @staticmethod
    def listar_categorias() -> List[str]:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT DISTINCT categoria FROM produto ORDER BY categoria")
                return [r[0] for r in cur.fetchall()]
            except Error as e:
                raise RuntimeError(f"Erro ao listar categorias: {e}")
            finally:
                cur.close()

    @staticmethod
    def gerar_relatorio() -> dict:
        sql = """SELECT COUNT(*), SUM(preco*quantidade),
                        AVG(preco), SUM(quantidade),
                        SUM(quantidade < 5)
                 FROM produto"""
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql)
                r = cur.fetchone()
                return {
                    "total_produtos":   r[0] or 0,
                    "valor_estoque":    float(r[1] or 0),
                    "preco_medio":      float(r[2] or 0),
                    "unidades_total":   r[3] or 0,
                    "estoque_baixo":    r[4] or 0,
                }
            except Error as e:
                raise RuntimeError(f"Erro no relatório: {e}")
            finally:
                cur.close()