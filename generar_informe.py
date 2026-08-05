from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


OUTPUT = "Informe_tecnico_perforacion_y_bomba.docx"
BLUE = "1F4E78"
LIGHT_BLUE = "D9EAF7"
LIGHT_GRAY = "F2F2F2"
AMBER = "FFF2CC"


def set_cell_shading(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def set_cell_margins(cell, top=100, start=100, bottom=100, end=100):
    tc = cell._tc
    tc_pr = tc.get_or_add_tcPr()
    tc_mar = tc_pr.first_child_found_in("w:tcMar")
    if tc_mar is None:
        tc_mar = OxmlElement("w:tcMar")
        tc_pr.append(tc_mar)
    for margin, value in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        node = tc_mar.find(qn(f"w:{margin}"))
        if node is None:
            node = OxmlElement(f"w:{margin}")
            tc_mar.append(node)
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def add_table(document, headers, rows, widths=None, total_row=None):
    table = document.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    table.autofit = False

    header = table.rows[0]
    set_repeat_table_header(header)
    for idx, text in enumerate(headers):
        cell = header.cells[idx]
        cell.text = str(text)
        set_cell_shading(cell, BLUE)
        set_cell_margins(cell)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for paragraph in cell.paragraphs:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in paragraph.runs:
                run.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(9)

    for row_idx, values in enumerate(rows):
        cells = table.add_row().cells
        for idx, value in enumerate(values):
            cells[idx].text = str(value)
            set_cell_margins(cells[idx])
            cells[idx].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if row_idx % 2:
                set_cell_shading(cells[idx], LIGHT_GRAY)
            for paragraph in cells[idx].paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(9)

    if total_row is not None:
        cells = table.add_row().cells
        for idx, value in enumerate(total_row):
            cells[idx].text = str(value)
            set_cell_shading(cells[idx], LIGHT_BLUE)
            set_cell_margins(cells[idx])
            for paragraph in cells[idx].paragraphs:
                for run in paragraph.runs:
                    run.bold = True
                    run.font.size = Pt(9)

    if widths:
        for row in table.rows:
            for idx, width in enumerate(widths):
                row.cells[idx].width = Cm(width)
    return table


def add_page_number(paragraph):
    paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = paragraph.add_run("Página ")
    run.font.size = Pt(8)
    field = OxmlElement("w:fldSimple")
    field.set(qn("w:instr"), "PAGE")
    paragraph._p.append(field)


def add_heading(document, text, level=1):
    paragraph = document.add_heading(text, level=level)
    paragraph.paragraph_format.keep_with_next = True
    return paragraph


def add_bullet(document, text):
    paragraph = document.add_paragraph(style="List Bullet")
    paragraph.add_run(text)
    return paragraph


document = Document()
section = document.sections[0]
section.top_margin = Cm(1.8)
section.bottom_margin = Cm(1.6)
section.left_margin = Cm(2)
section.right_margin = Cm(2)

styles = document.styles
normal = styles["Normal"]
normal.font.name = "Aptos"
normal.font.size = Pt(10.5)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.08

for style_name, size, color in (("Title", 26, BLUE), ("Heading 1", 16, BLUE), ("Heading 2", 12, BLUE)):
    style = styles[style_name]
    style.font.name = "Aptos Display"
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor.from_string(color)

footer = section.footer
footer_p = footer.paragraphs[0]
footer_p.add_run("Informe técnico de perforación y sistema de bombeo  |  ")
add_page_number(footer_p)

# Portada
title = document.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
title.paragraph_format.space_before = Pt(72)
title.paragraph_format.space_after = Pt(18)
run = title.add_run("INFORME TÉCNICO")
run.bold = True
run.font.name = "Aptos Display"
run.font.size = Pt(28)
run.font.color.rgb = RGBColor.from_string(BLUE)

subtitle = document.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
subtitle.paragraph_format.space_after = Pt(48)
run = subtitle.add_run("Perforación, entubado y sistema de bombeo")
run.font.size = Pt(18)
run.font.color.rgb = RGBColor.from_string(BLUE)

summary = document.add_table(rows=4, cols=2)
summary.style = "Table Grid"
summary.alignment = WD_TABLE_ALIGNMENT.CENTER
summary_data = (
    ("Profundidad total", "42 m"),
    ("Diámetro de entubado", "PVC pocero Ø 115 mm"),
    ("Bomba prevista", "Motorarg Pack 120M, 1 HP, monofásica"),
    ("Fecha del informe", "5 de agosto de 2026"),
)
for i, (label, value) in enumerate(summary_data):
    summary.cell(i, 0).text = label
    summary.cell(i, 1).text = value
    set_cell_shading(summary.cell(i, 0), LIGHT_BLUE)
    for cell in summary.rows[i].cells:
        set_cell_margins(cell, 140, 140, 140, 140)
    for run in summary.cell(i, 0).paragraphs[0].runs:
        run.bold = True

document.add_paragraph()
notice = document.add_paragraph()
notice.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = notice.add_run("Documento elaborado a partir de la información suministrada.")
run.italic = True
run.font.size = Pt(9)
run.font.color.rgb = RGBColor(100, 100, 100)

document.add_page_break()

add_heading(document, "1. Objeto y alcance")
document.add_paragraph(
    "El presente informe describe los trabajos previstos para la ejecución de una perforación de "
    "42 m de profundidad, su entubado, acondicionamiento, limpieza, instalación de la electrobomba "
    "sumergible definitiva y armado de la cañería de impulsión con sus accesorios de salida."
)

add_heading(document, "2. Perforación y perfil constructivo")
document.add_paragraph(
    "La perforación tendrá una profundidad total de 42 m y será revestida con componentes de PVC "
    "pocero de 115 mm. De acuerdo con las longitudes informadas, el perfil constructivo queda "
    "distribuido del siguiente modo:"
)

add_table(
    document,
    ["Tramo de profundidad", "Elemento", "Longitud", "Función"],
    [
        ("0 a 31 m", "Tubo PVC pocero Ø 115 mm, liso", "31 m", "Revestimiento ciego del pozo"),
        ("31 a 40 m", "Tubo PVC pocero Ø 115 mm, ranurado", "9 m", "Sector de captación de agua"),
        ("40 a 42 m", "Tapón / tramo de fondo", "2 m", "Cierre y protección del fondo"),
    ],
    widths=[3.1, 5.4, 2.0, 5.8],
    total_row=("Total", "", "42 m", ""),
)

document.add_paragraph()
add_heading(document, "2.1 Materiales y terminación", level=2)
add_table(
    document,
    ["Cantidad", "Material o componente", "Aplicación"],
    [
        ("31 m", "Tubo PVC pocero Ø 115 mm, liso", "Entubado ciego"),
        ("9 m", "Tubo PVC pocero Ø 115 mm, ranurado", "Filtro de captación"),
        ("2 m", "Tapón / tramo de fondo", "Terminación inferior"),
        ("1 unidad", "Tapa Tigre PVC 110 torneada", "Cierre superior"),
        ("1,5 m³", "Grava seleccionada", "Prefiltro alrededor del tramo ranurado"),
        ("2 bolsas", "Cemento", "Sellado de la parte superior"),
        ("1 unidad", "Grampa de sujeción de cañería", "Fijación del conjunto"),
        ("2 unidades", "Cámara de inspección cloacal 60 × 60 × 40 cm", "Protección superficial"),
    ],
    widths=[2.5, 7.0, 7.0],
)

add_heading(document, "2.2 Procedimiento previsto", level=2)
for text in (
    "Ejecutar la perforación hasta alcanzar los 42 m de profundidad total.",
    "Instalar el entubado liso, el tramo ranurado y el tapón de fondo según el perfil indicado.",
    "Colocar 1,5 m³ de grava seleccionada como prefiltro.",
    "Cementar y sellar la parte superior del pozo.",
    "Realizar la limpieza y el desarrollo del pozo con bomba propiedad del ejecutor.",
    "Proteger la boca y las conexiones mediante cámara de cemento.",
):
    add_bullet(document, text)

add_heading(document, "3. Electrobomba sumergible")
add_table(
    document,
    ["Característica", "Especificación informada"],
    [
        ("Marca", "Motorarg"),
        ("Modelo", "Pack 120M"),
        ("Tipo", "Electrobomba sumergible"),
        ("Potencia", "1 HP"),
        ("Alimentación", "Monofásica"),
        ("Rendimiento nominal informado", "6.000 L/h (6 m³/h)"),
        ("Cable incluido", "15 m"),
        ("Profundidad de colocación", "18 m estimados según la cañería de bajada; a confirmar en obra"),
    ],
    widths=[6.0, 10.5],
)

document.add_paragraph()
warning = document.add_table(rows=1, cols=1)
warning.style = "Table Grid"
cell = warning.cell(0, 0)
set_cell_shading(cell, AMBER)
set_cell_margins(cell, 150, 180, 150, 180)
p = cell.paragraphs[0]
r = p.add_run("Observación técnica: ")
r.bold = True
p.add_run(
    "la cañería informada para bajar la bomba tiene 18 m, mientras que la bomba se entrega con "
    "15 m de cable. Antes del montaje debe confirmarse la cota definitiva de instalación y prever, "
    "si corresponde, una extensión o empalme sumergible estanco ejecutado con materiales aptos."
)

add_heading(document, "4. Cañería de bomba y accesorios de salida")
document.add_paragraph(
    "La impulsión se realizará con caño de polipropileno de 1¼”. La salida contará con unión "
    "desmontable, llave para toma de muestra y caudalímetro para control del volumen bombeado."
)
add_table(
    document,
    ["Cantidad", "Componente", "Función principal"],
    [
        ("18 m", "Caño de polipropileno 1¼”", "Bajada e impulsión de la bomba"),
        ("2", "Cuplas de polipropileno 1¼”", "Unión de tramos"),
        ("1", "Curva HH de polipropileno 1¼”", "Cambio de dirección"),
        ("1", "Unión doble de polipropileno 1¼”", "Desmontaje y mantenimiento"),
        ("3", "Roscas con tuerca de polipropileno 1¼”", "Conexiones roscadas"),
        ("1", "Tee de polipropileno 1¼”", "Derivación de salida"),
        ("1", "Buje reductor 1¼” × ½” de polipropileno", "Reducción para toma de muestra"),
        ("1", "Llave esférica con pico para manguera ½”, italiana", "Canilla para toma de muestra"),
        ("1", "Caudalímetro roscado 1¼”", "Medición del caudal/volumen"),
        ("1", "Grampa de sujeción", "Sujeción de la cañería"),
    ],
    widths=[2.2, 8.2, 6.1],
)

add_heading(document, "4.1 Secuencia funcional de salida", level=2)
document.add_paragraph(
    "Bomba sumergible → cañería de impulsión de 1¼” → curva y uniones → tee de derivación → "
    "reducción de ½” con llave para toma de muestra → caudalímetro de 1¼” → salida de servicio."
)

document.add_page_break()
add_heading(document, "5. Resumen económico")
document.add_paragraph(
    "Los importes se reproducen según los datos suministrados. No se informó condición impositiva, "
    "vigencia de precios ni forma de pago."
)
add_table(
    document,
    ["Concepto", "Importe"],
    [
        ("Perforación, entubado, materiales y trabajos asociados", "$ 2.740.000"),
        ("Electrobomba Motorarg Pack 120M", "$ 480.000"),
        ("Cañería de bomba, accesorios, caudalímetro y cámaras", "$ 960.100"),
    ],
    widths=[12.5, 4.0],
    total_row=("TOTAL GENERAL", "$ 4.180.100"),
)

add_heading(document, "5.1 Detalle económico de cañería y salida", level=2)
add_table(
    document,
    ["Cant.", "Descripción", "Importe"],
    [
        ("18 m", "Caño polipropileno 1¼”", "$ 108.900"),
        ("2", "Cupla polipropileno 1¼”", "$ 3.800"),
        ("1", "Curva HH polipropileno 1¼”", "$ 5.500"),
        ("1", "Unión doble polipropileno 1¼”", "$ 5.700"),
        ("3", "Roscas con tuerca polipropileno 1¼”", "$ 2.700"),
        ("1", "Tee polipropileno 1¼”", "$ 2.600"),
        ("1", "Buje reductor 1¼” × ½”", "$ 900"),
        ("1", "Llave esférica pico manguera ½”, italiana", "$ 15.000"),
        ("1", "Caudalímetro rosca 1¼”", "$ 715.000"),
        ("2", "Cámara de inspección cloacal 60 × 60 × 40 cm", "$ 100.000"),
    ],
    widths=[2.0, 10.5, 4.0],
    total_row=("", "SUBTOTAL", "$ 960.100"),
)

add_heading(document, "6. Verificaciones y puesta en servicio")
for text in (
    "Confirmar en obra la profundidad definitiva de suspensión de la bomba.",
    "Verificar que la longitud y sección del cable eléctrico sean adecuadas; cualquier empalme debe ser sumergible y estanco.",
    "Comprobar el sentido de flujo y la correcta instalación del caudalímetro.",
    "Purgar y limpiar la instalación antes de tomar la muestra de agua.",
    "Registrar el caudal de explotación y, de ser requerido, los niveles estático y dinámico.",
    "Mantener la boca del pozo sellada y la cámara superficial limpia, protegida y con acceso para mantenimiento.",
):
    add_bullet(document, text)

add_heading(document, "7. Aclaraciones")
document.add_paragraph(
    "No se suministró un perfil geológico ni una descripción de los estratos atravesados; por lo "
    "tanto, este informe detalla los materiales constructivos de la perforación, pero no identifica "
    "los materiales del terreno. Tampoco se informaron nivel estático, nivel dinámico, ensayo de "
    "bombeo, ubicación de la obra ni análisis de calidad de agua."
)
document.add_paragraph(
    "Las cotas de los tramos se presentan en función de las longitudes declaradas (31 m lisos, "
    "9 m ranurados y 2 m de tapón). Deben cotejarse con el registro final de obra."
)

document.save(OUTPUT)
print(OUTPUT)
