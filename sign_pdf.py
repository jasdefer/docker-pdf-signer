import argparse
import logging
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import os
import tempfile


def create_overlay(page, svg_path, x, y, scale):
    media_box = page.MediaBox
    page_width = float(media_box[2]) - float(media_box[0])
    page_height = float(media_box[3]) - float(media_box[1])

    fd, overlay_path = tempfile.mkstemp(suffix='.pdf')
    os.close(fd)

    c = canvas.Canvas(overlay_path, pagesize=(page_width, page_height))
    drawing = svg2rlg(svg_path)
    drawing.scale(scale, scale)
    renderPDF.draw(drawing, c, x, y)

    c.showPage()
    c.save()

    overlay_pdf = PdfReader(overlay_path)
    overlay_page = overlay_pdf.pages[0]

    os.remove(overlay_path)
    return overlay_page


def main():
    parser = argparse.ArgumentParser(
        description="Stamp an SVG signature onto a PDF page."
    )
    parser.add_argument("--pdf", required=True, help="Input PDF file")
    parser.add_argument("--page", type=int, required=True, help="1-based page number")

    # Absolute coordinates
    parser.add_argument("--x", type=float, help="X absolute coord in points")
    parser.add_argument("--y", type=float, help="Y absolute coord in points")

    # Relative coordinates
    parser.add_argument("--rel-x", type=float, help="Relative X in [0,1]")
    parser.add_argument("--rel-y", type=float, help="Relative Y in [0,1]")

    parser.add_argument("--scale", type=float, required=True, help="Scale factor")
    parser.add_argument("--signature", default="signature.svg", help="SVG signature filename")
    parser.add_argument("--output", help="Output filename")
    
    # NEW OPTION: overwrite input PDF
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite the original PDF instead of creating a .signed.pdf file"
    )

    args = parser.parse_args()

    input_path = args.pdf
    sig_path = args.signature

    if not os.path.isfile(input_path):
        raise SystemExit(f"Input PDF not found: {input_path}")
    if not os.path.isfile(sig_path):
        raise SystemExit(f"Signature SVG not found: {sig_path}")
    if args.page < 1:
        raise SystemExit("Page number must be >= 1")

    using_rel = (args.rel_x is not None or args.rel_y is not None)
    using_abs = (args.x is not None or args.y is not None)

    if using_rel and using_abs:
        raise SystemExit("Use either --x/--y OR --rel-x/--rel-y, not both")

    if not using_rel and not using_abs:
        raise SystemExit("Provide either absolute (--x/--y) or relative (--rel-x/--rel-y)")

    reader = PdfReader(input_path)
    num_pages = len(reader.pages)

    if args.page > num_pages:
        raise SystemExit(f"Page {args.page} out of range (document has {num_pages} pages)")

    page = reader.pages[args.page - 1]
    media_box = page.MediaBox
    page_width = float(media_box[2]) - float(media_box[0])
    page_height = float(media_box[3]) - float(media_box[1])

    if using_rel:
        if args.rel_x is None or args.rel_y is None:
            raise SystemExit("Both --rel-x and --rel-y must be provided when using relative coords")
        if not (0 <= args.rel_x <= 1 and 0 <= args.rel_y <= 1):
            raise SystemExit("--rel-x and --rel-y must be in [0,1]")
        x = args.rel_x * page_width
        y = args.rel_y * page_height
    else:
        if args.x is None or args.y is None:
            raise SystemExit("Both --x and --y must be provided when using absolute coords")
        x, y = args.x, args.y

    overlay_page = create_overlay(page, sig_path, x, y, args.scale)
    merger = PageMerge(page)
    merger.add(overlay_page)
    merger.render()

    # Output logic including overwrite mode
    if args.overwrite:
        output_path = input_path
    elif args.output:
        output_path = args.output
    else:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}.signed{ext}"

    writer = PdfWriter()
    writer.trailer = reader
    writer.write(output_path)

    print(f"Written signed PDF to: {output_path}")

def quiet_pdfrw():
    # Set pdfrw-related loggers to ERROR or higher
    logging.getLogger("pdfrw").setLevel(logging.ERROR)
    logging.getLogger("pdfrw.tokens").setLevel(logging.ERROR)
    logging.getLogger("pdfrw.pdfreader").setLevel(logging.ERROR)

if __name__ == "__main__":
    quiet_pdfrw()
    main()
