import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";
import "@testing-library/jest-dom/extend-expect";

test("renders the header text", () => {
  render(<App />);
  const headerElement = screen.getByText(/David Lynch Daily Video/i);
});
