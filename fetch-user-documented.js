/**
 * Pobiera dane użytkownika z zewnętrznego API na podstawie jego identyfikatora.
 * 
 * @param {string|number} userId - Unikalny identyfikator użytkownika, którego dane mają zostać pobrane.
 * @returns {Promise<{name: string, email: string, lastLogin: Date}|null>} Zwraca obietnicę (Promise), która po pomyślnym zakończeniu resuelve'uje się do obiektu zawierającego zmapowane dane użytkownika, lub `null` w przypadku wystąpienia błędu.
 */
function fetchUserData(userId) {
  return fetch(`https://api.example.com/users/${userId}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      return {
        name: data.name,
        email: data.email,
        lastLogin: new Date(data.lastLoginTimestamp)
      };
    })
    .catch(error => {
      console.error('Fetch error:', error);
      return null;
    });
}
