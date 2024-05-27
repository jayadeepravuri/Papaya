import scrapy
from googletrans import Translator

class BoeSpider(scrapy.Spider):
    name = 'boe'
    allowed_domains = ['www.boe.es']
    start_urls = ['https://www.boe.es/diario_boe/xml.php?id=BOE-B-2022-20725']

    def parse(self, response):
        identifier = response.xpath('//identificador/text()').get()
        department = response.xpath('//departamento/text()').get()
        title = response.xpath('//titulo/text()').get()
        diary = response.xpath('//diario/text()').get()
        publication_date = response.xpath('//fecha_publicacion/text()').get()
        diary_number = response.xpath('//diario_numero/text()').get()
        section = response.xpath('//seccion/text()').get()
        subsection = response.xpath('//subseccion/text()').get()
        announcement_number = response.xpath('//numero_anuncio/text()').get()
        pdf_url = response.xpath('//url_pdf/text()').get()
        grant_type = response.xpath('//tipo/text()').get()

        # Helper function to get text and handle None
        def get_text_or_none(xpath_query):
            element = response.xpath(xpath_query).get()
            self.logger.debug(f"Extracted element for '{xpath_query}': {element}")
            return element.strip() if element else None

        # Find the next sibling <p> tag after the specified text for each field
        amount = get_text_or_none('//p[contains(text(), "Cuarto: Cuantía.")]/following-sibling::p[1]/text()')
        beneficiaries = get_text_or_none('//p[contains(text(), "Primero. Beneficiarios.")]/following-sibling::p[1]/text()')
        object_text = get_text_or_none('//p[contains(text(), "Segundo. Objeto.")]/following-sibling::p[1]/text()')
        regulations = get_text_or_none('//p[contains(text(), "Tercero. Bases Reguladoras.")]/following-sibling::p[1]/text()')
        deadline = get_text_or_none('//p[contains(text(), "Quinto. Plazo de Presentación de solicitudes.")]/following-sibling::p[1]/text()')

        # Initialize the translator
        translator = Translator()

        # Translate the text fields
        amount_translated = translator.translate(amount, dest='en').text if amount else None
        beneficiaries_translated = translator.translate(beneficiaries, dest='en').text if beneficiaries else None
        object_text_translated = translator.translate(object_text, dest='en').text if object_text else None
        regulations_translated = translator.translate(regulations, dest='en').text if regulations else None
        deadline_translated = translator.translate(deadline, dest='en').text if deadline else None

        yield {
            'identifier': identifier,
            'department': department,
            'title': title,
            'diary': diary,
            'publication_date': publication_date,
            'diary_number': diary_number,
            'section': section,
            'subsection': subsection,
            'announcement_number': announcement_number,
            'pdf_url': pdf_url,
            'grant_type': grant_type,
            'amount': amount_translated,
            'beneficiaries': beneficiaries_translated,
            'object_text': object_text_translated,
            'regulations': regulations_translated,
            'deadline': deadline_translated
        }
