from unittest.mock import patch, Mock
from etl.extract import get_station_info

@patch('etl.extract.requests.get')
def test_get_station_info(mock_get):
    # Mock the API response so we don't hit the real internet
    mock_response = Mock()
    mock_response.json.return_value = {"items": [{"label": "HIPPER_PARK"}]}
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = get_station_info("E64999A")
    
    # Verify the results and that our code called the API correctly
    assert result["label"] == "HIPPER_PARK"
    mock_get.assert_called_once()
    assert "E64999A" in mock_get.call_args[0][0]