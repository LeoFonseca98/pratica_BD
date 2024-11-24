from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email =Column(String, nullable=False)
    data_nascimento = Column(Date)

    conta = relationship(
        "Conta", back_populates="cliente", cascade="all, delete-orphan"
    ) 

    def __str__(self):
        return f"Cliente: nome({self.nome}) - email({self.email}) - Data de Nascimento({self.data_nascimento}) "

class Conta(Base):
    __tablename__ = 'conta'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    tipo = Column(String, nullable=False)

    cliente = relationship(
        "Cliente", back_populates="conta"
    )

    def __str__(self):
        return f"Conta: {self.tipo}"

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inspector_engine = inspect(engine)
print(inspector_engine.has_table("cliente"))

print(inspector_engine.get_table_names())
print(inspector_engine.default_schema_name)


with Session(engine) as session:
    leonardo = Cliente(
        nome = "Leonardo",
        email = "leonardo.fonseca@gmail.com",
        data_nascimento=date(1998, 7, 17)
    )
     

    joao = Cliente(
        nome = "João",
        email = "joao.fonseca@gmail.com",
        data_nascimento=date(1995, 7, 15)
    )

    session.add_all([leonardo, joao])

    session.commit()

    conta_leonardo = Conta(
        client_id=leonardo.id,
        tipo = "Corrente"
    )

    conta_joao = Conta(
        client_id=joao.id,
        tipo = "Poupança"
    )

    session.add_all([conta_leonardo])
    session.add_all([conta_joao])
    session.commit()

stmt_cliente = select(Cliente).where(Cliente.nome == "Leonardo")
leonardo = session.scalars(stmt_cliente).first()
print(leonardo)

stmt = select(Conta).where(Conta.client_id == leonardo.id)
for conta in session.scalars(stmt):
   print(f"Conta do tipo: {conta.tipo}, ID do Cliente: {conta.client_id}")


stmt_cliente = select(Cliente).where(Cliente.nome == "João")
joao = session.scalars(stmt_cliente).first()
print(joao)

stmt = select(Conta).where(Conta.client_id == joao.id)
for conta in session.scalars(stmt):
   print(f"Conta do tipo: {conta.tipo}, ID do Cliente: {conta.client_id}")
