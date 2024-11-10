import pytest
from project.treap import Treap

def test_set_and_get():
    treap = Treap()
    treap[10] = 'a'
    treap[20] = 'b'
    treap[5] = 'c'
    
    # Проверка вставленных значений
    assert treap[10] == 'a'
    assert treap[20] == 'b'
    assert treap[5] == 'c'

def test_update():
    treap = Treap()
    treap[10] = 'a'
    treap[10] = 'updated'
    
    # Проверка обновленного значения
    assert treap[10] == 'updated'

def test_delete():
    treap = Treap()
    treap[10] = 'a'
    del treap[10]
    
    # Проверка, что ключ удален
    with pytest.raises(KeyError):
        _ = treap[10]

def test_contains():
    treap = Treap()
    treap[15] = 'present'
    
    # Проверка наличия ключа
    assert 15 in treap
    assert 10 not in treap

def test_iter():
    treap = Treap()
    treap[10] = 'a'
    treap[20] = 'b'
    treap[5] = 'c'
    
    # Прямой обход
    assert list(treap) == [5, 10, 20]

def test_reversed_iter():
    treap = Treap()
    treap[10] = 'a'
    treap[20] = 'b'
    treap[5] = 'c'
    
    # Обратный обход
    assert list(reversed(treap)) == [20, 10, 5]

def test_len():
    treap = Treap()
    assert len(treap) == 0
    treap[10] = 'a'
    treap[20] = 'b'
    assert len(treap) == 2
    del treap[10]
    assert len(treap) == 1
