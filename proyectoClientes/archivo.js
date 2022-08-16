function AgregarCliente() {
  let htmlModal = document.getElementById("modal");
  htmlModal.setAttribute("class", "modale opened");

}

function editUserReturn(id) {
  let htmlModal = document.getElementById("modal");
  htmlModal.setAttribute("class", "modale opened");
  let htmlmodalFooter = document.getElementById("btn_ingresar");
  htmlmodalFooter.setAttribute("onclick", "editUser(" + id + ")");


}


function CerrarModal() {
  let htmlModal = document.getElementById("modal");
  htmlModal.setAttribute("class", "modale");

}

document.addEventListener("DOMContentLoaded", init())
function init() {
  search()
}

async function search() {
  let url = "http://127.0.0.1:3000/api/customers"
  const response = await fetch(url, { "method": 'GET', "headers": { "Content-Type": 'application/json' } })

  const request = await response.json()
  //console.log(request)

  var html = ''
  for (user of request) {
    var row = `
<tr>
<td>${user.firstname}</td>
<td>${user.lastname}</td>
<td>${user.email}</td>
<td>${user.phone}</td>
<td>
    <button onclick="deleteUser(${user.id})" class="Buttondel">Eliminar</button>
    <button onclick="editUserReturn(${user.id});" class="myButton">Editar</button>
</td>
</tr>`
    html += row
  }
  document.querySelector("#customers > tbody").outerHTML = html
}
async function deleteUser(id) {

  const respuesta = confirm("are you sure delete user ?")
  if (respuesta) {
    let url = "http://127.0.0.1:3000/api/customers/"
    await fetch(url + id, {
      "method": 'DELETE',
      "headers": { "Content-Type": 'application/json' }
    })

    alert("it was delete")

    window.location.reload()
  }
}


async function addUser() {
  //debugger
  //{request.json['firstname']}', '{request.json['lastname']}', '{request.json['email']}', '{request.json['phone']}', '{request.json['address']}', '{today}
  User = {
    "address": document.getElementById("txtAddress").value,
    "date_created": "",
    "email": document.getElementById("txtEmail").value,
    "firstname": document.getElementById("txtFirstname").value,
    "lastname": document.getElementById("txtLastname").value,
    "phone": document.getElementById("txtPhone").value
  }


  var url = "http://127.0.0.1:3000/api/customers"
  await fetch(url, {
    "method": 'POST',
    "body": JSON.stringify(User),
    "headers": { "Content-Type": 'application/json' }
  })

  window.location.reload()

}

async function editUser(id) {
  respuesta = confirm("are you sure edit user ?")

  if (respuesta) {

    User = {
      "address": document.getElementById("txtAddress").value,
      "date_created": "",
      "email": document.getElementById("txtEmail").value,
      "firstname": document.getElementById("txtFirstname").value,
      "id": id,
      "lastname": document.getElementById("txtLastname").value,
      "phone": document.getElementById("txtPhone").value
    }
    var url = "http://127.0.0.1:3000/api/customers"
    await fetch(url, {
      "method": 'POST',//the back-end await only POST for edit and add 
      "body": JSON.stringify(User),
      "headers": { "Content-Type": 'application/json' }
    })

    alert("it changed successfully")
    window.location.reload()
  }
}

