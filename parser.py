from datetime import datetime
import json
import xml.etree.ElementTree as ET
from datetime import datetime

from constants import DEFAULT_LANGUAGE, DEFAULT_OPTIONS_QUOTA
from exceptions import BookingValidationError
from models import BookingRequest, Parameter
from services import BookingService


class BookingRequestParser:
    @staticmethod
    def parse_request(xml_string: str) -> BookingRequest:
        root = ET.fromstring(xml_string)

        language_code = root.find(".//languageCode")
        options_quota_elem = root.find("optionsQuota")
        parameters = Parameter.from_xml(root.find(".//Parameter"))

        start_date = datetime.strptime(root.find("StartDate").text, "%d/%m/%Y")
        end_date = datetime.strptime(root.find("EndDate").text, "%d/%m/%Y")

        return BookingRequest(
            language_code=(
                language_code.text if language_code is not None else DEFAULT_LANGUAGE
            ),
            options_quota=(
                int(options_quota_elem.text)
                if options_quota_elem is not None
                else DEFAULT_OPTIONS_QUOTA
            ),
            parameters=parameters,
            search_type=root.find("SearchType").text,
            start_date=start_date,
            end_date=end_date,
            currency=root.find("Currency").text,
            nationality=root.find("Nationality").text,
            rooms=[],
        )


def process_booking_request(xml_string: str) -> str:
    try:
        # Parse request
        parser = BookingRequestParser()
        request = parser.parse_request(xml_string)

        # Process request
        service = BookingService()
        response = service.process_request(request)

        return json.dumps(response, indent=2)

    except BookingValidationError as e:
        return json.dumps({"error": str(e)}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Internal error: {str(e)}"}, indent=2)
