import { Routes, Route } from "react-router-dom";
import Landing from "../Landing/Landing";
import Dashboard from "../Dashboard/Dashboard";
import Onboarding from "../Onboarding/Onboarding";
import ProtectedRoute from "../../auth/ProtectedRoute";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/onboarding" element={<Onboarding />} />
      </Route>
    </Routes>
  );
};
