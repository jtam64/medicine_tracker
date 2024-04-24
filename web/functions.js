const getAll = () => {
    return fetch('http://medicine_tracker-medicine_store-1:8900/get_all')
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
                        <button onclick="toggleButton('modMedicineFormDiv${medicine.name}')">Change Medicine</button>
                        <div style="display:none;" id="modMedicineFormDiv${medicine.name}">
                            <form id="modMedicineForm">
                                <input type="hidden" name="id" id="id" value="${medicine.id}">
                                <input type="text" name="name" id="name" value="${medicine.name}">
                                <input type="number" name="quantity" id="quantity" value="${medicine.quantity}">
                                <input type="number" name="modifier" id="modifier" value="${medicine.modifier}">
                                <input type="submit" value="Submit" onclick="modMedicine()"></input>
                                <input type="submit" value="Cancel" onclick="cancel()"></input>
                        </div>
                        <button onclick="removeMedicine(${medicine.id})">Remove Medicine</button>`
        list.appendChild(div)
    })
}

const cancel = () => {
    window.location.reload();
}

const modMedicine = () => {
    const form = document.getElementById('modMedicineForm');
    const formData = new FormData(form);

    const formDataObject = {};

    formData.forEach((value, key) => {
        formDataObject[key] = !isNaN(value) ? Number(value) : value;
    });

    const data = JSON.stringify(formDataObject);

    fetch('http://medicine_tracker-medicine_store-1:8900/modify_medication', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: data,
        }
    )
}

const removeMedicine = (id) => {
    fetch('http://medicine_tracker-medicine_store-1:8900/remove_medication', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({id: Number(id)}),
        }
    )
    .then(response => response.json())
    .then(data => {
        console.log('Server Response', data);
        window.location.reload();
    })
    .catch(error => {
        console.log('Error sending data:', error);
    })
}

const toggleButton = (tag) => {
    const form = document.getElementById(tag)
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

    fetch('http://medicine_tracker-medicine_store-1:8900/add_medicine', {
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
    const interval = setInterval(() => {
        getAll()
    }, 5000);

    getAll()
}



document.addEventListener('DOMContentLoaded', setup)
