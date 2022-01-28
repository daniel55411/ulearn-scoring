from ulearn_scoring._modules import ModulesIndex


def test_modules_index():
    index = ModulesIndex(['module1', 'module2'])

    assert 'module1' in index
    assert 'module2' in index
    assert 'module3' not in index


def test_modules_index__all_modules():
    index = ModulesIndex('*')

    assert 'any1' in index
    assert 'any2' in index
    assert 'any3' in index
