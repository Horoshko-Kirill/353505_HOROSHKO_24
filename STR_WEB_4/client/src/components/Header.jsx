import React, { useState, useEffect, useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { TimezoneContext } from "../context/TimezoneContext";
import "./css/Header.css";

const Header = ({ currentPage, setCurrentPage }) => {
  const { user, setUser } = useContext(AuthContext);
  const { timezone, toggleTimezone } = useContext(TimezoneContext);
  const navigate = useNavigate();

  const [time, setTime] = useState(() => {
    const saved = localStorage.getItem("currentTime");
    return saved ? new Date(saved) : new Date();
  });

  useEffect(() => {
    const interval = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    localStorage.setItem("currentTime", time);
  }, [time]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login");
  };

  return (
    <header>
      <div className="header-left">
        <Link to="/catalog">Каталог</Link>
        {user && <Link to="/admin">Админ-панель</Link>}
      </div>

      <div className="header-center">
        {user ? (
          <>
            <span>Привет, {user.name}!</span>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>

      <div className="header-right">
        <span>{time.toLocaleTimeString()}</span>
      </div>

      {user && (
        <nav>
          <Link to="/news-manager">Новости</Link>
          <Link to="/order-manager">Управление заказами</Link>
          <Link to="/recipe-book">База рецептов</Link>
        </nav>
      )}
    </header>
  );
};

export default Header;
