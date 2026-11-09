const sum = require('./sum');

test('poprawnie dodaje dwie liczby (1 + 2 = 3)', () => {
  expect(sum(1, 2)).toBe(3);
});

test('poprawnie obsługuje liczby ujemne (-1 + -2 = -3)', () => {
  expect(sum(-1, -2)).toBe(-3);
});
