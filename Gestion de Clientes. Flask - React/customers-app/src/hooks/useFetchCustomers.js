import React, { useEffect } from "react";
import { useState } from "react";
import { getAllCustomers } from "../helpers/getAllCustomers";

export const useFetchCustomers = (newCustomers) => {
  const [customers, setCustomers] = useState([]);

  const getCustomers = async () => {
    const customers = await getAllCustomers();
    setCustomers(customers);
  };

  useEffect(() => {
    getCustomers();
  }, [newCustomers]);

  return {
    customers,
  };
};
