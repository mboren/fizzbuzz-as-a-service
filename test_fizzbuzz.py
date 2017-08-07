import fizzbuzz as fb


def test_multiple_3_should_return_fizz():
    expected = "Fizz"
    actual = fb.fizzbuzz(7*3)
    assert expected == actual


def test_multiple_3_and_5_should_return_fizzbuzz():
    expected = "FizzBuzz"
    actual = fb.fizzbuzz(2*3*5)
    assert expected == actual


def test_multiple_5_should_return_buzz():
    expected = "Buzz"
    actual = fb.fizzbuzz(11*5)
    assert expected == actual


def test_not_multiple_3_or_5_should_return_input():
    expected = str(2)
    actual = fb.fizzbuzz(2)
    assert expected == actual
