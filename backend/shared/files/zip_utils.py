import os
import uuid
import zipfile


def extract_zip(tmp_zip_path: str) -> str:
    extract_dir = f"/tmp/{uuid.uuid4()}"
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(tmp_zip_path, "r") as z:
        z.extractall(extract_dir)

    files = os.listdir(extract_dir)
    if not files:
        raise ValueError("Zip пустой")

    return os.path.join(extract_dir, files[0])

