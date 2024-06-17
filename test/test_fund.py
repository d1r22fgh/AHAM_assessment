
from app import schemas
import pytest


def test_get_all_fund(client, test_funds):
    assert len(test_funds) > 0

def test_get_one_fund_not_exist(client):
    response = client.get("/posts/89898")
    assert response.status_code == 404

def test_get_one_post(client, test_funds):
    response = client.get(f"/funds/2")
    fund = response.json()
    assert fund['fund_id'] == test_funds["2"]['fund_id']

@pytest.mark.parametrize(
    "fund_name, manager, performance", "nav", "description", "expected", 
    [
        ("Tesla", "Elon Mask", "70%", "70%", "", True),
        ("IBM", "Jensen Huang", "100%", "50%", "content", True),
        ("Amazon", "Jeff Bezos", "er", "50%", "", False)
    ]
    )
def create_fund(client, fund_name, manager, performance, nav, description):
    response = client.post(
        "/funds", json={
            "fund_name": fund_name,
            "manager": manager,
            "performance": performance,
            "nav": nav,
            "description": description
            })

    created_fund = response.json()
    assert response.status_code == 201
    assert created_fund['fund_name'] == fund_name
    assert created_fund['manager'] == manager
    assert created_fund['performance'] == performance
    assert created_fund['nav'] == nav
    assert created_fund['description'] == description

def test_delete_fund_success(client, test_funds):
    response = client.delete(
        f"/funds/{2}")

    assert response.status_code == 204