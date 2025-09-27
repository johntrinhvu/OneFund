import onefund from "../../assets/OneFundLogo.png";
import googleLogo from "../../assets/googleLogo.png";
import appleLogo from "../../assets/appleLogo.png";
import SignInButton from "../../components/SignInButton/SignInButton";

export default function Landing() {
    const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000";
    return (
      <main className="min-h-screen text-slate-800">
        <div className="mx-auto flex min-h-screen max-w-5xl items-center justify-center px-6">
          <section className="w-full max-w-md rounded-3xl bg-white/80 shadow-xl ring-1 ring-black/5 backdrop-blur p-8">
            <div className="flex flex-col items-center text-center">
              <div className="-mb-12">
                <img
                  src={onefund}
                  alt="OneFund"
                  className="-mt-20 h-56"
                />
              </div>
  
              <h1 className="text-3xl font-semibold tracking-tight">
                Welcome to <span className="text-one-600">OneFund</span>
              </h1>
              <p className="mt-2 text-sm text-slate-500">
                Simple investing. One place.
              </p>
  
              <div className="mt-8 w-full space-y-3">
                <SignInButton 
                  name="Google" 
                  logo={googleLogo}
                  onClick={() => {
                    window.location.href = `${API_BASE}/auth/google/login`;
                  }}
                />

                <SignInButton 
                  name="Apple" 
                  logo={appleLogo}
                  onClick={() => {
                    console.log("Apple sign in clicked");
                  }}
                />
              </div>
  
              <p className="mt-6 text-xs text-slate-400">
                Created by John Vu
              </p>
            </div>
          </section>
        </div>
      </main>
    );
  };
  