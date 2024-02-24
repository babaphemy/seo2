import pytest
from unittest.mock import patch, MagicMock
from app.service import seo_serv
@pytest.mark.usefixtures("setup")
class TestC():
    def multiply(self,x,y):
        return x * y
    def test_multipl(self):
        assert self.multiply(2,5) == 10, " Invalid argument"
    def test_multifail(self):
        assert self.multiply(4,4) == 16, "Gbese re ooooo"

@pytest.mark.asyncio
async def test_get_page_info():
    url = "http://example.com"
    expected_result = {
        "title": "Example Domain",
        "h1s": ["Example Domain"],
        "meta_description": "Example Domain for illustration"
    }

    # Mocking async_playwright and its methods
    mock_browser = MagicMock()
    mock_context = MagicMock()
    mock_page = MagicMock()
    mock_page.title.return_value = "Example Domain"
    mock_page.query_selector_all.return_value = [MagicMock(inner_text=MagicMock(return_value="Example Domain"))]
    mock_page.eval_on_selector.return_value = "Example Domain for illustration"

    with patch("your_module.async_playwright") as mock_async_playwright:
        mock_async_playwright.return_value.__aenter__.return_value = mock_browser
        mock_browser.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        mock_context.new_page.return_value = mock_page

        result = await seo_serv.get_page_info(url)

    assert result == expected_result
