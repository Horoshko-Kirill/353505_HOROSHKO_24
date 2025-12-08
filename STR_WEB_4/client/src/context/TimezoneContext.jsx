import { createContext, useState } from "react";

export const TimezoneContext = createContext();

export const TimezoneProvider = ({ children }) => {
  const [useUTC, setUseUTC] = useState(false);

  const toggleTimezone = () => setUseUTC(prev => !prev);

  return (
    <TimezoneContext.Provider value={{ useUTC, toggleTimezone }}>
      {children}
    </TimezoneContext.Provider>
  );
};