// Generic add/update
function saveToStore(storeName, dataArray) {
    const tx = db.transaction(storeName, 'readwrite');
    const store = tx.objectStore(storeName);
    dataArray.forEach(data => store.put(data));
}

// Generic get all
function getAllFromStore(storeName, callback) {
    const tx = db.transaction(storeName, 'readonly');
    const store = tx.objectStore(storeName);
    const request = store.getAll();

    request.onsuccess = () => {
        callback(request.result);
    };
}
