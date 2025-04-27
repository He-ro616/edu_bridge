let db;

const dbName = 'EduDB';
const version = 1;

const request = indexedDB.open(dbName, version);

request.onerror = (event) => {
    console.error('Database error:', event.target.error);
};

request.onsuccess = (event) => {
    db = event.target.result;
    console.log('IndexedDB initialized');
};

request.onupgradeneeded = (event) => {
    db = event.target.result;

    if (!db.objectStoreNames.contains('courses')) {
        db.createObjectStore('courses', { keyPath: 'id' });
    }
    if (!db.objectStoreNames.contains('quizzes')) {
        db.createObjectStore('quizzes', { keyPath: 'id' });
    }
    if (!db.objectStoreNames.contains('notes')) {
        db.createObjectStore('notes', { keyPath: 'id' });
    }
    if (!db.objectStoreNames.contains('video')) {
        db.createObjectStore('video', { keyPath: 'id' });
    }
};
