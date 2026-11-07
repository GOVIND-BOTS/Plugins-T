
from sqlalchemy import Column, String, UnicodeText

from TelethonHell.DB import BASE, SESSION


class Gvar(BASE):
    __tablename__ = "gvar"

    variable = Column(String, primary_key=True, nullable=False)
    value = Column(UnicodeText, nullable=False)

    def __init__(self, variable, value):
        self.variable = str(variable)
        self.value = str(value)


Gvar.__table__.create(checkfirst=True)


def gvarstat(variable):
    try:
        result = (
            SESSION.query(Gvar.value)
            .filter(Gvar.variable == str(variable))
            .first()
        )

        return result[0] if result else None

    except Exception:
        SESSION.rollback()
        return None

    finally:
        SESSION.close()


def addgvar(variable, value):
    try:
        variable = str(variable)
        value = str(value)

        existing = (
            SESSION.query(Gvar)
            .filter(Gvar.variable == variable)
            .first()
        )

        if existing:
            existing.value = value
        else:
            adder = Gvar(variable, value)
            SESSION.add(adder)

        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()


def delgvar(variable):
    try:
        SESSION.query(Gvar).filter(
            Gvar.variable == str(variable)
        ).delete(synchronize_session=False)

        SESSION.commit()
        return True

    except Exception:
        SESSION.rollback()
        raise

    finally:
        SESSION.close()
