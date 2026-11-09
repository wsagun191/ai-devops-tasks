//opcja 1
function findPairsOptimized(arr, targetSum) {
  const pairs = [];
  const seen = new Set();
  const foundPairs = new Set(); // do unikania duplikatów, jeśli w tablicy są powtórzenia

  for (const num of arr) {
    const complement = targetSum - num;
    if (seen.has(complement)) {
      // Tworzymy unikalny klucz pary, aby uniknąć duplikatów w wyniku
      const pairKey = [num, complement].sort((a, b) => a - b).join(',');
      if (!foundPairs.has(pairKey)) {
        foundPairs.add(pairKey);
        pairs.push([complement, num]);
      }
    }
    seen.add(num);
  }
  return pairs;
}

//opcja 2
function findPairsTwoPointers(arr, targetSum) {
  // Kopia i sortowanie tablicy: O(n log n)
  const sorted = [...arr].sort((a, b) => a - b);
  const pairs = [];
  
  let left = 0;
  let right = sorted.length - 1;

  while (left < right) {
    const sum = sorted[left] + sorted[right];

    if (sum === targetSum) {
      pairs.push([sorted[left], sorted[right]]);
      
      // Pomijanie duplikatów dla lewego wskaźnika
      while (left < right && sorted[left] === sorted[left + 1]) left++;
      // Pomijanie duplikatów dla prawego wskaźnika
      while (left < right && sorted[right] === sorted[right - 1]) right--;
      
      left++;
      right--;
    } else if (sum < targetSum) {
      left++;
    } else {
      right--;
    }
  }

  return pairs;
}
