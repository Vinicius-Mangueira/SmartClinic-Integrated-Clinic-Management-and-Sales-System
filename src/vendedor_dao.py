from dataclasses import dataclass
from typing import List, Optional
from mysql.connector import Error
from db import get_conn


@dataclass(frozen=True)
class Vendedor:
    id_vendedor: int
    nome: str
    cpf: str
    email: str
    telefone: Optional[str]


class VendedorDAO:

    @staticmethod
    def inserir(nome, cpf, email, telefone=None) -> int:
        sql = "INSERT INTO vendedor (nome, cpf, email, telefone) VALUES (%s,%s,%s,%s)"
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (nome, cpf, email, telefone))
                conn.commit()
                return int(cur.lastrowid)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao inserir vendedor: {e}")
            finally:
                cur.close()

    @staticmethod
    def alterar(id_vendedor, nome, cpf, email, telefone=None) -> int:
        sql = "UPDATE vendedor SET nome=%s,cpf=%s,email=%s,telefone=%s WHERE id_vendedor=%s"
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (nome, cpf, email, telefone, id_vendedor))
                conn.commit(); return int(cur.rowcount)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao alterar vendedor: {e}")
            finally:
                cur.close()

    @staticmethod
    def remover(id_vendedor) -> int:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM vendedor WHERE id_vendedor=%s", (id_vendedor,))
                conn.commit(); return int(cur.rowcount)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao remover vendedor: {e}")
            finally:
                cur.close()

    @staticmethod
    def listar_todos() -> List[Vendedor]:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id_vendedor,nome,cpf,email,telefone FROM vendedor ORDER BY nome")
                return [Vendedor(*r) for r in cur.fetchall()]
            except Error as e:
                raise RuntimeError(f"Erro ao listar vendedores: {e}")
            finally:
                cur.close()

    @staticmethod
    def buscar_por_id(id_vendedor) -> Optional[Vendedor]:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id_vendedor,nome,cpf,email,telefone FROM vendedor WHERE id_vendedor=%s",
                            (id_vendedor,))
                r = cur.fetchone()
                return Vendedor(*r) if r else None
            except Error as e:
                raise RuntimeError(f"Erro ao buscar vendedor: {e}")
            finally:
                cur.close()

    @staticmethod
    def pesquisar_por_nome(parte_nome) -> List[Vendedor]:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id_vendedor,nome,cpf,email,telefone FROM vendedor WHERE nome LIKE %s ORDER BY nome",
                            (f"%{parte_nome}%",))
                return [Vendedor(*r) for r in cur.fetchall()]
            except Error as e:
                raise RuntimeError(f"Erro ao pesquisar vendedor: {e}")
            finally:
                cur.close()

    @staticmethod
    def relatorio_mensal(ano=None, mes=None) -> List[dict]:
        """Usa a view vw_relatorio_mensal para gerar relatório por vendedor."""
        sql = "SELECT vendedor, ano, mes, total_vendas, faturamento, ticket_medio FROM vw_relatorio_mensal"
        params = []
        filtros = []
        if ano:
            filtros.append("ano=%s"); params.append(ano)
        if mes:
            filtros.append("mes=%s"); params.append(mes)
        if filtros:
            sql += " WHERE " + " AND ".join(filtros)
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, params)
                cols = ["vendedor","ano","mes","total_vendas","faturamento","ticket_medio"]
                return [dict(zip(cols, r)) for r in cur.fetchall()]
            except Error as e:
                raise RuntimeError(f"Erro no relatório: {e}")
            finally:
                cur.close()