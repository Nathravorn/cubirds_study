import pytest

from stack import Stack, get_deck

def test_stack_example():
    stack = Stack(['cube', 'cube'])
    assert stack.l == ['cube', 'cube']
    assert len(stack) == 2

    stack['sandwich'] += 1
    assert sorted(stack.l) == ['cube', 'cube', 'sandwich']

    stack += ['cube', 'sparrow']
    assert sorted(stack.l) == ['cube', 'cube', 'cube', 'sandwich', 'sparrow']
    assert len(stack) == 5

    stack -= ['sparrow']
    assert sorted(stack.l) == ['cube', 'cube', 'cube', 'sandwich']

    with pytest.raises(Exception):
        stack -= ['sparrow']

    # TODO: strange. should raise exception ?
    stack['sparrow'] -= 1
    assert sorted(stack.l) == ['cube', 'cube', 'cube', 'sandwich']

    stack.draw_all('cube')
    assert stack.l == ['sandwich']


def draw_one_by_one(stack):
    for _ in range(len(stack)):
        stack.draw()

def test_pref_draw_deck(benchmark):
    deck = get_deck()
    benchmark(draw_one_by_one, deck)
