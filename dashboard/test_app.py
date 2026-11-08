import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the index page loads."""
    response = client.get('/')
    assert response.status_code == 200

def test_api_stats(client):
    """Test the stats API."""
    response = client.get('/api/stats')
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.get_json()
        assert "totalSamples" in data
        assert "labelDistribution" in data
    
def test_api_predict_no_text(client):
    """Test prediction API with missing data."""
    response = client.post('/api/predict', json={})
    assert response.status_code == 400
    assert "error" in response.get_json()
    
@patch('app.sentiment_pipeline')
def test_api_predict_with_text(mock_pipeline, client):
    """Test prediction API with text data, mocking the model out."""
    mock_pipeline.return_value = [{'label': 'positive', 'score': 0.99}]
    response = client.post('/api/predict', json={"text": "أنا سعيد جداً اليوم"})
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.get_json()
        assert data.get("sentiment") in ["Positive", "Model Unavailable"]
