import nanoid
from uuid import uuid4


def gen_nuid() -> str:
    return nanoid.generate()


def gen_uuid() -> str:
    return str(uuid4())


if __name__ == "__main__":
    print(gen_nuid())
    print(gen_uuid())
