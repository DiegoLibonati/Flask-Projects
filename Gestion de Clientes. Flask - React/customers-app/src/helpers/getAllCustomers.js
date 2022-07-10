export const getAllCustomers = async () => {
  const URL = "http://localhost:5000/api/customers";

  const resp = await fetch(URL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const customers = await resp.json();

  const customer = customers.map((customer) => ({
    id: customer.id,
    address: customer.address,
    email: customer.email,
    firstname: customer.firstname,
    lastname: customer.lastname,
    phone: customer.phone,
  }));

  return customer;
};
