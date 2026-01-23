import xml.etree.ElementTree as ET
from xml.dom import minidom

from output.serializers.base import OutputSerializer
from domain.scrape_result import ScrapeResult

class XMLSerializer(OutputSerializer):
    
    @staticmethod
    def serialize(data: ScrapeResult) -> str:
        if not data:
            return "<ScrapeResult></ScrapeResult>"
        
        root = ET.Element("ScrapeResult")
        
        ET.SubElement(root, "ProfileName").text = data.profile_name
        ET.SubElement(root, "ProfileURL").text = data.profile_url
        ET.SubElement(root, "CommentsStatus").text = data.comments_status.value

        account_comments = ET.SubElement(root, "AccountComments")
        for comment in data.account_comments:
            comment_element = ET.SubElement(account_comments, "Comment")
            ET.SubElement(comment_element, "AuthorName").text = comment.author_name
            ET.SubElement(comment_element, "Text").text = comment.text
            ET.SubElement(comment_element, "Timestamp").text = str(comment.timestamp)

        return XMLSerializer._prettify(root)
    
    @staticmethod
    def _prettify(element: ET.Element) -> str:
        rough_string = ET.tostring(element, 'unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")