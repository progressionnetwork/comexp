def pagination(offset: int = 0, limit: int = 10):
    return {"offset": offset, "limit": limit}


def list_chunk(data: list, chunk_size: int = 1000) -> list:
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]
