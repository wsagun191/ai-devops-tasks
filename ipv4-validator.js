const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;

console.log(ipRegex.test("192.168.1.1"));   // true
console.log(ipRegex.test("255.255.255.255")); // true
console.log(ipRegex.test("256.100.10.1"));   // false (256 jest poza zakresem)
console.log(ipRegex.test("192.168.1"));       // false (brak czwartego oktetu)
