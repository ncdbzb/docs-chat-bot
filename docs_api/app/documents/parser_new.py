import io
import re
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.documents.schemas import Chunk


def extract_paragraphs_from_docx(docx_bytes: bytes) -> list[dict]:
    """Извлекает параграфы из docx вместе с их стилем"""
    file_stream = io.BytesIO(docx_bytes)
    doc = Document(file_stream)
    
    paragraphs = []
    figure_pattern = re.compile(r"^Рисунок\s+\d+(\.\d+)*", re.IGNORECASE)
    
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue
        if figure_pattern.match(text):
            continue
        paragraphs.append({
            "text": text,
            "style": paragraph.style.name
        })
    return paragraphs


def split_paragraphs_into_chunks(paragraphs: list[dict], min_chunk_size=800, max_chunk_size=1000, overlap=150) -> list[dict]:
    """
    Разбивает текст на чанки:
    - Использует заголовки как секции
    - Разбивает длинные чанки с RecursiveCharacterTextSplitter
    - Объединяет короткие с соседними
    """
    chunks = []
    current_chunk = None
    current_section = None

    for para in paragraphs:
        text = para["text"]
        style = para["style"]

        # Определяем заголовок
        if style.startswith("Heading"):
            current_section = text
            # Сохраняем предыдущий чанк
            if current_chunk and current_chunk["content"]:
                chunks.append(current_chunk)
            current_chunk = {
                "heading": text,
                "content": []
            }
        else:
            if current_chunk is None:
                current_chunk = {
                    "heading": "Без заголовка",
                    "content": []
                }
            current_chunk["content"].append(text)

    # Добавляем последний чанк
    if current_chunk and current_chunk["content"]:
        chunks.append(current_chunk)

    final_chunks = []
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=overlap,
        separators=["\n"]
    )

    for ch in chunks:
        chunk_text = "\n".join(ch["content"])
        section = ch["heading"]
        if len(chunk_text) > max_chunk_size:
            split_texts = text_splitter.split_text(chunk_text)
            for t in split_texts:
                final_chunks.append({"chunk": t, "section": section})
        else:
            final_chunks.append({"chunk": chunk_text, "section": section})

    merged_chunks = []
    buffer_text = ""
    buffer_section = None

    for c in final_chunks:
        text = c["chunk"]
        section = c["section"]

        if buffer_text and buffer_section == section and len(buffer_text) + len(text) <= max_chunk_size:
            buffer_text += "\n" + text
        else:
            if buffer_text:
                merged_chunks.append({"chunk": buffer_text, "section": buffer_section})
            buffer_text = text
            buffer_section = section

    if buffer_text:
        merged_chunks.append({"chunk": buffer_text, "section": buffer_section})

    return merged_chunks


def parse_docx_to_chunks(file_bytes: bytes) -> list[Chunk]:
    paragraphs = extract_paragraphs_from_docx(file_bytes)
    raw_chunks = split_paragraphs_into_chunks(paragraphs)

    chunks: list[Chunk] = []
    for c in raw_chunks:
        chunks.append(Chunk(
            id=Chunk.create_id(),
            text=c["chunk"],
            section=c.get("section"),
            source_id=0
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
