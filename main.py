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

response = process_booking_request(sample_xml)
print(response)
