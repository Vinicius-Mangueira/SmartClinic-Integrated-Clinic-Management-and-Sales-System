from dataclasses import dataclass
from typing import List, Optional
from mysql.connector import Error
from db import get_conn


@dataclass(frozen=True)
class Cliente:
    id_cliente: int
    nome: str
    cpf: str
    telefone: Optional[str]
    email: str
    data_nascimento: Optional[str]
    cidade: Optional[str]
    torce_flamengo: bool
    assiste_one_piece: bool

    @property
    def tem_desconto(self) -> bool:
        return (self.torce_flamengo or self.assiste_one_piece or
                (self.cidade or "").lower() == "sousa")


class ClienteDAO:

    _SEL = """SELECT id_cliente, nome, cpf, telefone, email,
                     data_nascimento, cidade, torce_flamengo, assiste_one_piece
              FROM cliente"""

    @staticmethod
    def _row(r) -> 'Cliente':
        return Cliente(r[0], r[1], r[2], r[3], r[4],
                       str(r[5]) if r[5] else None,
                       r[6], bool(r[7]), bool(r[8]))

    @staticmethod
    def inserir(nome, cpf, telefone, email, data_nascimento,
                cidade=None, torce_flamengo=False, assiste_one_piece=False) -> int:
        sql = """INSERT INTO cliente
                 (nome,cpf,telefone,email,data_nascimento,cidade,torce_flamengo,assiste_one_piece)
                 VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (nome, cpf, telefone, email, data_nascimento,
                                  cidade, int(torce_flamengo), int(assiste_one_piece)))
                conn.commit(); return int(cur.lastrowid)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao inserir cliente: {e}")
            finally:
                cur.close()

    @staticmethod
    def alterar(id_cliente, nome, cpf, telefone, email, data_nascimento,
                cidade=None, torce_flamengo=False, assiste_one_piece=False) -> int:
        sql = """UPDATE cliente
                 SET nome=%s,cpf=%s,telefone=%s,email=%s,data_nascimento=%s,
                     cidade=%s,torce_flamengo=%s,assiste_one_piece=%s
                 WHERE id_cliente=%s"""
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (nome, cpf, telefone, email, data_nascimento,
                                  cidade, int(torce_flamengo), int(assiste_one_piece),
                                  id_cliente))
                conn.commit(); return int(cur.rowcount)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao alterar cliente: {e}")
            finally:
                cur.close()

    @staticmethod
    def pesquisar_por_nome(parte_nome) -> List['Cliente']:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(ClienteDAO._SEL + " WHERE nome LIKE %s ORDER BY nome",
                            (f"%{parte_nome}%",))
                return [ClienteDAO._row(r) for r in cur.fetchall()]
            except Error as e:
                raise RuntimeError(f"Erro ao pesquisar: {e}")
            finally:
                cur.close()

    @staticmethod
    def remover(id_cliente) -> int:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_cliente,))
                conn.commit(); return int(cur.rowcount)
            except Error as e:
                conn.rollback(); raise RuntimeError(f"Erro ao remover: {e}")
            finally:
                cur.close()

    @staticmethod
    def listar_todos() -> List['Cliente']:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(ClienteDAO._SEL + " ORDER BY nome")
                return [ClienteDAO._row(r) for r in cur.fetchall()]
            except Error as e:
                raise RuntimeError(f"Erro ao listar: {e}")
            finally:
                cur.close()

    @staticmethod
    def buscar_por_id(id_cliente) -> Optional['Cliente']:
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(ClienteDAO._SEL + " WHERE id_cliente=%s", (id_cliente,))
                r = cur.fetchone()
                return ClienteDAO._row(r) if r else None
            except Error as e:
                raise RuntimeError(f"Erro ao buscar: {e}")
            finally:
                cur.close()

    @staticmethod
    def gerar_relatorio() -> dict:
        sql = """SELECT COUNT(*), COUNT(telefone), COUNT(email),
                        SUM(torce_flamengo), SUM(assiste_one_piece),
                        SUM(LOWER(cidade)='sousa')
                 FROM cliente"""
        with get_conn() as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql)
                r = cur.fetchone()
                return {
                    "total_clientes":        r[0] or 0,
                    "clientes_com_telefone": r[1] or 0,
                    "clientes_com_email":    r[2] or 0,
                    "torcem_flamengo":       r[3] or 0,
                    "assistem_one_piece":    r[4] or 0,
                    "de_sousa":              r[5] or 0,
                }
            except Error as e:
                raise RuntimeError(f"Erro no relatório: {e}")
            finally:
                cur.close()