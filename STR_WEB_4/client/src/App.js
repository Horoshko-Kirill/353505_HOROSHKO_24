import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import CatalogPage from "./pages/CatalogPage";
import GoogleSuccess from "./pages/GoogleSuccess";
import PrivateRoute from "./components/PrivateRoute";
import AdminPage from "./pages/AdminPage.jsx"; 
import Header from "./components/Header";
import CakeDetails from "./pages/CakeDetails";
import { TimezoneProvider } from "./context/TimezoneContext";
import OrderManager from "./components/OrderManager";
import RecipeBook from "./components/RecipeBook";
import NewsManager from "./components/NewsManager";
import "./components/css/variables.css";

function App() {
  return (
    <TimezoneProvider>
    <Router>
      <Header />
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/google-success" element={<GoogleSuccess />} />
        <Route path="/catalog" element={<CatalogPage />} />
        <Route path="/cakes/:id" element={<CakeDetails />} />
        <Route
          path="/admin"
          element={
            <PrivateRoute>
              <AdminPage />
            </PrivateRoute>
          }
        />
        <Route
            path="/news-manager"
            element={
              <PrivateRoute>
                <NewsManager />
              </PrivateRoute>
            }
          />
           <Route
            path="/order-manager"
            element={
              <PrivateRoute>
                <OrderManager />
              </PrivateRoute>
            }
          />
          <Route
            path="/recipe-book"
            element={
              <PrivateRoute>
                <RecipeBook />
              </PrivateRoute>
            }
          />
      </Routes>
    </Router>
    </TimezoneProvider>
  );
}

export default App;
