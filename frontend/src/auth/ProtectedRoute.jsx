import { Navigate, Outlet } from "react-router-dom";
import { useSession } from "../hooks/useSession";

export default function ProtectedRoute() {
  const { user, ready } = useSession();
  if (!ready) return null;
  if (!user) return <Navigate to="/" replace />;
  return <Outlet />;
}

