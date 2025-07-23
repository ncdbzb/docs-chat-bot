import io
from docx import Document
from app.documents.schemas import Chunk


def is_all_caps(text: str) -> bool:
    clean_text = text.replace(' ', '').replace('\n', '')
    return clean_text.isupper() and any(c.isalpha() for c in clean_text)


def parse_docx_to_chunks(file_bytes: bytes) -> list[Chunk]:
    file_stream = io.BytesIO(file_bytes)
    doc = Document(file_stream)
    chunks: list[Chunk] = []

    current_heading = None
    current_content = []
    preamble = []

    def flush_chunk():
        nonlocal current_heading, current_content
        if current_heading and current_content:
            full_text = f"{current_heading}\n\n" + "\n".join(current_content).strip()
            chunks.append(Chunk(
                id=Chunk.create_id(),
                text=full_text
            ))
        current_content = []

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        if is_all_caps(text):
            if preamble:
                chunks.append(Chunk(
                    id=Chunk.create_id(),
                    text="\n".join(preamble).strip()
                ))
                preamble = []
            flush_chunk()
            current_heading = text
        else:
            if current_heading:
                current_content.append(text)
            else:
                preamble.append(text)

    if current_heading and current_content:
        flush_chunk()
    elif preamble:
        chunks.append(Chunk(
            id=Chunk.create_id(),
            text="\n".join(preamble).strip()
        ))

    # save_chunks_to_txt(chunks)
    return chunks


# def save_chunks_to_txt(chunks: list[Chunk], output_path="chunks.txt"):
#     with open(output_path, "w", encoding="utf-8") as f:
#         for chunk in chunks:
#             f.write(chunk.text.strip() + "\n\n")

