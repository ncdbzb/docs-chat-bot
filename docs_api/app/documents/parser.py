import io
from unstructured.partition.api import partition_via_api
from unstructured.documents.elements import Element

from app.documents.schemas import Chunk
from app.logger import logger
from app.config import settings


def _element_to_chunk(el: Element) -> Chunk:
    """
    Преобразует unstructured.Element в Chunk.
    - el.text -> text
    - el.category -> element_type
    - el.metadata может содержать filename, page_number и другие поля
    """
    text = getattr(el, "text", "") or ""
    metadata = {}
    try:
        metadata = dict(getattr(el, "metadata", {}) or {})
    except Exception:
        metadata = {}

    section = metadata.get("section") or metadata.get("title") or getattr(el, "category", None)

    source = metadata.get("filename") or metadata.get("source") or None

    page_number = metadata.get("page_number") or metadata.get("page") or None
    if isinstance(page_number, str) and page_number.isdigit():
        page_number = int(page_number)

    element_type = getattr(el, "category", None)

    return Chunk(
        id=Chunk.create_id(),
        text=text.strip(),
        section=section,
        source=source,
        page_number=page_number,
        element_type=element_type,
        metadata=metadata or None,
    )


def parse_docx_to_chunks(file_bytes: bytes, metadata_filename: str | None = "uploaded.docx") -> list[Chunk]:
    """
    Основная функция: принимает байты .docx и возвращает список Chunk.
    :param file_bytes: байты документа (как из MinIO)
    :param metadata_filename: имя файла, которое будет записано в метаданные (обязательно при передаче file)
    :return: список Chunk
    """
    if not isinstance(file_bytes, (bytes, bytearray)):
        raise TypeError("file_bytes должен быть bytes или bytearray")

    try:
        elements = partition_via_api(
            file=file_bytes,
            metadata_filename=metadata_filename,
            api_url=settings.unstructured_api_url,
            # chunking params
            chunking_strategy=settings.CHUNKING_STRATEGY,
            strategy=settings.UNSTRUCTURED_STRATEGY,
            max_characters=settings.MAX_CHARACTERS,
            new_after_n_chars=settings.NEW_AFTER_N_CHARS,
            combine_under_n_chars=settings.COMBINE_UNDER_N_CHARS,
        )
    except Exception as e:
        logger.exception("Error while partitioning document via unstructured API: %s", e)
        raise e

    chunks: list[Chunk] = []
    for el in elements:
        text = getattr(el, "text", None) or ""
        if not text.strip():
            continue
        chunks.append(_element_to_chunk(el))

    logger.info("Parsed %d chunks from document (metadata_filename=%s)", len(chunks), metadata_filename)

    save_chunks_to_file(chunks)
    return chunks


def save_chunks_to_file(chunks: list[Chunk], filename: str = "chunks.txt") -> None:
    """
    Сохраняет все чанки в текстовый файл.
    """
    with open(filename, "w", encoding="utf-8") as fh:
        for chunk in chunks:
            fh.write("=== Chunk ID: %s ===\n" % chunk.id)
            fh.write(f"Section: {chunk.section}\n")
            fh.write(f"Element type: {chunk.element_type}\n")
            fh.write(f"Source: {chunk.source}\n")
            fh.write(f"Page: {chunk.page_number}\n")
            fh.write("---\n")
            fh.write(chunk.text + "\n\n")
    logger.info("Chunks saved to %s", filename)
