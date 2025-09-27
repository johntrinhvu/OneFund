import { useEffect, useState } from "react";

export function useSession() {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";
    fetch(`${API_BASE}/me`, { credentials: "include" })
      .then(r => r.ok ? r.json() : null)
      .then(data => setUser(data || null))
      .finally(() => setReady(true));
  }, []);

  return { user, ready };
}

