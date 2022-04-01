from todo_app.models.Item import Item
from todo_app.models.ViewModel import ViewModel
import pytest

@pytest.fixture
def viewModel() -> ViewModel:
    items = [Item(1, 'Not started item', 'Not Started'), Item(2, 'In progress item', 'In Progress'), Item(3, 'Done item', 'Done')]
    return ViewModel(items)

def test_can_get_all_items_from_model(viewModel: ViewModel):
    allItems = viewModel.items
    assert len(allItems) == 3

def test_can_get_only_todo_items_from_model(viewModel: ViewModel):
    notStartedItems = viewModel.to_do_items
    assert len(notStartedItems) == 1
    assert notStartedItems[0].status == 'Not Started'

def test_can_get_only_in_progress_items_from_model(viewModel: ViewModel):
    inProgressItems = viewModel.in_progress_items
    assert len(inProgressItems) == 1
    assert inProgressItems[0].status == 'In Progress'

def test_can_get_only_done_items_from_modelo(viewModel: ViewModel):
    doneItems = viewModel.completed_items
    assert len(doneItems) == 1
    assert doneItems[0].status == 'Done'