export default function SignInButton({ name, logo, onClick }) {
    return (
      <button
        onClick={onClick}
        className="inline-flex w-full items-center justify-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 text-sm font-medium text-slate-700 shadow-sm transition-colors hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-one-500 focus:ring-offset-2"
      >
        <span className="inline-flex h-5 w-5 shrink-0 items-center justify-center">
            <img
                src={logo}
                alt={`${name} logo`}
                className="block h-full w-full object-contain"
            />
        </span>
  
        <span className="leading-none">Continue with {name}</span>
      </button>
    );
  }
  