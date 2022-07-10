import React from "react";

export const Row = ({
  id,
  firstname,
  lastname,
  email,
  phone,
  address,
  customers,
  setNewCustomers,
  setModal,
  setEdit,
  setIdValue,
  setFirstnameValue,
  setLastnameValue,
  setEmailValue,
  setPhoneValue,
  setAddressValue,
}) => {
  const handleEditCustomer = async (id) => {
    setModal(true);

    const customerToEdit = customers.find((x) => x.id === id);

    setIdValue(customerToEdit.id);
    setFirstnameValue(customerToEdit.firstname);
    setLastnameValue(customerToEdit.lastname);
    setEmailValue(customerToEdit.email);
    setPhoneValue(customerToEdit.phone);
    setAddressValue(customerToEdit.address);

    setEdit(true);
  };

  const handleRemoveCustomer = async (id) => {
    const res = window.confirm("¿Estas seguro de eliminarlo?");

    if (res) {
      const URL = "http://localhost:5000/api/customers/" + id;
      await fetch(URL, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      });
    }

    const newArray = customers.filter((customer) => customer.id !== id);

    setNewCustomers(newArray);
  };

  return (
    <>
      <tr>
        <td data-label="Nombre">{firstname}</td>
        <td data-label="Apellido">{lastname}</td>
        <td data-label="Email">{email}</td>
        <td data-label="Telefono">{phone}</td>
        <td data-label="Direccion">{address}</td>
        <td data-label="Acciones">
          <div>
            <button onClick={() => handleEditCustomer(id)}>Editar</button>
            <button onClick={() => handleRemoveCustomer(id)}>Eliminar</button>
          </div>
        </td>
      </tr>
    </>
  );
};
