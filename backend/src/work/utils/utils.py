from uuid import uuid4
import secrets


def gen_uuid() -> str:
    return str(uuid4())

if __name__ == '__main__':
    print(gen_uuid())