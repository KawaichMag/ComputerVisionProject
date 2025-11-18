import {createContext, useState, useContext, useEffect } from 'react'


type ThemeContextType = {
  theme: string;
  toggleTheme: React.Dispatch<React.SetStateAction<string>>;
};

export const ThemeContext = createContext<ThemeContextType>({
  theme: "light",
  toggleTheme: () => {},
});

type ThemeProviderProps = {
  children: React.ReactNode;
};

export default function ThemeProvider( { children }: ThemeProviderProps ) {
    const [theme, setTheme] = useState("dark");

    useEffect(() => {
      document.documentElement.setAttribute("data-theme", theme);
    }, [theme]);
    
    const toggleTheme = () => setTheme(prev => (prev === 'light' ? 'dark' : 'light'));

    return (
        <ThemeContext value={{theme, toggleTheme}}>
            {children}
        </ThemeContext>
    )
}

export const useTheme = () => useContext(ThemeContext)