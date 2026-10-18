const resultDiv = document.getElementById('result');
const tbody = document.querySelector('#table tbody');

async function loadRecords() {
    const res = await fetch('/api/records');
    const data = await res.json();
    tbody.innerHTML = '';
    data.forEach(r => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${r.id}</td>
            <td>${r.name}</td>
            <td>${r.gender === 'f' ? 'Ж' : 'М'}</td>
            <td>${r.age}</td>
            <td>${r.height}</td>
            <td>${r.weight}</td>
            <td>${r.bmi}</td>
            <td>${r.category}</td>
            <td>${r.calories}</td>
            <td>${r.created_at}</td>
            <td><button class="del" onclick="deleteRecord(${r.id})">Удалить</button></td>
        `;
        tbody.appendChild(tr);
    });
}

async function calculate() {
    const body = {
        name: document.getElementById('name').value,
        gender: document.getElementById('gender').value,
        age: document.getElementById('age').value,
        height: document.getElementById('height').value,
        weight: document.getElementById('weight').value,
        activity: document.getElementById('activity').value
    };

    const res = await fetch('/api/calc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });
    const data = await res.json();

    if (!res.ok) {
        resultDiv.innerHTML = `<p class="error">${data.error}</p>`;
        return;
    }

    resultDiv.innerHTML = `
        <p>ИМТ: <b>${data.bmi}</b> (${data.category})</p>
        <p>Базовый обмен веществ: ${data.bmr} ккал</p>
        <p>Суточная норма с учетом активности: <b>${data.calories} ккал</b></p>
    `;
    loadRecords();
}

async function deleteRecord(id) {
    await fetch('/api/records/' + id, { method: 'DELETE' });
    loadRecords();
}

document.getElementById('calcBtn').addEventListener('click', calculate);
document.getElementById('loadBtn').addEventListener('click', loadRecords);
