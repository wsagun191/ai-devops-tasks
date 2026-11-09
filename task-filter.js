/**
 * Filtruje, sortuje i wyciąga tytuły ukończonych zadań.
 * 
 * @param {Array<{id: number, title: string, status: string}>} tasks - Tablica zadań
 * @returns {string[]} Tablica z tytułami ukończonych zadań posortowana rosnąco po id
 */
function getCompletedTaskTitles(tasks) {
  return tasks
    .filter(task => task.status === 'completed') // 1. Filtrowanie: tylko status "completed"
    .sort((a, b) => a.id - b.id)                 // 2. Sortowanie: według id rosnąco
    .map(task => task.title);                    // 3. Mapowanie: zwracamy tylko tytuły
}
