document.addEventListener("DOMContentLoaded", () => {
    const userId = "{{ current_user.id }}";

    // Sync courses
    fetch(`/api/user/${userId}/courses`)
        .then(res => res.json())
        .then(data => {
            saveToStore('courses', data);
            displayCourses(data);
        }).catch(() => {
            getAllFromStore('courses', displayCourses);
        });

    // Sync quizzes
    fetch(`/api/user/${userId}/quizzes`)
        .then(res => res.json())
        .then(data => {
            saveToStore('quizzes', data);
            displayQuizzes(data);
        }).catch(() => {
            getAllFromStore('quizzes', displayQuizzes);
        });

    // Sync notes
    fetch(`/api/user/${userId}/notes`)
        .then(res => res.json())
        .then(data => {
            saveToStore('notes', data);
            displayNotes(data);
        }).catch(() => {
            getAllFromStore('notes', displayNotes);
        });
});


function displayCourses(courses) {
    const section = document.getElementById('courses');
    section.innerHTML = courses.map(c => `<li>${c.name}</li>`).join('');
}

function displayQuizzes(quizzes) {
    const section = document.getElementById('quizzes');
    section.innerHTML = quizzes.map(q => `<li>${q.title} - Score: ${q.score}</li>`).join('');
}

function displayNotes(notes) {
    const section = document.getElementById('notes');
    section.innerHTML = notes.map(n => `<li>${n.title}: ${n.content}</li>`).join('');
}
