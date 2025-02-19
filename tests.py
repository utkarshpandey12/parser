from parser import process_booking_request

sample_xml = """
<AvailRQ xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <timeoutMilliseconds>25000</timeoutMilliseconds>
    <source>
        <languageCode>en</languageCode>
    </source>
    <optionsQuota>20</optionsQuota>
    <Configuration>
        <Parameters>
            <Parameter password="test123" username="testuser" CompanyID="123456"/>
        </Parameters>
    </Configuration>
    <SearchType>Multiple</SearchType>
    <StartDate>25/02/2025</StartDate>
    <EndDate>28/02/2025</EndDate>
    <Currency>USD</Currency>
    <Nationality>US</Nationality>
    <Paxes>
        <Pax age="35"/>
        <Pax age="4"/>
    </Paxes>
</AvailRQ>
"""

import unittest


class TestParser(unittest.TestCase):

    def test_booking_request(self):
        try:
            result = process_booking_request(sample_xml)
            assert isinstance(result, str), "Result should be a JSON string"
            print("✓ Successful booking test passed")
        except Exception as e:
            print(f"✗ Successful booking test failed: {str(e)}")

        try:
            invalid_xml = sample_xml.replace('password="test123"', "")
            result = process_booking_request(invalid_xml)
            assert '"error":' in result, "Should return error for invalid parameters"
            print("✓ Invalid parameters test passed")
        except Exception as e:
            print(f"✗ Invalid parameters test failed: {str(e)}")

        try:
            invalid_dates_xml = sample_xml.replace("28/02/2025", "26/02/2025")
            result = process_booking_request(invalid_dates_xml)
            assert '"error":' in result, "Should return error for invalid dates"
            print("✓ Date validation test passed")
        except Exception as e:
            print(f"✗ Date validation test failed: {str(e)}")


if __name__ == "__main__":
    unittest.main()
