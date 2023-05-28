import os
import traceback
from pathlib import Path

import aiofiles
from fastapi import File, UploadFile
from files.constants import FileType
from files.models import FileData, FileDataRead
from settings import get_settings
from share.exceptions import UnkownModelError
from sqlalchemy.ext.asyncio import AsyncSession


def generate_outfile_path(filename: str | None) -> str:
    if filename is None:
        filename = "filename"
    settings = get_settings()
    count = 1
    original_name = filename
    while os.path.exists(str(Path(settings.files_path, filename))):
        filename = f"{original_name.split('.')[0]}_{count}.{original_name.split('.')[-1]}"
        count += 1
    return str(Path(settings.files_path, filename))


async def create(file_type: FileType, session: AsyncSession, file: UploadFile = File(...)) -> FileDataRead:
    out_file = generate_outfile_path(file.filename)
    try:
        async with aiofiles.open(out_file, "wb") as save_file:
            content = await file.read()
            await save_file.write(content)
        instance = FileData(
            name=os.path.basename(out_file),
            file_path=out_file,
            file_type=file_type,
            id=None,
        )
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
    except Exception as error:
        print(traceback.format_exc())
        raise UnkownModelError(model="files", msg=str(error))
    return FileDataRead(**instance.dict())
