import { MainNav } from "@/components/MainNav";
import { navigationLinks } from "../config/navigationLinks";
import { UserNav } from "./CustomersPage/components/UserNav";
import { useState } from "react";

export const AddCustomerPage = () => {
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");

  const nameHandler = (event) => {
    setName(event.target.value);
  };

  const surnameHandler = (event) => {
    setSurname(event.target.value);
  };
  const emailHandler = (event) => {
    setEmail(event.target.value);
  };

  const submitDataHandler = async (e) => {
    e.preventDefault();
    if (name === "") return;
    if (email === "") return;

    const customerData = {
      name: name,
      surname: surname,
      email: email,
    };

    const response = fetch("http://127.0.0.1:8000/customers", {
      method: "POST",
      body: JSON.stringify(customerData),
      headers: {
        "Content-Type": "application/json",
      },
    });

    console.log(response);

    if (!response.ok) {
      setResMessage("incorrect data");
      throw new Error(response.message || "incorrect data");
    }

    setName("");
    setSurname("");
    setEmail("");
  };
  return (
    <div className="hidden flex-col md:flex">
      <div className="border-b">
        <div className="flex h-16 items-center px-4">
          <MainNav className="mx-6" links={navigationLinks} />
          <div className="ml-auto flex items-center space-x-4">
            <UserNav />
          </div>
        </div>
      </div>
      <div className="flex-1 space-y-4 p-8 pt-6">
        <div className="flex items-center justify-between space-y-2">
          <h2 className="text-3xl font-bold tracking-tight">Add customer</h2>
        </div>
        <div className="hidden h-full flex-1 flex-col space-y-8 md:flex"></div>
      </div>
      <form onSubmit={submitDataHandler} className="addCustomer">
        <input onChange={nameHandler} value={name} type="text" placeholder="Name"></input>
        <input onChange={surnameHandler} value={surname} type="text" placeholder="Surname"></input>
        <input onChange={emailHandler} value={email} type="text" placeholder="Email"></input>
        <button type="submit">Add</button>
      </form>
    </div>
  );
};
