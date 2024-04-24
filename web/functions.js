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

const addMedicineButton = () => {
    const form = document.getElementById('addMedicine')
    if (form.style.display === "none") {
        form.style.display = "block"
    } else {
        form.style.display = "none"
    }
}

const addMedicine = () => {
    const form = document.getElementById('medicineForm');
    const formData = new FormData(form);

    const formDataObject = {};

    formData.forEach((value, key) => {
        formDataObject[key] = !isNaN(value) ? Number(value) : value;
    });

    const data = JSON.stringify(formDataObject);
    console.log(data)

    fetch('http://localhost:8900/add_medicine', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: data,
        }
    )
    .then(response => response.json())
    .then(data => {
        console.log('Server Response', data);
    })
    .catch(error => {
        console.log('Error sending data:', error);
    })
}

const setup = () => {
    // const interval = setInterval(() => {
    //     getAll()
    // }, 5000);

    getAll()
}



document.addEventListener('DOMContentLoaded', setup)
