"""
Module contains url builder
"""
from urllib import parse
from pydantic.networks import AnyUrl

class URLBuilder(AnyUrl):
    """
    URL builder for application configuration
    Args:
        AnyUrl (_type_): resulting url
    """
    allowed_schemes = {
        'http',
        'https',
    }
    __slots__ = ()

    @classmethod
    def encode_special_characters(cls, raw_input: str) -> str:
        """
        Encodes raw string with special characters('@' or '/' for example),
        into byte form
        Args:
            input (str): raw string with special characters

        Returns:
            str: resulting encoded string
        """
        return parse.quote_plus(raw_input)
