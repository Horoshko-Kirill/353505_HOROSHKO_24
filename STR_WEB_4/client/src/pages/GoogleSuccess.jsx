import { useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";

const GoogleSuccess = () => {
  const navigate = useNavigate();
  const { setUser } = useContext(AuthContext);

  useEffect(() => {
  const params = new URLSearchParams(window.location.search);
  const token = params.get("token");

    if (token) {
      localStorage.setItem("token", token);

      axios.get("http://localhost:5000/api/auth/me", {
        headers: { Authorization: `Bearer ${token}` }
      })
      .then(res => {
        const userName = res.data.name;
        setUser({ token, name: userName, isAuth: true });
        localStorage.setItem("name", userName);
        navigate("/catalog");
      })
      .catch(() => navigate("/login"));
    } else {
      navigate("/login");
    }
  }, [navigate]);


  return <div>Вход через Google успешен… Перенаправление…</div>;
};

export default GoogleSuccess;
