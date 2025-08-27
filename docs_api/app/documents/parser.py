import io
import re
from docx2python import docx2python
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.documents.schemas import Chunk


def extract_paragraphs(docx_bytes: bytes) -> list[str]:
    """Извлечение всех параграфов из docx, включая вложенные списки"""
    file_stream = io.BytesIO(docx_bytes)
    doc = docx2python(file_stream)
    paragraphs = []

    def extract_text(para):
        texts = []
        for item in para:
            if isinstance(item, list):
                texts.extend(extract_text(item))
            elif isinstance(item, str):
                text = item.strip()
                if text:
                    texts.append(text)
        return texts

    for section in doc.body:
        for para in section:
            paragraphs.extend(extract_text(para))
    return paragraphs


def clean_text(text: str) -> str:
    """
    Очищает текст от:
    - маркеров списка "--", "-"
    - нумерации типа "1)", "1.2.3)", "12."
    """
    text = re.sub(r'^\d+([\.\d+]*)\)?\.?\s*', '', text)
    text = re.sub(r'^[-–—]{1,2}\s*', '', text)
    return text.strip()


def split_into_chunks(paragraphs: list[str], min_size=500, max_size=1000) -> list[dict]:
    """
    Делит документ на чанки:
    - объединяет маленькие подряд идущие чанки одного раздела
    - разбивает большие чанки с overlap 10%
    """
    chunks = []
    current_section = None
    current_chunk = []

    numbered_re = re.compile(r'^\d+([\.\d+]*)\)?\s+')
    header_re = re.compile(r'^[А-ЯЁ\s0-9\(\)]+$')

    # Шаг 1: базовое формирование чанков и merge подпунктов
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if header_re.match(para):
            current_section = clean_text(para)
            continue

        if numbered_re.match(para):
            if current_chunk:
                chunks.append({
                    "section": current_section,
                    "chunk": "\n".join(current_chunk)
                })
            current_chunk = [clean_text(para)]
        elif para.startswith("--") or para.startswith("-"):
            current_chunk.append(clean_text(para))
        else:
            current_chunk.append(clean_text(para))

    if current_chunk:
        chunks.append({
            "section": current_section,
            "chunk": "\n".join(current_chunk)
        })

    # Шаг 2: объединяем маленькие подряд идущие чанки внутри одного раздела
    temp = []
    for chunk in chunks:
        if len(chunk["chunk"]) < min_size:
            if temp and temp[-1]["section"] == chunk["section"]:
                temp[-1]["chunk"] += "\n" + chunk["chunk"]
            else:
                temp.append(chunk.copy())
        else:
            temp.append(chunk.copy())
    chunks = temp

    # Шаг 3: разбиваем большие чанки с overlap 10%
    final_chunks = []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_size,
        chunk_overlap=int(max_size * 0.1),
        separators=["\n"]
    )

    for idx, chunk in enumerate(chunks):
        text = chunk["chunk"]
        if len(text) > max_size:
            split_texts = splitter.split_text(text)
            for part in split_texts:
                final_chunks.append({
                    "section": chunk["section"],
                    "chunk": part,
                    "source_id": idx
                })
        else:
            final_chunks.append({
                "section": chunk["section"],
                "chunk": text,
                "source_id": idx
            })

    return final_chunks


# === Новая версия parse_docx_to_chunks для приложения ===
def parse_docx_to_chunks(file_bytes: bytes) -> list[Chunk]:
    paragraphs = extract_paragraphs(file_bytes)
    raw_chunks = split_into_chunks(paragraphs)

    chunks: list[Chunk] = []
    for c in raw_chunks:
        chunks.append(Chunk(
            id=Chunk.create_id(),
            text=c["chunk"],
            section=c.get("section"),
            source_id=c.get("source_id")
        ))

    save_chunks_to_file(chunks)
    return chunks


def save_chunks_to_file(chunks: list[Chunk], filename: str = 'chunks.txt') -> None:
    """
    Сохраняет все чанки в текстовый файл.
    
    :param chunks: Список объектов Chunk
    :param filename: Имя файла для сохранения
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for chunk in chunks:
            file.write(f"=== Раздел: {chunk.section} ===\n")
            file.write(f"{chunk.text}\n\n")
    print(f"Чанки успешно сохранены в {filename}")
