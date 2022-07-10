import React, { useState } from "react";
import { Row } from "./Row";
import { useFetchCustomers } from "../hooks/useFetchCustomers";

export const Main = () => {
  const [modal, setModal] = useState(false);
  const [edit, setEdit] = useState(false);

  const [firstnameValue, setFirstnameValue] = useState("");
  const [lastnameValue, setLastnameValue] = useState("");
  const [emailValue, setEmailValue] = useState("");
  const [phoneValue, setPhoneValue] = useState("");
  const [idValue, setIdValue] = useState("");
  const [addressValue, setAddressValue] = useState("");

  const [newCustomers, setNewCustomers] = useState([]);
  const { customers } = useFetchCustomers(newCustomers);

  const handleInputChangeFirstname = (e) => {
    setFirstnameValue(e.target.value);
  };

  const handleInputChangeLastname = (e) => {
    setLastnameValue(e.target.value);
  };
  const handleInputChangeEmail = (e) => {
    setEmailValue(e.target.value);
  };
  const handleInputChangePhone = (e) => {
    setPhoneValue(e.target.value);
  };
  const handleInputChangeId = (e) => {
    setIdValue(e.target.value);
  };
  const handleInputChangeAddress = (e) => {
    setAddressValue(e.target.value);
  };

  const handleSave = async (e) => {
    e.preventDefault();

    if (!edit) {
      const data = {
        address: addressValue,
        email: emailValue,
        firstname: firstnameValue,
        lastname: lastnameValue,
        phone: phoneValue,
      };

      const URL = "http://localhost:5000/api/customers";
      const result = await fetch(URL, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (result.ok) {
        setNewCustomers([...newCustomers, data]);
      }
    } else {
      const data = {
        id: idValue,
        address: addressValue,
        email: emailValue,
        firstname: firstnameValue,
        lastname: lastnameValue,
        phone: phoneValue,
      };

      console.log(data);

      const URL = "http://localhost:5000/api/customers";
      const result = await fetch(URL, {
        method: "PUT",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (result.ok) {
        setNewCustomers([...newCustomers, data]);
      }
    }

    setModal(false);
  };

  return (
    <>
      <main className="main_container">
        <section className="title_app_container">
          <article>
            <h1>Gestion de Clientes</h1>
          </article>
        </section>

        <section className="button_add_container">
          <article>
            <button onClick={() => setModal(true)}>Agregar</button>
          </article>
        </section>

        <section className="section_table_container">
          <table className="table_container">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Apellido</th>
                <th>Email</th>
                <th>Telefono</th>
                <th>Direccion</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {customers.map((customer) => (
                <Row
                  key={customer.id}
                  {...customer}
                  customers={customers}
                  setNewCustomers={setNewCustomers}
                  setModal={setModal}
                  setEdit={setEdit}
                  setAddressValue={setAddressValue}
                  setEmailValue={setEmailValue}
                  setIdValue={setIdValue}
                  setFirstnameValue={setFirstnameValue}
                  setLastnameValue={setLastnameValue}
                  setPhoneValue={setPhoneValue}
                ></Row>
              ))}
            </tbody>
          </table>
        </section>

        {modal ? (
          <section className="section_form_container">
            <form onSubmit={(e) => handleSave(e)}>
              <input
                type="text"
                id="txtId"
                value={idValue}
                onChange={handleInputChangeId}
                placeholder="id"
                size="20"
                disabled
              />
              <br />
              <input
                type="text"
                id="txtFirstName"
                placeholder="Nombre"
                size="20"
                value={firstnameValue}
                onChange={handleInputChangeFirstname}
              />
              <br />
              <input
                type="text"
                id="txtLastName"
                placeholder="Apellido"
                size="20"
                value={lastnameValue}
                onChange={handleInputChangeLastname}
              />
              <br />
              <input
                type="text"
                id="txtPhone"
                placeholder="Telefono"
                size="20"
                value={phoneValue}
                onChange={handleInputChangePhone}
              />
              <br />
              <input
                type="text"
                id="txtEmail"
                placeholder="Email"
                size="20"
                value={emailValue}
                onChange={handleInputChangeEmail}
              />
              <br />
              <input
                type="text"
                id="txtAddress"
                placeholder="Address"
                value={addressValue}
                onChange={handleInputChangeAddress}
                size="20"
              />
              <br />

              <button type="submit">Guardar</button>
            </form>
          </section>
        ) : (
          <></>
        )}
      </main>
    </>
  );
};
