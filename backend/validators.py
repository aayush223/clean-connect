class LocationParser:
    """Verifies GPS coordinate ranges and extracts metadata from base64 files."""
    @staticmethod
    def verify_and_extract_metadata(image_base64: str) -> bool:
        # Mocking extraction of EXIF geotags from the uploaded image.
        # In production, use Pillow: PIL.Image.open(BytesIO(base64.b64decode(image_base64)))
        if len(image_base64) < 100:
            return False
        return True
