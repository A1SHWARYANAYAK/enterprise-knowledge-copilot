import fitz


def extract_text_from_pdf(pdf_path: str):
    """
    Extract text page-by-page from a PDF.
    """

    document = fitz.open(pdf_path)

    pages = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)

        pages.append(
            {
                "page": page_num + 1,
                "text": page.get_text()
            }
        )

    document.close()

    return pages