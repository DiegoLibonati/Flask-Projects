import { useState } from "react";

export const useHide = () => {
  const [hide, setHide] = useState(false);

  const handleHide = () => {
    if (hide) {
      setHide(false);
    } else {
      setHide(true);
    }
  };

  return {
    hide,
    handleHide,
  };
};
