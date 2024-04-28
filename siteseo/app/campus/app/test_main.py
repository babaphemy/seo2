import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
Base = declarative_base()
test_email = "babaphemy@yahoo.com"
# Setup an in-memory SQLite database for testing
@pytest.fixture(scope="module")
def test_engine():
    return create_engine("sqlite:///:memory:")

# Create a database session fixture
@pytest.fixture(scope="module")
def test_session(test_engine):
    Base.metadata.create_all(test_engine)  # Create tables
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    return SessionLocal()