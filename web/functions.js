const getAll = () => {
    return fetch('http://localhost:8900/get_all')
        .then(response => response.json())
        .then(data => renderHTML(data))
}

const renderHTML = (data) => {
    const list = document.getElementById('medicine')
    list.innerHTML = ''
    data.forEach(medicine => {
        const div = document.createElement('div')
        div.setAttribute('class', 'item')
        div.innerHTML = `<h3>${medicine.name.toUpperCase()}</h3>
                        <p>Quantity= ${medicine.quantity}</p>
                        <p>Remaining Days=${medicine.remaining_days}</p>
                        <p>Modifier=${medicine.modifier}</p>
                        <p>End Date=${medicine.end_date}</p>
                        <button onclick="modMedicine(${medicine.id})">Change Medicine</button>
                        <button onclick="removeMedicine(${medicine.id})">Remove Medicine</button>`
        list.appendChild(div)
    })
}

const setup = () => {
    // const interval = setInterval(() => {
    //     getAll()
    // }, 5000);

    getAll()
}

document.addEventListener('DOMContentLoaded', setup)
